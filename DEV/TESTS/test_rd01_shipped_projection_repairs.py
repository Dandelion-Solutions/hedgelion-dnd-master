from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / "GAME"
INSTALL = GAME / "INSTALL"
CORE = GAME / "CORE"

INSTALL_FINAL_CHECKPOINT = "RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION_READY"
CORE_BOOTSTRAP_FINAL_CHECKPOINT = "CORE_BOOTSTRAP_RUNTIME_FINAL_INTEGRATION_READY"
SHIPPED_INTEGRATION_CHECKPOINT = "W05_SHIPPED_INTEGRATION_READY"

EXPECTED_FINAL_WRITERS = {
    INSTALL / "README.md": INSTALL_FINAL_CHECKPOINT,
    INSTALL / "PROJECT_INSTRUCTIONS.txt": INSTALL_FINAL_CHECKPOINT,
    INSTALL / "00_DND_BOOTSTRAP.md": INSTALL_FINAL_CHECKPOINT,
    CORE / "BOOTSTRAP_RUNTIME.md": CORE_BOOTSTRAP_FINAL_CHECKPOINT,
    CORE / "RANDOMNESS.md": SHIPPED_INTEGRATION_CHECKPOINT,
    CORE / "EXPLORATION.md": SHIPPED_INTEGRATION_CHECKPOINT,
}

HISTORICAL_RUNTIME_DOMAIN_ALIASES = (
    "DOMAIN_RULES_COVERAGE.md",
    "domain_rules_coverage.md",
    "CORE/DOMAIN_RULES_COVERAGE",
    "core/domain_rules_coverage",
)


@dataclass(frozen=True)
class FinalWriterRepair:
    path: Path
    stale_fragment: str
    replacement: str
    final_checkpoint: str


REPAIR_INPUTS: tuple[FinalWriterRepair, ...] = (
    FinalWriterRepair(
        path=INSTALL / "README.md",
        stale_fragment=(
            "## Что нужно\n\n- ChatGPT Project;\n- один или несколько runtime ZIP вида "
            "`hedgelion-dnd-master-runtime-vX.Y.zip`"
        ),
        replacement=(
            "## Что нужно\n\n- ChatGPT Plus (supported MVP plan);\n- ChatGPT Project;\n"
            "- один или несколько runtime ZIP вида `hedgelion-dnd-master-runtime-vX.Y.zip`"
        ),
        final_checkpoint=INSTALL_FINAL_CHECKPOINT,
    ),
    FinalWriterRepair(
        path=INSTALL / "README.md",
        stale_fragment=(
            "Use the connected GitHub Connector as the default transport for campaign-storage "
            "GitHub reads/writes. Do not substitute shell `git`, `gh`, local clone, direct "
            "private-repository HTTP, or web scraping first."
        ),
        replacement=(
            "Use the connected GitHub Connector as the only permitted transport for campaign-storage "
            "GitHub reads/writes. Do not attempt or probe shell `git`, `gh`, local clone, direct "
            "private-repository HTTP, web scraping, or any other alternate transport. Missing required "
            "Connector capability is a supported-profile capability failure."
        ),
        final_checkpoint=INSTALL_FINAL_CHECKPOINT,
    ),
    FinalWriterRepair(
        path=INSTALL / "PROJECT_INSTRUCTIONS.txt",
        stale_fragment=(
            "Use the connected GitHub Connector as the default transport for campaign-storage "
            "GitHub reads/writes. Do not substitute shell `git`, `gh`, local clone, direct "
            "private-repository HTTP, or web scraping first."
        ),
        replacement=(
            "Use the connected GitHub Connector as the only permitted transport for campaign-storage "
            "GitHub reads/writes. Do not attempt or probe shell `git`, `gh`, local clone, direct "
            "private-repository HTTP, web scraping, or any other alternate transport. Missing required "
            "Connector capability is a supported-profile capability failure."
        ),
        final_checkpoint=INSTALL_FINAL_CHECKPOINT,
    ),
    FinalWriterRepair(
        path=INSTALL / "00_DND_BOOTSTRAP.md",
        stale_fragment=(
            "Do not try shell git, `gh`, local clone, direct private-repository HTTP, or web scraping "
            "first. Diagnose Connector binding, identity, App access, permissions/status, then a real "
            "capability gap."
        ),
        replacement=(
            "Do not attempt or probe shell git, `gh`, local clone, direct private-repository HTTP, web "
            "scraping, or any other alternate transport. Missing required Connector capability is a "
            "supported-profile capability failure; diagnose Connector binding, identity, App access, and "
            "permissions/status within that fixed path."
        ),
        final_checkpoint=INSTALL_FINAL_CHECKPOINT,
    ),
    FinalWriterRepair(
        path=CORE / "BOOTSTRAP_RUNTIME.md",
        stale_fragment=(
            "Use connected GitHub Connector as normal transport for campaign-storage reads/writes and "
            "GitHub identity/metadata.\n\nDo not first use shell git, `gh`, local clone/pull, direct private "
            "HTTP or web scraping. Do not copy engine blobs/tree objects into campaign storage and do not "
            "reconstruct engine from GitHub."
        ),
        replacement=(
            "Use connected GitHub Connector as the only permitted transport for campaign-storage reads/writes "
            "and GitHub identity/metadata.\n\nDo not attempt or probe shell git, `gh`, local clone/pull, direct "
            "private HTTP, web scraping, or any other alternate transport. Missing required Connector capability "
            "is a supported-profile capability failure. Do not copy engine blobs/tree objects into campaign "
            "storage and do not reconstruct engine from GitHub."
        ),
        final_checkpoint=CORE_BOOTSTRAP_FINAL_CHECKPOINT,
    ),
    FinalWriterRepair(
        path=CORE / "RANDOMNESS.md",
        stale_fragment=(
            "Maintain the compact operational trace required by `MECHANICS_INTEGRITY.md` during the current "
            "action sequence/encounter.\n\nWhen randomness materially causes durable state, the semantic record "
            "may include:"
        ),
        replacement=(
            "Maintain the compact operational trace required by `MECHANICS_INTEGRITY.md` during the current "
            "action sequence/encounter. When a Resolution or Continuation carrying accepted fixed RNG can survive "
            "suspension or recovery, retain that result with its Resolution/Continuation closure; on resume, "
            "restore and reuse it rather than rerolling. This does not require Git logging every trivial roll.\n\n"
            "When randomness materially causes durable state, the semantic record may include:"
        ),
        final_checkpoint="W05_SHIPPED_INTEGRATION_READY",
    ),
    FinalWriterRepair(
        path=CORE / "EXPLORATION.md",
        stale_fragment="For complex tactical spaces, create a compact spatial record/map rather than repeatedly reconstructing geometry from prose.",
        replacement=(
            "For complex tactical spaces, retain only the bounded location/procedure/applicability facts needed "
            "by the current decision. Do not introduce a generic spatial record/map, pathfinding engine, or "
            "geometry authority."
        ),
        final_checkpoint="W05_SHIPPED_INTEGRATION_READY",
    ),
)


