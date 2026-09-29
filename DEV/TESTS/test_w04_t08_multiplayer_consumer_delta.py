from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MULTIPLAYER_DELTA = (
    ROOT / "DEV" / "TESTS" / "fixtures" / "w04_multiplayer_consumer_delta.json"
)


class MultiplayerConsumerDeltaTests(unittest.TestCase):
    def _load_delta(self) -> dict[str, object]:
        self.assertTrue(
            MULTIPLAYER_DELTA.is_file(),
            "W04.T08A must publish its bounded Wave-05 MULTIPLAYER consumer delta",
        )
        return json.loads(MULTIPLAYER_DELTA.read_text(encoding="utf-8"))

    def test_delta_identifies_the_multiplayer_consumer_output_and_scope(self) -> None:
        delta = self._load_delta()

        self.assertEqual(delta["kind"], "w04.multiplayer_consumer_delta")
        self.assertEqual(delta["output"], "W04_MULTIPLAYER_CONSUMER_DELTA_READY")
        self.assertEqual(
            delta["direct_change_paths"],
            [
                "DEV/TESTS/test_w04_t08_multiplayer_consumer_delta.py",
                "DEV/TESTS/fixtures/w04_multiplayer_consumer_delta.json",
            ],
        )
        self.assertEqual(delta["physical_multiplayer_core_change"], "none")

    def test_principal_route_candidates_require_exact_current_player_reload(
        self,
    ) -> None:
        delta = self._load_delta()

        self.assertEqual(
            delta["principal_player_binding"],
            {
                "principal_identity": "verified_stable_account_id",
                "candidate_player_ids": "current_principal_player_route",
                "player_revalidation": "exact_current_PLAYER_reload",
                "mutable_input": "only_after_current_binding_and_routing",
            },
        )

    def test_player_index_and_scan_are_not_authorization_fallbacks(self) -> None:
        delta = self._load_delta()

        self.assertEqual(
            delta["forbidden_authorization_fallbacks"],
            [
                "MANIFEST.players.player_ids",
                "GAME/CAMPAIGN/INDEX/PLAYER_INDEX.yaml",
                "repository_or_directory_scan",
            ],
        )
        self.assertEqual(delta["authorization_fallbacks"], [])

    def test_catch_up_uses_only_current_collaboration_history_and_access(self) -> None:
        delta = self._load_delta()

        catch_up = delta["catch_up"]
        self.assertEqual(
            catch_up["required_current_sources"],
            ["collaboration", "native_history", "access"],
        )
        self.assertEqual(
            catch_up["projection_scope"], "current_recipient_eligible_material"
        )
        self.assertIs(catch_up["assembled_before_mutable_input"], True)
        self.assertIs(catch_up["cursor_hint_proves_human_consumption"], False)

    def test_catch_up_excludes_planning_and_other_participants_private_input(
        self,
    ) -> None:
        delta = self._load_delta()

        self.assertEqual(
            delta["catch_up"]["excluded_material"],
            [
                "dramaturg_planning_only",
                "other_participant_private_input",
                "full_chat_transcript",
            ],
        )

    def test_login_is_human_facing_while_stable_account_id_binds_player(self) -> None:
        delta = self._load_delta()

        self.assertEqual(
            delta["github_identity"],
            {
                "login_role": "human_selection_and_display_only",
                "PLAYER_binding": "verified_stable_account_id",
                "login_or_chat_claim_grants_authority": False,
            },
        )


if __name__ == "__main__":
    unittest.main()
