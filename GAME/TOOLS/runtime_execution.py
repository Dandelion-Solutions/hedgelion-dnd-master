"""Typed acceptance and verification for authoritative ``runtime.command`` records."""

from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Final

from .catalog_runtime import (
    BoundCatalogContext,
    CatalogBindingError,
    bind_executable_catalog,
    canonical_json,
    sha256,
    validate_executable_binding,
)
from .native_storage import (
    IdentityMismatch,
    NativeStorageError,
    route_native_record,
    validate_loaded_identity,
)
from .policy_basis import (
    AcceptedAdjudicationBasis,
    PinnedCampaign,
    PolicyBasisResolutionError,
    is_accepted_basis_issued,
    validate_adjudicated_input_surface,
    validate_frozen_adjudication_basis,
    validate_policy_applicability_witnesses,
)

# framework_module_version: 1.0.8
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.8"
RUNTIME_COMMAND_SCHEMA_VERSION: Final = 3
INTERPRETER_RESULT_FINGERPRINT_GENERATION: Final = 1
RUNTIME_COMMAND_INPUT_FINGERPRINT_GENERATION: Final = 2
INTERPRETER_RESULT_FIELDS: Final = frozenset(
    {"kind", "purpose", "bundle_id", "source_generation", "intent"}
)
COMMAND_PROPOSAL_FIELDS: Final = frozenset(
    {
        "command_id",
        "interaction_id",
        "intent_plan_id",
        "clause_id",
        "action_request",
        "root_resolution_id",
    }
)
COMMAND_STATE_FIELDS: Final = frozenset(
    {
        "schema_version",
        "command_id",
        "interaction_id",
        "intent_plan_id",
        "clause_id",
        "command_kind",
        "catalog_context_fingerprint",
        "input_fingerprint_generation",
        "input_fingerprint",
        "disposition",
        "invocation_facts",
        "action_request",
        "root_resolution_id",
        "pending_child_invocations",
        "interpreter_result",
        "interpreter_result_fingerprint_generation",
        "interpreter_result_fingerprint",
        "catalog_context",
        "candidate_binding",
    }
)
ACCEPTED_INPUT_FIELDS: Final = frozenset(
    {
        "command_kind",
        "catalog_context_fingerprint",
        "invocation_facts",
        "action_request",
        "interpreter_result",
        "interpreter_result_fingerprint_generation",
        "interpreter_result_fingerprint",
        "catalog_context",
        "candidate_binding",
    }
)
_INTERPRETER_RESULT_DOMAIN: Final = b"HDM_INTERPRETER_RESULT/1\n"
_RUNTIME_COMMAND_INPUT_DOMAIN: Final = b"HDM_RUNTIME_COMMAND_INPUT/2\n"
_SHA256_HEX: Final = frozenset("0123456789abcdef")


class CommandAcceptanceError(ValueError):
    """Raised when a command is not a valid accepted ``runtime.command`` record."""


class NativeOrderingError(ValueError):
    """Raised when a native ordered-owner proof cannot be established."""


class NativeOrderingStatus(StrEnum):
    """Ephemeral native ordered-owner result status."""

    RULE_OWNED_ORDERED = "RULE_OWNED_ORDERED"
    NO_ORDERED_OWNER = "NO_ORDERED_OWNER"


@dataclass(frozen=True, slots=True)
class NativeOrderingEvidence:
    """Derived evidence for one exact current Step-3 ordered offer."""

    status: NativeOrderingStatus
    campaign_id: str
    source_scope: str
    source_key: str
    source_revision: str
    resolution_id: str
    continuation_id: str
    continuation_generation: int
    offer_kind: str
    offer_id: str
    responder_id: str
    procedure_id: str | None = None


@dataclass(frozen=True, slots=True)
class NativeOrderingNoOwner:
    """Ephemeral negative result when no exact Resolution reference is requested."""

    status: NativeOrderingStatus
    campaign_id: str
    route: str = "runtime_execution"


class CatalogGap:
    """Typed non-acceptance evidence for an unavailable catalog candidate."""

    __slots__ = ("gap_report",)

    def __init__(self, gap_report: Mapping[str, object]) -> None:
        self.gap_report = MappingProxyType(dict(gap_report))


