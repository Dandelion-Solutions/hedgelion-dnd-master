# Step 4 — Truth, Knowledge, Disclosure — Decision Brief

Status: **HUMAN ARCHITECT DECISION REQUIRED**

Research:

- `DEV/docs/superpowers/design/2026-08-20-step-4-lore-knowledge-story-research-draft.md`

## 1. What is being decided

Choose the durable authority split for:

- objective propositions/truth;
- in-fiction PC/NPC/organization knowledge and belief;
- information actually disclosed to a human player;
- the legacy Secret container.

This decision must precede the Step-4 candidate specification because it determines schemas, context filtering, live-scene compaction, migration of old PC/NPC/Faction fields, and whether a new durable meta-level record class is admitted.

## 2. Existing facts that constrain the choice

- CORE already distinguishes objective truth, NPC belief, PC knowledge, and what a player has actually been told.
- Current legacy schemas duplicate writable knowledge across PC/NPC/Faction/Secret/Player/live-scene fields.
- Step-1 already admitted `world.lore_fact` and `world.knowledge` specifically to separate proposition truth from who knows it.
- Human player disclosure has a different semantic lifetime from PC knowledge: a player can know something OOC, can control several differently informed PCs, and cannot literally be made to unsee information.
- Repository read access is not a secrecy boundary; LLM context eligibility is.

## 3. Recommendation — Alternative C

```text
world.lore_fact
    objective proposition/truth authority

world.knowledge
    current in-fiction epistemic state
    PC/NPC/organization -> proposition

runtime.disclosure        # exact machine name provisional
    durable human-player exposure state
    PLAYER -> proposition

LOG / SemanticEvent
    immutable historical evidence of changes/perception/disclosure

Secret
    no independent authority/entity
```

### `world.lore_fact`

Keep the existing machine kind and normalize its axes:

- objective truth: `undetermined | established | disproven`;
- in-world disagreement leaves objective truth status and lives in beliefs;
- canonicality is not a truth value;
- supersession/retcon is lifecycle/provenance, not a truth value.

### `world.knowledge`

One durable current relation per material `(knower, proposition)` with a small closed epistemic stance vocabulary such as:

- known;
- believed;
- suspected;
- rejected.

Exact machine names follow mechanically after approval.

Actor/Faction embedded knowledge arrays cease to be writable authority. Derived HOT indexes may restore local-read convenience.

### Player disclosure

Use a separate durable meta-level relation for `(player, proposition) -> disclosed`.

It records only disclosure whose future context correctness may matter; ordinary throwaway dialogue need not generate a relation for every sentence.

This does **not** imply any controlled PC knows the proposition.

### Secret

Remove the legacy Secret truth/knowledge container as an authority concept.

A fact is "secret to context X" when objective truth exists but X lacks the appropriate knowledge/disclosure. If a reveal mechanism is mechanically real, the actual Feature/Effect/Activity/Trigger/world owner stores that behavior. If it is only preparation guidance, it remains preparation rather than executable canon.

## 4. Alternatives

### Alternative A — Keep embedded knowledge and Secret

```text
PC/NPC/Faction knowledge arrays
+ Secret known/suspected arrays
+ player visibility lists
```

**Reject.** Cheapest migration today, but preserves duplicate writable authority, poor provenance, and inconsistent context filtering.

### Alternative B — One universal `world.knowledge`, including PLAYER disclosure

```text
world.knowledge
    PC -> known/believed/...
    NPC -> known/believed/...
    PLAYER -> disclosed
```

Benefits:

- one record kind;
- no new runtime class.

Weaknesses:

- mixes fictional cognition with meta-level human exposure;
- a `world.*` record becomes owner of user-interface state;
- query mistakes can accidentally convert player knowledge into character knowledge;
- disclosure is effectively monotonic while fictional knowledge/belief can change through world causes.

**Viable but not recommended.**

### Alternative C — separate knowledge and disclosure owners

The recommended split above.

Benefits:

- matches already accepted PC-vs-player semantics;
- one writable owner for each meaning;
- clear context filtering;
- no need for a universal information graph;
- live perception/history remains evidence rather than current duplicate state.

Cost:

- one additional durable record class/index;
- narration context may require two bounded lookups instead of one.

**Recommended.**

## 5. Strongest objection to C

It adds another class and makes an NPC/PC record less self-contained. A simple embedded list is cheaper to inspect manually.

Response:

HDM already relies on bounded indexed hydration and rebuildable HOT projections. A by-knower index restores local retrieval without duplicating canonical ownership. The added disclosure class represents a real semantic boundary rather than speculative abstraction.

## 6. Consequences if C is accepted

The agent can proceed mechanically to:

1. specify exact proposition/knowledge/disclosure lifecycles and provenance;
2. specify knowledge-safe LLM context views;
3. retire legacy Secret truth/known/suspected ownership;
4. migrate embedded PC/NPC/Faction knowledge and player visibility fields;
5. define live-scene compaction into normalized knowledge/disclosure;
6. retire `world.chapter`, `transition.chapter_append`, `event.chapter.appended` as already owner-approved;
7. specify `STORY/{TRANSCRIPT,EVENTS,MECHANICS,NARRATIVE}` and chapter index grouping;
8. specify minimum promotion closure;
9. run candidate-spec adversarial review before any machine implementation.

## 7. Decision requested

**Recommend accepting Alternative C:**

> Objective propositions remain in `world.lore_fact`; in-fiction current epistemic state belongs only to `world.knowledge`; human-player disclosure receives a separate durable meta-level owner; Secret ceases to be an independent truth/knowledge entity.

Confidence: **HIGH**.

The exact machine name `runtime.disclosure` is provisional and may be mechanically adjusted without reopening the semantic decision.
