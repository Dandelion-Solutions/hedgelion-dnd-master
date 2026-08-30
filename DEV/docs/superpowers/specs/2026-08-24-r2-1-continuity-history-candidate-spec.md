# R2.1 Candidate Specification — Continuity, Memory and History-Aligned Derived State

Status: **CANDIDATE ARCHITECTURE — OWNER DIRECTION APPROVED / ADVERSARIAL REVIEW REQUIRED**

Date: 2026-08-24

Owner decision:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-projection-owner-decision.md`

Task brief:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-memory-history-task-brief.md`

Evidence ledger:

- `DEV/docs/superpowers/design/2026-08-24-r2-1-continuity-evidence-ledger.md`

This candidate formalizes the approved reuse-first continuity direction. It does not authorize implementation.

---

# 1. Canonical direction

HDM long-campaign continuity SHALL be realized as a **typed source/lifecycle model over existing semantic owners and non-authoritative projections**, not as a new generic memory authority.

```text
CURRENT AUTHORITATIVE SOURCES
    natural world/runtime owners
    world.lore_fact where applicable
    world.knowledge
    runtime.disclosure

ACCEPTED HISTORICAL EVIDENCE
    runtime.interaction
    runtime.message
    runtime.semantic_event / LOG
    runtime.mechanical_event / receipts
    chronology evidence
    other admitted owner-specific history

DERIVED DURABLE CONTINUITY
    STORY/*
    source-bound, optional/lagging, noncanonical
    may provide eligible broad/episodic orientation

TRANSIENT WORKING CONTINUITY
    loaded working set
    generated recap
    current-turn/session orientation
    disposable

SELECTIVE EXACT EVIDENCE
    Step-5.11 protected message/slice
    natural exact owner
    verified exact Transcript where admitted

OPTIONAL FUTURE DERIVED VIEWS
    no baseline authority
    admitted only by later concrete requirement
```

Core invariant:

> **Continuity helps the LLM recover what matters; it does not decide what is true, currently known, disclosed, or mechanically established.**

---

# 2. Continuity class contract

## 2.1 Current authoritative sources

Purpose:

- answer current semantic questions;
- own mutable/current world, runtime, epistemic and disclosure state.

Properties:

```text
authoritative        yes, within native owner contract
durable              according to native owner policy
rebuildable           owner-specific
exact-protected       owner-specific
projection            no
```

Continuity logic SHALL NOT copy these sources into a second writable current-state store.

## 2.2 Accepted historical evidence

Purpose:

- prove accepted occurrences, communications, causal/history relations and retained evidence according to each source's native contract.

Properties:

```text
authoritative        only for the evidence/occurrence semantics the source owns
durable              according to Step-5/native policy
current-state owner   no
projection            no
```

A historical record proving that a claim was said does not prove the claim true. A mechanical event proving a committed effect does not become the current-state owner after later state changes.

## 2.3 Story as durable derived continuity

Story remains the Step-4/5 durable noncanonical projection family:

```text
STORY/TRANSCRIPT
STORY/EVENTS
STORY/MECHANICS
STORY/NARRATIVE
```

R2.1 adds one permitted consumer relationship:

> Eligible gameplay logical roles MAY use Story as broad/episodic continuity orientation or as a route toward stronger underlying evidence.

Properties:

```text
authoritative        no
durable              yes when published
rebuildable/repairable according to Story source availability/retention
may lag              yes
may be absent         yes
may block gameplay    no
source-bound          yes
role eligibility      independently evaluated downstream
```

Story does not acquire a gameplay authority merely because gameplay roles consume it.

## 2.4 Transient working continuity

Examples:

- current loaded working set;
- generated session/new-chat recap;
- turn-local synthesis;
- temporary entity-oriented orientation assembled from admitted evidence.

Properties:

```text
authoritative        no
durable              not required
rebuildable          yes or safely disposable
recovery dependency  no
```

Loss of transient working continuity may cost latency or prose quality, but cannot erase accepted campaign semantics.

## 2.5 Selective exact evidence

Exact recall remains entirely governed by Step 5.11 and natural exact-content owners.

R2.1 introduces no broader exact-history promise.

Properties:

```text
exact claim allowed  only from surviving exact evidence
semantic fallback    yes
fabricated quote      forbidden
```

## 2.6 Optional future derived views

