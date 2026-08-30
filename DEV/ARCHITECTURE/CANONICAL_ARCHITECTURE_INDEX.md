# HDM Canonical Architecture Index — Steps 1–5 and Later Canonical Additions

Status: **DERIVATIVE / NON-NORMATIVE NAVIGATION AND INTEGRATION INDEX**

Date: 2026-08-29

Architecture state: **STEPS 1–5 CLOSED; S6D COMPLETE / INTEGRATED CLOSURE PASS; R2.7 WP-06 CLOSED / SENIOR REVIEW PASS; DOCUMENTATION CORPUS REFACTOR ACTIVE; WP-07 NOT STARTED**

---

# 1. Purpose and authority

This document is the fast integration map over accepted HDM mechanical architecture through Step 5.14. The canonical design is intentionally distributed across model contracts, owner decisions, canonical specifications, amendments and final assurance/review artifacts.

Use this file to answer quickly:

- where does the authoritative rule live?
- who owns this state/decision?
- which neighboring specs must be read together?
- which older abstraction is superseded/demoted?
- which integrated recovery/concurrency invariant is relevant?
- which Step-6 feasibility gate depends on the rule?

It is **not** a semantic source of truth. It creates no owners, schemas, lifecycle states, persistence edges or product promises.

If this index conflicts with an owning canonical specification, explicit owner decision, accepted architecture/model contract, machine contract or later canonical amendment, **the owning source wins and this index is stale**.

Correctness-sensitive workflow:

```text
locate rule here
    -> open owning primary source
    -> verify exact current wording / scope / supersession
    -> reason from primary source
```

Do not use this index as the sole proof for an architecturally disputed claim.

