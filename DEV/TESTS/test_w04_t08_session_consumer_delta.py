from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SESSION_DELTA = ROOT / "DEV" / "TESTS" / "fixtures" / "w04_session_consumer_delta.json"


class SessionConsumerDeltaTests(unittest.TestCase):
    def _load_delta(self) -> dict[str, object]:
        self.assertTrue(
            SESSION_DELTA.is_file(),
            "W04.T08B must publish its bounded Wave-05 SESSION consumer delta",
        )
        return json.loads(SESSION_DELTA.read_text(encoding="utf-8"))

    def test_delta_identifies_the_session_consumer_output(self) -> None:
        delta = self._load_delta()

        self.assertEqual(delta["kind"], "w04.session_consumer_delta")
        self.assertEqual(delta["output"], "W04_SESSION_CONSUMER_DELTA_READY")
        self.assertEqual(delta["physical_session_schema_change"], "none")

    def test_session_metadata_cannot_authorize_native_domains(self) -> None:
        delta = self._load_delta()

        self.assertEqual(
            delta["session_metadata_role"],
            "coordination_recovery_navigation_audit_observability_known_frontier_hints_only",
        )
        self.assertEqual(
            delta["session_metadata_cannot"],
            [
                "campaign_truth",
                "live_truth",
                "player_membership_or_control",
                "gameplay_write_authority",
                "definitive_recovery_frontier",
                "host_liveness",
                "recovery_safe_handoff_success",
            ],
        )
        self.assertIn("session.status", delta["non_authoritative_session_fields"])
        self.assertIn("session.player_id", delta["non_authoritative_session_fields"])
        self.assertIn(
            "session.base_head_sha", delta["non_authoritative_session_fields"]
        )
        self.assertIn(
            "session.last_published_head_sha",
            delta["non_authoritative_session_fields"],
        )

    def test_stale_or_relinquished_host_revalidates_native_sources(self) -> None:
        delta = self._load_delta()

        self.assertEqual(
            delta["pre_mutation_revalidation"],
            {
                "campaign": [
                    "pin_current_selected_campaign_ref_and_exact_revision",
                    "load_current_campaign_route_and_policy_from_native_owner",
                ],
                "player": [
                    "use_verified_stable_principal_id",
                    "resolve_candidate_PLAYER_ids_from_principal_route",
                    "reload_exact_current_PLAYER",
                    "revalidate_binding_status_control_and_operation_policy",
                ],
                "live": [
                    "resolve_current_campaign_LIVE_route",
                    "select_exact_LIVE_epoch_and_source_ref",
                    "validate_exact_current_LIVE_source_revision",
                ],
            },
        )
        self.assertEqual(
            delta["stale_or_relinquished_host"],
            {
                "discard_pre_handoff_hot_assumptions": True,
                "before_dependent_action": "revalidate_applicable_native_sources_and_authority",
            },
        )

    def test_controlled_handoff_names_exact_durable_current_source_basis(self) -> None:
        delta = self._load_delta()
        handoff = delta["controlled_handoff"]

        self.assertEqual(
            handoff["acknowledgement_requires"],
            "complete_compatible_actually_durable_native_source_closure",
        )
        self.assertEqual(
            handoff["exact_source_basis"],
            {
                "scope": "each_participating_native_dependency_in_the_promised_resume_closure",
                "campaign": [
                    "selected_campaign_ref",
                    "exact_current_campaign_revision",
                ],
                "player": [
                    "verified_stable_principal_id",
                    "routed_candidate_PLAYER_id",
                    "exact_current_PLAYER_record",
                    "exact_current_campaign_revision",
                ],
                "live": [
                    "current_campaign_LIVE_route",
                    "selected_LIVE_epoch",
                    "selected_LIVE_source_ref",
                    "exact_current_LIVE_source_revision",
                ],
            },
        )
        self.assertEqual(
            handoff["external_source_movement"],
            "invalidate_revalidate_reselect_or_fail",
        )
        self.assertIs(handoff["session_metadata_proves_success"], False)
        self.assertIs(handoff["universal_cross_domain_currentness_scalar"], False)
        self.assertIs(handoff["already_durable_closure_requires_publication"], False)

    def test_handoff_adds_no_heartbeat_lease_or_noop_publication(self) -> None:
        publication = self._load_delta()["handoff_publication"]

        self.assertEqual(
            publication["forbidden_paths"],
            [
                "heartbeat_write",
                "campaign_global_host_lease",
                "no_op_write_solely_to_record_handoff",
            ],
        )
        self.assertIs(publication["heartbeat_required"], False)
        self.assertIs(publication["lease_introduced"], False)
        self.assertIs(publication["no_op_publication_introduced"], False)


if __name__ == "__main__":
    unittest.main()
