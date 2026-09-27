"""Transient typed controls for one logical HDM turn."""

from __future__ import annotations

import re
from collections.abc import Iterator, Mapping
from copy import deepcopy
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import Any, NoReturn, Protocol
from uuid import uuid4

PHASE_RESULT_KINDS = {
    "INTERPRETER": {"interpreter_result"},
    "DRAMATURG": {"preparation_draft"},
    "ACTOR": {"actor_proposal"},
    "CHRONICLER": {"story_projection_draft"},
    "NARRATOR": {"narration_result"},
}
RESULT_REQUIRED_FIELDS = {
    "interpreter_result": frozenset(
        {"kind", "purpose", "bundle_id", "source_generation", "intent"}
    ),
    "preparation_draft": frozenset(
        {"kind", "purpose", "bundle_id", "source_generation", "pressures"}
    ),
    "actor_proposal": frozenset(
        {"kind", "purpose", "bundle_id", "source_generation", "subject_id", "proposal"}
    ),
    "story_projection_draft": frozenset(
        {"kind", "purpose", "bundle_id", "source_generation", "source_refs"}
    ),
    "narration_result": frozenset(
        {
            "kind",
            "purpose",
            "source_generation",
            "response_language",
            "bundle_id",
            "recipient_id",
            "prose",
            "disclosure_refs",
        }
    ),
}
EXECUTION_HANDOFF_KIND = "execution_result"
EXECUTION_HANDOFF_REQUIRED_FIELDS = frozenset(
    {
        "kind",
        "accepted_command_id",
        "accepted_input_fingerprint",
        "execution_owner_id",
        "resolution_id",
        "status",
        "segment_id",
        "event_id",
        "turn_id",
        "recipient_role",
        "purpose",
        "bundle_id",
        "recipient_id",
    }
)
FORBIDDEN_HANDOFF_KEYS = frozenset(
    {
        "raw_bundle",
        "context_trace",
        "trace",
        "private_diagnostics",
        "diagnostic_evidence",
        "private",
        "private_context",
        "hidden_reasoning",
        "role_frame",
        "tool_payload",
    }
)
FALLBACKS = frozenset({"BLOCKED", "DEGRADED", "CLARIFICATION", "DETERMINISTIC_PATH"})
EXECUTION_STATES = frozenset(
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
INTERNAL_NARRATION_TOKENS = frozenset(
    FALLBACKS
    | EXECUTION_STATES
    | frozenset(PHASE_RESULT_KINDS)
    | frozenset(
        result_kind
        for result_kinds in PHASE_RESULT_KINDS.values()
        for result_kind in result_kinds
    )
    | frozenset({EXECUTION_HANDOFF_KIND})
)
_INTERNAL_NARRATION_TOKEN_PATTERN = re.compile(
    r"(?<!\w)(?:"
    + "|".join(
        re.escape(token)
        for token in sorted(
            INTERNAL_NARRATION_TOKENS, key=lambda token: (-len(token), token)
        )
    )
    + r")(?!\w)"
)
SHA256_HEX = frozenset("0123456789abcdef")
_HANDOFF_SEAL = object()
_CONTEXT_BASIS_SEAL = object()
_PHASE_RESULT_SEAL = object()
_RESPONSE_LANGUAGE_SEAL = object()
_CONTEXT_DIAGNOSTIC_KEYS = frozenset(
    {
        "trace",
        "context_trace",
        "private_diagnostics",
        "diagnostic_evidence",
        "raw_bundle",
        "private",
        "private_context",
        "hidden_reasoning",
        "role_frame",
        "tool_payload",
    }
)


class ContextAssembler(Protocol):
    """The existing injected RuntimeHost ContextService capability."""

    def assemble(
        self,
        request: dict[str, object],
        candidates: list[dict[str, object]],
    ) -> dict[str, object]: ...


@dataclass(frozen=True, slots=True, init=False)
class AcceptedContextBasis:
    """Exact TurnRuntime-issued, per-phase proof of one ContextService result."""

    turn_id: str
    role: str
    purpose: str
    profile_id: str
    subject_id: str
    recipient_id: str
    source_frontier: str
    bundle_id: str
    assembly_ordinal: int
    _turn_seal: object = dataclass_field(repr=False, compare=False)
    _seal: object = dataclass_field(repr=False, compare=False)
    _bundle: dict[str, object] = dataclass_field(repr=False, compare=False)

    def __init__(
        self,
        *,
        _seal: object,
        _turn_seal: object,
        turn_id: str,
        role: str,
        purpose: str,
        profile_id: str,
        subject_id: str,
        recipient_id: str,
        source_frontier: str,
        bundle_id: str,
        assembly_ordinal: int,
        bundle: dict[str, object],
    ) -> None:
        if _seal is not _CONTEXT_BASIS_SEAL:
            raise TypeError("accepted Context basis is TurnRuntime-issued")
        for label, value in (
            ("turn_id", turn_id),
            ("role", role),
            ("purpose", purpose),
            ("profile_id", profile_id),
            ("subject_id", subject_id),
            ("recipient_id", recipient_id),
            ("source_frontier", source_frontier),
            ("bundle_id", bundle_id),
        ):
            if not isinstance(value, str) or not value:
                raise TypeError(f"accepted Context basis {label} must be nonempty")
            object.__setattr__(self, label, value)
        if (
            isinstance(assembly_ordinal, bool)
            or not isinstance(assembly_ordinal, int)
            or assembly_ordinal < 1
        ):
            raise TypeError("accepted Context basis assembly ordinal must be positive")
        if not isinstance(bundle, dict):
            raise TypeError("accepted Context basis bundle must be an object")
        object.__setattr__(self, "assembly_ordinal", assembly_ordinal)
        object.__setattr__(self, "_turn_seal", _turn_seal)
        object.__setattr__(self, "_seal", _seal)
        object.__setattr__(self, "_bundle", deepcopy(bundle))

    @property
    def bundle(self) -> dict[str, object]:
        """Return an isolated copy of the admitted semantic bundle, never its trace."""
        return deepcopy(self._bundle)

    def __reduce__(self) -> NoReturn:
        raise TypeError("accepted Context basis is transient and cannot be serialized")

    def __reduce_ex__(self, protocol: int) -> NoReturn:
        raise TypeError("accepted Context basis is transient and cannot be serialized")


@dataclass(frozen=True, slots=True, init=False)
class ResolvedResponseLanguage:
    """TurnRuntime-issued opaque language basis for one human-visible response."""

    language: str
    turn_id: str
    _turn_seal: object = dataclass_field(repr=False, compare=False)
    _seal: object = dataclass_field(repr=False, compare=False)

    def __init__(
        self,
        *,
        _seal: object,
        _turn_seal: object,
        turn_id: str,
        language: str,
    ) -> None:
        if _seal is not _RESPONSE_LANGUAGE_SEAL:
            raise TypeError("ResolvedResponseLanguage is TurnRuntime-issued")
        if not isinstance(language, str) or not language or not language.strip():
            raise TypeError("ResolvedResponseLanguage must be nonempty opaque text")
        if not isinstance(turn_id, str) or not turn_id:
            raise TypeError("ResolvedResponseLanguage turn_id must be nonempty")
        object.__setattr__(self, "language", language)
        object.__setattr__(self, "turn_id", turn_id)
        object.__setattr__(self, "_turn_seal", _turn_seal)
        object.__setattr__(self, "_seal", _seal)

    def __reduce__(self) -> NoReturn:
        raise TypeError(
            "ResolvedResponseLanguage is transient and cannot be serialized"
        )

    def __reduce_ex__(self, protocol: int) -> NoReturn:
        raise TypeError(
            "ResolvedResponseLanguage is transient and cannot be serialized"
        )


@dataclass(frozen=True, slots=True, init=False)
class AcceptedPhaseResult:
    """Minimum registered result sealed to its accepted source phase and scope."""

    kind: str
    role: str
    purpose: str
    profile_id: str
    subject_id: str
    recipient_id: str
    source_frontier: str
    bundle_id: str
    turn_id: str
    assembly_ordinal: int
    _turn_seal: object = dataclass_field(repr=False, compare=False)
    _seal: object = dataclass_field(repr=False, compare=False)
    _result: dict[str, Any] = dataclass_field(repr=False, compare=False)

    def __init__(
        self,
        *,
        _seal: object,
        _turn_seal: object,
        kind: str,
        role: str,
        purpose: str,
        profile_id: str,
        subject_id: str,
        recipient_id: str,
        source_frontier: str,
        bundle_id: str,
        turn_id: str,
        assembly_ordinal: int,
        result: dict[str, Any],
    ) -> None:
        if _seal is not _PHASE_RESULT_SEAL:
            raise TypeError("accepted phase result is TurnRuntime-issued")
        for label, value in (
            ("kind", kind),
            ("role", role),
            ("purpose", purpose),
            ("profile_id", profile_id),
            ("subject_id", subject_id),
            ("recipient_id", recipient_id),
            ("source_frontier", source_frontier),
            ("bundle_id", bundle_id),
            ("turn_id", turn_id),
        ):
            if not isinstance(value, str) or not value:
                raise TypeError(f"accepted phase result {label} must be nonempty")
            object.__setattr__(self, label, value)
        if not isinstance(result, dict):
            raise TypeError("accepted phase result payload must be an object")
        object.__setattr__(self, "assembly_ordinal", assembly_ordinal)
        object.__setattr__(self, "_turn_seal", _turn_seal)
        object.__setattr__(self, "_seal", _seal)
        object.__setattr__(self, "_result", deepcopy(result))

    def to_dict(self) -> dict[str, Any]:
        """Return only the minimal schema-validated semantic payload."""
        return deepcopy(self._result)

    def __reduce__(self) -> NoReturn:
        raise TypeError("accepted phase result is transient and cannot be serialized")

    def __reduce_ex__(self, protocol: int) -> NoReturn:
        raise TypeError("accepted phase result is transient and cannot be serialized")


@dataclass(frozen=True, slots=True, init=False)
class ExecutionHandoff(Mapping[str, str]):
    """Owner-issued typed execution evidence admitted to one role phase."""

    kind: str
    accepted_command_id: str
    accepted_input_fingerprint: str
    execution_owner_id: str
    resolution_id: str
    status: str
    segment_id: str
    event_id: str
    turn_id: str
    recipient_role: str
    purpose: str
    bundle_id: str
    recipient_id: str

    def __init__(
        self,
        *,
        _seal: object,
        kind: str,
        accepted_command_id: str,
        accepted_input_fingerprint: str,
        execution_owner_id: str,
        resolution_id: str,
        status: str,
        segment_id: str,
        event_id: str,
        turn_id: str,
        recipient_role: str,
        purpose: str,
        bundle_id: str,
        recipient_id: str,
    ) -> None:
        if _seal is not _HANDOFF_SEAL:
            raise TypeError("execution handoff is owner-issued")
        for field, value in (
            ("kind", kind),
            ("accepted_command_id", accepted_command_id),
            ("accepted_input_fingerprint", accepted_input_fingerprint),
            ("execution_owner_id", execution_owner_id),
            ("resolution_id", resolution_id),
            ("status", status),
            ("segment_id", segment_id),
            ("event_id", event_id),
            ("turn_id", turn_id),
            ("recipient_role", recipient_role),
            ("purpose", purpose),
            ("bundle_id", bundle_id),
            ("recipient_id", recipient_id),
        ):
            if not isinstance(value, str) or not value:
                raise TypeError(f"execution handoff {field} must be a nonempty string")
            object.__setattr__(self, field, value)

    def to_dict(self) -> dict[str, str]:
        return {field: getattr(self, field) for field in EXECUTION_HANDOFF_REQUIRED_FIELDS}

    def __getitem__(self, key: str) -> str:
        return self.to_dict()[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.to_dict())

    def __len__(self) -> int:
        return len(EXECUTION_HANDOFF_REQUIRED_FIELDS)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ExecutionHandoff):
            return self.to_dict() == other.to_dict()
        if isinstance(other, Mapping):
            return self.to_dict() == dict(other)
        return NotImplemented


