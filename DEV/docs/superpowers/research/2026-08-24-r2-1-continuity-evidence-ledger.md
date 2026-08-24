# R2.1 Continuity / Memory / History Alignment — Evidence Ledger

Status: **RESEARCH EVIDENCE / PRE-DECISION SYNTHESIS**

Date: 2026-08-24

Task brief:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-memory-history-task-brief.md`

This artifact records source-derived claims, qualifiers and architectural deltas for R2.1. It is not a canonical design.

---

## 1. Established canonical constraints

### C01 — Current state remains with natural owners

Source: Step-4 canonical specification.

Actual claim:

- ordinary current world state remains with its existing Actor/Asset/Effect/Condition/Scene/etc. owners;
- `world.lore_fact` is not a universal copy of current state;
- helper/projection records do not gain current-state authority merely by being easier for an LLM to read.

R2.1 consequence:

> A continuity summary must not become a writable current-state cache that competes with natural owners.

Current interpretation: **BOUNDARY / NON-NEGOTIABLE**.

---

### C02 — `world.knowledge` is current fictional epistemic authority

Source: Step-4 canonical specification.

Actual claim:

- material current subject-to-proposition epistemic state is owned by `world.knowledge`;
- full transition history belongs to LOG/SemanticEvents;
- derived indexes may support bounded retrieval but do not become writable authority.

R2.1 consequence:

> Generic continuity must not create a second NPC/PC knowledge store.

Current interpretation: **BOUNDARY / NON-NEGOTIABLE**.

---

### C03 — Story is durable but noncanonical

Sources: Step-4 canonical specification; Step-5.10 Story projection specification.

Actual claim:

- Story is a durable presentation/history projection;
- Story may lag, fail, restart, be corrected or be partially absent without changing gameplay truth or recovery authority;
- Chronicler transforms occurred evidence, while deterministic control owns final validation/publication/coverage;
- Story records carry source refs and entity refs useful to traceability/retrieval.

R2.1 consequence:

> Story is already an admitted durable derived historical projection. A new generic “memory” store must justify why Story plus existing historical owners cannot satisfy the consumer.

Current interpretation: **STRONG REUSE CANDIDATE**, not yet approved as a gameplay-role continuity source.

---

### C04 — Story records cannot replace source authority

Sources: Step 4; Step 5.10.

Actual claim:

- Story content/indexes/coverage do not become gameplay semantic authority;
- unsupported literary inference cannot be restated as factual history;
- Story-to-Story references do not promote prose into fact authority.

R2.1 consequence:

> If Story is admitted as gameplay continuity input, it may orient/retrieve but cannot be the sole correctness-critical evidence when an owning source exists.

Current interpretation: **BOUNDARY / NON-NEGOTIABLE**.

---

### C05 — Story source coverage already has generation-aware projection semantics

Source: Step-5.10.

Actual claim:

- Story projection state tracks typed source-domain coverage;
- semantic projection-contract generation determines compatibility;
- model/prompt version is not itself coverage generation;
- incompatible semantic generation movement requires migration/reprojection/reset rather than silent reuse.

R2.1 consequence:

> R2.1 should reuse this pattern where durable derived projections need source coverage rather than inventing a second generic ancestry/version system.

Current interpretation: **REUSE PRINCIPLE**.

---

### C06 — Semantic continuity is the product promise; verbatim is selective

Sources: Step-5.11 owner decision and canonical specification.

Actual claim:

- HDM promises strong durable semantic continuity of materially established campaign history;
- HDM does not promise permanent verbatim retention of arbitrary conversation;
- exact wording is separately protected where semantics/policy require it;
- if exact wording is gone, HDM must state that and use strongest surviving semantic evidence rather than fabricate a quote.

R2.1 consequence:

> Any continuity architecture must optimize for semantic survival without silently upgrading the exact-history promise.

Current interpretation: **PRODUCT LAW**.

---

### C07 — Host conversation history is not accepted campaign history authority

Sources: Step-5.11; Step-5.12.

Actual claim:

- host Retry/regeneration/edit/branch/delete does not rewrite accepted Interaction/message/canonical history;
- old host controls do not rerun accepted mechanics/RNG or rewind disclosure;
- current campaign authority comes from HDM storage/routing.

R2.1 consequence:

> D05/D06 cannot be implemented as “wait until the ChatGPT branch is stable.” The relevant boundary is HDM source acceptance/compatibility, not host UI age/ancestry.

Current interpretation: **MATERIAL CORRECTION TO RESEARCH FORMULATION**.

---

### C08 — Accepted history sources already have stable identity after payload compaction

Source: Step-5.11.

Actual claim:

- `runtime.message` retains stable historical identity even after exact payload compaction;
- semantic consumers must become content-sufficient before payload loss;
- exact text may be protected at whole-payload/slice/natural-owner scope;
- source enumeration remains interpretable after lawful compaction.

R2.1 consequence:

> A continuity projection can survive loss of raw prose if its semantic claim is already discharged into proper owners/history evidence.

Current interpretation: **REUSE FOUNDATION**.

---

### C09 — Recovery may not depend on hidden model/context memory

Sources: Step 3; Step 4; Step 5.14.

Actual claim:

- recovery resumes from HDM-owned accepted/durable evidence;
- hidden LLM thought/prior context is never required recovery state.

R2.1 consequence:

> Any durable continuity needed after context loss must be recoverable from HDM-owned sources or be safely disposable/rebuildable.

Current interpretation: **BOUNDARY / NON-NEGOTIABLE**.

---

### C10 — Context Assembler is downstream projection, not storage authority

Source: Step 4 + single-context amendment.

Actual claim:

- RoleContextBundle is a logical execution projection;
- Context Assembler selects bounded eligible sources;
- source eligibility is role/subject/player/purpose-specific;
- physical co-presence does not widen logical eligibility.

R2.1 consequence:

> R2.1 should define source/lifecycle semantics only. Ranking, placement, budget and final bundle construction remain R2.3.

Current interpretation: **STAGE BOUNDARY**.

---

### C11 — Current runtime already expects compact semantic recap from durable state

Source: `GAME/CORE/SESSION.md`.

Actual claim:

- session/new-chat resume does not begin by rereading old chat history;
- a compact recap may be generated from canonical state when useful;
- when exact current-chat evidence is unavailable, durable state/event evidence supports a semantic summary;
- exact quotes may not be fabricated from semantic evidence.

R2.1 consequence:

> Ephemeral recap generation is already a valid continuity mechanism and need not imply a durable “global memory” record.

Current interpretation: **REUSE CANDIDATE**.

---

### C12 — Current runtime already forbids whole-history preload

Source: `GAME/CORE/AI_REASONING.md`.

Actual claim:

- retrieve the smallest authoritative working set needed;
- do not preload WORLD/LOG/index/entity data wholesale;
- compression preserves hard facts, unresolved obligations and causal links rather than ornamental prose.

R2.1 consequence:

> Long-range continuity must support bounded retrieval/projection rather than “keep all history in context.”

Current interpretation: **BOUNDARY / HANDOFF TO R2.3**.

---

## 2. Active research candidates

### D01 — Layered continuity

Research claim:

- authoritative state, broad summary, episodic recall, recent exact evidence, entity-local continuity, private actor continuity and transient scene state solve different problems;
- simplest proposed starting point is authoritative state + recent exact history + broad summary + episodic retrieval;
- risk is layer synchronization/maintenance/priority ambiguity.

Canonical reconciliation:

- authoritative state and recent/exact history already have owners;
- Story already supplies a durable derived history/presentation layer;
- Actor-private continuity belongs downstream to R2.2;
- transient scene/context belongs downstream to current working set/R2.3.

Current R2.1 interpretation:

> Treat “layers” first as **semantic continuity source classes**, not as permission to create one durable store per class.

Disposition inside R2.1: **ACTIVE — REUSE-FIRST**.

---

### D05 — Mutable recent horizon

Research claim:

- do not consolidate retry/edit-sensitive fresh text into durable summaries too early.

Canonical reconciliation:

- host Retry/Edit cannot rewrite accepted HDM history;
- generated/unaccepted/rejected candidate text is not admitted history;
- accepted messages/events already have stable HDM identity.

Current R2.1 interpretation:

> Replace “mutable UI horizon” with an **accepted-source boundary**: only admitted HDM evidence may feed durable derived projections. No age-based or host-branch stability timer is required.

Remaining delta:

- define whether some accepted sources still need a semantic-discharge/coverage condition before a derived projection may claim them as summarized.

Disposition: **ACTIVE — FORMULATION CHANGED**.

---

### D06 — History-aligned derived state

Research claim:

- history-dependent derived state must follow branch/ancestry to avoid contamination from rejected history;
- risk is accidentally treating UI history tree as canonical chronology.

Canonical reconciliation:

- host branch/edit history is explicitly non-authoritative;
- HDM history sources have stable IDs/current owner transitions;
- Story projection already uses source-domain coverage + semantic contract generation.

Current R2.1 interpretation:

> Align derived continuity to **HDM-owned source refs/current source compatibility**, not ChatGPT conversation ancestry. No generic history-node tree is justified for baseline.

Remaining delta:

- specify stale/incompatible source detection and source-correction/supersession behavior for derived projections.

Disposition: **ACTIVE — NARROWED**.

---

### D07 — Broad summary versus episodic retrieval

Research claim:

- broad campaign orientation and specific old-event recall are different needs.

Canonical reconciliation:

- Story/NARRATIVE + chapter synopsis already form a broad narrative projection;
- Story/EVENTS, TRANSCRIPT, runtime.message and SemanticEvents provide episodic/history evidence;
- Story may lag/omit and therefore cannot become correctness-critical.

Current R2.1 interpretation:

> Reuse existing Story/history sources before inventing a separate global-summary and episodic-memory subsystem.

Open decision:

- whether gameplay logical roles may consume eligible Story as derived orientation/retrieval acceleration.

Disposition: **ACTIVE — OWNER DECISION NEEDED**.

---

### D08 — Per-entity continuity

Research claim:

- returning entity continuity benefits from entity-local history and compact older representation;
- risk is many derived artifacts and divergence from global summary.

Canonical reconciliation:

- Story records already carry `entity_refs`;
- current entity state remains in natural owners;
- NPC detailed private continuity is R2.2.

Current R2.1 interpretation:

> Start with **entity-scoped retrieval/view over existing owners + history/Story refs**, not a new durable per-entity memory record.

Trigger for a stored entity synopsis:

- R2.3 evidence shows repeated bounded retrieval cannot meet latency/context/quality needs without one.

Disposition: **ACTIVE — MINIMAL VIEW FIRST**.

---

### D09 — Evidence-bound durable mutation

Research claim:

- LLM may propose bounded mutation from fresh evidence; deterministic validator checks membership/ownership/current revision/shape before commit.

Canonical reconciliation:

- general proposal-versus-authoritative-commit rule is already Step 3;
- semantic correctness of a generated summary cannot be fully proven by structural validation.

Current R2.1 interpretation:

> For derived continuity, deterministic control must validate source identity/eligibility/coverage/shape and must never promote the derived text into canon. Semantic-quality errors remain repairable projection defects, not canonical truth.

Disposition: **ACTIVE DELTA — SPECIALIZED APPLICATION ONLY**.

---

### D18 — Long-range archive retrieval + selective exact

Research claim:

- coarse selection plus exact source lookup improves deep recall;
- exact archive is a separate evidence source;
- coarse selector requires fallback.

Canonical reconciliation:

- Step 5.11 already defines selective exact retention and verified Transcript exactness;
- Story/chapters/entity refs can provide coarse semantic routing;
- R2.3 owns retrieval algorithms/budgets.

Current R2.1 interpretation:

> R2.1 defines the **recall promise/source classes**; R2.3 later decides two-stage retrieval policy. Exact recall must terminate at retained exact evidence, never generated reconstruction.

Disposition: **ACTIVE — SPLIT BETWEEN R2.1 AND R2.3**.

---

### S03 — Source trust/provenance

Research claim:

- different evidence sources should not support automatic mutation equally;
- risk is an overgrown provenance lattice.

Canonical reconciliation:

- HDM already has source-specific authority semantics rather than one universal trust score.

Current R2.1 interpretation:

> Do not add a scalar/global trust lattice. Determine validity by **claim type + owning source contract**. Story, message, semantic event and current owner each prove different things.

Disposition: **ACTIVE — NARROW CLAIM-TYPED PROVENANCE**.

---

### S04 — Semantic dedup across continuity channels

Research claim:

- do not send one fact repeatedly via multiple memory channels;
- risk is collapsing distinct similar facts.

Current R2.1 interpretation:

- avoid duplicate stored continuity channels where possible;
- stable source refs/coverage should enable deterministic/source-aware dedup;
- semantic ranking/dedup algorithm is R2.3.

Disposition: **ACTIVE — ARCHITECTURAL GUARDRAIL**.

---

### S19 — Reviewable summarization transformation

Research claim:

- high-value summary may be generated as candidate and reviewed/validated before promotion;
- human review cannot be mandatory gameplay work.

Canonical reconciliation:

- Story projection already separates Chronicler draft from deterministic publication;
- semantic summary quality cannot be made canonical by review mechanics.

Current R2.1 interpretation:

> Keep generated summaries non-authoritative. Structural/source validation is mandatory; human review is optional tooling; factual gameplay decisions must remain traceable to stronger owners.

Disposition: **ACTIVE DELTA — REUSE STORY-LIKE TRANSFORMATION MODEL**.

---

### S27 — One durable mutation per semantic assessment

Research claim:

- one assessment commits at most one bounded mutation;
- risk is update backlog.

R2.1 analysis:

- for non-authoritative projection catch-up, a bounded source window may legitimately yield several coherent derived records in one publication;
- Step-5.10 already allows coherent multi-record Story transactions;
- “one mutation” is not required for correctness if the whole derived write set is bounded and source-traceable.

Current interpretation:

> Reject as a universal R2.1 rule. Preserve as a possible R2.2 cognition-specific simplification if one-Actor assessment semantics benefit from it.

Disposition: **RESOLVED IN R2.1 — NOT ADOPTED GENERICALLY / DOWNSTREAM POSSIBILITY**.

---

## 3. Relevant negative evidence

### N01 — Unverified summary amplification

Dossier failure pattern:

- automatic summary without provenance/verification can amplify one error repeatedly.

R2.1 guardrail:

> Derived summaries must be source-bound, non-authoritative and safely excludable/rebuildable. They may not recursively become stronger evidence merely because later summaries copied them.

---

### N02 — Durable memory every turn

Dossier failure pattern:

- creating long-term memory every turn creates noise and context capture.

R2.1 guardrail:

> No per-turn durable memory obligation. Projection/summary work is selective and may lag/defer.

---

### N03 — Duplicate state

Dossier failure pattern:

- internal object plus editable text card creates ambiguous authority.

R2.1 guardrail:

> Current truth never lives in continuity projection; current owners win without reconciliation vote.

---

### N04 — Invent missing details

Dossier failure pattern:

- LLM fills unknowns and continuity later treats them as facts.

R2.1 guardrail:

> Derived continuity may summarize only admitted source evidence. `unknown`/insufficient evidence remains representable; invention does not become history.

---

### N05 — Whole-history preload

Existing runtime/negative evidence:

- archive and working context are different products.

R2.1 guardrail:

> Durable history may be deep; working role context remains bounded and is constructed later by R2.3.

---

## 4. Emerging synthesis

The evidence does **not** currently justify a new generic `memory` semantic owner.

A lower-complexity architecture can distinguish:

```text
1. CURRENT AUTHORITATIVE SOURCES
   natural world/runtime owners
   authoritative for current truth/state/cognition/disclosure

