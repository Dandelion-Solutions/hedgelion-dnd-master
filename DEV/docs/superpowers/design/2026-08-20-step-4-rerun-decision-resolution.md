# Step 4 Rerun — Decision Revalidation and Resolution

Status: **OWNER DECISIONS REVALIDATED — NO NEW MATERIAL HUMAN GATE**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Inputs:

- `2026-08-20-step-4-rerun-task-brief.md`
- `2026-08-20-step-4-rerun-research-draft.md`
- `2026-08-20-step-4-truth-knowledge-disclosure-decision-brief.md`
- `2026-08-20-llm-logical-roles-draft.md`

## 1. Purpose

This document records the decision phase of the Step-4 full-cycle rerun.

The rerun was requested after the owner approved six logical LLM roles. Its purpose was to determine whether the new role architecture invalidated, modified, or resolved the previously accepted truth/knowledge/disclosure decisions.

## 2. Previously accepted owner decisions

The owner had already approved:

```text
world.lore_fact
    objective proposition/truth authority

world.knowledge
    current in-fiction epistemic authority

separate durable player disclosure owner
    human exposure, distinct from PC cognition

Secret
    no independent truth/knowledge authority
```

The owner also approved:

```text
STORY/
    TRANSCRIPT/
    EVENTS/
    MECHANICS/
    NARRATIVE/
```

as one-branch, Git-backed, non-canonical presentation/history material, plus retirement of the old `world.chapter` concept in favor of NARRATIVE records and chapter grouping in index metadata.

The owner subsequently approved six logical LLM roles:

1. Interpreter;
2. Dramaturg;
3. Actor;
4. Narrator;
5. Chronicler;
6. Commentator.

A logical role is not necessarily a distinct physical agent/model call.

## 3. Rerun conclusion

The six-role model **strengthens rather than changes** the accepted ownership split.

No newly discovered alternative remains sufficiently competitive to require another owner decision.

The prior Alternative C is therefore revalidated as the governing Step-4 authority model.

## 4. Decisions now treated as settled for Step 4

### D4.1 Objective proposition authority

`world.lore_fact` remains the durable proposition identity and objective truth owner when independent propositional identity is required.

Objective truth and record lifecycle are separate axes.

Initial objective truth semantics:

```text
undetermined
established
disproven
```

In-world disagreement is represented by epistemic relations, not by an objective `disputed` truth state.

### D4.2 Fictional epistemic authority

`world.knowledge` is the sole durable current owner of material fictional subject-to-proposition epistemic state.

PC/NPC/faction embedded knowledge arrays do not remain parallel writable authority.

### D4.3 Human-player disclosure authority

Human exposure is semantically different from fictional cognition and receives a separate campaign-durable meta-level owner.

The candidate specification may use `runtime.disclosure` as the machine kind unless review finds a concrete classification conflict.

Player disclosure does not imply any controlled PC knows or believes the same proposition.

### D4.4 Secret retirement

No generic Secret truth/knowledge authority survives.

Secret is contextual eligibility relative to a subject/player/role context.

Legacy Secret responsibilities route to:

- proposition/world truth owner;
- `world.knowledge`;
- player disclosure;
- Dramaturg preparation;
- actual mechanical/world reveal owner;
- ordinary thread/provenance references.

### D4.5 Role-specific context assembly

Step 4 admits a deterministic **Context Assembler** capability.

It is:

- not a seventh LLM role;
- not a new canonical state owner;
- not a generic ACL/knowledge-graph engine.

It builds bounded role-specific source bundles from role, subject/player, purpose and pinned frontier.

### D4.6 Cross-role handoff rule

A logical role may pass a typed result to another role or core component.

It may not implicitly pass the raw private source context from which that result was generated.

Physical co-location in one future model/process cannot merge logical information eligibility.

### D4.7 Role information boundaries

- Interpreter receives only information needed to understand/bind the external message and bounded fiction-dependent facts.
- Dramaturg may receive broad relevant DM truth for non-canonical preparation.
- Actor receives the represented subject's own cognition/circumstances rather than DM omniscience.
- Narrator receives player/PC-eligible settled material, not raw private adjudication or Dramaturg context.
- Chronicler receives occurred historical evidence sufficient to build Story.
- Commentator is Story-first/Story-only by default and navigates Story without creating facts.

### D4.8 Story structure

`STORY/{TRANSCRIPT,EVENTS,MECHANICS,NARRATIVE}` remains non-canonical.

One independently addressable Story record per file remains the default.

Layer-local IDs and explicit many-to-many source/cross-layer references remain accepted.

NARRATIVE chapter grouping is index metadata rather than a world entity.

### D4.9 Spectator reveal semantics

The Commentator requirement establishes a need for Story retrieval to respect a session-local reveal/spoiler frontier.

Story records that can contain reveal-sensitive claims need record-level availability/reveal metadata. Mixed-eligibility material should be split before field-level redaction machinery is introduced.

The exact default spectator mode is deferred to Step 6.

### D4.10 Promotion

Invocation facts, preparation, role proposals and narrative prose do not automatically become durable truth.

A previously untracked claim may be promoted as `world.lore_fact` with `truth_status=undetermined` when a canonical durable knowledge/disclosure/history reference requires stable identity without asserting objective truth.

Existing local-entity publication closure rules continue to apply to canonical durable references.

## 5. Questions resolved by the six-role model

The following no longer require independent architecture decisions:

1. **Where do generic revelation-condition ideas live?**
   - Dramaturg preparation when non-canonical;
   - actual mechanical/world owner when executable.

2. **Which LLM may see secrets?**
   - determined by role-specific Context Assembler eligibility, not one generic visibility flag.

3. **How does private adjudication avoid narration leaks?**
   - Narrator receives a separately assembled eligible bundle and typed settled results, never raw private source context.

4. **How does NPC cognition avoid DM omniscience?**
   - Actor context is subject-scoped through `world.knowledge` and observable facts.

5. **How does spectator access avoid requiring a public branch?**
   - Commentator consumes Story plus session-local reveal frontier inside the same campaign branch.

6. **Who writes Story and who reads it interactively?**
   - Chronicler authors/edits Story; Commentator consumes it.

## 6. Remaining work is mechanical architecture formalization

No new product-semantic trade-off is open before Candidate Specification.

The agent therefore owns:

- exact candidate contracts and invariants;
- context request/bundle conceptual fields;
- disclosure aspects and recording protocol;
- Story schemas/indices/provenance rules;
- migration/retirement mapping;
- adversarial review and non-material fixes;
- roadmap/status correction after resolution.

Any finding that changes canonical state ownership, player/PC agency semantics, guest disclosure semantics, or another material product boundary must still be escalated.

## 7. Resolution

**Proceed to Candidate Specification without another human decision gate.**

Confidence: **HIGH**.
