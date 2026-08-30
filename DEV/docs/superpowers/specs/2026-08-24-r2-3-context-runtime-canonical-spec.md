# R2.3 — Context Runtime, Retrieval, Lazy Discovery and Allocation — Canonical Specification

Status: **CANONICAL — R2.3 ARCHITECTURE CLOSED SUBJECT TO RESOLUTION GATE**

Date: 2026-08-24

Canonicalization basis:

- `../design/2026-08-24-r2-3-context-runtime-lazy-discovery-task-brief.md`
- `../design/2026-08-24-r2-3-context-runtime-evidence-ledger.md`
- `../design/2026-08-24-r2-3-context-runtime-decision-brief.md`
- `../design/2026-08-24-r2-3-context-runtime-owner-decision.md`
- `../design/2026-08-24-r2-3-context-runtime-candidate-spec.md`
- `../design/2026-08-24-r2-3-context-runtime-adversarial-review.md`

Owner-approved architecture:

> **BOUNDED MULTI-CHANNEL DISCOVERY + PACKET-FIRST ALLOCATION**

This specification realizes the Step-4 Context Assembler as a deterministic bounded Context Runtime. It defines logical discovery, retrieval, currentness, eligibility, packet closure, representation, allocation, trace and storage-routing constraints. It does not define final ChatGPT prompt topology, exact host limits, final filesystem shard mapping, SQLite table layout or implementation code.

---

## 1. Central invariant

Context is an ephemeral logical execution projection over durable/current owners and admitted derived evidence.

```text
RoleContextRequest
    -> bounded typed discovery
    -> candidate frontier
    -> minimum routing/currentness/eligibility resolution
    -> bounded required-packet closure
    -> targeted owner/source loads
    -> legal representation selection
    -> packet-first allocation
    -> RoleContextBundle + ContextTrace
```

Context Runtime stores no new truth and gains no semantic authority from discovery, ranking, caching, tracing or physical prompt inclusion.

## LAW R2.3-1 — CONTEXT IS A MATERIALIZED LOGICAL PROJECTION

A `RoleContextBundle` is a bounded logical execution product for one role/purpose/subject scope. Omission from one bundle does not imply loss from campaign memory/state, semantic absence or ineligibility in another role.

---

## 2. Registered request and need profile

A registered Context consumer supplies a logical request identifying, as applicable:

- receiving logical role;
- purpose/task class;
- campaign/current routing basis;
- subject Actor(s);
- recipient/player scope;
- active scene/current scope;
- explicit typed refs/targets already admitted by the applicable binder;
- requested historical/exact dependencies when material.

The consuming task class supplies a registered `ContextNeedProfile` defining:

- allowed discovery channels/relations;
- required evidence classes/refs;
- legal minimum representation floors;
- allowed representation downgrade forms;
- supporting/optional categories;
- finite dependency/discovery limits;
- safe failure/fallback class.

The LLM cannot create a new profile or enlarge private/secret eligibility merely by requesting more context.

## LAW R2.3-2 — REQUIREDNESS IS TASK-CONTRACT-OWNED

Correctness-critical requiredness belongs to the registered semantic consumer/task contract, not to a generic model relevance/importance score.

---

## 3. Discovery before full semantic load

Potential relevance must be discoverable through compact routing/selector metadata before complete entity/history bodies are loaded.

Baseline semantic discovery channels are:

- `CURRENT_SCOPE`;
- `SCENE_MANIFEST`;
- `EXPLICIT_REF`;
- `ACTIVE_DEPENDENCY`;
- `LIVE_CURRENT`;
- `INDEX_LOOKUP`;
- `HISTORY_HINT`.

Exact machine enum spelling remains implementation work.

Keyword/semantic matching may contribute a hint but never bypasses identity, currentness or eligibility.

## LAW R2.3-3 — DISCOVERY PRECEDES FULL LOAD

Full Actor/Asset/history/knowledge bodies are not prerequisites for merely knowing that a record may be relevant.

## LAW R2.3-4 — DISCOVERY IS MULTI-CHANNEL AND BOUNDED

Scene/location is the cheapest primary seed, not the sole relevance oracle. Every additional channel/expansion exists because a real registered consumer needs it and operates under finite work/depth/result bounds.

