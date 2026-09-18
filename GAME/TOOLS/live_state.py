"""Strict LIVE source envelopes, typed claims and exact-source CAS evidence.

This module owns only the bounded LIVE source/currentness boundary.  Campaign
routing selects a source; a prepared source, local write, commit object,
timestamp or source-local counter never becomes current authority by itself.
The transport adapter is deliberately outside this module: callers provide the
exact source observation and the authority-changing acknowledgement.
"""

from __future__ import annotations

import base64
import binascii
from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from dataclasses import InitVar, dataclass, replace
from enum import StrEnum
import hashlib
import json
import re
from types import MappingProxyType
from typing import Final, TypeAlias
import weakref


# framework_module_version: 1.0.10
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.10"

LiveSourceKey: TypeAlias = tuple[str, str, str]

LIVE_CLAIM_SCHEMA_VERSION: Final[int] = 2
LIVE_ROUTING_SCHEMA_VERSION: Final[int] = 4
LIVE_PUBLICATION_ATTEMPT_SCHEMA_VERSION: Final[int] = 5
LIVE_OPENING_PREPARATION_SCHEMA_VERSION: Final[int] = 1
LIVE_OPENING_SEED_SCHEMA_VERSION: Final[int] = 2
LIVE_NATIVE_STATE_PACK_SCHEMA_VERSION: Final[int] = 2
LIVE_ABSORPTION_ATTEMPT_SCHEMA_VERSION: Final[int] = 1

SOURCE_NATIVE_LIVE_ENCODING: Final[str] = "framed_base32hex_v1"
SOURCE_NATIVE_CURSOR_MAX: Final[int] = (1 << 64) - 1
_SOURCE_NATIVE_ID_MARKER = ":live1:"
_SOURCE_NATIVE_ID_DOMAIN = b"HDM-LIVE-ID-V1"

# This is the closed T04 admission law.  It is deliberately local and
# read-only: W05 owns the physical catalog projection, while T04 must not
# accept a caller's proposed disposition as authority.
LIVE_BIRTH_ADMISSION_TABLE: Final[Mapping[str, str]] = MappingProxyType(
    {
        "world.actor": "SOURCE_NATIVE_LIVE",
        "world.actor_group": "SOURCE_NATIVE_LIVE",
        "world.asset": "SOURCE_NATIVE_LIVE",
        "world.location": "SOURCE_NATIVE_LIVE",
        "world.connection": "SOURCE_NATIVE_LIVE",
        "world.zone": "SOURCE_NATIVE_LIVE",
        "world.organization": "SOURCE_NATIVE_LIVE",
        "world.contract": "SOURCE_NATIVE_LIVE",
        "world.mission": "SOURCE_NATIVE_LIVE",
        "world.scene": "SOURCE_NATIVE_LIVE",
        "world.encounter": "SOURCE_NATIVE_LIVE",
        "world.hazard": "SOURCE_NATIVE_LIVE",
        "world.effect": "SOURCE_NATIVE_LIVE",
        "world.lore_fact": "SOURCE_NATIVE_LIVE",
        "world.knowledge": "OWNER_EQUIVALENT",
        "world.thread": "SOURCE_NATIVE_LIVE",
        "world.player": "FORBIDDEN",
        "runtime.session": "FORBIDDEN",
        "runtime.message": "SOURCE_NATIVE_LIVE",
        "runtime.interaction": "SOURCE_NATIVE_LIVE",
        "runtime.procedure": "SOURCE_NATIVE_LIVE",
        "runtime.intent_plan": "OWNER_EQUIVALENT",
        "runtime.command": "OWNER_EQUIVALENT",
        "runtime.resolution": "SOURCE_NATIVE_LIVE",
        "runtime.continuation": "OWNER_EQUIVALENT",
        "runtime.mechanical_event": "OWNER_EQUIVALENT",
        "runtime.semantic_event": "SOURCE_NATIVE_LIVE",
        "runtime.resolution_trace": "OWNER_EQUIVALENT",
        "runtime.disclosure": "OWNER_EQUIVALENT",
        "runtime.collaboration_obligation": "FORBIDDEN",
        "runtime.checkpoint": "FORBIDDEN",
        "runtime.id_allocator": "FORBIDDEN",
        "runtime.maintenance_audit": "FORBIDDEN",
        "runtime.catalog_gap_report": "FORBIDDEN",
    }
)

_CAMPAIGN_ROUTE_DOMAIN = b"HDM-LIVE-CAMPAIGN-ROUTE-V1"
_SCENE_ROUTE_DOMAIN = b"HDM-LIVE-SCENE-ROUTE-V1"
_EPOCH_ID_DOMAIN = b"HDM-LIVE-EPOCH-ID-V1"
_EPOCH_ID = re.compile(r"^e1-[0-9a-f]{64}$")

_MACHINE_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_NATIVE_FAMILY = re.compile(r"^(world|runtime)\.[a-z][a-z0-9_]*$")
_REVISION = re.compile(r"^(?:[a-f0-9]{40}(?:[a-f0-9]{24})?|[A-Za-z][A-Za-z0-9_.:-]*)$")
_CLAIM_TYPES = frozenset(
    {"EXACT_OWNER", "EPOCH_LOCAL_CREATION", "OWNER_DEFINED_PARTITION"}
)


class LiveContractError(ValueError):
    """Raised when a LIVE envelope, claim or currentness contract is invalid."""


class SourceNativeAllocationError(LiveContractError):
    """Raised when source-native LIVE allocation cannot be accepted safely."""


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


def _semantic_id(value: object, label: str) -> str:
    """Validate semantic identity without constraining its physical spelling."""

    return _nonempty(value, label)


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
        _semantic_id(value[0], f"{label}.campaign_id"),
        _semantic_id(value[1], f"{label}.scene_id"),
        _epoch_id(value[2], f"{label}.epoch_id"),
    )


def _epoch_id(value: object, label: str) -> str:
    result = _semantic_id(value, label)
    if _EPOCH_ID.fullmatch(result) is None:
        raise LiveContractError(f"{label} must use the versioned e1 identity encoding")
    return result


def _frame_string(value: str, label: str) -> bytes:
    encoded = _semantic_id(value, label).encode("utf-8")
    return len(encoded).to_bytes(4, "big") + encoded


def _frame_list(values: Sequence[bytes]) -> bytes:
    if len(values) > 0xFFFFFFFF:
        raise LiveContractError("canonical LIVE identity list is too large")
    framed = [len(values).to_bytes(4, "big")]
    for value in values:
        if len(value) > 0xFFFFFFFF:
            raise LiveContractError("canonical LIVE identity component is too large")
        framed.extend((len(value).to_bytes(4, "big"), value))
    return b"".join(framed)


def _domain_frame(domain: bytes, values: Sequence[str]) -> bytes:
    return domain + b"\x00" + b"".join(
        _frame_string(value, "LIVE identity component") for value in values
    )


def _uint64(value: object, label: str, *, allow_zero: bool = False) -> int:
    if type(value) is not int:
        raise SourceNativeAllocationError(f"{label} must be a uint64 integer")
    minimum = 0 if allow_zero else 1
    if value < minimum or value > SOURCE_NATIVE_CURSOR_MAX:
        raise SourceNativeAllocationError(f"{label} is outside the uint64 range")
    return value


def _copy_json_mapping(value: object, label: str) -> dict[str, object]:
    """Copy one explicit JSON-shaped owner input without inventing defaults."""

    if not isinstance(value, Mapping):
        raise LiveContractError(f"{label} must be an explicit mapping")

    def validate(item: object, item_label: str) -> None:
        if isinstance(item, Mapping):
            for key, nested in item.items():
                if not isinstance(key, str) or not key:
                    raise LiveContractError(f"{item_label} has a non-string key")
                validate(nested, f"{item_label}.{key}")
        elif isinstance(item, Sequence) and not isinstance(item, (str, bytes, bytearray)):
            for index, nested in enumerate(item):
                validate(nested, f"{item_label}[{index}]")
        elif item is not None and not isinstance(item, (str, int, float, bool)):
            raise LiveContractError(f"{item_label} is not JSON-shaped native state")

    validate(value, label)
    try:
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as error:
        raise LiveContractError(f"{label} is not canonical JSON-shaped native state") from error
    return deepcopy(dict(value))


def _state_digest(value: Mapping[str, object]) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _source_native_policy_row(
    native_family: str,
    identifier_policy: Mapping[str, object],
) -> Mapping[str, object]:
    """Resolve one explicit source-native policy row without a catalog fallback."""

    if not isinstance(identifier_policy, Mapping):
        raise LiveContractError("source-native identifier policy must be a mapping")
    row: object = identifier_policy.get(native_family)
    if row is None:
        domain = native_family.split(".", 1)[0]
        rows = identifier_policy.get(domain)
        if isinstance(rows, Mapping):
            row = rows.get(native_family)
    if not isinstance(row, Mapping):
        raise LiveContractError("source-native LIVE identifier policy is missing")
    disposition = LIVE_BIRTH_ADMISSION_TABLE.get(native_family)
    if disposition != "SOURCE_NATIVE_LIVE":
        raise LiveContractError(
            f"family {native_family} is not admitted for source-native LIVE identity: "
            f"{disposition or 'UNKNOWN'}"
        )
    live_birth = row.get("live_birth")
    if not isinstance(live_birth, Mapping):
        raise LiveContractError("source-native LIVE disposition is missing")
    if str(live_birth.get("disposition", "")).upper() != disposition:
        raise LiveContractError("family live_birth disposition does not match the closed T04 table")
    if live_birth.get("encoding") != SOURCE_NATIVE_LIVE_ENCODING:
        raise LiveContractError("source-native LIVE encoding is not admitted")
    prefix = row.get("prefix")
    if not isinstance(prefix, str) or re.fullmatch(r"[A-Za-z][A-Za-z0-9_.:-]*", prefix) is None:
        raise LiveContractError("source-native LIVE policy prefix is invalid")
    return row


@dataclass(frozen=True, slots=True, order=True)
class SourceNativeCursor:
    """The next source-local source-native creation ordinal for one LIVE source."""

    next_source_native_creation_ordinal: int = 1

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "next_source_native_creation_ordinal",
            _uint64(
                self.next_source_native_creation_ordinal,
                "next_source_native_creation_ordinal",
            ),
        )

    @property
    def next_ordinal(self) -> int:
        return self.next_source_native_creation_ordinal

    @property
    def value(self) -> int:
        return self.next_source_native_creation_ordinal


@dataclass(frozen=True, slots=True)
class SourceNativeCreation:
    """One normalized owner-local creation slot before source-native allocation."""

    native_family: str
    owner_local_index: int

    def __post_init__(self) -> None:
        family = _machine_id(self.native_family, "native_family")
        if (
            _NATIVE_FAMILY.fullmatch(family) is None
            or LIVE_BIRTH_ADMISSION_TABLE.get(family) != "SOURCE_NATIVE_LIVE"
        ):
            raise SourceNativeAllocationError("native family is not admitted for LIVE creation")
        object.__setattr__(self, "native_family", family)
        object.__setattr__(
            self,
            "owner_local_index",
            _uint64(self.owner_local_index, "owner_local_index", allow_zero=True),
        )

    @classmethod
    def from_value(cls, value: object) -> SourceNativeCreation:
        if isinstance(value, SourceNativeCreation):
            return value
        if not isinstance(value, Mapping):
            raise SourceNativeAllocationError("source-native creation must be typed")
        return cls(
            native_family=value.get("native_family", value.get("family")),  # type: ignore[arg-type]
            owner_local_index=value.get("owner_local_index"),  # type: ignore[arg-type]
        )


