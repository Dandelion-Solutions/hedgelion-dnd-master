# CORE Index

framework_module_version: 0.1.2
rules_baseline: D&D 2024 / SRD 5.2.1

During gameplay ALWAYS load:
- `RUNTIME.md` — turn pipeline, agency, causality and canon boundaries.
- `AI_REASONING.md` — LLM-specific correctness discipline, anti-sycophancy and commitment preservation.

Load every other module only when the current situation requires it.

- `BOOTSTRAP_RUNTIME.md` — campaign discovery/startup and runtime routing.
- `CAMPAIGN_SETUP.md` — create/initialize a new campaign branch.
- `GM_CRAFT.md` — high-level synthesis of established GM best practices; use for setup/prep/design/audit.
- `CAMPAIGN_OPERATIONS.md` — campaign/session organization and maintenance.
- `SESSION.md` — session start/resume/end/checkpoints.
- `CHARACTER.md` — PC creation and novice onboarding.
- `ADJUDICATION.md` — checks, uncertainty, consequences, temporary rulings.
- `RANDOMNESS.md` — actual RNG and dice integrity.
- `INFORMATION.md` — clues, mysteries, perception, knowledge boundaries.
- `NPC.md` — NPC agency, knowledge, relationships, personality continuity.
- `DIALOGUE.md` — dialogue and social interaction.
- `EXPLORATION.md` — locations, investigation, travel, time, resources.
- `ENCOUNTERS.md` — encounter objectives, difficulty and environment.
- `COMBAT.md` — combat runtime.
- `MAGIC.md` — spell/magic adjudication.
- `PROCESSES.md` — long-running threats, projects, clocks and off-screen change.
- `WORLDGEN.md` — create/expand world only to the required horizon.
- `LORE.md` — history, culture, disputed accounts and lore-reveal discipline.
- `REWARDS.md` — economy, payment, treasure and ownership.
- `ADVANCEMENT.md` — level-up, rest, downtime and long-term progression.
- `SAFETY.md` — campaign boundaries and tone.
- `NARRATIVE.md` — narration, pacing, information density, novice guidance.
- `PREP.md` — situation-based, high-value preparation and strong starts.
- `STORAGE.md` — canonical storage, batching, lazy retrieval and resync.
- `INTEGRITY.md` — incremental canon-integrity detection and bounded repair; load only on suspect/corrupt state or explicit integrity diagnosis.
- `MULTIPLAYER.md` — shared-world concurrency and environment-level conflict handling.
- `ANTIPATTERNS.md` — extended LLM-specific failure catalogue for audits/debugging.
- `SOURCES.md` — research provenance; never load during normal gameplay.

Recommended bundles:

`new campaign` -> RUNTIME + AI_REASONING + GM_CRAFT + CAMPAIGN_OPERATIONS + CAMPAIGN_SETUP + CHARACTER + SAFETY + WORLDGEN.

`session prep/start` -> RUNTIME + AI_REASONING + SESSION + CAMPAIGN_OPERATIONS + GM_CRAFT/PREP only if preparation is needed.

`lore/history` -> RUNTIME + AI_REASONING + LORE + INFORMATION, plus exact relevant world records.

Rules lookup policy:
1. established campaign house rules;
2. stored exact character/entity mechanics;
3. `RULES/` routing/local references;
4. official D&D 2024 / SRD 5.2.1 source when exact mechanics materially matter;
5. consequential rulings become explicit campaign rules if they must remain consistent.
