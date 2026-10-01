from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "GAME" / "SCHEMA"


def _load_yaml(relative_path: str) -> dict[str, object]:
    value = yaml.safe_load((ROOT / relative_path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{relative_path} must contain a YAML object")
    return value


def _load_json(relative_path: str) -> dict[str, object]:
    value = json.loads((ROOT / relative_path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{relative_path} must contain a JSON object")
    return value


class SharedSchemaStorageReadmeIntegrationProofTests(unittest.TestCase):
    def test_t04_retained_schemas_match_the_strict_native_owner_shapes(self) -> None:
        targets = (
            (
                "GAME/SCHEMA/scene.schema.yaml",
                3,
                "DEV/SCHEMAS/world-scene-state.schema.json",
            ),
            (
                "GAME/SCHEMA/location.schema.yaml",
                2,
                "DEV/SCHEMAS/world-location-state.schema.json",
            ),
            (
                "GAME/SCHEMA/player.schema.yaml",
                2,
                "DEV/SCHEMAS/world-player-state.schema.json",
            ),
        )
        for game_path, version, native_path in targets:
            with self.subTest(schema=game_path):
                game_schema = _load_yaml(game_path)
                native_schema = _load_json(native_path)
                self.assertEqual(game_schema["schema_version"], version)
                self.assertIs(game_schema["strict"], True)
                self.assertEqual(
                    set(game_schema["required"]), set(native_schema["required"])
                )
                self.assertEqual(
                    set(game_schema["fields"]), set(native_schema["properties"])
                )

    def test_scene_and_location_names_preserve_nonempty_owner_constraints(self) -> None:
        targets = (
            (
                "GAME/SCHEMA/scene.schema.yaml",
                "DEV/SCHEMAS/world-scene-state.schema.json",
            ),
            (
                "GAME/SCHEMA/location.schema.yaml",
                "DEV/SCHEMAS/world-location-state.schema.json",
            ),
        )
        for game_path, native_path in targets:
            with self.subTest(schema=game_path):
                game_schema = _load_yaml(game_path)
                native_schema = _load_json(native_path)
                self.assertEqual(game_schema["fields"]["name"], "nonempty_string")
                self.assertEqual(native_schema["properties"]["name"]["minLength"], 1)

    def test_scene_v3_keeps_chronology_and_live_currentness_with_native_routes(
        self,
    ) -> None:
        schema = _load_yaml("GAME/SCHEMA/scene.schema.yaml")
        fields = schema["fields"]

        self.assertNotIn("scene_id", fields)
        self.assertNotIn("player_character_ids", fields)
        self.assertNotIn("chronology_frontier_event_id", fields)
        self.assertNotIn("live_epoch", fields)
        self.assertNotIn("last_absorbed_live_head_sha", fields)

        invariants = " ".join(
            yaml.safe_dump(schema["invariants"], sort_keys=True).lower().split()
        )
        self.assertIn("scene-local", invariants)
        self.assertIn("global", invariants)
        self.assertIn("live_routing", invariants)
        self.assertIn("exact source", invariants)
        self.assertIn("details", invariants)
        self.assertIn("summary", invariants)
        self.assertIn("transcript", invariants)

    def test_location_v2_does_not_duplicate_presence_information_or_secrets(
        self,
    ) -> None:
        schema = _load_yaml("GAME/SCHEMA/location.schema.yaml")
        fields = schema["fields"]

        for retired_or_duplicate in (
            "present_entity_ids",
            "active_thread_ids",
            "known_fact_ids",
            "secret_ids",
            "last_event_id",
            "identity",
            "spatial",
        ):
            with self.subTest(field=retired_or_duplicate):
                self.assertNotIn(retired_or_duplicate, fields)

        invariants = " ".join(
            yaml.safe_dump(schema["invariants"], sort_keys=True).lower().split()
        )
        self.assertIn("actor", invariants)
        self.assertIn("asset", invariants)
        self.assertIn("placement", invariants)
        self.assertIn("index", invariants)

    def test_player_v2_uses_strict_collaboration_refs_without_authority_fallback(
        self,
    ) -> None:
        schema = _load_yaml("GAME/SCHEMA/player.schema.yaml")
        fields = schema["fields"]
        native_player = _load_json("DEV/SCHEMAS/world-player-state.schema.json")
        github_binding = fields["github_binding"]
        native_github_binding = native_player["$defs"]["githubBinding"]
        delta = _load_json("DEV/TESTS/fixtures/w04_player_collaboration_delta.json")
        expected_ref = delta["player_fragment_schema"]["properties"][
            "collaboration_route_refs"
        ]
        collaboration_refs = fields["collaboration_route_refs"]

        self.assertEqual(collaboration_refs["type"], "array")
        self.assertIs(collaboration_refs["uniqueItems"], True)
        self.assertEqual(
            collaboration_refs["required"],
            expected_ref["items"]["required"],
        )
        self.assertEqual(
            set(collaboration_refs["item_fields"]),
            set(expected_ref["items"]["properties"]),
        )
        self.assertEqual(
            collaboration_refs["item_fields"]["obligation_id"], "nonempty_string"
        )
        self.assertEqual(
            collaboration_refs["item_fields"]["generation"], "integer[>=1]"
        )
        self.assertEqual(
            expected_ref["items"]["properties"]["obligation_id"]["minLength"], 1
        )
        self.assertEqual(
            expected_ref["items"]["properties"]["generation"]["minimum"], 1
        )
        self.assertEqual(
            github_binding.get("required"), native_github_binding["required"]
        )
        self.assertEqual(github_binding.get("required"), ["user_id"])
        self.assertEqual(
            set(github_binding) - {"required"},
            set(native_github_binding["properties"]),
        )
        self.assertEqual(github_binding["user_id"], "integer|nonempty_string")
        self.assertEqual(github_binding["login"], "nonempty_string|null")
        github_properties = native_github_binding["properties"]
        self.assertEqual(github_properties["user_id"]["oneOf"][0]["minLength"], 1)
        self.assertEqual(github_properties["login"]["minLength"], 1)
        self.assertEqual(
            fields["policy_authority"]["mechanical_override_policy"],
            "boolean|null",
        )

        invariants = " ".join(
            yaml.safe_dump(schema["invariants"], sort_keys=True).lower().split()
        )
        self.assertIn("stable", invariants)
        self.assertIn("mutable", invariants)
        self.assertIn("routing-only", invariants)
        self.assertIn("authorization", invariants)
        preserved_player_laws = (
            "do not mirror personal chatgpt memory/profile",
            "never use github login as the gameplay actor id",
            "may be refreshed after a github rename",
            "never trust a self-declared player_id",
            "does not delete the player record",
            "active bindings should have deactivated_by null",
            "self-reactivated by the same authenticated github user",
            "requiring creator reactivation",
            "must not automatically create a replacement player or pc",
            "creator self-removal is not represented",
            "missing/null mechanical_override_policy means false",
            "no stored interpretive-policy grant is required",
            "creator-only hard access-control persistence boundary",
            "later revocation is prospective",
            "never bypasses deterministic realization",
            "null defaults are 3 and 6",
            "preferences never alter mechanics",
            "a one-off request for an exact mechanical value does not by itself change",
            "both detail values should be 0",
            "a pc controller change requires explicit persistent event",
            "not a source for real-world sensitive personal data",
        )
        for marker in preserved_player_laws:
            with self.subTest(player_law=marker):
                self.assertIn(marker, invariants)
        for marker in (
            "status inactive",
            "inactive with deactivated_by self",
            "inactive with deactivated_by creator",
            "reactivation reuses the same player_id",
            "creator self-removal",
            "mechanical_override_policy grants policy-adoption authority only",
            "mechanics_detail and decision_support_detail are presentation values",
            "explicit preference or a clear repeated pattern may update it",
        ):
            with self.subTest(player_state=marker):
                self.assertIn(marker, invariants)
        self.assertNotIn("PLAYER_INDEX.yaml", yaml.safe_dump(schema))
        self.assertNotIn("MANIFEST.players.player_ids", yaml.safe_dump(schema))

    def test_schema_readme_covers_current_targets_and_separate_native_owners(
        self,
    ) -> None:
        readme = (SCHEMA_ROOT / "README.md").read_text(encoding="utf-8")
        required_schema_links = (
            "scene.schema.yaml",
            "location.schema.yaml",
            "player.schema.yaml",
            "current_state.schema.yaml",
            "thread.schema.yaml",
            "live_scene.schema.yaml",
            "event.schema.yaml",
            "lore.schema.yaml",
            "session.schema.yaml",
            "checkpoint.schema.yaml",
            "index.schema.yaml",
            "operational_root_routing.schema.yaml",
            "operational_root_handoff.schema.yaml",
        )
        for filename in required_schema_links:
            with self.subTest(schema=filename):
                self.assertIn(filename, readme)
                self.assertTrue((SCHEMA_ROOT / filename).is_file())

        expected_versions = {
            "current_state.schema.yaml": 3,
            "thread.schema.yaml": 2,
            "live_scene.schema.yaml": 2,
            "event.schema.yaml": 2,
            "lore.schema.yaml": 2,
            "session.schema.yaml": 1,
            "checkpoint.schema.yaml": 4,
            "index.schema.yaml": 2,
            "scene.schema.yaml": 3,
            "location.schema.yaml": 2,
            "player.schema.yaml": 2,
        }
        for filename, version in expected_versions.items():
            marker = re.compile(
                rf"\[{re.escape(filename)}\]\({re.escape(filename)}\)\s*\|\s*{version}\s*\|"
            )
            with self.subTest(schema=filename):
                self.assertRegex(readme, marker)
        for owner in (
            "world.lore_fact",
            "world.knowledge",
            "runtime.disclosure",
            "runtime.message",
            "world.actor",
            "world.asset",
            "world.effect",
        ):
            with self.subTest(owner=owner):
                self.assertIn(owner, readme)
        self.assertIn("STATE/RUNTIME/LIVE_ROUTING.yaml", readme)
        for retired_authority in (
            "MANIFEST.players.player_ids",
            "PLAYER_INDEX.yaml",
            "Secret.schema.yaml",
            "scene.chronology_frontier_event_id",
        ):
            with self.subTest(retired_authority=retired_authority):
                self.assertNotIn(retired_authority, readme)

        links = re.findall(r"\]\(([^)]+\.schema\.yaml)\)", readme)
        self.assertTrue(links, "schema README must use local links for schema routes")
        for target in links:
            with self.subTest(link=target):
                self.assertFalse(target.startswith(("/", "../")))
                self.assertTrue((SCHEMA_ROOT / target).is_file())

    def test_storage_readme_is_supporting_and_covers_bounded_recovery_roots(
        self,
    ) -> None:
        readme = (ROOT / "GAME" / "TEMPLATE" / "STORAGE_README.md").read_text(
            encoding="utf-8"
        )
        required_markers = (
            "DND_STORAGE.yaml",
            "campaign/*",
            "MANIFEST.yaml",
            "STATE/",
            "WORLD/",
            "INDEX/",
            "LOG/",
            "CHECKPOINTS/",
            "LIVE/LIVE_STATE.yaml",
            "STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml",
            "runtime.command",
            "runtime.procedure",
            "runtime.interaction",
            "runtime.intent_plan",
        )
        for marker in required_markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, readme)

        lower = readme.lower()
        self.assertIn("кандидата", lower)
        self.assertIn("точным путям", lower)
        self.assertIn("не подтверждает", lower)
        self.assertIn("sqlite", lower)
        self.assertNotIn("GAME/TEMPLATE/STORAGE_README.md", readme)
        self.assertNotIn("MANIFEST.players.player_ids", readme)
        self.assertNotIn("PLAYER_INDEX.yaml", readme)


if __name__ == "__main__":
    unittest.main()