class TurnContractError(ValueError):
    """A transient turn control contract was not satisfied."""


def _nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise TurnContractError(f"{label} must be a nonempty string")
    return value


def bind_resolved_response_language(
    envelope: dict[str, Any], language: object
) -> ResolvedResponseLanguage:
    """Bind the already-resolved opaque language value to one current turn."""
    if not isinstance(envelope, dict):
        raise TurnContractError("turn envelope must be an object")
    turn_id = _nonempty_string(envelope.get("turn_id"), "turn_id")
    turn_seal = envelope.get("_turn_seal")
    if turn_seal is None:
        raise TurnContractError("turn envelope is not a current TurnRuntime envelope")
    if not isinstance(language, str) or not language or not language.strip():
        raise TurnContractError("ResolvedResponseLanguage must be nonempty opaque text")

    existing = envelope.get("_resolved_response_language_basis")
    if existing is not None:
        current = current_resolved_response_language(envelope)
        if current != language:
            raise TurnContractError(
                "ResolvedResponseLanguage is already bound for this turn"
            )
        return existing
    if "response_language" in envelope:
        raise TurnContractError(
            "caller-shaped response language cannot establish ResolvedResponseLanguage"
        )

    basis = ResolvedResponseLanguage(
        _seal=_RESPONSE_LANGUAGE_SEAL,
        _turn_seal=turn_seal,
        turn_id=turn_id,
        language=language,
    )
    envelope["response_language"] = language
    envelope["_resolved_response_language_basis"] = basis
    return basis


