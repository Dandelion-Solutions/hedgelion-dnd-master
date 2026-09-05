# HDM Product Owner Decision — Historical Actor Decision Basis

Status: **OWNER-APPROVED PRODUCT SEMANTICS — CANONICAL INPUT**

Date: 2026-09-05

Product Owner input:

- `DEV/PRODUCT_OWNER_INPUT.md` — `PO-003`.

This decision records owner-approved product semantics. It does not select a concrete schema, physical path, storage topology, fixed field list, persistence encoding, event shape or implementation.

---

## 1. Decision

HDM SHALL preserve enough **event-time Actor decision basis** for a later authorized Master or Commentator to explain or replay a material historical NPC decision using the information that was relevant **at the time of that decision**, even when the NPC's current cognition, goals, relationships or knowledge have since changed.

This requirement is deliberately narrower than retaining a full historical psychology of every NPC.

Baseline product rule:

```text
NO FULL NPC-PSYCHOLOGY HISTORY
NO PER-TURN FULL ACTOR SNAPSHOTS

MATERIAL ACTOR DECISION / MATERIAL COGNITIVE TRANSITION
    -> retain bounded event-time decision basis when later historical explanation/replay may depend on mutable Actor-private or epistemic state
```

---

## 2. Variable, situation-specific basis

The retained basis is **not required to use one fixed universal list of fields**.

Different situations may legitimately require different relevant evidence. Depending on the decision, the event-time basis may need some combination of:

- then-current knowledge / belief / suspicion / rejection state;
- current objective or goal;
- next intention or approach;
- material commitments;
- directed relationship facets such as trust, affinity, fear, respect, hostility or felt obligation;
- relevant constraints, resources or circumstances;
- causal/source event or fact references;
- other current Actor-private state that materially affected the decision.

The LLM/Actor reasoning step may determine which eligible fields are materially relevant for the particular decision at event time. The later architecture must preserve boundedness, source eligibility and inspectability without replacing this with a mandatory full-state snapshot or a fixed all-purpose psychological schema.

The exact validation, serialization and field vocabulary remain downstream architecture work.

---

## 3. Event-time semantics, not current-state substitution

Historical explanation/replay must distinguish:

```text
WHAT THE NPC KNOWS/WANTS/FEELS NOW
```

from:

```text
WHAT WAS RELEVANT TO THE NPC'S DECISION THEN
```

A later current Actor record must not silently substitute for the event-time basis of an earlier decision.

If a referenced current owner can change over time, the historical basis must retain or resolve evidence sufficient to recover the materially relevant **then-current value/stance**, rather than merely pointing at a mutable current record whose meaning has since changed.

---

## 4. Historical evidence, not a second current owner

Historical decision basis is retrospective evidence.

It SHALL NOT become:

- a second writable owner of current Actor cognition;
- a second `world.knowledge` authority;
- a mechanism that restores or overwrites current NPC state;
- a complete Actor memory graph;
- a permanent archive of every transient thought;
- hidden chain-of-thought retention.

R2.2 source-Actor continuity remains the owner of current non-epistemic Actor-private state. Step-4 `world.knowledge` remains the owner of current epistemic stance. Historical decision basis records only the bounded event-time evidence necessary for later causal explanation/replay.

---

## 5. Materiality boundary

HDM does not need a retained decision basis for every NPC, every turn, every `NO_CHANGE`, every transient feeling or every trivial choice.

Retention is required where a decision/transition is materially significant enough that future continuity, explanation, replay or causal interpretation may depend on mutable Actor-private or epistemic state that would otherwise be lost.

Exact trigger classification remains downstream architecture work. The product intent is sparse/event-driven retention rather than exhaustive psychological history.

---

## 6. Master and Commentator consumption

For a later question/replay such as:

- why did this NPC betray the party then?;
- what did the NPC believe at that point?;
- what relationship stance or commitment materially drove that action?;
- how should a historical scene be replayed without importing later knowledge/motivation?;

an authorized Master or Commentator should use the retained event-time basis and associated historical evidence rather than reconstructing the answer from the NPC's current state alone.

This does not widen disclosure. Current player/principal/PC knowledge, disclosure, no-spoiler and role-context eligibility still govern what may be revealed.

When historical evidence is absent or insufficient, HDM must not present a newly inferred exact motive as established historical fact merely because the current Actor state makes that inference plausible.

---

## 7. Save / durability relationship

This decision does **not** require a save operation to snapshot the full psychology of all NPCs.

The required historical basis is generated/retained at the material decision or transition boundary. Existing persistence/save/publication owners must later ensure that required retained historical evidence receives the applicable durability guarantee.

A physical implementation may co-locate, reference or separately normalize that basis. The product requirement is logical/event-time coherence, not a mandated single file or record.

---

## 8. Current architecture routing

This input is immediately relevant to the active WP-19 retrospective/history consumer framing and therefore invalidates the prior Step-1 review basis that did not include it.

The next WP-19 evidence pass must determine, without presupposing the answer:

- whether the requirement is a new consumer over already sufficient accepted historical evidence;
- whether accepted history/event/record-family architecture is materially insufficient;
- which existing owner should retain the bounded decision basis;
- whether any closed architecture actually requires reopening under normal HDM reopen rules;
- how the requirement composes with R2.2 current cognition, Step-4 knowledge history, R2.1 continuity, WP-18 Story, durability/publication, chronology, Context Runtime and retrospective Master/Commentator consumers.

This decision itself does not declare an upstream reopen and does not authorize WP-19 Step 2 or implementation.