Canonical integrated Step-5 closure:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md`

---

# 2. Source precedence and sequencing

Practical precedence:

1. explicit owner-approved product/capability decision for its decision scope;
2. canonical specification/amendment governing the concrete semantic boundary;
3. accepted architecture/model contract or machine contract delegated by that spec;
4. canonical final integrated review / assurance confirming closure and known residual debt;
5. current roadmap for sequencing/status only;
6. this index and `DEV/PROJECT_MAP.md` for navigation only;
7. research drafts/candidates/historical proposals/status snapshots for derivation only.

Filename recency alone never establishes supersession.

Sequencing authority:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Architecture process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

General repository discovery:

- `DEV/PROJECT_MAP.md`

---

# 3. Master stage registry

| Stage | Status | Primary accepted direction | Main sources |
|---|---|---|---|
| 1 | COMPLETE / ASSURED | catalog/class authority audited; misleading/duplicate ownership removed/assigned | `CRITICAL_ARCHITECTURE_AUDIT.md`; Step-1/2 assurance |
| 2 | COMPLETE / ASSURED | deterministic resource/HP/effect/condition/duration/recovery/query architecture over explicit entity/catalog ownership | architecture models/contracts + schemas/catalogs/tests + Step-1/2 assurance |
| 3 | COMPLETE / ASSURED | **Alternative C** execution boundary | Step-3 canonical + final critical review |
| 4 | COMPLETE / ARCHITECTURE CLOSED | **FACT-CENTERED TRUTH / DERIVED-PLUS-OVERRIDE KNOWLEDGE / SIX LOGICAL ROLES / DETERMINISTIC CONTEXT ASSEMBLY / NON-CANONICAL STORY / EXPLICIT PROMOTION** | Step-4 canonical |
| 5 | COMPLETE / ARCHITECTURE CLOSED | integrated durability/recovery/live/chronology/Story/transcript/disclosure/cleanup model survived full adversarial review | Step-5.14 canonical final |
| 5.0 | CLOSED | authority/contamination gate | Step-5.0 final |
| 5.1 | CLOSED | **B-NARROW / domain-typed progress, no implicit cross-domain order** | Step-5.1 canonical |
| 5.2 | CLOSED | **RRC over native durable owners + bounded typed recovery routing** | Step-5.2 canonical v2 |
| 5.3 | CLOSED | **A-NARROW / OWNER-CLAIM MATERIALIZATION** | Step-5.3 canonical + 5.3↔5.9 amendment |
| 5.4 | CLOSED | **BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF** | Step-5.4 canonical |
| 5.5 | CLOSED | **EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY** | Step-5.5 canonical |
| 5.6 | CLOSED | **PYTHON-OWNED SINGLE-REF CAS PUBLICATION** | Step-5.6 canonical |
| 5.7 | CLOSED | **CURRENT-AUTHORITY-FIRST / CHECKPOINT-OPTIONAL NATIVE-ROUTED BOUNDED RECOVERY** | Step-5.7 canonical |
| 5.8 | CLOSED | **ROUTED FIXED-CLAIM LIVE EPOCH / EXACT-SOURCE CAS / TERMINAL FREEZE / FORWARD ABSORPTION** | Step-5.8 canonical |
| 5.9 | CLOSED | **OWNER-ANCHORED SPARSE CHRONOLOGY / DOMAIN-TYPED ORDER / TYPED METRIC COORDINATES / MATERIAL BRIDGES / FORWARD-EXTENSIBLE HISTORY** | Step-5.9 + owner decision + amendment |
| 5.10 | CLOSED | **LAYER-LOCAL COVERAGE / QUEUE-FREE PULL CATCH-UP / DETERMINISTIC STORY PUBLICATION / OPTIONAL CHRONICLER / GAMEPLAY-PRIORITY CAS** | Step-5.10 |
| 5.11 | CLOSED | **STABLE MESSAGE EVIDENCE / SELECTIVE EXACT / SEMANTIC-DISCHARGE COMPACTION / OPTIONAL VERIFIED TRANSCRIPT** | Step-5.11 + owner decision |
| 5.12 | CLOSED | **VALIDATED EMISSION-COMMIT / SOFT OUTBOUND DISCLOSURE / NO BASELINE DELIVERY-ACK SUBSYSTEM / RECIPIENT-SCOPED** | Step-5.12 + owner decision |
| 5.13 | CLOSED | **OWNER-GATED RETIREMENT / CLOSED BLOCKERS / COMPLETE TYPED PROTECTION / CURRENT-BASIS PROOF / SURVIVOR-BEFORE-REMOVAL** | Step-5.13 |
| 5.14 | CLOSED | **FULL RECOVERY & CONCURRENCY ADVERSARIAL REVIEW — 0 UNRESOLVED STEP-5 BLOCKERS** | Step-5.14 canonical final |
| Former Step 6 | CLOSED / REBASELINED | physical-host findings reallocated into Round 2; old stage is not active | Round-1 closure / Round-2 rebaseline owner decision |
| S6D-01 | COMPLETE / ARCHITECTURE CLOSED | content-addressed ruleset package snapshots + exact resolved-set identity + owner-local context projections | `RULESET_PACKAGE_IDENTITY.md`; S6D-01 canonicalization |
| S6D | COMPLETE / INTEGRATED CLOSURE PASS | S6D-01…12 semantic closure plus MRC-01…04 realization verified; Step-8 blocked disposition is historical only | `2026-08-29-s6d-integrated-machine-realization-closure.md`; roadmap |
| R2.7 | WP-06 CLOSED / SENIOR REVIEW PASS; DOCUMENTATION CORPUS REFACTOR ACTIVE; WP-07 NOT STARTED | inserted refactor is required before substantive WP-07 and is not a numbered WP | roadmap + R2.7 durable cursor |

---

# 4. Global invariant backbone

These are locator summaries; open the owning source for exact law text.

| ID | Integrated invariant | Primary owner(s) |
|---|---|---|
| GI-01 | Every mutable/current semantic concern has one authoritative owner; helper storage never silently becomes a second owner. | Steps 1–4, 5.0 |
| GI-02 | LLM statement/draft/narration/Story text does not become canon merely by generation. | Steps 3–4 |
| GI-03 | Deterministic core owns accepted execution; LLMs interpret/propose only inside typed boundaries. | Step 3 |
| GI-04 | Accepted execution/occurrence/message identities remain stable across retry/recovery/source movement where owner contract requires continuity. | Step 3, 5.3, 5.8, 5.11–5.12 |
| GI-05 | Correctness-relevant progress/order/frontier/cursor values name their semantic domain/scope; no implicit cross-domain comparison. | 5.1 |
| GI-06 | Current authority comes from current routing/native owner contracts, never branch age/name, timestamps, cached session or remembered chat. | 5.7–5.8 |
| GI-07 | Independently writable native sources use exact source revision/currentness as publication fence. | 5.6, 5.8 |
| GI-08 | `ESTABLISHED` and `DURABLE` are distinct; SOFT may be current but crash-volatile; HARD is a named-edge obligation. | 5.5 |
| GI-09 | Prepared objects, checkpoints, Story, Agenda, indexes/caches and cleanup assessments do not gain gameplay authority by persistence/usefulness. | 5.0, 5.3, 5.7, 5.10, 5.13 |
| GI-10 | Cold recovery starts from current authority and resolves compatible native sources; newest-looking checkpoint/branch/chat never wins by appearance. | 5.2, 5.7, 5.8 |
| GI-11 | Recovery never depends on hidden LLM thought, prior context or process memory. | 3, 4, 5.2, 5.7 |
| GI-12 | Temporal owner says what exists; Agenda says what may need recheck; chronology supplies evidence; Step 3 executes accepted consequence. | 5.3 + amendment + 5.9 |
| GI-13 | Git/ref/CAS/ID/host-message order never implicitly establishes fictional chronology. | 5.1, 5.9 |
| GI-14 | Story is durable but noncanonical; lag/failure cannot block gameplay publication, SAVE or recovery READY. | 4, 5.10 |
| GI-15 | Objective truth, fictional knowledge, human disclosure, accepted communication evidence and Story are distinct. | 4, 5.11–5.12 |
| GI-16 | HDM promises semantic continuity, not universal verbatim recording; exactness survives only through explicit protection/archive/natural-owner semantics. | 5.11 |
| GI-17 | Visible ChatGPT history is mutable host context; Edit/Retry/branch/delete cannot rewrite accepted campaign history. | 5.11–5.12 |
| GI-18 | Irreversible cleanup is conservative: unknown/incompatible/stale proof means retain/retry/repair. | 5.13 |
| GI-19 | No correctness law relies on generic heartbeat/TTL/wall-clock/background polling unless a future explicit owner contract adds it. | 5.3–5.5, 5.8, 5.10, 5.13 |
| GI-20 | Transport retry, Story conflict and presentation repair never replay already accepted mechanics/RNG/fictional actions. | 3, 5.6, 5.8, 5.10, 5.12 |
| GI-21 | No universal frontier/snapshot/scheduler/Story cursor/chronology clock/GC graph may become cross-domain authority. | 5.1–5.3, 5.7, 5.9–5.10, 5.13 |
| GI-22 | Step 6 may optimize physical topology only while preserving Step-4 information eligibility and Step-5 authority/durability/recovery. | 4 + 5.14 |
| GI-23 | Role-context basis is domain-composed: campaign pin plus exact current native source pins selected by routing; campaign HEAD alone is not complete current truth. | 5.14-1 + 5.1/5.7/5.8 |
| GI-24 | Cross-source cleanup protection must precede/participate in consumer acceptance unless consumer is self-contained or source fenced. | 5.14-2 + 5.13 |
| GI-25 | `runtime.disclosure` monotonic merge is owner-specific; never generalize to arbitrary mutable owners or transport last-writer-wins. | 5.14-3 + 5.12 |
| GI-26 | Partial multi-live prerequisite freeze is technical currentness, not partial fictional establishment. | 5.14-4 + 5.8 |

---

# 5. End-to-end architecture spine

## 5.1 Gameplay / execution / delivery / history

```text
host communication
    ↓
