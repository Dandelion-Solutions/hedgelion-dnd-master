# R2.1 Decision Brief — Continuity Projection Architecture

Status: **DECISION BRIEF / OWNER DECISION REQUIRED**

Date: 2026-08-24

Task brief:

- `DEV/docs/superpowers/design/2026-08-24-r2-1-continuity-memory-history-task-brief.md`

Evidence ledger:

- `DEV/docs/superpowers/design/2026-08-24-r2-1-continuity-evidence-ledger.md`

This brief follows source extraction. It does not canonicalize an architecture until the owner decides.

---

## 1. Decision to make

R2.1 needs one material component-boundary decision:

> **What durable derived continuity surface should ordinary gameplay roles use for broad/episodic long-campaign memory?**

The choice must preserve:

- natural current-state owners;
- Step-4 `world.knowledge` and `runtime.disclosure`;
- Story nonauthority;
- Step-5 semantic-continuity/selective-exact product promise;
- host Retry/Edit non-rewind;
- recovery without hidden model/context memory;
- bounded context/retrieval;
- no background-worker correctness dependency.

---

## 2. Facts established before the decision

### F1 — A new current-state/memory authority is unnecessary and unsafe

Current state, knowledge, disclosure, accepted interaction/history and exact-retention semantics already have owners.

The missing problem is **derived orientation/recall**, not authoritative memory.

### F2 — Story already is a durable source-bound derived history projection

Story already provides:

- NARRATIVE;
- EVENTS;
- TRANSCRIPT;
- MECHANICS;
- source refs;
- entity refs;
- layer-local projection coverage;
- semantic contract generation;
- deterministic publication control;
- optional/lagging Chronicler transformation.

It was originally designed primarily as presentation/history/Commentator surface, not as the ordinary gameplay-role memory source.

### F3 — Host history cannot define the consolidation/branch model

Accepted HDM history does not rewind because ChatGPT Retry/Edit/branch controls change.

Therefore D05/D06 must align to HDM-owned accepted sources and source compatibility rather than UI age or conversation ancestry.

### F4 — Exact-history behavior is already product-decided

R2.1 cannot turn semantic continuity into universal verbatim recall.

Exact answers terminate at protected exact evidence; otherwise the engine uses strongest surviving semantic evidence and says exact wording is not retained.

### F5 — Current runtime already permits ephemeral recap from durable sources

A new chat/session may construct a compact semantic recap without making that recap a new authority.

---

## 3. Alternative A — Dedicated layered continuity subsystem

Introduce a new durable gameplay-oriented derived family, conceptually:

```text
continuity.summary
continuity.episode
continuity.entity_view
possibly continuity indexes/coverage
```

Story remains presentation/history only.

### Advantages

- clean purpose-specific semantics for gameplay memory;
- can optimize structure independently from literary Story;
- private/role-oriented derived content does not need to share Story's spectator availability model;
- easy to describe broad/episodic/entity layers explicitly.

### Costs / risks

- duplicates much of Story's projection, source-ref, coverage and entity-index responsibility;
- creates another Chronicler-like transformation/maintenance path;
- increases risk that “gameplay memory” becomes de facto current truth because it is closer to hot reasoning;
- requires new durability/repair/versioning rules already solved in analogous form by Step 5.10;
- raises migration/schema/catalog/runtime obligations before a concrete consumer proves Story/history reuse insufficient;
- likely creates the layer-synchronization problem D01 itself warns about.

### Assessment

Technically viable but **not justified by current evidence**.

---

## 4. Alternative B — Reuse-first continuity projections — RECOMMENDED

Treat continuity as a semantic source taxonomy over existing owners.

Baseline:

```text
CURRENT AUTHORITATIVE SOURCES
    natural world/runtime owners

ACCEPTED HISTORICAL EVIDENCE
    Interaction / runtime.message / SemanticEvent /
    MechanicalEvent / chronology / other admitted history

STORY
    durable noncanonical broad/episodic historical projection
    eligible as orientation/retrieval acceleration under strict source/role rules

TRANSIENT WORKING CONTINUITY
    current working set / generated recap
    disposable

SELECTIVE EXACT EVIDENCE
    Step-5.11 protected message/slice/natural owner/
    verified Transcript when available

OPTIONAL FUTURE DERIVED VIEWS
    admitted only when a concrete downstream consumer proves the need
```

