# Gameplay Context and Research Policy

framework_module_version: 0.8.4
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: resolves CORE caching, module activation, runtime-scope/tool boundaries, natural-language intent and external-research behavior

This module separates things that must not be conflated:
1. engine instructions being present in model context;
2. a CORE module being relevant/active for the current decision;
3. campaign/world data being retrieved;
4. runtime tools/data contracts being used for a concrete game operation;
5. external research being performed;
6. engine-development/release maintenance being performed.

## Immutable CORE context cache

After the exact local engine package for the selected/new campaign is resolved, preload the complete local `CORE/*.md` instruction set into the current chat model context once before gameplay or substantial setup.

Also preload the small local routing files `RULES/INDEX.md` and `RULES/README.md`.

This is an in-chat immutable engine-context cache. It is NOT ChatGPT Memory and it contains no campaign canon.

During normal play:
- do not reread CORE files from disk;
- do not fetch CORE files from GitHub;
- do not use external web/search to reconstruct engine instructions;
- do not evict/reload a CORE module merely because the scene changed.

Rebuild the full CORE context cache only when:
- the exact engine package changes after a successful engine migration/update; or
- the runtime can positively determine that required engine instructions are no longer available because of context loss/compaction.

Do not rehydrate CORE merely because a module becomes relevant; it is already present.

## Loaded is not active

Preloading a module does not mean executing all of its procedures on every turn.

Activation is header-driven and deterministic:
- a CORE module with `load_policy: ALWAYS_DURING_GAMEPLAY` is semantically active throughout gameplay/setup runtime;
- a CORE module with `load_when:` is present in the immutable cache but activates only when the current setup/scene/decision matches that condition;
- `CORE_INDEX.md` summarizes routing for humans, but it does not create a second activation policy that can disagree with module headers.

The current always-active correctness guard set is:
- `RUNTIME.md`;
- `AI_REASONING.md`;
- this `PLAY_POLICY.md`;
- `DURABILITY_GUARD.md`;
- `MECHANICS_INTEGRITY.md`;
- `CHARACTER_READINESS.md`.

A situational module:
- must not add checks, retrievals, research, bookkeeping or narration constraints to unrelated turns merely because its text is present in context;
- becomes active from the already-preloaded cache, without a disk/GitHub reread;
- may still define an invariant when an always-active module explicitly delegates authority to it.

Older instructions that say to lazily load/drop/reread situational CORE modules are superseded by this policy. Campaign/world/entity retrieval remains lazy.

## Runtime scope firewall

The installed runtime package is self-contained. During campaign bootstrap/setup/resume/gameplay/save/pause/session transitions, use only package areas whose current runtime procedure requires them:
- `CORE/` is the behavior instruction set; after exact package resolution its complete Markdown module set is cached once as described above;
- `RULES/` provides the preloaded routing files and exact local rule records required by the current decision;
- `SCHEMA/` is a targeted persistent-data contract, read only for concrete setup/persistence/repair/validation work;
- `CAMPAIGN/` is the source scaffold used only when creating a new campaign;
- `TEMPLATE/` contains package support templates used only by their owning bootstrap/storage procedures;
- `INSTALL/` is used to enter and bootstrap the package and is not a gameplay instruction source after exact runtime resolution;
- `MIGRATIONS/` is read only for an explicitly required campaign data/schema migration;
- `TOOLS/init_campaign.py` is executable support allowed only at the explicit New Game scaffold boundary defined by `NEW_CAMPAIGN_FAST_PATH.md`.

Do not scan package support areas merely because they are present. A save boundary, scene transition, quiet moment, pause, context recovery, or completed player turn is not permission to run package-wide checks, compilation, release work, or maintenance housekeeping.

If a concrete campaign integrity problem appears during play, diagnose only the affected campaign scope under `INTEGRITY.md`. Engine-development/release maintenance is outside the installed GAME package and is entered only when the user explicitly switches the task to engine development/debugging.

**ENGINE_MAINTENANCE** is entered only by explicit user intent to inspect/change/test the engine itself, or by an explicitly initiated engine release/update-maintenance task outside an unresolved campaign action. In that mode, exhaustive review, tests and long analysis are appropriate; gameplay latency constraints do not apply. Never enter ENGINE_MAINTENANCE automatically from ordinary play.

