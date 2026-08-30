# R2.3 — Context Runtime Resolution Gate

Status: **RESOLUTION GATE — READY TO CLOSE R2.3**

Date: 2026-08-24

Canonical spec:

- `2026-08-24-r2-3-context-runtime-canonical-spec.md`

## 1. Owner decision satisfied

Approved direction:

> **Bounded Multi-Channel Discovery + Packet-First Allocation**

Approved storage clarifications:

- deterministic physical sharding for plausible high-cardinality durable file-per-record collections;
- semantic identity remains independent of shard/path;
- current per-type indexes remain monolithic single-file routing projections;
- index partitioning is intentionally deferred as cheap dev debt until measured scale/host evidence triggers reconsideration;
- YAML/Git native records remain durable reconstruction/interchange representation under existing owner contracts;
- SQLite/HOT remains local execution/transaction/query realization and may physically host current established SOFT owner state without becoming a second durable canon.

## 2. R2.3 exit criteria

| Exit criterion | Result |
|---|---|
| Context remains projection, not owner | PASS |
| lazy discovery does not require full entity/history preload | PASS |
| scene/location acts as cheap primary seed without becoming closed-world oracle | PASS |
| off-scene dependencies have typed bounded discovery paths | PASS |
| currentness composes with live/HOT/native routing | PASS |
| recipient/role/subject eligibility precedes semantic admission | PASS |
| correctness-critical inputs form a complete bounded packet | PASS |
| packet closure may expand through registered dependencies without generic graph walk | PASS |
| legal representation downgrade/floors defined | PASS |
| required evidence wins budget before optional material | PASS |
| no provider-specific fixed percentages | PASS |
| bounded long-range history retrieval + exact escalation defined | PASS |
| deterministic trace/dry-run defined | PASS |
| explicit non-looping `UNSATISFIABLE` outcome defined | PASS |
| centralized size-estimator contract defined | PASS |
| sharding/index decisions do not create new semantic authority | PASS |
| monolithic index debt has explicit revisit trigger | PASS |
| YAML/SQLite authority boundary remains consistent with Step 5 | PASS |
| no new generic database/graph/vector/search subsystem introduced | PASS |

R2.3 architecture is therefore complete for its semantic scope.

## 3. Adversarial findings disposition

- **AR-1 packet closure staged dependencies** — incorporated as bounded typed required closure.
- **AR-2 discovery not closed-world proof** — incorporated; exhaustiveness requires owner contract.
- **AR-3 eligibility may need internal reads** — incorporated; minimum internal read separated from role evidence admission.
- **AR-4 HOT/SQLite authority ambiguity** — incorporated; owner authority distinguished from storage format/cache authority.
- **AR-5 monolithic index hot path** — incorporated; ordinary lookup does not require entity-directory enumeration.
- **AR-6 shard path coupling** — incorporated; stable ID remains semantic identity.
- **AR-7 fairness ledger overengineering** — persistent state remains unintroduced.
- **AR-8 broad historical fallback** — escalation is dependency-specific and bounded.

No unresolved adversarial blocker remains.

## 4. Diamond / Strong disposition summary

