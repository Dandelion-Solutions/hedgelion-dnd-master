# R2.3 Decision Brief — Context Runtime Discovery, Retrieval and Allocation Shape

Status: **DECISION BRIEF / OWNER DECISION REQUIRED**

Date: 2026-08-24

Task brief:

- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-lazy-discovery-task-brief.md`

Evidence ledger:

- `DEV/docs/superpowers/design/2026-08-24-r2-3-context-runtime-evidence-ledger.md`

Upstream canonical architecture:

- R2.1 continuity canonical specification;
- R2.2 Actor continuity canonical specification;
- Step-4 Context Assembler + single-context amendment;
- relevant accepted Step-5 currentness/Story/exact-history architecture.

---

# 1. Decision to make

R2.3 must choose the baseline shape of the deterministic Context Runtime that turns a role/purpose/current scope into a bounded `RoleContextBundle`.

The material question is:

> **What is the first-class discovery and allocation strategy that gives HDM true lazy loading without missing off-scene causal evidence, leaking secrets, silently truncating correctness-critical packets or falling back to whole-campaign scans?**

This decision does **not** choose concrete YAML fields, index sharding, tokenizer implementation, prompt ordering or ChatGPT host tool mechanics.

---

# 2. Facts established before the decision

## F1 — The Context Assembler already exists semantically

Step 4 already assigns deterministic role/purpose/subject eligibility and bounded source selection to Context Assembler.

R2.3 must realize that contract, not create a competing context owner.

## F2 — Lazy loading is already a runtime correctness requirement

Current runtime doctrine requires the smallest authoritative working set and explicitly rejects wholesale WORLD/LOG/INDEX/entity preload and unneeded recursive link following.

## F3 — HDM already has compact discovery surfaces

Current architecture provides reusable seeds:

- `CURRENT.active_scenes` and active threads;
- SCENE location/PC/thread/item/feature refs and actionable summary;
- compact per-type campaign INDEX files;
- explicit entity refs/targets;
- current live overlays/created/touched refs;
- Story/history indexes/refs where historical retrieval is requested.

The generic entity index is already defined as a routing structure compact enough to search without loading entity bodies.

## F4 — Scene/location alone cannot be exhaustive relevance

Material off-scene dependencies can include:

- an active antagonist/process;
- a thread or obligation;
- remote controller/owner/source;
- exact historical evidence;
- a fact referenced explicitly by the player;
- another typed causal dependency.

Therefore a scene manifest is necessary but insufficient as the only discovery path.

## F5 — Index omission is not default proof of absence

R2.1/R2.2 already prohibit treating omission from derived projection/index as semantic absence unless a current exhaustive contract specifically guarantees the queried scope.

## F6 — Currentness may be routed through live state

During a live epoch, campaign-base Actor/location/index state may be stale relative to live overlays/new entities/current authority.

## F7 — Required evidence must survive context pressure

Owner-declared exact evidence and correctness-critical semantic packets cannot be silently summarized or partially omitted merely to fit.

## F8 — Exact physical prompt topology belongs downstream

R2.3 determines logical bundle acquisition/ordering/representation. R2.4 determines the concrete single-turn instruction/phase topology; R2.6 validates actual ChatGPT host limits.

---

# 3. Alternative A — Scene-Manifest-Dominant Lazy Loading

Use the current scene/location manifest as the dominant Context Runtime index.

Conceptually:

```text
CURRENT -> active SCENE
    -> scene-local actors/items/features/threads
    -> load relevant entity records
    -> optional local history
    -> allocate bundle
```

A small number of explicit-reference escapes may fetch an off-scene entity directly.

## Advantages

- simplest runtime model;
- excellent common-turn cost;
- directly matches the owner's scene/location index intuition;
- easy to inspect/debug;
- low candidate count;
- natural fit for dungeon/social/combat scenes.

## Costs / risks

- scene manifest must either grow into a catch-all relevance database or miss off-scene causal dependencies;
- stale/incomplete scene manifests create dangerous false negatives;
- history/thread/remote-process retrieval becomes a growing collection of exceptions;
- split-party and cross-scene dependency cases become increasingly awkward;
- exact query such as “what exactly did X promise months ago?” does not naturally start from current scene membership.

## Assessment

Useful as a **primary seed**, but too narrow as the baseline Context Runtime architecture.

---

# 4. Alternative B — Bounded Multi-Channel Discovery + Packet-First Allocation — RECOMMENDED

Use the current scene/location manifest as the cheapest high-priority seed, but combine it with a small registered set of other typed discovery channels before full semantic loading.

Conceptually:

```text
RoleContextRequest
    |
    +--> current scene/location refs
    +--> explicit refs/targets
    +--> active thread/process/dependency refs
    +--> routed live refs/created entities
    +--> compact INDEX routing hints
    +--> Story/history coarse hints when requested
    |
    v
