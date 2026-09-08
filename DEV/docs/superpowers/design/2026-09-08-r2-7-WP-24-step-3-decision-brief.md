# R2.7 WP-24 Step 3 — Decision Brief

Status: **STEP 3 COMPLETE — SELECTED OWNER-COMPOSED PATH BUDGETS / TRIGGER-GATED OPTIMIZATION**

Date: 2026-09-08

Evidence basis: Step-2 reconciliation published at `388512e4bc14503a4fa0fb09d33469c1c88ce5bc`.

Human decision required: **NO**.

---

## 1. Decision to make

WP-24 must decide the architecture-level performance/scale posture for the accepted HDM runtime without redesigning already-owned semantics or inventing unsupported numeric budgets.

The decision is not "how many milliseconds/tokens/files should HDM allow?" Current owners do not provide a single global scalar and in several places explicitly reject one.

The real choice is which architecture policy controls:

- ordinary critical-path boundedness;
- special/maintenance path cost;
- campaign-growth surfaces;
- partition/cache/optimization activation;
- proof/measurement timing;
- failure/degradation when a bounded path cannot satisfy required semantics.

---

## 2. Alternatives

### Alternative A — One global numerical performance budget

Define one or more universal limits for turn latency, model tokens/context, repository calls, retries, file count or retained Story size.

**Advantages**

- simple dashboard/acceptance story;
- superficially easy to compare implementations.

**Disqualifying problems**

- no current owner supplies a valid universal number;
- `RUNTIME.md` explicitly rejects fixed token/time/step/complexity turn ceilings;
- R2.6 prohibits correctness dependency on exact hidden capacity telemetry;
- Story intentionally has no corpus-wide size quota;
- different paths have fundamentally different semantics and evidence classes;
- a global value could force correctness/required evidence below owner-defined floors.

**Disposition:** REJECTED.

### Alternative B — Owner-composed path budgets with trigger-gated optimization

Preserve existing hard laws and structural bounds per path; define WP-24 as the integration policy that classifies scaling surfaces, optimization triggers and proof classes without replacing their owners.

Core shape:

```text
ordinary path
    -> must remain owner-bounded / decision-scoped
    -> no unowned global scans or mandatory background service

special path
    -> bounded to its semantic scope
    -> measured after realization where cost matters

campaign-growing retained surface
    -> may grow if owner semantics require retention
    -> ordinary access remains bounded
    -> safe partition path exists before dead-end

optimization
    -> dormant until owner-defined measurement/trigger
    -> preserves identity/authority/currentness/eligibility

proof
    -> structural law now
    -> Class A current surface where meaningful
    -> Class B realized benchmark
    -> Class C real supported-host/product evaluation
```

**Advantages**

- composes every current owner;
- preserves correctness and product interactivity law;
- avoids premature physical architecture;
- allows real measurements to select implementation thresholds later;
- distinguishes total retained cardinality from per-operation boundedness;
- fits WP-22 evidence discipline.

**Costs / risks**

- no single universal "performance number" before implementation;
- later implementation planning must preserve multiple measurement/acceptance obligations;
- trigger evidence must be actively collected rather than assumed.

**Disposition:** SELECTED.

### Alternative C — Preemptive physical optimization

Partition current indexes, select Story shard/page topology, introduce generic caching/batching/retry policies or background processing now.

**Advantages**

- could reduce some future costs if assumptions happen to be correct.

**Disqualifying problems**

- WP-11 index partitioning is explicitly measurement-triggered;
- Story growth owner explicitly requires partitionability but leaves exact partition choice evidence-driven;
- no realized production Story corpus currently supports concrete shard layout/count/threshold selection;
- generic workers/schedulers/registries conflict with current negative architecture;
- additional caching can accidentally create authority/currentness/eligibility problems;
- premature choices add migration/version surface before evidence exists.

**Disposition:** REJECTED FOR CURRENT WP-24.

---

## 3. Selected architecture direction

**Alternative B — OWNER-COMPOSED PATH BUDGETS + TRIGGER-GATED OPTIMIZATION + STAGED PROOF.**

WP-24 will not create a universal performance authority. It will define one integration contract over existing owners:

1. **ordinary correctness paths stay bounded by semantic scope**, not total campaign size;
2. **accepted hard constraints remain hard** (notably PO-003/WP-19 zero-extra-serial capture and the 10 KiB per-file mutable-text cap);
3. **owner-supplied ergonomics guidance remains guidance**, not an invented SLA;
4. **campaign-growing retained corpora are permitted only with bounded operation and safe partitionability**;
5. **physical optimization is trigger-gated** and cannot change authority/identity/currentness/eligibility semantics;
6. **unprovable completeness fails/defer boundedly**, never by global scan;
7. **no mandatory background worker/heartbeat is introduced**;
8. **performance proof is claim-specific under WP-22** and meaningful empirical evaluation runs on the real implemented supported target.

---

## 4. Required path classifications

The candidate/final specification must distinguish at least:

### P1 — Ordinary turn fast path

- already-loaded CORE;
- already-loaded campaign working set where sufficient;
- no repository traffic merely for routine adjudication;
- finite targeted retrieval when a concrete dependency is missing;
- PO-003 basis capture remains in-band and zero-extra-serial in its scope.

### P2 — Instruction-cache construction/reconstruction

- initial exact-package full CORE+RULES preload;
- package-switch full rebuild;
- verified context-loss full rehydrate;
- never treat current 370,728 B measurement as final production forecast.

