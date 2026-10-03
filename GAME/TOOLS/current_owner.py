"""Operation-scoped reads over admitted HOT and exact native campaign owners."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType

from .hot_store import HotOwnerReadSnapshot, HotOwnerStorePort, OwnerDocument
from .live_state import (
    LIVE_NATIVE_STATE_PACK_SCHEMA_VERSION,
    LiveEnvelope,
    LiveNativeStatePack,
    LiveRouting,
    WriteAuthority,
    lookup_write_authority,
    select_live_source,
)
from .native_storage import (
    IdentityMismatch,
    NativeStorageError,
    route_native_record,
    validate_loaded_identity,
)
from .policy_basis import PinnedCampaign


class CurrentOwnerError(ValueError):
    """A bounded current-owner read cannot be established or retained."""


class CurrentOwnerStatus(StrEnum):
    RESOLVED = "RESOLVED"
    ABSENT = "ABSENT"
    INCOMPATIBLE = "INCOMPATIBLE"
    UNAVAILABLE = "UNAVAILABLE"
    REVALIDATION_REQUIRED = "REVALIDATION_REQUIRED"


class CurrentOwnerSource(StrEnum):
    SELECTED_LIVE = "SELECTED_LIVE"
    ACCEPTED_HOT = "ACCEPTED_HOT"
    PINNED_CAMPAIGN = "PINNED_CAMPAIGN"


@dataclass(frozen=True, slots=True)
class NativeOwnerRef:
    """One exact family/identity routed under WP-11."""

    family_key: str
    identity: tuple[str, ...]

    def __post_init__(self) -> None:
        identity = tuple(self.identity)
        route_native_record(self.family_key, identity)
        object.__setattr__(self, "identity", identity)


@dataclass(frozen=True, slots=True)
class CurrentOwnerRead:
    """One exact owner result and the source basis that supplied it."""

    owner_ref: NativeOwnerRef
    status: CurrentOwnerStatus
    source: CurrentOwnerSource
    source_basis: str | None
    generation: int | None
    fingerprint: str | None
    _payload_bytes: bytes | None = field(repr=False)
    predecessor_fingerprint: str | None = None

    def __init__(
        self,
        owner_ref: NativeOwnerRef,
        status: CurrentOwnerStatus,
        source: CurrentOwnerSource,
        source_basis: str | None,
        generation: int | None,
        fingerprint: str | None,
        payload: Mapping[str, object] | None,
        predecessor_fingerprint: str | None = None,
    ) -> None:
        object.__setattr__(self, "owner_ref", owner_ref)
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "source_basis", source_basis)
        object.__setattr__(self, "generation", generation)
        object.__setattr__(self, "fingerprint", fingerprint)
        object.__setattr__(
            self,
            "_payload_bytes",
            (
                json.dumps(
                    dict(payload),
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=False,
                    allow_nan=False,
                ).encode("utf-8")
                if payload is not None
                else None
            ),
        )
        object.__setattr__(self, "predecessor_fingerprint", predecessor_fingerprint)

    @property
    def payload(self) -> Mapping[str, object] | None:
        """Return an isolated copy so nested mutation cannot change retained evidence."""

        if self._payload_bytes is None:
            return None
        payload = json.loads(self._payload_bytes)
        if not isinstance(payload, dict):
            raise CurrentOwnerError("retained current-owner payload is malformed")
        return payload


@dataclass(frozen=True, slots=True)
class CurrentOwnerObservation:
    """A closed observation over the complete finite key union requested so far."""

    operation_token: object
    key_union: tuple[NativeOwnerRef, ...]
    reads: Mapping[NativeOwnerRef, CurrentOwnerRead]
    observation_fingerprint: str
    _hot_snapshot: HotOwnerReadSnapshot

    def require(self, owner_ref: NativeOwnerRef) -> CurrentOwnerRead:
        try:
            return self.reads[owner_ref]
        except KeyError as exc:
            raise CurrentOwnerError(
                "owner ref was not included in the observation"
            ) from exc


class CurrentOwnerReadSession:
    """Reacquire the full accumulated owner union for every bounded expansion."""

    __slots__ = (
        "_campaign_id",
        "_hot_store",
        "_last_observation",
        "_live_reader",
        "_operation_token",
        "_pinned_campaign",
        "_reader",
        "_requested",
        "_selected_live",
        "_source_basis_reader",
    )

    def __init__(
        self,
        *,
        campaign_id: str,
        operation_token: object,
        pinned_campaign: PinnedCampaign,
        selected_live: LiveRouting | None,
        hot_store: HotOwnerStorePort,
        reader: Callable[[PinnedCampaign, str], object],
        source_basis_reader: Callable[
            [PinnedCampaign], tuple[PinnedCampaign, LiveRouting | None]
        ],
        live_reader: Callable[[LiveRouting, LiveEnvelope], object] | None = None,
    ) -> None:
        if not campaign_id or pinned_campaign.campaign_id != campaign_id:
            raise CurrentOwnerError("current-owner session campaign is not exact")
        self._campaign_id = campaign_id
        self._operation_token = operation_token
        self._pinned_campaign = pinned_campaign
        self._selected_live = selected_live
        self._hot_store = hot_store
        self._reader = reader
        self._source_basis_reader = source_basis_reader
        self._live_reader = live_reader
        self._requested: dict[tuple[str, tuple[str, ...]], NativeOwnerRef] = {}
        self._last_observation: CurrentOwnerObservation | None = None

    @property
    def operation_token(self) -> object:
        return self._operation_token

    @property
    def observation(self) -> CurrentOwnerObservation | None:
        return self._last_observation

    def require(
        self, owner_keys: tuple[NativeOwnerRef, ...]
    ) -> CurrentOwnerObservation:
        if not isinstance(owner_keys, tuple):
            raise CurrentOwnerError("owner keys must be a finite tuple")
        if not owner_keys:
            raise CurrentOwnerError("at least one exact owner key is required")
        for owner_ref in owner_keys:
            if not isinstance(owner_ref, NativeOwnerRef):
                raise CurrentOwnerError("owner key must be a NativeOwnerRef")
            key = (owner_ref.family_key, owner_ref.identity)
            self._requested[key] = owner_ref

        key_union = tuple(self._requested[key] for key in sorted(self._requested))
        snapshot = self._hot_store.read_admitted_snapshot(
            self._campaign_id,
            tuple((ref.family_key, ref.identity) for ref in key_union),
        )
        reads: dict[NativeOwnerRef, CurrentOwnerRead] = {}
        for owner_ref in key_union:
            key = (owner_ref.family_key, owner_ref.identity)
            live_source = _selected_live_source(self._selected_live, owner_ref)
            if live_source is not None:
                reads[owner_ref] = self._read_selected_live(owner_ref, live_source)
                continue
            document = snapshot.rows.get(key)
            if document is not None:
                reads[owner_ref] = _hot_read(
                    owner_ref,
                    document,
                    snapshot,
                    pinned_campaign=self._pinned_campaign,
                    reader=self._reader,
                )
                continue
            if _selected_live_owns(self._selected_live, owner_ref):
                reads[owner_ref] = CurrentOwnerRead(
                    owner_ref=owner_ref,
                    status=CurrentOwnerStatus.REVALIDATION_REQUIRED,
                    source=CurrentOwnerSource.SELECTED_LIVE,
                    source_basis=self._pinned_campaign.revision,
                    generation=None,
                    fingerprint=None,
                    payload=None,
                )
                continue

            reads[owner_ref] = self._read_pinned(owner_ref)

        fingerprint = _observation_fingerprint(reads, snapshot.snapshot_fingerprint)
        observation = CurrentOwnerObservation(
            operation_token=self._operation_token,
            key_union=key_union,
            reads=MappingProxyType(reads),
            observation_fingerprint=fingerprint,
            _hot_snapshot=snapshot,
        )
        self._last_observation = observation
        return observation

    def read(self, owner_ref: NativeOwnerRef) -> CurrentOwnerRead:
        return self.require((owner_ref,)).require(owner_ref)

    def revalidate(self, observation: CurrentOwnerObservation | None = None) -> bool:
        candidate = self._last_observation if observation is None else observation
        if (
            candidate is None
            or candidate.operation_token is not self._operation_token
            or self._last_observation is not candidate
        ):
            return False

        try:
            fresh_pinned_campaign, fresh_selected_live = self._source_basis_reader(
                self._pinned_campaign
            )
        except (AttributeError, KeyError, OSError, TypeError, ValueError):
            return False
        if fresh_pinned_campaign.campaign_id != self._campaign_id:
            return False

        fresh_snapshot = self._hot_store.read_admitted_snapshot(
            self._campaign_id,
            tuple((ref.family_key, ref.identity) for ref in candidate.key_union),
        )
        if (
            fresh_snapshot.snapshot_fingerprint
            != candidate._hot_snapshot.snapshot_fingerprint
        ):
            return False
        fresh_reads: dict[NativeOwnerRef, CurrentOwnerRead] = {}
        for owner_ref, prior_read in candidate.reads.items():
            live_source = _selected_live_source(fresh_selected_live, owner_ref)
            if prior_read.source is CurrentOwnerSource.SELECTED_LIVE:
                if live_source is None:
                    return False
                current_read = self._read_selected_live(
                    owner_ref, live_source, selected_live=fresh_selected_live
                )
            else:
                if _selected_live_owns(fresh_selected_live, owner_ref):
                    return False
                key = (owner_ref.family_key, owner_ref.identity)
                document = fresh_snapshot.rows.get(key)
                if prior_read.source is CurrentOwnerSource.ACCEPTED_HOT:
                    if document is None:
                        return False
                    current_read = _hot_read(
                        owner_ref,
                        document,
                        fresh_snapshot,
                        pinned_campaign=fresh_pinned_campaign,
                        reader=self._reader,
                    )
                else:
                    if document is not None:
                        return False
                    current_read = self._read_pinned(
                        owner_ref, pinned_campaign=fresh_pinned_campaign
                    )
            fresh_reads[owner_ref] = current_read
            if _read_basis(current_read) != _read_basis(prior_read):
                return False

        return (
            _observation_fingerprint(fresh_reads, fresh_snapshot.snapshot_fingerprint)
            == candidate.observation_fingerprint
        )

    def _read_pinned(
        self,
        owner_ref: NativeOwnerRef,
        *,
        pinned_campaign: PinnedCampaign | None = None,
    ) -> CurrentOwnerRead:
        source = self._pinned_campaign if pinned_campaign is None else pinned_campaign
        route = route_native_record(owner_ref.family_key, owner_ref.identity)
        try:
            raw = self._reader(source, route.relative_path)
        except KeyError:
            return CurrentOwnerRead(
                owner_ref,
                CurrentOwnerStatus.ABSENT,
                CurrentOwnerSource.PINNED_CAMPAIGN,
                source.revision,
                None,
                None,
                None,
            )
        except (OSError, TypeError, ValueError, NativeStorageError):
            return CurrentOwnerRead(
                owner_ref,
                CurrentOwnerStatus.UNAVAILABLE,
                CurrentOwnerSource.PINNED_CAMPAIGN,
                source.revision,
                None,
                None,
                None,
            )
        if not isinstance(raw, Mapping):
            return CurrentOwnerRead(
                owner_ref,
                CurrentOwnerStatus.INCOMPATIBLE,
                CurrentOwnerSource.PINNED_CAMPAIGN,
                source.revision,
                None,
                None,
                None,
            )
        payload = deepcopy(dict(raw))
        try:
            _validate_owner_identity(owner_ref, payload)
            _validate_current_payload(owner_ref, payload)
            fingerprint = _payload_fingerprint(
                owner_ref, payload, source.revision, None
            )
        except (NativeStorageError, TypeError, ValueError):
            return CurrentOwnerRead(
                owner_ref,
                CurrentOwnerStatus.INCOMPATIBLE,
                CurrentOwnerSource.PINNED_CAMPAIGN,
                source.revision,
                None,
                None,
                None,
            )
        generation = payload.get("state_revision")
        return CurrentOwnerRead(
            owner_ref,
            CurrentOwnerStatus.RESOLVED,
            CurrentOwnerSource.PINNED_CAMPAIGN,
            source.revision,
            generation if type(generation) is int else None,
            fingerprint,
            MappingProxyType(payload),
            _actor_source_fingerprint(owner_ref, payload)
            if owner_ref.family_key == "world.actor"
            else None,
        )

    def _read_selected_live(
        self,
        owner_ref: NativeOwnerRef,
        source: LiveEnvelope,
        *,
        selected_live: LiveRouting | None = None,
    ) -> CurrentOwnerRead:
        routing = self._selected_live if selected_live is None else selected_live
        if routing is None or self._live_reader is None:
            return CurrentOwnerRead(
                owner_ref,
                CurrentOwnerStatus.UNAVAILABLE,
                CurrentOwnerSource.SELECTED_LIVE,
                None,
                None,
                None,
                None,
            )
        try:
            raw_pack = self._live_reader(routing, source)
            pack = _validate_live_pack(raw_pack, source)
            raw_owner = pack.native_owner_states.get(owner_ref.family_key)
            if not isinstance(raw_owner, Mapping):
                raise CurrentOwnerError("selected LIVE pack has no exact owner payload")
            payload = deepcopy(dict(raw_owner))
            _validate_owner_identity(owner_ref, payload)
            _validate_current_payload(owner_ref, payload)
            source_basis = f"{source.source_ref}@{source.source_revision}"
            fingerprint = _payload_fingerprint(owner_ref, payload, source_basis, None)
            generation = payload.get("state_revision")
            return CurrentOwnerRead(
                owner_ref,
                CurrentOwnerStatus.RESOLVED,
                CurrentOwnerSource.SELECTED_LIVE,
                source_basis,
                generation if type(generation) is int else None,
                fingerprint,
                MappingProxyType(payload),
            )
        except (
            AttributeError,
            KeyError,
            OSError,
            TypeError,
            ValueError,
            NativeStorageError,
        ):
            return CurrentOwnerRead(
                owner_ref,
                CurrentOwnerStatus.UNAVAILABLE,
                CurrentOwnerSource.SELECTED_LIVE,
                f"{source.source_ref}@{source.source_revision}",
                None,
                None,
                None,
            )


def _hot_read(
    owner_ref: NativeOwnerRef,
    document: OwnerDocument,
    snapshot: HotOwnerReadSnapshot,
    *,
    pinned_campaign: PinnedCampaign,
    reader: Callable[[PinnedCampaign, str], object],
) -> CurrentOwnerRead:
    payload = deepcopy(dict(document.payload))
    key = (owner_ref.family_key, owner_ref.identity)
    admission_basis = snapshot.admission_bases.get(key)
    effective_source_basis = document.source_basis
    predecessor_fingerprint = (
        admission_basis.source_fingerprint if admission_basis is not None else None
    )
    try:
        _validate_owner_identity(owner_ref, payload)
        _validate_current_payload(owner_ref, payload)
        if owner_ref.family_key == "world.actor":
            if (
                admission_basis is None
                or document.source_basis != admission_basis.source_revision
            ):
                raise CurrentOwnerError(
                    "accepted HOT Actor source basis is incompatible"
                )
            if admission_basis.source_revision != pinned_campaign.revision:
                route = route_native_record(owner_ref.family_key, owner_ref.identity)
                try:
                    source_payload = reader(pinned_campaign, route.relative_path)
                except (KeyError, OSError, TypeError, ValueError):
                    return CurrentOwnerRead(
                        owner_ref,
                        CurrentOwnerStatus.REVALIDATION_REQUIRED,
                        CurrentOwnerSource.ACCEPTED_HOT,
                        document.source_basis,
                        document.generation,
                        snapshot.row_fingerprints.get(key),
                        None,
                    )
                if not isinstance(source_payload, Mapping):
                    raise CurrentOwnerError(
                        "current campaign Actor predecessor is unavailable"
                    )
                current_source = deepcopy(dict(source_payload))
                _validate_owner_identity(owner_ref, current_source)
                _validate_current_payload(owner_ref, current_source)
                current_source_fingerprint = _actor_source_fingerprint(
                    owner_ref, current_source
                )
                current_hot_fingerprint = _actor_source_fingerprint(owner_ref, payload)
                if current_source_fingerprint not in {
                    admission_basis.source_fingerprint,
                    current_hot_fingerprint,
                }:
                    return CurrentOwnerRead(
                        owner_ref,
                        CurrentOwnerStatus.REVALIDATION_REQUIRED,
                        CurrentOwnerSource.ACCEPTED_HOT,
                        document.source_basis,
                        document.generation,
                        snapshot.row_fingerprints.get(key),
                        None,
                    )
                # Re-anchor only the transient read basis after proving the exact
                # current campaign Actor equals either the original predecessor
                # or the complete admitted HOT after-image. No semantic row write
                # is performed by this read path.
                effective_source_basis = pinned_campaign.revision
                predecessor_fingerprint = current_source_fingerprint
    except (NativeStorageError, TypeError, ValueError):
        return CurrentOwnerRead(
            owner_ref,
            CurrentOwnerStatus.INCOMPATIBLE,
            CurrentOwnerSource.ACCEPTED_HOT,
            document.source_basis,
            document.generation,
            snapshot.row_fingerprints.get(key),
            None,
        )
    return CurrentOwnerRead(
        owner_ref,
        CurrentOwnerStatus.RESOLVED,
        CurrentOwnerSource.ACCEPTED_HOT,
        effective_source_basis,
        document.generation,
        snapshot.row_fingerprints[key],
        MappingProxyType(payload),
        predecessor_fingerprint,
    )


def _validate_current_payload(
    owner_ref: NativeOwnerRef, payload: Mapping[str, object]
) -> None:
    if owner_ref.family_key != "world.actor":
        return
    if set(payload) - {
        "schema_version",
        "id",
        "kind",
        "definition_id",
        "state_revision",
        "state",
    } or not {"schema_version", "id", "kind", "state_revision", "state"}.issubset(
        payload
    ):
        raise CurrentOwnerError("native Actor envelope is not the strict current shape")
    from .actor_continuity import validate_actor_source

    if (
        type(payload.get("schema_version")) is not int
        or payload.get("schema_version") != 2
    ):
        raise CurrentOwnerError(
            "native Actor schema version is not the admitted current shape"
        )
    validate_actor_source(payload)


def _actor_source_fingerprint(
    owner_ref: NativeOwnerRef, source_payload: Mapping[str, object]
) -> str:
    encoded = json.dumps(
        {
            "family_key": owner_ref.family_key,
            "identity": owner_ref.identity,
            "payload": source_payload,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validate_owner_identity(
    owner_ref: NativeOwnerRef, payload: Mapping[str, object]
) -> None:
    if owner_ref.family_key == "runtime.collaboration_obligation":
        if (
            len(owner_ref.identity) != 1
            or payload.get("kind") != owner_ref.family_key
            or payload.get("obligation_id") != owner_ref.identity[0]
        ):
            raise IdentityMismatch(
                "collaboration obligation does not match its exact owner route"
            )
        return
    validate_loaded_identity(owner_ref.family_key, owner_ref.identity, payload)


def _selected_live_owns(
    selected_live: LiveRouting | None, owner_ref: NativeOwnerRef
) -> bool:
    if selected_live is None:
        return False
    try:
        authority = lookup_write_authority(
            owner_ref.family_key, owner_ref.identity[0], selected_live
        )
    except (TypeError, ValueError):
        return True
    return authority in {WriteAuthority.LIVE, WriteAuthority.INTEGRITY_CONFLICT}


def _selected_live_source(
    selected_live: LiveRouting | None, owner_ref: NativeOwnerRef
) -> LiveEnvelope | None:
    if selected_live is None:
        return None
    matches = tuple(
        source
        for source in selected_live.entries
        if source.claims_contain(owner_ref.family_key, owner_ref.identity[0])
    )
    if len(matches) != 1:
        return None
    return select_live_source(selected_live, matches[0].source_key)


def _validate_live_pack(value: object, source: LiveEnvelope) -> LiveNativeStatePack:
    if isinstance(value, LiveNativeStatePack):
        pack = value
    elif isinstance(value, Mapping):
        required_fields = {
            "schema_version",
            "kind",
            "source_key",
            "source_revision",
            "next_source_native_creation_ordinal",
            "source_native_ids",
            "native_owner_states",
            "provenance",
            "privacy",
            "chronology",
            "unresolved_work",
        }
        if set(value) != required_fields:
            raise CurrentOwnerError("selected LIVE pack fields are not strict")
        if (
            value.get("schema_version") != LIVE_NATIVE_STATE_PACK_SCHEMA_VERSION
            or value.get("kind") != "runtime.live_native_state_pack"
        ):
            raise CurrentOwnerError("selected LIVE pack schema is unsupported")
        source_key = value.get("source_key")
        if not isinstance(source_key, Sequence) or isinstance(source_key, (str, bytes)):
            raise CurrentOwnerError("selected LIVE pack source key is malformed")
        pack = LiveNativeStatePack(
            source_key=tuple(source_key),
            source_revision=value["source_revision"],
            next_source_native_creation_ordinal=value[
                "next_source_native_creation_ordinal"
            ],
            source_native_ids=value["source_native_ids"],
            native_owner_states=value["native_owner_states"],
            provenance=value["provenance"],
            privacy=value["privacy"],
            chronology=value["chronology"],
            unresolved_work=value["unresolved_work"],
        )
    else:
        raise CurrentOwnerError("selected LIVE source is not a typed native-state pack")
    if (
        pack.source_key != source.source_key
        or pack.source_revision != source.source_revision
    ):
        raise CurrentOwnerError("selected LIVE native-state pack is stale")
    return pack


def _payload_fingerprint(
    owner_ref: NativeOwnerRef,
    payload: Mapping[str, object],
    source_basis: str,
    generation: int | None,
) -> str:
    encoded = json.dumps(
        {
            "family_key": owner_ref.family_key,
            "identity": owner_ref.identity,
            "payload": payload,
            "source_basis": source_basis,
            "generation": generation,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _observation_fingerprint(
    reads: Mapping[NativeOwnerRef, CurrentOwnerRead], snapshot_fingerprint: str
) -> str:
    parts = [snapshot_fingerprint]
    for owner_ref in sorted(reads, key=lambda ref: (ref.family_key, ref.identity)):
        read = reads[owner_ref]
        parts.append(
            "\0".join(
                (
                    owner_ref.family_key,
                    *owner_ref.identity,
                    read.status.value,
                    read.source.value,
                    read.source_basis or "",
                    str(read.generation),
                    read.fingerprint or "",
                )
            )
        )
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def _read_basis(read: CurrentOwnerRead) -> tuple[object, ...]:
    return (
        read.status,
        read.source,
        read.source_basis,
        read.generation,
        read.fingerprint,
        read.predecessor_fingerprint,
    )
