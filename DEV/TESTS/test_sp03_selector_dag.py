"""SP03 finite selector/accessor DAG over compiler-issued and native inputs."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytest_plugins = ("DEV.TESTS.test_local_spell_catalog",)

ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ID = "hdm.rules.dnd2024-srd52-core"
PROFILE_ID = "calculation.roll_advantage_srd521"


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def _selector_test_runtime(
    source_root: Path,
    installed_template: Path,
    destination: Path,
    *,
    selector_role: str = "actor",
) -> Path:
    import copy
    import shutil

    import yaml

    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_policy_carriers as policy_tests
    from GAME.TOOLS import ruleset_package

    catalog_tests._stage_clean_source_tree(source_root)
    policy_tests._prepare_sp03_source_tree(source_root)

    primitive_root = source_root / "DEV/CATALOG/activity-primitive-contracts/primitives"
    for primitive_path in primitive_root.glob("*.json"):
        primitive = json.loads(primitive_path.read_text(encoding="utf-8"))
        declaration = (
            primitive["contract"]
            .get("compiler_declarations", {})
            .get("activity.conformance.compiler")
        )
        if isinstance(declaration, dict) and isinstance(declaration.get("roles"), dict):
            declaration["roles"].pop("asset_owner", None)
            _write_json(primitive_path, primitive)

    roll_path = (
        source_root / "DEV/CATALOG/activity-primitive-contracts/primitives/op.roll.json"
    )
    roll = json.loads(roll_path.read_text(encoding="utf-8"))
    declarations = roll["contract"]["compiler_declarations"][
        "activity.conformance.compiler"
    ]
    selector_id = "attack.roll"
    operation_ids = ("rule.add_flat", "rule.grant_advantage")
    for binding in declarations["calculation_policies"]:
        binding["reads"] = [f"selector:{selector_id}"]
        binding["selector_operation_pairs"] = [
            {"selector_id": selector_id, "operation_ids": list(operation_ids)}
        ]
        binding["context_fact_bindings"] = []
        binding["native_role_bindings"] = [
            {
                "read_ref": f"selector:{selector_id}",
                "role_names": [selector_role],
            }
        ]
    _write_json(roll_path, roll)

    mechanical_path = source_root / "DEV/CATALOG/mechanical-surfaces.json"
    mechanical = json.loads(mechanical_path.read_text(encoding="utf-8"))
    selector = mechanical["selectors"][selector_id]
    selector.update(
        {
            "calculation_policy_id": PROFILE_ID,
            "calculation_policy_generation": 1,
            "allowed_input_classes": ["ENGINE_STATE"],
            "permitted_context_fact_ids": [],
            "static_dependencies": [
                "accessor:health.bloodied",
                "derived:effect_availability",
            ],
        }
    )
    for operation_id in operation_ids:
        operation = selector["operation_contracts"][operation_id]
        constraints = list(operation["constraints"])
        if "stable_raw_dice_identity_and_contribution_provenance" not in constraints:
            constraints.append("stable_raw_dice_identity_and_contribution_provenance")
        operation.update(
            {
                "value_kind": "roll_modifier",
                "normalization": "CANCEL_APPLICABLE_OPPOSITES",
                "constraints": constraints,
                "calculation_policy_id": PROFILE_ID,
                "calculation_policy_generation": 1,
            }
        )
    for values, permission in (
        (
            mechanical["accessors"]["health.bloodied"]["permitted_consumer_ids"],
            "selector:attack.roll",
        ),
        (
            mechanical["derived_nodes"]["effect_availability"][
                "permitted_consumer_ids"
            ],
            "selector:attack.roll",
        ),
    ):
        if permission not in values:
            values.append(permission)
    _write_json(mechanical_path, mechanical)

    selector_ledger_path = (
        source_root
        / "DEV/CATALOG/catalog-admission-ledger/families/rule_selectors.json"
    )
    selector_ledger = json.loads(selector_ledger_path.read_text(encoding="utf-8"))
    for entry in selector_ledger["entries"]:
        if (
            entry["id"] == selector_id
            and "activity.conformance.compiler" not in entry["consumer_or_dependency"]
        ):
            entry["consumer_or_dependency"] += "; activity.conformance.compiler"
    _write_json(selector_ledger_path, selector_ledger)

    package_seed_path = (
        source_root
        / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-mvp-seed.json"
    )
    package_seed = json.loads(package_seed_path.read_text(encoding="utf-8"))
    innate_sorcery = next(
        row
        for row in package_seed["support_definitions"]
        if row["id"] == "effect.innate_sorcery"
    )
    advantage = next(
        row
        for row in innate_sorcery["data"]["rule_elements"]
        if row["selector"] == "attack.roll"
    )
    advantage["predicate"] = {
        "compare": {
            "left": {
                "accessor_id": "health.bloodied",
                "subject": selector_role,
            },
            "operator": "eq",
            "right": False,
        }
    }
    target_effect_definition = copy.deepcopy(innate_sorcery)
    target_effect_definition["id"] = "effect.sp03.target"
    target_effect_definition["data"]["rule_elements"] = [
        {
            "selector": "attack.roll",
            "operation_id": "rule.add_flat",
            "value": 17,
        }
    ]
    package_seed["support_definitions"].append(target_effect_definition)
    target_asset_definition = copy.deepcopy(
        next(
            row
            for row in package_seed["support_definitions"]
            if row["id"] == "asset.arcane_focus"
        )
    )
    target_asset_definition["id"] = "asset.sp03.target"
    target_asset_definition["data"]["rule_elements"] = [
        {
            "selector": "attack.roll",
            "operation_id": "rule.add_flat",
            "value": 19,
        }
    ]
    package_seed["support_definitions"].append(target_asset_definition)
    _write_json(package_seed_path, package_seed)

    runtime_root = policy_tests._installed_source_compiler_fixture(
        source_root, installed_template, destination
    )
    package_seed_relative = "RULES/packages/" + PACKAGE_ID + "/character-mvp-seed.json"
    shutil.copy2(package_seed_path, runtime_root / package_seed_relative)
    package_root = source_root / "GAME/RULES/packages" / PACKAGE_ID
    manifest = ruleset_package.load_json_bytes(
        (package_root / "ruleset-package-manifest.json").read_bytes()
    )
    lock, _snapshots = ruleset_package.build_resolved_lock(
        [package_root],
        root_package_ids=[PACKAGE_ID],
        engine_version=manifest["engine_requirement"]["engine_version"],
        catalog_generation=manifest["catalog_generation"],
    )
    marker_path = runtime_root / "RUNTIME_PACKAGE.yaml"
    marker = yaml.safe_load(marker_path.read_text(encoding="utf-8"))
    marker["ruleset_set_sha256"] = lock["ruleset_set_sha256"]
    marker["resolved_ruleset_lock"] = lock
    marker_path.write_text(yaml.safe_dump(marker, sort_keys=False), encoding="utf-8")
    return runtime_root


def _selector_probe_script(compiler_probe: str) -> str:
    compiler_probe = compiler_probe.replace("TOOLS.", "GAME.TOOLS.")
    return (
        compiler_probe
        + r"""