Examples may include a stored entity synopsis or another role-oriented cache.

No such class is admitted by baseline R2.1.

Admission requires:

1. a concrete downstream consumer;
2. evidence that existing owners + Story/history + transient synthesis are insufficient;
3. explicit authority/lifecycle/source/repair contract;
4. no duplicate semantic authority;
5. normal architecture approval before implementation.

---

# 3. R2.1 laws

## LAW R2.1-1 — CONTINUITY IS NOT A NEW AUTHORITY

No generic `memory`, `continuity`, `episode_memory`, `entity_memory` or equivalent semantic owner is introduced by R2.1.

Continuity classes classify how information is owned, retained, projected or consumed. They do not create new truth ownership.

## LAW R2.1-2 — NATIVE CURRENT OWNERS ANSWER CURRENT QUESTIONS

For a current semantic question, the applicable native owner wins by contract.

There is no reconciliation vote among:

```text
current owner
Story summary
old transcript
current chat prose
model recollection
```

A conflicting derived projection is stale/defective evidence, not a competing candidate authority.

## LAW R2.1-3 — STORY MAY SERVE AS DERIVED GAMEPLAY CONTINUITY

Eligible Story may provide:

- broad campaign orientation;
- episodic historical orientation;
- entity-linked history hints;
- navigation toward source evidence;
- prose continuity useful to a gameplay role.

It remains durable, noncanonical, optional and allowed to lag.

## LAW R2.1-4 — DERIVED CONTINUITY DOES NOT WIDEN ELIGIBILITY

Physical repository availability, Story availability, current-chat visibility or prior model exposure does not make material eligible for a logical role, fictional subject or human recipient.

Concrete role/player/subject filtering belongs to R2.3 and later runtime realization.

R2.1 requires only that every derived continuity consumer preserve the same eligibility boundary as the material claim it conveys.

## LAW R2.1-5 — DECISION-CRITICAL CLAIMS ESCALATE TO THE PROPER SOURCE CLASS

Story or transient recap may orient a role, identify likely relevant entities/events or suggest a retrieval route.

When a material decision depends on:

- current state;
- current fictional cognition;
- current disclosure;
- objective proposition status;
- exact wording;
- an accepted occurrence/provenance claim;
- another owner-specific correctness fact;

use the source class that owns that semantic question.

Story alone is not sufficient merely because its prose is plausible or source-linked.

## LAW R2.1-6 — HISTORY ALIGNMENT IS HDM-SOURCE ALIGNMENT

Durable derived continuity aligns through HDM-owned evidence, conceptually:

```text
stable source refs / source-domain coverage
+ source-specific current/correction/supersession semantics where material
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

Host history is presentation/context, not the campaign-history branch authority.

## LAW R2.1-7 — ONLY ADMITTED HDM EVIDENCE MAY ENTER DURABLE CONTINUITY

Durable derived continuity may project only admitted source evidence under its source-domain contract.

The following do not enter durable continuity merely because they were generated or physically visible:

- rejected generations;
- abandoned Narrator drafts;
- hidden chain-of-thought;
- internal prompt text;
- private diagnostic reasoning;
- unaccepted candidate mutations;
- speculative prose lacking admitted source status.

No age-based "recent mutable horizon" is required for baseline correctness. The relevant gate is source admission and compatibility.

## LAW R2.1-8 — STALE OR INCOMPATIBLE PROJECTION DEGRADES TO STRONGER EVIDENCE

When compatibility of a derived projection cannot be established:

```text
exclude or downgrade projection
-> retrieve/use stronger admitted source evidence
-> rebuild/repair derived projection later when useful
```

Do not guess reconciliation and do not block gameplay merely to repair an optional continuity projection.

## LAW R2.1-9 — DERIVED TEXT CANNOT SELF-AMPLIFY FACTUAL AUTHORITY

A derived transformation may use prior Story for editorial continuity, organization or navigation.

Its factual support SHALL remain traceable to admitted underlying source evidence appropriate to the claim.

Repeated summarization, recurrence or repeated mention does not increase factual authority, truth status or confidence by itself.

## LAW R2.1-10 — ENTITY CONTINUITY STARTS AS A VIEW

Baseline entity continuity is a scoped composition over:

```text
current entity/native owner
+ relevant accepted history
+ eligible Story/entity refs
+ selective exact evidence when required
```

No durable per-entity synopsis is required.

Revisit only if R2.3 demonstrates that the view cannot meet bounded context/latency/quality needs.

## LAW R2.1-11 — EXACT RECALL REMAINS SELECTIVE EXACT

If exact wording is materially requested:

```text
surviving exact source available
    -> exact claim may be made under that source contract

