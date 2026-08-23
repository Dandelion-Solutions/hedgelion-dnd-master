# Step 6 — Reusable Instruction Modules — Working Note

Status: **NON-CANONICAL / DEFERRED DESIGN IDEA / PRE-IMPLEMENTATION**

Date: 2026-08-23

Purpose:

> Preserve a potentially useful prompt/runtime organization pattern for later Step-6 design without installing, depending on, or standardizing any external skill/plugin system.

This note is intentionally small and non-binding. It does **not** define the final master prompt, runtime file layout, module catalog, loading algorithm, or implementation. Step 6 remains responsible for deciding whether this pattern is useful after the role/context architecture and runtime topology are formally redesigned.

The idea is retained here because it may materially improve prompt maintainability and context discipline later, while being cheap to preserve now.

---

## 1. Core idea

HDM may represent reusable LLM procedures as small, first-party Markdown instruction modules owned by the repository.

A module would encode **how to perform one bounded kind of reasoning or presentation work**, rather than holding campaign facts or acting as an autonomous agent.

Conceptually:

```text
stable runtime constitution
    + current turn envelope
    + only the procedural modules relevant to this turn
    + role-local context
    -> model execution
```

Examples of future procedure families might include:

- interpreting materially free-form player intent;
- Dramaturg turn development;
- Actor/NPC decision-making under uncertainty;
- multi-NPC scene execution;
- Narrator presentation;
- investigation/evidence handling;
- scene transition or time advance;
- canonical-commit candidate review;
- recovery/re-entry assistance where LLM judgment is actually required.

These names are examples, not an approved catalog.

---

## 2. Why preserve the pattern

A single monolithic master prompt tends to accumulate unrelated rules and makes it difficult to answer:

- which instructions were actually relevant to this turn;
- which rules belong to all roles versus one procedure;
- whether a change affects ordinary dialogue, investigation, combat narration, preparation, or persistence;
- how much procedural text is consuming context on every turn;
- how to test one reasoning behavior without retesting an inseparable giant prompt.

Small repository-owned modules could make procedural guidance:

- composable;
- version-controlled;
- testable in isolation;
- reviewable by responsibility;
- selectively loadable;
- easier to replace without changing campaign state;
- independent of any external skill runtime.

The intended benefit is **instruction modularity**, not a new agent framework.

---

## 3. Candidate module shape

A future module could use a deliberately boring Markdown contract such as:

```md
# <Procedure name>

## Purpose
What bounded task this procedure performs.

## Activate when
Conditions under which the Master Prompt Builder should include it.

## Inputs
The role-local facts, typed results, observations, or other eligible inputs it may use.

## Procedure
1. Rebind to the active logical role and its eligible information.
2. Identify the unresolved decision or presentation task.
3. Apply the procedure-specific reasoning rules.
4. Produce only the allowed result/proposal/output.
5. Keep invention, fictional cognition, and canonical truth at their proper authority levels.

## Boundaries
What this procedure must not read as authority, infer, mutate, reveal, or commit.

## Output
The minimal result expected by the surrounding turn pipeline.

## Quality checks
A short checklist for the failure modes that matter to this procedure.
```

This is only a design sketch. Exact headings and file format should be chosen later based on the real master-prompt and Context Assembler design.

---

## 4. Modules are instructions, not state

A reusable instruction module must not become another storage layer.

It should not contain mutable campaign truth such as:

- current world facts;
- NPC memories from a specific campaign;
- inventory or resource state;
- secret plot state;
- current relationships;
- current scene consequences.

Those belong to the existing/future authoritative state and context-selection architecture.

The module tells the model **how to reason about supplied state**. It does not own that state.

Therefore:

```text
instruction module
    != campaign memory
    != canon
    != NPC record
    != Dramaturg latent-state store
    != mechanical authority
```

---

## 5. Modules are not logical-role isolation

A module must not be treated as a substitute for role/context semantics.

For example, an Actor procedure may say how an NPC should choose an action, but the Actor's actual eligible knowledge, beliefs, goals, relationships, observations and allowed handoffs must still be assembled separately for that Actor.

Likewise, a Narrator procedure may govern presentation, but it does not make Dramaturg-only material player-eligible.

A useful composition model to investigate is:

