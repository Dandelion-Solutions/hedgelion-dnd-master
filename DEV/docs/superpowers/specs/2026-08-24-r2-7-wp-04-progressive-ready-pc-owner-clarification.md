# R2.7 WP-04 — Progressive READY_PC Owner Clarification

Status: **OWNER-APPROVED ARCHITECTURE CLARIFICATION**

Date: 2026-08-24

Scope: narrow correction to WP-04 character materialization/readiness semantics. This clarification supersedes older wording that equates READY_PC with a 100%-filled character dossier or treats the first durable PC write as something that must wait for full mechanical completion.

## 1. Product decision

Character creation may occur through gameplay. HDM SHALL distinguish:

```text
stable protagonist/Actor establishment
    -> early durable provisional Actor
    -> rapid initial mechanical commitment
    -> READY_PC
    -> later safe/lazy materialization and ordinary character evolution
```

No additional persistent `PLAYABLE_PC` status/class is introduced.

`PROVISIONAL_IDENTITY` and `READY_PC` remain the two relevant boundaries, but their semantics are clarified below.

## 2. PROVISIONAL_IDENTITY is an early canonicalization boundary

`PROVISIONAL_IDENTITY` SHALL NOT depend on the player having supplied a name.

The boundary may fire once a stable protagonist/Actor anchor has been adopted for continued play and losing that identity would make honest resume wrong. Examples include:

- a player-established name;
- a stable protagonist concept such as `я буду демоном огня`;
- an accepted Actor/archetype/build anchor that the fiction is already relying on;
- another unambiguous player-authored identity anchor.

The same stable Actor ID is used before and after READY_PC.

The early durability transaction stores every already-established durable fact needed for honest resume. It does **not** wait for the full character dossier or all mechanics to be materialized.

## 3. Actor identity versus Actor name

Actor record identity is the stable `world.actor` record ID, not `state.name`.

Therefore `state.name` is optional. An unnamed but otherwise stably established protagonist is a valid provisional Actor.

A normalized player-facing `concept` may be stored as current nonmechanical Actor framing. It is descriptive/player-intent state, not executable mechanics by itself. Mechanical consequences require translation into accepted rules-valid Actor/build/archetype state.

## 4. READY_PC means initial mechanical commitment frontier

READY_PC SHALL mean that the initial mechanically material character choices and dependencies are sufficiently committed for ordinary mechanics-capable play without context-sensitive completion.

It does **not** mean:

- every possible character/backstory field is filled;
- every derived number is persisted;
- every future mechanically relevant value is eagerly materialized;
- every catalog definition is preloaded into context;
- no later character evolution/level-up/gear/spell/preparation decision may occur.

For the selected ruleset, READY_PC must close every currently unresolved **discretionary** choice whose alternatives could materially change ordinary current-play legality, probability, defense, resource availability, capability or consequence.

## 5. Mechanical initialization sources

A player is not expected to state values such as level, HP maximum, resource capacity or every proficiency when those values can be selected/derived safely by the Master.

The Master SHALL use this precedence when materializing the initial character:

```text
1. explicit player statement/choice
2. deterministic rules inheritance from already accepted class/species/archetype/level/features
3. strong concept-compatible inference from explicit player intent
4. adopted campaign/rules default
5. deterministic conservative Master default under delegated bookkeeping
6. one targeted player question only when materially different legal choices remain unresolved
```

Examples:

- `я буду демоном огня` may justify selecting/creating a rules-valid fire-demon-compatible archetype/build and its implied capabilities;
- HP maximum or a resource capacity should normally derive from the accepted class/archetype/level/resource definitions rather than being asked as a questionnaire field;
- if two materially different legal builds remain equally compatible with the player's intent and no deterministic/delegated default resolves them, ask the smallest targeted question.

Concept inference never bypasses rules validation. The concept is evidence/input to preparation; accepted mechanical state is the authoritative result.

## 6. Anti-retrofit / no situational optimization

A mechanical choice cannot remain conveniently unbound until the exact situation in which one option becomes advantageous.

Before READY_PC, if an unresolved legal choice could affect ordinary current play, HDM must commit it through the precedence above before allowing situational knowledge to bias the choice.

After READY_PC, a missing value is safe to materialize lazily only when one of these is true:

1. it is uniquely/deterministically derivable from already committed authoritative anchors;
2. it is purely descriptive/nonmechanical;
3. it belongs to a genuine future acquisition/evolution boundary (for example level-up, new item, later spell preparation) and could not have affected earlier play;
4. a pre-existing deterministic/delegated policy already fixed how it will be selected before the situation where it matters.

If a still-open choice could have changed an already-resolved or currently pending outcome, it was not safely deferrable.

## 7. READY_PC minimum outcome guarantee

READY_PC is a semantic predicate over the Actor plus referenced Assets/Effects/definitions/player binding. The exact data layout remains owned by WP-04/WP-06/WP-10.

At READY_PC, HDM must be able to derive ordinary current-play mechanics without inventing character state on demand. This normally requires committed anchors sufficient for:

- current rules/build/archetype/level progression;
- common ability checks and saves;
- proficiency/capability eligibility used by ordinary play;
- HP/LifeState and relevant recovery basis;
- ordinary defenses and movement;
- mechanically significant starting/current equipment;
- current core resources and action/capability sources;
- spellcasting state when applicable;
- any other current discretionary choice whose alternatives could materially change ordinary play.

Derived values may remain lazy/recomputable.

## 8. Onboarding latency principle

Diegetic onboarding is not a reason to stretch character creation across a long sequence of otherwise unnecessary scenes.

The Master SHOULD converge rapidly toward READY_PC, normally during the first few meaningful interactions when the player has delegated bookkeeping, by using inheritance/inference/defaults instead of serial questionnaire prompts.

This is a product latency principle, not a hard wall-clock/turn SLA. A player who intentionally wants extended character exploration may take longer.

Playable scenes are useful while this convergence occurs, but they must not be manufactured solely to postpone establishing the mechanical baseline.

## 9. Persistence semantics

Persistence SHALL be sparse but early enough to protect established identity/play state:

```text
blank scaffold
    -> gameplay may begin
    -> stable protagonist anchor adopted
    -> PROVISIONAL_IDENTITY durable write
    -> continued gameplay + rapid mechanical materialization
    -> READY_PC predicate becomes true
    -> coherent READY_PC durability transaction
    -> PLAY_READY/active when remaining campaign launch requirements are satisfied
```

The READY_PC transaction persists the **initial mechanical commitment frontier**, not a 100%-filled lifelong dossier.

Later deterministic lazy materialization and ordinary character evolution use normal durability rules.

## 10. Required R2.7 alignment

WP-04 SHALL align:

- `DEV/ARCHITECTURE/ACTOR_MODEL.md`;
- `DEV/SCHEMAS/world-actor-state.schema.json`;
- `DEV/CATALOG/entity-structures.json`;
- `GAME/CORE/CHARACTER.md`;
- `GAME/CORE/DIEGETIC_ONBOARDING.md`;
- `GAME/CORE/CHARACTER_READINESS.md`;
- `GAME/CORE/DURABILITY_GUARD.md`.

WP-19/WP-26 SHALL remove remaining setup/bootstrap prose that still uses `pre-live` / `first true live scene` assumptions.

WP-06 SHALL close advancement choice IDs/validation needed to prove the READY_PC commitment frontier.

WP-22 SHALL test provisional persistence, rapid inferred/default build convergence, no situation-aware late option selection, and lazy deterministic post-READY materialization.

Human decision required now: **NO**.