BOUNDED CANDIDATE FRONTIER
    |
    v
ELIGIBILITY + CURRENTNESS VERIFICATION
    |
    v
TASK-DEFINED COMPLETE PACKET
    |
    v
TARGETED LOAD
    |
    v
PACKET-FIRST ALLOCATION + SAFE DOWNGRADE
    |
    v
RoleContextBundle + ContextTrace
```

The important constraint is that this is **not** a generic graph engine or universal search language. Discovery channels are registered because an actual Context consumer needs them.

## 4.1 First-tier candidate descriptor

A candidate descriptor is routing/selection metadata, not semantic truth.

Conceptually it may expose to deterministic assembly:

```text
source_ref / entity_ref
source_class / entity_type
routing path/ref
one or more discovery channels
scope/thread/location hints when legally available
currentness/routing hint
source revision/frontier hint when available
representation capabilities after source resolution
```

Secret-bearing human-readable metadata is not automatically role-visible.

## 4.2 Discovery channels

Baseline semantic channels:

```text
CURRENT_SCOPE
    active scene / current subject / current PCs / current location

EXPLICIT_REF
    typed entity/fact/rule/history reference from accepted request/binder

SCENE_MANIFEST
    scene-local actor/item/feature/thread routing refs

LIVE_CURRENT
    current live overlay / created / touched / observable routing evidence

ACTIVE_DEPENDENCY
    typed active thread/process/owner/causal dependency

INDEX_LOOKUP
    compact per-type routing/index lookup

HISTORY_HINT
    Story/semantic-history coarse candidate when historical recall is material
```

Exact spelling is not yet machine schema.

Keyword/semantic matching may contribute a hint but is not a privileged channel and cannot bypass typed eligibility/currentness.

## 4.3 Bounded expansion

One discovered candidate may activate a registered dependency only when the consumer/profile admits that relation.

Every expansion has bounded work/depth and cycle suppression.

No “follow every referenced entity” behavior exists.

## 4.4 Eligibility before role-local content allocation

Candidate discovery can happen over internal routing metadata, but role-local semantic material enters the bundle only after role/subject/player/purpose eligibility is resolved.

Ranking does not grant privilege.

Explicit user mention does not grant privilege.

Physical model visibility under the single-context host does not grant logical eligibility.

## 4.5 Currentness before material reliance

A candidate may be discovered from stale/derived routing metadata.

Before a material current-state claim is used, Context Runtime follows the proper current source/routing contract.

During live ownership this includes live state/overlay currentness rather than blindly trusting campaign-base index fields.

## 4.6 Packet-first correctness

The consuming semantic task provides a typed need/profile describing its minimum complete input semantics.

Conceptually:

```text
ContextNeedProfile
    purpose
    required evidence classes/refs
    minimum representation floor per requirement
    allowed downgrade representations
    optional/supporting categories
    failure policy class
