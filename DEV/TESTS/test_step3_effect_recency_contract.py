import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
CATALOG = ROOT / "DEV" / "CATALOG"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def registry():
    result = Registry()
    for path in SCHEMAS.glob("*.json"):
        data = load(path)
        if "$id" in data:
            result = result.with_resource(data["$id"], Resource.from_contents(data))
    return result


class Step3EffectRecencyContractTest(unittest.TestCase):
    def test_effect_accepts_positive_local_episode_order_key(self):
        schema = load(SCHEMAS / "world-effect-state.schema.json")
        validator = Draft202012Validator(schema, registry=registry())
        valid = {
            "target_id": "actor-0042",
            "application_order_key": 2,
            "lifecycle": {"state_id": "effect_lifecycle.active"},
        }
        validator.validate(valid)
        for bad in (0, -1, 1.5, "2026-08-19T20:00:00Z", {"counter": 2}):
            invalid = dict(valid, application_order_key=bad)
            with self.assertRaises(ValidationError):
                validator.validate(invalid)

    def test_inventory_exposes_only_compact_recency_evidence(self):
        structures = load(CATALOG / "entity-structures.json")
        expected = structures["world_records"]["world.effect"]["expected"]
        self.assertIn("application_order_key", expected)
        for forbidden in ("created_at", "recency_timestamp", "global_order"):
            self.assertNotIn(forbidden, expected)


if __name__ == "__main__":
    unittest.main()
