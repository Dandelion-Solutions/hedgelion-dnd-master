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

Integration amendment:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-3-5-9-temporal-agenda-chronology-integration-canonical-amendment.md`

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

Prepared objects are nonauthority; ambiguous ACK requires bounded lineage/current-closure proof; conflicts are dependency-aware; accepted gameplay/RNG is not replayed merely because transport retries. No force push, generic merge or distributed transaction.

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
CLOSED_UNABSORBED = truth with zero ordinary writers
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
campaign absorption order does not become fictional chronology
```

Machine-realization debt includes typed claim routing/lookup, containment rules per supported owner class, live ID namespace, Step-3-edge-aligned physical persistence, Procedure/Continuation/temporal routing through close/absorption, Step-4 knowledge/disclosure cleanup, Python `LiveSourceCAS`, concurrency/crash/save/handoff/transfer tests and fixed-claim rollover performance measurement.

### Step 5.9 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md`

Architecture direction: **OWNER-ANCHORED SPARSE CHRONOLOGY / DOMAIN-TYPED ORDER / TYPED METRIC COORDINATES / MATERIAL BRIDGE RECONCILIATION / FORWARD-EXTENSIBLE HISTORY**.

Owner-approved temporal capability boundary:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-9-forward-extensible-time-boundary-owner-decision.md`

Canonical consequences include:

```text
Git/ref/ID/CAS/host order never becomes fictional chronology implicitly
causal ancestry, domain-typed precedence and metric coordinate order remain distinct
independent scenes/processes may remain incomparable indefinitely
no mandatory global current world clock or generic global chronology frontier
metric contexts are rulers; native temporal scopes/providers own exact/bounded position evidence
TemporalBinding metric due evaluation re-resolves deterministic owner-specific position provider
exact/bounded evidence preserves uncertainty and feeds NOT_DUE | DUE | INDETERMINATE
cross-scope chronology uses sparse material bridge relations only when concrete dependencies require them
late-established historical relations extend append-only history through immutable relation evidence rather than rewriting old events
protected temporal/causal consumers require bounded durable relation-evidence routing
scope-local frontier is bounded ActiveExtensionFrontier, not all historical maxima
live close/absorption/successor order is technical and does not create fictional order
compaction eligibility preserves protected-consumer decidability, feasible metric evidence and unique causal provenance
baseline causal history is forward-extensible; mutable-past/branching/causal-loop mechanics require a future explicit extension
```

Machine-realization debt includes typed relation domain/context representation, stable late-relation evidence IDs/refs, owner-specific temporal position-provider routing, exact/bounded metric position and elapsed evidence, ActiveExtensionFrontier representation, bounded relation dependency indexes where required, live chronology preservation, migration of legacy world-time/singleton frontier/ambiguous sequence fields, scoped integrity checks and Dramaturg temporal capability guard realization.

### Step 5.10 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-10-story-projection-durability-canonical-spec.md`

Architecture direction: **LAYER-LOCAL COVERAGE / QUEUE-FREE PULL CATCH-UP / DETERMINISTIC STORY PUBLICATION / OPTIONAL GENERATIVE CHRONICLER / GAMEPLAY-PRIORITY SAME-REF CAS**.

Canonical consequences include:

```text
Story remains durable non-canonical projection and never gameplay authority
no required Work/Pro/Enterprise/background-worker dependency
backlog = typed source-domain basis minus compatible layer coverage
campaign HEAD is transport pin, never Story source watermark
coverage is typed by layer + source domain + semantic projection-contract generation
cursor-capable source domains require append-monotonic projection enumeration
MUST_MATERIALIZE vs MAY_OMIT controls legal coverage advancement
no durable Story job queue/worker claim/lease is baseline authority
Chronicler proposes editorial/generative draft; deterministic core owns final IDs, validation, coverage and publication
Story IDs are layer-local, assigned at publication from Story-local non-reusing allocator state
ordinary catch-up publishes one layer closure; layers may lag independently
coverage/output/index/availability/allocator advance crash-coherently
Story-only campaign movement is semantically disjoint from ordinary gameplay and may cause transport-only rebuild, never mechanics/RNG replay
Story yields under repeated contention and has no freshness priority
SAVE/RRC/gameplay recovery never require Story catch-up
source retention may require typed projection closure only when Step-5.11 policy says so
source cursor interpretability/resume continuity must survive lawful 5.11/5.13 compaction
```

