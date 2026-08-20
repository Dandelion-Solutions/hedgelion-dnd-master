# HDM Catalog Design Status

Status: **STEPS 1–3 CLOSED / STEP 4 IN PROGRESS — ARCHITECTURE CANONICAL, MACHINE ALIGNMENT PENDING**

Target branch: `feature/mechanical-runtime-hot-state`

This file is a current-status index, not a second normative specification. Detailed reasoning/history lives in linked architecture/spec documents and Git history.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

Sequencing authority:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

## 1. Current checkpoint

Steps 1–2 are complete and retrospectively assured.

Step 3 is closed: owner decision, candidate, adversarial review, canonical spec, machine-contract TDD alignment, integrated A–N cases, final critical review and final same-head validation all completed successfully.

Step 4 is the sole active numbered stage.

Step-4 **architecture is now canonical**, but the stage remains open until catalogs/schemas/runtime/template/tests are aligned and freshly verified.

Canonical Step-4 specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`

## 2. Current machine baseline

The implemented machine baseline remains catalog version `1.4.0` until Step-4 implementation deliberately updates it.

Current Steps 1–3 invariants remain in force, including:

- one coherent `ResolvedCatalogContext`;
- no same-ID shadowing inside one resolved context;
- explicit definition/world binding compatibility;
- `runtime.procedure` as sole procedure-local ResourceState owner;
- distinct Encounter / Procedure / Resolution / Continuation lifetimes;
- embedded ExecutionSegment and pending-child descriptors, not standalone workflow classes;
- current world records as current-state authority;
- MechanicalEvents as immutable committed mechanical evidence;
- no generic scheduler/job/workflow engine.

Normative current machine inventory/catalogs:

- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`
- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/entity-structures.json`
- `DEV/CATALOG/identifier-policies.json`
- `DEV/CATALOG/mechanical-surfaces.json`

These still reflect the implemented 1.4.0 baseline and therefore retain some Step-4 legacy IDs until the Step-4 machine-contract implementation lands.

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

Step-4 context/knowledge work does not weaken any Step-3 execution authority.

## 4. Step-4 full-cycle rerun

The owner requested a full Step-4 rerun after approving six logical LLM roles.

Rerun artifacts:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-research-draft.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-decision-resolution.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-resolution-gate.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`

Cross-cutting role draft:

- `DEV/docs/superpowers/specs/2026-08-20-llm-logical-roles-draft.md`

Adversarial result:

```text
owner-decision blockers: 0
mechanically resolved Step-4 findings: 10
later-owner findings: 4
```

No new owner-level semantic gate remained after the six-role rerun.

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
- in-world disagreement belongs to epistemic relations, not objective `disputed` truth;
- lifecycle/supersession is separate from truth status;
- identity-defining statement/scope cannot be silently rewritten after durable reference.

### Knowledge

- `world.knowledge` is the sole durable current fictional epistemic owner;
- initial stance semantics: `aware / known / believed / suspected / rejected`;
- PC factual availability may become known through qualifying resolved sources;
- voluntary PC belief/suspicion/rejection remains player-controlled unless a real rule forces cognition;
- Actor may propose NPC/faction epistemic changes, but core commits them.

### Player disclosure

- `runtime.disclosure` is separate from PC cognition;
- it records sparse material human exposure;
- statement exposure and objective truth-revision exposure are distinct;
- Narrator returns structured disclosure refs and host records exposure only after player-facing emission/acceptance.

### Secret

No generic Secret authority remains. Secret is contextual source eligibility.

- objective truth -> lore/world owner;
- fictional cognition -> `world.knowledge`;
- human exposure -> `runtime.disclosure`;
- reveal/clue planning -> Dramaturg preparation;
- actual automatic reveal mechanics -> actual rules/world owner.

## 6. Six logical LLM roles and Context Assembler

Accepted logical roles:

1. Interpreter;
2. Dramaturg;
3. Actor;
4. Narrator;
5. Chronicler;
6. Commentator.

