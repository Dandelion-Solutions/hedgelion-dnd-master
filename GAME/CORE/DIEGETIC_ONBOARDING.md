# Diegetic Character Onboarding

framework_module_version: 1.1.0
load_when: story-first character setup, adopted provisional PC identity, or resume of unfinished onboarding
precedence: authoritative for gameplay-first progressive character materialization and the PROVISIONAL_IDENTITY boundary; CHARACTER_READINESS owns READY_PC and DURABILITY_GUARD owns general save timing

## Purpose

Character creation may happen through play instead of a questionnaire. After the blank campaign scaffold exists, the Master may begin ordinary player-facing fiction and let interaction establish missing character/world facts naturally.

This **is gameplay**, even while campaign lifecycle remains `initializing` and the PC remains `provisional`.

Initialization/readiness status is bookkeeping about which mechanical and persistence guarantees are already available. It is not a requirement to withhold fiction until a complete sheet exists.

Examples of natural onboarding include:
- the player says `я буду демоном огня`, giving the Master a strong protagonist/build direction before a name exists;
- an NPC later asks the protagonist's name and the player's answer establishes it;
- clothing, appearance, ordinary possessions or visible habits become concrete when they matter in-scene;
- background, origin, proficiencies or other choices emerge from player statements or situations rather than a front-loaded form;
- the Master may seed harmless external details that do not steal player-owned identity choices or create hidden mechanical advantage.

Do not force this style. Direct character creation remains valid when the player prefers it or arrives with a complete concept/build.

## Progressive mechanical boundary

A provisional PC may participate in gameplay before READY_PC, but the Master must never resolve an outcome from missing mechanics.

For each proposed mechanically relevant action, distinguish:

```text
all material dependencies for THIS outcome are already established
    -> the bounded outcome may be resolved honestly

one or more material dependencies remain unresolved
or an unresolved character choice could change legality/probability/consequence
    -> do not cross that mechanical boundary yet
```

The second case does **not** end gameplay. Keep the scene alive through fiction that does not require the missing mechanic, or establish the smallest missing dependency/choice first. Ask a direct question only when the dependency cannot be safely established from player intent, accepted rules inheritance, campaign/default policy or delegated Master bookkeeping.

Until READY_PC, be especially conservative with attacks, saves, contested irreversible outcomes, resource expenditure, damage/conditions, spell use and other actions whose legality or result commonly depends on several unfinished character choices.

Harmless description, dialogue, ordinary movement, identity establishment, non-mechanical social interaction and DM-seeded cosmetic framing remain valid when fiction supports them.

## Rapid mechanical convergence

Progressive onboarding is not permission to stretch setup across a long sequence of unnecessary scenes.

When the player delegates bookkeeping, the Master SHOULD converge toward READY_PC during the first few meaningful interactions by materializing the initial mechanical baseline in this order:

```text
1. explicit player statement / explicit choice
2. deterministic rules inheritance from accepted class/species/archetype/level/features
3. strong rules-valid inference from explicit player concept
4. adopted campaign/rules default
5. deterministic conservative Master default under delegated bookkeeping
6. one targeted player question if materially different legal choices still remain
```

This is a latency principle, not a fixed turn-count or wall-clock SLA.

The player is not expected to supply values such as level, maximum HP or a resource capacity merely because the engine needs them. The Master derives/selects them from the accepted rules-valid build/archetype/defaults when possible.

A concept is not itself executable mechanics. `я буду демоном огня` may guide the Master toward a compatible archetype/build, fire-related capabilities and corresponding rules-valid values, but those mechanical commitments must be validated and stored through their native Actor/build/definition owners before they affect adjudication.

If several materially different legal options remain equally compatible with player intent and no delegated deterministic policy resolves them, ask the smallest useful question instead of choosing opportunistically.

## No situational retrofit

Do not leave a discretionary mechanical option open until one branch becomes useful in the current situation.

If an unresolved choice could materially change ordinary current-play legality, probability, defense, resource availability, capability or consequence, commit it before READY_PC without using situational knowledge to optimize the selection.

After READY_PC, lazy materialization is valid only for values that are uniquely derivable from already committed anchors, purely descriptive, created by a genuine later evolution/acquisition boundary, or governed by a deterministic/delegated policy fixed before the situation where the value matters.

## Stable identity and PROVISIONAL_IDENTITY

Exploration is not commitment. Tentative alternatives remain volatile.