def reconcile_text(source: str, repair: FinalWriterRepair) -> str:
    stale_count = source.count(repair.stale_fragment)
    replacement_count = source.count(repair.replacement)
    if stale_count == 1 and replacement_count == 0:
        return source.replace(repair.stale_fragment, repair.replacement, 1)
    if stale_count == 0 and replacement_count == 1:
        return source
    raise AssertionError(
        f"{repair.path.relative_to(ROOT)} must contain exactly one stale or repaired form"
    )


def reconciled_source(repair: FinalWriterRepair) -> str:
    return reconcile_text(repair.path.read_text(encoding="utf-8"), repair)


def repair_for(relative_path: str) -> FinalWriterRepair:
    return next(repair for repair in REPAIR_INPUTS if repair.path == ROOT / relative_path)


class CoreCurrentProjectionTests(unittest.TestCase):
    def test_domain_rules_coverage_remains_absent_from_all_runtime_paths_and_references(self) -> None:
        historical_path = CORE / "DOMAIN_RULES_COVERAGE.md"

        self.assertFalse(historical_path.exists())
        historical_hits = []
        for game_path in GAME.rglob("*"):
            relative_path = game_path.relative_to(GAME).as_posix()
            if any(alias.casefold() in relative_path.casefold() for alias in HISTORICAL_RUNTIME_DOMAIN_ALIASES):
                historical_hits.append(relative_path)
            if game_path.is_file():
                source = game_path.read_bytes().lower()
                for alias in HISTORICAL_RUNTIME_DOMAIN_ALIASES:
                    if alias.casefold().encode("utf-8") in source:
                        historical_hits.append(f"{relative_path}: {alias}")

        self.assertEqual([], historical_hits)

    def test_repair_inputs_have_the_exact_six_path_to_final_writer_mapping(self) -> None:
        actual_paths = {repair.path for repair in REPAIR_INPUTS}
        actual_mapping = {
            path: {repair.final_checkpoint for repair in REPAIR_INPUTS if repair.path == path}
            for path in actual_paths
        }

        self.assertEqual(set(EXPECTED_FINAL_WRITERS), actual_paths)
        self.assertEqual(
            {path: {checkpoint} for path, checkpoint in EXPECTED_FINAL_WRITERS.items()},
            actual_mapping,
        )

    def test_nonshared_core_repair_inputs_flow_to_the_wave_five_shipped_integration_writer(self) -> None:
        expected_paths = ("GAME/CORE/RANDOMNESS.md", "GAME/CORE/EXPLORATION.md")

        for relative_path in expected_paths:
            self.assertEqual("W05_SHIPPED_INTEGRATION_READY", repair_for(relative_path).final_checkpoint)


