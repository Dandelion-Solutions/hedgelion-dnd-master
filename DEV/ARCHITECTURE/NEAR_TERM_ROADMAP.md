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

### Step 5.2 — NEXT, NOT STARTED

Step 5.2 owns **Resumable Runtime Closure**: determining which gameplay-significant
in-memory/operational state must survive process/chat loss, what is authoritative
versus recovery projection versus rebuildable cache versus truly ephemeral, and
what minimum durable closure permits a fresh runtime to resume from the real
recoverable point.

Step 5.2 must preserve the Step-5.1 domain-typing and no-implicit-cross-domain-
order laws. It must not serialize derived Temporal Agenda as a new temporal
authority; Temporal Agenda rebuild and pending-obligation lifecycle are primarily
5.3 concerns.

**Do not start 5.2 as part of 5.1 closure.**

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

## Exact continuation point

**Step 5.2 / Resumable Runtime Closure — NOT STARTED.**

Step 5.1 is closed. Do not begin Step 5.2 until the 5.1 closure/result has been
reported and the architecture sequence is explicitly continued.