"""Pure, pre-RNG realization of the selected attack-roll policy."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from . import activity_contracts as contracts
from . import mechanical_context, structural_contracts
from .current_owner import NativeOwnerRef

# framework_module_version: 1.0.1
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.1"

ROLL_POLICY_ID: Final[str] = "calculation.roll_advantage_srd521"
ROLL_POLICY_GENERATION: Final[int] = 1
ROLL_SELECTOR_ID: Final[str] = "attack.roll"
ROLL_COMBINATION_POLICY: Final[str] = "roll_advantage_cancellation_v1"
ROLL_OPERATION_KINDS: Final[Mapping[str, str]] = MappingProxyType(
    {
        "rule.add_flat": "FLAT_MODIFIER",
        "rule.grant_advantage": "ADVANTAGE",
        "rule.grant_disadvantage": "DISADVANTAGE",
    }
)
ROLL_OPERATION_CONSTRAINTS: Final[Mapping[str, frozenset[str]]] = MappingProxyType(
    {
        "rule.add_flat": frozenset(
            {"finite_integer", "stable_raw_dice_identity_and_contribution_provenance"}
        ),
        "rule.grant_advantage": frozenset(
            {
                "literal_true",
                "effect.innate_sorcery_source_only",
                "bound_activity_family.activity.spell_attack_only",
                "stable_raw_dice_identity_and_contribution_provenance",
            }
        ),
        "rule.grant_disadvantage": frozenset(
            {
                "literal_true",
                "effect.innate_sorcery_source_only",
                "bound_activity_family.activity.spell_attack_only",
                "stable_raw_dice_identity_and_contribution_provenance",
            }
        ),
    }
)
_REJECTION_ORDER: Final[tuple[str, ...]] = (
    "PREDICATE_FALSE",
    "SOURCE_NOT_ELIGIBLE",
    "ACTIVITY_NOT_ELIGIBLE",
)
_UNSUPPORTED_ROLL_ELEMENT_MEMBERS: Final[frozenset[str]] = frozenset(
    {"gate", "priority", "stacking_key"}
)


class CalculationError(ValueError):
    """A selected calculation policy is not closed by its issued source."""


def calculate_selector(
    context: contracts.NativePreparationContext, selector_id: str
) -> Mapping[str, object]:
    """Normalize an authentic raw selector DAG without selecting or drawing dice.

    The only realized policy in this bounded slice is ``attack.roll`` under the
    selected roll-advantage profile. MechanicalContext remains the authority for
    compiler/source pair, exact bindings, predicates, complete native membership,
    transitive read/fact permissions, and revalidation. This function consumes
    that issued raw DAG and adds only the finite policy result/trace.
    """
    if type(context) is not contracts.NativePreparationContext:
        raise CalculationError("roll calculation requires a typed preparation context")
    if selector_id != ROLL_SELECTOR_ID:
        raise CalculationError(
            "roll calculation selector is not the selected attack.roll root"
        )
    if not contracts._preparation_context_is_issued(context):
        raise CalculationError(
            "roll calculation requires the exact unchanged issued context"
        )

    # The evaluator enforces exact issuance/currentness while acquiring the
    # complete native read union and again before returning.
    raw_evaluation = mechanical_context.evaluate_selector(
        context.compiled,
        selector_id,
        consumer_id=context.consumer_id,
        observation=context.observation,
        role_bindings=context.role_bindings,
        accepted_command=context.accepted_command,
    )
    policy = _issued_roll_policy(context)
    activity_family_id = _activity_family_id(context)
    normalized = _normalize_roll_policy(
        context, policy, activity_family_id, raw_evaluation
    )
    try:
        structural_contracts.validate_contract("roll_policy_result", normalized)
    except structural_contracts.StructuralContractError as error:
        raise CalculationError(
            "normalized roll result violates its installed closed contract"
        ) from error
    return normalized


def _issued_roll_policy(
    context: contracts.NativePreparationContext,
) -> contracts.CompiledCalculationPolicy:
    matches = tuple(
        policy
        for policy in context.compiled.calculation_policy_bindings
        if policy.binding.consumer_id == context.consumer_id
        and policy.binding.profile_id == ROLL_POLICY_ID
        and policy.binding.profile_generation == ROLL_POLICY_GENERATION
        and any(
            pair.selector_id == ROLL_SELECTOR_ID
            for pair in policy.binding.selector_operation_pairs
        )
    )
    if len(matches) != 1:
        raise CalculationError("issued consumer does not retain one exact roll policy")
    policy = matches[0]
    pairs = policy.binding.selector_operation_pairs
    if (
        len(pairs) != 1
        or pairs[0].selector_id != ROLL_SELECTOR_ID
        or set(pairs[0].operation_ids) != set(ROLL_OPERATION_KINDS)
        or len(pairs[0].operation_ids) != len(ROLL_OPERATION_KINDS)
        or policy.binding.context_fact_bindings
        or any(reference.startswith("fact:") for reference in policy.binding.reads)
        or policy.context_fact_contracts
    ):
        raise CalculationError("issued roll policy pair/fact closure is incomplete")
    selector = policy.selector_contracts.get(ROLL_SELECTOR_ID)
    if not isinstance(selector, Mapping):
        raise CalculationError("issued roll selector metadata is unavailable")
    if (
        selector.get("calculation_policy_id") != ROLL_POLICY_ID
        or selector.get("calculation_policy_generation") != ROLL_POLICY_GENERATION
        or selector.get("contribution_type") != "roll_modifier"
        or selector.get("result_type") != "roll_modifier_set"
        or selector.get("combination_policy") != ROLL_COMBINATION_POLICY
        or selector.get("allowed_input_classes") != ("ENGINE_STATE",)
        or selector.get("permitted_context_fact_ids") != ()
        or set(selector.get("allowed_operations", ())) != set(ROLL_OPERATION_KINDS)
    ):
        raise CalculationError(
            "issued roll selector contract is not the exact selected profile"
        )
    operation_contracts = selector.get("operation_contracts")
    if not isinstance(operation_contracts, Mapping) or set(operation_contracts) != set(
        ROLL_OPERATION_KINDS
    ):
        raise CalculationError(
            "issued roll selector operation contracts are incomplete"
        )
    for operation_id, contribution_kind in ROLL_OPERATION_KINDS.items():
        operation = operation_contracts.get(operation_id)
        if not isinstance(operation, Mapping):
            raise CalculationError(f"issued roll pair is missing {operation_id}")
        constraints = operation.get("constraints")
        if not isinstance(constraints, (tuple, list)):
            raise CalculationError(
                f"issued roll constraints are malformed for {operation_id}"
            )
        if (
            operation.get("roll_contribution_type") != contribution_kind
            or operation.get("value_kind") != "roll_modifier"
            or operation.get("normalization") != "CANCEL_APPLICABLE_OPPOSITES"
            or operation.get("calculation_policy_id") != ROLL_POLICY_ID
            or operation.get("calculation_policy_generation") != ROLL_POLICY_GENERATION
            or frozenset(constraints) != ROLL_OPERATION_CONSTRAINTS[operation_id]
            or (
                contribution_kind != "FLAT_MODIFIER"
                and operation.get("fixed_value") is not True
            )
        ):
            raise CalculationError(
                f"issued roll operation contract is not exact: {operation_id}"
            )
    return policy


def _activity_family_id(context: contracts.NativePreparationContext) -> str:
    activity = context.catalog.frozen_definitions.get(context.compiled.activity_id)
    if (
        not isinstance(activity, Mapping)
        or activity.get("kind") != "definition.activity"
    ):
        raise CalculationError("issued Activity source definition is unavailable")
    data = activity.get("data")
    family_id = data.get("family_id") if isinstance(data, Mapping) else None
    if not isinstance(family_id, str) or not family_id:
        raise CalculationError("issued Activity family identity is missing")
    return family_id


def _normalize_roll_policy(
    context: contracts.NativePreparationContext,
    policy: contracts.CompiledCalculationPolicy,
    activity_family_id: str,
    raw_evaluation: Mapping[str, object],
) -> dict[str, object]:
    if set(raw_evaluation) != {
        "selector_id",
        "consumer_id",
        "calculation_policy_id",
        "calculation_policy_generation",
        "selector_result",
        "context_facts",
        "read_refs",
        "native_membership",
        "provenance",
    }:
        raise CalculationError(
            "raw MechanicalContext evaluation is not the closed selector result"
        )
    if (
        raw_evaluation.get("selector_id") != ROLL_SELECTOR_ID
        or raw_evaluation.get("consumer_id") != context.consumer_id
        or raw_evaluation.get("calculation_policy_id") != ROLL_POLICY_ID
        or raw_evaluation.get("calculation_policy_generation") != ROLL_POLICY_GENERATION
        or raw_evaluation.get("context_facts") not in ([], ())
    ):
        raise CalculationError(
            "raw selector result differs from the issued roll policy binding"
        )
    selector_result = raw_evaluation.get("selector_result")
    if not isinstance(selector_result, Mapping) or set(selector_result) != {
        "node_ref",
        "value_type",
        "contribution_type",
        "combination_policy",
        "operation_ids",
        "resolution_owner",
        "trace_policy",
        "policy_id",
        "dependencies",
        "raw_contributions",
    }:
        raise CalculationError(
            "raw selector node is not the unnormalized roll contribution set"
        )
    if (
        selector_result.get("node_ref") != "selector:attack.roll"
        or selector_result.get("value_type") != "roll_modifier_set"
        or selector_result.get("contribution_type") != "roll_modifier"
        or selector_result.get("combination_policy") != ROLL_COMBINATION_POLICY
        or selector_result.get("policy_id") != ROLL_POLICY_ID
        or selector_result.get("resolution_owner") != "SELECTOR_METADATA"
        or selector_result.get("trace_policy") != "RETAIN_ACCEPTED_REJECTED_PROVENANCE"
        or set(selector_result.get("operation_ids", ())) != set(ROLL_OPERATION_KINDS)
        or "value" in selector_result
    ):
        raise CalculationError(
            "raw selector result violates the selected unnormalized roll contract"
        )

    raw_contributions = selector_result.get("raw_contributions")
    if not isinstance(raw_contributions, (tuple, list)):
        raise CalculationError(
            "raw roll contributions are not an ordered source collection"
        )
    native_membership = raw_evaluation.get("native_membership")
    if not isinstance(native_membership, Mapping):
        raise CalculationError("roll source membership evidence is unavailable")
    effect_evidence = _membership_evidence_by_application(
        native_membership.get("effects"), "world.effect"
    )
    asset_evidence = _membership_evidence_by_application(
        native_membership.get("assets"), "world.asset"
    )
    trace_rows = [
        _normalize_contribution(
            context.execution_ref,
            row,
            activity_family_id,
            effect_evidence,
            asset_evidence,
        )
        for row in raw_contributions
    ]
    trace_rows.sort(key=_contribution_sort_key)

    flat_values: list[int] = []
    accepted_advantage_count = 0
    accepted_disadvantage_count = 0
    for row in trace_rows:
        if row["disposition"] != "ACCEPTED":
            continue
        kind = row["contribution_kind"]
        if kind == "FLAT_MODIFIER":
            value = row["value"]
            if type(value) is not int:
                raise CalculationError("accepted flat modifier is not a finite integer")
            flat_values.append(value)
        elif kind == "ADVANTAGE":
            accepted_advantage_count += 1
        elif kind == "DISADVANTAGE":
            accepted_disadvantage_count += 1
        else:
            raise CalculationError("raw roll contribution kind is not admitted")

    if accepted_advantage_count and accepted_disadvantage_count:
        mode = "NORMAL"
        cancellation = "OPPOSITES_CANCEL"
    elif accepted_advantage_count:
        mode = "ADVANTAGE"
        cancellation = "ADVANTAGE_ONLY"
    elif accepted_disadvantage_count:
        mode = "DISADVANTAGE"
        cancellation = "DISADVANTAGE_ONLY"
    else:
        mode = "NORMAL"
        cancellation = "NO_APPLICABLE_STATE"

    root_role_bindings = tuple(
        binding
        for binding in policy.binding.native_role_bindings
        if binding.read_ref == "selector:attack.roll"
    )
    if len(root_role_bindings) != 1:
        raise CalculationError("roll selector has no exact native role binding")
    selector_subject_bindings = []
    for role_name in sorted(root_role_bindings[0].role_names):
        owner_ref = context.role_bindings.get(role_name)
        if type(owner_ref) is not NativeOwnerRef:
            raise CalculationError(
                f"roll selector role has no exact native owner: {role_name}"
            )
        selector_subject_bindings.append(
            {"role_name": role_name, "owner_ref": _owner_ref_wire(owner_ref)}
        )

    read_refs = raw_evaluation.get("read_refs")
    if (
        not isinstance(read_refs, (tuple, list))
        or any(not isinstance(reference, str) for reference in read_refs)
        or any(reference.startswith("fact:") for reference in read_refs)
    ):
        raise CalculationError(
            "roll selector transitive read/fact permission differs from its profile"
        )
    provenance = raw_evaluation.get("provenance")
    if not isinstance(native_membership, Mapping) or not isinstance(
        provenance, Mapping
    ):
        raise CalculationError(
            "roll source membership/provenance evidence is unavailable"
        )
    source_revision = native_membership.get("source_revision")
    source_tree_sha = native_membership.get("source_tree_sha")
    observation_fingerprint = provenance.get("observation_fingerprint")
    if set(native_membership) != {
        "source_revision",
        "source_tree_sha",
        "effect_ids",
        "effect_dependencies",
        "effects",
        "excluded_effect_ids",
        "exclusions",
        "asset_ids",
        "assets",
        "family_coverage",
        "owner_reads",
    }:
        raise CalculationError(
            "native membership evidence is not the closed source observation"
        )
    if not all(
        isinstance(value, str) and value
        for value in (source_revision, source_tree_sha, observation_fingerprint)
    ):
        raise CalculationError("roll source observation identity is incomplete")
    if source_revision != provenance.get(
        "source_revision"
    ) or source_tree_sha != provenance.get("source_tree_sha"):
        raise CalculationError(
            "roll source evidence identity differs across the raw join"
        )
    fixed_roll_results = context.resolution.get("fixed_rng_results")
    if not isinstance(fixed_roll_results, (tuple, list)):
        raise CalculationError("fixed raw-roll evidence is not a closed sequence")
    if context.fixed_roll_refs or fixed_roll_results:
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        )

    result: dict[str, object] = {
        "selector_id": ROLL_SELECTOR_ID,
        "consumer_id": context.consumer_id,
        "profile_id": ROLL_POLICY_ID,
        "profile_generation": ROLL_POLICY_GENERATION,
        "activity_id": context.compiled.activity_id,
        "activity_family_id": activity_family_id,
        "occurrence_id": context.occurrence_id,
        "execution_ref": _execution_ref_wire(context.execution_ref),
        "compiled_policy": _compiled_policy_wire(policy),
        "read_refs": list(read_refs),
        "context_facts": _plain(raw_evaluation["context_facts"]),
        "selector_subject_bindings": selector_subject_bindings,
        "mode": mode,
        "modifier": sum(flat_values),
        "required_d20_count": 1 if mode == "NORMAL" else 2,
        "fixed_roll_selection": "HELD_NO_FIXED_ROLL_AUTHORITY",
        "fixed_roll_refs": [],
        "fixed_roll_results": [],
        "rng_draw_count": 0,
        "trace": {
            "raw_contributions": trace_rows,
            "accepted_advantage_count": accepted_advantage_count,
            "accepted_disadvantage_count": accepted_disadvantage_count,
            "accepted_flat_modifier_count": len(flat_values),
            "cancellation": cancellation,
            "mode": mode,
        },
        "source_evidence": {
            "observation_fingerprint": observation_fingerprint,
            "source_revision": source_revision,
            "source_tree_sha": source_tree_sha,
            "catalog_context_fingerprint": context.compiled.catalog_context_fingerprint,
            "definition_semantic_hash": context.compiled.definition_semantic_hash,
            "compiler_generation": context.compiled.compiler_generation,
            "native_membership": _plain(native_membership),
        },
    }
    return result


def _normalize_contribution(
    execution_ref: contracts.ExecutionRef,
    raw: object,
    activity_family_id: str,
    effect_evidence: Mapping[str, Mapping[str, object]],
    asset_evidence: Mapping[str, Mapping[str, object]],
) -> dict[str, object]:
    if not isinstance(raw, Mapping):
        raise CalculationError("raw roll contribution is not a source-backed object")
    required = {
        "owner_ref",
        "owner_definition_id",
        "owner_kind",
        "owner_application_id",
        "rule_element_ordinal",
        "operation_id",
        "value_kind",
        "operation_contract",
        "value",
        "rule_element",
        "predicate",
        "predicate_result",
        "predicate_state",
    }
    if set(raw) != required:
        raise CalculationError("raw roll contribution provenance is not closed")
    operation_id = raw.get("operation_id")
    if not isinstance(operation_id, str) or operation_id not in ROLL_OPERATION_KINDS:
        raise CalculationError(
            "raw roll contribution operation is outside the exact pair"
        )
    contribution_kind = ROLL_OPERATION_KINDS[operation_id]
    operation = raw.get("operation_contract")
    if not isinstance(operation, Mapping):
        raise CalculationError("raw roll operation contract is unavailable")
    constraints = operation.get("constraints")
    if not isinstance(constraints, (tuple, list)):
        raise CalculationError("raw roll operation constraints are malformed")
    if (
        operation.get("roll_contribution_type") != contribution_kind
        or operation.get("value_kind") != "roll_modifier"
        or operation.get("normalization") != "CANCEL_APPLICABLE_OPPOSITES"
        or operation.get("calculation_policy_id") != ROLL_POLICY_ID
        or operation.get("calculation_policy_generation") != ROLL_POLICY_GENERATION
        or frozenset(constraints) != ROLL_OPERATION_CONSTRAINTS[operation_id]
    ):
        raise CalculationError(
            f"raw roll operation contract is not exact: {operation_id}"
        )

    value = raw.get("value")
    if contribution_kind == "FLAT_MODIFIER":
        if type(value) is not int:
            raise CalculationError("raw flat modifier is not a finite integer")
    elif (
        type(value) is not bool
        or value is not True
        or operation.get("fixed_value") is not True
    ):
        raise CalculationError(
            "raw roll state is not the exact literal-true contribution"
        )

    raw_rule_element = raw.get("rule_element")
    if (
        not isinstance(raw_rule_element, Mapping)
        or raw_rule_element.get("selector") != ROLL_SELECTOR_ID
        or raw_rule_element.get("operation_id") != operation_id
        or type(raw_rule_element.get("value")) is not type(value)
        or raw_rule_element.get("value") != value
    ):
        raise CalculationError(
            "raw roll Rule Element differs from its typed contribution"
        )
    unknown_members = set(raw_rule_element) - {
        "selector",
        "operation_id",
        "value",
        "predicate",
        *_UNSUPPORTED_ROLL_ELEMENT_MEMBERS,
    }
    if unknown_members:
        raise CalculationError(
            "raw roll Rule Element has unknown members: "
            + ",".join(sorted(unknown_members))
        )
    unsupported_members = _UNSUPPORTED_ROLL_ELEMENT_MEMBERS.intersection(
        raw_rule_element
    )
    if "gate" in unsupported_members:
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", execution_ref, ()
        )
    if unsupported_members:
        raise CalculationError(
            "roll Rule Element has unsupported optional members: "
            + ",".join(sorted(unsupported_members))
        )
    predicate_result = raw.get("predicate_result")
    predicate_state = raw.get("predicate_state")
    if type(predicate_result) is not bool or predicate_state not in {"TRUE", "FALSE"}:
        raise CalculationError(
            "raw roll predicate result is not a closed true/false value"
        )
    if predicate_result is not (predicate_state == "TRUE"):
        raise CalculationError("raw roll predicate state/result disagree")

    owner_ref = raw.get("owner_ref")
    owner_definition_id = raw.get("owner_definition_id")
    owner_kind = raw.get("owner_kind")
    owner_application_id = raw.get("owner_application_id")
    ordinal = raw.get("rule_element_ordinal")
    if (
        not isinstance(owner_ref, Mapping)
        or not isinstance(owner_definition_id, str)
        or owner_kind not in {"definition.effect", "definition.asset"}
        or not isinstance(owner_application_id, str)
        or type(ordinal) is not int
        or ordinal < 0
    ):
        raise CalculationError("raw roll source identity is malformed")
    family_key = owner_ref.get("family_key")
    identity = owner_ref.get("identity")
    expected_family = (
        "world.effect" if owner_kind == "definition.effect" else "world.asset"
    )
    if (
        family_key != expected_family
        or not isinstance(identity, (tuple, list))
        or len(identity) != 1
        or identity[0] != owner_application_id
    ):
        raise CalculationError(
            "raw roll source is not bound to its exact native application"
        )

    source_eligibility = "INELIGIBLE"
    activity_eligibility = "NOT_REQUIRED"
    rejection_reasons: set[str] = set()
    if not predicate_result:
        rejection_reasons.add("PREDICATE_FALSE")
    native_source: Mapping[str, object]
    if owner_kind == "definition.effect":
        native_source = effect_evidence.get(owner_application_id, {})
        if not native_source or not _same_value(
            native_source.get("owner_ref"), owner_ref
        ):
            raise CalculationError(
                "raw Effect contribution lacks its exact native membership evidence"
            )
        source_is_active_and_target_local = (
            native_source.get("lifecycle") == "effect_lifecycle.active"
            and native_source.get("is_target_local") is True
        )
    else:
        native_source = asset_evidence.get(owner_application_id, {})
        if not native_source or not _same_value(
            native_source.get("owner_ref"), owner_ref
        ):
            raise CalculationError(
                "raw Asset contribution lacks its exact native membership evidence"
            )
        source_is_active_and_target_local = native_source.get(
            "accessible"
        ) is True and native_source.get("equipment_mode") in {"held", "worn"}
    if contribution_kind == "FLAT_MODIFIER":
        source_is_eligible = source_is_active_and_target_local
    else:
        source_is_eligible = (
            source_is_active_and_target_local
            and owner_kind == "definition.effect"
            and owner_definition_id == "effect.innate_sorcery"
            and family_key == "world.effect"
        )
    source_eligibility = "ELIGIBLE" if source_is_eligible else "INELIGIBLE"
    if not source_is_eligible:
        rejection_reasons.add("SOURCE_NOT_ELIGIBLE")
    if contribution_kind in {"ADVANTAGE", "DISADVANTAGE"}:
        activity_is_spell_attack = activity_family_id == "activity.spell_attack"
        activity_eligibility = "ELIGIBLE" if activity_is_spell_attack else "INELIGIBLE"
        if not activity_is_spell_attack:
            rejection_reasons.add("ACTIVITY_NOT_ELIGIBLE")
    disposition = "REJECTED" if rejection_reasons else "ACCEPTED"
    return {
        "contribution_kind": contribution_kind,
        "operation_id": operation_id,
        "owner_ref": _plain(owner_ref),
        "owner_definition_id": owner_definition_id,
        "owner_kind": owner_kind,
        "owner_application_id": owner_application_id,
        "rule_element_ordinal": ordinal,
        "value": value,
        "operation_contract": _plain(operation),
        "predicate_source_present": raw.get("predicate") is not None,
        "predicate_result": predicate_result,
        "predicate_state": predicate_state,
        "source_eligibility": source_eligibility,
        "activity_eligibility": activity_eligibility,
        "disposition": disposition,
        "rejection_reasons": [
            reason for reason in _REJECTION_ORDER if reason in rejection_reasons
        ],
    }


def _contribution_sort_key(row: Mapping[str, object]) -> tuple[object, ...]:
    owner_ref = row["owner_ref"]
    if not isinstance(owner_ref, Mapping):
        raise CalculationError("normalized source owner identity is malformed")
    identity = owner_ref.get("identity")
    if not isinstance(identity, (tuple, list)):
        raise CalculationError("normalized source identity is malformed")
    return (
        owner_ref.get("family_key", ""),
        tuple(str(item) for item in identity),
        row["owner_application_id"],
        row["rule_element_ordinal"],
        row["operation_id"],
    )


def _membership_evidence_by_application(
    raw_members: object, family_key: str
) -> dict[str, Mapping[str, object]]:
    if not isinstance(raw_members, (tuple, list)):
        raise CalculationError(
            f"native {family_key} membership is not a closed sequence"
        )
    indexed: dict[str, Mapping[str, object]] = {}
    for item in raw_members:
        if not isinstance(item, Mapping):
            raise CalculationError(
                f"native {family_key} membership member is malformed"
            )
        owner_ref = item.get("owner_ref")
        if (
            not isinstance(owner_ref, Mapping)
            or owner_ref.get("family_key") != family_key
        ):
            raise CalculationError(
                f"native membership has a foreign {family_key} identity"
            )
        identity = owner_ref.get("identity")
        if not isinstance(identity, (tuple, list)) or len(identity) != 1:
            raise CalculationError(f"native {family_key} identity is not exact")
        application_id = identity[0]
        if not isinstance(application_id, str) or application_id in indexed:
            raise CalculationError(
                f"native {family_key} membership repeats an application"
            )
        indexed[application_id] = item
    return indexed


def _same_value(left: object, right: object) -> bool:
    same_container_kind = (
        isinstance(left, Mapping) and isinstance(right, Mapping)
    ) or (isinstance(left, (tuple, list)) and isinstance(right, (tuple, list)))
    if type(left) is not type(right) and not same_container_kind:
        return False
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        return set(left) == set(right) and all(
            _same_value(left[key], right[key]) for key in left
        )
    if isinstance(left, (tuple, list)) and isinstance(right, (tuple, list)):
        return len(left) == len(right) and all(
            _same_value(a, b) for a, b in zip(left, right, strict=True)
        )
    return left == right


def _compiled_policy_wire(
    policy: contracts.CompiledCalculationPolicy,
) -> dict[str, object]:
    binding = policy.binding
    return {
        "binding": {
            "consumer_id": binding.consumer_id,
            "profile_id": binding.profile_id,
            "profile_generation": binding.profile_generation,
            "reads": list(binding.reads),
            "selector_operation_pairs": [
                {
                    "selector_id": pair.selector_id,
                    "operation_ids": list(pair.operation_ids),
                }
                for pair in binding.selector_operation_pairs
            ],
            "context_fact_bindings": [
                {"consumer_ref": item.consumer_ref, "fact_ids": list(item.fact_ids)}
                for item in binding.context_fact_bindings
            ],
            "native_role_bindings": [
                {"read_ref": item.read_ref, "role_names": list(item.role_names)}
                for item in binding.native_role_bindings
            ],
        },
        "selector_contracts": _plain(policy.selector_contracts),
        "accessor_contracts": _plain(policy.accessor_contracts),
        "derived_node_contracts": _plain(policy.derived_node_contracts),
        "context_fact_contracts": _plain(policy.context_fact_contracts),
        "role_contracts": _plain(policy.role_contracts),
        "dependency_read_refs": list(policy.dependency_read_refs),
    }


def _owner_ref_wire(owner_ref: NativeOwnerRef) -> dict[str, object]:
    return {"family_key": owner_ref.family_key, "identity": list(owner_ref.identity)}


def _execution_ref_wire(reference: contracts.ExecutionRef) -> dict[str, object]:
    value: dict[str, object] = {
        "command_id": reference.command_id,
        "resolution_id": reference.resolution_id,
    }
    if isinstance(reference, contracts.CastExecutionRef):
        value["cast_generation"] = reference.cast_generation
    return value


def _plain(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_plain(item) for item in value]
    return value