---

## 4. Scene/location and closed-world limits

Current scene/location is the default high-yield discovery seed.

However, off-scene material may matter through active threads/processes, ownership/control, explicit references, historical evidence or another typed causal dependency.

Scene records shall not become universal catch-all relevance databases.

## LAW R2.3-5 — BOUNDED DISCOVERY IS NOT GLOBAL CLOSED-WORLD PROOF

A bounded candidate frontier is the best admitted candidate set for the current request; it does not prove that no other campaign entity/fact exists.

If a consumer requires exhaustive scope, exhaustiveness must come from an authoritative/current owner contract for that scope. Derived indexes, Story and scene hints cannot manufacture an exhaustive guarantee.

---

## 5. Bounded dependency expansion and packet closure

A discovered/loaded record may activate another requirement only through a registered relation admitted by the current need profile.

Every expansion uses finite bounds and cycle suppression.

Required packet construction may be staged: loading one required owner may expose a registered mandatory dependency not known from the initial routing descriptor.

## LAW R2.3-6 — REQUIRED PACKET IS A BOUNDED TYPED CLOSURE

The minimum correct packet is not necessarily a static flat list. It is the finite closure of required owners/evidence under the consuming profile's admitted dependency relations.

The LLM cannot invent a new dependency relation. If required closure cannot be completed within legal semantics/currentness/eligibility or cannot fit at minimum representation, the attempt is not complete.

## LAW R2.3-7 — NO GENERIC WORLD-GRAPH WALK

Context Runtime does not recursively follow arbitrary refs, tags or prose associations. Dependency expansion is typed, purpose-scoped, bounded and cycle-safe.

---

## 6. Routing metadata and monolithic indexes

Routing/index metadata is derived and non-authoritative.

Existing per-type `*_INDEX.yaml` artifacts remain monolithic single-file routing projections under the current product profile.

An index entry may contain stable identity/path and compact lookup metadata but shall not duplicate complete entity semantics.

Ordinary Context Runtime lookup may load the applicable monolithic index artifact; it shall not require enumerating every physical entity file merely to answer an indexed lookup.

Index rebuild/audit is maintenance/recovery work, not ordinary hot-path lookup.

## LAW R2.3-8 — INDEX IS ROUTING, NOT SEMANTIC AUTHORITY

Index content may locate candidates. It does not override owners and omission is not semantic absence unless a future explicit exhaustive current contract says so.

## LAW R2.3-9 — INDEX PARTITIONING IS DORMANT DEBT

Current indexes remain monolithic. Reopen partitioning only when real large-campaign evidence, measured file-size/latency/tool-limit behavior or a concrete host/API constraint proves the single-file index operationally unacceptable.

No pre-emptive index hierarchy is introduced.

---

## 7. High-cardinality durable record sharding

Durable file-per-record collections with plausible high/unbounded cardinality shall support deterministic bounded physical sharding.

This applies to record families whose plausible campaign volume materially exceeds a bounded GitHub directory working set, such as append-heavy log/history and high-cardinality Actor/Asset/knowledge/event-like families where physically represented file-per-record.

Naturally small collections remain flat unless evidence later proves otherwise.

Exact per-family directory names, shard widths/arithmetic and migration tooling remain R2.7 machine-realization work.

## LAW R2.3-10 — SHARDING IS ROUTING-ONLY

Stable record ID remains semantic reference identity. Shard/bucket/path is storage routing metadata and cannot determine fictional location, kind semantics, chronology, ownership, relevance or authority beyond the storage-routing contract.

A future shard-policy migration may change paths without changing semantic IDs/refs, subject to ordinary migration/index consistency laws.

---

## 8. Routed currentness

A candidate may be discovered from stale/derived routing metadata.

Before a material current-state claim is used, Context Runtime resolves the applicable current owner/source under existing routing laws.

During live ownership, live overlays/new entities/current refs control the live-owned scope over stale campaign-base hints.

Story units, indexes, prior chat context and ordinary caches do not outrank current native owners.

## LAW R2.3-11 — ROUTED CURRENTNESS WINS

