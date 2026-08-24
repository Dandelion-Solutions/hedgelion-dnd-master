# R2.2 Resolution Gate — Actor Continuity, Cognition and Directed Relationships

Status: **R2.2 ARCHITECTURE CLOSURE GATE**

Date: 2026-08-24

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-canonical-spec.md`

Owner decision:

- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-owner-decision.md`

Adversarial review:

- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-adversarial-review.md`

---

## 1. Gate verdict

> **R2.2 MAY CLOSE.**

The owner-selected Source-Actor-Owned Sparse Continuity architecture survived adversarial review after AR-1 through AR-6 were incorporated into the canonical specification.

No unresolved R2.2 product decision remains.

No implementation is authorized by this closure.

---

## 2. Exit-criteria coverage

| Requirement | Closure evidence |
|---|---|
| stable foundation vs durable evolving vs transient Actor state | canonical §§1, 3 |
| exact boundary with `world.knowledge` | canonical §§1–2, LAW R2.2-2 |
| goals / objectives / intentions / commitments | canonical §§3, 5 |
| directed relationship semantics | canonical §4 |
| minimum useful relationship facets | canonical LAW R2.2-9/10 |
| evidence-bound persistent updates | canonical §6 |
| `NO_CHANGE` | canonical LAW R2.2-15 |
| sparse/event-driven cognition | canonical LAW R2.2-13/14 |
| transient expiry/refresh | canonical LAW R2.2-7/17 |
| progressive Actor depth / no over-modeling | canonical §7 |
| PC agency exclusions | canonical §8 |
| Story/history boundary | canonical §9 |
| explicit R2.3 source/discovery handoff | canonical §§10–11 |
| no duplicate semantic authority | canonical §§1–2 and adversarial review |
| adversarial review closure | `2026-08-24-r2-2-actor-continuity-adversarial-review.md` |
| unresolved/deferred/dormant work explicit | canonical §§12–14 and this gate §5 |

All required exit categories are represented.

---

## 3. Diamond / Strong accounting

| Item | R2.2 closure disposition |
|---|---|
| D10 stable/durable/transient | **ADOPTED / REFINED** — lifetime separation under one source-Actor owner; explicit foundation-transition barrier; inspectable transient invalidation. |
| D11 truth/knowledge/belief/intention | **PARTLY INHERITED + ACTIVE DELTA ADOPTED** — truth/epistemics remain Step 4; only missing non-epistemic Actor continuity added. |
| D12 directed relationships/player agency | **ADOPTED** — A->B independent; subjective facets source-Actor-owned; PC voluntary mental state protected. |
| D13 sparse/event-driven cognition | **ADOPTED** — no every-NPC/every-turn simulation. |
| S07 cognition modes | **ADOPTED AS SEMANTIC PURPOSES** — bounded purposes without a new orchestration framework. |
| S10 NO_CHANGE | **ADOPTED** — valid assessment with no forced state write. |
| S11 transient TTL | **PROBLEM ADOPTED / GENERIC TURN-TTL REJECTED** — owner/state/event/fictional-time invalidation instead. |
| D09 evidence-bound mutation | **SPECIALIZED APPLICATION ADOPTED** — bounded Actor-purpose delta + deterministic write-boundary validation. |
| S27 one mutation per assessment | **REFORMULATED** — one bounded Actor-purpose delta, potentially several coherent dependent fields. |
| S06 bounded active cast | **INHERITED / PRESERVED** — already owned by progressive materialization/runtime doctrine. |
| S08 protected core/selective forgetting | **CONDITIONAL / DORMANT** — trigger: demonstrated Actor-local context/storage pressure. |
| S09 staged evolution | **CONDITIONAL / DORMANT** — trigger: authored companions/major NPC arcs require explicit staged evolution. |

No active R2.2 research item is left without an architectural disposition or downstream owner.

---

## 4. Adversarial clarification closure

### AR-1 — subjective relationship vs objective social facts

Closed by canonical LAW R2.2-3/11.

### AR-2 — cumulative foundation drift

Closed by LAW R2.2-5 and foundation-transition validation in LAW R2.2-17.

### AR-3 — immortal transient state

Closed by LAW R2.2-7/17 requiring inspectable invalidation tied to existing state/time/event ownership.

### AR-4 — index omission as false absence

Closed by LAW R2.2-24: derived omission is not general closed-world evidence.

### AR-5 — stale campaign index during live authority

Closed by LAW R2.2-25: discovery/currentness follows routed authority and must account for live overlays/current owner state.

### AR-6 — location-only discovery and secret metadata

Closed by LAW R2.2-26/27: discovery is typed/multi-channel and eligibility-safe.

No adversarial finding remains unresolved inside R2.2.

---

## 5. Deferred / conditional work

The following do not block R2.2:

- concrete Actor schema fields / physical representation — R2.7 mapping + later implementation planning;
- high-cardinality relationship normalization — conditional on machine/performance evidence;
- richer retained private planning — conditional on a demonstrated consumer;
- selective Actor-core forgetting/pruning — conditional on demonstrated pressure;
- authored staged evolution — conditional on explicit major-NPC/companion arc requirement;
- concrete context candidate indexes/manifests/ranking/budget/dedup — **R2.3**;
- exact LLM cognition/orchestration phase placement — R2.4;
- multiplayer recipient/context integration — R2.5.

---

## 6. Mandatory R2.3 handoff — lazy discovery

Owner requirement:

> LLM/runtime context must lazy-load semantic detail to control context/token cost while retaining cheap awareness of potentially relevant actors/items/features/etc.

R2.3 must therefore design a bounded discovery-to-load pipeline with at least these properties:

```text
DISCOVER compact candidates
-> SELECT / VERIFY role/currentness/eligibility
-> LOAD only required semantic sources
-> PROJECT bounded decision context
```

It must explicitly address:

- scene/location relevance manifests;
- existing campaign INDEX surfaces;
- current/live routing and staleness;
- off-scene causal/thread relevance;
- false-negative protection;
- secret-safe candidate metadata;
- no global full-record scan/preload;
- token/cost-aware progressive representations;
- trace/explainability.

This is now a required R2.3 consumer constraint, not optional optimization.

---

## 7. Stage transition

R2.2 is ready for roadmap transition:

```text
R2.2  COMPLETE / ARCHITECTURE CLOSED
R2.3  IN PROGRESS
```

R2.3 must begin with a fresh task-specific Source Manifest and evidence extraction for Context Runtime, retrieval, allocation, lazy discovery and observability.

Broad implementation remains blocked.
