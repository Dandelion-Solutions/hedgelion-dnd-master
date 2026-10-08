"""Source-bound compiled reads and disposable committed-view cache identity.

Exact owner acquisition is not affected-set completeness. This module neither
interprets an index miss as absence nor issues selector, casting or mutation
authority. Prospective views require the native builder's future issuance join.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import replace
from types import MappingProxyType
from typing import Final

from . import activity_contracts as contracts
from . import structural_contracts
from .catalog_runtime import _thaw
from .current_owner import (
    CurrentOwnerObservation,
    CurrentOwnerReadSession,
    CurrentOwnerStatus,
    NativeOwnerRef,
)
from .hot_store import OwnerDocument
from .policy_basis import (
    PolicyBasisResolutionError,
    is_accepted_basis_issued,
    validate_policy_applicability_witnesses,
)
from .runtime_execution import CommandAcceptanceError, validate_execution_proposal

# framework_module_version: 1.0.4
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.4"
_DAMAGE_CONTRIBUTION_TYPES: Final[Mapping[str, str]] = MappingProxyType(
    {
        "rule.add_flat": "ADJUSTMENT",
        "rule.resistance": "RESISTANCE",
        "rule.vulnerability": "VULNERABILITY",
        "rule.immunity": "IMMUNITY",
    }
)


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
    if not contracts._preparation_context_is_issued(context):
        raise MechanicalContextError(
            "cache identity requires an authentic source-bound preparation context"
        )
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


def _selector_context(
    compiled: contracts.CompiledActivity,
    consumer_id: str,
    observation: CurrentOwnerObservation,
    role_bindings: Mapping[str, NativeOwnerRef],
    accepted_command: Mapping[str, object],
    prospective_documents: tuple[OwnerDocument, ...],
) -> contracts.NativePreparationContext:
    if prospective_documents:
        raise MechanicalContextError(
            "prospective documents require same-builder native issuance"
        )
    contexts = contracts._preparation_contexts_for_observation(observation)
    matches = tuple(
        context
        for context in contexts
        if context.compiled is compiled
        and context.consumer_id == consumer_id
        and context.role_bindings is role_bindings
        and context.accepted_command is accepted_command
        and context.prospective_owner_documents is prospective_documents
    )
    if len(matches) != 1:
        raise MechanicalContextError(
            "selector inputs are not joined to one exact native preparation context"
        )
    context = matches[0]
    if not contracts._preparation_context_is_issued(context):
        raise MechanicalContextError(
            "selector evaluation requires an authentic source-bound preparation context"
        )
    if context.prospective_owner_documents:
        raise MechanicalContextError(
            "prospective documents require same-builder native issuance"
        )
    return context


def _policy_for_selector(
    compiled: contracts.CompiledActivity, consumer_id: str, selector_id: str
) -> contracts.CompiledCalculationPolicy:
    if not contracts._compiler_value_is_issued(compiled, kind="compiled"):
        raise MechanicalContextError(
            "selector evaluation requires an exact compiler-issued Activity"
        )
    instruction = _instruction(compiled, consumer_id)
    candidates = tuple(
        policy
        for policy in compiled.calculation_policy_bindings
        if policy.binding.consumer_id == consumer_id
        and any(
            pair.selector_id == selector_id
            for pair in policy.binding.selector_operation_pairs
        )
    )
    if len(candidates) != 1:
        raise MechanicalContextError(
            "selector is not one exact paired root of the compiled consumer policy"
        )
    policy = candidates[0]
    selector_ref = f"selector:{selector_id}"
    required_reads = set(policy.binding.reads) | set(policy.dependency_read_refs)
    if (
        selector_ref not in policy.binding.reads
        or not required_reads <= set(instruction.read_contract_refs)
    ):
        raise MechanicalContextError(
            "selector policy closure is not retained by the exact compiled consumer read plan"
        )
    pair = next(
        pair
        for pair in policy.binding.selector_operation_pairs
        if pair.selector_id == selector_id
    )
    selector = policy.selector_contracts.get(selector_id)
    if not isinstance(selector, Mapping):
        raise MechanicalContextError("compiled selector metadata is unavailable")
    allowed = selector.get("allowed_operations")
    operation_contracts = selector.get("operation_contracts")
    if (
        not isinstance(allowed, (list, tuple))
        or not isinstance(operation_contracts, Mapping)
        or set(operation_contracts) != set(allowed)
        or not pair.operation_ids
        or len(pair.operation_ids) != len(set(pair.operation_ids))
        or not set(pair.operation_ids) <= set(allowed)
    ):
        raise MechanicalContextError("compiled selector-operation pair is incomplete")
    if (
        selector.get("calculation_policy_id") != policy.binding.profile_id
        or selector.get("calculation_policy_generation")
        != policy.binding.profile_generation
    ):
        raise MechanicalContextError("compiled selector has a foreign calculation policy")
    return policy


def _compiled_policy_graph(
    compiled: contracts.CompiledActivity,
    policy: contracts.CompiledCalculationPolicy,
) -> tuple[
    dict[str, tuple[str, ...]],
    dict[tuple[str, str], frozenset[str]],
    dict[tuple[str, str], tuple[str, ...]],
]:
    binding = policy.binding
    selector_contracts = policy.selector_contracts
    accessor_contracts = policy.accessor_contracts
    derived_contracts = policy.derived_node_contracts
    fact_contracts = policy.context_fact_contracts
    fact_edges: dict[str, set[str]] = {}
    all_fact_edges: set[tuple[str, str]] = set()
    for fact_binding in binding.context_fact_bindings:
        for fact_id in fact_binding.fact_ids:
            edge = (fact_binding.consumer_ref, fact_id)
            if edge in all_fact_edges:
                raise MechanicalContextError("compiled fact consumer edge is duplicated")
            all_fact_edges.add(edge)
            fact_edges.setdefault(fact_binding.consumer_ref, set()).add(fact_id)

    declared_fact_ids = {
        reference.partition(":")[2]
        for reference in binding.reads
        if reference.startswith("fact:")
    }
    bound_fact_ids = {fact_id for _consumer_ref, fact_id in all_fact_edges}
    if declared_fact_ids != bound_fact_ids or set(fact_contracts) != declared_fact_ids:
        raise MechanicalContextError(
            "compiled policy facts differ from their exact consumer bindings"
        )

    roots = tuple(
        reference
        for reference in binding.reads
        if reference.startswith(("selector:", "accessor:"))
    )
    if len(roots) != len(set(roots)):
        raise MechanicalContextError("compiled policy repeats an exact mechanical root")
    paired_selector_ids = {
        pair.selector_id for pair in binding.selector_operation_pairs
    }
    direct_selector_ids = {
        reference.partition(":")[2]
        for reference in roots
        if reference.startswith("selector:")
    }
    if direct_selector_ids != paired_selector_ids:
        raise MechanicalContextError(
            "compiled selector roots differ from their exact operation pairs"
        )

    graph: dict[str, tuple[str, ...]] = {}
    node_facts: dict[tuple[str, str], frozenset[str]] = {}
    node_roles: dict[tuple[str, str], tuple[str, ...]] = {}
    visiting: set[tuple[str, str]] = set()
    visited: set[tuple[str, str]] = set()

    def visit(
        node_ref: str,
        parent_ref: str | None,
        root_roles: tuple[str, ...],
        root_ref: str,
    ) -> frozenset[str]:
        instance = (root_ref, node_ref)
        if instance in visiting:
            raise MechanicalContextError(f"mechanical dependency cycle at {node_ref}")
        if instance in visited:
            return node_facts[instance]
        kind, separator, node_id = node_ref.partition(":")
        if not separator or kind not in {"selector", "accessor", "derived"}:
            raise MechanicalContextError(f"unproven mechanical dependency: {node_ref}")
        if kind == "selector":
            metadata = selector_contracts.get(node_id)
            if not isinstance(metadata, Mapping):
                raise MechanicalContextError(f"compiled selector dependency is missing: {node_ref}")
            dependency_refs = metadata.get("static_dependencies", ())
            allowed_kinds = set(metadata.get("allowed_dependency_kinds", ()))
            allowed_facts = set(metadata.get("permitted_context_fact_ids", ()))
            allowed_classes = set(metadata.get("allowed_input_classes", ()))
            allowed_operations = metadata.get("allowed_operations")
            operation_contracts = metadata.get("operation_contracts")
            if (
                not isinstance(allowed_operations, (list, tuple))
                or not isinstance(operation_contracts, Mapping)
                or set(operation_contracts) != set(allowed_operations)
            ):
                raise MechanicalContextError(f"compiled selector pairs are incomplete: {node_ref}")
        elif kind == "accessor":
            metadata = accessor_contracts.get(node_id)
            if not isinstance(metadata, Mapping):
                raise MechanicalContextError(f"compiled accessor dependency is missing: {node_ref}")
            dependency_refs = metadata.get("dependencies", ())
            allowed_kinds = {"selector", "accessor", "derived"}
            allowed_facts = set()
            allowed_classes = {metadata.get("input_class")}
        else:
            metadata = derived_contracts.get(node_id)
            if not isinstance(metadata, Mapping):
                raise MechanicalContextError(f"compiled derived dependency is missing: {node_ref}")
            dependency_refs = metadata.get("dependencies", ())
            allowed_kinds = set(metadata.get("allowed_dependency_kinds", ()))
            allowed_facts = set(metadata.get("permitted_context_fact_ids", ()))
            allowed_classes = set(metadata.get("allowed_input_classes", ()))

        if not isinstance(dependency_refs, (list, tuple)):
            raise MechanicalContextError(f"mechanical dependency list is malformed: {node_ref}")
        subject_kinds = metadata.get("subject_kinds")
        if kind in {"selector", "accessor"} and subject_kinds:
            role_families = {
                policy.role_contracts[role_name]["family_key"]
                for role_name in root_roles
            }
            if not role_families <= set(subject_kinds):
                raise MechanicalContextError(f"subject binding is incompatible at {node_ref}")
        if parent_ref is None and kind == "accessor":
            permissions = metadata.get("permitted_consumer_ids", ())
            if f"activity:{compiled.activity_id}" not in permissions:
                raise MechanicalContextError(f"unauthorized accessor root: {node_ref}")
        if parent_ref is not None and kind in {"accessor", "derived"}:
            permissions = metadata.get("permitted_consumer_ids", ())
            if parent_ref not in permissions:
                raise MechanicalContextError(
                    f"unauthorized mechanical edge: {parent_ref} -> {node_ref}"
                )

        direct_facts = frozenset(fact_edges.get(node_ref, set()))
        reached_facts = set(direct_facts)
        reached_classes = {"ENGINE_STATE"}
        for fact_id in direct_facts:
            fact_metadata = fact_contracts.get(fact_id)
            if (
                not isinstance(fact_metadata, Mapping)
                or fact_metadata.get("disposition") != "ACTIVE_ADMITTED"
                or compiled.activity_id not in fact_metadata.get("permitted_consumer_ids", ())
            ):
                raise MechanicalContextError(f"compiled fact is unauthorized: {fact_id}")
            reached_classes.add(str(fact_metadata.get("source_class")))

        visiting.add(instance)
        normalized_dependencies: list[str] = []
        for raw_dependency in dependency_refs:
            if not isinstance(raw_dependency, str):
                raise MechanicalContextError(f"mechanical dependency is malformed at {node_ref}")
            dependency_kind, separator, _dependency_id = raw_dependency.partition(":")
            if not separator or dependency_kind not in allowed_kinds:
                raise MechanicalContextError(
                    f"illegal mechanical dependency kind from {node_ref}: {raw_dependency}"
                )
            dependency_metadata = {
                "selector": selector_contracts,
                "accessor": accessor_contracts,
                "derived": derived_contracts,
            }[dependency_kind].get(_dependency_id)
            if not isinstance(dependency_metadata, Mapping):
                raise MechanicalContextError(f"unproven mechanical dependency: {raw_dependency}")
            child_facts = visit(raw_dependency, node_ref, root_roles, root_ref)
            reached_facts.update(child_facts)
            normalized_dependencies.append(raw_dependency)
        visiting.remove(instance)

        if not reached_facts <= allowed_facts:
            raise MechanicalContextError(
                f"transitive fact permission exceeds exact allowlist at {node_ref}"
            )
        if not reached_classes <= allowed_classes:
            raise MechanicalContextError(
                f"transitive input class exceeds exact allowlist at {node_ref}"
            )
        graph[node_ref] = tuple(normalized_dependencies)
        node_facts[instance] = frozenset(reached_facts)
        node_roles[instance] = root_roles
        visited.add(instance)
        return node_facts[instance]

    role_bindings_by_root = {
        item.read_ref: item.role_names for item in binding.native_role_bindings
    }
    if set(role_bindings_by_root) != set(roots):
        raise MechanicalContextError("compiled policy native roles differ from exact read roots")
    for root_ref in roots:
        role_names = role_bindings_by_root[root_ref]
        for role_name in role_names:
            role = policy.role_contracts.get(role_name)
            if not isinstance(role, Mapping):
                raise MechanicalContextError(f"compiled policy role is missing: {role_name}")
        visit(root_ref, None, role_names, root_ref)

    direct_roots = set(roots)
    expected_dependencies = tuple(sorted(set(graph) - direct_roots))
    if expected_dependencies != policy.dependency_read_refs:
        raise MechanicalContextError(
            "compiled mechanical dependency closure differs from its retained read plan"
        )

    for fact_binding in binding.context_fact_bindings:
        if fact_binding.consumer_ref not in graph:
            raise MechanicalContextError(
                f"compiled fact edge has no mechanical node: {fact_binding.consumer_ref}"
            )
        if not any(
            set(fact_binding.fact_ids) <= node_facts[(root_ref, fact_binding.consumer_ref)]
            for root_ref in roots
            if (root_ref, fact_binding.consumer_ref) in node_facts
        ):
            raise MechanicalContextError(
                f"compiled fact edge is outside its exact transitive closure: {fact_binding.consumer_ref}"
            )
    return graph, node_facts, node_roles


def _accepted_fact_inputs(
    context: contracts.NativePreparationContext,
    policy: contracts.CompiledCalculationPolicy,
    required_fact_ids: frozenset[str],
) -> dict[str, Mapping[str, object]]:
    command_value = _thaw(context.accepted_command.get("invocation_facts", ()))
    if not isinstance(command_value, list):
        raise MechanicalContextError("accepted invocation facts are not a finite list")
    basis_facts = [
        _thaw(fact)
        for basis in context.accepted_adjudication
        for fact in basis.invocation_facts
    ]
    if _value_identity(command_value) != _value_identity(basis_facts):
        raise MechanicalContextError(
            "accepted invocation facts differ from their issuer-bound adjudication basis"
        )
    supplied_ids = tuple(
        sorted(str(fact.get("fact_id")) for fact in command_value if isinstance(fact, Mapping))
    )
    if tuple(sorted(set(context.accepted_fact_refs))) != tuple(sorted(set(supplied_ids))):
        raise MechanicalContextError("accepted fact refs differ from retained fact inputs")

    by_id: dict[str, Mapping[str, object]] = {}
    root_activity_id = context.accepted_command["action_request"]["activity_id"]
    for fact_id in required_fact_ids:
        matches = [
            fact
            for fact in command_value
            if isinstance(fact, Mapping) and fact.get("fact_id") == fact_id
        ]
        if not matches:
            raise MechanicalContextError(f"missing accepted invocation fact: {fact_id}")
        if len(matches) != 1:
            raise MechanicalContextError(f"duplicate accepted invocation fact: {fact_id}")
        fact = matches[0]
        if (
            type(fact.get("value")) is not bool
            or fact.get("provenance_class") != "INVOCATION_ADJUDICATED"
            or fact.get("consumer_id") != root_activity_id
            or fact.get("rules_context_fingerprint")
            != context.compiled.catalog_context_fingerprint
        ):
            raise MechanicalContextError(f"accepted invocation fact is stale or malformed: {fact_id}")
        refs = fact.get("policy_basis_refs")
        if (
            not isinstance(refs, (list, tuple))
            or tuple(refs) != tuple(sorted(set(refs)))
        ):
            raise MechanicalContextError(f"accepted fact policy refs are not canonical: {fact_id}")
        metadata = policy.context_fact_contracts.get(fact_id)
        if not isinstance(metadata, Mapping) or metadata.get("value_type") != "boolean":
            raise MechanicalContextError(f"compiled fact type is unavailable: {fact_id}")
        by_id[fact_id] = fact
    return by_id


def _owner_payload(
    observation: CurrentOwnerObservation,
    owner_ref: NativeOwnerRef,
    execution_ref: contracts.ExecutionRef,
) -> tuple[Mapping[str, object], object]:
    try:
        read = observation.require(owner_ref)
    except (AttributeError, KeyError, TypeError, ValueError) as error:
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", execution_ref, ()
        ) from error
    if read.status is CurrentOwnerStatus.REVALIDATION_REQUIRED:
        raise contracts.NativePreparationHold("REVALIDATION_REQUIRED", execution_ref, ())
    if read.status is not CurrentOwnerStatus.RESOLVED:
        raise contracts.NativePreparationHold("AUTHORITY_UNAVAILABLE", execution_ref, ())
    payload = read.payload
    if payload is None:
        raise contracts.NativePreparationHold("AUTHORITY_UNAVAILABLE", execution_ref, ())
    return payload, read


def _role_owner(
    context: contracts.NativePreparationContext,
    role_names: tuple[str, ...],
    allowed_families: Sequence[object],
) -> NativeOwnerRef:
    allowed = set(allowed_families)
    candidates = [
        context.role_bindings[role_name]
        for role_name in role_names
        if role_name in context.role_bindings
        and context.role_bindings[role_name].family_key in allowed
    ]
    if len(candidates) != 1:
        raise MechanicalContextError("selector dependency has no exact subject owner binding")
    return candidates[0]


def _owner_ref_wire(owner_ref: NativeOwnerRef) -> dict[str, object]:
    return {"family_key": owner_ref.family_key, "identity": list(owner_ref.identity)}


def _membership_effect_wire(item: object) -> dict[str, object]:
    return {
        "owner_ref": _owner_ref_wire(item.owner_ref),
        "target_id": item.target_id,
        "lifecycle": item.lifecycle,
        "source_id": item.source_id,
        "rules_origin_id": item.rules_origin_id,
        "support_effect_id": item.support_effect_id,
        "source_basis": item.source_basis,
        "fingerprint": item.fingerprint,
        "is_target_local": item.is_target_local,
    }


def _membership_wire(membership: object) -> dict[str, object]:
    def asset_wire(item: object) -> dict[str, object]:
        return {
            "owner_ref": _owner_ref_wire(item.owner_ref),
            "placement_owner_id": item.placement_owner_id,
            "container_path": list(item.container_path),
            "equipment_mode": item.equipment_mode,
            "accessible": item.accessible,
            "blocker_asset_id": item.blocker_asset_id,
            "attuned_actor_id": item.attuned_actor_id,
            "conversion_mode": item.conversion_mode,
            "source_basis": item.source_basis,
            "fingerprint": item.fingerprint,
        }

    return {
        "source_revision": membership.source_revision,
        "source_tree_sha": membership.source_tree_sha,
        "effect_ids": [item.owner_ref.identity[0] for item in membership.effects],
        "effect_dependencies": [
            _membership_effect_wire(item) for item in membership.effect_dependencies
        ],
        "effects": [_membership_effect_wire(item) for item in membership.effects],
        "excluded_effect_ids": [item.owner_ref.identity[0] for item in membership.exclusions],
        "exclusions": [
            {
                "owner_ref": _owner_ref_wire(item.owner_ref),
                "target_id": item.target_id,
                "reason": item.reason,
                "source_basis": item.source_basis,
                "fingerprint": item.fingerprint,
            }
            for item in membership.exclusions
        ],
        "asset_ids": [item.owner_ref.identity[0] for item in membership.assets],
        "assets": [asset_wire(item) for item in membership.assets],
        "family_coverage": [
            {
                "family_key": item.family_key,
                "root_path": item.root_path,
                "subtree_id": item.subtree_id,
                "absence_parent_id": item.absence_parent_id,
                "absent_child": item.absent_child,
                "files": [list(row) for row in item.files],
            }
            for item in membership.family_coverage
        ],
        "owner_reads": [
            {
                "owner_ref": _owner_ref_wire(owner),
                "status": observation.require(owner).status.value,
                "source": observation.require(owner).source.value,
                "source_basis": observation.require(owner).source_basis,
                "generation": observation.require(owner).generation,
                "fingerprint": observation.require(owner).fingerprint,
            }
            for owner in membership.p0_observation.key_union
            for observation in (membership.p0_observation,)
        ],
    }


def _closed_operation_value(
    operation_id: str, operation: Mapping[str, object], value: object
) -> object:
    """Validate only value forms closed by the retained pair metadata.

    Complex selected-profile payloads have no additional value schema in this
    slice. They fail closed instead of becoming an arbitrary contribution bag.
    """
    value_kind = operation.get("value_kind")
    constraints = operation.get("constraints", ())
    if not isinstance(constraints, (list, tuple)):
        raise MechanicalContextError(f"operation constraints are malformed: {operation_id}")
    if value_kind == "numeric_scalar" or (
        value_kind == "roll_modifier" and "finite_integer" in constraints
    ):
        if type(value) is not int:
            raise MechanicalContextError(
                f"operation value is not a finite integer: {operation_id}"
            )
        return value
    if value_kind == "boolean_constant" or (
        value_kind == "roll_modifier" and "literal_true" in constraints
    ):
        fixed_value = operation.get("fixed_value", True)
        if type(value) is not bool or value is not fixed_value:
            raise MechanicalContextError(
                f"operation value differs from its fixed boolean contract: {operation_id}"
            )
        return value
    if value_kind == "damage_defense":
        contribution_type = _DAMAGE_CONTRIBUTION_TYPES.get(operation_id)
        if (
            contribution_type is None
            or operation.get("damage_contribution_type") != contribution_type
            or operation.get("normalization") != "SOURCE_DEFINED_ORDER"
            or operation.get("calculation_policy_id")
            != "calculation.damage_defense_srd521"
            or operation.get("calculation_policy_generation") != 1
            or frozenset(constraints)
            != frozenset({"damage_type_origin_bypass_order_and_rounding"})
        ):
            raise MechanicalContextError(
                f"damage operation contract is not exact: {operation_id}"
            )
        contract_name = (
            "damage_defense_adjustment"
            if contribution_type == "ADJUSTMENT"
            else "damage_defense_match"
        )
        try:
            structural_contracts.validate_contract(contract_name, value)
        except structural_contracts.StructuralContractError as error:
            raise MechanicalContextError(
                f"damage Rule Element value is not closed for {operation_id}"
            ) from error
        return value
    if value_kind in {"roll_modifier", "damage_defense", "armor_class_base", "capability_change"}:
        raise MechanicalContextError(
            f"operation value shape is not closed by the current finite schema: {operation_id}"
        )
    raise MechanicalContextError(f"operation value kind is not admitted: {operation_id}")


def _rule_element_sources_for_roles(
    context: contracts.NativePreparationContext,
    membership: object,
    role_names: tuple[str, ...],
) -> tuple[tuple[object, ...], tuple[object, ...], frozenset[str]]:
    """Project complete membership onto this compiled node's exact subjects."""
    if not role_names or len(role_names) != len(set(role_names)):
        raise MechanicalContextError("selector has no canonical native subject roles")

    actor_ids: set[str] = set()
    asset_refs: set[NativeOwnerRef] = set()
    asset_ids: set[str] = set()
    for role_name in role_names:
        owner_ref = context.role_bindings.get(role_name)
        if type(owner_ref) is not NativeOwnerRef or len(owner_ref.identity) != 1:
            raise MechanicalContextError(
                f"selector subject role has no exact owner binding: {role_name}"
            )
        if owner_ref.family_key == "world.actor":
            actor_ids.add(owner_ref.identity[0])
        elif owner_ref.family_key == "world.asset":
            asset_refs.add(owner_ref)
            asset_ids.add(owner_ref.identity[0])
        else:
            raise MechanicalContextError(
                f"selector subject role has an unsupported owner family: {role_name}"
            )
    if actor_ids & asset_ids:
        raise MechanicalContextError(
            "selector subject IDs are ambiguous across owner families"
        )

    subject_ids = frozenset(actor_ids | asset_ids)
    effects: list[object] = []
    for item in membership.effects:
        if item.target_id not in subject_ids:
            continue
        if not item.is_target_local:
            raise MechanicalContextError(
                "selector Effect source is not bound as a target-local application"
            )
        effects.append(item)

    assets = tuple(
        item
        for item in membership.assets
        if item.owner_ref in asset_refs or item.placement_owner_id in actor_ids
    )
    return tuple(effects), assets, subject_ids


