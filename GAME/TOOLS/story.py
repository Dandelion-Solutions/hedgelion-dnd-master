"""Bounded noncanonical Story projection helpers over native semantic history."""

from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Final

from GAME.TOOLS.history import (
    HistoryContractError,
    validate_semantic_event_draft,
    validate_t0_basis,
)

STORY_ROOT = "STORY"
_STORY_ID = re.compile(r"^(?P<prefix>[TEMN])(?P<sequence>[0-9]{6,})$")
_PREFIX_LAYERS = {"T": "TRANSCRIPT", "E": "EVENTS", "M": "MECHANICS", "N": "NARRATIVE"}
_LOCAL_SOURCE_KEY = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
_LIVE_ORIGIN = re.compile(r"^LIVE:[A-Za-z0-9_.:-]+$")

# framework_module_version: 1.0.1
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.1"


class StoryIdentityComponent(StrEnum):
    TEXT = "TEXT"
    POSITIVE_INTEGER = "POSITIVE_INTEGER"
    TERMINAL = "TERMINAL"


class StoryRequirementPolicy(StrEnum):
    MUST_MATERIALIZE = "MUST_MATERIALIZE"
    MAY_OMIT = "MAY_OMIT"
    SOURCE_CLASSIFIED = "SOURCE_CLASSIFIED"


class StoryCardinalityPolicy(StrEnum):
    ZERO_OR_ONE_PER_CANDIDATE = "ZERO_OR_ONE_PER_CANDIDATE"
    EXACTLY_ONE_PER_CANDIDATE = "EXACTLY_ONE_PER_CANDIDATE"
    ONE_OR_MORE_PER_CANDIDATE = "ONE_OR_MORE_PER_CANDIDATE"


@dataclass(frozen=True, slots=True)
class StorySourceRegistration:
    """One closed generation-1 layer/source projection contract."""

    registration_id: str
    layer: str
    source_domain_prefix: str
    lane: str
    identity_codec: tuple[StoryIdentityComponent, ...]
    requirement_policy: StoryRequirementPolicy
    cardinality_policy: StoryCardinalityPolicy
    omission_codes: tuple[str, ...]
    semantic_contract_generation: int = 1


STORY_SOURCE_REGISTRATIONS: Final[Mapping[str, StorySourceRegistration]] = (
    MappingProxyType(
        {
            registration.registration_id: registration
            for registration in (
                StorySourceRegistration(
                    "T-MSG",
                    "TRANSCRIPT",
                    "campaign.participant_messages@",
                    "msg",
                    (StoryIdentityComponent.TEXT,),
                    StoryRequirementPolicy.MAY_OMIT,
                    StoryCardinalityPolicy.ZERO_OR_ONE_PER_CANDIDATE,
                    ("OPTIONAL_TRANSCRIPT",),
                ),
                StorySourceRegistration(
                    "T-ARC",
                    "TRANSCRIPT",
                    "campaign.transcript_archival_requests@",
                    "arc",
                    (
                        StoryIdentityComponent.TEXT,
                        StoryIdentityComponent.TEXT,
                        StoryIdentityComponent.POSITIVE_INTEGER,
                    ),
                    StoryRequirementPolicy.MUST_MATERIALIZE,
                    StoryCardinalityPolicy.EXACTLY_ONE_PER_CANDIDATE,
                    (),
                ),
                StorySourceRegistration(
                    "E-EVT",
                    "EVENTS",
                    "campaign.semantic_events@",
                    "evt",
                    (StoryIdentityComponent.TEXT,),
                    StoryRequirementPolicy.SOURCE_CLASSIFIED,
                    StoryCardinalityPolicy.ONE_OR_MORE_PER_CANDIDATE,
                    ("TECHNICAL_ONLY_EVENT",),
                ),
                StorySourceRegistration(
                    "E-REL",
                    "EVENTS",
                    "campaign.semantic_relations@",
                    "rel",
                    (
                        StoryIdentityComponent.TEXT,
                        StoryIdentityComponent.TEXT,
                        StoryIdentityComponent.TEXT,
                    ),
                    StoryRequirementPolicy.MUST_MATERIALIZE,
                    StoryCardinalityPolicy.ONE_OR_MORE_PER_CANDIDATE,
                    (),
                ),
                StorySourceRegistration(
                    "M-SEG",
                    "MECHANICS",
                    "campaign.mechanical_segments@",
                    "seg",
                    (
                        StoryIdentityComponent.TEXT,
                        StoryIdentityComponent.TEXT,
                        StoryIdentityComponent.POSITIVE_INTEGER,
                    ),
                    StoryRequirementPolicy.SOURCE_CLASSIFIED,
                    StoryCardinalityPolicy.ONE_OR_MORE_PER_CANDIDATE,
                    ("EXECUTION_BOOKKEEPING_ONLY",),
                ),
                StorySourceRegistration(
                    "M-OUT",
                    "MECHANICS",
                    "campaign.mechanical_outcomes@",
                    "out",
                    (
                        StoryIdentityComponent.TEXT,
                        StoryIdentityComponent.TEXT,
                        StoryIdentityComponent.TERMINAL,
                    ),
                    StoryRequirementPolicy.SOURCE_CLASSIFIED,
                    StoryCardinalityPolicy.ONE_OR_MORE_PER_CANDIDATE,
                    ("NO_GAMEPLAY_OUTCOME",),
                ),
                StorySourceRegistration(
                    "N-EVT",
                    "NARRATIVE",
                    "campaign.semantic_events@",
                    "evt",
                    (StoryIdentityComponent.TEXT,),
                    StoryRequirementPolicy.SOURCE_CLASSIFIED,
                    StoryCardinalityPolicy.ONE_OR_MORE_PER_CANDIDATE,
                    ("TECHNICAL_ONLY_EVENT",),
                ),
                StorySourceRegistration(
                    "N-REL",
                    "NARRATIVE",
                    "campaign.semantic_relations@",
                    "rel",
                    (
                        StoryIdentityComponent.TEXT,
                        StoryIdentityComponent.TEXT,
                        StoryIdentityComponent.TEXT,
                    ),
                    StoryRequirementPolicy.MUST_MATERIALIZE,
                    StoryCardinalityPolicy.ONE_OR_MORE_PER_CANDIDATE,
                    (),
                ),
            )
        }
    )
)

