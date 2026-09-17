"""Typed acceptance and verification for authoritative ``runtime.command`` records."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
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


# framework_module_version: 1.0.2
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


class CatalogGap:
    """Typed non-acceptance evidence for an unavailable catalog candidate."""

    __slots__ = ("gap_report",)

    def __init__(self, gap_report: Mapping[str, object]) -> None:
        self.gap_report = MappingProxyType(dict(gap_report))


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
    if not isinstance(value, str) or len(value) != 64 or any(char not in _SHA256_HEX for char in value):
        raise CommandAcceptanceError(f"{label} must be a lower-case SHA-256 digest")
    return value


def _typed_interpreter_result(value: object) -> dict[str, str]:
    raw_result = _require_exact_fields(value, INTERPRETER_RESULT_FIELDS, "interpreter result")
    result = {
        field: _require_nonempty_string(raw_result[field], f"interpreter result {field}")
        for field in INTERPRETER_RESULT_FIELDS
    }
    if result["kind"] != "interpreter_result":
        raise CommandAcceptanceError("interpreter result kind is not interpreter_result")
    return result


def _candidate_identity(value: object) -> tuple[str, str]:
    candidate = _require_exact_fields(value, frozenset({"definition_id", "kind"}), "candidate")
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
    action_request = _require_mapping(proposal["action_request"], "command proposal action_request")
    allowed_action_fields = {"activity_id", "actor_id", "source_id", "target_ids", "parameter_bindings"}
    if set(action_request) - allowed_action_fields or not {"activity_id", "actor_id"}.issubset(
        action_request
    ):
        raise CommandAcceptanceError("command proposal action_request has unexpected or missing fields")
    activity_id = _require_nonempty_string(action_request["activity_id"], "action_request activity_id")
    if activity_id != candidate_id:
        raise CommandAcceptanceError("action_request activity_id differs from candidate")
    normalized["action_request"] = _thaw(action_request)
    return normalized


def _interpreter_result_fingerprint(interpreter_result: Mapping[str, str]) -> str:
    return sha256(_INTERPRETER_RESULT_DOMAIN + canonical_json(dict(interpreter_result)))


def _input_fingerprint(command: Mapping[str, object]) -> str:
    material = {
        key: _thaw(command[key])
        for key in ACCEPTED_INPUT_FIELDS
    }
    return sha256(_RUNTIME_COMMAND_INPUT_DOMAIN + canonical_json(material))


def _require_admitted_context(context: object) -> BoundCatalogContext:
    if not isinstance(context, BoundCatalogContext) or not context._is_admitted():
        raise CommandAcceptanceError("catalog context must be an admitted bound context")
    return context


def accept_command(
    interpreter_result: object,
    context: BoundCatalogContext,
    candidate: object,
    command_proposal: object,
) -> dict[str, object] | CatalogGap:
    """Return a schema-shaped accepted command or typed catalog-gap evidence."""

    typed_result = _typed_interpreter_result(interpreter_result)
    admitted_context = _require_admitted_context(context)
    candidate_id, _candidate_kind = _candidate_identity(candidate)
    proposal = _typed_command_proposal(command_proposal, candidate_id)
    try:
        catalog_result = bind_executable_catalog(admitted_context, candidate)
    except CatalogBindingError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    if catalog_result["status"] == "gap":
        return CatalogGap(_require_mapping(catalog_result["gap_report"], "catalog gap report"))

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
        "invocation_facts": [],
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

    command = _require_exact_fields(accepted_command, COMMAND_STATE_FIELDS, "accepted command")
    admitted_context = _require_admitted_context(context)
    if command["schema_version"] != RUNTIME_COMMAND_SCHEMA_VERSION:
        raise CommandAcceptanceError("unsupported runtime command schema version")
    for field in ("command_id", "interaction_id", "intent_plan_id", "clause_id", "root_resolution_id"):
        _require_nonempty_string(command[field], f"accepted command {field}")
    if command["command_kind"] != "action" or command["disposition"] not in {
        "command.accepted",
        "command.settled",
    }:
        raise CommandAcceptanceError("accepted command has an unsupported disposition")
    if not isinstance(command["invocation_facts"], list):
        raise CommandAcceptanceError("accepted command invocation facts must be an array")
    if not isinstance(command["pending_child_invocations"], list):
        raise CommandAcceptanceError("accepted command pending child invocations must be an array")
    if command["disposition"] == "command.settled" and command["pending_child_invocations"]:
        raise CommandAcceptanceError("settled command retains pending child invocations")
    if command["input_fingerprint_generation"] != RUNTIME_COMMAND_INPUT_FINGERPRINT_GENERATION:
        raise CommandAcceptanceError("unsupported command input fingerprint generation")
    if command["interpreter_result_fingerprint_generation"] != INTERPRETER_RESULT_FINGERPRINT_GENERATION:
        raise CommandAcceptanceError("unsupported interpreter result fingerprint generation")
    interpreter_result = _typed_interpreter_result(command["interpreter_result"])
    if command["interpreter_result_fingerprint"] != _interpreter_result_fingerprint(interpreter_result):
        raise CommandAcceptanceError("interpreter result fingerprint differs from accepted result")
    if command["catalog_context_fingerprint"] != admitted_context.fingerprint:
        raise CommandAcceptanceError("stale catalog context")
    if command["catalog_context"] != admitted_context.to_dict():
        raise CommandAcceptanceError("catalog context differs from accepted basis")
    binding = _require_mapping(command["candidate_binding"], "accepted command catalog binding")
    try:
        validate_executable_binding(admitted_context, binding)
    except CatalogBindingError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    candidate_id, candidate_kind = _candidate_identity(candidate)
    if candidate_id != binding["definition_id"] or candidate_kind != binding["kind"]:
        raise CommandAcceptanceError("candidate differs from accepted binding")
    _typed_command_proposal(
        {
            key: command[key]
            for key in COMMAND_PROPOSAL_FIELDS
        },
        candidate_id,
    )
    _require_sha256(command["input_fingerprint"], "accepted command input fingerprint")
    if command["input_fingerprint"] != _input_fingerprint(command):
        raise CommandAcceptanceError("input fingerprint differs from accepted command")