exact source unavailable
    -> state that exact wording is not retained
    -> provide strongest supported semantic account
```

Generated reconstruction is never promoted to exact-history status.

## LAW R2.1-12 — CONTINUITY MAINTENANCE IS NOT A GAMEPLAY CORRECTNESS CLOCK

No baseline correctness requirement creates:

- one summary per turn;
- periodic heartbeat memory writes;
- an autonomous background summarizer;
- an hourly continuity worker;
- a mandatory projection-refresh barrier before ordinary gameplay.

Story/derived continuity may lag, defer, rebuild or remain absent.

---

# 4. Stability and consolidation

## 4.1 Source admission is the stability boundary

R2.1 does not define stability by elapsed time in the host UI.

Conceptually:

```text
unaccepted/generated material
    -> not durable continuity input

accepted HDM source evidence
    -> may become an admitted projection candidate
       under its source-domain contract
```

A source may still have native correction/supersession semantics after acceptance. Projection compatibility must respect those semantics.

## 4.2 Consolidation is projection, not authority promotion

When historical evidence is summarized/grouped/compressed into Story or another future admitted derived view:

```text
source evidence
    -> bounded transformation candidate
    -> structural/source validation
    -> noncanonical projection publication
```

No consolidation operation upgrades the projection into current truth.

## 4.3 No universal consolidation threshold

R2.1 does not introduce one fixed rule such as:

- after N turns;
- after N minutes;
- after one scene;
- after one host branch becomes old;
- after one model confidence threshold.

Story projection activation remains downstream/runtime policy constrained by Step 5.10. A future derived view must define its own justified activation contract.

---

# 5. Source provenance and coverage

## 5.1 Claim-typed provenance

HDM SHALL NOT define one global scalar trust score for continuity sources.

Source sufficiency depends on the semantic question.

Examples:

```text
current HP
    -> current Actor/state owner

current NPC belief
    -> world.knowledge

what a participant said
    -> admitted runtime.message / communication evidence

objective truth of that statement
    -> applicable world/lore owner

broad narrative orientation
    -> eligible Story may summarize with source refs
```

## 5.2 Durable derived projection source basis

A durable derived continuity record/unit must retain sufficient source identity/coverage metadata to:

- trace its factual spine;
- test compatibility where its source contract requires it;
- avoid treating unsupported derivative prose as original evidence;
- repair/rebuild or retire it without relying on hidden model memory.

For Story, existing Step-5.10 source refs, source-domain coverage and semantic projection-contract generation remain the baseline mechanism.

R2.1 creates no parallel generic coverage registry.

## 5.3 Semantic source sufficiency before exact loss

Step-5.11 semantic discharge remains binding.

A derived projection cannot justify deletion of exact/source payload if surviving semantic consumers still depend on content that has not been preserved by an appropriate owner/source contract.

R2.1 does not weaken compaction safety.

---

# 6. History alignment and correction

## 6.1 Host Retry / regeneration

A host Retry/regeneration does not create a second campaign history branch by itself.

Accepted HDM source identities remain the history basis.

A regenerated presentation must not silently replace accepted source evidence merely because the host UI now displays different prose.

## 6.2 Old user-message edit / host branch

Editing/branching host history does not invalidate accepted HDM sources automatically and does not retroactively mutate durable derived continuity.

If the user intends a campaign correction, that correction must enter through normal current HDM semantics and then affect downstream sources/projections according to their owner contracts.

## 6.3 Source correction / supersession

Where an owning source supports correction/supersession/version movement, a dependent derived projection must not continue to assert incompatible material as if current.

Permitted response:

```text
compatible -> retain
repairable -> regenerate/update projection
obsolete -> retire/omit from current continuity selection
uncertain -> exclude/degrade and use stronger sources
```

The exact dependency lookup/selection implementation is downstream.

## 6.4 Projection-contract generation

A semantic change to what a projection means, which candidates it admits or what terminal coverage proves requires compatible migration/reprojection/reset semantics according to Step-5.10-style generation rules.

Model version, prose style or prompt wording alone does not automatically invalidate semantic coverage.

---

# 7. Derived mutation and validation

## 7.1 Generative transformation boundary

Where an LLM/Chronicler produces derived continuity:

```text
bounded admitted source bundle
    -> derived draft
    -> deterministic structural/source validation
    -> durable noncanonical publication if accepted