def current_resolved_response_language(
    envelope: dict[str, Any], binding: dict[str, Any] | None = None
) -> str:
    """Return the language only when its sealed basis remains current for this turn."""
    if not isinstance(envelope, dict):
        raise TurnContractError("turn envelope must be an object")
    basis = envelope.get("_resolved_response_language_basis")
    if (
        type(basis) is not ResolvedResponseLanguage
        or basis._seal is not _RESPONSE_LANGUAGE_SEAL
    ):
        raise TurnContractError("current ResolvedResponseLanguage basis is required")
    if basis._turn_seal is not envelope.get(
        "_turn_seal"
    ) or basis.turn_id != envelope.get("turn_id"):
        raise TurnContractError("ResolvedResponseLanguage is not current for this turn")
    if envelope.get("response_language") != basis.language:
        raise TurnContractError(
            "current response language differs from its accepted basis"
        )
    if binding is not None and (
        not isinstance(binding, dict)
        or binding.get("response_language_basis") is not basis
        or binding.get("response_language") != basis.language
    ):
        raise TurnContractError(
            "Narrator response language differs from its accepted basis"
        )
    return basis.language


def is_internal_narration_text(value: str) -> bool:
    """Identify registered machine tokens embedded in ordinary prose."""
    return _INTERNAL_NARRATION_TOKEN_PATTERN.search(value) is not None


def start_turn(turn_id: str, accepted_frontier: str, protected_narrator_capacity: int) -> dict[str, Any]:
    """Start a control-only envelope; it deliberately carries no gameplay state."""
    _nonempty_string(turn_id, "turn_id")
    _nonempty_string(accepted_frontier, "accepted_frontier")
    if (
        isinstance(protected_narrator_capacity, bool)
        or not isinstance(protected_narrator_capacity, int)
        or protected_narrator_capacity < 0
    ):
        raise TurnContractError("protected_narrator_capacity must be a nonnegative integer")
    return {
        "turn_id": turn_id,
        "accepted_frontier": accepted_frontier,
        "protected_narrator_capacity": protected_narrator_capacity,
        "auxiliary_capacity": 0,
        "phase_bindings": {},
        "accepted_results": {},
        "accepted_handoffs": {},
        "_resolved_response_language_basis": None,
        "remaining_narrator_capacity": protected_narrator_capacity,
        "emitted_payload": None,
        "_turn_seal": object(),
        "_context_assembly_sequence": 0,
        "_bound_context_basis_ids": set(),
    }