STORY_UNIT_SCHEMA_VERSIONS: Final[Mapping[str, int]] = MappingProxyType(
    {
        "TRANSCRIPT": 1,
        "EVENTS": 2,
        "MECHANICS": 2,
        "NARRATIVE": 2,
    }
)
STORY_PROJECTION_STATE_SCHEMA_VERSION: Final[int] = 2


class StoryContractError(ValueError):
    """Raised when an owner-local Story projection violates its boundary."""


def story_source_registration(registration_id: object) -> StorySourceRegistration:
    if not isinstance(registration_id, str):
        raise StoryContractError("Story source registration must be text")
    registration = STORY_SOURCE_REGISTRATIONS.get(registration_id)
    if registration is None:
        raise StoryContractError("Story source registration is not admitted")
    return registration


def _origin_scope(value: object) -> str:
    origin = _nonempty_string(value, "Story native origin")
    if origin != "LOCAL" and _LIVE_ORIGIN.fullmatch(origin) is None:
        raise StoryContractError("Story origin must be LOCAL or a native LIVE epoch")
    return origin


def _encode_origin_scope(origin: str) -> str:
    safe = frozenset(
        b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
    )
    return "".join(
        chr(byte) if byte in safe else f"%{byte:02X}" for byte in origin.encode("utf-8")
    )


def _decode_origin_scope(value: str) -> str:
    raw = bytearray()
    index = 0
    while index < len(value):
        character = value[index]
        if character == "%":
            if (
                index + 2 >= len(value)
                or re.fullmatch(r"[0-9A-F]{2}", value[index + 1 : index + 3]) is None
            ):
                raise StoryContractError(
                    "Story source-domain scope escape is not canonical"
                )
            raw.append(int(value[index + 1 : index + 3], 16))
            index += 3
            continue
        if not character.isascii() or not (character.isalnum() or character in "-._~"):
            raise StoryContractError(
                "Story source-domain scope is not canonically encoded"
            )
        raw.append(ord(character))
        index += 1
    try:
        origin = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StoryContractError("Story source-domain scope is not UTF-8") from exc
    if _encode_origin_scope(_origin_scope(origin)) != value:
        raise StoryContractError("Story source-domain scope is not canonical")
    return origin


def story_source_domain(registration_id: object, origin: object) -> str:
    registration = story_source_registration(registration_id)
    return registration.source_domain_prefix + _encode_origin_scope(
        _origin_scope(origin)
    )


def _identity_component(value: object, component: StoryIdentityComponent) -> str | int:
    if component is StoryIdentityComponent.TEXT:
        if not isinstance(value, str) or not value:
            raise StoryContractError(
                "candidate identity component must be nonempty text"
            )
        try:
            value.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise StoryContractError(
                "candidate identity cannot contain an isolated surrogate"
            ) from exc
        return value
    if component is StoryIdentityComponent.POSITIVE_INTEGER:
        if type(value) is not int or value < 1:
            raise StoryContractError(
                "candidate identity ordinal must be a positive integer"
            )
        return value
    if component is StoryIdentityComponent.TERMINAL:
        if value != "terminal":
            raise StoryContractError(
                "terminal outcome identity component must be terminal"
            )
        return "terminal"
    raise StoryContractError("candidate identity codec is not registered")


