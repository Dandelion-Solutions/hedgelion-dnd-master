# S6D-09 — Domain Rules Coverage Matrix — Collaborative Review

Status: **STEP 4 COMPLETE — OWNER DECISION C INCORPORATED**

Date: 2026-08-27

## 1. Accepted product boundary

The built-in MVP supports a minimal playable gameplay spine, not a broad D&D corpus. The spine consists of generic typed check/save resolution; minimal initiative/turn/action/movement procedure; bounded spatial inputs; basic significant-Asset ownership/equip/use/transfer; hazard/social uncertainty lowered through check/save; reward-item ownership lowered through Asset transition; and the already accepted S6D-07/08 exact routes.

The decision does not enumerate player actions and grants no primitive activation authority.

## 2. Whole-project challenge result

### Generic check/save

No new primitive is required. Existing active `op.roll`, `op.resolve_check` and `op.resolve_save`, selectors `check.roll`/`save.roll`, strict RollRequest/Result, adjudicated parameter bindings and Step-3 receipt/retry owners are sufficient. S6D-09 requires two exact reusable Activity consumers, not a universal rules DSL. Ability/proficiency, threshold and situational inputs are bound by declared parameters; missing/stale/unauthorized input fails closed.

### Procedure and movement

`runtime.procedure` already owns procedure-local order, turn, action and movement budgets. Actor `location_id` and the applicable scene/location/zone owner retain durable world placement. No tactical map, pathfinding, global geometry service or duplicated Encounter timing owner is introduced.

Ordinary movement lowers to a typed direct TransitionRequest validated against the pinned Procedure budget and a bounded destination/spatial binding. This makes `op.move_entity` unnecessary for the current spine: no current Activity needs a reusable internal movement step inside a compiled multi-step Activity.

### Spatial inputs

Existing TargetSpec/AreaSpec and Activity parameter bindings are sufficient for exact supported Activities. Engine-known Actor/Scene/Zone/location/target state remains engine-owned. The current MVP spatial profile is deliberately engine-bound only. It does not consume or activate dormant `fiction.target_visible`, `fiction.target_reachable` or equivalent adjudicated spatial facts. A future exact consumer must first amend the S6D-04 owner; S6D-09 cannot create that authority indirectly.

**Superseded spatial detail after Senior audit.** The engine-bound-only/dormant-reachability conclusion above is replaced by the narrow S6D-09 repair: `fiction.target_reachable` is active only for seven named existing `op.select_targets` consumers and is fixed per consumer/source/TargetSpec/AreaSpec/candidate/provenance/pinned-rules-context binding. It is not world truth and has no lifecycle. `fiction.target_visible` remains dormant. Durable Actor location changes require a current canonical `world.location`; within-location repositioning spends Procedure movement without an Actor-location mutation or fake location. The repair creates neither a geometry/query engine nor new primitive authority.

### Asset ownership/equip/use/transfer

`world.asset` already owns `owner_actor_id`, exclusive location/container placement and equipment mode. Basic reward transfer, equip/unequip and use lower to closed typed direct transitions against that owner. No inventory aggregate, currency ledger or generic economy service is created.

`op.transfer_asset` is unnecessary for the current spine because no admitted compiled Activity needs Asset transfer as an internal Activity step. If a later exact Activity does, it must run a fresh Necessity Challenge.

### Hazard, social and reward

These are fictional/domain entry points, not new mechanical engines:

- social uncertainty -> generic check/save -> outcome/receipt -> only separately justified owner transition;
- hazard uncertainty -> generic check/save -> existing damage/Effect or direct location/resource transition when exact;
- reward item -> existing world.asset creation/identity -> bounded asset-owner transition.

An outcome may be Mechanical-Null. Prose consequences remain prose unless an accepted owner transition is required.

## 3. Primitive Necessity Challenges

| Primitive | Exact current consumer | Result |
|---|---|---|
| `op.roll` | generic check/save Activities | already active; add exact consumers |
| `op.resolve_check` | generic check Activity | already active; add exact consumer |
| `op.resolve_save` | generic save Activity | already active; add exact consumer |
| `op.move_entity` | none; direct transition is sufficient | remain quarantined |
| `op.transfer_asset` | none; direct transition is sufficient | remain quarantined |
| `op.open_reaction_window` | no exact seed consumer | remain quarantined |
| `op.resolve_contest` | explicitly outside scope | remain quarantined |
| `op.advance_local_time` | chronology/procedure owner transition suffices | remain quarantined |

Compiler lowering and existing owner transitions are preferred. No new primitive passes the challenge.

## 4. Required end-to-end walkthrough

```text
Player attempts to persuade a guard to allow entry.
-> GM interprets intent and fictional leverage; no “persuade guard” action ID is created.
-> activity.check.generic binds actor, ability/proficiency basis, adjudicated DC and provenance.
-> op.roll fixes RNG; op.resolve_check deterministically produces outcome and receipt.
-> no world mutation is required merely because the guard refuses: Mechanical-Null is valid; the genuine check-resolution event and receipt remain.

The party then crosses a damaged gallery containing a falling-stone hazard.
-> hazard signs/trigger remain fiction/world.hazard state where identity matters.
-> avoiding the hazard reuses activity.save.generic with a typed threshold.
-> failure lowers to the existing exact damage route; success may be Mechanical-Null.

The PC moves to an engine-identified pillar location.
-> fiction establishes intent, but the admitted transition consumes only the engine-bound destination/location references.
-> one direct transition validates actor and Procedure revisions, destination and current movement budget.
-> one ExecutionSegment atomically advances runtime.procedure movement spent and changes Actor location; partial commit is forbidden.

Hostility becomes initiative-scale.
-> runtime.procedure establishes participants, fixed initiative order, round/turn cursor and per-participant action/movement budgets.
-> supported ranged attack/spell Activities reuse the existing exact S6D-07/08 routes.
-> no generic reaction window is opened because no supported exact consumer requires one.

After victory the guard grants a significant item.
-> the item is one world.asset with a definition when reusable mechanics matter.
-> a direct asset-transfer transition validates current owner/location and new owner.
-> the same owner transition serves reward, gift and loot fiction; no reward engine or transfer-action vocabulary is added.
```

This walkthrough uses one small spine across social, exploration/hazard, movement/spatial judgment, combat and reward. Fiction chooses among existing routes; it does not invent execution capability.

## 5. Review findings resolved

- General check/save are exact reusable Activities, not unconstrained schemas.
- Procedure state is owner-local and bounded; Encounter is not a second owner.
- Movement has no pathfinding or universal position model.
- Asset transitions do not create inventory/economy authority.
- Mechanical-Null remains first-class.
- The older “every roll produces StateDelta” wording in GAME/CORE must be synchronized to “typed outcome/consequence, plus owner mutation only when required”.
- Outside-scope families remain absent/nonselectable with explicit revisit triggers.

No further human decision is required for the candidate.