No new generic `memory` record/class/subsystem is created in R2.1.

### Story gameplay-use rule

An eligible Story unit may be included for a gameplay logical role only as **derived continuity orientation**.

It SHALL NOT:

- widen information eligibility beyond its underlying material sources;
- override a current owner;
- establish current Actor cognition;
- establish objective truth;
- be the sole correctness-critical evidence for a decision when a stronger owning/historical source is required;
- recursively amplify an unsupported Story inference into stronger factual evidence.

For factual/decision-critical use:

```text
Story hint/orientation
    -> underlying source refs / current owners as required
    -> validated decision input
```

R2.3 decides the exact retrieval/selection/budget mechanism.

### Entity continuity rule

Baseline per-entity continuity is an entity-scoped retrieval/view over:

- current entity owner;
- relevant historical evidence;
- eligible Story records/entity refs.

Do not add a stored entity synopsis until measured R2.3 evidence shows this cannot meet bounded latency/context/quality needs.

### Advantages

- reuses an already accepted durable derived projection rather than building a parallel memory plane;
- preserves one-owner discipline;
- reuses source refs, projection coverage and semantic contract generation;
- broad narrative continuity and episodic retrieval already have natural Story/history surfaces;
- Story may lag/fail, so correctness naturally remains anchored in stronger owners;
- lowest new persistence/migration/maintenance complexity;
- compatible with eventual R2.3 two-stage retrieval.

### Costs / risks

- expands Story from presentation/history into an additional **consumer role** for gameplay continuity;
- Story's existing availability model was designed around Commentator/spectator use, so R2.3 must not equate Commentator availability with gameplay role eligibility;
- Story prose may contain editorial compression/inference, requiring fallback to underlying sources for correctness-critical decisions;
- if Story is badly lagging/absent, gameplay may pay extra retrieval/synthesis cost even though correctness remains available.

### Assessment

Best fit to current HDM ownership and YAGNI constraints.

---

## 5. Alternative C — No durable gameplay continuity projection

Keep Story spectator/history-oriented only.

Gameplay roles use:

```text
current owners
+ accepted event/message history
+ selective exact archive
+ ephemeral on-demand recap/synthesis
```

No durable gameplay-oriented summary is reused or added.

### Advantages

- smallest semantic surface;
- no Story consumer expansion;
- no risk of old derived prose entering ordinary gameplay reasoning;
- all gameplay facts come from owning/history sources.

### Costs / risks

- repeated long-range synthesis work after context loss/new chat;
- more expensive context/retrieval path for broad campaign orientation;
- likely recreates summaries ephemerally many times;
- underuses existing Story/NARRATIVE/EVENTS/entity refs;
- weaker long-campaign narrative coherence when exact relevant event retrieval misses the broad arc;
- pushes more complexity and token pressure into R2.3.

### Assessment

Correct but likely unnecessarily expensive and lower quality.

---

## 6. Recommendation

Select **Alternative B — Reuse-first continuity projections**.

Confidence: **HIGH**.

Reason:

> The unresolved requirement is not “where can HDM store another memory?” but “how can a long-running LLM recover broad and specific continuity without confusing projections with authority?”

HDM already possesses the necessary durable truth/history and a durable noncanonical Story projection with source traceability.

Adding a parallel gameplay-memory persistence family now creates more synchronization risk than value.

---

## 7. Proposed R2.1 laws if Alternative B is approved

### R2.1-L1 — CONTINUITY IS NOT A NEW AUTHORITY

No generic `memory` or `continuity` owner is introduced.

Continuity classes describe source/lifecycle roles, not new truth ownership.

### R2.1-L2 — CURRENT OWNERS ALWAYS WIN CURRENT QUESTIONS

A derived continuity projection cannot override current world/runtime/knowledge/disclosure owners.

No reconciliation vote between summary and current state exists.

### R2.1-L3 — STORY MAY SERVE AS DERIVED GAMEPLAY CONTINUITY

Eligible Story may orient gameplay roles and help route long-range recall.

Story remains durable, noncanonical and optional/lagging.

### R2.1-L4 — DERIVED CONTINUITY DOES NOT WIDEN ELIGIBILITY

