# R2.7 WP-24 Step 4 — Cross-System Review

Status: **STEP 4 COMPLETE — SELECTED DIRECTION RECONCILED ACROSS CURRENT OWNERS**

Date: 2026-09-08

Selected direction from Step 3: **owner-composed path budgets + trigger-gated optimization + staged proof**.

Human decision required: **NO**.

---

## 1. Review method

The selected direction was challenged against the current owner graph rather than treated as a standalone performance policy.

Review dimensions:

```text
semantic authority
currentness / concurrency
persistence / durability
context / LLM execution
Story / retrospective continuity
multiplayer / collaboration
cleanup / retained residue
host capability
verification / empirical acceptance
version / migration boundary
```

The test is whether WP-24 can add scale/operability integration without weakening or duplicating those owners.

---

## 2. Context Runtime / ordinary gameplay

### Existing boundary

R2.3/WP-09 already require finite registered discovery, typed closure, required representation floors before optional allocation, one terminal `UNSATISFIABLE` outcome path and no generic campaign/history/world graph scan.

`RUNTIME.md` and `PLAY_POLICY.md` further define the already-loaded working-set fast path and require additional retrieval to have a concrete current-decision reason.

### Review conclusion

WP-24 must not invent a second context budget, separate per-subsystem token estimator or global context percentage. It may require measurement of realized packet size/operation count and later host calibration, but the semantic allocation policy remains R2.3/R2.6-owned.

```text
CONFLICT: NO
OWNER REOPEN: NO
WP24 ADDITION: proof/measurement/trigger integration only
```

---

## 3. PO-003 historical Actor basis

### Existing boundary

WP-19 `L38/L39` makes historical decision-basis capture an in-band byproduct of already-required decision work and preserves zero dedicated sequential LLM call, redundant admitted-data read or separate publication.

### Review conclusion

No performance optimization may move basis capture into a post-decision model call, background job or separate publication merely to simplify implementation. Conversely, WP-24 cannot impose a fixed turn time that forces basis loss.

Any future realization that proves an extra serial critical-path round trip is necessary is an explicit material escalation, not an implementation tuning detail.

```text
CONFLICT: NO
HARD LAW PRESERVED: YES
```

---

## 4. Full CORE instruction cache

### Existing boundary

R2.4/PLAY_POLICY/BOOTSTRAP_RUNTIME/WP-09 already select:

```text
initial exact package -> full CORE + RULES routing preload
package switch -> invalidate + full target rebuild
verified instruction loss -> full rehydrate
ordinary activation -> no CORE reread
```

### Review conclusion

WP-24 may measure physical corpus growth and must preserve a real-target behavioral/context/latency evaluation obligation. It may not replace full preload with lazy instruction loading merely because current source bytes appear large, nor may it treat the current 370,728 B source corpus as a production sizing forecast.

A later alternate loading proposal is legitimate only if real evidence fires a material revisit and the instruction architecture is explicitly reopened.

```text
CONFLICT: NO
LOADING STRATEGY REOPENED: NO
FUTURE EMPIRICAL TRIGGER PRESERVED: YES
```

---

## 5. WP-11/WP-12 routing and HOT

### Existing boundary

Known-ID reads derive an exact route; indexes are discovery-only; HOT/SQLite is non-authoritative local support. WP-11 keeps family discovery indexes monolithic until measured scale/host evidence fires its trigger.

### Review conclusion

WP-24 must not select index partitioning from route-space cardinality, current tiny scaffold indexes or anticipated future campaign size alone. A future partition scheme must preserve direct known-ID routing, identity validation and non-authoritative index semantics.

HOT/cache optimizations remain physical support; cache freshness cannot become semantic currentness.

```text
CONFLICT: NO
INDEX PARTITION SELECTED: NO
CACHE AUTHORITY INTRODUCED: NO
```

---

## 6. WP-13 publication/currentness

### Existing boundary

Campaign durability closure is bounded to selected roots/dirty scope/direct dependencies. Publication uses one frozen attempt, one coherent campaign tree, one single-parent commit and one final non-force ref transition. Conflict/ambiguity is owner/currentness-classified and automatic retry is bounded.

### Review conclusion

