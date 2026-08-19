# HDM Mechanical Architecture — Six-Step Roadmap

Status: **ACTIVE WORKING PLAN**

Target branch: `feature/mechanical-runtime-hot-state`

This roadmap is the sequencing gate for the next mechanical-architecture work.
It exists to prevent a later topic from displacing an unfinished earlier one.
The engine-wide architecture workflow is `ARCHITECTURE/DESIGN_PROCESS.md`.

## Operating rule

- Exactly one step may be `IN PROGRESS`.
- A later step may be discussed only when it reveals a dependency of the active
  step; it may not silently become the active implementation topic.
- A step is complete only when its listed artifacts exist, its exit checks pass,
  and unresolved questions are either assigned to a later numbered step or
  recorded explicitly in the backlog with a reason.
- Every completed step updates this file and
  `ARCHITECTURE/CATALOG_DESIGN_STATUS.md` in the same change.
- Architecture is reviewed before implementation. Repository consistency and
  JSON Schema validation are run before claiming completion.
- After all major architecture modules have designs, the owner intends a holistic
  review and additional brainstorming pass over the **entire architecture,
  structures, logic, ownership, schemas, and inter-module relationships**. This
  global review applies to every current accepted/provisional checkpoint rather
  than to one singled-out subsystem.

## Roadmap

| # | Status | Scope | Required result | Exit gate |
|---:|---|---|---|---|
| 1 | **COMPLETE** | Finish the critical audit of already accepted architecture | One audit ledger covering catalog layers, envelopes, IDs, Actors, Assets, Activities, Rule Elements, persistence/time, modes, and information boundaries | Every finding is classified as fixed now, owned by steps 2–6, or deliberately deferred; no unowned blocker or backward dependency remains |
| 2 | **IN PROGRESS — SUPERPOWERS GATE OPEN** | Resources, HP/LifeState, Effects, Conditions, Duration, and Recovery | Minimal normative models plus schemas and catalog alignment | D&D health, lifecycle outcomes, temporary health, slots/uses, rests, timed effects, conditions, concentration, stacking, expiry, and triggered transformations can be represented without duplicate authority or a hard-coded `0 HP -> dead` rule |
| 3 | `BLOCKED BY 2` | `IntentPlan -> Resolution -> Signal/Event` | Exact compound-turn and execution boundary, operation contracts, event payloads, and focused mini-cases | Multiple intents, partial completion, suspension/resume, reactions, idempotency, and atomic mutation segments have deterministic receipts and tests |
| 4 | `BLOCKED BY 3` | Lore, chapters, knowledge, secrets, and the minimum promotion interface | Minimum durable truth/disclosure model and context-selection boundary needed by shared play and strict isolation | Public/restricted knowledge has one authority; event disclosure and context assembly are defined; durable references cannot depend on unpromoted local entities |
| 5 | `BLOCKED BY 4` | Durability, multiplayer, and event-local time | One compatible policy for SOFT/HARD publication, shared visibility, conflicts, chronology, and local time budgets | No proposal contradicts authoritative CORE publication barriers or live-scene ownership; recovery and narration ordering are explicit |
| 6 | `BLOCKED BY 5` | Game modes and LLM execution budget plus migration, catalog-gap, full seed, and final closure | Minimal mode profiles and final cross-cutting architecture consistency pass | Mode activation and isolation are enforceable over the settled state model; promotion/migration/gap/seed ownership is complete; full audit passes |

## Current checkpoint

Step 1 is complete after owner approval of its adversarial second pass. Step 2
is active under the Superpowers architecture gate. Its live design spec is
`DEV/docs/superpowers/specs/2026-08-18-step-2-mechanical-state-ownership-design.md`.
The detailed preliminary Recovery B2 checkpoint is
`DEV/docs/superpowers/specs/2026-08-19-step-2-recovery-boundary-b2-design.md`.
The detailed preliminary Effect-application checkpoint is
`DEV/docs/superpowers/specs/2026-08-19-step-2-effect-application-design.md`.

The ownership map must close before new Step 2 schema fields are introduced.
Accepted ownership sub-decisions now include:

- Actor `hp` is the sole HP/temporary-HP authority, while `life_state_id` is a
  separate lifecycle authority and zero HP never hard-codes death;
- generic Resource semantics use different lifetime owners for persistent
  Actor/Asset state versus serializable procedure-local budgets; procedure
  capacity is derived and procedure consumption is stored without making the
  Resolution its owner;
