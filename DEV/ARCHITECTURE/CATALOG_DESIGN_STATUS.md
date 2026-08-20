# HDM Catalog Design Status

Status: **STEPS 1–4 ARCHITECTURE CLOSED / STEP 5 IN PROGRESS**

Target branch: `feature/mechanical-runtime-hot-state`

This file is a current-status index, not a second normative specification.
Detailed reasoning/history lives in linked architecture/spec documents and Git
history.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

Sequencing authority:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

## 1. Current checkpoint

Steps 1–2 are complete and retrospectively assured.

Step 3 is closed: owner decision, candidate, adversarial review, canonical spec,
machine-contract TDD alignment, integrated A–N cases, final critical review and
final same-head validation completed successfully.

Step 4 completed its full architecture rerun after adoption of six logical LLM
roles. Its architecture is closed. The obsolete literary Chapter world surface
has also been removed from the active machine catalog and current normative
catalog documents.

Step 5 is the sole active numbered architecture stage.

Per owner direction, broad implementation planning for the remaining Step-4/5/6
contracts waits until the remaining architecture sequence is complete.

## 2. Current machine baseline

Active catalog version: `1.5.0`.

The `1.5.0` bump is deliberately narrow: it records the incompatible retirement
of the old literary Chapter world vocabulary:

```text
world.chapter                removed
transition.chapter_append    removed
event.chapter.appended       removed
```

All four machine catalog files move coherently at `1.5.0`.

This version bump does **not** claim that the rest of canonical Step-4 machine
realization already exists. In particular, the current machine schemas still
require later implementation alignment for normalized lore/knowledge,
`runtime.disclosure`, Context Assembler contracts and Story schemas.

Current Steps 1–3 implemented invariants remain in force, including:

- one coherent `ResolvedCatalogContext`;
- no same-ID shadowing inside one resolved context;
- explicit definition/world binding compatibility;
- `runtime.procedure` as sole procedure-local ResourceState owner;
- distinct Encounter / Procedure / Resolution / Continuation lifetimes;
- embedded ExecutionSegment and pending-child descriptors rather than generic
  workflow records;
- current world records as current-state authority;
- MechanicalEvents as immutable committed mechanical evidence;
- no generic scheduler/job/workflow engine.

Current normative catalog surfaces:

- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`
- `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`
- `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md`
- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/entity-structures.json`
- `DEV/CATALOG/identifier-policies.json`
- `DEV/CATALOG/mechanical-surfaces.json`

## 3. Step-3 execution boundary

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`

Core ownership remains:

```text
Interaction
    -> IntentPlan
        -> RuntimeCommand
            -> ActionRequest -> Resolution(Activity)
            OR
            -> TransitionRequest -> direct deterministic execution

runtime.procedure
    sole procedure-local ResourceState owner

Resolution / direct transition
    -> embedded ExecutionSegment(s)
        -> MechanicalEvents
        -> receipts/idempotency
        -> mandatory child descriptors

Continuation
    one portable suspended Resolution generation
```

Step-4 information architecture does not weaken Step-3 execution authority.

## 4. Step-4 architecture closure

Canonical Step-4 specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`

Rerun artifacts:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-research-draft.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-decision-resolution.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-resolution-gate.md`

Cross-cutting LLM-role draft:

- `DEV/docs/superpowers/specs/2026-08-20-llm-logical-roles-draft.md`

Adversarial result from the rerun:

```text
owner-decision blockers: 0
mechanically resolved Step-4 findings: 10
later-owner findings: 4
```

No unresolved Step-4 product-semantic or ownership gate remains.

## 5. Canonical Step-4 authority model

```text
OBJECTIVE / CURRENT
    ordinary world state owners
    world.lore_fact

FICTIONAL CURRENT PERSPECTIVE
    world.knowledge

HUMAN PLAYER EXPOSURE
    runtime.disclosure

HISTORICAL EVIDENCE
    runtime.semantic_event / LOG
    runtime.mechanical_event

ROLE CONTEXT
    deterministic Context Assembler
        -> Interpreter
        -> Dramaturg
        -> Actor
        -> Narrator
        -> Chronicler
        -> Commentator

NON-CANONICAL PRESENTATION HISTORY
    STORY/
        TRANSCRIPT/
        EVENTS/
        MECHANICS/
        NARRATIVE/
