# HDM Implementation Planning — Temporal Completeness Routing Repair Addendum

Status: **CURRENT MANDATORY AUTHOR REPAIR — PLANNING ONLY**
Date: 2026-09-14
Baseline before publication: `9ec618ac33a960b63b090b4aafe18381445db625`
Production implementation authorized: **NO**.

This addendum repairs an implementation-planning defect discovered by the author adversarial owner/dependency graph audit. It does not create a new semantic owner, readiness identity, scheduler, global clock, or recovery frontier.

## 1. Finding and root cause

**AUTHOR FINDING 6 — SIGNIFICANT.**

WP-15 machine-alignment items 3–6 and readiness `R076` require complete typed temporal-source routing, deterministic dependency extraction, bounded reverse invalidation/enrollment, coherent lifecycle rewrite, and cold-recovery reconstruction. The base RD-08 plan specifies dependency keys and a rebuildable Agenda but never gives cold recovery a durable completeness route from which the complete set of independently-due armed native owners can be enumerated without a forbidden scan. Its interface

```text
rebuild_temporal_agenda(native_owners)
```

therefore leaves `native_owners` unbounded/unproduced at the exact correctness edge where WP-15, Step-5.2 and Step-5.7 require complete typed routing.

RD-07 consumes “current routing/lifecycle evidence” but does not create that evidence. RD-04 family discovery indexes are explicitly non-authoritative for absence and cannot repair the gap. Agenda/current summaries/`THREAD_INDEX` likewise cannot prove temporal-root completeness.

This is a planning defect, not an architecture gap: `R076` already records architecture-blocker PASS and leaves physical routing representation as implementation choice under the accepted owner laws.

## 2. Fixed v1.0 realization boundary

The initial v1.0 realization is deliberately narrow and source-local:

```text
CAMPAIGN SOURCE
  STATE/RUNTIME/TEMPORAL_ROUTING.yaml
    = completeness-protected derivative routing companion

SELECTED LIVE SOURCE
  LIVE_STATE.yaml.temporal_routing
    = the same logical entry contract embedded in the exact-source CAS envelope
```

The campaign file is a fixed derivative companion beneath the existing `state_root`; it is **not** a new native semantic record family and needs no new MANIFEST selector. The LIVE form is embedded so owner mutation plus temporal membership can cross one exact-source CAS acceptance edge.

The initial campaign companion may remain one campaign-source file until WP-24 measured fanout/size/latency evidence requires repartitioning. No premature distributed routing service is introduced.

A healthy blank campaign scaffold contains an explicit empty companion; missing companion is not interpreted as “no armed temporal sources”.

## 3. Shared entry contract

RD-08 must add one reusable validation contract:

```text
DEV/SCHEMAS/temporal-source-routing.schema.json
GAME/SCHEMA/temporal_routing.schema.yaml
```

Conceptual entry:

```text
TemporalSourceRouteEntry {
  owner_ref: {
    native_family,
    identity_components[]
  },
  occurrence_key,
  binding_discriminator,
  dependency_keys[]
}
```

The route may carry only retrieval/completeness/invalidation evidence required by accepted owner laws. It does **not** own or copy deadline/time value, DUE result, owner lifecycle/state payload, chronology evidence, execution state, RNG, Procedure state, currentness, or fictional order.

Stable identity is owner identity + current occurrence/binding discriminator; path/list order conveys no semantics.

## 4. RD-08 mandatory replacement for R076

Base RD-08 Checkpoint 3 remains the temporal semantic owner checkpoint but is strengthened as follows.

### Future file actions

- `NEW_CREATE DEV/SCHEMAS/temporal-source-routing.schema.json`
- `NEW_CREATE GAME/SCHEMA/temporal_routing.schema.yaml`
- `NEW_CREATE GAME/CAMPAIGN/STATE/RUNTIME/TEMPORAL_ROUTING.yaml`
- `EXISTING_MODIFY GAME/TOOLS/temporal.py`
- `EXISTING_MODIFY DEV/TESTS/test_rd08_temporal.py`
- exact README/project-map/audit projections only as required by the new shipped contract.

### Required interfaces