- non-interchangeable extra action-economy budgets use distinct Resource
  definitions rather than inflating an unrestricted base budget;
- `definition.condition` remains a named rules identity, while each concrete
  application is ordinary Effect-instance state; Actor condition lists are
  derived HOT/SQLite projections, not canon;
- Condition and Effect definitions may share the same validated mechanical
  payload model without mandatory `Condition -> EffectDefinition` indirection;
- LifeState and Condition remain distinct authorities, for example a dying or
  stable lifecycle may coexist with an Unconscious condition application;
- Concentration is not a duration mode. Maintained Effect lifecycle support is
  a narrow Effect-to-Effect relation with zero or one immutable parent per
  dependent Effect, producing a forest rather than an arbitrary dependency
  graph;
- only parent terminal state breaks structural support; suppression does not.
  Parent termination computes and atomically expires the full descendant
  closure, while child termination has no automatic effect on the parent;
- maintenance-root identity is stable for one episode, reverse child indexes are
  HOT/SQLite projections, and ruleset-specific Concentration exclusivity is not
  generalized into a second uniqueness subsystem;
- reusable Duration semantics belong to definitions while each active Effect
  owns its concrete temporal binding. Bindings use one mechanically appropriate
  basis: metric deadline, procedure boundary, or semantic boundary;
- metric elapsed time uses a lazy local monotonic coordinate, never wall clock
  or a universal campaign clock. The coordinate advances only through explicit
  runtime/procedure advancement and may freeze while no mechanic requires
  metric precision;
- the Temporal Agenda is a disposable HOT/SQLite due-index, not a canonical
  scheduler entity or second duration authority;
- metric advancement is interruptible at the nearest due boundary, resolves
  same-time consequences before advancing further, and leaves continuation
  validity/order to Step 3;
- remaining duration is normally derived from an anchor. Re-anchoring occurs
  only when an Effect crosses an actually incompatible temporal basis/context;
  no writable countdown is maintained in parallel with a deadline;
- **preliminary Recovery B2:** the producer owns whether a registered scoped
  boundary occurred, while each authoritative state owner owns its own automatic
  response; RestPolicy does not own cross-subsystem recovery mutation lists;
- Duration/recovery/procedure refresh converge on one registered boundary
  vocabulary, while a concrete BoundaryOccurrence is transient typed runtime
  context rather than a world entity;
- Resource definitions own baseline recovery, pure `resource.recovery` Rule
  Element contributions may modify the calculation, and ResourceState remains
  the sole mutable Resource authority;
- Effect expiry and timed/procedure Resource recovery use the same disposable
  Temporal Agenda/indexing infrastructure; no RecoveryScheduler or separate
  action-economy reset engine is introduced;
- boundary processing discovers the full immediately due set before mutation,
  uses scoped indexes rather than campaign-wide broadcasts, and delegates exact
  same-boundary phase ordering/idempotency to Step 3 and cross-scene
  reconciliation to Step 5;
- **preliminary Effect applications:** one independent target-local application
  is one Effect instance. Multi-target persistent effects split into one
  application per target; spatial mechanics may instead target one Zone/Asset/
  Location record when that is the true lifecycle owner;
- new Effect applications create new instances by default. Refresh preserves one
  lifecycle identity only under explicit policy; replace atomically terminates
  the old identity and creates a new one without overwriting provenance;
- overlap arbitration is derived by target plus rules-origin/application family,
  not by SQL uniqueness or Effect template name. Zero/one-candidate groups take
  the fast path; rare overlaps use a registered whole-application comparator;
- Effect arbitration decides which applications participate, while Rule Element
  resolvers decide how their typed contributions add, collapse, override, or
  otherwise combine;
- generic mutable Effect stacks are not part of the preferred model. Independent
  repeated units are separate applications; one-episode severity/intensity is a
  typed application value or Resource when it has true resource semantics;
- lifecycle, suppression/availability, and derived arbitration are separate
  axes; winner/shadowed state is disposable HOT derivation rather than canonical
  mutable authority;
- genuine Effect-end consequences use typed Effect-end Signal/Event plus existing
  TriggerBinding/Activity machinery. No arbitrary Effect-end callback language
  or separate combination graph is introduced.

The exact continuation point is **minimum LifeState vocabulary and transitions**:
settle the minimum stored lifecycle states, HP/death-save/healing interactions,
Unconscious and other Condition relationships, terminal entity state, and
revival/transformation boundaries. Health/effect selectors, schema/catalog
alignment, focused cases, and the final Step 2 critical pass follow before Step
2 can close.
