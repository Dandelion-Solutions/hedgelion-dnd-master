# CORE Index

framework_module_version: 0.2.0
rules_baseline: D&D 2024 / SRD 5.2.1

## Context model

After the exact engine package is resolved, the COMPLETE local `CORE/*.md` set is preloaded once into the current chat model context. `RULES/INDEX.md` and `RULES/README.md` are preloaded with it.

Preloaded != active.

Always active during gameplay:
- `RUNTIME.md` — turn pipeline, agency, causality and canon boundaries.
- `AI_REASONING.md` — LLM-specific correctness discipline.
- `PLAY_POLICY.md` — CORE cache, activation semantics, natural-language intent and offline-first research policy.

All other modules remain present but dormant until their domain is relevant. In older module headers, `load_when` means activate-when after the CORE cache has been built; it is not an instruction to reread the file from disk.

- `BOOTSTRAP_RUNTIME.md` — campaign discovery/startup and runtime routing.
- `ENGINE_UPDATES.md` — release discovery and safe campaign integration; activate only at update opportunities.
- `CAMPAIGN_SETUP.md` — create/initialize a campaign.
- `GM_CRAFT.md` — setup/prep/design/audit craft.
- `CAMPAIGN_OPERATIONS.md` — campaign/session organization and maintenance.
- `SESSION.md` — session start/resume/end/checkpoints.
- `CHARACTER.md` — PC creation and novice onboarding.
- `ADJUDICATION.md` — uncertain actions, consequences, local rulings.
- `RANDOMNESS.md` — actual RNG and dice integrity.
- `INFORMATION.md` — clues, mysteries, perception, knowledge boundaries.
- `NPC.md` — NPC agency, knowledge, relationships and continuity.
- `DIALOGUE.md` — dialogue/social interaction.
- `EXPLORATION.md` — locations, investigation, travel, time and resources.
- `ENCOUNTERS.md` — encounter objectives, difficulty and environment.
- `COMBAT.md` — combat runtime.
- `MAGIC.md` — spell/magic adjudication.
- `PROCESSES.md` — long-running threats/projects/clocks/off-screen change.
- `CHRONOLOGY.md` — relative ordering when chronology materially constrains play.
- `WORLDGEN.md` — create/expand only the required world horizon.
- `LORE.md` — history/culture/disputed accounts/lore reveal.
- `REWARDS.md` — economy/payment/treasure/ownership.
- `ADVANCEMENT.md` — level-up/rest/downtime/long-term progression.
- `SAFETY.md` — campaign boundaries and tone.
- `NARRATIVE.md` — narration, pacing and information density.
- `PREP.md` — situation-based preparation and strong starts.
- `STORAGE.md` — canonical storage, batching, lazy CAMPAIGN retrieval and resync.
- `INTEGRITY.md` — bounded repair when canon is suspect/corrupt.
- `MULTIPLAYER.md` — shared-world concurrency and access behavior.
- `LIVE_SCENE.md` — temporary live synchronization for shared actionable scenes.
- `ANTIPATTERNS.md` — extended failure catalogue for audit/debug.
- `SOURCES.md` — provenance appendix; preloaded but DORMANT. Never follow/open its links during normal play.

## Activation examples

`new campaign` -> activate GM_CRAFT + CAMPAIGN_OPERATIONS + CAMPAIGN_SETUP + CHARACTER + SAFETY + WORLDGEN in addition to always-active modules.

`ordinary in-scene action` -> normally only always-active modules plus the smallest domain modules actually implicated by the action.

`spell/magic` -> activate MAGIC and ADJUDICATION only as needed.

`combat` -> activate COMBAT + RANDOMNESS/ADJUDICATION as needed.

`engine update opportunity` -> activate ENGINE_UPDATES + BOOTSTRAP_RUNTIME + STORAGE.

`multiplayer shared scene` -> activate MULTIPLAYER + LIVE_SCENE plus current domain modules.

`explicit rules research` -> activate SOURCES/rules-source routing only for that bounded research request.

## Rules decision policy

During normal gameplay:
1. established campaign house rules/rulings;
2. stored exact character/entity mechanics;
3. local CORE/RULES guidance and exact local records;
4. best local adjudication from character capability + fiction + model rules knowledge;
5. quick fair ruling if exact RAW is unavailable.

Do NOT automatically browse the web or D&D Beyond as step 5. External rules research requires an explicit user request. See `PLAY_POLICY.md`.