A projection may be used by a role only when its material content is eligible for that role.

Physical/storage availability and Story availability do not automatically imply gameplay role eligibility.

R2.3 owns concrete filtering/selection.

### R2.1-L5 — DECISION-CRITICAL CLAIMS RETURN TO THE PROPER SOURCE CLASS

Story may suggest what historical/current evidence to load.

Where correctness depends on a fact, exact wording, current cognition or current state, use the owning source required by that semantic question.

### R2.1-L6 — HISTORY ALIGNMENT USES HDM SOURCES, NOT HOST ANCESTRY

Durable derived projections align through stable source refs/source-domain coverage, source-specific correction/supersession semantics and semantic projection-contract generation.

ChatGPT Retry/Edit/branch ancestry is not the alignment key.

### R2.1-L7 — ONLY ADMITTED HDM EVIDENCE MAY ENTER DURABLE CONTINUITY

Rejected generations, hidden chain-of-thought, abandoned Narrator drafts and other non-admitted host/model material do not enter durable continuity merely because they were physically generated.

No time-based “recent mutable horizon” is required for baseline correctness.

### R2.1-L8 — STALE OR INCOMPATIBLE PROJECTION FAILS OPEN TO STRONGER EVIDENCE, NOT TO GUESSING

If projection compatibility cannot be proven:

```text
exclude/degrade it
-> retrieve stronger current/historical sources
-> rebuild/repair later if useful
```

Story failure/lag cannot block gameplay correctness.

### R2.1-L9 — NO FACTUAL SELF-AMPLIFICATION THROUGH DERIVED TEXT

A new derived summary may use prior Story for editorial continuity, but factual support must remain traceable to admitted underlying source refs.

Repeated summarization does not increase factual authority/confidence.

### R2.1-L10 — PER-ENTITY CONTINUITY STARTS AS A VIEW

Entity-local continuity initially composes current owner + bounded historical/Story retrieval.

A durable entity synopsis requires a later demonstrated consumer/performance need.

### R2.1-L11 — EXACT RECALL REMAINS STEP-5.11 SELECTIVE EXACT

No R2.1 projection may fabricate exact wording.

If exact evidence no longer survives, return semantic evidence with the existing product limitation.

### R2.1-L12 — NO PER-TURN OR BACKGROUND MAINTENANCE REQUIREMENT

Derived continuity may lag, defer or be rebuilt.

No heartbeat, queue, timer or autonomous worker is needed for baseline correctness.

---

## 8. Consequences for downstream stages

### R2.2 Actor continuity

Receives a clean boundary:

- Actor current/private cognition must have proper owners;
- generic continuity/Story cannot become Actor cognition merely by mentioning it.

### R2.3 Context Runtime

Must design:

- Story/history candidate eligibility;
- role-specific projection filtering;
- broad -> episodic/exact source routing;
- complete decision packet fallback;
- dedup;
- entity-scoped retrieval;
- stale projection exclusion;
- context trace.

### R2.4 LLM execution

May use Story/recap as derived input but cannot treat it as authority or persist hidden reasoning through continuity.

### R2.5 multiplayer

Recipient/Actor scope applies equally to derived continuity: one Story/canon repository does not imply one identical role/player projection.

---

## 9. Deferred / rejected within R2.1

If Alternative B is approved:

- **dedicated generic memory subsystem:** rejected for current scope;
- **durable per-entity synopsis:** conditional on R2.3 evidence;
- **host-history stability timer:** rejected;
- **generic history-node/ancestry tree based on ChatGPT UI:** rejected;
- **global scalar evidence trust score:** rejected;
- **one durable mutation per summary assessment:** not adopted as generic rule; may be reconsidered for R2.2 cognition;
- **background summarization worker:** not required;
- **universal exact transcript:** rejected by existing owner decision.

---

## 10. Exact owner decision requested

Choose one:

```text
A — Dedicated layered continuity subsystem
B — Reuse-first Story/history continuity projections  [RECOMMENDED]
C — No durable gameplay continuity projection; on-demand synthesis only
```

Approval of **B** also approves the proposed R2.1-L1 through R2.1-L12 direction for candidate-spec formalization.

It does not approve R2.3 retrieval algorithms, concrete schemas or implementation.
