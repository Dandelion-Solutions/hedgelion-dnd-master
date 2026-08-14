# Gameplay Context and Research Policy

framework_module_version: 0.1.0
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: resolves CORE caching, module activation, natural-language intent and external-research behavior

This module separates three things that must not be conflated:
1. engine instructions being present in model context;
2. a CORE module being relevant/active for the current decision;
3. external research being performed.

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

Preloading a module does not mean running all of its procedures on every turn.

`load_when` / situational-routing language in older CORE modules is interpreted as an ACTIVATION condition once the CORE cache exists.

Always-active modules:
- `RUNTIME.md`;
- `AI_REASONING.md`;
- this `PLAY_POLICY.md`.

Every other CORE module is dormant unless the current setup/scene/decision falls within its declared purpose or activation condition.

A dormant module:
- must not add checks, retrievals, research, bookkeeping or narration constraints to the current turn merely because its text is present in context;
- may still supply a passive invariant if another active module explicitly depends on it.

Older instructions that say to lazily load/drop/reread situational CORE modules are superseded by this policy. Campaign/world/entity retrieval remains lazy.

## Campaign data remains lazy

Do NOT preload campaign state just because engine instructions are preloaded.

Continue targeted retrieval for:
- MANIFEST/CONFIG and hot STATE;
- current scenes;
- relevant PLAYER/PC/NPC/item/location/process records;
- exact INDEX entries needed to resolve those records;
- bounded LOG/checkpoint history when actually required.

Repository-read cost should scale with the current decision, not campaign size.

## Offline-first gameplay

Normal gameplay and ordinary character/setup adjudication are offline-first.

Do NOT automatically use web search, browser/open-web tools, D&D Beyond, search engines, wikis, forums, blogs, videos or other external rules/reference sites to:
- validate a player's action;
- check whether the player's wording is an official spell/feature/action name;
- look up RAW wording during an ordinary turn;
- decide whether a creative action is allowed;
- confirm a ruling that can be made fairly from local context.

GitHub Connector operations required for campaign persistence/synchronization and explicit engine-release metadata maintenance are not external rules research and remain allowed under their own policies.

Links present in `CORE/SOURCES.md`, `RULES/OFFICIAL_SOURCES.md` or any other local file are references, not automatic instructions to open those URLs.

## Rules decision order

For ordinary play resolve rules in this order:
1. campaign house rules and established campaign rulings;
2. exact mechanics already stored for the PC/NPC/item/effect;
3. local preloaded CORE/rules-routing guidance and any exact local rule record already available;
4. the model's best rules knowledge plus established fiction, character capability and common-sense causal reasoning;
5. a quick fair local ruling when exact RAW is unavailable.

External research is NOT the next automatic step.

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

## Explicit external research

External rules research is opt-in for gameplay.

It may be used when the user explicitly asks for something like:
- `проверь по официальным правилам`;
- `найди точную формулировку RAW`;
- `посмотри, как это работает в SRD`;
- `дай источник`.

For that request:
- prefer authoritative/official sources where available;
- keep the research scoped to the requested question;
- distinguish the external rule text from the campaign's current ruling/canon;
- do not retroactively rewrite already-resolved outcomes unless the user explicitly chooses a correction and campaign authority permits it.

No background or deferred web verification is required after a local ruling.

## Latency priority

For ordinary play, immersion and response latency are protected by avoiding unnecessary I/O.

Once exact engine instructions and the current working set are available, the default turn should be resolved locally from them. Additional disk, GitHub or web operations need a concrete persistence, synchronization, missing-canon or explicit-research reason.