```

The deterministic layer can validate at least as applicable:

- source identities exist/are admitted;
- source-domain membership/coverage is legal;
- references resolve under the applicable pinned basis;
- output shape/size/cardinality satisfies the projection contract;
- no forbidden authority field is written;
- required availability/source metadata is present;
- publication updates projection output/coverage coherently.

## 7.2 Semantic quality is not canonicalized by validation

Deterministic structural validation cannot prove every prose inference correct.

Therefore a semantically poor but structurally valid Story record is a **repairable noncanonical projection defect**, not accepted world truth.

Gameplay correctness remains protected by LAW R2.1-5.

## 7.3 Human review is optional tooling

Human/editor review may improve high-value Story/summary quality but SHALL NOT be a baseline gameplay correctness dependency.

## 7.4 Bounded publication may contain several records

R2.1 rejects a universal "one assessment -> one durable mutation" rule for noncanonical projection catch-up.

A bounded coherent source window may lawfully produce several derived records under one projection publication, as Step 5.10 already permits.

---

# 8. Repair, rebuild and retirement

## 8.1 Repair principle

Derived continuity is disposable before authority.

If a derived product is stale, malformed, incompatible or semantically suspect:

- remove it from correctness-sensitive selection;
- use stronger surviving evidence;
- rebuild/repair only when useful;
- do not repair current canon merely to match a summary.

## 8.2 Story lag/failure

Story lag/failure SHALL NOT:

- block gameplay;
- block recovery;
- roll back current state;
- force recreation of lost exact wording;
- promote transient model memory into recovery evidence.

## 8.3 Retirement

A derived continuity unit may become non-current for retrieval because:

- its source basis is superseded/incompatible;
- its semantic projection generation is obsolete;
- it was corrected/replaced editorially;
- it no longer satisfies role/player/subject eligibility;
- it is otherwise lawfully removed under Story retention/cleanup rules.

Physical deletion/GC remains governed by Step-5 retention/cleanup owners. R2.1 does not create a new GC subsystem.

## 8.4 No global repair scan requirement

R2.1 does not authorize campaign-wide scans merely to prove all derived continuity fresh before each turn.

R2.3 must use bounded candidate acquisition and compatibility checks. Maintenance may repair broader projection state when explicitly useful.

---

# 9. Broad, episodic and entity continuity

## 9.1 Broad orientation

Broad orientation is a **consumer need**, not a mandatory new record type.

Preferred existing sources include compatible eligible Story/NARRATIVE, chapter/index synopsis where available and generated transient recap from durable evidence.

## 9.2 Episodic recall

Episodic recall may use compatible Story/EVENTS, relevant Transcript/Message evidence, SemanticEvents and other source-specific history.

R2.1 does not decide ranking or retrieval order beyond source-authority boundaries.

## 9.3 Entity continuity

Entity continuity is initially a scoped view as defined by LAW R2.1-10.

R2.2 may define additional current Actor-owned cognition/state. R2.1 generic continuity SHALL NOT preempt those owners.

## 9.4 Recent exact/history evidence

There is no new durable `recent_memory` layer.

Recent accepted messages/events remain their existing historical evidence. Current-chat exact material may be used while available but is not recovery authority unless admitted/persisted by existing HDM contracts.

---

# 10. Relationship to Story and Chronicler

## 10.1 Story responsibility is extended only at the consumer edge

R2.1 does not change Story publication ownership or canon status.

The architectural extension is:

```text
previously:
    occurred evidence -> Story -> presentation/history/Commentator

now also permitted:
    eligible Story -> gameplay-role continuity orientation
                 -> stronger source retrieval where correctness requires
