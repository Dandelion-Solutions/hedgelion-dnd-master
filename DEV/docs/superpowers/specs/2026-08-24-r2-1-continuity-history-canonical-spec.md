# R2.1 Canonical Specification — Continuity, Memory and History-Aligned Derived State

Status: **CANONICAL ARCHITECTURE — R2.1**

Date: 2026-08-24

Owner decision:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-projection-owner-decision.md`

Derivation:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-memory-history-task-brief.md`
- `DEV/docs/superpowers/design/2026-08-24-r2-1-continuity-evidence-ledger.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-projection-decision-brief.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-adversarial-review.md`

This specification incorporates adversarial clarifications AR-1 through AR-3. It defines architecture only; implementation remains deferred.

---

# 1. Canonical invariant

HDM long-campaign continuity is a **typed source/lifecycle model over existing semantic owners and non-authoritative projections**.

R2.1 introduces no generic memory authority.

```text
CURRENT AUTHORITATIVE SOURCES
    natural world/runtime owners
    world.lore_fact where applicable
    world.knowledge
    runtime.disclosure

ACCEPTED HISTORICAL EVIDENCE
    runtime.interaction / runtime.message
    SemanticEvent / MechanicalEvent / receipts
    chronology and other admitted owner-specific history

DERIVED DURABLE CONTINUITY
    STORY/*
    source-bound, optional/lagging, noncanonical
    eligible gameplay roles may consume it as orientation

TRANSIENT WORKING CONTINUITY
    loaded working set / generated recap / turn-session synthesis
    disposable and non-authoritative

SELECTIVE EXACT EVIDENCE
    Step-5.11 protected exact source / natural exact owner /
    verified exact Transcript where applicable

OPTIONAL FUTURE DERIVED VIEWS
    not admitted by baseline
    require a concrete downstream need and architecture approval
```

Core rule:

> **Continuity may help a role recover what matters; it never decides what is true, current, known, disclosed, exact, or mechanically established.**

---

# 2. Continuity classes and lifecycles

## 2.1 Current authoritative sources

Native world/runtime/knowledge/disclosure owners remain authoritative within their existing contracts.

Continuity machinery SHALL NOT maintain a parallel writable copy of current state for LLM convenience.

## 2.2 Accepted historical evidence

Interaction/message/event/receipt/chronology and other owner-specific historical sources remain authoritative only for the evidence semantics they own.

Historical evidence is not automatically current-state authority.

## 2.3 Story

Story remains:

- durable;
- noncanonical;
- source-bound;
- optional/lagging;
- repairable according to surviving source evidence;
- unable to block gameplay/recovery merely because it is stale, missing or defective.

R2.1 adds one permitted consumer edge:

> **eligible gameplay logical roles may use eligible Story as broad/episodic continuity orientation and as routing evidence toward stronger sources.**

Story gains no new authority.

## 2.4 Transient working continuity

Generated recap, loaded working set and current turn/session synthesis are disposable working products.

They may be rebuilt from HDM-owned evidence and SHALL NOT become recovery authority merely because they improve local quality.

## 2.5 Selective exact evidence

Exact recall remains governed by Step 5.11 and natural exact-content owners.

R2.1 does not widen the verbatim-retention product promise.

## 2.6 Optional future derived views

A stored entity synopsis or other new derived continuity family is not admitted by this specification.

Admission requires a demonstrated consumer, explicit lifecycle/source/repair contract and proof that the new view does not create duplicate authority.

---

# 3. Canonical laws

## LAW R2.1-1 — NO NEW MEMORY AUTHORITY

No generic `memory`, `continuity`, `episode_memory`, `entity_memory` or equivalent semantic owner is created by R2.1.

Continuity classes classify source and lifecycle roles; they do not create truth ownership.

## LAW R2.1-2 — CURRENT QUESTIONS RESOLVE THROUGH CURRENT OWNERS

For a current semantic question, the applicable native owner/currentness contract is authoritative.

There is no reconciliation vote between current owners and derived prose.

A derived projection conflicting with a current owner is stale/defective evidence, not a competing authority.

## LAW R2.1-3 — STORY MAY PROVIDE GAMEPLAY CONTINUITY ORIENTATION

Eligible Story may support:

- broad campaign orientation;
- episodic historical orientation;
- entity-linked history hints;
- navigation toward admitted source evidence;
- prose continuity useful to a logical role.

It remains noncanonical, optional and allowed to lag.

## LAW R2.1-4 — DERIVED CONTINUITY DOES NOT WIDEN ELIGIBILITY

Repository visibility, Story availability, current-chat visibility and prior model exposure do not grant logical-role, fictional-subject or human-recipient eligibility.

