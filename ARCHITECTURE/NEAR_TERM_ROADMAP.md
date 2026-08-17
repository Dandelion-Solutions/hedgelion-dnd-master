# HDM Mechanical Architecture — Six-Step Roadmap

Status: **ACTIVE WORKING PLAN**

Target branch: `feature/mechanical-runtime-hot-state`

This roadmap is the sequencing gate for the next mechanical-architecture work.
It exists to prevent a later topic from displacing an unfinished earlier one.

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
| 1 | **COMPLETE** | Finish the critical audit of already accepted architecture | One audit ledger covering catalog layers, envelopes, IDs, Actors, Assets, Activities, Rule Elements, persistence/time, modes, and information boundaries | Every finding is classified as fixed now, owned by steps 2–6, or deliberately deferred; no unowned blocker remains |
| 2 | **IN PROGRESS** | Resources, Effects, Conditions, Duration, and Recovery | Minimal normative models plus schemas and catalog alignment | D&D health, temporary health, slots/uses, rests, timed effects, conditions, concentration, stacking, and expiry can be represented without duplicate authority |
| 3 | `BLOCKED BY 2` | `IntentPlan -> Resolution -> Signal/Event` | Exact compound-turn and execution boundary, operation contracts, event payloads, and focused mini-cases | Multiple intents, partial completion, suspension/resume, reactions, idempotency, and atomic mutation segments have deterministic receipts and tests |
| 4 | `BLOCKED BY 3` | Durability, multiplayer, and event-local time | One compatible policy for SOFT/HARD publication, shared visibility, conflicts, chronology, and local time budgets | No proposal contradicts authoritative CORE publication barriers or live-scene ownership; recovery and narration ordering are explicit |
| 5 | `BLOCKED BY 4` | Game modes and LLM execution budget | Minimal mode-profile contract for quick narrative, ordinary adventure, canonical D&D, and strict detective isolation | Each mode states which mechanics/context isolation are active; presentation detail is not confused with rules enforcement; ordinary turns retain a bounded fast path |
| 6 | `BLOCKED BY 5` | Lore/chapters/knowledge/secrets plus promotion, migration, catalog-gap, and seed closure | Final cross-cutting contracts and architecture consistency pass | Durable narrative context, restricted knowledge, entity promotion, migrations, gap reports, and selected ruleset seed ownership are unambiguous; full audit passes |

## Current checkpoint

Step 1 is closed in `ARCHITECTURE/CRITICAL_ARCHITECTURE_AUDIT.md`. Step 2 is
active. Its first deliverable is a dependency/ownership map proving where each
resource, effect, condition, duration, and recovery fact lives before any new
field or schema is added.
