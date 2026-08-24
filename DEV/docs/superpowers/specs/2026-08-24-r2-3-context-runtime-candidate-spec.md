# R2.3 — Context Runtime Candidate Specification

Status: **CANDIDATE SPECIFICATION — OWNER DIRECTION APPROVED / ADVERSARIAL REVIEW REQUIRED**

Date: 2026-08-24

Owner decision:

- `2026-08-24-r2-3-context-runtime-owner-decision.md`

This specification defines logical Context Runtime semantics. It does not define concrete prompt topology, exact ChatGPT limits, final filesystem paths/shard widths or SQLite table layout.

## 1. Central architecture

HDM uses **Bounded Multi-Channel Discovery + Packet-First Allocation**.

```text
RoleContextRequest
    -> bounded typed discovery
    -> candidate frontier
    -> routed currentness + eligibility verification
    -> task-owned complete packet construction
    -> targeted semantic loads
    -> legal representation selection
    -> packet-first allocation
    -> RoleContextBundle + ContextTrace
```

Context Runtime is a deterministic projection capability. It stores no new truth and gains no authority from discovery, ranking, caching or prompt inclusion.

## 2. Request and need profile

A registered Context consumer supplies a logical request identifying, as applicable:

- role;
- purpose/task class;
- campaign/current routing basis;
- subject Actor(s);
- recipient/player scope where applicable;
- active scene/current scope;
- explicit typed refs/targets already resolved by an admitted binder;
- requested historical/exact dependencies where material.

A registered `ContextNeedProfile` owns the minimum complete semantic input required for that task class.

It conceptually declares:

- required evidence classes/refs;
- minimum legal representation floor for each requirement;
- allowed downgrade representations;
- supporting/optional categories;
- bounded discovery/dependency rules;
- safe failure/fallback class.

The LLM cannot invent a new need profile or self-authorize extra private evidence merely by asking for it.

## 3. Discovery-before-load

Potential relevance SHALL be discoverable from compact routing/selector metadata without first loading complete entity/history bodies.

Baseline discovery channels are:

- `CURRENT_SCOPE` — active scene/current subject/current PCs/current location;
- `SCENE_MANIFEST` — scene-local Actor/item/feature/thread refs;
- `EXPLICIT_REF` — typed target/entity/fact/history ref;
- `ACTIVE_DEPENDENCY` — registered active thread/process/owner/causal dependency;
- `LIVE_CURRENT` — current live overlay/created/touched routing evidence;
- `INDEX_LOOKUP` — compact per-type routing index;
- `HISTORY_HINT` — Story/semantic-history coarse hint when historical recall is materially requested.

This vocabulary is semantic, not final machine enum spelling.

Keyword/semantic matching may contribute candidate hints but is not a privileged discovery channel and cannot bypass typed identity, currentness or eligibility.

## 4. Scene/location is primary seed, not closed-world authority

Current scene/location is the cheapest and usually highest-yield discovery seed.

However, absence from scene/location metadata does not prove irrelevance or absence. Off-scene dependencies may be material through active threads/processes, explicit references, ownership/control relations, historical evidence or another registered causal dependency.

The Scene record SHALL NOT grow into a universal catch-all relevance database merely to avoid other discovery channels.

## 5. Bounded dependency expansion

One candidate may activate another only through a registered relation admitted by the current need profile.

Every expansion is bounded by:

- allowed relation kinds;
- maximum work/depth or equivalent finite cap;
- remaining discovery budget;
- cycle suppression;
- current request/purpose scope.

There is no generic recursive world-graph walk and no universal query language.

## 6. Routing metadata and indexes

Routing/index metadata is derived and non-authoritative.

Existing per-type `*_INDEX.yaml` files remain monolithic single-file routing projections under the current product profile.

An index entry may route through stable identity/path plus compact lookup metadata. It SHALL NOT duplicate complete entity semantics.

Index omission is not general proof of semantic absence unless a future explicit current exhaustive contract defines such a scope.

Index partitioning is intentionally deferred. Reopen only on measured large-campaign/file-size/latency/tool-limit evidence.