Gameplay role/player/subject filtering is a downstream Context Runtime obligation.

Material eligibility ambiguity must not be resolved by physical availability.

## LAW R2.1-5 — MATERIAL ROLE DECISIONS ESCALATE TO THE PROPER SOURCE CLASS

A derived projection may orient a role, but whenever a **material role decision** depends on a claim whose current/source-specific correctness matters, the role SHALL use the appropriate owning/admitted source class rather than relying solely on derived prose.

This applies to Interpreter, Dramaturg, Actor and Narrator decisions even when their immediate outputs remain noncanonical.

Examples requiring proper-source escalation include material dependence on:

- current world/runtime state;
- current fictional cognition;
- current disclosure;
- objective proposition status;
- exact wording;
- accepted occurrence/provenance;
- another owner-specific correctness fact.

## LAW R2.1-6 — SOURCE-BOUND DOES NOT MEAN CURRENT

Source traceability proves derivation, not currentness.

A derived historical statement SHALL NOT answer a current-state question unless currentness is established through the applicable native owner/currentness relation.

R2.1 creates no generic projection freshness frontier.

## LAW R2.1-7 — HISTORY ALIGNMENT USES HDM SOURCES, NOT HOST ANCESTRY

Durable derived continuity aligns through:

```text
stable source refs / source-domain coverage
+ source-specific correction/currentness/supersession semantics where material
+ semantic projection-contract generation
```

It SHALL NOT align through:

```text
host chat cursor
host message age
host Retry/Edit branch ancestry
wall-clock age
model memory state
```

## LAW R2.1-8 — ONLY ADMITTED HDM EVIDENCE MAY ENTER DURABLE CONTINUITY

Rejected generations, abandoned Narrator drafts, hidden chain-of-thought, internal prompts, private diagnostic reasoning and unaccepted candidate mutations do not become durable continuity input merely because they were generated or visible to the model.

For baseline correctness, source admission replaces the research idea of a time-based mutable host-history horizon.

## LAW R2.1-9 — STALE OR INCOMPATIBLE PROJECTION DEGRADES TO STRONGER EVIDENCE

When compatibility cannot be established:

```text
exclude or downgrade derived projection
-> use stronger admitted current/historical evidence
-> repair/rebuild projection later when useful
```

Do not guess reconciliation.

Optional continuity repair SHALL NOT block gameplay correctness.

## LAW R2.1-10 — DERIVED TEXT CANNOT SELF-AMPLIFY FACTUAL AUTHORITY

Repeated summarization, recurrence or repeated mention does not increase factual authority, truth status or confidence.

A derived transformation may use prior Story for editorial continuity/navigation, but factual support for material claims must remain traceable to admitted underlying evidence appropriate to the claim.

## LAW R2.1-11 — PROJECTION ABSENCE IS NOT SEMANTIC ABSENCE

Absence or omission from Story/another derived projection is not evidence that the underlying fact, event, entity or relation does not exist unless that exact projection contract explicitly proves exhaustive coverage for the semantic question being asked.

Story coverage is typed to its own source-domain/candidate/terminal-disposition contract and SHALL NOT be generalized into a global closed-world claim.

## LAW R2.1-12 — ENTITY CONTINUITY STARTS AS A VIEW

Baseline entity continuity composes:

```text
current native owner
+ relevant accepted historical evidence
+ eligible Story/entity refs
+ selective exact evidence where required
```

A durable per-entity synopsis is conditional on R2.3 evidence that bounded scoped retrieval cannot meet latency/context/quality requirements.

## LAW R2.1-13 — EXACT RECALL REMAINS SELECTIVE EXACT

For an exact-wording request:

```text
surviving exact evidence exists
    -> exact claim may be made under that source contract

no exact evidence survives
    -> state that exact wording is not retained
    -> provide strongest supported semantic account
```

Generated reconstruction is never exact-history evidence.

## LAW R2.1-14 — NO PER-TURN OR BACKGROUND CONTINUITY CLOCK

No baseline correctness requirement creates a per-turn durable memory write, heartbeat, timer, autonomous summarizer or mandatory projection-refresh barrier.

Story/derived continuity may lag, defer, rebuild or remain absent.

## LAW R2.1-15 — DEEP HISTORY AVAILABILITY IS NOT PRELOAD PERMISSION

A durable archive may be large while one role context remains bounded.

R2.1 does not authorize whole-history preload. R2.3 owns bounded acquisition, retrieval, ranking, placement and degradation.

---

# 4. Stability and consolidation

## 4.1 Stability boundary