def _validate_phase_contract(
    role: str,
    purpose: str,
    profile_id: str,
    allowed_results: tuple[str, ...],
    subject_id: str | None,
    recipient_id: str | None,
    allowed_handoffs: tuple[str, ...],
    allowed_prior_results: tuple[str, ...],
) -> None:
    if not isinstance(role, str) or role not in PHASE_RESULT_KINDS:
        raise TurnContractError("unregistered role")
    for label, value in (("purpose", purpose), ("profile_id", profile_id)):
        _nonempty_string(value, label)
    if (
        not isinstance(allowed_results, tuple)
        or not allowed_results
        or any(
            not isinstance(item, str) or item not in PHASE_RESULT_KINDS[role]
            for item in allowed_results
        )
    ):
        raise TurnContractError(
            "allowed_results must be registered for the bound phase"
        )
    if not isinstance(allowed_handoffs, tuple) or any(
        item != EXECUTION_HANDOFF_KIND for item in allowed_handoffs
    ):
        raise TurnContractError("allowed_handoffs must be registered typed handoffs")
    if role == "NARRATOR" and allowed_handoffs != (EXECUTION_HANDOFF_KIND,):
        raise TurnContractError("Narrator requires an owner-verified execution handoff")
    if (
        not isinstance(allowed_prior_results, tuple)
        or any(
            not isinstance(item, str) or item not in RESULT_REQUIRED_FIELDS
            for item in allowed_prior_results
        )
        or len(allowed_prior_results) != len(set(allowed_prior_results))
    ):
        raise TurnContractError(
            "allowed prior results must be unique registered result kinds"
        )
    for label, value in (("subject_id", subject_id), ("recipient_id", recipient_id)):
        if value is not None:
            _nonempty_string(value, label)
    if role == "NARRATOR" and recipient_id is None:
        raise TurnContractError("Narrator requires a recipient scope")
    if role == "ACTOR" and subject_id is None:
        raise TurnContractError("Actor requires a subject scope")


def bind_phase_from_context(
    envelope: dict[str, Any],
    role: str,
    purpose: str,
    profile_id: str,
    context_service: ContextAssembler,
    request: dict[str, object],
    candidates: list[dict[str, object]],
    allowed_results: tuple[str, ...],
    *,
    subject_id: str | None = None,
    recipient_id: str | None = None,
    allowed_handoffs: tuple[str, ...] = (),
    allowed_prior_results: tuple[str, ...] = (),
) -> dict[str, Any]:
    """Assemble once through the injected ContextService, then bind its sealed basis."""
    _validate_phase_contract(
        role,
        purpose,
        profile_id,
        allowed_results,
        subject_id,
        recipient_id,
        allowed_handoffs,
        allowed_prior_results,
    )
    if not isinstance(envelope, dict):
        raise TurnContractError("turn envelope must be an object")
    if role == "NARRATOR":
        current_resolved_response_language(envelope)
    turn_id = _nonempty_string(envelope.get("turn_id"), "turn_id")
    frontier = _nonempty_string(envelope.get("accepted_frontier"), "accepted_frontier")
    turn_seal = envelope.get("_turn_seal")
    if turn_seal is None:
        raise TurnContractError("turn envelope is not a current TurnRuntime envelope")
    if not isinstance(request, dict) or not isinstance(candidates, list):
        raise TurnContractError("ContextService request and candidates must be objects")
    request_subject = _nonempty_string(request.get("subject_id"), "Context subject_id")
    request_recipient = _nonempty_string(
        request.get("recipient_id"), "Context recipient_id"
    )
    expected_request = {
        "role": role,
        "purpose": purpose,
        "profile_id": profile_id,
        "source_frontier": frontier,
    }
    for field_name, expected in expected_request.items():
        if request.get(field_name) != expected:
            raise TurnContractError(
                f"Context request {field_name} does not match phase binding"
            )
    if subject_id is not None and request_subject != subject_id:
        raise TurnContractError("Context subject does not match phase binding")
    if recipient_id is not None and request_recipient != recipient_id:
        raise TurnContractError("Context recipient does not match phase binding")
    if role == "ACTOR" and request_subject != subject_id:
        raise TurnContractError("Actor Context subject does not match phase binding")
    bound_subject = request_subject if subject_id is None else subject_id
    bound_recipient = request_recipient if recipient_id is None else recipient_id
    assembler = getattr(context_service, "assemble", None)
    if not callable(assembler):
        raise TurnContractError("injected ContextService capability is required")

    # This exact existing RuntimeHost capability is the sole basis issuer input.
    assembled = assembler(request, candidates)
    if not isinstance(assembled, dict):
        raise TurnContractError("ContextService result must be an object")
    if assembled.get("outcome") not in {"ASSEMBLED", "ASSEMBLED_DEGRADED"}:
        raise TurnContractError(
            "ContextService did not produce an assembled phase basis"
        )
    bundle = assembled.get("bundle")
    if not isinstance(bundle, dict):
        raise TurnContractError("ContextService result is missing its role bundle")
    if _CONTEXT_DIAGNOSTIC_KEYS.intersection(bundle):
        raise TurnContractError(
            "Context bundle contains diagnostic or private transport"
        )
    if "bundle_id" in bundle:
        raise TurnContractError("ContextService bundle cannot supply its identity")
    expected_bundle = {
        "role": role,
        "purpose": purpose,
        "profile_id": profile_id,
        "subject_id": bound_subject,
        "recipient_id": bound_recipient,
        "source_frontier": frontier,
    }
    for field_name, expected in expected_bundle.items():
        if bundle.get(field_name) != expected:
            raise TurnContractError(
                f"Context bundle {field_name} does not match phase binding"
            )

    assembly_ordinal = envelope.get("_context_assembly_sequence")
    if (
        isinstance(assembly_ordinal, bool)
        or not isinstance(assembly_ordinal, int)
        or assembly_ordinal < 0
    ):
        raise TurnContractError("turn Context assembly sequence is invalid")
    assembly_ordinal += 1
    basis = AcceptedContextBasis(
        _seal=_CONTEXT_BASIS_SEAL,
        _turn_seal=turn_seal,
        turn_id=turn_id,
        role=role,
        purpose=purpose,
        profile_id=profile_id,
        subject_id=bound_subject,
        recipient_id=bound_recipient,
        source_frontier=frontier,
        bundle_id=uuid4().hex,
        assembly_ordinal=assembly_ordinal,
        bundle=bundle,
    )
    envelope["_context_assembly_sequence"] = assembly_ordinal
    return bind_phase(
        envelope,
        role,
        purpose,
        profile_id,
        basis,
        allowed_results,
        subject_id=bound_subject,
        recipient_id=bound_recipient,
        allowed_handoffs=allowed_handoffs,
        allowed_prior_results=allowed_prior_results,
    )