def _support_effect_dependencies(
    membership: object, subject_effects: tuple[object, ...]
) -> tuple[object, ...]:
    """Retain only support ancestors required by this subject's Effects."""
    subject_effect_ids = {item.owner_ref.identity[0] for item in subject_effects}
    dependencies = {
        item.owner_ref.identity[0]: item for item in membership.effect_dependencies
    }
    pending = [item.support_effect_id for item in subject_effects]
    retained: dict[str, object] = {}
    while pending:
        effect_id = pending.pop()
        if effect_id is None or effect_id in subject_effect_ids or effect_id in retained:
            continue
        item = dependencies.get(effect_id)
        if item is None:
            raise MechanicalContextError(
                "selector Effect support ancestor is absent from complete membership"
            )
        retained[effect_id] = item
        pending.append(item.support_effect_id)
    return tuple(retained[key] for key in sorted(retained))


def _raw_rule_elements(
    context: contracts.NativePreparationContext,
    membership: object,
    policy: contracts.CompiledCalculationPolicy,
    selector_id: str,
    metadata: Mapping[str, object],
    operation_ids: tuple[str, ...],
    facts: Mapping[str, Mapping[str, object]],
    fact_edges_by_consumer: Mapping[str, frozenset[str]],
    root_role_names: tuple[str, ...],
    evaluate_node: object,
) -> list[dict[str, object]]:
    allowed_operations = set(operation_ids)
    operation_contracts = metadata.get("operation_contracts")
    if not isinstance(operation_contracts, Mapping):
        raise MechanicalContextError(f"selector operation contracts are unavailable: {selector_id}")

    def read_definition(owner_ref: NativeOwnerRef, kind: str) -> tuple[Mapping[str, object], Mapping[str, object]]:
        read = membership.p0_observation.require(owner_ref)
        payload = read.payload
        if not isinstance(payload, Mapping):
            raise contracts.NativePreparationHold("AUTHORITY_UNAVAILABLE", context.execution_ref, ())
        definition_id = payload.get("definition_id")
        definition = context.catalog.frozen_definitions.get(definition_id)
        if not isinstance(definition, Mapping) or definition.get("kind") != kind:
            raise MechanicalContextError(
                f"native member definition is outside the exact compiled closure: {definition_id}"
            )
        data = definition.get("data")
        if not isinstance(data, Mapping):
            raise MechanicalContextError(f"native member definition data is malformed: {definition_id}")
        return payload, definition

    subject_effects, subject_assets, _subject_ids = _rule_element_sources_for_roles(
        context, membership, root_role_names
    )
    sources: list[tuple[NativeOwnerRef, str]] = [
        (item.owner_ref, "definition.effect") for item in subject_effects
    ] + [(item.owner_ref, "definition.asset") for item in subject_assets]
    contributions: list[dict[str, object]] = []
    for owner_ref, definition_kind in sources:
        payload, definition = read_definition(owner_ref, definition_kind)
        data = definition["data"]
        raw_elements = data.get("rule_elements", ())
        if not isinstance(raw_elements, (list, tuple)):
            raise MechanicalContextError("bound Rule Element collection is malformed")
        for ordinal, raw_element in enumerate(raw_elements):
            if not isinstance(raw_element, Mapping):
                raise MechanicalContextError("bound Rule Element is not a closed object")
            if raw_element.get("selector") != selector_id:
                continue
            operation_id = raw_element.get("operation_id")
            if not isinstance(operation_id, str) or operation_id not in allowed_operations:
                raise MechanicalContextError(
                    f"bound Rule Element uses an unpaired operation for {selector_id}"
                )
            operation = operation_contracts.get(operation_id)
            if not isinstance(operation, Mapping):
                raise MechanicalContextError("bound Rule Element pair contract is unavailable")
            value = _closed_operation_value(
                operation_id, operation, raw_element.get("value")
            )
            predicate = raw_element.get("predicate")
            predicate_result = True
            if predicate is not None:
                if not isinstance(evaluate_node, Mapping):
                    raise MechanicalContextError("selector predicate evaluator is unavailable")
                predicate_result = _evaluate_predicate(
                    predicate,
                    context,
                    membership.p0_observation,
                    facts,
                    policy,
                    fact_edges_by_consumer,
                    root_role_names,
                    evaluate_node,
                    f"selector:{selector_id}",
                )
            contributions.append(
                {
                    "owner_ref": _owner_ref_wire(owner_ref),
                    "owner_definition_id": definition["id"],
                    "owner_kind": definition_kind,
                    "owner_application_id": payload["id"],
                    "rule_element_ordinal": ordinal,
                    "operation_id": operation_id,
                    "value_kind": operation.get("value_kind"),
                    "operation_contract": _thaw(operation),
                    "value": _thaw(value),
                    "rule_element": _thaw(raw_element),
                    "predicate": _thaw(predicate) if predicate is not None else None,
                    "predicate_result": predicate_result,
                    "predicate_state": "TRUE" if predicate_result else "FALSE",
                }
            )
    return contributions