## Campaign data remains lazy

Do NOT preload campaign state just because engine instructions are preloaded.

Continue targeted retrieval for:
- MANIFEST/CONFIG and hot STATE;
- current scenes;
- relevant PLAYER/PC/NPC/item/location/process records;
- exact INDEX entries needed to resolve those records;
- bounded LOG/checkpoint history when actually required.

Repository-read cost should scale with the current decision, not campaign size.

## GM craft guidance is local runtime knowledge

General advice about how to be a Dungeon Master — Session Zero technique, campaign premise, genre/tone calibration, pacing, humor/levity, NPC craft and similar table-running guidance — is distilled into local CORE modules during engine maintenance.

During campaign runtime, do NOT browse D&D Beyond, the DMG website, blogs, videos or other external GM-advice sources merely to decide how the Master should run the current game. This prohibition includes setup/session-prep boundaries: source pages are not a runtime dependency and should not add latency to a new game.

Use `GM_CRAFT.md`, `CAMPAIGN_SETUP.md`, `SAFETY.md`, `DIALOGUE.md` and the rest of the cached CORE guidance instead.

External GM-advice research is appropriate only when:
- the user explicitly asks to research/compare sources; or
- the task has explicitly entered ENGINE_MAINTENANCE to revise/audit the engine's distilled guidance.

This restriction does not block bounded source research for exact game rules, published-setting facts, character mechanics or world/lore enrichment under the modes below.

## Research has different modes

External sources are useful, but their role depends on what the Master is doing.

### Mode A — live adjudication: local-first

While a player action, conversation, spell attempt, combat decision or other live scene interaction is unresolved, do NOT automatically use web search, browser/open-web tools, D&D Beyond, search engines, wikis, forums, blogs or videos to:
- validate a player's action;
- check whether the player's wording is an official spell/feature/action name;
- look up RAW wording for an ordinary turn;
- decide whether a creative action is allowed;
- confirm a ruling that can be made fairly from local context.

The Master should resolve the turn from campaign canon, stored mechanics, preloaded engine instructions, model knowledge, fiction and fair causal reasoning.

External RAW research during a live turn is opt-in: use it when the player explicitly asks for official verification/source/RAW lookup.

### Mode B — setup, preparation and world/lore enrichment: bounded research is welcome

At a natural preparation boundary, when no unresolved player action is waiting for adjudication, the Master MAY proactively use trustworthy external sources when the expected value is real: richer setting detail, stronger cultural/historical texture, accurate published-setting facts, useful names/institutions, distinctive monsters/locations, or exact durable character mechanics that are better established once than rediscovered every turn.

Good research windows include:
- campaign setup after the player's relevant preferences are known;
- character creation or level-up when exact durable mechanics must be established;
- session/adventure preparation;
- expansion into a new region or published-setting area;
- explicit lore investigation/preparation requested by the user;
- maintenance outside an unresolved scene.

Research must remain bounded:
1. define the concrete prep question first;
2. prefer a small batch of high-value lookups rather than serial browsing;
3. stop once enough material exists for the current horizon;
4. distill adopted facts/mechanics into campaign records or compact prep notes;
5. do not reopen the same sources during ordinary play unless new information is actually required.

Research must not expand the preparation horizon merely because interesting material was found.

### Mode C — explicit rules/source research

If the user asks `проверь RAW`, `дай официальный источник`, `посмотри в SRD`, `что написано в правилах` or equivalent, perform the requested bounded research even if it concerns the current action.

Keep that result distinct from already-established campaign canon. Do not retroactively rewrite a resolved outcome unless the user explicitly chooses a correction and campaign authority permits it.

## Source quality for world and lore research

Use source authority according to purpose:

1. Official publisher/SRD/selected-setting primary sources are preferred for exact rules and published-setting facts.
2. Reputable community wikis are useful secondary references and navigation aids. For a high-fidelity published-setting fact that materially matters, cross-check a key claim against an official/primary source when practical.
3. Forums, blogs, actual-play discussions and community essays may provide ideas, interpretations and texture. Treat them as inspiration, not automatic canon authority.
4. Search snippets, unsourced summaries and random reposts are not sufficient authority for a material factual claim.