| Idea | Final R2.3 disposition | HDM result |
|---|---|---|
| **D02 — context as materialized projection** | **APPLIED / existing principle realized** | Step-4 Context Assembler becomes concrete bounded discovery/retrieval/allocation runtime; context remains ephemeral/non-authoritative. |
| **D03 — semantic allocator** | **APPLIED WITH SIMPLIFICATION** | One packet-first allocator, legal representation floors and centralized budget envelope. Copied fixed percentages rejected. |
| **D04 — context execution trace** | **APPLIED** | Restricted `ContextTrace` + same-path dry-run for diagnostics/tests; not prompt content or authority. |
| **D14 — complete decision packet** | **APPLIED AND STRENGTHENED** | Required input is bounded typed closure; partial correctness-critical truncation prohibited; `UNSATISFIABLE` is explicit/non-looping. |
| **D18 — coarse-to-deep retrieval + selective exact** | **APPLIED** | Broad Story/entity/thread hint → bounded episodic/history search → exact/native evidence only when required; no routine global scan. |
| **D19 — typed reactive selectors** | **APPLIED / NARROWED** | Small registered discovery-channel/dependency vocabulary tied to real consumers; no generic graph/query language. |
| **D24 — participant-scoped projection** | **PARTLY INHERITED + ACTIVE REALIZATION** | Step 4 owns disclosure/eligibility; R2.3 enforces eligibility before role-local semantic admission, including minimum internal checks. |
| **S02 — recurrence/recency/diversity ranking** | **APPLIED ONLY TO OPTIONAL SUPPORT** | Ranking helps budget-contending optional material; it cannot override requiredness/authority/eligibility. |
| **S22 — bounded dependency activation** | **APPLIED** | Typed staged dependency closure with finite bounds/cycle suppression. |
| **S25 — central token/cost accounting** | **APPLIED AS LOGICAL CONTRACT** | One `SizeEstimator/ContextBudgetEnvelope`; physical tokenizer/host details remain R2.4/R2.6. |
| **S29 — dry-run context assembly** | **APPLIED** | Side-effect-free same-pipeline assembly with trace. |
| **S36 — witness/knowledge-aware retrieval** | **APPLIED NARROWLY** | Subject knowledge/witness state influences eligible relevance for Actor/history context, not objective factual authority. |
| **S40 — anti-starvation fairness** | **APPLIED PRINCIPLE / PERSISTENT STATE REJECTED FOR NOW** | Deterministic coverage/fairness among optional peers; no starvation ledger until evaluation proves need. |
| **S48 — explicit target as context hint** | **APPLIED** | Strong discovery seed; never permission/authority escalation. |
| **S49 — party-size-aware budgeting** | **APPLIED** | Representation scales toward compact/reference forms rather than linearly loading every participant in full. |
| **S20 — pinned critical context** | **INHERITED / SATISFIED BY FLOOR SEMANTICS** | Required/protected minimum representation prevents eviction until consumer dependency is discharged. |
| **S23 — visibility/secrecy semantics** | **INHERITED** | Step 4/R2.2 already own distinction; R2.3 enforces it in discovery/admission. |
| **S35 — structured fact register** | **CONDITIONAL / DORMANT** | No generic fact index created. Revisit only if a concrete projection consumer proves need. |
| **S39 — cache-aware rolling context** | **CONDITIONAL / DORMANT** | Revisit only after a real host/model caching contract exists and R2.6 evidence supports it. |

## 5. Additional owner-approved implementation debt

### Monolithic indexes

Disposition: **CONSCIOUS CHEAP DEV DEBT / NOT CURRENT WORK**.

Reason: current scale does not justify partitioning complexity and indexes are rebuildable projections.

Revisit when one of the following becomes true:

- measured index file size or load latency is operationally material;
- realistic large-campaign evaluation shows lookup/budget pressure;
- host/API file/tool limits make one index artifact unreliable;
- maintenance/rebuild cost becomes materially dominant.

Until then, do not create index-of-indexes, buckets or partition registries.

### Durable record sharding

Disposition: **APPROVED PHYSICAL CONSTRAINT / EXACT MAPPING DEFERRED TO R2.7**.

R2.7 must determine which concrete record families are flat vs sharded and the deterministic path rule without changing semantic refs/owners.

## 6. Downstream handoff

R2.4 receives:

- registered logical `ContextNeedProfile` concept;
- bounded multi-channel discovery and packet closure;
- logical `RoleContextBundle` assembly outcomes;
- `UNSATISFIABLE` caller/fallback obligation;
- eligibility/currentness guarantees;
- size/budget envelope interface;
- no assumption that each logical role receives a physically separate model invocation.

R2.6 later validates the real ChatGPT Plus operating envelope.

R2.7 later maps files/shards/indexes/SQLite/tests/migrations.

## 7. Gate result

**R2.3 may be marked `COMPLETE / ARCHITECTURE CLOSED`.**

There is no remaining owner decision inside R2.3 scope.
