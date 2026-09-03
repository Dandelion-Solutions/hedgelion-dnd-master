# R2.7 WP-15 — Temporal Owners / Processes / Chronology — Step-1 Task-Brief Critic

Status: **MANDATORY WHOLE-PROJECT TASK-BRIEF CRITIC — 3 BLOCKING + 9 SIGNIFICANT / ALL MECHANICALLY RESOLVABLE**

Date: 2026-09-03

Domain: **WP-15 — temporal owners / processes / chronology**

This critic evaluates the WP-15 Step-1 framing against the current dependency subgraph reconstructed from `DEV/PROJECT_MAP.md`, current accepted Step-3/Step-5 temporal architecture, closed WP-11..WP-14 machine-realization constraints, and actual CORE/schema/test consumers.

It does not reopen accepted architecture merely because current runtime/schema/test wording is stale.

---

## 1. Critic method

The critic attacks the framing bidirectionally:

```text
ARCHITECTURE -> MACHINE
accepted temporal/chronology laws
-> required runtime/schema/process/test destinations

MACHINE -> ARCHITECTURE
current temporal/chronology/frontier/process fields and behaviors
-> accepted owner/disposition
```

Required failure classes include duplicate authority, global scheduler/frontier reintroduction, fictional-order leakage from technical order, accepted-execution replay, unbounded temporal scans, recovery/currentness conflation, stale schemas/tests and missing downstream consumers.

---

## 2. Findings

### C01 — BLOCKING — four-way temporal responsibility split was not binding enough

**Problem**

A generic “temporal system” framing can collapse four already-separated responsibilities:

```text
NATIVE TEMPORAL OWNER
    owns obligation existence / current occurrence / arming / settlement / TemporalBinding

TEMPORAL AGENDA
    derived candidate/recheck routing only

CHRONOLOGY
    accepted typed relation / metric-position / bridge evidence

STEP-3 EXECUTION
    accepted consequence / Resolution / Continuation / fixed RNG / idempotency
```

Step 5.3 and the Step-5.3/5.9 integration amendment explicitly forbid Agenda or chronology from becoming a firing/job owner.

**Repair**

Make this four-way split a top-level Task-Brief invariant and a mandatory Step-2 evidence axis. Manifest must include Step 5.3 and the Step-5.3/5.9 integration amendment as direct canonical owners.

**Disposition:** AUTO_RESOLVED IN REPAIRED STEP-1 PACKAGE.

---

### C02 — BLOCKING — technical order/frontier non-authority perimeter was incomplete

**Problem**

The framing did not enumerate enough ways physical/operational order can leak into fiction or due evaluation.

The following are domain-specific technical evidence and cannot select fictional order, simultaneity, due status or elapsed fiction absent an explicit chronology owner contract:

- Git commit/ref/ancestry order outside its publication meaning;
- campaign/live HEAD and live revision/CAS order;
- SQLite row/insertion/transaction/timestamp order;
- storage/path/index order;
- host process/session/chat/message order;
- wall-clock elapsed time;
- SemanticEvent ID allocation order;
- Agenda/list/priority/traversal order;
- durability exposure/frontier/timer language;
- cleanup/retention age or GC eligibility.

Step 5.1 requires domain typing; Step 5.9 explicitly rejects transport concurrency/CAS as temporal equality and CAS winner as fictional winner.

**Repair**

Add an explicit technical-order non-authority matrix to the Task Brief and require Step 2 to trace every current `frontier`, clock/time, sequence/revision and ordering field in relevant runtime/schema surfaces to its exact semantic domain.

**Disposition:** AUTO_RESOLVED IN REPAIRED STEP-1 PACKAGE.

---

### C03 — BLOCKING — current machine/test debt was not forced into completeness accounting

**Problem**

A prose-only review could miss current machine surfaces that encode superseded chronology assumptions:

- `GAME/CORE/CHRONOLOGY.md` still describes singleton `chronology_frontier_event_id` and `CURRENT.world_time.frontier` as a globally reconciled chronology frontier;
- `GAME/SCHEMA/current_state.schema.yaml` / `GAME/CAMPAIGN/STATE/CURRENT.yaml` still carry `world_time.frontier`;
- `GAME/SCHEMA/scene.schema.yaml` still carries singleton `chronology_frontier_event_id`;
- `GAME/CORE/MULTIPLAYER.md` repeats global-ish chronology-frontier wording;
- `DEV/TESTS/CHRONOLOGY_CASES.md` C12/C13 still assert singleton/global frontier assumptions.

Step 5.9 has already retired/demoted those semantics in favor of typed sparse chronology and `ActiveExtensionFrontier(S)`, which may contain multiple anchors.

**Repair**

Step 2 must perform field/behavior/test-level reverse accounting over these surfaces before synthesis. Existing tests/scaffolds receive zero correctness presumption.

**Disposition:** AUTO_RESOLVED IN REPAIRED STEP-1 PACKAGE.

---

### C04 — SIGNIFICANT — Step-5.3/5.9 Agenda/chronology integration amendment was not mandatory

**Problem**

Reading Step 5.3 and Step 5.9 separately is insufficient to prove Agenda enrollment, invalidation and due-evaluation behavior.

**Repair**

Promote `DEV/docs/superpowers/specs/2026-08-21-step-5-3-5-9-temporal-agenda-chronology-integration-canonical-amendment.md` to mandatory canonical evidence.

**Disposition:** AUTO_RESOLVED.

---

### C05 — SIGNIFICANT — owner-approved temporal capability boundary was omitted

**Problem**

Without the accepted forward-extensible-history boundary, later synthesis could accidentally infer support for mutable-past rewrite, branching authoritative timelines or causal loops from chronology reconciliation machinery.

**Repair**

Add `DEV/docs/superpowers/design/2026-08-21-step-5-9-forward-extensible-time-boundary-owner-decision.md` as an owner-approved current decision despite its physical `design/` path. Require Step 2 to preserve supported forward-extensible scenarios and the explicit unsupported mutable-past/branching/causal-loop boundary.

**Disposition:** AUTO_RESOLVED.

---

### C06 — SIGNIFICANT — recovery/Agenda rebuild and duplicate-materialization route was under-specified

**Problem**

WP-15 can only be correct if Step-5.2 RRC and closed WP-14 recovery constraints are consumed directly:

- armed temporal roots remain discoverable through native routes;
- Agenda is rebuildable derived state;
- hydration/restart does not advance fiction;
- once occurrence G crosses accepted execution, it is not freshly materialized again;
- fixed accepted RNG/Continuation/execution identity resumes rather than rerolls/replays.

**Repair**

Make Step 5.2 and WP-14 final canonical result mandatory inputs and require an explicit recovery/no-rematerialization Step-2 axis.

**Disposition:** AUTO_RESOLVED.

---

### C07 — SIGNIFICANT — Step-3 execution/Continuation machine debt was missing

**Problem**

Temporal materialization crosses into Step-3 execution, but the framing did not force inspection of current execution schemas. In particular `DEV/SCHEMAS/runtime-continuation-state.schema.json` still requires generic `future_rng_frontier`, even though Step 5.3 says a universal future PRNG frontier is unjustified absent a concrete accepted reservation mechanic. `unconsumed_advancement` also requires exact owner/continuation disposition rather than becoming an elapsed-host-time surrogate.

**Repair**

Require Step-2 inspection of RuntimeCommand/Procedure/Resolution/Continuation/ExecutionSegment schemas, fixed RNG, pending-child and temporal advancement fields against Step-3/Step-5.3 authority.

**Disposition:** AUTO_RESOLVED.

---

### C08 — SIGNIFICANT — concrete native temporal-owner families were insufficiently represented

**Problem**

A generic chronology framing can miss actual owners for effect expiration/triggers, actor/asset resource recovery, stable LifeState recovery, Procedure boundaries/resources, rests and event/signal followups.

**Repair**

Add `DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md` and direct machine contracts including TemporalBinding, DurationSpec, BoundaryOccurrence, world Effect/Actor, Resource/Rest/Trigger/Signal and Procedure state/evidence schemas. Step 2 must map every admitted temporal family to native owner, binding/occurrence identity, derived enrollment and accepted consequence path.