runtime.interaction
    ↓
IntentPlan                       [noncanonical interpretation]
    ↓
RuntimeCommand                   [accepted command/idempotency/provenance]
    ↓
Resolution(Activity) OR direct deterministic transition
    ↓
ExecutionSegment
    ↓
MechanicalEvents + receipts + mandatory children + native owner mutations
    ↓
ESTABLISHED HOT state
    ↓
Step-5.5 durability policy
    ├─ campaign publication -> Step 5.6 exact-base single-ref CAS
    └─ live publication     -> Step 5.8 exact-source CAS
    ↓
Step-4 NarrationResult / information eligibility
    ↓
Step-5.12 EMISSION_COMMIT
    ↓
outbound runtime.message + relevant runtime.disclosure
    ↓
Step-5.10 Story projection, optionally lagging
    ↓
Step-5.11 selective exact retention/compaction
    ↓
Step-5.13 owner-gated cleanup
```

Critical non-equivalences:

```text
accepted command        != narrated prose
narrated prose           != objective truth
runtime.disclosure       != PC knowledge
runtime.message          != world truth
Story                    != canon
ESTABLISHED              != DURABLE
current-tree deletion    != Git historical erasure
```

## 5.2 Temporal execution

```text
native temporal owner
    owns obligation + occurrence + TemporalBinding + lifecycle
        ↓
Temporal Agenda
    rebuildable dependency-indexed candidate selection
        ↓
chronology/provider evidence
    typed order / metric / boundary / bridge evidence
        ↓
NOT_DUE | DUE | INDETERMINATE
        ↓ if occurrence crosses accepted execution boundary
Step-3 execution
    stable identity / fixed randomness / mandatory consequences
```

## 5.3 Cold recovery

```text
selected campaign ref
    ↓
pin exact campaign H
    ↓
resolve current native/live routes
    ↓
pin exact mutable native sources
    ↓
enumerate RRC roots
    ↓
hydrate required native closure
    ↓
optional compatible checkpoint acceleration
    ↓
rebuild Agenda / indexes / caches / projections as required
    ↓
validate coherent current domain-composed basis
    ↓
READY | RETRY | BLOCKED
```

The coherent composition need not represent one wall-clock instant and is not a stored global snapshot.

## 5.4 Story catch-up

```text
typed accepted source evidence
    ↓
source-domain candidate enumeration/high watermark
    −
compatible layer coverage
    =
backlog
    ↓
optional Chronicler draft
    ↓
deterministic validation / ID allocation / index+coverage closure
    ↓
Story-only publication
```

Campaign HEAD is transport/current-tree pin only; it is not Story source watermark.

---

# 6. Authority and ownership map

| Concern | Authority | Durable/current representation | Helpers / projections | False authority to reject | Primary source |
|---|---|---|---|---|---|
| Catalog definition identity/schema | admitted catalog/model contracts | `DEV/CATALOG`, schemas/runtime catalog realization | indexes/resolution context | definition as mutable entity-state owner | Steps 1–2 |
| Actor/Asset current mutable state | owning world entity | Actor/Asset owner records | selectors/query views | catalog definition | Steps 1–2 |
| Procedure lifecycle/resource state | `runtime.procedure` | Procedure ResourceState | Resolution/Continuation refs | Activity definition/LLM prose | Step 3 |
| Accepted external exchange | `runtime.interaction` | stable Interaction identity/evidence | host context | visible chat position | 3 + 5.11 |
| Accepted gameplay command | RuntimeCommand | command/idempotency/provenance | IntentPlan | retry text alone | 3 |
| Deliberative execution | Resolution | accepted execution state/segments | typed context | hidden reasoning | 3 |
| Suspended Resolution generation | Continuation | portable next-instruction + accepted deps | host conversation | prior LLM context | 3 |
| Random result | deterministic runtime/RNG contract | accepted fixed RNG evidence | dice prose | reroll on retry | 3 |
| Objective lore/truth | `world.lore_fact` or natural world owner | owner record | Story/Narration | Story statement | 4 |
| Fictional knowledge | `world.knowledge` | knowledge owner state | role-context projection | human disclosure | 4 |
| Human exposure | `runtime.disclosure` | recipient-scoped state | message/Story refs | PC knowledge/Narrator intent | 4 + 5.12 |
| Temporal obligation | native temporal owner | lifecycle/occurrence/binding | Agenda | scheduler/due flag | 5.3 |
| Temporal candidate routing | none; derivative | rebuildable Agenda/index | reverse enrollment | Agenda order as fiction | 5.3 amendment |
| Fictional chronology relation | accepted typed chronology evidence | anchor/relation/metric evidence | scoped indexes/frontiers | Git/ref/time/ID order | 5.9 |
| Campaign durable publication | selected campaign ref + 5.6 protocol | exact commit/ref | prepared objects | created commit alone | 5.6 |
| Live current truth/write authority | current campaign routing + selected live epoch/claims | exact live revision | routing/claim indexes | branch existence/session memory | 5.8 |
| Recovery basis | current campaign + resolved routes | exact pinned source composition | checkpoint | checkpoint/newest branch | 5.7 + 5.14 |
| Role-context source basis | receiving role + current routing/accepted pinned inputs | ephemeral exact domain-composed source basis | Context Assembler | campaign HEAD as universal current frontier | 4 + 5.14 |
| Story | Story layer projection state | Story records/indexes/coverage | Chronicler draft | gameplay truth/recovery authority | 4 + 5.10 |
| Accepted communication evidence | `runtime.message` | stable envelope; exact/compacted payload | Story Transcript | mutable chat history | 5.11 |
| Verified exact historical Transcript | Story Transcript + certification basis | noncanonical Story record | digest/provenance | objective truth | 5.11 |
| Cleanup eligibility | native owner terminality/replacement + cleanup proof | no generic owner | candidate index/SafeRetirementAssessment | age/refcount/global GC | 5.13 + 5.14 |
| Git unreachable-object reclamation | host platform | host-managed object store | cleanup tools | current delete as secure erase | 5.13 |

---

# 7. Durability / publication / recovery matrix

## 7.1 Durability axes

```text
SEMANTIC SURVIVAL
    EPHEMERAL | ESTABLISHED