@dataclass(frozen=True, slots=True)
class SourceNativeLiveIdentityComponents:
    """Decoded source-native identity evidence for audit/integrity checks."""

    live_source_key: LiveSourceKey
    native_family: str
    source_local_creation_ordinal: int
    prefix: str
    encoding: str = SOURCE_NATIVE_LIVE_ENCODING

    @property
    def campaign_id(self) -> str:
        return self.live_source_key[0]

    @property
    def scene_id(self) -> str:
        return self.live_source_key[1]

    @property
    def epoch_id(self) -> str:
        return self.live_source_key[2]

    @property
    def ordinal(self) -> int:
        return self.source_local_creation_ordinal


@dataclass(frozen=True, slots=True)
class SourceNativeAllocation:
    """One frozen slot-to-ordinal-to-ID allocation in a LIVE attempt."""

    native_family: str
    owner_local_index: int
    creation_slot_index: int
    source_local_creation_ordinal: int
    native_id: str

    def __post_init__(self) -> None:
        SourceNativeCreation(self.native_family, self.owner_local_index)
        _uint64(self.source_local_creation_ordinal, "source_local_creation_ordinal")
        if type(self.creation_slot_index) is not int or self.creation_slot_index < 0:
            raise SourceNativeAllocationError("creation_slot_index must be a non-negative integer")
        if not isinstance(self.native_id, str) or not self.native_id:
            raise SourceNativeAllocationError("source-native allocation must carry a native ID")
        try:
            _, _, family, ordinal = _decode_source_native_live_id(self.native_id)
        except LiveContractError as error:
            raise SourceNativeAllocationError(
                "source-native allocation must carry a framed LIVE ID"
            ) from error
        if family != self.native_family or ordinal != self.source_local_creation_ordinal:
            raise SourceNativeAllocationError(
                "source-native allocation ID does not match its family and ordinal"
            )

    def as_mapping(self) -> dict[str, object]:
        return {
            "native_family": self.native_family,
            "owner_local_index": self.owner_local_index,
            "source_local_creation_ordinal": self.source_local_creation_ordinal,
            "native_id": self.native_id,
            "creation_slot_index": self.creation_slot_index,
        }


def _source_native_frame(
    live_source_key: LiveSourceKey,
    native_family: str,
    source_local_creation_ordinal: int,
) -> bytes:
    campaign_id, scene_id, epoch_id = _source_key(live_source_key, "LIVE source key")
    family = _machine_id(native_family, "native_family")
    if (
        _NATIVE_FAMILY.fullmatch(family) is None
        or LIVE_BIRTH_ADMISSION_TABLE.get(family) != "SOURCE_NATIVE_LIVE"
    ):
        raise SourceNativeAllocationError("native family is not admitted for LIVE creation")
    ordinal = _uint64(source_local_creation_ordinal, "source_local_creation_ordinal")
    return (
        _SOURCE_NATIVE_ID_DOMAIN
        + b"\x00"
        + _frame_string(campaign_id, "campaign_id")
        + _frame_string(scene_id, "scene_id")
        + _frame_string(epoch_id, "epoch_id")
        + _frame_string(family, "native_family")
        + ordinal.to_bytes(8, "big")
    )


def encode_source_native_live_id(
    live_source_key: LiveSourceKey,
    native_family: str,
    source_local_creation_ordinal: int,
    identifier_policy: Mapping[str, object],
) -> str:
    """Encode one accepted LIVE-born identity using framed Base32hex v1."""

    family = _machine_id(native_family, "native_family")
    row = _source_native_policy_row(family, identifier_policy)
    frame = _source_native_frame(live_source_key, family, source_local_creation_ordinal)
    payload = base64.b32hexencode(frame).decode("ascii").rstrip("=").lower()
    return f"{row['prefix']}{_SOURCE_NATIVE_ID_MARKER}{payload}"


def _decode_source_native_frame(payload: str) -> tuple[LiveSourceKey, str, int]:
    if not payload or re.fullmatch(r"[a-z0-9]+", payload) is None:
        raise LiveContractError("source-native ID payload has invalid encoding")
    padded = payload + "=" * ((-len(payload)) % 8)
    try:
        raw = base64.b32hexdecode(padded, casefold=True)
    except (ValueError, binascii.Error) as error:
        raise LiveContractError("source-native ID payload is not valid Base32hex") from error
    cursor = 0

    def read_bytes(label: str) -> bytes:
        nonlocal cursor
        if cursor + 4 > len(raw):
            raise LiveContractError(f"source-native ID frame is truncated at {label}")
        length = int.from_bytes(raw[cursor : cursor + 4], "big")
        cursor += 4
        end = cursor + length
        if end > len(raw):
            raise LiveContractError(f"source-native ID frame is truncated at {label}")
        value = raw[cursor:end]
        cursor = end
        return value

    if not raw.startswith(_SOURCE_NATIVE_ID_DOMAIN + b"\x00"):
        raise LiveContractError("source-native ID has the wrong encoding version")
    cursor = len(_SOURCE_NATIVE_ID_DOMAIN) + 1
    try:
        components = tuple(read_bytes(label).decode("utf-8") for label in (
            "campaign_id",
            "scene_id",
            "epoch_id",
            "native_family",
        ))
    except UnicodeDecodeError as error:
        raise LiveContractError("source-native ID frame is not UTF-8") from error
    if cursor + 8 != len(raw):
        raise LiveContractError("source-native ID frame has trailing or missing bytes")
    ordinal = int.from_bytes(raw[cursor:], "big")
    source_key = _source_key(components[:3], "LIVE source key")
    family = _machine_id(components[3], "native_family")
    _uint64(ordinal, "source_local_creation_ordinal")
    return source_key, family, ordinal


def _decode_source_native_live_id(native_id: str) -> tuple[str, LiveSourceKey, str, int]:
    if not isinstance(native_id, str) or native_id.count(_SOURCE_NATIVE_ID_MARKER) != 1:
        raise LiveContractError("source-native ID has invalid encoding marker")
    prefix, payload = native_id.split(_SOURCE_NATIVE_ID_MARKER, 1)
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9_.:-]*", prefix) is None:
        raise LiveContractError("source-native ID prefix is invalid")
    source_key, family, ordinal = _decode_source_native_frame(payload)
    return prefix, source_key, family, ordinal


def parse_source_native_live_id(
    native_id: str,
    identifier_policy: Mapping[str, object],
    *,
    expected_source_key: LiveSourceKey | None = None,
    expected_native_family: str | None = None,
    expected_source_local_creation_ordinal: int | None = None,
) -> SourceNativeLiveIdentityComponents:
    """Parse and validate a source-native ID against its explicit family policy."""

    prefix, source_key, family, ordinal = _decode_source_native_live_id(native_id)
    row = _source_native_policy_row(family, identifier_policy)
    if row["prefix"] != prefix:
        raise LiveContractError("source-native ID prefix does not match its family policy")
    if expected_source_key is not None and source_key != _source_key(
        expected_source_key, "expected LIVE source key"
    ):
        raise LiveContractError("source-native ID is bound to the wrong LIVE source")
    if expected_native_family is not None and family != _machine_id(
        expected_native_family, "expected native_family"
    ):
        raise LiveContractError("source-native ID is bound to the wrong native family")
    if expected_source_local_creation_ordinal is not None and ordinal != _uint64(
        expected_source_local_creation_ordinal,
        "expected source_local_creation_ordinal",
    ):
        raise LiveContractError("source-native ID is bound to the wrong creation ordinal")
    return SourceNativeLiveIdentityComponents(
        live_source_key=source_key,
        native_family=family,
        source_local_creation_ordinal=ordinal,
        prefix=prefix,
    )


def _validate_source_native_history(
    live_source_key: LiveSourceKey,
    next_creation_ordinal: int,
    source_native_ids: Sequence[str],
    identifier_policy: Mapping[str, object] | None = None,
) -> None:
    expected_count = next_creation_ordinal - 1
    if len(source_native_ids) != expected_count:
        raise LiveContractError("source-native ID history must be contiguous from ordinal one")
    for expected_ordinal, native_id in enumerate(source_native_ids, start=1):
        if identifier_policy is not None:
            try:
                parse_source_native_live_id(
                    native_id,
                    identifier_policy,
                    expected_source_key=live_source_key,
                    expected_source_local_creation_ordinal=expected_ordinal,
                )
            except LiveContractError as error:
                raise LiveContractError(
                    "source-native ID history does not match the exact family policy"
                ) from error
            continue
        try:
            _, source_key, family, ordinal = _decode_source_native_live_id(native_id)
        except LiveContractError as error:
            raise LiveContractError(
                "source-native ID history contains an invalid framed ID"
            ) from error
        if source_key != live_source_key:
            raise LiveContractError("source-native ID history contains a different LIVE source")
        if LIVE_BIRTH_ADMISSION_TABLE.get(family) != "SOURCE_NATIVE_LIVE":
            raise LiveContractError("source-native ID history contains a non-admitted family")
        if ordinal != expected_ordinal:
            raise LiveContractError("source-native ID history ordinals are not contiguous")


def normalize_source_native_creations(
    creations: Iterable[SourceNativeCreation | Mapping[str, object]],
) -> tuple[SourceNativeCreation, ...]:
    """Canonicalize creation slots by UTF-8 family bytes, then local index."""

    normalized = tuple(SourceNativeCreation.from_value(value) for value in creations)
    seen: set[tuple[str, int]] = set()
    for creation in normalized:
        key = (creation.native_family, creation.owner_local_index)
        if key in seen:
            raise SourceNativeAllocationError("duplicate owner-local index for native family")
        seen.add(key)
    return tuple(
        sorted(normalized, key=lambda item: (item.native_family.encode("utf-8"), item.owner_local_index))
    )


def allocate_source_native_creations(
    live_source_key: LiveSourceKey,
    creations: Iterable[SourceNativeCreation | Mapping[str, object]],
    cursor: SourceNativeCursor | int,
    identifier_policy: Mapping[str, object],
) -> tuple[SourceNativeAllocation, ...]:
    """Assign deterministic slots, ordinals and final IDs without campaign allocation."""

    current = cursor if isinstance(cursor, SourceNativeCursor) else SourceNativeCursor(cursor)
    normalized = normalize_source_native_creations(creations)
    if len(normalized) > SOURCE_NATIVE_CURSOR_MAX - current.next_ordinal:
        raise SourceNativeAllocationError("source-native cursor exhausted; allocation would overflow")
    return tuple(
        SourceNativeAllocation(
            native_family=creation.native_family,
            owner_local_index=creation.owner_local_index,
            creation_slot_index=slot,
            source_local_creation_ordinal=current.next_ordinal + slot,
            native_id=encode_source_native_live_id(
                live_source_key,
                creation.native_family,
                current.next_ordinal + slot,
                identifier_policy,
            ),
        )
        for slot, creation in enumerate(normalized)
    )