**Disposition:** AUTO_RESOLVED.

---

### C09 — SIGNIFICANT — live currentness and fictional chronology boundary was not explicit enough

**Problem**

Current LIVE prose uses `frontier`, HEAD/revision and close/absorption transitions heavily. Step 5.8 makes those currentness/CAS/authority-transition evidence, while Step 5.9 says live source revision, close, absorption and successor opening do not themselves advance or order fiction.

**Repair**

Require Step-5.8 plus `LIVE_SCENE.md` / `MULTIPLAYER.md` reconciliation, with an explicit live-currentness-versus-chronology matrix. WP-16 remains future physical-live owner and is not started.

**Disposition:** AUTO_RESOLVED.

---

### C10 — SIGNIFICANT — field-level GAME chronology evidence route was incomplete

**Problem**

The framing needs auditable disposition of current chronology-adjacent fields, not a thematic summary.

Minimum Step-2 inspection must include:

- `current_state.world_time.frontier/display`;
- `SemanticEvent.world_order.time/sequence/scene_id`;
- `caused_by_event_ids` / `after_event_ids`;
- `scene.local_time` / `chronology_frontier_event_id` / `last_event_id`;
- live `revision`, `local_time`, observable-event `world_time`/identity;
- any current technical `frontier` term encountered in relevant consumers.

**Repair**

Add field/behavior-level accounting requirement and owner/disposition categories to Task Brief and Manifest.

**Disposition:** AUTO_RESOLVED.

---

### C11 — SIGNIFICANT — chronology retention/GC protection route was omitted

**Problem**

Chronology evidence can be compacted only while every protected consumer remains decidable. Step 5.13 forbids generic age/reachability/global-GC-frontier decisions and requires new consumer enrollment before dependence.

**Repair**

Add Step 5.13 as mandatory cross-system owner. Step 2 must map protected chronology consumers, bounded evidence routes, compaction/retention eligibility and derivative frontier/index lifecycle without turning GC into chronology authority.

**Disposition:** AUTO_RESOLVED.

---

### C12 — SIGNIFICANT — downstream verification/performance/consumer routes were incomplete

**Problem**

Step-1 framing must preserve, without activating, known downstream consumers:

- WP-16 live physical realization;
- WP-18 Dramaturg temporal-capability guard;
- WP-22 conformance/adversarial tests, including repair of stale C12/C13 chronology cases;
- WP-24 bounded chronology/Agenda/reconciliation performance measurement before optimization;
- WP-26 stale CORE/schema/routing documentation consistency where routed.

Ordinary chronology must remain local/bounded: no full campaign event scan, all-scene scan, global timeline rebuild, giant vector or campaign-wide temporal CSP.

**Repair**

Add typed downstream obligations and explicit no-activation boundary.

**Disposition:** AUTO_RESOLVED.

---

## 3. Whole-project consistency result

The critic found no accepted-architecture contradiction, no new unsatisfied product consumer and no material upstream insufficiency.

All findings are framing/completeness defects mechanically resolvable by consuming current accepted owners and actual machine/test consumers.

No human-owned product semantics, material trade-off or explicit risk acceptance is required in Step 1.

---

## 4. Final critic counts

```text
STEP_1_CRITIC_BLOCKING:     3
STEP_1_CRITIC_SIGNIFICANT:  9

UNRESOLVED_BLOCKING:        0
UNRESOLVED_SIGNIFICANT:     0
HUMAN_DECISION_REQUIRED:    NO
UPSTREAM_REOPEN_REQUIRED:   NO
```

C01-C12 are historical Step-1 critic findings. The repaired WP-15 Task Brief and Source Manifest incorporate every repair before Step-1 closure.

---

## 5. Gate

The critic authorizes publication only of the repaired Step-1 framing package and cursor update.

It does **not** authorize:

- Step 2 evidence extraction;
- candidate/spec synthesis;
- WP-16;
- implementation planning;
- runtime/schema/template/test implementation changes.

Next gate after coherent Step-1 publication is **MANDATORY SENIOR REVIEW**.
