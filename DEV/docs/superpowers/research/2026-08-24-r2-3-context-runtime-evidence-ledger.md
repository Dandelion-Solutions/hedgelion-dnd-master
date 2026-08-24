# R2.3 Evidence Ledger — Context Runtime, Retrieval, Lazy Discovery and Allocation

Status: **RESEARCH EVIDENCE / PRE-DECISION SYNTHESIS**

Date: 2026-08-24

Task brief:

- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-lazy-discovery-task-brief.md`

Upstream canonical architecture:

- Step-4 truth/knowledge/role-context/Story canonical specification;
- Step-4 single-context role-containment canonical amendment;
- R2.1 continuity canonical specification;
- R2.2 Actor continuity canonical specification;
- accepted Step-5 Story/exact/live/currentness architecture.

This ledger preserves source claims, qualifiers, applicability and current R2.3 disposition before synthesis. It is not an accepted architecture decision.

---

# 1. Source Manifest completion

For the R2.3 design question, the required source set has been inspected to task depth:

| Source family | Authority role | Task status |
|---|---|---|
| current roadmap + R2.3 task brief | sequencing / scoped question | exhausted-for-task |
| Step-4 Context Assembler + role contracts | canonical owner | exhausted-for-task |
| Step-4 single-context amendment | later canonical amendment | exhausted-for-task |
| R2.1 continuity | upstream canonical owner | exhausted-for-task |
| R2.2 Actor/lazy-discovery handoff | upstream canonical owner | exhausted-for-task |
| Step-5.10 Story projection | historical/derived retrieval owner | inspected for retrieval/coverage boundary |
| Step-5.11 Selective Exact | exact-evidence owner | inspected for exactness boundary |
| `GAME/CORE/AI_REASONING.md` | current runtime consumer discipline | exhausted-for-task |
| `GAME/CORE/SESSION.md` | current runtime resume/working-set discipline | exhausted-for-task |
| `GAME/CORE/LIVE_SCENE.md` + live schema | routed currentness / hot-path owner | exhausted-for-task |
| `GAME/SCHEMA/current_state.schema.yaml` | compact current-scope machine surface | inspected |
| `GAME/SCHEMA/scene.schema.yaml` | compact scene machine surface | inspected |
| `GAME/SCHEMA/index.schema.yaml` + current INDEX scaffolds | routing/index machine surface | exhausted-for-task |
| active R2.3 DIAMOND/STRONG records | research input | item-level extracted below |
| relevant negative/reserve patterns | adversarial evidence | extracted below |

No current evidence justifies making unrelated catalog/schema/test families part of the R2.3 semantic decision. Concrete machine mapping remains R2.7.

---

# 2. Established canonical/current constraints

## C01 — Context Assembler already owns deterministic bounded role projection

Source: Step-4 canonical specification.

Actual claim:

- Context Assembler selects the smallest role-eligible source set for one LLM task;
- it is not a role, canon, ACL engine, knowledge graph, generic query language or permission for campaign-wide scans;
- `RoleContextRequest` already carries role, campaign/frontier, purpose and subject/player identities plus requested refs/bounded discovery intent;
- `RoleContextBundle` already contains eligible structured facts, bounded prose, source manifest and typed prior-role results.

R2.3 consequence:

> R2.3 extends the existing Context Assembler into an executable discovery/retrieval/allocation policy. It does not create a second context authority.

Disposition: **BOUNDARY / NON-NEGOTIABLE**.

## C02 — Logical context is not the whole physical model context

Source: Step-4 single-context amendment.

Actual claim:

- one physical ChatGPT context may contain several logical role phases;
- physical availability does not grant logical eligibility;
- Context Assembler still owns per-role source eligibility and bounded selection;
- a `RoleContextBundle` is a logical execution projection, not necessarily a separate physical invocation payload.

R2.3 consequence:

> R2.3 defines logical source acquisition/projection. R2.4 owns exact physical prompt/turn placement.

Disposition: **BOUNDARY**.

## C03 — Runtime already requires smallest authoritative working set

Source: `GAME/CORE/AI_REASONING.md`.

Actual claim:

- retrieve the smallest authoritative working set needed for the decision;
- do not preload WORLD/LOG/INDEX/entity data wholesale;
- do not recursively follow links without need;
- do not let recent prose outrank structured state;
- unknown-to-runtime is distinct from undefined.

R2.3 consequence:

> Lazy loading is a current correctness discipline, not only token optimization.

Disposition: **CURRENT CONSUMER REQUIREMENT**.

## C04 — Session start/resume already follows minimal/lazy acquisition

Source: `GAME/CORE/SESSION.md`.

Actual claim:

Startup resolves only current campaign/frontier, current scene/time/location, participating PCs, active threads/entities needed immediately and required recovery state. Old chat history is not reread wholesale. Tree metadata may be fetched lazily.

R2.3 consequence:

> R2.3 should generalize this selective acquisition discipline rather than create a preload phase.

Disposition: **CURRENT CONSUMER REQUIREMENT**.

## C05 — CURRENT and SCENE already form compact first-tier routing surfaces

Sources: `current_state.schema.yaml`, `scene.schema.yaml`.

Actual claim:

`CURRENT` keeps compact active scene refs and active threads. A SCENE may carry location, PCs/participants, active threads, relevant item refs, persistent feature refs, transient facts, chronology frontier and an actionable summary.

R2.3 consequence:

> Scene/current surfaces are strong discovery seeds, but are not guaranteed exhaustive registries of every semantically relevant entity.

Disposition: **REUSE CANDIDATE / NOT SUFFICIENT ALONE**.

## C06 — Existing entity index is explicitly routing metadata

Source: `GAME/SCHEMA/index.schema.yaml`.

Actual claim:

- index is a routing structure, not duplicate entity database;
- entries must remain compact enough to search without loading entity bodies;
- affected index entry updates atomically with canonical entity changes;
- aliases aid lookup without redefining identity.

Current entry contract includes routing fields such as identity, optional name/aliases/status, path, parent, tags and last event.

R2.3 consequence:

> Existing INDEX architecture is directly compatible with lazy candidate discovery, but current fields are not necessarily sufficient for scene/location relevance and secret-safe selection.

Disposition: **STRONG REUSE SURFACE / MACHINE DETAIL LATER**.

## C07 — Live routed authority can supersede campaign-base discovery hints

Source: `GAME/CORE/LIVE_SCENE.md` + live schema.

Actual claim:

- during live epoch, current truth for live-owned scope is base campaign state + current live state;
- live overlays and newly created entities may differ from campaign base/index;
- ordinary hot path forbids broad WORLD/index traversal;
- live state carries compact touched/created/observable evidence;
- currentness is synchronized through targeted live-source probing/refresh.

R2.3 consequence:

> Campaign index/scene hints cannot be treated as current negative authority during live play. Discovery must compose with current routed live evidence.

Disposition: **CURRENTNESS BOUNDARY**.

## C08 — R2.1 continuity is orientation, not current authority

Source: R2.1 canonical spec.

Actual claim:

- Story may orient gameplay roles;
- material current/source-specific questions return to proper owners;
- source-bound does not mean current;
- projection omission does not mean semantic absence;
- exact recall remains Selective Exact.

R2.3 consequence:

> Story/history hints can seed discovery/ranking, but required current evidence must load from current/native owners.

Disposition: **UPSTREAM BOUNDARY**.

## C09 — R2.2 mandates discoverability without full entity load

Source: R2.2 canonical spec.

Actual claim:

- full Actor continuity is not a discovery prerequisite;
- discovery metadata is derived, not authority;
- index omission is not general proof of absence;
- currentness follows routed authority;
- discovery is multi-channel, not location-only;
- candidate metadata must not leak protected material;
- existing CURRENT/SCENE/INDEX/live surfaces are candidate realizations only.

R2.3 consequence:

> Two-stage `discover -> verify/load` is now a mandatory downstream consumer contract.

Disposition: **UPSTREAM REQUIREMENT**.

## C10 — Story retrieval already has typed source-domain/coverage semantics

Source: Step 5.10.

Actual claim:

- Story is noncanonical and may lag;
- projection source domains have typed candidate enumeration/coverage contracts;
- Story source coverage is contract-specific rather than global truth completeness;
- no background worker or generic job queue is required.

R2.3 consequence:

> Story layer/index may support coarse historical retrieval, but its coverage cannot become a global closed-world guarantee.

Disposition: **RETRIEVAL BOUNDARY**.

## C11 — Exactness is owner-declared and selective

Source: Step 5.11.

Actual claim:

- semantic continuity is baseline; verbatim recall is selective;
- exactness requires surviving exact evidence;
- exact protection is declared by the semantic consumer/contract, not LLM importance judgment;
- smallest sufficient exact representation is preferred.

R2.3 consequence:

> Allocator must carry an explicit minimum representation floor. Exact-required evidence cannot be silently summarized to fit.

Disposition: **EXACTNESS BOUNDARY**.

---

# 3. Active DIAMOND / STRONG extraction

## D02 — Context as materialized projection

Research claim:

- finite LLM context must be separated from durable campaign knowledge/state;
- context is an execution product with typed source, eligibility/relevance and budget policy;
- omission from one context does not mean loss from campaign memory.

Simplest form:

- candidate has source, semantic class, eligibility reason and size.

Strongest counterargument/risk:

- overcomplicated selection can create false confidence that retrieval found everything needed.

R2.3 reconciliation:

- concept already exists in Step 4;
- R2.3 must materialize concrete discovery/retrieval/allocation/trace semantics.

Disposition: **ADOPT / REALIZE EXISTING PRINCIPLE**.

## D03 — Semantic allocator with reservations/degradation

Research claim:

- independent subsystem budgets cause accidental eviction;
- importance and prompt position are different;
- use semantic classes, minimum reservations, maxima/soft budgets, protected entries and representation downgrade.

Simplest form:

- small number of semantic classes and required/optional distinction.

Strongest counterargument/risk:

- copied fixed quotas become rigid, wasteful and provider-specific.

R2.3 reconciliation:

> Adopt one allocator and representation floors, but reject copied fixed percentages. Required packet floors come first; optional allocation uses remaining budget under a runtime-supplied budget envelope.

Disposition: **ADOPT PRINCIPLE / REJECT FIXED QUOTAS**.

## D04 — Context assembly execution trace

Research claim:

Trace should explain source/revision, eligibility, selectors, privilege, rank, budget, chosen representation and inclusion/exclusion.

Risk:

- trace can itself leak secrets.

R2.3 reconciliation:

> ContextTrace is required diagnostic/test evidence, access-restricted and not automatically included in the role/player prompt.

Disposition: **ADOPT**.

## D14 — Complete decision packet before partial truncation

Research claim:

- partial decision-critical evidence can yield plausible but wrong semantic decisions;
- downgrade representations before omission;
- if minimum packet still cannot fit, defer rather than truncate.

Risk:

- naive defer can become an infinite stall loop.

R2.3 reconciliation:

> Adopt minimum complete packet semantics. `UNSATISFIABLE` must be a terminal assembly outcome for the current attempt, forcing caller fallback/reframing rather than blindly repeating the same defer.

Disposition: **ADOPT / ADD NON-LOOP FAILURE LAW**.

## D18 — Coarse-to-deep archive retrieval + selective exact

Research claim:

- first select relevant chapters/segments, then exact/scene/event evidence;
- exact archive remains separate;
- coarse selector miss requires fallback.

Risk:

- first-stage miss hides the needed segment.

R2.3 reconciliation:

> Adopt staged broad -> episodic/entity -> exact retrieval where long-range history is actually queried. Fallback is targeted escalation triggered by unresolved required evidence, not a global search on every turn.

Disposition: **ADOPT RETRIEVAL REALIZATION**.

## D19 — Typed selectors instead of keyword-only activation

Research claim:

- explicit refs, scope, actor presence, state predicates, chronology/thread membership and bounded dependencies outperform substring activation;
- recursion must have depth/budget/cycle caps.

Risk:

- selector layer can become a second rules engine/query language.

R2.3 reconciliation:

> Adopt a small registered selector/channel vocabulary tied to actual Context consumers. Keyword/semantic match may be one signal only. No universal graph/query language.

Disposition: **ADOPT / NARROW**.

## D24-delta — Participant/controlled-Actor scoped projection

Research claim:

- one shared canon must yield recipient-specific context/disclosure;
- filtering must precede ranking/budget, otherwise secret material may enter shared summaries/caches.

Canonical reconciliation:

- Step 4 already owns role/subject/player eligibility and disclosure;
- R2.2 reaffirms secret-safe discovery;
- R2.5 later owns multiplayer collaboration semantics.

R2.3 delta:

> Eligibility/currentness verification occurs before content representation is admitted into role-local allocation. Recipient/subject scope is part of the request/profile, not an after-the-fact redaction pass.

Disposition: **PARTLY INHERITED + ACTIVE REALIZATION DELTA**.

## S02 — Recurrence + recency + diversity ranking

Qualifier:

- revisit when candidate queues/retrieval ranking exists;
- risk is opaque heuristic.

R2.3 applicability:

- trigger is now true.

R2.3 interpretation:

> Use recurrence/recency/diversity only for budget-contending supporting/optional candidates after required packet closure. Do not let popularity heuristics override authority, eligibility or required evidence.

Disposition: **ADOPT FOR OPTIONAL RANKING ONLY**.

## S22 — Bounded dependency activation

Qualifier:

- dependencies may activate records;
- recursion requires depth/budget/cycle limits;
- risk is fan-out.

R2.3 interpretation:

> Adopt bounded typed dependency expansion. Expansion is scoped by request/purpose and remaining discovery budget; no transitive world-graph walk.

Disposition: **ADOPT**.

## S25 — Central token/cost accounting

Qualifier:

- subsystems should not invent independent char heuristics;
- provider may not expose exact tokenizer.

R2.3 interpretation:

> Adopt one ContextBudget/SizeEstimator contract. It may use exact provider data when available or a conservative centrally versioned estimate with uncertainty margin. No claim that ordinary ChatGPT exposes an exact tokenizer/capacity interface.

Disposition: **ADOPT CONTRACT / PHYSICAL PROFILE DOWNSTREAM**.

## S29 — Dry-run context assembly

Qualifier:

- primarily diagnostic/testing;
- cost is an extra interface.

R2.3 interpretation:

> Adopt side-effect-free dry run as the same deterministic assembly path with generation/commit disabled, returning ContextTrace and projected size/contents.

Disposition: **ADOPT**.

## S36 — Witness/knowledge-aware retrieval weighting

Qualifier:

- requires knowledge records;
- revisit at Actor-specific context.

R2.3 applicability:

- Step 4 `world.knowledge` exists and Actor context is an actual consumer.

R2.3 interpretation:

> For Actor/history candidates, subject-known/witnessed evidence is a typed relevance/eligibility signal stronger than mere textual mention. It does not increase objective factual authority.

Disposition: **ADOPT NARROWLY**.

## S40 — Fairness against positional starvation

Qualifier:

- repeated stable ordering can exclude the same candidate;
- random ordering harms reproducibility;
- deterministic starvation score preferred.

R2.3 analysis:

- fairness is real for multiplayer/large candidate sets;
- a persistent per-record starvation ledger would add derived mutable state before evidence proves need;
- required evidence must never depend on fairness ranking.

Current candidate disposition:

> Preserve deterministic fairness as an allocator requirement for optional/supporting sets. Prefer group/participant/category coverage and stable tie-breaking first. Add cross-turn starvation history only if evaluation proves same-candidate chronic exclusion.

Disposition: **ADOPT PRINCIPLE / DEFER PERSISTENT STARVATION STATE**.

## S48 — Explicit entity/Actor target as context hint

Qualifier:

- target improves precision but cannot bypass identity/eligibility;
- malicious target may try to pull secret entity.

R2.3 interpretation:

> Explicit target/reference is a high-value discovery seed, never authority or privilege escalation.

Disposition: **ADOPT**.

## S49 — Party-size-aware context budgeting

Qualifier:

- linear full-character expansion fails as party grows;
- relevance/scene participation should select `full -> compact` representations;
- risk is secondary-PC starvation.

R2.3 interpretation:

> Adopt representation scaling by current role/task participation and material dependency. Do not guarantee full PC/NPC sheets for every participant in every bundle.

Disposition: **ADOPT**.

---

# 4. Relevant inherited / dormant items

## S20 — Pinned critical context

Current status:

- concept already exists through owner-declared exact protection / required evidence semantics;
- R2.3 may express it as packet/representation floor rather than a new generic pin subsystem.

Disposition: **INHERITED / REALIZED THROUGH REQUIRED PACKET FLOORS**.

## S23 — Visibility/secrecy distinction

Current status:

- already accepted in Step 4 and R2.2.

Disposition: **INHERITED**.

## S35 — Structured fact register

Original trigger:

- only as projection above canonical owners when an actual compact fact-index consumer exists.

R2.3 analysis:

- current INDEX/SCENE/source refs already provide narrower candidate routing;
- no independent generic fact register is required for baseline Context Runtime.

Disposition: **CONDITIONAL / DORMANT — NOT ACTIVATED**.

## S39 — Cache-aware rolling context

Original trigger:

- after deployment profile selection/provider caching capability.

R2.3 analysis:

- current ChatGPT Plus baseline does not provide a stable architecture-level prompt-cache contract we should assume here.

Disposition: **CONDITIONAL / DORMANT**.

---

# 5. Negative/adversarial evidence and resulting guardrails

## N01 — Whole WORLD/LOG/index preload

Failure:

- destroys lazy loading/token control and violates current runtime discipline.

Guardrail:

> First-tier discovery uses bounded compact routing surfaces and typed seeds; full owner loads are second-stage.

## N02 — Keyword-only activation

Failure:

- substring false positives/negatives and no semantic scope.

Guardrail:

> Keyword/semantic match is at most one discovery signal; typed refs/scope/dependencies govern the deterministic boundary.

## N03 — Unbounded cascading dependencies

Failure:

- fan-out/cycles/context explosion.

Guardrail:

> Every dependency expansion is bounded by registered relation type + depth/work budget + cycle suppression.

## N04 — Fixed copied token percentages

Failure:

- rigid provider/model-specific behavior and wasted budget.

Guardrail:

> Use policy floors/soft maxima under a supplied budget envelope; no copied percentages become canonical.

## N05 — Partial decision packet

Failure:

- valid-looking but semantically unreliable LLM decision.

Guardrail:

> Required packet reaches certified minimum representations or assembly returns controlled unsatisfied/degraded result.

## N06 — Global search as normal fallback

Failure:

- makes every turn expensive and defeats bounded discovery.

Guardrail:

> Escalation is targeted and request-triggered. Global/broad search is a bounded exceptional path only when an unresolved required dependency cannot otherwise be located and the source contract permits it.

## N07 — Duplicate context channels

Failure:

- same fact appears through current owner + Story + scene summary + event history, consuming budget and creating artificial confidence.

Guardrail:

> Dedup is source/provenance/owner-aware. Current authority is not removed in favor of a derived paraphrase.

## N08 — Stale index false negative

Failure:

- omission from stale routing projection becomes fictional absence.

Guardrail:

> Index/manifest omission is not closed-world proof unless its exact current contract explicitly guarantees exhaustive coverage for that query scope.

## N09 — Secret-bearing candidate metadata

Failure:

- entity name/tag/summary leaks protected information before deeper filtering.

Guardrail:

> Deterministic discovery may use protected routing metadata internally, but role-local candidate projection exposes only eligibility-safe metadata/content.

## N10 — Common context blob for incompatible roles/recipients

Failure:

- private/secret evidence becomes logically available by convenience.

Guardrail:

> Each logical role/subject/player phase has its independently assembled eligibility result even inside one physical turn.

## N11 — Trace leakage

Failure:

- diagnostics reveal excluded secret material.

Guardrail:

> Full ContextTrace is development/operator evidence with explicit exposure control; player-facing explanations require a sanitized projection.

## N12 — Positional starvation

Failure:

- same supporting participant/source loses every tie.

Guardrail:

> Deterministic coverage/diversity/fairness rules apply after required correctness inputs; persistent starvation history is not baseline unless measured need appears.

## N13 — Exactness lost through compaction

Failure:

- exact-required phrase replaced by summary.

Guardrail:

> Owner-declared exact representation floor is non-downgradable.

## N14 — Defer loop

Failure:

- same impossible packet repeatedly returns defer without changing inputs.

Guardrail:

> Assembly failure is typed and terminal for the current request/budget profile; caller must select a different safe path, narrower task or explicit limitation rather than blind retry.

---

# 6. Emerging architecture synthesis

The evidence supports a **bounded multi-channel, packet-first Context Runtime** rather than a single monolithic scene manifest or repeated repository search.

Conceptually:

```text
RoleContextRequest
    role / subject / player / purpose
    pinned current routing/frontier
    explicit refs / current scope
    |
    v
