#!/usr/bin/env python3
"""Maintenance-only consistency/smoke audit for the HDM GAME/DEV source tree."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

REPO_ROOT = Path(__file__).resolve().parents[2]
DEV_ROOT = REPO_ROOT / "DEV"
GAME_ROOT = REPO_ROOT / "GAME"
ERRORS: list[str] = []
WARNINGS: list[str] = []


def require(cond: bool, msg: str) -> None:
    if not cond:
        ERRORS.append(msg)


def forbid(haystack: str, needle: str, where: str) -> None:
    if needle in haystack:
        ERRORS.append(f"stale/contradictory wording in {where}: {needle!r}")


def _text(root: Path, rel: str) -> str:
    p = root / rel
    if not p.is_file():
        ERRORS.append(f"missing required file: {p.relative_to(REPO_ROOT)}")
        return ""
    return p.read_text(encoding="utf-8")


def game_text(rel: str) -> str:
    return _text(GAME_ROOT, rel)


def dev_text(rel: str) -> str:
    return _text(DEV_ROOT, rel)


def repo_text(rel: str) -> str:
    return _text(REPO_ROOT, rel)


def parse_header_activation(src: str) -> tuple[str | None, str | None]:
    lp = re.search(r"(?m)^load_policy:\s*(.+)$", src)
    lw = re.search(r"(?m)^load_when:\s*(.+)$", src)
    return (lp.group(1).strip() if lp else None, lw.group(1).strip() if lw else None)


def audit_current_progress_authority() -> None:
    progress = dev_text('CURRENT_PROGRESS.md')
    required_progress = (
        'Status: **CANONICAL GLOBAL CURRENT-PROGRESS AUTHORITY**',
        'GLOBAL_PROGRAM:',
        'GLOBAL_STATE:',
        'CURRENT_WORKSTREAM:',
        'CURRENT_SLICE:',
        'LAST_CLOSED_UNIT:',
        'NEXT_AUTHORIZED_UNIT:',
        'REQUIRED_GATE:',
        'TASK_LOCAL_CURSOR:',
        'KNOWN_BLOCKERS:',
    )
    for marker in required_progress:
        require(marker in progress, f'CURRENT_PROGRESS.md missing required marker: {marker}')

    agents = repo_text('AGENTS.md')
    project_map = dev_text('PROJECT_MAP.md')
    design_process = dev_text('DESIGN_PROCESS.md')
    architecture_process = dev_text('ARCHITECTURE/DESIGN_PROCESS.md')
    roadmap = dev_text('ARCHITECTURE/NEAR_TERM_ROADMAP.md')
    canonical_index = dev_text('ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md')
    r27_cursor = dev_text('docs/superpowers/design/2026-08-24-r2-7-audit-status.md')

    for where, content in {
        'AGENTS.md': agents,
        'DEV/PROJECT_MAP.md': project_map,
        'DEV/DESIGN_PROCESS.md': design_process,
        'DEV/ARCHITECTURE/DESIGN_PROCESS.md': architecture_process,
        'DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md': canonical_index,
        'R2.7 task-local cursor': r27_cursor,
    }.items():
        require('DEV/CURRENT_PROGRESS.md' in content, f'{where} must route global progress through DEV/CURRENT_PROGRESS.md')

    require('NOT CURRENT-PROGRESS AUTHORITY' in roadmap, 'roadmap must disclaim global current-progress authority')
    require('This file is the sequencing/status authority' not in roadmap, 'roadmap must not claim sequencing/status authority')
    require('## 8. R2.7 current status' not in roadmap, 'roadmap must not retain a global R2.7 current-status section')
    require('## 9. Current continuation point' not in roadmap, 'roadmap must not retain a global continuation cursor')
    require('Architecture state:' not in canonical_index, 'canonical index must not retain a global architecture-state summary')
    require('TASK-LOCAL R2.7 AUDIT CURSOR — NOT GLOBAL CURRENT-PROGRESS AUTHORITY' in r27_cursor, 'R2.7 cursor must declare task-local scope')


def audit_layout_and_version() -> None:
    forbidden_root = {
        "CORE", "RULES", "SCHEMA", "CAMPAIGN", "TEMPLATE", "MIGRATIONS", "INSTALL",
        "TOOLS", "ARCHITECTURE", "TESTS", "RELEASE", "CATALOG", "SCHEMAS", "docs",
        "ENGINE_VERSION.yaml",
    }
    for name in sorted(forbidden_root):
        require(not (REPO_ROOT / name).exists(), f"old root ownership path must be absent: {name}")
    require(GAME_ROOT.is_dir(), "GAME root missing")
    require(DEV_ROOT.is_dir(), "DEV root missing")
    require((GAME_ROOT / "ENGINE_VERSION.yaml").is_file(), "GAME runtime marker missing")
    require((DEV_ROOT / "ENGINE_DEVELOPMENT.yaml").is_file(), "DEV version superset missing")
    markers = list(REPO_ROOT.rglob("ENGINE_VERSION.yaml"))
    require(markers == [GAME_ROOT / "ENGINE_VERSION.yaml"], f"ENGINE_VERSION.yaml must be unique: {markers}")
    require(not (GAME_ROOT / "TEMPLATE" / "CAMPAIGN_MANIFEST.yaml").exists(), "deprecated campaign manifest stub must be absent")
    require(not (REPO_ROOT / "docs").exists(), "repository-root docs/ must not reappear")

    try:
        dev = yaml.safe_load((DEV_ROOT / "ENGINE_DEVELOPMENT.yaml").read_text(encoding="utf-8"))
        game = yaml.safe_load((GAME_ROOT / "ENGINE_VERSION.yaml").read_text(encoding="utf-8"))
    except Exception as exc:
        ERRORS.append(f"version manifest parse failed: {exc}")
        return
    expected_game_fields = {
        "engine_version", "release_status", "repository", "engine_owner_login",
        "rules_baseline", "campaign_contract_generation", "campaign_update", "recommended_tag",
    }
    require(set(game or {}) == expected_game_fields, f"GAME version fields mismatch: {sorted(set(game or {}))}")
    for key in expected_game_fields:
        require(dev.get(key) == game.get(key), f"DEV/GAME version field differs: {key}")
    engine_version = str(game.get("engine_version") or "")
    require(bool(re.fullmatch(r"\d+\.\d+(?:-[0-9A-Za-z][0-9A-Za-z.-]*)?", engine_version)), "engine_version must use MAJOR.MINOR[-prerelease]")
    require(game.get("campaign_contract_generation") == 2, "campaign_contract_generation must be 2")
    require(game.get("recommended_tag") == f"v{engine_version}", "recommended_tag must exactly project engine_version")
    revision_fields = [key for key in game if key.endswith("_revision")]
    require(not revision_fields, f"GAME manifest leaked DEV revisions: {revision_fields}")
    require("schema_version" not in game, "GAME engine manifest must not carry aggregate schema_version")


def audit_core_activation() -> None:
    idx = game_text("CORE/CORE_INDEX.md")
    policy = game_text("CORE/PLAY_POLICY.md")
    core_files = sorted((GAME_ROOT / "CORE").glob("*.md"))
    ignored = {"README.md", "CORE_INDEX.md"}
    always = set()
    for p in core_files:
        if p.name in ignored:
            continue
        src = p.read_text(encoding="utf-8")
        lp, lw = parse_header_activation(src)
        require(bool(lp) ^ bool(lw), f"{p.relative_to(REPO_ROOT)} must declare exactly one of load_policy/load_when")
        if lp:
            require(lp == "ALWAYS_DURING_GAMEPLAY", f"unsupported load_policy in {p.relative_to(REPO_ROOT)}: {lp}")
            always.add(p.name)
        require(f"`{p.name}`" in idx, f"CORE_INDEX does not route {p.name}")
    expected = {
        "RUNTIME.md", "AI_REASONING.md", "PLAY_POLICY.md",
        "DURABILITY_GUARD.md", "MECHANICS_INTEGRITY.md", "CHARACTER_READINESS.md",
    }
    require(always == expected, f"always-active header set mismatch: found {sorted(always)}, expected {sorted(expected)}")
    for name in expected:
        require(f"`{name}`" in policy, f"PLAY_POLICY always-active roster missing {name}")
    require("Activation is header-driven" in policy, "PLAY_POLICY must state header-driven activation")
    require("complete local `CORE/*.md`" in policy, "PLAY_POLICY must retain full-CORE-once preload contract")


def audit_runtime_scope() -> None:
    policy = game_text("CORE/PLAY_POLICY.md")
    require("## Runtime scope firewall" in policy, "PLAY_POLICY must define runtime scope firewall")
    require("ENGINE_MAINTENANCE" in policy, "PLAY_POLICY must separate engine maintenance from campaign runtime")
    for leaked in ("`ARCHITECTURE/`", "`RELEASE/`", "`TESTS/`", "TOOLS/audit_engine.py", "DEV/"):
        require(leaked not in policy, f"GAME runtime policy must not name DEV-only path: {leaked}")
    for token in ("`CORE/`", "`RULES/`", "`SCHEMA/`", "`CAMPAIGN/`", "`TEMPLATE/`", "`INSTALL/`", "`MIGRATIONS/`", "`TOOLS/init_campaign.py`"):
        require(token in policy, f"PLAY_POLICY positive runtime scope missing {token}")


def audit_gm_guidance() -> None:
    setup = game_text("CORE/CAMPAIGN_SETUP.md")
    craft = game_text("CORE/GM_CRAFT.md")
    safety = game_text("CORE/SAFETY.md")
    runtime = game_text("CORE/RUNTIME.md")
    narrative = game_text("CORE/NARRATIVE.md")
    lore = game_text("CORE/LORE.md")
    ops = game_text("CORE/CAMPAIGN_OPERATIONS.md")
    policy = game_text("CORE/PLAY_POLICY.md")
    sources = game_text("CORE/SOURCES.md")
    require("Я — Мастер этой игры" in setup and "Кем хочешь играть?" in setup, "campaign setup must retain human Master introduction before protagonist prompt")
    require("This is an invitation, NOT a required genre/tone question" in setup, "campaign setup must keep genre/tone invitation optional")
    require("Do NOT require every player to rate mechanics" in setup and "Do NOT require the player to rate lore fidelity" in setup, "campaign setup must not regress into mandatory preference scales")
    require("Session Zero is a conversation, not a form" in craft, "GM_CRAFT must keep low-friction Session Zero doctrine")
    require("Do not hard-code a single humor style" in craft and "humor is a tool, not a quota" in craft.lower(), "GM_CRAFT must keep flexible humor doctrine")
    require("## Intent-preserving improvisation" in craft and "player's assertion inside an action is not automatically canon" in craft, "GM_CRAFT must preserve intent")
    require("## Worldbuilding through encounters" in craft and "generative abundance" in craft, "GM_CRAFT must adapt encounter/worldbuilding guidance")
    require("## Closure is part of good play" in craft and "Do not protect endlessness" in craft, "GM_CRAFT must allow genuine story closure")
    require("## Stop at meaningful player decision points" in narrative and "New material information beats autocomplete" in narrative, "NARRATIVE must prevent AI autocomplete")
    require("## Show the world doing something" in lore and "do not compensate for sparse context" in lore, "LORE must prefer concrete world manifestation")
    require("## Arc resolution and campaign closure" in ops and "zero urgent conflicts" in ops and "does not need a teaser for a sequel" in ops, "CAMPAIGN_OPERATIONS must preserve real closure")
    require("Broad expectation disclosure without spoilers" in safety, "SAFETY must keep targeted heavy-theme expectation disclosure")
    require("Out-of-character Master channel" in runtime and "Мастер" in runtime and "Master" in runtime, "RUNTIME must preserve explicit Master OOC channel")
    require("GM craft guidance is local runtime knowledge" in policy and "do NOT browse D&D Beyond" in policy, "PLAY_POLICY must keep GM-advice web lookup out of runtime")
    require("D&D Beyond — Session Zero" in sources and "929-how-to-run-a-session-0" in sources and "881-creating-terror" in sources, "SOURCES must retain audited tone/onboarding provenance")
    require("160-improvisation-in-d-d-for-new-dungeon-masters" in sources and "769-worldbuilding-through-encounters" in sources, "SOURCES must retain audited improvisation/worldbuilding provenance")


def audit_no_stale_policy() -> None:
    files = {
        "CORE/AI_REASONING.md": game_text("CORE/AI_REASONING.md"),
        "CORE/RUNTIME.md": game_text("CORE/RUNTIME.md"),
        "CORE/STORAGE.md": game_text("CORE/STORAGE.md"),
        "CORE/SESSION.md": game_text("CORE/SESSION.md"),
        "CORE/CAMPAIGN_OPERATIONS.md": game_text("CORE/CAMPAIGN_OPERATIONS.md"),
        "CORE/NEW_CAMPAIGN_FAST_PATH.md": game_text("CORE/NEW_CAMPAIGN_FAST_PATH.md"),
        "CORE/CAMPAIGN_SETUP.md": game_text("CORE/CAMPAIGN_SETUP.md"),
        "INSTALL/00_DND_BOOTSTRAP.md": game_text("INSTALL/00_DND_BOOTSTRAP.md"),
        "RELEASE/CHECKLIST.md": dev_text("RELEASE/CHECKLIST.md"),
    }
    forbid(files["CORE/AI_REASONING.md"], "preload all CORE/WORLD/LOG", "CORE/AI_REASONING.md")
    forbid(files["CORE/RUNTIME.md"], "Drop it when the scene moves on", "CORE/RUNTIME.md")
    forbid(files["CORE/STORAGE.md"], "Stable-ID reservation remains HARD", "CORE/STORAGE.md")
    forbid(files["CORE/STORAGE.md"], "meaningful action-sequence completion, scene/encounter transition", "CORE/STORAGE.md")
    forbid(files["CORE/SESSION.md"], "Persistence boundaries include meaningful action-sequence completion", "CORE/SESSION.md")
    forbid(files["CORE/CAMPAIGN_OPERATIONS.md"], "natural persistence boundary under `RUNTIME.md` / `PERSISTENCE.md`", "CORE/CAMPAIGN_OPERATIONS.md")
    forbid(files["CORE/NEW_CAMPAIGN_FAST_PATH.md"], "Normally perform ZERO campaign GitHub writes while", "CORE/NEW_CAMPAIGN_FAST_PATH.md")
    forbid(files["CORE/CAMPAIGN_SETUP.md"], "obtain explicit player acceptance", "CORE/CAMPAIGN_SETUP.md")
    forbid(files["RELEASE/CHECKLIST.md"], "full engine is not preloaded", "DEV/RELEASE/CHECKLIST.md")
    require("header-driven" in files["INSTALL/00_DND_BOOTSTRAP.md"], "bootstrap must use header-driven activation")


def audit_persistence_ownership() -> None:
    dur = game_text("CORE/DURABILITY_GUARD.md")
    pers = game_text("CORE/PERSISTENCE.md")
    save = game_text("CORE/SAVE_CONTRACT.md")
    storage = game_text("CORE/STORAGE.md")
    session = game_text("CORE/SESSION.md")
    require("authoritative for deciding WHEN" in dur, "DURABILITY_GUARD must own ordinary publication timing")
    require("does not create ordinary gameplay save boundaries" in pers, "PERSISTENCE must explicitly be HOW-only")
    require("does not invent additional timing rules" in storage, "STORAGE must defer timing to DURABILITY_GUARD")
    require("does not automatically" in session or "not automatically" in session, "SESSION must not invent per-scene boundaries")
    require(("unfinished pre-live setup" in save or "unfinished pre-live onboarding" in save) and "`initializing`" in save, "SAVE_CONTRACT must preserve initializing during unfinished onboarding")
    require("`paused` is reserved" in dur, "DURABILITY_GUARD must define paused as post-PLAY_READY")


def audit_onboarding_and_identity() -> None:
    onboarding = game_text("CORE/DIEGETIC_ONBOARDING.md")
    fast = game_text("CORE/NEW_CAMPAIGN_FAST_PATH.md")
    setup = game_text("CORE/CAMPAIGN_SETUP.md")
    ready = game_text("CORE/CHARACTER_READINESS.md")
    ident = game_text("CORE/CAMPAIGN_IDENTITY.md")
    card = game_text("CORE/CAMPAIGN_CARD.md")
    char = game_text("CORE/CHARACTER.md")
    require("PROVISIONAL_IDENTITY" in onboarding and "`initializing`" in onboarding, "diegetic onboarding must define provisional identity")
    require("PROVISIONAL_IDENTITY" in fast, "new-campaign fast path must acknowledge provisional identity exception")
    require("semantic" in setup.lower() and "PROVISIONAL_IDENTITY" in setup, "campaign setup must use semantic acceptance")
    require("READY_PC is not a gate" in ready and "provisional PC" in ready, "character readiness must preserve gameplay-first provisional onboarding")
    require("Эмо-вампир в мире розовых пони и радужных единорогов" in ident, "campaign identity should preserve early title example")
    require("exact projection" in ident and "MANIFEST.campaign_name" in ident, "campaign identity must define exact card projection")
    require("player retains final authority" in char and "player-authored identity fields" in onboarding, "character authority must distinguish seeded vs player-authored facts")
    require("paused" in card and "unfinished" in card, "card lifecycle must distinguish unfinished setup from paused play")


def audit_schema_and_templates() -> None:
    manifest = game_text("CAMPAIGN/MANIFEST.yaml")
    m_schema = game_text("SCHEMA/campaign_manifest.schema.yaml")
    storage_schema = game_text("SCHEMA/dnd_storage.schema.yaml")
    c_schema = game_text("SCHEMA/campaign_card.schema.yaml")
    pc_schema = game_text("SCHEMA/pc.schema.yaml")
    readme = game_text("CAMPAIGN/README.md")
    require("schema_version: 4" in manifest, "campaign scaffold manifest must use schema_version 4")
    require("campaign_contract:" in manifest and "created_with: 2" in manifest and "current: 2" in manifest, "campaign scaffold manifest must carry campaign contract generation 2")
    require("ruleset_set_digest_generation: 1" in manifest, "campaign scaffold manifest must carry ruleset digest generation")
    require("created_with:" in manifest and "package_sha256:" in manifest, "campaign scaffold manifest must use portable runtime identity")
    for stale in ("base_tag:", "base_sha:", "integrated_tag:", "integrated_main_sha:"):
        require(stale not in manifest, f"campaign scaffold manifest leaked legacy engine field: {stale}")
    require("campaign_name_origin: null" in manifest, "campaign scaffold manifest must initialize campaign_name_origin")
    require("schema_version: 4" in m_schema and "campaign_contract:" in m_schema and "package_sha256:" in m_schema, "manifest schema must define runtime identity v4")
    require("campaign_name_origin" in m_schema, "manifest schema must define campaign_name_origin")
    require("READY_PC" in m_schema and "PLAY_READY" in m_schema, "manifest schema must encode active lifecycle gate")
    require("schema_version: 4" in storage_schema and "storage_format_generation:" in storage_schema and "storage_format_version" not in storage_schema, "storage schema must define generation-based portable storage v4")
    require("MANIFEST.campaign_name" in c_schema and "including null" in c_schema, "card schema must encode exact name projection")
    require("DM-seeded" in pc_schema and "player_defined_traits" in pc_schema, "PC schema must encode seeded/player-authored distinction")
    markers = [
        "DND_MASTER:CAMPAIGN_OVERVIEW_BEGIN", "DND_MASTER:CAMPAIGN_OVERVIEW_END",
        "DND_MASTER:PLAYER_GUIDE_BEGIN", "DND_MASTER:PLAYER_GUIDE_END",
    ]
    for marker in markers:
        require(readme.count(marker) == 1, f"campaign README must contain marker exactly once: {marker}")
    pos = [readme.find(m) for m in markers]
    require(pos == sorted(pos), "campaign README markers are out of order")
    require(not (GAME_ROOT / "TEMPLATE/CAMPAIGN_MANIFEST.yaml").exists(), "deprecated template stub must stay deleted")


def audit_json_schemas() -> None:
    schemas: dict[str, dict] = {}
    for path in sorted((DEV_ROOT / "SCHEMAS").glob("*.schema.json")):
        rel = str(path.relative_to(REPO_ROOT))
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            schemas[path.name] = schema
        except Exception as exc:
            ERRORS.append(f"invalid JSON Schema {rel}: {exc}")
    required_step3_schemas = (
        "invocation-fact.schema.json",
        "intent-clause.schema.json",
        "runtime-intent-plan-state.schema.json",
        "runtime-command-state.schema.json",
        "runtime-procedure-state.schema.json",
        "runtime-resolution-state.schema.json",
        "runtime-continuation-state.schema.json",
        "execution-segment.schema.json",
        "runtime-mechanical-event-state.schema.json",
        "pending-child-invocation.schema.json",
        "resolution-receipt.schema.json",
        "boundary-occurrence.schema.json",
    )
    for required_schema in required_step3_schemas:
        require(required_schema in schemas, f"missing Step-3 schema: {required_schema}")
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema))
        for schema in schemas.values() if "$id" in schema
    )
    for schema_name, schema in schemas.items():
        validator = Draft202012Validator(schema, registry=registry)
        for index, example in enumerate(schema.get("examples", [])):
            try:
                validator.validate(example)
            except Exception as exc:
                ERRORS.append(f"invalid example {index} in DEV/SCHEMAS/{schema_name}: {exc}")
    instance_pairs = {
        "core-catalog.schema.json": "core-catalog.json",
        "entity-structures.schema.json": "entity-structures.json",
        "identifier-policies.schema.json": "identifier-policies.json",
        "mechanical-surfaces.schema.json": "mechanical-surfaces.json",
    }
    for schema_name, filename in instance_pairs.items():
        schema = schemas.get(schema_name)
        if schema is None:
            continue
        try:
            instance = json.loads((DEV_ROOT / "CATALOG" / filename).read_text(encoding="utf-8"))
            Draft202012Validator(schema, registry=registry).validate(instance)
        except Exception as exc:
            ERRORS.append(f"invalid catalog instance DEV/CATALOG/{filename}: {exc}")
    try:
        core = json.loads((DEV_ROOT / "CATALOG/core-catalog.json").read_text(encoding="utf-8"))
        structures = json.loads((DEV_ROOT / "CATALOG/entity-structures.json").read_text(encoding="utf-8"))
        identifiers = json.loads((DEV_ROOT / "CATALOG/identifier-policies.json").read_text(encoding="utf-8"))
        surfaces = json.loads((DEV_ROOT / "CATALOG/mechanical-surfaces.json").read_text(encoding="utf-8"))
        require(
            core["catalog_generation"] == structures["catalog_generation"] == identifiers["catalog_generation"] == surfaces["catalog_generation"] == 2,
            "all coordinated machine catalogs must use catalog_generation 2",
        )
        require(set(core["registries"]["content_definition_kinds"]) == set(structures["definitions"]), "content_definition_kinds and entity-structure definition keys differ")
        require(set(core["registries"]["world_record_kinds"]) == set(structures["world_records"]), "world_record_kinds and entity-structure world-record keys differ")
    except Exception as exc:
        ERRORS.append(f"catalog cross-validation failed: {exc}")


def audit_tests() -> None:
    pt = dev_text("TESTS/PERSISTENCE_TRANSACTION_CASES.md")
    do = dev_text("TESTS/DIEGETIC_ONBOARDING_CASES.md")
    ci = dev_text("TESTS/CAMPAIGN_IDENTITY_CASES.md")
    bs = dev_text("TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md")
    ec = dev_text("TESTS/ENGINE_CONSISTENCY_CASES.md")
    gt = dev_text("TESTS/GM_TONE_ONBOARDING_CASES.md")
    ad = dev_text("TESTS/AI_DM_CRAFT_CASES.md")
    require("PT30" in pt and "Narrow race after commit" in pt and "README guide" in pt, "persistence regressions must cover concurrency + path preservation")
    require("DO14" in do and "Explicit save during onboarding" in do, "diegetic onboarding regression coverage incomplete")
    require("CI13" in ci and "Card never invents" in ci, "campaign identity regression coverage incomplete")
    require("adopted identity" in bs.lower() or "PROVISIONAL_IDENTITY" in bs, "bootstrap regression must not demand zero writes through adopted identity")
    require("EC15" in ec and "maintenance-only" in ec.lower(), "engine consistency cases must protect gameplay/maintenance separation")
    require("GT01" in gt and "GT13" in gt and "GM advice is local" in gt, "GM tone/onboarding regressions must cover human opening and local guidance")
    require("ADC01" in ad and "ADC16" in ad and "automatic sequel hook" in ad, "AI DM craft regressions must cover intent, decision points, worldbuilding and closure")
    for path in sorted((DEV_ROOT / "TESTS").glob("*.md")):
        src = path.read_text(encoding="utf-8")
        ids = re.findall(r"(?m)^##\s+([A-Z]{1,4}\d+[a-z]?)\s+[—-]", src)
        seen: set[str] = set(); dupes: set[str] = set()
        for case_id in ids:
            if case_id in seen: dupes.add(case_id)
            seen.add(case_id)
        require(not dupes, f"duplicate regression case id(s) in {path.relative_to(REPO_ROOT)}: {sorted(dupes)}")


def audit_release_contracts() -> None:
    sys.path.insert(0, str(DEV_ROOT / "TOOLS"))
    import release_builder
    try:
        _dev_manifest, game_manifest = release_builder.load_and_validate_manifests(REPO_ROOT)
        recommended_tag = game_manifest["recommended_tag"]
        release_builder.validate_project_instructions_parity(GAME_ROOT / "INSTALL")
        for root_name in ("LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md"):
            require((REPO_ROOT / root_name).read_bytes() == (GAME_ROOT / root_name).read_bytes(), f"GAME/{root_name} differs from root canonical copy")
        require((REPO_ROOT / "LICENSES/SRD-5.2.1-ATTRIBUTION.md").read_bytes() == (GAME_ROOT / "LICENSES/SRD-5.2.1-ATTRIBUTION.md").read_bytes(), "GAME LICENSES attribution differs from root copy")
        active = {
            "README.md": repo_text("README.md"),
            "GAME/INSTALL/README.md": game_text("INSTALL/README.md"),
            "GAME/CORE/ENGINE_UPDATES.md": game_text("CORE/ENGINE_UPDATES.md"),
            "DEV/RELEASE/CHECKLIST.md": dev_text("RELEASE/CHECKLIST.md"),
        }
        for where, src in active.items():
            require("runtime" in src.lower(), f"{where} must identify the custom runtime asset")
            if "Source code" in src:
                require(
                    any(token in src.lower() for token in ("not install", "not gameplay", "not runtime", "не установ", "не является")),
                    f"{where} mentions GitHub source archives without explicitly rejecting them as runtime installation artifacts",
                )
        with tempfile.TemporaryDirectory(prefix="hdm-release-audit-") as td:
            out = Path(td)
            z1 = release_builder.build_runtime_zip(REPO_ROOT, out, recommended_tag)
            h1 = z1.read_bytes()
            z1.unlink()
            z2 = release_builder.build_runtime_zip(REPO_ROOT, out, recommended_tag)
            require(h1 == z2.read_bytes(), "runtime ZIP is not byte-reproducible")
            with zipfile.ZipFile(z2) as zf:
                names = zf.namelist()
                require("ENGINE_VERSION.yaml" in names and "RUNTIME_PACKAGE.yaml" in names and "CORE/PLAY_POLICY.md" in names and "TOOLS/init_campaign.py" in names, "runtime ZIP missing required root members")
                require(not any(n.startswith(("GAME/", "DEV/")) for n in names), "runtime ZIP contains GAME/DEV wrapper")
                zf.extractall(out / "extract")
            release_builder.validate_extracted_package_root(out / "extract")
    except Exception as exc:
        ERRORS.append(f"release contract audit failed: {exc}")


def smoke_generator() -> None:
    script = GAME_ROOT / "TOOLS/init_campaign.py"
    try:
        game_version = yaml.safe_load((GAME_ROOT / "ENGINE_VERSION.yaml").read_text(encoding="utf-8"))["engine_version"]
    except Exception as exc:
        ERRORS.append(f"cannot derive engine version for generator smoke: {exc}")
        return
    with tempfile.TemporaryDirectory(prefix="dnd-audit-") as td:
        out = Path(td) / "campaign"
        cmd = [
            sys.executable, str(script), "--output", str(out),
            "--campaign-id", "camp-audit", "--branch", "campaign/20990101",
            "--engine-version", str(game_version), "--package-id", f"dev-v{game_version}",
            "--package-sha256", "0" * 64,
            "--ruleset-set-sha256", "1" * 64,
            "--created-at", "2099-01-01T00:00:00+00:00",
            "--creator-github-login", "audit-user", "--mode", "singleplayer",
            "--source-root", str(GAME_ROOT),
        ]
        cp = subprocess.run(cmd, capture_output=True, text=True)
        require(cp.returncode == 0, f"init_campaign smoke failed: {cp.stderr.strip() or cp.stdout.strip()}")
        if cp.returncode != 0: return
        require((out / "MANIFEST.yaml").is_file(), "generator output missing root MANIFEST.yaml")
        require(not (out / "CAMPAIGN/MANIFEST.yaml").exists(), "generator incorrectly nests CAMPAIGN/MANIFEST.yaml")
        require(not (out / "DND_STORAGE.yaml").exists(), "generator leaked storage marker")
        manifest = (out / "MANIFEST.yaml").read_text(encoding="utf-8")
        card = (out / "CAMPAIGN_CARD.yaml").read_text(encoding="utf-8")
        readme = (out / "README.md").read_text(encoding="utf-8")
        require("schema_version: 4" in manifest, "generated MANIFEST must use schema_version 4")
        require("campaign_contract:" in manifest and "created_with: 2" in manifest and "current: 2" in manifest, "generated MANIFEST missing campaign contract generation")
        require("ruleset_set_digest_generation: 1" in manifest, "generated MANIFEST missing ruleset digest generation")
        require("status: initializing" in manifest, "generated MANIFEST must start initializing")
        require("campaign_name: null" in manifest and "campaign_name_origin: null" in manifest, "generated MANIFEST must start unnamed")
        require("created_with:" in manifest and "package_sha256:" in manifest, "generated MANIFEST missing portable runtime identity")
        for stale in ("base_tag:", "base_sha:", "integrated_tag:", "integrated_main_sha:"):
            require(stale not in manifest, f"generated MANIFEST leaked legacy engine field: {stale}")
        require("campaign_name: null" in card, "generated card must start with null campaign name")
        require("DND_MASTER:CAMPAIGN_OVERVIEW_BEGIN" in readme and "DND_MASTER:PLAYER_GUIDE_END" in readme, "generated README missing protected markers")


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    audit_layout_and_version()
    audit_current_progress_authority()
    audit_core_activation()
    audit_runtime_scope()
    audit_gm_guidance()
    audit_no_stale_policy()
    audit_persistence_ownership()
    audit_onboarding_and_identity()
    audit_schema_and_templates()
    audit_json_schemas()
    audit_tests()
    audit_release_contracts()
    smoke_generator()
    for w in WARNINGS: print(f"WARN: {w}")
    if ERRORS:
        for e in ERRORS: print(f"ERROR: {e}")
        print(f"FAIL: {len(ERRORS)} error(s)")
        return 1
    print("OK: engine consistency audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