def _evaluate_predicate(
    predicate: object,
    context: contracts.NativePreparationContext,
    observation: CurrentOwnerObservation,
    facts: Mapping[str, Mapping[str, object]],
    policy: contracts.CompiledCalculationPolicy,
    fact_edges_by_consumer: Mapping[str, frozenset[str]],
    root_role_names: tuple[str, ...],
    evaluate_node: object,
    consumer_ref: str,
) -> bool:
    if not isinstance(predicate, Mapping):
        raise MechanicalContextError("bound mechanical predicate is malformed")
    if set(predicate) == {"fact"}:
        fact_id = predicate["fact"]
        if not isinstance(fact_id, str) or fact_id not in fact_edges_by_consumer.get(
            consumer_ref, frozenset()
        ):
            raise MechanicalContextError(
                f"predicate fact is not bound to exact consumer {consumer_ref}"
            )
        fact = facts.get(fact_id) if isinstance(fact_id, str) else None
        if fact is None:
            raise MechanicalContextError(f"missing or unauthorized predicate fact: {fact_id}")
        return fact["value"]
    if set(predicate) == {"all"} or set(predicate) == {"any"}:
        key = "all" if "all" in predicate else "any"
        children = predicate[key]
        if not isinstance(children, (list, tuple)) or not children:
            raise MechanicalContextError("bound predicate children are malformed")
        values = [
            _evaluate_predicate(
                child,
                context,
                observation,
                facts,
                policy,
                fact_edges_by_consumer,
                root_role_names,
                evaluate_node,
                consumer_ref,
            )
            for child in children
        ]
        return all(values) if key == "all" else any(values)
    if set(predicate) == {"not"}:
        return not _evaluate_predicate(
            predicate["not"],
            context,
            observation,
            facts,
            policy,
            fact_edges_by_consumer,
            root_role_names,
            evaluate_node,
            consumer_ref,
        )
    if set(predicate) != {"compare"} or not isinstance(predicate["compare"], Mapping):
        raise MechanicalContextError("bound predicate discriminator is unknown")
    comparison = predicate["compare"]
    if set(comparison) != {"left", "operator", "right"}:
        raise MechanicalContextError("bound comparison has unexpected fields")

    def operand_value(operand: object) -> object:
        if isinstance(operand, Mapping):
            accessor_id = operand.get("accessor_id")
            if not isinstance(accessor_id, str) or set(operand) - {
                "accessor_id", "subject", "condition_id", "resource_id", "parameter_id"
            }:
                raise MechanicalContextError("bound accessor operand is not a closed registered reference")
            subject_role = operand.get("subject")
            if subject_role is not None and subject_role not in root_role_names:
                raise MechanicalContextError(
                    f"predicate subject is not bound to exact consumer {consumer_ref}"
                )
            node_ref = f"accessor:{accessor_id}"
            accessor = policy.accessor_contracts.get(accessor_id)
            if (
                not isinstance(accessor, Mapping)
                or consumer_ref not in accessor.get("permitted_consumer_ids", ())
            ):
                raise MechanicalContextError(
                    f"predicate accessor is not permitted for exact consumer {consumer_ref}"
                )
            if not isinstance(evaluate_node, Mapping):
                raise MechanicalContextError("selector accessor evaluator is unavailable")
            if node_ref not in evaluate_node:
                raise MechanicalContextError(
                    f"bound definition accessor is not in the compiled DAG: {node_ref}"
                )
            return evaluate_node[node_ref]["value"]
        if not isinstance(operand, (str, int, float, bool)) or isinstance(operand, float) and not math.isfinite(operand):
            raise MechanicalContextError("bound comparison scalar is malformed")
        return operand

    left = operand_value(comparison["left"])
    right = operand_value(comparison["right"])
    operator = comparison["operator"]
    if type(left) is not type(right):
        raise MechanicalContextError("bound comparison operands have incompatible types")
    try:
        if operator == "eq":
            return left == right
        if operator == "ne":
            return left != right
        if operator == "lt":
            return left < right
        if operator == "lte":
            return left <= right
        if operator == "gt":
            return left > right
        if operator == "gte":
            return left >= right
    except TypeError as error:
        raise MechanicalContextError("bound comparison is not defined for its operand types") from error
    raise MechanicalContextError(f"bound comparison operator is not admitted here: {operator}")