WP-24 may treat remote round trips, tree/commit/ref operations, repin/rebuild and currentness conflict amplification as cost dimensions. It may not change one logical publication into per-file writes, merge commits, staging refs, force updates or an unowned batching frontier merely for performance.

Exact retry count/latency threshold remains implementation/measurement work; architecture requires terminal bounded failure, not a new number.

```text
CONFLICT: NO
PUBLICATION AUTHORITY REOPENED: NO
```

---

## 7. LIVE / multiplayer contention

### Existing boundary

WP-16 requires bounded `WriteAuthorityLookup`, exact selected-source currentness and exact-source CAS. It rejects WORLD/all-ref/all-LIVE scans, generic leader/server/lease semantics and cross-domain freshness scalars.

### Review conclusion

Performance work may measure contention, refresh, CAS and conflict amplification but cannot introduce a global LIVE registry, total frontier or lock service as an optimization shortcut. Relevant movement remains owner-specific revalidation.

```text
CONFLICT: NO
GLOBAL LIVE INDEX/SERVER: NO
EMPIRICAL CONTENTION MEASUREMENT: DEFERRED UNTIL REALIZATION
```

---

## 8. Async collaboration

### Existing boundary

WP-17 requires durable collaboration only for bounded agency-dependent collective input. Recovery uses completeness-protected bounded PLAYER route companions plus direct obligation reads; no collaboration directory/index/scheduler/presence heartbeat is baseline.

### Review conclusion

Scale is participant/obligation-route fan-out, not a global queue. Performance pressure cannot justify silent contributor-set widening/narrowing, silence-as-input, or a global registry that becomes liveness/currentness authority.

```text
CONFLICT: NO
BACKGROUND COLLAB SERVICE: NO
```

---

## 9. Story service opportunity versus catch-up execution

### Existing boundary

R2.4 requires every ordinary TurnEnvelope to evaluate compatible Story backlog/service opportunity using compact typed metadata. WP-18/baseline source contracts require bounded source windows and allow catch-up to lag/yield to gameplay. There is no durable queue/worker/heartbeat.

### Review conclusion

WP-24 must preserve an explicit distinction:

```text
compact service-opportunity check
    != Story generation/catch-up/publication
```

The check is an envelope-level obligation but may not become an unbounded Story/history scan. `SERVICE(window)` runs only after correctness/agency/protected Narrator capacity is reserved; `DEFER(reason)` remains legal where prerequisites/capacity are unavailable. Catch-up conflict must yield rather than block visible response.

Therefore the phrase "Story is outside the ordinary critical path" is too broad if it erases the accepted opportunity check. The correct scale statement is that **Story catch-up execution/publication is not an unconditional per-turn critical-path requirement**, while the envelope-level opportunity decision remains compact and bounded.

This distinction will be normative in the candidate.

```text
OWNER CONFLICT FOUND: NO
WORDING HAZARD RESOLVED: YES
```

---

## 10. Story corpus growth / source registration geometry

### Existing boundary

The baseline source companion defines eight fixed registrations and independent EVENTS/NARRATIVE coverage over common event/relation native streams. Origin is LOCAL or selected LIVE epoch, with lane/origin-local cursors and no cross-lane/global ordering.

### Review conclusion

WP-24 must model scale as at least:

```text
registration
× admitted native origin
× lane/domain generation
× independent coverage state
```

without converting this geometry into a universal cursor or corpus quota.

A bounded source/read window proves only one operation is finite. Total backlog and total retained Story corpus remain campaign-growing by design.

```text
CONFLICT: NO
CORPUS-WIDE QUOTA: NO
GLOBAL STORY CURSOR: NO
```

---

## 11. Story growth/sharding owner

### Existing boundary

Every plausibly unbounded Story collection needs a safe deterministic bounded partition path. The owner explicitly leaves concrete layout/count/rollover threshold to later evidence/realization work.

### Review conclusion

This is stronger than "partition if convenient" but weaker than "partition now":

- **safe partitionability is mandatory architecture**;
- **activation point and concrete physical representation are evidence-driven**.

Physical partitioning may not become identity, chronology, eligibility, coverage or currentness. Retrospective consumers remain topology-neutral.

```text
CONFLICT: NO
CONCRETE SHARD LAYOUT: NOT SELECTED
SAFE PARTITION PATH: REQUIRED
```