CURRENT DURABILITY
    DURABLE | VOLATILE_DIRTY

CURRENT OBLIGATION
    MAY_DEFER | MUST_BE_DURABLE_BEFORE(edge)
```

```text
SOFT = ESTABLISHED + VOLATILE_DIRTY + MAY_DEFER
HARD = MUST_BE_DURABLE_BEFORE(named edge)
```

Never infer `SOFT = unimportant`, `HARD = permanent`, or `SAVE = snapshot of everything`.

SAVE selects established dirty gameplay-significant roots plus compatible recovery/reference/interpretation closure. Clean SAVE needs no heartbeat/no-op commit.

## 7.2 Campaign publication

```text
pin H
 -> freeze normalized delta + dependency footprint
 -> derive one resulting tree
 -> validate resulting state
 -> one single-parent commit C(parent=H)
 -> non-force authoritative ref CAS H -> C
 -> ACCEPTED | REJECTED | INDETERMINATE
```

Prepared objects are nonauthority. Ambiguous ACK resolves by current ref + bounded lineage/closure evidence; transport retry never replays accepted gameplay.

## 7.3 Live publication

```text
campaign route selects epoch E + immutable claims Q(E)
ACTIVE @ exact L
    ↓
authorized native transition
    ↓
CAS expected L -> L2
```

`ACTIVE -> CLOSED` is terminal. `CLOSED_UNABSORBED` stays current truth with zero ordinary writers until forward campaign absorption.

## 7.4 Multi-live cross-scope transition

```text
close/freeze A
close/freeze B
...
(partial freeze = technical state only)
    ↓
all required final sources known
    ↓
one campaign-domain transition establishes cross-scope semantic result
```

Do not interpret one user action as a distributed Step-3 segment over several refs.

## 7.5 Checkpoints

Checkpoint = optional immutable recovery/maintenance evidence, never current-state authority or SAVE proof.

---

# 8. Information / memory / Story map

| Dimension | Objective truth | Fictional knowledge | Human disclosure | `runtime.message` | Story |
|---|---|---|---|---|---|
| Owner | `world.lore_fact` / natural world owner | `world.knowledge` | `runtime.disclosure` | accepted communication evidence | Story layer projection |
| Gameplay authority? | yes within scope | yes for epistemic state | yes for exposure bookkeeping | evidence only, not proposition truth | no |
| Scoped by | proposition/world owner | fictional subject | human recipient | communication/source | presentation/availability |
| Exact wording | only when natural semantics require it | usually proposition-level | no universal requirement | selective | optional verified exact Transcript |
| Implies objective truth? | n/a | no | no | no | no |
| Implies PC knowledge? | not automatically | n/a | no | no | no |
| May lag durability? | current owner may be SOFT | current owner may be SOFT | normally SOFT after emission | payload may compact | yes explicitly |

Key rule:

```text
truth != knowledge != disclosure != communication evidence != Story
```

Role-context source basis must respect current live/native authority as required by LAW 5.14-1.

---

# 9. Temporal / chronology locator

```text
NATIVE TEMPORAL OWNER
    WHAT obligation/occurrence/binding exists

TEMPORAL AGENDA
    WHAT armed occurrence may need reevaluation

CHRONOLOGY
    WHAT typed evidence is available

STEP-3 EXECUTION
    WHAT accepted due consequence executes
```

Conceptual relations:

```text
CAUSES(A,B)
PRECEDES(A,B,D)
SAME_COORDINATE(A,B,C)
ELAPSED(A,B,C,[lo,hi])
```

`D` = order domain. `C` = metric coordinate context.

Metric provider position:

```text
EXACT(v)
BOUNDED(lo,hi)
UNKNOWN
```

Derived due state:

```text
NOT_DUE | DUE | INDETERMINATE
```

Never infer fictional order/simultaneity from Git commit/ref/CAS order, host response order, stable IDs, Story order, Agenda order, absorption order or host wall-clock unless an owning temporal contract explicitly establishes the relation.

---

# 10. Story / transcript / delivery / cleanup chain

## 10.1 Story projection

Per layer/source domain:

```text
backlog = accepted candidate basis - compatible coverage
```

Coverage is typed by layer + source domain + projection-contract generation.

No global Story frontier, mandatory background worker or durable Story job queue. Chronicler may generate; deterministic core owns final validation/IDs/indexes/coverage/publication.

## 10.2 Selective exact memory

```text
EXACT_RETAINED
    ↓ after exact consumers discharged/promoted/archived