```

The profile is HDM-defined for registered task classes. It is not arbitrary LLM self-authorization.

Examples:

- Actor cognition mutation requires current source Actor continuity + relevant eligible evidence + current `world.knowledge` where material;
- exact-wording adjudication requires the declared exact source slice;
- secret-sensitive disclosure requires the relevant disclosure/knowledge/current-observation packet;
- semantic mechanics interpretation requires the minimum authoritative state/rules candidates required by that invocation contract.

## 4.7 Representation floors

A source/requirement may support a ladder such as:

```text
EXACT
FULL_STRUCTURED
COMPACT_STRUCTURED
SUMMARY
REFERENCE_ONLY
```

but only representations certified by the source/consumer contract are legal.

Examples:

- exact oath wording: `EXACT` floor; cannot summarize;
- nearby incidental NPC: `REFERENCE_ONLY` may be enough until interacted with;
- significant Actor decision: compact foundation/current-goal/relationship view may be enough without full biography/history;
- Story orientation: compact summary may be acceptable until exact historical evidence is requested.

The allocator may downgrade only to the declared floor.

## 4.8 Allocation order

Baseline order:

```text
1. reserve non-bundle/turn budget supplied by downstream host profile
2. satisfy required packet at legal minimum representation
3. add protected/high-value supporting evidence
4. spend remaining budget on ranked supporting/optional context
5. stop before violating output/safety margin
```

No fixed percentages are canonical.

Importance and physical prompt position remain separate concepts.

## 4.9 Optional ranking

For supporting/optional candidates, deterministic ranking may use:

- explicit/current task relevance;
- typed scope/scene participation;
- source/semantic class;
- recency where semantically meaningful;
- recurrence where useful;
- diversity/coverage;
- subject knowledge/witness relevance;
- deterministic fairness among otherwise comparable candidates.

Required evidence never loses to optional ranking.

No generic global scalar “importance score” becomes semantic authority.

## 4.10 Dedup

Dedup is conservative and typed.

Strong deterministic evidence includes:

- identical stable source ref;
- same proposition/owner identity;
- explicit projection/source coverage relationship;
- same exact source slice represented twice.

When current owner and derived Story both discuss the same subject, current owner is not removed merely because Story paraphrases it.

Generic semantic similarity alone is insufficient to collapse distinct facts.

## 4.11 Long-range retrieval

Historical retrieval uses progressive expansion:

```text
broad Story/segment/entity/thread hint
    -> bounded episodic/history candidate set
    -> exact source/evidence only when required
```

If the coarse stage cannot satisfy a required historical dependency, Context Runtime may escalate to a broader **bounded targeted** search for that dependency.

This is not a global search performed on every turn.

## 4.12 Budget estimation

R2.3 defines one logical `ContextBudgetEnvelope / SizeEstimator` interface.

It may be supplied by R2.4/R2.6 with:

- known model/context profile when available;
- reserved instruction/turn/output margin;
- exact token estimate where available;
- otherwise centrally versioned conservative estimate + uncertainty margin.

Individual subsystems do not independently estimate chars/tokens.

## 4.13 Assembly outcomes

Baseline semantic outcomes:

```text
ASSEMBLED
    all required packet semantics satisfied

ASSEMBLED_DEGRADED
    all required semantics satisfied, but one or more legal compact representations used / optional evidence omitted

UNSATISFIABLE
    required packet cannot be established or fit at legal minimum under current request/profile
```

`UNSATISFIABLE` is terminal for the current assembly attempt.

The caller must choose a safe alternate path: narrower task, deterministic path, explicit limitation/clarification, different host/profile where supported, or another registered fallback. It must not blindly re-run the same impossible assembly.

Exact caller behavior is R2.4/R2.6 integration.

## 4.14 Trace / dry-run

The same deterministic pipeline can run without generation/commit and return:

```text
ContextTrace
    request/profile identity
    candidate source/ref
    discovery channel(s)
    currentness check/result
    eligibility result
    dependency expansion path
    selected representation
    size estimate
    packet membership
    rank/fairness inputs where applicable
    inclusion/exclusion/downgrade reason
    logical bundle ordering
    assembly result
```

Full trace is operator/test evidence and may itself contain protected information. A player-visible explanation, if ever desired, is a separate sanitized projection.

## Advantages

- satisfies the owner's scene/location lazy-loading requirement without making scene membership a universal relevance oracle;
- composes with existing CURRENT/SCENE/INDEX/live surfaces;
- preserves Step-4 eligibility and currentness before reliance;
- handles off-scene causal dependencies;
- supports exact historical retrieval without whole-history preload;
- makes context pressure deterministic and inspectable;
- naturally supports party-size scaling;
- no new semantic authority required;
- no provider-specific fixed token quotas required.

## Costs / risks

- more policy machinery than scene-only loading;
- candidate-channel overlap requires conservative dedup;
- malformed task profiles could over-require context;
- ContextTrace/diagnostics need secrecy handling;
- bounded expansion/search policies require careful testing to avoid false negatives.

## Assessment

Best fit with current HDM architecture and research evidence.

---

# 5. Alternative C — Query-On-Demand with Minimal Persistent Indexing

Keep only CURRENT/SCENE and basic IDs. Resolve most other relevance each turn using targeted repository search/query over canonical owners.

Conceptually:

```text
current scope
    -> formulate query
    -> search owners/history/indexes
    -> load matches
    -> allocate
