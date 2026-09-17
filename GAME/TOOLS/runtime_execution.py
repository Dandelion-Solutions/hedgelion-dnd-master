"""Typed command acceptance over an exact, caller-supplied catalog context."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
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


INTERPRETER_RESULT_FIELDS: Final = frozenset(
    {"kind", "purpose", "bundle_id", "source_generation", "intent"}
)
INTERPRETER_RESULT_FINGERPRINT_GENERATION: Final = 1
RUNTIME_COMMAND_INPUT_FINGERPRINT_GENERATION: Final = 1
_INTERPRETER_RESULT_DOMAIN: Final = b"HDM_INTERPRETER_RESULT/1\n"
_RUNTIME_COMMAND_INPUT_DOMAIN: Final = b"HDM_RUNTIME_COMMAND_INPUT/1\n"


class CommandAcceptanceError(ValueError):
    """Raised when a proposed command cannot be accepted against its exact basis."""


@dataclass(frozen=True, slots=True)
class CatalogGap:
    """Typed non-acceptance evidence for an unavailable catalog candidate."""

    gap_report: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class AcceptedRuntimeCommand:
    """The immutable, catalog-backed acceptance record before mechanics execute."""

    interpreter_result: Mapping[str, str]
    interpreter_result_fingerprint: str
    catalog_context: Mapping[str, object]
    candidate_binding: Mapping[str, object]
    input_fingerprint: str

    def to_dict(self) -> dict[str, object]:
        """Return the complete serializable acceptance evidence."""

        return {
            "interpreter_result": dict(self.interpreter_result),
            "interpreter_result_fingerprint_generation": (
                INTERPRETER_RESULT_FINGERPRINT_GENERATION
            ),
            "interpreter_result_fingerprint": self.interpreter_result_fingerprint,
            "catalog_context": _thaw(self.catalog_context),
            "candidate_binding": _thaw(self.candidate_binding),
            "input_fingerprint_generation": RUNTIME_COMMAND_INPUT_FINGERPRINT_GENERATION,
            "input_fingerprint": self.input_fingerprint,
        }


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, Sequence) and not isinstance(value, str):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, str):
        return [_thaw(item) for item in value]
    return value


def _typed_interpreter_result(value: object) -> dict[str, str]:
    if not isinstance(value, Mapping) or set(value) != INTERPRETER_RESULT_FIELDS:
        raise CommandAcceptanceError("interpreter result does not satisfy its typed contract")
    result: dict[str, str] = {}
    for field in INTERPRETER_RESULT_FIELDS:
        field_value = value[field]
        if not isinstance(field_value, str) or not field_value:
            raise CommandAcceptanceError(f"interpreter result {field} must be a nonempty string")
        result[field] = field_value
    if result["kind"] != "interpreter_result":
        raise CommandAcceptanceError("interpreter result kind is not interpreter_result")
    return result


def _candidate_identity(value: object) -> tuple[str, str]:
    if not isinstance(value, Mapping) or set(value) != {"definition_id", "kind"}:
        raise CommandAcceptanceError("candidate must contain only definition_id and kind")
    definition_id = value["definition_id"]
    kind = value["kind"]
    if not isinstance(definition_id, str) or not definition_id:
        raise CommandAcceptanceError("candidate definition_id must be a nonempty string")
    if not isinstance(kind, str) or not kind:
        raise CommandAcceptanceError("candidate kind must be a nonempty string")
    return definition_id, kind


def _frozen_mapping(value: object, label: str) -> Mapping[str, object]:
    frozen = _freeze(value)
    if not isinstance(frozen, Mapping):
        raise CommandAcceptanceError(f"{label} must be an object")
    return frozen


def _acceptance_fingerprint(
    interpreter_result: Mapping[str, str],
    catalog_context: Mapping[str, object],
    candidate_binding: Mapping[str, object],
) -> str:
    return sha256(
        _RUNTIME_COMMAND_INPUT_DOMAIN
        + canonical_json(
            {
                "interpreter_result": dict(interpreter_result),
                "catalog_context": _thaw(catalog_context),
                "candidate_binding": _thaw(candidate_binding),
            }
        )
    )


def accept_command(
    interpreter_result: object,
    context: BoundCatalogContext,
    candidate: object,
) -> AcceptedRuntimeCommand | CatalogGap:
    """Accept exactly one typed candidate or return its catalog-bound gap evidence."""

    typed_result = _typed_interpreter_result(interpreter_result)
    _candidate_identity(candidate)
    if not isinstance(context, BoundCatalogContext):
        raise CommandAcceptanceError("catalog context must be an exact bound context")
    try:
        catalog_result = bind_executable_catalog(context, candidate)
    except CatalogBindingError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    if catalog_result["status"] == "gap":
        return CatalogGap(_frozen_mapping(catalog_result["gap_report"], "catalog gap report"))

    binding = _frozen_mapping(catalog_result["binding"], "catalog binding")
    try:
        validate_executable_binding(context, binding)
    except CatalogBindingError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    frozen_result = _frozen_mapping(typed_result, "interpreter result")
    typed_frozen_result = {key: str(frozen_result[key]) for key in INTERPRETER_RESULT_FIELDS}
    frozen_context = _frozen_mapping(context.to_dict(), "catalog context")
    interpreter_result_fingerprint = sha256(
        _INTERPRETER_RESULT_DOMAIN + canonical_json(typed_frozen_result)
    )
    return AcceptedRuntimeCommand(
        interpreter_result=MappingProxyType(typed_frozen_result),
        interpreter_result_fingerprint=interpreter_result_fingerprint,
        catalog_context=frozen_context,
        candidate_binding=binding,
        input_fingerprint=_acceptance_fingerprint(typed_frozen_result, frozen_context, binding),
    )


def validate_execution_proposal(
    accepted_command: AcceptedRuntimeCommand,
    context: BoundCatalogContext,
    candidate: object,
) -> None:
    """Reject execution if a later proposal differs from the accepted catalog basis."""

    if not isinstance(accepted_command, AcceptedRuntimeCommand):
        raise CommandAcceptanceError("accepted command has an invalid type")
    if not isinstance(context, BoundCatalogContext):
        raise CommandAcceptanceError("catalog context must be an exact bound context")
    try:
        validate_executable_binding(context, accepted_command.candidate_binding)
    except CatalogBindingError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    definition_id, kind = _candidate_identity(candidate)
    if (
        definition_id != accepted_command.candidate_binding["definition_id"]
        or kind != accepted_command.candidate_binding["kind"]
    ):
        raise CommandAcceptanceError("candidate differs from accepted binding")
    if context.to_dict() != _thaw(accepted_command.catalog_context):
        raise CommandAcceptanceError("catalog context differs from accepted basis")
