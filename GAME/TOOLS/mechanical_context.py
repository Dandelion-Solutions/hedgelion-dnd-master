"""Source-bound compiled reads and disposable committed-view cache identity.

Exact owner acquisition is not affected-set completeness. This module neither
interprets an index miss as absence nor issues selector, casting or mutation
authority. Prospective views require the native builder's future issuance join.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from typing import Final

from . import activity_contracts as contracts
from .catalog_runtime import _thaw
from .current_owner import (
    CurrentOwnerObservation,
    CurrentOwnerReadSession,
    CurrentOwnerStatus,
    NativeOwnerRef,
)
from .policy_basis import (
    PolicyBasisResolutionError,
    is_accepted_basis_issued,
    validate_policy_applicability_witnesses,
)
from .runtime_execution import CommandAcceptanceError, validate_execution_proposal

# framework_module_version: 1.0.2
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.2"


class MechanicalContextError(ValueError):
    """A read consumer crosses its compiled binding or evidence boundary."""


def _instruction(
    compiled: contracts.CompiledActivity, consumer_id: str
) -> contracts.CompiledInstruction:
    if not contracts._compiler_value_is_issued(compiled, kind="compiled"):
        raise MechanicalContextError("read plan requires an exact compiler-issued Activity")
    pending = list(compiled.instructions)
    while pending:
        instruction = pending.pop()
        if instruction.consumer_id == consumer_id:
            return instruction
        pending.extend(instruction.children)
    raise MechanicalContextError("read plan has a foreign consumer occurrence")


def compiled_read_plan(
    compiled: contracts.CompiledActivity, consumer_id: str
) -> tuple[str, ...]:
    """Return the immutable exact instruction read plan, not a family allowlist."""
    return _instruction(compiled, consumer_id).read_contract_refs


def _roles(
    compiled: contracts.CompiledActivity,
    role_bindings: Mapping[str, NativeOwnerRef],
) -> tuple[NativeOwnerRef, ...]:
    if not isinstance(role_bindings, Mapping) or set(role_bindings) - set(compiled.role_contracts):
        raise MechanicalContextError("read plan contains a foreign native role")
    for role, specification in compiled.role_contracts.items():
        owner = role_bindings.get(role)
        if owner is None:
            if specification["required"]:
                raise MechanicalContextError("read plan is missing a required native role")
        elif type(owner) is not NativeOwnerRef or owner.family_key != specification["family_key"]:
            raise MechanicalContextError("read plan native role has the wrong owner family")
    owners = set(role_bindings.values())
    if not owners:
        raise MechanicalContextError("read plan has no exact native owner binding")
    return tuple(sorted(owners, key=lambda owner: (owner.family_key, owner.identity)))


def _accepted_command(
    compiled: contracts.CompiledActivity, command: Mapping[str, object]
) -> Mapping[str, object]:
    lineage = contracts._compiler_value_lineage(compiled, kind="compiled")
    if lineage is None:
        raise MechanicalContextError("accepted command requires compiler-issued lineage")
    try:
        value = _thaw(command)
        binding = value["candidate_binding"]
        candidate = {"definition_id": binding["definition_id"], "kind": binding["kind"]}
        validate_execution_proposal(value, lineage[0], candidate)
    except (CommandAcceptanceError, KeyError, TypeError, ValueError) as error:
        raise MechanicalContextError("accepted command does not retain its exact input basis") from error
    return value


def _resolved(
    observation: CurrentOwnerObservation,
    execution_ref: contracts.ExecutionRef,
) -> None:
    # Check the entire accumulated union. A prior semantic read cannot disappear
    # when a later consumer expands its native footprint.
    for owner in observation.key_union:
        read = observation.require(owner)
        if read.status is CurrentOwnerStatus.REVALIDATION_REQUIRED:
            raise contracts.NativePreparationHold("REVALIDATION_REQUIRED", execution_ref, ())
        if read.status is not CurrentOwnerStatus.RESOLVED or read.payload is None:
            raise contracts.NativePreparationHold("AUTHORITY_UNAVAILABLE", execution_ref, ())


def acquire_observation(
    compiled: contracts.CompiledActivity,
    *,
    consumer_id: str,
    owner_session: CurrentOwnerReadSession,
    role_bindings: Mapping[str, NativeOwnerRef],
    accepted_command: Mapping[str, object],
) -> CurrentOwnerObservation:
    """Adapt finite compiled owner bindings to P0's accumulated-union reader.

    Domain/infrastructure reads without exact native role mapping cannot be
    reconstructed from indexes or ambient state. They remain affected-consumer
    holds until the owning builder supplies their declared source closure.
    """
    instruction = _instruction(compiled, consumer_id)
    owners = _roles(compiled, role_bindings)
    command = _accepted_command(compiled, accepted_command)
    request = command["action_request"]
    if request["activity_id"] != compiled.activity_id:
        raise MechanicalContextError("root acquisition Activity differs from accepted command")
    actor = role_bindings.get("actor")
    if actor is not None and actor.identity != (request["actor_id"],):
        raise MechanicalContextError("root Actor read binding differs from accepted command")
    if not isinstance(owner_session, CurrentOwnerReadSession):
        raise MechanicalContextError("read plan requires a native owner session")
    execution_ref = contracts.ExecutionRef(command["command_id"], command["root_resolution_id"])
    for reference in instruction.read_contract_refs:
        kind, _, identity = reference.partition(":")
        if kind == "domain_owner" and identity not in {
            "definition", "effect_definition", "zone_definition",
            *(owner.family_key for owner in owners),
        }:
            raise contracts.NativePreparationHold("AUTHORITY_UNAVAILABLE", execution_ref, ())
        if kind == "infrastructure":
            raise contracts.NativePreparationHold("AUTHORITY_UNAVAILABLE", execution_ref, ())
    return_observation = owner_session.require(owners)
    _resolved(return_observation, execution_ref)
    return return_observation


def _value_identity(value: object) -> object:
    """Exact immutable equality value, not a new serialized digest namespace."""
    if isinstance(value, Mapping):
        return tuple((key, _value_identity(value[key])) for key in sorted(value))
    if isinstance(value, (list, tuple)):
        return tuple(_value_identity(item) for item in value)
    return (type(value).__name__, value)


def context_cache_identity(context: contracts.NativePreparationContext) -> tuple[object, ...]:
    """Revalidate and derive the complete identity of this committed read view.

    No result/cache survives this check by authority. After child expansion or
    suspension the builder must reacquire and issue a fresh preparation context.
    Full accepted input/Resolution values are equality inputs, retaining exact
    facts (including false), fixed rolls and causal bindings without hashing
    them into another independently persisted fingerprint.
    """
    if type(context) is not contracts.NativePreparationContext:
        raise MechanicalContextError("cache identity requires a typed preparation context")
    # Re-run the closed validation on a detached wrapper, without mutating the
    # caller's frozen containers while deriving this disposable equality value.
    context = replace(context)
    _instruction(context.compiled, context.consumer_id)
    _roles(context.compiled, context.role_bindings)
    command = _accepted_command(context.compiled, context.accepted_command)
    if context.execution_ref.resolution_id == command["root_resolution_id"]:
        request = command["action_request"]
        if request["activity_id"] != context.compiled.activity_id:
            raise MechanicalContextError("root acquisition Activity differs from accepted command")
        actor = context.role_bindings.get("actor")
        if actor is not None and actor.identity != (request["actor_id"],):
            raise MechanicalContextError("root Actor read binding differs from accepted command")
    adjudication = []
    for basis in context.accepted_adjudication:
        if not is_accepted_basis_issued(basis):
            raise MechanicalContextError("adjudication cache input is not issuer-bound")
        try:
            validate_policy_applicability_witnesses(basis.verified_policies,
                context.accepted_command["action_request"]["activity_id"], context.catalog.catalog_context)
        except PolicyBasisResolutionError as error:
            raise MechanicalContextError("adjudication cache input is not applicable") from error
        adjudication.append((_value_identity(basis.parameter_bindings),
                             _value_identity(basis.invocation_facts),
                             tuple(policy.policy_ref for policy in basis.verified_policies)))
    if context.prospective_owner_documents:
        raise MechanicalContextError("prospective documents require same-builder native issuance")
    if tuple(sorted(set(context.policy_refs))) != context.policy_refs:
        raise MechanicalContextError("material policy references must be canonical sorted unique values")
    if not context.owner_session.revalidate(context.observation):
        raise contracts.NativePreparationHold("REVALIDATION_REQUIRED", context.execution_ref, ())
    _resolved(context.observation, context.execution_ref)
    compiled = context.compiled
    native_basis = tuple(
        (owner.family_key, owner.identity, read.status.value, read.source.value,
         read.source_basis, read.generation, read.fingerprint, read.predecessor_fingerprint)
        for owner in context.observation.key_union
        for read in (context.observation.require(owner),)
    )
    return (
        compiled.ruleset_set_digest_generation, compiled.ruleset_set_sha256,
        compiled.catalog_context_fingerprint_generation, compiled.catalog_context_fingerprint,
        compiled.activity_id, compiled.definition_semantic_hash_generation,
        compiled.definition_semantic_hash, compiled.compiler_generation,
        compiled.engine_contract_inventory_sha256, compiled.mode_policy_profile_id,
        context.consumer_id, context.occurrence_id,
        context.execution_ref.command_id, context.execution_ref.resolution_id,
        tuple((role, owner.family_key, owner.identity) for role, owner in sorted(context.role_bindings.items())),
        native_basis, _value_identity(context.accepted_command), _value_identity(context.resolution),
        context.accepted_fact_refs, context.policy_refs,
        tuple((reference.execution_ref.command_id, reference.execution_ref.resolution_id,
               reference.request_id, reference.occurrence_id, reference.generation)
              for reference in context.fixed_roll_refs),
        tuple(adjudication),
    )