```

## Advantages

- minimum persistent derived routing metadata;
- fewer index synchronization concerns;
- flexible for unusual questions;
- avoids designing much candidate metadata early.

## Costs / risks

- ordinary-turn latency/tool use grows;
- search may repeatedly examine large surfaces;
- ordinary ChatGPT/GitHub environment does not guarantee cheap semantic repository queries;
- false negatives become search-query quality failures;
- “if uncertain, search wider” tends to become global scan fallback;
- exact source/currentness/secret eligibility still require the same later machinery;
- difficult to make deterministic and reproducibly testable across host/tool evolution.

## Assessment

Useful as an exceptional targeted fallback, not a baseline runtime architecture.

---

# 6. Recommendation

Choose **Alternative B — Bounded Multi-Channel Discovery + Packet-First Allocation**.

Confidence: **HIGH**.

Reason:

> HDM already has cheap scene/current/index routing surfaces and already forbids whole-world preload. The missing architecture is therefore not “more memory”; it is a bounded deterministic frontier that combines those routing hints with explicit/off-scene dependencies, verifies authority/eligibility/currentness, and then spends context budget only on a complete task-defined evidence packet plus ranked support.

This preserves the owner's lazy-loading goal while avoiding the two failure extremes:

```text
scene-only false negatives
        <--- recommended B --->