Machine-realization debt includes Story root/scaffold/migration, four layer schemas/indexes, StoryLayerProjectionState, layer-local allocator, typed projection-source contracts/generations, bounded candidate enumeration/coverage, StorySourceBundle/StoryProjectionDraft protocols, availability/ref closure, Python Story publication/conflict handling, Commentator lag status, structural correction tooling and 5.11/5.12/5.13 integration.

### Step 5.11 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md`

Owner-approved product decision:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-11-selective-exact-semantic-continuity-owner-decision.md`

Architecture direction: **STABLE MESSAGE EVIDENCE / SELECTIVE EXACT PROTECTION / SEMANTIC-DISCHARGE COMPACTION / OPTIONAL VERIFIED TRANSCRIPT ARCHIVE**.

Canonical consequences include:

```text
HDM guarantees semantic continuity, not universal verbatim recall
visible ChatGPT history is mutable host context, not campaign transcript authority
runtime.message owns stable accepted communication evidence identity
exact payload is retained only while typed consumers require it or an archival policy protects it
exact protection uses the smallest sufficient whole/slice representation
enduring exact game semantics move to natural canonical owners
payload compaction requires semantic-content discharge
bounded owner-declared exact dependencies/protection routing replace campaign-wide reference scans
runtime.message payload transitions EXACT_RETAINED -> COMPACTED while stable provenance/enumeration identity survives
hash/digest verifies an available copy but cannot reconstruct deleted text
STORY/TRANSCRIPT may preserve verified exact historical text without becoming gameplay truth authority
Step-5.10 Transcript candidate identity survives payload compaction
live-born message identity follows Step-5.8 source-native identity and survives absorption
host edit/retry/branch/delete cannot rewrite accepted campaign history
knowledge/disclosure/truth/chronology remain separate owners from retained transcript
maintenance age/storage pressure may select already-eligible compaction candidates but does not define semantic TTL
compaction failure/ambiguity biases toward extra retention
```

Machine-realization debt includes `runtime.message` schema/paths, accepted-text exactness and whole/slice refs, digest/provenance envelope, semantic-discharge checks, typed exact-dependency routing, natural-owner promotion, Selective-Exact Transcript source policy, deterministic exact-archive certification, Step-5.10 cursor continuity, Step-5.8-compatible live message IDs, host divergence hooks, OOC/multiplayer retention rules, exact-unavailable query semantics, legacy migration, Step-5.12 delivery integration, Step-5.13 envelope GC and bounded maintenance/integrity tests.

### Step 5.12 — CLOSED

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md`

Owner-approved scope/product decision:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-12-minimal-host-delivery-owner-scope-decision.md`

Architecture direction: **VALIDATED EMISSION-COMMIT / SOFT OUTBOUND DISCLOSURE CLOSURE / NO BASELINE DELIVERY-ACK SUBSYSTEM / DOCUMENTED INTERRUPTION RISK / RECIPIENT-SCOPED DISCLOSURE**.

Canonical consequences include:

```text
normal uninterrupted Master output is the supported baseline
host interruption/edit/Retry/branch are not campaign rewind/correction mechanisms
validated material player-facing output crosses logical EMISSION_COMMIT before becoming supported delivery evidence
runtime.message + material runtime.disclosure transitions form one HOT OutboundEmissionClosure
outbound/disclosure is normally SOFT and creates no generic second post-narration publication
loss of unsaved disclosure may cause later repetition but never replay mechanics/RNG/fiction
pending gameplay communication obligations remain with native gameplay/runtime owners, never delivery bookkeeping
no prefix/chunk exposure ledger, durable delivery outbox, background resend worker or post-render ACK state machine is baseline
material disclosure refs and recipient eligibility remain pre-emission integrity requirements
human disclosure is player-scoped and remains separate from fictional world.knowledge
outbound message IDs remain Step-5.8/5.11 collision-safe/source-native under concurrency
semantic truth-transition lineage, not Git/host order, governs disclosure revision merge
presentation repair/repetition does not create a second fictional speech/action
Story Transcript candidates come from emission-committed outbound messages, never private drafts
```

Machine-realization debt includes `runtime.disclosure` machine/catalog/schema realization, outbound `runtime.message` schema/provenance/compaction, typed NarrationResult disclosure refs, deterministic pre-emission validation/completeness guard, HOT OutboundEmissionClosure, Step-5.5/5.6 dirty publication integration, live-safe outbound IDs, recipient binding, Transcript source routing, legacy live knowledge/disclosure cleanup, auxiliary visible-surface fencing hooks, player help/manual warnings and regression cases.

Explicitly **not** Step-5.12 implementation debt: durable delivery outbox, autonomous resend worker, token/chunk exposure frontier, generic delayed-delivery reconciliation, full Retry/edit/branch repair or a per-response Git write solely for delivery tracking.

### Step 5.13 — IN PROGRESS

Task brief:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-task-brief.md`

