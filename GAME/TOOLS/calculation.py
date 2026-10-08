"""Pure, pre-RNG realization of the selected attack-roll policy."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from types import MappingProxyType
from typing import Final

from . import activity_contracts as contracts
from . import mechanical_context, structural_contracts
from .current_owner import NativeOwnerRef

# framework_module_version: 1.0.3
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.3"

ROLL_POLICY_ID: Final[str] = "calculation.roll_advantage_srd521"
ROLL_POLICY_GENERATION: Final[int] = 1
ROLL_SELECTOR_ID: Final[str] = "attack.roll"
ROLL_COMBINATION_POLICY: Final[str] = "roll_advantage_cancellation_v1"
DAMAGE_POLICY_ID: Final[str] = "calculation.damage_defense_srd521"
DAMAGE_POLICY_GENERATION: Final[int] = 1
DAMAGE_SELECTOR_ID: Final[str] = "damage.received"
DAMAGE_COMBINATION_POLICY: Final[str] = "damage_defense_source_ordered_v1"
ARMOR_CLASS_POLICY_ID: Final[str] = "calculation.armor_class_srd521"
ARMOR_CLASS_POLICY_GENERATION: Final[int] = 1
ARMOR_CLASS_SELECTOR_ID: Final[str] = "defense.armor_class"
ARMOR_CLASS_COMBINATION_POLICY: Final[str] = "armor_class_nonadditive_base_v1"
ARMOR_CLASS_OPERATION_IDS: Final[tuple[str, str]] = (
    "rule.add_flat",
    "rule.override",
)
_ARMOR_CLASS_OPERATION_CONTRACTS: Final[Mapping[str, Mapping[str, object]]] = (
    MappingProxyType(
        {
            "rule.add_flat": MappingProxyType(
                {
                    "value_kind": "numeric_scalar",
                    "normalization": "SUM",
                    "constraints": ("finite_integer",),
                    "calculation_policy_id": ARMOR_CLASS_POLICY_ID,
                    "calculation_policy_generation": ARMOR_CLASS_POLICY_GENERATION,
                }
            ),
            "rule.override": MappingProxyType(
                {
                    "value_kind": "armor_class_base",
                    "normalization": "SELECT_ONE_LEGAL_BASE",
                    "constraints": ("eligible_nonadditive_ac_base",),
                    "calculation_policy_id": ARMOR_CLASS_POLICY_ID,
                    "calculation_policy_generation": ARMOR_CLASS_POLICY_GENERATION,
                }
            ),
        }
    )
)
_ARMOR_CLASS_REJECTION_ORDER: Final[tuple[str, ...]] = (
    "PREDICATE_FALSE",
    "SOURCE_NOT_ELIGIBLE",
)
_UNSUPPORTED_ARMOR_CLASS_ELEMENT_MEMBERS: Final[frozenset[str]] = frozenset(
    {"gate", "priority", "stacking_key"}
)
_MAGE_ARMOR_DEFINITION_ID: Final[str] = "effect.spell.mage_armor"
_MAGE_ARMOR_RULES_ORIGIN_ID: Final[str] = "source.spell.mage_armor"
_SHIELD_DEFINITION_ID: Final[str] = "effect.spell.shield"
_SHIELD_RULES_ORIGIN_ID: Final[str] = "source.spell.shield"
DAMAGE_OPERATION_TYPES: Final[Mapping[str, str]] = MappingProxyType(
    {
        "rule.add_flat": "ADJUSTMENT",
        "rule.resistance": "RESISTANCE",
        "rule.vulnerability": "VULNERABILITY",
        "rule.immunity": "IMMUNITY",
    }
)
_DAMAGE_STAGE_ORDER: Final[tuple[str, ...]] = (
    "ADJUSTMENT",
    "RESISTANCE",
    "VULNERABILITY",
    "IMMUNITY",
)
_DAMAGE_REJECTION_ORDER: Final[tuple[str, ...]] = (
    "PREDICATE_FALSE",
    "SOURCE_NOT_ELIGIBLE",
    "DAMAGE_TYPE_MISMATCH",
    "ORIGIN_MISMATCH",
    "BYPASSED_BY_COMPONENT",
)
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
_UNSUPPORTED_DAMAGE_ELEMENT_MEMBERS: Final[frozenset[str]] = frozenset(
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
    if selector_id not in {
        ROLL_SELECTOR_ID,
        DAMAGE_SELECTOR_ID,
        ARMOR_CLASS_SELECTOR_ID,
    }:
        raise CalculationError(
            "calculation selector is outside the finite selected policy set"
        )
    if not contracts._preparation_context_is_issued(context):
        raise CalculationError(
            "calculation requires the exact unchanged issued context"
        )

    if selector_id == DAMAGE_SELECTOR_ID:
        return _calculate_damage_selector(context)
    if selector_id == ARMOR_CLASS_SELECTOR_ID:
        return _calculate_armor_class_selector(context)

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


def _calculate_damage_selector(
    context: contracts.NativePreparationContext,
) -> Mapping[str, object]:
    binding = _issued_damage_input_binding(context)
    policy = _issued_damage_policy(context, binding)
    components, amount_basis = _source_damage_components(context, binding)
    raw_evaluation = mechanical_context.evaluate_selector(
        context.compiled,
        DAMAGE_SELECTOR_ID,
        consumer_id=context.consumer_id,
        observation=context.observation,
        role_bindings=context.role_bindings,
        accepted_command=context.accepted_command,
    )
    normalized = _normalize_damage_policy(
        context,
        binding,
        policy,
        components,
        amount_basis,
        raw_evaluation,
    )
    try:
        structural_contracts.validate_contract("damage_policy_result", normalized)
    except structural_contracts.StructuralContractError as error:
        raise CalculationError(
            "normalized damage result violates its installed closed contract"
        ) from error
    return normalized


def _calculate_armor_class_selector(
    context: contracts.NativePreparationContext,
) -> Mapping[str, object]:
    policy = _issued_armor_class_policy(context)
    raw_evaluation = mechanical_context.evaluate_selector(
        context.compiled,
        ARMOR_CLASS_SELECTOR_ID,
        consumer_id=context.consumer_id,
        observation=context.observation,
        role_bindings=context.role_bindings,
        accepted_command=context.accepted_command,
    )
    normalized = _normalize_armor_class_policy(context, policy, raw_evaluation)
    try:
        structural_contracts.validate_contract("armor_class_policy_result", normalized)
    except structural_contracts.StructuralContractError as error:
        raise CalculationError(
            "normalized Armor Class result violates its installed closed contract: "
            f"{error}"
        ) from error
    return normalized


def _issued_armor_class_policy(
    context: contracts.NativePreparationContext,
) -> contracts.CompiledCalculationPolicy:
    matches = tuple(
        policy
        for policy in context.compiled.calculation_policy_bindings
        if policy.binding.consumer_id == context.consumer_id
        and policy.binding.profile_id == ARMOR_CLASS_POLICY_ID
        and policy.binding.profile_generation == ARMOR_CLASS_POLICY_GENERATION
    )
    if len(matches) != 1:
        raise CalculationError(
            "issued consumer does not retain one exact Armor Class policy"
        )
    policy = matches[0]
    binding = policy.binding
    descriptor = binding.native_base_descriptor
    if type(descriptor) is not contracts.ArmorClassNativeBaseDescriptor:
        raise CalculationError("issued Armor Class policy has no typed native base")
    expected_role_binding = contracts.NativeRoleBinding(
        f"selector:{ARMOR_CLASS_SELECTOR_ID}", (descriptor.subject_role,)
    )
    if (
        descriptor.kind != "ACTOR_DEXTERITY_BASE"
        or descriptor.ability_id != "ability.dexterity"
        or descriptor.subject_role not in {"actor", "target"}
        or binding.reads != (f"selector:{ARMOR_CLASS_SELECTOR_ID}",)
        or binding.selector_operation_pairs
        != (
            contracts.SelectorOperationPair(
                ARMOR_CLASS_SELECTOR_ID, ARMOR_CLASS_OPERATION_IDS
            ),
        )
        or binding.context_fact_bindings
        or binding.native_role_bindings != (expected_role_binding,)
        or policy.context_fact_contracts
        or policy.dependency_read_refs
    ):
        raise CalculationError(
            "issued Armor Class pair/fact/role/native-base closure is incomplete"
        )

    role_contract = policy.role_contracts.get(descriptor.subject_role)
    if (
        not isinstance(role_contract, Mapping)
        or role_contract.get("family_key") != "world.actor"
        or role_contract.get("required") is not True
    ):
        raise CalculationError(
            "issued Armor Class subject is not a required Actor role"
        )

    selector = policy.selector_contracts.get(ARMOR_CLASS_SELECTOR_ID)
    if not isinstance(selector, Mapping):
        raise CalculationError("issued Armor Class selector metadata is unavailable")
    expected_selector_values = {
        "calculation_policy_id": ARMOR_CLASS_POLICY_ID,
        "calculation_policy_generation": ARMOR_CLASS_POLICY_GENERATION,
        "contribution_type": "armor_class",
        "result_type": "integer",
        "result_constraints": {},
        "combination_policy": ARMOR_CLASS_COMBINATION_POLICY,
        "resolution_owner": "SELECTOR_METADATA",
        "trace_policy": "RETAIN_ACCEPTED_REJECTED_PROVENANCE",
        "allowed_dependency_kinds": (),
        "allowed_input_classes": ("ENGINE_STATE",),
        "permitted_context_fact_ids": (),
        "static_dependencies": (),
        "subject_kinds": ("world.actor",),
        "binding_kinds": ("subject",),
    }
    if any(
        not _same_value(selector.get(name), expected)
        for name, expected in expected_selector_values.items()
    ):
        raise CalculationError(
            "issued Armor Class selector is not the exact selected profile"
        )
    allowed_operations = selector.get("allowed_operations")
    if (
        not isinstance(allowed_operations, (tuple, list))
        or len(allowed_operations) != len(ARMOR_CLASS_OPERATION_IDS)
        or set(allowed_operations) != set(ARMOR_CLASS_OPERATION_IDS)
    ):
        raise CalculationError("issued Armor Class operation pair is not exact")
    operation_contracts = selector.get("operation_contracts")
    if not isinstance(operation_contracts, Mapping) or set(operation_contracts) != set(
        ARMOR_CLASS_OPERATION_IDS
    ):
        raise CalculationError("issued Armor Class operation contracts are incomplete")
    for operation_id, expected in _ARMOR_CLASS_OPERATION_CONTRACTS.items():
        operation = operation_contracts.get(operation_id)
        if not isinstance(operation, Mapping) or not _same_value(operation, expected):
            raise CalculationError(
                f"issued Armor Class operation contract is not exact: {operation_id}"
            )
    return policy


def _normalize_armor_class_policy(
    context: contracts.NativePreparationContext,
    policy: contracts.CompiledCalculationPolicy,
    raw_evaluation: Mapping[str, object],
) -> dict[str, object]:
    expected_evaluation_members = {
        "selector_id",
        "consumer_id",
        "calculation_policy_id",
        "calculation_policy_generation",
        "selector_result",
        "context_facts",
        "read_refs",
        "native_membership",
        "provenance",
    }
    if set(raw_evaluation) != expected_evaluation_members:
        raise CalculationError(
            "raw Armor Class evaluation is not the closed selector result"
        )
    if (
        raw_evaluation.get("selector_id") != ARMOR_CLASS_SELECTOR_ID
        or raw_evaluation.get("consumer_id") != context.consumer_id
        or raw_evaluation.get("calculation_policy_id") != ARMOR_CLASS_POLICY_ID
        or raw_evaluation.get("calculation_policy_generation")
        != ARMOR_CLASS_POLICY_GENERATION
        or raw_evaluation.get("context_facts") not in ((), [])
    ):
        raise CalculationError(
            "raw selector result differs from the issued Armor Class binding"
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
        "native_base_inputs",
    }:
        raise CalculationError(
            "raw Armor Class node is not the closed native-base contribution set"
        )
    operation_ids = selector_result.get("operation_ids")
    if (
        selector_result.get("node_ref") != f"selector:{ARMOR_CLASS_SELECTOR_ID}"
        or selector_result.get("value_type") != "integer"
        or selector_result.get("contribution_type") != "armor_class"
        or selector_result.get("combination_policy") != ARMOR_CLASS_COMBINATION_POLICY
        or selector_result.get("policy_id") != ARMOR_CLASS_POLICY_ID
        or selector_result.get("resolution_owner") != "SELECTOR_METADATA"
        or selector_result.get("trace_policy") != "RETAIN_ACCEPTED_REJECTED_PROVENANCE"
        or not isinstance(operation_ids, (tuple, list))
        or len(operation_ids) != len(ARMOR_CLASS_OPERATION_IDS)
        or set(operation_ids) != set(ARMOR_CLASS_OPERATION_IDS)
        or not isinstance(selector_result.get("dependencies"), Mapping)
        or selector_result.get("dependencies")
        or "value" in selector_result
    ):
        raise CalculationError(
            "raw selector result violates the selected Armor Class contract"
        )

    native_membership = raw_evaluation.get("native_membership")
    provenance = raw_evaluation.get("provenance")
    if not isinstance(native_membership, Mapping) or not isinstance(
        provenance, Mapping
    ):
        raise CalculationError(
            "Armor Class source membership/provenance evidence is unavailable"
        )
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
            "Armor Class membership evidence is not the closed native source proof"
        )
    if set(provenance) != {
        "activity_id",
        "consumer_id",
        "occurrence_id",
        "command_id",
        "resolution_id",
        "definition_semantic_hash",
        "compiler_generation",
        "catalog_context_fingerprint",
        "role_bindings",
        "accepted_fact_refs",
        "policy_refs",
        "observation_fingerprint",
        "source_revision",
        "source_tree_sha",
    }:
        raise CalculationError("Armor Class provenance fields are not closed")
    source_revision = native_membership.get("source_revision")
    source_tree_sha = native_membership.get("source_tree_sha")
    observation_fingerprint = provenance.get("observation_fingerprint")
    if not all(
        isinstance(value, str) and value
        for value in (source_revision, source_tree_sha, observation_fingerprint)
    ):
        raise CalculationError("Armor Class source observation identity is incomplete")
    expected_provenance_roles = {
        role_name: _owner_ref_wire(owner_ref)
        for role_name, owner_ref in sorted(context.role_bindings.items())
        if type(owner_ref) is NativeOwnerRef
    }
    if (
        provenance.get("activity_id") != context.compiled.activity_id
        or provenance.get("consumer_id") != context.consumer_id
        or provenance.get("occurrence_id") != context.occurrence_id
        or provenance.get("command_id") != context.execution_ref.command_id
        or provenance.get("resolution_id") != context.execution_ref.resolution_id
        or provenance.get("definition_semantic_hash")
        != context.compiled.definition_semantic_hash
        or provenance.get("compiler_generation") != context.compiled.compiler_generation
        or provenance.get("catalog_context_fingerprint")
        != context.compiled.catalog_context_fingerprint
        or not _same_value(provenance.get("role_bindings"), expected_provenance_roles)
        or provenance.get("accepted_fact_refs") not in ((), [])
        or provenance.get("policy_refs") not in ((), [])
        or provenance.get("source_revision") != source_revision
        or provenance.get("source_tree_sha") != source_tree_sha
    ):
        raise CalculationError(
            "Armor Class provenance differs across its issued source join"
        )
    read_refs = raw_evaluation.get("read_refs")
    if not isinstance(read_refs, (tuple, list)) or tuple(read_refs) != (
        f"selector:{ARMOR_CLASS_SELECTOR_ID}",
    ):
        raise CalculationError("Armor Class policy reads differ from its exact profile")
    if set(context.role_bindings) - set(expected_provenance_roles):
        raise CalculationError("Armor Class role binding contains an untyped owner")

    descriptor = policy.binding.native_base_descriptor
    subject_ref = context.role_bindings.get(descriptor.subject_role)
    if (
        type(subject_ref) is not NativeOwnerRef
        or subject_ref.family_key != "world.actor"
        or len(subject_ref.identity) != 1
    ):
        raise CalculationError("Armor Class subject role is not an exact Actor owner")
    native_base_inputs = selector_result.get("native_base_inputs")
    subject_id = _validate_armor_class_native_inputs(
        context,
        native_base_inputs,
        native_membership,
        subject_ref,
        descriptor,
    )

    fixed_roll_results = context.resolution.get("fixed_rng_results")
    if not isinstance(fixed_roll_results, (tuple, list)):
        raise CalculationError(
            "Armor Class fixed-roll evidence is not a closed sequence"
        )
    if context.fixed_roll_refs or fixed_roll_results:
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        )

    raw_contributions = selector_result.get("raw_contributions")
    if not isinstance(raw_contributions, (tuple, list)):
        raise CalculationError(
            "raw Armor Class contributions are not an ordered source sequence"
        )
    effect_evidence = _membership_evidence_by_application(
        native_membership.get("effects"), "world.effect"
    )
    asset_evidence = _membership_evidence_by_application(
        native_membership.get("assets"), "world.asset"
    )
    selector_metadata = policy.selector_contracts.get(ARMOR_CLASS_SELECTOR_ID)
    operation_contracts = (
        selector_metadata.get("operation_contracts")
        if isinstance(selector_metadata, Mapping)
        else None
    )
    if not isinstance(operation_contracts, Mapping):
        raise CalculationError("compiled Armor Class operation metadata is unavailable")

    base_contributions: list[dict[str, object]] = []
    modifier_contributions: list[dict[str, object]] = []
    mage_candidates: list[dict[str, object]] = []
    seen_sources: set[tuple[object, ...]] = set()
    for raw in raw_contributions:
        trace, candidate = _normalize_armor_class_contribution(
            context,
            raw,
            operation_contracts,
            effect_evidence,
            asset_evidence,
            subject_id,
            native_base_inputs["native_ability_basis"]["dexterity_modifier"],
            native_base_inputs["equipment_membership"]["assets"],
        )
        source_ref = trace["source_owner_ref"]
        if not isinstance(source_ref, Mapping):
            raise CalculationError("Armor Class contribution source is malformed")
        identity = source_ref.get("identity")
        if not isinstance(identity, (tuple, list)):
            raise CalculationError("Armor Class contribution identity is malformed")
        source_key = (
            source_ref.get("family_key"),
            tuple(identity),
            trace["owner_application_id"],
            trace["rule_element_ordinal"],
            trace["operation_id"],
        )
        if source_key in seen_sources:
            raise CalculationError(
                "Armor Class source repeated one Rule Element contribution"
            )
        seen_sources.add(source_key)
        if trace["operation_id"] == "rule.override":
            base_contributions.append(trace)
            if candidate is not None:
                mage_candidates.append(candidate)
        else:
            modifier_contributions.append(trace)
    if len(mage_candidates) > 1:
        # This profile has no admitted arbitration rule for competing Mage Armor
        # applications or multiple eligible base elements.
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        )
    base_contributions.sort(key=_armor_class_contribution_sort_key)
    modifier_contributions.sort(key=_armor_class_contribution_sort_key)
    mage_candidates.sort(
        key=lambda candidate: (
            tuple(candidate["source_owner_ref"]["identity"]),
            candidate["source_application_id"],
            candidate["rule_element_ordinal"],
        )
    )
    shield_application_ids = {
        trace["owner_application_id"]
        for trace in modifier_contributions
        if trace["owner_definition_id"] == _SHIELD_DEFINITION_ID
        and trace["rules_origin_id"] == _SHIELD_RULES_ORIGIN_ID
        and trace["source_id"] == subject_id
        and trace["disposition"] == "APPLIED"
    }
    if len(shield_application_ids) > 1:
        # The AC profile has no admitted resolver for competing Shield apps.
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        )

    ability_basis = native_base_inputs["native_ability_basis"]
    default_candidate = {
        "base_kind": "UNARMORED_10_PLUS_DEX",
        "base_value": 10 + ability_basis["dexterity_modifier"],
        "source_owner_ref": _plain(ability_basis["subject_owner_ref"]),
        "source_definition_id": None,
        "source_application_id": None,
        "rule_element_ordinal": None,
        "source_id": None,
        "rules_origin_id": None,
        "source_basis": ability_basis["actor_read"]["source_basis"],
        "fingerprint": ability_basis["actor_read"]["fingerprint"],
    }
    base_candidates = [*mage_candidates, default_candidate]
    modifier_total = sum(
        trace["value"]
        for trace in modifier_contributions
        if trace["disposition"] == "APPLIED"
    )
    selection_status = (
        "SELECTED_SOLE_LEGAL_BASE" if len(base_candidates) == 1 else "CHOICE_REQUIRED"
    )
    result: dict[str, object] = {
        "selector_id": ARMOR_CLASS_SELECTOR_ID,
        "consumer_id": context.consumer_id,
        "profile_id": ARMOR_CLASS_POLICY_ID,
        "profile_generation": ARMOR_CLASS_POLICY_GENERATION,
        "activity_id": context.compiled.activity_id,
        "occurrence_id": context.occurrence_id,
        "execution_ref": _execution_ref_wire(context.execution_ref),
        "compiled_policy": _compiled_policy_wire(policy),
        "read_refs": list(read_refs),
        "context_facts": [],
        "subject_binding": {
            "role_name": descriptor.subject_role,
            "owner_ref": _owner_ref_wire(subject_ref),
        },
        "native_base_inputs": _plain(native_base_inputs),
        "selection_status": selection_status,
        "modifier_total": modifier_total,
        "fixed_roll_refs": [],
        "rng_draw_count": 0,
        "trace": {
            "base_candidates": base_candidates,
            "base_contributions": base_contributions,
            "modifier_contributions": modifier_contributions,
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
    if len(base_candidates) == 1:
        selected_base = base_candidates[0]
        result.update(
            {
                "selected_base_kind": selected_base["base_kind"],
                "selected_base_value": selected_base["base_value"],
                "selected_ac": selected_base["base_value"] + modifier_total,
            }
        )
    return result


def _validate_armor_class_native_inputs(
    context: contracts.NativePreparationContext,
    value: object,
    native_membership: Mapping[str, object],
    subject_ref: NativeOwnerRef,
    descriptor: contracts.ArmorClassNativeBaseDescriptor,
) -> str:
    if not isinstance(value, Mapping):
        raise CalculationError("Armor Class native base inputs are unavailable")
    try:
        structural_contracts.validate_contract("armor_class_native_base_inputs", value)
    except structural_contracts.StructuralContractError as error:
        raise CalculationError(
            "Armor Class native base inputs are malformed"
        ) from error
    ability = value.get("native_ability_basis")
    equipment = value.get("equipment_membership")
    if not isinstance(ability, Mapping) or not isinstance(equipment, Mapping):
        raise CalculationError("Armor Class native base inputs are not closed")
    subject_id = subject_ref.identity[0]
    if (
        ability.get("subject_role") not in {"actor", "target"}
        or ability.get("subject_role") != descriptor.subject_role
        or ability.get("ability_id") != "ability.dexterity"
        or not _same_value(
            ability.get("subject_owner_ref"), _owner_ref_wire(subject_ref)
        )
        or equipment.get("subject_actor_id") != subject_id
    ):
        raise CalculationError(
            "Armor Class native base is not bound to its issued Actor"
        )
    base_score = ability.get("base_score")
    adjustment = ability.get("instance_adjustment")
    resolved_score = ability.get("resolved_score")
    dexterity_modifier = ability.get("dexterity_modifier")
    if (
        type(base_score) is not int
        or type(adjustment) is not int
        or type(resolved_score) is not int
        or type(dexterity_modifier) is not int
        or resolved_score != base_score + adjustment
        or dexterity_modifier != (resolved_score - 10) // 2
    ):
        raise CalculationError("Armor Class native Dex math is inconsistent")
    if ability.get("base_source") == "ACTOR_ARCHETYPE":
        archetype_id = ability.get("archetype_definition_id")
        archetype = (
            context.catalog.frozen_definitions.get(archetype_id)
            if isinstance(archetype_id, str)
            else None
        )
        data = archetype.get("data") if isinstance(archetype, Mapping) else None
        abilities = data.get("abilities") if isinstance(data, Mapping) else None
        if (
            not isinstance(archetype, Mapping)
            or archetype.get("id") != archetype_id
            or archetype.get("kind") != "definition.actor_archetype"
            or not isinstance(abilities, Mapping)
            or type(abilities.get("ability.dexterity")) is not int
            or abilities["ability.dexterity"] != base_score
        ):
            raise CalculationError("Armor Class archetype Dex source is not exact")

    actor_read = ability.get("actor_read")
    owner_reads = native_membership.get("owner_reads")
    if not isinstance(actor_read, Mapping) or not isinstance(
        owner_reads, (tuple, list)
    ):
        raise CalculationError("Armor Class Actor read evidence is unavailable")
    actor_reads = [
        row
        for row in owner_reads
        if isinstance(row, Mapping)
        and _same_value(row.get("owner_ref"), _owner_ref_wire(subject_ref))
    ]
    if (
        len(actor_reads) != 1
        or not _same_value(actor_reads[0], actor_read)
        or actor_read.get("status") != "RESOLVED"
        or not isinstance(actor_read.get("source_basis"), str)
        or not actor_read.get("source_basis")
        or not isinstance(actor_read.get("fingerprint"), str)
        or len(actor_read["fingerprint"]) != 64
    ):
        raise CalculationError(
            "Armor Class Actor read does not match native membership"
        )

    asset_evidence = _membership_evidence_by_application(
        native_membership.get("assets"), "world.asset"
    )
    expected_equipment = [
        member
        for _asset_id, member in sorted(asset_evidence.items())
        if member.get("placement_owner_id") == subject_id
    ]
    retained_equipment = equipment.get("assets")
    if not isinstance(retained_equipment, (tuple, list)) or len(
        retained_equipment
    ) != len(expected_equipment):
        raise CalculationError(
            "Armor Class equipment closure differs from native membership"
        )
    for member, retained in zip(expected_equipment, retained_equipment, strict=True):
        if not isinstance(retained, Mapping):
            raise CalculationError("Armor Class retained equipment member is malformed")
        if any(
            not _same_value(retained.get(name), member.get(name))
            for name in (
                "owner_ref",
                "equipment_mode",
                "placement_owner_id",
                "container_path",
                "accessible",
                "blocker_asset_id",
                "conversion_mode",
                "source_basis",
                "fingerprint",
            )
        ):
            raise CalculationError(
                "Armor Class equipment member differs from its native membership"
            )
        definition_id = retained.get("definition_id")
        asset_definition = (
            context.catalog.frozen_definitions.get(definition_id)
            if isinstance(definition_id, str)
            else None
        )
        facets = (
            asset_definition.get("facets")
            if isinstance(asset_definition, Mapping)
            else None
        )
        if (
            not isinstance(asset_definition, Mapping)
            or asset_definition.get("id") != definition_id
            or asset_definition.get("kind") != "definition.asset"
            or not isinstance(facets, (tuple, list))
            or not _same_value(retained.get("facets"), facets)
        ):
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
            )
    for member in retained_equipment:
        facets = member.get("facets")
        if (
            member.get("equipment_mode") == "worn"
            and isinstance(facets, (tuple, list))
            and "asset.armor" in facets
        ):
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
            )
    return subject_id


def _normalize_armor_class_contribution(
    context: contracts.NativePreparationContext,
    raw: object,
    expected_operation_contracts: Mapping[str, object],
    effect_evidence: Mapping[str, Mapping[str, object]],
    asset_evidence: Mapping[str, Mapping[str, object]],
    subject_id: str,
    dexterity_modifier: int,
    equipment_members: object,
) -> tuple[dict[str, object], dict[str, object] | None]:
    required_members = {
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
    if not isinstance(raw, Mapping) or set(raw) != required_members:
        raise CalculationError("raw Armor Class contribution provenance is not closed")
    operation_id = raw.get("operation_id")
    if (
        not isinstance(operation_id, str)
        or operation_id not in _ARMOR_CLASS_OPERATION_CONTRACTS
    ):
        raise CalculationError(
            "raw Armor Class operation is outside the exact selected pair"
        )
    expected_operation = expected_operation_contracts.get(operation_id)
    operation = raw.get("operation_contract")
    if (
        not isinstance(operation, Mapping)
        or not isinstance(expected_operation, Mapping)
        or not _same_value(operation, expected_operation)
        or not _same_value(operation, _ARMOR_CLASS_OPERATION_CONTRACTS[operation_id])
    ):
        raise CalculationError(
            f"raw Armor Class operation contract is not exact: {operation_id}"
        )

    value = raw.get("value")
    if operation_id == "rule.add_flat":
        if type(value) is not int:
            raise CalculationError("raw Armor Class flat modifier is not an integer")
    else:
        try:
            structural_contracts.validate_contract("armor_class_base_value", value)
        except structural_contracts.StructuralContractError as error:
            raise CalculationError(
                "raw Armor Class base is not the exact Mage Armor value"
            ) from error

    rule_element = raw.get("rule_element")
    if not isinstance(rule_element, Mapping):
        raise CalculationError("raw Armor Class Rule Element source is unavailable")
    unsupported = _UNSUPPORTED_ARMOR_CLASS_ELEMENT_MEMBERS.intersection(rule_element)
    if unsupported:
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        )
    if set(rule_element) - {"selector", "operation_id", "value", "predicate"}:
        raise CalculationError(
            "Armor Class Rule Element has unsupported source members"
        )
    if (
        rule_element.get("selector") != ARMOR_CLASS_SELECTOR_ID
        or rule_element.get("operation_id") != operation_id
        or not _same_value(rule_element.get("value"), value)
        or not _same_value(raw.get("predicate"), rule_element.get("predicate"))
    ):
        raise CalculationError(
            "raw Armor Class Rule Element differs from its typed contribution"
        )

    owner_ref = raw.get("owner_ref")
    owner_definition_id = raw.get("owner_definition_id")
    owner_kind = raw.get("owner_kind")
    application_id = raw.get("owner_application_id")
    ordinal = raw.get("rule_element_ordinal")
    if (
        not isinstance(owner_ref, Mapping)
        or not isinstance(owner_definition_id, str)
        or not owner_definition_id
        or owner_kind not in {"definition.effect", "definition.asset"}
        or not isinstance(application_id, str)
        or not application_id
        or type(ordinal) is not int
        or ordinal < 0
    ):
        raise CalculationError("raw Armor Class source identity is malformed")
    expected_family = (
        "world.effect" if owner_kind == "definition.effect" else "world.asset"
    )
    identity = owner_ref.get("identity")
    if (
        owner_ref.get("family_key") != expected_family
        or not isinstance(identity, (tuple, list))
        or len(identity) != 1
        or identity[0] != application_id
    ):
        raise CalculationError(
            "raw Armor Class source is not its exact native application"
        )

    definition = context.catalog.frozen_definitions.get(owner_definition_id)
    definition_data = (
        definition.get("data") if isinstance(definition, Mapping) else None
    )
    source_elements = (
        definition_data.get("rule_elements")
        if isinstance(definition_data, Mapping)
        else None
    )
    if (
        not isinstance(definition, Mapping)
        or definition.get("id") != owner_definition_id
        or definition.get("kind") != owner_kind
        or not isinstance(source_elements, (tuple, list))
        or ordinal >= len(source_elements)
        or not _same_value(source_elements[ordinal], rule_element)
    ):
        raise CalculationError(
            "Armor Class Rule Element differs from its exact source definition"
        )
    if owner_definition_id == _MAGE_ARMOR_DEFINITION_ID:
        mage_armor_ac_elements = [
            element
            for element in source_elements
            if isinstance(element, Mapping)
            and element.get("selector") == ARMOR_CLASS_SELECTOR_ID
        ]
        if len(mage_armor_ac_elements) != 1:
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
            )
    if owner_definition_id == _SHIELD_DEFINITION_ID:
        shield_ac_elements = [
            element
            for element in source_elements
            if isinstance(element, Mapping)
            and element.get("selector") == ARMOR_CLASS_SELECTOR_ID
        ]
        expected_shield_element = {
            "selector": ARMOR_CLASS_SELECTOR_ID,
            "operation_id": "rule.add_flat",
            "value": 5,
        }
        if (
            owner_kind != "definition.effect"
            or definition.get("kind") != "definition.effect"
            or len(shield_ac_elements) != 1
            or not _same_value(shield_ac_elements[0], expected_shield_element)
        ):
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
            )
    if (
        owner_kind == "definition.effect"
        and isinstance(definition_data, Mapping)
        and "arbitration_policy_id" in definition_data
    ):
        # This AC binding has no Effect-arbitration read. Membership proves
        # existence, not participation, so do not combine unarbitrated sources.
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        )

    predicate_result = raw.get("predicate_result")
    predicate_state = raw.get("predicate_state")
    if type(predicate_result) is not bool or predicate_state not in {"TRUE", "FALSE"}:
        raise CalculationError("raw Armor Class predicate is not a closed boolean")
    if predicate_result is not (predicate_state == "TRUE"):
        raise CalculationError("raw Armor Class predicate result/state disagree")

    if owner_kind == "definition.effect":
        native_source = effect_evidence.get(application_id, {})
    else:
        native_source = asset_evidence.get(application_id, {})
    if not native_source or not _same_value(native_source.get("owner_ref"), owner_ref):
        raise CalculationError(
            "Armor Class contribution lacks exact native membership evidence"
        )
    source_id = (
        native_source.get("source_id") if owner_kind == "definition.effect" else None
    )
    rules_origin_id = (
        native_source.get("rules_origin_id")
        if owner_kind == "definition.effect"
        else None
    )
    mage_armor_source_claimed = (
        owner_definition_id == _MAGE_ARMOR_DEFINITION_ID
        or rules_origin_id == _MAGE_ARMOR_RULES_ORIGIN_ID
    )
    if operation_id == "rule.add_flat" and mage_armor_source_claimed:
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        )
    shield_source_claimed = (
        owner_definition_id == _SHIELD_DEFINITION_ID
        or rules_origin_id == _SHIELD_RULES_ORIGIN_ID
    )
    if shield_source_claimed and (
        owner_kind != "definition.effect"
        or
        operation_id != "rule.add_flat"
        or owner_definition_id != _SHIELD_DEFINITION_ID
        or rules_origin_id != _SHIELD_RULES_ORIGIN_ID
        or source_id != subject_id
        or value != 5
    ):
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        )
    source_basis = native_source.get("source_basis")
    fingerprint = native_source.get("fingerprint")
    if (
        not isinstance(source_basis, str)
        or not source_basis
        or not isinstance(fingerprint, str)
        or len(fingerprint) != 64
    ):
        raise CalculationError("Armor Class native source evidence is incomplete")

    if (
        operation_id == "rule.override"
        and owner_kind == "definition.effect"
        and owner_definition_id == _MAGE_ARMOR_DEFINITION_ID
        and predicate_result
        and native_source.get("lifecycle") == "effect_lifecycle.active"
        and native_source.get("is_target_local") is True
        and native_source.get("target_id") == subject_id
        and (
            native_source.get("support_effect_id") is not None
            or not isinstance(source_id, str)
            or not source_id
            or rules_origin_id != _MAGE_ARMOR_RULES_ORIGIN_ID
        )
    ):
        # A potentially participating exact Mage Armor application cannot be
        # demoted to ordinary source ineligibility when its support or source
        # provenance is unproved. This profile has no support/arbitration reader.
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        )

    if owner_kind == "definition.effect":
        source_is_target_local = (
            native_source.get("lifecycle") == "effect_lifecycle.active"
            and native_source.get("is_target_local") is True
            and native_source.get("target_id") == subject_id
            and isinstance(source_id, str)
            and bool(source_id)
            and isinstance(rules_origin_id, str)
            and bool(rules_origin_id)
            and native_source.get("support_effect_id") is None
        )
    else:
        source_is_target_local = (
            native_source.get("accessible") is True
            and native_source.get("placement_owner_id") == subject_id
            and native_source.get("equipment_mode") in {"held", "worn"}
            and native_source.get("blocker_asset_id") is None
            and native_source.get("conversion_mode") is None
            and isinstance(equipment_members, (tuple, list))
            and any(
                isinstance(member, Mapping)
                and _same_value(member.get("owner_ref"), owner_ref)
                for member in equipment_members
            )
        )
        attunement = (
            definition_data.get("attunement")
            if isinstance(definition_data, Mapping)
            else None
        )
        if attunement is not None:
            if (
                not isinstance(attunement, Mapping)
                or set(attunement) - {"required", "allowed_class_ids"}
                or type(attunement.get("required")) is not bool
            ):
                raise contracts.NativePreparationHold(
                    "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
                )
            allowed_class_ids = attunement.get("allowed_class_ids", ())
            if (
                not isinstance(allowed_class_ids, (tuple, list))
                or any(
                    not isinstance(class_id, str) or not class_id
                    for class_id in allowed_class_ids
                )
                or len(allowed_class_ids) != len(set(allowed_class_ids))
            ):
                raise contracts.NativePreparationHold(
                    "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
                )
            if attunement["required"]:
                if native_source.get("attuned_actor_id") != subject_id:
                    source_is_target_local = False
                elif allowed_class_ids:
                    # This profile has no compiled class-prerequisite proof.
                    raise contracts.NativePreparationHold(
                        "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
                    )
        attunement = definition_data.get("attunement")
        if attunement is not None:
            if (
                not isinstance(attunement, Mapping)
                or set(attunement) - {"required", "allowed_class_ids"}
                or type(attunement.get("required")) is not bool
            ):
                raise contracts.NativePreparationHold(
                    "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
                )
            allowed_class_ids = attunement.get("allowed_class_ids", ())
            if (
                not isinstance(allowed_class_ids, (tuple, list))
                or any(
                    not isinstance(class_id, str) or not class_id
                    for class_id in allowed_class_ids
                )
                or len(allowed_class_ids) != len(set(allowed_class_ids))
            ):
                raise contracts.NativePreparationHold(
                    "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
                )
            if attunement["required"]:
                attunement_is_eligible = (
                    native_source.get("attuned_actor_id") == subject_id
                )
                if attunement_is_eligible and allowed_class_ids:
                    # This profile has no compiled prerequisite/class-membership
                    # proof. Never treat a declared restriction as decorative.
                    raise contracts.NativePreparationHold(
                        "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
                    )
                source_is_target_local = (
                    source_is_target_local and attunement_is_eligible
                )

    if operation_id == "rule.override":
        source_is_eligible = (
            source_is_target_local
            and owner_kind == "definition.effect"
            and owner_definition_id == _MAGE_ARMOR_DEFINITION_ID
            and rules_origin_id == _MAGE_ARMOR_RULES_ORIGIN_ID
        )
    else:
        source_is_eligible = source_is_target_local

    rejection_reasons: set[str] = set()
    if not predicate_result:
        rejection_reasons.add("PREDICATE_FALSE")
    if not source_is_eligible:
        rejection_reasons.add("SOURCE_NOT_ELIGIBLE")
    is_candidate = not rejection_reasons and operation_id == "rule.override"
    disposition = (
        "CANDIDATE"
        if is_candidate
        else "APPLIED"
        if not rejection_reasons
        else "REJECTED"
    )
    trace = {
        "operation_id": operation_id,
        "source_owner_ref": _plain(owner_ref),
        "owner_definition_id": owner_definition_id,
        "owner_kind": owner_kind,
        "owner_application_id": application_id,
        "rule_element_ordinal": ordinal,
        "source_id": source_id,
        "rules_origin_id": rules_origin_id,
        "value": _plain(value),
        "predicate": _plain(raw.get("predicate")),
        "predicate_source_present": raw.get("predicate") is not None,
        "predicate_result": predicate_result,
        "predicate_state": predicate_state,
        "source_eligibility": "ELIGIBLE" if source_is_eligible else "INELIGIBLE",
        "disposition": disposition,
        "rejection_reasons": [
            reason
            for reason in _ARMOR_CLASS_REJECTION_ORDER
            if reason in rejection_reasons
        ],
        "source_basis": source_basis,
        "fingerprint": fingerprint,
    }
    candidate = None
    if is_candidate:
        candidate = {
            "base_kind": "MAGE_ARMOR_13_PLUS_DEX",
            "base_value": 13 + dexterity_modifier,
            "source_owner_ref": _plain(owner_ref),
            "source_definition_id": owner_definition_id,
            "source_application_id": application_id,
            "rule_element_ordinal": ordinal,
            "source_id": source_id,
            "rules_origin_id": rules_origin_id,
            "source_basis": source_basis,
            "fingerprint": fingerprint,
        }
    return trace, candidate


def _issued_damage_input_binding(
    context: contracts.NativePreparationContext,
) -> contracts.CompiledDamageInputBinding:
    matches = tuple(
        binding
        for binding in context.compiled.damage_input_bindings
        if binding.consumer_id == context.consumer_id
    )
    if len(matches) != 1:
        raise CalculationError(
            "issued damage consumer does not retain one exact source input binding"
        )
    binding = matches[0]
    if (
        type(binding) is not contracts.CompiledDamageInputBinding
        or binding.profile_id != DAMAGE_POLICY_ID
        or binding.profile_generation != DAMAGE_POLICY_GENERATION
        or binding.selector_id != DAMAGE_SELECTOR_ID
    ):
        raise CalculationError("issued damage input binding is not the selected profile")
    return binding


def _issued_damage_policy(
    context: contracts.NativePreparationContext,
    input_binding: contracts.CompiledDamageInputBinding,
) -> contracts.CompiledCalculationPolicy:
    matches = tuple(
        policy
        for policy in context.compiled.calculation_policy_bindings
        if policy.binding.consumer_id == context.consumer_id
        and policy.binding.profile_id == DAMAGE_POLICY_ID
        and policy.binding.profile_generation == DAMAGE_POLICY_GENERATION
    )
    if len(matches) != 1:
        raise CalculationError("issued consumer does not retain one exact damage policy")
    policy = matches[0]
    pairs = policy.binding.selector_operation_pairs
    if (
        len(pairs) != 1
        or pairs[0].selector_id != DAMAGE_SELECTOR_ID
        or set(pairs[0].operation_ids) != set(DAMAGE_OPERATION_TYPES)
        or len(pairs[0].operation_ids) != len(DAMAGE_OPERATION_TYPES)
        or policy.binding.reads != (f"selector:{DAMAGE_SELECTOR_ID}",)
        or policy.binding.context_fact_bindings
        or policy.context_fact_contracts
        or policy.dependency_read_refs
        or policy.binding.native_role_bindings
        != (
            contracts.NativeRoleBinding(
                f"selector:{DAMAGE_SELECTOR_ID}",
                (input_binding.recipient_role,),
            ),
        )
    ):
        raise CalculationError("issued damage pair/fact/role closure is incomplete")
    selector = policy.selector_contracts.get(DAMAGE_SELECTOR_ID)
    if not isinstance(selector, Mapping) or (
        selector.get("calculation_policy_id") != DAMAGE_POLICY_ID
        or selector.get("calculation_policy_generation") != DAMAGE_POLICY_GENERATION
        or selector.get("contribution_type") != "damage_defense"
        or selector.get("result_type") != "damage_result"
        or selector.get("result_constraints") != {"minimum": 0}
        or selector.get("combination_policy") != DAMAGE_COMBINATION_POLICY
        or selector.get("resolution_owner") != "SELECTOR_METADATA"
        or selector.get("trace_policy") != "RETAIN_ACCEPTED_REJECTED_PROVENANCE"
        or selector.get("allowed_input_classes") != ("ENGINE_STATE",)
        or selector.get("permitted_context_fact_ids") != ()
        or selector.get("static_dependencies") != ()
        or set(selector.get("allowed_operations", ())) != set(DAMAGE_OPERATION_TYPES)
    ):
        raise CalculationError("issued damage selector is not the exact selected profile")
    operation_contracts = selector.get("operation_contracts")
    if not isinstance(operation_contracts, Mapping) or set(operation_contracts) != set(
        DAMAGE_OPERATION_TYPES
    ):
        raise CalculationError("issued damage operation contracts are incomplete")
    required_constraints = frozenset(
        {"damage_type_origin_bypass_order_and_rounding"}
    )
    for operation_id, contribution_type in DAMAGE_OPERATION_TYPES.items():
        operation = operation_contracts.get(operation_id)
        if not isinstance(operation, Mapping):
            raise CalculationError(f"issued damage pair is missing {operation_id}")
        constraints = operation.get("constraints")
        if (
            operation.get("damage_contribution_type") != contribution_type
            or operation.get("value_kind") != "damage_defense"
            or operation.get("normalization") != "SOURCE_DEFINED_ORDER"
            or operation.get("calculation_policy_id") != DAMAGE_POLICY_ID
            or operation.get("calculation_policy_generation")
            != DAMAGE_POLICY_GENERATION
            or not isinstance(constraints, (tuple, list))
            or frozenset(constraints) != required_constraints
        ):
            raise CalculationError(
                f"issued damage operation contract is not exact: {operation_id}"
            )
    return policy


def _source_damage_components(
    context: contracts.NativePreparationContext,
    binding: contracts.CompiledDamageInputBinding,
) -> tuple[tuple[dict[str, object], ...], dict[str, object]]:
    instruction = _compiled_instruction_for_consumer(
        context.compiled.instructions, binding.consumer_id
    )
    if (
        instruction is None
        or instruction.primitive_id != "op.apply_damage"
        or instruction.arguments.get("components")
        != {
            "symbol_ref": binding.components_symbol_id,
            "value_kind": "damage_components",
        }
        or instruction.arguments.get("target_role") != binding.recipient_role
    ):
        raise CalculationError(
            "issued damage input no longer matches its exact compiled primitive binding"
        )
    for role_name in (binding.source_role, binding.recipient_role):
        owner_ref = context.role_bindings.get(role_name)
        if (
            type(owner_ref) is not NativeOwnerRef
            or owner_ref.family_key != "world.actor"
            or len(owner_ref.identity) != 1
        ):
            raise CalculationError(
                f"damage source/recipient role has no exact Actor owner: {role_name}"
            )
        owner_read = context.observation.require(owner_ref)
        if owner_read.status.value != "RESOLVED" or owner_read.payload is None:
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
            )
    descriptor = context.compiled.symbol_contracts.get(binding.components_symbol_id)
    permitted_occurrences = (
        descriptor.get("permitted_occurrence_ids", ())
        if isinstance(descriptor, Mapping)
        else ()
    )
    if (
        not isinstance(descriptor, Mapping)
        or descriptor.get("value_kind") != "damage_components"
        or descriptor.get("cardinality") != "single"
        or descriptor.get("scope") is not None
        or not isinstance(permitted_occurrences, (tuple, list))
        or binding.consumer_id not in permitted_occurrences
        or descriptor.get("reads") not in ((), [])
    ):
        raise CalculationError("frozen damage symbol differs from its exact source binding")

    if "value" in descriptor and "template" not in descriptor:
        if descriptor.get("dependencies") not in ((), []):
            raise CalculationError("literal damage symbol has an undeclared dependency")
        try:
            structural_contracts.validate_contract(
                "typed_export_value",
                {"value_kind": "damage_components", "value": descriptor["value"]},
            )
        except structural_contracts.StructuralContractError as error:
            raise CalculationError(
                "frozen literal damage components are malformed"
            ) from error
        components = _assemble_bound_damage_components(
            context, descriptor["value"], binding.component_annotations
        )
        amount_basis = {
            "kind": "SOURCE_LITERAL",
            "symbol_id": binding.components_symbol_id,
            "dependency_symbol_ids": [],
        }
    elif "template" in descriptor and "value" not in descriptor:
        template = descriptor.get("template")
        if (
            not isinstance(template, Mapping)
            or set(template) != {"kind", "source_symbol", "input_contract"}
            or template.get("kind") != "HALF_DAMAGE_FLOOR_MIN_ZERO"
            or template.get("input_contract") != "SAME_FIXED_FULL_DAMAGE_RESULT"
        ):
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
            )
        source_symbol_id = template.get("source_symbol")
        source_descriptor = (
            context.compiled.symbol_contracts.get(source_symbol_id)
            if isinstance(source_symbol_id, str)
            else None
        )
        if (
            not isinstance(source_symbol_id, str)
            or descriptor.get("dependencies") not in ((source_symbol_id,), [source_symbol_id])
            or not isinstance(source_descriptor, Mapping)
            or source_descriptor.get("value_kind") != "damage_components"
            or source_descriptor.get("cardinality") != "single"
            or "value" not in source_descriptor
            or "template" in source_descriptor
            or source_descriptor.get("dependencies") not in ((), [])
            or source_descriptor.get("reads") not in ((), [])
            or source_descriptor.get("scope") is not None
            or not isinstance(
                source_descriptor.get("permitted_occurrence_ids"), (tuple, list)
            )
            or binding.consumer_id
            not in source_descriptor.get("permitted_occurrence_ids", ())
        ):
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
            )
        try:
            structural_contracts.validate_contract(
                "typed_export_value",
                {
                    "value_kind": "damage_components",
                    "value": source_descriptor["value"],
                },
            )
        except structural_contracts.StructuralContractError as error:
            raise CalculationError(
                "half-damage source components are malformed"
            ) from error
        full_components = _assemble_bound_damage_components(
            context, source_descriptor["value"], binding.component_annotations
        )
        components = tuple(
            {
                **component,
                "amount": max(0, component["amount"] // 2),
            }
            for component in full_components
        )
        amount_basis = {
            "kind": "HALF_DAMAGE_FLOOR_MIN_ZERO",
            "symbol_id": binding.components_symbol_id,
            "source_symbol_id": source_symbol_id,
            "dependency_symbol_ids": [source_symbol_id],
        }
    else:
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        )

    _validate_damage_components(context, components)
    try:
        structural_contracts.validate_contract(
            "damage_defense_input_components", components
        )
    except structural_contracts.StructuralContractError as error:
        raise CalculationError("derived damage components are malformed") from error
    return tuple(components), amount_basis


def _assemble_bound_damage_components(
    context: contracts.NativePreparationContext,
    legacy_components: object,
    annotations: tuple[contracts.CompiledDamageComponentAnnotation, ...],
) -> tuple[dict[str, object], ...]:
    if not isinstance(legacy_components, (tuple, list)) or not legacy_components:
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        )
    if len(legacy_components) != len(annotations) or tuple(
        annotation.source_component_ordinal for annotation in annotations
    ) != tuple(range(len(legacy_components))):
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        )

    typed_components: list[dict[str, object]] = []
    for legacy_component, annotation in zip(
        legacy_components, annotations, strict=True
    ):
        if not isinstance(legacy_component, Mapping) or set(legacy_component) != {
            "amount",
            "damage_type_ref",
        }:
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
            )
        typed_components.append(
            {
                "amount": legacy_component["amount"],
                "damage_type_id": legacy_component["damage_type_ref"],
                "origin_id": annotation.origin_id,
                "bypass_ids": annotation.bypass_ids,
            }
        )
    return tuple(typed_components)


def _compiled_instruction_for_consumer(
    instructions: Sequence[contracts.CompiledInstruction], consumer_id: str
) -> contracts.CompiledInstruction | None:
    pending = list(instructions)
    matches: list[contracts.CompiledInstruction] = []
    while pending:
        instruction = pending.pop()
        if instruction.consumer_id == consumer_id:
            matches.append(instruction)
        pending.extend(instruction.children)
    return matches[0] if len(matches) == 1 else None


def _validate_damage_components(
    context: contracts.NativePreparationContext,
    value: object,
) -> None:
    if not isinstance(value, (tuple, list)) or not value:
        raise CalculationError("damage input must be a nonempty typed component sequence")
    required_members = {"amount", "damage_type_id", "origin_id", "bypass_ids"}
    seen_partitions: set[tuple[str, str, tuple[str, ...]]] = set()
    for component in value:
        if not isinstance(component, Mapping) or set(component) != required_members:
            raise CalculationError("damage component members are not closed")
        amount = component.get("amount")
        damage_type_id = component.get("damage_type_id")
        origin_id = component.get("origin_id")
        bypass_ids = component.get("bypass_ids")
        if (
            type(amount) is not int
            or amount < 0
            or not isinstance(damage_type_id, str)
            or not damage_type_id
            or not isinstance(origin_id, str)
            or not origin_id
            or not isinstance(bypass_ids, (tuple, list))
            or any(not isinstance(item, str) or not item for item in bypass_ids)
            or len(bypass_ids) != len(set(bypass_ids))
        ):
            raise CalculationError("damage component value is not a finite typed source value")
        partition = (damage_type_id, origin_id, tuple(sorted(bypass_ids)))
        if partition in seen_partitions:
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
            )
        seen_partitions.add(partition)


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


def _normalize_damage_policy(
    context: contracts.NativePreparationContext,
    binding: contracts.CompiledDamageInputBinding,
    policy: contracts.CompiledCalculationPolicy,
    components: tuple[dict[str, object], ...],
    amount_basis: Mapping[str, object],
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
        raise CalculationError("raw damage evaluation is not a closed selector result")
    if (
        raw_evaluation.get("selector_id") != DAMAGE_SELECTOR_ID
        or raw_evaluation.get("consumer_id") != context.consumer_id
        or raw_evaluation.get("calculation_policy_id") != DAMAGE_POLICY_ID
        or raw_evaluation.get("calculation_policy_generation")
        != DAMAGE_POLICY_GENERATION
        or raw_evaluation.get("context_facts") not in ([], ())
    ):
        raise CalculationError("raw damage result differs from the issued policy")
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
        raise CalculationError("raw damage selector node is not a closed contribution set")
    operation_ids = selector_result.get("operation_ids", ())
    dependencies = selector_result.get("dependencies")
    if (
        selector_result.get("node_ref") != f"selector:{DAMAGE_SELECTOR_ID}"
        or selector_result.get("value_type") != "damage_result"
        or selector_result.get("contribution_type") != "damage_defense"
        or selector_result.get("combination_policy") != DAMAGE_COMBINATION_POLICY
        or selector_result.get("policy_id") != DAMAGE_POLICY_ID
        or selector_result.get("resolution_owner") != "SELECTOR_METADATA"
        or selector_result.get("trace_policy") != "RETAIN_ACCEPTED_REJECTED_PROVENANCE"
        or not isinstance(operation_ids, (tuple, list))
        or len(operation_ids) != len(DAMAGE_OPERATION_TYPES)
        or set(operation_ids) != set(DAMAGE_OPERATION_TYPES)
        or not isinstance(dependencies, Mapping)
        or dependencies
        or "value" in selector_result
    ):
        raise CalculationError("raw damage selector violates the selected profile")

    native_membership = raw_evaluation.get("native_membership")
    provenance = raw_evaluation.get("provenance")
    if not isinstance(native_membership, Mapping) or not isinstance(provenance, Mapping):
        raise CalculationError("damage source membership/provenance is unavailable")
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
        raise CalculationError("damage membership evidence is not the closed source proof")
    if set(provenance) != {
        "activity_id",
        "consumer_id",
        "occurrence_id",
        "command_id",
        "resolution_id",
        "definition_semantic_hash",
        "compiler_generation",
        "catalog_context_fingerprint",
        "role_bindings",
        "accepted_fact_refs",
        "policy_refs",
        "observation_fingerprint",
        "source_revision",
        "source_tree_sha",
    }:
        raise CalculationError("damage provenance fields are not closed")
    source_revision = native_membership.get("source_revision")
    source_tree_sha = native_membership.get("source_tree_sha")
    observation_fingerprint = provenance.get("observation_fingerprint")
    if not all(
        isinstance(value, str) and value
        for value in (source_revision, source_tree_sha, observation_fingerprint)
    ):
        raise CalculationError("damage source observation identity is incomplete")
    if (
        source_revision != provenance.get("source_revision")
        or source_tree_sha != provenance.get("source_tree_sha")
        or provenance.get("activity_id") != context.compiled.activity_id
        or provenance.get("consumer_id") != context.consumer_id
        or provenance.get("occurrence_id") != context.occurrence_id
        or provenance.get("command_id") != context.execution_ref.command_id
        or provenance.get("resolution_id") != context.execution_ref.resolution_id
        or provenance.get("definition_semantic_hash")
        != context.compiled.definition_semantic_hash
        or provenance.get("compiler_generation") != context.compiled.compiler_generation
        or provenance.get("catalog_context_fingerprint")
        != context.compiled.catalog_context_fingerprint
        or provenance.get("accepted_fact_refs") != list(context.accepted_fact_refs)
        or provenance.get("policy_refs") != list(context.policy_refs)
    ):
        raise CalculationError("damage provenance identity differs across its source join")

    raw_contributions = selector_result.get("raw_contributions")
    if not isinstance(raw_contributions, (tuple, list)):
        raise CalculationError("raw damage contributions are not an ordered source sequence")
    effect_evidence = _membership_evidence_by_application(
        native_membership.get("effects"), "world.effect"
    )
    asset_evidence = _membership_evidence_by_application(
        native_membership.get("assets"), "world.asset"
    )
    selector_metadata = policy.selector_contracts.get(DAMAGE_SELECTOR_ID)
    operation_contracts = (
        selector_metadata.get("operation_contracts")
        if isinstance(selector_metadata, Mapping)
        else None
    )
    if not isinstance(operation_contracts, Mapping) or set(operation_contracts) != set(
        DAMAGE_OPERATION_TYPES
    ):
        raise CalculationError("compiled damage operation metadata is unavailable")
    recipient = context.role_bindings.get(binding.recipient_role)
    source = context.role_bindings.get(binding.source_role)
    if (
        type(recipient) is not NativeOwnerRef
        or recipient.family_key != "world.actor"
        or len(recipient.identity) != 1
        or type(source) is not NativeOwnerRef
        or source.family_key != "world.actor"
        or len(source.identity) != 1
    ):
        raise CalculationError("damage source/recipient roles are not exact Actor refs")
    root_roles = provenance.get("role_bindings")
    expected_root_roles = {
        role_name: _owner_ref_wire(owner_ref)
        for role_name, owner_ref in sorted(context.role_bindings.items())
        if type(owner_ref) is NativeOwnerRef
    }
    if not isinstance(root_roles, Mapping) or not _same_value(
        root_roles, expected_root_roles
    ) or (
        root_roles.get(binding.source_role) != _owner_ref_wire(source)
        or root_roles.get(binding.recipient_role) != _owner_ref_wire(recipient)
    ):
        raise CalculationError("damage role provenance differs from its issued context")

    contributions: list[dict[str, object]] = []
    seen_sources: set[tuple[object, ...]] = set()
    for component_index, component in enumerate(components):
        for raw in raw_contributions:
            row = _normalize_damage_contribution(
                context,
                component_index,
                component,
                raw,
                recipient.identity[0],
                effect_evidence,
                asset_evidence,
                operation_contracts,
            )
            source_ref = row["source_owner_ref"]
            if not isinstance(source_ref, Mapping):
                raise CalculationError("damage contribution source identity is malformed")
            identity = source_ref.get("identity")
            if not isinstance(identity, (tuple, list)):
                raise CalculationError("damage contribution source identity is malformed")
            source_key = (
                component_index,
                source_ref.get("family_key"),
                tuple(identity),
                row["owner_application_id"],
                row["rule_element_ordinal"],
                row["operation_id"],
            )
            if source_key in seen_sources:
                raise CalculationError("damage source repeated one Rule Element contribution")
            seen_sources.add(source_key)
            contributions.append(row)
    contributions.sort(key=_damage_contribution_sort_key)
    component_results, total_damage = _apply_damage_stages(components, contributions)

    read_refs = raw_evaluation.get("read_refs")
    if (
        not isinstance(read_refs, (tuple, list))
        or any(not isinstance(reference, str) for reference in read_refs)
        or set(read_refs) != {f"selector:{DAMAGE_SELECTOR_ID}"}
    ):
        raise CalculationError("damage policy reads differ from its exact empty-fact profile")
    fixed_roll_results = context.resolution.get("fixed_rng_results")
    if not isinstance(fixed_roll_results, (tuple, list)):
        raise CalculationError("damage fixed-roll evidence is not a closed sequence")
    if context.fixed_roll_refs or fixed_roll_results:
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        )

    return {
        "selector_id": DAMAGE_SELECTOR_ID,
        "consumer_id": context.consumer_id,
        "profile_id": DAMAGE_POLICY_ID,
        "profile_generation": DAMAGE_POLICY_GENERATION,
        "activity_id": context.compiled.activity_id,
        "occurrence_id": context.occurrence_id,
        "execution_ref": _execution_ref_wire(context.execution_ref),
        "compiled_policy": _compiled_policy_wire(policy),
        "read_refs": list(read_refs),
        "context_facts": [],
        "input_binding": _damage_input_binding_wire(binding),
        "input_roles": {
            "source_role": binding.source_role,
            "source_owner_ref": _owner_ref_wire(source),
            "recipient_role": binding.recipient_role,
            "recipient_owner_ref": _owner_ref_wire(recipient),
        },
        "logical_identity": {
            "kind": "LOGICAL_PREPARATION_ONLY",
            "execution_ref": _execution_ref_wire(context.execution_ref),
            "activity_id": context.compiled.activity_id,
            "consumer_id": binding.consumer_id,
            "binding_id": binding.binding_id,
            "instance_key": binding.instance_key,
            "simultaneous_group_key": binding.simultaneous_group_key,
        },
        "amount_basis": _plain(amount_basis),
        "components": _plain(components),
        "component_results": component_results,
        "total_damage": total_damage,
        "fixed_roll_refs": [],
        "rng_draw_count": 0,
        "trace": {
            "stage_order": list(_DAMAGE_STAGE_ORDER),
            "contributions": contributions,
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


def _normalize_damage_contribution(
    context: contracts.NativePreparationContext,
    component_index: int,
    component: Mapping[str, object],
    raw: object,
    recipient_actor_id: str,
    effect_evidence: Mapping[str, Mapping[str, object]],
    asset_evidence: Mapping[str, Mapping[str, object]],
    expected_operation_contracts: Mapping[str, object],
) -> dict[str, object]:
    if not isinstance(raw, Mapping) or set(raw) != {
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
    }:
        raise CalculationError("raw damage contribution provenance is not closed")
    operation_id = raw.get("operation_id")
    if not isinstance(operation_id, str) or operation_id not in DAMAGE_OPERATION_TYPES:
        raise CalculationError("raw damage operation is outside the exact selected pair")
    contribution_type = DAMAGE_OPERATION_TYPES[operation_id]
    operation = raw.get("operation_contract")
    expected_operation = expected_operation_contracts.get(operation_id)
    if not isinstance(operation, Mapping) or not isinstance(expected_operation, Mapping):
        raise CalculationError("damage operation contract is unavailable")
    constraints = operation.get("constraints")
    if (
        raw.get("value_kind") != "damage_defense"
        or not _same_value(operation, expected_operation)
        or operation.get("damage_contribution_type") != contribution_type
        or operation.get("value_kind") != "damage_defense"
        or operation.get("normalization") != "SOURCE_DEFINED_ORDER"
        or operation.get("calculation_policy_id") != DAMAGE_POLICY_ID
        or operation.get("calculation_policy_generation") != DAMAGE_POLICY_GENERATION
        or not isinstance(constraints, (tuple, list))
        or frozenset(constraints)
        != frozenset({"damage_type_origin_bypass_order_and_rounding"})
    ):
        raise CalculationError(f"raw damage operation contract is not exact: {operation_id}")
    value = raw.get("value")
    value_contract = (
        "damage_defense_adjustment"
        if contribution_type == "ADJUSTMENT"
        else "damage_defense_match"
    )
    try:
        structural_contracts.validate_contract(value_contract, value)
    except structural_contracts.StructuralContractError as error:
        raise CalculationError(
            f"raw damage Rule Element value is not closed: {operation_id}"
        ) from error
    if not isinstance(value, Mapping):
        raise CalculationError("damage Rule Element value is not an exact object")

    rule_element = raw.get("rule_element")
    if not isinstance(rule_element, Mapping):
        raise CalculationError("damage Rule Element source is unavailable")
    unsupported = _UNSUPPORTED_DAMAGE_ELEMENT_MEMBERS.intersection(rule_element)
    if unsupported:
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        )
    unknown_members = set(rule_element) - {"selector", "operation_id", "value", "predicate"}
    if unknown_members:
        raise CalculationError(
            "damage Rule Element has unknown members: "
            + ",".join(sorted(unknown_members))
        )
    if (
        rule_element.get("selector") != DAMAGE_SELECTOR_ID
        or rule_element.get("operation_id") != operation_id
        or not _same_value(rule_element.get("value"), value)
        or not _same_value(raw.get("predicate"), rule_element.get("predicate"))
    ):
        raise CalculationError("damage Rule Element differs from its typed contribution")

    predicate_result = raw.get("predicate_result")
    predicate_state = raw.get("predicate_state")
    if type(predicate_result) is not bool or predicate_state not in {"TRUE", "FALSE"}:
        raise CalculationError("damage predicate result/state is not a closed boolean")
    if predicate_result is not (predicate_state == "TRUE"):
        raise CalculationError("damage predicate state/result disagree")

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
        raise CalculationError("damage source identity is malformed")
    family_key = "world.effect" if owner_kind == "definition.effect" else "world.asset"
    identity = owner_ref.get("identity")
    if (
        owner_ref.get("family_key") != family_key
        or not isinstance(identity, (tuple, list))
        or len(identity) != 1
        or identity[0] != owner_application_id
    ):
        raise CalculationError("damage source is not bound to its exact native application")
    definition = context.catalog.frozen_definitions.get(owner_definition_id)
    if (
        not isinstance(definition, Mapping)
        or definition.get("id") != owner_definition_id
        or definition.get("kind") != owner_kind
    ):
        raise CalculationError("damage source definition is outside the frozen catalog")
    definition_data = definition.get("data")
    elements = definition_data.get("rule_elements") if isinstance(definition_data, Mapping) else None
    if (
        not isinstance(elements, (tuple, list))
        or ordinal >= len(elements)
        or not isinstance(elements[ordinal], Mapping)
        or not _same_value(elements[ordinal], rule_element)
    ):
        raise CalculationError("damage Rule Element differs from its frozen source definition")

    native_source: Mapping[str, object]
    if owner_kind == "definition.effect":
        native_source = effect_evidence.get(owner_application_id, {})
        if not native_source or not _same_value(native_source.get("owner_ref"), owner_ref):
            raise CalculationError("damage Effect lacks exact native membership evidence")
        source_eligible = (
            native_source.get("lifecycle") == "effect_lifecycle.active"
            and native_source.get("is_target_local") is True
            and native_source.get("target_id") == recipient_actor_id
        )
    else:
        native_source = asset_evidence.get(owner_application_id, {})
        if not native_source or not _same_value(native_source.get("owner_ref"), owner_ref):
            raise CalculationError("damage Asset lacks exact native membership evidence")
        source_eligible = (
            native_source.get("accessible") is True
            and native_source.get("equipment_mode") in {"held", "worn"}
            and native_source.get("placement_owner_id") == recipient_actor_id
        )

    reasons: set[str] = set()
    if not predicate_result:
        reasons.add("PREDICATE_FALSE")
    if not source_eligible:
        reasons.add("SOURCE_NOT_ELIGIBLE")
    damage_type_ids = value.get("damage_type_ids")
    origin_ids = value.get("origin_ids")
    if not isinstance(damage_type_ids, (tuple, list)) or component.get(
        "damage_type_id"
    ) not in damage_type_ids:
        reasons.add("DAMAGE_TYPE_MISMATCH")
    if not isinstance(origin_ids, (tuple, list)) or component.get("origin_id") not in origin_ids:
        reasons.add("ORIGIN_MISMATCH")
    bypass_ids = component.get("bypass_ids")
    if not isinstance(bypass_ids, (tuple, list)):
        raise CalculationError("damage bypass identities are malformed")
    if value.get("bypass_id") in bypass_ids:
        reasons.add("BYPASSED_BY_COMPONENT")
    if reasons == {"BYPASSED_BY_COMPONENT"}:
        disposition = "BYPASSED"
    elif reasons:
        disposition = "REJECTED"
    else:
        disposition = "APPLIED"
    return {
        "component_index": component_index,
        "stage_id": contribution_type,
        "contribution_type": contribution_type,
        "operation_id": operation_id,
        "source_owner_ref": _plain(owner_ref),
        "owner_definition_id": owner_definition_id,
        "owner_kind": owner_kind,
        "owner_application_id": owner_application_id,
        "rule_element_ordinal": ordinal,
        "value": _plain(value),
        "predicate": _plain(raw.get("predicate")),
        "predicate_source_present": raw.get("predicate") is not None,
        "predicate_result": predicate_result,
        "predicate_state": predicate_state,
        "source_eligibility": "ELIGIBLE" if source_eligible else "INELIGIBLE",
        "disposition": disposition,
        "rejection_reasons": [
            reason for reason in _DAMAGE_REJECTION_ORDER if reason in reasons
        ],
    }


def _damage_contribution_sort_key(row: Mapping[str, object]) -> tuple[object, ...]:
    owner_ref = row.get("source_owner_ref")
    if not isinstance(owner_ref, Mapping):
        raise CalculationError("damage contribution owner reference is malformed")
    identity = owner_ref.get("identity")
    if not isinstance(identity, (tuple, list)):
        raise CalculationError("damage contribution identity is malformed")
    return (
        row.get("component_index", -1),
        owner_ref.get("family_key", ""),
        tuple(str(item) for item in identity),
        row.get("owner_application_id", ""),
        row.get("rule_element_ordinal", -1),
        row.get("operation_id", ""),
    )


def _apply_damage_stages(
    components: tuple[dict[str, object], ...],
    contributions: list[dict[str, object]],
) -> tuple[list[dict[str, object]], int]:
    trace_indices_by_component: dict[int, list[int]] = {}
    for trace_index, contribution in enumerate(contributions):
        component_index = contribution["component_index"]
        if type(component_index) is not int:
            raise CalculationError("damage trace component index is malformed")
        trace_indices_by_component.setdefault(component_index, []).append(trace_index)

    results: list[dict[str, object]] = []
    total_damage = 0
    for component_index, component in enumerate(components):
        raw_amount = component.get("amount")
        if type(raw_amount) is not int or raw_amount < 0:
            raise CalculationError("damage amount is not a nonnegative integer")
        rows = trace_indices_by_component.get(component_index, [])
        adjustment_rows = [
            index
            for index in rows
            if contributions[index]["contribution_type"] == "ADJUSTMENT"
            and contributions[index]["disposition"] == "APPLIED"
        ]
        adjustment_amounts: list[int] = []
        for index in adjustment_rows:
            adjustment_value = contributions[index].get("value")
            amount = (
                adjustment_value.get("amount")
                if isinstance(adjustment_value, Mapping)
                else None
            )
            if type(amount) is not int:
                raise CalculationError("damage adjustment is not an exact integer")
            adjustment_amounts.append(amount)
        adjustment_delta = sum(adjustment_amounts)
        adjusted = max(0, raw_amount + adjustment_delta)
        stages: list[dict[str, object]] = [
            {
                "stage_id": "ADJUSTMENT",
                "input_amount": raw_amount,
                "output_amount": adjusted,
                "contribution_ordinals": adjustment_rows,
                "applied": bool(adjustment_rows),
                "adjustment_delta": adjustment_delta,
            }
        ]

        after_resistance = adjusted
        resistance_rows = [
            index
            for index in rows
            if contributions[index]["contribution_type"] == "RESISTANCE"
            and contributions[index]["disposition"] == "APPLIED"
        ]
        if resistance_rows:
            for duplicate_index in resistance_rows[1:]:
                contributions[duplicate_index]["disposition"] = "COALESCED_DUPLICATE"
            after_resistance = adjusted // 2
        stages.append(
            {
                "stage_id": "RESISTANCE",
                "input_amount": adjusted,
                "output_amount": after_resistance,
                "contribution_ordinals": resistance_rows,
                "applied": bool(resistance_rows),
                "adjustment_delta": 0,
            }
        )

        after_vulnerability = after_resistance
        vulnerability_rows = [
            index
            for index in rows
            if contributions[index]["contribution_type"] == "VULNERABILITY"
            and contributions[index]["disposition"] == "APPLIED"
        ]
        if vulnerability_rows:
            for duplicate_index in vulnerability_rows[1:]:
                contributions[duplicate_index]["disposition"] = "COALESCED_DUPLICATE"
            after_vulnerability = after_resistance * 2
        stages.append(
            {
                "stage_id": "VULNERABILITY",
                "input_amount": after_resistance,
                "output_amount": after_vulnerability,
                "contribution_ordinals": vulnerability_rows,
                "applied": bool(vulnerability_rows),
                "adjustment_delta": 0,
            }
        )

        immunity_rows = [
            index
            for index in rows
            if contributions[index]["contribution_type"] == "IMMUNITY"
            and contributions[index]["disposition"] == "APPLIED"
        ]
        if immunity_rows:
            for duplicate_index in immunity_rows[1:]:
                contributions[duplicate_index]["disposition"] = "COALESCED_DUPLICATE"
            received = 0
        else:
            received = after_vulnerability
        stages.append(
            {
                "stage_id": "IMMUNITY",
                "input_amount": after_vulnerability,
                "output_amount": received,
                "contribution_ordinals": immunity_rows,
                "applied": bool(immunity_rows),
                "adjustment_delta": 0,
            }
        )
        total_damage += received
        results.append(
            {
                "component_index": component_index,
                "component": _plain(component),
                "stages": stages,
                "received_amount": received,
            }
        )
    return results, total_damage


def _damage_input_binding_wire(
    binding: contracts.CompiledDamageInputBinding,
) -> dict[str, object]:
    wire = {
        "binding_id": binding.binding_id,
        "consumer_id": binding.consumer_id,
        "profile_id": binding.profile_id,
        "profile_generation": binding.profile_generation,
        "selector_id": binding.selector_id,
        "components_symbol_id": binding.components_symbol_id,
        "component_annotations": [
            {
                "source_component_ordinal": annotation.source_component_ordinal,
                "origin_id": annotation.origin_id,
                "bypass_ids": list(annotation.bypass_ids),
            }
            for annotation in binding.component_annotations
        ],
        "source_role": binding.source_role,
        "recipient_role": binding.recipient_role,
        "instance_key": binding.instance_key,
        "simultaneous_group_key": binding.simultaneous_group_key,
    }
    return wire


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


def _armor_class_contribution_sort_key(
    row: Mapping[str, object],
) -> tuple[object, ...]:
    owner_ref = row.get("source_owner_ref")
    if not isinstance(owner_ref, Mapping):
        raise CalculationError("normalized Armor Class source identity is malformed")
    identity = owner_ref.get("identity")
    if not isinstance(identity, (tuple, list)):
        raise CalculationError("normalized Armor Class source identity is malformed")
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
    binding_wire: dict[str, object] = {
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
    }
    if binding.native_base_descriptor is not None:
        descriptor = binding.native_base_descriptor
        binding_wire["native_base_descriptor"] = {
            "kind": descriptor.kind,
            "ability_id": descriptor.ability_id,
            "subject_role": descriptor.subject_role,
        }
    return {
        "binding": binding_wire,
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