2. ACCEPTED HISTORICAL EVIDENCE
   runtime.message / Interaction / SemanticEvent / MechanicalEvent /
   chronology and other admitted historical owners
   authoritative for their own occurrence/evidence semantics

3. STORY
   durable, source-bound, noncanonical historical/presentation projection
   potentially reusable as broad/episodic continuity orientation

4. TRANSIENT WORKING CONTINUITY
   current chat/session/turn working set and generated recap
   disposable; not durable authority

5. SELECTIVE EXACT EVIDENCE
   exact message/slice/natural owner/verified Transcript only where Step 5.11 protects it

6. OPTIONAL FUTURE DERIVED VIEWS
   entity synopsis or other cached continuity projection only after a concrete
   downstream consumer proves that existing owners + Story/history retrieval are insufficient
```

The key distinction is:

> **continuity class != new storage authority**

---

## 5. Proposed history-alignment law

A durable derived continuity product, if admitted, should align to HDM sources through:

```text
stable source refs / source-domain coverage
+ source-specific current/supersession semantics where material
+ semantic projection-contract generation
```

It should **not** align through:

```text
host chat cursor
host message age
ChatGPT retry/edit branch ancestry
wall-clock age
LLM memory state
```

If a projection's source basis becomes incompatible/unknown:

```text
exclude/degrade projection
-> fall back to stronger source evidence
-> rebuild/repair when useful
```

Do not guess reconciliation.

---

## 6. Proposed authority law for derived continuity

No universal scalar “source trust” ordering is sufficient because sources prove different claim classes.

Examples:

```text
current HP
    -> Actor/current-state owner

what NPC currently believes
    -> world.knowledge

what was said
    -> retained runtime.message / accepted communication evidence

whether what was said was objectively true
    -> world/lore owner

what broad arc occurred
    -> Story may summarize/orient, source refs remain factual spine
```

Therefore:

> Derived continuity chooses source authority by the semantic question being answered, not by one global confidence score.

---

## 7. Open architectural decision after source extraction

One material component-boundary choice remains:

> **May eligible Story be admitted as a gameplay-role continuity/orientation source, while remaining non-authoritative and never the sole correctness-critical evidence?**

This choice determines whether R2.1 can reuse the already-designed Story projection for broad/episodic continuity or must create a separate gameplay-memory projection family.

The next artifact is the R2.1 Decision Brief comparing the credible alternatives.
