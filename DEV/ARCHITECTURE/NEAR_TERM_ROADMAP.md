# HDM Mechanical Architecture — Six-Step Roadmap

Status: **ACTIVE WORKING PLAN**

Target branch: `feature/mechanical-runtime-hot-state`

This roadmap is the sequencing gate for the current architecture program. It is
a status/order document, not a duplicate normative specification.

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

## Roadmap

| # | Status | Scope | Required architecture result | Exit gate |
|---:|---|---|---|---|
| 1 | **COMPLETE / ASSURED** | Critical audit of catalog/class architecture and accepted baseline | Owned audit ledger + retrospective assurance | Every finding fixed, assigned, or consciously deferred; no unowned blocker |
| 2 | **COMPLETE / ASSURED** | Resources, HP/LifeState, Effects, Conditions, Duration, Recovery, selector/query boundaries | Normative ownership models + aligned schemas/catalogs + focused cases + retrospective assurance | No unresolved Step-2 blocker; validation passed |
| 3 | **COMPLETE / ASSURED** | `IntentPlan -> Resolution -> Signal/Event`, including LLM/core execution boundary, Procedure ownership and checkpointable continuation | Canonical Alternative-C execution contract + machine schemas/catalogs + A–N cases + adversarial/final critical review | Final same-head validation succeeded; no unresolved Step-3 blocker |
| 4 | **COMPLETE / ARCHITECTURE CLOSED** | Truth/lore, fictional knowledge, human disclosure, six-role LLM context boundaries, Story projections, promotion | Canonical truth/knowledge/disclosure owners + deterministic Context Assembler + role handoffs + four-layer Story contract + promotion/migration contract | Full-cycle rerun + adversarial resolution complete; obsolete Chapter world authority removed; no unresolved Step-4 architecture blocker; remaining machine realization explicitly deferred |
| 5 | **IN PROGRESS** | Durability, multiplayer, event-local time, Story/transcript publication/retention | Compatible SOFT/HARD publication, shared visibility/conflict/recovery model, Story persistence/compaction | Publication/live-scene ownership, cross-scene recovery, chronology, Story/index publication, transcript retention and shared revision semantics are coherent |
| 6 | `BLOCKED BY 5` | Modes, physical LLM orchestration/budget, migration, catalog gaps, full seed, final closure | Mode profiles + role-call compatibility/isolation + final cross-cutting consistency pass | Mode/context isolation enforceable; migration/gap/seed ownership complete; holistic architecture audit passes |

## Steps 1–2 retrospective assurance

The non-numbered retrospective assurance overlay is complete:

- `DEV/docs/superpowers/specs/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`

Steps 1–2 remain closed and assured.

## Step 3 closure

Owner-approved architecture: **Alternative C**.

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`

Final critical review:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-final-critical-review.md`

Core Step-3 ownership remains:

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
        -> receipts / idempotency
        -> mandatory child descriptors

Continuation
    portable suspended Resolution generation
```

## Step 4 — closed architecture stage

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`

Step 4 fixed the objective-truth / fictional-knowledge / human-disclosure
ownership split, the six logical LLM roles and deterministic Context Assembler,
noncanonical four-layer Story model, promotion closure, and removal of separate
Secret and literary Chapter authority.

The obsolete literary world vocabulary remains retired:

```text
world.chapter
transition.chapter_append
event.chapter.appended
```

Most Step-4 machine realization remains explicitly deferred until the integrated
implementation program after Steps 5–6 architecture.

## Step 5 — active architecture stage

Expanded Step-5 architecture agenda:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-expanded-architecture-agenda.md`

The current slice order is:

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

5.0 removed obsolete/ownerless machine-visible abstractions before they could
leak into later persistence design, including independent Secret/tactical
placeholders, generic pending consequences, old global timeline record IDs,
premature dirty/publication record classes, duplicate checkpoint/frontier
pointers and obsolete campaign-path wrapper spelling.

Catalog `1.6.0` is the current machine baseline after those retirements.

### Step 5.1 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md`

Owner-approved decision: **B-NARROW**.

Canonical shared laws:

```text
LAW 1 — DOMAIN TYPING
Every correctness-relevant progress/coverage/revision/cursor/frontier claim
identifies the semantic domain/scope in which it is meaningful.

LAW 2 — NO IMPLICIT CROSS-DOMAIN ORDER
No ordering/comparison is valid across different semantic domains unless a
specific owning contract explicitly defines that relation.
```

Step 5.1 deliberately introduces no generic Frontier record/schema/API,
universal comparison operation, global monotonic sequence or RecoveryCut record.
Concrete representations remain domain-native.

Important consequences:

- frontier/progress metadata never becomes semantic authority merely by existing;
- HOT current truth and campaign durability are distinct axes;
- a composed coherent read view does not merge writable authority;
- campaign publication, live operational revision, fictional chronology,
  runtime continuation/RNG state and Story projection coverage remain distinct
  domains;