def bind_phase(
    envelope: dict[str, Any],
    role: str,
    purpose: str,
    profile_id: str,
    context_basis: object,
    allowed_results: tuple[str, ...],
    *,
    subject_id: str | None = None,
    recipient_id: str | None = None,
    allowed_handoffs: tuple[str, ...] = (),
    allowed_prior_results: tuple[str, ...] = (),
) -> dict[str, Any]:
    """Bind a phase only to an exact basis issued by one ContextService assembly."""
    _validate_phase_contract(
        role,
        purpose,
        profile_id,
        allowed_results,
        subject_id,
        recipient_id,
        allowed_handoffs,
        allowed_prior_results,
    )
    if not isinstance(envelope, dict) or not isinstance(
        context_basis, AcceptedContextBasis
    ):
        raise TurnContractError("accepted Context basis is required")
    if role == "NARRATOR":
        current_resolved_response_language(envelope)
    basis = context_basis
    if basis._seal is not _CONTEXT_BASIS_SEAL:
        raise TurnContractError("accepted Context basis is not TurnRuntime-issued")
    turn_seal = envelope.get("_turn_seal")
    if (
        basis._turn_seal is not turn_seal
        or basis.turn_id != envelope.get("turn_id")
        or basis.source_frontier != envelope.get("accepted_frontier")
    ):
        raise TurnContractError("accepted Context basis is not current for this turn")
    if (
        basis.role != role
        or basis.purpose != purpose
        or basis.profile_id != profile_id
        or (subject_id is not None and basis.subject_id != subject_id)
        or (recipient_id is not None and basis.recipient_id != recipient_id)
    ):
        raise TurnContractError(
            "accepted Context basis scope does not match phase binding"
        )
    if role == "ACTOR" and basis.subject_id != subject_id:
        raise TurnContractError("Actor Context basis requires an exact subject scope")
    if role == "NARRATOR" and basis.recipient_id != recipient_id:
        raise TurnContractError(
            "Narrator Context basis requires an exact recipient scope"
        )
    phase_bindings = envelope.get("phase_bindings")
    if not isinstance(phase_bindings, dict):
        raise TurnContractError("turn envelope phase bindings are invalid")
    if any(
        isinstance(existing, dict) and existing.get("context_basis") is basis
        for existing in phase_bindings.values()
    ):
        raise TurnContractError("accepted Context basis is already bound to a phase")
    bound_basis_ids = envelope.get("_bound_context_basis_ids")
    if not isinstance(bound_basis_ids, set):
        raise TurnContractError("turn Context-basis consumption state is invalid")
    if basis.bundle_id in bound_basis_ids:
        raise TurnContractError("accepted Context basis is already bound to a phase")
    prior_results = _collect_prior_results(envelope, basis, allowed_prior_results)
    previous_binding = phase_bindings.get(role)
    if isinstance(previous_binding, dict):
        previous_basis = _validate_bound_context_basis(envelope, role, previous_binding)
        if previous_basis.bundle_id != basis.bundle_id:
            accepted_handoffs = envelope.get("accepted_handoffs")
            if not isinstance(accepted_handoffs, dict):
                raise TurnContractError("turn envelope accepted handoffs are invalid")
            previous_handoffs = accepted_handoffs.get(role, [])
            if not isinstance(previous_handoffs, list):
                raise TurnContractError("turn envelope accepted handoffs are invalid")
            for handoff in previous_handoffs:
                if (
                    type(handoff) is not ExecutionHandoff
                    or handoff.turn_id != envelope.get("turn_id")
                    or handoff.recipient_role != role
                    or handoff.purpose != previous_binding.get("purpose")
                    or handoff.bundle_id != previous_binding.get("bundle_id")
                    or handoff.recipient_id != previous_binding.get("recipient_id")
                ):
                    raise TurnContractError(
                        "prior execution handoff is not bound to the replaced phase"
                    )
            accepted_handoffs[role] = []
    binding = {
        "role": role,
        "purpose": purpose,
        "profile_id": profile_id,
        "bundle_id": basis.bundle_id,
        "context_basis": basis,
        "subject_id": basis.subject_id,
        "recipient_id": basis.recipient_id,
        "source_frontier": basis.source_frontier,
        "assembly_ordinal": basis.assembly_ordinal,
        "allowed_results": list(allowed_results),
        "allowed_handoffs": list(allowed_handoffs),
        "allowed_prior_results": list(allowed_prior_results),
        "prior_results": prior_results,
    }
    if role == "NARRATOR":
        response_language = current_resolved_response_language(envelope)
        binding["response_language"] = response_language
        binding["response_language_basis"] = envelope[
            "_resolved_response_language_basis"
        ]
    phase_bindings[role] = binding
    bound_basis_ids.add(basis.bundle_id)
    return binding


