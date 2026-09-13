# PB-02 Source Manifest — RD-01..RD-04

Status: **PB-02 CONTROLLED SOURCE MANIFEST / IMPLEMENTATION PLANNING ONLY**

Baseline HEAD: `d159a7dfc551b51175b6fe3225d01c472dc50479`

This manifest is subordinate to accepted native owners, the exact WP-27 Step-2 readiness records, the WP-27 canonical readiness specification and the critic-approved bounded decomposition v2. It authorizes no production implementation.

## Shared controlling sources

- `DEV/CURRENT_PROGRESS.md`
- `DEV/docs/superpowers/design/2026-09-13-implementation-planning-task-brief.md`
- `DEV/docs/superpowers/design/2026-09-13-implementation-planning-candidate-bounded-decomposition-v2.md`
- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-evidence-ledger.md`
- `DEV/docs/superpowers/specs/2026-09-11-r2-7-WP-27-final-implementation-planning-readiness-canonical-spec.md`
- package conventions + Impact/TDD contract under `DEV/docs/superpowers/plans/`.

## RD-01 — shipped/stale projection repairs

Direct readiness: `R001,R003,R033,R043,R047,R048,R050`.

Owner/source set: exact Step-2 records plus the native domain/randomness/information owners referenced there, WP-26 documentation-routing closure, current install/bootstrap projections.

Current machine/projection surfaces inspected:
- `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` and current install/bootstrap documentation;
- `GAME/CORE/**` including the partially v1-compatible information prose;
- current GAME/DEV routing and maintenance-validation surfaces.

Currentness resolution: old references to `GAME/AGENTS.md` and `GAME/CORE/START.md` are stale; these paths are absent and must not be recreated merely to satisfy historical path literals. RD-01 repairs the actual shipped instruction projections and stale runtime-path assumptions.

## RD-02 — information / knowledge / disclosure / message

Direct readiness: `R007,R008,R009,R017,R049,R052`.
Composite slices: `R006.INFO,R016.INFO,R018.INFO,R053.INFO,R062.KNOWLEDGE,R062.DISCLOSURE,R062.RETAINED_MESSAGE`.

Canonical owners:
- Step-4 truth/knowledge/role/context Story specification;
- host delivery/disclosure boundary;
- WP-10 durable-family allocation;
- WP-11 native topology/identity/indexing.

Native family allocation that implementation must preserve:
- `world.lore_fact` -> `WORLD/LORE`;
- `world.knowledge` -> `WORLD/KNOWLEDGE`, composite identity `(knower_id,fact_id)`, no discovery index;
- `runtime.disclosure` -> `STATE/RUNTIME/DISCLOSURES`, composite identity `(player_id,fact_id)`, no discovery index;
- `runtime.message` -> `LOG/MESSAGES`, no baseline discovery index.

Current machine surfaces:
- `GAME/SCHEMA/lore.schema.yaml` plus legacy epistemic fields in `pc.schema.yaml`, `npc.schema.yaml`, `faction.schema.yaml`, `location.schema.yaml`, `item.schema.yaml`;
- `GAME/CORE/INFORMATION.md` contains useful v1 truth/knowledge/belief/player-told distinctions and is not blanket-legacy;
- `DEV/SCHEMAS` has no current owner-native knowledge/disclosure/message schema equivalents.

Required planning consequence: create explicit owner-native v1 machine contracts for lore fact, knowledge, disclosure and retained message; retire embedded/parallel legacy secret/knowledge aliases; run repository-wide stale-reference proof. Do not restore absent `world_state.schema.yaml`.

## RD-03 — Actor / Asset / Effect continuity

Direct readiness: `R025..R028,R104,R108..R111,R113..R116,R126,R128..R130,R132,R136`.
Composite slices: `R006.ACTOR,R016.ACTOR,R018.ACTOR,R029.ACTOR,R062.ACTOR_CONTINUITY_RELATIONS,R062.EFFECT_APPLICATION`.

Canonical owners:
- R2.1 continuity/history;
- R2.2 Actor continuity;
- Actor/Asset/Effect native contracts referenced by Step-2;
- WP-10 allocation and WP-11 topology.

Current v1-oriented DEV machine contracts already present:
- `DEV/SCHEMAS/world-actor-state.schema.json`;
- `DEV/SCHEMAS/world-actor-group-state.schema.json`;
- `DEV/SCHEMAS/world-asset-state.schema.json`;
- `DEV/SCHEMAS/world-effect-state.schema.json`;
- supporting entity/effect/mechanical schemas.

Legacy GAME surfaces to replace/reconcile include `GAME/SCHEMA/pc.schema.yaml`, `npc.schema.yaml`, `item.schema.yaml` and embedded epistemic/secret fields across old entity families.

Native topology: `world.actor -> WORLD/ACTORS`, `world.actor_group -> WORLD/ACTOR_GROUPS`, `world.asset -> WORLD/ITEMS`, `world.effect -> WORLD/EFFECTS`. PC/NPC indexes may classify Actors but cannot define route subtype.

Negative laws carried into plans: no one memory blob, no Actor-owned replacement for `world.knowledge`, no symmetric relationship inference, no PC voluntary-mental-state ownership, no continuous NPC simulation, no generic turn-count TTL, no Context Runtime ranking authority.

## RD-04 — owner-native routing / indexes / HOT

Direct readiness: `R015,R063..R067`; composite contribution: R018 route/root integration only after native owners finalize shape.

Canonical owners:
- WP-11 physical topology/identity/indexing;
- WP-12 HOT/SQLite/transaction realization;
- downstream publication/recovery owners only at their joins.

WP-11 fixes the deterministic framed route law, native family roots and rebuildable index dispositions. Known-ID reads derive one route without index/directory enumeration; path/shard/index/order never becomes semantic/currentness/chronology authority.

WP-12 fixes a typed native-owner HOT store over SQLite plus narrow rebuildable helpers. Exact SQL DDL, serialization, pragmas, database lifecycle and programming API remain implementation-selectable provided native family+identity uniqueness, campaign/context isolation, source-basis currentness and authority laws are mechanically enforced.

Current machine surfaces:
- `GAME/SCHEMA/index.schema.yaml` is a legacy/general index surface requiring conformance or replacement;
- current `GAME/SCHEMA` contains no HOT schema family and there is no current `GAME/HOT` authority surface;
- DEV has current owner schemas that RD-04 must consume rather than redefine.

Required planning consequence: create deterministic route/validation implementation and tests; create typed HOT owner-envelope/data-access substrate and rebuildable-helper contracts; do not create a generic ID registry, state service, global dirty frontier, SQL chronology, automatic partitioning or SQLite+LIVE distributed transaction.

## Cross-RD joins

- RD-02 and RD-03 provide owner shapes consumed by RD-04 routing/HOT integration.
- RD-04 may integrate routes only after each native family shape is final; it never becomes semantic owner.
- RD-03 supplies provisional Actor shape downstream to RD-14 onboarding/bootstrap and participates in later persistence/runtime joins.
- RD-02 supplies information contracts downstream to RD-09/RD-11/RD-13 without serializing unrelated work.

## GAME reconstruction classification

`GAME/**` is reconstructable v1 surface, not preservation constraint. Touched artifacts must be classified `V1_COMPATIBLE`, `MIXED` or `LEGACY_SUPERSEDED`. Surviving v1 laws are preserved before retiring legacy structure; no v0.8 compatibility layer is added merely because an old path exists.

## PB-02 currentness result

No owner/decomposition conflict discovered. No Product Owner decision or architecture reopen is required by this manifest. Exact worker task/file selections remain in the four PB-02 RD plans and must fresh-recheck the named surfaces before implementation writes.