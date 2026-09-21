# W04.T01A fix round 1 — System-Impact Brief

TRIGGER: The approved targeted repair requires a finite, owner-defined,
schema-validated native opportunity route for `AGENCY_DEPENDENT_COLLECTIVE`,
but the current repository has no such route. Creating one would add or change
a persistent/runtime contract and native currentness owner beyond the approved
implementation envelope.

LAST_SAFE_SHA: `17598c8a8bc86ffe0b1278b5be5ef31f7f66bf5d`

CURRENT_TASK: W04.T01A collaboration admission, fix round 1.

## Approved expectation

The accepted T01A ruling requires Collaboration to revalidate a bounded
candidate against the smallest applicable native currentness/ownership basis.
The candidate may nominate `native_owner_kind`, `native_owner_id`, and
`opportunity_id`, but the native owner must supply the authoritative current
opportunity. Existing Procedure/Continuation/Choice/Reaction ordering remains
the separate `RULE_OWNED_ORDERED` route.

## Discovered implementation pressure

`GAME/TOOLS/collaboration.py` currently loads the nominated native record and
looks for `state.coordination_opportunities`. That field is not declared by
any current native owner schema:

- `DEV/SCHEMAS/runtime-interaction-state.schema.json` and
  `DEV/SCHEMAS/runtime-intent-plan-state.schema.json` reject unknown fields and
  do not define a native opportunity collection.
- `DEV/SCHEMAS/world-scene-state.schema.json` rejects
  `coordination_opportunities` as an additional property and requires a
  different scene record shape.
- `DEV/SCHEMAS/runtime-procedure-state.schema.json` and
  `DEV/SCHEMAS/runtime-continuation-state.schema.json` define their own native
  execution/continuation fields; Continuation's admitted response route is
  the finite Choice/Reaction union, not a generic coordination opportunity.
- `GAME/SCHEMA/player.schema.yaml` defines PLAYER binding and authorization,
  not decision opportunities.
- `GAME/TOOLS/native_storage.py` has finite physical family routes, but no
  `coordination_opportunity` family route.

The only current `coordination_opportunities` records are the implementation
fixture shape in `DEV/TESTS/test_rd12_collaboration.py` and the corresponding
untyped lookup in `collaboration.py`. The accepted
`DEV/SCHEMAS/intent-clause.schema.json` field is only a bounded nomination;
it does not define the nominated native opportunity's record schema or
currentness semantics.

## Evidence from verification

The focused baseline remains 18 passing tests. Direct schema validation of the
fixture/native records showed:

- scene fixture: `coordination_opportunities` is unexpected, `name` is
  missing, and `active` has the wrong type;
- interaction fixture: `interaction_id`, `kind`, and `state_revision` are
  unexpected under the current schema;
- missing `kind` was accepted for `runtime.interaction`,
  `runtime.intent_plan`, and `world.player`; scene rejection came from generic
  native identity validation rather than a native opportunity schema.

These results show that the current positive collective path is not reloading
an admitted owner contract. Tightening the optional kind check or adding a
schema to this task would not be a local repair: it would choose and define a
new native contract/authority.

## Affected owners and protected invariants

- W04 Collaboration admission and obligation persistence.
- Interaction/IntentPlan native owners and their persistent schemas.
- The eventual native decision-opportunity owner, currently unspecified.
- WP-11 physical routing and owner-local identity/schema validation.
- W03 PLAYER/control authorization, which must not become an opportunity
  authority.

Protected invariants include no caller-selected family/contributors/currentness,
no callback or second currentness owner, no generic collaboration in place of
an admitted ordered owner, and no collaboration authority over native gameplay
state.

## What can proceed without the disputed change

- Preserve the current known-ID transport boundary and owner-local validation.
- Preserve the existing finite `RULE_OWNED_ORDERED` route once its native
  records are supplied through their accepted schemas.
- Add the positive collective admission tests only after a concrete native
  opportunity owner/schema/route is accepted.

## Safe options

1. Senior design review designates an existing native owner and its exact
   schema/currentness route, then updates the T01A implementation contract.
2. Senior narrows T01A to the already admitted ordered route and defers
   `AGENCY_DEPENDENT_COLLECTIVE` until a native opportunity contract exists.
3. If a new opportunity record/family is genuinely required, return through
   the architecture/specification process before implementation; this brief is
   not authorization for that change.

RECOMMENDATION: Choose option 1 or 2 before production-code changes. Do not
teach Collaboration to interpret the current untyped `state` fixture as a
native opportunity.

COST / RISK IF RECOMMENDATION IS WRONG: A local-looking patch could admit
caller-shaped or stale opportunity data, create a second currentness authority,
or persist a collaboration obligation whose native owner cannot reproduce its
authority. That would violate the T01A ruling and make replay/recovery
currentness unsound.

UNPUBLISHED_WORK: NONE. No production, schema, test, cursor, or version files
were changed in this stop slice. The pre-existing untracked `.entire/`
directory was left untouched.
