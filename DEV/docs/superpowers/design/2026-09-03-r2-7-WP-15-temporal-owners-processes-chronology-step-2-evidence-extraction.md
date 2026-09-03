# R2.7 WP-15 — Step 2 Evidence Extraction

Status: **STEP 2 COMPLETE — SYNTHESIS COMPLETENESS GATE PASS / READY FOR STEP 3**

Date: 2026-09-03

Domain: **temporal owners / processes / chronology**

Starting verified ref for this extraction:

- `72259ceebcc36e95b01a5914559f154081e8a072`

Companion open-world manifest expansion:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-source-manifest-step-2-expansion.md`

This extraction consumes the repaired Step-1 package and `SR15-01..03`. It is evidence and disposition, not implementation and not a replacement for the owning upstream specifications.

---

## 1. Controlling architecture extracted

The current owner graph fixes four distinct responsibilities:

```text
NATIVE TEMPORAL OWNER
    owns obligation existence, current occurrence/lifecycle,
    owner-local binding/claim/settlement

TEMPORAL AGENDA
    rebuildable candidate/dependency recheck routing only

CHRONOLOGY
    sparse accepted typed cause/order/metric/bridge evidence

STEP-3 EXECUTION
    accepted consequence execution, Procedure/Resolution/Continuation,
    fixed RNG, committed segments and idempotency
