from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def _yaml(relative_path: str) -> dict[str, object]:
    value = yaml.safe_load((ROOT / relative_path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{relative_path} must contain a YAML object")
    return value


def _json(relative_path: str) -> dict[str, object]:
    value = json.loads((ROOT / relative_path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{relative_path} must contain a JSON object")
    return value


class ImplementationPackageVersionCutoverTests(unittest.TestCase):
    def test_t03_versions_and_verify_only_targets_are_exact(self) -> None:
        expected = {
            "current_state": ("GAME/SCHEMA/current_state.schema.yaml", 3),
            "thread": ("GAME/SCHEMA/thread.schema.yaml", 2),
            "live_scene": ("GAME/SCHEMA/live_scene.schema.yaml", 2),
            "event": ("GAME/SCHEMA/event.schema.yaml", 2),
            "lore": ("GAME/SCHEMA/lore.schema.yaml", 2),
            "session": ("GAME/SCHEMA/session.schema.yaml", 1),
            "checkpoint": ("GAME/SCHEMA/checkpoint.schema.yaml", 4),
            "index": ("GAME/SCHEMA/index.schema.yaml", 2),
        }
        for name, (path, version) in expected.items():
            with self.subTest(schema=name):
                self.assertEqual(_yaml(path)["schema_version"], version)

    def test_current_state_v3_has_no_global_frontier_or_scene_route_copy(self) -> None:
        schema = _yaml("GAME/SCHEMA/current_state.schema.yaml")
        fields = schema["fields"]
        self.assertIsInstance(fields, dict)
        assert isinstance(fields, dict)

        world_time = fields.get("world_time")
        self.assertIsInstance(world_time, dict)
        assert isinstance(world_time, dict)
        self.assertEqual(set(world_time), {"display"})

        active_scenes = fields["active_scenes"]
        self.assertIsInstance(active_scenes, dict)
        assert isinstance(active_scenes, dict)
        scene_item = active_scenes["item"]
        self.assertIsInstance(scene_item, dict)
        assert isinstance(scene_item, dict)
        self.assertEqual(set(scene_item), {"scene_id"})

    def test_thread_v2_is_the_narrow_native_process_shape(self) -> None:
        schema = _yaml("GAME/SCHEMA/thread.schema.yaml")
        native = _json("DEV/SCHEMAS/world-thread-state.schema.json")

        self.assertEqual(set(schema["required"]), set(native["required"]))
        fields = schema["fields"]
        self.assertIsInstance(fields, dict)
        assert isinstance(fields, dict)
        self.assertEqual(set(fields), set(native["properties"]))

        identifier = fields["id"]
        self.assertIsInstance(identifier, dict)
        assert isinstance(identifier, dict)
        self.assertEqual(
            identifier["pattern"], r"^THREAD_[A-Za-z0-9_.:-]+$"
        )

        state = fields["state"]
        self.assertIsInstance(state, dict)
        assert isinstance(state, dict)
        self.assertEqual(set(state), {"stage", "progress"})

        temporal = fields["temporal"]
        self.assertIsInstance(temporal, dict)
        assert isinstance(temporal, dict)
        self.assertEqual(
            set(temporal),
            set(native["$defs"]["temporalOccurrence"]["required"]),
        )

    def test_lore_v2_matches_the_native_objective_fact_shape(self) -> None:
        schema = _yaml("GAME/SCHEMA/lore.schema.yaml")
        native = _json("DEV/SCHEMAS/world-lore-fact-state.schema.json")

        self.assertEqual(set(schema["required"]), set(native["required"]))
        fields = schema["fields"]
        self.assertIsInstance(fields, dict)
        assert isinstance(fields, dict)
        self.assertEqual(set(fields), set(native["properties"]))
        self.assertNotIn("visibility", fields)
        self.assertNotIn("known_by_pc_ids", fields)

    def test_live_scene_v2_matches_the_source_native_state_pack(self) -> None:
        schema = _yaml("GAME/SCHEMA/live_scene.schema.yaml")
        native = _json("DEV/SCHEMAS/live-native-state-pack.schema.json")

        self.assertEqual(set(schema["required"]), set(native["required"]))
        fields = schema["fields"]
        self.assertIsInstance(fields, dict)
        assert isinstance(fields, dict)
        self.assertEqual(set(fields), set(native["properties"]))
        self.assertNotIn("campaign_branch", fields)
        self.assertNotIn("live_branch", fields)
        self.assertNotIn("participant_ids", fields)
        self.assertNotIn("player_character_ids", fields)

    def test_event_v2_keeps_order_domain_scoped_and_semantics_separate(self) -> None:
        schema = _yaml("GAME/SCHEMA/event.schema.yaml")
        self.assertEqual(schema["schema_version"], 2)
        fields = schema["fields"]
        self.assertIsInstance(fields, dict)
        assert isinstance(fields, dict)
        self.assertTrue(
            {"id", "kind", "world_order", "caused_by_event_ids", "after_event_ids"}
            <= set(fields)
        )
        world_order = fields["world_order"]
        self.assertIsInstance(world_order, dict)
        assert isinstance(world_order, dict)
        self.assertEqual(set(world_order), {"time", "sequence", "scene_id"})
        invariants = yaml.safe_dump(schema["invariants"], sort_keys=True).lower()
        self.assertIn("local", invariants)
        self.assertIn("optional", invariants)
        self.assertIn("causal ancestry", invariants)
        self.assertIn("relative order", invariants)
        self.assertNotIn("commentator_eligibility_projection", fields)
        self.assertNotIn("commentator_control_projection", fields)

    def test_session_v1_keeps_its_existing_wire_shape_and_non_authority(self) -> None:
        schema = _yaml("GAME/SCHEMA/session.schema.yaml")
        template = _yaml("GAME/CAMPAIGN/SESSIONS/_TEMPLATE.yaml")
        self.assertEqual(
            set(schema["required"]), {"schema_version", "session_id", "status"}
        )
        self.assertEqual(
            set(schema["fields"]),
            {
                "schema_version",
                "session_id",
                "status",
                "player_id",
                "pc_id",
                "scene_id",
                "base_head_sha",
                "last_published_head_sha",
                "started_at",
                "ended_at",
                "notes",
            },
        )
        self.assertEqual(template["schema_version"], 1)
        self.assertEqual(set(template), set(schema["fields"]))
        invariants = " ".join(schema["invariants"]).lower()
        self.assertIn("not authoritative", invariants)
        self.assertIn("current source", invariants)
        self.assertIn("handoff names the exact durable/current source basis", invariants)
        self.assertIn("heartbeat", invariants)


if __name__ == "__main__":
    unittest.main()
