# Round 2 Roadmap — Evidence Rebaseline and Owner Decision

Status: **OWNER-APPROVED ARCHITECTURE PROGRAM DECISION**

Date: 2026-08-24

Applies to:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- Architecture Round 2 sequencing/status;
- the DIAMOND/STRONG research-candidate horizon in `HDM_External_Architecture_Idea_Dossier_2026-08-21.md`.

Evidence accounting:

- `DEV/docs/superpowers/research/2026-08-24-round-2-evidence-disposition-ledger.md`

This decision supersedes the previous Round-2 stage decomposition in the roadmap. It does not supersede accepted Round-1 semantic architecture and does not authorize broad implementation.

---

## 1. Decision

The owner approves a new Round-2 decomposition derived from current accepted architecture plus item-level evidence accounting.

The approved sequence is:

```text
R2.0 Evidence Rebaseline & Scope Reconstruction
    -> R2.1 Continuity, Memory & History-Aligned Derived State
    -> R2.2 Actor Continuity, Cognition & Directed Relationships
    -> R2.3 Context Runtime, Retrieval & Allocation
    -> R2.4 Single-Context LLM Execution & Instruction Architecture
    -> R2.5 Collaboration & Multiplayer Interaction Semantics
    -> R2.6 ChatGPT-Plus Assurance, Evaluation, Security & Degradation
    -> R2.7 Machine Realization Mapping & Holistic Architecture Closure
    -> implementation planning
```

Exactly one numbered Round-2 stage is active at a time unless the roadmap is explicitly changed.

---

## 2. What is superseded

The previous Round-2 decomposition is retired as a sequencing plan.

In particular:

- old R2.2 Context Runtime no longer precedes Actor continuity;
- old standalone mandatory Dramaturg/Narrative Dynamics stage is removed;
- old optional-capability gate is removed;
- old R2.8/R2.9 numbering is retired;
- research classification no longer creates an implicit review/backlog obligation.

Useful questions from the previous roadmap remain evidence only where they are still owned by one of the new stages.

No old stage is considered completed merely because its subject overlaps a new stage.

---

## 3. Why Actor precedes Context Runtime

The Context Runtime is a projection/selection layer.

It must not invent upstream Actor semantics merely because a representation is convenient for retrieval.

Therefore the dependency is:

```text
R2.1
    define continuity source/lifecycle semantics

R2.2
    define Actor continuity/cognition/relation source semantics

R2.3
    select, budget, retrieve and trace those admitted sources
```

The projection layer remains downstream from the state/continuity semantics it consumes.

---

## 4. No mandatory Narrative Dynamics subsystem

Current accepted/runtime HDM already has:

- noncanonical Dramaturg preparation;
- situation/pressure preparation;
- causal world processes;
- NPC goals/plans/relationships;
- bounded off-screen advancement;
- pacing/GM-initiative rules without plot authority.

Therefore research candidates involving retained planning artifacts, staged world pressure, anti-stagnation or additional timeskip machinery do not justify a mandatory Round-2 subsystem now.

They remain conditional and may re-enter architecture only when their preserved revisit trigger becomes true and existing owners prove insufficient.

---

## 5. Conditional work does not reserve roadmap stages

A `CONDITIONAL / DORMANT` candidate creates no immediate architecture task.

If its trigger becomes true:

1. establish the concrete current requirement;
2. determine whether accepted architecture already satisfies it;
3. if not, identify the smallest bounded design delta;
4. insert/reorder a roadmap stage only where the dependency graph requires it.

No generic end-of-round optional-capability review is required.

---

## 6. Round-1 preservation

Round 1 remains the accepted strong base.

A Round-1 topic is reopened only when current work:

1. materially extends the accepted decision;
2. exposes a contradiction/invalid assumption;
3. introduces a new unsatisfied consumer; or
4. makes the accepted decision insufficient.

Examples retained rather than reopened include:

- LLM proposal versus deterministic mechanical commit;
- truth versus fictional knowledge versus human disclosure;
- Story nonauthority;
- selective exact/semantic history principles;
- accepted gameplay not replayed because presentation is retried;
- Step-5 recovery/currentness/concurrency/chronology foundations.

---

## 7. Evidence-disposition result

The roadmap horizon was derived from the 82 DIAMOND/STRONG candidates under the current accepted HDM architecture.

Disposition result:

```text
ACTIVE / ACTIVE DELTA          43
INHERITED / ALREADY SATISFIED  16
CONDITIONAL / DORMANT          23
unaccounted                     0
```

This accounting does not mean all active candidates become independent subsystems or stage deliverables. Multiple candidates may resolve through one architectural boundary.

The evidence ledger preserves the item-level rationale and revisit triggers.

---

## 8. Current transition

With owner approval of this decision:

```text
R2.0  COMPLETE / EVIDENCE-REBASELINED
R2.1  IN PROGRESS
R2.2  PLANNED
R2.3  PLANNED
R2.4  PLANNED
R2.5  PLANNED
R2.6  PLANNED
R2.7  PLANNED
```

R2.1 begins with its task brief and Source Manifest under the normal HDM architecture process.

Broad implementation remains blocked.
