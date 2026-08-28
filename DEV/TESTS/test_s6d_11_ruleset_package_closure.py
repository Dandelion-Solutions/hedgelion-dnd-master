import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "DEV" / "TOOLS"))

from validate_ruleset_package_closure import (
    INVENTORY_DOMAIN, LOAD_FAILURE_REASONS, REQUIRED_ENGINE_CONTRACT_FAMILIES, RulesetContractError,
    build_resolved_lock, combined_semantic_entries, compare_resolved_sets,
    compile_conformance_attestation, validate_compatibility_result,
    validate_runtime_conformance_evidence, validate_transitional_identity_census,
    canonical_json, derive_engine_contract_inventory, sha256,
    current_identity_projection_mismatches,
)
import validate_ruleset_package_closure as closure_tool
from validate_domain_rules_coverage import build_binding, build_contract, validate_binding, validate_contract

PACKAGE_ID = "hdm.rules.dnd2024-srd52-core"
PACKAGE = ROOT / "GAME" / "RULES" / "packages" / PACKAGE_ID


class RulesetPackageClosureTests(unittest.TestCase):
    def build(self, package=PACKAGE):
        return build_resolved_lock([package], root_package_ids=[PACKAGE_ID], engine_version="1.0-alpha", catalog_generation="2.0.0")

    def inventory(self, lock, marker="a"):
        core = {
            "inventory_schema_version": 1,
            "engine_version": "1.0-alpha",
            "ruleset_set_sha256": lock["ruleset_set_sha256"],
            "items": [
                {"family":family,"contract_id":f"engine_contract.{family}.v1","semantic_sha256":marker*64}
                for family in sorted(REQUIRED_ENGINE_CONTRACT_FAMILIES)
            ],
        }
        return {**core, "inventory_sha256": sha256(INVENTORY_DOMAIN + canonical_json(core))}

    def compare(self, adopted_lock, adopted_snapshots, candidate_lock, candidate_snapshots, *, adopted_sources=None, candidate_sources=None, frontier=None):
        return compare_resolved_sets(
            adopted_lock, adopted_snapshots, adopted_sources or self.inventory(adopted_lock),
            candidate_lock, candidate_snapshots, candidate_sources or self.inventory(candidate_lock),
            engine_version="1.0-alpha",
            dependency_frontier=frontier or {"owner":"campaign.runtime-dependencies","state_revision":0,"required_entry_keys":[]},
        )

    def test_current_package_builds_exact_reconstructive_lock(self):
        lock, snapshots = self.build()
        self.assertEqual(lock["ruleset_set_sha256"], "fa0a0794e75a9e0a4343b6394f9d52677e123cd3f01d9b380dd0481bba8fa143")
        self.assertEqual(lock["packages"][0]["content_sha256"], "0ad0e9368f30d5aaa0f22392a83f7e19b6bff8ac4d6e6a19f5aa5f4ad3932d6f")
        self.assertIn("ruleset-package-manifest.json", {row["path"] for row in lock["packages"][0]["members"]})
        self.assertGreaterEqual(len(combined_semantic_entries(snapshots)), 90)

    def test_s6d09_semantic_and_binding_producers_are_separate_and_current(self):
        semantic = json.loads((ROOT / "DEV/CATALOG/domain-rules-coverage.json").read_text(encoding="utf-8"))
        binding = json.loads((ROOT / "DEV/CATALOG/domain-rules-coverage-binding.json").read_text(encoding="utf-8"))
        self.assertEqual(semantic, build_contract(ROOT))
        self.assertEqual(binding, build_binding(ROOT))
        self.assertNotIn("package_binding", semantic)
        self.assertTrue(validate_contract(semantic, ROOT))
        self.assertTrue(validate_binding(binding, ROOT))

    def test_current_identity_projection_census_has_zero_mismatches(self):
        self.assertEqual(current_identity_projection_mismatches(ROOT), [])

    def test_shipped_game_contract_loads_and_hashes_without_dev_tree(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            tool = root / "GAME/TOOLS/ruleset_package.py"
            tool.parent.mkdir(parents=True)
            shutil.copy2(ROOT / "GAME/TOOLS/ruleset_package.py", tool)
            package = root / "GAME/RULES/packages" / PACKAGE_ID
            shutil.copytree(PACKAGE, package)
            script = (
                "from pathlib import Path;"
                "from GAME.TOOLS.ruleset_package import build_resolved_lock;"
                f"p=Path(r'{package}');"
                f"lock,_=build_resolved_lock([p],root_package_ids=['{PACKAGE_ID}'],engine_version='1.0-alpha',catalog_generation='2.0.0');"
                f"assert lock['ruleset_set_sha256']=='fa0a0794e75a9e0a4343b6394f9d52677e123cd3f01d9b380dd0481bba8fa143'"
            )
            completed = subprocess.run([sys.executable, "-c", script], cwd=root, capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertFalse((root / "DEV").exists())

    def test_runtime_conformance_evidence_is_path_neutral_bound_and_closed(self):
        lock, _snapshots = self.build()
        inventory = self.inventory(lock)
        results = [{"validator_id":key,"result":"PASS"} for key in sorted({
            "character_seed_closure","health_effect_recovery_closure",
            "domain_rules_coverage_closure","house_rules_boundary_closure",
        })]
        attestation = compile_conformance_attestation(
            inventory, results, lock=lock, engine_version="1.0-alpha"
        )
        serialized = json.dumps({"inventory":inventory,"attestation":attestation}, sort_keys=True)
        self.assertNotIn("DEV/", serialized)
        validate_runtime_conformance_evidence(
            inventory, attestation, lock=lock, engine_version="1.0-alpha"
        )
        recompiled_results = copy.deepcopy(results)
        self.assertEqual(
            attestation,
            compile_conformance_attestation(
                inventory, recompiled_results, lock=lock, engine_version="1.0-alpha"
            ),
        )
        forged = copy.deepcopy(attestation)
        forged["validator_results"][0]["result"] = "FAIL"
        with self.assertRaises(RulesetContractError):
            validate_runtime_conformance_evidence(
                inventory, forged, lock=lock, engine_version="1.0-alpha"
            )
        missing = copy.deepcopy(inventory)
        missing["items"].pop()
        core = {key:missing[key] for key in ("inventory_schema_version","engine_version","ruleset_set_sha256","items")}
        missing["inventory_sha256"] = sha256(INVENTORY_DOMAIN + canonical_json(core))
        with self.assertRaises(RulesetContractError):
            validate_runtime_conformance_evidence(
                missing, attestation, lock=lock, engine_version="1.0-alpha"
            )

    def test_dev_topology_rename_does_not_change_compiled_runtime_semantics(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            groups_a = {}
            groups_b = {}
            for index, family in enumerate(sorted(REQUIRED_ENGINE_CONTRACT_FAMILIES)):
                stable_id = f"{family}_member"
                rel_a = f"layout-a/{index}/owner.json"
                rel_b = f"renamed-layout/{family}/contract.json"
                for rel in (rel_a, rel_b):
                    path = root / rel
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(json.dumps({"stable_semantics":family,"value":index}), encoding="utf-8")
                groups_a[family] = ((stable_id, rel_a),)
                groups_b[family] = ((stable_id, rel_b),)
            kwargs = {"engine_version":"1.0-alpha","ruleset_set_sha256":"0"*64}
            first = derive_engine_contract_inventory(root, source_groups=groups_a, **kwargs)
            renamed = derive_engine_contract_inventory(root, source_groups=groups_b, **kwargs)
            self.assertEqual(first, renamed)
            lock = {"ruleset_set_sha256":"0"*64}
            results = [{"validator_id":key,"result":"PASS"} for key in sorted({
                "character_seed_closure","health_effect_recovery_closure",
                "domain_rules_coverage_closure","house_rules_boundary_closure",
            })]
            self.assertEqual(
                compile_conformance_attestation(first, results, lock=lock, engine_version="1.0-alpha"),
                compile_conformance_attestation(renamed, results, lock=lock, engine_version="1.0-alpha"),
            )
            changed_path = root / groups_b["primitive"][0][1]
            changed_path.write_text('{"stable_semantics":"primitive","value":"changed"}', encoding="utf-8")
            changed = derive_engine_contract_inventory(root, source_groups=groups_b, **kwargs)
            self.assertNotEqual(first["inventory_sha256"], changed["inventory_sha256"])

    def test_capability_file_has_no_transitional_identity_authority(self):
        capability = json.loads((PACKAGE / "character-capabilities.json").read_text(encoding="utf-8"))
        forbidden = {"content_file", "content_sha256", "content_files", "content_set_sha256", "package_version", "catalog_generation"}
        self.assertFalse(forbidden.intersection(capability))
        self.assertEqual(capability["identity_source"], "ruleset-package-manifest.json")

    def test_manifest_is_self_including_and_non_self_hashing(self):
        manifest = json.loads((PACKAGE / "ruleset-package-manifest.json").read_text(encoding="utf-8"))
        self.assertIn("ruleset-package-manifest.json", manifest["content_files"])
        self.assertFalse({"content_sha256", "content_set_sha256", "sha256"}.intersection(manifest))

    def test_changed_member_bytes_change_package_and_set_identity(self):
        with tempfile.TemporaryDirectory() as td:
            candidate = Path(td) / PACKAGE_ID
            shutil.copytree(PACKAGE, candidate)
            path = candidate / "character-mvp-seed.json"
            path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            adopted, _ = self.build()
            changed, _ = self.build(candidate)
            self.assertNotEqual(adopted["packages"][0]["content_sha256"], changed["packages"][0]["content_sha256"])
            self.assertNotEqual(adopted["ruleset_set_sha256"], changed["ruleset_set_sha256"])

    def test_manifest_embedded_digest_and_missing_self_are_rejected(self):
        for mutation in ("embedded", "missing-self"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as td:
                candidate = Path(td) / PACKAGE_ID
                shutil.copytree(PACKAGE, candidate)
                path = candidate / "ruleset-package-manifest.json"
                manifest = json.loads(path.read_text(encoding="utf-8"))
                if mutation == "embedded": manifest["content_sha256"] = "0" * 64
                else: manifest["content_files"].remove("ruleset-package-manifest.json")
                path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
                with self.assertRaises(RulesetContractError) as cm: self.build(candidate)
                self.assertEqual(cm.exception.reason, "invalid_manifest")

    def test_manifest_case_fold_collision_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            candidate = Path(td) / PACKAGE_ID
            shutil.copytree(PACKAGE, candidate)
            path = candidate / "ruleset-package-manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["content_files"].append("CHARACTER-MVP-SEED.JSON")
            path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            with self.assertRaises(RulesetContractError) as cm:
                self.build(candidate)
            self.assertEqual(cm.exception.reason, "invalid_manifest")

    def test_path_escape_engine_catalog_and_missing_member_fail_closed(self):
        cases = (("path", "invalid_manifest"), ("engine", "engine_incompatibility"), ("catalog", "catalog_incompatibility"), ("missing", "content_mismatch"))
        for mutation, reason in cases:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as td:
                candidate = Path(td) / PACKAGE_ID
                shutil.copytree(PACKAGE, candidate)
                path = candidate / "ruleset-package-manifest.json"
                manifest = json.loads(path.read_text(encoding="utf-8"))
                if mutation == "path": manifest["content_files"].append("../escape.json")
                elif mutation == "engine": manifest["engine_requirement"]["engine_version"] = "9.9"
                elif mutation == "catalog": manifest["catalog_generation"] = "9.9.9"
                else: (candidate / "gameplay-spine-seed.json").unlink()
                if mutation != "missing": path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
                with self.assertRaises(RulesetContractError) as cm: self.build(candidate)
                self.assertEqual(cm.exception.reason, reason)

    def test_additive_semantic_entry_is_compatible(self):
        adopted_lock, adopted_snapshots = self.build()
        with tempfile.TemporaryDirectory() as td:
            candidate = Path(td) / PACKAGE_ID
            shutil.copytree(PACKAGE, candidate)
            path = candidate / "character-mvp-seed.json"
            value = json.loads(path.read_text(encoding="utf-8"))
            value["additive_contracts"] = [{"id":"feature.additive_proof","kind":"definition.feature"}]
            path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
            candidate_lock, candidate_snapshots = self.build(candidate)
            result = self.compare(adopted_lock, adopted_snapshots, candidate_lock, candidate_snapshots)
            self.assertEqual(result["result"], "COMPATIBLE_ADDITIVE")

    def test_removal_kind_semantics_and_active_contract_changes_block(self):
        lock, snapshots = self.build()
        key = next(iter(combined_semantic_entries(snapshots)))
        mutations = []
        removed = copy.deepcopy(snapshots); removed[PACKAGE_ID].semantic_entries.pop(key); mutations.append((removed, self.inventory(lock), "ENTRY_REMOVED"))
        kind = copy.deepcopy(snapshots); kind[PACKAGE_ID].semantic_entries[key]["kind"] = "repurposed"; mutations.append((kind, self.inventory(lock), "ENTRY_KIND_CHANGED"))
        semantics = copy.deepcopy(snapshots); semantics[PACKAGE_ID].semantic_entries[key]["semantic_sha256"] = "f" * 64; mutations.append((semantics, self.inventory(lock), "ENTRY_SEMANTICS_CHANGED"))
        active = self.inventory(lock, "e"); mutations.append((snapshots, active, "ENTRY_SEMANTICS_CHANGED"))
        for candidate, sources, code in mutations:
            with self.subTest(code=code):
                result = self.compare(lock, snapshots, lock, candidate, candidate_sources=sources)
                self.assertEqual(result["result"], "BLOCKED_INCOMPATIBLE")
                self.assertIn(code, {row["code"] for row in result["reasons"]})

    def test_declaration_ancestry_labels_and_load_pass_do_not_replace_evidence(self):
        lock, snapshots = self.build()
        incomplete = self.inventory(lock); incomplete["items"].pop()
        incomplete["inventory_sha256"] = sha256(INVENTORY_DOMAIN + canonical_json({key:incomplete[key] for key in ("inventory_schema_version","engine_version","ruleset_set_sha256","items")}))
        result = self.compare(lock, snapshots, lock, snapshots, candidate_sources=incomplete)
        self.assertEqual(result["result"], "BLOCKED_INSUFFICIENT_EVIDENCE")
        self.assertEqual(result["reasons"][0]["code"], "EVIDENCE_MISSING")

    def test_namespace_and_exact_adopted_dependency_changes_block(self):
        lock, snapshots = self.build()
        namespace_changed = copy.deepcopy(lock)
        namespace_changed["packages"][0]["owned_namespaces"] = ["replacement.*"]
        result = self.compare(lock, snapshots, namespace_changed, snapshots)
        self.assertIn("NAMESPACE_OWNERSHIP_CHANGED", {row["code"] for row in result["reasons"]})
        adopted_with_dependency = copy.deepcopy(lock)
        adopted_with_dependency["packages"][0]["dependencies"] = [
            {"package_id": "hdm.dependency", "content_sha256": "d" * 64}
        ]
        result = self.compare(adopted_with_dependency, snapshots, lock, snapshots)
        self.assertIn("DEPENDENCY_CHANGED", {row["code"] for row in result["reasons"]})

    def test_durable_dependency_frontier_is_derived_and_fail_closed(self):
        lock, snapshots = self.build()
        key = next(iter(combined_semantic_entries(snapshots)))
        candidate = copy.deepcopy(snapshots)
        candidate[PACKAGE_ID].semantic_entries.pop(key)
        result = self.compare(
            lock, snapshots, lock, candidate,
            frontier={"owner":"campaign.runtime-dependencies","state_revision":7,"required_entry_keys":[key]},
        )
        self.assertIn("ACCEPTED_DEPENDENCY_INVALIDATED", {row["code"] for row in result["reasons"]})
        result = self.compare(lock, snapshots, lock, snapshots, frontier={"required_entry_keys":[]})
        self.assertEqual(result["result"], "BLOCKED_INSUFFICIENT_EVIDENCE")

    def test_compatibility_result_shape_and_result_reason_consistency(self):
        lock, snapshots = self.build()
        compatible = self.compare(lock, snapshots, lock, snapshots)
        validate_compatibility_result(compatible)
        invalid = copy.deepcopy(compatible)
        invalid["result"] = "BLOCKED_INCOMPATIBLE"
        with self.assertRaises(RulesetContractError):
            validate_compatibility_result(invalid)

    def test_transitional_identity_keys_are_absent_from_current_carriers(self):
        carriers = [
            PACKAGE / "character-capabilities.json",
            ROOT / "DEV" / "CATALOG" / "domain-rules-coverage.json",
            ROOT / "DEV" / "CATALOG" / "domain-rules-coverage-binding.json",
            ROOT / "DEV" / "CATALOG" / "house-rules-mechanical-boundary.json",
            ROOT / "DEV" / "TESTS" / "fixtures" / "s6d-07-character-mvp-actors.json",
            ROOT / "DEV" / "TOOLS" / "validate_character_mvp_seed.py",
            ROOT / "DEV" / "TOOLS" / "validate_health_effects_recovery_seed.py",
            ROOT / "DEV" / "TOOLS" / "validate_domain_rules_coverage.py",
            ROOT / "DEV" / "TOOLS" / "validate_house_rules_mechanical_boundary.py",
        ]
        forbidden = ("content_set_sha256", "package_content_set_sha256", "identity_bound_package_candidate")
        for carrier in carriers:
            text = carrier.read_text(encoding="utf-8")
            with self.subTest(carrier=str(carrier)):
                self.assertFalse(any(key in text for key in forbidden))
        validate_transitional_identity_census(ROOT)

    def test_transitional_census_rejects_orphans_and_parallel_authority(self):
        closure = json.loads((ROOT / "DEV/CATALOG/ruleset-package-closure.json").read_text(encoding="utf-8"))
        missing = copy.deepcopy(closure)
        missing["transitional_package_identity"].pop()
        with self.assertRaises(RulesetContractError):
            validate_transitional_identity_census(ROOT, missing)
        orphan = copy.deepcopy(closure)
        orphan["transitional_package_identity"][0]["consumer_paths"][0] = "DEV/TOOLS/not-present.py"
        with self.assertRaises(RulesetContractError):
            validate_transitional_identity_census(ROOT, orphan)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            shutil.copytree(ROOT / "DEV", root / "DEV")
            shutil.copytree(ROOT / "GAME", root / "GAME")
            copied = root / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/parallel.json"
            copied.write_text('{"content_set_sha256":"'+("0"*64)+'"}\n', encoding="utf-8")
            with self.assertRaises(RulesetContractError):
                validate_transitional_identity_census(root)

    def test_registered_package_validators_are_explicit_and_present(self):
        closure = json.loads((ROOT / "DEV" / "CATALOG" / "ruleset-package-closure.json").read_text(encoding="utf-8"))
        rows = closure["registered_package_validators"]
        self.assertEqual(len(rows), 4)
        for row in rows:
            self.assertEqual(row["stage"], "BUILD_AND_CONFORMANCE")
            self.assertTrue((ROOT / row["path"]).is_file(), row["path"])

    def test_integrated_validator_registry_cannot_be_skipped_staled_or_failed(self):
        source = json.loads((ROOT / "DEV/CATALOG/ruleset-package-closure.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for row in source["registered_package_validators"]:
                (root / row["path"]).parent.mkdir(parents=True, exist_ok=True)
                (root / row["path"]).write_text("# validator\n", encoding="utf-8")
                (root / row["test_path"]).parent.mkdir(parents=True, exist_ok=True)
                (root / row["test_path"]).write_text("# test\n", encoding="utf-8")
            ledger = root / "DEV/CATALOG/ruleset-package-closure.json"
            ledger.parent.mkdir(parents=True, exist_ok=True)
            ledger.write_text(json.dumps(source), encoding="utf-8")
            passed = mock.Mock(returncode=0, stdout="", stderr="")
            with mock.patch.object(closure_tool.subprocess, "run", return_value=passed):
                results = closure_tool.validate_registered_package_suite(root)
            self.assertEqual(len(results), 4)
            for mutation in ("missing", "stale", "incomplete"):
                changed = copy.deepcopy(source)
                if mutation == "missing":
                    changed["registered_package_validators"].pop()
                elif mutation == "stale":
                    changed["registered_package_validators"][0]["test_path"] = "DEV/TESTS/test_stale.py"
                else:
                    changed["registered_package_validators"][0].pop("scope")
                ledger.write_text(json.dumps(changed), encoding="utf-8")
                with self.assertRaises(RulesetContractError):
                    closure_tool.validate_registered_package_suite(root)
            ledger.write_text(json.dumps(source), encoding="utf-8")
            failed = mock.Mock(returncode=1, stdout="", stderr="validator failed")
            with mock.patch.object(closure_tool.subprocess, "run", return_value=failed):
                with self.assertRaises(RulesetContractError):
                    closure_tool.validate_registered_package_suite(root)

    def test_closed_load_failure_taxonomy(self):
        self.assertEqual(set(LOAD_FAILURE_REASONS), {"invalid_manifest","content_mismatch","missing_dependency","ambiguous_dependency","dependency_cycle","package_id_ambiguity","namespace_conflict","engine_incompatibility","catalog_incompatibility","resolved_set_mismatch","unreconstructable_context"})


if __name__ == "__main__":
    unittest.main()
