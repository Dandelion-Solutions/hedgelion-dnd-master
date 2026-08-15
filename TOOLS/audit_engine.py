#!/usr/bin/env python3
"""Maintenance-only consistency/smoke audit for the D&D Master engine tree.

This executable is for explicit engine development/release maintenance. It is NOT
part of campaign bootstrap, setup, gameplay, save, pause/resume, or campaign
integrity fast paths and must never be invoked automatically by runtime.

Standard-library only. Exits non-zero on normative contradictions or scaffold
smoke failure.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []


def text(rel: str) -> str:
    p = ROOT / rel
    if not p.is_file():
        ERRORS.append(f"missing required file: {rel}")
        return ""
    return p.read_text(encoding="utf-8")


def require(cond: bool, msg: str) -> None:
    if not cond:
        ERRORS.append(msg)


def forbid(haystack: str, needle: str, where: str) -> None:
    if needle in haystack:
        ERRORS.append(f"stale/contradictory wording in {where}: {needle!r}")


def parse_header_activation(src: str) -> tuple[str | None, str | None]:
    lp = re.search(r"(?m)^load_policy:\s*(.+)$", src)
    lw = re.search(r"(?m)^load_when:\s*(.+)$", src)
    return (lp.group(1).strip() if lp else None, lw.group(1).strip() if lw else None)


def audit_core_activation() -> None:
    idx = text("CORE/CORE_INDEX.md")
    policy = text("CORE/PLAY_POLICY.md")
    core_files = sorted((ROOT / "CORE").glob("*.md"))
    ignored = {"README.md", "CORE_INDEX.md"}
    always = set()

    for p in core_files:
        if p.name in ignored:
            continue
        src = p.read_text(encoding="utf-8")
        lp, lw = parse_header_activation(src)
        require(bool(lp) ^ bool(lw), f"{p.relative_to(ROOT)} must declare exactly one of load_policy/load_when")
        if lp:
            require(lp == "ALWAYS_DURING_GAMEPLAY", f"unsupported load_policy in {p.relative_to(ROOT)}: {lp}")
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
    policy = text("CORE/PLAY_POLICY.md")
    release = text("RELEASE/CHECKLIST.md")
    require("## Runtime scope firewall" in policy, "PLAY_POLICY must define runtime scope firewall")
    require("ENGINE_MAINTENANCE" in policy, "PLAY_POLICY must explicitly separate engine maintenance from campaign runtime")
    for token in ("`ARCHITECTURE/`", "`RELEASE/`", "`TESTS/`", "`TEMPLATE/`"):
        require(token in policy, f"PLAY_POLICY runtime firewall missing non-runtime area {token}")
    require("`TOOLS/audit_engine.py`" in policy and "MUST NOT run" in policy, "PLAY_POLICY must forbid engine audit during campaign runtime")
    require("`TOOLS/init_campaign.py`" in policy and "explicit New Game" in policy, "PLAY_POLICY must narrowly allow init_campaign only for New Game")
    require("regression tests" in policy and "py_compile" in policy, "PLAY_POLICY must forbid opportunistic development checks during gameplay")
    require("maintenance-only" in release.lower(), "release checklist must label audit_engine maintenance-only")

    bad_refs = []
    for p in sorted((ROOT / "CORE").glob("*.md")):
        if p.name == "PLAY_POLICY.md":
            continue
        if "TOOLS/audit_engine.py" in p.read_text(encoding="utf-8"):
            bad_refs.append(str(p.relative_to(ROOT)))
    require(not bad_refs, f"runtime CORE modules must not invoke/reference audit_engine outside PLAY_POLICY firewall: {bad_refs}")


def audit_gm_guidance() -> None:
    setup = text("CORE/CAMPAIGN_SETUP.md")
    craft = text("CORE/GM_CRAFT.md")
    safety = text("CORE/SAFETY.md")
    runtime = text("CORE/RUNTIME.md")
    narrative = text("CORE/NARRATIVE.md")
    lore = text("CORE/LORE.md")
    ops = text("CORE/CAMPAIGN_OPERATIONS.md")
    policy = text("CORE/PLAY_POLICY.md")
    sources = text("CORE/SOURCES.md")

    require("Я — Мастер этой игры" in setup and "Кем хочешь играть?" in setup, "campaign setup must retain human Master introduction before protagonist prompt")
    require("This is an invitation, NOT a required genre/tone question" in setup, "campaign setup must keep genre/tone invitation optional")
    require("Do NOT require every player to rate mechanics" in setup and "Do NOT require the player to rate lore fidelity" in setup, "campaign setup must not regress into mandatory preference scales")
    require("Session Zero is a conversation, not a form" in craft, "GM_CRAFT must keep low-friction Session Zero doctrine")
    require("Do not hard-code a single humor style" in craft and "humor is a tool, not a quota" in craft.lower(), "GM_CRAFT must keep flexible humor doctrine")
    require("## Intent-preserving improvisation" in craft and "player's assertion inside an action is not automatically canon" in craft, "GM_CRAFT must preserve intent without accepting player assertions as truth")
    require("## Worldbuilding through encounters" in craft and "generative abundance" in craft, "GM_CRAFT must adapt encounter/worldbuilding guidance for generative overproduction")
    require("## Closure is part of good play" in craft and "Do not protect endlessness" in craft, "GM_CRAFT must allow genuine story closure")
    require("## Stop at meaningful player decision points" in narrative and "New material information beats autocomplete" in narrative, "NARRATIVE must prevent AI autocomplete across new PC decisions")
    require("## Show the world doing something" in lore and "do not compensate for sparse context" in lore, "LORE must prefer concrete world manifestation without generative lore inflation")
    require("## Arc resolution and campaign closure" in ops and "zero urgent conflicts" in ops and "does not need a teaser for a sequel" in ops, "CAMPAIGN_OPERATIONS must preserve quiet aftermath and real closure")
    require("Broad expectation disclosure without spoilers" in safety, "SAFETY must keep targeted heavy-theme expectation disclosure")
    require("Out-of-character Master channel" in runtime and "Мастер" in runtime and "Master" in runtime, "RUNTIME must preserve explicit Master OOC channel")
    require("GM craft guidance is local runtime knowledge" in policy and "do NOT browse D&D Beyond" in policy, "PLAY_POLICY must keep GM-advice web lookup out of campaign runtime")
    require("D&D Beyond — Session Zero" in sources and "929-how-to-run-a-session-0" in sources and "881-creating-terror" in sources, "SOURCES must retain audited D&D Beyond tone/onboarding provenance")
    require("160-improvisation-in-d-d-for-new-dungeon-masters" in sources and "769-worldbuilding-through-encounters" in sources, "SOURCES must retain audited D&D Beyond improvisation/worldbuilding provenance")


def audit_no_stale_policy() -> None:
    files = {
        "CORE/AI_REASONING.md": text("CORE/AI_REASONING.md"),
        "CORE/RUNTIME.md": text("CORE/RUNTIME.md"),
        "CORE/STORAGE.md": text("CORE/STORAGE.md"),
        "CORE/SESSION.md": text("CORE/SESSION.md"),
        "CORE/CAMPAIGN_OPERATIONS.md": text("CORE/CAMPAIGN_OPERATIONS.md"),
        "CORE/NEW_CAMPAIGN_FAST_PATH.md": text("CORE/NEW_CAMPAIGN_FAST_PATH.md"),
        "CORE/CAMPAIGN_SETUP.md": text("CORE/CAMPAIGN_SETUP.md"),
        "INSTALL/00_DND_BOOTSTRAP.md": text("INSTALL/00_DND_BOOTSTRAP.md"),
        "RELEASE/CHECKLIST.md": text("RELEASE/CHECKLIST.md"),
    }
    forbid(files["CORE/AI_REASONING.md"], "preload all CORE/WORLD/LOG", "CORE/AI_REASONING.md")
    forbid(files["CORE/RUNTIME.md"], "Drop it when the scene moves on", "CORE/RUNTIME.md")
    forbid(files["CORE/STORAGE.md"], "Stable-ID reservation remains HARD", "CORE/STORAGE.md")
    forbid(files["CORE/STORAGE.md"], "meaningful action-sequence completion, scene/encounter transition", "CORE/STORAGE.md")
    forbid(files["CORE/SESSION.md"], "Persistence boundaries include meaningful action-sequence completion", "CORE/SESSION.md")
    forbid(files["CORE/CAMPAIGN_OPERATIONS.md"], "natural persistence boundary under `RUNTIME.md` / `PERSISTENCE.md`", "CORE/CAMPAIGN_OPERATIONS.md")
    forbid(files["CORE/NEW_CAMPAIGN_FAST_PATH.md"], "Normally perform ZERO campaign GitHub writes while", "CORE/NEW_CAMPAIGN_FAST_PATH.md")
    forbid(files["CORE/CAMPAIGN_SETUP.md"], "obtain explicit player acceptance", "CORE/CAMPAIGN_SETUP.md")
    forbid(files["RELEASE/CHECKLIST.md"], "full engine is not preloaded", "RELEASE/CHECKLIST.md")
    require("header-driven" in files["INSTALL/00_DND_BOOTSTRAP.md"], "bootstrap must use header-driven activation")


def audit_persistence_ownership() -> None:
    dur = text("CORE/DURABILITY_GUARD.md")
    pers = text("CORE/PERSISTENCE.md")
    save = text("CORE/SAVE_CONTRACT.md")
    storage = text("CORE/STORAGE.md")
    session = text("CORE/SESSION.md")
    require("authoritative for deciding WHEN" in dur, "DURABILITY_GUARD must own ordinary publication timing")
    require("does not create ordinary gameplay save boundaries" in pers, "PERSISTENCE must explicitly be HOW-only")
    require("does not invent additional timing rules" in storage, "STORAGE must defer timing to DURABILITY_GUARD")
    require("does not automatically" in session or "not automatically" in session, "SESSION must not invent per-scene boundaries")
    require(("unfinished pre-live setup" in save or "unfinished pre-live onboarding" in save) and "`initializing`" in save, "SAVE_CONTRACT must preserve initializing during unfinished onboarding")
    require("`paused` is reserved" in dur, "DURABILITY_GUARD must define paused as post-PLAY_READY")


def audit_onboarding_and_identity() -> None:
    onboarding = text("CORE/DIEGETIC_ONBOARDING.md")
    fast = text("CORE/NEW_CAMPAIGN_FAST_PATH.md")
    setup = text("CORE/CAMPAIGN_SETUP.md")
    ready = text("CORE/CHARACTER_READINESS.md")
    ident = text("CORE/CAMPAIGN_IDENTITY.md")
    card = text("CORE/CAMPAIGN_CARD.md")
    char = text("CORE/CHARACTER.md")

    require("PROVISIONAL_IDENTITY" in onboarding and "`initializing`" in onboarding, "diegetic onboarding must define provisional identity without activation")
    require("PROVISIONAL_IDENTITY" in fast, "new-campaign fast path must acknowledge provisional identity exception")
    require("semantic" in setup.lower() and "PROVISIONAL_IDENTITY" in setup, "campaign setup must use semantic acceptance and story-first checkpoint")
    require("pre-live" in ready and "true" in ready, "character readiness must distinguish pre-live onboarding from true live play")
    require("Эмо-вампир в мире розовых пони и радужных единорогов" in ident, "campaign identity should preserve early hero+world title example")
    require("exact projection" in ident and "MANIFEST.campaign_name" in ident, "campaign identity must define exact card projection")
    require("DM-seeded" in char and "player_defined_traits" in onboarding, "character authority must distinguish seeded vs player-authored facts")
    require("paused" in card and "unfinished" in card, "card lifecycle must distinguish unfinished setup from paused play")


def audit_schema_and_templates() -> None:
    manifest = text("CAMPAIGN/MANIFEST.yaml")
    m_schema = text("SCHEMA/campaign_manifest.schema.yaml")
    c_schema = text("SCHEMA/campaign_card.schema.yaml")
    pc_schema = text("SCHEMA/pc.schema.yaml")
    readme = text("CAMPAIGN/README.md")
    stub = text("TEMPLATE/CAMPAIGN_MANIFEST.yaml")

    require("campaign_name_origin: null" in manifest, "campaign scaffold manifest must initialize campaign_name_origin")
    require("campaign_name_origin" in m_schema, "manifest schema must define campaign_name_origin")
    require("READY_PC" in m_schema and "PLAY_READY" in m_schema, "manifest schema must encode active lifecycle gate")
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
    require("root MANIFEST.yaml" in stub, "deprecated template stub must describe root-layout output")


def audit_tests() -> None:
    pt = text("TESTS/PERSISTENCE_TRANSACTION_CASES.md")
    do = text("TESTS/DIEGETIC_ONBOARDING_CASES.md")
    ci = text("TESTS/CAMPAIGN_IDENTITY_CASES.md")
    bs = text("TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md")
    ec = text("TESTS/ENGINE_CONSISTENCY_CASES.md")
    gt = text("TESTS/GM_TONE_ONBOARDING_CASES.md")
    ad = text("TESTS/AI_DM_CRAFT_CASES.md")
    require("PT30" in pt and "Narrow race after commit" in pt and "README guide" in pt, "persistence regressions must cover concurrency + path preservation")
    require("DO14" in do and "Explicit save during onboarding" in do, "diegetic onboarding regression coverage incomplete")
    require("CI13" in ci and "Card never invents" in ci, "campaign identity regression coverage incomplete")
    require("adopted identity" in bs.lower() or "PROVISIONAL_IDENTITY" in bs, "bootstrap regression must not demand zero writes through adopted identity")
    require("EC15" in ec and "maintenance-only" in ec.lower(), "engine consistency cases must protect gameplay/maintenance separation")
    require("GT01" in gt and "GT13" in gt and "GM advice is local" in gt, "GM tone/onboarding regressions must cover human opening and local guidance")
    require("ADC01" in ad and "ADC16" in ad and "automatic sequel hook" in ad, "AI DM craft regressions must cover intent, decision points, worldbuilding and closure")

    # Duplicate case IDs make regression references ambiguous and usually indicate
    # a copy/paste oversight. Check each regression document independently.
    for path in sorted((ROOT / "TESTS").glob("*.md")):
        src = path.read_text(encoding="utf-8")
        ids = re.findall(r"(?m)^##\s+([A-Z]{1,4}\d+[a-z]?)\s+[—-]", src)
        seen: set[str] = set()
        dupes: set[str] = set()
        for case_id in ids:
            if case_id in seen:
                dupes.add(case_id)
            seen.add(case_id)
        require(not dupes, f"duplicate regression case id(s) in {path.relative_to(ROOT)}: {sorted(dupes)}")


def smoke_generator() -> None:
    script = ROOT / "TOOLS/init_campaign.py"
    with tempfile.TemporaryDirectory(prefix="dnd-audit-") as td:
        out = Path(td) / "campaign"
        cmd = [
            sys.executable, str(script),
            "--output", str(out),
            "--campaign-id", "camp-audit",
            "--branch", "campaign/20990101",
            "--engine-tag", "dev-v0.7",
            "--created-at", "2099-01-01T00:00:00+00:00",
            "--creator-github-login", "audit-user",
            "--mode", "singleplayer",
            "--source-root", str(ROOT),
        ]
        cp = subprocess.run(cmd, capture_output=True, text=True)
        require(cp.returncode == 0, f"init_campaign smoke failed: {cp.stderr.strip() or cp.stdout.strip()}")
        if cp.returncode != 0:
            return
        require((out / "MANIFEST.yaml").is_file(), "generator output missing root MANIFEST.yaml")
        require(not (out / "CAMPAIGN" / "MANIFEST.yaml").exists(), "generator incorrectly nests CAMPAIGN/MANIFEST.yaml")
        require(not (out / "DND_STORAGE.yaml").exists(), "generator leaked storage marker")
        m = (out / "MANIFEST.yaml").read_text(encoding="utf-8")
        card = (out / "CAMPAIGN_CARD.yaml").read_text(encoding="utf-8")
        readme = (out / "README.md").read_text(encoding="utf-8")
        require("status: initializing" in m, "generated MANIFEST must start initializing")
        require("campaign_name: null" in m and "campaign_name_origin: null" in m, "generated MANIFEST must start unnamed with null origin")
        require("campaign_name: null" in card, "generated card must start with null campaign name")
        require("DND_MASTER:CAMPAIGN_OVERVIEW_BEGIN" in readme and "DND_MASTER:PLAYER_GUIDE_END" in readme, "generated README missing protected markers")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    audit_core_activation()
    audit_runtime_scope()
    audit_gm_guidance()
    audit_no_stale_policy()
    audit_persistence_ownership()
    audit_onboarding_and_identity()
    audit_schema_and_templates()
    audit_tests()
    smoke_generator()

    if WARNINGS:
        for w in WARNINGS:
            print(f"WARN: {w}")
    if ERRORS:
        for e in ERRORS:
            print(f"ERROR: {e}")
        print(f"FAIL: {len(ERRORS)} error(s)")
        return 1
    print("OK: engine consistency audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
