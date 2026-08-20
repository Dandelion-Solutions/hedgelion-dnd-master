# HDM Mechanical Architecture — Six-Step Roadmap

Status: **ACTIVE WORKING PLAN**

Target branch: `feature/mechanical-runtime-hot-state`

This roadmap is the sequencing gate for the current architecture program. It is
a status/order document, not a duplicate normative specification.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

## Operating rule

- Exactly one numbered architecture step may be `IN PROGRESS`.
- Later steps may be inspected only to expose dependencies/contradictions.
- A step closes when its architecture artifacts/review/verification pass and
  every unresolved implementation item has an explicit later owner or deferred
  implementation obligation.
- Architecture-stage closure does **not** imply that every accepted contract is
  already implemented in GAME/runtime machine schemas.
- Per owner direction, Steps 4–6 complete the remaining architecture sequence
  before broad implementation planning begins.
- After all major modules have designs, run one holistic architecture review over
  the complete ownership graph, schemas, logic and cross-module relationships.

## Roadmap

| # | Status | Scope | Required architecture result | Exit gate |
|---:|---|---|---|---|
| 1 | **COMPLETE / ASSURED** | Critical audit of catalog/class architecture and accepted baseline | Owned audit ledger + retrospective assurance | Every finding fixed, assigned, or consciously deferred; no unowned blocker |
| 2 | **COMPLETE / ASSURED** | Resources, HP/LifeState, Effects, Conditions, Duration, Recovery, selector/query boundaries | Normative ownership models + aligned schemas/catalogs + focused cases + retrospective assurance | No unresolved Step-2 blocker; validation passed |
| 3 | **COMPLETE / ASSURED** | `IntentPlan -> Resolution -> Signal/Event`, including LLM/core execution boundary, Procedure ownership and checkpointable continuation | Canonical Alternative-C execution contract + machine schemas/catalogs + A–N cases + adversarial/final critical review | Final same-head validation succeeded; no unresolved Step-3 blocker |
| 4 | **COMPLETE / ARCHITECTURE CLOSED** | Truth/lore, fictional knowledge, human disclosure, six-role LLM context boundaries, Story projections, promotion | Canonical truth/knowledge/disclosure owners + deterministic Context Assembler + role handoffs + four-layer Story contract + promotion/migration contract | Full-cycle rerun + adversarial resolution complete; obsolete Chapter world authority removed; no unresolved Step-4 architecture blocker; remaining machine realization explicitly deferred |
| 5 | **IN PROGRESS** | Durability, multiplayer, event-local time, Story/transcript publication/retention | Compatible SOFT/HARD publication, shared visibility/conflict/recovery model, Story persistence/compaction | Publication/live-scene ownership, cross-scene recovery, chronology, Story/index publication, transcript retention and shared revision semantics are coherent |
| 6 | `BLOCKED BY 5` | Modes, physical LLM orchestration/budget, migration, catalog gaps, full seed, final closure | Mode profiles + role-call compatibility/isolation + final cross-cutting consistency pass | Mode/context isolation enforceable; migration/gap/seed ownership complete; holistic architecture audit passes |

## Steps 1–2 retrospective assurance

The non-numbered retrospective assurance overlay is complete:

- `DEV/docs/superpowers/specs/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`

Steps 1–2 remain closed and assured.

## Step 3 closure

Owner-approved architecture: **Alternative C**.

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`

Final critical review:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-final-critical-review.md`

Machine-contract plan:

- `DEV/docs/superpowers/plans/2026-08-19-step-3-execution-boundary-machine-contract.md`

Core Step-3 ownership remains:

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
        -> committed MechanicalEvents
        -> receipts / idempotency
        -> mandatory child descriptors

Continuation
    portable suspended Resolution generation
```

## Step 4 — closed architecture stage

Step 4 completed a full design rerun after adoption of the six logical LLM roles.

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`

Rerun chain:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-research-draft.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-decision-resolution.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-resolution-gate.md`

Cross-cutting role draft:

- `DEV/docs/superpowers/specs/2026-08-20-llm-logical-roles-draft.md`

### Canonical Step-4 ownership graph

```text
CURRENT / OBJECTIVE
    ordinary world state owners
    world.lore_fact

FICTIONAL PERSPECTIVE
    world.knowledge

HUMAN PLAYER EXPOSURE
    runtime.disclosure

HISTORY / EVIDENCE
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

NON-CANONICAL STORY
    STORY/
        TRANSCRIPT/
        EVENTS/
        MECHANICS/
        NARRATIVE/
