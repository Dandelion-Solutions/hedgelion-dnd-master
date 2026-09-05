from __future__ import annotations

import json
import re
import unittest
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / "GAME"
DEV = ROOT / "DEV"

SEARCH_FAMILIES = (
    r"engine_version",
    r"framework_module_version",
    r"runtime_bootstrap_version",
    r"launcher_version",
    r"launcher_revision",
    r"schema_version",
    r"\b\w+_schema_version\b",
    r"\b\w+_revision\b",
    r"\b\w+_generation\b",
    r"storage_format_version",
    r"storage_format_generation",
    r"catalog_version",
    r"catalog_generation",
    r"package_version",
    r"package_revision",
    r"compatibility_id",
    r"compatibility_family",
    r"compatibility_generation",
    r"ruleset_set_sha256",
    r"catalog_context_fingerprint",
    r"_V1",
    r"\.v1\b",
    r"\b0\.9\.\d+\b",
    r"\b1\.1\.\d+\b",
    r"\b2\.0\.0\b",
    r"\b1\.6\.0\b",
    r"\b1\.2\.0\b",
    r"\bv\d+(?:\.\d+){0,2}(?:[-.][A-Za-z0-9]+)*\b",
    r"\b\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?\b",
)
SEARCH_RE = re.compile("|".join(f"(?:{p})" for p in SEARCH_FAMILIES))
CORE_VERSION_RE = re.compile(r"(?m)^framework_module_version:\s*(\d+)\.(\d+)\.(\d+)\s*$")

HISTORICAL_DOC_PREFIXES = (
    "DEV/docs/superpowers/research/",
    "DEV/docs/superpowers/design/",
    "DEV/docs/superpowers/plans/",
)
EXTERNAL_PATHS = {
    ".github/workflows/release-runtime.yml",
    ".github/workflows/validate.yml",
}


