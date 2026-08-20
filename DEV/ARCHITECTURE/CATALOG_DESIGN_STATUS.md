# HDM Catalog Design Status

Status: **STEPS 1–4 ARCHITECTURE CLOSED / STEP 5.0 CLOSED / STEP 5.1 CLOSED / STEP 5.2 NOT STARTED**

Target branch: `feature/mechanical-runtime-hot-state`

This file is a current-status index, not a second normative specification.
Detailed reasoning/history lives in linked architecture/spec documents and Git
history.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

Sequencing authority:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

## 1. Current checkpoint

Steps 1–2 are complete and retrospectively assured.

Step 3 is closed: owner decision, candidate, adversarial review, canonical spec,
machine-contract TDD alignment, integrated cases, final critical review and
same-head validation completed successfully.

Step 4 architecture is closed after its six-role rerun and Chapter retirement.
Most Step-4 machine realization remains explicitly deferred until the remaining
Steps 5–6 architecture sequence is complete.

Step 5 remains the sole active numbered architecture stage.

Completed Step-5 slices:

```text
5.0 Authority / Contamination Audit    CLOSED
5.1 Frontier Model                     CLOSED
```

Next slice:

```text
5.2 Resumable Runtime Closure          NOT STARTED
```

Broad implementation planning remains blocked until the remaining architecture
sequence is complete unless the owner explicitly changes that order.

## 2. Current machine baseline

Active catalog version: `1.6.0`.

Step 5.0 retired early owner-like placeholders that had no surviving accepted
independent lifecycle/authority contract:

```text
world.timeline_marker
transition.timeline_place
event.timeline.placed
runtime.dirty_record
runtime.publication_batch
```

It also removed obsolete active template/schema surfaces including independent
Secret storage/schema, untyped tactical storage, generic pending consequences,
duplicate checkpoint pointers, duplicate MANIFEST chronology/event cursors and
obsolete branch-root `CAMPAIGN/...` path spelling.

Current routing/ownership consequences include:

- `MANIFEST.last_checkpoint_id` is the sole latest-checkpoint pointer;
- `CURRENT.world_time.frontier` remains the current chronology marker pending
  the dedicated chronology slice;
- `CURRENT.last_event_id` is now retired and absent from the active
  current-state schema/template;
- campaign-storage paths are branch-root-relative (`STATE/`, `WORLD/`, `LIVE/`,
  `LOG/`, `CHECKPOINTS/`);
- `GAME/CAMPAIGN/` is only the engine-source template directory copied into a
  new campaign branch root.

This does not claim deferred Step-4/5 machine realization already exists.

## 3. Step 5.1 canonical frontier discipline

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md`

Owner-approved architecture: **B-NARROW**.

Two cross-cutting laws are canonical:

```text
LAW 1 — DOMAIN TYPING
Every correctness-relevant progress/coverage/revision/cursor/frontier claim
identifies its semantic domain/scope.

LAW 2 — NO IMPLICIT CROSS-DOMAIN ORDER
No ordering/comparison is inferred between different semantic domains unless an
owning contract explicitly defines the relation.
```

No generic `runtime.frontier`, common Frontier schema/API/registry, universal
comparison operation, global monotonic sequence or RecoveryCut record is
admitted.

Important classifications:

- HOT current state is a working/read view, not a frontier;
- dirty state is unpublished delta/closure bookkeeping;
- SOFT/HARD are durability classifications/requirements;
- campaign ref/reachable commit provides campaign publication evidence;
- live revisions are scope-local and independent live epochs are incomparable by
  default;
- checkpoint ID is a pointer; checkpoint is recovery descriptor/evidence, not
  current-state authority;
- chronology is independent of Git and SemanticEvent allocation order;
- Story source coverage is projection metadata and may lag;
- `runtime.id_allocator` / `campaign-allocator` owns campaign-scoped allocation
  counters and conflict bookkeeping, not progress/frontier semantics.

A composed coherent read view may use several compatible native owners, but:

```text
composed read view != merged writable authority
```

Every mutation still routes to one current writable owner for its affected
scope/entity.

`coherent source cut` is only a conceptual per-operation selection/compatibility
relation over native source markers. It has no independent identity, authority
or Step-5.1 storage contract.

## 4. `CURRENT.last_event_id` disposition

The old provisional `STATE/CURRENT.last_event_id` has been retired as a global
semantic-log/reconnect/recovery cursor.

It did not own any of the global problems it was tempting to blur together:

- campaign reconnect/resync uses campaign revision/HEAD plus scoped changed-path
  synchronization;
- active shared-scene reconnect uses live-epoch state/revision semantics;
- campaign-scoped ID allocation/conflict handling belongs to
  `runtime.id_allocator` / `campaign-allocator`;
- fictional chronology belongs to chronology evidence;
- cold recovery may require campaign + live + operational roots.

SemanticEvent IDs remain stable record identities. Explicit per-record
`last_event_id` provenance fields are not retired by this decision.
`checkpoint.valid_through_event_id` remains pending Step 5.7 and is not a
universal recovery frontier.

## 5. Campaign allocator remains a distinct owner

The accepted catalog contract remains:

```text
campaign-allocator singleton
    -> last_allocated by identity policy
    -> next derived

allocation + record creation
    -> atomic HOT operation

canonical allocation mutation
    -> joins durable publication closure

stale publication conflict
    -> reload allocator
    -> rekey only conflicting unpublished records/direct local refs
    -> retry publication

published IDs
    -> immutable / never reused
```

Central semantic ownership of counters does not imply a global synchronous lock
on every gameplay action. Eligible local IDs remain local until promotion.
Exact publication/retry and live contention semantics belong to later Step-5
slices.

## 6. Step 5.1 design chain

- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-pre-research-charter.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-research-draft.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-analytical-challenge.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-decision-brief.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-resolution-gate.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md`

Adversarial review result:

```text
BLOCKING / owner decision required: 0
SIGNIFICANT mechanically resolved: 5
MINOR resolved: 3
```

The B-NARROW decision survived review without reopening the owner decision.

## 7. Design-process improvement

`DEV/DESIGN_PROCESS.md` now includes the canonical
**Problem-Framing / Task-Brief Quality Gate** before substantive deep-design
research.

The gate requires deliberate review of the research assignment itself for
embedded solutions, stale assumptions, wrong abstraction boundaries,
mis-scoping and framing that prevents negative/simpler outcomes. It explicitly
does not prescribe one universal research-prompt template; framing must follow
the actual project/stage/goals/unknowns/evidence/failure model/cost of error.

## 8. Deferred Step-4 machine realization

The integrated implementation program after Steps 5–6 must still realize and
verify at least:

- normalized `world.lore_fact` truth/lifecycle;
- normalized `world.knowledge` stances/current ownership;
- `runtime.disclosure`;
- Context Assembler request/bundle/source-manifest contracts;
- role-specific source eligibility and disclosure evidence;
- Story root/layout/IDs/index/availability schemas;
- legacy knowledge/Secret migration;
- live knowledge/disclosure compaction alignment.

These are deferred implementation obligations, not unresolved Step-4
architecture questions.

## 9. Exact continuation

> **Step 5.1 / Frontier Model — CLOSED.**

Next architecture slice:

> **Step 5.2 / Resumable Runtime Closure — NOT STARTED.**

Do not begin Step 5.2 as part of Step-5.1 closure.