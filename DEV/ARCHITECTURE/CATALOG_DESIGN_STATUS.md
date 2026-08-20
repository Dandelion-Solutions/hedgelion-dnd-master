# HDM Catalog Design Status

Status: **STEPS 1–4 ARCHITECTURE CLOSED / STEP 5.0–5.2 CLOSED / STEP 5.3 NOT STARTED**

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
5.2 Resumable Runtime Closure          CLOSED
```

Next slice:

```text
5.3 Temporal & Pending-Obligation Continuity    NOT STARTED
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
- `CURRENT.last_event_id` is retired from active current-state schema/template;
- campaign-storage paths are branch-root-relative (`STATE/`, `WORLD/`, `LIVE/`,
  `LOG/`, `CHECKPOINTS/`);
- `GAME/CAMPAIGN/` is only the engine-source template directory copied into a
  new campaign branch root.

This does not claim deferred Step-4/5 machine realization already exists.

## 3. Step 5.1 canonical frontier discipline

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md`

Owner-approved architecture: **B-NARROW**.

Two cross-cutting laws remain canonical:

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

Important consequences:

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

A composed coherent read/recovery view may use several compatible native owners,
but:

```text
composed read view != merged writable authority
```

## 4. `CURRENT.last_event_id` disposition

The old provisional `STATE/CURRENT.last_event_id` remains retired as a global
semantic-log/reconnect/recovery cursor.

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

Step 5.2 adds the recovery consequence that a promised recoverable owner may not
require a shorter-lived local identity that would disappear on cold restart;
such dependencies must be promoted/materialized before that recovery source set
is acknowledged.

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

## 7. Step 5.2 canonical recovery-closure discipline

Current canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`

The earlier `...canonical-spec.md` remains historical derivation and is
superseded for current Step-5.2 authority by v2.

Canonical result:

> **Resumable Runtime Closure is a correctness property over compatible
> domain-native durable sources and gameplay-significant native owners reachable
> from bounded typed recovery routing. It is not a new semantic owner or closure
> record.**

Key consequences:

- native world/runtime/live owners remain current authority;
- normal cold recovery requires bounded typed operational-root discovery, not
  history/world scans;
- routing/index membership is recovery evidence only;
- routing must be partitionable by existing writable scopes and cannot require a
  globally hot singleton;
- Procedure remains independently recovery-relevant across gaps between Commands;
- Continuation/Resolution/Command preserve accepted fixed execution inputs and
  pending child/response continuity under Step 3;
- Temporal Agenda remains rebuildable from native temporal owners;
- every armed temporal owner whose admitted obligation can become due
  independently of ordinary owner loading stays in typed temporal-source routing
  for its whole armed lifetime, even if another root also reaches it;
- one hydration attempt pins every mutable native source to an exact revision;
- recovery resolves through current owning scope, so stale campaign copies cannot
  silently replace live-owned truth;
- owner activation/terminality drives required operational-root enrollment and
  publication must keep membership coherent;
- suspended execution requires resolvable compatible runtime/catalog/rules
  interpretation context;
- a checkpoint remains sparse recovery evidence and cannot be the sole current
  active-root source;
- exact root/index/checkpoint/live physical representation is deferred to 5.7/5.8.

For temporal routing, duplicate **references** are intentionally allowed where
needed for the simpler armed-lifetime invariant. Routing never owns duplicated
deadline, due/order/firing state or lifecycle.

Step-5.2 review chain found no blocking owner decision. The final refinement
removed a conditional reachability optimization that would have coupled temporal
enrollment to unrelated root termination.

Step 5.2 also carries generated/emitted/acknowledged player-delivery ambiguity
forward to Step 5.12 rather than making transcript/narration mechanical authority.

## 8. Step 5.2 design chain

- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-pre-research-charter.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-research-draft.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-analytical-challenge.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-decision-brief.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-resolution-gate.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-adversarial-review-addendum.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-resolution-gate-addendum.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`

## 9. Design-process improvement

`DEV/DESIGN_PROCESS.md` includes the canonical **Problem-Framing / Task-Brief
Quality Gate** before substantive deep-design research.

The gate requires deliberate review of the research assignment itself for
embedded solutions, stale assumptions, wrong abstraction boundaries,
mis-scoping and framing that prevents negative/simpler outcomes. It does not
prescribe one universal prompt template.

## 10. Deferred machine realization

The integrated implementation program after Steps 5–6 must still realize and
verify existing Step-4 obligations plus Step-5.2 recovery realization including:

- normalized Step-4 truth/knowledge/disclosure/Story machine surfaces;
- repository placement/schemas for accepted Step-3 runtime owners;
- bounded active runtime and temporal-source recovery routing;
- deterministic Procedure lifecycle evidence;
- Interaction/message pending-input realization;
- SAVE/session completeness alignment with operational owners;
- cold hydration runtime/catalog interpretability validation;
- later checkpoint/live physical routing selected by 5.7/5.8;
- exact future-RNG representation reconciled by Step 5.3.

These are deferred implementation obligations, not unresolved Step-5.2
architecture questions.

## 11. Exact continuation

> **Step 5.2 / Resumable Runtime Closure — CLOSED.**

Next architecture slice:

> **Step 5.3 / Temporal & Pending-Obligation Continuity — NOT STARTED.**

Do not begin Step 5.3 as part of Step-5.2 closure verification.