def _collect_prior_results(
    envelope: dict[str, Any],
    basis: AcceptedContextBasis,
    allowed_result_kinds: tuple[str, ...],
) -> tuple[AcceptedPhaseResult, ...]:
    phase_bindings = envelope.get("phase_bindings")
    if not isinstance(phase_bindings, dict):
        raise TurnContractError("turn envelope phase bindings are invalid")
    selected: list[AcceptedPhaseResult] = []
    for result_kind in allowed_result_kinds:
        if result_kind == "story_projection_draft":
            raise TurnContractError(
                "Chronicler Story output is not a same-envelope prior result"
            )
        matches = [
            (source_role, binding, binding["accepted_phase_result"])
            for source_role, binding in phase_bindings.items()
            if isinstance(binding, dict)
            and isinstance(binding.get("accepted_phase_result"), AcceptedPhaseResult)
            and binding["accepted_phase_result"].kind == result_kind
        ]
        if len(matches) != 1:
            raise TurnContractError("allowed prior result is absent or ambiguous")
        source_role, source_binding, prior = matches[0]
        source_basis = _validate_bound_context_basis(
            envelope, source_role, source_binding
        )
        if (
            prior._seal is not _PHASE_RESULT_SEAL
            or prior._turn_seal is not basis._turn_seal
            or prior.turn_id != basis.turn_id
            or prior.role != source_role
            or prior.role != source_basis.role
            or prior.purpose != source_basis.purpose
            or prior.profile_id != source_basis.profile_id
            or prior.subject_id != source_basis.subject_id
            or prior.recipient_id != source_basis.recipient_id
            or prior.bundle_id != source_basis.bundle_id
            or prior.source_frontier != basis.source_frontier
            or prior.assembly_ordinal >= basis.assembly_ordinal
        ):
            raise TurnContractError(
                "prior result is not an earlier accepted turn result"
            )
        if prior.recipient_id != basis.recipient_id:
            raise TurnContractError(
                "prior result recipient scope differs from Context basis"
            )
        if prior.kind == "actor_proposal" and prior.subject_id != basis.subject_id:
            raise TurnContractError(
                "Actor prior result subject differs from Context basis"
            )
        prior_payload = prior.to_dict()
        if (
            set(prior_payload) != RESULT_REQUIRED_FIELDS[result_kind]
            or prior_payload.get("kind") != result_kind
            or prior_payload.get("bundle_id") != prior.bundle_id
            or prior_payload.get("source_generation") != prior.source_frontier
            or (
                "purpose" in RESULT_REQUIRED_FIELDS[result_kind]
                and prior_payload.get("purpose") != prior.purpose
            )
            or (
                "subject_id" in RESULT_REQUIRED_FIELDS[result_kind]
                and prior_payload.get("subject_id") != prior.subject_id
            )
            or (
                "recipient_id" in RESULT_REQUIRED_FIELDS[result_kind]
                and prior_payload.get("recipient_id") != prior.recipient_id
            )
        ):
            raise TurnContractError(
                "prior result payload is not its registered minimum"
            )
        selected.append(prior)
    return tuple(selected)