- `coherent source cut` is a conceptual one-operation selection/compatibility
  relation, not an owner or required record;
- `runtime.id_allocator` / `campaign-allocator` remains the distinct owner of
  campaign-scoped allocation counters; centralized counter ownership is not a
  frontier and does not imply a synchronous global gameplay lock;
- `CURRENT.last_event_id` is retired from the active schema/template as a global
  reconnect/recovery/log cursor;
- SemanticEvent identities and explicit per-record provenance remain valid;
- `checkpoint.valid_through_event_id` remains a narrower 5.7 question and is not
  treated as the universal recovery frontier;
- numeric/sparse ordering remains allowed inside an explicit chronology domain;
  5.9 owns final chronology representation.

Adversarial review found no owner blocker and resolved all significant findings
without reopening B-NARROW.

### Step 5.2 — CLOSED

Current canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`

The earlier `...canonical-spec.md` remains historical derivation and is superseded
for current Step-5.2 authority by v2.

Step 5.2 defines **Resumable Runtime Closure** as a correctness property over
compatible domain-native durable sources and bounded typed recovery routing. It
does not introduce a new state authority, universal snapshot, RecoveryCut record,
serialized Temporal Agenda or mandatory closure record.

Canonical consequences include:

```text
native owners remain authority
bounded typed operational-root discovery is required
routing membership is recovery evidence, not owner state
routing must be partitionable by native writable scope
Procedure remains independently recoverable across gaps between Commands
Temporal Agenda is rebuilt from native temporal owners
all armed independently-due temporal source owners stay enrolled while armed
fixed accepted execution inputs survive in Step-3 owners
hydration pins each mutable native source to an exact revision
recovery resolves through current owning scope; stale cross-domain fallback is forbidden
root enrollment changes are correctness-critical derivatives of native lifecycle
open execution requires resolvable compatible runtime/catalog interpretation context
lost unpublished HOT/SOFT state is never invented after total context loss
```

The unconditional armed-temporal enrollment rule deliberately avoids a dynamic
reachability optimization: a due-capable armed owner remains in typed temporal
routing even if another active root also reaches it. Only owner identity/routing
is duplicated; deadlines, due state, ordering, firing state and lifecycle remain
native owner/chronology/execution semantics.

Checkpoint remains sparse recovery evidence and cannot be the sole current active
root source. Exact routing/checkpoint/live placement is intentionally deferred to
5.7/5.8 after due-work, durability and publication constraints are known.

Adversarial review plus addendum found no blocking owner decision. Significant
findings were resolved through pinned native hydration, owning-scope resolution,
root-membership completeness, Procedure lifecycle validation, temporal routing
field exclusions, interpretation-context closure and simplified armed-temporal
enrollment.

### Step 5.3 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md`

Owner-approved decision: **A-NARROW / OWNER-CLAIM MATERIALIZATION**.

Canonical consequences include:

```text
Temporal due evaluation is derived: NOT_DUE | DUE | INDETERMINATE
occurrence identity is distinct from timing value
accepted occurrence G must stop being freshly materializable
materialization uses one of:
    DIRECT FINALIZATION
    SAFE IMMEDIATE REARM
    CONTINGENT CLAIMED(G,F)
Step-3 remains accepted execution authority
CLAIMED exists only while source-owner settlement depends on F
source/execution closure is an integrity invariant
bounded recovery reachability remains continuous across root handoff
multiple due obligations do not gain implicit storage/ID order
cold hydration/host elapsed time do not invent fictional advancement
accepted RNG continuity is experiment-scoped, not a universal future stream
accepted firing resumes under pinned compatible interpretation context
```

Step 5.3 introduces no generic scheduler, generic pending-obligation/job record,
standalone firing authority, durable due marker, authoritative Temporal Agenda,
synthetic background RuntimeCommand or universal future RNG frontier.

The current machine schemas intentionally remain behind the canonical semantic
contract in places such as temporal occurrence generation/claim representation
and `Continuation.future_rng_frontier`; those are recorded implementation
obligations for the integrated machine-realization program after architecture.

Adversarial review resolved significant refinements around conditional claim
scope, continuous bounded-recovery handoff, immediate-rearm overlap safety and
stable experiment association for fixed RNG. No Step-5.3 architecture blocker
remains.

### Step 5.4 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-canonical-spec.md`

Owner-approved decision: **BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF**.