```

### Truth

- `world.lore_fact` owns independently identified objective propositions;
- objective truth semantics are `undetermined / established / disproven`;
- in-world disagreement belongs to epistemic relations rather than objective
  `disputed` truth;
- lifecycle/supersession is separate from truth status;
- identity-defining proposition meaning/scope cannot be silently rewritten after
  durable reference.

### Knowledge

- `world.knowledge` is the sole durable current fictional epistemic owner;
- initial stance semantics are `aware / known / believed / suspected / rejected`;
- PC factual availability may become `known` through qualifying resolved sources;
- voluntary PC belief/suspicion/rejection remains player-controlled unless a
  genuine rules/world mechanism constrains cognition;
- Actor may propose NPC/faction epistemic changes; core commits authoritative
  changes.

### Player disclosure

- `runtime.disclosure` is separate from PC cognition;
- it records sparse material human exposure;
- statement exposure and objective truth-transition exposure are distinct;
- Narrator returns structured disclosure refs; host records exposure only after
  the player-facing emission boundary.

### Secret

No generic Secret authority survives.

- objective truth -> lore/world owner;
- fictional cognition -> `world.knowledge`;
- human exposure -> `runtime.disclosure`;
- reveal/clue planning -> Dramaturg preparation;
- actual automatic reveal mechanics -> actual rules/world owner.

## 6. Six logical LLM roles and Context Assembler

Accepted roles:

1. Interpreter;
2. Dramaturg;
3. Actor;
4. Narrator;
5. Chronicler;
6. Commentator.

A role is not necessarily a separate physical model/agent call.

Step-4 invariant:

> each role consumes a separately eligible bounded source bundle plus typed
> prior-role results; raw private source context does not flow transitively
> between roles.

A narrower role cannot run inside a physical model context that still contains
ineligible broader-role material. Step 6 owns physical placement and must use
genuine reset/isolation or separate calls when eligibility differs.

Context Assembler is deterministic working machinery, not a seventh LLM role or
canonical owner.

## 7. Story and Chapter result

Campaign Story root:

```text
STORY/
    TRANSCRIPT/
    EVENTS/
    MECHANICS/
    NARRATIVE/
```

All Story layers are durable but non-canonical.

- `TRANSCRIPT` — retained visible participant discourse;
- `EVENTS` — Story-facing adaptation of semantic LOG/history;
- `MECHANICS` — curated player/spectator-relevant mechanics;
- `NARRATIVE` — editable literary prose.

Story IDs are independent per layer (`T...`, `E...`, `M...`, `N...`) with
explicit many-to-many refs. Default storage is one record per file with
deterministic thousand-slot shards.

Literary Chapters are **only NARRATIVE index groupings** over ordered N refs.
They are not world records, runtime transitions or committed world events.

The active catalog no longer contains the retired Chapter IDs, and current
catalog semantics/field/identifier documents agree with that classification.

Historical design documents may retain references to those IDs solely as
historical derivation material; they do not override current authority.

## 8. Deferred machine realization from Step 4

Architecture closure is not implementation closure.

The integrated implementation program after Steps 5–6 must still realize, test
and migrate at least:

- `world.lore_fact` truth/lifecycle normalization;
- `world.knowledge` stance/current-owner normalization;
- `runtime.disclosure` record/schema/provenance;
- knowledge/disclosure transition and event contracts;
- Context Assembler request/bundle/source-manifest contracts;
- role-specific eligibility and disclosure-delivery tests;
- Story root/layout/IDs/shards/index/four-layer schemas;
- dependency-based Story availability;
- legacy Secret/embedded-knowledge migration;
- live-scene knowledge/disclosure compaction alignment.

These are explicit deferred implementation obligations, not unresolved Step-4
architecture questions.

## 9. Later-stage ownership

### Step 5 — active

Owns architecture for:

- repository-backed checkpoint publication/restoration;
- SOFT/HARD durability;
- multiplayer/shared conflict semantics and live-scene compaction transport;
- chronology evidence and cross-scene reconciliation;
- Story publication/body-index-availability coherence;
- Story ID allocation under concurrency;
- transcript/history retention and compaction;
- exact host response-delivery acknowledgement.

There is no default long-lived public/spectator branch.

### Step 6

Owns architecture for:

- physical model-call topology for six roles;
- model selection/context isolation/token/latency/cost budgets;
- preparation retention/cache policy if justified;
- default Commentator spoiler/perspective profile and optional deep-source/debug
  mode;
- optional narration semantic verification/evaluation;
- engine/ruleset/package/catalog snapshot metadata;
- migration/catalog-gap/full seed closure;
- final holistic architecture audit and implementation-obligation consolidation.

## 10. Exact continuation

Step 4 architecture is closed.

The sole active architecture stage is now:

> **Step 5 / Durability, Multiplayer, Event-Local Time, Story/Transcript
> Publication and Retention.**

Do not begin broad implementation planning before the remaining architecture
sequence is complete unless the owner explicitly changes that order.
