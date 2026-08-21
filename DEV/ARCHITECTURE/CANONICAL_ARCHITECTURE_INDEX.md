# HDM Canonical Architecture Index — Steps 1–5

Status: **DERIVATIVE / NON-NORMATIVE NAVIGATION AND INTEGRATION INDEX**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Prepared for: **Step 5.14 / Full Recovery & Concurrency Adversarial Review**

---

# 1. Purpose and authority

This document is a fast integration map over the accepted HDM mechanical architecture through Step 5.13. It exists because the canonical design is intentionally distributed across model contracts, owner decisions, canonical specifications, amendments and final assurance artifacts.

It answers:

- **where does the authoritative rule live?**
- **who owns this state or decision?**
- **which neighboring specifications must be read together?**
- **which older abstraction has been superseded or demoted?**
- **which invariants must survive an integrated Step-5.14 stress case?**

It is **not** a new source of semantic authority. It does not create owners, schemas, lifecycle states, persistence edges or product promises.

If this index conflicts with a linked canonical specification, explicit owner decision, accepted architecture contract, machine contract or later canonical amendment, **the owning source wins and this index is stale**.

For correctness-sensitive work:

```text
locate rule here
    -> open the owning primary source
    -> verify exact current wording / scope / supersession
    -> reason from the primary source
```

Do not use this index as the sole proof for an architecturally disputed claim.

---

# 2. Source-precedence and lookup rules

Use the narrowest applicable accepted owner contract.

Practical precedence:

1. explicit owner-approved product/capability decision for its decision scope;
2. canonical specification or canonical amendment governing the concrete semantic boundary;
3. accepted architecture/model contract or machine contract to which the canonical spec delegates realization semantics;
4. final assurance / final critical-review artifact confirming closure and known residual debt;
5. current roadmap for sequencing/status only;
6. this index and `DEV/PROJECT_MAP.md` for navigation only;
7. research drafts, candidates, historical proposals and superseded status snapshots for derivation/provenance only.

A newer filename does not automatically supersede an older contract. Supersession must follow explicit status/scope or a later canonical rule.

Current sequencing authority:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Canonical design process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

General repository discovery map:

- `DEV/PROJECT_MAP.md`

---

# 3. Master stage registry

| Stage | Status | Primary accepted direction | Main sources |
|---|---|---|---|
| 1 | COMPLETE / ASSURED | class/catalog authority audited; misleading/duplicate ownership removed or assigned | `DEV/ARCHITECTURE/CRITICAL_ARCHITECTURE_AUDIT.md`; Step-1/2 final assurance |
| 2 | COMPLETE / ASSURED | deterministic resource/HP/effect/condition/duration/recovery/query architecture over explicit entity/catalog ownership | `CATALOG_CONTRACTS.md`, `CATALOG_RESOLUTION.md`, `ENTITY_STRUCTURES.md`, `ACTOR_MODEL.md`, `ASSET_MODEL.md`, `ACTIVITY_MODEL.md`, `RULE_ELEMENT_MODEL.md`, schemas/catalogs/tests; Step-1/2 final assurance |
| 3 | COMPLETE / ASSURED | **Alternative C** execution boundary | Step-3 canonical spec + final critical review |
| 4 | COMPLETE / ARCHITECTURE CLOSED | **FACT-CENTERED TRUTH / DERIVED-PLUS-OVERRIDE KNOWLEDGE / SIX LOGICAL ROLES / DETERMINISTIC CONTEXT ASSEMBLY / NON-CANONICAL STORY PROJECTION / EXPLICIT PROMOTION BOUNDARY** | Step-4 canonical spec |
| 5.0 | CLOSED | authority/contamination gate before persistence architecture | Step-5.0 final |
| 5.1 | CLOSED | **B-NARROW / domain-typed progress, no implicit cross-domain order** | Step-5.1 canonical |
| 5.2 | CLOSED | **Resumable Runtime Closure over native durable owners + bounded typed recovery routing** | Step-5.2 canonical v2 |
| 5.3 | CLOSED | **A-NARROW / OWNER-CLAIM MATERIALIZATION** | Step-5.3 canonical + 5.3↔5.9 amendment |
| 5.4 | CLOSED | **BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF** | Step-5.4 canonical |
| 5.5 | CLOSED | **EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY** | Step-5.5 canonical |
| 5.6 | CLOSED | **PYTHON-OWNED SINGLE-REF CAS PUBLICATION** | Step-5.6 canonical |
| 5.7 | CLOSED | **CURRENT-AUTHORITY-FIRST / CHECKPOINT-OPTIONAL NATIVE-ROUTED BOUNDED RECOVERY** | Step-5.7 canonical |
| 5.8 | CLOSED | **ROUTED FIXED-CLAIM LIVE EPOCH / EXACT-SOURCE CAS / TERMINAL SOURCE FREEZE / FORWARD CAMPAIGN ABSORPTION** | Step-5.8 canonical |
| 5.9 | CLOSED | **OWNER-ANCHORED SPARSE CHRONOLOGY / DOMAIN-TYPED ORDER / TYPED METRIC COORDINATES / MATERIAL BRIDGE RECONCILIATION / FORWARD-EXTENSIBLE HISTORY** | Step-5.9 canonical + owner decision + 5.3↔5.9 amendment |
| 5.10 | CLOSED | **LAYER-LOCAL COVERAGE / QUEUE-FREE PULL CATCH-UP / DETERMINISTIC STORY PUBLICATION / OPTIONAL GENERATIVE CHRONICLER / GAMEPLAY-PRIORITY SAME-REF CAS** | Step-5.10 canonical |
| 5.11 | CLOSED | **STABLE MESSAGE EVIDENCE / SELECTIVE EXACT PROTECTION / SEMANTIC-DISCHARGE COMPACTION / OPTIONAL VERIFIED TRANSCRIPT ARCHIVE** | Step-5.11 canonical + owner decision |
| 5.12 | CLOSED | **VALIDATED EMISSION-COMMIT / SOFT OUTBOUND DISCLOSURE CLOSURE / NO BASELINE DELIVERY-ACK SUBSYSTEM / DOCUMENTED INTERRUPTION RISK / RECIPIENT-SCOPED DISCLOSURE** | Step-5.12 canonical + owner scope decision |
| 5.13 | CLOSED | **OWNER-GATED RETIREMENT / CLOSED BLOCKER CONTRACTS / COMPLETENESS-TYPED PROTECTION ROUTING / PINNED CURRENT-BASIS SAFE-RETIREMENT PROOF / SURVIVOR-BEFORE-REMOVAL** | Step-5.13 canonical |
| 5.14 | NEXT / NOT STARTED | integrated recovery/concurrency red-team of all Step-5 architecture | expanded Step-5 agenda + current roadmap |