class DomainExplorationTests(unittest.TestCase):
    def test_spatial_repair_input_replaces_the_stale_generalized_map_instruction(self) -> None:
        repair = repair_for("GAME/CORE/EXPLORATION.md")
        projected = reconciled_source(repair)

        self.assertIn("bounded location/procedure/applicability facts", repair.replacement)
        self.assertIn("Do not introduce a generic spatial record/map", repair.replacement)
        self.assertNotIn(repair.stale_fragment, projected)
        self.assertIn(repair.replacement, projected)


class InstallProjectionTests(unittest.TestCase):
    def test_install_repair_inputs_cover_supported_profile_and_fixed_connector_transport(self) -> None:
        expected_paths = {
            ROOT / "GAME/INSTALL/README.md",
            ROOT / "GAME/INSTALL/PROJECT_INSTRUCTIONS.txt",
            ROOT / "GAME/INSTALL/00_DND_BOOTSTRAP.md",
            ROOT / "GAME/CORE/BOOTSTRAP_RUNTIME.md",
        }

        actual_paths = {repair.path for repair in REPAIR_INPUTS}
        self.assertTrue(expected_paths <= actual_paths)
        for path in expected_paths:
            repairs = [repair for repair in REPAIR_INPUTS if repair.path == path]
            self.assertTrue(repairs, path)
            for repair in repairs:
                expected_checkpoint = (
                    CORE_BOOTSTRAP_FINAL_CHECKPOINT
                    if path == CORE / "BOOTSTRAP_RUNTIME.md"
                    else INSTALL_FINAL_CHECKPOINT
                )
                self.assertEqual(expected_checkpoint, repair.final_checkpoint)
                projected = reconciled_source(repair)
                self.assertIn(repair.replacement, projected)
                if repair.stale_fragment not in repair.replacement:
                    self.assertNotIn(repair.stale_fragment, projected)

    def test_repaired_project_instructions_remain_identical_in_both_install_projections(self) -> None:
        readme = (INSTALL / "README.md").read_text(encoding="utf-8")
        for repair in REPAIR_INPUTS:
            if repair.path == INSTALL / "README.md":
                readme = reconcile_text(readme, repair)

        marker = "```text\n"
        embedded = readme.split(marker, 1)[1].split("\n```", 1)[0]
        instructions = (INSTALL / "PROJECT_INSTRUCTIONS.txt").read_text(encoding="utf-8")
        for repair in REPAIR_INPUTS:
            if repair.path == INSTALL / "PROJECT_INSTRUCTIONS.txt":
                instructions = reconcile_text(instructions, repair)

        self.assertEqual(embedded, instructions.rstrip("\n"))

    def test_repair_inputs_are_idempotent_after_the_final_writer_applies_them(self) -> None:
        for repair in REPAIR_INPUTS:
            self.assertEqual(repair.replacement, reconcile_text(repair.replacement, repair))

    def test_reconciliation_requires_exactly_one_stale_or_repaired_form_and_one_replacement(self) -> None:
        for repair in REPAIR_INPUTS:
            self.assertEqual(repair.replacement, reconcile_text(repair.stale_fragment, repair))
            self.assertEqual(repair.replacement, reconcile_text(repair.replacement, repair))
            for invalid_source in (
                "",
                repair.stale_fragment * 2,
                repair.replacement * 2,
                repair.stale_fragment + repair.replacement,
            ):
                with self.assertRaises(AssertionError):
                    reconcile_text(invalid_source, repair)


class RandomnessProjectionTests(unittest.TestCase):
    def test_fixed_rng_repair_input_preserves_recovery_reuse_without_trace_bloat(self) -> None:
        repair = repair_for("GAME/CORE/RANDOMNESS.md")
        projected = reconciled_source(repair)

        self.assertIn("Resolution or Continuation", repair.replacement)
        self.assertIn("restore and reuse it rather than rerolling", repair.replacement)
        self.assertIn("does not require Git logging every trivial roll", repair.replacement)
        self.assertNotIn(repair.stale_fragment, projected)
        self.assertIn(repair.replacement, projected)


if __name__ == "__main__":
    unittest.main()