```

Consequences:

- no Agenda entry, index, clock display, repository marker or cache can become a temporal obligation owner;
- no generic durable `due=true` exists;
- chronology evidence may make an owner predicate decidable, but the owner still returns `NOT_DUE | DUE | INDETERMINATE`;
- once an occurrence crosses accepted execution, recovery/retry/source movement resumes the same accepted identity and fixed RNG rather than rematerializing, replaying or rerolling;
- cold recovery rebuilds Agenda from current native owners and does not advance fiction.

No inspected current owner contradicts this split.

---

## 2. Native temporal/process owner accounting

| Concern / current representation | Native owner | Temporal/process disposition | Negative boundary |
|---|---|---|---|
| Effect intrinsic expiration | `world.effect` | `temporal_binding` is owner-local armed lifetime state | Agenda does not own expiration |
| Effect scheduled trigger next occurrence | `world.effect.scheduled_trigger_state[trigger_key]` | one owner-local next binding per admitted scheduled trigger | no generic callback/job scheduler |
| Actor persistent resource recovery | owning Actor ResourceState | ResourceState owns amount + valid `recovery_binding` | thread/process cannot copy current resource authority |
| Asset persistent resource recovery | owning Asset ResourceState | same owner-local recovery rule | no central recovery clock |
| Stable LifeState automatic recovery | `world.actor` LifeState progress/binding | Actor owns stable recovery state | no thread duplicate |
| Procedure round/turn/boundary/action-budget state | `runtime.procedure` | Procedure owns local order/resources/accepted boundary generation | `world.encounter` is not duplicate timing owner |
| Rest qualification/progress/completion | RestPolicy + owning rest Procedure/process | policy defines duration/completion semantics; active owner tracks progress | sleep/downtime alone does not create rest completion |
| Choice/reaction suspension | `runtime.continuation` | accepted suspended execution generation | no temporal queue owner |
| Accepted RNG | Resolution/Continuation accepted evidence | fixed across retry/recovery | never reroll because time/source was reevaluated |
| Event/signal/boundary follow-up | source binding + Step-3 accepted execution | transient `Signal`/`BoundaryOccurrence`/`TemporalBinding` are typed values | values do not become lifecycle owners |
| `world.mission` goal/stage/progression | `world.mission` | mission is already admitted independent progression owner | do not duplicate mission state in thread |
| `world.contract` obligations/deadlines | `world.contract` | contract owns its obligations/terms/deadlines | do not transfer contract obligation to thread |
| Generic independent threat/project/countdown/investigation/pursuit/process with its own identity/lifecycle and no more specific owner | `world.thread` | narrow independent process owner; may own stage/progress/dependencies and an owner-local typed temporal binding | `world.thread` is not universal temporal owner, chronology owner or scheduler |
| Harmless narration/travel with no material dependency | no new durable temporal owner | precision may remain coarse | no bookkeeping clock required |

### 2.1 `world.thread` admission/reconciliation evidence

Current evidence is internally split but mechanically reconcilable:

- `GAME/CORE/PROCESSES.md`, `GAME/SCHEMA/thread.schema.yaml`, `GAME/CAMPAIGN/WORLD/THREADS/`, `THREAD_INDEX.yaml` and `CURRENT.active_threads` represent an independently addressable durable process family;
- closed WP-11 already names `world.thread` as a native routed family at `WORLD/THREADS` with `THREAD_INDEX.yaml` as discovery-only index;
- current catalog-2.0 `CATALOG_INVENTORY.md`, `entity-structures.json` and `identifier-policies.json` do not yet admit/materialize `world.thread`.

Under `CATALOG_CONTRACTS.md`, independent responsibility + lifecycle is the admission test; serialization alone is insufficient. The shipped process family satisfies the lifecycle test for genuinely independent generic processes: stable identity, active/paused/terminal lifecycle, cross-turn/off-screen state and current WP-11 native routing. Therefore the current catalog absence is **coordinated machine-alignment debt**, not evidence that a generic independent process must be forced into another owner.

This does not admit blanket process ownership. Where `world.mission`, `world.contract`, `world.effect`, Actor/Asset ResourceState, Actor LifeState, `runtime.procedure`, rest Procedure/policy, Resolution or Continuation already owns the state, that owner remains controlling.

No human-owned decision is required to apply the existing class-admission law to this already-routed family.

---

## 3. `world.thread` field-by-field disposition

Current `thread.schema.yaml` is implementation evidence and requires later clean-slate alignment.

| Current field | Step-2 disposition |
|---|---|
| `id` | stable `world.thread` identity for an independent generic process; exact catalog/identifier materialization is downstream machine alignment |
| `status` | owner-local process lifecycle; active/paused/terminal distinctions are legitimate process state |
| `kind` | descriptive process class constrained to admitted machine vocabulary; it does not select temporal semantics by itself |
| `owner_entity_id` | association/provenance/control reference only; referenced entity does not inherit or surrender unrelated owner state |
| `objective` | process-local semantic description; not executable instruction |
| `state.stage` | current process-local stage |
| `state.progress` | only a process-local semantic measure/segmented clock with predefined in-world meaning; never generic elapsed time or drama meter |
| `state.next_development` | bounded prospective owner-local cue; cannot self-fire or replace actual causal conditions/accepted execution |
| `state.advancement_conditions` | owner-local dependency/predicate descriptors; not jobs and not execution |
| `state.deadline` | current generic `object` is under-specified machine debt; a surviving deadline must be a valid owner-local typed `TemporalBinding`/predicate and yields no durable `due` bit |
| `state.resources` | requirements/references only; current ResourceState remains with its native Actor/Asset/Procedure owner |
| `affected_entity_ids` | forward references only |
| `created_event_id` | provenance/causal-history reference only; ID magnitude/order is not chronology |
| `last_event_id` | provenance/latest-owner-transition reference only if retained; not chronology/currentness by ID |
| `visibility.known_by_pc_ids` | **RETIRE as canonical writable thread-owner state**; any convenience projection must be rebuildable/non-authoritative from current `world.knowledge` + eligibility evidence |
| `visibility.public` | **RETIRE as standalone canonical knowledge/delivery/eligibility authority**; any retained presentation/discovery hint must be derived/non-authoritative |

A process transition still requires an established causal trigger/condition. Pacing, host uptime, message count, commit count or a background daemon are not causes.

---

## 4. SR15-03 information-owner route

Open-world traversal reached the requested current owning surfaces:

- `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md`;
- `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`;
- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`;
- `DEV/ARCHITECTURE/CATALOG_ADMISSION.md`;
- `DEV/CATALOG/entity-structures.json`;
- `DEV/CATALOG/identifier-policies.json`;
- Step-4 canonical truth/knowledge owner;
- Step-5.12 disclosure owner;
- closed WP-07 decision/candidate/adversarial/resolution/canonicalization chain;
- `GAME/CORE/INFORMATION.md`;
- current PC, SemanticEvent and live-scene consumers.

Current exact relation identities remain:

```text
world.knowledge
    key = (knower_id, fact_id)

runtime.disclosure
    key = (player_id, fact_id)
```

Binding result:

```text
thread.visibility.known_by_pc_ids
    != durable fictional knowledge owner

thread.visibility.public
    != PC knowledge
    != PLAYER delivery
    != role/context eligibility

SemanticEvent.delta.knowledge_changes / visibility.*
    = historical semantic/communication evidence only

live known_by_pc_ids / perceived_by_pc_ids
    = epoch-local perception/knowledge evidence and normalization input only
```