COMPACTED
    ↓ after Step-5.13 safe-retirement proof if envelope disposable
RETIRED CURRENT REPRESENTATION
```

Digest validates equality against an available copy; it cannot reconstruct deleted text.

## 10.3 Host delivery

```text
NarrationResult
 -> material disclosure / recipient validation
 -> freeze supported response
 -> EMISSION_COMMIT
 -> outbound runtime.message + runtime.disclosure HOT closure
 -> host presentation
```

Baseline has no delivery outbox, post-render ACK state machine, background resend worker or token/prefix exposure ledger.

Interruption/Edit/Retry/branch is not campaign rewind. Interruption after emission commit may over-confirm the full committed representation; this is accepted product risk.

## 10.4 Cleanup

Automatic retirement requires at least:

```text
compatible closed CleanupContract
native terminality / sufficient replacement
closed blocker vocabulary
current blocker absence/discharge
all blocker-creating source classes covered
survivor closure complete
surviving reference semantics valid
resulting state valid
publication/currentness basis valid
```

Cross-source consumer safety uses one of:

```text
SELF-CONTAINED CONSUMER
PROTECTION REGISTERED BEFORE/AT ACCEPTANCE
SOURCE FENCE / SYNCHRONIZATION
```

Unknown/ambiguous/stale => retain/retry/repair.

---

# 11. Practical rule locator

Open the listed primary source after locating a concern here.

| Question | Primary source(s) | Search anchor |
|---|---|---|
| Who owns current Actor/Asset HP/resources/effects? | Step-2 models/contracts | mutable state ownership |
| Can catalog definition carry mutable current entity state? | `CATALOG_CONTRACTS.md` + entity models | definition vs state |
| How is catalog reference resolved? | `CATALOG_RESOLUTION.md` | deterministic resolution |
| Can an LLM establish mechanical consequence directly? | Step 3 | deterministic execution authority |
| What is accepted action/idempotency unit? | Step 3 | Interaction / RuntimeCommand |
| Does identical text mean same command? | Step 3 | retry identity vs new Interaction |
| Can retry/recovery reroll accepted RNG? | 3 + 5.6 + 5.8 | fixed RNG / no replay |
| Who owns Procedure state? | 3 | Procedure sole ResourceState owner |
| What survives suspended execution? | 3 + 5.2 | Continuation + pinned dependencies |
| Can Narrator prose create truth? | 4 | promotion / no LLM canon |
| Does player disclosure imply PC knowledge? | 4 | disclosure vs knowledge |
| Does PC knowledge imply player disclosure? | 4 | knowledge vs disclosure |
| Can Story be current world truth? | 4 + 5.10 | noncanonical Story |
| What current sources may Context Assembler use? | 4 + 5.7 + 5.8 + 5.14 | domain-composed role-context basis |
| Can campaign HEAD alone stand for all current truth? | 5.1 + 5.7 + 5.8 + 5.14 | no; live/native sources may own scopes |
| Can Git order establish fictional order? | 5.1 + 5.9 | no implicit cross-domain order |
| Is there one global campaign frontier? | 5.1 | B-NARROW |
| What must fresh process recover? | 5.2 + 5.7 | RRC / current-authority-first |
| Can recovery depend on prior LLM context? | 3 + 5.2 | no hidden state dependency |
| Who owns timer/trigger existence? | 5.3 | native temporal owner |
| Can Agenda order due occurrences fictionally? | 5.3 + amendment | no |
| What happens when late chronology evidence changes due result? | amendment + 5.9 | typed dependent recheck |
| Is host wall clock fictional time? | 5.3 + 5.9 | no |
| What does controlled handoff promise? | 5.4 | scoped durable RRC before ack |
| What does SOFT mean? | 5.5 | established + volatile dirty + may defer |
| What makes something HARD? | 5.5 | named durability edge |
| Does SAVE require Story catch-up? | 5.5 + 5.10 | no |
| How is campaign state published? | 5.6 | Python-owned single-ref CAS |
| Does prepared commit establish state? | 5.6 | no |
| Lost publication ACK? | 5.6 | current ref + bounded lineage proof |
| Can checkpoint override current branch/native state? | 5.7 | no |
| Does branch existence make live source authoritative? | 5.8 | routing selects authority |
| Can two ordinary writers own same live scope? | 5.8 | no |
| What is CLOSED_UNABSORBED? | 5.8 | current truth, zero writers |
| Do live IDs rekey on absorption? | 5.8 | no |
| Can independent scenes remain temporally incomparable? | 5.1 + 5.9 | yes |
| Can time-travel arrival be calendar-earlier but causally-later? | 5.9 | yes; separate causal/metric order |
| Where does metric deadline position come from? | 5.9 | ResolveTemporalPosition |
| Can Chronicler assign authoritative Story IDs/coverage? | 5.10 | no; deterministic core finalizes |
| Can Story failure block canon? | 5.10 | no |
| Is campaign HEAD Story cursor? | 5.10 | no |
| Can model/prompt change force Story replay? | 5.10 | projection contract generation, not model version |
| Is visible ChatGPT history durable transcript authority? | 5.11 | no |
| Exact old quote after compaction? | 5.11 | only if exact evidence survives |
| Can exact Transcript become world truth? | 4 + 5.11 | no |
| Can old Edit/Retry rewrite accepted history? | 5.11 + 5.12 | no |
| When does outbound disclosure become exposure evidence? | 5.12 | EMISSION_COMMIT |
| Does interruption require outbox/worker? | 5.12 owner decision | no baseline subsystem |
| Can presentation repair repeat fictional NPC action? | 5.12 | no |
| How merge concurrent disclosure updates? | 5.12 + 5.14 | semantic monotonic owner merge only |
| Can same merge rule apply to world.knowledge? | 5.14 | no unless owner separately proves it |
| Can cleanup trust absence in best-effort index? | 5.13 | no; complete typed protection required |
| Can cleanup accept consumer then register protection later? | 5.13 + 5.14 | no unless self-contained/fenced |
| Can cleanup delete CLOSED_UNABSORBED live source? | 5.8 + 5.13 | no |
| Does current delete erase old Git blob? | 5.13 | no |
| Can runtime resurrect compacted quote from Git history? | 5.11 + 5.13 | no ordinary semantic resurrection |
| Can cleanup index authorize own retirement? | 5.13 | no |
| What happens if physical host cannot enforce Step-4/5 boundary? | 5.14 + roadmap Step 6 | reject/refine profile before weakening semantics |

---

# 12. Supersession / contamination ledger

| Older / tempting abstraction | Current disposition | Owning correction |
|---|---|---|
| `CURRENT.world_time.frontier` as global chronology authority | superseded/noncanonical | 5.1 + 5.9 |
| singleton `scene.chronology_frontier_event_id` as universal history edge | superseded by scoped ActiveExtensionFrontier; singleton only optimization | 5.9 |
| `world_order.sequence` as cross-domain fictional order | invalid absent explicit owner domain semantics | 5.1 + 5.9 |
| one-hour / `durable_frontier_time` durability contract | noncanonical debt | 5.5 |
| checkpoint-first recovery / checkpoint snapshot authority | rejected | 5.2 + 5.7 |
| universal RecoveryCut/snapshot owner | rejected | 5.1–5.2 + 5.7 |
| generic durable scheduler/pending queue/firing authority | rejected | 5.3 |
| durable generic `due=true` | rejected; due derived | 5.3 + 5.9 |
| Agenda/list order as execution/chronology order | rejected | 5.3 + amendment |
| host heartbeat/TTL as authority | rejected | 5.4 + 5.8 |
| branch existence/age/name as live authority | rejected | 5.8 |
| campaign-global Story frontier | rejected | 5.10 |
| campaign HEAD as Story source watermark | rejected | 5.10 |
| durable Story job queue/worker lease baseline | rejected | 5.10 |
| visible ChatGPT history as immutable transcript | rejected | 5.11 |
| universal exact transcript forever | rejected by Selective Exact owner decision | 5.11 |
| Story Transcript as objective truth | rejected | 4 + 5.11 |
| live-local duplicate knowledge/disclosure owner | rejected; semantic owners remain world.knowledge/runtime.disclosure | 4 + 5.8 + 5.12 |
| generic last-writer-wins for overlapping disclosure/world state | rejected; owner-specific semantics only | 5.6 + 5.12 + 5.14 |
| post-render delivery ACK/outbox/chunk ledger baseline | explicitly not implementation debt | 5.12 owner decision |
| generic global GC / mark-and-sweep semantic graph | rejected | 5.13 |
| generic durable refcount as deletion authority | rejected | 5.13 |
| protect-after-accept cross-source cleanup dependency | rejected as unsafe | 5.13 + 5.14 |
| Git historical reachability as exact-memory fallback | rejected as semantic resurrection | 5.11 + 5.13 |
| campaign HEAD as complete Step-4 role-context source basis | rejected after live/native ownership; use domain-composed basis | 5.14 |
| `CATALOG_DESIGN_STATUS.md` as sequencing authority | historical snapshot | roadmap |
| `MECHANICAL_RUNTIME_PROPOSAL.md` as current Step-5 authority | historical derivation | later canonical specs |

---

# 13. Step-6 boundary / feasibility gates

Step 5 is closed. The former Step 6 has been rebaselined; its physical-host findings were allocated into Round 2. Current sequencing is owned by `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`.

Material gates identified by Step 5.14:

| ID | Step-6 proof | Severity |
|---|---|---|
| SD-1 | deterministic authenticated Python-owned/equivalent `RepositoryPort` preserving Step-5.6 semantics | BLOCKING for persistence-capable profile |
| SD-2 | material Narrator output staged/validated before player-visible secret-bearing render | BLOCKING for secret-bearing profile |
| SD-3 | stable invocation/message/retry/edit/branch identity adequate for claimed idempotency profile | SIGNIFICANT / potentially blocking |
| SD-4 | authenticated acting-principal and recipient/audience mapping | BLOCKING for secure multiplayer profile |
| SD-5 | genuine role-context isolation/reset or separate compatible invocations | BLOCKING for mixed-privilege logical-role topology |
| SD-6 | optional live-ref deletion | nonblocking; cleanup may be capability-deferred |

Other Step-6 carry-forward:

- physical six-role model-call topology;
- model selection and token/latency/cost budgets;
- ordinary ChatGPT vs richer host profiles;
- player-visible surface inventory/fencing;
- optional cheap completed-message acknowledgement;
- Commentator serving/spoiler policy;
- Story/Chronicler activation/optional async optimization;
- migration/catalog/full-seed closure;
- holistic architecture/catalog/schema audit;
- consolidation of implementation obligations before implementation planning.

**Step-6 feasibility failure rejects/refines/restricts a deployment profile before weakening accepted Step-4/5 semantics.**

---

# 14. Step-5.14 closure / regression attack matrix

Step 5.14 completed all thirty routes below plus seven stronger composites. Keep this matrix as the integrated regression router during later realization.

| # | Integrated adversarial scenario | Required specs | Critical invariant |
|---:|---|---|---|
| 1 | long singleplayer accumulated SOFT | 3, 5.2, 5.5–5.7 | no invention beyond actual durable RPO |
| 2 | explicit SAVE | 5.2, 5.5–5.7, 5.10 | selected dirty roots + RRC durable; Story irrelevant |
| 3 | controlled handoff | 3, 5.2, 5.4–5.5, 5.7 | scoped barrier + actual durable RRC before ack |
| 4 | abrupt crash before durability | 5.2, 5.5, 5.7 | lost SOFT not invented |
| 5 | crash/lost campaign publication ACK | 3, 5.5–5.7 | bounded lineage/current proof; no replay |
| 6 | suspended Resolution/Continuation crash | 3, 5.2, 5.5, 5.7 | same generation/fixed deps survive or block |
| 7 | due temporal trigger crash pre/post materialization | 3, 5.3, amendment, 5.7, 5.9 | no lost/double occurrence |
| 8 | fixed RNG before restart | 3, 5.2, 5.6–5.8 | exact accepted RNG reused |
| 9 | players in independent scenes | 5.1, 5.7–5.9 | independent authority/chronology may remain incomparable |
| 10 | players in one live scene | 3, 5.5, 5.8 | exact-source CAS; one writable authority |
| 11 | live CAS conflict | 3, 5.8 | stale refresh/revalidate; no overwrite/replay |
| 12 | close/rollover/failed absorption | 5.2, 5.7–5.8, 5.13 | CLOSED truth/no writers; forward resume |
| 13 | entity crosses live scopes | 5.8–5.9, 5.13, 5.14 | freeze/transfer identity; partial freeze not partial fiction |
| 14 | global event touches multiple live scenes | 3, 5.5, 5.8–5.9, 5.14 | no distributed semantic transaction |
| 15 | commit order conflicts with fictional chronology | 5.1, 5.6, 5.9 | transport order no fictional force |
| 16 | late cross-scene temporal dependency | 5.1, amendment, 5.9 | sparse bridge + bounded recheck |
| 17 | Story lag / Chronicler restart | 4, 5.7, 5.10 | queue-free pull catch-up |
| 18 | Story publication fails while canon succeeds | 5.5–5.6, 5.10 | canon never waits/rolls back |
| 19 | transcript compaction with Story/history refs | 4, 5.10–5.11, 5.13 | discharge/certification/cursor survivor |
| 20 | disclosure emission/interruption/Retry | 3–4, 5.11–5.12 | eligibility before emission; no gameplay replay |
| 21 | checkpoint missing/corrupt dependency | 5.2, 5.7, 5.13 | checkpoint never overrides native requirements |
| 22 | stale session after membership/authority change | 5.4, 5.7–5.8, 5.12, 5.14 | stale host grants no authority; Step-6 physical fence required |
| 23 | local entity/fact promotion from durable dependency | 3–4, 5.5, 5.8, 5.11 | natural owner before dependency escape |
| 24 | cleanup under concurrent/recovery dependency | 5.2, 5.7–5.14 | current complete negative proof + survivor-first |
| 25 | cleanup vocabulary upgrade with open execution | 3, 5.2, 5.13 | pinned interpretation + migration before cleanup |
| 26 | zero LLM memory with ACTIVE+CLOSED+Continuation+temporal+lagging Story | 3–4, 5.2–5.10 | bounded native recovery without host memory |
| 27 | Story-only commit races gameplay | 5.6, 5.10 | transport-only rebuild if truly disjoint; no replay |
| 28 | late chronology bridge makes owner due during source move | amendment, 5.7–5.9 | enrollment/provider currentness + same occurrence ID |
| 29 | exact Transcript last copy while source retires | 4, 5.10–5.14 | certification survivor; Story still not truth |
| 30 | protection generation changes during cleanup assessment | 5.13–5.14 | old negative proof invalidates; index never self-authorizes |

Stronger composite attacks closed by 5.14:

1. total host amnesia across mixed ACTIVE/CLOSED/Continuation/temporal/Story/disclosure state;
2. SAVE racing Story movement + live advancement + ambiguous ACK;
3. cleanup racing new live consumer;
4. late chronology bridge racing owner/provider transfer;
5. cleanup contract generation change while old Continuation open;
6. stale revoked host attempts write + secret-bearing emission;
7. lawfully compacted exact text remains in old Git history.

Detailed outcomes: Step-5.14 integrated review + analytical challenge + canonical final.

---

# 15. Canonical artifact registry

## 15.1 Steps 1–2

Final assurance:

- `DEV/docs/superpowers/design/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`

Primary anchors:

- `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`
- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`
- `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md`
- `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md`
- `DEV/ARCHITECTURE/ACTOR_MODEL.md`
- `DEV/ARCHITECTURE/ASSET_MODEL.md`
- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`
- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`
- `DEV/CATALOG/`
- `DEV/SCHEMAS/`
- `DEV/TESTS/`