repeated/global search cost
```

---

# 7. Proposed R2.3 laws if B is approved

## R2.3-L1 — CONTEXT IS A MATERIALIZED LOGICAL PROJECTION

Context Runtime produces bounded role-local execution evidence; it stores no new truth.

## R2.3-L2 — DISCOVERY PRECEDES FULL LOAD

Potential relevance must be discoverable from compact routing/selector metadata without loading complete semantic entity/history bodies.

## R2.3-L3 — DISCOVERY IS MULTI-CHANNEL AND BOUNDED

Scene/location is the primary cheap seed but not the only relevance channel. Registered explicit/dependency/live/index/history channels may add candidates under bounded expansion.

## R2.3-L4 — DISCOVERY METADATA IS NOT AUTHORITY

Candidate/index/manifest contents route to owners; they do not override current owner state or prove absence by omission unless an explicit exhaustive current contract says so.

## R2.3-L5 — ROUTED CURRENTNESS WINS

Material current claims resolve through the applicable routed current source, including live overlays where current.

## R2.3-L6 — ELIGIBILITY PRECEDES ROLE-LOCAL CONTENT USE

Role/subject/player/purpose eligibility is resolved before candidate semantic content enters the role's logical evidence allocation. Ranking/explicit mention cannot grant eligibility.

## R2.3-L7 — REQUIREDNESS IS TASK-CONTRACT-OWNED

A registered semantic consumer/task defines minimum complete evidence requirements; Context Runtime does not invent correctness requirements from a generic relevance score.

## R2.3-L8 — COMPLETE PACKET BEFORE OPTIONAL CONTEXT

The allocator first satisfies the complete required packet at legal minimum representations, then spends remaining budget on supporting/optional material.

## R2.3-L9 — REPRESENTATION DOWNGRADE IS CONTRACT-BOUNDED

Exact/full/compact/summary/reference representations may substitute only when the source/consumer contract permits them. Exact-required evidence cannot be summarized away.

## R2.3-L10 — NO FIXED GLOBAL CONTEXT PERCENTAGES

Canonical architecture defines floors/soft maxima/policy classes, not copied provider-specific percentages.

## R2.3-L11 — OPTIONAL RANKING CANNOT OVERRIDE CORRECTNESS

Recency/recurrence/diversity/witness/fairness are ranking signals only among otherwise eligible non-required candidates.

## R2.3-L12 — DEPENDENCY ACTIVATION IS BOUNDED

No unrestricted recursive graph traversal. Every expansion has typed relation eligibility, work/depth limit and cycle suppression.

## R2.3-L13 — DEDUP IS SOURCE/PROVENANCE AWARE

Stable identity/typed coverage may suppress duplicate representations. Generic semantic similarity alone cannot erase distinct facts or current authority.

## R2.3-L14 — LONG-RANGE RETRIEVAL ESCALATES PROGRESSIVELY

Use coarse orientation/index -> bounded episodic/entity candidates -> exact evidence. Broader search is targeted exception when a required dependency remains unresolved.

## R2.3-L15 — ONE CENTRAL BUDGET ESTIMATION CONTRACT

Context size/model-limit estimates are supplied through one versioned contract with explicit uncertainty; individual subsystems do not invent incompatible estimates.

## R2.3-L16 — PARTY SIZE SCALES REPRESENTATION, NOT AUTOMATIC PRELOAD

More participants/entities do not imply full representations for all of them. Relevance/task dependency chooses full/compact/reference form subject to required packet correctness.

## R2.3-L17 — ASSEMBLY FAILURE IS TYPED AND NON-LOOPING

If the minimum required packet cannot be established or fit, return `UNSATISFIABLE` for that attempt rather than silent truncation or blind repeated defer.

## R2.3-L18 — CONTEXT TRACE IS FIRST-CLASS DIAGNOSTIC EVIDENCE

Assembly decisions are inspectable through a secret-protected trace and side-effect-free dry run.

## R2.3-L19 — PHYSICAL PROMPT PLACEMENT IS DOWNSTREAM

R2.3 may order a logical bundle and provide placement classes/hints, but R2.4 owns exact single-context instruction/phase topology and R2.6 validates actual host effects.

---

# 8. Diamond / Strong disposition under recommended B

| Item | Recommended R2.3 result |
|---|---|
| D02 materialized context projection | **ADOPT / REALIZE** — concrete Context Runtime over existing Step-4 owner. |
| D03 semantic allocator | **ADOPT / REFINE** — packet floors + legal degradation; reject fixed copied quotas. |
| D04 context trace | **ADOPT** — operator/test trace, not automatic prompt/player content. |
| D14 complete decision packet | **ADOPT / REFINE** — complete minimum packet; typed non-looping `UNSATISFIABLE`. |
| D18 coarse-to-exact retrieval | **ADOPT** — progressive historical retrieval with targeted escalation. |
| D19 typed selectors | **ADOPT / NARROW** — registered discovery channels, no generic query/graph engine. |
| D24 participant-scoped projection | **PARTLY INHERITED + REALIZATION DELTA** — eligibility/currentness before role-local allocation. |
| S02 recurrence/recency/diversity ranking | **ADOPT NARROWLY** — optional/supporting ranking only. |
| S22 bounded dependencies | **ADOPT** — typed bounded expansion + cycle suppression. |
| S25 central tokenizer/token-cost | **ADOPT CONTRACT** — central estimator/profile with uncertainty; physical data downstream. |
| S29 dry-run | **ADOPT** — same deterministic pipeline without side effects/generation. |
| S36 witness/knowledge weighting | **ADOPT NARROWLY** — Actor/history relevance signal, not factual authority. |
| S40 fairness/starvation | **ADOPT PRINCIPLE / DEFER PERSISTENT LEDGER** — deterministic fairness first; persistent starvation history only if measured. |
| S48 explicit target hint | **ADOPT** — high-value seed, never privilege. |
| S49 party-size budget | **ADOPT** — relevance-dependent representation scaling. |
| S20 pinned critical context | **INHERITED** — represented as task/owner minimum representation floor. |
| S23 visibility/secrecy | **INHERITED** — existing Step-4/R2.2 law. |
| S35 structured fact register | **DORMANT** — no new generic fact index needed. |
| S39 cache-aware rolling context | **DORMANT** — await actual supported host caching profile. |

---

# 9. Exact owner decision requested

Choose one:

```text
A — Scene-Manifest-Dominant Lazy Loading
B — Bounded Multi-Channel Discovery + Packet-First Allocation  [RECOMMENDED]
C — Query-On-Demand / Minimal Persistent Indexing
```

Approval of **B** also approves the R2.3-L1 through R2.3-L19 direction for candidate-spec formalization.

It does **not** approve concrete schemas/index fields/sharding, physical prompt layout, provider token limits or implementation.