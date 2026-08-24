# R2.3 Task Brief — Context Runtime, Retrieval, Lazy Discovery and Allocation

Status: **ACTIVE TASK BRIEF — R2.3 IN PROGRESS**

Date: 2026-08-24

Roadmap authority:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Upstream canonical architecture:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-canonical-spec.md`

Program evidence disposition:

- `DEV/docs/superpowers/research/2026-08-24-round-2-evidence-disposition-ledger.md`

---

## 1. Task classification

**Architectural / deep-work task.**

R2.3 defines the deterministic Context Runtime that discovers, verifies, retrieves, budgets and projects a bounded role-local working set over finite ChatGPT context.

No implementation is authorized.

---

## 2. Problem statement

Round 1/Step 4 already established Context Assembler as a deterministic logical projection capability and role/source eligibility boundary.

R2.1 established typed continuity source/lifecycle semantics without a generic memory authority.

R2.2 established source-Actor-owned sparse cognition and added an explicit owner requirement:

> LLM/runtime semantic detail must be **lazy-loaded** to control context/token cost while retaining cheap awareness of potentially relevant actors/items/features/etc.

Therefore R2.3 must solve two linked problems:

1. **Discovery:** know cheaply what may be relevant without reading/loading the entire campaign or every entity record;
2. **Decision context:** load only the complete eligible semantic evidence required by one logical role/task, under finite context/token pressure.

The design must not turn discovery indexes, summaries or Context Runtime itself into semantic authority.

---

## 3. Required end-to-end model

R2.3 must formalize a bounded pipeline equivalent in semantics to:

```text
CURRENT / SCENE / INDEX / EXPLICIT REFS / DEPENDENCIES / HISTORY HINTS
    |
    v
DISCOVER
    compact typed candidate metadata
    |
    v
SELECT / VERIFY
    role + subject/player + purpose
    eligibility + currentness + source contract
    |
    v
LOAD
    only semantic owners/evidence needed for the decision packet
    |
    v
ALLOCATE / DEGRADE
    complete minimum packet + optional context under token pressure
    |
    v
PROJECT
    RoleContextBundle
    + inspectable ContextTrace
