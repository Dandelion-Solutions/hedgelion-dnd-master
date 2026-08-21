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
| 5 | **COMPLETE / ARCHITECTURE CLOSED** | Durability, recovery, multiplayer/live authority, chronology, Story/transcript publication/retention/cleanup | Integrated Step-5 architecture survived full recovery/concurrency adversarial review |
| 6 | **NEXT / NOT STARTED** | Modes, physical LLM orchestration/budget, deployment feasibility, migration/catalog/seed closure, holistic review | Enforceable deployment/context topology and final architecture closure |

## Steps 1–2 — CLOSED / ASSURED

Final retrospective assurance:

- `DEV/docs/superpowers/specs/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`

## Step 3 — CLOSED / ASSURED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`

Final critical review:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-final-critical-review.md`

Owner-approved architecture: **Alternative C**.

## Step 4 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`

Step 4 fixed objective truth, fictional knowledge, human disclosure, six logical LLM roles, deterministic Context Assembler, noncanonical four-layer Story model and promotion boundary. Physical role-call topology remains Step 6.

Deferred Step-6 feasibility input:

- `DEV/docs/superpowers/specs/2026-08-20-step-6-llm-role-isolation-feasibility-spike-notes.md`

## Step 5 — CLOSED / ARCHITECTURE CLOSED

Expanded historical/working agenda:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-expanded-architecture-agenda.md`

Canonical integrated final review:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md`

Completed slice order:

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

### Step 5.1 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md`

Decision: **B-NARROW / DOMAIN TYPING / NO IMPLICIT CROSS-DOMAIN ORDER**. No generic Frontier record/API, universal sequence or RecoveryCut authority.

### Step 5.2 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`

Resumable Runtime Closure is a property over compatible domain-native durable sources plus bounded typed recovery routing. Native owners remain authority; mutable sources are exact-revision pinned; derived indexes/caches rebuild; lost unpublished HOT/SOFT is never invented.

### Step 5.3 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md`

Integration amendment:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-3-5-9-temporal-agenda-chronology-integration-canonical-amendment.md`

Decision: **A-NARROW / OWNER-CLAIM MATERIALIZATION**. Temporal authority remains owner-local; due evaluation is derived; accepted occurrence/execution identities, fixed RNG and no-lost/no-double continuity survive restart without a global scheduler.

### Step 5.4 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-canonical-spec.md`

Decision: **BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF**.

### Step 5.5 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md`

Decision: **EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY**. SOFT/HARD are durability obligations at named semantic edges; explicit SAVE protects selected established dirty roots plus required recovery closure; no universal dirty timeout/heartbeat.

### Step 5.6 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md`

Direction: **PYTHON-OWNED SINGLE-REF CAS PUBLICATION**. Complete base-derived tree -> single-parent commit -> non-force authoritative ref transition; ambiguous ACK is resolved by bounded currentness/lineage proof; accepted gameplay/RNG is not replayed because transport retries.

Step-6 transport feasibility input:

- `DEV/docs/superpowers/specs/2026-08-20-step-6-repository-port-transport-feasibility-spike.md`

### Step 5.7 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`

Direction: **CURRENT-AUTHORITY-FIRST / CHECKPOINT-OPTIONAL NATIVE-ROUTED BOUNDED RECOVERY**. Cold recovery resolves current native authority/routes first; checkpoint is optional evidence/metadata, never current-state authority.

### Step 5.8 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md`

Direction: **ROUTED FIXED-CLAIM LIVE EPOCH / EXACT-SOURCE CAS / TERMINAL SOURCE FREEZE / FORWARD CAMPAIGN ABSORPTION**. At most one ordinary writable authority exists for a claimed scope; CLOSED_UNABSORBED remains recoverable current truth with no ordinary writer; accepted identities/lifecycles survive absorption.

### Step 5.9 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md`

Owner-approved temporal capability boundary:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-9-forward-extensible-time-boundary-owner-decision.md`

Direction: **OWNER-ANCHORED SPARSE CHRONOLOGY / DOMAIN-TYPED ORDER / TYPED METRIC COORDINATES / MATERIAL BRIDGE RECONCILIATION / FORWARD-EXTENSIBLE HISTORY**. Git/ref/ID order never becomes fictional chronology; protected consumers retain bounded temporal/causal evidence; mutable-past/branching/causal-loop baseline mechanics require a future explicit extension.

### Step 5.10 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-10-story-projection-durability-canonical-spec.md`