def _validate_bound_context_basis(
    envelope: dict[str, Any], role: str, binding: object
) -> AcceptedContextBasis:
    if not isinstance(binding, dict):
        raise TurnContractError("phase binding is not a control object")
    basis = binding.get("context_basis")
    if (
        not isinstance(basis, AcceptedContextBasis)
        or basis._seal is not _CONTEXT_BASIS_SEAL
    ):
        raise TurnContractError("phase binding lacks an accepted Context basis")
    if (
        basis._turn_seal is not envelope.get("_turn_seal")
        or basis.turn_id != envelope.get("turn_id")
        or basis.source_frontier != envelope.get("accepted_frontier")
    ):
        raise TurnContractError("phase Context basis is not current for this turn")
    expected = {
        "role": role,
        "purpose": basis.purpose,
        "profile_id": basis.profile_id,
        "bundle_id": basis.bundle_id,
        "subject_id": basis.subject_id,
        "recipient_id": basis.recipient_id,
        "source_frontier": basis.source_frontier,
        "assembly_ordinal": basis.assembly_ordinal,
    }
    if any(binding.get(name) != value for name, value in expected.items()):
        raise TurnContractError("phase binding differs from its accepted Context basis")
    if role == "NARRATOR":
        current_resolved_response_language(envelope, binding)
    return basis


def current_phase_context_basis(
    envelope: dict[str, Any], role: str
) -> AcceptedContextBasis:
    """Return the exact current accepted Context basis for one bound phase."""
    if not isinstance(envelope, dict):
        raise TurnContractError("turn envelope must be an object")
    if role not in PHASE_RESULT_KINDS:
        raise TurnContractError("unregistered role")
    phase_bindings = envelope.get("phase_bindings")
    if not isinstance(phase_bindings, dict):
        raise TurnContractError("turn envelope phase bindings are invalid")
    return _validate_bound_context_basis(envelope, role, phase_bindings.get(role))


def accept_phase_result(
    envelope: dict[str, Any], result: dict[str, Any]
) -> dict[str, Any]:
    """Accept the minimum registered result; raw role-private material never crosses."""
    if not isinstance(result, dict):
        raise TurnContractError("result must be an object")
    if FORBIDDEN_HANDOFF_KEYS.intersection(result):
        raise TurnContractError("result contains protected private material")
    kind = result.get("kind")
    if not isinstance(kind, str):
        raise TurnContractError("result kind must be a registered result string")
    required_fields = RESULT_REQUIRED_FIELDS.get(kind)
    if required_fields is None or set(result) != required_fields:
        raise TurnContractError(
            "result does not satisfy its registered schema contract"
        )
    bindings = envelope.get("phase_bindings", {})
    matching_roles = [
        role
        for role, allowed in PHASE_RESULT_KINDS.items()
        if kind in allowed and role in bindings
    ]
    if len(matching_roles) != 1:
        raise TurnContractError(
            "result kind is not accepted by exactly one bound phase"
        )
    role = matching_roles[0]
    binding = bindings[role]
    basis = _validate_bound_context_basis(envelope, role, binding)
    if kind not in binding["allowed_results"]:
        raise TurnContractError(
            "result kind is outside the bound allowed-results scope"
        )
    if role == "NARRATOR":
        chronicler_binding = bindings.get("CHRONICLER")
        if isinstance(chronicler_binding, dict):
            chronicler_basis = _validate_bound_context_basis(
                envelope, "CHRONICLER", chronicler_binding
            )
            if basis.assembly_ordinal <= chronicler_basis.assembly_ordinal:
                raise TurnContractError(
                    "Narrator requires a fresh Context rebind after Chronicler"
                )
    if "purpose" in required_fields and result.get("purpose") != binding["purpose"]:
        raise TurnContractError("result purpose does not match phase binding")
    if role == "NARRATOR":
        response_language = current_resolved_response_language(envelope, binding)
        if result.get("response_language") != response_language:
            raise TurnContractError(
                "narration response language does not match current response language"
            )
        prose = result.get("prose")
        if isinstance(prose, str) and is_internal_narration_text(prose):
            raise TurnContractError(
                "internal role, status, or fallback token is not narration"
            )
    if result.get("bundle_id") != binding["bundle_id"]:
        raise TurnContractError("result bundle_id does not match phase binding")
    for field in ("subject_id", "recipient_id"):
        if field in required_fields and result.get(field) != binding[field]:
            raise TurnContractError(f"result {field} does not match phase binding")
    if "source_generation" in required_fields and result.get(
        "source_generation"
    ) != envelope.get("accepted_frontier"):
        raise TurnContractError(
            "result source_generation does not match accepted frontier"
        )
    accepted = dict(result)
    accepted_results = envelope.get("accepted_results")
    if not isinstance(accepted_results, dict):
        raise TurnContractError("turn envelope accepted-result registries are invalid")
    typed_result = AcceptedPhaseResult(
        _seal=_PHASE_RESULT_SEAL,
        _turn_seal=basis._turn_seal,
        kind=kind,
        role=role,
        purpose=basis.purpose,
        profile_id=basis.profile_id,
        subject_id=basis.subject_id,
        recipient_id=basis.recipient_id,
        source_frontier=basis.source_frontier,
        bundle_id=basis.bundle_id,
        turn_id=basis.turn_id,
        assembly_ordinal=basis.assembly_ordinal,
        result=accepted,
    )
    accepted_results[role] = accepted
    binding["accepted_phase_result"] = typed_result
    return accepted