```

### Step-4 decisions settled

- `world.lore_fact` owns independently identified objective propositions;
- objective truth separates `undetermined / established / disproven` from record
  lifecycle and in-world disagreement;
- `world.knowledge` is the sole durable current fictional epistemic owner;
- human-player exposure is separate `runtime.disclosure`, never implicit PC
  knowledge;
- legacy Secret has no independent truth/knowledge authority; secrecy is
  contextual eligibility;
- non-canonical reveal/clue preparation belongs to Dramaturg; actual reveal
  mechanics remain with their real rules/world owner;
- six logical LLM roles have role-specific source eligibility and typed handoffs;
- narrower roles may not inherit broader hidden physical model context without a
  genuine reset/isolation boundary;
- `STORY` lives in the same campaign branch and is non-canonical;
- `STORY/{TRANSCRIPT,EVENTS,MECHANICS,NARRATIVE}` uses layer-local IDs, explicit
  crossrefs, one-record-per-file default and deterministic thousand-slot
  sharding;
- literary Chapters are NARRATIVE index groupings, not world entities;
- Story spoiler/reveal eligibility is dependency/reference based rather than a
  global chronological frontier;
- durable knowledge/disclosure/history refs may promote an untracked proposition
  as `world.lore_fact` with `undetermined` truth without asserting it true;
- durable canonical refs close local-entity promotion dependencies.

### Chapter retirement applied

The obsolete literary-book seed has been removed from the active world machine
namespace:

```text
world.chapter                RETIRED
transition.chapter_append    RETIRED
event.chapter.appended       RETIRED
```

Catalog version `1.5.0` is the first active closed vocabulary without those IDs.
`CATALOG_INVENTORY.md`, `CATALOG_CONTRACTS.md`, `ENTITY_STRUCTURES.md`, machine
entity structures and identifier policy all agree that literary Chapters are
Story/NARRATIVE index metadata rather than world/runtime authority.

Historical derivation documents may still mention the retired IDs as history;
they are non-authoritative where they conflict with the current inventory and
canonical Step-4 specification.

### Deferred Step-4 machine realization

Step-4 architecture is closed, but most of its accepted machine contracts are
**not yet implemented**. This is deliberate, not an assertion of implementation.
The deferred implementation obligation includes at least:

- normalized `world.lore_fact` truth/lifecycle schema;
- normalized `world.knowledge` stances/current ownership;
- `runtime.disclosure` class/schema/provenance;
- Context Assembler request/bundle/source-manifest contracts;
- role-specific eligibility and NarrationResult disclosure evidence;
- Story root/layout/record/index/availability schemas;
- legacy Secret and embedded-knowledge migration;
- live-scene knowledge/disclosure compaction alignment.

These obligations must be carried into the integrated implementation program
after Steps 5–6 architecture, unless a later architecture decision explicitly
supersedes them.

## Step 5 — active architecture stage

Step 5 now owns physical durability/transport and shared-state semantics needed
by the already-defined Step-4 information/Story contracts, including:

- checkpoint publication/restoration;
- SOFT/HARD durability;
- multiplayer/shared conflicts and live-scene compaction transport;
- chronology evidence and cross-scene reconciliation;
- Story record/index/availability publication atomicity;
- Story ID allocation under concurrency;
- transcript/history retention and compaction;
- checkpoint cleanup/expiry;
- exact host response-delivery acknowledgement used by disclosure persistence.

Step 5 does **not** own a separate long-lived public/spectator campaign branch;
the accepted topology remains one durable campaign branch plus temporary
live-scene branches only.

## Step 6 carry-forward

Step 6 owns:

- physical model-call topology for the six logical LLM roles;
- model selection, context reset/isolation and role-call compatibility matrix;
- token/latency/cost budgets;
- default Commentator spoiler/perspective mode and optional deep-source/debug
  mode;
- optional narration semantic verification/evaluation;
- preparation caching/retention if justified;
- exact engine/ruleset/package/catalog snapshot metadata;
- full D&D seed and migration/catalog-gap closure;
- final holistic architecture/catalog/seed audit;
- consolidation of implementation obligations discovered in Steps 4–6 before
  implementation planning begins.

Step 6 may optimize role placement but cannot weaken Step-4 context/authority
boundaries.

## Documentation debt

`DEV/ARCHITECTURE/CATALOG_MODEL.md` and
`DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` remain historical derivation
material with examples/version labels predating current canonical Step-2/3/4
contracts. They are non-authoritative relative to `CATALOG_INVENTORY.md`,
machine catalogs/schemas and canonical specs. Strengthen supersession warnings
before implementation relies on those historical examples.

## Exact continuation point

**Step 5 / Durability, Multiplayer, Event-Local Time, Story/Transcript
Publication and Retention.**

Do not begin broad implementation planning merely because Step 4 is closed;
complete the remaining architecture sequence first unless the owner explicitly
changes that order.