_ORDERING_FAMILIES: Final[frozenset[str]] = frozenset(
    {"runtime.resolution", "runtime.continuation", "runtime.procedure"}
)
_ORDERING_REQUEST_FIELDS: Final[frozenset[str]] = frozenset({"resolution_id"})
_CHOICE_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "kind",
        "offer_id",
        "parent_resolution_id",
        "continuation_generation",
        "responder_id",
        "option_ids",
    }
)
_REACTION_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "kind",
        "offer_id",
        "parent_resolution_id",
        "continuation_generation",
        "responder_id",
        "candidate_activity_ids",
    }
)
_ORDERING_OWNER_REQUIRED_FIELDS: Final[dict[str, frozenset[str]]] = {
    "runtime.resolution": frozenset(
        {
            "root_command_id",
            "activity_id",
            "actor_id",
            "ruleset_set_digest_generation",
            "ruleset_set_sha256",
            "catalog_context_fingerprint_generation",
            "catalog_context_fingerprint",
            "status",
            "next_segment_sequence",
            "invocation_facts",
            "fixed_rng_results",
            "prior_step_exports",
            "child_resolution_ids",
            "segments",
        }
    ),
    "runtime.continuation": frozenset(
        {
            "generation",
            "root_command_id",
            "resolution_id",
            "activity_id",
            "actor_id",
            "ruleset_set_digest_generation",
            "ruleset_set_sha256",
            "catalog_context_fingerprint_generation",
            "catalog_context_fingerprint",
            "execution_cursor",
            "safe_recompute_phase",
            "invocation_facts",
            "fixed_rng_results",
            "prior_step_exports",
            "committed_segment_refs",
            "dependency_frontier_refs",
            "expected_child_resolution_ids",
            "future_rng_frontier",
        }
    ),
    "runtime.procedure": frozenset(
        {"schema_version", "lifecycle", "participant_resources"}
    ),
}
_RESOLUTION_BASIS_FIELDS: Final[frozenset[str]] = frozenset(
    {"initiating_command_id", "causal_invocation_key"}
)
_ORDERING_ID_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_ORDERING_SHA256_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[a-f0-9]{64}$")
_ORDERING_POLICY_REF_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z][A-Za-z0-9_.:-]*@[a-f0-9]{40}(?:[a-f0-9]{24})?$"
)
_ORDERING_EXECUTION_STATES: Final[frozenset[str]] = frozenset(
    {
        "PENDING",
        "RUNNING",
        "AWAITING_CHOICE",
        "AWAITING_REACTION",
        "HYDRATION_REQUIRED",
        "PUBLISH_REQUIRED",
        "COMPLETED",
        "REJECTED",
        "ABORTED",
        "FAILED",
    }
)
_ORDERING_FAILURE_CODES: Final[frozenset[str]] = frozenset(
    {
        "failure.idempotency_conflict",
        "failure.hydration_required",
        "failure.missing_reference",
        "failure.catalog_context_incompatible",
        "failure.continuation_conflict",
        "failure.continuation_stale",
        "failure.dependency_cycle",
        "failure.transition_requires_procedure",
        "failure.order_adjudication_required",
        "failure.execution_limit",
        "failure.invocation_fact_missing",
        "failure.invocation_fact_unauthorized",
        "failure.adjudication_input_missing",
        "failure.adjudication_input_unauthorized",
        "failure.adjudication_input_invalid",
        "failure.adjudication_context_stale",
        "failure.policy_conflict",
        "failure.policy_realization_gap",
    }
)
_ORDERING_ENVELOPE_FIELDS: Final[frozenset[str]] = frozenset(
    {"kind", "id", "campaign_id", "revision"}
)
_ORDERING_RESOLUTION_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "root_command_id",
        "initiating_command_id",
        "causal_invocation_key",
        "activity_id",
        "actor_id",
        "source_id",
        "target_ids",
        "parameter_bindings",
        "catalog_context_fingerprint_generation",
        "catalog_context_fingerprint",
        "ruleset_set_digest_generation",
        "ruleset_set_sha256",
        "procedure_id",
        "status",
        "failure_code",
        "cursor",
        "safe_recompute_phase",
        "next_segment_sequence",
        "invocation_facts",
        "fixed_rng_results",
        "prior_step_exports",
        "child_resolution_ids",
        "segments",
        "continuation_id",
        "trace_id",
        "details",
    }
)
_ORDERING_CONTINUATION_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "generation",
        "root_command_id",
        "resolution_id",
        "activity_id",
        "actor_id",
        "source_id",
        "target_ids",
        "parameter_bindings",
        "catalog_context_fingerprint_generation",
        "catalog_context_fingerprint",
        "ruleset_set_digest_generation",
        "ruleset_set_sha256",
        "procedure_id",
        "execution_cursor",
        "safe_recompute_phase",
        "invocation_facts",
        "fixed_rng_results",
        "prior_step_exports",
        "committed_segment_refs",
        "dependency_frontier_refs",
        "expected_child_resolution_ids",
        "future_rng_frontier",
        "pending_response",
        "unconsumed_advancement",
        "details",
    }
)


def _ordering_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise NativeOrderingError(f"{label} must be a nonempty string")
    return value


def _ordering_id(value: object, label: str) -> str:
    result = _ordering_text(value, label)
    if _ORDERING_ID_PATTERN.fullmatch(result) is None:
        raise NativeOrderingError(f"{label} must be a machine identifier")
    return result


