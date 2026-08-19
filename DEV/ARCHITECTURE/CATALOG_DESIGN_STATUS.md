# HDM Catalog Design Status

Status: **STEPS 1–2 ASSURED / CLOSED — STEP 3 DECISION GATE ACTIVE**

Target branch: `feature/mechanical-runtime-hot-state`

This file is a current-status index, not a second normative specification.
Detailed reasoning/history lives in the linked architecture/spec documents and
Git history.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

Sequencing authority:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Final retrospective assurance:

- `DEV/docs/superpowers/specs/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`

## 1. Current checkpoint

Steps 1 and 2 are complete and have passed the retrospective deep-design assurance overlay.

```text
0A Catalog meta-model / class boundaries       ASSURED / AMENDED
0B Catalog evolution / identity / strata       ASSURED
A  Actor mechanical state                      ASSURED / AMENDED
B  Effects / Conditions                        ASSURED / AMENDED
C  Temporal / Recovery                         ASSURED / AMENDED
D  Mechanical evaluation / read boundaries     ASSURED / AMENDED
E  Whole Steps 1–2 integration                 ASSURED / AMENDED
```

Step 3 is again the active numbered roadmap stage and resumes from its preserved human Decision Gate:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-research-draft.md`

No Step-3 candidate specification or implementation is authorized before that material architecture decision.

## 2. Current catalog/class baseline

- catalog version: `1.3.0`;
- one coherent `ResolvedCatalogContext` interprets plain definition IDs;
- same-ID shadowing inside one resolved context is invalid;
- incompatible catalog/runtime adoption requires coherent migration or blocks;
- `definition_id` world compatibility is explicit per `world.*` kind;
- `runtime.procedure` is admitted as the independently addressable operational owner for procedure-local state;
- `world.encounter`, `runtime.procedure`, `runtime.resolution`, and `runtime.continuation` are distinct lifetimes/responsibilities.

Normative class inventory:

- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`

Machine catalogs:

- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/entity-structures.json`
- `DEV/CATALOG/identifier-policies.json`
- `DEV/CATALOG/mechanical-surfaces.json`

## 3. Step-2 ownership baseline

### Actor health and lifecycle

- `world.actor.state.hp` is the sole HP/temp-HP state authority;
- maximum HP and Bloodied are derived;
- `life_state_id` is a separate lifecycle authority;
- Dying owns death-save progress; Stable owns its recovery `TemporalBinding`;
- zero HP is not universal death and death does not purge Effects/delete Actor.

### Resources

- persistent Actor/Asset ResourceState owns `current`;
- `runtime.procedure` owns participant-local procedure ResourceState storing `spent`;
- persistent current is normalized against state-stable resolved capacity;
- procedure spent survives capacity changes and availability is derived;
- Resource definitions own baseline recovery, ResourceState remains sole mutable Resource authority;
- the initial persistent contract allows at most one metric delayed-recovery policy plus independent registered boundary recoveries.

### Effects and Conditions

- one independent target-local application is one `world.effect`;
- generic mutable stacks are absent;
- create/refresh/replace, arbitration, support, Condition aggregation, and Rule Element combination are separate responsibilities;
- `definition_id`, reusable `rules_origin_id`, concrete `source_id`, and Step-3 causal execution identity are distinct;
- Effect terminal reasons are closed registered values;
- Conditions use ordinary Effect applications and no canonical Actor Condition list;
- Condition aggregation policies are initially `presence` and `cumulative_units`;
- intrinsic rule scopes are `aggregate_once` and `per_effective_application`;
- `condition.applicability` gates current effectiveness, so later immunity may suppress a live application without terminating it;
- Exhaustion uses independent effective unit applications and derived bounded value.

### Duration, recovery, scheduled triggers

- reusable `DurationSpec` and concrete owner `TemporalBinding` are separate;
- no wall-clock/global campaign clock;
- explicitly established quantitative elapsed evidence is retained even if no timer is armed;
- Temporal Agenda is a rebuildable due index, not authority;
- boundary producer and state-owner automatic response are separate;
- `world.effect.temporal_binding` owns intrinsic lifetime only;
- a live Effect may own finite `scheduled_trigger_state[key]` bindings for declarations in `definition.effect.scheduled_triggers[key]`;
- terminal Effects cannot retain armed scheduled-trigger state;
- Step 3 owns due execution and `REARM | UNARM | OWNER TERMINAL` semantics.

### Evaluation/read/query boundary

```text
Calculation Selector
MechanicalContext accessor / registered invocation fact
runtime-only Domain Query
```

- no arbitrary path/query/eval from declarative content;
- engine-owned state uses typed accessors/calculations;
- invocation facts are a closed boolean `INVOCATION_ADJUDICATED` channel;
- explicit true/false/missing fact states are distinct;
- state-sensitive reviewed Step-2 selectors admit only `ENGINE_STATE` transitively;
- structured derived-node metadata carries dependency/input contracts;
- current Condition aggregation depends on Effect availability plus current `condition.applicability`;
- MechanicalContext is pinned to one state view; invocation-sensitive calculation identity also includes the accepted fact-input fingerprint;
- unordered multi-result runtime queries cannot use storage order as gameplay semantics.

## 4. Mandatory Step-3 carry-forward

Step 3 must incorporate these already-assured constraints:

1. `runtime.procedure` owns procedure-local participant ResourceState and any additional procedure/boundary state Step 3 proves necessary;
2. Resolution/Continuation reference Procedure identity rather than copying procedure ResourceState;
3. parent/child reactions share one Procedure and parent re-pins/recomputes after committed child effects;
4. live Effect creation/replacement materializes compact immutable application-order evidence for recency arbitration; refresh preserves it;
5. RuntimeCommand/Resolution/Continuation pin `ResolvedCatalogContext` identity/frontier;
6. incompatible catalog adoption cannot silently reinterpret suspended execution;
7. invocation facts require explicit values/provenance, missing-input failure, deterministic fingerprinting, and Continuation preservation;
8. owner-local scheduled-trigger due work enters ordinary bounded Resolution execution;
9. checkpoints serialize source owners/inputs at immutable recovery frontiers rather than derived Agenda/DAG/winner state.

## 5. Later-stage ownership

### Step 4

- lore/knowledge/secrets/disclosure authority;
- knowledge-safe context selection for invocation facts;
- explicit promotion of situational adjudication into durable truth.

### Step 5

- repository-backed checkpoint publication/restoration;
- SOFT/HARD durability and multiplayer revision/conflict semantics;
- chronology evidence persistence/compaction and cross-scene reconciliation;
- checkpoint cleanup/expiry.

### Step 6

- exact engine/ruleset/package/catalog snapshot identity metadata;
- full D&D seed/migration/catalog-gap closure;
- complete structured selector/input/dependency metadata coverage;
- proven extensions to scheduled-trigger/invocation-fact shapes;
- final full architecture/catalog/seed audit.

## 6. Documentation debt

`DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` is historical proposal material and contains examples superseded by current Step-2 contracts. It must receive a supersession cleanup/warning before implementation planning relies on it.

Older explanatory documents may contain stale catalog-version labels. The normative inventory and coordinated machine catalogs are `1.3.0`; stale labels are documentation debt, not authority.

## 7. Exact continuation

Resume **Step 3 / `IntentPlan -> Resolution -> Signal/Event` Decision Gate** from the preserved Task Brief and Research Draft.
