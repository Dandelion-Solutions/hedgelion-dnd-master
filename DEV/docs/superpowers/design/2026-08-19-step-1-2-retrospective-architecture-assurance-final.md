# Steps 1–2 Retrospective Architecture Assurance — Final Resolution

Status: **ASSURANCE COMPLETE — STEPS 1–2 ASSURED / AMENDED / CLOSED**

Target branch: `feature/mechanical-runtime-hot-state`

Master plan: `2026-08-19-step-1-2-retrospective-architecture-assurance-plan.md`

This document closes the non-numbered retrospective assurance overlay applied after Steps 1 and 2 had already been accepted. The assurance independently reconstructed early problem framing, attacked the accepted architecture, repaired concrete omissions, and then re-ran a whole-system integration pass.

The assurance does **not** replace the numbered roadmap. Step 3 resumes from its preserved Decision Gate.

## 1. Overall verdict

```text
0A Catalog meta-model / class boundaries       ASSURED / AMENDED
0B Catalog evolution / identity / strata       ASSURED
A  Actor mechanical state                      ASSURED / AMENDED
B  Effects / Conditions                        ASSURED / AMENDED
C  Temporal / Recovery                         ASSURED / AMENDED
D  Mechanical evaluation / read boundaries     ASSURED / AMENDED
E  Whole Steps 1–2 integration                 ASSURED / AMENDED
```

Final recommendation:

> **KEEP Steps 1 and 2 closed. Resume Step 3.**

No unresolved Step-1/2 architecture blocker remains.

Confidence: **HIGH**.

## 2. What the assurance changed

The pass found real omissions rather than invalidating the core architecture.

### Catalog/class boundary

- each `world.*` kind now explicitly declares whether `definition_id` is forbidden/optional/required and which definition kinds are compatible;
- `world.organization` no longer has a duplicate archetype link;
- resolved catalog strata are assembly sources, not same-ID shadowing precedence;
- one coherent `ResolvedCatalogContext` interprets plain definition IDs;
- incompatible content/runtime adoption requires coherent migration or blocks rather than mixing old/new per-instance semantics.

### Resource state

- persistent Resource `current` is normalized against state-stable resolved capacity;
- a true capacity decrease below current clamps current atomically; capacity growth alone does not restore uses;
- procedure `spent` remains unchanged by capacity shifts;
- the initial persistent Resource contract permits at most one metric delayed-recovery policy while retaining independent registered boundary recoveries.

### Effect/Condition state

- Effect provenance roles are explicitly separated: applied definition, reusable rules origin, concrete world source, and later causal execution identity;
- Effect terminal reasons are a closed registered vocabulary;
- current Condition effectiveness includes `condition.applicability`, so later immunity can suppress participation without terminating the application;
- application lifecycle, named Condition aggregation, source-relative intrinsic rules, and Effect payload remain separate.

### Temporal state

A material human architecture decision was required and approved during Slice C:

> live Effect applications may own finite owner-local stateful scheduled triggers, keyed by stable local declaration key and independent from intrinsic Effect lifetime.

This represents proven rare periodic elapsed mechanics without fake timer Effects, long-lived Resolutions, or a generic scheduler/job subsystem.

Also, explicitly established quantitative elapsed evidence can no longer be discarded merely because no timer is currently armed.

### Mechanical input/evaluation boundary

- invocation-adjudicated context facts are a closed machine-registered boolean input channel;
- engine-owned state cannot be smuggled into that channel;
- explicit true, explicit false, and missing invocation facts are distinct;
- reviewed state-sensitive Step-2 selectors admit only `ENGINE_STATE` dependencies, transitively;
- structured derived-node metadata now records input/dependency contracts;
- current Condition aggregation explicitly depends on current applicability;
- MechanicalContext/cache identity includes accepted invocation-input fingerprint when such input is allowed;
- multi-result runtime queries are unordered semantic sets unless the typed contract defines mechanical order.

### Whole-system integration

- a logical `runtime.procedure` record is admitted as the independently addressable owner of procedure-local operational state;
- Resolution/Continuation/checkpoint are not alternate writable owners of procedure ResourceState;
- live Effect applications that require recency arbitration must retain compact immutable mechanical-order evidence independent of old trace/event-body retention;
- checkpoints are immutable recovery-frontier representations, not concurrently mutable truth;
- durable publication closure follows mechanically required forward references but does not promote derived indexes or invocation facts;
- Continuations must pin resolved catalog context and cannot silently resume across incompatible adoption.

## 3. Core architecture that survived unchanged

The assurance reinforced rather than replaced these foundations:

- reusable content definition / world instance / runtime owner / protocol value are distinct classes;
- one semantic fact has one mutable authority;
- Actor HP and LifeState are separate authorities;
- procedure-local and persistent Resources share semantic concepts but not lifetime/storage authority;
- one independent target-local Effect application is one Effect instance;
- generic mutable Effect stacks are absent;
- Condition is named rules identity while concrete applications use Effect machinery;
- Effect arbitration and Rule Element contribution combination are separate;
- concentration/maintenance is a narrow support forest, not duration or generic uniqueness;
- reusable Duration semantics and concrete owner-local temporal bindings are separate;
- Temporal Agenda, Condition indexes, arbitration winners, reverse support edges, caches, and dependency DAGs are rebuildable projections;
- no background wall-clock scheduler is required;
- Calculation Selector, MechanicalContext read/input, and runtime Domain Query remain separate surfaces;
- the LLM cannot invent deterministic engine-owned mechanical authority;
- prospective state uses one pinned view and rejects dependency cycles rather than relying on evaluation order/fixed points;
- campaign-wide scans and global dependency graph rebuilds are not required for ordinary resolution.