```text
GLOBAL CONSTITUTION
    invariant authority / agency / canon rules

TURN ENVELOPE
    current player input + authoritative current-state material

SELECTED PROCEDURE MODULE(S)
    how to perform the needed work on this turn

ROLE FRAME
    what this logical role may know/use and what it is trying to do

TYPED RESULTS / HANDOFFS
    only the explicitly permitted cross-phase information
```

The same procedure module may therefore be reused with many different role-local contexts without merging those contexts.

---

## 6. Selective activation instead of preloading everything

If this pattern is adopted, the default should be **just-in-time procedural activation**, not loading every available module on every turn.

Conceptually:

```text
current turn requirements
    -> determine required logical phases
    -> select the minimum applicable procedural modules
    -> assemble role-local context
    -> execute the turn
```

Potential benefits:

- lower context consumption;
- less instruction interference;
- clearer role focus;
- easier debugging of behavioral regressions;
- simpler evolution of specialized procedures.

This must not become a correctness-sensitive LLM guessing game. The eventual design should decide which activations are deterministic/rule-based, which may be selected by interpreted intent, and what conservative fallback applies when classification is uncertain.

---

## 7. Procedural modules and creative play

The module pattern should not make gameplay scripted.

In particular:

- Dramaturg guidance should define creative responsibilities and authority boundaries, not prescribe a fixed plot;
- Actor guidance should help an NPC reason from personality, goals, beliefs, relationships and pressure, not select from frozen dialogue scripts;
- Narrator guidance should improve readable player-facing presentation without inventing unauthorized persistent state;
- investigation guidance should preserve uncertainty without forcing characters into sterile `insufficient evidence` responses when a provisional choice is appropriate.

A module is therefore closer to a **reusable craft/procedure contract** than to a scenario template.

---

## 8. Relationship to Python/runtime authority

Procedural Markdown must remain subordinate to deterministic authority.

A module may help the model produce:

- an interpretation candidate;
- a Dramaturg proposal or latent branch;
- an Actor decision/utterance;
- a Narrator presentation;
- a candidate fictional-cognition update;
- a candidate persistent-world change.

It must not make persistence authoritative merely by saying that something happened.

The later Step-6 design must preserve the distinction:

```text
LLM procedure produces candidate/prose/invention
    -> authority/validation boundary
    -> accepted persistent consequence where applicable
```

Instruction modularity is compatible with a deterministic Python core precisely because the modules organize nondeterministic work rather than replacing authority.

---

## 9. Versioning and testing direction

If adopted later, modules should be ordinary first-party source files and should be reviewable/testable like other runtime instructions.

Questions for formal design:

- where shipped modules live under `GAME/`;
- whether modules have explicit IDs/versions or rely on release identity;
- how the Master Prompt Builder selects and orders them;
- whether ordering/composition conflicts need machine validation;
- maximum procedural context budget;
- which modules are always-on versus conditional;
- how prompt regression tests isolate one module's behavior;
- whether a module may request a deterministic tool/runtime action;
- how module changes interact with saved campaigns and engine updates.

Do not create a module registry, schema, loader, plugin mechanism or runtime abstraction until Step 6 demonstrates that the additional machinery solves a concrete problem.

---

## 10. Public-source / dependency boundary

If this pattern is used, HDM should own its wording and semantics.

The runtime should not require installation of an external skill collection or plugin merely to obtain core gameplay reasoning behavior.

Any useful general procedure learned from external research should enter HDM only after independent restatement in HDM terminology and review against HDM's authority, role-context, player-agency and persistence rules.

The desired long-term property is:

> A released HDM runtime contains every procedural instruction required for correct gameplay, while optional external development aids remain optional.

---

## 11. Deferred decision

Preserve this as a candidate Step-6 implementation pattern, not as architecture already chosen.

During formal Step-6 design, reconsider it alongside the actual master-prompt construction, role-rebinding model, Context Assembler, Python interaction protocol, context/token budget and runtime packaging constraints.

Possible outcomes remain intentionally open:

- adopt repository-owned procedural modules substantially as described;
- use a smaller variant for only a few complex procedures;
- compile equivalent modules into a generated master prompt;
- keep some instructions monolithic because modularity adds no value;
- reject the pattern if it creates more composition complexity than it removes.

The point of this note is to avoid losing the idea before those decisions are ready to be made.