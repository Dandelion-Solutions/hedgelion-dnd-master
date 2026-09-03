# R2.7 WP-15 — Senior Recovery — Process Source-Graph Omissions

Status: **SENIOR REPAIR COMPLETE — MANDATORY SENIOR REVIEW**

Date: 2026-09-03

Domain: **WP-15 — temporal owners / processes / chronology**

Pre-repair verified Step-1 SHA:

- `8daf9de4d42a53b00a894d5b13646545cb4a3a53`

Companion Step-1 artifacts:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-task-brief.md`
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-source-manifest.md`
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-task-brief-critic.md`

This record preserves two mandatory Senior-review findings separately from the historical Step-1 critic. Historical `C01–C12` remain exactly the original `3 BLOCKING + 9 SIGNIFICANT` findings and are not rewritten as if they discovered these omissions.

---

## SR15-01 — BLOCKING — shipped process runtime and durable representation omitted

### Finding

The Step-1 dependency graph omitted the primary shipped process runtime and its current durable representation:

- `GAME/CORE/PROCESSES.md`
- `GAME/SCHEMA/thread.schema.yaml`

`PROCESSES.md` currently describes threats, goals, projects, countdowns, investigations, pursuits, long-running/off-screen processes, clocks, causal advancement, deadlines, simulation budget, multiplayer duplicate-advancement prevention, visibility and event dependencies.

`thread.schema.yaml` currently carries the durable representation for `world.thread`-shaped process records, including:

```text
kind
status
owner_entity_id
objective
state.stage
state.progress
state.next_development
state.advancement_conditions
state.deadline
state.resources
affected_entity_ids
visibility.known_by_pc_ids
visibility.public
created_event_id
last_event_id
```

### Authority classification

Both sources are **current implementation / machine-contract evidence**.

They are mandatory Step-2 inputs, but their existence does **not** prove that `world.thread` owns every represented temporal obligation, clock or deadline.

For each process/clock/deadline, Step 2 must establish the actual native owner and the exact relationship, if any, to:

- `TemporalBinding`;
- chronology anchors/relations/position-provider evidence;
- Step-3 accepted execution;
- derived Temporal Agenda enrollment/recheck;
- recovery/currentness;
- durability/publication;
- retention/GC protection.

A process abstraction or `world.thread` record may own process state only where current owner law actually assigns that responsibility. It cannot become a generic scheduler, chronology owner, execution owner or universal temporal-obligation owner by convenience.

### Mandatory Step-2 reverse-audit route

Step 2 must explicitly account for:

- threats / goals / projects / countdowns / investigations / pursuits;
- stage, progress, next-development and advancement-condition semantics;
- deadlines and resources;
- segmented clocks and their predefined in-world meaning;
- off-screen advancement and the prohibition on continuous dormant simulation;
- causal advancement triggers;
- simulation-budget/boundedness behavior;
- multiplayer prevention of duplicate advancement for one causal stage/elapsed interval;
- `created_event_id` / `last_event_id` dependencies and whether they are causal/history pointers versus chronology authority;
- process visibility and information-eligibility consequences;
- recovery/rebuild/currentness implications;
- durability/publication closure implications;
- retention/cleanup/protected-consumer implications.

### Disposition

**CLOSED BY SENIOR REPAIR.**

The Task Brief and Source Manifest now make both sources mandatory Step-2 evidence and explicitly prohibit blanket `world.thread` temporal ownership.

---

## SR15-02 — SIGNIFICANT — direct temporal/process CORE consumers omitted

### Finding

The Step-1 dependency graph omitted four direct current consumers containing material temporal/process statements:

- `GAME/CORE/ADVANCEMENT.md`
- `GAME/CORE/EXPLORATION.md`
- `GAME/CORE/COMBAT.md`
- `GAME/CORE/ENCOUNTERS.md`

### Authority classification

These are **current implementation / machine-contract consumers** for WP-15 only to the extent of their temporal/process statements. They do not reopen or transfer ownership of unrelated advancement, exploration, combat or encounter mechanics.

### Mandatory Step-2 scoped inspection

Step 2 must inspect only the relevant statements:

- rest, downtime and long projects;
- in-world elapsed/travel time;
- off-screen process advancement driven by causality;
- Procedure-local initiative / round / turn / active participant / local procedure time;
- time pressure and process consequences in encounters.

In particular, `GAME/CORE/COMBAT.md` already states that Procedure-local initiative/round/turn/local-time operational state belongs to active `runtime.procedure`, while `world.encounter` owns durable encounter identity/participants/status and is not a duplicate timing owner. WP-15 must preserve that boundary rather than reopen unrelated combat/encounter semantics.

### Disposition

**CLOSED BY SENIOR REPAIR.**

The Task Brief and Source Manifest now list all four as direct scoped Step-2 consumers.

---

## Open-world preservation

The repaired Source Manifest remains explicitly open-world.

Step 2, if later authorized, must discover and add any additional real process/domain consumer, representation, schema, test, bootstrap/migration route or owner reached from:

```text
PROCESSES / world.thread
process kind/stage/progress/deadline/clock
TemporalBinding / chronology / Agenda
Step-3 execution
rest/downtime/travel/combat/encounter temporal statements
recovery/publication/retention consumers
```

Discovery does not imply activation or ownership. Each source receives an explicit owner/classification/disposition.

---

## Recovery gate

```text
SENIOR_FINDING:             SR15-01
INITIAL_SEVERITY:           BLOCKING
DISPOSITION:                CLOSED BY SENIOR REPAIR

SENIOR_FINDING:             SR15-02
INITIAL_SEVERITY:           SIGNIFICANT
DISPOSITION:                CLOSED BY SENIOR REPAIR

HISTORICAL_CRITIC_C01_C12:  UNCHANGED
UNRESOLVED_BLOCKING:        0
UNRESOLVED_SIGNIFICANT:     0
HUMAN_DECISION_REQUIRED:    NO
UPSTREAM_REOPEN_REQUIRED:   NO
STEP_2_AUTHORIZED:          NO
WP16_AUTHORIZED:            NO
IMPLEMENTATION_PLANNING:    NOT AUTHORIZED
NEXT_GATE:                  MANDATORY SENIOR REVIEW
```

No `GAME/` runtime/schema/template/test implementation is changed by this repair.