```text
derive_temporal_route_entry(owner_state, binding, source_scope) -> TemporalSourceRouteEntry | NONE
reconcile_temporal_route_membership(before_owner, after_owner, source_route) -> TemporalRouteDelta
resolve_temporal_dependency_dependents(source_route, dependency_key) -> tuple[TemporalOwnerRef, ...]
rebuild_temporal_agenda_from_route(source_route, hydrated_owners, chronology_evidence) -> AgendaEntries
```

`derive_temporal_dependency_keys(...)` remains owner-family logic and supplies the complete declared key set consumed by the route entry.

### Required lifecycle behavior

For every independently-due admitted temporal occurrence:

```text
ARM / provider move / SAFE_REBASE / rearm
  -> owner state + exact current route entry

unarm / terminalize
  -> owner state + route removal

claim/materialize accepted execution
  -> owner occurrence closure + route removal/replacement
     + accepted execution root/evidence under RD-05
```

Every transition computes the route delta from native owner semantics. Route presence never defines lifecycle.

`INDETERMINATE` does not remove an otherwise independently-due armed occurrence when future admitted evidence may decide it.

### Required focused tests

Add `TemporalRoutingCompletenessTests` proving at minimum:

1. each admitted independently-due armed owner/binding family yields exactly one current route membership per current occurrence;
2. all declared dependency keys survive round-trip and can boundedly nominate every affected enrolled occurrence;
3. provider move/rebase/rearm rewrites membership without omission gap;
4. unarm/claim/terminalization removes or replaces membership coherently;
5. `INDETERMINATE` remains enrolled when later evidence can decide it;
6. `THREAD_INDEX`, CURRENT, Agenda and directory enumeration cannot prove absence;
7. missing required route entry is a coherence/integrity defect, never semantic termination;
8. Agenda is rebuilt from validated current route + hydrated owner state and may be deleted/rebuilt without canon loss;
9. route entry cannot carry deadline/DUE/chronology/execution/RNG/owner-state authority;
10. technical ordering of route entries is non-semantic.

Checkpoint 3 is publishable only when `TemporalBindingAgendaTests` **and** `TemporalRoutingCompletenessTests` are green.

## 5. RD-06 campaign publication join

RD-06 keeps campaign publication ownership. It does not gain temporal semantics.

For campaign-owned lifecycle changes that create/change/remove required temporal membership, `freeze_campaign_publication_attempt(...)` and bounded resulting-tree validation must consume the owner mutation and matching `STATE/RUNTIME/TEMPORAL_ROUTING.yaml` delta as one required campaign-domain closure.

Add an integration scenario to `PublicationPlanTests` / `PublicationOutcomeTests` proving:

- durable armed owner without required membership is rejected before publication acknowledgement;
- durable membership pointing to absent/incompatible owner is rejected;
- owner lifecycle + route delta enter one base-derived resulting tree;
- stale publication cannot acknowledge a split owner/route basis;
- no-write proof is invalid if owner/routing coherence is unresolved.

This is a `JOIN_BEFORE_INTEGRATION` for the implicated durability edge, not a whole-RD hard prerequisite.

## 6. RD-09 LIVE exact-source CAS join

RD-09 remains sole owner of LIVE currentness/CAS and of `live_scene.schema.yaml`.

The future LIVE envelope must include the same logical routing contract as a required `temporal_routing` member, empty when no independently-due LIVE-owned occurrence is enrolled.

RD-09 Task 3/6 future actions are strengthened:

- `EXISTING_REPLACE GAME/SCHEMA/live_scene.schema.yaml` includes validated `temporal_routing`;
- `FrozenLiveAttempt` includes the exact temporal membership delta whenever the accepted native owner transition changes enrollment;
- the exact-source CAS establishes owner/current source state + matching route membership together;
- rejected/stale CAS establishes neither;
- accepted CAS cannot be locally rolled back if later cache adoption fails.

Add LIVE tests proving route/owner split cannot become an acknowledged current source and that campaign temporal routing never claims LIVE-owned current truth.

RD-08 supplies temporal membership semantics/entry derivation; RD-09 owns the physical LIVE acceptance edge. No concurrent independent write to `live_scene.schema.yaml` is allowed.

## 7. RD-07 cold-recovery consumer

RD-07 keeps recovery/source-selection ownership and gains no temporal authority.

After current mutable sources are selected and exact-pinned, recovery must:

