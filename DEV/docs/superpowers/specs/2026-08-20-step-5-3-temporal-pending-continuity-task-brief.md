# Step 5.3 — Temporal & Pending-Obligation Continuity — Architecture Task Brief

Status: **RESEARCH ASSIGNMENT — ARCHITECTURAL**

Date: 2026-08-20

Pre-research framing:

- `2026-08-20-step-5-3-temporal-pending-continuity-pre-research-charter.md`

## Problem statement

HDM already has owner-local temporal obligations, Step-3 stable execution/pending-child identity, recoverable Procedures/Resolutions/Continuations, and Step-5.2 bounded recovery routing. It does not yet have one canonical architecture for the transition from an armed temporal obligation through due detection/materialization to exactly-once semantic continuation across interruption or crash.

The design must make it impossible for a promised gameplay-significant obligation to disappear or execute twice merely because process/chat/runtime state was lost or a retry occurs.

## Goals

1. Define the semantic boundary between rebuildable due-candidate state and irreducible accepted mandatory execution.
2. Define no-lost/no-double invariants across that boundary.
3. Reconcile owner-local TemporalBindings with Step-3 pending-child / ExecutionSegment / idempotency semantics.
4. Define continuity rules for suspended Choice/Reaction and already accepted/reserved RNG.
5. Define how chronology insufficiency affects due evaluation without inventing total order.
6. Preserve partitionable native ownership for future multiplayer/live persistence.
7. Produce decision-ready alternatives and recommendation before any canonicalization.

## Non-goals

- final Git publication algorithm;
- checkpoint wire format;
- live CAS/compaction protocol;
- chronology storage representation;
- durability cadence/policy;
- Story/host-delivery job state machines;
- general-purpose scheduler/job framework;
- implementation or schema migration.

## Fixed constraints

- Step 5.1 B-NARROW domain typing/no implicit cross-domain order.
- Step 5.2 v2 laws, especially native-owner preservation, bounded routing, pinned hydration, owning-scope resolution, root-membership coherence and unconditional armed-temporal enrollment for independently-due source owners.
- Step 3 Alternative C execution kernel and stable pending child/firing identity.
- Temporal Agenda remains rebuildable derived state.
- Procedure remains sole owner of procedure-local ResourceState.
- Continuation does not copy Procedure/Agenda/MechanicalContext/derived caches.
- Git ordering is never fictional chronology.
- No force-push or generic pending-work authority.

## Primary repository evidence to inspect

Architecture/specification:

- current Step-5.2 canonical v2;
- Step-3 canonical execution spec and final review;
- Steps 1–2 temporal/scheduled-trigger/resource-recovery specs;
- Step-5 expanded agenda;
- current roadmap/status;
- project navigation index.

Machine/runtime contracts:

- `DEV/SCHEMAS/temporal-binding.schema.json` and related Effect/Resource/LifeState schemas;
- execution schemas for command, resolution, continuation, execution segment, pending child, boundary occurrence, receipt, RNG/roll values;
- `DEV/CATALOG/core-catalog.json` and relevant mechanical surfaces;
- `GAME/CORE/RANDOMNESS.md`;
- `GAME/CORE/CHRONOLOGY.md`;
- `GAME/CORE/RUNTIME.md`;
- `GAME/CORE/SESSION.md`;
- `GAME/CORE/MULTIPLAYER.md` / `LIVE_SCENE.md` only where ownership scope constrains the logical model;
- focused Step-2/Step-3 tests and scenario cases.

## Required analysis outputs

### A. Ownership/lifecycle matrix

For each pending/temporal family:

- owner;
- armed state;
- due evaluation;
- occurrence identity;
- materialization boundary;
- pending execution owner;
- completion/rearm/terminal state;
- recovery source;
- duplicate suppression evidence.

### B. Crash-window matrix

For every transition from armed source through completed execution, identify each possible process-loss point and prove whether restart:

- reconstructs candidate;
- resumes already-materialized child;
- suppresses duplicate selection/execution;
- blocks on insufficient chronology/evidence;
- raises integrity suspicion when impossible state is found.

### C. RNG continuity disposition

Distinguish:

- ungenerated future randomness;
- semantically reserved experiment identity;
- generated/accepted result;
- result consumed/committed;
- retry/recovery evidence.

Explicitly decide whether current `future_rng_frontier` remains necessary.

### D. Alternatives

At minimum compare:

1. owner-local atomic materialization into Step-3 pending execution identity;
2. separate durable firing/occurrence record before child materialization;
3. generic pending-obligation ledger/job model.

Do not limit research to these if evidence suggests a simpler or different model.

### E. Later-slice requirements

State only logical requirements to be satisfied by 5.5–5.9; do not select their physical implementation.

## Analytical challenge requirements

Before recommendation, explicitly test:

- strongest case for a separate firing record;
- strongest case for a generic job/obligation abstraction;
- whether owner-local atomic materialization can be expressed without requiring impossible cross-domain transactions;
- whether periodic rearm makes one-step materialization ambiguous;
- whether boundary-trigger obligations need a different identity model from metric deadlines;
- whether due evaluation can be indeterminate and how that impacts liveness;
- whether two due obligations need deterministic order or only independent idempotent identities;
- whether current Step-3 pending-child representation is sufficient after crash;
- whether RNG reservation needs sequence/frontier semantics at all.

## Exit criteria

The Step-5.3 design cycle may proceed to a decision brief only when:

1. every gameplay-significant obligation family has one semantic owner and lifecycle;
2. the candidate/materialization boundary is explicit;
3. every crash window has a no-lost/no-double disposition;
4. due evaluation cannot accidentally infer fictional order from persistence order;
5. already accepted RNG cannot be regenerated inconsistently;
6. no new abstraction lacks a concrete consumer;
7. later Step-5 responsibilities remain cleanly separated;
8. alternatives/trade-offs and a recommendation are decision-ready.