### P3 — Context acquisition

- finite registered discovery/closure;
- required representation floors first;
- no generic world graph walk;
- terminal `UNSATISFIABLE` and one finite caller alternative.

### P4 — Durability/publication

- bounded participating-source closure;
- coherent publication attempt;
- conflict/currentness amplification is bounded/failable rather than infinite retry.

### P5 — LIVE / multi-chat

- bounded per-target authority lookup;
- exact-source currentness;
- contention measured on realized target;
- no all-ref/all-LIVE scan or global lock/server introduced by WP-24.

### P6 — Collaboration

- bounded positive route companions + direct known-ID obligation;
- no global collaboration index/scheduler/presence heartbeat.

### P7 — Story opportunity check

- R2.4 envelope-level compact typed backlog/service-opportunity control;
- bounded, not a Story/history scan;
- distinct from actually executing catch-up.

### P8 — Story catch-up/publication

- bounded selected source window;
- may lag/yield to current response;
- no mandatory per-turn publication or background worker;
- total backlog/corpus may grow.

### P9 — Story retained corpus / physical persistence

- no corpus quota;
- per-file 10 KiB hard cap;
- direct LLM-facing ~250/251–300/>300 guidance only where applicable;
- deterministic safe partition path for every plausibly unbounded collection;
- concrete layout deferred to measurement/realization;
- exact archival oversized representation requires pre-admission exact partition/reconstruction semantics.

### P10 — Diagnostics/cleanup/ref residue

- question-bounded diagnostics;
- no background cleanup service;
- branch/ref deletion impossible;
- retained ref operational pressure measurable but never authority-bearing.

---

## 5. Optimization activation rules

A physical optimization may become active only when all applicable conditions hold:

```text
current owner permits the optimization class
AND current evidence proves the baseline has reached/materially approaches an operability trigger
AND the proposed optimization preserves semantic identity/authority/currentness/eligibility
AND the proof class matches the claim
AND any version/migration impact is handled by its owner
```

Examples:

- family-index partitioning: WP-11 measured size/transfer/host-tool trigger;
- Story partition activation: growth-bearing realized collection plus 10 KiB/whole-file replacement/transport/conflict/host evidence, while safe partitionability already exists as a requirement;
- retry tuning: realized contention data, preserving WP-13 bounded terminal behavior;
- alternate instruction-loading strategy: only if real-target evidence materially fails the current full-preload strategy and the accepted semantic instruction architecture is properly reopened;
- cache additions: only if measured benefit justifies them without turning cache presence into authority/currentness/eligibility.

No trigger is considered fired merely because future growth is possible.

---

## 6. Proof obligations selected

### Structural/specification proof now

Can establish:

- no global-scan dependency in accepted ordinary paths;
- direct known-ID routing;
- finite context closure/failure vocabulary;
- per-file 10 KiB rule;
- Story partitionability requirement;
- no background-worker correctness dependency;
- correct no-authority boundaries;
- trigger/defer logic.

### Class A — current surface

May measure only current concrete physical artifacts such as shipped CORE bytes/file count and current scaffold/index bytes. These measurements are not production forecasts.

### Class B — after realization

Measure, as applicable:

- instruction-cache construction mechanics;
- exact context discovery/hydration operation counts/volume;
- family-index transfer/parse behavior;
- publication object/ref operations and conflict rebuild;
- Story enumeration/catch-up/publication/shard routing;
- exact archive partition/reconstruction;
- physically retained ref operational/listing pressure.

### Class C — real implemented supported target

Evaluate, as applicable:

- end-to-end turn responsiveness;
- long-chat/context pressure;
- full-preload behavioral prompt pressure;
- procedural verbosity/unnecessary checks or retrievals;
- GM/NPC initiative and improvisation quality;
- real Connector latency and multi-chat contention;
- Story opportunity/catch-up interaction with visible response quality;
- supported-host degradation and `UNSATISFIABLE` behavior.

No preimplementation parallel MVP is authorized.

---

## 7. Why no Product Owner decision remains

The evidence does not leave two materially different product-semantic alternatives alive:

- Alternative A would invent unsupported product budgets and contradict accepted owners;
- Alternative C would activate explicitly dormant physical choices without evidence;
- Alternative B is the only direction that composes the accepted owner laws without adding a new product trade-off.

Therefore the remaining work is technical synthesis, cross-system consistency and specification—not human product judgment.

```text
HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
MATERIAL_RISK_ACCEPTANCE_REQUIRED: NO
```

---

## 8. Step-3 result

```text
WP24_STEP3_COMPLETE: YES
SELECTED_ALTERNATIVE: B
SELECTED_DIRECTION: OWNER-COMPOSED PATH BUDGETS + TRIGGER-GATED OPTIMIZATION + STAGED PROOF
NEW_GLOBAL_NUMERIC_SLA: NO
CONCRETE_STORY_SHARD_LAYOUT_SELECTED: NO
FAMILY_INDEX_PARTITION_SELECTED: NO
BACKGROUND_WORKER/SCHEDULER_SELECTED: NO
FULL_CORE_LOADING_STRATEGY_REOPENED: NO
HUMAN_DECISION_REQUIRED: NO
STEP4_AUTHORIZED_BY_EXISTING_GO: YES
IMPLEMENTATION_PLANNING_STARTED: NO
IMPLEMENTATION_STARTED: NO
```