Physical readability, repository access, index presence or `public=true` never proves character knowledge or `runtime.disclosure`. Closed WP-07 remains a constraint; no information subsystem is reopened.

---

## 5. Chronology field and consumer accounting

### 5.1 Current GAME fields

| Surface | Disposition |
|---|---|
| `CURRENT.world_time.frontier` | **RETIRE** as generic/global chronology frontier/authority; Step-5.9 already supersedes it |
| `CURRENT.world_time.display` | presentation only unless a separate typed owner supplies exact coordinate meaning; never DUE/currentness authority |
| `scene.chronology_frontier_event_id` | **RETIRE as general semantic singleton frontier**; `ActiveExtensionFrontier(S)` is owner-scoped, derivative and may contain multiple anchors; a singleton cache is only an equivalent optimization when cardinality is one |
| `scene.local_time` | owner-scoped presentation/position observation unless validated as typed provider evidence |
| `scene.last_event_id` | provenance/routing reference only; ID order is not chronology |
| `event.caused_by_event_ids` | accepted causal ancestry evidence |
| `event.after_event_ids` | accepted noncausal precedence only when owning order domain is explicit/unambiguous; otherwise final realization requires typed domain evidence |
| `event.world_order.sequence` | optional local owner/domain coordinate; never campaign-global fictional counter |
| `event.world_order.time` | optional typed metric/position evidence only when context/provider semantics are valid; generic serialization is not a clock |
| live `revision`, HEAD/base/absorption fields | currentness/CAS/fencing only |
| live `local_time` / observable `world_time` | typed/presentation evidence only where owner/provider contract gives meaning |

### 5.2 Technical-order contamination rejected

None of the following establish fictional order, elapsed time, simultaneity or DUE by themselves:

- Git commit/ref/ancestry;
- campaign/live HEAD, revision or CAS winner;
- SQLite row/insertion/transaction/timestamp order;
- path/index/list order;
- host process/session/chat/message order;
- wall-clock elapsed time;
- SemanticEvent or other ID allocation order;
- Agenda/list/priority/traversal order;
- durability timer/frontier/exposure age;
- cleanup/GC age/eligibility.

Only admitted typed chronology evidence and the native owner predicate may decide temporal semantics.

---

## 6. Position-provider / DUE reproduction

For a metric binding the current architecture requires deterministic owner-specific provider routing. Conceptually:

```text
ResolveTemporalPosition(owner, binding, current basis)
    -> EXACT(v)
     | BOUNDED(lo,hi)
     | INDETERMINATE_NO_COMPATIBLE_PROVIDER
     | INTEGRITY_CONFLICT
```

Movement follows one owner-defined rule:

```text
FOLLOW CURRENT SCOPE
PRESERVE SOURCE PROVIDER
SAFE REBASE
```

For scalar deadline D:

```text
EXACT(x):
  x < D  -> NOT_DUE
  x >= D -> DUE

BOUNDED(lo,hi):
  hi < D -> NOT_DUE
  lo >= D -> DUE
  otherwise -> INDETERMINATE
```

Unknown/incompatible provider evidence never becomes guessed global time.

---

## 7. Agenda, occurrence and accepted execution

Agenda rebuildability is mandatory. A candidate contains enough owner identity/occurrence/binding/dependency information to nominate reevaluation; it is not a durable job.

Owner occurrence identity is distinct from timing evidence. When a candidate becomes DUE:

```text
native owner validates current occurrence
-> owner claim/materialization rules if applicable
-> accepted Step-3 execution identity
-> fixed RNG / Procedure / Resolution / Continuation / committed segments
```

After that boundary:

- Agenda rebuild cannot rematerialize the same occurrence;
- recovery cannot allocate replacement accepted identities;
- transport/live conflict cannot reroll the same accepted random experiment;
- source movement only revalidates dependencies/currentness required by the owning contract.

Current `runtime-continuation-state.schema.json` field `future_rng_frontier` is **STALE MACHINE DEBT** absent a concrete accepted reserve-before-generation mechanic. `unconsumed_advancement` is legal only as accepted execution/Continuation remainder tied to exact typed context; it cannot represent wall-clock catch-up/global fictional time.

Current `runtime-procedure-state.schema.json` under-realizes Procedure-local initiative/round/turn/local-time state already owned by Step-3/COMBAT; this is machine-realization debt, not a reason to transfer timing into `world.encounter` or `world.thread`.

---

## 8. Recovery, live, durability and cleanup

