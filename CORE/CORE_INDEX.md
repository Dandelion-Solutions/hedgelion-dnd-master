# CORE Index

framework_module_version: 0.3.0
rules_baseline: D&D 2024 / SRD 5.2.1

## Context model

After the exact engine package is resolved, the COMPLETE local `CORE/*.md` set is preloaded once into the current chat model context. `RULES/INDEX.md` and `RULES/README.md` are preloaded with it.

Preloaded != active.

Always active is determined by each module header (`load_policy: ALWAYS_DURING_GAMEPLAY`). Current guard set:
- `RUNTIME.md` — turn pipeline, agency, causality and lifecycle gate.
- `AI_REASONING.md` — LLM-specific correctness discipline.
- `PLAY_POLICY.md` — CORE cache/activation and research policy.
- `DURABILITY_GUARD.md` — authoritative ordinary gameplay save-boundary classifier.
- `MECHANICS_INTEGRITY.md` — pre-narration mechanical proof gate.
- `CHARACTER_READINESS.md` — READY_PC gate.

`CORE_INDEX.md` is a routing summary; it does not override module headers.

All other modules remain present but dormant until their domain is relevant. In older module headers, `load_when` means activate-when after the CORE cache has been built; it is not an instruction to reread the file from disk.

- `BOOTSTRAP_RUNTIME.md` — campaign discovery/startup and runtime routing.
- `ENGINE_UPDATES.md` — release discovery and safe campaign integration; activate only at update opportunities.
- `NEW_CAMPAIGN_FAST_PATH.md` — authoritative ordering/transport/latency contract for creating a new campaign scaffold and reaching the first scene quickly.
- `CAMPAIGN_SETUP.md` — substantive character/world setup after the fast-path scaffold exists.
- `DIEGETIC_ONBOARDING.md` — pre-live story-first onboarding and PROVISIONAL_IDENTITY.
- `CAMPAIGN_IDENTITY.md` — evolving campaign title and protected README overview.
- `CAMPAIGN_CARD.md` — fast campaign menu projection, emoji/access hints and card-refresh discipline.
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
- `WORLDGEN.md` — create/expand only the required world horizon; may use bounded source research at prep boundaries.
- `LORE.md` — history/culture/disputed accounts/lore reveal.
- `REWARDS.md` — economy/payment/treasure/ownership.
- `ADVANCEMENT.md` — level-up/rest/downtime/long-term progression.
- `SAFETY.md` — campaign boundaries and tone.
- `NARRATIVE.md` — narration, pacing and information density.
- `PREP.md` — situation-based preparation, strong starts and bounded enrichment research.
- `STORAGE.md` — canonical storage model, targeted reads and durable data organization.
- `PERSISTENCE.md` — authoritative GitHub write transaction/transport protocol; activate for any save/publication.
- `SAVE_CONTRACT.md` — explicit-save completeness/lifecycle semantics; activate only for explicit save/save-and-stop.
- `INTEGRITY.md` — bounded repair when canon is suspect/corrupt.
- `MULTIPLAYER.md` — shared-world concurrency and access behavior.
- `LIVE_SCENE.md` — temporary one-file CAS synchronization for shared actionable scenes.
- `ANTIPATTERNS.md` — extended failure catalogue for audit/debug.
- `SOURCES.md` — provenance/reference appendix; preloaded but DORMANT during ordinary live turns. May activate for explicit source research or bounded setup/prep enrichment.

## Activation examples

`new campaign` -> always-active guards already apply; activate NEW_CAMPAIGN_FAST_PATH FIRST + CAMPAIGN_SETUP + CAMPAIGN_CARD, and activate DIEGETIC_ONBOARDING/CAMPAIGN_IDENTITY only if their conditions arise. Scaffold publication obeys NEW_CAMPAIGN_FAST_PATH before character/world questions; before the first true live scene CHARACTER_READINESS requires READY_PC and DURABILITY_GUARD requires a post-scaffold PLAY_READY durable frontier.

`campaign menu/discovery` -> activate BOOTSTRAP_RUNTIME + CAMPAIGN_CARD; prefer card-only presentation reads and defer authoritative/deep campaign loading until selection.

`ordinary in-scene action` -> normally only always-active modules plus the smallest domain modules actually implicated by the action. DURABILITY_GUARD performs only an in-memory boundary check; CHARACTER_READINESS guarantees the active PC has usable mechanics; MECHANICS_INTEGRITY requires a real resolution class before any material outcome is narrated.

`spell/magic` -> activate MAGIC and ADJUDICATION/RANDOMNESS as needed; MECHANICS_INTEGRITY remains the final mechanical proof gate.

`combat` -> activate COMBAT + RANDOMNESS/ADJUDICATION as needed. Assert READY_PC, establish/maintain combat mechanical state and current resolution trace before narrating uncertain combat outcomes.

`session/world prep` -> activate PREP + WORLDGEN/LORE as needed; SOURCES may activate for one bounded enrichment pass.

`campaign persistence boundary` -> DURABILITY_GUARD decides that a boundary exists; activate PERSISTENCE + STORAGE; also activate CAMPAIGN_CARD when the durable delta changes any projected card field.

`explicit save / save game` -> activate SAVE_CONTRACT; it creates SAVE_ALL_DIRTY; activate PERSISTENCE + STORAGE and every domain needed to materialize missing dirty records. A summary-only save is invalid.

`engine update opportunity` -> activate ENGINE_UPDATES + BOOTSTRAP_RUNTIME + STORAGE + PERSISTENCE + CAMPAIGN_CARD when publication changes campaign engine metadata.

`multiplayer membership change` -> activate MULTIPLAYER + CAMPAIGN_CARD + PERSISTENCE; participant display cache changes in the same campaign transaction.

`multiplayer shared scene` -> activate MULTIPLAYER + LIVE_SCENE plus current domain modules; ordinary live-epoch writes follow LIVE_SCENE's one-file CAS profile, not campaign-tree transport.

`explicit rules research` -> activate SOURCES/rules-source routing only for that bounded research request.

## Rules decision policy

During a normal live turn:
1. established campaign house rules/rulings;
2. stored exact character/entity mechanics;
3. local CORE/RULES guidance and exact local records;
4. best local adjudication from character capability + fiction + model rules knowledge;
5. quick fair ruling if exact RAW is unavailable.

Do NOT automatically browse the web or D&D Beyond as step 5. External RAW research during a live turn requires an explicit user request.

Whatever ruling is chosen, `MECHANICS_INTEGRITY.md` still requires the ruling to be actually executed. A quick local ruling is not permission to skip its roll/math.

Character creation is different from a live-turn lookup loop: if exact durable PC mechanics are missing during setup, `CHARACTER_READINESS.md` permits/requires one bounded official-source setup pass so the complete sheet can be stored before play.

Setup/prep/worldbuilding may use bounded trustworthy source research under `PLAY_POLICY.md`; that is a different mode from live-turn rules checking.