def accept_execution_handoff(
    envelope: dict[str, Any], recipient_role: str, execution_result: object
) -> dict[str, Any]:
    """Project committed mechanics into one registered, recipient-scoped handoff."""
    if not isinstance(recipient_role, str) or not recipient_role:
        raise TurnContractError("recipient role must be a nonempty string")
    bindings = envelope.get("phase_bindings", {})
    if not isinstance(bindings, dict):
        raise TurnContractError("turn envelope phase bindings are invalid")
    binding = bindings.get(recipient_role)
    if not isinstance(binding, dict):
        raise TurnContractError("recipient phase is not bound")
    allowed_handoffs = binding.get("allowed_handoffs")
    if not isinstance(allowed_handoffs, list) or allowed_handoffs != [EXECUTION_HANDOFF_KIND]:
        raise TurnContractError("execution result is outside the bound handoff scope")
    handoff = _execution_handoff(execution_result)
    turn_id = _nonempty_string(envelope.get("turn_id"), "turn_id")
    purpose = _nonempty_string(binding.get("purpose"), "handoff purpose")
    bundle_id = _nonempty_string(binding.get("bundle_id"), "handoff bundle_id")
    recipient_id = _nonempty_string(binding.get("recipient_id"), "handoff recipient_id")
    typed_handoff = ExecutionHandoff(
        _seal=_HANDOFF_SEAL,
        **handoff,
        turn_id=turn_id,
        recipient_role=recipient_role,
        purpose=purpose,
        bundle_id=bundle_id,
        recipient_id=recipient_id,
    )
    accepted_handoffs = envelope.setdefault("accepted_handoffs", {})
    if not isinstance(accepted_handoffs, dict):
        raise TurnContractError("turn envelope accepted handoffs are invalid")
    prior = accepted_handoffs.setdefault(recipient_role, [])
    if not isinstance(prior, list):
        raise TurnContractError("turn envelope accepted handoffs are invalid")
    for existing in prior:
        if not isinstance(existing, ExecutionHandoff):
            raise TurnContractError("execution handoff is not owner-verified")
        if existing.accepted_command_id == typed_handoff.accepted_command_id:
            if existing != typed_handoff:
                raise TurnContractError("execution handoff conflicts with an accepted result")
            return typed_handoff.to_dict()
    prior.append(typed_handoff)
    return typed_handoff.to_dict()


def advance_phase(envelope: dict[str, Any], role: str) -> str:
    """Record that a bound phase completed without inventing durable lifecycle state."""
    if role not in envelope.get("phase_bindings", {}):
        raise TurnContractError("phase is not bound")
    return role


def reserve_auxiliary_capacity(envelope: dict[str, Any], requested: int) -> int:
    """Reserve only spare capacity; protected Narrator capacity is never spendable."""
    if isinstance(requested, bool) or not isinstance(requested, int) or requested < 0:
        raise TurnContractError("requested capacity must be a nonnegative integer")
    # This owner receives a protected reservation, not a total host envelope.
    # No separately admitted spare capacity exists at this boundary.
    return 0


def _execution_handoff(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        raise TurnContractError("execution result must be a typed object")
    if FORBIDDEN_HANDOFF_KEYS.intersection(value):
        raise TurnContractError("execution result contains protected diagnostic material")
    segment = value.get("segment")
    event = value.get("event")
    if not isinstance(segment, dict) or not isinstance(event, dict):
        raise TurnContractError("execution result is missing committed segment evidence")
    command_id = _nonempty_string(value.get("accepted_command_id"), "accepted_command_id")
    input_fingerprint = _nonempty_string(
        value.get("accepted_input_fingerprint"), "accepted_input_fingerprint"
    )
    if len(input_fingerprint) != 64 or any(char not in SHA256_HEX for char in input_fingerprint):
        raise TurnContractError("accepted_input_fingerprint must be a SHA-256 fingerprint")
    execution_owner_id = _nonempty_string(value.get("execution_owner_id"), "execution_owner_id")
    resolution_id = _nonempty_string(value.get("resolution_id"), "resolution_id")
    status = _nonempty_string(value.get("status"), "status")
    if status not in EXECUTION_STATES:
        raise TurnContractError("execution result status is not registered")
    segment_id = _nonempty_string(segment.get("segment_id"), "segment_id")
    event_id = _nonempty_string(value.get("event_id"), "event_id")
    event_ids = segment.get("event_ids")
    if not isinstance(event_ids, list) or event_id not in event_ids:
        raise TurnContractError("execution event is not committed by its segment")
    if event.get("segment_id") != segment_id or event.get("root_command_id") != command_id:
        raise TurnContractError("execution event evidence is not bound to the accepted command")
    return {
        "kind": EXECUTION_HANDOFF_KIND,
        "accepted_command_id": command_id,
        "accepted_input_fingerprint": input_fingerprint,
        "execution_owner_id": execution_owner_id,
        "resolution_id": resolution_id,
        "status": status,
        "segment_id": segment_id,
        "event_id": event_id,
    }


def select_fallback(outcome: str, registered_fallbacks: tuple[str, ...]) -> str:
    """Choose exactly one registered finite fallback for a terminal assembly outcome."""
    if outcome != "UNSATISFIABLE":
        raise TurnContractError("fallback selection requires UNSATISFIABLE")
    if not registered_fallbacks or any(item not in FALLBACKS for item in registered_fallbacks):
        raise TurnContractError("no registered finite fallback")
    return registered_fallbacks[0]