---

# 4. Global invariant backbone

These are navigation summaries. Follow the cited owner for exact law wording.

| ID | Integrated invariant | Primary owner(s) |
|---|---|---|
| GI-01 | Every mutable/current semantic concern has one authoritative owner; helper storage does not silently become a second owner. | Steps 1–2, 3, 4, 5.0 |
| GI-02 | An LLM statement, draft, narration or Story text does not become canon merely by being generated. | Steps 3–4 |
| GI-03 | Deterministic mechanical core owns accepted execution; LLMs interpret/propose within explicit boundaries. | Step 3 |
| GI-04 | Accepted execution, occurrence, message and other externally referenced identities remain stable across retry/recovery/source movement where their owner contract requires identity continuity. | Steps 3, 5.3, 5.8, 5.11–5.12 |
| GI-05 | Correctness-relevant progress/order/frontier/cursor values identify their semantic domain/scope; no implicit cross-domain comparison. | Step 5.1 |
| GI-06 | Current authority comes from current routing/native owner contracts, not branch existence, age, timestamps, remembered chat state or cached host state. | Steps 5.7–5.8 |
| GI-07 | Independently writable native sources use exact current source revision/currentness evidence as their publication fence. | Steps 5.6, 5.8 |
| GI-08 | `ESTABLISHED` and `DURABLE` are different axes. Accepted SOFT state may exist before publication; HARD is a named-edge obligation, not a quality adjective. | Step 5.5 |
| GI-09 | Prepared objects, checkpoints, Story, Agenda entries, indexes, caches and ephemeral assessments do not gain current gameplay authority merely by persisting or being useful for recovery. | Steps 5.0, 5.3, 5.7, 5.10, 5.13 |
| GI-10 | Cold recovery starts from current authority and resolves compatible native sources; it does not choose truth from the newest-looking checkpoint/branch/chat. | Steps 5.2, 5.7, 5.8 |
| GI-11 | Recovery correctness never depends on hidden LLM thought, prior conversation context or host memory. | Steps 3, 4, 5.2, 5.7 |
| GI-12 | Temporal obligation existence/lifecycle belongs to the native temporal owner; Agenda is a rebuildable candidate/dependency index; chronology is evidence; Step 3 owns accepted execution. | Step 5.3 + amendment + 5.9 |
| GI-13 | Git commit/ref/CAS order, IDs and host message order never implicitly establish fictional chronology. | Steps 5.1, 5.9 |
| GI-14 | Story is durable but noncanonical; Story lag/failure cannot block gameplay publication, SAVE or recovery readiness. | Steps 4, 5.10 |
| GI-15 | Objective truth, fictional knowledge, human-player disclosure and historical communication evidence are separate concerns/owners. | Step 4 + 5.11–5.12 |
| GI-16 | HDM promises semantic continuity, not universal verbatim recording; exact wording survives only through explicit exact protection/archive/natural-owner semantics. | Step 5.11 |
| GI-17 | Visible ChatGPT history is mutable host context, not campaign-history authority; edit/Retry/branch/delete cannot rewrite accepted campaign history. | Steps 5.11–5.12 |
| GI-18 | Irreversible cleanup is conservative: unknown/incompatible/stale proof means retain/retry/repair, not delete. | Step 5.13 |
| GI-19 | No correctness law depends on generic heartbeat, TTL, host wall-clock staleness or background polling unless a specific future owner contract explicitly adds it. | Steps 5.3–5.5, 5.8, 5.10 |
| GI-20 | Transport retry, Story conflict and presentation repair do not replay already accepted mechanics, RNG or fictional actions. | Steps 3, 5.6, 5.8, 5.10, 5.12 |
| GI-21 | No universal frontier, snapshot, scheduler, Story cursor, chronology clock or GC graph is allowed to become cross-domain authority. | Steps 5.1–5.3, 5.7, 5.9–5.10, 5.13 |
| GI-22 | Step 6 may choose physical LLM/deployment topology only if it preserves Step-4 information eligibility and Step-5 authority/durability/recovery laws. | Step 4 + roadmap Step-6 boundary |

---

# 5. End-to-end architecture spine

## 5.1 Gameplay / execution / delivery / history

