"""Installed-source conformance for the bounded SP03 roll calculation."""

from __future__ import annotations

import json
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

pytest_plugins = ("DEV.TESTS.test_local_spell_catalog",)

ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ID = "hdm.rules.dnd2024-srd52-core"
PROFILE_ID = "calculation.roll_advantage_srd521"
ROLL_OPERATIONS = (
    "rule.add_flat",
    "rule.grant_advantage",
    "rule.grant_disadvantage",
)
from DEV.TESTS import test_sp03_policy_carriers as _policy_carrier_tests

_BASE_SOURCE_COMPILER_FIXTURE = _policy_carrier_tests._installed_source_compiler_fixture


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def _install_roll_conformance_pair(
    source_root: Path,
    installed_template: Path,
    destination: Path,
    base_installer: Callable[[Path, Path, Path], Path],
    *,
    bad_constraint: bool = False,
    bad_fact: bool = False,
    bad_flat_payload: bool = False,
    bad_state_payload: str | None = None,
    bad_unknown_member: bool = False,
    bad_optional_member: str | None = None,
    permuted: bool = False,
) -> Path:
    """Stage the registered opposite pair only in the isolated source tree."""
    import copy

    primitive_root = source_root / "DEV/CATALOG/activity-primitive-contracts/primitives"
    roll_path = primitive_root / "op.roll.json"
    roll = json.loads(roll_path.read_text(encoding="utf-8"))
    activity_id = "activity.conformance.compiler"
    declaration = roll["contract"]["compiler_declarations"][activity_id]
    for policy in declaration["calculation_policies"]:
        pair = next(
            item
            for item in policy["selector_operation_pairs"]
            if item["selector_id"] == "attack.roll"
        )
        pair["operation_ids"] = list(ROLL_OPERATIONS)
        if bad_fact:
            policy["reads"].append("fact:fiction.target_reachable")
            policy["context_fact_bindings"] = [
                {
                    "consumer_ref": "selector:attack.roll",
                    "fact_ids": ["fiction.target_reachable"],
                }
            ]
    _write_json(roll_path, roll)

    mechanical_path = source_root / "DEV/CATALOG/mechanical-surfaces.json"
    mechanical = json.loads(mechanical_path.read_text(encoding="utf-8"))
    selector = mechanical["selectors"]["attack.roll"]
    selector["allowed_operations"] = list(ROLL_OPERATIONS)
    selector["operation_contracts"]["rule.add_flat"]["roll_contribution_type"] = (
        "FLAT_MODIFIER"
    )
    selector["operation_contracts"]["rule.grant_advantage"][
        "roll_contribution_type"
    ] = "ADVANTAGE"
    selector["operation_contracts"]["rule.grant_disadvantage"] = {
        "value_kind": "roll_modifier",
        "fixed_value": True,
        "normalization": "CANCEL_APPLICABLE_OPPOSITES",
        "constraints": [
            "literal_true",
            "effect.innate_sorcery_source_only",
            "bound_activity_family.activity.spell_attack_only",
            "stable_raw_dice_identity_and_contribution_provenance",
        ],
        "calculation_policy_id": PROFILE_ID,
        "calculation_policy_generation": 1,
        "roll_contribution_type": "DISADVANTAGE",
    }
    if bad_constraint:
        selector["operation_contracts"]["rule.grant_advantage"]["constraints"] = [
            "literal_true",
            "stable_raw_dice_identity_and_contribution_provenance",
        ]
    if bad_fact:
        selector["allowed_input_classes"] = [
            "ENGINE_STATE",
            "INVOCATION_ADJUDICATED",
        ]
        selector["permitted_context_fact_ids"] = ["fiction.target_reachable"]
        fact = mechanical["context_facts"]["fiction.target_reachable"]
        if activity_id not in fact["permitted_consumer_ids"]:
            fact["permitted_consumer_ids"].append(activity_id)
    _write_json(mechanical_path, mechanical)

    operation_ledger_path = (
        source_root
        / "DEV/CATALOG/catalog-admission-ledger/families/rule_operations.json"
    )
    operation_ledger = json.loads(operation_ledger_path.read_text(encoding="utf-8"))
    disadvantage = next(
        row
        for row in operation_ledger["entries"]
        if row["id"] == "rule.grant_disadvantage"
    )
    disadvantage.update(
        {
            "realization_state": "COMPLETE",
            "downstream_owner": None,
            "admission_disposition": "ACTIVE_ADMITTED",
            "evidence_class": "ISOLATED_CONFORMANCE_ONLY",
            "evidence_citation": (
                "SP03 exact attack.roll conformance pair; never production activation"
            ),
            "consumer_or_dependency": (
                "activity.conformance.compiler attack.roll only in isolated source"
            ),
            "activation_trigger": "ISOLATED_SP03_SOURCE_COMPILER_CONFORMANCE_ONLY",
        }
    )
    operation_ledger["registry_census"]["admitted"] += 1
    operation_ledger["registry_census"]["dormant_nonselectable"] -= 1
    _write_json(operation_ledger_path, operation_ledger)

    package_seed_path = (
        source_root
        / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-mvp-seed.json"
    )
    package_seed = json.loads(package_seed_path.read_text(encoding="utf-8"))
    innate = next(
        row
        for row in package_seed["support_definitions"]
        if row["id"] == "effect.innate_sorcery"
    )
    innate_rules = innate["data"]["rule_elements"]
    advantage = next(
        row
        for row in innate_rules
        if row["selector"] == "attack.roll"
        and row["operation_id"] == "rule.grant_advantage"
    )
    advantage.pop("predicate", None)
    if bad_unknown_member:
        advantage["unknown_roll_member"] = "not admitted"
    if bad_state_payload == "advantage_false":
        advantage["value"] = False
    elif bad_state_payload == "advantage_integer":
        advantage["value"] = 1
    if bad_optional_member == "gate":
        advantage["gate"] = {"resource_ref": "resource.innate_sorcery"}
    elif bad_optional_member == "priority":
        advantage["priority"] = 1
    elif bad_optional_member == "stacking_key":
        advantage["stacking_key"] = "stack.roll"
    second_advantage = copy.deepcopy(advantage)
    disadvantage_rule = {
        "selector": "attack.roll",
        "operation_id": "rule.grant_disadvantage",
        "value": True,
        "predicate": {
            "compare": {
                "left": {"accessor_id": "health.bloodied", "subject": "actor"},
                "operator": "eq",
                "right": True,
            }
        },
    }
    if bad_state_payload == "disadvantage_integer":
        disadvantage_rule["value"] = 1
    elif bad_state_payload == "disadvantage_missing":
        disadvantage_rule.pop("value")
    attack_rules = [advantage, second_advantage, disadvantage_rule]
    if permuted:
        attack_rules.reverse()
    innate["data"]["rule_elements"] = [
        row for row in innate_rules if row.get("selector") != "attack.roll"
    ] + attack_rules

    wrong_source = next(
        row
        for row in package_seed["support_definitions"]
        if row["id"] == "effect.sp03.target"
    )
    wrong_source["data"]["rule_elements"].append(
        {
            "selector": "attack.roll",
            "operation_id": "rule.grant_advantage",
            "value": True,
        }
    )

    arcane_focus = next(
        row
        for row in package_seed["support_definitions"]
        if row["id"] == "asset.arcane_focus"
    )
    arcane_focus["data"]["rule_elements"] = [
        {
            "selector": "attack.roll",
            "operation_id": "rule.add_flat",
            "value": True if bad_flat_payload else 3,
        }
    ]
    _write_json(package_seed_path, package_seed)

    return base_installer(source_root, installed_template, destination)


