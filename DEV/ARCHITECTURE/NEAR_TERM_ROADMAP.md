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
  generalized into a second uniqueness subsystem.

The exact continuation point is **intrinsic Duration / expiry anchors**: settle
reusable duration specification versus concrete progress/anchors,
turn/round/local-time and rest/event endings, and explicit advancement without
any background clock. Concentration support itself is closed; a maintained root
may still have an intrinsic maximum lifetime governed by the Duration contract.
Remaining Effect/Recovery ownership, minimum LifeState transitions, selectors,
schema/catalog alignment, focused cases, and the final Step 2 critical pass
follow before Step 2 can close.
