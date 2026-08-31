# R2.1 Task Brief — Continuity, Memory and History-Aligned Derived State

Status: **ACTIVE TASK BRIEF — R2.1 IN PROGRESS**

Date: 2026-08-24

Roadmap authority:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Program decision:

- `DEV/docs/superpowers/specs/2026-08-24-round-2-roadmap-owner-decision.md`

Evidence disposition:

- `DEV/docs/superpowers/design/2026-08-24-round-2-evidence-disposition-ledger.md`

---

## 1. Task classification

**Architectural / deep-work task.**

R2.1 defines long-campaign continuity semantics that will constrain Actor continuity, Context Runtime, LLM execution, multiplayer catch-up and eventual machine realization.

No implementation is authorized.

---

## 2. Problem statement

Round 1 already defines:

- authoritative current world/runtime owners;
- objective lore propositions;
- fictional knowledge;
- human disclosure;
- semantic/mechanical history evidence;
- Story as a durable noncanonical projection;
- selective exact versus semantic history retention;
- host Retry/Edit/branch/delete as non-authoritative presentation controls.

What is not yet fully designed is the **derived continuity layer used by long-running LLM reasoning**.

R2.1 must determine the minimum continuity products needed for a long campaign, their authority/lifecycle/provenance, and how they remain aligned with accepted history without becoming duplicate canon.

The design must make it possible to forget/compress/rebuild derived representations while preserving the product promise of strong semantic continuity.

---

## 3. Primary decision questions

### 3.1 Continuity classes

Determine which classes are actually required, considering at least:

- authoritative current state/evidence as upstream sources, not a new memory layer;
- recent exact/history evidence;
- broad campaign continuity summary;
- episodic recall records;
- entity-local continuity;
- deep/history archive retrieval basis;
- exact-protected material already governed by Step 5.11;
- derived/private continuity products that later Actor work may consume.

Reject unnecessary layers.

### 3.2 Authority and lifecycle

For every admitted continuity product decide:

- authoritative vs derived;
- durable vs ephemeral;
- rebuildable vs exact-protected;
- source coverage/provenance;
- creation/admission boundary;
- update/consolidation boundary;
- stale/superseded detection;
- repair/rebuild behavior;
- retirement/compaction behavior.

No derived product may become a second writable owner of current world truth, knowledge, disclosure or Story source history.

### 3.3 Stability and consolidation

Determine when recent evidence may be consolidated.

The design must distinguish:

- host-editable/retriable presentation history;
- accepted HDM Interaction/message/history evidence;
- current accepted branch/ancestry;
- semantic evidence stable enough to support a derived representation.

Do not equate "old enough in the UI" with stable campaign history.

### 3.4 History alignment

Define how history-dependent derived continuity behaves when:

- host Retry/regeneration occurs;
- an older user message is edited;
- a host conversation branches;
- a legitimate new HDM semantic branch/correction exists;
- source facts are superseded/corrected;
- an old derived record refers to incompatible ancestry.

The host conversation tree must not become canonical chronology or campaign branch authority.

### 3.5 Semantic versus exact recall

Reconcile R2.1 with Step 5.11:

- what HDM already promises semantically;
- what exact text is protected by existing owner contracts;
- what long-range semantic recall adds;
- when an exact archive lookup is required;
- what the engine must say/do when exact wording was lawfully compacted.

R2.1 must not silently expand the product promise into universal verbatim recall.

### 3.6 Derived mutation and repair

Evaluate bounded evidence-bound update patterns for derived continuity:

```text
bounded source evidence
    -> candidate transformation/update/NO_CHANGE
    -> deterministic structural/source validation
    -> admitted derived write
```

The general Step-3 LLM-proposer/deterministic-commit principle is inherited. R2.1 decides only what additional validation/provenance is required for continuity products.

---

## 4. Explicit non-goals

R2.1 does **not** design:

- detailed Actor cognition/goals/relationships — R2.2;
- context ranking/token allocation/placement — R2.3;
- single-context role execution/instruction composition — R2.4;
- multiplayer coordination/catch-up protocol — R2.5;
- final ChatGPT host assurance — R2.6;
- schemas/catalogs/runtime implementation — R2.7 mapping and later implementation planning;
- generic knowledge graphs;
- universal vector memory;
- automatic entity discovery;
- plugin/extension architecture;
- new canonical plot/planning authority.

If analysis proves one of these is a prerequisite rather than a downstream concern, record the dependency and propose a roadmap change rather than silently expanding R2.1.

---

## 5. Round-1 constraints that remain law

R2.1 must preserve at least:

- one semantic owner per mutable/current concern;
- LLM prose/drafts/Story do not become canon by generation or persistence;
- deterministic core owns accepted execution;
- recovery cannot depend on hidden LLM thought/context memory;
- objective truth, fictional knowledge, human disclosure, communication evidence and Story remain distinct;
- host chat history mutation does not rewrite accepted campaign history;
- semantic continuity is stronger than universal verbatim retention;
- exactness survives only through explicit protection/natural-owner/archive semantics;
- Story may lag/fail without blocking gameplay/recovery;
- no universal frontier/snapshot/history clock is introduced.

---

## 6. Source Manifest

### 6.1 Process / sequencing

| Source | Role | Required inspection |
|---|---|---|
| `AGENTS.md` | repository governance | documentation/source/transport rules |
| `DEV/DESIGN_PROCESS.md` | canonical process | evidence/synthesis and decision gates |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | HDM process adapter | Round-1 preservation and item-level evidence rules |
| `DEV/PROJECT_MAP.md` | derivative locator | R2.1 dependency subgraph |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | current sequencing authority | R2.1 scope/exit and downstream dependencies |
| `2026-08-24-round-2-roadmap-owner-decision.md` | owner decision | approved program decomposition |
| `2026-08-24-round-2-evidence-disposition-ledger.md` | research synthesis | active/inherited/dormant candidate routing |

