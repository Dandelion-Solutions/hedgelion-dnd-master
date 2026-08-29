import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "DEV" / "CATALOG"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def collect_fact_ids(predicate):
    if predicate is None:
        return set()
    if "fact" in predicate:
        return {predicate["fact"]}
    if "all" in predicate:
        result = set()
        for child in predicate["all"]:
            result.update(collect_fact_ids(child))
        return result
    if "any" in predicate:
        result = set()
        for child in predicate["any"]:
            result.update(collect_fact_ids(child))
        return result
    if "not" in predicate:
        return collect_fact_ids(predicate["not"])
    if "compare" in predicate:
        return set()
    raise AssertionError(f"unknown predicate shape: {predicate!r}")


class Step2EvaluationInputContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.surfaces = load_json(CATALOG / "mechanical-surfaces.json")
        cls.schema = load_json(SCHEMAS / "mechanical-surfaces.schema.json")
        cls.validator = Draft202012Validator(cls.schema)

    def compile_rule_element(self, rule_element):
        selector = self.surfaces["selectors"][rule_element["selector"]]
        allowed_inputs = set(selector["allowed_input_classes"])
        for fact_id in collect_fact_ids(rule_element.get("predicate")):
            try:
                fact = self.surfaces["context_facts"][fact_id]
            except KeyError as exc:
                raise ValueError(f"unregistered context fact: {fact_id}") from exc
            if fact["disposition"] != "ACTIVE_ADMITTED":
                raise ValueError(f"dormant context fact: {fact_id}")
            if fact_id not in selector["permitted_context_fact_ids"]:
                raise ValueError(
                    f"selector {rule_element['selector']} forbids exact fact {fact_id}"
                )
            if fact["source_class"] not in allowed_inputs:
                raise ValueError(
                    f"selector {rule_element['selector']} forbids input class "
                    f"{fact['source_class']} from {fact_id}"
                )

    def test_structured_surface_catalog_validates(self):
        self.validator.validate(self.surfaces)
        self.assertIn("context_facts", self.surfaces)
        self.assertIn("derived_nodes", self.surfaces)
        self.assertNotIn("derived_node_kinds", self.surfaces)

    def test_context_facts_are_registered_boolean_invocation_inputs(self):
        facts = self.surfaces["context_facts"]
        self.assertIn("fiction.target_visible", facts)
        self.assertIn("fiction.target_reachable", facts)
        for metadata in facts.values():
            self.assertEqual(metadata["source_class"], "INVOCATION_ADJUDICATED")
            self.assertEqual(metadata["value_type"], "boolean")
            self.assertIn(metadata["disposition"], {"DORMANT_RESERVED", "ACTIVE_ADMITTED"})

    def test_unknown_context_fact_is_compile_error(self):
        with self.assertRaisesRegex(ValueError, "unregistered context fact"):
            self.compile_rule_element({
                "selector": "resource.capacity",
                "operation_id": "rule.add_flat",
                "value": 1,
                "predicate": {"fact": "fiction.unregistered_guess"},
            })

    def test_state_sensitive_step2_selectors_forbid_invocation_adjudicated_inputs(self):
        for selector_id in (
            "health.maximum",
            "resource.capacity",
            "condition.applicability",
        ):
            self.assertEqual(
                self.surfaces["selectors"][selector_id]["allowed_input_classes"],
                ["ENGINE_STATE"],
            )

        with self.assertRaisesRegex(ValueError, "dormant context fact"):
            self.compile_rule_element({
                "selector": "resource.capacity",
                "operation_id": "rule.add_flat",
                "value": 1,
                "predicate": {"fact": "fiction.target_visible"},
            })

    def test_condition_aggregation_depends_on_current_applicability(self):
        node = self.surfaces["derived_nodes"]["condition_aggregation"]
        self.assertIn("derived:effect_availability", node["dependencies"])
        self.assertIn("selector:condition.applicability", node["dependencies"])
        self.assertEqual(node["allowed_input_classes"], ["ENGINE_STATE"])

    def test_derived_node_registry_is_structured_and_complete_for_initial_nodes(self):
        nodes = self.surfaces["derived_nodes"]
        self.assertEqual(
            set(nodes),
            {
                "effect_availability",
                "effect_arbitration",
                "condition_aggregation",
                "condition_intrinsic",
            },
        )
        for metadata in nodes.values():
            self.assertIn("allowed_dependency_kinds", metadata)
            self.assertIn("allowed_input_classes", metadata)
            self.assertIn("dependencies", metadata)
            self.assertEqual(metadata["permitted_context_fact_ids"], [])
        self.assertEqual(
            nodes["condition_intrinsic"]["allowed_input_classes"],
            ["ENGINE_STATE"],
        )


if __name__ == "__main__":
    unittest.main()