Step 5.13 owns **Garbage Collection / Orphan Cleanup**.

Purpose: define bounded proof-driven cleanup so obsolete physical artifacts can be removed without stranding active owners, recovery dependencies, chronology relations, retained exact-text requirements, Story projection sources, disclosure/message provenance or live-epoch handoff evidence.

Required investigation includes owner-local terminality, typed protection routing, safe-delete proof coherence, replacement-before-delete ordering, checkpoint/runtime/message/Story/chronology cleanup, closed/absorbed and orphan live refs, prepared/unreachable Git objects, current Connector/RepositoryPort deletion capabilities, bounded maintenance candidate discovery and idempotent crash/concurrency handling.

The framing explicitly does **not** assume a generic mark-and-sweep/reference-count GC. Owner-local or hybrid maintenance is a valid and likely simpler outcome if it satisfies the proof obligations.

**Do not begin Step 5.14 while Step 5.13 is in progress.**

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
- Story/Chronicler activation policy and optional future async execution using the Step-5.10 coverage/CAS protocol;
- stable host invocation/message/revision identity feasibility for Step-3/5.11/5.12 edit-retry-branch semantics;
- physical pre-player-visible staging/validation feasibility for Step-4/5.12 material Narrator output before any secret-bearing content is rendered;
- inventory/fencing of actual player-visible host surfaces such as final response, commentary/tool UI, citations/widgets/errors where applicable;
- authenticated recipient/audience mapping for supported host profiles;
- whether any cheap trustworthy completed-message acknowledgement is available and worth using as an optional strengthening without becoming baseline correctness machinery;
- preparation caching/retention if justified;
- migration/catalog-gap/full-seed closure;
- final holistic architecture/catalog/seed audit;
- consolidation of implementation obligations before implementation planning.

Step 6 may optimize physical placement/deployment but cannot weaken Step-4 information boundaries or Step-5 durability/recovery/authority laws. It may strengthen host-delivery evidence cheaply, but may not introduce a mandatory delivery outbox/background reliability subsystem without a new explicit owner decision.

## Documentation / implementation debt

- `DEV/ARCHITECTURE/CATALOG_MODEL.md` and `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` remain historical derivation where later canonical specs supersede them.
- The expanded Step-5 agenda contains older wording superseded by canonical slices; use the slice specs for semantics.
- Runtime persistence/recovery/live/chronology/Story/transcript/disclosure prose and schemas are materially stale relative to Steps 5.2–5.12. Known debt includes checkpoint-first fields/assumptions, missing typed recovery routing and Procedure lifecycle, missing immutable live claims/bounded claim lookup, missing live-containment representation, campaign-only ID-allocation assumptions, one-high-level-action/one-live-write assumptions, legacy live knowledge/disclosure representation, missing Python live `RepositoryPort`, generic `CURRENT.world_time.frontier`, singleton chronology-frontier assumptions, ambiguous local sequence semantics, missing typed chronology relation domains/metric providers/bounded chronology dependency routing, absent Story root/layer schemas/projection machinery, absent finalized `runtime.message` exact-payload/provenance/protection/compaction machinery including Step-5.8-compatible live message identity, and absent finalized `runtime.disclosure` / OutboundEmissionClosure / recipient-scoped delivery integration.
- Player-facing help/manual must eventually document the Step-5.12 interruption/Retry/edit limitation.
- The owner-approved Step-5.9 forward-extensible temporal capability boundary must be reflected in eventual Dramaturg/runtime role policy.
- Broad GAME/schema/test realization remains deferred until the architecture sequence closes and implementation planning begins.

## Exact continuation point

**Step 5.13 / Garbage Collection & Orphan Cleanup — IN PROGRESS.**

Current design artifact:

`DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-task-brief.md`

Do not begin Step 5.14 until Step 5.13 architecture closes.