import copy
import json
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
from GAME.TOOLS import mechanical_context
from GAME.TOOLS.current_owner import NativeOwnerRef
from GAME.TOOLS.hot_store import NativeHotStore, OwnerDocument
from GAME.TOOLS.runtime_execution import accept_command
from inspect import Parameter, signature

selector_signature = signature(mechanical_context.evaluate_selector)
assert tuple(selector_signature.parameters) == (
    "compiled",
    "selector_id",
    "consumer_id",
    "observation",
    "role_bindings",
    "accepted_command",
    "prospective_documents",
)
assert all(
    selector_signature.parameters[name].kind is Parameter.KEYWORD_ONLY
    for name in (
        "consumer_id",
        "observation",
        "role_bindings",
        "accepted_command",
        "prospective_documents",
    )
)
assert selector_signature.parameters["prospective_documents"].default == ()

def _native_fixture(repository_root, *, health: bool):
    repository = GitCampaignRepository(repository_root)
    repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
    repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
    repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
    actor = _actor_record()
    if health:
        actor["state"]["hp"] = {
            "current": 11,
            "maximum_base": 20,
            "maximum_adjustment": 0,
            "temporary": 0,
        }
        actor["state"]["life_state_id"] = "life.active"
        actor["state"]["life_state_policy_id"] = "life_policy.dnd2024.character_like"
    _write_routed(repository, "world.actor", actor)
    target = copy.deepcopy(_actor_record())
    target["id"] = "actor.target"
    if health:
        target["state"]["hp"] = {
            "current": 1,
            "maximum_base": 20,
            "maximum_adjustment": 0,
            "temporary": 0,
        }
        target["state"]["life_state_id"] = "life.active"
        target["state"]["life_state_policy_id"] = "life_policy.dnd2024.character_like"
    _write_routed(repository, "world.actor", target)
    effect = _effect("effect.sp03.selector", ACTOR_ID)
    effect["definition_id"] = "effect.innate_sorcery"
    effect["state"]["source_id"] = ACTOR_ID
    _write_routed(repository, "world.effect", effect)
    foreign_effect = _effect("effect.sp03.foreign", "actor.target")
    foreign_effect["definition_id"] = "effect.sp03.target"
    foreign_effect["state"]["source_id"] = ACTOR_ID
    _write_routed(repository, "world.effect", foreign_effect)
    asset = _asset("asset.sp03.selector", owner=ACTOR_ID, equipment="held")
    asset["definition_id"] = "asset.arcane_focus"
    _write_routed(repository, "world.asset", asset)
    target_asset = _asset(
        "asset.sp03.target", owner="actor.target", equipment="held"
    )
    target_asset["definition_id"] = "asset.sp03.target"
    _write_routed(repository, "world.asset", target_asset)
    repository.commit("native selector DAG fixture")
    return repository