def evaluate_selector(
    compiled: contracts.CompiledActivity,
    selector_id: str,
    *,
    consumer_id: str,
    observation: CurrentOwnerObservation,
    role_bindings: Mapping[str, NativeOwnerRef],
    accepted_command: Mapping[str, object],
    prospective_documents: tuple[OwnerDocument, ...] = (),
) -> Mapping[str, object]:
    """Return raw finite selector inputs and provenance, never policy arithmetic.

    The only executable root is an exact compiler-retained pair at ``consumer_id``.
    Complete Effect/Asset membership is acquired from the issuer-bound native
    preparation context; index nominations, missing rules, and prospective caller
    documents cannot stand in for that source evidence.
    """
    if not isinstance(selector_id, str) or not selector_id:
        raise MechanicalContextError("selector identity is missing")
    context = _selector_context(
        compiled,
        consumer_id,
        observation,
        role_bindings,
        accepted_command,
        prospective_documents,
    )
    # This validates the original pinned view, compiler lineage, binding basis,
    # accepted facts, and canonical material-policy identity before any expansion.
    context_cache_identity(context)
    policy = _policy_for_selector(compiled, consumer_id, selector_id)
    graph, node_facts, node_roles = _compiled_policy_graph(compiled, policy)
    root_ref = f"selector:{selector_id}"
    if root_ref not in graph:
        raise MechanicalContextError("selected selector root is outside the compiled DAG")
    root_fact_ids = node_facts[(root_ref, root_ref)]
    facts = _accepted_fact_inputs(context, policy, root_fact_ids)

    # Completeness is required even for an empty result. The conformance adapter
    # reads the fixed native families from the pinned source and joins every P0
    # payload; it never interprets an index miss as absence.
    from . import mechanical_sources

    membership = mechanical_sources.prepare_membership(context)
    if not mechanical_sources.is_membership_issued(membership):
        raise MechanicalContextError("native membership is not adapter-issued")
    if not mechanical_sources.revalidate_membership(membership, context):
        raise contracts.NativePreparationHold("REVALIDATION_REQUIRED", context.execution_ref, ())
    membership_observation = membership.p0_observation
    membership_evidence = _membership_wire(membership)
    node_values: dict[str, Mapping[str, object]] = {}
    visiting: set[str] = set()
    fact_edges_by_consumer_mutable: dict[str, set[str]] = {}
    for fact_binding in policy.binding.context_fact_bindings:
        fact_edges_by_consumer_mutable.setdefault(
            fact_binding.consumer_ref, set()
        ).update(fact_binding.fact_ids)
    fact_edges_by_consumer = {
        consumer_ref: frozenset(fact_ids)
        for consumer_ref, fact_ids in fact_edges_by_consumer_mutable.items()
    }
    pairs = {
        pair.selector_id: pair.operation_ids
        for pair in policy.binding.selector_operation_pairs
    }

    def node_value(node_ref: str) -> Mapping[str, object]:
        if node_ref in node_values:
            return node_values[node_ref]
        if node_ref in visiting:
            raise MechanicalContextError(f"mechanical dependency cycle at {node_ref}")
        if node_ref not in graph:
            raise MechanicalContextError(f"unproven mechanical dependency: {node_ref}")
        visiting.add(node_ref)
        kind, _, node_id = node_ref.partition(":")
        metadata: Mapping[str, object]
        if kind == "selector":
            metadata = policy.selector_contracts[node_id]
        elif kind == "accessor":
            metadata = policy.accessor_contracts[node_id]
        elif kind == "derived":
            metadata = policy.derived_node_contracts[node_id]
        else:
            raise MechanicalContextError(f"unproven mechanical dependency: {node_ref}")
        dependencies = {
            dependency: node_value(dependency) for dependency in graph[node_ref]
        }
        role_names = node_roles[(root_ref, node_ref)]
        if kind == "selector":
            operations = pairs.get(node_id)
            if operations is None:
                operations = tuple(metadata["allowed_operations"])
            contributions = _raw_rule_elements(
                context,
                membership,
                policy,
                node_id,
                metadata,
                tuple(operations),
                facts,
                fact_edges_by_consumer,
                role_names,
                node_values,
            )
            result: dict[str, object] = {
                "node_ref": node_ref,
                "value_type": metadata["result_type"],
                "contribution_type": metadata["contribution_type"],
                "combination_policy": metadata["combination_policy"],
                "operation_ids": list(operations),
                "resolution_owner": metadata["resolution_owner"],
                "trace_policy": metadata["trace_policy"],
                "policy_id": metadata.get("calculation_policy_id"),
                "dependencies": dependencies,
                "raw_contributions": contributions,
            }
            if node_id == "health.maximum":
                owner = _role_owner(context, role_names, metadata["subject_kinds"])
                payload, owner_read = _owner_payload(
                    membership_observation, owner, context.execution_ref
                )
                state = payload.get("state")
                if isinstance(state, Mapping) and "build" in state:
                    raise MechanicalContextError(
                        "health.maximum requires the bound Actor build contribution closure"
                    )
                hp = state.get("hp") if isinstance(state, Mapping) else None
                if not isinstance(hp, Mapping):
                    raise contracts.NativePreparationHold(
                        "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
                    )
                base = hp.get("maximum_base")
                adjustment = hp.get("maximum_adjustment", 0)
                if (
                    type(base) is not int
                    or type(adjustment) is not int
                ):
                    raise contracts.NativePreparationHold(
                        "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
                    )
                applicable_candidates = [
                    contribution
                    for contribution in contributions
                    if contribution["predicate_state"] == "TRUE"
                ]
                if applicable_candidates:
                    raise MechanicalContextError(
                        "health.maximum candidates require the Calculation owner"
                    )
                minimum = metadata.get("result_constraints", {}).get("minimum", 1)
                value = max(minimum, base + adjustment)
                result["value"] = value
                result["base_inputs"] = {
                    "maximum_base": base,
                    "maximum_adjustment": adjustment,
                    "owner_ref": _owner_ref_wire(owner),
                    "source_basis": owner_read.source_basis,
                    "generation": owner_read.generation,
                    "fingerprint": owner_read.fingerprint,
                }
            node_values[node_ref] = result
        elif kind == "accessor":
            if node_id in {"health.current", "health.temporary", "life.state"}:
                owner = _role_owner(context, role_names, metadata["subject_kinds"])
                payload, owner_read = _owner_payload(
                    membership_observation, owner, context.execution_ref
                )
                state = payload.get("state")
                if not isinstance(state, Mapping):
                    raise contracts.NativePreparationHold(
                        "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
                    )
                if node_id == "life.state":
                    value = state.get("life_state_id")
                else:
                    hp = state.get("hp")
                    value = hp.get("current" if node_id == "health.current" else "temporary") if isinstance(hp, Mapping) else None
                if (node_id == "life.state" and not isinstance(value, str)) or (
                    node_id != "life.state" and type(value) is not int
                ):
                    raise contracts.NativePreparationHold(
                        "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
                    )
                result = {
                    "node_ref": node_ref,
                    "value_type": metadata["value_type"],
                    "value": value,
                    "owner_ref": _owner_ref_wire(owner),
                    "source_basis": owner_read.source_basis,
                    "generation": owner_read.generation,
                    "fingerprint": owner_read.fingerprint,
                    "dependencies": dependencies,
                }
            elif node_id == "health.maximum":
                selector_result = dependencies.get("selector:health.maximum")
                if not isinstance(selector_result, Mapping) or type(selector_result.get("value")) is not int:
                    raise MechanicalContextError("health.maximum selector result is unavailable")
                result = {
                    "node_ref": node_ref,
                    "value_type": metadata["value_type"],
                    "value": selector_result["value"],
                    "dependencies": dependencies,
                }
            elif node_id == "health.bloodied":
                current = dependencies.get("accessor:health.current")
                maximum = dependencies.get("accessor:health.maximum")
                if (
                    not isinstance(current, Mapping)
                    or not isinstance(maximum, Mapping)
                    or type(current.get("value")) is not int
                    or type(maximum.get("value")) is not int
                ):
                    raise MechanicalContextError("health.bloodied dependencies are unavailable")
                result = {
                    "node_ref": node_ref,
                    "value_type": metadata["value_type"],
                    "value": current["value"] * 2 <= maximum["value"],
                    "dependencies": dependencies,
                }
            else:
                raise MechanicalContextError(
                    f"accessor requires a bound input outside this finite DAG slice: {node_id}"
                )
            node_values[node_ref] = result
        else:
            if node_id != "effect_availability":
                raise MechanicalContextError(
                    f"derived node requires an unimplemented native contract: {node_id}"
                )
            subject_effects, _subject_assets, subject_ids = (
                _rule_element_sources_for_roles(context, membership, role_names)
            )
            support_dependencies = _support_effect_dependencies(
                membership, subject_effects
            )
            result = {
                "node_ref": node_ref,
                "result_role": metadata["result_role"],
                "membership_candidates": [
                    _membership_effect_wire(item) for item in subject_effects
                ],
                "effect_dependencies": [
                    _membership_effect_wire(item) for item in support_dependencies
                ],
                "exclusions": [
                    {
                        "owner_ref": _owner_ref_wire(item.owner_ref),
                        "target_id": item.target_id,
                        "reason": item.reason,
                        "source_basis": item.source_basis,
                        "fingerprint": item.fingerprint,
                    }
                    for item in membership.exclusions
                    if item.target_id in subject_ids
                ],
                "dependencies": dependencies,
            }
            node_values[node_ref] = result
        visiting.remove(node_ref)
        return node_values[node_ref]

    selector_result = node_value(root_ref)
    if not mechanical_sources.revalidate_membership(membership, context):
        raise contracts.NativePreparationHold("REVALIDATION_REQUIRED", context.execution_ref, ())
    return {
        "selector_id": selector_id,
        "consumer_id": consumer_id,
        "calculation_policy_id": policy.binding.profile_id,
        "calculation_policy_generation": policy.binding.profile_generation,
        "selector_result": selector_result,
        "context_facts": [
            _thaw(facts[fact_id]) for fact_id in sorted(root_fact_ids)
        ],
        "read_refs": list(policy.binding.reads)
        + [reference for reference in policy.dependency_read_refs if reference not in policy.binding.reads],
        "native_membership": membership_evidence,
        "provenance": {
            "activity_id": compiled.activity_id,
            "consumer_id": consumer_id,
            "occurrence_id": context.occurrence_id,
            "command_id": context.execution_ref.command_id,
            "resolution_id": context.execution_ref.resolution_id,
            "definition_semantic_hash": compiled.definition_semantic_hash,
            "compiler_generation": compiled.compiler_generation,
            "catalog_context_fingerprint": compiled.catalog_context_fingerprint,
            "role_bindings": {
                role: _owner_ref_wire(owner)
                for role, owner in sorted(context.role_bindings.items())
            },
            "accepted_fact_refs": list(context.accepted_fact_refs),
            "policy_refs": list(context.policy_refs),
            "observation_fingerprint": membership.p0_observation.observation_fingerprint,
            "source_revision": membership.source_revision,
            "source_tree_sha": membership.source_tree_sha,
        },
    }
