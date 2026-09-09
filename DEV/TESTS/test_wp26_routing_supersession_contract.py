from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class WP26RoutingSupersessionContractTests(unittest.TestCase):
    def test_project_map_routes_current_po009_and_po010_owners(self) -> None:
        text = read("DEV/PROJECT_MAP.md")
        self.assertIn("2026-09-09-story-commentator-self-contained-corpus-owner-decision.md", text)
        self.assertIn("2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md", text)

    def test_canonical_index_routes_current_po009_and_po010_owners(self) -> None:
        text = read("DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md")
        self.assertIn("2026-09-09-story-commentator-self-contained-corpus-owner-decision.md", text)
        self.assertIn("2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md", text)

    def test_baseline_commentator_story_support_is_not_native_only(self) -> None:
        producer = read("DEV/docs/superpowers/specs/2026-09-07-story-producer-persistence-retrospective-consumer-contract.md")
        baseline = read("DEV/docs/superpowers/specs/2026-09-08-story-baseline-projection-source-contracts.md")
        owner_name = "2026-09-09-story-commentator-self-contained-corpus-owner-decision.md"
        self.assertIn(owner_name, producer)
        self.assertIn(owner_name, baseline)
        self.assertIn("baseline Commentator", producer)
        self.assertIn("Story-local", producer)
        self.assertIn("Story-local", baseline)

    def test_current_sizing_law_does_not_enforce_10240_as_universal_rejection(self) -> None:
        story_growth = read("DEV/docs/superpowers/specs/2026-09-08-story-persistence-growth-sharding-consumer-decoupling-owner-decision.md")
        wp24 = read("DEV/docs/superpowers/specs/2026-09-08-r2-7-WP-24-performance-scale-operational-budget-canonical-spec.md")
        perf = read("DEV/TESTS/PERFORMANCE_CASES.md")
        owner_name = "2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md"
        for text in (story_growth, wp24, perf):
            self.assertIn(owner_name, text)
        self.assertNotIn("10241", perf)
        self.assertTrue("13–16 KiB" in perf or "13-16 KiB" in perf)
        self.assertIn("review", perf.lower())

    def test_old_size_owner_is_explicitly_superseded_for_threshold_semantics(self) -> None:
        text = read("DEV/docs/superpowers/specs/2026-09-04-runtime-mutable-github-artifact-size-owner-decision.md")
        self.assertIn("2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md", text)
        self.assertIn("SUPERSEDED", text.upper())

    def test_readiness_projection_does_not_use_pre_live_as_no_gameplay_proxy(self) -> None:
        forbidden = {
            "GAME/CORE/RUNTIME.md": ("first true live", "pre-live setup"),
            "GAME/CORE/CAMPAIGN_SETUP.md": ("pre-live vignette", "first true live", "Durable pre-live"),
            "GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md": ("first true live",),
            "GAME/CORE/SAVE_CONTRACT.md": ("unfinished pre-live", "campaign is still pre-live"),
            "GAME/CORE/CORE_INDEX.md": ("pre-live story-first", "first true live", "before play."),
        }
        for path, phrases in forbidden.items():
            text = read(path)
            for phrase in phrases:
                self.assertNotIn(phrase, text, f"{path} still contains stale readiness phrase: {phrase}")

    def test_save_audit_checks_pre_play_ready_semantics_not_pre_live_phrase(self) -> None:
        text = read("DEV/TOOLS/audit_engine.py")
        self.assertNotIn("unfinished pre-live setup", text)
        self.assertNotIn("unfinished pre-live onboarding", text)
        self.assertTrue("pre-PLAY_READY" in text or "before PLAY_READY" in text)

    def test_regression_cases_preserve_provisional_gameplay_before_play_ready(self) -> None:
        readiness = read("DEV/TESTS/CHARACTER_READINESS_CASES.md")
        explicit_save = read("DEV/TESTS/EXPLICIT_SAVE_CASES.md")
        bootstrap = read("DEV/TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md")
        self.assertIn("provisional gameplay", readiness)
        self.assertNotIn("pre-live onboarding", explicit_save)
        self.assertNotIn("before first live scene", bootstrap)

    def test_closed_wp_canonical_headers_do_not_claim_final_senior_pending(self) -> None:
        for path in (
            "DEV/docs/superpowers/specs/2026-09-07-r2-7-WP-21-diagnostics-observability-cleanup-retirement-canonical-spec.md",
            "DEV/docs/superpowers/specs/2026-09-07-r2-7-WP-22-verification-test-evaluation-completeness-canonical-spec.md",
            "DEV/docs/superpowers/specs/2026-09-08-r2-7-WP-24-performance-scale-operational-budget-canonical-spec.md",
        ):
            head = "\n".join(read(path).splitlines()[:12]).upper()
            self.assertNotIn("FINAL SENIOR REVIEW PENDING", head)
            self.assertTrue("CLOSED" in head or "PASS" in head)

    def test_po006_no_longer_routes_to_future_opening_of_wp24(self) -> None:
        text = read("DEV/PRODUCT_OWNER_INPUT.md")
        match = re.search(r"## PO-006\b(.*?)(?=\n---\n\n## PO-007\b)", text, flags=re.S)
        self.assertIsNotNone(match, "PO-006 section not found")
        section = match.group(1)
        self.assertNotIn("when WP-24 opens", section)
        self.assertNotIn("deferred WP-24 operational-cost route", section)
        self.assertIn("WP-24", section)
        self.assertTrue("CLOSED" in section or "INCORPORATED" in section)

    def test_wp26_does_not_claim_deferred_po009_schema_realization(self) -> None:
        event_schema = read("GAME/SCHEMA/event.schema.yaml")
        self.assertNotIn("commentator_eligibility_projection", event_schema)
        self.assertNotIn("commentator_control_projection", event_schema)


if __name__ == "__main__":
    unittest.main()