def _seed_native_root(repository, accepted_command, compiled):
    resolution = {
        "root_command_id": accepted_command["command_id"],
        "initiating_command_id": accepted_command["command_id"],
        "activity_id": compiled.activity_id,
        "actor_id": ACTOR_ID,
        "target_ids": accepted_command["action_request"]["target_ids"],
        "parameter_bindings": accepted_command["action_request"].get(
            "parameter_bindings", {}
        ),
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
    resolution_id = accepted_command["root_resolution_id"]
    _write_routed(
        repository,
        "runtime.command",
        {
            "kind": "runtime.command",
            "id": accepted_command["command_id"],
            **accepted_command,
        },
    )
    _write_routed(
        repository,
        "runtime.resolution",
        {
            "kind": "runtime.resolution",
            "id": resolution_id,
            "campaign_id": CAMPAIGN_ID,
            **resolution,
        },
    )
    repository.commit("seed accepted native selector root")

def _evaluate(context):
    return mechanical_context.evaluate_selector(
        compiled,
        "attack.roll",
        consumer_id=context.consumer_id,
        observation=context.observation,
        role_bindings=context.role_bindings,
        accepted_command=context.accepted_command,
    )

with tempfile.TemporaryDirectory(prefix="sp03-selector-dag-") as temporary:
    repository = _native_fixture(Path(temporary) / "campaign.git", health=True)
    with NativeHotStore(":memory:") as store:
        host, _source = _selected_host(store, repository=repository)
        if set(compiled.role_contracts) != {"actor", "target"}:
            raise AssertionError("fixture roles must be source-bindable actor/target only")
        proposal = _proposal(compiled.activity_id)
        proposal["action_request"]["actor_id"] = ACTOR_ID
        proposal["action_request"]["target_ids"] = ["actor.target"]
        accepted = accept_command(
            _interpreter_result(),
            catalog.catalog_context,
            {"definition_id": compiled.activity_id, "kind": "definition.activity"},
            proposal,
        )
        _seed_native_root(repository, accepted, compiled)
        root_consumer = compiled.instructions[0].consumer_id
        child_consumer = compiled.instructions[1].children[0].consumer_id
        root_context = host._current_owner._prepare_root_context(
            catalog, compiled, command_id=accepted["command_id"],
            consumer_id=root_consumer,
        )
        if set(root_context.role_bindings) != {"actor", "target"}:
            raise AssertionError("issuer did not derive the exact accepted root roles")
        root = _evaluate(root_context)
        try:
            _evaluate(root_context)
        except contracts.NativePreparationHold as hold:
            if hold.operation_status != "REVALIDATION_REQUIRED":
                raise
            stale_context_status = hold.operation_status
        else:
            raise AssertionError("expanded selector read union reused an old context")

        repinned = host._current_owner._prepare_root_context(
            catalog, compiled, command_id=accepted["command_id"],
            consumer_id=root_consumer,
        )
        root_repin = _evaluate(repinned)
        foreign_roles = dict(repinned.role_bindings)
        foreign_roles["actor"] = NativeOwnerRef("world.asset", ("asset.sp03.selector",))
        try:
            mechanical_context.evaluate_selector(
                compiled, "attack.roll", consumer_id=root_consumer,
                observation=repinned.observation, role_bindings=foreign_roles,
                accepted_command=repinned.accepted_command
            )
        except mechanical_context.MechanicalContextError as error:
            binding_failure = str(error)
        else:
            raise AssertionError("foreign owner family rebound the compiled role")

        actor_owner = repinned.role_bindings["actor"]
        actor_read = repinned.observation.require(actor_owner)
        fake_document = OwnerDocument(
            CAMPAIGN_ID, actor_owner.family_key, actor_owner.identity,
            actor_read.payload, actor_read.source_basis or "test-source",
            actor_read.generation or 0
        )
        try:
            mechanical_context.evaluate_selector(
                compiled, "attack.roll", consumer_id=root_consumer,
                observation=repinned.observation, role_bindings=repinned.role_bindings,
                accepted_command=repinned.accepted_command,
                prospective_documents=(fake_document,)
            )
        except mechanical_context.MechanicalContextError as error:
            prospective_failure = str(error)
        else:
            raise AssertionError("caller prospective document acquired builder provenance")

        child_context = host._current_owner._prepare_root_context(
            catalog, compiled, command_id=accepted["command_id"],
            consumer_id=child_consumer,
        )
        child = _evaluate(child_context)
        forged_child_resolution = dict(root_context.resolution)
        forged_child_resolution["causal_invocation_key"] = "invented:segment:event"
        forged_child = replace(
            root_context,
            occurrence_id="occ.invented.child",
            execution_ref=contracts.ExecutionRef(
                accepted["command_id"], "resolution.invented.child"
            ),
            resolution=forged_child_resolution,
        )
        try:
            mechanical_context.context_cache_identity(forged_child)
        except mechanical_context.MechanicalContextError as error:
            forged_child_failure = str(error)
        else:
            raise AssertionError("caller-created child Resolution acquired issuance")
    missing_repository = _native_fixture(Path(temporary) / "campaign-missing.git", health=False)
    _seed_native_root(missing_repository, accepted, compiled)
    with NativeHotStore(":memory:") as missing_store:
        missing_host, _source = _selected_host(missing_store, repository=missing_repository)
        missing_context = missing_host._current_owner._prepare_root_context(
            catalog, compiled, command_id=accepted["command_id"],
            consumer_id=root_consumer,
        )
        try:
            _evaluate(missing_context)
        except contracts.NativePreparationHold as error:
            missing_result = error.operation_status
        else:
            raise AssertionError("missing HP authority was interpreted as false")

    print(json.dumps({
        "root": root,
        "root_repin": root_repin,
        "child": child,
        "missing": missing_result,
        "stale_context_status": stale_context_status,
        "binding_failure": binding_failure,
        "prospective_failure": prospective_failure,
        "forged_child_failure": forged_child_failure,
    }, sort_keys=True))
"""
    )


def _game_runtime_probe(
    runtime_root: Path, script: str, *arguments: str
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["HDM_INSTALLED_STRUCTURAL_TEST"] = str(runtime_root.resolve())
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONPATH"] = os.pathsep.join(
        (str(runtime_root.parent.resolve()), str(ROOT))
    )
    return subprocess.run(
        [sys.executable, "-c", script, *arguments],
        cwd=runtime_root,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize("selector_role", ("actor", "target"))
def test_real_compiled_root_and_child_selector_inputs_keep_false_distinct_from_missing(
    installed_runtime_root: Path,
    tmp_path: Path,
    selector_role: str,
) -> None:
    runtime_parent = tmp_path / "installed"
    runtime_parent.mkdir()
    runtime_root = runtime_parent / "GAME"
    runtime_root = _selector_test_runtime(
        tmp_path / "source",
        installed_runtime_root,
        runtime_root,
        selector_role=selector_role,
    )
    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_policy_carriers as policy_tests

    recipe = policy_tests._source_compiler_recipe()
    recipe["data"]["family_id"] = "activity.spell_attack"
    dependencies = {
        "effect.innate_sorcery": "definition.effect",
        "effect.sp03.target": "definition.effect",
        "asset.arcane_focus": "definition.asset",
        "asset.sp03.target": "definition.asset",
    }
    result = _game_runtime_probe(
        runtime_root,
        _selector_probe_script(catalog_tests._RECIPE_PROBE),
        json.dumps(recipe),
        json.dumps(dependencies),
        "[]",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    evidence = json.loads(result.stdout)
    for kind, consumer in (
        ("root", "activity.conformance.compiler.step.0"),
        ("root_repin", "activity.conformance.compiler.step.0"),
        ("child", "activity.conformance.compiler.step.1.steps.step.0"),
    ):
        assert set(evidence[kind]) == {
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
        assert evidence[kind]["selector_id"] == "attack.roll"
        assert evidence[kind]["consumer_id"] == consumer
        assert evidence[kind]["calculation_policy_id"] == PROFILE_ID
        assert evidence[kind]["context_facts"] == []
        assert set(evidence[kind]["selector_result"]) == {
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
        }
        contributions = evidence[kind]["selector_result"]["raw_contributions"]
        if selector_role == "actor":
            assert len(contributions) == 1
            contribution = contributions[0]
            assert contribution["owner_definition_id"] == "effect.innate_sorcery"
            assert contribution["owner_application_id"] == "effect.sp03.selector"
            assert contribution["operation_id"] == "rule.grant_advantage"
            assert contribution["value"] is True
            assert contribution["predicate_state"] == "TRUE"
            assert contribution["predicate_result"] is True
            assert (
                contribution["predicate"]["compare"]["left"]["accessor_id"]
                == "health.bloodied"
            )
            assert contribution["predicate"]["compare"]["left"]["subject"] == "actor"
            assert contribution["operation_contract"]["fixed_value"] is True
            assert evidence[kind]["selector_result"]["dependencies"][
                "derived:effect_availability"
            ]["membership_candidates"][0]["owner_ref"]["identity"] == [
                "effect.sp03.selector"
            ]
        else:
            assert [
                (
                    contribution["owner_application_id"],
                    contribution["operation_id"],
                    contribution["value"],
                )
                for contribution in contributions
            ] == [
                ("effect.sp03.foreign", "rule.add_flat", 17),
                ("asset.sp03.target", "rule.add_flat", 19),
            ]
            assert all(
                contribution["predicate_state"] == "TRUE"
                for contribution in contributions
            )
            assert evidence[kind]["selector_result"]["dependencies"][
                "derived:effect_availability"
            ]["membership_candidates"][0]["owner_ref"]["identity"] == [
                "effect.sp03.foreign"
            ]
        assert "value" not in evidence[kind]["selector_result"]
        assert set(evidence[kind]["read_refs"]) == {
            "selector:attack.roll",
            "accessor:health.bloodied",
            "accessor:health.current",
            "accessor:health.maximum",
            "selector:health.maximum",
            "derived:effect_availability",
        }
        assert evidence[kind]["selector_result"]["dependencies"][
            "accessor:health.bloodied"
        ]["value"] is (selector_role == "target")
        assert (
            evidence[kind]["selector_result"]["dependencies"][
                "accessor:health.bloodied"
            ]["dependencies"]["accessor:health.current"]["owner_ref"]["identity"]
            == evidence[kind]["provenance"]["role_bindings"][selector_role]["identity"]
        )
        assert evidence[kind]["native_membership"]["effect_ids"] == [
            "effect.sp03.foreign",
            "effect.sp03.selector",
        ]
        assert evidence[kind]["native_membership"]["asset_ids"] == [
            "asset.sp03.selector",
            "asset.sp03.target",
        ]
        assert set(evidence[kind]["native_membership"]) == {
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
        }
        assert evidence[kind]["native_membership"]["excluded_effect_ids"] == []
    assert evidence["missing"] == "AUTHORITY_UNAVAILABLE"
    assert evidence["stale_context_status"] == "REVALIDATION_REQUIRED"
    assert "exact native preparation context" in evidence["binding_failure"]
    assert "same-builder native issuance" in evidence["prospective_failure"]
