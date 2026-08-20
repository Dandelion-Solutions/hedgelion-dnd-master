# HDM Mechanical Architecture — Six-Step Roadmap

Status: **ACTIVE WORKING PLAN**

Target branch: `feature/mechanical-runtime-hot-state`

This roadmap is the sequencing gate for the current architecture program. It is
a status/order document, not a duplicate normative specification. Closed-step
semantic detail belongs to the linked canonical specifications.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

## Operating rule

- Exactly one numbered architecture step may be `IN PROGRESS`.
- Later steps may be inspected only to expose dependencies/contradictions.
- A step closes when its architecture artifacts/review/verification pass and
  every unresolved implementation item has an explicit later owner or deferred
  implementation obligation.
- Architecture-stage closure does **not** imply that every accepted contract is
  already implemented in GAME/runtime machine schemas.
- Per owner direction, Steps 4–6 complete the remaining architecture sequence
  before broad implementation planning begins.
- After all major modules have designs, run one holistic architecture review over
  the complete ownership graph, schemas, logic and cross-module relationships.

## Program roadmap

| # | Status | Scope | Exit result |
|---:|---|---|---|
| 1 | **COMPLETE / ASSURED** | Critical audit of catalog/class architecture and accepted baseline | All findings fixed, owned or consciously deferred |
| 2 | **COMPLETE / ASSURED** | Resources, HP/LifeState, Effects, Conditions, Duration, Recovery, selectors/query boundaries | Accepted ownership/mechanics contracts and assurance |
| 3 | **COMPLETE / ASSURED** | `IntentPlan -> Resolution -> Signal/Event`, deterministic execution boundary, Procedure/Continuation | Canonical Alternative-C execution contract |
| 4 | **COMPLETE / ARCHITECTURE CLOSED** | Truth/lore, fictional knowledge, disclosure, six logical LLM roles, Context Assembler, Story, promotion | Canonical information/role/Story architecture |
| 5 | **IN PROGRESS** | Durability, recovery, multiplayer/live authority, chronology, Story/transcript publication/retention | Coherent publication/recovery/shared-state architecture through 5.14 |
| 6 | `BLOCKED BY 5` | Modes, physical LLM orchestration/budget, deployment feasibility, migration/catalog/seed closure, holistic review | Enforceable mode/context topology and final architecture closure |

## Steps 1–2 retrospective assurance

Final retrospective assurance:

- `DEV/docs/superpowers/specs/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`

Steps 1–2 remain closed and assured.

## Step 3 — CLOSED / ASSURED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`

Final critical review:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-final-critical-review.md`

Owner-approved architecture: **Alternative C**.

Core ownership remains:

```text
Interaction
    -> IntentPlan
        -> RuntimeCommand
            -> ActionRequest -> Resolution(Activity)
            OR
            -> TransitionRequest -> direct deterministic execution

runtime.procedure
    sole procedure-local ResourceState owner

Resolution / direct transition
    -> embedded ExecutionSegment(s)
        -> committed MechanicalEvents
        -> receipts/idempotency
        -> mandatory child descriptors

Continuation
    portable suspended Resolution generation
```

## Step 4 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`

Step 4 fixed objective-truth / fictional-knowledge / human-disclosure ownership,
the six logical LLM roles, deterministic Context Assembler, noncanonical
four-layer Story model and promotion/migration boundary.

Physical role-call topology remains Step 6 work. Feasibility notes already
preserved for that future spike:

- `DEV/docs/superpowers/specs/2026-08-20-step-6-llm-role-isolation-feasibility-spike-notes.md`

The obsolete literary world vocabulary remains retired:

```text
world.chapter
transition.chapter_append
event.chapter.appended
```

## Step 5 — active architecture stage

Expanded historical/working agenda:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-expanded-architecture-agenda.md`

Current slice order:

```text
5.0  Authority / Contamination Audit
5.1  Frontier Model
5.2  Resumable Runtime Closure
5.3  Temporal & Pending-Obligation Continuity
5.4  Host Lifecycle & Session Handoff
5.5  SOFT / HARD / SAVE Durability Semantics
5.6  Campaign Publication & Crash Consistency
5.7  Checkpoint / Recovery Protocol
5.8  Multiplayer / Live-Epoch Ownership
5.9  Chronology Persistence & Reconciliation
5.10 Story Projection Durability
5.11 Transcript / History Retention & Compaction
5.12 Host Delivery / Disclosure Boundary
5.13 Garbage Collection / Orphan Cleanup
5.14 Full Recovery & Concurrency Adversarial Review
```

### Step 5.0 — CLOSED

Final artifact:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-0-authority-contamination-final.md`

5.0 retired obsolete/ownerless machine-visible abstractions before later
persistence design. Catalog `1.6.0` remains the machine baseline produced by
that cleanup.

### Step 5.1 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md`