A role is not necessarily a separate physical model/agent call.

Step-4 invariant:

> each role consumes a separately eligible bounded source bundle plus typed prior-role results; raw private source context does not flow transitively between roles.

A narrower role cannot run inside a physical model context that still contains ineligible broader-role material. Step 6 must use genuine reset/isolation or separate calls where eligibility differs.

Context Assembler is deterministic working machinery, not a seventh role or canonical owner.

## 7. Canonical Story model

Campaign branch contains one peer Story root:

```text
STORY/
    TRANSCRIPT/
    EVENTS/
    MECHANICS/
    NARRATIVE/
```

All Story layers are durable but non-canonical.

- `TRANSCRIPT` — retained visible participant discourse;
- `EVENTS` — story-facing adaptation of semantic LOG/history;
- `MECHANICS` — curated player/spectator-relevant mechanics;
- `NARRATIVE` — editable literary prose.

Story IDs are independent per layer (`T...`, `E...`, `M...`, `N...`) with explicit many-to-many refs.

Default storage is one record per file with deterministic thousand-slot shards.

Non-canonical does not imply fully regenerable: after source compaction, Story may be the only retained exact transcript/literary copy without becoming world/recovery authority.

### Chapter retirement

Retire during Step-4 machine alignment:

```text
world.chapter
transition.chapter_append
event.chapter.appended
```

Literary Chapters are NARRATIVE index groupings with explicit ordered N refs.

### Commentator availability

Story spoiler/reveal eligibility is dependency/reference based, not one scalar global chronology frontier.

Availability applies to complete retrieval units including spoiler-bearing titles/refs/index entries.

Material Story edits recompute availability metadata.

Exact Commentator default perspective/spoiler mode remains Step 6.

## 8. Promotion

Invocation facts, preparation, Actor proposals, Narrator prose and Story prose do not become canon automatically.

Promote/create a stable `world.lore_fact` when a canonical durable knowledge/disclosure/history reference or future consistency requires proposition identity.

An untracked claim may be promoted with `truth_status=undetermined` without asserting it true.

Durable references to local entities still require same-publication dependency closure or rejection.

## 9. Required Step-4 machine alignment

The implementation plan must cover at minimum:

- catalog/version changes implied by retired/added/changed IDs;
- `world.lore_fact` schema and truth/lifecycle separation;
- `world.knowledge` schema/stances and uniqueness semantics;
- `runtime.disclosure` class/schema/identifier policy;
- knowledge/disclosure transitions/events/provenance;
- Context Assembler protocol/bundle contracts and inspectable source manifests;
- role-specific eligibility tests;
- NarrationResult disclosure evidence;
- Story root/layout/IDs/shards/index and four layer schemas;
- dependency-based Story availability;
- legacy Chapter/Secret/embedded-knowledge retirement and migration fixtures;
- live-scene compaction alignment;
- maintenance audit and integrated examples.

No implementation begins before a `superpowers:writing-plans` implementation plan.

## 10. Later-stage ownership

### Step 5

Owns physical durability/transport details:

- Story publication/body-index-availability coherence;
- Story ID allocation under concurrency;
- transcript/history retention/compaction;
- checkpoint/publication interactions;
- multiplayer conflicts and live-scene compaction transport;
- chronology evidence persistence;
- exact host response-delivery acknowledgement.

No default long-lived public/spectator branch.

### Step 6

Owns:

- physical model-call topology for six roles;
- model selection/context isolation/token/latency/cost budgets;
- preparation retention/cache policy if justified;
- default Commentator spoiler/perspective profile and optional deep-source/debug mode;
- optional narration semantic verification/evaluation;
- full migration/catalog-gap/seed/final holistic closure.

## 11. Exact continuation

Step 4 remains the sole active numbered stage.

Next action:

> Use `superpowers:writing-plans` to produce the Step-4 machine-contract implementation plan from the canonical Step-4 specification, then implement via TDD and fresh same-head verification before claiming Step-4 closure.