For a concrete Step-2 mechanic, follow owning model/schema references; do not treat final assurance as detailed rule definition.

## 15.2 Step 3

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`
- `DEV/docs/superpowers/design/2026-08-19-step-3-final-critical-review.md`

## 15.3 Step 4

- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`

## 15.4 Step 5

- 5.0: `DEV/docs/superpowers/specs/2026-08-20-step-5-0-authority-contamination-final.md`
- 5.1: `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md`
- 5.2: `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`
- 5.3: `DEV/docs/superpowers/specs/2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md`
- 5.3↔5.9: `DEV/docs/superpowers/specs/2026-08-21-step-5-3-5-9-temporal-agenda-chronology-integration-canonical-amendment.md`
- 5.4: `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-canonical-spec.md`
- 5.5: `DEV/docs/superpowers/specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md`
- 5.6: `DEV/docs/superpowers/specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md`
- 5.7: `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`
- 5.8: `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md`
- 5.9: `DEV/docs/superpowers/specs/2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md`
- 5.9 decision: `DEV/docs/superpowers/design/2026-08-21-step-5-9-forward-extensible-time-boundary-owner-decision.md`
- 5.10: `DEV/docs/superpowers/specs/2026-08-21-step-5-10-story-projection-durability-canonical-spec.md`
- 5.11: `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md`
- 5.11 decision: `DEV/docs/superpowers/design/2026-08-21-step-5-11-selective-exact-semantic-continuity-owner-decision.md`
- 5.12: `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md`
- 5.12 decision: `DEV/docs/superpowers/specs/2026-08-21-step-5-12-minimal-host-delivery-owner-scope-decision.md`
- 5.13: `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`
- 5.14 task: `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-task-brief.md`
- 5.14 integrated review: `DEV/docs/superpowers/specs/2026-08-21-step-5-14-integrated-adversarial-review-draft.md`
- 5.14 challenge: `DEV/docs/superpowers/specs/2026-08-21-step-5-14-analytical-challenge.md`
- 5.14 gate: `DEV/docs/superpowers/specs/2026-08-21-step-5-14-resolution-gate.md`
- **5.14 canonical final / Step-5 closure:** `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md`