The first stable protagonist/Actor anchor creates a `PROVISIONAL_IDENTITY` boundary when the Master adopts it for continued play and losing it would make honest resume wrong.

A name is one possible anchor, not a requirement. Examples include:
- the player gives an unambiguous protagonist concept and the Master continues on that basis;
- the player supplies a name;
- a rules-valid archetype/build anchor has been accepted for the protagonist;
- another player-authored identity fact unambiguously identifies the same continuing PC.

The stable `world.actor` ID is record identity. `Actor.name` may still be unknown. The optional Actor `concept` field may preserve a compact normalized protagonist framing, while exact source dialogue/evidence remains under its native evidence/history contracts.

Before further player-facing fiction accumulates beyond this stable anchor, publish one coherent transaction containing all already-established durable setup/play canon needed for honest resume, normally:
- PLAYER binding/preferences already settled;
- one stable PC Actor ID with `status: provisional` in the applicable player/index projection;
- Actor `name` if known, `concept` if established, and only mechanics actually committed so far;
- PC index entry;
- singleplayer card protagonist projection as currently known;
- settled CONFIG values;
- already-established starting premise/location/NPC/relationship/scene/current routing when those were presented as real campaign truth;
- optional first automatic campaign title under `CAMPAIGN_IDENTITY.md` when protagonist/party concept and broad surrounding world are already durable.

Keep MANIFEST/card lifecycle `initializing`. This boundary is not READY_PC or full mechanics readiness.

The fiction before and after this checkpoint is still part of the campaign. `initializing` does not mean "not playing"; it means the campaign has not yet crossed the READY_PC/PLAY_READY lifecycle frontier.

## DM-seeded surface details

The Master may seed undefined harmless external details such as clothing, hair, a visible mannerism or ordinary keepsake when they fit the concept and grant no hidden mechanical advantage. If presented as current fact and not contradicted, they may be stored as DM-seeded canon.

The player may later correct such details. Apply a compatible correction without ceremonial confirmation. Never label silence as player authorship; player-authored identity fields contain only player-explicit facts.

Changes that would affect equipment, wealth, stats, abilities or prior causal consequences follow normal rules instead of becoming free retcons.

## Cadence after the checkpoint

PROVISIONAL_IDENTITY is intentionally early and narrow. Do not autosave every cosmetic/backstory answer afterward.

Accumulate ordinary established additions in HOT/SOFT state under `DURABILITY_GUARD.md` until:
- READY_PC / PLAY_READY;
- explicit save;
- session/maintenance safety boundary;
- another authoritative HARD boundary.

If a newly established fact becomes a HARD dependency for honest continuation under another owner, that owner may require earlier publication.

Promote/update the **same PC Actor ID** when the initial mechanical commitment later reaches READY_PC. Never replace the PC merely because an earlier provisional checkpoint exists.

## READY_PC convergence

The runtime continuously tracks whether the current provisional Actor now satisfies `CHARACTER_READINESS.md`.

Do not demand a separate player command such as `finish character creation`. When the accumulated accepted mechanical commitments are sufficient:

```text
provisional Actor
    -> deterministic READY_PC validation
    -> semantic acceptance/ownership checks
    -> coherent durability transaction
    -> same Actor crosses initial mechanical commitment frontier
    -> campaign may cross PLAY_READY/active lifecycle frontier when remaining launch requirements are satisfied
```

The READY_PC transaction fixes the reconstructable **initial mechanical commitment frontier** in the campaign repository. It is not a promise that every possible future/dossier field has been eagerly filled.

Derived mechanics may remain recomputable. Deterministically derivable values may be materialized lazily later. New choices introduced by genuine later level-up/acquisition/preparation remain normal character evolution.

READY_PC is therefore a **detected state and persistence boundary**, not a prerequisite for the first gameplay scene and not a 100%-filled character-card requirement.

## Resume

A campaign stopped after PROVISIONAL_IDENTITY resumes the same ongoing onboarding play from durable provisional PC/world/scene state. It remains lifecycle `initializing` until READY_PC + PLAY_READY, but this does not erase or downgrade prior gameplay.

On resume:
- preserve the same PC Actor identity;
- restore already established fiction and committed choices;
- do not ask again for facts already settled;
- continue naturally from the current scene when safe;
- use the same inference/default precedence for remaining baseline mechanics;
- never re-open a committed mechanical choice merely because a later situation makes another option attractive.

Routine successful persistence is invisible to the player.
