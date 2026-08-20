# HDM Mechanical Architecture — Six-Step Roadmap

Status: **ACTIVE WORKING PLAN**

Target branch: `feature/mechanical-runtime-hot-state`

This roadmap is the sequencing/status gate for the current architecture program. It is intentionally compact; closed-step semantic detail belongs to linked canonical specifications rather than being duplicated here.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

## Operating rule

- Exactly one numbered architecture slice may be `IN PROGRESS`.
- Later slices may be inspected only to expose dependencies or contradictions.
- A slice closes when its architecture/review/verification pass and unresolved implementation work has an explicit later owner/debt entry.
- Architecture closure does **not** imply GAME/runtime/schema implementation is complete.
- Steps 4–6 complete the architecture sequence before broad implementation planning.
- After all major modules have designs, run one holistic architecture review over the full ownership graph, schemas, logic and cross-module relationships.

## Program roadmap

| # | Status | Scope | Exit result |
|---:|---|---|---|
| 1 | **COMPLETE / ASSURED** | Critical audit of catalog/class architecture and accepted baseline | Findings fixed, owned or consciously deferred |
| 2 | **COMPLETE / ASSURED** | Resources, HP/LifeState, Effects, Conditions, Duration, Recovery, selectors/query boundaries | Accepted mechanics/ownership contracts and assurance |
| 3 | **COMPLETE / ASSURED** | `IntentPlan -> Resolution -> Signal/Event`, deterministic execution, Procedure/Continuation | Canonical Alternative-C execution contract |
| 4 | **COMPLETE / ARCHITECTURE CLOSED** | Truth/lore, knowledge, disclosure, six logical LLM roles, Context Assembler, Story, promotion | Canonical information/role/Story architecture |
| 5 | **IN PROGRESS** | Durability, recovery, multiplayer/live authority, chronology, Story/transcript publication/retention | Coherent recoverable Step-5 architecture through 5.14 |
| 6 | `BLOCKED BY 5` | Modes, physical LLM orchestration/budget, deployment feasibility, migration/catalog/seed closure, holistic review | Enforceable deployment/context topology and final architecture closure |

## Steps 1–2 — CLOSED / ASSURED

Final retrospective assurance:

- `DEV/docs/superpowers/specs/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`

## Step 3 — CLOSED / ASSURED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`

Final critical review:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-final-critical-review.md`

Owner-approved architecture: **Alternative C**.

Core ownership remains:

```text
Interaction -> IntentPlan -> RuntimeCommand
RuntimeCommand -> Resolution(Activity) OR direct deterministic transition
runtime.procedure -> sole Procedure ResourceState owner
ExecutionSegment -> committed MechanicalEvents + receipts + mandatory children
Continuation -> one portable suspended Resolution generation
```

## Step 4 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`

Step 4 fixed objective truth, fictional knowledge, human disclosure, six logical LLM roles, deterministic Context Assembler, noncanonical four-layer Story model and promotion boundary. Physical role-call topology remains Step 6.

Deferred Step-6 feasibility input:

- `DEV/docs/superpowers/specs/2026-08-20-step-6-llm-role-isolation-feasibility-spike-notes.md`

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

Obsolete/ownerless persistence abstractions were removed or assigned to later owners before later Step-5 work depended on them.

### Step 5.1 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md`

Owner-approved decision: **B-NARROW**.

```text
DOMAIN TYPING
NO IMPLICIT CROSS-DOMAIN ORDER
```

No generic Frontier record/API, universal sequence or RecoveryCut authority.

### Step 5.2 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`

**Resumable Runtime Closure** is a property over compatible domain-native durable sources plus bounded typed recovery routing. Native owners remain authority; mutable sources are exact-revision pinned; Temporal Agenda/caches rebuild; lost unpublished HOT/SOFT is never invented.

### Step 5.3 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md`

Owner-approved decision: **A-NARROW / OWNER-CLAIM MATERIALIZATION**. Temporal authority remains owner-local; due evaluation is derived; accepted occurrence/execution identities, fixed RNG and no-lost/no-double continuity are preserved without a global scheduler or total order.

### Step 5.4 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-canonical-spec.md`

Owner-approved decision: **BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF**. Controlled handoff requires actual durable RRC; unexpected loss recovers actual durable native sources; host/chat lifecycle is not gameplay authority; clean handoff creates no heartbeat.

### Step 5.5 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md`

Owner-approved decision: **EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY**.

Key consequences:

```text
SOFT = ESTABLISHED + VOLATILE_DIRTY + MAY_DEFER
HARD = MUST_BE_DURABLE_BEFORE(named edge)
required durable closure != physical pending write set
SAVE protects selected established dirty roots + required recovery closure
failed ordinary save does not hard-lock coherent local/private play
no universal dirty timeout
clean state never creates heartbeat/no-op publication
```

The old runtime `one hour / durable_frontier_time` contract is noncanonical implementation debt.

### Step 5.6 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md`

Architecture direction: **PYTHON-OWNED SINGLE-REF CAS PUBLICATION**.

Owner-fixed boundary: runtime Git/repository publication belongs to deterministic Python core; LLM roles do not own repository transport.

```text
complete campaign write-set
-> one base-derived tree
-> one single-parent commit from pinned H
-> one non-force authoritative ref transition
```

Prepared objects are nonauthority; ambiguous ACK requires bounded lineage/current-closure verification; conflicts are dependency-aware; accepted gameplay/RNG is not replayed merely because transport retries. No force push, generic merge or distributed transaction.