```text
host communication
    ↓
runtime.interaction
    ↓
IntentPlan                       [noncanonical interpretation result]
    ↓
RuntimeCommand                   [accepted command/idempotency/provenance owner]
    ↓
Resolution(Activity) OR direct deterministic transition
    ↓
ExecutionSegment
    ↓
MechanicalEvents + receipts + mandatory children/native owner mutations
    ↓
ESTABLISHED HOT state
    ↓
Step-5.5 durability policy
    ├─ campaign publication -> Step 5.6 single-ref CAS
    └─ live publication     -> Step 5.8 exact-source CAS
    ↓
Step-4 NarrationResult / deterministic information eligibility
    ↓
Step-5.12 EMISSION_COMMIT
    ↓
outbound runtime.message + material runtime.disclosure
    ↓
Step-5.10 Story projection, optionally later/lagging
    ↓
Step-5.11 selective exact compaction/retention
    ↓
Step-5.13 owner-gated representation cleanup
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
    rebuildable enrollment / dependency-indexed candidate selection
        ↓
chronology/provider evidence
    typed order / metric / boundary / bridge evidence
        ↓
NOT_DUE | DUE | INDETERMINATE
        ↓ if accepted occurrence crosses execution boundary
Step-3 execution
    stable identity / fixed randomness / mandatory consequences
```

## 5.3 Cold recovery

```text
selected campaign reference
    ↓
pin exact current campaign H
    ↓
resolve current native/live routes
    ↓
pin exact mutable native sources
    ↓
enumerate Step-5.2 resumable roots
    ↓
hydrate required native closure
    ↓
optional compatible checkpoint acceleration
    ↓
rebuild Agenda / indexes / caches / projections as required
    ↓
validate coherent current composition
    ↓
READY | RETRY | BLOCKED
```

## 5.4 Story catch-up

```text
typed source-domain accepted evidence
    ↓
source-domain high-watermark / candidate enumeration
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

Campaign HEAD is only a transport/current-tree pin here; it is not a Story source watermark.

---

# 6. Authority and ownership map

| Concern | Authority | Durable/current representation | Helpers / projections | False authority to reject | Primary source |
|---|---|---|---|---|---|
| Catalog definition identity/schema semantics | admitted catalog/model contracts | `DEV/CATALOG`, schemas / runtime catalog realization | indexes/resolution context | mutable entity state stored in definition | Steps 1–2 contracts |
| Actor/Asset current mutable state | owning world entity | Actor/Asset owner records | derived selectors/query views | catalog definition as mutable state owner | Steps 1–2 models |
| Procedure lifecycle/resource state | `runtime.procedure` | Procedure ResourceState | Resolution/Continuation references | Activity definition or LLM prose | Step 3 |
| Accepted external exchange | `runtime.interaction` | stable accepted Interaction identity/evidence | host message context | visible chat position | Step 3 + 5.11 |
| Accepted gameplay command | `RuntimeCommand` | stable command/idempotency/provenance | IntentPlan | retry text / host request alone | Step 3 |
| Deliberative execution | `Resolution` | accepted execution state/segments | Context/LLM interpretation | hidden reasoning | Step 3 |
| Suspended Resolution generation | `Continuation` | portable exact next-instruction + accepted dependencies | host conversation | prior LLM context | Step 3 |
| Random result | deterministic runtime/RNG contract | accepted fixed RNG evidence/handle | dice prose | reroll on retry | Step 3 |
| Objective lore/truth claim | `world.lore_fact` or natural authoritative world owner | owner record | Story/Narration | Story statement | Step 4 |
| Fictional character knowledge | `world.knowledge` | knowledge owner state | Context projection | human disclosure | Step 4 |
| Human-player exposure | `runtime.disclosure` | recipient-scoped exposure state | Story/transcript/message refs | PC knowledge; Narrator intent | Step 4 + 5.12 |
| Temporal obligation | native temporal owner | owner lifecycle/occurrence/binding | Temporal Agenda | scheduler queue / due flag | Step 5.3 |
| Temporal candidate routing | none; derivative | rebuildable Agenda/index | reverse dependency enrollment | Agenda order as fictional/execution order | 5.3 amendment |
| Fictional chronology relation | accepted typed chronology evidence / native relevant owner semantics | typed anchor/relation/metric evidence | scoped indexes/frontiers | Git/ref/time/ID order | Step 5.9 |
| Campaign publication currentness | selected campaign ref + Step-5.6 protocol | exact current commit/ref | prepared commits | created commit object alone | Step 5.6 |
| Live current truth/write authority | current campaign routing + selected live epoch/native claim contract | exact live source revision + immutable claims/lifecycle | claim/routing indexes | branch existence / remembered session | Step 5.8 |
| Recovery current basis | current campaign + resolved native routes | exact pinned source composition | optional checkpoint | checkpoint/newest branch | Step 5.7 |
| Story | Story layer projection state | Story records/indexes/coverage | Chronicler draft | gameplay truth/current world state | Step 4 + 5.10 |
| Accepted communication evidence | `runtime.message` | stable envelope; exact or compacted payload according to policy | Story Transcript | mutable ChatGPT history | Step 5.11 |
| Verified exact historical transcript copy | Story Transcript + certification basis | Story noncanonical record | digest/provenance refs | objective truth | Step 5.11 |
| Cleanup eligibility | native owner terminality/replacement + closed cleanup contract proof | no generic cleanup authority required | candidate index / ephemeral SafeRetirementAssessment | age/refcount/global GC graph | Step 5.13 |
| Git unreachable-object reclamation | hosting platform, not HDM semantic authority | host-managed Git object store | repository cleanup tools if available | current-tree deletion as secure erase | Step 5.13 |

---

# 7. Durability, publication and recovery matrix

## 7.1 Durability axes

Step 5.5 separates three axes:

```text
SEMANTIC SURVIVAL
    EPHEMERAL | ESTABLISHED

