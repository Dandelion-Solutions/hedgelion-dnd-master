from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_project_map_routes_current_po009_and_po010_owners() -> None:
    text = read("DEV/PROJECT_MAP.md")
    assert "2026-09-09-story-commentator-self-contained-corpus-owner-decision.md" in text
    assert "2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md" in text


def test_canonical_index_routes_current_po009_and_po010_owners() -> None:
    text = read("DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md")
    assert "2026-09-09-story-commentator-self-contained-corpus-owner-decision.md" in text
    assert "2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md" in text


def test_baseline_commentator_story_support_is_not_native_only() -> None:
    producer = read("DEV/docs/superpowers/specs/2026-09-07-story-producer-persistence-retrospective-consumer-contract.md")
    baseline = read("DEV/docs/superpowers/specs/2026-09-08-story-baseline-projection-source-contracts.md")
    owner_name = "2026-09-09-story-commentator-self-contained-corpus-owner-decision.md"
    assert owner_name in producer
    assert owner_name in baseline
    assert "baseline Commentator" in producer
    assert "Story-local" in producer
    assert "Story-local" in baseline


def test_current_sizing_law_does_not_enforce_10240_as_universal_rejection() -> None:
    story_growth = read("DEV/docs/superpowers/specs/2026-09-08-story-persistence-growth-sharding-consumer-decoupling-owner-decision.md")
    wp24 = read("DEV/docs/superpowers/specs/2026-09-08-r2-7-WP-24-performance-scale-operational-budget-canonical-spec.md")
    perf = read("DEV/TESTS/PERFORMANCE_CASES.md")
    owner_name = "2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md"
    for text in (story_growth, wp24, perf):
        assert owner_name in text
    assert "10241" not in perf
    assert "13–16 KiB" in perf or "13-16 KiB" in perf
    assert "review" in perf.lower()


def test_old_size_owner_is_explicitly_superseded_for_threshold_semantics() -> None:
    text = read("DEV/docs/superpowers/specs/2026-09-04-runtime-mutable-github-artifact-size-owner-decision.md")
    assert "2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md" in text
    assert "SUPERSEDED" in text.upper()


def test_readiness_projection_does_not_use_pre_live_as_no_gameplay_proxy() -> None:
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
            assert phrase not in text, f"{path} still contains stale readiness phrase: {phrase}"


def test_save_audit_checks_pre_play_ready_semantics_not_pre_live_phrase() -> None:
    text = read("DEV/TOOLS/audit_engine.py")
    assert "unfinished pre-live setup" not in text
    assert "unfinished pre-live onboarding" not in text
    assert "pre-PLAY_READY" in text or "before PLAY_READY" in text


def test_regression_cases_preserve_provisional_gameplay_before_play_ready() -> None:
    readiness = read("DEV/TESTS/CHARACTER_READINESS_CASES.md")
    explicit_save = read("DEV/TESTS/EXPLICIT_SAVE_CASES.md")
    bootstrap = read("DEV/TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md")
    assert "provisional gameplay" in readiness
    assert "pre-live onboarding" not in explicit_save
    assert "before first live scene" not in bootstrap


def test_closed_wp_canonical_headers_do_not_claim_final_senior_pending() -> None:
    for path in (
        "DEV/docs/superpowers/specs/2026-09-07-r2-7-WP-21-diagnostics-observability-cleanup-retirement-canonical-spec.md",
        "DEV/docs/superpowers/specs/2026-09-07-r2-7-WP-22-verification-test-evaluation-completeness-canonical-spec.md",
        "DEV/docs/superpowers/specs/2026-09-08-r2-7-WP-24-performance-scale-operational-budget-canonical-spec.md",
    ):
        head = "\n".join(read(path).splitlines()[:12]).upper()
        assert "FINAL SENIOR REVIEW PENDING" not in head
        assert "CLOSED" in head or "PASS" in head


def test_po006_no_longer_routes_to_future_opening_of_wp24() -> None:
    text = read("DEV/PRODUCT_OWNER_INPUT.md")
    match = re.search(r"## PO-006\b(.*?)(?=\n---\n\n## PO-007\b)", text, flags=re.S)
    assert match, "PO-006 section not found"
    section = match.group(1)
    assert "when WP-24 opens" not in section
    assert "deferred WP-24 operational-cost route" not in section
    assert "WP-24" in section and ("CLOSED" in section or "INCORPORATED" in section)


def test_wp26_does_not_claim_deferred_po009_schema_realization() -> None:
    event_schema = read("GAME/SCHEMA/event.schema.yaml")
    assert "commentator_eligibility_projection" not in event_schema
    assert "commentator_control_projection" not in event_schema