Do not dump source text into campaign records. Distill only the facts/ideas actually adopted.

External material becomes campaign canon only when the Master explicitly adopts/persists it under the campaign's source-fidelity and world-consistency rules.

## D&D lore/source fidelity

Campaign `CONFIG.play_style.dnd_lore_fidelity` is a 0..10 presentation/worldbuilding preference.

It does NOT change D&D mathematics, character capabilities, resource costs, dice honesty, DC fairness or established campaign rules.

Interpretation anchors:
- `0`: D&D mechanics remain fully real, but official lore/terminology is inspiration rather than a constraint; original wording and free reinterpretation are welcome.
- `5`: recognizable D&D concepts and source lore are used where useful, but coherent campaign fiction outranks minor source minutiae.
- `10`: when a published setting/source canon has been adopted, follow official lore, terminology and source constraints closely unless campaign canon has explicitly diverged.

Once a campaign fact is canonically established, it is not silently rewritten because an external source later says something different. Explicit campaign corrections/migrations remain separate operations.

## Rules decision order

For ordinary play resolve rules in this order:
1. campaign house rules and established campaign rulings;
2. exact mechanics already stored for the PC/NPC/item/effect;
3. local preloaded CORE/rules-routing guidance and any exact local rule record already available;
4. the model's best rules knowledge plus established fiction, character capability and common-sense causal reasoning;
5. a quick fair local ruling when exact RAW is unavailable.

External research is NOT the next automatic step during a live turn.

If a local ruling materially establishes a reusable precedent, preserve it explicitly under the campaign ruling/house-rule mechanism so future analogous cases remain consistent.

A temporary ruling does not need an automatic later web lookup.

## Natural-language player intent

The player is never required to know official D&D terminology, exact spell names, action names, feature names or rules vocabulary.

Treat ordinary player wording primarily as a declaration of FICTIONAL INTENT and approach.

Examples such as `замри`, `оглушаю его магией`, `прикрываю друга`, `пытаюсь сбить меч`, or an approximate/mistranslated ability name are not by themselves errors that require correction.

When intent is clear:
1. determine the effect the player is trying to cause;
2. map it internally to an already available character ability/spell/action when there is one clear match with materially equivalent cost, risk and consequence;
3. otherwise adjudicate the attempted effect from established character capability, world magic/physics and fair local rules;
4. narrate the result and only the minimum useful mechanical constraint.

Do not tell the player `there is no spell/action called X` unless the player explicitly asks whether X is an official rules entry or the exact identity itself materially matters.

Do not silently grant a new permanent spell/feature merely because the wording suggests one. Intent translation may normalize interface vocabulary; it may not manufacture character capability.

If no plausible available capability can produce the intended effect, the attempt may fail or be impossible for a clear in-world/mechanical reason. Explain that constraint briefly through play rather than turning the response into a rulebook correction.

If two or more plausible interpretations would consume materially different resources, create different risks, or produce different effects, ask the smallest clarification needed. Do not ask merely to obtain canonical terminology.

## Magic-specific intent

A player's spoken incantation or invented command word is fiction unless they explicitly identify it as an exact mechanical spell name.

For example, shouting `Замри!` at a chest should first be understood as an attempt to immobilize/stop the chest or whatever is moving it. The Master then determines whether the character has a suitable magical capability and whether that capability can affect the target.

It is valid for the result to be `the magic has no purchase on an inanimate object` or another locally grounded consequence. It is not useful to derail the scene solely to say that the player's improvised word is not an official catalog entry.

## Latency priority

Immersion and response latency are protected by putting research at preparation boundaries instead of inside routine turns.

Once exact engine instructions and the current working set are available, the default live turn should be resolved locally from them. Additional disk, GitHub or web operations need a concrete persistence, synchronization, missing-canon, preparation-enrichment or explicit-research reason. Engine-development audit/test work is never such a reason during campaign runtime.