## 7. High-cardinality durable record sharding

Durable file-per-record collections with plausible high/unbounded cardinality SHALL support deterministic bounded sharding.

Properties:

- shard placement is derived from stable identity by an implementation-defined deterministic policy;
- sharding does not alter semantic identity, owner or authority;
- refs remain identity-based, not path-identity-based;
- routing/index metadata may carry the resolved path;
- Context Runtime follows routing and does not infer semantics from shard location;
- exact per-family path/shard policy is deferred to R2.7.

Naturally small collections remain flat unless real scale evidence justifies otherwise.

## 8. Routed currentness

A discovered candidate may originate from stale or derived routing metadata.

Before a material current-state claim is relied upon, Context Runtime resolves the proper current source under existing routing/currentness laws.

During live ownership, current live overlays/new entities/current refs supersede stale campaign-base discovery hints for the live-owned scope.

No index, Story unit, cached SQLite row or prior chat context can outrank the applicable current native owner.

## 9. Eligibility before role-local semantic use

Role/subject/player/purpose eligibility SHALL be resolved before candidate semantic content is admitted as evidence to the receiving logical role.

Consequences:

- ranking does not grant privilege;
- explicit user mention does not grant privilege;
- physical co-presence in one ChatGPT context does not grant logical eligibility;
- secret-bearing routing metadata must not be promoted into player-visible/role-ineligible content;
- recipient-specific filtering is not a late prose-redaction pass.

## 10. Packet-first correctness

Required evidence is determined by the registered task contract, not by a generic importance score.

Before optional/supporting context receives budget, the allocator SHALL establish the complete required packet at legal minimum representations.

If a required semantic dependency is unresolved, stale, ineligible or unavailable, the bundle is not silently treated as complete.

## 11. Representation floors

Logical representation classes may include:

```text
EXACT
FULL_STRUCTURED
COMPACT_STRUCTURED
SUMMARY
REFERENCE_ONLY
```

A source/consumer contract declares which forms are legal and the minimum floor for the current requirement.

Examples:

- exact protected wording may require `EXACT`;
- an incidental nearby NPC may initially be `REFERENCE_ONLY`;
- a material Actor decision may use a certified compact Actor projection rather than full biography/history;
- Story orientation may be `SUMMARY` until a material current/exact claim requires owner escalation.

The allocator may not summarize correctness-critical exact evidence below its declared floor.

## 12. Allocation

Logical order:

1. accept a downstream-supplied total context budget envelope including non-bundle reservations/margins;
2. satisfy the complete required packet at legal minimum representations;
3. add protected/high-value supporting evidence;
4. allocate remaining budget to ranked optional/supporting context;
5. stop before violating required output/safety margin.

Canonical architecture does not fix provider-specific percentages.

## 13. Optional/supporting ranking

Only budget-contending supporting/optional candidates are ranked heuristically.

Permitted deterministic inputs include:

- explicit/current task relevance;
- scene/scope participation;
- source/semantic class;
- semantically meaningful recency;
- recurrence where useful;
- diversity/coverage;
- subject knowledge/witness relevance;
- deterministic fairness among otherwise comparable candidates.

Required evidence never loses to optional ranking.

No global scalar importance score becomes semantic authority.

Persistent cross-turn starvation state is not baseline architecture. Add only if evaluation proves chronic deterministic exclusion that simpler coverage/fairness rules cannot solve.

## 14. Conservative deduplication

Deduplication SHALL rely on typed evidence such as:

- same stable source ref;
- same exact source slice;
- same proposition/owner identity;
- explicit projection/source coverage relation.

Generic semantic similarity alone is insufficient to collapse two facts.

Derived Story text does not displace a current owner merely because both discuss the same subject.

## 15. Progressive historical retrieval

Long-range historical retrieval proceeds progressively when needed:

```text
broad Story/entity/thread/segment hint
    -> bounded episodic/history candidate set
    -> exact/current owner evidence only when required
```

If a coarse stage cannot satisfy a required dependency, Context Runtime may perform a broader **bounded targeted** escalation for that dependency.