Direction: **LAYER-LOCAL COVERAGE / QUEUE-FREE PULL CATCH-UP / DETERMINISTIC STORY PUBLICATION / OPTIONAL GENERATIVE CHRONICLER / GAMEPLAY-PRIORITY SAME-REF CAS**. Story remains noncanonical, may lag independently, requires no background worker and never blocks gameplay/SAVE/recovery.

### Step 5.11 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md`

Owner-approved product decision:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-11-selective-exact-semantic-continuity-owner-decision.md`

Direction: **STABLE MESSAGE EVIDENCE / SELECTIVE EXACT PROTECTION / SEMANTIC-DISCHARGE COMPACTION / OPTIONAL VERIFIED TRANSCRIPT ARCHIVE**. HDM guarantees semantic continuity, not universal verbatim recall; exact wording survives only when protected or deliberately archived; compaction cannot destroy meaning still promised by a surviving consumer.

### Step 5.12 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md`

Owner-approved scope/product decision:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-12-minimal-host-delivery-owner-scope-decision.md`

Direction: **VALIDATED EMISSION-COMMIT / SOFT OUTBOUND DISCLOSURE CLOSURE / NO BASELINE DELIVERY-ACK SUBSYSTEM / DOCUMENTED INTERRUPTION RISK / RECIPIENT-SCOPED DISCLOSURE**. Normal uninterrupted Master output is the supported baseline; interruption/Retry/edit do not justify outbox/worker/chunk-ledger machinery.

### Step 5.13 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`

Direction: **OWNER-GATED RETIREMENT / CLOSED BLOCKER CONTRACTS / COMPLETENESS-TYPED PROTECTION ROUTING / PINNED CURRENT-BASIS SAFE-RETIREMENT PROOF / SURVIVOR-BEFORE-REMOVAL / OPTIONAL POST-AUTHORITY REF CLEANUP / SEMANTIC RETENTION SEPARATE FROM GIT-HISTORY REACHABILITY / HOST-MANAGED GIT OBJECT RECLAMATION**.

Canonical consequences include:

```text
native owners define liveness/terminality; cleanup is not a new authority
no universal GC frontier, global mark-and-sweep semantic graph or generic durable refcount
cleanup is admitted only under a compatible closed CleanupContract for the target representation
negative blocker proof is valid only from complete typed protection routing under one coherent current native basis
unknown/incompatible cleanup contract or stale/incomplete protection evidence => retain/retry/repair
required survivor/replacement evidence exists before source representation disappears
surviving refs distinguish current-dereference, opaque provenance and survivor-backed semantics
current-tree retirement does not erase ancestor Git history
Git-history bytes are transport/audit provenance and do not restore semantic/exact capabilities already lawfully compacted away
ACTIVE and CLOSED_UNABSORBED live sources cannot be cleaned; absorbed/non-authoritative refs are post-authority cleanup only
prepared/unselected Git objects are nonauthority; server object reclamation remains host-managed
candidate discovery may be stale/incomplete because every actual retirement revalidates the full safe-retirement proof
ordinary gameplay performs no garbage scan; cleanup is bounded maintenance work
cleanup contract/protection semantics participate in runtime/catalog compatibility and migration
failure/ambiguity biases toward extra retention rather than premature irreversible loss
```

Machine-realization debt includes target-kind cleanup contracts/generations, typed blocker classes, completeness-typed protection routing, cleanup-compatibility migration, bounded candidate selection, SafeRetirementAssessment validation, survivor/reference migration, runtime execution-detail/idempotency compaction, checkpoint retirement/pointer coherence, compact-message-envelope retirement, Story/chronology derivative-generation cleanup, live absorbed/orphan ref cleanup when RepositoryPort supports it, Git-history semantic exclusion from ordinary recovery/exact recall, maintenance diagnostics and crash/concurrency/integrity tests.

### Step 5.14 — CLOSED

Canonical final review:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md`

Supporting review chain:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-14-integrated-adversarial-review-draft.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-14-analytical-challenge.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-14-resolution-gate.md`