---

## 12. Direct LLM-facing Story shape

### Existing boundary

Growth/sharding owner defines:

```text
~250 lines   preferred design ceiling
251–300      review zone
>300         not normal steady-state without explicit safe bounded-alternate-retrieval reason
```

It explicitly classifies line count as LLM/tooling ergonomics guidance, not byte/token/latency evidence.

### Review conclusion

The policy applies only to directly LLM-facing semantic units. It must not become a universal line-count limit for machine-facing structured control artifacts, which may be denser while still respecting 10 KiB and bounded-growth requirements.

```text
CONFLICT: NO
NEW SLA: NO
UNIVERSAL LINE LIMIT: NO
```

---

## 13. Exact archival edge

### Existing boundary

T-ARCH is MUST_MATERIALIZE for accepted exact archival commitments. The 10 KiB owner and Story growth owner both prohibit loss of required exact semantics to satisfy storage size.

### Review conclusion

An exact archive request cannot be accepted into a representation model that may require an indivisible >10 KiB mutable file unless owner/schema already supplies bounded exact partition/reconstruction semantics. Rejection/failure before admission is preferable to silently accepting an impossible exact promise.

This is an admission-safety law, not a request for WP-24 to design archive shards.

```text
CONFLICT: NO
PRE-ADMISSION GATE REQUIRED: YES
ARCHIVE SHARD LAYOUT SELECTED: NO
```

---

## 14. Cleanup and retained refs

### Existing boundary

WP-21/PO-006 prohibit branch/ref deletion absolutely. Ref retirement is logical; physical residue may remain indefinitely. Diagnostics are question-bounded.

### Review conclusion

Retained refs are not "bounded storage" and must not be described that way. The bounded property is that **ordinary authority/currentness/correctness does not enumerate or infer from all retained refs**. Operational pressure from repository residue remains measurable future evidence.

```text
CONFLICT: NO
PHYSICAL RESIDUE BOUNDED: NO
ORDINARY AUTHORITY DEPENDENCE BOUNDED: YES
REF DELETION REINTRODUCED: NO
```

---

## 15. Host and verification boundary

### Existing boundary

R2.6 rejects exact hidden-capacity dependence and requires real-MVP production-like evaluation after implementation. WP-22 keeps architecture, realization, verification and empirical acceptance distinct.

### Review conclusion

WP-24 canonical result must include a claim-to-proof matrix. It must not claim latency/context/behavior acceptance from current source measurements, scenario presence, maintenance audit or green CI.

No parallel MVP/benchmark surrogate will be created.

```text
CONFLICT: NO
WP22 PROOF BOUNDARY PRESERVED: YES
```

---

## 16. Version / migration impact

WP-24 Steps 2–8 are architecture documentation only. They do not change runtime schemas, storage generation, Story generation, package protocol or executable behavior.

Future physical optimization that changes compatibility-bearing layout/schema remains subject to the applicable Version Impact and WP-20 migration/adoption owner.

```text
CURRENT WP24 VERSION IMPACT: NONE
FUTURE OPTIMIZATION VERSION IMPACT: MUST BE RE-EVALUATED WHEN REALIZED
```

---

## 17. Cross-system review result

```text
WP24_STEP4_COMPLETE: YES
SELECTED_DIRECTION_CROSS_SYSTEM_CONSISTENT: YES
UPSTREAM_OWNER_REOPEN_REQUIRED: NO
NEW_SEMANTIC_OWNER_REQUIRED: NO
NEW_GLOBAL_PERFORMANCE_AUTHORITY_REQUIRED: NO
NEW_BACKGROUND_SERVICE_REQUIRED: NO
NEW_NUMERIC_SLA_REQUIRED: NO
CONCRETE_INDEX_PARTITION_REQUIRED_NOW: NO
CONCRETE_STORY_SHARD_LAYOUT_REQUIRED_NOW: NO
HUMAN_DECISION_REQUIRED: NO
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
STEP5_AUTHORIZED_BY_EXISTING_GO: YES
IMPLEMENTATION_PLANNING_STARTED: NO
IMPLEMENTATION_STARTED: NO
```

Proceed to Step 5 candidate specification.