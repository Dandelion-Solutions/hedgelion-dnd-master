# CORE Index

framework_version: 0.2-development
rules_baseline: D&D 2024 / SRD 5.2.1

Load `RUNTIME.md` for every gameplay turn. Load other modules only when required.

- `BOOTSTRAP_RUNTIME.md` — campaign discovery/startup and runtime routing.
- `RUNTIME.md` — invariant DM turn pipeline and agency/canon boundaries. ALWAYS during gameplay.
- `SESSION.md` — session start/resume/end/checkpoints.
- `CHARACTER.md` — PC creation and novice onboarding.
- `ADJUDICATION.md` — checks, uncertainty, consequences, temporary rulings.
- `RANDOMNESS.md` — dice/randomness integrity.
- `INFORMATION.md` — clues, mysteries, perception, knowledge boundaries.
- `NPC.md` — NPC agency, knowledge, relationships, personality continuity.
- `DIALOGUE.md` — dialogue and social interaction.
- `EXPLORATION.md` — locations, investigation, travel, time, resources.
- `COMBAT.md` — combat runtime.
- `MAGIC.md` — spell/magic adjudication.
- `PROCESSES.md` — long-running threats, projects, clocks and off-screen change.
- `NARRATIVE.md` — narration, pacing, information density, novice guidance.
- `PREP.md` — situation-based preparation and strong starts.
- `STORAGE.md` — canonical storage, batching, lazy retrieval and resync.
- `MULTIPLAYER.md` — shared-world concurrency and environment-level conflict handling.
- `ANTIPATTERNS.md` — LLM-specific failure modes.
- `SOURCES.md` — research provenance; never load during normal gameplay.

Rules lookup policy:
1. established campaign house rules;
2. stored character/entity mechanics;
3. local/official D&D 2024 / SRD 5.2.1 baseline;
4. verify material uncertainty from an official source rather than inventing a rule;
5. persist consequential temporary/permanent rulings when future consistency requires it.