```

No stage in this path gains canonical-state authority.

---

## 4. Primary decision questions

### 4.1 Candidate discovery / lazy loading

Determine:

- what a first-tier context candidate is;
- minimum discovery metadata needed before full source load;
- whether candidate metadata is scene-local, index-derived, query-derived, or a combination;
- how physical co-location, explicit refs, active threads, causal/process dependencies, ownership/relationship links and recent evidence contribute candidates;
- how potentially relevant NPCs/assets/features at a scene/location become discoverable without scanning all entity records;
- how off-scene but causally material entities enter the candidate set;
- how current/live routing modifies discovery;
- how stale/incomplete indexes degrade safely;
- when absence from an index can or cannot prove absence;
- how secret-bearing metadata is withheld until eligible;
- how candidate discovery remains bounded and avoids recursive graph explosion.

### 4.2 Candidate source/currentness/eligibility

Determine:

- source identity/revision/frontier metadata;
- role/player/PC/subject/purpose eligibility;
- currentness verification requirements;
- Story/history orientation versus native-owner escalation;
- Actor-private versus objective versus disclosure data;
- explicit entity/Actor targeting as a retrieval hint without privilege escalation.

### 4.3 Complete decision packets

Define which role tasks require a complete minimum evidence/constraint packet rather than partial truncation.

At minimum consider:

- Actor cognition mutation;
- mechanics interpretation where LLM semantic interpretation is involved;
- secret-sensitive classification/disclosure;
- consequential Dramaturg/Actor decisions;
- other decisions where omitted evidence can change correctness.

Specify what happens when the minimum packet cannot fit.

### 4.4 Semantic allocation and degradation

Determine:

- semantic budget classes;
- minimum reservations versus maximum/soft budgets;
- `required | protected | downgradable | omittable` or a better minimal vocabulary;
- allowed representation ladders such as exact/full -> compact -> emergency summary/reference;
- whether fixed quotas are avoided in favor of model/task-aware policy;
- party-size scaling;
- fairness/starvation control;
- ordering/placement separate from importance.

### 4.5 Retrieval depth

Reconcile:

- R2.1 broad Story orientation;
- episodic/history retrieval;
- entity-local view;
- Step-5.11 selective exact evidence;
- D18 coarse -> exact retrieval concept;
- fallback/global search when a coarse selector may miss the needed segment.

R2.3 defines retrieval policy, not a new history authority.

### 4.6 Dedup and source precedence

Define how semantically overlapping material from:

- current native owners;
- Story;
- SemanticEvents/runtime messages;
- Actor continuity;
- explicit exact evidence;
- scene summary/discovery metadata

is prevented from consuming context repeatedly or conflicting ambiguously.

Dedup must not collapse legitimately distinct propositions/sources.

### 4.7 Token/model-limit accounting

Determine a centralized token/cost estimate contract compatible with ordinary ChatGPT operation where exact provider tokenizer/runtime metrics may not always be exposed.

Do not allow each subsystem to invent independent character-count heuristics.

### 4.8 Trace / dry-run / diagnostics

Define an inspectable ContextTrace sufficient to explain:

- candidate source/revision;
- discovery channel;
- eligibility decision;
- currentness status;
- matched selectors/dependencies;
- rank/priority/fairness inputs;
- budget class/reservation;
- chosen representation;
- included/excluded/deferred reason;
- final placement.

Trace itself may contain secrets and is not automatically player-visible.

R2.3 should support side-effect-free dry-run context assembly for tests/diagnostics.

---

## 5. Canonical constraints inherited from upstream

R2.3 must preserve at least:

- Context Assembler is deterministic projection, not canonical authority;
- physical availability != logical eligibility;
- one gameplay RoleContextBundle uses one coherent current campaign/source frontier as required by owner contracts;
- raw prior-role contexts are not transitively inherited;
- current semantic questions return to native owners;
- Story may orient but cannot establish current/source-specific material claims alone;
- source-bound does not imply current;
- projection/index omission does not imply semantic absence unless an exact exhaustive contract proves it;
- source Actor owns current non-epistemic Actor continuity;
- `world.knowledge` owns proposition stance;
- discovery must not require full entity loads;
- routed live authority/currentness beats stale campaign-base index data;
- discovery metadata cannot leak protected material merely to support lookup;
- archive availability is not preload permission;
- no campaign-wide scan permission is implied by Context Runtime.

---

## 6. Source Manifest

### 6.1 Process / sequencing

| Source | Role | Required inspection |
|---|---|---|
| `AGENTS.md` | repository governance | source/current-ref/document discipline |
| `DEV/DESIGN_PROCESS.md` | canonical process | evidence/synthesis/decision gates |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | HDM adapter | source manifest/item-level research rules |
| `DEV/PROJECT_MAP.md` | derivative locator | Context Runtime dependency subgraph |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | sequencing authority | R2.3 scope and downstream boundary |

### 6.2 Canonical architecture owners

| Source | Why required |
|---|---|
| Step-4 truth/knowledge/role-context/Story canonical spec | Context Assembler request/bundle/source manifest, role eligibility, no raw transitive inheritance |
| Step-4 single-context amendment | physical availability vs logical eligibility and current one-context law |
| R2.1 canonical continuity spec | Story/history/current-source escalation, exact vs semantic, projection-absence rule |
| R2.2 canonical Actor spec | Actor source classes, lazy discovery/currentness/secrecy handoff |
| relevant Step-5 currentness/live/chronology specs | routed source/frontier/currentness constraints |

### 6.3 Current runtime / machine neighbors

Inspect current owners/representations as evidence, not as architecture inertia:

- `GAME/CORE/AI_REASONING.md` — smallest authoritative working set / no whole-history preload;
- `GAME/CORE/SESSION.md` — compact resume/current working set;
- `GAME/CORE/LIVE_SCENE.md` — live currentness/routing where relevant;
- `GAME/SCHEMA/current_state.schema.yaml`;
- `GAME/SCHEMA/scene.schema.yaml`;
- `GAME/SCHEMA/live_scene.schema.yaml`;
- `GAME/CAMPAIGN/INDEX/NPC_INDEX.yaml`;
- `GAME/CAMPAIGN/INDEX/ITEM_INDEX.yaml`;
- `GAME/CAMPAIGN/INDEX/LOCATION_INDEX.yaml`;
- `GAME/CAMPAIGN/INDEX/SCENE_INDEX.yaml`;
- additional index/schema/runtime consumers discovered from these owners.

### 6.4 Primary active Dossier inputs

- D02 — context as materialized projection;
- D03 — semantic allocator/reservations/degradation;
- D04 — context assembly trace;
- D14 — complete decision packet before defer;
- D19 — typed reactive selectors;
- D24-delta — recipient/controlled-Actor scoped projection;
- D18 retrieval realization;
- S02 — recurrence/recency/diversity candidate ranking;
- S22 — bounded dependency activation;
- S25 — centralized tokenizer/token-cost service;
- S29 — dry-run context assembly;
- S36 — witness/knowledge-aware retrieval weighting;
- S40 — fairness against positional starvation;
- S48 — explicit entity/Actor targeting hint;
- S49 — party-size-aware context budget.

### 6.5 Relevant inherited / dormant candidates

Inspect where they constrain alternatives but do not activate new scope:

- S20 pinned critical context — already inherited from exact-protection semantics;
- S23 secrecy/visibility distinction — inherited Step 4;
- S35 structured fact register — dormant unless an actual compact fact-index consumer is required;
- S39 cache-aware rolling context — dormant unless selected host profile exposes useful prompt caching.

### 6.6 Negative/adversarial evidence

Include at least failure patterns involving:

- whole-world/whole-history preload;
- keyword-only activation;
- fixed copied context quotas;
- partial decision packets;
- recursive dependency fan-out;
- duplicate context channels;
- stale index false negatives;
- secret-bearing index metadata;
- context trace leaks;
- common context blob sent to roles/recipients with different eligibility;
- positional starvation;
- global scan as fallback for every turn.

---

## 7. Required R2.3 evidence ledger

Before a Decision Brief, produce an inspectable ledger containing for each material source/candidate:

```text
Source/item
Actual claim
Qualifier/applicability
Existing owner/constraint
R2.3 problem addressed
Conflict / extension / inherited / no-delta
Candidate disposition
Reason
Downstream consequence
```

For Dossier items preserve simplest form, strongest counterargument, risks and revisit triggers.

---

## 8. Mandatory analytical challenges

At minimum challenge candidate designs against:

1. **False-negative discovery** — stale/incomplete index hides a material entity.
2. **Global-scan fallback** — safety fallback destroys lazy-loading cost/token goals.
3. **Secret leakage** — candidate labels/metadata expose information before eligibility.
4. **Live staleness** — campaign index disagrees with current live overlay/created entity.
5. **Location tunnel vision** — remote but causal Actor/process is missed.
6. **Partial decision packet** — truncation yields plausible but wrong mutation/classification.
7. **Budget starvation** — stable ordering repeatedly excludes one relevant source/participant.
8. **Dedup collapse** — similar but distinct facts are merged incorrectly.
9. **Derived authority creep** — scene summary/index/Story becomes current truth by convenience.
10. **Trace leakage** — diagnostics reveal secrets or hidden private state.
11. **Tokenizer uncertainty** — exact budget assumptions cannot be observed on ChatGPT host.
12. **Party scaling** — context grows linearly with every PC/NPC regardless of relevance.
13. **Recursive activation** — dependency expansion becomes an unbounded graph traversal.
14. **Exactness loss** — compact representation accidentally substitutes for required exact evidence.
15. **Defer loop** — complete-packet requirement can never fit and the runtime stalls indefinitely.

---

## 9. Alternatives requirement

The Decision Brief must compare at least three credible Context Runtime shapes, including:

### A. Scene-manifest-first

Use a compact current scene/location manifest as the dominant discovery tier, then targeted owner loads.

Challenge: off-scene relevance and manifest maintenance/currentness.

### B. Multi-channel candidate index + typed selectors

Combine scene/local refs, global/reverse index hints, explicit references, active dependencies and semantic/history hints into one bounded candidate set before source load.

Challenge: more policy complexity and dedup/currentness handling.

### C. Query-on-demand with minimal persistent indexing

Keep few discovery projections and perform targeted source queries/search from explicit current scope each turn.

Challenge: latency/cost and risk of repeated broad searches.

The analysis may produce a hybrid/simpler alternative; these are comparison requirements, not preselected outcomes.

---

## 10. Exit criteria

R2.3 may close only when canonical architecture defines:

- candidate/discovery metadata and authority status;
- discovery channels and bounded expansion;
- lazy-load path from candidate to full semantic source;
- currentness/live-routing rules;
- role/subject/player/purpose eligibility;
- complete decision-packet contract;
- semantic allocation and representation degradation;
- retrieval depth/fallback/exact evidence rules;
- source-aware dedup;
- token/model-limit accounting contract;
- party-size/fairness/starvation handling;
- side-effect-free dry-run;
- secret-safe ContextTrace;
- failure/defer behavior;
- explicit R2.4/R2.5 handoffs;
- no new semantic authority;
- adversarial review closure;
- Diamond/Strong item disposition summary;
- unresolved/deferred/dormant work explicitly owned.

---

## 11. Current continuation point

```text
R2.3 status: IN PROGRESS
task brief: established
next activity: source extraction / R2.3 evidence ledger
broad implementation: BLOCKED
```