def encode_candidate_id(registration_id: object, identity: object) -> str:
    registration = story_source_registration(registration_id)
    if not isinstance(identity, Sequence) or isinstance(identity, (str, bytes)):
        raise StoryContractError("candidate identity must be an array")
    if len(identity) != len(registration.identity_codec):
        raise StoryContractError("candidate identity has the wrong component count")
    parts = [
        _identity_component(value, component)
        for value, component in zip(identity, registration.identity_codec, strict=True)
    ]
    return json.dumps(parts, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def decode_candidate_id(
    registration_id: object, candidate_id: object
) -> tuple[str | int, ...]:
    if not isinstance(candidate_id, str) or not candidate_id:
        raise StoryContractError("candidate identity codec must be nonempty text")
    try:
        parts = json.loads(candidate_id)
    except json.JSONDecodeError as exc:
        raise StoryContractError("candidate identity is not canonical JSON") from exc
    if not isinstance(parts, list):
        raise StoryContractError("candidate identity must encode a JSON array")
    normalized = encode_candidate_id(registration_id, parts)
    if normalized != candidate_id:
        raise StoryContractError("candidate identity spelling is not canonical")
    return tuple(parts)


def encode_candidate_cursor(registration_id: object, ordinal: object) -> str:
    registration = story_source_registration(registration_id)
    if type(ordinal) is not int or ordinal < 1:
        raise StoryContractError("Story source ordinal must be a positive integer")
    return f"{registration.lane}:{ordinal}"


def decode_candidate_cursor(registration_id: object, cursor: object) -> int:
    registration = story_source_registration(registration_id)
    if not isinstance(cursor, str):
        raise StoryContractError("Story source cursor must be text")
    prefix = registration.lane + ":"
    if not cursor.startswith(prefix):
        raise StoryContractError("Story source cursor belongs to another lane")
    digits = cursor[len(prefix) :]
    if not digits.isascii() or not digits.isdecimal() or digits.startswith("0"):
        raise StoryContractError(
            "Story source cursor is not canonical positive decimal"
        )
    ordinal = int(digits)
    if ordinal < 1 or encode_candidate_cursor(registration_id, ordinal) != cursor:
        raise StoryContractError("Story source cursor is not canonical")
    return ordinal


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise StoryContractError(f"{label} must be an object")
    return value


def _nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise StoryContractError(f"{label} must be a nonempty string")
    return value


def _unique_strings(value: object, label: str) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise StoryContractError(f"{label} must be an array")
    items = [_nonempty_string(item, label) for item in value]
    if not items or len(items) != len(set(items)):
        raise StoryContractError(f"{label} must be nonempty and unique")
    return items


def _string_array(value: object, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise StoryContractError(f"{label} must be an array")
    items = [_nonempty_string(item, label) for item in value]
    if (not allow_empty and not items) or len(items) != len(set(items)):
        raise StoryContractError(
            f"{label} must be unique{'' if allow_empty else ' and nonempty'}"
        )
    return items


def _plain_json(value: object, label: str) -> object:
    if value is None or type(value) in {str, bool, int}:
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise StoryContractError(f"{label} must not contain a non-finite number")
        return value
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise StoryContractError(f"{label} object keys must be strings")
        return {key: _plain_json(item, label) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [_plain_json(item, label) for item in value]
    raise StoryContractError(f"{label} must contain JSON-compatible values")


def _native_ref(value: object, label: str) -> dict[str, object]:
    reference = _mapping(value, label)
    if set(reference) - {"family", "identity", "selector"} or not {
        "family",
        "identity",
    }.issubset(reference):
        raise StoryContractError(f"{label} fields are not strict")
    raw_identity = reference["identity"]
    if not isinstance(raw_identity, Sequence) or isinstance(raw_identity, (str, bytes)):
        raise StoryContractError(f"{label} identity must be an array")
    identity = [
        _nonempty_string(part, f"{label} identity component") for part in raw_identity
    ]
    if not identity:
        raise StoryContractError(f"{label} identity cannot be empty")
    normalized: dict[str, object] = {
        "family": _nonempty_string(reference["family"], f"{label} family"),
        "identity": identity,
    }
    if "selector" in reference:
        normalized["selector"] = _plain_json(reference["selector"], f"{label} selector")
    return normalized


def _native_ref_array(value: object, label: str) -> list[dict[str, object]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise StoryContractError(f"{label} must be an array")
    refs = [_native_ref(item, label) for item in value]
    identities = [
        json.dumps(ref, sort_keys=True, separators=(",", ":")) for ref in refs
    ]
    if len(identities) != len(set(identities)):
        raise StoryContractError(f"{label} must be unique")
    return refs


def _source_dependencies(value: object) -> dict[str, dict[str, object]]:
    sources = _mapping(value, "Story sources")
    if not sources:
        raise StoryContractError("Story sources must be nonempty")
    normalized: dict[str, dict[str, object]] = {}
    for key, raw_dependency in sources.items():
        if not isinstance(key, str) or _LOCAL_SOURCE_KEY.fullmatch(key) is None:
            raise StoryContractError("Story source key is not canonical")
        dependency = _mapping(raw_dependency, "Story source dependency")
        if set(dependency) - {"ref", "basis"} or "ref" not in dependency:
            raise StoryContractError("Story source dependency fields are not strict")
        item: dict[str, object] = {"ref": _native_ref(dependency["ref"], "source ref")}
        if "basis" in dependency:
            item["basis"] = _plain_json(dependency["basis"], "source basis")
        normalized[key] = item
    return normalized


def _story_ref_array(value: object, label: str) -> list[str]:
    refs = _string_array(value, label, allow_empty=True)
    for ref in refs:
        _story_layer(ref)
    return refs


def _registration_for_domain(
    layer: str, source_domain: object
) -> StorySourceRegistration:
    domain = _nonempty_string(source_domain, "source_domain")
    matches = tuple(
        registration
        for registration in STORY_SOURCE_REGISTRATIONS.values()
        if registration.layer == layer
        and domain.startswith(registration.source_domain_prefix)
    )
    if len(matches) != 1:
        raise StoryContractError("source domain is not registered for this Story layer")
    registration = matches[0]
    origin = _decode_origin_scope(
        domain.removeprefix(registration.source_domain_prefix)
    )
    if story_source_domain(registration.registration_id, origin) != domain:
        raise StoryContractError("source domain is not canonical")
    return registration


def validate_story_unit(value: object, *, layer: str) -> dict[str, object]:
    """Validate one canonical common-envelope StoryUnit for its fixed layer."""
    if layer not in STORY_UNIT_SCHEMA_VERSIONS:
        raise StoryContractError("Story layer is not registered")
    unit = _mapping(value, "Story unit")
    required = {
        "schema_version",
        "story_id",
        "content",
        "sources",
        "projection_basis",
        "availability",
        "payload",
    }
    optional = {
        "entity_refs",
        "cross_refs",
        "temporal_source_keys",
        "causal_source_keys",
    }
    if not required.issubset(unit) or set(unit) - required - optional:
        raise StoryContractError("Story unit fields are not strict")
    version = unit["schema_version"]
    if type(version) is not int or version != STORY_UNIT_SCHEMA_VERSIONS[layer]:
        raise StoryContractError("unsupported Story unit schema version")
    actual_layer, _sequence = _story_layer(unit["story_id"])
    if actual_layer != layer:
        raise StoryContractError("Story ID prefix does not match the requested layer")

    content = _mapping(unit["content"], "Story content")
    if set(content) - {"body", "title"} or "body" not in content:
        raise StoryContractError("Story content fields are not strict")
    normalized_content: dict[str, object] = {
        "body": _nonempty_string(content["body"], "Story body")
    }
    if "title" in content:
        normalized_content["title"] = _nonempty_string(content["title"], "Story title")

    sources = _source_dependencies(unit["sources"])
    raw_contributions = unit["projection_basis"]
    if (
        not isinstance(raw_contributions, Sequence)
        or isinstance(raw_contributions, (str, bytes))
        or not raw_contributions
    ):
        raise StoryContractError("projection_basis must be a nonempty array")
    contributions: list[dict[str, object]] = []
    contribution_registrations: list[StorySourceRegistration] = []
    for raw_contribution in raw_contributions:
        contribution = _mapping(raw_contribution, "ProjectionContribution")
        if set(contribution) != {
            "source_domain",
            "semantic_contract_generation",
            "candidate_ids",
        }:
            raise StoryContractError("ProjectionContribution fields are not strict")
        registration = _registration_for_domain(layer, contribution["source_domain"])
        contribution_registrations.append(registration)
        generation = contribution["semantic_contract_generation"]
        if (
            type(generation) is not int
            or generation != registration.semantic_contract_generation
        ):
            raise StoryContractError("unsupported Story semantic contract generation")
        candidate_ids = _unique_strings(
            contribution["candidate_ids"], "projection candidate_ids"
        )
        for candidate_id in candidate_ids:
            decode_candidate_id(registration.registration_id, candidate_id)
        if (
            registration.cardinality_policy
            in {
                StoryCardinalityPolicy.ZERO_OR_ONE_PER_CANDIDATE,
                StoryCardinalityPolicy.EXACTLY_ONE_PER_CANDIDATE,
            }
            and len(candidate_ids) != 1
        ):
            raise StoryContractError(
                "this Story registration cannot merge candidate identities"
            )
        contributions.append(
            {
                "source_domain": registration.source_domain_prefix
                + _encode_origin_scope(
                    _decode_origin_scope(
                        contribution["source_domain"].removeprefix(
                            registration.source_domain_prefix
                        )
                    )
                ),
                "semantic_contract_generation": generation,
                "candidate_ids": candidate_ids,
            }
        )
    if (
        layer == "TRANSCRIPT"
        and sum(
            len(contribution["candidate_ids"])
            for registration, contribution in zip(
                contribution_registrations, contributions, strict=True
            )
            if registration.registration_id == "T-MSG"
        )
        > 1
    ):
        raise StoryContractError(
            "TRANSCRIPT cannot combine distinct message candidates"
        )

    availability = _mapping(unit["availability"], "Story availability")
    if set(availability) - {"requires_story_refs", "requires_source_refs"} or (
        "requires_story_refs" not in availability
    ):
        raise StoryContractError("Story availability fields are not strict")
    normalized_availability: dict[str, object] = {
        "requires_story_refs": _story_ref_array(
            availability["requires_story_refs"], "requires_story_refs"
        )
    }
    if "requires_source_refs" in availability:
        normalized_availability["requires_source_refs"] = _native_ref_array(
            availability["requires_source_refs"], "requires_source_refs"
        )

    payload = _mapping(unit["payload"], "Story payload")
    if layer == "TRANSCRIPT":
        allowed = {
            "message_source_key",
            "speaker",
            "recipient_refs",
            "interaction_ref",
            "exact_text_ref",
        }
        if set(payload) - allowed or not {"message_source_key", "speaker"}.issubset(
            payload
        ):
            raise StoryContractError("TRANSCRIPT payload fields are not strict")
        message_key = _nonempty_string(
            payload["message_source_key"], "message_source_key"
        )
        if message_key not in sources:
            raise StoryContractError("TRANSCRIPT message source key is unbound")
        speaker = _mapping(payload["speaker"], "TRANSCRIPT speaker")
        if speaker.get("kind") == "ENTITY" and set(speaker) == {"kind", "ref"}:
            normalized_speaker = {
                "kind": "ENTITY",
                "ref": _native_ref(speaker["ref"], "speaker ref"),
            }
        elif speaker.get("kind") == "ROLE" and set(speaker) == {"kind", "role"}:
            normalized_speaker = {
                "kind": "ROLE",
                "role": _nonempty_string(speaker["role"], "speaker role"),
            }
        else:
            raise StoryContractError("TRANSCRIPT speaker variant is not registered")
        normalized_payload = {
            "message_source_key": message_key,
            "speaker": normalized_speaker,
        }
        if "recipient_refs" in payload:
            normalized_payload["recipient_refs"] = _native_ref_array(
                payload["recipient_refs"], "recipient_refs"
            )
        for field in ("interaction_ref", "exact_text_ref"):
            if field in payload:
                normalized_payload[field] = _native_ref(payload[field], field)
    elif layer == "EVENTS":
        allowed = {"event_source_keys", "relation_source_keys", "t0_basis"}
        if set(payload) - allowed or not (
            {"event_source_keys", "relation_source_keys"} & set(payload)
        ):
            raise StoryContractError("EVENTS payload fields are not strict")
        normalized_payload = {}
        for field in ("event_source_keys", "relation_source_keys"):
            if field in payload:
                keys = _unique_strings(payload[field], field)
                if not set(keys).issubset(sources):
                    raise StoryContractError(f"{field} contains an unbound source key")
                normalized_payload[field] = keys
        if "t0_basis" in payload:
            try:
                basis = validate_t0_basis(payload["t0_basis"])
            except HistoryContractError as exc:
                raise StoryContractError(str(exc)) from exc
            event_keys = normalized_payload.get("event_source_keys", [])
            if not any(
                sources[key]["ref"]["family"] == "runtime.semantic_event"
                and basis["event_id"] in sources[key]["ref"]["identity"]
                for key in event_keys
            ):
                raise StoryContractError(
                    "Story-local T0 basis is not bound to an event source"
                )
            normalized_payload["t0_basis"] = basis
    elif layer == "MECHANICS":
        allowed = {"mechanical_source_keys", "resolution_refs", "receipt_refs"}
        if set(payload) - allowed or "mechanical_source_keys" not in payload:
            raise StoryContractError("MECHANICS payload fields are not strict")
        keys = _unique_strings(
            payload["mechanical_source_keys"], "mechanical_source_keys"
        )
        if not set(keys).issubset(sources):
            raise StoryContractError("MECHANICS source key is unbound")
        normalized_payload = {"mechanical_source_keys": keys}
        for field in ("resolution_refs", "receipt_refs"):
            if field in payload:
                normalized_payload[field] = _native_ref_array(payload[field], field)
    else:
        if set(payload) != {"factual_source_keys"}:
            raise StoryContractError("NARRATIVE payload fields are not strict")
        keys = _unique_strings(payload["factual_source_keys"], "factual_source_keys")
        if not set(keys).issubset(sources):
            raise StoryContractError("NARRATIVE factual source key is unbound")
        normalized_payload = {"factual_source_keys": keys}

    normalized: dict[str, object] = {
        "schema_version": version,
        "story_id": unit["story_id"],
        "content": normalized_content,
        "sources": sources,
        "projection_basis": contributions,
        "availability": normalized_availability,
        "payload": normalized_payload,
    }
    if "entity_refs" in unit:
        normalized["entity_refs"] = _native_ref_array(
            unit["entity_refs"], "entity_refs"
        )
    if "cross_refs" in unit:
        normalized["cross_refs"] = _story_ref_array(unit["cross_refs"], "cross_refs")
    for field in ("temporal_source_keys", "causal_source_keys"):
        if field in unit:
            keys = _unique_strings(unit[field], field)
            if not set(keys).issubset(sources):
                raise StoryContractError(f"{field} contains an unbound source key")
            normalized[field] = keys
    return normalized


def select_story_root(value: object) -> str:
    """Select the accepted static root without consulting deferred manifest routing."""

    if value != STORY_ROOT:
        raise StoryContractError("only the accepted STORY root is selectable")
    return STORY_ROOT


def _story_layer(story_id: object) -> tuple[str, int]:
    if not isinstance(story_id, str):
        raise StoryContractError("story_id must be a string")
    match = _STORY_ID.fullmatch(story_id)
    if match is None:
        raise StoryContractError(
            "story_id must have a known prefix and canonical decimal sequence"
        )
    sequence = int(match["sequence"])
    if sequence < 1:
        raise StoryContractError("story_id sequence must be positive")
    return _PREFIX_LAYERS[match["prefix"]], sequence


def story_record_path(story_root: object, story_id: object) -> Path:
    """Derive the fixed bounded route; physical placement is not Story authority."""

    root = select_story_root(story_root)
    layer, sequence = _story_layer(story_id)
    return Path(root) / layer / f"{sequence // 1000:03d}" / f"{story_id}.yaml"


def _coverage_cursor(
    value: object, registration: StorySourceRegistration, label: str
) -> tuple[int | None, dict[str, object]]:
    coverage = _mapping(value, label)
    if set(coverage) != {"kind", "through"} or coverage["kind"] != "CONTIGUOUS":
        raise StoryContractError(f"{label} must use the registered CONTIGUOUS codec")
    through = coverage["through"]
    ordinal = (
        None
        if through is None
        else decode_candidate_cursor(registration.registration_id, through)
    )
    return ordinal, {"kind": "CONTIGUOUS", "through": through}


def _validate_owner_contracts(value: object) -> list[dict[str, object]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or not value:
        raise StoryContractError("source owner contracts must be a nonempty array")
    contracts: list[dict[str, object]] = []
    for raw_contract in value:
        contract = _mapping(raw_contract, "source owner contract")
        if set(contract) - {"family", "schema_version", "semantic_generation"}:
            raise StoryContractError("source owner contract fields are not registered")
        if "family" not in contract or not (
            "schema_version" in contract or "semantic_generation" in contract
        ):
            raise StoryContractError(
                "source owner contract needs identity and version evidence"
            )
        normalized: dict[str, object] = {
            "family": _nonempty_string(contract["family"], "owner family")
        }
        for field in ("schema_version", "semantic_generation"):
            if field in contract:
                version = contract[field]
                if type(version) is not int or version < 1:
                    raise StoryContractError(
                        f"owner {field} must be a positive integer"
                    )
                normalized[field] = version
        contracts.append(normalized)
    return contracts


def validate_story_source_window(
    registration_id: object, value: object
) -> dict[str, object]:
    """Validate one fixed generation-1 bounded source/coverage window."""
    registration = story_source_registration(registration_id)
    window = _mapping(value, "Story source window")
    expected_fields = {
        "source_domain",
        "semantic_contract_generation",
        "source_basis",
        "expected_coverage",
        "proposed_coverage",
        "candidates",
    }
    if set(window) != expected_fields:
        raise StoryContractError("Story source window fields are not strict")
    if (
        window["semantic_contract_generation"]
        != registration.semantic_contract_generation
        or type(window["semantic_contract_generation"]) is not int
    ):
        raise StoryContractError("unsupported Story semantic contract generation")
    source_domain = _nonempty_string(window["source_domain"], "source_domain")
    if not source_domain.startswith(registration.source_domain_prefix):
        raise StoryContractError("Story source window domain differs from registration")
    origin = _decode_origin_scope(
        source_domain.removeprefix(registration.source_domain_prefix)
    )
    if story_source_domain(registration.registration_id, origin) != source_domain:
        raise StoryContractError("Story source window domain is not canonical")

    source_basis = _mapping(window["source_basis"], "Story source basis")
    basis_fields = {
        "origin",
        "lane",
        "upper",
        "enumeration_representation",
        "owner_contracts",
    }
    if set(source_basis) != basis_fields:
        raise StoryContractError("Story source basis fields are not strict")
    if _origin_scope(source_basis["origin"]) != origin:
        raise StoryContractError("Story source basis origin differs from domain scope")
    if source_basis["lane"] != registration.lane:
        raise StoryContractError("Story source basis lane differs from registration")
    _nonempty_string(
        source_basis["enumeration_representation"], "enumeration_representation"
    )
    owner_contracts = _validate_owner_contracts(source_basis["owner_contracts"])
    upper = (
        None
        if source_basis["upper"] is None
        else decode_candidate_cursor(
            registration.registration_id, source_basis["upper"]
        )
    )

    expected_ordinal, expected_coverage = _coverage_cursor(
        window["expected_coverage"], registration, "expected_coverage"
    )
    proposed_ordinal, proposed_coverage = _coverage_cursor(
        window["proposed_coverage"], registration, "proposed_coverage"
    )
    raw_candidates = window["candidates"]
    if not isinstance(raw_candidates, Sequence) or isinstance(
        raw_candidates, (str, bytes)
    ):
        raise StoryContractError("Story source candidates must be an array")
    candidates: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for raw_candidate in raw_candidates:
        candidate = _mapping(raw_candidate, "Story source candidate")
        if set(candidate) != {"candidate_id", "requirement", "source_keys"}:
            raise StoryContractError("Story source candidate fields are not strict")
        candidate_id = _nonempty_string(candidate["candidate_id"], "candidate_id")
        decode_candidate_id(registration.registration_id, candidate_id)
        if candidate_id in seen_ids:
            raise StoryContractError("Story source candidate IDs must be unique")
        seen_ids.add(candidate_id)
        requirement = candidate["requirement"]
        if requirement not in {"MUST_MATERIALIZE", "MAY_OMIT"}:
            raise StoryContractError("candidate requirement is not registered")
        if (
            registration.requirement_policy is StoryRequirementPolicy.MUST_MATERIALIZE
            and requirement != "MUST_MATERIALIZE"
        ):
            raise StoryContractError("this registration requires every candidate")
        if (
            registration.requirement_policy is StoryRequirementPolicy.MAY_OMIT
            and requirement != "MAY_OMIT"
        ):
            raise StoryContractError(
                "this registration has optional Transcript candidates"
            )
        source_keys = _unique_strings(candidate["source_keys"], "candidate source_keys")
        if any(_LOCAL_SOURCE_KEY.fullmatch(key) is None for key in source_keys):
            raise StoryContractError("candidate source key is not canonical")
        candidates.append(
            {
                "candidate_id": candidate_id,
                "requirement": requirement,
                "source_keys": source_keys,
            }
        )

    if candidates:
        if expected_ordinal is not None and proposed_ordinal is not None:
            progress = proposed_ordinal - expected_ordinal
        elif expected_ordinal is None and proposed_ordinal is not None:
            progress = proposed_ordinal
        else:
            progress = 0
        if progress != len(candidates) or progress < 1:
            raise StoryContractError(
                "candidate cardinality does not match contiguous coverage"
            )
        if upper is None or proposed_ordinal is None or proposed_ordinal > upper:
            raise StoryContractError("proposed coverage exceeds the exact source upper")
    elif expected_ordinal != proposed_ordinal:
        raise StoryContractError("an empty source window cannot advance coverage")
    if upper is None:
        if expected_ordinal is not None or proposed_ordinal is not None or candidates:
            raise StoryContractError("empty source upper conflicts with coverage")
    elif (expected_ordinal or 0) > upper:
        raise StoryContractError("expected coverage exceeds the exact source upper")

    return {
        "source_domain": source_domain,
        "semantic_contract_generation": registration.semantic_contract_generation,
        "source_basis": {
            "origin": origin,
            "lane": registration.lane,
            "upper": source_basis["upper"],
            "enumeration_representation": source_basis["enumeration_representation"],
            "owner_contracts": owner_contracts,
        },
        "expected_coverage": expected_coverage,
        "proposed_coverage": proposed_coverage,
        "candidates": candidates,
    }


def validate_story_candidate_result(
    registration_id: object,
    source_domain: object,
    candidate: object,
    result: object,
) -> dict[str, object]:
    """Enforce registration-owned terminal disposition/cardinality vocabulary."""
    registration = story_source_registration(registration_id)
    domain = _nonempty_string(source_domain, "source_domain")
    if not domain.startswith(registration.source_domain_prefix):
        raise StoryContractError("candidate result domain differs from registration")
    origin = _decode_origin_scope(
        domain.removeprefix(registration.source_domain_prefix)
    )
    expected_domain = story_source_domain(registration.registration_id, origin)
    if domain != expected_domain:
        raise StoryContractError("candidate result domain differs from registration")
    candidate_value = _mapping(candidate, "Story source candidate")
    if set(candidate_value) != {"candidate_id", "requirement", "source_keys"}:
        raise StoryContractError("Story source candidate fields are not strict")
    candidate_id = _nonempty_string(candidate_value["candidate_id"], "candidate_id")
    decode_candidate_id(registration.registration_id, candidate_id)
    requirement = candidate_value["requirement"]
    if requirement not in {"MUST_MATERIALIZE", "MAY_OMIT"}:
        raise StoryContractError("candidate requirement is not registered")
    if (
        registration.requirement_policy is StoryRequirementPolicy.MUST_MATERIALIZE
        and requirement != "MUST_MATERIALIZE"
    ):
        raise StoryContractError("this registration requires materialization")
    if (
        registration.requirement_policy is StoryRequirementPolicy.MAY_OMIT
        and requirement != "MAY_OMIT"
    ):
        raise StoryContractError(
            "this registration is Selective Exact optional Transcript"
        )

    disposition = _mapping(result, "Story CandidateResult")
    outcome = disposition.get("outcome")
    base_fields = {"source_domain", "candidate_id", "outcome"}
    if (
        disposition.get("source_domain") != domain
        or disposition.get("candidate_id") != candidate_id
    ):
        raise StoryContractError("candidate result does not bind its source candidate")
    if outcome == "MATERIALIZED":
        if set(disposition) != base_fields | {"record_keys"}:
            raise StoryContractError("MATERIALIZED result fields are not strict")
        record_keys = _unique_strings(disposition["record_keys"], "record_keys")
        if any(_LOCAL_SOURCE_KEY.fullmatch(key) is None for key in record_keys):
            raise StoryContractError("record key is not canonical")
        return {
            "source_domain": domain,
            "candidate_id": candidate_id,
            "outcome": "MATERIALIZED",
            "record_keys": record_keys,
        }
    if outcome == "OMITTED":
        if set(disposition) != base_fields | {"reason_code"}:
            raise StoryContractError("OMITTED result fields are not strict")
        reason_code = _nonempty_string(disposition["reason_code"], "reason_code")
        if requirement != "MAY_OMIT" or reason_code not in registration.omission_codes:
            raise StoryContractError("omission is not admitted by this source contract")
        return {
            "source_domain": domain,
            "candidate_id": candidate_id,
            "outcome": "OMITTED",
            "reason_code": reason_code,
        }
    raise StoryContractError("candidate result outcome is not registered")


def validate_story_projection(value: object, *, layer: str) -> dict[str, object]:
    """Validate the existing T07D Commentator carrier, not a persisted StoryUnit."""

    if layer != "EVENTS":
        raise StoryContractError(
            "owner-local projection currently supports EVENTS only"
        )
    projection = _mapping(value, "Story projection")
    expected = {
        "schema_version",
        "story_id",
        "content",
        "sources",
        "t0_basis",
        "availability",
    }
    if set(projection) != expected:
        raise StoryContractError("Story projection has unsupported or missing fields")
    actual_layer, _ = _story_layer(projection["story_id"])
    if actual_layer != layer:
        raise StoryContractError(
            "Story identity prefix does not match projection layer"
        )
    content = _mapping(projection["content"], "Story content")
    if set(content) != {"body"}:
        raise StoryContractError(
            "Story content must contain only body in this owner-local shape"
        )
    availability = _mapping(projection["availability"], "Story availability")
    if set(availability) != {"visible_to"}:
        raise StoryContractError("Story availability must contain only visible_to")
    visible_to = _unique_strings(availability["visible_to"], "visible_to")
    try:
        basis = validate_t0_basis(projection["t0_basis"])
    except HistoryContractError as exc:
        raise StoryContractError(str(exc)) from exc
    sources = _unique_strings(projection["sources"], "sources")
    if basis["event_id"] not in sources:
        raise StoryContractError("Story-local T0 basis must name an event source")
    version = projection["schema_version"]
    if not isinstance(version, int) or isinstance(version, bool) or version != 1:
        raise StoryContractError("unsupported schema_version")
    return {
        "schema_version": version,
        "story_id": projection["story_id"],
        "content": {"body": _nonempty_string(content["body"], "Story body")},
        "sources": sources,
        "t0_basis": basis,
        "availability": {"visible_to": visible_to},
    }


def build_story_source_bundle(events: object, *, layer: str) -> dict[str, object]:
    """Build a caller-supplied finite source bundle; no scan or source mutation occurs."""

    if layer != "EVENTS":
        raise StoryContractError(
            "owner-local source bundles currently support EVENTS only"
        )
    if not isinstance(events, Sequence) or isinstance(events, str):
        raise StoryContractError("events must be an array")
    try:
        normalized = [validate_semantic_event_draft(event) for event in events]
    except HistoryContractError as exc:
        raise StoryContractError(str(exc)) from exc
    ids = [event["event_id"] for event in normalized]
    if len(ids) != len(set(ids)):
        raise StoryContractError("source bundle event identities must be unique")
    return {"layer": layer, "events": normalized}


def project_story_window(
    bundle: object, projections: object
) -> list[dict[str, object]]:
    """Validate a finite EVENTS projection window without changing native history."""

    source_bundle = _mapping(bundle, "Story source bundle")
    if set(source_bundle) != {"layer", "events"} or source_bundle["layer"] != "EVENTS":
        raise StoryContractError("invalid EVENTS Story source bundle")
    if not isinstance(projections, Sequence) or isinstance(projections, str):
        raise StoryContractError("projections must be an array")
    raw_events = source_bundle["events"]
    if not isinstance(raw_events, Sequence) or isinstance(raw_events, str):
        raise StoryContractError("Story source bundle events must be an array")
    try:
        events = [validate_semantic_event_draft(event) for event in raw_events]
    except HistoryContractError as exc:
        raise StoryContractError(str(exc)) from exc
    event_ids = [event["event_id"] for event in events]
    if len(event_ids) != len(set(event_ids)):
        raise StoryContractError("source bundle event identities must be unique")
    source_event_ids = set(event_ids)
    validated = [
        validate_story_projection(projection, layer="EVENTS")
        for projection in projections
    ]
    for projection in validated:
        if not set(projection["sources"]).issubset(source_event_ids):
            raise StoryContractError(
                "Story projection must use only its bounded native sources"
            )
    return deepcopy(validated)
