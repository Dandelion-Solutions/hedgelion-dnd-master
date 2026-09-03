# R2.7 WP-15 — Step 4 Collaborative Review

Status: **COLLABORATIVE REVIEW COMPLETE — NO HUMAN DECISION REQUIRED / READY FOR STEP 5**

Date: 2026-09-03

Reviewed direction:

> **NARROW PROCESS-NATIVE OWNERSHIP + DERIVED TEMPORAL AGENDA + OWNER-ANCHORED SPARSE CHRONOLOGY + ACCEPTED-EXECUTION CONTINUITY**

Input:

- Step-2 evidence extraction and open-world manifest expansion;
- Step-3 Decision Brief;
- repaired Step-1 package / SR15-01..03;
- explicit Senior GO constraints for Steps 2–8.

---

## 1. Review questions

The review challenged the Step-3 recommendation on five axes:

1. Does narrow `world.thread` admission accidentally reopen catalog/class architecture?
2. Can any existing specific process/temporal owner be stolen or duplicated by thread state?
3. Do chronology/frontier decisions require a new global storage/service decision?
4. Does retiring thread visibility lose a needed product behavior?
5. Are recovery, live conflict, fixed RNG and unsupported time-model boundaries preserved?

---

## 2. `world.thread` class challenge

### Concern

Current exact catalog-2.0 files omit `world.thread`, so admitting it could look like a new arbitrary record family.

### Evidence response

It is not arbitrary:

- shipped `PROCESSES.md` and `thread.schema.yaml` define independent identity/status/process state;
- scaffold contains `WORLD/THREADS` and `THREAD_INDEX`;
- closed WP-11 explicitly treats `world.thread` as a native routed family;
- `CATALOG_CONTRACTS.md` admits world records on independent responsibility/lifecycle, not on historical catalog presence alone;
- catalog generation 2.0 is unreleased and explicitly allows coordinated later-domain alignment.

### Review result

**PASS WITH NARROW QUALIFICATION.**

Candidate must say that `world.thread` exists only for independently identified generic processes that are not already owned more specifically. It must not infer one thread per deadline/clock/activity or require every off-screen consequence to become a thread.

Exact identifier syntax/allocation remains downstream machine realization constrained by the existing WP-11 route law and current catalog identity rules. WP-15 need not invent an allocator here.

---

## 3. Specific-owner theft challenge

The following assignments were attacked explicitly:

| Tempting thread capture | Required owner |
|---|---|
| mission stage/goal progress | `world.mission` |
| contract obligation/deadline | `world.contract` |
| effect expiration/periodic trigger | `world.effect` |
| persistent actor/asset resource recharge | owner ResourceState |
| stable LifeState recovery | `world.actor` |
| combat initiative/round/turn/action budget/local Procedure time | `runtime.procedure` |
| rest completion/progress | RestPolicy + owning rest Procedure/process |
| pending choice/reaction | `runtime.continuation` |
| accepted execution/randomness | Resolution/Continuation/Step-3 evidence |
| transient event/signal/boundary | source binding + embedded typed value + Step-3 execution |

Review result: **PASS** if candidate includes an explicit owner-precedence law:

> choose the already-admitted specific owner whenever it owns the responsibility; use `world.thread` only for the remaining independently identified generic process lifecycle.

References from a thread to these owners may express dependency/affected subjects; they do not copy current authoritative state.

---

## 4. Thread field challenge

### `state.progress`

Risk: a generic number becomes hidden global time or drama meter.

Resolution: progress is legal only when the process owner defines its semantic scale/segments and completion meaning. It is not chronology merely because it increases.

### `state.deadline`

Risk: current `object` becomes arbitrary timestamp or durable DUE flag.

Resolution: candidate requires an accepted typed owner-local temporal predicate/TemporalBinding. DUE is evaluated, not stored generically.

### `state.next_development`

Risk: prose self-executes or creates Dramaturg/planning authority.

Resolution: if retained, it is non-executable owner-local prospective metadata only. Actual transition still requires a lawful cause and accepted execution path.

### `state.resources`

Risk: duplicate Actor/Asset/Procedure ResourceState.

Resolution: only requirements/references are permitted; resource current state stays native.

### event IDs

Risk: `created_event_id` / `last_event_id` become chronology via numeric/lexical order.

Resolution: provenance/dependency references only; typed chronology relations decide order.

Review result: **PASS WITH THESE QUALIFIERS**.

---

## 5. SR15-03 visibility challenge

### Could removing thread visibility lose “who can see a threat” behavior?

No semantic product capability is lost. The required behaviors already decompose into existing owners:

