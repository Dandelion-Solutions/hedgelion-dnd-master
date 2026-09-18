"""Strict LIVE source envelopes, typed claims and exact-source CAS evidence.

This module owns only the bounded LIVE source/currentness boundary.  Campaign
routing selects a source; a prepared source, local write, commit object,
timestamp or source-local counter never becomes current authority by itself.
The transport adapter is deliberately outside this module: callers provide the
exact source observation and the authority-changing acknowledgement.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
import re
from typing import Final, TypeAlias


# framework_module_version: 1.0.2
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.2"

LiveSourceKey: TypeAlias = tuple[str, str, str]

LIVE_CLAIM_SCHEMA_VERSION: Final[int] = 1
LIVE_ROUTING_SCHEMA_VERSION: Final[int] = 1
LIVE_PUBLICATION_ATTEMPT_SCHEMA_VERSION: Final[int] = 2

_MACHINE_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_NATIVE_FAMILY = re.compile(r"^(world|runtime)\.[a-z][a-z0-9_]*$")
_REVISION = re.compile(r"^(?:[a-f0-9]{40}(?:[a-f0-9]{24})?|[A-Za-z][A-Za-z0-9_.:-]*)$")
_FORBIDDEN_FAMILIES = frozenset(
    {
        "world.player",
        "runtime.session",
        "runtime.collaboration_obligation",
        "runtime.checkpoint",
        "runtime.id_allocator",
        "runtime.maintenance_audit",
        "runtime.catalog_gap_report",
    }
)
_CLAIM_TYPES = frozenset(
    {"EXACT_OWNER", "EPOCH_LOCAL_CREATION", "OWNER_DEFINED_PARTITION"}
)


class LiveContractError(ValueError):
    """Raised when a LIVE envelope, claim or currentness contract is invalid."""


class LiveLifecycle(StrEnum):
    """Monotonic lifecycle state for one source/epoch."""

    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    CLOSED_UNABSORBED = "CLOSED_UNABSORBED"
    ABSORBED = "ABSORBED"


class LivePublicationStatus(StrEnum):
    """Epistemic result of an authority-changing LIVE publication."""

    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    REJECTED_STALE = "REJECTED_STALE"
    INDETERMINATE = "INDETERMINATE"


class WriteAuthority(StrEnum):
    """Bounded current write-authority lookup result."""

    CAMPAIGN = "CAMPAIGN"
    LIVE = "LIVE"
    INTEGRITY_CONFLICT = "INTEGRITY_CONFLICT"


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise LiveContractError(f"{label} must be a non-empty string")
    return value


def _machine_id(value: object, label: str) -> str:
    result = _nonempty(value, label)
    if _MACHINE_ID.fullmatch(result) is None:
        raise LiveContractError(f"{label} must be a machine identifier")
    return result


def _revision(value: object, label: str) -> str:
    result = _nonempty(value, label)
    if _REVISION.fullmatch(result) is None:
        raise LiveContractError(f"{label} must be an exact source revision")
    return result


def _source_key(value: object, label: str = "source key") -> LiveSourceKey:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise LiveContractError(f"{label} must be (campaign_id, scene_id, epoch_id)")
    if len(value) != 3:
        raise LiveContractError(f"{label} must contain campaign_id, scene_id and epoch_id")
    return (
        _machine_id(value[0], f"{label}.campaign_id"),
        _machine_id(value[1], f"{label}.scene_id"),
        _machine_id(value[2], f"{label}.epoch_id"),
    )


@dataclass(frozen=True, slots=True)
class LiveClaimAdmission:
    """Caller-supplied owner evidence for non-exact LIVE claim forms.

    The T02 owner does not define identifier-policy or partition catalogs.  A
    creation or owner-partition claim therefore needs an explicit admission
    supplied by the owning future contract; absence of that evidence fails
    closed.  This context is ephemeral and is never serialized as authority.
    """

    creation_families: frozenset[str] = frozenset()
    owner_defined_partitions: frozenset[tuple[str, str]] = frozenset()

    def __post_init__(self) -> None:
        families = frozenset(
            _machine_id(family, "admitted creation family")
            for family in self.creation_families
        )
        if any(_NATIVE_FAMILY.fullmatch(family) is None for family in families):
            raise LiveContractError("admitted creation family is not a native family")
        if any(family in _FORBIDDEN_FAMILIES for family in families):
            raise LiveContractError("forbidden family cannot be admitted for LIVE creation")
        partitions = frozenset(
            (
                _machine_id(partition_type, "admitted partition type"),
                _machine_id(partition_key, "admitted partition key"),
            )
            for partition_type, partition_key in self.owner_defined_partitions
        )
        object.__setattr__(self, "creation_families", families)
        object.__setattr__(self, "owner_defined_partitions", partitions)

    def admits_creation(self, native_family: str) -> bool:
        return native_family in self.creation_families

    def admits_partition(self, partition_type: str, partition_key: str) -> bool:
        return (partition_type, partition_key) in self.owner_defined_partitions


def _claims(
    value: object,
    *,
    admission: LiveClaimAdmission | None = None,
) -> tuple[LiveClaim, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise LiveContractError("LIVE claims must be an array")
    result = tuple(
        item
        if isinstance(item, LiveClaim)
        else LiveClaim.from_mapping(item, admission=admission)
        for item in value
    )
    keys = [claim.identity_key for claim in result]
    if len(keys) != len(set(keys)):
        raise LiveContractError("LIVE claim set contains duplicate or overlapping claims")
    return result


@dataclass(frozen=True, slots=True)
class LiveClaim:
    """One closed typed claim; references do not implicitly expand its scope."""

    claim_type: str
    native_family: str | None = None
    native_identity: str | None = None
    partition_type: str | None = None
    partition_key: str | None = None
    _admission: LiveClaimAdmission | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.claim_type not in _CLAIM_TYPES:
            raise LiveContractError("LIVE claim must use the closed typed claim grammar")
        family = self.native_family
        if family is not None:
            family = _machine_id(family, "claim.native_family")
            if _NATIVE_FAMILY.fullmatch(family) is None or family in _FORBIDDEN_FAMILIES:
                raise LiveContractError("claim family is not admitted as LIVE authority")
            object.__setattr__(self, "native_family", family)
        if self.claim_type == "EXACT_OWNER":
            if family is None or self.native_identity is None:
                raise LiveContractError("EXACT_OWNER requires native family and identity")
            object.__setattr__(
                self,
                "native_identity",
                _machine_id(self.native_identity, "claim.native_identity"),
            )
            if any(value is not None for value in (self.partition_type, self.partition_key)):
                raise LiveContractError("EXACT_OWNER cannot carry partition fields")
        elif self.claim_type == "EPOCH_LOCAL_CREATION":
            if family is None or self.native_identity is not None:
                raise LiveContractError("EPOCH_LOCAL_CREATION requires only native family")
            if any(value is not None for value in (self.partition_type, self.partition_key)):
                raise LiveContractError("EPOCH_LOCAL_CREATION cannot carry partition fields")
            if self._admission is None or not self._admission.admits_creation(family):
                raise LiveContractError("creation family is not admitted as LIVE authority")
        else:
            if self.partition_type is None or self.partition_key is None:
                raise LiveContractError(
                    "OWNER_DEFINED_PARTITION requires partition type and key"
                )
            if self.native_family is not None or self.native_identity is not None:
                raise LiveContractError("OWNER_DEFINED_PARTITION cannot carry an exact owner")
            partition_type = _machine_id(self.partition_type, "claim.partition_type")
            partition_key = _machine_id(self.partition_key, "claim.partition_key")
            if self._admission is None or not self._admission.admits_partition(
                partition_type, partition_key
            ):
                raise LiveContractError("owner-defined partition is not admitted as LIVE authority")

    @classmethod
    def exact_owner(cls, native_family: str, native_identity: str) -> LiveClaim:
        """Claim exactly one existing native owner."""

        return cls("EXACT_OWNER", native_family=native_family, native_identity=native_identity)

    @classmethod
    def epoch_local_creation(
        cls,
        native_family: str,
        *,
        admission: LiveClaimAdmission | None = None,
    ) -> LiveClaim:
        """Admit creation of a new owner of one explicitly admitted family."""

        return cls("EPOCH_LOCAL_CREATION", native_family=native_family, _admission=admission)

    @classmethod
    def owner_defined_partition(
        cls,
        partition_type: str,
        partition_key: str,
        *,
        admission: LiveClaimAdmission | None = None,
    ) -> LiveClaim:
        """Claim only an already owner-defined bounded partition."""

        return cls(
            "OWNER_DEFINED_PARTITION",
            partition_type=partition_type,
            partition_key=partition_key,
            _admission=admission,
        )

    @classmethod
    def from_mapping(
        cls,
        value: object,
        *,
        admission: LiveClaimAdmission | None = None,
    ) -> LiveClaim:
        if not isinstance(value, Mapping):
            raise LiveContractError("LIVE claim must be an object")
        claim_type = value.get("claim_type")
        if claim_type == "EXACT_OWNER":
            expected = {"claim_type", "native_family", "native_identity"}
            if set(value) != expected:
                raise LiveContractError("EXACT_OWNER claim fields are not strict")
            return cls.exact_owner(value["native_family"], value["native_identity"])  # type: ignore[arg-type]
        if claim_type == "EPOCH_LOCAL_CREATION":
            expected = {"claim_type", "native_family"}
            if set(value) != expected:
                raise LiveContractError("EPOCH_LOCAL_CREATION claim fields are not strict")
            return cls.epoch_local_creation(
                value["native_family"], admission=admission  # type: ignore[arg-type]
            )
        if claim_type == "OWNER_DEFINED_PARTITION":
            expected = {"claim_type", "partition_type", "partition_key"}
            if set(value) != expected:
                raise LiveContractError("OWNER_DEFINED_PARTITION claim fields are not strict")
            return cls.owner_defined_partition(
                value["partition_type"],  # type: ignore[arg-type]
                value["partition_key"],  # type: ignore[arg-type]
                admission=admission,
            )
        raise LiveContractError("LIVE claim must use the closed typed claim grammar")

    @property
    def identity_key(self) -> tuple[str, ...]:
        if self.claim_type == "OWNER_DEFINED_PARTITION":
            return (self.claim_type, self.partition_type or "", self.partition_key or "")
        return (self.claim_type, self.native_family or "", self.native_identity or "")

    def _is_admitted(self) -> bool:
        return self.claim_type == "EXACT_OWNER" or self._admission is not None

    def as_mapping(self) -> dict[str, str]:
        if self.claim_type == "EXACT_OWNER":
            return {
                "claim_type": self.claim_type,
                "native_family": self.native_family or "",
                "native_identity": self.native_identity or "",
            }
        if self.claim_type == "EPOCH_LOCAL_CREATION":
            return {
                "claim_type": self.claim_type,
                "native_family": self.native_family or "",
            }
        return {
            "claim_type": self.claim_type,
            "partition_type": self.partition_type or "",
            "partition_key": self.partition_key or "",
        }


@dataclass(frozen=True, slots=True)
class LiveEnvelope:
    """Immutable source/scene envelope selected by campaign routing."""

    campaign_id: str
    scene_id: str
    epoch_id: str
    source_ref: str
    source_revision: str
    claims: tuple[LiveClaim, ...]
    status: LiveLifecycle = LiveLifecycle.ACTIVE

    def __post_init__(self) -> None:
        key = _source_key((self.campaign_id, self.scene_id, self.epoch_id))
        object.__setattr__(self, "campaign_id", key[0])
        object.__setattr__(self, "scene_id", key[1])
        object.__setattr__(self, "epoch_id", key[2])
        object.__setattr__(self, "source_ref", _nonempty(self.source_ref, "source_ref"))
        object.__setattr__(self, "source_revision", _revision(self.source_revision, "source_revision"))
        try:
            status = self.status if isinstance(self.status, LiveLifecycle) else LiveLifecycle(self.status)
        except ValueError as error:
            raise LiveContractError("LIVE lifecycle status is not admitted") from error
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "claims", _claims(self.claims))

    @property
    def source_key(self) -> LiveSourceKey:
        return self.campaign_id, self.scene_id, self.epoch_id

    @property
    def ordinary_writes_allowed(self) -> bool:
        return self.status is LiveLifecycle.ACTIVE

    def claims_contain(self, native_family: str, native_identity: str) -> bool:
        return any(
            claim.claim_type == "EXACT_OWNER"
            and claim.native_family == native_family
            and claim.native_identity == native_identity
            for claim in self.claims
        )

    def as_mapping(self) -> dict[str, object]:
        return {
            "campaign_id": self.campaign_id,
            "scene_id": self.scene_id,
            "epoch_id": self.epoch_id,
            "source_ref": self.source_ref,
            "source_revision": self.source_revision,
            "status": self.status.value,
            "claims": [claim.as_mapping() for claim in self.claims],
        }

    @classmethod
    def from_mapping(
        cls,
        value: object,
        *,
        admission: LiveClaimAdmission | None = None,
    ) -> LiveEnvelope:
        if not isinstance(value, Mapping):
            raise LiveContractError("LIVE envelope must be an object")
        expected = {
            "campaign_id",
            "scene_id",
            "epoch_id",
            "source_ref",
            "source_revision",
            "status",
            "claims",
        }
        if set(value) != expected:
            raise LiveContractError("LIVE envelope fields are not strict")
        return cls(
            campaign_id=value["campaign_id"],  # type: ignore[arg-type]
            scene_id=value["scene_id"],  # type: ignore[arg-type]
            epoch_id=value["epoch_id"],  # type: ignore[arg-type]
            source_ref=value["source_ref"],  # type: ignore[arg-type]
            source_revision=value["source_revision"],  # type: ignore[arg-type]
            status=value["status"],  # type: ignore[arg-type]
            claims=_claims(value["claims"], admission=admission),
        )


@dataclass(frozen=True, slots=True)
class LiveRouting:
    """Complete bounded campaign projection selecting exact LIVE sources."""

    campaign_id: str
    entries: tuple[LiveEnvelope, ...]
    complete: bool = True

    def __post_init__(self) -> None:
        campaign_id = _machine_id(self.campaign_id, "LIVE route campaign_id")
        object.__setattr__(self, "campaign_id", campaign_id)
        if type(self.complete) is not bool or not self.complete:
            raise LiveContractError("LIVE route must be complete")
        if not isinstance(self.entries, Sequence) or isinstance(self.entries, (str, bytes)):
            raise LiveContractError("LIVE route entries must be an array")
        entries = tuple(self.entries)
        if any(entry.campaign_id != campaign_id for entry in entries):
            raise LiveContractError("LIVE route entry campaign differs from route")
        keys = [entry.source_key for entry in entries]
        if len(keys) != len(set(keys)):
            raise LiveContractError("LIVE route contains duplicate source keys")
        active_claims: dict[tuple[str, str], LiveEnvelope] = {}
        active_partitions: set[str] = set()
        for entry in entries:
            if entry.status not in {
                LiveLifecycle.ACTIVE,
                LiveLifecycle.CLOSED,
                LiveLifecycle.CLOSED_UNABSORBED,
            }:
                continue
            for claim in entry.claims:
                if not claim._is_admitted():
                    raise LiveContractError("selected LIVE claim lacks owner admission")
                if claim.claim_type != "EXACT_OWNER":
                    if claim.partition_type in active_partitions:
                        raise LiveContractError("selected LIVE claims overlap")
                    if claim.partition_type is not None:
                        active_partitions.add(claim.partition_type)
                    continue
                claim_key = (claim.native_family or "", claim.native_identity or "")
                previous = active_claims.get(claim_key)
                if previous is not None:
                    raise LiveContractError("selected LIVE claims overlap")
                active_claims[claim_key] = entry
        object.__setattr__(self, "entries", entries)

    def as_mapping(self) -> dict[str, object]:
        return {
            "schema_version": LIVE_ROUTING_SCHEMA_VERSION,
            "kind": "runtime.live_routing",
            "campaign_id": self.campaign_id,
            "complete": True,
            "entries": [entry.as_mapping() for entry in self.entries],
        }

    @classmethod
    def from_mapping(cls, value: object) -> LiveRouting:
        if not isinstance(value, Mapping):
            raise LiveContractError("LIVE route must be an object")
        expected = {"schema_version", "kind", "campaign_id", "complete", "entries"}
        if set(value) != expected:
            raise LiveContractError("LIVE route fields are not strict")
        if value["schema_version"] != LIVE_ROUTING_SCHEMA_VERSION:
            raise LiveContractError("unsupported LIVE route schema")
        if value["kind"] != "runtime.live_routing":
            raise LiveContractError("LIVE route kind is not admitted")
        raw_entries = value["entries"]
        if not isinstance(raw_entries, Sequence) or isinstance(raw_entries, (str, bytes)):
            raise LiveContractError("LIVE route entries must be an array")
        return cls(
            campaign_id=value["campaign_id"],  # type: ignore[arg-type]
            entries=tuple(
                LiveEnvelope.from_mapping(item, admission=admission) for item in raw_entries
            ),
            complete=value["complete"],  # type: ignore[arg-type]
        )


def build_live_route(campaign_id: str, entries: Sequence[LiveEnvelope]) -> LiveRouting:
    """Build a complete route only from explicitly supplied owner envelopes."""

    return LiveRouting(campaign_id=campaign_id, entries=tuple(entries))


def _route_or_none(route: LiveRouting | LiveEnvelope | Mapping[str, object]) -> LiveRouting | LiveEnvelope | None:
    if isinstance(route, (LiveRouting, LiveEnvelope)):
        return route
    if not isinstance(route, Mapping):
        return None
    try:
        if route.get("campaign_id") is None:
            return None
        return LiveRouting.from_mapping(route)
    except (LiveContractError, TypeError, ValueError):
        return None


def select_live_source(
    route: LiveRouting | LiveEnvelope | Mapping[str, object],
    source_key: LiveSourceKey,
) -> LiveEnvelope | None:
    """Select only the exact route entry; no source/latest fallback is allowed."""

    key = _source_key(source_key)
    resolved = _route_or_none(route)
    if resolved is None:
        return None
    if isinstance(resolved, LiveEnvelope):
        selected = resolved if resolved.source_key == key else None
    else:
        selected = next((entry for entry in resolved.entries if entry.source_key == key), None)
    if selected is None or selected.status is LiveLifecycle.ABSORBED:
        return None
    return selected


def lookup_write_authority(
    native_family: str,
    native_identity: str,
    route: LiveRouting | LiveEnvelope | Mapping[str, object],
) -> WriteAuthority:
    """Resolve one owner through bounded selected claims, never by scanning sources."""

    _machine_id(native_family, "native_family")
    _machine_id(native_identity, "native_identity")
    resolved = _route_or_none(route)
    if resolved is None:
        return WriteAuthority.CAMPAIGN
    entries = (resolved,) if isinstance(resolved, LiveEnvelope) else resolved.entries
    matches = tuple(
        entry
        for entry in entries
        if entry.status
        in {LiveLifecycle.ACTIVE, LiveLifecycle.CLOSED, LiveLifecycle.CLOSED_UNABSORBED}
        and entry.claims_contain(native_family, native_identity)
    )
    if len(matches) > 1:
        return WriteAuthority.INTEGRITY_CONFLICT
    if not matches:
        return WriteAuthority.CAMPAIGN
    return WriteAuthority.LIVE if matches[0].ordinary_writes_allowed else WriteAuthority.INTEGRITY_CONFLICT


def validate_exact_source(
    selected: LiveEnvelope,
    observed: LiveEnvelope | Mapping[str, object],
) -> bool:
    """Return true only when key, ref, revision, lifecycle and claims all match."""

    if not isinstance(selected, LiveEnvelope):
        raise LiveContractError("selected LIVE source must be owner-typed")
    if isinstance(observed, LiveEnvelope):
        candidate = observed
    else:
        try:
            candidate = LiveEnvelope.from_mapping(observed)
        except (LiveContractError, TypeError, ValueError):
            return False
    return (
        selected.source_key == candidate.source_key
        and selected.source_ref == candidate.source_ref
        and selected.source_revision == candidate.source_revision
        and selected.status is candidate.status
        and selected.claims == candidate.claims
    )


@dataclass(frozen=True, slots=True)
class FrozenLivePublicationAttempt:
    """Immutable prospective LIVE transition, not a lease or publication journal."""

    selected_route: LiveRouting
    source_key: LiveSourceKey
    target_ref: str
    expected_source_revision: str
    proposed_source_revision: str
    transition_kind: str
    claims: tuple[LiveClaim, ...]
    source_status: LiveLifecycle
    successor_route: LiveRouting

    def __post_init__(self) -> None:
        if not isinstance(self.selected_route, LiveRouting) or not self.selected_route.complete:
            raise LiveContractError("LIVE publication requires complete selected route evidence")
        object.__setattr__(self, "source_key", _source_key(self.source_key))
        object.__setattr__(self, "target_ref", _nonempty(self.target_ref, "target_ref"))
        object.__setattr__(
            self,
            "expected_source_revision",
            _revision(self.expected_source_revision, "expected_source_revision"),
        )
        proposed = _revision(self.proposed_source_revision, "proposed_source_revision")
        if proposed == self.expected_source_revision:
            raise LiveContractError("proposed source revision must advance its predecessor")
        object.__setattr__(self, "proposed_source_revision", proposed)
        if self.transition_kind not in {"MUTATION", "CLOSE", "ABSORB"}:
            raise LiveContractError("LIVE transition kind is not admitted")
        object.__setattr__(self, "claims", _claims(self.claims))
        if not isinstance(self.source_status, LiveLifecycle):
            object.__setattr__(self, "source_status", LiveLifecycle(self.source_status))
        selected = select_live_source(self.selected_route, self.source_key)
        if selected is None or not validate_exact_source(
            selected,
            LiveEnvelope(
                campaign_id=self.source_key[0],
                scene_id=self.source_key[1],
                epoch_id=self.source_key[2],
                source_ref=self.target_ref,
                source_revision=self.expected_source_revision,
                claims=self.claims,
                status=self.source_status,
            ),
        ):
            raise LiveContractError("frozen attempt is not bound to the selected route source")
        if not isinstance(self.successor_route, LiveRouting) or not self.successor_route.complete:
            raise LiveContractError("LIVE publication requires complete successor closure")
        successors = self.successor_route.entries
        if len(successors) != 1:
            raise LiveContractError("LIVE successor closure must contain exactly one source")
        successor = successors[0]
        expected_successor_status = {
            "MUTATION": LiveLifecycle.ACTIVE,
            "CLOSE": LiveLifecycle.CLOSED,
            "ABSORB": LiveLifecycle.ABSORBED,
        }[self.transition_kind]
        if (
            successor.source_key != self.source_key
            or successor.source_ref != self.target_ref
            or successor.source_revision != self.proposed_source_revision
            or successor.claims != self.claims
            or successor.status is not expected_successor_status
        ):
            raise LiveContractError("frozen attempt successor closure is incomplete or mismatched")

    def as_mapping(self) -> dict[str, object]:
        return {
            "schema_version": LIVE_PUBLICATION_ATTEMPT_SCHEMA_VERSION,
            "selected_route": self.selected_route.as_mapping(),
            "source_key": list(self.source_key),
            "target_ref": self.target_ref,
            "expected_source_revision": self.expected_source_revision,
            "proposed_source_revision": self.proposed_source_revision,
            "transition_kind": self.transition_kind,
            "source_status": self.source_status.value,
            "claims": [claim.as_mapping() for claim in self.claims],
            "successor": self.successor_route.as_mapping(),
        }


def freeze_live_attempt(
    source: LiveEnvelope,
    *,
    route: LiveRouting,
    proposed_source_revision: str,
    transition_kind: str = "MUTATION",
    expected_source_revision: str | None = None,
) -> FrozenLivePublicationAttempt:
    """Freeze one exact-source attempt after route/currentness selection."""

    if not isinstance(source, LiveEnvelope):
        raise LiveContractError("LIVE publication requires an owner-typed source")
    if not isinstance(route, LiveRouting) or not route.complete:
        raise LiveContractError("LIVE publication requires complete selected route evidence")
    selected = select_live_source(route, source.source_key)
    if selected is None or not validate_exact_source(source, selected):
        raise LiveContractError("LIVE publication source is not the exact selected route source")
    expected = source.source_revision if expected_source_revision is None else _revision(
        expected_source_revision, "expected_source_revision"
    )
    if expected != source.source_revision:
        raise LiveContractError("attempt expected revision differs from selected source")
    if source.status is not LiveLifecycle.ACTIVE:
        raise LiveContractError("closed LIVE source rejects ordinary writes and cannot reopen")
    successor_status = {
        "MUTATION": LiveLifecycle.ACTIVE,
        "CLOSE": LiveLifecycle.CLOSED,
        "ABSORB": LiveLifecycle.ABSORBED,
    }.get(transition_kind)
    if successor_status is None:
        raise LiveContractError("LIVE transition kind is not admitted")
    successor = LiveEnvelope(
        campaign_id=source.campaign_id,
        scene_id=source.scene_id,
        epoch_id=source.epoch_id,
        source_ref=source.source_ref,
        source_revision=proposed_source_revision,
        claims=source.claims,
        status=successor_status,
    )
    return FrozenLivePublicationAttempt(
        selected_route=route,
        source_key=source.source_key,
        target_ref=source.source_ref,
        expected_source_revision=expected,
        proposed_source_revision=proposed_source_revision,
        transition_kind=transition_kind,
        claims=source.claims,
        source_status=source.status,
        successor_route=build_live_route(source.campaign_id, (successor,)),
    )


@dataclass(frozen=True, slots=True)
class LivePublicationResult:
    """Typed CAS result preserving ambiguous transport knowledge."""

    status: LivePublicationStatus
    source_key: LiveSourceKey
    authoritative: bool
    observed_source_revision: str | None = None

    @property
    def acknowledged(self) -> bool:
        return self.status is LivePublicationStatus.ACCEPTED and self.authoritative

    @property
    def kind(self) -> str:
        return self.status.name.lower()

    @property
    def requires_repin(self) -> bool:
        return self.status in {
            LivePublicationStatus.REJECTED,
            LivePublicationStatus.REJECTED_STALE,
        }

    @property
    def can_reexecute(self) -> bool:
        return False

    def acknowledge(self) -> bool:
        if not self.acknowledged:
            raise LiveContractError("indeterminate/rejected LIVE publication cannot be acknowledged")
        return True


def _result(
    status: LivePublicationStatus,
    attempt: FrozenLivePublicationAttempt,
    *,
    authoritative: bool,
    observed_source_revision: str | None = None,
) -> LivePublicationResult:
    return LivePublicationResult(
        status=status,
        source_key=attempt.source_key,
        authoritative=authoritative,
        observed_source_revision=observed_source_revision,
    )


def classify_cas_result(
    attempt: FrozenLivePublicationAttempt,
    acknowledgement: Mapping[str, object] | None,
) -> LivePublicationResult:
    """Classify a transport acknowledgement without inferring success locally."""

    if not isinstance(attempt, FrozenLivePublicationAttempt):
        raise LiveContractError("CAS classification requires a frozen LIVE attempt")
    if acknowledgement is None:
        return _result(LivePublicationStatus.INDETERMINATE, attempt, authoritative=False)
    if not isinstance(acknowledgement, Mapping):
        return _result(LivePublicationStatus.INDETERMINATE, attempt, authoritative=False)
    raw_key = acknowledgement.get("source_key")
    if raw_key is not None:
        try:
            if _source_key(raw_key) != attempt.source_key:
                return _result(LivePublicationStatus.REJECTED_STALE, attempt, authoritative=False)
        except LiveContractError:
            return _result(LivePublicationStatus.REJECTED_STALE, attempt, authoritative=False)
    raw_status = str(acknowledgement.get("status", "")).upper()
    accepted = acknowledgement.get("accepted") is True or raw_status in {
        "ACCEPTED",
        "CONFIRMED_ACCEPTED",
    }
    if not accepted:
        current = acknowledgement.get("current_source_revision")
        if raw_status in {"REJECTED", "CONFIRMED_REJECTED", "ERROR", "FAILED"} and current is None:
            return _result(LivePublicationStatus.REJECTED, attempt, authoritative=False)
        if current is None or current == attempt.expected_source_revision:
            return _result(LivePublicationStatus.INDETERMINATE, attempt, authoritative=False)
        return _result(
            LivePublicationStatus.REJECTED_STALE,
            attempt,
            authoritative=False,
            observed_source_revision=_revision(current, "current_source_revision"),
        )
    if raw_key is None:
        return _result(LivePublicationStatus.INDETERMINATE, attempt, authoritative=False)
    acknowledged_target = acknowledgement.get("target_ref")
    if acknowledged_target != attempt.target_ref:
        return _result(LivePublicationStatus.REJECTED_STALE, attempt, authoritative=False)
    acknowledged_expected = acknowledgement.get("expected_source_revision")
    if acknowledged_expected != attempt.expected_source_revision:
        return _result(LivePublicationStatus.REJECTED_STALE, attempt, authoritative=False)
    if "selected_route" not in acknowledgement or "successor" not in acknowledgement:
        return _result(LivePublicationStatus.INDETERMINATE, attempt, authoritative=False)
    if acknowledgement["selected_route"] != attempt.selected_route.as_mapping():
        return _result(LivePublicationStatus.REJECTED_STALE, attempt, authoritative=False)
    if acknowledgement["successor"] != attempt.successor_route.as_mapping():
        return _result(LivePublicationStatus.REJECTED_STALE, attempt, authoritative=False)
    proposed = acknowledgement.get("new_source_revision")
    if proposed is None:
        return _result(LivePublicationStatus.INDETERMINATE, attempt, authoritative=False)
    if proposed != attempt.proposed_source_revision:
        raise LiveContractError("accepted CAS acknowledgement has non-monotonic source revision")
    _revision(proposed, "new_source_revision")
    return _result(
        LivePublicationStatus.ACCEPTED,
        attempt,
        authoritative=True,
        observed_source_revision=attempt.proposed_source_revision,
    )


def reconcile_indeterminate(
    attempt: FrozenLivePublicationAttempt,
    current_source: LiveEnvelope,
) -> LivePublicationResult:
    """Resolve an ambiguous acknowledgement from one exact current-source read."""

    if not isinstance(current_source, LiveEnvelope):
        raise LiveContractError("indeterminate reconciliation requires exact source evidence")
    if current_source.source_key != attempt.source_key or current_source.source_ref != attempt.target_ref:
        return _result(LivePublicationStatus.REJECTED_STALE, attempt, authoritative=False)
    predecessor = LiveEnvelope(
        campaign_id=attempt.source_key[0],
        scene_id=attempt.source_key[1],
        epoch_id=attempt.source_key[2],
        source_ref=attempt.target_ref,
        source_revision=attempt.expected_source_revision,
        claims=attempt.claims,
        status=attempt.source_status,
    )
    successor = attempt.successor_route.entries[0]
    if validate_exact_source(successor, current_source):
        return _result(
            LivePublicationStatus.ACCEPTED,
            attempt,
            authoritative=True,
            observed_source_revision=current_source.source_revision,
        )
    if validate_exact_source(predecessor, current_source):
        return _result(LivePublicationStatus.INDETERMINATE, attempt, authoritative=False)
    return _result(
        LivePublicationStatus.REJECTED_STALE,
        attempt,
        authoritative=False,
        observed_source_revision=current_source.source_revision,
    )


def close_live_source(
    source: LiveEnvelope,
    *,
    expected_source_revision: str,
    closed_source_revision: str,
) -> LiveEnvelope:
    """Build a terminal CLOSED successor only from the exact current source."""

    if source.status is not LiveLifecycle.ACTIVE:
        raise LiveContractError("closed LIVE source cannot reopen or close again")
    if expected_source_revision != source.source_revision:
        raise LiveContractError("close requires the exact selected source predecessor")
    _revision(closed_source_revision, "closed_source_revision")
    if closed_source_revision == source.source_revision:
        raise LiveContractError("closed source revision must advance its predecessor")
    return LiveEnvelope(
        campaign_id=source.campaign_id,
        scene_id=source.scene_id,
        epoch_id=source.epoch_id,
        source_ref=source.source_ref,
        source_revision=closed_source_revision,
        claims=source.claims,
        status=LiveLifecycle.CLOSED,
    )


def mark_closed_unabsorbed(source: LiveEnvelope) -> LiveEnvelope:
    """Retain closed selected truth with zero ordinary writers pending absorption."""

    if source.status is not LiveLifecycle.CLOSED:
        raise LiveContractError("only a CLOSED source can become CLOSED_UNABSORBED")
    return LiveEnvelope(
        campaign_id=source.campaign_id,
        scene_id=source.scene_id,
        epoch_id=source.epoch_id,
        source_ref=source.source_ref,
        source_revision=source.source_revision,
        claims=source.claims,
        status=LiveLifecycle.CLOSED_UNABSORBED,
    )


# Compatibility names for the owner-local contract vocabulary.  These aliases
# do not create another authority or another representation.
LiveRoute = LiveRouting
LiveSource = LiveEnvelope
LivePublicationAttempt = FrozenLivePublicationAttempt
LivePublicationOutcome = LivePublicationResult