Step 5.14 attacked all 30 integrated scenario routes plus seven stronger composite crash/concurrency cases and performed the final authority/contamination sweep. No unresolved Step-5 architecture blocker or new owner-level product decision remained.

Canonical Step-5.14 integration clarifications include:

```text
role-context current source basis is domain-composed, not campaign-HEAD-only
cross-source cleanup protection precedes consumer dependency acceptance
runtime.disclosure monotonic merge is owner-specific and never generic last-writer-wins
partial multi-live prerequisite freeze is technical currentness, not partial fictional establishment
Step-6 physical feasibility failure rejects/refines a deployment profile before weakening Step-4/5 semantics
```

Step 5 is therefore **COMPLETE / ARCHITECTURE CLOSED**.

## Step 6 — NEXT / NOT STARTED

Step 6 owns at least:

- LLM role-isolation feasibility before physical orchestration design;
- physical model-call topology for six logical roles;
- model selection and real context reset/isolation compatibility;
- minimum physical invocation count preserving Step-4 eligibility;
- token/latency/cost budgets;
- host/deployment capability profiles;
- deterministic Python `RepositoryPort` bridge feasibility for campaign/live publication and optional post-authority ref cleanup;
- authenticated acting-principal transport feasibility;
- Commentator serving/spoiler/perspective policy;
- Story/Chronicler activation policy and optional future async execution using Step-5.10 coverage/CAS;
- stable host invocation/message/revision identity feasibility for Step-3/5.11/5.12 edit-retry-branch semantics;
- physical pre-player-visible staging/validation feasibility for Step-4/5.12 material Narrator output before secret-bearing content is rendered;
- inventory/fencing of actual player-visible host surfaces;
- authenticated recipient/audience mapping for supported host profiles;
- whether cheap trustworthy completed-message acknowledgement is available and worth optional strengthening;
- migration/catalog-gap/full-seed closure, including cleanup-contract/protection-routing compatibility realization;
- final holistic architecture/catalog/seed audit;
- consolidation of implementation obligations before implementation planning.

Step-5.14 identifies the following as material Step-6 feasibility gates:

```text
SD-1 deterministic authenticated RepositoryPort               blocking for persistence-capable profile
SD-2 pre-player-visible Narrator staging/validation            blocking for secret-bearing profile
SD-3 stable invocation/message/retry identity                  significant / potentially blocking
SD-4 authenticated acting-principal + recipient/audience       blocking for secure multiplayer profile
SD-5 genuine role-context isolation/reset                      blocking for mixed-privilege role topology
SD-6 live-ref deletion                                         optional / nonblocking
```

Step 6 may optimize physical placement/deployment but cannot weaken Step-4 information boundaries or Step-5 durability/recovery/authority laws.

## Documentation / implementation debt

- `DEV/ARCHITECTURE/CATALOG_MODEL.md` and `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` remain historical derivation where later canonical specs supersede them.
- The expanded Step-5 agenda contains older wording superseded by canonical slices; use the slice specs and Step-5.14 integration clarifications for semantics.
- Runtime persistence/recovery/live/chronology/Story/transcript/disclosure/cleanup prose and schemas are materially stale relative to canonical Steps 5.2–5.14; broad realization remains deferred until Step-6 architecture closes and the normal implementation-planning gate is reached.
- Player-facing help/manual must eventually document the Step-5.12 interruption/Retry/edit limitation.
- The Step-5.9 forward-extensible temporal capability boundary must be reflected in eventual Dramaturg/runtime role policy.
- Git current-tree cleanup is not secure historical erasure; no product/API promise to the contrary exists in Step 5.13.
- Step-5.14 integrated implementation tests must cover its 30 required scenarios and stronger composite cases; local per-slice tests are not sufficient for final realization assurance.

## Exact continuation point

**Step 5.14 / Full Recovery & Concurrency Adversarial Review — CLOSED.**

**Step 5 / Persistence, Recovery & Concurrency — COMPLETE / ARCHITECTURE CLOSED.**

Next architecture stage:

**Step 6 / Physical LLM Orchestration, Deployment Feasibility & Final Architecture Closure — NEXT / NOT STARTED.**

Do not begin broad implementation until Step-6 architecture closes and the normal planning gate is reached.