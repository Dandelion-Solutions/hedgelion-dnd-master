import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "DEV" / "TOOLS" / "validate_house_rules_mechanical_boundary.py"
SPEC = importlib.util.spec_from_file_location("s6d10_boundary_validator", VALIDATOR_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATOR)


class HouseRulesMechanicalBoundaryContractTests(unittest.TestCase):
    def schema_registry(self):
        result = Registry()
        for path in (ROOT / "DEV/SCHEMAS").glob("*.json"):
            schema = json.loads(path.read_text(encoding="utf-8"))
            if "$id" in schema:
                result = result.with_resource(schema["$id"], Resource.from_contents(schema))
        return result

    def validate_schema(self, name, value):
        schema = json.loads((ROOT / "DEV/SCHEMAS" / name).read_text(encoding="utf-8"))
        Draft202012Validator(schema, registry=self.schema_registry()).validate(value)

    def write_json(self, root: Path, relative: str, value) -> None:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value), encoding="utf-8")

    def make_fixture(self, root: Path) -> None:
        package_root = "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/"
        self.write_json(root, package_root + "gameplay.json", {
            "activity_definitions": [
                {"id": "activity.check.generic", "kind": "definition.activity", "data": {"parameters": {"dc": {"source_class": "INVOCATION_ADJUDICATED", "value_type": "integer", "cardinality": "single", "required": True, "minimum": 1, "maximum": 30}}}},
                {"id": "activity.save.generic", "kind": "definition.activity", "data": {"parameters": {"dc": {"source_class": "INVOCATION_ADJUDICATED", "value_type": "integer", "cardinality": "single", "required": True, "minimum": 1, "maximum": 30}}}},
            ]
        })
        self.write_json(root, package_root + "character-capabilities.json", {
            "identity_source": "ruleset-package-manifest.json", "profile_id": "test.profile",
        })
        self.write_json(root, package_root + "ruleset-package-manifest.json", {
            "manifest_schema_version": 1, "package_id": "hdm.rules.dnd2024-srd52-core", "package_version": "0.1.0-mvp",
            "compatibility_id": "hdm.rules.dnd2024-srd52.v1", "engine_requirement": {"engine_version": "1.0-alpha"},
            "catalog_generation": "2.0.0", "owned_namespaces": ["activity.*"], "dependencies": [],
            "content_files": ["ruleset-package-manifest.json", "character-capabilities.json", "gameplay.json"],
        })
        package_dir = root / package_root
        lock, _ = VALIDATOR.build_resolved_lock([package_dir], root_package_ids=["hdm.rules.dnd2024-srd52-core"], engine_version="1.0-alpha", catalog_generation="2.0.0")
        consumers = [
            "activity.attack.ranged_weapon",
            "activity.spell.fire_bolt",
            "activity.spell.poison_spray",
            "activity.spell.thunderclap",
            "activity.spell.acid_splash",
            "activity.spell.magic_missile",
            "activity.spell.burning_hands",
        ]
        self.write_json(root, "DEV/CATALOG/mechanical-surfaces.json", {"context_facts": {
            "fiction.target_visible": {"disposition": "DORMANT_RESERVED", "source_class": "INVOCATION_ADJUDICATED", "value_type": "boolean", "permitted_consumer_ids": []},
            "fiction.target_reachable": {"disposition": "ACTIVE_ADMITTED", "source_class": "INVOCATION_ADJUDICATED", "value_type": "boolean", "permitted_consumer_ids": consumers},
        }})
        rows = [
            {"edge_key": "parameter:activity.check.generic:dc", "input_kind": "ACTIVITY_PARAMETER", "consumer_id": "activity.check.generic", "input_id": "dc", "value_type": "integer", "source_class": "INVOCATION_ADJUDICATED", "cardinality": "single", "required": True, "minimum": 1, "maximum": 30, "policy_basis_mode": "REQUIRED_ARRAY_MAY_BE_EMPTY"},
            {"edge_key": "parameter:activity.save.generic:dc", "input_kind": "ACTIVITY_PARAMETER", "consumer_id": "activity.save.generic", "input_id": "dc", "value_type": "integer", "source_class": "INVOCATION_ADJUDICATED", "cardinality": "single", "required": True, "minimum": 1, "maximum": 30, "policy_basis_mode": "REQUIRED_ARRAY_MAY_BE_EMPTY"},
        ] + [
            {"edge_key": f"fact:{consumer}:fiction.target_reachable", "input_kind": "INVOCATION_FACT", "consumer_id": consumer, "input_id": "fiction.target_reachable", "value_type": "boolean", "source_class": "INVOCATION_ADJUDICATED", "disposition": "ACTIVE_ADMITTED", "policy_basis_mode": "REQUIRED_ARRAY_MAY_BE_EMPTY"}
            for consumer in consumers
        ]
        self.write_json(root, "DEV/CATALOG/house-rules-mechanical-boundary.json", {
            "schema_version": 1,
            "identity_bound_package_capabilities_path": package_root + "character-capabilities.json",
            "resolved_ruleset_identity": {"package_id": "hdm.rules.dnd2024-srd52-core", "package_version": "0.1.0-mvp", "catalog_generation": "2.0.0", "ruleset_set_sha256": lock["ruleset_set_sha256"], "runtime_selection_state": "ACTIVE_VERIFIED_MACHINE_CONTRACT"},
            "route_profiles": {key: {"policy_revision_and_lifecycle":"x","authority_and_eligibility":"x","consumer_and_value_contract":"x","provenance_and_freeze":"x","catalog_and_native_validation":"x","rng_and_mutation":"x","execution_and_failure":"x","retry_recovery_and_publication":"x","proof_ids": ([row["edge_key"] for row in rows if row["input_kind"]=="ACTIVITY_PARAMETER"] if key.endswith("parameter_to_mechanics") else [row["edge_key"] for row in rows if row["input_kind"]=="INVOCATION_FACT"] if key.endswith("fact_to_mechanics") else ["valid-link","missing-link","quarantined-link"]),"revisit_trigger":"x"} for key in ("route.adjudicated_parameter_to_mechanics","route.invocation_fact_to_mechanics","route.policy_realization_link_conformance")},
            "active_adjudicated_consumers": rows,
            "current_supported_policy_realizations": [],
            "conformance_only_policy_realizations": [
                {"fixture_id": "valid-link", "policy_basis_ref": "policy.test@" + "d" * 40, "target_class": "PACKAGE_DEFINITION", "realization_refs": ["activity.check.generic"], "expected": "CONFORMANCE_VALID_LINK_ONLY"},
                {"fixture_id": "missing-link", "policy_basis_ref": "policy.test@" + "d" * 40, "target_class": "PACKAGE_DEFINITION", "realization_refs": ["activity.missing"], "expected": "failure.policy_realization_gap"},
                {"fixture_id": "quarantined-link", "policy_basis_ref": "policy.test@" + "d" * 40, "target_class": "PRIMITIVE", "realization_refs": ["op.request_choice"], "expected": "failure.policy_realization_gap"},
            ],
        })
        self.write_json(root, "DEV/CATALOG/activity-primitive-contracts.json", {"contracts": [{"primitive_id": "op.request_choice", "selection_state": "DORMANT_NONSELECTABLE", "realization_state": "QUARANTINED"}]})
        failures = sorted(VALIDATOR.POLICY_FAILURES)
        self.write_json(root, "DEV/CATALOG/core-catalog.json", {"registries": {"execution_failure_codes": failures}})
        self.write_json(root, "DEV/CATALOG/catalog-admission-ledger/manifest.json", {
            "schema_name": "hdm_catalog_admission_ledger", "schema_version": 1,
            "catalog_generation": "test", "source_registry": "DEV/CATALOG/core-catalog.json",
            "decision_owner": "test", "laws": {}, "ruleset_package_admission": {},
            "retired_reference_audit": [], "family_shards": ["execution_failure_codes"],
        })
        self.write_json(root, "DEV/CATALOG/catalog-admission-ledger/families/execution_failure_codes.json", {
            "registry_family": "execution_failure_codes",
            "registry_census": {
                "registry_family": "execution_failure_codes", "count": len(failures),
                "scope_stratum": "S6D_PRIMARY", "admitted": len(failures),
                "embedded_nonowner": 0, "dormant_nonselectable": 0, "stale_remove": 0,
            },
            "family_policy": {},
            "entries": [{"registry_family": "execution_failure_codes", "id": value, "admission_disposition": "ACTIVE_ADMITTED"} for value in failures],
        })
        template = root / "GAME/CAMPAIGN/RULES/HOUSE_RULES.yaml"
        template.parent.mkdir(parents=True, exist_ok=True)
        template.write_text("schema_version: 1\npolicies: []\n", encoding="utf-8")

    def mutate_contract(self, root: Path, mutation) -> None:
        path = root / "DEV/CATALOG/house-rules-mechanical-boundary.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        mutation(value)
        path.write_text(json.dumps(value), encoding="utf-8")

    def test_current_repository_contract_has_exact_zero_difference_counts(self):
        self.assertEqual(VALIDATOR.validate(ROOT), {
            "active_adjudicated_consumer_edges": 9,
            "conformance_only_policy_realizations": 3,
            "current_supported_policy_realizations": 0,
            "status": "PASS",
        })

    def test_mutable_policy_revision_label_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture(root)
            self.mutate_contract(root, lambda value: value["conformance_only_policy_realizations"][0].update({"policy_basis_ref": "policy.test@rev-3"}))
            with self.assertRaisesRegex(ValueError, "invalid exact policy basis ref"):
                VALIDATOR.validate(root)

    def test_consumer_edge_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture(root)
            self.mutate_contract(root, lambda value: value["active_adjudicated_consumers"].pop())
            with self.assertRaisesRegex(ValueError, "route profile proof coverage mismatch"):
                VALIDATOR.validate(root)

    def test_complete_row_semantics_and_package_bytes_are_identity_bound(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture(root)
            self.mutate_contract(root, lambda value: value["active_adjudicated_consumers"][0].update({"maximum": 29}))
            with self.assertRaisesRegex(ValueError, "consumer row parameter contract"):
                VALIDATOR.validate(root)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture(root)
            package_member = root / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/gameplay.json"
            package_member.write_text(package_member.read_text(encoding="utf-8") + " ", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "resolved ruleset identity mismatch"):
                VALIDATOR.validate(root)

    def test_missing_or_quarantined_definition_cannot_claim_valid_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture(root)
            self.mutate_contract(root, lambda value: value["conformance_only_policy_realizations"][2].update({"expected": "CONFORMANCE_VALID_LINK_ONLY"}))
            with self.assertRaisesRegex(ValueError, "wrong conformance expectation"):
                VALIDATOR.validate(root)

    def test_parameter_and_fact_use_one_exact_policy_reference_schema(self):
        policy = json.loads((ROOT / "DEV/SCHEMAS/policy-basis-ref.schema.json").read_text(encoding="utf-8"))
        binding = json.loads((ROOT / "DEV/SCHEMAS/activity-parameter-binding.schema.json").read_text(encoding="utf-8"))
        fact = json.loads((ROOT / "DEV/SCHEMAS/invocation-fact.schema.json").read_text(encoding="utf-8"))
        expected_ref = "https://hedgelion.invalid/schemas/policy-basis-ref.schema.json"
        self.assertEqual(policy["pattern"], "^[A-Za-z][A-Za-z0-9_.:-]*@[a-f0-9]{40}(?:[a-f0-9]{24})?$")
        self.assertEqual(binding["$defs"]["adjudicatedBinding"]["properties"]["policy_basis_refs"]["items"]["$ref"], expected_ref)
        self.assertIn("policy_basis_refs", fact["required"])
        self.assertEqual(fact["properties"]["policy_basis_refs"]["items"]["$ref"], expected_ref)

    def test_policy_reference_requires_exact_revision_resolver_evidence(self):
        revision = "d" * 40
        ref = "policy.test@" + revision
        evidence = {
            "policy_id": "policy.test", "campaign_revision": revision,
            "sidecar_source_path": "RULES/HOUSE_RULES.md",
            "sidecar_policy_ids": ["policy.test"],
            "resolved_normative_anchors": {"policy.test": "#policy-test"},
            "authority_validated": True, "applicable": True,
        }
        self.assertTrue(VALIDATOR.validate_policy_basis_resolution(ref, evidence))
        later = dict(evidence, campaign_revision="e" * 40)
        with self.assertRaisesRegex(ValueError, "identity mismatch"):
            VALIDATOR.validate_policy_basis_resolution(ref, later)

    def test_policy_basis_refs_have_one_canonical_order(self):
        refs = ["policy.a@" + "a" * 40, "policy.b@" + "b" * 40]
        self.assertTrue(VALIDATOR.validate_policy_basis_refs(refs))
        with self.assertRaisesRegex(ValueError, "lexicographically sorted"):
            VALIDATOR.validate_policy_basis_refs(list(reversed(refs)))

    def test_resolution_continuation_and_cold_recovery_preserve_frozen_policy_basis(self):
        policy_ref = "policy.test@" + "d" * 40
        binding = {
            "source_class": "INVOCATION_ADJUDICATED", "value": 15,
            "provenance_ref": "interaction-1:dc", "eligibility_basis_fingerprint": "eligibility-A",
            "rules_context_fingerprint": "rules-A", "policy_basis_refs": [policy_ref],
        }
        fact = {
            "fact_id": "fiction.target_reachable", "value": True,
            "provenance_class": "INVOCATION_ADJUDICATED", "provenance_ref": "interaction-1:fact-1",
            "consumer_id": "activity.spell.fire_bolt", "binding_fingerprint": "a" * 64,
            "rules_context_fingerprint": "b" * 64, "policy_basis_refs": [policy_ref],
        }
        package = ROOT / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core"
        activities = {}
        for member in ("character-mvp-seed.json", "gameplay-spine-seed.json"):
            payload = json.loads((package / member).read_text(encoding="utf-8"))
            activities.update({row["id"]: row for row in payload.get("activity_definitions", [])})
        facts = json.loads((ROOT / "DEV/CATALOG/mechanical-surfaces.json").read_text(encoding="utf-8"))["context_facts"]

        fixtures = [
            ("activity.check.generic", {"dc": binding}, []),
            ("activity.spell.fire_bolt", {}, [fact]),
        ]
        for index, (activity_id, parameter_bindings, invocation_facts) in enumerate(fixtures, 1):
            self.assertTrue(VALIDATOR.validate_accepted_policy_basis_collections(parameter_bindings, invocation_facts))
            declaration = activities[activity_id]["data"].get("parameters", {})
            self.assertTrue(set(parameter_bindings) <= set(declaration))
            for parameter_id, accepted_binding in parameter_bindings.items():
                self.assertTrue(VALIDATOR.validate_policy_basis_refs(accepted_binding["policy_basis_refs"]))
                self.assertEqual(declaration[parameter_id]["source_class"], accepted_binding["source_class"])
                self.assertLessEqual(declaration[parameter_id]["minimum"], accepted_binding["value"])
                self.assertLessEqual(accepted_binding["value"], declaration[parameter_id]["maximum"])
            for accepted_fact in invocation_facts:
                self.assertTrue(VALIDATOR.validate_policy_basis_refs(accepted_fact["policy_basis_refs"]))
                self.assertEqual(facts[accepted_fact["fact_id"]]["disposition"], "ACTIVE_ADMITTED")
                self.assertIn(activity_id, facts[accepted_fact["fact_id"]]["permitted_consumer_ids"])

            resolution = {
                "root_command_id": f"cmd-{index}", "initiating_command_id": f"cmd-{index}",
                "activity_id": activity_id, "actor_id": "actor-1",
                "parameter_bindings": parameter_bindings, "catalog_context_fingerprint": "catalog-A",
                "ruleset_set_sha256": "fa0a0794e75a9e0a4343b6394f9d52677e123cd3f01d9b380dd0481bba8fa143",
                "status": "RUNNING", "next_segment_sequence": 1, "invocation_facts": invocation_facts,
                "fixed_rng_results": [], "prior_step_exports": {}, "child_resolution_ids": [], "segments": [],
            }
            continuation = {
                "generation": 1, "root_command_id": f"cmd-{index}", "resolution_id": f"resolution-{index}",
                "activity_id": activity_id, "actor_id": "actor-1",
                "parameter_bindings": parameter_bindings, "catalog_context_fingerprint": "catalog-A",
                "ruleset_set_sha256": "fa0a0794e75a9e0a4343b6394f9d52677e123cd3f01d9b380dd0481bba8fa143",
                "execution_cursor": "step.accepted-inputs", "safe_recompute_phase": "determine",
                "invocation_facts": invocation_facts, "fixed_rng_results": [], "prior_step_exports": {},
                "committed_segment_refs": [], "dependency_frontier_refs": [],
                "expected_child_resolution_ids": [], "future_rng_frontier": f"rng:{index}",
            }
            self.validate_schema("runtime-resolution-state.schema.json", resolution)
            self.validate_schema("runtime-continuation-state.schema.json", continuation)
            accepted = {"parameter_bindings": parameter_bindings, "invocation_facts": invocation_facts}
            checkpoint = json.loads(json.dumps(continuation))
            recovered = {"parameter_bindings": checkpoint["parameter_bindings"], "invocation_facts": checkpoint["invocation_facts"]}
            self.assertEqual(accepted, recovered)
            self.assertEqual(VALIDATOR.fingerprint(accepted), VALIDATOR.fingerprint(recovered))
            changed = json.loads(json.dumps(recovered))
            if changed["parameter_bindings"]:
                changed["parameter_bindings"]["dc"]["policy_basis_refs"] = ["policy.test@" + "e" * 40]
            else:
                changed["invocation_facts"][0]["policy_basis_refs"] = ["policy.test@" + "e" * 40]
            self.assertNotEqual(VALIDATOR.fingerprint(accepted), VALIDATOR.fingerprint(changed))
            self.assertEqual(resolution["fixed_rng_results"], [])
            self.assertEqual(resolution["segments"], [])
        reversed_refs = ["policy.b@" + "b" * 40, "policy.a@" + "a" * 40]
        noncanonical = json.loads(json.dumps(binding))
        noncanonical["policy_basis_refs"] = reversed_refs
        with self.assertRaisesRegex(ValueError, "lexicographically sorted"):
            VALIDATOR.validate_accepted_policy_basis_collections({"dc": noncanonical}, [])
        core = json.loads((ROOT / "DEV/CATALOG/core-catalog.json").read_text(encoding="utf-8"))
        self.assertIn("failure.idempotency_conflict", core["registries"]["execution_failure_codes"])

    def test_integration_schema_is_fail_closed(self):
        schema = json.loads((ROOT / "DEV/SCHEMAS/house-rules-mechanical-boundary.schema.json").read_text(encoding="utf-8"))
        self.assertFalse(schema["additionalProperties"])
        self.assertFalse(schema["$defs"]["parameterEdge"]["additionalProperties"])
        self.assertFalse(schema["$defs"]["factEdge"]["additionalProperties"])
        self.assertFalse(schema["$defs"]["currentRealization"]["additionalProperties"])
        self.assertFalse(schema["$defs"]["conformanceFixture"]["additionalProperties"])
        contract = json.loads((ROOT / "DEV/CATALOG/house-rules-mechanical-boundary.json").read_text(encoding="utf-8"))
        Draft202012Validator(schema, registry=self.schema_registry()).validate(contract)


if __name__ == "__main__":
    unittest.main()