CURRENT DURABILITY
    DURABLE | VOLATILE_DIRTY

CURRENT OBLIGATION
    MAY_DEFER | MUST_BE_DURABLE_BEFORE(edge)
```

Canonical shorthand:

```text
SOFT = ESTABLISHED + VOLATILE_DIRTY + MAY_DEFER
HARD = correctness-critical MUST_BE_DURABLE_BEFORE(named edge)
```

Do not infer:

```text
SOFT = unimportant
HARD = permanent
SAVE = snapshot of everything
```

SAVE selects established dirty roots required by save policy plus their compatible recovery closure, publishes them, then validates resumability. A clean save creates no heartbeat/no-op commit.

## 7.2 Campaign publication

Step 5.6:

```text
pin H
 -> freeze complete normalized write set
 -> derive one resulting tree
 -> validate resulting state
 -> create one single-parent commit C(parent=H)
 -> non-force authoritative ref CAS H -> C
 -> resolve ACCEPTED | REJECTED | INDETERMINATE
```

Prepared object creation is not authority. An ambiguous transport acknowledgement is resolved by current-ref + bounded lineage/closure evidence, not by replaying gameplay.

## 7.3 Live publication

Step 5.8:

```text
campaign route selects epoch E + immutable typed claims Q(E)
ACTIVE source @ exact L
    ↓
authorized native transition
    ↓
CAS expected L -> new exact live source revision
```

`ACTIVE -> CLOSED` is terminal. `CLOSED_UNABSORBED` remains current truth for claimed scope but has zero ordinary writers. Campaign truth for that scope resumes only after forward absorption succeeds.

## 7.4 Checkpoints

A checkpoint is optional immutable acceleration/evidence, never current-state authority. Cold recovery starts from current campaign routing and exact native sources even when a checkpoint exists.

---

# 8. Information, memory and Story map

| Dimension | Objective truth | Fictional knowledge | Human disclosure | `runtime.message` | Story |
|---|---|---|---|---|---|
| Owner | `world.lore_fact` / natural world owner | `world.knowledge` | `runtime.disclosure` | accepted communication evidence owner | Story layer projection |
| Canonical gameplay authority? | yes, within owner scope | yes, for fictional knowledge | yes, for human exposure bookkeeping | evidence identity/content according to retention contract; not world truth | no |
| Recipient/perspective scoped? | not inherently | character/entity scoped | human recipient scoped | communication/source scoped | presentation/read-model scoped |
| Exact wording required? | only if natural owner semantics require exact text | generally proposition/knowledge semantics | no universal exact wording requirement | selectively | optional/verified exact in Transcript layer |
| Can imply objective truth? | n/a | no | no | no | no |
| Can imply PC knowledge? | not automatically | n/a | no | no | no |
| Can lag? | no for current owner state | no for current owner state | SOFT durability may lag publication | payload may compact after discharge | yes, explicitly |
| Recovery may invent missing value? | no | no | no | no | no |

Key rule:

```text
truth != knowledge != disclosure != communication evidence != Story
```

Context Assembler and Narrator eligibility must respect these boundaries. Physical role isolation is Step 6, but Step 6 may not weaken them.

---

# 9. Temporal / chronology locator

## 9.1 Four responsibilities

```text
NATIVE TEMPORAL OWNER
    WHAT obligation exists and which occurrence/lifecycle/binding is current

TEMPORAL AGENDA
    WHAT armed occurrence may require reevaluation after dependency changes

CHRONOLOGY
    WHAT typed causal/order/metric/boundary evidence is lawfully available

STEP-3 EXECUTION
    WHAT accepted due consequence actually executes
```

## 9.2 Canonical relation vocabulary

Conceptually:

```text
CAUSES(A,B)
PRECEDES(A,B,D)
SAME_COORDINATE(A,B,C)
ELAPSED(A,B,C,[lo,hi])
```

`D` is an order domain. `C` is a metric coordinate context. Causal ancestry and calendar/metric order are not interchangeable.

Metric provider position:

```text
EXACT(v)
BOUNDED(lo,hi)
UNKNOWN
```

Due evaluation remains derived:

```text
NOT_DUE | DUE | INDETERMINATE
```

No generic durable `due=true` becomes temporal authority.

## 9.3 Forbidden chronology shortcuts

Never infer fictional order/simultaneity from:

- Git commit order;
- ref movement;
- CAS order;
- host response order;
- stable IDs;
- Story order;
- Agenda/list order;
- source absorption order;
- wall-clock elapsed time without an admitted owner/provider contract.

---

# 10. Story projection / transcript / delivery / cleanup chain

## 10.1 Story projection

Per layer/source-domain:

```text
backlog = accepted candidate basis - compatible coverage
```

Coverage is typed by:

```text
layer
+ source domain
+ semantic projection-contract generation
```

No global Story frontier. No background worker/job queue required. Chronicler may generate a draft, but deterministic core owns final IDs, validation, indexes, coverage and publication.

## 10.2 Selective exact memory

Product contract from Step 5.11:

> HDM preserves semantic continuity and exact wording where exactness is materially protected; it is not a universal recorder of every historical utterance.

Message payload lifecycle is conceptually:

```text
EXACT_RETAINED
    ↓ after all exact consumers discharged/promoted/archived
COMPACTED
    ↓ only after Step-5.13 safe-retirement proof if current envelope itself is disposable