Owner-approved decision: **B-NARROW**.

Canonical shared laws:

```text
LAW 1 — DOMAIN TYPING
Every correctness-relevant progress/coverage/revision/cursor/frontier claim
identifies its semantic domain/scope.

LAW 2 — NO IMPLICIT CROSS-DOMAIN ORDER
No ordering/comparison is valid across different semantic domains unless a
specific owning contract explicitly defines it.
```

No generic Frontier record/API, universal sequence or RecoveryCut authority was
introduced.

### Step 5.2 — CLOSED

Current canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`

Step 5.2 defines **Resumable Runtime Closure** as a correctness property over
compatible domain-native durable sources + bounded typed recovery routing.
Native owners remain authority; Temporal Agenda/caches are rebuilt; mutable
sources are pinned to exact revisions; armed independently-due temporal owners
remain enrolled; lost unpublished HOT/SOFT state is never invented.

No universal snapshot/RecoveryCut/serialized Temporal Agenda was introduced.

### Step 5.3 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md`

Owner-approved decision: **A-NARROW / OWNER-CLAIM MATERIALIZATION**.

Canonical consequences include derived due evaluation, distinct occurrence
identity, direct/rearm/contingent-claim materialization, Step-3 execution
authority, continuous bounded recovery reachability, experiment-scoped accepted
RNG continuity and no implicit ordering between unrelated due obligations.

No generic scheduler/job queue/pending ledger/firing authority was introduced.

### Step 5.4 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-canonical-spec.md`

Owner-approved decision: **BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF**.

Successful controlled handoff requires actual durable Resumable Runtime Closure;
unexpected loss recovers only actual durable native sources. Host/chat lifecycle
is not gameplay authority. Clean handoff creates no heartbeat write. Advisory
capacity heuristics are not durability authority.

### Step 5.5 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md`

Owner-approved decision: **EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY**.

Core canonical consequences:

```text
EPHEMERAL/ESTABLISHED is separate from DURABLE/VOLATILE_DIRTY
SOFT = established dirty state whose durability may currently defer
HARD = MUST_BE_DURABLE_BEFORE(named edge), not an intrinsic fact class
required durable source closure != physical pending write set
durability closure = policy roots + accumulation roots + required dependencies
explicit save protects every established dirty root in selected save scope + closure
failed save does not hard-lock coherent local/private play
correctness-critical edge cannot be falsely crossed without required durability
unpublished exposure is scope-policy-owned risk control, not semantic expiry
no universal numeric dirty threshold
clean state never creates heartbeat/no-op publication
```

The old runtime `one hour / durable_frontier_time` contract is noncanonical
implementation debt.

### Step 5.6 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md`

Architecture direction: **PYTHON-OWNED SINGLE-REF CAS PUBLICATION**.

Owner-fixed boundary:

> Runtime repository/GitHub work is executed by deterministic Python core; LLM
> roles do not directly own repository publication.

Canonical consequences include:

```text
one campaign durability transaction
    -> one complete validated base-tree-derived tree
    -> one single-parent commit from pinned H
    -> one non-force/fast-forward authoritative ref transition

prepared Git objects are never campaign authority
preflight ref probe is optimization; final guard is parent(H)+non-force update
ambiguous ACK uses bounded current-ref + lineage + current-closure verification
HEAD movement is checked against bounded semantic/read/auth/recovery dependencies
persistence retry does not replay accepted gameplay/RNG by default
automatic contention retries are bounded
publication dirty clearing is frozen-generation-specific
successful native-domain publication remains real after another domain fails
no distributed transaction, rollback-by-force, generic merge or transaction journal
no checkpoint/Story/transcript publication merely because campaign state publishes
```

Host/deployment prerequisite discovered by 5.6:

- every persistence-capable deployment must provide Python core a trustworthy
  authenticated `RepositoryPort`/equivalent;
- there is no LLM-owned Git fallback in canonical runtime architecture.

Preliminary Step-6 transport feasibility evidence is preserved in:

- `DEV/docs/superpowers/specs/2026-08-20-step-6-repository-port-transport-feasibility-spike.md`

### Step 5.7 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`

Architecture direction:

**CURRENT-AUTHORITY-FIRST / CHECKPOINT-OPTIONAL NATIVE-ROUTED BOUNDED RECOVERY**.

