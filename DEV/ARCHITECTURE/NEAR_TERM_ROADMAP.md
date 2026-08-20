# HDM Mechanical Architecture — Six-Step Roadmap

Status: **ACTIVE WORKING PLAN**

Target branch: `feature/mechanical-runtime-hot-state`

This roadmap is the sequencing gate for the current architecture program. It is a status/order document, not a duplicate normative specification.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

## Operating rule

- Exactly one numbered step may be `IN PROGRESS`.
- Later steps may be inspected only to expose dependencies/contradictions.
- A step closes only after required artifacts/review/verification pass and every unresolved item has a later owner or explicit deferred/debt/backlog record.
- Step closure updates this roadmap and `DEV/ARCHITECTURE/CATALOG_DESIGN_STATUS.md`.
- After all major modules have designs, run one holistic architecture review over the complete ownership graph, schemas, logic and cross-module relationships.

## Roadmap

| # | Status | Scope | Required result | Exit gate |
|---:|---|---|---|---|
| 1 | **COMPLETE / ASSURED** | Critical audit of catalog/class architecture and accepted baseline | Owned audit ledger + retrospective assurance | Every finding fixed, assigned, or consciously deferred; no unowned blocker |
| 2 | **COMPLETE / ASSURED** | Resources, HP/LifeState, Effects, Conditions, Duration, Recovery, selector/query boundaries | Normative ownership models + aligned schemas/catalogs + focused cases + retrospective assurance | No unresolved Step-2 blocker; maintenance/schema/unit-test validation passes |
| 3 | **COMPLETE / ASSURED** | `IntentPlan -> Resolution -> Signal/Event`, including LLM/core execution boundary, Procedure ownership and checkpointable continuation | Canonical Alternative-C execution contract + machine schemas/catalogs + A–N cases + adversarial/final critical review | Final same-head validation succeeded; no unresolved Step-3 blocker |
| 4 | **IN PROGRESS — ARCHITECTURE CANONICAL / MACHINE ALIGNMENT PENDING** | Truth/lore, fictional knowledge, human disclosure, six-role LLM context boundaries, Story projections, promotion | Canonical truth/knowledge/disclosure owners + deterministic Context Assembler + role handoffs + four-layer Story contract + promotion/migration contract | Machine catalogs/schemas/runtime/template/tests align with canonical Step-4 spec; no duplicate knowledge/Secret/Chapter authority; validation passes |
| 5 | `BLOCKED BY 4` | Durability, multiplayer, event-local time, Story/transcript publication/retention | Compatible SOFT/HARD publication, shared visibility/conflict/recovery model, Story persistence/compaction | Publication/live-scene ownership, cross-scene recovery, chronology, Story/index publication, transcript retention and shared revision semantics are coherent |
| 6 | `BLOCKED BY 5` | Modes, physical LLM orchestration/budget, migration, catalog gaps, full seed, final closure | Mode profiles + role-call compatibility/isolation + final cross-cutting consistency pass | Mode/context isolation enforceable; migration/gap/seed ownership complete; full audit passes |

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

Current machine baseline remains catalog version `1.4.0` until Step-4 machine alignment deliberately changes it.

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

## Step 4 — active stage

Step-4 architecture has completed its full design rerun with the six accepted logical LLM roles and has a canonical specification:

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

### Step-4 decisions now settled

- `world.lore_fact` owns independently identified objective propositions;
- objective truth separates `undetermined / established / disproven` from record lifecycle and in-world disagreement;
- `world.knowledge` is the sole durable current fictional epistemic owner;
- human-player exposure is separate `runtime.disclosure`, never implicit PC knowledge;
- legacy Secret is retired as a truth/knowledge authority; secrecy is contextual eligibility;
- non-canonical reveal/clue preparation belongs to Dramaturg; real reveal mechanics remain with their actual rule/world owner;
- six logical LLM roles have role-specific source eligibility; a role consumes typed handoffs, not another role's raw private context;
- a narrower role cannot physically follow a broader secret-bearing role in the same model context unless the platform provides genuine reset/isolation;
- `STORY` lives in the same campaign branch and is non-canonical;
- `STORY/{TRANSCRIPT,EVENTS,MECHANICS,NARRATIVE}` has layer-local IDs, explicit crossrefs, one-record-per-file default and deterministic thousand-slot sharding;
- literary Chapters are NARRATIVE index grouping, not `world.chapter` entities;
- Story spoiler/reveal eligibility is dependency/reference based rather than one global chronological frontier;
- durable knowledge/disclosure/history refs may promote an untracked proposition as `world.lore_fact` with `undetermined` truth without asserting it true;
- durable canonical refs still close local-entity promotion dependencies.

### Step-4 legacy retirements required by implementation

Retire/replace as machine authority:

```text
world.chapter
transition.chapter_append
event.chapter.appended
legacy Secret truth/knowledge ownership
embedded PC/NPC/Faction current knowledge ownership
objective truth.disputed semantics
```

Migration must preserve evidence conservatively rather than guessing ambiguous old truth/disclosure state.

### Step-4 exact continuation

Architecture is canonical, but the numbered stage remains active until machine alignment and verification are complete.

Next action:

1. use `superpowers:writing-plans` for the Step-4 machine-contract implementation plan;
2. implement catalog/schema/runtime/template/test alignment through TDD;
3. run integrated/adversarial machine cases and maintenance audit;
4. run final same-head verification;
5. only then close Step 4 and activate Step 5.

## Step 5 carry-forward

Step 5 owns physical repository durability/transport after Step-4 semantics are implemented, including:

- checkpoint publication/restoration;
- SOFT/HARD durability;
- multiplayer/shared conflicts and live-scene compaction transport;
- chronology evidence and cross-scene reconciliation;
- Story record/index/availability publication atomicity;
- Story ID allocation under concurrency;
- transcript/history retention and compaction;
- checkpoint cleanup/expiry;
- exact host response-delivery acknowledgement used by disclosure persistence.

Step 5 does **not** own a separate long-lived public/spectator campaign branch; the accepted topology remains one durable campaign branch plus temporary live-scene branches only.

## Step 6 carry-forward

Step 6 owns:

- physical model-call topology for the six logical LLM roles;
- model selection, context reset/isolation and role-call compatibility matrix;
- token/latency/cost budgets;
- default Commentator spoiler/perspective mode and optional deep-source/debug mode;
- optional narration semantic verification/evaluation;
- preparation caching/retention if justified;
- exact engine/ruleset/package/catalog snapshot metadata;
- full D&D seed and migration/catalog-gap closure;
- final holistic architecture/catalog/seed audit.

Step 6 may optimize role placement but cannot weaken Step-4 context/authority boundaries.

## Documentation debt

`DEV/ARCHITECTURE/CATALOG_MODEL.md` and `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` remain historical derivation material with examples/version labels predating current canonical Step-2/3/4 contracts. They are non-authoritative relative to `CATALOG_INVENTORY.md`, machine catalogs/schemas and canonical specs. Strengthen supersession warnings before implementation relies on those historical examples.