Derivation/review artifacts include:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-research-draft.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-analytical-challenge.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-decision-brief.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-resolution-gate.md`

Canonical consequences include:

```text
host/chat/process lifecycle is not gameplay authority
controlled handoff and unexpected loss have different guarantees
successful handoff requires actual durable Resumable Runtime Closure
handoff uses scoped mutation/semantic-acceptance quiescence, not a global lock
external native-source movement revalidates/invalidate selected closure
existing Step-3/5.2/5.3 native owners carry resume semantics
clean handoff does not require a heartbeat write
session metadata remains non-authoritative
relinquished hosts must rehydrate/revalidate before later mutation
hydration does not prove absence of unpublished volatile state in another host
destructive maintenance uses the same handoff guarantee
partial model reasoning/raw context is never recovery authority
accepted-but-not-typed input requires resolvable evidence or materialization
open execution preserves compatible accepted interpretation context
```

Host conversation/message/context capacity exhaustion is explicitly covered:

```text
RELIABLE_DESTRUCTIVE
    -> controlled handoff opportunity/attempt
    -> warning reliability does not guarantee enough execution budget

ADVISORY_CAPACITY
    -> OOC warning/recommend proactive transfer
    -> no durability/recovery authority

NO_USABLE_SIGNAL / HARD STOP
    -> unexpected-loss recovery to actual durable closure
```

No trustworthy remaining-message/token/capacity metric is assumed. Message count,
approximate token count, chat age or a future locally derived predictor may only
support an explicitly advisory heuristic unless a future host contract provides
stronger reliable semantics.

Step 5.4 introduces no mandatory handoff snapshot/ticket, generic resume-point
record, campaign-global host/session lease, durable RELINQUISHED marker,
authoritative capacity heuristic or raw model-context persistence.

The owner carry-forward about periodic durability remains owned by Step 5.5:

- maximum age/exposure of gameplay-significant unpublished SOFT must be designed
  independently of whether a lifecycle warning exists;
- no numerical threshold is currently approved;
- the current runtime hard-coded `one hour` value is provisional/stale policy,
  not an architectural constant;
- advisory host-capacity risk may be considered by 5.5 as a durability-policy
  input, but 5.4 does not decide whether it forces an opportunistic flush;
- clean state must not create heartbeat/no-op publication.

Adversarial review found no owner-level blocker. Significant findings around
late warnings, external source movement, post-freeze input, invisible volatile
state in another host, accepted-message evidence and advisory-capacity semantics
were resolved without reopening BARRIER-NATIVE.

### Step 5.5 — NEXT, NOT STARTED

Step 5.5 owns **SOFT / HARD / SAVE Durability Semantics**.

It must now define one architecture-level durability classifier and completeness
contract using the already-closed host/recovery semantics from 5.2–5.4.

Required questions include at minimum:

- exact SOFT / HARD / EPHEMERAL semantics;
- exact forced controlled-handoff durability closure;
- relation between accumulated SOFT and a forced boundary;
- explicit SAVE_ALL_DIRTY relation to ordinary durability;
- when HARD blocks further execution/narration;
- complete dependency closure required by publication;
- failure/acknowledgement semantics at the durability-class level, without
  stealing physical Git crash consistency from 5.6;
- independent maximum age/exposure policy for gameplay-significant unpublished
  SOFT when ordinary forced boundaries accumulate slowly;
- behavior when no background execution opportunity exists;
- whether advisory host-capacity risk changes durability policy;
- no-heartbeat behavior for clean state;
- final disposition of the current provisional hard-coded `one hour` runtime
  policy.

No numeric dirty-age/capacity threshold is pre-approved by 5.4.

**Do not begin Step 5.6 while Step 5.5 is in progress.**

## Step 6 carry-forward

Step 6 owns:

- physical model-call topology for the six logical LLM roles;
- model selection, context reset/isolation and role-call compatibility matrix;
- token/latency/cost budgets;
- Commentator serving/spoiler/perspective policy;
- preparation caching/retention if justified;
- migration/catalog-gap/full-seed closure;
- final holistic architecture/catalog/seed audit;
- consolidation of implementation obligations before implementation planning.

Step 6 may optimize role placement but cannot weaken Step-4 context/authority
boundaries or Step-5 durability/recovery invariants.

## Documentation debt

`DEV/ARCHITECTURE/CATALOG_MODEL.md` and
`DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` remain historical derivation
material predating current canonical Step-2/3/4/5 contracts. They are
non-authoritative relative to current inventory, machine schemas/catalogs and
canonical specs.

The Step-5 expanded working agenda contains older wording referring to a
`one-hour` dirty ceiling. Current owner direction and canonical Step 5.4 supersede
that numerical assumption for sequencing purposes: Step 5.5 must decide the
actual exposure policy/value rather than inheriting one hour as an approved
constant.

## Exact continuation point

**Step 5.4 / Host Lifecycle & Session Handoff — CLOSED.**

Next architecture slice:

**Step 5.5 / SOFT / HARD / SAVE Durability Semantics — NOT STARTED.**

Do not begin Step 5.6 until Step 5.5 architecture closes.