Derivation/review artifacts:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-research-draft.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-analytical-challenge.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-resolution-gate.md`

Canonical consequences include:

```text
ordinary cold recovery starts from current campaign authority, not checkpoint
campaign HEAD anchors discovery but does not prove complete multi-domain RRC
current owning-scope routing selects native sources
all participating mutable sources are exact-revision pinned per attempt
Step-5.2 native typed routing/lifecycle owns bounded root discovery
checkpoint may be completely ignored during healthy ordinary recovery
checkpoint is optional immutable evidence/maintenance metadata, never state authority
stale checkpoint never rolls newer valid native authority backward
checkpoint hints are non-exhaustive and require current validation
checkpoint absence does not invalidate save or recovery
root-routing/lifecycle basis participates in final validation
derived Agenda/cache/context state rebuilds
recovery result is READY | RETRY | BLOCKED plus typed reason, separate from canon integrity
READY is a validated basis, not a lock/lease or bypass of later CAS/fencing
source movement causes bounded retry, not automatic corruption
post-publication crash/lost ACK recovers actual current authority
partial multi-domain publication remains real and is never checkpoint-rolled back
accepted gameplay/RNG/choices are not replayed to rediscover persistence outcome
valid_through_event_id is retired as generic checkpoint frontier
expected_commit_sha is retired as self-referential checkpoint field
checkpoint-local world_time is not chronology authority
last_checkpoint_id is only an optional campaign-domain descriptor pointer
checkpoint creation requires independent recovery/maintenance value, never freshness/age alone
checkpoint + pointer publish in one campaign transaction; checkpoint is immutable
historical rewind is not a default checkpoint guarantee and never uses force-ref rewind
current recovery correctness does not depend on retaining old optional checkpoints
```

Machine-realization debt includes typed partitioned recovery routing, Procedure
lifecycle/root-enrollment evidence, checkpoint-schema reduction, current-authority-
first bootstrap, deterministic Python recovery executor, bounded retry/currentness
tests and removal of old checkpoint-first/mandatory-checkpoint assumptions.

### Step 5.8 — NEXT, NOT STARTED

Step 5.8 owns **Multiplayer / Live-Epoch Ownership**.

It must now define the exact temporary shared-scene authority protocol that makes
Step-5.7 current native source selection and recovery decidable under concurrent
writers.

Required questions include at minimum:

- opening/adopting one live epoch and binding its owning scope;
- one-writer/entity ownership and authorization/lease/fencing semantics;
- exact active CAS mutation contract;
- stale writer detection and rejection;
- cold-host recovery/adoption while another live writer may still exist;
- freeze/close semantics;
- compaction/absorption into campaign authority;
- authority-transfer ordering that never leaves two writable owners or no valid
  current owner;
- crash windows during campaign/live partial publication/compaction;
- closed-but-unabsorbed, abandoned, stuck and orphan live branches;
- rollover/new epoch creation;
- membership changes during an epoch;
- entity transfer between live scopes;
- rare multi-scene/global-event slow path;
- compatibility with Step-4 knowledge/disclosure and Step-5.7 recovery routing.

Exit target:

> Every live-owned mutable entity/scope has exactly one decidable current writable
> authority, stale writers cannot publish, and cold recovery can adopt/reject a
> live source without guessing from branch age, checkpoint age or Git timestamps.

**Do not begin Step 5.9 while Step 5.8 is in progress.**

## Step 6 carry-forward

Step 6 owns:

- LLM role-isolation feasibility spike before physical orchestration design;
- physical model-call topology for the six logical LLM roles;
- model selection, context reset/isolation and role-call compatibility matrix;
- minimum physical invocation count preserving Step-4 eligibility boundaries;
- token/latency/cost budgets;
- host/deployment capability profiles;
- Step-5.6 Python `RepositoryPort` bridge feasibility for supported ChatGPT/API/app
  deployment profiles;
- authenticated acting-principal transport feasibility;
- Commentator serving/spoiler/perspective policy;
- preparation caching/retention if justified;
- migration/catalog-gap/full-seed closure;
- final holistic architecture/catalog/seed audit;
- consolidation of implementation obligations before implementation planning.

Step 6 may optimize physical role placement/deployment but cannot weaken Step-4
context/authority boundaries or Step-5 durability/recovery invariants.

## Documentation / implementation debt

- `DEV/ARCHITECTURE/CATALOG_MODEL.md` and
  `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` remain historical derivation
  material where later canonical specs supersede them.
- The Step-5 expanded agenda contains old `one-hour` wording superseded by
  canonical Step 5.5.
- Current runtime persistence/recovery prose and schemas are partially stale
  relative to Steps 5.2/5.5/5.6/5.7. In particular, old checkpoint-first wording,
  `valid_through_event_id`, `expected_commit_sha`, mandatory PLAY_READY checkpoint
  assumptions and missing typed recovery-routing/Procedure lifecycle realization
  are implementation debt, not current architecture authority.
- Broad GAME/schema/test realization remains deferred until the architecture
  sequence closes and implementation planning begins.

## Exact continuation point

**Step 5.7 / Checkpoint / Recovery Protocol — CLOSED.**

Next architecture slice:

**Step 5.8 / Multiplayer / Live-Epoch Ownership — NOT STARTED.**

Do not begin Step 5.9 until Step 5.8 architecture closes.