```

## 10.2 Chronicler authority does not expand

Chronicler remains editorial/generative only.

It does not:

- establish canon;
- establish current knowledge/cognition;
- decide Story source coverage authoritatively;
- certify its prose as factual truth;
- decide role eligibility merely by writing content.

## 10.3 Story availability is not gameplay role eligibility

Commentator/spectator availability semantics and gameplay role/subject/player eligibility are different concerns.

R2.3 must evaluate gameplay continuity candidates under the receiving role's actual eligibility contract.

---

# 11. Semantic versus exact recall contract

R2.1 preserves the owner-approved Step-5.11 product promise:

> HDM should remember established campaign meaning extremely well; it is not a universal tape recorder.

For recall requests:

```text
semantic question
    -> strongest appropriate current/history/derived evidence

exact wording question
    -> exact-protected/natural exact/verified exact source if available
    -> otherwise explicit non-retention statement + semantic account
```

Story prose that paraphrases an old communication is not exact evidence unless separately verified under the existing exact-archive contract.

---

# 12. Downstream contracts

## 12.1 R2.2 — Actor continuity

R2.2 receives these constraints:

- generic continuity/Story is not current Actor cognition;
- current Actor epistemics continue through `world.knowledge`;
- new goals/private plans/relationships/transient cognition require explicit proper ownership;
- an Actor may consume eligible continuity evidence without automatically adopting it as belief/knowledge;
- R2.2 may reconsider a narrow one-assessment/one-mutation pattern for cognition if useful.

## 12.2 R2.3 — Context Runtime

R2.3 must define:

- bounded candidate acquisition across current/history/Story/exact classes;
- receiving role/player/subject eligibility for Story-derived candidates;
- broad -> episodic/current/exact escalation policy;
- complete decision-packet behavior;
- semantic/source-aware dedup;
- entity-scoped retrieval;
- stale/incompatible projection exclusion;
- budget/placement/degradation policy;
- dry-run/context trace.

R2.3 must not create a new memory authority to simplify retrieval.

## 12.3 R2.4 — LLM execution

R2.4 may use Story/transient recap as role input but must preserve:

- role rebinding/eligibility;
- typed handoff boundaries;
- no hidden chain-of-thought persistence;
- deterministic authority gateway.

## 12.4 R2.5 — Multiplayer

One shared repository/Story surface does not imply one identical player/Actor continuity projection.

Recipient/subject/player eligibility remains scoped independently.

## 12.5 R2.7 — Machine realization

Only after architecture closure may machine mapping decide whether existing Story indexes/metadata suffice or require schema/catalog/tool changes.

No schema is approved by R2.1 itself.

---

# 13. Explicitly rejected or conditional alternatives

Rejected for current architecture:

- generic layered memory subsystem parallel to Story/history;
- one permanent global summary as authoritative memory;
- host Retry/Edit ancestry as campaign-history lineage;
- time-based UI stabilization timer for accepted evidence;
- global source-trust score;
- per-turn durable memory writes;
- background summarization as correctness dependency;
- universal exact conversation archive.

Conditional:

- durable entity synopsis — trigger: R2.3 proves existing scoped retrieval insufficient;
- separate broad/episodic projection family — trigger: measured consumer need cannot be met by Story/history reuse without violating Story boundaries;
- additional derived self-repair/index machinery — trigger: concrete persistent derived representation is admitted and requires it.

---

# 14. Falsifiability / reopen conditions

Reopen R2.1 only if later evidence shows at least one of:

- eligible Story/history reuse cannot provide adequate broad/episodic continuity without making Story a correctness-critical authority;
- R2.3 cannot assemble bounded entity continuity without a durable entity synopsis or equivalent derived store;
- source-aligned repair cannot be bounded without a new owned dependency surface;
- a required product promise needs broader exact retention than Step 5.11;
- an admitted continuity consumer cannot recover safely after host/context loss from HDM-owned sources;
- a new derived view would otherwise create unavoidable duplicate authority.

Implementation convenience or preference for a conventional memory subsystem is not sufficient to reopen the architecture.

---

# 15. Candidate exit assessment

This candidate addresses the R2.1 Task Brief exit requirements for:

- continuity classes and rejected alternatives;
- owner/authority/lifecycle;
- source/provenance/coverage;
- stability/consolidation;
- history alignment;
- stale/conflict/repair/rebuild/retirement;
- semantic versus exact recall;
- Story/Chronicler relationship;
- bounded generative projection validation;
- R2.2/R2.3 downstream contracts;
- duplicate-authority prevention.

R2.1 remains **IN PROGRESS** until adversarial review and closure gate complete.
