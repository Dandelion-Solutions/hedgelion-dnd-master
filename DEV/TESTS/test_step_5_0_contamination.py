import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class Step50ContaminationRetirementTests(unittest.TestCase):
    def read(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def load_json(self, relative):
        return json.loads(self.read(relative))

    def test_retired_catalog_ids_are_absent(self):
        core = self.load_json("DEV/CATALOG/core-catalog.json")
        runtime = set(core["registries"]["runtime_record_kinds"])
        world = set(core["registries"]["world_record_kinds"])
        transitions = set(core["registries"]["transition_kinds"])
        events = set(core["registries"]["event_kinds"])

        self.assertNotIn("world.timeline_marker", world)
        self.assertNotIn("transition.timeline_place", transitions)
        self.assertNotIn("event.timeline.placed", events)
        self.assertNotIn("runtime.dirty_record", runtime)
        self.assertNotIn("runtime.publication_batch", runtime)

    def test_catalog_version_advances_coherently(self):
        versions = {
            self.load_json("DEV/CATALOG/core-catalog.json")["catalog_version"],
            self.load_json("DEV/CATALOG/entity-structures.json")["catalog_version"],
            self.load_json("DEV/CATALOG/identifier-policies.json")["catalog_version"],
            self.load_json("DEV/CATALOG/mechanical-surfaces.json")["catalog_version"],
        }
        self.assertEqual(len(versions), 1)
        version = versions.pop()
        self.assertRegex(version, r"^[0-9]+\.[0-9]+\.[0-9]+$")

    def test_retired_record_policies_are_absent(self):
        structures = self.load_json("DEV/CATALOG/entity-structures.json")
        ids = self.load_json("DEV/CATALOG/identifier-policies.json")
        self.assertNotIn("world.timeline_marker", structures["world_records"])
        self.assertNotIn("world.timeline_marker", ids["world"])
        self.assertNotIn("runtime.dirty_record", ids["runtime"])
        self.assertNotIn("runtime.publication_batch", ids["runtime"])

    def test_template_has_no_secret_or_untyped_tactical_placeholder(self):
        self.assertFalse((ROOT / "GAME/CAMPAIGN/WORLD/SECRETS").exists())
        self.assertFalse((ROOT / "GAME/CAMPAIGN/STATE/TACTICAL").exists())
        self.assertFalse((ROOT / "GAME/SCHEMA/secret.schema.yaml").exists())
        schema_index = self.read("GAME/SCHEMA/README.md")
        self.assertNotIn("secret.schema.yaml", schema_index)
        scene_schema = self.read("GAME/SCHEMA/scene.schema.yaml")
        self.assertNotIn("tactical_state_path", scene_schema)

    def test_current_state_has_no_generic_pending_or_checkpoint_duplicate(self):
        schema = self.read("GAME/SCHEMA/current_state.schema.yaml")
        template = self.read("GAME/CAMPAIGN/STATE/CURRENT.yaml")
        for retired in ("pending_global_consequences", "last_checkpoint_id", "last_event_id"):
            self.assertNotIn(retired, schema)
            self.assertNotIn(retired, template)

    def test_manifest_is_sole_latest_checkpoint_pointer(self):
        manifest_schema = self.read("GAME/SCHEMA/campaign_manifest.schema.yaml")
        manifest = self.read("GAME/CAMPAIGN/MANIFEST.yaml")
        self.assertIn("last_checkpoint_id", manifest_schema)
        self.assertIn("last_checkpoint_id", manifest)
        self.assertNotIn("last_event_id", manifest_schema)
        self.assertNotIn("last_event_id", manifest)
        self.assertNotIn("frontier:", manifest_schema.split("world_time:", 1)[1].split("players:", 1)[0])
        self.assertNotIn("frontier:", manifest.split("world_time:", 1)[1].split("players:", 1)[0])
        self.assertFalse((ROOT / "GAME/CAMPAIGN/CHECKPOINTS/LATEST.yaml").exists())

    def test_current_live_and_manifest_paths_are_root_layout(self):
        live = self.read("GAME/CORE/LIVE_SCENE.md")
        multiplayer = self.read("GAME/CORE/MULTIPLAYER.md")
        live_schema = self.read("GAME/SCHEMA/live_scene.schema.yaml")
        for text in (live, multiplayer, live_schema):
            self.assertNotIn("CAMPAIGN/LIVE/LIVE_STATE.yaml", text)
        self.assertIn("LIVE/LIVE_STATE.yaml", live)
        self.assertIn("LIVE/LIVE_STATE.yaml", multiplayer)
        self.assertIn("LIVE/LIVE_STATE.yaml", live_schema)
        self.assertNotIn("CAMPAIGN/MANIFEST", multiplayer)

    def test_partial_order_chronology_remains_available(self):
        chronology = self.read("GAME/CORE/CHRONOLOGY.md")
        ids = self.load_json("DEV/CATALOG/identifier-policies.json")
        self.assertIn("partial order", chronology.lower())
        self.assertIn("world_order.sequence", chronology)
        self.assertIn("independent events", chronology.lower())
        self.assertEqual(ids["non_records"]["timeline_slot"], "ordering_value_not_identity")


if __name__ == "__main__":
    unittest.main()