Historical Step-5 agenda:

- `DEV/docs/superpowers/design/2026-08-20-step-5-expanded-architecture-agenda.md`

Per-slice canon + Step-5.14 integration clarifications supersede older agenda wording where they differ.

---

# 16. Search anchors / glossary

| Term | Fast meaning | First place to open |
|---|---|---|
| Interaction | accepted external exchange / interpretation-idempotency unit | 3 |
| IntentPlan | noncanonical interpreted intent candidate | 3 |
| RuntimeCommand | accepted command/idempotency/provenance root | 3 |
| Resolution | one Activity execution owner | 3 |
| ExecutionSegment | local atomic accepted execution slice | 3 |
| Procedure | sole owner of long-running Procedure ResourceState | 3 |
| Continuation | portable suspended Resolution generation | 3 |
| LoreFact | objective claim identity where durable proposition semantics needed | 4 |
| `world.knowledge` | fictional epistemic authority | 4 |
| `runtime.disclosure` | human recipient exposure authority | 4 + 5.12 |
| Resumable Runtime Closure | recoverability property over compatible native durable sources + routing | 5.2 |
| TemporalBinding | owner-governed temporal predicate/boundary/metric relation | 5.3 + 5.9 |
| Firing/occurrence identity | stable temporal occurrence identity preventing duplicate materialization | 5.3 |
| Temporal Agenda | rebuildable dependency-indexed armed-owner selector | amendment |
| ActiveExtensionFrontier | scoped chronology anchors still required for extension/recovery basis | 5.9 |
| metric context | typed temporal ruler, not global clock | 5.9 |
| StoryLayerProjectionState | layer-local allocator/coverage/index state | 5.10 |
| MUST_MATERIALIZE | Story candidate cannot be covered without required durable layer output | 5.10 |
| MAY_OMIT | candidate may be terminally considered without Story output | 5.10 |
| `runtime.message` | stable accepted communication evidence identity | 5.11 |
| EMISSION_COMMIT | validated/frozen supported outbound representation committed to player-visible path | 5.12 |
| OutboundEmissionClosure | HOT outbound message + material disclosure/provenance closure | 5.12 |
| CleanupContract | target-kind/generation closed blocker/survivor/currentness vocabulary | 5.13 |
| SafeRetirementAssessment | ephemeral deterministic cleanup proof working value | 5.13 |
| domain-composed role-context basis | current exact source composition for one role invocation, not campaign-HEAD-only | 5.14 |
| protection-before-acceptance | cross-source cleanup registration safety ordering | 5.14 |