def advance_source_native_cursor(
    cursor: SourceNativeCursor | int,
    publication: LivePublicationResult,
    accepted_source: LiveEnvelope | None = None,
) -> SourceNativeCursor:
    """Advance only from an authoritative accepted exact-source publication."""

    current = cursor if isinstance(cursor, SourceNativeCursor) else SourceNativeCursor(cursor)
    if not isinstance(publication, LivePublicationResult):
        raise SourceNativeAllocationError("cursor advancement requires a typed CAS result")
    if not publication.acknowledged or not publication.source_native_allocations:
        return current
    if not _is_owner_issued_cas_result(publication):
        raise SourceNativeAllocationError(
            "cursor advancement requires accepted owner-issued CAS evidence"
        )
    if not isinstance(publication.accepted_source, LiveEnvelope):
        raise SourceNativeAllocationError(
            "cursor advancement requires the exact source envelope accepted by CAS"
        )
    if accepted_source is not None and accepted_source != publication.accepted_source:
        raise SourceNativeAllocationError("cursor advancement envelope differs from CAS evidence")
    accepted = publication.accepted_source
    if accepted.source_key != publication.source_key:
        raise SourceNativeAllocationError("cursor advancement source differs from CAS evidence")
    if accepted.source_revision != publication.observed_source_revision:
        raise SourceNativeAllocationError("cursor advancement revision differs from CAS evidence")
    if publication.expected_next_source_native_creation_ordinal != current.next_ordinal:
        raise SourceNativeAllocationError("accepted CAS result has a different source cursor")
    proposed = publication.proposed_next_source_native_creation_ordinal
    if proposed is None or proposed <= current.next_ordinal:
        raise SourceNativeAllocationError("accepted CAS result does not advance the source cursor")
    if proposed > SOURCE_NATIVE_CURSOR_MAX:
        raise SourceNativeAllocationError("accepted CAS result overflows the source cursor")
    allocation_ids = tuple(item.native_id for item in publication.source_native_allocations)
    if (
        accepted.next_source_native_creation_ordinal != proposed
        or accepted.source_native_ids[-len(allocation_ids) :] != allocation_ids
    ):
        raise SourceNativeAllocationError(
            "accepted source envelope does not contain the CAS allocation history"
        )
    return SourceNativeCursor(proposed)


def encode_live_campaign_route_token(campaign_id: str) -> str:
    """Encode semantic campaign identity as a physical c1 route component."""

    return "c1-" + hashlib.sha256(
        _domain_frame(_CAMPAIGN_ROUTE_DOMAIN, (campaign_id,))
    ).hexdigest()


def encode_live_scene_route_token(scene_id: str) -> str:
    """Encode semantic scene identity as a physical s1 route component."""

    return "s1-" + hashlib.sha256(
        _domain_frame(_SCENE_ROUTE_DOMAIN, (scene_id,))
    ).hexdigest()


def _canonical_claim_frame(claim: LiveClaim) -> bytes:
    if not isinstance(claim, LiveClaim):
        raise LiveContractError("LIVE identity basis contains an untyped claim")
    if claim.claim_type == "EXACT_OWNER":
        identity = claim.native_identity
        if identity is None or claim.native_family is None:
            raise LiveContractError("EXACT_OWNER claim has incomplete identity basis")
        return b"\x01" + _frame_string(claim.native_family, "claim.native_family") + _frame_list(
            (identity.encode("utf-8"),)
        )
    raise LiveContractError(
        "LIVE claim type has no admitted canonical identity encoding"
    )


def canonicalize_live_claim_set(claims: Iterable[LiveClaim]) -> tuple[bytes, ...]:
    """Return sorted complete claim frames, rejecting duplicate identity frames."""

    frames = tuple(_canonical_claim_frame(claim) for claim in claims)
    if len(frames) != len(set(frames)):
        raise LiveContractError("LIVE identity basis contains duplicate claim frames")
    return tuple(sorted(frames))


def derive_live_epoch_id(
    campaign_id: str,
    scene_id: str,
    opening_campaign_revision: str,
    immutable_claims: Iterable[LiveClaim],
) -> str:
    """Derive the full-digest e1 identity from one immutable opening basis."""

    claim_frames = canonicalize_live_claim_set(immutable_claims)
    opening_revision = _revision(opening_campaign_revision, "opening_campaign_revision")
    frame = (
        _EPOCH_ID_DOMAIN
        + b"\x00"
        + _frame_string(campaign_id, "campaign_id")
        + _frame_string(scene_id, "scene_id")
        + _frame_string(opening_revision, "opening_campaign_revision")
        + _frame_list(claim_frames)
    )
    return "e1-" + hashlib.sha256(frame).hexdigest()


def build_live_ref(campaign_id: str, scene_id: str, epoch_id: str) -> str:
    """Build the bounded physical LIVE ref from semantic IDs."""

    encoded_epoch_id = _epoch_id(epoch_id, "epoch_id")
    return "/".join(
        (
            "live",
            encode_live_campaign_route_token(campaign_id),
            encode_live_scene_route_token(scene_id),
            encoded_epoch_id,
            "LIVE",
            "LIVE_STATE.yaml",
        )
    )


def _route_identity_route(
    expected_route: LiveRouting | LiveEnvelope | Mapping[str, object] | Sequence[str],
) -> LiveRouting | LiveEnvelope | LiveSourceKey:
    if isinstance(expected_route, (LiveRouting, LiveEnvelope)):
        return expected_route
    if isinstance(expected_route, Mapping):
        if "entries" in expected_route:
            return LiveRouting.from_mapping(expected_route)
        return _source_key(
            (
                expected_route.get("campaign_id"),
                expected_route.get("scene_id"),
                expected_route.get("epoch_id"),
            ),
            "expected route identity",
        )
    return _source_key(expected_route, "expected route identity")


def validate_live_route_identity(
    expected_route: LiveRouting | LiveEnvelope | Mapping[str, object] | Sequence[str],
    live_state: LiveEnvelope | Mapping[str, object],
    physical_ref: str,
) -> None:
    """Validate semantic body identity, opening basis and derived physical ref."""

    if isinstance(live_state, LiveEnvelope):
        body = live_state
    else:
        body = LiveEnvelope.from_mapping(live_state)
    expected = _route_identity_route(expected_route)
    if isinstance(expected, LiveRouting):
        selected = next(
            (entry for entry in expected.entries if entry.source_key == body.source_key),
            None,
        )
        if selected is None or not validate_exact_source(selected, body):
            raise LiveContractError("LIVE route/body identity tuple or opening basis mismatch")
    elif isinstance(expected, LiveEnvelope):
        if not validate_exact_source(expected, body):
            raise LiveContractError("LIVE route/body identity tuple or opening basis mismatch")
    elif expected != body.source_key:
        raise LiveContractError("LIVE route/body identity tuple mismatch")

    expected_epoch = derive_live_epoch_id(
        body.campaign_id,
        body.scene_id,
        body.opening_campaign_revision,
        body.claims,
    )
    if expected_epoch != body.epoch_id:
        raise LiveContractError("LIVE epoch identity does not match its opening basis")
    expected_ref = build_live_ref(body.campaign_id, body.scene_id, body.epoch_id)
    if physical_ref != expected_ref or body.source_ref != expected_ref:
        raise LiveContractError("LIVE physical route identity mismatch")