Step-6 transport feasibility input:

- `DEV/docs/superpowers/specs/2026-08-20-step-6-repository-port-transport-feasibility-spike.md`

### Step 5.7 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`

Architecture direction: **CURRENT-AUTHORITY-FIRST / CHECKPOINT-OPTIONAL NATIVE-ROUTED BOUNDED RECOVERY**.

Cold recovery starts from current campaign authority, resolves current native owning routes, exact-pins participating sources, discovers Step-5.2 roots, hydrates required closure, rebuilds derived state and returns `READY | RETRY | BLOCKED`. Checkpoint is optional immutable evidence/maintenance metadata, never current-state authority or mandatory startup anchor.

### Step 5.8 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md`

Architecture direction: **ROUTED FIXED-CLAIM LIVE EPOCH / EXACT-SOURCE CAS / TERMINAL SOURCE FREEZE / FORWARD CAMPAIGN ABSORPTION**.

Derivation/review artifacts:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-research-draft.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-analytical-challenge.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-resolution-gate.md`

Canonical consequences include:

```text
current campaign routing selects one live epoch + immutable typed claims
exact live source revision/HEAD is the CAS fence
no leader/TTL lease/heartbeat correctness dependency
exactly one current truth authority; at most one ordinary writable authority
CLOSED_UNABSORBED = current truth with zero ordinary gameplay writers
route-away requires confirmed source-local ACTIVE -> CLOSED fence
claims may identify exact owners or owner-defined typed writable partitions
write-authority lookup is bounded/machine-decidable; no all-live scan
live claim requires native writable-scope containment
live-born accepted IDs use collision-free epoch-qualified stable namespace
live atomicity is per native Step-3 durability edge, not per user message
accepted execution/RNG/Procedure/Continuation/temporal state survives close
absorption is forward campaign publication; no distributed transaction/force rollback
SAVE does not close healthy live epochs merely to obtain durability
revocation/controller removal closes affected live source before one combined campaign absorption+authorization transaction
multi-live owner transfer freezes every affected source before one campaign transfer transaction
partial multi-scope freeze is a valid recoverable mixed state
cold host adopts ACTIVE or resumes CLOSED/absorption without leader takeover
Step-4 truth/knowledge/disclosure remain separate semantic owners
Python RepositoryPort owns live CAS; connector-specific CAS is feasibility evidence only
```

Machine-realization debt includes typed claim routing/lookup, containment rules per supported owner class, live ID namespace, Step-3-edge-aligned physical persistence, Procedure/Continuation/temporal routing through close/absorption, Step-4 knowledge/disclosure cleanup, Python `LiveSourceCAS`, concurrency/crash/save/handoff/transfer tests and fixed-claim rollover performance measurement.

### Step 5.9 — NEXT, NOT STARTED

Step 5.9 owns **Chronology Persistence & Reconciliation**.

Purpose: persist only temporal/causal evidence required for later correct rulings and recovery while preserving domain typing and partial ordering.

Required investigation from the approved expanded agenda:

- event-local partial ordering;
- local scene frontiers;
- globally reconciled sparse frontier;
- retained quantitative elapsed evidence;
- exact/approximate time;
- cross-scene dependencies;
- simultaneous/contested actions;
- chronology interaction with Step-5.8 live compaction/recovery;
- compaction of old chronology evidence without breaking still-live temporal predicates.

Exit target:

> Fictional chronology cannot be accidentally inferred from Git commit order, and retained evidence is sufficient for every still-live temporal obligation and causal dependency.

**Do not begin Step 5.10 while Step 5.9 is in progress.**

## Step 6 carry-forward

Step 6 owns at least:

- LLM role-isolation feasibility before physical orchestration design;
- physical model-call topology for six logical roles;
- model selection and real context reset/isolation compatibility;
- minimum physical invocation count preserving Step-4 eligibility;
- token/latency/cost budgets;
- host/deployment capability profiles;
- deterministic Python `RepositoryPort` bridge feasibility for campaign and live CAS;
- authenticated acting-principal transport feasibility;
- Commentator serving/spoiler/perspective policy;
- preparation caching/retention if justified;
- migration/catalog-gap/full-seed closure;
- final holistic architecture/catalog/seed audit;
- consolidation of implementation obligations before implementation planning.

Step 6 may optimize physical placement/deployment but cannot weaken Step-4 information boundaries or Step-5 durability/recovery/authority laws.

## Documentation / implementation debt

- `DEV/ARCHITECTURE/CATALOG_MODEL.md` and `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` remain historical derivation where later canonical specs supersede them.
- The expanded Step-5 agenda contains older wording superseded by canonical slices; use the slice specs for semantics.
- Runtime persistence/recovery/live prose and schemas are materially stale relative to Steps 5.2–5.8. Known debt includes checkpoint-first fields/assumptions, missing typed recovery routing and Procedure lifecycle, missing immutable live claims/bounded claim lookup, missing live-containment representation, campaign-only ID-allocation assumptions, one-high-level-action/one-live-write assumptions, legacy live knowledge representation and missing Python live `RepositoryPort` realization.
- Broad GAME/schema/test realization remains deferred until the architecture sequence closes and implementation planning begins.

## Exact continuation point

**Step 5.8 / Multiplayer / Live-Epoch Ownership — CLOSED.**

Next architecture slice:

**Step 5.9 / Chronology Persistence & Reconciliation — NOT STARTED.**

Do not begin Step 5.10 until Step 5.9 architecture closes.