It SHALL NOT perform a whole-history/global campaign scan as the ordinary-turn fallback.

## 16. Budget and size estimation

R2.3 defines one logical `ContextBudgetEnvelope / SizeEstimator` contract.

A later physical host profile may supply exact token accounting if available. Otherwise the estimator uses a centrally versioned conservative estimate with uncertainty margin.

Subsystems SHALL NOT independently invent incompatible character/token heuristics.

## 17. Assembly outcomes

Every assembly attempt terminates as one of:

- `ASSEMBLED` — required packet satisfied at preferred/legal representations;
- `ASSEMBLED_DEGRADED` — required semantics satisfied, but legal compact forms and/or optional omission were necessary;
- `UNSATISFIABLE` — required packet cannot be established or fit at legal minimum under the current request/profile.

`UNSATISFIABLE` is terminal for that attempt. The caller must select a registered safe alternate path rather than blindly repeat the same impossible assembly.

Exact caller behavior belongs to R2.4/R2.6 integration.

## 18. Trace and dry-run

The same deterministic assembly path SHALL support side-effect-free dry-run.

`ContextTrace` conceptually records:

- request/need-profile identity;
- candidate source/ref;
- discovery channel(s);
- expansion path;
- currentness result;
- eligibility result;
- representation chosen;
- estimated size;
- packet membership;
- optional rank/fairness inputs;
- inclusion/exclusion/downgrade reason;
- logical bundle ordering;
- final assembly result.

Full trace is restricted operator/test evidence and may itself contain protected material. It is not automatically inserted into the role/player context.

## 19. YAML / SQLite boundary

R2.3 preserves existing persistence authority:

- Git-published native campaign files are the durable reconstruction/interchange representation according to their owner contracts;
- SQLite/HOT is local execution/transaction/query state and may contain hydrated copies, established-but-unpublished SOFT state, operational records, reverse indexes and derived caches;
- SQLite is not a second durable canon;
- a cached/indexed SQLite value cannot outrank the current native owner;
- publication materializes the coherent dirty native-file closure under Step-5 durability/publication rules.

Context Runtime may use SQLite indexes/caches as acceleration surfaces provided all currentness/authority rules above remain true.

## 20. Non-goals

R2.3 does not create:

- generic memory database;
- global knowledge graph;
- universal relevance/query language;
- provider-specific prompt cache architecture;
- mandatory vector database;
- independent context authority;
- partitioned index subsystem;
- background retrieval worker;
- full-world preload path.

## 21. Candidate laws

- **R2.3-L1** Context is a materialized logical projection, not storage authority.
- **R2.3-L2** Discovery precedes full semantic load.
- **R2.3-L3** Discovery is multi-channel and bounded.
- **R2.3-L4** Discovery metadata routes; it does not own truth or default closed-world absence.
- **R2.3-L5** Routed currentness wins before material reliance.
- **R2.3-L6** Eligibility precedes role-local semantic use.
- **R2.3-L7** Requiredness is registered task-contract-owned.
- **R2.3-L8** Complete required packet precedes optional context.
- **R2.3-L9** Representation downgrade is contract-bounded.
- **R2.3-L10** No fixed global context percentages are canonical.
- **R2.3-L11** Optional ranking cannot override requiredness, eligibility or authority.
- **R2.3-L12** Dependency activation is typed, bounded and cycle-safe.
- **R2.3-L13** Historical retrieval expands progressively and only as required.
- **R2.3-L14** `UNSATISFIABLE` is an explicit non-looping outcome.
- **R2.3-L15** ContextTrace/dry-run use the same deterministic assembly path.
- **R2.3-L16** Size estimation is centralized behind one logical contract.
- **R2.3-L17** Durable high-cardinality file collections support deterministic physical sharding without changing semantic identity.
- **R2.3-L18** Current per-type index files remain monolithic until a measured scale/host trigger justifies repartitioning.
- **R2.3-L19** SQLite/HOT may accelerate assembly but never becomes competing durable/context authority.