def _claims(value: object) -> tuple[LiveClaim, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise LiveContractError("LIVE claims must be an array")
    result = tuple(
        item if isinstance(item, LiveClaim) else LiveClaim.from_mapping(item)
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
    def __post_init__(self) -> None:
        if self.claim_type not in _CLAIM_TYPES:
            raise LiveContractError("LIVE claim must use the closed typed claim grammar")
        family = self.native_family
        if family is not None:
            family = _machine_id(family, "claim.native_family")
            if _NATIVE_FAMILY.fullmatch(family) is None or (
                LIVE_BIRTH_ADMISSION_TABLE.get(family) == "FORBIDDEN"
            ):
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
            raise LiveContractError(
                "non-exact LIVE claims require a current owner-backed contract"
            )
        else:
            raise LiveContractError(
                "non-exact LIVE claims require a current owner-backed contract"
            )

    @classmethod
    def exact_owner(cls, native_family: str, native_identity: str) -> LiveClaim:
        """Claim exactly one existing native owner."""

        return cls("EXACT_OWNER", native_family=native_family, native_identity=native_identity)

    @classmethod
    def epoch_local_creation(cls, native_family: str) -> LiveClaim:
        """Admit creation of a new owner of one explicitly admitted family."""

        raise LiveContractError(
            "non-exact LIVE claims require a current owner-backed contract"
        )

    @classmethod
    def owner_defined_partition(cls, partition_type: str, partition_key: str) -> LiveClaim:
        """Claim only an already owner-defined bounded partition."""

        raise LiveContractError(
            "non-exact LIVE claims require a current owner-backed contract"
        )

    @classmethod
    def from_mapping(
        cls,
        value: object,
    ) -> LiveClaim:
        if not isinstance(value, Mapping):
            raise LiveContractError("LIVE claim must be an object")
        claim_type = value.get("claim_type")
        if value.get("schema_version") != LIVE_CLAIM_SCHEMA_VERSION:
            raise LiveContractError("unsupported LIVE claim schema")
        if claim_type == "EXACT_OWNER":
            expected = {"schema_version", "claim_type", "native_family", "native_identity"}
            if set(value) != expected:
                raise LiveContractError("EXACT_OWNER claim fields are not strict")
            return cls.exact_owner(value["native_family"], value["native_identity"])  # type: ignore[arg-type]
        if claim_type == "EPOCH_LOCAL_CREATION":
            expected = {"schema_version", "claim_type", "native_family"}
            if set(value) != expected:
                raise LiveContractError("EPOCH_LOCAL_CREATION claim fields are not strict")
            raise LiveContractError(
                "non-exact LIVE claims require a current owner-backed contract"
            )
        if claim_type == "OWNER_DEFINED_PARTITION":
            expected = {
                "schema_version",
                "claim_type",
                "partition_type",
                "partition_key",
            }
            if set(value) != expected:
                raise LiveContractError("OWNER_DEFINED_PARTITION claim fields are not strict")
            raise LiveContractError(
                "non-exact LIVE claims require a current owner-backed contract"
            )
        raise LiveContractError("LIVE claim must use the closed typed claim grammar")

    @property
    def identity_key(self) -> tuple[str, ...]:
        if self.claim_type == "OWNER_DEFINED_PARTITION":
            return (self.claim_type, self.partition_type or "", self.partition_key or "")
        return (self.claim_type, self.native_family or "", self.native_identity or "")

    def as_mapping(self) -> dict[str, object]:
        if self.claim_type == "EXACT_OWNER":
            return {
                "schema_version": LIVE_CLAIM_SCHEMA_VERSION,
                "claim_type": self.claim_type,
                "native_family": self.native_family or "",
                "native_identity": self.native_identity or "",
            }
        if self.claim_type == "EPOCH_LOCAL_CREATION":
            return {
                "schema_version": LIVE_CLAIM_SCHEMA_VERSION,
                "claim_type": self.claim_type,
                "native_family": self.native_family or "",
            }
        return {
            "schema_version": LIVE_CLAIM_SCHEMA_VERSION,
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
    opening_campaign_revision: str = ""
    next_source_native_creation_ordinal: int = 1
    source_native_ids: tuple[str, ...] = ()
    identifier_policy: InitVar[Mapping[str, object] | None] = None

    def __post_init__(self, identifier_policy: Mapping[str, object] | None) -> None:
        key = _source_key((self.campaign_id, self.scene_id, self.epoch_id))
        object.__setattr__(self, "campaign_id", key[0])
        object.__setattr__(self, "scene_id", key[1])
        object.__setattr__(self, "epoch_id", key[2])
        object.__setattr__(self, "source_ref", _nonempty(self.source_ref, "source_ref"))
        object.__setattr__(self, "source_revision", _revision(self.source_revision, "source_revision"))
        object.__setattr__(
            self,
            "opening_campaign_revision",
            _revision(self.opening_campaign_revision, "opening_campaign_revision"),
        )
        try:
            status = self.status if isinstance(self.status, LiveLifecycle) else LiveLifecycle(self.status)
        except ValueError as error:
            raise LiveContractError("LIVE lifecycle status is not admitted") from error
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "claims", _claims(self.claims))
        object.__setattr__(
            self,
            "next_source_native_creation_ordinal",
            _uint64(
                self.next_source_native_creation_ordinal,
                "next_source_native_creation_ordinal",
            ),
        )
        if not isinstance(self.source_native_ids, Sequence) or isinstance(
            self.source_native_ids, (str, bytes)
        ):
            raise LiveContractError("source_native_ids must be an array")
        source_native_ids = tuple(self.source_native_ids)
        if any(not isinstance(native_id, str) or not native_id for native_id in source_native_ids):
            raise LiveContractError("source_native_ids must contain non-empty IDs")
        if len(source_native_ids) != len(set(source_native_ids)):
            raise LiveContractError("source_native_ids must be unique")
        object.__setattr__(self, "source_native_ids", source_native_ids)
        _validate_source_native_history(
            self.source_key,
            self.next_source_native_creation_ordinal,
            source_native_ids,
            identifier_policy,
        )

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
            "opening_campaign_revision": self.opening_campaign_revision,
            "status": self.status.value,
            "claims": [claim.as_mapping() for claim in self.claims],
            "next_source_native_creation_ordinal": self.next_source_native_creation_ordinal,
            "source_native_ids": list(self.source_native_ids),
        }

    @classmethod
    def from_mapping(
        cls,
        value: object,
        *,
        identifier_policy: Mapping[str, object] | None = None,
    ) -> LiveEnvelope:
        if not isinstance(value, Mapping):
            raise LiveContractError("LIVE envelope must be an object")
        expected = {
            "campaign_id",
            "scene_id",
            "epoch_id",
            "source_ref",
            "source_revision",
            "opening_campaign_revision",
            "status",
            "claims",
            "next_source_native_creation_ordinal",
            "source_native_ids",
        }
        if set(value) != expected:
            raise LiveContractError("LIVE envelope fields are not strict")
        if value["source_native_ids"] and identifier_policy is None:
            raise LiveContractError(
                "persisted source-native ID history requires the exact family policy"
            )
        return cls(
            campaign_id=value["campaign_id"],  # type: ignore[arg-type]
            scene_id=value["scene_id"],  # type: ignore[arg-type]
            epoch_id=value["epoch_id"],  # type: ignore[arg-type]
            source_ref=value["source_ref"],  # type: ignore[arg-type]
            source_revision=value["source_revision"],  # type: ignore[arg-type]
            opening_campaign_revision=value["opening_campaign_revision"],  # type: ignore[arg-type]
            status=value["status"],  # type: ignore[arg-type]
            claims=_claims(value["claims"]),
            next_source_native_creation_ordinal=value["next_source_native_creation_ordinal"],  # type: ignore[arg-type]
            source_native_ids=value["source_native_ids"],  # type: ignore[arg-type]
            identifier_policy=identifier_policy,
        )


@dataclass(frozen=True, slots=True)
class LiveRouting:
    """Complete bounded campaign projection selecting exact LIVE sources."""

    campaign_id: str
    entries: tuple[LiveEnvelope, ...]
    complete: bool = True

    def __post_init__(self) -> None:
        campaign_id = _semantic_id(self.campaign_id, "LIVE route campaign_id")
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
        active_creation_families: set[str] = set()
        for entry in entries:
            if entry.status not in {
                LiveLifecycle.ACTIVE,
                LiveLifecycle.CLOSED,
                LiveLifecycle.CLOSED_UNABSORBED,
            }:
                continue
            for claim in entry.claims:
                if claim.claim_type != "EXACT_OWNER":
                    if claim.claim_type == "EPOCH_LOCAL_CREATION":
                        family = claim.native_family or ""
                        if family in active_creation_families:
                            raise LiveContractError("selected LIVE claims overlap")
                        active_creation_families.add(family)
                    elif claim.partition_type in active_partitions:
                        raise LiveContractError("selected LIVE claims overlap")
                    elif claim.partition_type is not None:
                        active_partitions.add(claim.partition_type)
                    raise LiveContractError(
                        "non-exact LIVE claims require a current owner-backed contract"
                    )
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
    def from_mapping(
        cls,
        value: object,
        *,
        identifier_policy: Mapping[str, object] | None = None,
    ) -> LiveRouting:
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
        route = cls(
            campaign_id=value["campaign_id"],  # type: ignore[arg-type]
            entries=tuple(
                LiveEnvelope.from_mapping(item, identifier_policy=identifier_policy)
                for item in raw_entries
            ),
            complete=value["complete"],  # type: ignore[arg-type]
        )
        for entry in route.entries:
            validate_live_route_identity(route, entry, entry.source_ref)
        return route


def build_live_route(
    campaign_id: str,
    entries: Sequence[LiveEnvelope],
    *,
    expected_source_keys: Sequence[LiveSourceKey] | None = None,
) -> LiveRouting:
    """Build a complete route only from explicitly supplied owner envelopes."""

    route = LiveRouting(campaign_id=campaign_id, entries=tuple(entries))
    for entry in route.entries:
        validate_live_route_identity(route, entry, entry.source_ref)
    if expected_source_keys is not None:
        validate_live_route_completeness(route, expected_source_keys)
    return route


def validate_live_route_completeness(
    route: LiveRouting,
    expected_source_keys: Sequence[LiveSourceKey] | None = None,
) -> None:
    """Require a complete current route body, never a partial/stale projection."""

    if not isinstance(route, LiveRouting) or not route.complete:
        raise LiveContractError("LIVE route must be complete")
    if any(entry.status is LiveLifecycle.ABSORBED for entry in route.entries):
        raise LiveContractError("LIVE route contains a stale absorbed member")
    if expected_source_keys is None:
        return
    expected = tuple(_source_key(key, "expected LIVE route source key") for key in expected_source_keys)
    if len(expected) != len(set(expected)):
        raise LiveContractError("expected LIVE route source keys must be unique")
    actual = tuple(entry.source_key for entry in route.entries)
    if set(actual) != set(expected) or len(actual) != len(expected):
        missing = set(expected).difference(actual)
        extra = set(actual).difference(expected)
        raise LiveContractError(
            "LIVE route body is incomplete or contains an extra member: "
            f"missing={sorted(missing)!r}, extra={sorted(extra)!r}"
        )


def handoff_temporal_route_to_live(
    temporal_route: object,
    *,
    campaign_revision: str,
    live_source: LiveEnvelope,
    live_route: LiveRouting,
) -> object:
    """Move temporal routing into the exact selected ACTIVE LIVE source."""

    if not isinstance(live_source, LiveEnvelope):
        raise LiveContractError("temporal LIVE handoff requires an owner-typed source")
    if live_source.status is not LiveLifecycle.ACTIVE:
        raise LiveContractError("temporal LIVE handoff requires an ACTIVE source")
    if not isinstance(live_route, LiveRouting) or not live_route.complete:
        raise LiveContractError("temporal LIVE handoff requires a complete route")
    validate_live_route_completeness(live_route)
    selected = select_live_source(live_route, live_source.source_key)
    if selected is None or not validate_exact_source(selected, live_source):
        raise LiveContractError("temporal LIVE handoff requires the exact selected source")
    from .temporal import reconcile_temporal_route_membership

    return reconcile_temporal_route_membership(
        temporal_route,  # type: ignore[arg-type]
        expected_source_scope="CAMPAIGN",
        expected_source_revision=_revision(campaign_revision, "campaign_revision"),
        target_source_scope="LIVE",
        target_source_revision=live_source.source_revision,
        target_source_key=live_source.source_key,
        campaign_id=live_source.campaign_id,
    )


def handoff_temporal_route_to_campaign(
    temporal_route: object,
    *,
    live_source: LiveEnvelope,
    live_route: LiveRouting,
    campaign_revision: str,
    absorption_acknowledged: bool,
) -> object:
    """Return temporal routing only after exact closed-LIVE absorption proof."""

    if not isinstance(live_source, LiveEnvelope):
        raise LiveContractError("temporal campaign handoff requires an owner-typed source")
    if live_source.status not in {
        LiveLifecycle.CLOSED,
        LiveLifecycle.CLOSED_UNABSORBED,
        LiveLifecycle.ABSORBED,
    }:
        raise LiveContractError("temporal campaign handoff requires a closed or absorbed LIVE source")
    if absorption_acknowledged is not True:
        raise LiveContractError("temporal campaign handoff requires accepted absorption evidence")
    if not isinstance(live_route, LiveRouting) or not live_route.complete:
        raise LiveContractError("temporal campaign handoff requires a complete route")
    validate_live_route_completeness(live_route)
    selected = select_live_source(live_route, live_source.source_key)
    if selected is None:
        raise LiveContractError("temporal campaign handoff requires the exact final source")
    if live_source.status is LiveLifecycle.ABSORBED:
        if selected.status not in {LiveLifecycle.CLOSED, LiveLifecycle.CLOSED_UNABSORBED}:
            raise LiveContractError("temporal campaign handoff requires the exact final source")
        exact_source = validate_exact_source(selected, replace(live_source, status=selected.status))
    else:
        exact_source = validate_exact_source(selected, live_source)
    if not exact_source:
        raise LiveContractError("temporal campaign handoff requires the exact final source")
    from .temporal import reconcile_temporal_route_membership

    return reconcile_temporal_route_membership(
        temporal_route,  # type: ignore[arg-type]
        expected_source_scope="LIVE",
        expected_source_revision=live_source.source_revision,
        expected_source_key=live_source.source_key,
        target_source_scope="CAMPAIGN",
        target_source_revision=_revision(campaign_revision, "campaign_revision"),
        campaign_id=live_source.campaign_id,
    )


@dataclass(frozen=True, slots=True)
class LiveOpeningPreparation:
    """Repeatable, non-authoritative preparation for one LIVE opening."""

    source: LiveEnvelope
    source_native_allocations: tuple[SourceNativeAllocation, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.source, LiveEnvelope):
            raise LiveContractError("LIVE opening preparation requires an owner-typed source")
        if self.source.status is not LiveLifecycle.ACTIVE:
            raise LiveContractError("LIVE opening preparation must begin ACTIVE")
        allocations = tuple(self.source_native_allocations)
        if any(not isinstance(item, SourceNativeAllocation) for item in allocations):
            raise SourceNativeAllocationError("opening allocations must be typed")
        expected_ids = tuple(item.native_id for item in allocations)
        if allocations and self.source.source_native_ids != expected_ids:
            raise SourceNativeAllocationError(
                "opening source-native history must equal the prepared allocations"
            )
        object.__setattr__(self, "source_native_allocations", allocations)

    @property
    def source_key(self) -> LiveSourceKey:
        return self.source.source_key

    @property
    def prepared(self) -> bool:
        return True

    @property
    def published(self) -> bool:
        return False

    def as_mapping(self) -> dict[str, object]:
        return {
            "schema_version": LIVE_OPENING_PREPARATION_SCHEMA_VERSION,
            "kind": "runtime.live_opening_preparation",
            "source": self.source.as_mapping(),
            "source_native_allocations": [
                allocation.as_mapping() for allocation in self.source_native_allocations
            ],
        }


def prepare_live_opening(
    campaign_id: str,
    scene_id: str,
    *,
    opening_campaign_revision: str,
    claims: Iterable[LiveClaim],
    source_revision: str,
    source_native_creations: Iterable[SourceNativeCreation | Mapping[str, object]] = (),
    identifier_policy: Mapping[str, object] | None = None,
) -> LiveOpeningPreparation:
    """Prepare one deterministic LIVE source without selecting it as authority."""

    normalized_claims = _claims(tuple(claims))
    if not normalized_claims:
        raise LiveContractError("LIVE opening requires explicit immutable claims")
    opening_revision = _revision(opening_campaign_revision, "opening_campaign_revision")
    prepared_revision = _revision(source_revision, "source_revision")
    epoch_id = derive_live_epoch_id(campaign_id, scene_id, opening_revision, normalized_claims)
    source_key = (campaign_id, scene_id, epoch_id)
    normalized_creations = normalize_source_native_creations(source_native_creations)
    allocations: tuple[SourceNativeAllocation, ...] = ()
    if normalized_creations:
        if identifier_policy is None:
            raise LiveContractError("opening source-native creation requires an explicit identifier policy")
        allocations = allocate_source_native_creations(
            source_key,
            normalized_creations,
            SourceNativeCursor(1),
            identifier_policy,
        )
    source = LiveEnvelope(
        campaign_id=campaign_id,
        scene_id=scene_id,
        epoch_id=epoch_id,
        source_ref=build_live_ref(campaign_id, scene_id, epoch_id),
        source_revision=prepared_revision,
        claims=normalized_claims,
        status=LiveLifecycle.ACTIVE,
        opening_campaign_revision=opening_revision,
        next_source_native_creation_ordinal=1 + len(allocations),
        source_native_ids=tuple(item.native_id for item in allocations),
        identifier_policy=identifier_policy,
    )
    return LiveOpeningPreparation(source=source, source_native_allocations=allocations)


@dataclass(frozen=True, slots=True)
class LiveOpeningSeed:
    """Complete explicit native inputs for one prepared LIVE source."""

    preparation: LiveOpeningPreparation
    native_owner_states: Mapping[str, object]
    provenance: Mapping[str, object]
    privacy: Mapping[str, object]
    chronology: Mapping[str, object]
    unresolved_work: Mapping[str, object]

    def __post_init__(self) -> None:
        if not isinstance(self.preparation, LiveOpeningPreparation):
            raise LiveContractError("opening seed requires typed preparation")
        owner_states = _copy_json_mapping(self.native_owner_states, "native_owner_states")
        if not owner_states:
            raise LiveContractError("opening seed requires explicit native owner inputs")
        _validate_opening_owner_families(self.preparation.source, owner_states)
        object.__setattr__(self, "native_owner_states", owner_states)
        for field_name in ("provenance", "privacy", "chronology", "unresolved_work"):
            object.__setattr__(
                self,
                field_name,
                _copy_json_mapping(getattr(self, field_name), field_name),
            )

    @property
    def source(self) -> LiveEnvelope:
        return self.preparation.source

    @property
    def source_key(self) -> LiveSourceKey:
        return self.source.source_key

    def as_mapping(self) -> dict[str, object]:
        return {
            "schema_version": LIVE_OPENING_SEED_SCHEMA_VERSION,
            "kind": "runtime.live_opening_seed",
            "preparation": self.preparation.as_mapping(),
            "source": self.source.as_mapping(),
            "native_owner_states": deepcopy(dict(self.native_owner_states)),
            "provenance": deepcopy(dict(self.provenance)),
            "privacy": deepcopy(dict(self.privacy)),
            "chronology": deepcopy(dict(self.chronology)),
            "unresolved_work": deepcopy(dict(self.unresolved_work)),
        }


def build_live_opening_seed(
    preparation: LiveOpeningPreparation | LiveEnvelope,
    *,
    native_owner_states: Mapping[str, object] | None = None,
    owner_states: Mapping[str, object] | None = None,
    provenance: Mapping[str, object] | None = None,
    privacy: Mapping[str, object] | None = None,
    chronology: Mapping[str, object] | None = None,
    unresolved_work: Mapping[str, object] | None = None,
) -> LiveOpeningSeed:
    """Build a seed only when every required native input is explicitly supplied."""

    typed_preparation = _as_opening_preparation(preparation)
    selected_owner_states = native_owner_states if native_owner_states is not None else owner_states
    if selected_owner_states is None:
        raise LiveContractError("opening seed requires explicit native owner inputs")
    if any(value is None for value in (provenance, privacy, chronology, unresolved_work)):
        raise LiveContractError(
            "opening seed requires explicit provenance, privacy, chronology and unresolved work"
        )
    return LiveOpeningSeed(
        preparation=typed_preparation,
        native_owner_states=selected_owner_states,
        provenance=provenance,  # type: ignore[arg-type]
        privacy=privacy,  # type: ignore[arg-type]
        chronology=chronology,  # type: ignore[arg-type]
        unresolved_work=unresolved_work,  # type: ignore[arg-type]
    )


def _as_opening_preparation(
    value: LiveOpeningPreparation | LiveEnvelope,
) -> LiveOpeningPreparation:
    if isinstance(value, LiveOpeningPreparation):
        return value
    if isinstance(value, LiveEnvelope):
        return LiveOpeningPreparation(source=value, source_native_allocations=())
    raise LiveContractError("LIVE opening requires typed preparation")


def _validate_opening_owner_families(
    source: LiveEnvelope,
    owner_states: Mapping[str, object],
) -> None:
    for family in owner_states:
        if not isinstance(family, str) or _NATIVE_FAMILY.fullmatch(family) is None:
            raise LiveContractError("opening native owner family is not typed")
    required_families = {
        claim.native_family
        for claim in source.claims
        if claim.claim_type == "EXACT_OWNER" and claim.native_family is not None
    }
    missing = required_families.difference(owner_states)
    if missing:
        raise LiveContractError(f"opening seed is missing claimed native owners: {sorted(missing)!r}")


@dataclass(frozen=True, slots=True)
class LiveNativeStatePack:
    """Lossless physical carrier for native owners and cross-cutting evidence."""

    source_key: LiveSourceKey
    source_revision: str
    next_source_native_creation_ordinal: int
    source_native_ids: tuple[str, ...]
    native_owner_states: Mapping[str, object]
    provenance: Mapping[str, object]
    privacy: Mapping[str, object]
    chronology: Mapping[str, object]
    unresolved_work: Mapping[str, object]

    def __post_init__(self) -> None:
        key = _source_key(self.source_key, "packed LIVE source key")
        object.__setattr__(self, "source_key", key)
        object.__setattr__(self, "source_revision", _revision(self.source_revision, "packed source revision"))
        next_ordinal = _uint64(
            self.next_source_native_creation_ordinal,
            "packed next_source_native_creation_ordinal",
        )
        object.__setattr__(self, "next_source_native_creation_ordinal", next_ordinal)
        if not isinstance(self.source_native_ids, Sequence) or isinstance(
            self.source_native_ids, (str, bytes)
        ):
            raise LiveContractError("packed source_native_ids must be an array")
        source_native_ids = tuple(self.source_native_ids)
        if any(not isinstance(native_id, str) or not native_id for native_id in source_native_ids):
            raise LiveContractError("packed source_native_ids must contain non-empty IDs")
        if len(source_native_ids) != len(set(source_native_ids)):
            raise LiveContractError("packed source_native_ids must be unique")
        _validate_source_native_history(key, next_ordinal, source_native_ids)
        object.__setattr__(self, "source_native_ids", source_native_ids)
        owner_states = _copy_json_mapping(self.native_owner_states, "native_owner_states")
        if not owner_states:
            raise LiveContractError("packed LIVE state requires native owner states")
        for family in owner_states:
            if _NATIVE_FAMILY.fullmatch(family) is None:
                raise LiveContractError("packed LIVE state contains an untyped owner family")
        object.__setattr__(self, "native_owner_states", owner_states)
        for field_name in ("provenance", "privacy", "chronology", "unresolved_work"):
            object.__setattr__(
                self,
                field_name,
                _copy_json_mapping(getattr(self, field_name), field_name),
            )

    def as_mapping(self) -> dict[str, object]:
        return {
            "schema_version": LIVE_NATIVE_STATE_PACK_SCHEMA_VERSION,
            "kind": "runtime.live_native_state_pack",
            "source_key": list(self.source_key),
            "source_revision": self.source_revision,
            "next_source_native_creation_ordinal": self.next_source_native_creation_ordinal,
            "source_native_ids": list(self.source_native_ids),
            "native_owner_states": deepcopy(dict(self.native_owner_states)),
            "provenance": deepcopy(dict(self.provenance)),
            "privacy": deepcopy(dict(self.privacy)),
            "chronology": deepcopy(dict(self.chronology)),
            "unresolved_work": deepcopy(dict(self.unresolved_work)),
        }


def pack_live_native_state(
    source: LiveOpeningSeed | LiveEnvelope | LiveNativeStatePack,
    native_owner_states: Mapping[str, object] | None = None,
    *,
    owner_states: Mapping[str, object] | None = None,
    provenance: Mapping[str, object] | None = None,
    privacy: Mapping[str, object] | None = None,
    chronology: Mapping[str, object] | None = None,
    unresolved_work: Mapping[str, object] | None = None,
) -> LiveNativeStatePack:
    """Pack explicit native state without dropping identities or evidence."""

    if isinstance(source, LiveNativeStatePack):
        if any(
            value is not None
            for value in (
                native_owner_states,
                owner_states,
                provenance,
                privacy,
                chronology,
                unresolved_work,
            )
        ):
            raise LiveContractError("an existing LIVE state pack cannot be silently replaced")
        return source
    if isinstance(source, LiveOpeningSeed):
        if any(
            value is not None
            for value in (
                native_owner_states,
                owner_states,
                provenance,
                privacy,
                chronology,
                unresolved_work,
            )
        ):
            raise LiveContractError("opening seed inputs cannot be overridden during packing")
        return LiveNativeStatePack(
            source_key=source.source_key,
            source_revision=source.source.source_revision,
            next_source_native_creation_ordinal=source.source.next_source_native_creation_ordinal,
            source_native_ids=source.source.source_native_ids,
            native_owner_states=source.native_owner_states,
            provenance=source.provenance,
            privacy=source.privacy,
            chronology=source.chronology,
            unresolved_work=source.unresolved_work,
        )
    if not isinstance(source, LiveEnvelope):
        raise LiveContractError("LIVE state packing requires typed source or opening seed")
    selected_owner_states = native_owner_states if native_owner_states is not None else owner_states
    if selected_owner_states is None:
        raise LiveContractError("LIVE state packing requires explicit native owner states")
    if any(value is None for value in (provenance, privacy, chronology, unresolved_work)):
        raise LiveContractError(
            "LIVE state packing requires explicit provenance, privacy, chronology and unresolved work"
        )
    _validate_opening_owner_families(source, selected_owner_states)
    return LiveNativeStatePack(
        source_key=source.source_key,
        source_revision=source.source_revision,
        next_source_native_creation_ordinal=source.next_source_native_creation_ordinal,
        source_native_ids=source.source_native_ids,
        native_owner_states=selected_owner_states,
        provenance=provenance,  # type: ignore[arg-type]
        privacy=privacy,  # type: ignore[arg-type]
        chronology=chronology,  # type: ignore[arg-type]
        unresolved_work=unresolved_work,  # type: ignore[arg-type]
    )


def unpack_live_native_state(pack: LiveNativeStatePack) -> dict[str, object]:
    """Return a deep copy of every packed native input, with no lossy projection."""

    if not isinstance(pack, LiveNativeStatePack):
        raise LiveContractError("LIVE state unpacking requires a typed state pack")
    return {
        "source_key": pack.source_key,
        "source_revision": pack.source_revision,
        "next_source_native_creation_ordinal": pack.next_source_native_creation_ordinal,
        "source_native_ids": tuple(pack.source_native_ids),
        "native_owner_states": deepcopy(dict(pack.native_owner_states)),
        "provenance": deepcopy(dict(pack.provenance)),
        "privacy": deepcopy(dict(pack.privacy)),
        "chronology": deepcopy(dict(pack.chronology)),
        "unresolved_work": deepcopy(dict(pack.unresolved_work)),
    }


def publish_live_opening(
    preparation: LiveOpeningPreparation,
    publication: LivePublicationResult,
) -> LiveEnvelope:
    """Adopt only an owner-issued exact-source CAS result for an opening."""

    if not isinstance(preparation, LiveOpeningPreparation):
        raise LiveContractError("opening publication requires typed preparation")
    if (
        not isinstance(publication, LivePublicationResult)
        or not publication.acknowledged
        or not _is_owner_issued_cas_result(publication)
    ):
        raise LiveContractError("opening publication requires an accepted exact-source CAS result")
    attempt = publication.attempt
    if not isinstance(attempt, FrozenLivePublicationAttempt):
        raise LiveContractError("opening publication lacks its frozen predecessor evidence")
    selected = select_live_source(attempt.selected_route, preparation.source_key)
    if selected is None or not validate_exact_source(selected, preparation.source):
        raise LiveContractError("opening publication predecessor differs from the prepared envelope")
    if (
        attempt.source_key != preparation.source.source_key
        or attempt.target_ref != preparation.source.source_ref
        or attempt.expected_source_revision != preparation.source.source_revision
        or attempt.source_status is not preparation.source.status
        or attempt.claims != preparation.source.claims
    ):
        raise LiveContractError("opening publication predecessor does not match preparation")
    accepted = publication.accepted_source
    if accepted is None or accepted.source_key != preparation.source_key:
        raise LiveContractError("accepted opening publication is not bound to the prepared source")
    if accepted.status is not LiveLifecycle.ACTIVE:
        raise LiveContractError("accepted opening publication must produce an ACTIVE source")
    if accepted.opening_campaign_revision != preparation.source.opening_campaign_revision:
        raise LiveContractError("accepted opening publication changed the opening basis")
    if (
        accepted.source_ref != preparation.source.source_ref
        or accepted.claims != preparation.source.claims
        or accepted.next_source_native_creation_ordinal
        != preparation.source.next_source_native_creation_ordinal
        or accepted.source_native_ids != preparation.source.source_native_ids
    ):
        raise LiveContractError("accepted opening publication changed the prepared envelope history")
    return accepted


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
        and selected.opening_campaign_revision == candidate.opening_campaign_revision
        and selected.status is candidate.status
        and selected.claims == candidate.claims
        and selected.next_source_native_creation_ordinal
        == candidate.next_source_native_creation_ordinal
        and selected.source_native_ids == candidate.source_native_ids
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
    source_native_allocations: tuple[SourceNativeAllocation, ...] = ()
    expected_next_source_native_creation_ordinal: int | None = None
    proposed_next_source_native_creation_ordinal: int | None = None

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
        allocations = tuple(self.source_native_allocations)
        if any(not isinstance(item, SourceNativeAllocation) for item in allocations):
            raise SourceNativeAllocationError("frozen source-native allocations must be typed")
        object.__setattr__(self, "source_native_allocations", allocations)
        if allocations:
            expected_cursor = _uint64(
                self.expected_next_source_native_creation_ordinal,
                "expected_next_source_native_creation_ordinal",
            )
            proposed_cursor = _uint64(
                self.proposed_next_source_native_creation_ordinal,
                "proposed_next_source_native_creation_ordinal",
            )
            if expected_cursor + len(allocations) != proposed_cursor:
                raise SourceNativeAllocationError("source-native cursor advance is not contiguous")
            if tuple(item.source_local_creation_ordinal for item in allocations) != tuple(
                range(expected_cursor, proposed_cursor)
            ):
                raise SourceNativeAllocationError("source-native allocations do not match cursor")
            object.__setattr__(self, "expected_next_source_native_creation_ordinal", expected_cursor)
            object.__setattr__(self, "proposed_next_source_native_creation_ordinal", proposed_cursor)
        elif any(
            value is not None
            for value in (
                self.expected_next_source_native_creation_ordinal,
                self.proposed_next_source_native_creation_ordinal,
            )
        ):
            raise SourceNativeAllocationError("source-native cursor evidence needs allocations")
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
                opening_campaign_revision=selected.opening_campaign_revision,
                next_source_native_creation_ordinal=selected.next_source_native_creation_ordinal,
                source_native_ids=selected.source_native_ids,
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
        if self.source_native_allocations:
            expected_ids = selected.source_native_ids + tuple(
                item.native_id for item in self.source_native_allocations
            )
            if (
                selected.next_source_native_creation_ordinal
                != self.expected_next_source_native_creation_ordinal
                or successor.next_source_native_creation_ordinal
                != self.proposed_next_source_native_creation_ordinal
                or successor.source_native_ids != expected_ids
            ):
                raise SourceNativeAllocationError("frozen source-native cursor/ID closure is incomplete")

    def as_mapping(self) -> dict[str, object]:
        result: dict[str, object] = {
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

        if self.source_native_allocations:
            result.update(
                {
                    "source_native_allocations": [
                        allocation.as_mapping() for allocation in self.source_native_allocations
                    ],
                    "expected_next_source_native_creation_ordinal": self.expected_next_source_native_creation_ordinal,
                    "proposed_next_source_native_creation_ordinal": self.proposed_next_source_native_creation_ordinal,
                }
            )
        return result


def freeze_live_attempt(
    source: LiveEnvelope,
    *,
    route: LiveRouting,
    proposed_source_revision: str,
    transition_kind: str = "MUTATION",
    expected_source_revision: str | None = None,
    source_native_creations: Iterable[SourceNativeCreation | Mapping[str, object]] = (),
    source_native_cursor: SourceNativeCursor | int | None = None,
    identifier_policy: Mapping[str, object] | None = None,
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
    normalized_creations = normalize_source_native_creations(source_native_creations)
    allocations: tuple[SourceNativeAllocation, ...] = ()
    expected_cursor: int | None = None
    proposed_cursor: int | None = None
    if normalized_creations:
        if transition_kind != "MUTATION":
            raise SourceNativeAllocationError("source-native creation requires an ordinary LIVE mutation")
        cursor = source.next_source_native_creation_ordinal if source_native_cursor is None else source_native_cursor
        current_cursor = cursor if isinstance(cursor, SourceNativeCursor) else SourceNativeCursor(cursor)
        if identifier_policy is None:
            raise LiveContractError("source-native creation requires an explicit identifier policy")
        allocations = allocate_source_native_creations(
            source.source_key,
            normalized_creations,
            current_cursor,
            identifier_policy,
        )
        expected_cursor = current_cursor.next_ordinal
        proposed_cursor = expected_cursor + len(allocations)
        if proposed_cursor > SOURCE_NATIVE_CURSOR_MAX:
            raise SourceNativeAllocationError("source-native cursor exhausted; allocation would overflow")
    elif source_native_cursor is not None:
        current_cursor = source_native_cursor if isinstance(source_native_cursor, SourceNativeCursor) else SourceNativeCursor(source_native_cursor)
        if current_cursor.next_ordinal != source.next_source_native_creation_ordinal:
            raise SourceNativeAllocationError("source-native cursor is not the exact selected source cursor")
    next_ordinal = source.next_source_native_creation_ordinal if proposed_cursor is None else proposed_cursor
    source_native_ids = source.source_native_ids + tuple(item.native_id for item in allocations)
    successor = LiveEnvelope(
        campaign_id=source.campaign_id,
        scene_id=source.scene_id,
        epoch_id=source.epoch_id,
        source_ref=source.source_ref,
        source_revision=proposed_source_revision,
        claims=source.claims,
        status=successor_status,
        opening_campaign_revision=source.opening_campaign_revision,
        next_source_native_creation_ordinal=next_ordinal,
        source_native_ids=source_native_ids,
        identifier_policy=identifier_policy,
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
        source_native_allocations=allocations,
        expected_next_source_native_creation_ordinal=expected_cursor,
        proposed_next_source_native_creation_ordinal=proposed_cursor,
    )


@dataclass(frozen=True, slots=True, weakref_slot=True)
class LivePublicationResult:
    """Typed CAS result preserving ambiguous transport knowledge."""

    status: LivePublicationStatus
    source_key: LiveSourceKey
    authoritative: bool
    observed_source_revision: str | None = None
    source_native_allocations: tuple[SourceNativeAllocation, ...] = ()
    expected_next_source_native_creation_ordinal: int | None = None
    proposed_next_source_native_creation_ordinal: int | None = None
    accepted_source: LiveEnvelope | None = None
    attempt: FrozenLivePublicationAttempt | None = None

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

    @property
    def source_native_ids(self) -> tuple[str, ...]:
        return tuple(item.native_id for item in self.source_native_allocations)

    @property
    def accepted_envelope(self) -> LiveEnvelope | None:
        """Compatibility vocabulary for the exact CAS-accepted source body."""

        return self.accepted_source

    def acknowledge(self) -> bool:
        if not self.acknowledged:
            raise LiveContractError("indeterminate/rejected LIVE publication cannot be acknowledged")
        return True


_OWNER_ISSUED_CAS_RESULTS: dict[
    int, weakref.ReferenceType[LivePublicationResult]
] = {}


def _mark_owner_issued_cas_result(
    result: LivePublicationResult,
) -> LivePublicationResult:
    result_id = id(result)

    def remove(reference: weakref.ReferenceType[LivePublicationResult]) -> None:
        if _OWNER_ISSUED_CAS_RESULTS.get(result_id) is reference:
            _OWNER_ISSUED_CAS_RESULTS.pop(result_id, None)

    _OWNER_ISSUED_CAS_RESULTS[result_id] = weakref.ref(result, remove)
    return result


def _is_owner_issued_cas_result(result: LivePublicationResult) -> bool:
    reference = _OWNER_ISSUED_CAS_RESULTS.get(id(result))
    return reference is not None and reference() is result


def _result(
    status: LivePublicationStatus,
    attempt: FrozenLivePublicationAttempt,
    *,
    authoritative: bool,
    observed_source_revision: str | None = None,
    include_source_native_allocation: bool = False,
) -> LivePublicationResult:
    allocations = attempt.source_native_allocations if include_source_native_allocation else ()
    result = LivePublicationResult(
        status=status,
        source_key=attempt.source_key,
        authoritative=authoritative,
        observed_source_revision=observed_source_revision,
        source_native_allocations=allocations,
        expected_next_source_native_creation_ordinal=(
            attempt.expected_next_source_native_creation_ordinal
            if include_source_native_allocation
            else None
        ),
        proposed_next_source_native_creation_ordinal=(
            attempt.proposed_next_source_native_creation_ordinal
            if include_source_native_allocation
            else None
        ),
        accepted_source=(
            attempt.successor_route.entries[0]
            if status is LivePublicationStatus.ACCEPTED and authoritative
            else None
        ),
        attempt=attempt,
    )
    return _mark_owner_issued_cas_result(result)


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
    if attempt.source_native_allocations:
        if (
            acknowledgement.get("source_native_allocations")
            != [item.as_mapping() for item in attempt.source_native_allocations]
            or acknowledgement.get("expected_next_source_native_creation_ordinal")
            != attempt.expected_next_source_native_creation_ordinal
            or acknowledgement.get("proposed_next_source_native_creation_ordinal")
            != attempt.proposed_next_source_native_creation_ordinal
        ):
            return _result(LivePublicationStatus.INDETERMINATE, attempt, authoritative=False)
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
        include_source_native_allocation=True,
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
    selected = next(
        (entry for entry in attempt.selected_route.entries if entry.source_key == attempt.source_key),
        None,
    )
    if selected is None:
        raise LiveContractError("indeterminate attempt is not bound to a selected route source")
    predecessor = LiveEnvelope(
        campaign_id=attempt.source_key[0],
        scene_id=attempt.source_key[1],
        epoch_id=attempt.source_key[2],
        source_ref=attempt.target_ref,
        source_revision=attempt.expected_source_revision,
        claims=attempt.claims,
        status=attempt.source_status,
        opening_campaign_revision=selected.opening_campaign_revision,
        next_source_native_creation_ordinal=attempt.expected_next_source_native_creation_ordinal
        if attempt.source_native_allocations
        else selected.next_source_native_creation_ordinal,
        source_native_ids=selected.source_native_ids,
    )
    successor = attempt.successor_route.entries[0]
    if validate_exact_source(successor, current_source):
        return _result(
            LivePublicationStatus.ACCEPTED,
            attempt,
            authoritative=True,
            observed_source_revision=current_source.source_revision,
            include_source_native_allocation=True,
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
        opening_campaign_revision=source.opening_campaign_revision,
        next_source_native_creation_ordinal=source.next_source_native_creation_ordinal,
        source_native_ids=source.source_native_ids,
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
        opening_campaign_revision=source.opening_campaign_revision,
        next_source_native_creation_ordinal=source.next_source_native_creation_ordinal,
        source_native_ids=source.source_native_ids,
    )


class LiveAbsorptionStatus(StrEnum):
    """Phase-B campaign publication knowledge for one closed LIVE source."""

    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    REJECTED_STALE = "REJECTED_STALE"
    INDETERMINATE = "INDETERMINATE"
    CLOSED_UNABSORBED = "CLOSED_UNABSORBED"


def _absorbed_successor_route(route: LiveRouting, source_key: LiveSourceKey) -> LiveRouting:
    validate_live_route_completeness(route)
    selected = select_live_source(route, source_key)
    if selected is None:
        raise LiveContractError("absorption requires the exact selected LIVE route member")
    if selected.status not in {LiveLifecycle.CLOSED, LiveLifecycle.CLOSED_UNABSORBED}:
        raise LiveContractError("only a closed LIVE source can be absorbed")
    remaining = tuple(entry for entry in route.entries if entry.source_key != selected.source_key)
    return build_live_route(route.campaign_id, remaining)


def _absorption_marker(source: LiveEnvelope) -> dict[str, object]:
    return {
        "source_key": list(source.source_key),
        "source_revision": source.source_revision,
    }


def _absorption_closure(
    source: LiveEnvelope,
    proposed_campaign_revision: str,
    successor_route: LiveRouting,
) -> dict[str, object]:
    return {
        "source_key": list(source.source_key),
        "source_revision": source.source_revision,
        "campaign_revision": proposed_campaign_revision,
        "successor_route": successor_route.as_mapping(),
    }


def _source_native_history(source: LiveEnvelope) -> dict[str, object]:
    return {
        "source_key": list(source.source_key),
        "source_revision": source.source_revision,
        "next_source_native_creation_ordinal": source.next_source_native_creation_ordinal,
        "source_native_ids": list(source.source_native_ids),
    }


def _merge_absorbed_state(
    campaign_state: Mapping[str, object],
    packed_state: LiveNativeStatePack,
    source: LiveEnvelope,
    successor_route: LiveRouting,
    proposed_campaign_revision: str,
) -> dict[str, object]:
    candidate = deepcopy(dict(campaign_state))
    for field_name in (
        "native_owner_states",
        "provenance",
        "privacy",
        "chronology",
        "unresolved_work",
    ):
        incoming = deepcopy(dict(getattr(packed_state, field_name)))
        current = candidate.get(field_name)
        if current is None:
            candidate[field_name] = incoming
            continue
        if not isinstance(current, Mapping):
            raise LiveContractError(f"campaign absorption target {field_name} is not a mapping")
        merged = deepcopy(dict(current))
        for key, value in incoming.items():
            if key in merged and merged[key] != value:
                raise LiveContractError(
                    f"campaign absorption conflicts with current {field_name}.{key}"
                )
            merged[key] = value
        candidate[field_name] = merged

    marker = _absorption_marker(source)
    raw_markers = candidate.get("absorbed_live_sources", [])
    if not isinstance(raw_markers, Sequence) or isinstance(raw_markers, (str, bytes)):
        raise LiveContractError("campaign absorption marker set is not an explicit array")
    markers = [deepcopy(dict(item)) if isinstance(item, Mapping) else item for item in raw_markers]
    for existing in markers:
        if not isinstance(existing, Mapping):
            raise LiveContractError("campaign absorption marker is not typed")
        existing_key = existing.get("source_key")
        existing_revision = existing.get("source_revision")
        if existing_key == marker["source_key"] and existing_revision != marker["source_revision"]:
            raise LiveContractError("campaign absorption marker conflicts with the exact final source")
    if marker not in markers:
        markers.append(marker)
    candidate["absorbed_live_sources"] = markers
    candidate["last_absorbed_live_source"] = deepcopy(marker)
    candidate["live_routing"] = successor_route.as_mapping()

    history_entry = _source_native_history(source)
    raw_history = candidate.get("absorbed_live_source_native_history", [])
    if not isinstance(raw_history, Sequence) or isinstance(raw_history, (str, bytes)):
        raise LiveContractError("campaign source-native history is not an explicit array")
    history = [deepcopy(dict(item)) if isinstance(item, Mapping) else item for item in raw_history]
    for existing in history:
        if not isinstance(existing, Mapping):
            raise LiveContractError("campaign source-native history entry is not typed")
        if (
            existing.get("source_key") == history_entry["source_key"]
            and existing != history_entry
        ):
            raise LiveContractError("campaign source-native history conflicts with the exact source")
    if history_entry not in history:
        history.append(history_entry)
    candidate["absorbed_live_source_native_history"] = history

    closure = _absorption_closure(source, proposed_campaign_revision, successor_route)
    existing_closure = candidate.get("accepted_live_absorption")
    if existing_closure is not None and existing_closure != closure:
        raise LiveContractError("campaign accepted absorption closure conflicts with the exact retry")
    candidate["accepted_live_absorption"] = closure
    return candidate


@dataclass(frozen=True, slots=True)
class FrozenCampaignAbsorption:
    """Immutable campaign CAS candidate for one exact final LIVE source."""

    selected_route: LiveRouting
    source_key: LiveSourceKey
    source_revision: str
    expected_campaign_revision: str
    proposed_campaign_revision: str
    packed_state: LiveNativeStatePack
    candidate_state: Mapping[str, object]
    successor_route: LiveRouting

    def __post_init__(self) -> None:
        validate_live_route_completeness(self.selected_route)
        object.__setattr__(self, "source_key", _source_key(self.source_key))
        object.__setattr__(self, "source_revision", _revision(self.source_revision, "source_revision"))
        expected = _revision(self.expected_campaign_revision, "expected_campaign_revision")
        proposed = _revision(self.proposed_campaign_revision, "proposed_campaign_revision")
        if expected == proposed:
            raise LiveContractError("campaign absorption must advance its exact predecessor")
        object.__setattr__(self, "expected_campaign_revision", expected)
        object.__setattr__(self, "proposed_campaign_revision", proposed)
        if not isinstance(self.packed_state, LiveNativeStatePack):
            raise LiveContractError("campaign absorption requires a typed native state pack")
        if self.packed_state.source_key != self.source_key:
            raise LiveContractError("packed state source differs from absorption source")
        if self.packed_state.source_revision != self.source_revision:
            raise LiveContractError("packed state revision differs from final LIVE source")
        selected = select_live_source(self.selected_route, self.source_key)
        if selected is None or selected.status not in {
            LiveLifecycle.CLOSED,
            LiveLifecycle.CLOSED_UNABSORBED,
        }:
            raise LiveContractError("absorption attempt lacks the exact closed route member")
        if (
            selected.source_revision != self.source_revision
            or selected.next_source_native_creation_ordinal
            != self.packed_state.next_source_native_creation_ordinal
            or selected.source_native_ids != self.packed_state.source_native_ids
        ):
            raise LiveContractError("absorption attempt source-native history differs from the route")
        if not isinstance(self.candidate_state, Mapping):
            raise LiveContractError("campaign absorption candidate must be a mapping")
        validate_live_route_completeness(self.successor_route)
        expected_successor = _absorbed_successor_route(self.selected_route, self.source_key)
        if self.successor_route.as_mapping() != expected_successor.as_mapping():
            raise LiveContractError("absorption attempt successor route has wrong membership")
        object.__setattr__(self, "candidate_state", deepcopy(dict(self.candidate_state)))

    @property
    def candidate_state_digest(self) -> str:
        return _state_digest(self.candidate_state)

    def as_mapping(self) -> dict[str, object]:
        return {
            "schema_version": LIVE_ABSORPTION_ATTEMPT_SCHEMA_VERSION,
            "kind": "runtime.live_absorption_attempt",
            "source_key": list(self.source_key),
            "source_revision": self.source_revision,
            "next_source_native_creation_ordinal": self.packed_state.next_source_native_creation_ordinal,
            "source_native_ids": list(self.packed_state.source_native_ids),
            "expected_campaign_revision": self.expected_campaign_revision,
            "proposed_campaign_revision": self.proposed_campaign_revision,
            "candidate_state_digest": self.candidate_state_digest,
            "selected_route": self.selected_route.as_mapping(),
            "successor_route": self.successor_route.as_mapping(),
        }


def freeze_campaign_absorption(
    source: LiveEnvelope,
    *,
    route: LiveRouting,
    packed_state: LiveNativeStatePack,
    campaign_state: Mapping[str, object],
    expected_campaign_revision: str,
    proposed_campaign_revision: str,
) -> FrozenCampaignAbsorption:
    """Freeze phase-B materialization; publication remains a separate exact CAS."""

    if not isinstance(source, LiveEnvelope):
        raise LiveContractError("campaign absorption requires an owner-typed source")
    if source.status not in {LiveLifecycle.CLOSED, LiveLifecycle.CLOSED_UNABSORBED}:
        raise LiveContractError("campaign absorption requires a closed LIVE source")
    if not isinstance(packed_state, LiveNativeStatePack):
        raise LiveContractError("campaign absorption requires a typed native state pack")
    if packed_state.source_key != source.source_key or packed_state.source_revision != source.source_revision:
        raise LiveContractError("packed state is not the exact final LIVE source")
    if not isinstance(campaign_state, Mapping):
        raise LiveContractError("campaign absorption target must be a mapping")
    selected = select_live_source(route, source.source_key)
    if selected is None or not validate_exact_source(selected, source):
        raise LiveContractError("campaign absorption requires exact selected LIVE route evidence")
    successor_route = _absorbed_successor_route(route, source.source_key)
    candidate = _merge_absorbed_state(
        campaign_state,
        packed_state,
        source,
        successor_route,
        proposed_campaign_revision,
    )
    return FrozenCampaignAbsorption(
        selected_route=route,
        source_key=source.source_key,
        source_revision=source.source_revision,
        expected_campaign_revision=expected_campaign_revision,
        proposed_campaign_revision=proposed_campaign_revision,
        packed_state=packed_state,
        candidate_state=candidate,
        successor_route=successor_route,
    )


@dataclass(frozen=True, slots=True, weakref_slot=True)
class LiveAbsorptionPublication:
    """Typed result of exact campaign CAS classification."""

    status: LiveAbsorptionStatus
    source_key: LiveSourceKey
    source_revision: str
    authoritative: bool
    candidate_state: Mapping[str, object] | None = None
    successor_route: LiveRouting | None = None
    attempt: FrozenCampaignAbsorption | None = None

    @property
    def acknowledged(self) -> bool:
        return self.status is LiveAbsorptionStatus.ACCEPTED and self.authoritative


_OWNER_ISSUED_ABSORPTION_RESULTS: dict[
    int, weakref.ReferenceType[LiveAbsorptionPublication]
] = {}


def _mark_owner_issued_absorption_result(
    result: LiveAbsorptionPublication,
) -> LiveAbsorptionPublication:
    result_id = id(result)

    def remove(reference: weakref.ReferenceType[LiveAbsorptionPublication]) -> None:
        if _OWNER_ISSUED_ABSORPTION_RESULTS.get(result_id) is reference:
            _OWNER_ISSUED_ABSORPTION_RESULTS.pop(result_id, None)

    _OWNER_ISSUED_ABSORPTION_RESULTS[result_id] = weakref.ref(result, remove)
    return result


def _is_owner_issued_absorption_result(result: LiveAbsorptionPublication) -> bool:
    reference = _OWNER_ISSUED_ABSORPTION_RESULTS.get(id(result))
    return reference is not None and reference() is result


def classify_campaign_absorption(
    attempt: FrozenCampaignAbsorption,
    acknowledgement: Mapping[str, object] | None,
) -> LiveAbsorptionPublication:
    """Classify campaign absorption only from complete exact-CAS evidence."""

    if not isinstance(attempt, FrozenCampaignAbsorption):
        raise LiveContractError("campaign absorption classification requires a frozen attempt")
    if acknowledgement is None or not isinstance(acknowledgement, Mapping):
        return _mark_owner_issued_absorption_result(LiveAbsorptionPublication(
            LiveAbsorptionStatus.INDETERMINATE,
            attempt.source_key,
            attempt.source_revision,
            False,
            attempt=attempt,
        ))
    raw_key = acknowledgement.get("source_key")
    try:
        if raw_key is None or _source_key(raw_key) != attempt.source_key:
            return _mark_owner_issued_absorption_result(LiveAbsorptionPublication(
                LiveAbsorptionStatus.REJECTED_STALE,
                attempt.source_key,
                attempt.source_revision,
                False,
                attempt=attempt,
            ))
    except LiveContractError:
        return _mark_owner_issued_absorption_result(LiveAbsorptionPublication(
            LiveAbsorptionStatus.REJECTED_STALE,
            attempt.source_key,
            attempt.source_revision,
            False,
            attempt=attempt,
        ))
    accepted = acknowledgement.get("accepted") is True or str(
        acknowledgement.get("status", "")
    ).upper() in {"ACCEPTED", "CONFIRMED_ACCEPTED"}
    if not accepted:
        current = acknowledgement.get("current_campaign_revision")
        status = (
            LiveAbsorptionStatus.REJECTED_STALE
            if current is not None and current != attempt.expected_campaign_revision
            else LiveAbsorptionStatus.REJECTED
        )
        return _mark_owner_issued_absorption_result(LiveAbsorptionPublication(
            status,
            attempt.source_key,
            attempt.source_revision,
            False,
            attempt=attempt,
        ))
    required = {
        "source_revision": attempt.source_revision,
        "expected_campaign_revision": attempt.expected_campaign_revision,
        "new_campaign_revision": attempt.proposed_campaign_revision,
        "candidate_state_digest": attempt.candidate_state_digest,
        "selected_route": attempt.selected_route.as_mapping(),
        "successor_route": attempt.successor_route.as_mapping(),
    }
    if any(acknowledgement.get(key) != value for key, value in required.items()):
        return _mark_owner_issued_absorption_result(LiveAbsorptionPublication(
            LiveAbsorptionStatus.INDETERMINATE,
            attempt.source_key,
            attempt.source_revision,
            False,
            attempt=attempt,
        ))
    return _mark_owner_issued_absorption_result(LiveAbsorptionPublication(
        LiveAbsorptionStatus.ACCEPTED,
        attempt.source_key,
        attempt.source_revision,
        True,
        candidate_state=attempt.candidate_state,
        successor_route=attempt.successor_route,
        attempt=attempt,
    ))


@dataclass(frozen=True, slots=True)
class LiveAbsorptionResult:
    """Phase-B result retaining closed-unabsorbed truth on every non-acceptance."""

    status: LiveAbsorptionStatus
    source: LiveEnvelope
    route: LiveRouting
    campaign_state: Mapping[str, object]
    authoritative: bool

    @property
    def absorbed(self) -> bool:
        return self.status is LiveAbsorptionStatus.ACCEPTED and self.authoritative


def _absorption_result_from_publication(
    publication: LiveAbsorptionPublication,
    source: LiveEnvelope,
    route: LiveRouting,
    campaign_state: Mapping[str, object],
) -> LiveAbsorptionResult:
    retained = source if source.status is LiveLifecycle.CLOSED_UNABSORBED else mark_closed_unabsorbed(source)
    return LiveAbsorptionResult(
        status=(
            LiveAbsorptionStatus.CLOSED_UNABSORBED
            if publication.status is not LiveAbsorptionStatus.ACCEPTED
            else publication.status
        ),
        source=retained,
        route=route,
        campaign_state=deepcopy(dict(campaign_state)),
        authoritative=False,
    )


def absorb_live_state(
    source: LiveEnvelope,
    packed_state: LiveNativeStatePack,
    campaign_state: Mapping[str, object],
    *,
    route: LiveRouting,
    publication: LiveAbsorptionPublication | Mapping[str, object] | None,
    expected_campaign_revision: str | None = None,
    proposed_campaign_revision: str | None = None,
) -> LiveAbsorptionResult:
    """Apply one accepted campaign absorption, or retain CLOSED_UNABSORBED truth."""

    if not isinstance(source, LiveEnvelope):
        raise LiveContractError("LIVE absorption requires an owner-typed source")
    if not isinstance(packed_state, LiveNativeStatePack):
        raise LiveContractError("LIVE absorption requires a typed native state pack")
    if packed_state.source_key != source.source_key or packed_state.source_revision != source.source_revision:
        raise LiveContractError("absorption pack does not match the exact final source")
    if not isinstance(campaign_state, Mapping):
        raise LiveContractError("LIVE absorption target must be a mapping")
    if not isinstance(route, LiveRouting):
        raise LiveContractError("LIVE absorption requires a typed route closure")

    if source.status is LiveLifecycle.ABSORBED:
        if (
            not isinstance(publication, LiveAbsorptionPublication)
            or not publication.acknowledged
            or not _is_owner_issued_absorption_result(publication)
        ):
            raise LiveContractError("absorbed LIVE source requires its accepted absorption evidence")
        attempt = publication.attempt
        if (
            not isinstance(attempt, FrozenCampaignAbsorption)
            or attempt.source_key != source.source_key
            or attempt.source_revision != source.source_revision
            or attempt.packed_state != packed_state
            or publication.successor_route is None
            or publication.successor_route.as_mapping() != route.as_mapping()
        ):
            raise LiveContractError("absorbed retry is not bound to the stored route closure")
        expected_closure = _absorption_closure(
            source,
            attempt.proposed_campaign_revision,
            publication.successor_route,
        )
        if campaign_state.get("accepted_live_absorption") != expected_closure:
            raise LiveContractError("absorbed retry lacks the stored accepted campaign closure")
        if campaign_state.get("live_routing") != expected_closure["successor_route"]:
            raise LiveContractError("absorbed retry lacks the stored accepted route closure")
        history = campaign_state.get("absorbed_live_source_native_history")
        if not isinstance(history, Sequence) or isinstance(history, (str, bytes)):
            raise LiveContractError("absorbed retry lacks stored source-native history")
        if _source_native_history(source) not in history:
            raise LiveContractError("absorbed retry lacks the exact stored source-native history")
        if (
            publication.candidate_state is None
            or publication.candidate_state.get("accepted_live_absorption") != expected_closure
        ):
            raise LiveContractError("absorbed retry evidence differs from the stored campaign closure")
        marker = campaign_state.get("last_absorbed_live_source")
        if marker != _absorption_marker(source):
            raise LiveContractError("absorbed LIVE source lacks exact campaign absorption marker")
        return LiveAbsorptionResult(
            LiveAbsorptionStatus.ACCEPTED,
            source,
            route,
            deepcopy(dict(campaign_state)),
            True,
        )
    if source.status not in {LiveLifecycle.CLOSED, LiveLifecycle.CLOSED_UNABSORBED}:
        raise LiveContractError("only CLOSED or CLOSED_UNABSORBED LIVE sources can be absorbed")
    validate_live_route_completeness(route)
    selected = select_live_source(route, source.source_key)
    if selected is None or not validate_exact_source(selected, source):
        raise LiveContractError("absorption requires the exact selected LIVE route body")

    if publication is None:
        retained = source if source.status is LiveLifecycle.CLOSED_UNABSORBED else mark_closed_unabsorbed(source)
        return LiveAbsorptionResult(
            LiveAbsorptionStatus.CLOSED_UNABSORBED,
            retained,
            route,
            deepcopy(dict(campaign_state)),
            False,
        )
    if isinstance(publication, Mapping):
        if expected_campaign_revision is None or proposed_campaign_revision is None:
            raise LiveContractError("mapping absorption evidence requires exact campaign revisions")
        attempt = freeze_campaign_absorption(
            source,
            route=route,
            packed_state=packed_state,
            campaign_state=campaign_state,
            expected_campaign_revision=expected_campaign_revision,
            proposed_campaign_revision=proposed_campaign_revision,
        )
        typed_publication = classify_campaign_absorption(attempt, publication)
    elif isinstance(publication, LiveAbsorptionPublication):
        typed_publication = publication
        if not _is_owner_issued_absorption_result(typed_publication):
            raise LiveContractError("absorption requires owner-issued CAS evidence")
    else:
        raise LiveContractError("campaign absorption publication evidence is not typed")
    if not typed_publication.acknowledged:
        return _absorption_result_from_publication(typed_publication, source, route, campaign_state)
    if not _is_owner_issued_absorption_result(typed_publication):
        raise LiveContractError("accepted absorption requires owner-issued CAS evidence")
    if typed_publication.attempt is None:
        raise LiveContractError("accepted absorption evidence is not bound to this source")
    attempt = typed_publication.attempt
    if (
        attempt.source_key != source.source_key
        or attempt.source_revision != source.source_revision
        or attempt.packed_state != packed_state
        or attempt.selected_route.as_mapping() != route.as_mapping()
    ):
        raise LiveContractError("accepted absorption evidence is not bound to the exact source and route")
    if typed_publication.candidate_state is None or typed_publication.successor_route is None:
        raise LiveContractError("accepted absorption evidence lacks complete campaign closure")
    expected_successor = _absorbed_successor_route(route, source.source_key)
    if typed_publication.successor_route.as_mapping() != expected_successor.as_mapping():
        raise LiveContractError("accepted absorption evidence has wrong route membership")
    expected_closure = _absorption_closure(
        source,
        attempt.proposed_campaign_revision,
        expected_successor,
    )
    if typed_publication.candidate_state.get("accepted_live_absorption") != expected_closure:
        raise LiveContractError("accepted absorption evidence lacks the stored campaign closure")
    absorbed_source = LiveEnvelope(
        campaign_id=source.campaign_id,
        scene_id=source.scene_id,
        epoch_id=source.epoch_id,
        source_ref=source.source_ref,
        source_revision=source.source_revision,
        claims=source.claims,
        status=LiveLifecycle.ABSORBED,
        opening_campaign_revision=source.opening_campaign_revision,
        next_source_native_creation_ordinal=source.next_source_native_creation_ordinal,
        source_native_ids=source.source_native_ids,
    )
    return LiveAbsorptionResult(
        LiveAbsorptionStatus.ACCEPTED,
        absorbed_source,
        expected_successor,
        deepcopy(dict(typed_publication.candidate_state)),
        True,
    )


def recover_closed_unabsorbed(
    route: LiveRouting,
    source_key: LiveSourceKey,
) -> LiveEnvelope:
    """Recover selected LIVE truth without falling back to campaign state."""

    validate_live_route_completeness(route)
    selected = select_live_source(route, source_key)
    if selected is None:
        raise LiveContractError("selected LIVE source is missing; campaign fallback is forbidden")
    if selected.status is LiveLifecycle.CLOSED:
        return mark_closed_unabsorbed(selected)
    if selected.status is not LiveLifecycle.CLOSED_UNABSORBED:
        raise LiveContractError("selected LIVE source is not closed-unabsorbed recovery truth")
    return selected


# Compatibility names for the owner-local contract vocabulary.  These aliases
# do not create another authority or another representation.
LiveRoute = LiveRouting
LiveSource = LiveEnvelope
LivePublicationAttempt = FrozenLivePublicationAttempt
LivePublicationOutcome = LivePublicationResult