---

# 17. Integrated failure-case usage protocol

Use this for later implementation/adversarial verification, not as a substitute for owning specs:

1. identify every semantic owner touched;
2. identify independently mutable durability/current sources;
3. locate governing rules in Sections 6, 11 and 14;
4. open exact primary specs;
5. write pre-failure current-authority/source composition;
6. distinguish `prospective`, `ESTABLISHED`, `DURABLE`, `current authority`, `projection`, `evidence`, `transport state`;
7. inject crash/concurrency/retry/source movement;
8. recover/reconcile only from permitted current/durable evidence;
9. verify no owner was duplicated, lost, invented or silently replaced;
10. classify finding:

```text
ARCHITECTURE BLOCKER
IMPLEMENTATION DEBT
STEP-6 FEASIBILITY DEPENDENCY
ACCEPTED PRODUCT LIMITATION / RISK
NO DEFECT
```

A closed Step-5 slice should reopen only when integrated evidence proves a real contradiction/unsatisfied invariant. Implementation inconvenience or preference for a central abstraction is not enough.

---

# 18. Maintenance rule

Update this index when:

- canonical architecture changes;
- owner decision is added/revised;
- canonical amendment changes a cross-slice seam;
- historical/current authority status changes;
- a later stage establishes physical realizations that materially change navigation/supersession;
- later implementation review exposes a real Step-5 reopen condition.

Do not copy every schema field/implementation detail here. The index is valuable as a compact **semantic locator + integration map + adversarial router**, not as a parallel specification corpus.