def _roll_runtime(
    tmp_path: Path,
    installed_runtime_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    bad_constraint: bool = False,
    bad_fact: bool = False,
    bad_flat_payload: bool = False,
    bad_state_payload: str | None = None,
    bad_unknown_member: bool = False,
    bad_optional_member: str | None = None,
    permuted: bool = False,
) -> Path:
    from DEV.TESTS import test_sp03_policy_carriers as policy_tests
    from DEV.TESTS import test_sp03_selector_dag as selector_tests

    original_installer = _BASE_SOURCE_COMPILER_FIXTURE

    def install_conformance_pair(
        source_root: Path, installed_template: Path, destination: Path
    ) -> Path:
        return _install_roll_conformance_pair(
            source_root,
            installed_template,
            destination,
            original_installer,
            bad_constraint=bad_constraint,
            bad_fact=bad_fact,
            bad_flat_payload=bad_flat_payload,
            bad_state_payload=bad_state_payload,
            bad_unknown_member=bad_unknown_member,
            bad_optional_member=bad_optional_member,
            permuted=permuted,
        )

    monkeypatch.setattr(
        policy_tests, "_installed_source_compiler_fixture", install_conformance_pair
    )
    installed_parent = tmp_path / "installed"
    installed_parent.mkdir(parents=True)
    return selector_tests._selector_test_runtime(
        tmp_path / "source",
        installed_runtime_root,
        installed_parent / "GAME",
        selector_role="actor",
    )


