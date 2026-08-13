# CORE Index

framework_version: 0.1-development
rules_baseline: D&D 2024 / SRD 5.2.1

Load `RUNTIME.md` for every gameplay turn. Load other modules only when the current task requires them.

- `RUNTIME.md` — invariant turn pipeline, player agency, canon boundaries. ALWAYS during gameplay.
- `ADJUDICATION.md` — action resolution, checks, DC policy, consequences, failure handling.
- `RANDOMNESS.md` — dice/randomness integrity, hidden/public rolls, no post-roll fudging.
- `INFORMATION.md` — clues, mysteries, perception, knowledge boundaries, secrets.
- `NPC.md` — NPC agency, goals, knowledge, relationships, long-term personality coherence.
- `DIALOGUE.md` — execution of conversations and social interaction.
- `EXPLORATION.md` — locations, investigation, travel, time, resources and discovery.
- `COMBAT.md` — combat runtime, initiative, tactical state and consequences.
- `MAGIC.md` — spell/magic adjudication and unknown magical phenomena.
- `NARRATIVE.md` — narration, pacing, descriptions, information density and novice onboarding.
- `PREP.md` — situation-based preparation, strong starts, potential scenes, secrets/clues.
- `STORAGE.md` — canonical state model, lazy retrieval, event log and atomic persistence.
- `MULTIPLAYER.md` — shared-world concurrency, synchronization and simultaneous actors.
- `ANTIPATTERNS.md` — LLM-specific failure modes and self-checks.
- `SOURCES.md` — provenance/research notes; never load during normal gameplay.

Rules lookup policy:
1. Use established campaign house rules first.
2. Use stored character/entity mechanics when present.
3. Use SRD 5.2.1 / official D&D 2024 rules as baseline.
4. When a material rule is uncertain and no local canonical rule exists, verify from an official source rather than inventing a rule.
5. A temporary ruling must be recorded as temporary if it materially affects future consistency.