- what a PC fictionally knows -> `world.knowledge`;
- what a human PLAYER was materially shown -> `runtime.disclosure`;
- what a logical role may consume now -> Step-4/R2.3 eligibility;
- what UI/index presentation chooses to display -> derived presentation/discovery policy after eligibility.

A writable `known_by_pc_ids` shortcut cannot represent stance/provenance and would duplicate `world.knowledge`. A writable `public` bit cannot prove either PC knowledge or delivery.

Review result: **PASS — RETIRE FROM CANONICAL WRITABLE THREAD STATE**.

Candidate may permit a derived/cache/projection implementation only if it is rebuildable and revalidated against current owner/eligibility evidence.

---

## 6. Chronology representation challenge

### Concern

Retiring `CURRENT.world_time.frontier` and singleton scene frontier might require choosing one new central chronology store now.

### Resolution

No. Step-5.9 already owns distributed sparse accepted chronology:

- stable anchors;
- typed cause/precedes/same-coordinate/elapsed evidence;
- owner/provider position evidence;
- sparse bridges only when material;
- derivative `ActiveExtensionFrontier(S)`.

WP-15 needs an implementation-facing semantic contract and field dispositions, not a mandatory centralized chronology service/table. Physical encoding may remain embedded with owning events/records or use a bounded typed representation consistent with WP-11/WP-12; later implementation planning chooses exact APIs/DDL after approval.

Review result: **PASS — NO CENTRAL CHRONOLOGY OWNER**.

---

## 7. Procedure/runtime under-realization challenge

`runtime-procedure-state.schema.json` currently does not materialize the full Procedure-local timing/order state described by Step 3 and `COMBAT.md`.

This is a real machine-realization gap, but not evidence to move combat timing into `world.encounter` or `world.thread`.

Candidate must preserve:

- `runtime.procedure` owner;
- owner-local boundary occurrences;
- typed elapsed consequences only when material;
- later coordinated schema/test realization.

No immediate implementation is authorized.

---

## 8. Recovery / conflict / RNG challenge

Attack cases reviewed:

- Agenda rebuilt after crash while occurrence already accepted;
- live CAS fails after deterministic prospective execution;
- repository campaign HEAD moves during persistence;
- host/session disappears and later restarts;
- a Continuation carries fixed RNG while chronology/provider evidence changes;
- a process deadline is reevaluated after source movement.

Required result in all cases:

- current native owner/currentness is revalidated;
- already accepted occurrence/execution identity is not replaced;
- fixed RNG and committed execution evidence are not rerolled/replayed;
- Agenda candidate may be reevaluated but cannot rematerialize an accepted occurrence;
- host/wall-clock absence never advances fictional time.

Review result: **PASS**.

---

## 9. Capability-boundary challenge

Candidate must continue to support, when owner/evidence contracts can represent them:

- deadlines/countdowns;
- independent/split-scene progression;
- differing temporal rates;
- forward jumps/stasis;
- bounded/exact elapsed evidence;
- late-established old relations;
- immutable-history time travel with forward-extensible causal ancestry.

Candidate must not silently claim baseline support for:

- rewriting accepted past;
- multiple authoritative branching worldlines;
- routine retrocausal mutation/causal loops;
- arbitrary timeline replacement/merge.

No technical Git-history rewriting or conflict repair may fake those semantics.

Review result: **PASS**.

---

## 10. Boundedness challenge

Ordinary evaluation must remain dependency-local:

- direct known-owner routing;
- narrow Agenda dependency keys;
- local chronology relation/provider evidence;
- material cross-scope bridges only;
- no full WORLD scan, full LOG scan, global timeline reconstruction, giant vector or campaign-wide temporal CSP.

If measured evidence later proves a performance issue, WP-24 owns optimization evidence. No speculative global structure is justified now.

---

## 11. Review outcome

No challenged point creates a product choice or material unresolved architecture tradeoff. All qualifications derive from accepted owners and current evidence.

```text
WORLD_THREAD_NARROW_OWNER:        ACCEPTED FOR CANDIDATE
SPECIFIC_OWNER_PRECEDENCE:        REQUIRED
THREAD_VISIBILITY_WRITABLE:       RETIRED IN CANDIDATE
GLOBAL_CLOCK_FRONTIER:            REJECTED
CENTRAL_SCHEDULER:                REJECTED
CENTRAL_CHRONOLOGY_OWNER:         REJECTED
BACKGROUND_FICTION:               REJECTED
ACCEPTED_EXECUTION_REPLAY:        REJECTED
FIXED_RNG_REROLL:                 REJECTED
CATALOG_ALIGNMENT:                DOWNSTREAM MACHINE DEBT
PROCEDURE_TIMING_ALIGNMENT:       DOWNSTREAM MACHINE DEBT
HUMAN_DECISION_REQUIRED:          NO
READY_FOR_STEP_5:                 YES
```