RETIRED CURRENT REPRESENTATION
```

A digest proves equality only when a candidate copy exists; it cannot reconstruct deleted text.

## 10.3 Host delivery

Supported baseline is normal uninterrupted Master output:

```text
NarrationResult
 -> deterministic material disclosure / recipient validation
 -> freeze supported player-visible response
 -> EMISSION_COMMIT
 -> outbound runtime.message + relevant runtime.disclosure HOT closure
 -> host presentation
```

Baseline intentionally has no durable delivery outbox, post-render ACK protocol, background resend worker or token/chunk exposure ledger.

Interruption/Edit/Retry/branch is not campaign rewind. Interruption may cause the user to miss content that HDM already treats as emitted; this is an accepted/documented presentation limitation.

## 10.4 Cleanup

A target representation is automatically retired only under a compatible closed cleanup contract and a coherent current proof including:

```text
compatible cleanup contract
native terminality / sufficient replacement
closed blocker vocabulary
current blocker absence/discharge
all blocker-creating source classes covered
survivor closure complete
surviving reference semantics valid
resulting state valid
publication/currentness basis still valid
```

Unknown => retain.

---

# 11. Practical rule locator

Open the listed primary sources after locating the concern here.

| Question | Primary source(s) | Search anchor / concept |
|---|---|---|
| Who owns current Actor/Asset HP/resources/effects? | `ENTITY_STRUCTURES.md`, `ACTOR_MODEL.md`, `ASSET_MODEL.md`, Step-1/2 assurance | field placement / mutable state ownership |
| Can a catalog definition carry mutable current entity state? | `CATALOG_CONTRACTS.md`, entity models | definition vs state ownership |
| How is a catalog reference resolved? | `CATALOG_RESOLUTION.md` | canonical deterministic resolution / ambiguity error |
| Can an LLM directly establish a mechanical consequence? | Step-3 canonical | deterministic execution authority |
| What is the accepted user-action/idempotency unit? | Step-3 canonical | `runtime.interaction`, `RuntimeCommand` |
| Does identical text mean the same command? | Step-3 canonical | retry identity vs new Interaction |
| Can retry/recovery reroll accepted randomness? | Step 3 + 5.6 + 5.8 | fixed RNG / no replay |
| Who owns long-running Procedure state? | Step 3 | `runtime.procedure` sole ResourceState owner |
| What survives suspended execution? | Step 3 + 5.2 | Continuation / fixed accepted dependencies |
| Can Narrator prose create objective truth? | Step 4 | promotion boundary / no LLM canon by statement |
| Does a player knowing a secret imply the PC knows it? | Step 4 | disclosure vs fictional knowledge |
| Does PC knowledge imply player disclosure? | Step 4 | `world.knowledge` vs `runtime.disclosure` |
| Can Story be used as current world truth? | Step 4 + 5.10 | Story noncanonical read model |
| Can Git commit order establish fictional event order? | 5.1 + 5.9 | no implicit cross-domain order |
| Is there one global campaign frontier? | 5.1 | B-NARROW / no generic Frontier |
| What must a fresh process recover? | 5.2 + 5.7 | Resumable Runtime Closure / current-authority-first recovery |
| Can recovery depend on previous LLM context? | Step 3 + 5.2 | no hidden thought/state dependency |
| Who owns whether a timer/trigger still exists? | 5.3 | native temporal owner |
| Can Temporal Agenda order two due occurrences fictionally? | 5.3 + amendment | Agenda is candidate index, no fictional order |
| What happens when late chronology evidence makes a timer decidable? | 5.3↔5.9 amendment | dependency-indexed recheck |
| Is host wall-clock passage fictional time? | 5.3 + 5.9 | cold hydration/process restart does not advance fiction |
| What does a clean controlled host handoff promise? | 5.4 | scoped recovery-safe barrier |
| What does SOFT mean? | 5.5 | established + volatile dirty + may defer |
| What makes something HARD? | 5.5 | MUST_BE_DURABLE_BEFORE(named edge) |
| Does SAVE require Story catch-up? | 5.5 + 5.10 | Story not in gameplay save closure by default |
| How is campaign state published? | 5.6 | Python-owned single-ref CAS |
| Does a prepared Git commit establish canon? | 5.6 | prepared objects nonauthority |
| What if publication ACK is lost? | 5.6 | current-ref + bounded lineage/closure proof |
| Can newest checkpoint override current branch state? | 5.7 | checkpoint optional evidence only |
| Does branch existence make a live branch authoritative? | 5.8 | routing selects live authority |
| Can two ordinary writers own the same live scope? | 5.8 | at most one ordinary writable authority |
| Can `CLOSED_UNABSORBED` be treated as campaign truth? | 5.8 | closed live source remains truth until absorption |
| Do live-created stable IDs rekey on absorption? | 5.8 | epoch-qualified stable identity survives absorption |
| Can two independent scenes remain temporally incomparable? | 5.1 + 5.9 | typed domains / sparse chronology |
| Can a time-travel arrival be earlier on calendar but later causally? | 5.9 | causal vs metric/calendar order separation |
| Where does metric deadline current position come from? | 5.9 | `ResolveTemporalPosition` / provider routing |
| Can Chronicler assign final Story IDs or advance coverage by prose? | 5.10 | deterministic finalization |
| Can Story publication failure block canon? | 5.10 | gameplay-priority / Story lag allowed |
| Is campaign HEAD a Story projection cursor? | 5.10 | HEAD is transport pin, not source watermark |
| Can changing model/prompt force whole Story replay? | 5.10 | projection-contract generation, not model version |
| Is visible ChatGPT history the durable transcript? | 5.11 | mutable host context, not authority |
| Can HDM promise an exact old quote after compaction? | 5.11 | only if exact copy/protection survives |
| Can a Story Transcript exact copy become world truth? | Step 4 + 5.11 | exact communication evidence != truth |
| Can old host Edit/Retry rewrite accepted campaign history? | 5.11 + 5.12 | no |
| When does outbound player disclosure become HDM exposure evidence? | 5.12 | logical `EMISSION_COMMIT` |
| Does interruption require a delivery outbox/retry worker? | 5.12 owner decision | explicitly no baseline reliability subsystem |
| Can presentation repair repeat the fictional NPC action? | 5.12 | repair/repetition != second fictional speech/action |
| Can cleanup delete a target merely because nothing currently references it in a best-effort index? | 5.13 | negative proof requires completeness-typed protection routing |
| Can cleanup delete `CLOSED_UNABSORBED` live state? | 5.8 + 5.13 | no |
| Does deleting a current path erase its old Git blob? | 5.13 | current-tree retirement != Git-history erasure |
| May runtime recover an exact quote from old Git history after lawful semantic compaction? | 5.11 + 5.13 | no semantic resurrection from transport/audit history |
| Can a cleanup index authorize its own deletion? | 5.13 | protection-routing generation lifecycle |

---

# 12. Supersession / contamination ledger

This table is intentionally blunt: it prevents Step 5.14 from accidentally reviving an older convenience abstraction.

| Older / tempting abstraction | Current disposition | Owning correction |
|---|---|---|
| `CURRENT.world_time.frontier` as generic global chronology authority | noncanonical/superseded | 5.1 + 5.9 |
| singleton `scene.chronology_frontier_event_id` as universal active history edge | superseded by scoped `ActiveExtensionFrontier`; singleton only possible optimization | 5.9 |
| `world_order.sequence` or generic local sequence as cross-domain fictional order | invalid unless explicit owner-defined domain semantics exist | 5.1 + 5.9 |
| one-hour / `durable_frontier_time` durability contract | noncanonical debt | 5.5 |
| checkpoint-first recovery / checkpoint as snapshot authority | rejected | 5.2 + 5.7 |
| universal `RecoveryCut`/snapshot owner | rejected | 5.1–5.2 + 5.7 |
| generic durable scheduler/pending queue/firing authority | rejected | 5.3 |
| durable generic `due=true` | rejected; due is derived | 5.3 + 5.9 |
| Agenda/list order as execution or chronology authority | rejected | 5.3 + amendment |
| host heartbeat/TTL as live authority | rejected | 5.4 + 5.8 |
| branch existence/age/name as live authority | rejected | 5.8 |
| campaign-global Story frontier | rejected | 5.10 |
| campaign HEAD as Story source watermark | rejected | 5.10 |
| durable Story job queue/worker lease as baseline projection authority | rejected | 5.10 |
| visible ChatGPT history as immutable transcript authority | rejected | 5.11 |
| universal exact transcript forever | rejected by owner decision S | 5.11 |
| Story Transcript as objective truth | rejected | Step 4 + 5.11 |
| live-local per-PC knowledge/disclosure as a second global semantic owner | reject duplicate ownership; semantic owners remain `world.knowledge` / `runtime.disclosure` | Step 4 + 5.8 + 5.12 |
| post-render delivery ACK/outbox/chunk ledger as baseline requirement | explicitly **not** implementation debt | 5.12 owner decision |
| generic global GC / mark-and-sweep semantic graph | rejected | 5.13 |
| generic durable reference count as deletion authority | rejected | 5.13 |
| Git historical reachability as secret exact-memory fallback | rejected as semantic resurrection | 5.11 + 5.13 |
| `DEV/ARCHITECTURE/CATALOG_DESIGN_STATUS.md` as current sequencing authority | historical snapshot; do not use as current roadmap | file status + `NEAR_TERM_ROADMAP.md` |
| `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` as current Step-5 authority | historical derivation where later canonical specs supersede it | roadmap / later specs |

---

# 13. Step-6 boundary / unresolved realization classes

Step 5 establishes semantic laws. Step 6 owns physical deployment/context feasibility and final integrated closure.

Major Step-6 carry-forward classes include:

- real context isolation/reset feasibility for the six logical LLM roles;
- minimum physical model-call topology preserving Step-4 eligibility;
- model selection and token/latency/cost budgets;
- ordinary ChatGPT vs richer host capability profiles;
- deterministic Python `RepositoryPort` bridge feasibility for campaign/live CAS and optional post-authority ref cleanup;
- authenticated acting-principal and recipient/audience mapping;
- stable host invocation/message/revision/retry identity feasibility;
- physical pre-player-visible Narrator staging/validation before secret-bearing output can render;
- fencing/inventory of actual player-visible host surfaces;
- optional cheap completed-message acknowledgement if available, without making it baseline correctness machinery;
- Chronicler activation policy / optional future asynchronous optimization over the already-canonical queue-free coverage protocol;
- migration/catalog/full-seed closure;
- final holistic catalog/schema/architecture audit;
- consolidation of implementation obligations before implementation planning.

These are **not** permission to reopen accepted Step-4/5 semantic boundaries merely for easier deployment.

---

# 14. Step-5.14 attack lookup matrix

Use this section as the initial scenario-router. Each test should then read the exact primary sources listed.

| # | Integrated adversarial scenario | Required specs to read together | Critical invariant(s) |
|---:|---|---|---|
| 1 | long singleplayer run with accumulated SOFT state | 3, 5.2, 5.5, 5.6, 5.7 | accepted state not invented/lost outside declared RPO; no hidden-context dependency |
| 2 | explicit SAVE | 5.2, 5.5, 5.6, 5.7, 5.10 | selected dirty roots + recovery closure durable; Story not prerequisite |
| 3 | controlled chat/runtime handoff | 3, 5.2, 5.4, 5.5, 5.7 | scoped acceptance barrier; promised RRC actually durable before acknowledgement |
| 4 | abrupt crash before durability boundary | 5.2, 5.5, 5.7 | recover only actual durable established sources; unpublished SOFT not invented |
| 5 | crash / lost ACK during campaign publication | 3, 5.5, 5.6, 5.7 | bounded lineage proof; no replay accepted mechanics/RNG |
| 6 | crash with suspended Resolution/Continuation | 3, 5.2, 5.5, 5.7 | exact continuation generation + fixed prior dependencies survive or recovery blocks |
| 7 | due temporal trigger crash before/after child materialization | 3, 5.3, amendment, 5.7, 5.9 | no lost/no double occurrence; claimed/accepted identity gates fresh materialization |
| 8 | fixed RNG generated before suspension/restart | 3, 5.2, 5.6–5.8 | fixed RNG reused; never rerolled for transport/recovery retry |
| 9 | two players in independent scenes | 5.1, 5.7–5.9 | independent authority/chronology may remain incomparable; no global vector requirement |
| 10 | two players in one live scene | 3, 5.5, 5.8 | exact-source CAS serialization; one truth authority / max one ordinary writer per scope |
| 11 | concurrent live CAS conflict | 3, 5.8 | stale candidate refresh/revalidate; no blind overwrite/replay |
| 12 | live epoch close / rollover / failed absorption | 5.2, 5.7, 5.8, 5.13 | CLOSED stays truth/no writers; forward absorption resumes; no reopen for maintenance |
| 13 | entity crosses live ownership scopes | 5.8, 5.9, 5.13 | freeze/transfer/absorb rules preserve identity and dependent evidence |
| 14 | global event touches multiple active scenes | 3, 5.5, 5.8, 5.9 | no accidental distributed transaction/total order; required synchronization explicit |
| 15 | campaign commit order conflicts with fictional chronology | 5.1, 5.6, 5.9 | transport order has zero implicit fictional ordering force |
| 16 | cross-scene temporal dependency appears after independent advancement | 5.1, 5.3 amendment, 5.9 | sparse bridge evidence + bounded dependent recheck; uncertainty preserved |
| 17 | Story lags; Chronicler restarts | 4, 5.7, 5.10 | queue-free pull catch-up; no duplicate/invented canon; layer-local coverage |
| 18 | Story publication fails while canon succeeds | 5.5, 5.6, 5.10 | canon stays accepted; Story failure never rolls back/blocks gameplay |
| 19 | transcript compaction while Story/history refs exist | 4, 5.10, 5.11, 5.13 | semantic discharge + exact certification + cursor/provenance continuity |
| 20 | disclosure generation/emission/interruption/Retry edge | 3, 4, 5.11, 5.12 | no mechanics rewind; recipient eligibility before emission; accepted presentation limitation remains bounded |
| 21 | checkpoint recovery with missing/corrupt dependency | 5.2, 5.7, 5.13 | checkpoint never overrides missing current-native requirements; READY/RETRY/BLOCKED honest |
| 22 | stale multiplayer session after membership/authority change | 5.4, 5.7, 5.8, 5.12 | stale host/session state cannot establish authority or leak recipient-restricted data |
| 23 | local entity/fact promotion forced by durable runtime/history/knowledge dependency | 3, 4, 5.5, 5.8, 5.11 | natural owner promotion before dependency escapes; no Story/message authority substitution |
| 24 | cleanup of obsolete artifact under concurrent/recovery dependencies | 5.2, 5.7–5.13 | coherent current negative proof; survivor-before-removal; uncertainty retains |
| 25 | engine/catalog upgrade changes cleanup blocker vocabulary while open execution exists | 3, 5.2, 5.13 | pinned compatible interpretation; migration before new automatic cleanup semantics |
| 26 | fresh process loses all LLM/chat memory with ACTIVE + CLOSED_UNABSORBED + Continuation + temporal owner + lagging Story | 3, 4, 5.2–5.10 | bounded native-source recovery recreates required working state without host memory |
| 27 | Story-only commit races gameplay commit | 5.6, 5.10 | semantic disjointness may cause transport rebuild only; never gameplay re-execution |
| 28 | late chronology bridge turns armed owner from INDETERMINATE to DUE while live sources move | 5.3 amendment, 5.7–5.9 | dependency enrollment tracks provider/route movement; same occurrence identity preserved |
| 29 | exact Transcript is last surviving text copy and source envelope retires | 4, 5.10–5.13 | exact certification basis survives; Story still not truth; opaque/survivor-backed refs explicit |
| 30 | cleanup candidate/protection index generation changes during an assessment | 5.13 | currentness movement invalidates old negative proof; index never authorizes its own retirement |

5.14 may add stronger composite scenarios. It should not reduce this matrix merely because each local slice already had an adversarial review.

---

# 15. Canonical artifact registry

## 15.1 Steps 1–2

Final assurance/status:

- `DEV/docs/superpowers/specs/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`

Primary model/contract anchors:

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

For a concrete Step-2 mechanic, follow the owner/model/schema references rather than treating the final assurance document as the detailed rule definition.

## 15.2 Step 3

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-3-final-critical-review.md`

