from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "DEV" / "TESTS" / "fixtures"
CONVERGENCE_DELTA = FIXTURES / "w04_multiplayer_session_deltas.json"


class MultiplayerSessionConvergenceTests(unittest.TestCase):
    def _load_json(self, path: Path, *, label: str) -> dict[str, object]:
        self.assertTrue(path.is_file(), f"W04.T08C requires {label}: {path.name}")
        return json.loads(path.read_text(encoding="utf-8"))

    def _load_convergence_delta(self) -> dict[str, object]:
        return self._load_json(CONVERGENCE_DELTA, label="the bounded delta")

    def _load_input_delta(
        self, convergence: dict[str, object], name: str
    ) -> dict[str, object]:
        inputs = convergence["inputs"]
        self.assertIsInstance(inputs, dict)
        input_spec = inputs[name]
        self.assertIsInstance(input_spec, dict)
        relative_path = input_spec["fixture"]
        self.assertIsInstance(relative_path, str)
        return self._load_json(ROOT / relative_path, label=f"the {name} input delta")

    def test_delta_binds_the_accepted_t03a_t08a_and_t08b_outputs(self) -> None:
        convergence = self._load_convergence_delta()

        self.assertEqual(convergence["kind"], "w04.multiplayer_session_deltas")
        self.assertEqual(convergence["output"], "W04_MULTIPLAYER_SESSION_DELTAS_READY")
        for name, expected_output in (
            ("T03A", "W04_PLAYER_COLLABORATION_DELTA_READY"),
            ("T08A", "W04_MULTIPLAYER_CONSUMER_DELTA_READY"),
            ("T08B", "W04_SESSION_CONSUMER_DELTA_READY"),
        ):
            with self.subTest(input_delta=name):
                self.assertEqual(convergence["inputs"][name]["output"], expected_output)
                input_delta = self._load_input_delta(convergence, name)
                self.assertEqual(input_delta["output"], expected_output)

    def test_convergence_changes_no_shared_final_writer_or_physical_schema(
        self,
    ) -> None:
        convergence = self._load_convergence_delta()

        self.assertEqual(convergence["shared_final_writer_changes"], [])
        self.assertEqual(convergence["runtime_owner_changes"], [])
        self.assertEqual(convergence["physical_schema_changes"], [])
        self.assertEqual(
            convergence["direct_change_paths"],
            [
                "DEV/TESTS/test_w04_t08_consumer_convergence.py",
                "DEV/TESTS/fixtures/w04_multiplayer_session_deltas.json",
            ],
        )

    def test_authorization_has_no_index_or_scan_fallback(self) -> None:
        convergence = self._load_convergence_delta()
        t03a = self._load_input_delta(convergence, "T03A")
        t08a = self._load_input_delta(convergence, "T08A")

        self.assertEqual(convergence["authorization_fallbacks"], [])
        self.assertEqual(t03a["route_reference_authority"], "routing_only")
        self.assertEqual(
            t03a["forbidden_authorization_fallbacks"],
            [
                "MANIFEST.players.player_ids",
                "GAME/CAMPAIGN/INDEX/PLAYER_INDEX.yaml",
            ],
        )
        self.assertEqual(t03a["authorization_fallbacks"], [])
        self.assertEqual(
            t08a["forbidden_authorization_fallbacks"],
            [
                "MANIFEST.players.player_ids",
                "GAME/CAMPAIGN/INDEX/PLAYER_INDEX.yaml",
                "repository_or_directory_scan",
            ],
        )
        self.assertEqual(t08a["authorization_fallbacks"], [])

    def test_stable_player_binding_does_not_promote_login_or_chat_claims(self) -> None:
        convergence = self._load_convergence_delta()
        t08a = self._load_input_delta(convergence, "T08A")

        self.assertEqual(
            t08a["principal_player_binding"],
            {
                "principal_identity": "verified_stable_account_id",
                "candidate_player_ids": "current_principal_player_route",
                "player_revalidation": "exact_current_PLAYER_reload",
                "mutable_input": "only_after_current_binding_and_routing",
            },
        )
        self.assertEqual(
            t08a["github_identity"],
            {
                "login_role": "human_selection_and_display_only",
                "PLAYER_binding": "verified_stable_account_id",
                "login_or_chat_claim_grants_authority": False,
            },
        )

    def test_catch_up_does_not_promote_planning_or_private_input(self) -> None:
        convergence = self._load_convergence_delta()
        t08a = self._load_input_delta(convergence, "T08A")
        catch_up = t08a["catch_up"]

        self.assertEqual(
            catch_up["required_current_sources"],
            ["collaboration", "native_history", "access"],
        )
        self.assertIn("dramaturg_planning_only", catch_up["excluded_material"])
        self.assertIn("other_participant_private_input", catch_up["excluded_material"])
        self.assertEqual(convergence["planning_leakage"], "forbidden")

    def test_campaign_live_player_and_currentness_have_separate_native_owners(
        self,
    ) -> None:
        convergence = self._load_convergence_delta()

        self.assertEqual(
            convergence["native_owner_by_dimension"],
            {
                "campaign": "current_campaign_route_and_exact_revision_owner",
                "LIVE": "selected_live_route_epoch_and_source_revision_owner",
                "PLAYER": "verified_stable_id_to_exact_current_PLAYER_access_owner",
                "collaboration": "current_obligation_record_and_exact_generation_owner",
                "procedure": "current_native_procedure_or_continuation_owner",
                "accepted_input": "current_accepted_input_owner",
            },
        )
        self.assertEqual(convergence["currentness_policy"], "owner_specific")
        self.assertIs(convergence["universal_cross_domain_currentness_scalar"], False)

    def test_session_delta_does_not_turn_metadata_into_native_authority(self) -> None:
        convergence = self._load_convergence_delta()
        t08b = self._load_input_delta(convergence, "T08B")

        self.assertEqual(t08b["physical_session_schema_change"], "none")
        self.assertEqual(
            t08b["session_metadata_role"],
            "coordination_recovery_navigation_audit_observability_known_frontier_hints_only",
        )
        self.assertIs(
            t08b["controlled_handoff"]["session_metadata_proves_success"], False
        )
        self.assertIs(
            t08b["controlled_handoff"]["universal_cross_domain_currentness_scalar"],
            False,
        )


if __name__ == "__main__":
    unittest.main()