def _roll_probe_script() -> str:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    compiler_probe = catalog_tests._RECIPE_PROBE.replace("TOOLS.", "GAME.TOOLS.")
    return (
        compiler_probe
        + r"""
sys.stderr.write("ROLL_POLICY_COMPILER_COMPLETE\n")
import copy
import tempfile
from dataclasses import replace
from pathlib import Path

from DEV.TESTS.test_rd05_runtime_execution import _interpreter_result, _proposal
from DEV.TESTS.test_sp03_native_membership import (
    ACTOR_ID,
    CAMPAIGN_ID,
    GitCampaignRepository,
    _actor_record,
    _asset,
    _effect,
    _write_routed,
)
from DEV.TESTS.test_w05_t06_p0_actor_producer import _selected_host
from GAME.TOOLS import activity_contracts as contracts
from GAME.TOOLS import calculation, mechanical_context
from GAME.TOOLS.current_owner import NativeOwnerRef
from GAME.TOOLS.hot_store import NativeHotStore
from GAME.TOOLS.runtime_execution import accept_command

scenario = json.loads(sys.argv[4])
proposal = _proposal(compiled.activity_id)
proposal["action_request"]["actor_id"] = ACTOR_ID
proposal["action_request"]["target_ids"] = ["actor.target"]
accepted = accept_command(
    _interpreter_result(),
    catalog.catalog_context,
    {"definition_id": compiled.activity_id, "kind": "definition.activity"},
    proposal,
)

def make_repository(path, health_current):
    repository = GitCampaignRepository(path)
    repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
    repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
    repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
    actor = _actor_record()
    if health_current is None:
        actor["state"].pop("hp", None)
        actor["state"].pop("life_state_id", None)
        actor["state"].pop("life_state_policy_id", None)
    else:
        actor["state"]["hp"] = {
            "current": health_current,
            "maximum_base": 20,
            "maximum_adjustment": 0,
            "temporary": 0,
        }
        actor["state"]["life_state_id"] = "life.active"
        actor["state"]["life_state_policy_id"] = "life_policy.dnd2024.character_like"
    _write_routed(repository, "world.actor", actor)
    target = copy.deepcopy(_actor_record())
    target["id"] = "actor.target"
    _write_routed(repository, "world.actor", target)

    source_effect = _effect("effect.sp03.innate", ACTOR_ID)
    source_effect["definition_id"] = "effect.innate_sorcery"
    source_effect["state"]["source_id"] = ACTOR_ID
    _write_routed(repository, "world.effect", source_effect)
    wrong_source_effect = _effect("effect.sp03.wrong_source", ACTOR_ID)
    wrong_source_effect["definition_id"] = "effect.sp03.target"
    wrong_source_effect["state"]["source_id"] = ACTOR_ID
    _write_routed(repository, "world.effect", wrong_source_effect)
    asset = _asset(
        "asset.sp03.focus",
        owner=ACTOR_ID,
        equipment=scenario["asset_equipment"],
    )
    asset["definition_id"] = "asset.arcane_focus"
    _write_routed(repository, "world.asset", asset)

    foreign_effect = _effect("effect.sp03.foreign", "actor.target")
    foreign_effect["definition_id"] = "effect.sp03.target"
    foreign_effect["state"]["source_id"] = ACTOR_ID
    _write_routed(repository, "world.effect", foreign_effect)
    foreign_asset = _asset("asset.sp03.foreign", owner="actor.target", equipment="held")
    foreign_asset["definition_id"] = "asset.sp03.target"
    _write_routed(repository, "world.asset", foreign_asset)
    repository.commit("seed source-backed SP03 roll conformance universe")
    return repository

def seed_root(repository):
    resolution = {
        "root_command_id": accepted["command_id"],
        "initiating_command_id": accepted["command_id"],
        "activity_id": compiled.activity_id,
        "actor_id": ACTOR_ID,
        "target_ids": accepted["action_request"]["target_ids"],
        "parameter_bindings": accepted["action_request"].get("parameter_bindings", {}),
        "ruleset_set_digest_generation": 1,
        "ruleset_set_sha256": compiled.ruleset_set_sha256,
        "catalog_context_fingerprint_generation": 1,
        "catalog_context_fingerprint": catalog.catalog_context.fingerprint,
        "status": "RUNNING",
        "next_segment_sequence": 1,
        "invocation_facts": [],
        "fixed_rng_results": [],
        "prior_step_exports": {},
        "child_resolution_ids": [],
        "segments": [],
    }
    _write_routed(
        repository,
        "runtime.command",
        {"kind": "runtime.command", "id": accepted["command_id"], **accepted},
    )
    _write_routed(
        repository,
        "runtime.resolution",
        {
            "kind": "runtime.resolution",
            "id": accepted["root_resolution_id"],
            "campaign_id": CAMPAIGN_ID,
            **resolution,
        },
    )
    repository.commit("seed accepted native root command and Resolution")

def run_calculation(path, health_current):
    repository = make_repository(path, health_current)
    seed_root(repository)
    with NativeHotStore(":memory:") as store:
        host, _source = _selected_host(store, repository=repository)
        consumer_id = compiled.instructions[0].consumer_id
        context = host._current_owner._prepare_root_context(
            catalog,
            compiled,
            command_id=accepted["command_id"],
            consumer_id=consumer_id,
        )
        assert contracts._preparation_context_is_issued(context)
        initial_identity = mechanical_context.context_cache_identity(context)
        source_revision_before = repository._git("rev-parse", "HEAD").stdout.decode("ascii").strip()

        def reject_unissued_context(label, configure=None):
            counterfeit = copy.copy(context)
            if configure is not None:
                configure(counterfeit)
            assert not contracts._preparation_context_is_issued(counterfeit)
            original_evaluator = mechanical_context.evaluate_selector
            evaluator_calls = []

            def forbidden_evaluator(*args, **kwargs):
                evaluator_calls.append(True)
                raise AssertionError("unissued context reached evaluator acquisition")

            mechanical_context.evaluate_selector = forbidden_evaluator
            try:
                calculation.calculate_selector(counterfeit, "attack.roll")
            except calculation.CalculationError as error:
                failure = str(error)
            finally:
                mechanical_context.evaluate_selector = original_evaluator
            if evaluator_calls:
                raise AssertionError("unissued context reached evaluator acquisition")
            if not contracts._preparation_context_is_issued(context):
                raise AssertionError(f"authentic context changed during {label} probe")
            return {"case": label, "status": "REJECTED_BEFORE_EVALUATOR", "reason": failure}

        def invent_occurrence(counterfeit):
            object.__setattr__(counterfeit, "occurrence_id", "occurrence.review.invented")

        def invent_fact_reference(counterfeit):
            object.__setattr__(counterfeit, "accepted_fact_refs", ("fiction.target_reachable",))

        def invent_child_resolution(counterfeit):
            object.__setattr__(
                counterfeit,
                "execution_ref",
                contracts.ExecutionRef(accepted["command_id"], "resolution.review.child"),
            )
            resolution = dict(counterfeit.resolution)
            resolution["causal_invocation_key"] = "invented:child:source"
            object.__setattr__(counterfeit, "resolution", resolution)

        def change_resolution_actor(counterfeit):
            resolution = dict(counterfeit.resolution)
            resolution["actor_id"] = "actor.review.foreign"
            object.__setattr__(counterfeit, "resolution", resolution)

        def copy_catalog(counterfeit):
            object.__setattr__(counterfeit, "catalog", copy.copy(counterfeit.catalog))

        def rebind_same_family_subject(counterfeit):
            roles = dict(counterfeit.role_bindings)
            roles["actor"] = NativeOwnerRef("world.actor", ("actor.review.foreign",))
            object.__setattr__(counterfeit, "role_bindings", roles)

        unissued_cases = [
            reject_unissued_context("shallow-copy"),
            reject_unissued_context("invented-occurrence", invent_occurrence),
            reject_unissued_context("invented-fact-ref", invent_fact_reference),
            reject_unissued_context("invented-child-resolution", invent_child_resolution),
            reject_unissued_context("changed-resolution", change_resolution_actor),
            reject_unissued_context("copied-catalog", copy_catalog),
            reject_unissued_context("same-family-role-rebind", rebind_same_family_subject),
        ]

        if scenario.get("consumer_gate"):
            original_evaluator = mechanical_context.evaluate_selector

            def inject_gated_raw_element(*args, **kwargs):
                raw = copy.deepcopy(original_evaluator(*args, **kwargs))
                contributions = raw["selector_result"]["raw_contributions"]
                advantage = next(
                    row
                    for row in contributions
                    if row["operation_id"] == "rule.grant_advantage"
                )
                advantage["rule_element"]["gate"] = {
                    "resource_ref": "resource.innate_sorcery"
                }
                return raw

            mechanical_context.evaluate_selector = inject_gated_raw_element
            try:
                gated_result = calculation.calculate_selector(context, "attack.roll")
            except contracts.NativePreparationHold as hold:
                gate_status = hold.operation_status
            else:
                return {
                    "status": "GATE_ACCEPTED_UNGATED",
                    "result": gated_result,
                    "unissued_cases": unissued_cases,
                }
            finally:
                mechanical_context.evaluate_selector = original_evaluator
            return {
                "status": "GATE_HOLD",
                "gate_status": gate_status,
                "unissued_cases": unissued_cases,
            }

        policy = next(
            item
            for item in context.compiled.calculation_policy_bindings
            if item.binding.consumer_id == consumer_id
            and item.binding.profile_id == "calculation.roll_advantage_srd521"
        )
        selector_contract = policy.selector_contracts["attack.roll"]
        operation_contracts = selector_contract["operation_contracts"]
        invalid_values = (
            ("rule.add_flat", True),
            ("rule.grant_advantage", 1),
            ("rule.grant_advantage", False),
            ("rule.grant_disadvantage", 1),
            ("rule.grant_disadvantage", None),
        )
        consumer_payload_rejections = []
        for operation_id, invalid_value in invalid_values:
            try:
                mechanical_context._closed_operation_value(
                    operation_id,
                    operation_contracts[operation_id],
                    invalid_value,
                )
            except mechanical_context.MechanicalContextError:
                consumer_payload_rejections.append(operation_id)
        if len(consumer_payload_rejections) != len(invalid_values):
            raise AssertionError("roll consumer accepted an invalid per-pair value")
        try:
            result = calculation.calculate_selector(context, "attack.roll")
        except contracts.NativePreparationHold as hold:
            return {
                "status": hold.operation_status,
                "source_revision": source_revision_before,
            }
        source_revision_after = repository._git("rev-parse", "HEAD").stdout.decode("ascii").strip()
        try:
            mechanical_context.context_cache_identity(context)
        except contracts.NativePreparationHold as hold:
            stale = hold.operation_status
        else:
            stale = "NOT_STALE"
        fresh = host._current_owner._prepare_root_context(
            catalog,
            compiled,
            command_id=accepted["command_id"],
            consumer_id=consumer_id,
        )
        assert contracts._preparation_context_is_issued(fresh)
        fresh_identity = mechanical_context.context_cache_identity(fresh)
        assert contracts._preparation_context_is_issued(fresh)
        assert mechanical_context.context_cache_identity(fresh) == fresh_identity
        assert contracts._preparation_context_is_issued(fresh)
        repinned = calculation.calculate_selector(fresh, "attack.roll")
        forged_fact = replace(fresh, accepted_fact_refs=("fiction.target_reachable",))
        try:
            calculation.calculate_selector(forged_fact, "attack.roll")
        except (
            calculation.CalculationError,
            mechanical_context.MechanicalContextError,
            contracts.ActivityContractError,
        ) as error:
            forged_fact_failure = str(error)
        else:
            raise AssertionError("caller-inserted fact acquired roll-policy authority")
        forged_roles = dict(fresh.role_bindings)
        forged_roles["actor"] = NativeOwnerRef("world.asset", ("asset.sp03.foreign",))
        try:
            rebound = replace(fresh, role_bindings=forged_roles)
            calculation.calculate_selector(rebound, "attack.roll")
        except (
            calculation.CalculationError,
            mechanical_context.MechanicalContextError,
            contracts.ActivityContractError,
        ) as error:
            binding_failure = str(error)
        else:
            raise AssertionError("caller-rebound subject acquired roll-policy authority")
        return {
            "status": "OK",
            "result": result,
            "repinned": repinned,
            "cache_identity_initially_present": bool(initial_identity),
            "cache_identity_after_repin_present": bool(fresh_identity),
            "same_context_after_expansion": stale,
            "source_revision_before": source_revision_before,
            "source_revision_after": source_revision_after,
            "forged_fact_failure": forged_fact_failure,
            "binding_failure": binding_failure,
            "unissued_cases": unissued_cases,
            "consumer_payload_rejections": consumer_payload_rejections,
        }

with tempfile.TemporaryDirectory(prefix="sp03-roll-policy-") as temporary:
    health = scenario["health_current"]
    try:
        evidence = run_calculation(Path(temporary) / "campaign.git", health)
    except mechanical_context.MechanicalContextError as error:
        evidence = {"status": "MECHANICAL_CONTEXT_ERROR", "detail": str(error)}
    print(json.dumps(evidence, sort_keys=True))
"""
    )