Material current reliance follows the current routed owner/source contract, not whichever candidate representation was discovered first or is easiest to query.

---

## 9. Eligibility and minimum internal reads

Some eligibility decisions require targeted reads of knowledge/disclosure/current-observation or owner policy state.

Deterministic assembly may perform the minimum internal read needed to resolve routing/currentness/eligibility. That internal read is not automatically admitted as semantic evidence to the receiving logical role.

## LAW R2.3-12 — ELIGIBILITY PRECEDES ROLE-LOCAL SEMANTIC USE

Role/subject/player/purpose eligibility must succeed before semantic material enters the receiving role's logical evidence allocation.

Ranking, explicit mention and physical co-presence in one ChatGPT context do not grant eligibility.

Secret-bearing routing/trace data remains internal unless independently eligible.

---

## 10. Packet-first allocation

The allocator first establishes the complete required packet at legal minimum representations.

Only then may remaining budget be spent on protected/high-value supporting evidence and ranked optional material.

## LAW R2.3-13 — COMPLETE REQUIRED PACKET PRECEDES OPTIONAL CONTEXT

Optional texture, background, popular entities or recency-ranked material cannot evict a correctness-critical required dependency.

---

## 11. Representation floors

Logical representation classes may include:

```text
EXACT
FULL_STRUCTURED
COMPACT_STRUCTURED
SUMMARY
REFERENCE_ONLY
```

A source/consumer contract defines legal forms and the minimum floor for each requirement.

Examples:

- exact protected wording may require `EXACT`;
- an incidental nearby NPC may begin at `REFERENCE_ONLY`;
- a material Actor decision may use a certified compact Actor view;
- Story orientation may use `SUMMARY` until current/exact evidence becomes material.

## LAW R2.3-14 — REPRESENTATION DOWNGRADE IS CONTRACT-BOUNDED

Context pressure cannot silently summarize exact-required or otherwise minimum-floor evidence below the consuming contract's legal floor.

---

## 12. Budget allocation and estimation

Logical allocation order:

1. accept downstream total-context envelope including instruction/output/safety reservation;
2. satisfy required packet at legal minimum representations;
3. add protected/high-value supporting evidence;
4. spend remaining budget on ranked optional/supporting material;
5. stop before violating required output/safety margin.

No provider-specific fixed percentages are canonical.

R2.3 defines one logical `ContextBudgetEnvelope / SizeEstimator` interface. Later host profiles may provide exact token data where available; otherwise use a centrally versioned conservative estimate with uncertainty margin.

## LAW R2.3-15 — NO FIXED GLOBAL CONTEXT PERCENTAGES

Canonical policy defines semantic floors/limits and allocation order, not copied provider-specific percentage quotas.

## LAW R2.3-16 — SIZE ESTIMATION IS CENTRALIZED

Subsystems do not independently invent incompatible token/character budgeting heuristics.

---

## 13. Optional/supporting ranking and fairness

Only budget-contending supporting/optional candidates use heuristic ranking.

Permitted deterministic signals include current task relevance, scene/scope participation, semantic/source class, meaningful recency/recurrence, diversity/coverage, subject knowledge/witness relevance and deterministic fairness among comparable candidates.

Required evidence is not ranked against optional evidence.

No global scalar importance score becomes authority.

Persistent cross-turn starvation state is not baseline architecture. Reopen only if evaluation proves chronic exclusion that simpler deterministic coverage/fairness rules cannot correct.

## LAW R2.3-17 — OPTIONAL RANKING CANNOT OVERRIDE AUTHORITY/ELIGIBILITY/REQUIREDNESS

Popularity, recurrence, recency and diversity influence only supporting/optional allocation within already legal candidates.

---

## 14. Conservative deduplication

Deduplication relies on typed evidence such as same source ref, same exact source slice, same proposition/owner identity or explicit source/projection coverage relation.

Generic semantic similarity alone is insufficient to collapse distinct facts.

Derived Story does not displace a current owner merely because both discuss the same subject.

---

## 15. Progressive historical retrieval

Long-range retrieval expands only when historical evidence is material:

```text
broad Story/entity/thread/segment hint
    -> bounded episodic/history candidate set
    -> exact/native evidence when required
```

