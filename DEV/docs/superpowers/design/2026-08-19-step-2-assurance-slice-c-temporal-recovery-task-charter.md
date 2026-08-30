# Step 2 Retrospective Assurance — Slice C Task Charter: Temporal and Recovery

Status: **SOLUTION-BLIND TASK CHARTER — DO NOT TREAT AS SOLUTION**

Target branch: `feature/mechanical-runtime-hot-state`

Parent assurance plan: `2026-08-19-step-1-2-retrospective-architecture-assurance-plan.md`.

## 1. Purpose

Independently reconstruct the minimum architecture required for elapsed-time mechanics, turn/round/rest/named boundaries, Effect expiry, delayed Resource recovery, automatic LifeState recovery, repeated/periodic obligations, interrupted time advancement, and restoration after process/chat loss.

The charter does not assume that the accepted local metric coordinate, TemporalBinding, boundary vocabulary, or Temporal Agenda are correct. It asks first what temporal facts must remain knowable and who owns them.

## 2. Problem statement

HDM deliberately does not run a wall-clock simulation. Fiction can compress, skip, or leave elapsed time imprecise. Nevertheless some mechanics require exact or relational timing:

```text
Effect lasts 1 minute
until end of target's next turn
until Long Rest completes
one charge returns after 1 hour
Stable actor recovers after 1d4 hours
Concentration lasts up to 10 minutes
Revivify requires target dead no longer than 1 minute
poison/curse lasts until dawn
wait/travel requests 20 minutes but a due effect occurs after 7
turn-start resets a reaction budget
several state owners respond to one Long Rest boundary
```

The architecture must distinguish:

- reusable duration semantics;
- one concrete active temporal obligation;
- fictional chronology/provenance;
- exact local metric coordinate where needed;
- procedure-relative boundaries;
- semantic/named boundaries;
- due-work indexing;
- automatic state-owner response;
- causal execution/commit ordering.

## 3. Goals

The design must provide at minimum:

1. no dependence on wall-clock time/background processes;
2. exact enough timing whenever a mechanic can depend on elapsed quantity;
3. procedure-native timing that is not naively converted into seconds;
4. semantic boundaries distinct from mere elapsed duration;
5. one authoritative concrete obligation per active owner/temporal rule;
6. reusable DurationSpec separate from materialized deadline/boundary binding;
7. deterministic earliest-due interruption of requested time advancement;
8. deterministic closure of all same-time consequences before advancing past a boundary;
9. cancellation/replacement/re-anchoring without duplicate remaining/deadline authorities;
10. boundary occurrence scoping so unrelated actors/scenes are not affected;
11. state-owner recovery/expiry responses rather than a Rest/Timer god object;
12. repeated recovery/cooldown semantics without a second scheduler;
13. restore/rebuild after process/chat/HOT loss;
14. no campaign-wide polling for ordinary due work;
15. ability to answer later rules that query elapsed time since a past mechanical occurrence when the architecture claims that fact remains recoverable;
16. safe cross-scene/multiplayer deferral without assuming one global clock;
17. explicit treatment of approximate/narrative time when exact quantity was never established;
18. version/migration behavior for active temporal obligations.

## 4. Non-goals

This slice does not finalize:

- exact Step-3 signal/event/segment ordering;
- Git publication and shared cross-scene reconciliation (Step 5);
- every SRD timed spell/recharge rule (Step 6);
- real-world alarms/background jobs;
- a universal continuous campaign simulation.

It must, however, define enough state so later stages can implement timing without inventing a second authority.

## 5. Required ownership questions

### Chronology versus metric time

- What temporal information is always retained as campaign chronology?
- What exact metric information may be absent?
- If a mechanic becomes relevant later and asks `how long since event X?`, when is that answer guaranteed exact?
- Can a local metric coordinate safely freeze while fiction advances narratively?
- Does explicit player/Activity time advancement always need to leave a quantitative trace even when no current timer is active?
- How are approximate statements such as `after several hours` represented without pretending exactness?

### DurationSpec versus TemporalBinding

- What belongs to reusable definition and what is materialized per application/state owner?
- Is one active binding sufficient?
- How does refresh/extend/shorten work?
- How does a binding move between incompatible temporal contexts?
- Can an owner have both intrinsic deadline and support/semantic termination without duplicate duration authority?

### Boundaries