```text
campaign source -> load exact STATE/RUNTIME/TEMPORAL_ROUTING.yaml
selected LIVE source(s) -> read embedded temporal_routing from exact LIVE_STATE basis
-> hydrate every routed native owner by exact owner route/current source
-> validate owner lifecycle/occurrence/binding against membership
-> reconstruct complete reverse dependency enrollment
-> rebuild Agenda
-> final basis validation
-> READY
```

Required failure behavior:

- missing campaign companion => `BLOCKED`/scoped integrity result, never “empty”; 
- membership -> missing/incompatible owner => scoped integrity result;
- current armed owner proven through another bounded owner path but omitted from required membership => completeness defect;
- selected source movement during hydration => `RETRY`;
- no healthy path may fall back to WORLD/thread/repository/history scan;
- accepted claimed/materialized work resumes through RD-05 instead of reopening the source occurrence.

Strengthen `CurrentSourceSelectionTests` and `AcceptedExecutionRecoveryTests` with the above scenarios.

## 8. RD-14 blank-scaffold consumer

The v1.0 template contains:

```text
GAME/CAMPAIGN/STATE/RUNTIME/TEMPORAL_ROUTING.yaml
```

with an explicitly valid empty route set. RD-14 generator/scaffold verification must prove the file survives blank campaign generation. This is static bootstrap material only; it creates no gameplay occurrence and no temporal prerequisite for PLAY_READY beyond schema-valid blank routing evidence.

Because v1.0 is clean-slate, no legacy v0.8 migration/shim/preservation path is required for the old absence of this file.

## 9. Proof and coverage joins

This repair discharges existing readiness only:

```text
R076 -> RD-08 TemporalRoutingCompletenessTests
      + RD-06 campaign publication coherence scenario
      + RD-09 LIVE route/CAS coherence scenario
      + RD-07 recovery reconstruction/no-scan scenario
```

No new readiness identity is created.

R077 item 17 package witness must explicitly include the current temporal routing artifact and campaign/LIVE publication/recovery failure-injection joins; “missing enrollment” without a real route implementation is no longer sufficient evidence.

R074 and R080 continue under their existing owner ledgers; their recovery/LIVE scenarios consume this repaired route where temporal enrollment participates but do not gain temporal semantics.

## 10. Execution-wave edges

Add these bounded edges to the current wave model:

```text
RD-08 temporal owner/membership semantics
    CONSTRAINS_WITHOUT_ORDERING RD-06 campaign publication
    CONSTRAINS_WITHOUT_ORDERING RD-09 LIVE CAS

RD-08 route + RD-06 implicated campaign publication
    JOIN_BEFORE_INTEGRATION RD-07 campaign temporal recovery READY

RD-08 route + RD-09 implicated exact-source CAS
    JOIN_BEFORE_INTEGRATION RD-07 selected-LIVE temporal recovery READY
```

Owner-local RD-06/RD-07/RD-09 work unrelated to temporal membership may proceed independently. Wave numbering does not become a barrier.

## 11. Negative laws

The repair forbids:

- Agenda as durable root/completeness authority;
- `THREAD_INDEX`, CURRENT or ordinary family indexes as absence proof;
- campaign-wide/world/history/directory fallback scan;
- new semantic temporal owner;
- durable DUE flag;
- generic scheduler/job queue/firing ledger;
- routing-owned deadlines/chronology/RNG/execution state;
- one cross-domain global routing singleton;
- campaign route claiming LIVE current truth;
- SQLite/HOT cache as cold completeness authority;
- legacy v0.8 preservation shim.

## 12. Version / migration disposition

Planning-only publication Version Impact: **NONE**.

Future implementation introduces a v1.0 persistent derivative routing contract and must run the normal Version Impact Gate for the actual GAME schema/API/template delta. Under the Product Owner clean-slate constraint, no v0.8 compatibility migration is required solely because the routing companion is new.

## 13. Finding disposition

```text
AUTHOR_FINDING_6: SIGNIFICANT
ROOT_CAUSE: R076 completeness-routing producer missing between native lifecycle and Agenda/recovery consumers
ARCHITECTURE_REOPEN: NO
HUMAN_DECISION_REQUIRED: NO
REPAIR_STATE: PLANNED IN THIS MANDATORY ADDENDUM
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