R2.1 uses **HDM source admission**, not host-message age, as the baseline stability gate for durable projection input.

```text
unaccepted/generated material
    -> not durable continuity input

accepted HDM source evidence
    -> eligible projection candidate under its source-domain contract
```

Accepted sources may still undergo owner-defined correction/supersession/currentness transitions. Derived compatibility must respect those contracts.

## 4.2 Consolidation

Consolidation is non-authoritative projection:

```text
bounded admitted source evidence
    -> derived transformation candidate
    -> structural/source validation
    -> noncanonical projection publication
```

No consolidation operation promotes the projection into current truth.

## 4.3 No universal consolidation threshold

R2.1 introduces no fixed N-turn, N-minute, session-end, model-confidence or host-history-age threshold.

Story projection activation remains governed by its existing projection semantics and later runtime policy.

---

# 5. Provenance and coverage

## 5.1 Claim-typed provenance

HDM SHALL NOT use one global scalar source-trust score.

Different source classes prove different semantic claims.

Examples:

```text
current HP                  -> current state owner
current NPC belief          -> world.knowledge
what was communicated       -> admitted message/communication evidence
objective truth of claim    -> applicable world/lore owner
broad historical orientation-> eligible Story with source refs
```

## 5.2 Durable derived source basis

A durable derived unit must retain enough source identity/coverage information to:

- trace its factual spine;
- evaluate compatibility under its projection contract;
- avoid treating derivative prose as original evidence;
- support bounded repair/rebuild/retirement without hidden model memory.

For Story, Step-5.10 source refs, typed source-domain coverage and semantic projection-contract generation remain the baseline mechanisms.

No parallel generic continuity coverage registry is introduced.

## 5.3 Coverage is contract-typed

Projection coverage proves only what its exact layer/source/semantic projection contract defines.

Coverage SHALL NOT be interpreted as global semantic completeness or proof that omitted concepts do not exist.

---

# 6. History alignment, correction and repair

## 6.1 Host Retry/Edit/branch

Host Retry/regeneration/edit/branch/delete does not rewrite accepted HDM history and does not automatically invalidate/rewrite durable continuity.

A real campaign correction must enter through normal HDM semantics and then propagate to affected derived projections according to source compatibility/repair rules.

## 6.2 Source correction/supersession/currentness change

For a dependent derived unit:

```text
compatible      -> retain
repairable       -> regenerate/update
obsolete         -> retire/exclude from current selection
uncertain        -> exclude/degrade and use stronger evidence
```

No global ancestry graph is required.

## 6.3 Projection semantic generation

If projection candidate meaning, admission, terminal disposition or semantic coverage changes incompatibly, the affected projection requires explicit compatible migration/reprojection/reset.

Model version, prose style or prompt wording alone does not automatically change semantic coverage generation.

## 6.4 Repair principle

Derived continuity is disposable before authority.

Repair SHALL target the projection, not mutate current canon to match the projection.

## 6.5 No global pre-turn repair scan

R2.1 does not authorize campaign-wide repair/freshness scans before gameplay.

R2.3 must operate through bounded candidate acquisition and relevant compatibility checks.

---

# 7. Generative transformation boundary

Where Chronicler/LLM generation creates a durable derived projection:

```text
bounded admitted source bundle
    -> derived draft
    -> deterministic structural/source validation
    -> durable noncanonical publication if accepted
```

Deterministic validation owns, as applicable:

- source identity/admission checks;
- source-domain membership/coverage legality;
- pinned reference resolution;
- shape/size/cardinality contract;
- absence of forbidden authority mutation;
- required source/availability metadata;
- coherent projection output/coverage publication.

Structural validation cannot prove every prose inference semantically correct.

A semantically poor but structurally valid Story unit remains a repairable noncanonical defect, not canon.

Human review is optional quality tooling, not baseline gameplay correctness machinery.

A bounded source window may produce several coherent derived records in one projection publication; R2.1 does not impose a universal one-assessment/one-mutation rule.

---

# 8. Broad, episodic, entity and exact continuity

## 8.1 Broad orientation

Broad orientation is a consumer need rather than a mandatory new record type.

Compatible eligible Story/NARRATIVE, chapter/index synopsis where available and transient recap from durable evidence are preferred reuse surfaces.

## 8.2 Episodic recall

Episodic recall may draw from compatible Story/EVENTS, Transcript/message evidence, SemanticEvents and other source-specific history.

R2.1 does not decide ranking/retrieval order.

## 8.3 Entity continuity

Entity continuity remains the scoped view defined by LAW R2.1-12.

R2.2 may add proper current Actor-owned cognition/state; generic continuity may not preempt those owners.