- Who decides turn start/end, rest completion, dawn, and other semantic occurrences?
- Does a boundary have independent durable identity or transient occurrence identity linked to committed Events?
- How is scope expressed?
- Can one producer occurrence cause many owner responses without ordering by array/SQL accident?

### Agenda/index

- What exact authoritative inputs rebuild the due index?
- Which due obligations are world state versus runtime/procedure state?
- What happens if HOT/SQLite is lost while a due boundary is pending?
- How are several due entries at exactly the same coordinate discovered before mutation?

### Recovery

- How are current/spent Resource recovery, Condition remove-count, Effect expiry, and HP/LifeState response kept separate while sharing one boundary vocabulary?
- Which responses may be automatic?
- What happens when a response needs a roll/choice/adjudication?
- Can a recovery rule arm another delayed recovery atomically?

## 6. Failure scenarios

1. An Effect expires in 10 minutes; player says `wait 1 hour`.
2. Two Effects and one Resource recovery are due at the same exact coordinate.
3. One due response changes capacity used by another recovery at the same boundary.
4. Parent support ends at the same boundary as child intrinsic expiry.
5. A Rest reaches 8 hours but is interrupted and does not complete.
6. Long Rest completes and several Resources/Conditions/HP respond.
7. Process dies after boundary discovery but before all responses commit.
8. Process dies after some atomic response segment commits and before continuation resumes.
9. Agenda cache is lost and must be rebuilt.
10. A local metric Effect survives leaving an encounter/procedure.
11. Two previously incomparable scene timelines later interact.
12. An Actor dies, no resurrection timer is created, fiction advances, and later a revival mechanic asks exact time-since-death.
13. A rules-bearing explicit travel/wait action advances 30 minutes while no active metric timer exists; later a mechanic asks whether an earlier event was within 10 minutes.
14. Fiction jumps `several days later` without exact duration and later a rule asks an exact deadline question crossing that gap.
15. A timed Resource recovery is refreshed/rearmed before its old deadline.
16. A terminal Effect still has a stale Agenda row.
17. A semantic dawn boundary occurs without a globally exact timestamp.
18. A paused Continuation spans a due temporal boundary.
19. A local-only due obligation becomes durable before its deadline.
20. A ruleset update changes duration units/semantics while active bindings exist.

## 7. Quality attributes

### Correctness

- no due mechanic is skipped because an index/cache was lost;
- no expired/cancelled obligation fires later;
- no exact elapsed query is answered from invented precision;
- no boundary producer owns unrelated state mutation.

### Determinism

- same authoritative bindings + chronology/procedure state + requested advance yield the same nearest boundary and due set;
- same-time final state does not depend on heap/SQL/list order;
- replay/retry does not duplicate due consequences.

### Performance

- ordinary actions do not scan the campaign for timers;
- Agenda indexes only active relevant obligations;
- local time precision is not forced on unrelated scenes/entities merely for convenience.

### Recovery

- continuity-critical timing source state survives/checkpoints;
- disposable Agenda/reverse indexes rebuild deterministically;
- due/partially resolved work resumes idempotently.

### Extensibility

- new boundary kinds and duration rules require registered typed semantics, not arbitrary callbacks;
- new rulesets can use different procedure clocks without replacing the world chronology model.

## 8. Known unknowns requiring investigation

- Whether demand-driven frozen metric coordinates lose information needed by later lazy eligibility checks such as revival windows.
- Whether campaign chronology already records quantitative elapsed contributions independently of active metric obligations.
- Whether one TemporalBinding shape can safely represent all current owner types without ambiguous anchor identity.
- Whether semantic boundaries need durable occurrence records or only Step-3 committed Events/receipts.
- Whether periodic Effects require a repeated trigger binding distinct from end-duration binding.
- Whether delayed recovery re-arming can be represented with one binding without hidden scheduler state.
- Whether cross-basis re-anchoring can preserve exactness when the source chronology is only partially ordered.
- What happens when exact and approximate fictional-time spans mix.
- Whether future compaction can discard chronology needed for active/lazy temporal queries.

## 9. Exit criteria

Slice C closes only after all requirements are mapped to the accepted baseline, the frozen-time/lazy-query risk is resolved, authoritative rebuild inputs for Agenda are explicit, recovery/boundary deferrals are audited, and an independent critic finds no unowned temporal correctness blocker.