- WP-11 direct routes and indexes preserve identity/routing separation; index absence never proves semantic absence.
- WP-12 HOT/SQLite may cache current owner state only after owner/identity/currentness validation; SQL order/timestamps are nonsemantic.
- WP-13 durability and SAVE compose native durability domains without a global timer/frontier; publication retry cannot replay accepted semantics.
- WP-14 recovery selects current native routes, discovers armed temporal roots, rebuilds Agenda and resumes accepted execution; checkpoint/session/SQLite/ambient context cannot choose time or current state.
- Step-5.8 LIVE currentness/CAS, close and absorption are technical ownership transitions and do not advance fiction.
- Step-5.13 cleanup must retain chronology/temporal/RNG/Continuation evidence while any protected current consumer still depends on it. GC age/reachability does not become fictional time.

No background polling or wall-clock catch-up is required or authorized.

---

## 9. Regression / machine-debt classification

`DEV/TESTS/CHRONOLOGY_CASES.md`:

- C01-C11, C14-C15 are compatible with current owner-anchored sparse chronology when interpreted through typed owners;
- C12 must be repaired from singleton local-frontier expectation to multi-anchor-capable `ActiveExtensionFrontier(S)` semantics;
- C13 must be repaired from compact global-frontier expectation to sparse material bridge/relation evidence without a global chronology owner.

Current catalog conformance tests correctly protect `world.knowledge` and `runtime.disclosure` composite owner identities. They do not yet account for the WP-11-routed `world.thread` family; later machine realization must add coherent catalog/admission/structure/identifier/conformance coverage.

No tests are changed during WP-15 architecture work.

---

## 10. Architecture -> machine accounting

Every material accepted architecture obligation now has a current machine destination or explicit debt route:

- native temporal owners -> Effect/Actor/Asset/Procedure/rest/current process records;
- generic independent process -> existing WP-11 `world.thread` route + current thread scaffold, pending catalog2.0 alignment;
- Agenda -> derived rebuildable helper, no durable owner;
- chronology -> current event/scene/live fields where semantically compatible plus later typed relation/provider realization; stale global/singleton fields retired;
- accepted firing -> Step-3 RuntimeCommand/Procedure/Resolution/Continuation machinery;
- fixed RNG -> Resolution/Continuation evidence;
- knowledge/disclosure -> exact composite owners, not thread/PC/live/event projections;
- recovery/durability/live/cleanup -> WP-11..14 and Step-5.8/5.13 owner contracts.

---

## 11. Machine -> architecture accounting

Every material current machine surface reached by the active dependency subgraph has one disposition:

- owner-conforming;
- derived/projection only;
- stale/retired debt;
- under-realized owner contract;
- coordinated catalog2.0 alignment debt;
- downstream live/bootstrap/test/performance/documentation route.

No current `frontier`, `revision`, `time`, `sequence`, `deadline`, `clock`, `progress`, visibility or ID field is accepted merely from its name or serialization.

---

## 12. Step-2 synthesis-completeness gate

```text
SOURCE_MANIFEST_OPEN_WORLD:      YES
PROJECT_MAP_ROUTE_REFRESHED:     YES
ACTUAL_OWNER_TRAVERSAL:          YES
ARCHITECTURE_TO_MACHINE:         COMPLETE FOR CURRENT WP-15 SUBGRAPH
MACHINE_TO_ARCHITECTURE:         COMPLETE FOR CURRENT WP-15 SUBGRAPH
SR15_01_CONSUMED:                YES
SR15_02_CONSUMED:                YES
SR15_03_CONSUMED:                YES
ENTITY_STRUCTURES_CONSUMED:      YES
CATALOG_CONTRACTS_CONSUMED:      YES
CATALOG_INVENTORY_CONSUMED:      YES
CATALOG_ADMISSION_CONSUMED:      YES
WORLD_THREAD_OWNER_PROOF:        YES — NARROW INDEPENDENT PROCESS LIFECYCLE ONLY
THREAD_VISIBILITY_DISPOSITION:   COMPLETE
TECHNICAL_ORDER_NONAUTHORITY:    COMPLETE
RECOVERY_NO_REMATERIALIZATION:   COMPLETE
FIXED_RNG_CONTINUITY:            COMPLETE
UNRESOLVED_EVIDENCE_GAPS:        0
HUMAN_DECISION_REQUIRED:         NO
UPSTREAM_REOPEN_REQUIRED:        NO
STEP_3_SYNTHESIS_ALLOWED:        YES
```

The manifest remains open-world for later Steps. A new actual owner/consumer discovered by Step 6 must be added and attacked before canonicalization.