### 6.2 Canonical owning architecture

| Source | Why required |
|---|---|
| Step-3 deterministic execution canonical spec | inherited proposer/validator/commit boundary |
| Step-4 truth/knowledge/role-context/Story canonical spec | authority geometry and derived/noncanonical boundaries |
| Step-4 single-context amendment | current role-containment law; prevents stale physical-isolation assumptions |
| Step-5.10 Story projection canonical spec | Story/Chronicler projection semantics, lag, source coverage |
| Step-5.11 Transcript/history retention canonical spec + selective-exact owner decision | exact vs semantic memory contract, compaction/protection |
| Step-5.12 delivery/disclosure canonical spec | host Retry/Edit non-rewind and outbound history/disclosure boundary |
| Step-5.14 integrated closure | recovery/currentness/chronology constraints affecting history-aligned derived state |

Open the owning primary specifications rather than relying on the canonical index when a conclusion depends on exact wording.

### 6.3 Research inputs

Primary active Dossier candidates:

- D01 — layered continuity;
- D05 — mutable recent horizon;
- D06 — history-aligned derived state;
- D07 — broad summary vs episodic retrieval;
- D08 — entity-local continuity;
- D09 — evidence-bound derived mutation delta;
- D18 — long-range archive retrieval / selective exact;
- S03 — evidence trust/provenance;
- S04 — semantic dedup across continuity channels;
- S19 — reviewable/validated summary transformation;
- S27 — bounded one-mutation assessment.

Relevant negative/adversarial Dossier evidence must be inspected during research, especially failure modes involving:

- unverified summaries;
- durable memory every turn;
- duplicate state/authority;
- invented missing details;
- whole-history preload;
- host Retry without accepted-history distinction.

### 6.4 Current runtime neighbors

Inspect as needed to determine existing responsibility rather than to preserve implementation by inertia:

- `GAME/CORE/SESSION.md`;
- `GAME/CORE/AI_REASONING.md`;
- `GAME/CORE/NPC.md` only where continuity ownership overlaps R2.1 rather than R2.2;
- Story/history/persistence runtime contracts located through `DEV/PROJECT_MAP.md`.

Machine schemas/tests are downstream unless a current machine contract already owns semantics that would contradict a proposed R2.1 architecture. Search/fetch them when such a dependency appears.

---

## 7. Required evidence ledger for R2.1

Before a Decision Brief, create an inspectable R2.1 evidence ledger containing, for every material source item:

```text
Source/item
Actual claim
Authority/classification
Qualifier/applicability
Existing owner
Conflict / extension / new consumer / no delta
Candidate disposition
Reason
Downstream consumer(s)
```

For Dossier items, preserve the difference between:

- current requirement;
- simplest candidate form;
- risk/counterargument;
- revisit/defer condition.

---

## 8. Analytical challenges that must be answered

At minimum challenge the design against:

1. **Duplicate authority** — can summary/memory disagree with current owners without becoming a hidden winner?
2. **False durability** — can one mistaken summary reinforce itself across future consolidations?
3. **History contamination** — can rejected/edit-displaced history survive in derived continuity?
4. **Repair cost** — can stale derived products be detected/rebuilt without global scans?
5. **Exactness inflation** — does semantic memory accidentally promise quotes it cannot prove?
6. **Layer explosion** — are several proposed layers solving the same consumer need?
7. **Actor leakage** — does R2.1 preempt R2.2 by embedding private cognition semantics in generic memory?
8. **Context leakage** — does R2.1 dictate ranking/budgets that belong in R2.3?
9. **Operational bureaucracy** — does consolidation require background workers, timers or queues that current product baseline does not provide?
10. **Recovery** — after total host/context loss, can derived continuity be reconstructed or safely degraded from durable HDM-owned evidence?

---

## 9. Candidate alternatives to compare

The research/Decision Brief must compare at least:

### A. Minimal continuity

```text
authoritative state/history
+ recent exact evidence
+ one broad derived summary
```

Add episodic/entity products only after demonstrated need.

### B. Layered derived continuity

```text
broad summary
+ episodic records
+ entity-local continuity
+ selective exact/deep archive access
```

All derived, provenance-bound and rebuildable where possible.

### C. Event/archive-first retrieval

Keep little/no durable semantic memory beyond canonical/history owners; retrieve and synthesize on demand.

The analysis may produce a hybrid or a simpler alternative, but it must not assume the Dossier's proposed layer set is automatically correct.

---

## 10. Exit criteria

R2.1 may close only when the canonical design defines:

- admitted continuity classes and rejected alternatives;
- owner/authority/lifecycle for each class;
- source/provenance/coverage requirements;
- stability/consolidation semantics;
- history/branch alignment;
- stale/conflict/repair/rebuild/retirement behavior;
- semantic versus exact recall promises;
- relationship to Story/Chronicler and Step-5 exact history;
- bounded mutation/validation semantics where generative transformation is used;
- explicit downstream contracts handed to R2.2 and R2.3;
- no duplicate semantic authority;
- adversarial review closure;
- unresolved work explicitly owned/deferred/dormant/debt.

---

## 11. Current continuation point

```text
R2.1 status: IN PROGRESS
task brief: established
next activity: source extraction / R2.1 evidence ledger
```

No R2.1 architecture alternative is selected by this task brief.