## 8.4 Recent exact/history evidence

No new durable `recent_memory` layer is introduced.

Recent accepted messages/events remain their existing history sources. Current-chat exact material may be used while present but is not recovery authority unless admitted/persisted through existing HDM contracts.

---

# 9. Story / Chronicler integration

Story responsibility changes only at the **consumer edge**:

```text
occurred evidence -> Story -> presentation/history/Commentator

plus now:

eligible Story -> gameplay continuity orientation
              -> proper-source escalation for material decisions
```

Chronicler authority does not expand.

Story spectator availability is not equivalent to gameplay role/player/subject eligibility.

A Story unit may be source-valid historically yet unsuitable for a current-state premise. R2.3 must preserve this distinction.

---

# 10. Recovery and degradation

After total host/context loss:

- recover current semantics from HDM-owned durable sources;
- use Story if compatible/eligible and available;
- otherwise synthesize bounded transient orientation from stronger sources;
- never invent lost unpublished/hidden model state;
- never block correctness on missing derived continuity.

Missing/lagging Story is a quality/latency degradation, not loss of semantic authority.

---

# 11. Downstream contracts

## 11.1 R2.2 — Actor continuity

R2.2 SHALL preserve:

- Story/generic continuity is not current Actor cognition;
- `world.knowledge` remains current epistemic owner;
- goals/private plans/relationships/transient Actor cognition require proper ownership;
- Actor consumption of a historical claim does not automatically establish belief/knowledge;
- material Actor decisions relying on current/source-specific claims must obtain proper-source evidence.

R2.2 may reconsider a narrow one-assessment/one-mutation pattern only for Actor cognition if justified.

## 11.2 R2.3 — Context Runtime

R2.3 SHALL define bounded:

- candidate acquisition across current/history/Story/exact classes;
- receiving role/player/subject eligibility;
- broad -> episodic/current/exact escalation;
- complete decision-packet behavior;
- source-aware semantic dedup;
- entity-scoped retrieval;
- stale/incompatible projection exclusion;
- budget/placement/degradation;
- projection-absence handling without closed-world inference;
- dry-run/context trace.

R2.3 SHALL NOT create a new memory authority for retrieval convenience.

## 11.3 R2.4 — LLM execution

R2.4 may use Story/transient recap as input while preserving role rebinding, eligibility, typed handoffs, deterministic authority and no hidden chain-of-thought persistence.

## 11.4 R2.5 — Multiplayer

Shared repository/Story availability does not imply identical player/Actor continuity projections.

Recipient/player/subject eligibility remains scoped.

## 11.5 R2.7 — Machine realization

Schema/catalog/index/tool changes are deferred to realization mapping after architecture closes.

R2.1 approves no concrete schema.

---

# 12. Rejected and conditional alternatives

Rejected for current architecture:

- generic layered memory subsystem parallel to Story/history;
- authoritative global summary;
- host Retry/Edit ancestry as campaign lineage;
- time-based host-history stabilization timer;
- global source-trust score;
- per-turn durable memory write;
- background summarization correctness dependency;
- universal exact conversation archive;
- global projection freshness frontier.

Conditional:

- durable entity synopsis — revisit only if R2.3 proves scoped retrieval insufficient;
- separate broad/episodic projection family — revisit only if Story/history reuse cannot satisfy a concrete consumer without violating Story boundaries;
- additional derived self-repair/index machinery — revisit only after a concrete persistent derived representation is admitted.

---

# 13. Falsifiability / reopen conditions

Reopen R2.1 only when later evidence establishes a material insufficiency such as:

- Story/history reuse cannot provide adequate continuity without becoming correctness-critical authority;
- R2.3 cannot build bounded entity continuity without a durable derived view;
- source-aligned repair cannot be bounded without a new owned dependency surface;
- a required product promise genuinely needs broader exact retention than Step 5.11;
- an admitted continuity consumer cannot safely recover from HDM-owned evidence after host/context loss;
- a new derived view otherwise creates unavoidable duplicate authority.

Implementation convenience is not sufficient.

---

# 14. R2.1 result

R2.1 establishes:

- minimum continuity source classes without new memory authority;
- Story as an eligible nonauthoritative gameplay continuity/orientation source;
- claim-typed provenance and source/currentness separation;
- source-admission rather than host-age stability;
- HDM-source-aligned history semantics;
- stale/degrade/repair/retirement behavior;
- projection absence != semantic absence;
- semantic versus selective-exact recall boundary;
- no background/per-turn maintenance dependency;
- explicit R2.2 and R2.3 consumer contracts.

Architecture closure is recorded separately by the R2.1 resolution gate.