## 15.3 Step 4

- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`

## 15.4 Step 5

- 5.0: `DEV/docs/superpowers/specs/2026-08-20-step-5-0-authority-contamination-final.md`
- 5.1: `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md`
- 5.2: `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`
- 5.3: `DEV/docs/superpowers/specs/2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md`
- 5.3↔5.9 amendment: `DEV/docs/superpowers/specs/2026-08-21-step-5-3-5-9-temporal-agenda-chronology-integration-canonical-amendment.md`
- 5.4: `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-canonical-spec.md`
- 5.5: `DEV/docs/superpowers/specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md`
- 5.6: `DEV/docs/superpowers/specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md`
- 5.7: `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`
- 5.8: `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md`
- 5.9: `DEV/docs/superpowers/specs/2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md`
- 5.9 owner decision: `DEV/docs/superpowers/specs/2026-08-21-step-5-9-forward-extensible-time-boundary-owner-decision.md`
- 5.10: `DEV/docs/superpowers/specs/2026-08-21-step-5-10-story-projection-durability-canonical-spec.md`
- 5.11: `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md`
- 5.11 owner decision: `DEV/docs/superpowers/specs/2026-08-21-step-5-11-selective-exact-semantic-continuity-owner-decision.md`
- 5.12: `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md`
- 5.12 owner decision: `DEV/docs/superpowers/specs/2026-08-21-step-5-12-minimal-host-delivery-owner-scope-decision.md`
- 5.13: `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`

Working/historical Step-5 agenda used to construct 5.14 scenario coverage:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-expanded-architecture-agenda.md`