## 4. Current catalog version

The assurance admitted the new runtime class `runtime.procedure` under the existing class-admission rule. Because the normative inventory requires a catalog version change when a new ID is admitted, the coordinated machine catalogs now use:

```text
catalog_version = 1.3.0
```

The catalog schema generation remains unchanged where appropriate (`schema_version = 1`).

Machine alignment covers:

- `DEV/CATALOG/core-catalog.json`;
- `DEV/CATALOG/entity-structures.json`;
- `DEV/CATALOG/identifier-policies.json`;
- `DEV/CATALOG/mechanical-surfaces.json`;
- corresponding Step-2 schemas/tests.

`DEV/ARCHITECTURE/CATALOG_INVENTORY.md` is aligned to catalog `1.3.0` and includes `runtime.procedure`.

## 5. Required Step-3 constraints now entering the Decision Gate

Step 3 must incorporate, not rediscover, these accepted constraints.

### Execution/runtime ownership

```text
runtime.intent_plan
    message-level ordered orchestration

runtime.command
    idempotent executable clause envelope

runtime.resolution
    one Activity invocation

runtime.procedure
    one independently addressable rules-procedure lifetime
    owns participant-local procedure ResourceState

runtime.continuation
    portable suspended Resolution authority, not procedure-state owner
```

Exact fields/phase semantics remain Step-3 design work.

### Parent/child reactions

Reaction children and parents bind the same Procedure identity where applicable. A committed child may invalidate the parent's prospective assumptions; parent resumes by advancing/re-pinning/recomputing from the safe Step-3 phase, not by restoring a stale procedure-budget copy.

### Live Effect causal order

Effect create/replace must materialize compact immutable application-order evidence sufficient for registered recency arbitration. Refresh preserves the lifecycle episode's order evidence. The representation cannot use wall time, Effect ID ordering, SQL order, or unlimited trace retention.

### Catalog context

RuntimeCommand/Resolution/Continuation pin the ResolvedCatalogContext identity/frontier used for validation. Incompatible adoption cannot silently reinterpret suspended execution.

### Invocation facts

Step 3 must define explicit boolean fact values, provenance, missing-input failure, deterministic fingerprinting, and Continuation preservation. Facts remain execution input rather than world truth.

### Scheduled triggers

A due owner-local scheduled Effect trigger enters ordinary bounded Activity/Resolution execution. Step 3 owns occurrence identity, idempotency, same-time ordering, and atomic:

```text
REARM | UNARM | OWNER TERMINAL
```

### Checkpoint continuity

Step 3 identifies checkpointable in-flight source state; Step 5 later owns repository publication/restoration. Checkpoint content must preserve owners/inputs needed for deterministic resume, not derived Agenda/DAG/winner authority.

## 6. Required Step-4 constraints

Step 4 must define:

- durable lore/knowledge/secrets/disclosure authority;
- knowledge-safe context selection for invocation-adjudicated facts;
- explicit promotion of a situational adjudication into durable truth when actually required;
- no retroactive rewriting of historical mechanical input merely because a proposition later becomes established lore.

## 7. Required Step-5 constraints

Step 5 must define:

- repository-backed runtime checkpoint publication/restoration;
- checkpoint frontier selection/cleanup/expiry;
- SOFT/HARD durability and multiplayer conflict/revision semantics;
- chronology-evidence persistence/compaction;
- cross-scene temporal reconciliation;
- restoration of local procedure/effect/execution owners without making immutable checkpoints a parallel mutable authority.

## 8. Required Step-6 constraints

Step 6 must close:

- exact engine/ruleset/package/catalog snapshot identity and compatibility metadata;
- full D&D seed/migration/catalog-gap coverage;
- complete structured selector/input/dependency metadata coverage;
- any proven extension of scheduled-trigger or invocation-fact value shapes;
- migration handling for incompatible active definition changes;
- final full architecture/catalog/seed audit.

## 9. Documentation debt

The historical `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` is explicitly an older proposal and still contains examples from before the accepted Step-2 refinements, including generic Effect-stack assumptions and engine-owned pseudo-fact examples.

It is not current normative authority. Before implementation planning relies on it, add a supersession warning/cleanup against current Activity, Rule Element, Step-2, and assurance contracts.

Some older explanatory documents may also contain stale catalog-version labels. The normative inventory and machine catalogs are `1.3.0`; stale labels are mechanical documentation debt and cannot override them.

## 10. Assurance evidence

The assurance used solution-blind charters, targeted coverage/research, independent adversarial reviews, and resolutions for the substantive slices.

Machine amendments were introduced through focused RED→GREEN tests. In each major RED pass, the maintenance audit and pre-existing test suite remained green while only the newly asserted missing contract failed. Subsequent GREEN passes ran the complete repository validation workflow.

The final assurance closure still requires one fresh full validation on the final documentation/status HEAD before this document's completion claim is used for implementation gating.

## 11. Final gate

After fresh final validation:

```text
Steps 1–2 retrospective assurance = CLOSED
Step 3 = resume saved Decision Gate
```

No candidate Step-3 specification or implementation is authorized until the human architect resolves the Step-3 material execution-boundary choices.