DISCOVERY SEEDS
    CURRENT / SCENE compact refs
    explicit target/ref
    current live overlay/created/touched refs
    active thread/process/dependency refs
    entity INDEX routing hints
    Story/history coarse hints when historical retrieval is requested
    |
    v
BOUNDED CANDIDATE FRONTIER
    opaque source identity/type/routing
    discovery channels
    cheap scope/currentness hints
    no authority gained here
    |
    v
VERIFY ELIGIBILITY + CURRENTNESS
    role/subject/player/purpose
    routed source authority
    source-specific currentness
    |
    v
FORM COMPLETE NEED/PACKET
    owner/task-declared required evidence classes
    exact/semantic representation floors
    supporting/optional candidates
    |
    v
LOAD TARGETED SOURCES
    only candidates needed to satisfy packet or ranked support
    |
    v
ALLOCATE / DEGRADE
    required packet first
    certified representation downgrade where allowed
    optional ranking/diversity/fairness in remaining budget
    |
    v
RoleContextBundle + ContextTrace
```

Important synthesis consequences:

1. **Scene manifest is a seed, not the whole discovery architecture.**
2. **Entity indexes remain routing projections, not current truth.**
3. **Requiredness belongs to the consuming task/owner contract, not to a global LLM relevance score.**
4. **Eligibility/currentness precede role-local allocation; ranking cannot authorize a source.**
5. **Representation downgrade must be source/consumer-certified, not arbitrary summarization.**
6. **Dedup uses stable identity/provenance/typed coverage first; generic semantic clustering is not required.**
7. **Budget accounting is centralized but may be approximate/conservative under ordinary ChatGPT.**
8. **Dry-run and trace are built into the same deterministic assembly path.**
9. **An unsatisfiable required packet is a controlled runtime result, not permission to omit silently or loop forever.**

---

# 7. Material architecture decision remaining

One component-shape decision remains after extraction:

> **Should the R2.3 Context Runtime be scene-manifest-dominant, multi-channel packet-first, or query-on-demand/minimal-index?**

The evidence currently favors the middle option because it uses the user's desired scene/location lazy manifest as the primary cheap seed while preserving off-scene causal retrieval, live currentness, recipient eligibility and complete-packet correctness without requiring global scans.

The next artifact is the R2.3 Decision Brief.