The per-slice canonical specs supersede older agenda wording where they differ.

---

# 16. Search anchors / glossary

| Term | Fast meaning | First place to open |
|---|---|---|
| `Interaction` | accepted external exchange / interpretation-idempotency unit | Step 3 |
| `IntentPlan` | noncanonical interpreted intent candidate | Step 3 |
| `RuntimeCommand` | accepted command/idempotency/provenance publication unit | Step 3 |
| `Resolution` | deliberative Activity execution owner | Step 3 |
| `ExecutionSegment` | atomic accepted resolution slice with events/receipts/mandatory children | Step 3 |
| `Procedure` | sole owner of long-running Procedure ResourceState | Step 3 |
| `Continuation` | portable suspended Resolution generation | Step 3 |
| `LoreFact` | stable objective truth/lore claim owner where explicit fact semantics needed | Step 4 |
| `world.knowledge` | fictional knowledge authority | Step 4 |
| `runtime.disclosure` | human recipient exposure authority | Step 4 + 5.12 |
| `Resumable Runtime Closure` | recoverability property over compatible native durable sources + routing | 5.2 |
| `TemporalBinding` | owner-governed temporal predicate/boundary/metric relation | 5.3 + 5.9 |
| `FiringIdentity` / occurrence identity | stable temporal occurrence identity preventing duplicate fresh materialization | 5.3 |
| `Temporal Agenda` | rebuildable dependency-indexed armed-owner candidate selector | 5.3 amendment |
| `ActiveExtensionFrontier` | scoped set of still-required chronology extension anchors | 5.9 |
| metric context | typed temporal ruler/coordinate context, not global clock | 5.9 |
| `StoryLayerProjectionState` | conceptual layer-local allocator/coverage/index state | 5.10 |
| `MUST_MATERIALIZE` | candidate cannot be covered without durable layer representation | 5.10 |
| `MAY_OMIT` | candidate may be deliberately considered without Story record | 5.10 |
| `runtime.message` | stable accepted communication evidence identity | 5.11 |
| `EMISSION_COMMIT` | logical boundary after validated supported outbound response is frozen for player-facing emission | 5.12 |
| `OutboundEmissionClosure` | HOT outbound message + material disclosure/provenance closure | 5.12 |
| `CleanupContract` | target-kind-specific closed blocker/survivor/currentness vocabulary for safe retirement | 5.13 |
| `SafeRetirementAssessment` | ephemeral deterministic proof working value; never liveness authority | 5.13 |