def _iter_text_files():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith((".git/", ".hdm-devtools/", ".pytest_cache/", "__pycache__/")):
            continue
        if any(part == "__pycache__" for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        yield rel, text


def _classify(rel: str, text: str, start: int, end: int) -> str:
    context = text[max(0, start - 100): min(len(text), end + 100)].lower()
    if rel.startswith(HISTORICAL_DOC_PREFIXES):
        return "HISTORICAL_PROVENANCE"
    if rel.startswith("DEV/TESTS/"):
        if any(word in context for word in ("legacy", "invalid", "reject", "negative", "stale", "wrong", "old_")):
            return "INTENTIONAL_NEGATIVE_FIXTURE"
        return "CURRENT_TEST_OR_FIXTURE"
    if rel in EXTERNAL_PATHS or rel in {"pyproject.toml", "requirements.txt", "requirements-dev.txt"}:
        return "EXTERNAL_VERSION_NAMESPACE"
    if rel.startswith(("DEV/CATALOG/", "DEV/SCHEMAS/", "DEV/TOOLS/")) or rel in {
        "DEV/ENGINE_DEVELOPMENT.yaml",
        "GAME/ENGINE_VERSION.yaml",
    }:
        return "CURRENT_MACHINE_OR_RUNTIME"
    if rel.startswith("GAME/"):
        return "CURRENT_MACHINE_OR_RUNTIME" if path_is_machine(rel) else "CURRENT_NORMATIVE_DOCUMENTATION"
    if rel.startswith(("DEV/ARCHITECTURE/", "DEV/RELEASE/")) or rel in {
        "DEV/PROJECT_MAP.md", "DEV/CURRENT_PROGRESS.md", "AGENTS.md", "README.md",
    }:
        return "CURRENT_NORMATIVE_DOCUMENTATION"
    if rel.startswith("DEV/"):
        return "CURRENT_NORMATIVE_DOCUMENTATION"
    return "NON_VERSION_SEMANTIC_IDENTIFIER"


def path_is_machine(rel: str) -> bool:
    return rel.endswith((".json", ".yaml", ".yml", ".py")) or rel.startswith((
        "GAME/TOOLS/", "GAME/RULES/", "GAME/SCHEMA/", "GAME/CAMPAIGN/", "GAME/TEMPLATE/",
    ))


def census():
    counts = Counter()
    unclassified = []
    examples = {}
    for rel, text in _iter_text_files():
        for match in SEARCH_RE.finditer(text):
            disposition = _classify(rel, text, match.start(), match.end())
            if not disposition:
                unclassified.append((rel, match.group(0)))
                continue
            counts[disposition] += 1
            examples.setdefault(disposition, [])
            if len(examples[disposition]) < 12:
                examples[disposition].append(f"{rel}:{match.group(0)}")
    return counts, examples, unclassified


class VersionNamespacePolicyTests(unittest.TestCase):
    def test_census_has_zero_unclassified_hits(self):
        counts, examples, unclassified = census()
        print("VERSION_CENSUS=" + json.dumps({"counts": counts, "examples": examples}, sort_keys=True))
        self.assertEqual(unclassified, [])

    def test_release_manifests_project_campaign_contract_generation(self):
        dev = yaml.safe_load((DEV / "ENGINE_DEVELOPMENT.yaml").read_text(encoding="utf-8"))
        game = yaml.safe_load((GAME / "ENGINE_VERSION.yaml").read_text(encoding="utf-8"))
        for name, data in (("DEV", dev), ("GAME", game)):
            self.assertNotIn("schema_version", data, name)
            self.assertEqual(data.get("campaign_contract_generation"), 2, name)
            self.assertEqual(data.get("engine_version"), "1.0-alpha", name)
            self.assertEqual(data.get("recommended_tag"), "v1.0-alpha", name)
        self.assertEqual(dev["campaign_contract_generation"], game["campaign_contract_generation"])

    def test_all_versioned_core_modules_use_canonical_header_and_real_engine_lines(self):
        bad = []
        for path in sorted((GAME / "CORE").glob("*.md")):
            text = path.read_text(encoding="utf-8")
            if path.name in {"README.md", "SOURCES.md"}:
                continue
            if "runtime_bootstrap_version:" in text:
                bad.append(f"{path.name}: runtime_bootstrap_version")
                continue
            match = CORE_VERSION_RE.search(text)
            if not match:
                bad.append(f"{path.name}: missing framework_module_version")
                continue
            major, minor, _revision = map(int, match.groups())
            if (major, minor) == (0, 9) or (major, minor) > (1, 0):
                bad.append(f"{path.name}: {match.group(0)}")
        self.assertEqual(bad, [])

    def test_history_reconstructed_core_versions(self):
        expected = {
            "ADJUDICATION.md": "1.0.2",
            "CHARACTER.md": "1.0.1",
            "CHARACTER_READINESS.md": "1.0.3",
            "DIEGETIC_ONBOARDING.md": "1.0.2",
            "DURABILITY_GUARD.md": "1.0.1",
            "ENGINE_UPDATES.md": "1.0.3",
        }
        actual = {}
        for name in expected:
            text = (GAME / "CORE" / name).read_text(encoding="utf-8")
            match = CORE_VERSION_RE.search(text)
            actual[name] = ".".join(match.groups()) if match else None
        self.assertEqual(actual, expected)

    def test_current_machine_legacy_names_are_absent(self):
        forbidden = (
            "runtime_bootstrap_version", "storage_format_version", "launcher_version",
            "catalog_version", 'catalog_generation": "2.0.0"', "package_version", "compatibility_id",
            "HDM_RULESET_PACKAGE_SNAPSHOT_V1", "HDM_RESOLVED_RULESET_SET_V1",
            "HDM_RULESET_SEMANTIC_ENTRY_V1", "HDM_RULESET_COMPATIBILITY_EVIDENCE_V1",
            "HDM_RULESET_ENGINE_CONTRACT_INVENTORY_V1", "HDM_RULESET_CONFORMANCE_ATTESTATION_V1",
        )
        bad = []
        current_machine_prefixes = (
            "GAME/", "DEV/CATALOG/", "DEV/SCHEMAS/", "DEV/TOOLS/",
        )
        for rel, text in _iter_text_files():
            if rel.startswith("DEV/TESTS/") or rel.startswith(HISTORICAL_DOC_PREFIXES):
                continue
            if rel == "DEV/ENGINE_DEVELOPMENT.yaml" or rel.startswith(current_machine_prefixes):
                for token in forbidden:
                    if token in text:
                        bad.append(f"{rel}: {token}")
        self.assertEqual(bad, [])

    def test_ruleset_manifest_uses_normalized_identity_axes(self):
        path = GAME / "RULES/packages/hdm.rules.dnd2024-srd52-core/ruleset-package-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(manifest.get("manifest_schema_version"), 2)
        self.assertEqual(manifest.get("package_revision"), 1)
        self.assertEqual(manifest.get("compatibility_family"), "hdm.rules.dnd2024-srd52")
        self.assertEqual(manifest.get("compatibility_generation"), 1)
        self.assertEqual(manifest.get("catalog_generation"), 2)
        self.assertNotIn("package_version", manifest)
        self.assertNotIn("compatibility_id", manifest)


if __name__ == "__main__":
    unittest.main()
