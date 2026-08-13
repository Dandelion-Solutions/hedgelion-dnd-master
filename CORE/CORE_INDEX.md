# CORE Index

framework_version: 0.3-development
rules_baseline: D&D 2024 / SRD 5.2.1

Load `RUNTIME.md` for every gameplay turn. Load other modules only when required.

- `BOOTSTRAP_RUNTIME.md` — campaign discovery/startup and runtime routing.
- `CAMPAIGN_SETUP.md` — create/initialize a new campaign branch.
- `RUNTIME.md` — invariant DM turn pipeline and agency/canon boundaries. ALWAYS during gameplay.
- `SESSION.md` — session start/resume/end/checkpoints.
- `CHARACTER.md` — PC creation and novice onboarding.
- `ADJUDICATION.md` — checks, uncertainty, consequences, temporary rulings.
- `RANDOMNESS.md` — dice/randomness integrity.
- `INFORMATION.md` — clues, mysteries, perception, knowledge boundaries.
- `NPC.md` — NPC agency, knowledge, relationships, personality continuity.
- `DIALOGUE.md` — dialogue and social interaction.
- `EXPLORATION.md` — locations, investigation, travel, time, resources.
- `ENCOUNTERS.md` — encounter objectives, difficulty and environment.
- `COMBAT.md` — combat runtime.
- `MAGIC.md` — spell/magic adjudication.
- `PROCESSES.md` — long-running threats, projects, clocks and off-screen change.
- `WORLDGEN.md` — create/expand world only to the required horizon.
- `REWARDS.md` — economy, payment, treasure and ownership.
- `ADVANCEMENT.md` — level-up, rest, downtime and long-term progression.
- `SAFETY.md` — campaign boundaries and tone.
- `NARRATIVE.md` — narration, pacing, information density, novice guidance.
- `PREP.md` — situation-based preparation and strong starts.
- `STORAGE.md` — canonical storage, batching, lazy retrieval and resync.
- `MULTIPLAYER.md` — shared-world concurrency and environment-level conflict handling.
- `ANTIPATTERNS.md` — LLM-specific failure modes.
- `SOURCES.md` — research provenance; never load during normal gameplay.

Rules lookup policy:
1. established campaign house rules;
2. stored exact character/entity mechanics;
3. `RULES/` routing/local references;
4. official D&D 2024 / SRD 5.2.1 source when exact mechanics materially matter;
5. consequential rulings become explicit campaign rules if they must remain consistent.