---

# 17. Step-5.14 usage protocol

Before running a composite failure case:

1. identify every semantic owner touched by the scenario;
2. identify every independently mutable durability source;
3. locate the governing rules in Sections 6, 11 and 14;
4. open the exact primary specs;
5. write the expected pre-crash/current-authority composition explicitly;
6. distinguish `prospective`, `ESTABLISHED`, `DURABLE`, `current authority`, `projection`, `evidence` and `transport state`;
7. inject crash/concurrency/retry/source-movement failure;
8. recover only from permitted durable/current evidence;
9. verify no owner was duplicated, lost, invented or silently replaced;
10. classify every finding as:

```text
ARCHITECTURE BLOCKER
IMPLEMENTATION DEBT
STEP-6 FEASIBILITY DEPENDENCY
ACCEPTED PRODUCT LIMITATION / RISK
NO DEFECT
```

An earlier Step-5 slice should reopen only when integrated evidence proves a real contradiction or unsatisfied correctness invariant. Convenience, implementation difficulty or a preference for a different abstraction is not enough.

---

# 18. Maintenance rule for this index

Update this index when:

- a canonical architecture rule changes;
- an owner decision is added/revised;
- a canonical amendment changes a cross-slice seam;
- a previously historical abstraction becomes current or vice versa;
- Step 5.14 resolves an integrated contradiction;
- Step 6 later establishes physical realizations that materially affect navigation/supersession.

Do not update it merely to copy every schema field or every implementation detail. Its value comes from being a compact **semantic locator and integration map**, not a parallel specification corpus.