def _run_roll_probe(
    runtime_root: Path,
    *,
    activity_family: str = "activity.spell_attack",
    health_current: int | None = 1,
    asset_equipment: str | None = "held",
    consumer_gate: bool = False,
) -> subprocess.CompletedProcess[str]:
    from DEV.TESTS import test_sp03_policy_carriers as policy_tests
    from DEV.TESTS import test_sp03_selector_dag as selector_tests

    recipe = policy_tests._source_compiler_recipe()
    recipe["data"]["family_id"] = activity_family
    dependencies = {
        "effect.innate_sorcery": "definition.effect",
        "effect.sp03.target": "definition.effect",
        "asset.arcane_focus": "definition.asset",
        "asset.sp03.target": "definition.asset",
    }
    return selector_tests._game_runtime_probe(
        runtime_root,
        _roll_probe_script(),
        json.dumps(recipe),
        json.dumps(dependencies),
        "[]",
        json.dumps(
            {
                "activity_family": activity_family,
                "health_current": health_current,
                "asset_equipment": asset_equipment,
                "consumer_gate": consumer_gate,
            }
        ),
    )


def test_real_issued_roll_calculation_cancels_multiple_advantages_against_one_disadvantage(
    installed_runtime_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime_root = _roll_runtime(tmp_path, installed_runtime_root, monkeypatch)
    result = _run_roll_probe(runtime_root)
    assert result.returncode == 0, result.stdout + result.stderr
    evidence = json.loads(result.stdout)
    assert evidence["status"] == "OK"
    for calculation in (evidence["result"], evidence["repinned"]):
        assert calculation["selector_id"] == "attack.roll"
        assert calculation["profile_id"] == PROFILE_ID
        assert calculation["profile_generation"] == 1
        assert calculation["mode"] == "NORMAL"
        assert calculation["required_d20_count"] == 1
        assert calculation["modifier"] == 20
        assert calculation["fixed_roll_selection"] == "HELD_NO_FIXED_ROLL_AUTHORITY"
        assert calculation["fixed_roll_refs"] == []
        assert calculation["fixed_roll_results"] == []
        assert calculation["rng_draw_count"] == 0
        assert calculation["context_facts"] == []
        assert calculation["selector_subject_bindings"] == [
            {
                "role_name": "actor",
                "owner_ref": {
                    "family_key": "world.actor",
                    "identity": ["actor.sp03"],
                },
            }
        ]
        assert set(calculation["read_refs"]) == {
            "selector:attack.roll",
            "accessor:health.bloodied",
            "accessor:health.current",
            "accessor:health.maximum",
            "derived:effect_availability",
            "selector:health.maximum",
        }
        assert {
            tuple(pair["operation_ids"])
            for pair in calculation["compiled_policy"]["binding"][
                "selector_operation_pairs"
            ]
        } == {ROLL_OPERATIONS}
        assert calculation["compiled_policy"]["binding"]["context_fact_bindings"] == []
        assert calculation["compiled_policy"]["binding"]["native_role_bindings"] == [
            {"read_ref": "selector:attack.roll", "role_names": ["actor"]}
        ]
        trace = calculation["trace"]
        assert trace["accepted_advantage_count"] == 2
        assert trace["accepted_disadvantage_count"] == 1
        assert trace["accepted_flat_modifier_count"] == 2
        assert trace["cancellation"] == "OPPOSITES_CANCEL"
        assert trace["raw_contributions"]
    assert (
        evidence["result"]["source_evidence"]["native_membership"]["source_revision"]
        == evidence["source_revision_before"]
    )
    assert (
        len(
            evidence["result"]["source_evidence"]["native_membership"][
                "source_tree_sha"
            ]
        )
        == 40
    )
    active_effect = next(
        row
        for row in evidence["result"]["source_evidence"]["native_membership"]["effects"]
        if row["owner_ref"]["identity"] == ["effect.sp03.innate"]
    )
    assert active_effect["source_id"] == "actor.sp03"
    assert active_effect["lifecycle"] == "effect_lifecycle.active"
    assert active_effect["is_target_local"] is True
    native_focus = next(
        item
        for item in evidence["result"]["source_evidence"]["native_membership"]["assets"]
        if item["owner_ref"]["identity"] == ["asset.sp03.focus"]
    )
    assert native_focus["equipment_mode"] == "held"
    assert native_focus["accessible"] is True
    assert evidence["result"]["occurrence_id"] == (
        evidence["result"]["execution_ref"]["resolution_id"]
        + ":"
        + evidence["result"]["consumer_id"]
    )
    wrong_source = [
        row
        for row in evidence["result"]["trace"]["raw_contributions"]
        if row["owner_definition_id"] == "effect.sp03.target"
        and row["operation_id"] == "rule.grant_advantage"
    ]
    assert len(wrong_source) == 1
    assert wrong_source[0]["disposition"] == "REJECTED"
    assert "SOURCE_NOT_ELIGIBLE" in wrong_source[0]["rejection_reasons"]
    assert evidence["same_context_after_expansion"] == "REVALIDATION_REQUIRED"
    assert evidence["source_revision_before"] == evidence["source_revision_after"]
    assert evidence["forged_fact_failure"]
    assert evidence["binding_failure"]
    assert {item["case"] for item in evidence["unissued_cases"]} == {
        "shallow-copy",
        "invented-occurrence",
        "invented-fact-ref",
        "invented-child-resolution",
        "changed-resolution",
        "copied-catalog",
        "same-family-role-rebind",
    }
    assert all(
        item["status"] == "REJECTED_BEFORE_EVALUATOR"
        for item in evidence["unissued_cases"]
    )
    assert len(evidence["consumer_payload_rejections"]) == 5


def test_duplicate_advantages_remain_two_dice_and_false_predicate_is_not_missing(
    installed_runtime_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime_root = _roll_runtime(tmp_path, installed_runtime_root, monkeypatch)
    result = _run_roll_probe(runtime_root, health_current=11)
    assert result.returncode == 0, result.stdout + result.stderr
    evidence = json.loads(result.stdout)
    assert evidence["status"] == "OK"
    calculation = evidence["result"]
    assert calculation["mode"] == "ADVANTAGE"
    assert calculation["required_d20_count"] == 2
    assert calculation["trace"]["accepted_advantage_count"] == 2
    assert calculation["trace"]["accepted_disadvantage_count"] == 0
    rejected = [
        row
        for row in calculation["trace"]["raw_contributions"]
        if row["operation_id"] == "rule.grant_disadvantage"
    ]
    assert len(rejected) == 1
    assert rejected[0]["predicate_result"] is False
    assert rejected[0]["predicate_state"] == "FALSE"
    assert rejected[0]["disposition"] == "REJECTED"
    assert "PREDICATE_FALSE" in rejected[0]["rejection_reasons"]


def test_carried_asset_rule_element_is_rejected_with_native_availability_evidence(
    installed_runtime_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime_root = _roll_runtime(tmp_path, installed_runtime_root, monkeypatch)
    result = _run_roll_probe(runtime_root, asset_equipment=None)
    assert result.returncode == 0, result.stdout + result.stderr
    evidence = json.loads(result.stdout)
    assert evidence["status"] == "OK"
    calculation = evidence["result"]
    assert calculation["modifier"] == 17
    asset_row = next(
        row
        for row in calculation["trace"]["raw_contributions"]
        if row["owner_application_id"] == "asset.sp03.focus"
    )
    assert asset_row["operation_id"] == "rule.add_flat"
    assert asset_row["source_eligibility"] == "INELIGIBLE"
    assert asset_row["disposition"] == "REJECTED"
    assert "SOURCE_NOT_ELIGIBLE" in asset_row["rejection_reasons"]
    native_asset = next(
        item
        for item in calculation["source_evidence"]["native_membership"]["assets"]
        if item["owner_ref"]["identity"] == ["asset.sp03.focus"]
    )
    assert native_asset["equipment_mode"] is None
    assert native_asset["accessible"] is True


def test_missing_health_is_a_typed_hold_and_wrong_activity_family_rejects_state_contributions(
    installed_runtime_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime_root = _roll_runtime(tmp_path, installed_runtime_root, monkeypatch)
    missing = _run_roll_probe(runtime_root, health_current=None)
    assert missing.returncode == 0, missing.stdout + missing.stderr
    assert json.loads(missing.stdout)["status"] == "AUTHORITY_UNAVAILABLE"

    wrong_family = _run_roll_probe(
        runtime_root, activity_family="activity.spell_save", health_current=1
    )
    assert wrong_family.returncode == 0, wrong_family.stdout + wrong_family.stderr
    evidence = json.loads(wrong_family.stdout)
    assert evidence["status"] == "OK"
    calculation = evidence["result"]
    assert calculation["activity_family_id"] == "activity.spell_save"
    assert calculation["mode"] == "NORMAL"
    assert calculation["trace"]["accepted_advantage_count"] == 0
    assert calculation["trace"]["accepted_disadvantage_count"] == 0
    state_contributions = [
        row
        for row in calculation["trace"]["raw_contributions"]
        if row["contribution_kind"] in {"ADVANTAGE", "DISADVANTAGE"}
        and row["owner_definition_id"] == "effect.innate_sorcery"
    ]
    assert len(state_contributions) == 3
    assert all(row["disposition"] == "REJECTED" for row in state_contributions)
    assert all(
        "ACTIVITY_NOT_ELIGIBLE" in row["rejection_reasons"]
        for row in state_contributions
    )


def test_source_order_permutation_does_not_change_roll_normalization(
    installed_runtime_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    standard = _roll_runtime(tmp_path / "standard", installed_runtime_root, monkeypatch)
    standard_probe = _run_roll_probe(standard)
    assert standard_probe.returncode == 0, standard_probe.stdout + standard_probe.stderr
    original = json.loads(standard_probe.stdout)["result"]
    permuted = _roll_runtime(
        tmp_path / "permuted",
        installed_runtime_root,
        monkeypatch,
        permuted=True,
    )
    permuted_probe = _run_roll_probe(permuted)
    assert permuted_probe.returncode == 0, permuted_probe.stdout + permuted_probe.stderr
    reordered = json.loads(permuted_probe.stdout)["result"]
    assert (
        original["mode"],
        original["modifier"],
        original["required_d20_count"],
        original["trace"]["accepted_advantage_count"],
        original["trace"]["accepted_disadvantage_count"],
    ) == (
        reordered["mode"],
        reordered["modifier"],
        reordered["required_d20_count"],
        reordered["trace"]["accepted_advantage_count"],
        reordered["trace"]["accepted_disadvantage_count"],
    )


def test_compiler_rejects_unclosed_source_constraint_and_unauthorized_roll_fact(
    installed_runtime_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for name, kwargs, expected_message in (
        (
            "constraint",
            {"bad_constraint": True},
            "mechanical-surfaces.schema.json",
        ),
        (
            "fact",
            {"bad_fact": True},
            "ENGINE_STATE-only reads and no context facts",
        ),
        (
            "gate",
            {"bad_optional_member": "gate"},
            "unsupported optional member: gate",
        ),
        (
            "priority",
            {"bad_optional_member": "priority"},
            "unsupported optional member: priority",
        ),
        (
            "stacking-key",
            {"bad_optional_member": "stacking_key"},
            "unsupported optional member: stacking_key",
        ),
    ):
        runtime_root = _roll_runtime(
            tmp_path / name,
            installed_runtime_root,
            monkeypatch,
            **kwargs,
        )
        result = _run_roll_probe(runtime_root)
        assert result.returncode != 0
        assert "ROLL_POLICY_COMPILER_COMPLETE" not in result.stderr
        assert "cannot import name 'calculation'" not in result.stderr
        assert expected_message in result.stderr


@pytest.mark.parametrize(
    "mutation",
    (
        pytest.param({"bad_state_payload": "advantage_false"}, id="false-advantage"),
        pytest.param(
            {"bad_state_payload": "advantage_integer"}, id="integer-advantage"
        ),
        pytest.param(
            {"bad_state_payload": "disadvantage_integer"}, id="integer-disadvantage"
        ),
        pytest.param(
            {"bad_state_payload": "disadvantage_missing"}, id="missing-disadvantage"
        ),
        pytest.param({"bad_unknown_member": True}, id="unknown-member"),
    ),
)
def test_cold_source_compiler_rejects_invalid_roll_payload_variants(
    installed_runtime_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutation: dict[str, object],
) -> None:
    runtime_root = _roll_runtime(
        tmp_path,
        installed_runtime_root,
        monkeypatch,
        **mutation,
    )
    result = _run_roll_probe(runtime_root)
    assert result.returncode != 0
    assert "ROLL_POLICY_COMPILER_COMPLETE" not in result.stderr
    assert "cannot import name 'calculation'" not in result.stderr


def test_compiler_rejects_non_integer_flat_payload_and_production_roster_stays_dormant(
    installed_runtime_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    invalid_runtime_root = _roll_runtime(
        tmp_path / "invalid-source",
        installed_runtime_root,
        monkeypatch,
        bad_flat_payload=True,
    )
    invalid_source = _run_roll_probe(invalid_runtime_root)
    assert invalid_source.returncode != 0
    assert "ROLL_POLICY_COMPILER_COMPLETE" not in invalid_source.stderr
    assert "flat roll Rule Element value is not an integer" in invalid_source.stderr
    assert "cannot import name 'calculation'" not in invalid_source.stderr

    valid_runtime_root = _roll_runtime(
        tmp_path / "valid-source", installed_runtime_root, monkeypatch
    )
    valid_source = _run_roll_probe(valid_runtime_root)
    assert valid_source.returncode == 0, valid_source.stdout + valid_source.stderr
    assert "ROLL_POLICY_COMPILER_COMPLETE" in valid_source.stderr
    evidence = json.loads(valid_source.stdout)
    assert evidence["status"] == "OK"
    assert len(evidence["consumer_payload_rejections"]) == 5

    mechanical = json.loads(
        (ROOT / "DEV/CATALOG/mechanical-surfaces.json").read_text(encoding="utf-8")
    )
    operations = json.loads(
        (
            ROOT / "DEV/CATALOG/catalog-admission-ledger/families/rule_operations.json"
        ).read_text(encoding="utf-8")
    )
    assert (
        "rule.grant_disadvantage"
        not in mechanical["selectors"]["attack.roll"]["allowed_operations"]
    )
    row = next(
        row for row in operations["entries"] if row["id"] == "rule.grant_disadvantage"
    )
    assert row["admission_disposition"] == "DORMANT_NONSELECTABLE"
    assert row["realization_state"] == "DOWNSTREAM_S6D_03"


def test_resource_gate_is_a_compiler_rejection_and_a_consumption_hold(
    installed_runtime_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    gated_compiler_root = _roll_runtime(
        tmp_path / "gated-source",
        installed_runtime_root,
        monkeypatch,
        bad_optional_member="gate",
    )
    compile_result = _run_roll_probe(gated_compiler_root)
    assert compile_result.returncode != 0
    assert "ROLL_POLICY_COMPILER_COMPLETE" not in compile_result.stderr
    assert "unsupported optional member: gate" in compile_result.stderr
    assert "cannot import name 'calculation'" not in compile_result.stderr

    valid_runtime_root = _roll_runtime(
        tmp_path / "valid-source",
        installed_runtime_root,
        monkeypatch,
    )
    consumption_result = _run_roll_probe(valid_runtime_root, consumer_gate=True)
    assert consumption_result.returncode == 0, (
        consumption_result.stdout + consumption_result.stderr
    )
    evidence = json.loads(consumption_result.stdout)
    assert "ROLL_POLICY_COMPILER_COMPLETE" in consumption_result.stderr
    assert evidence["status"] == "GATE_HOLD"
    assert evidence["gate_status"] == "AUTHORITY_UNAVAILABLE"
