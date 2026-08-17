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
| 2 | **IN PROGRESS — SUPERPOWERS GATE OPEN** | Resources, Effects, Conditions, Duration, and Recovery | Minimal normative models plus schemas and catalog alignment | D&D health, temporary health, slots/uses, rests, timed effects, conditions, concentration, stacking, and expiry can be represented without duplicate authority |
| 3 | `BLOCKED BY 2` | `IntentPlan -> Resolution -> Signal/Event` | Exact compound-turn and execution boundary, operation contracts, event payloads, and focused mini-cases | Multiple intents, partial completion, suspension/resume, reactions, idempotency, and atomic mutation segments have deterministic receipts and tests |
| 4 | `BLOCKED BY 3` | Lore, chapters, knowledge, secrets, and the minimum promotion interface | Minimum durable truth/disclosure model and context-selection boundary needed by shared play and strict isolation | Public/restricted knowledge has one authority; event disclosure and context assembly are defined; durable references cannot depend on unpromoted local entities |
| 5 | `BLOCKED BY 4` | Durability, multiplayer, and event-local time | One compatible policy for SOFT/HARD publication, shared visibility, conflicts, chronology, and local time budgets | No proposal contradicts authoritative CORE publication barriers or live-scene ownership; recovery and narration ordering are explicit |
| 6 | `BLOCKED BY 5` | Game modes and LLM execution budget plus migration, catalog-gap, full seed, and final closure | Minimal mode profiles and final cross-cutting architecture consistency pass | Mode activation and isolation are enforceable over the settled state model; promotion/migration/gap/seed ownership is complete; full audit passes |

## Current checkpoint

Step 1 is complete after owner approval of its adversarial second pass. Step 2
is active for research and drafting, but its architecture cannot be accepted
until the Superpowers gate in `DESIGN_PROCESS.md` is satisfied. The first Step 2
deliverable remains the ownership map proving where every Resource, Effect,
Condition, Duration, and Recovery fact lives before new schema fields are added.