Any broader escalation must name the unresolved registered dependency/question, eligible source family/domain, finite work/result bound and success/failure condition.

## LAW R2.3-18 — HISTORICAL ESCALATION IS DEPENDENCY-SPECIFIC AND BOUNDED

Failure of a coarse selector may trigger bounded targeted escalation; it does not authorize whole-history/global campaign scanning as an ordinary fallback.

---

## 16. Assembly outcomes

Every attempt terminates as:

- `ASSEMBLED`;
- `ASSEMBLED_DEGRADED`;
- `UNSATISFIABLE`.

`ASSEMBLED_DEGRADED` still satisfies all required semantics using legal representations; only optional/supporting material and/or preferred representation was reduced.

`UNSATISFIABLE` means required closure cannot be established or fit under the current request/profile.

## LAW R2.3-19 — UNSATISFIABLE IS NON-LOOPING

`UNSATISFIABLE` is terminal for the current assembly attempt. The caller must select a registered safe alternate path instead of blindly re-running the same impossible assembly.

Exact caller behavior belongs to R2.4/R2.6 integration.

---

## 17. Trace and dry-run

The deterministic assembler supports side-effect-free dry-run through the same discovery/currentness/eligibility/closure/allocation path.

`ContextTrace` conceptually records request/profile identity, candidates, discovery channels, expansion paths, currentness, eligibility, representation, size, required/optional membership, ranking inputs where relevant, inclusion/exclusion/downgrade reason, ordering and final result.

Full trace is restricted operator/test evidence and may contain protected material. It is not automatically inserted into the role/player context.

## LAW R2.3-20 — TRACE IS DIAGNOSTIC EVIDENCE, NOT PROMPT CONTENT OR AUTHORITY

Trace/dry-run must make false-negative, eviction, currentness and eligibility behavior testable without creating another gameplay state owner.

---

## 18. YAML / SQLite responsibility boundary

Authority is semantic-owner-relative, not storage-format-relative.

Git-published native campaign files are durable reconstruction/interchange representations according to their existing owner contracts.

During a live local runtime, current established owner state may be physically represented in HOT/SQLite and be newer than the last durable Git frontier. This is valid SOFT state under Step 5.5.

SQLite may also hold hydrated copies, execution/transaction state, reverse indexes, query indexes and derived caches.

## LAW R2.3-21 — SQLITE FORMAT DOES NOT CREATE AUTHORITY

SQLite may physically host current established owner state, but SQLite format itself is never the source of semantic authority.

A SQLite cache/index/projection does not outrank its semantic owner merely because it is local, fresh or fast.

If unpublished SOFT owner state is lost with the local environment, recovery returns to actual compatible durable native sources under Step-5 recovery laws; it does not pretend the lost state was durable.

## LAW R2.3-22 — DURABLE PUBLICATION MATERIALIZES OWNER STATE, NOT SQLITE AS CANON

Durability publication materializes the coherent required native-file delta from accepted current owner state through existing Step-5 publication contracts. The SQLite database is not committed as the campaign's durable canon/interchange format.

---

## 19. Non-goals

R2.3 does not introduce:

- generic memory database;
- global knowledge graph;
- universal query/relevance language;
- mandatory vector database;
- independent context authority;
- partitioned index subsystem;
- provider-specific prompt-cache architecture;
- persistent fairness ledger;
- background retrieval worker;
- full-world/full-history ordinary preload path.

---

## 20. Downstream obligations

### R2.4 — Single-Context LLM Execution

Must define how registered need profiles, typed handoffs, role rebinding and `UNSATISFIABLE` caller behavior fit inside one physical ChatGPT turn/context without violating logical eligibility.

### R2.6 — Assurance / ChatGPT profile

Must measure/evaluate context pressure, false-negative discovery, role leakage, estimator uncertainty, long-chat behavior and degradation paths against the current ChatGPT Plus host profile.

### R2.7 — Machine realization

Must map each record family to durable physical root, flat/sharded policy, deterministic shard rule where required, monolithic index ownership/path, SQLite hydration/query realization, migrations and tests.

Index partitioning remains dormant unless its explicit measured-scale trigger fires before then.