def _ordering_integer(value: object, label: str, *, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise NativeOrderingError(f"{label} must be an integer >= {minimum}")
    return value


def _ordering_mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or any(not isinstance(key, str) for key in value):
        raise NativeOrderingError(f"{label} must be an object with string keys")
    return value


def _ordering_array(value: object, label: str) -> Sequence[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise NativeOrderingError(f"{label} must be an array")
    return value


def _ordering_scalar(value: object, label: str) -> None:
    if value is None or not isinstance(value, (str, int, float, bool)):
        raise NativeOrderingError(f"{label} must be a scalar")
    if isinstance(value, float) and not math.isfinite(value):
        raise NativeOrderingError(f"{label} must be a finite scalar")


def _ordering_sha256(value: object, label: str) -> str:
    result = _ordering_text(value, label)
    if _ORDERING_SHA256_PATTERN.fullmatch(result) is None:
        raise NativeOrderingError(f"{label} must be a lower-case SHA-256 digest")
    return result


def _ordering_unique_strings(
    value: object, label: str, *, machine_ids: bool = False, minimum: int = 0
) -> None:
    values = _ordering_array(value, label)
    if len(values) < minimum:
        raise NativeOrderingError(f"{label} must contain at least {minimum} item(s)")
    normalized: list[str] = []
    for item in values:
        normalized.append(
            _ordering_id(item, label) if machine_ids else _ordering_text(item, label)
        )
    if len(normalized) != len(set(normalized)):
        raise NativeOrderingError(f"{label} must contain unique items")


def _ordering_scalar_object(value: object, label: str) -> None:
    mapping = _ordering_mapping(value, label)
    for key, item in mapping.items():
        _ordering_text(key, f"{label} key")
        _ordering_scalar(item, f"{label} value")


def _ordering_policy_refs(value: object, label: str) -> None:
    refs = _ordering_array(value, label)
    normalized: list[str] = []
    for ref in refs:
        text = _ordering_text(ref, f"{label} item")
        if _ORDERING_POLICY_REF_PATTERN.fullmatch(text) is None:
            raise NativeOrderingError(f"{label} contains an invalid policy reference")
        normalized.append(text)
    if len(normalized) != len(set(normalized)):
        raise NativeOrderingError(f"{label} must contain unique items")


def _ordering_parameter_binding(value: object, label: str) -> None:
    if isinstance(value, (str, int, float, bool)):
        _ordering_scalar(value, label)
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        values = list(value)
        if not values:
            raise NativeOrderingError(f"{label} array must not be empty")
        for item in values:
            _ordering_scalar(item, f"{label} array item")
        return
    binding = _ordering_mapping(value, label)
    allowed = {
        "source_class",
        "value",
        "provenance_ref",
        "eligibility_basis_fingerprint",
        "rules_context_fingerprint",
        "policy_basis_refs",
        "candidate_set_fingerprint",
    }
    if set(binding) - allowed or not {
        "source_class",
        "value",
        "provenance_ref",
        "eligibility_basis_fingerprint",
        "rules_context_fingerprint",
        "policy_basis_refs",
    }.issubset(binding):
        raise NativeOrderingError(f"{label} has unexpected or missing fields")
    if binding["source_class"] != "INVOCATION_ADJUDICATED":
        raise NativeOrderingError(f"{label} has an unsupported source class")
    _ordering_scalar(binding["value"], f"{label} value")
    for field in (
        "provenance_ref",
        "eligibility_basis_fingerprint",
        "rules_context_fingerprint",
        "candidate_set_fingerprint",
    ):
        if field in binding:
            _ordering_text(binding[field], f"{label} {field}")
    _ordering_policy_refs(binding["policy_basis_refs"], f"{label} policy_basis_refs")


def _ordering_parameter_bindings(value: object, label: str) -> None:
    bindings = _ordering_mapping(value, label)
    for key, item in bindings.items():
        _ordering_id(key, f"{label} key")
        _ordering_parameter_binding(item, f"{label} {key}")


def _ordering_invocation_fact(value: object, label: str) -> None:
    fact = _ordering_mapping(value, label)
    required = {
        "fact_id",
        "value",
        "provenance_class",
        "provenance_ref",
        "consumer_id",
        "binding_fingerprint",
        "rules_context_fingerprint",
        "policy_basis_refs",
    }
    if set(fact) != required:
        raise NativeOrderingError(f"{label} has unexpected or missing fields")
    _ordering_id(fact["fact_id"], f"{label} fact_id")
    if type(fact["value"]) is not bool:
        raise NativeOrderingError(f"{label} value must be boolean")
    if fact["provenance_class"] != "INVOCATION_ADJUDICATED":
        raise NativeOrderingError(f"{label} provenance class is unsupported")
    _ordering_text(fact["provenance_ref"], f"{label} provenance_ref")
    _ordering_id(fact["consumer_id"], f"{label} consumer_id")
    _ordering_sha256(fact["binding_fingerprint"], f"{label} binding_fingerprint")
    _ordering_sha256(
        fact["rules_context_fingerprint"], f"{label} rules_context_fingerprint"
    )
    _ordering_policy_refs(fact["policy_basis_refs"], f"{label} policy_basis_refs")


def _ordering_roll_result(value: object, label: str) -> None:
    result = _ordering_mapping(value, label)
    required = {
        "roll_id",
        "request_id",
        "expression",
        "raw_values",
        "source_kind",
        "provenance_ref",
    }
    if set(result) != required:
        raise NativeOrderingError(f"{label} has unexpected or missing fields")
    _ordering_id(result["roll_id"], f"{label} roll_id")
    _ordering_id(result["request_id"], f"{label} request_id")
    _ordering_text(result["expression"], f"{label} expression")
    values = _ordering_array(result["raw_values"], f"{label} raw_values")
    if not values or any(type(item) is not int for item in values):
        raise NativeOrderingError(f"{label} raw_values must contain integers")
    if result["source_kind"] not in {"rng.system", "rng.player", "rng.external"}:
        raise NativeOrderingError(f"{label} source_kind is unsupported")
    _ordering_text(result["provenance_ref"], f"{label} provenance_ref")


def _ordering_pending_child(value: object, label: str) -> None:
    child = _ordering_mapping(value, label)
    required = {"firing_key", "root_command_id", "activity_id", "trigger_ref", "reason"}
    allowed = required | {"procedure_id", "child_resolution_id"}
    if set(child) - allowed or not required.issubset(child):
        raise NativeOrderingError(f"{label} has unexpected or missing fields")
    for field in ("firing_key", "root_command_id", "trigger_ref"):
        _ordering_text(child[field], f"{label} {field}")
    _ordering_id(child["activity_id"], f"{label} activity_id")
    for field in ("procedure_id", "child_resolution_id"):
        if field in child:
            _ordering_text(child[field], f"{label} {field}")
    if child["reason"] not in {"mandatory_followup", "execution_limit"}:
        raise NativeOrderingError(f"{label} reason is unsupported")


def _ordering_segment(value: object, label: str) -> None:
    segment = _ordering_mapping(value, label)
    required = {
        "segment_id",
        "segment_sequence",
        "commit_state",
        "resulting_execution_state",
        "event_ids",
        "pending_child_invocations",
        "receipt_exports",
        "affected_revision_refs",
    }
    allowed = required | {"continuation_id"}
    if set(segment) - allowed or not required.issubset(segment):
        raise NativeOrderingError(f"{label} has unexpected or missing fields")
    _ordering_id(segment["segment_id"], f"{label} segment_id")
    _ordering_integer(
        segment["segment_sequence"], f"{label} segment_sequence", minimum=1
    )
    if segment["commit_state"] != "committed":
        raise NativeOrderingError(f"{label} commit_state is unsupported")
    if segment["resulting_execution_state"] not in _ORDERING_EXECUTION_STATES:
        raise NativeOrderingError(f"{label} resulting_execution_state is unsupported")
    _ordering_unique_strings(segment["event_ids"], f"{label} event_ids")
    children = _ordering_array(
        segment["pending_child_invocations"], f"{label} pending_child_invocations"
    )
    for index, child in enumerate(children):
        _ordering_pending_child(child, f"{label} pending_child_invocations[{index}]")
    receipt_exports = _ordering_mapping(
        segment["receipt_exports"], f"{label} receipt_exports"
    )
    for key, item in receipt_exports.items():
        _ordering_id(key, f"{label} receipt export key")
        _ordering_scalar(item, f"{label} receipt export value")
    _ordering_unique_strings(
        segment["affected_revision_refs"], f"{label} affected_revision_refs"
    )
    if "continuation_id" in segment:
        _ordering_text(segment["continuation_id"], f"{label} continuation_id")


def _ordering_pending_response_schema(value: object, label: str) -> None:
    offer = _ordering_mapping(value, label)
    kind = offer.get("kind")
    fields = (
        _CHOICE_FIELDS
        if kind == "choice"
        else _REACTION_FIELDS
        if kind == "reaction"
        else None
    )
    if fields is None or set(offer) != fields:
        raise NativeOrderingError(
            f"{label} is not a valid ChoiceRequest or ReactionOffer"
        )
    _ordering_text(offer["offer_id"], f"{label} offer_id")
    _ordering_text(offer["parent_resolution_id"], f"{label} parent_resolution_id")
    _ordering_integer(
        offer["continuation_generation"], f"{label} continuation_generation", minimum=1
    )
    _ordering_text(offer["responder_id"], f"{label} responder_id")
    item_field = "option_ids" if kind == "choice" else "candidate_activity_ids"
    _ordering_unique_strings(offer[item_field], f"{label} {item_field}", minimum=1)


def _ordering_resolution_schema(payload: Mapping[str, object]) -> None:
    for field in (
        "root_command_id",
        "initiating_command_id",
        "causal_invocation_key",
        "cursor",
        "safe_recompute_phase",
        "trace_id",
    ):
        if field in payload:
            _ordering_text(payload[field], f"resolution {field}")
    for field in ("activity_id", "actor_id", "source_id"):
        if field in payload:
            _ordering_id(payload[field], f"resolution {field}")
    for field in ("continuation_id", "procedure_id"):
        if field in payload:
            _ordering_text(payload[field], f"resolution {field}")
    if "target_ids" in payload:
        _ordering_unique_strings(
            payload["target_ids"], "resolution target_ids", machine_ids=True
        )
    if "parameter_bindings" in payload:
        _ordering_parameter_bindings(
            payload["parameter_bindings"], "resolution parameter_bindings"
        )
    for field in (
        "catalog_context_fingerprint_generation",
        "ruleset_set_digest_generation",
    ):
        if type(payload[field]) is not int or payload[field] != 1:
            raise NativeOrderingError(f"resolution {field} must be exactly 1")
    _ordering_text(
        payload["catalog_context_fingerprint"], "resolution catalog_context_fingerprint"
    )
    _ordering_sha256(payload["ruleset_set_sha256"], "resolution ruleset_set_sha256")
    if payload["status"] not in _ORDERING_EXECUTION_STATES:
        raise NativeOrderingError("resolution status is unsupported")
    if (
        "failure_code" in payload
        and payload["failure_code"] not in _ORDERING_FAILURE_CODES
    ):
        raise NativeOrderingError("resolution failure_code is unsupported")
    if (
        payload["status"] in {"HYDRATION_REQUIRED", "REJECTED", "FAILED"}
        and "failure_code" not in payload
    ):
        raise NativeOrderingError("resolution failure_code is required for its status")
    if "failure_code" in payload and payload["status"] not in {
        "HYDRATION_REQUIRED",
        "REJECTED",
        "ABORTED",
        "FAILED",
    }:
        raise NativeOrderingError("resolution failure_code conflicts with its status")
    _ordering_integer(
        payload["next_segment_sequence"], "resolution next_segment_sequence", minimum=1
    )
    facts = _ordering_array(payload["invocation_facts"], "resolution invocation_facts")
    for index, fact in enumerate(facts):
        _ordering_invocation_fact(fact, f"resolution invocation_facts[{index}]")
    rolls = _ordering_array(
        payload["fixed_rng_results"], "resolution fixed_rng_results"
    )
    for index, roll in enumerate(rolls):
        _ordering_roll_result(roll, f"resolution fixed_rng_results[{index}]")
    _ordering_scalar_object(
        payload["prior_step_exports"], "resolution prior_step_exports"
    )
    _ordering_unique_strings(
        payload["child_resolution_ids"], "resolution child_resolution_ids"
    )
    segments = _ordering_array(payload["segments"], "resolution segments")
    for index, segment in enumerate(segments):
        _ordering_segment(segment, f"resolution segments[{index}]")
    if "details" in payload:
        _ordering_mapping(payload["details"], "resolution details")


def _ordering_continuation_schema(payload: Mapping[str, object]) -> None:
    _ordering_integer(payload["generation"], "continuation generation", minimum=1)
    for field in (
        "root_command_id",
        "resolution_id",
        "execution_cursor",
        "safe_recompute_phase",
        "future_rng_frontier",
    ):
        _ordering_text(payload[field], f"continuation {field}")
    if "procedure_id" in payload:
        _ordering_text(payload["procedure_id"], "continuation procedure_id")
    for field in ("activity_id", "actor_id", "source_id"):
        if field in payload:
            _ordering_id(payload[field], f"continuation {field}")
    if "target_ids" in payload:
        _ordering_unique_strings(
            payload["target_ids"], "continuation target_ids", machine_ids=True
        )
    if "parameter_bindings" in payload:
        _ordering_parameter_bindings(
            payload["parameter_bindings"], "continuation parameter_bindings"
        )
    for field in (
        "catalog_context_fingerprint_generation",
        "ruleset_set_digest_generation",
    ):
        if type(payload[field]) is not int or payload[field] != 1:
            raise NativeOrderingError(f"continuation {field} must be exactly 1")
    _ordering_text(
        payload["catalog_context_fingerprint"],
        "continuation catalog_context_fingerprint",
    )
    _ordering_sha256(payload["ruleset_set_sha256"], "continuation ruleset_set_sha256")
    for field in ("invocation_facts", "fixed_rng_results"):
        values = _ordering_array(payload[field], f"continuation {field}")
        validator = (
            _ordering_invocation_fact
            if field == "invocation_facts"
            else _ordering_roll_result
        )
        for index, item in enumerate(values):
            validator(item, f"continuation {field}[{index}]")
    _ordering_scalar_object(
        payload["prior_step_exports"], "continuation prior_step_exports"
    )
    for field in (
        "committed_segment_refs",
        "dependency_frontier_refs",
        "expected_child_resolution_ids",
    ):
        _ordering_unique_strings(payload[field], f"continuation {field}")
    if "pending_response" in payload:
        _ordering_pending_response_schema(
            payload["pending_response"], "continuation pending_response"
        )
    if "unconsumed_advancement" in payload:
        advancement = _ordering_mapping(
            payload["unconsumed_advancement"], "continuation unconsumed_advancement"
        )
        if set(advancement) != {"amount", "unit_id", "context_id"}:
            raise NativeOrderingError(
                "continuation unconsumed_advancement has unexpected or missing fields"
            )
        _ordering_integer(
            advancement["amount"], "continuation advancement amount", minimum=1
        )
        if advancement["unit_id"] not in {
            "unit.second",
            "unit.minute",
            "unit.hour",
            "unit.day",
        }:
            raise NativeOrderingError("continuation advancement unit_id is unsupported")
        _ordering_text(advancement["context_id"], "continuation advancement context_id")
    if "details" in payload:
        _ordering_mapping(payload["details"], "continuation details")


def _validate_ordering_owner_schema(family: str, payload: Mapping[str, object]) -> None:
    missing = _ORDERING_OWNER_REQUIRED_FIELDS[family].difference(payload)
    if missing:
        raise NativeOrderingError(
            f"exact {family} record is missing required owner-schema fields"
        )
    if family == "runtime.resolution" and not _RESOLUTION_BASIS_FIELDS.intersection(
        payload
    ):
        raise NativeOrderingError(
            "exact runtime.resolution record is missing command or invocation basis"
        )
    allowed = _ORDERING_ENVELOPE_FIELDS.copy()
    if family == "runtime.resolution":
        allowed |= _ORDERING_RESOLUTION_FIELDS
    elif family == "runtime.continuation":
        allowed |= _ORDERING_CONTINUATION_FIELDS
    else:
        return
    unexpected = set(payload) - allowed
    if unexpected:
        raise NativeOrderingError(
            f"exact {family} record has unsupported owner-schema fields"
        )
    if family == "runtime.resolution":
        _ordering_resolution_schema(payload)
    else:
        _ordering_continuation_schema(payload)


def _ordering_record(
    repository: object, campaign_pin: PinnedCampaign, family: str, record_id: str
) -> Mapping[str, object]:
    if family not in _ORDERING_FAMILIES:
        raise NativeOrderingError("native ordering family is not admitted")
    try:
        route = route_native_record(family, (record_id,))
        payload = repository.read_exact_path(campaign_pin, route.relative_path)
        if not isinstance(payload, Mapping):
            raise NativeOrderingError(f"exact {family} record is not an object")
        validate_loaded_identity(family, (record_id,), payload)
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        if isinstance(exc, NativeOrderingError):
            raise
        if isinstance(exc, (IdentityMismatch, NativeStorageError)):
            raise NativeOrderingError(
                f"exact {family} identity is stale or foreign"
            ) from exc
        raise NativeOrderingError(f"exact {family} owner read failed") from exc
    if payload.get("campaign_id") not in {None, campaign_pin.campaign_id}:
        raise NativeOrderingError(f"exact {family} belongs to another campaign")
    record_revision = payload.get("revision")
    if record_revision is not None and record_revision != campaign_pin.revision:
        raise NativeOrderingError(f"exact {family} record is stale")
    _validate_ordering_owner_schema(family, payload)
    return payload


def _pending_offer(
    response: object,
    *,
    resolution_id: str,
    continuation_generation: int,
) -> tuple[str, str, str]:
    offer = response if isinstance(response, Mapping) else None
    if offer is None or set(offer) not in {_CHOICE_FIELDS, _REACTION_FIELDS}:
        raise NativeOrderingError(
            "continuation pending response is not a valid ChoiceRequest or ReactionOffer"
        )
    kind = offer.get("kind")
    expected_fields = (
        _CHOICE_FIELDS
        if kind == "choice"
        else _REACTION_FIELDS
        if kind == "reaction"
        else None
    )
    if expected_fields is None or set(offer) != expected_fields:
        raise NativeOrderingError("continuation pending response kind is not admitted")
    offer_id = _ordering_text(offer.get("offer_id"), "pending offer id")
    if offer.get("parent_resolution_id") != resolution_id:
        raise NativeOrderingError(
            "pending offer does not belong to the current resolution"
        )
    if offer.get("continuation_generation") != continuation_generation:
        raise NativeOrderingError(
            "pending offer generation differs from the current continuation"
        )
    responder_id = _ordering_text(offer.get("responder_id"), "pending responder id")
    item_field = "option_ids" if kind == "choice" else "candidate_activity_ids"
    item_ids = offer.get(item_field)
    if (
        not isinstance(item_ids, Sequence)
        or isinstance(item_ids, (str, bytes))
        or not item_ids
        or any(not isinstance(item, str) or not item for item in item_ids)
        or len(item_ids) != len(set(item_ids))
    ):
        raise NativeOrderingError("pending offer candidates are invalid")
    return str(kind), offer_id, responder_id


def _validate_linked_procedure(
    repository: object,
    campaign_pin: PinnedCampaign,
    resolution: Mapping[str, object],
    continuation: Mapping[str, object],
    procedure_id: object,
) -> str:
    procedure_ref = _ordering_text(procedure_id, "linked procedure id")
    continuation_procedure = continuation.get("procedure_id")
    if continuation_procedure != procedure_ref:
        raise NativeOrderingError(
            "resolution and continuation procedure linkage differs"
        )
    procedure = _ordering_record(
        repository, campaign_pin, "runtime.procedure", procedure_ref
    )
    declared_procedure_id = procedure.get("procedure_id", procedure.get("id"))
    if declared_procedure_id != procedure_ref:
        raise NativeOrderingError(
            "linked procedure identity differs from its native route"
        )
    state = procedure.get("state")
    if state is not None and not isinstance(state, Mapping):
        raise NativeOrderingError("linked procedure state is malformed")
    procedure_state = state if isinstance(state, Mapping) else procedure
    if (
        procedure_state.get("schema_version") != 2
        or procedure_state.get("lifecycle") != "ACTIVE"
    ):
        raise NativeOrderingError("linked procedure is not current schema v2 ACTIVE")
    for field, expected in (
        ("resolution_id", resolution.get("id")),
        ("continuation_id", continuation.get("id")),
    ):
        declared = procedure.get(field, procedure_state.get(field))
        if declared is not None and declared != expected:
            raise NativeOrderingError("linked procedure identity is inconsistent")
    return procedure_ref


def resolve_native_ordering_evidence(
    request: object,
    *,
    repository: object,
    campaign_pin: PinnedCampaign,
    selected_live: object,
) -> NativeOrderingEvidence | NativeOrderingNoOwner:
    """Produce the sole generation-1 ``RULE_OWNED_ORDERED`` evidence.

    The caller supplies only an exact Resolution reference.  Continuation,
    Procedure, status, pending offer and family values are loaded from their
    current owner records and are never accepted as caller evidence.
    """
    del selected_live
    if isinstance(request, Mapping) and "resolution_id" not in request:
        return NativeOrderingNoOwner(
            status=NativeOrderingStatus.NO_ORDERED_OWNER,
            campaign_id=campaign_pin.campaign_id,
        )
    if not isinstance(request, Mapping) or set(request) != _ORDERING_REQUEST_FIELDS:
        raise NativeOrderingError(
            "native ordering request must contain only resolution_id"
        )
    resolution_id = _ordering_text(request.get("resolution_id"), "resolution id")
    resolution = _ordering_record(
        repository, campaign_pin, "runtime.resolution", resolution_id
    )
    declared_resolution_id = resolution.get("resolution_id", resolution.get("id"))
    if declared_resolution_id != resolution_id:
        raise NativeOrderingError("resolution identity differs from requested identity")
    status = resolution.get("status")
    if status not in {"AWAITING_CHOICE", "AWAITING_REACTION"}:
        raise NativeOrderingError("resolution is not awaiting an owner response")
    continuation_id = _ordering_text(
        resolution.get("continuation_id"), "resolution continuation id"
    )
    continuation = _ordering_record(
        repository, campaign_pin, "runtime.continuation", continuation_id
    )
    if continuation.get("resolution_id") != resolution_id:
        raise NativeOrderingError(
            "continuation does not belong to the current resolution"
        )
    generation = continuation.get("generation")
    if (
        isinstance(generation, bool)
        or not isinstance(generation, int)
        or generation < 1
    ):
        raise NativeOrderingError("continuation generation is invalid")
    expected_generation = resolution.get("continuation_generation")
    if expected_generation is not None and expected_generation != generation:
        raise NativeOrderingError("resolution continuation generation is stale")
    offer_kind, offer_id, responder_id = _pending_offer(
        continuation.get("pending_response"),
        resolution_id=resolution_id,
        continuation_generation=generation,
    )
    if (status == "AWAITING_CHOICE" and offer_kind != "choice") or (
        status == "AWAITING_REACTION" and offer_kind != "reaction"
    ):
        raise NativeOrderingError("resolution status does not match pending offer kind")
    resolution_procedure = resolution.get("procedure_id")
    continuation_procedure = continuation.get("procedure_id")
    if (resolution_procedure is None) != (continuation_procedure is None):
        raise NativeOrderingError(
            "resolution and continuation procedure linkage is incomplete"
        )
    procedure_id = None
    if resolution_procedure is not None:
        procedure_id = _validate_linked_procedure(
            repository,
            campaign_pin,
            resolution,
            continuation,
            resolution_procedure,
        )
    return NativeOrderingEvidence(
        status=NativeOrderingStatus.RULE_OWNED_ORDERED,
        campaign_id=campaign_pin.campaign_id,
        source_scope="campaign",
        source_key=f"runtime.resolution/{resolution_id}",
        source_revision=campaign_pin.revision,
        resolution_id=resolution_id,
        continuation_id=continuation_id,
        continuation_generation=generation,
        offer_kind=offer_kind,
        offer_id=offer_id,
        responder_id=responder_id,
        procedure_id=procedure_id,
    )


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, str):
        return [_thaw(item) for item in value]
    return value


def _require_mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise CommandAcceptanceError(f"{label} must be an object")
    return value


def _require_exact_fields(
    value: object, fields: frozenset[str], label: str
) -> Mapping[str, object]:
    mapping = _require_mapping(value, label)
    if set(mapping) != fields:
        raise CommandAcceptanceError(f"{label} has unexpected or missing fields")
    return mapping


def _require_nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise CommandAcceptanceError(f"{label} must be a nonempty string")
    return value


def _require_sha256(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(char not in _SHA256_HEX for char in value)
    ):
        raise CommandAcceptanceError(f"{label} must be a lower-case SHA-256 digest")
    return value


def _typed_interpreter_result(value: object) -> dict[str, str]:
    raw_result = _require_exact_fields(
        value, INTERPRETER_RESULT_FIELDS, "interpreter result"
    )
    result = {
        field: _require_nonempty_string(
            raw_result[field], f"interpreter result {field}"
        )
        for field in INTERPRETER_RESULT_FIELDS
    }
    if result["kind"] != "interpreter_result":
        raise CommandAcceptanceError(
            "interpreter result kind is not interpreter_result"
        )
    return result


def _candidate_identity(value: object) -> tuple[str, str]:
    candidate = _require_exact_fields(
        value, frozenset({"definition_id", "kind"}), "candidate"
    )
    return (
        _require_nonempty_string(candidate["definition_id"], "candidate definition_id"),
        _require_nonempty_string(candidate["kind"], "candidate kind"),
    )


def _typed_command_proposal(value: object, candidate_id: str) -> dict[str, object]:
    proposal = _require_exact_fields(value, COMMAND_PROPOSAL_FIELDS, "command proposal")
    normalized = {
        field: _require_nonempty_string(proposal[field], f"command proposal {field}")
        for field in (
            "command_id",
            "interaction_id",
            "intent_plan_id",
            "clause_id",
            "root_resolution_id",
        )
    }
    action_request = _require_mapping(
        proposal["action_request"], "command proposal action_request"
    )
    allowed_action_fields = {
        "activity_id",
        "actor_id",
        "source_id",
        "target_ids",
        "parameter_bindings",
    }
    if set(action_request) - allowed_action_fields or not {
        "activity_id",
        "actor_id",
    }.issubset(action_request):
        raise CommandAcceptanceError(
            "command proposal action_request has unexpected or missing fields"
        )
    activity_id = _require_nonempty_string(
        action_request["activity_id"], "action_request activity_id"
    )
    if activity_id != candidate_id:
        raise CommandAcceptanceError(
            "action_request activity_id differs from candidate"
        )
    if "parameter_bindings" in action_request:
        try:
            parameter_bindings, _facts, _refs = validate_frozen_adjudication_basis(
                action_request["parameter_bindings"], []
            )
        except PolicyBasisResolutionError as exc:
            raise CommandAcceptanceError(str(exc)) from exc
        normalized_action_request = _thaw(action_request)
        if not isinstance(normalized_action_request, dict):
            raise CommandAcceptanceError("action_request must be an object")
        normalized_action_request["parameter_bindings"] = parameter_bindings
        normalized["action_request"] = normalized_action_request
    else:
        normalized["action_request"] = _thaw(action_request)
    return normalized


def _interpreter_result_fingerprint(interpreter_result: Mapping[str, str]) -> str:
    return sha256(_INTERPRETER_RESULT_DOMAIN + canonical_json(dict(interpreter_result)))


def _input_fingerprint(command: Mapping[str, object]) -> str:
    material = {key: _thaw(command[key]) for key in ACCEPTED_INPUT_FIELDS}
    return sha256(_RUNTIME_COMMAND_INPUT_DOMAIN + canonical_json(material))


def _require_admitted_context(context: object) -> BoundCatalogContext:
    if not isinstance(context, BoundCatalogContext) or not context._is_admitted():
        raise CommandAcceptanceError(
            "catalog context must be an admitted bound context"
        )
    return context


def accept_command(
    interpreter_result: object,
    context: BoundCatalogContext,
    candidate: object,
    command_proposal: object,
    *,
    adjudication_basis: AcceptedAdjudicationBasis | None = None,
) -> dict[str, object] | CatalogGap:
    """Return a schema-shaped accepted command or typed catalog-gap evidence."""

    typed_result = _typed_interpreter_result(interpreter_result)
    admitted_context = _require_admitted_context(context)
    candidate_id, _candidate_kind = _candidate_identity(candidate)
    proposal = _typed_command_proposal(command_proposal, candidate_id)
    action_request = _require_mapping(
        proposal["action_request"], "accepted action_request"
    )
    if adjudication_basis is not None:
        if not is_accepted_basis_issued(adjudication_basis):
            raise CommandAcceptanceError(
                "adjudication basis must be resolver-produced evidence"
            )
        expected_bindings = adjudication_basis.runtime_parameter_bindings()
        actual_bindings = action_request.get("parameter_bindings", {})
        if actual_bindings != expected_bindings:
            raise CommandAcceptanceError(
                "accepted adjudication parameters differ from verified basis"
            )
        invocation_facts = adjudication_basis.runtime_invocation_facts()
    else:
        invocation_facts = []
        if any(
            isinstance(binding, Mapping)
            and binding.get("source_class") == "INVOCATION_ADJUDICATED"
            for binding in action_request.get("parameter_bindings", {}).values()
        ):
            raise CommandAcceptanceError(
                "adjudicated parameters require a verified policy basis"
            )
    try:
        normalized_parameters, normalized_facts = validate_adjudicated_input_surface(
            str(action_request["activity_id"]),
            action_request.get("parameter_bindings", {}),
            invocation_facts,
        )
        if adjudication_basis is not None:
            validate_policy_applicability_witnesses(
                adjudication_basis.verified_policies,
                str(action_request["activity_id"]),
                admitted_context,
            )
    except PolicyBasisResolutionError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    if adjudication_basis is not None and normalized_parameters != expected_bindings:
        raise CommandAcceptanceError(
            "accepted adjudication parameters differ from verified basis"
        )
    invocation_facts = normalized_facts
    try:
        catalog_result = bind_executable_catalog(admitted_context, candidate)
    except CatalogBindingError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    if catalog_result["status"] == "gap":
        return CatalogGap(
            _require_mapping(catalog_result["gap_report"], "catalog gap report")
        )

    binding = _require_mapping(catalog_result["binding"], "catalog binding")
    try:
        validate_executable_binding(admitted_context, binding)
    except CatalogBindingError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    command: dict[str, object] = {
        "schema_version": RUNTIME_COMMAND_SCHEMA_VERSION,
        **proposal,
        "command_kind": "action",
        "catalog_context_fingerprint": admitted_context.fingerprint,
        "input_fingerprint_generation": RUNTIME_COMMAND_INPUT_FINGERPRINT_GENERATION,
        "input_fingerprint": "",
        "disposition": "command.accepted",
        "invocation_facts": invocation_facts,
        "pending_child_invocations": [],
        "interpreter_result": typed_result,
        "interpreter_result_fingerprint_generation": INTERPRETER_RESULT_FINGERPRINT_GENERATION,
        "interpreter_result_fingerprint": _interpreter_result_fingerprint(typed_result),
        "catalog_context": admitted_context.to_dict(),
        "candidate_binding": _thaw(binding),
    }
    command["input_fingerprint"] = _input_fingerprint(command)
    return command


def validate_execution_proposal(
    accepted_command: object,
    context: BoundCatalogContext,
    candidate: object,
) -> None:
    """Verify a serialized command's exact basis and recomputed acceptance fingerprints."""

    command = _require_exact_fields(
        accepted_command, COMMAND_STATE_FIELDS, "accepted command"
    )
    admitted_context = _require_admitted_context(context)
    if command["schema_version"] != RUNTIME_COMMAND_SCHEMA_VERSION:
        raise CommandAcceptanceError("unsupported runtime command schema version")
    for field in (
        "command_id",
        "interaction_id",
        "intent_plan_id",
        "clause_id",
        "root_resolution_id",
    ):
        _require_nonempty_string(command[field], f"accepted command {field}")
    if command["command_kind"] != "action" or command["disposition"] not in {
        "command.accepted",
        "command.settled",
    }:
        raise CommandAcceptanceError("accepted command has an unsupported disposition")
    if not isinstance(command["invocation_facts"], list):
        raise CommandAcceptanceError(
            "accepted command invocation facts must be an array"
        )
    action_request = _require_mapping(
        command["action_request"], "accepted command action_request"
    )
    try:
        parameters, facts = validate_adjudicated_input_surface(
            _require_nonempty_string(
                action_request.get("activity_id"), "action_request activity_id"
            ),
            action_request.get("parameter_bindings", {}),
            command["invocation_facts"],
        )
    except PolicyBasisResolutionError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    if (
        parameters != action_request.get("parameter_bindings", {})
        or facts != command["invocation_facts"]
    ):
        raise CommandAcceptanceError(
            "accepted adjudication input differs from its normalized basis"
        )
    if not isinstance(command["pending_child_invocations"], list):
        raise CommandAcceptanceError(
            "accepted command pending child invocations must be an array"
        )
    if (
        command["disposition"] == "command.settled"
        and command["pending_child_invocations"]
    ):
        raise CommandAcceptanceError(
            "settled command retains pending child invocations"
        )
    if (
        command["input_fingerprint_generation"]
        != RUNTIME_COMMAND_INPUT_FINGERPRINT_GENERATION
    ):
        raise CommandAcceptanceError("unsupported command input fingerprint generation")
    if (
        command["interpreter_result_fingerprint_generation"]
        != INTERPRETER_RESULT_FINGERPRINT_GENERATION
    ):
        raise CommandAcceptanceError(
            "unsupported interpreter result fingerprint generation"
        )
    interpreter_result = _typed_interpreter_result(command["interpreter_result"])
    if command["interpreter_result_fingerprint"] != _interpreter_result_fingerprint(
        interpreter_result
    ):
        raise CommandAcceptanceError(
            "interpreter result fingerprint differs from accepted result"
        )
    if command["catalog_context_fingerprint"] != admitted_context.fingerprint:
        raise CommandAcceptanceError("stale catalog context")
    if command["catalog_context"] != admitted_context.to_dict():
        raise CommandAcceptanceError("catalog context differs from accepted basis")
    binding = _require_mapping(
        command["candidate_binding"], "accepted command catalog binding"
    )
    try:
        validate_executable_binding(admitted_context, binding)
    except CatalogBindingError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    candidate_id, candidate_kind = _candidate_identity(candidate)
    if candidate_id != binding["definition_id"] or candidate_kind != binding["kind"]:
        raise CommandAcceptanceError("candidate differs from accepted binding")
    _typed_command_proposal(
        {key: command[key] for key in COMMAND_PROPOSAL_FIELDS},
        candidate_id,
    )
    _require_sha256(command["input_fingerprint"], "accepted command input fingerprint")
    if command["input_fingerprint"] != _input_fingerprint(command):
        raise CommandAcceptanceError("input fingerprint differs from accepted command")
