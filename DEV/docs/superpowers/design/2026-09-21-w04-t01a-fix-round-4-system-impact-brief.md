# W04.T01A fix round 4 — Implementation Impact Brief

**DATE:** 2026-09-21
**TASK:** W04.T01A — coordination-family admission and exact participant authority
**STATUS:** **SYSTEM-IMPACT STOP / SENIOR REVIEW REQUIRED**

## Trigger

The round-four review established that the proposed
`mechanics.validate_native_ordering_owner()` is a new public/manual mirror of
Procedure/Continuation ordering validation. It is not an existing authoritative
owner route. No approved existing complete Procedure, Continuation, Choice or
Reaction validator has been identified.

Using that function to classify `RULE_OWNED_ORDERED` would therefore add a new
validation authority and dependency boundary rather than consume an accepted
native owner result. This crosses the approved T01A implementation envelope.

This brief records the stop. It does not authorize another production repair.

## Last safe state

```text
LAST_SAFE_SHA: ce05e58e9f398e779dcdda68cb9aec53e82cfe7a
LAST_SAFE_PRODUCT_TREE: exact clean-basis restoration of the ruled task paths
RESTORED_PRODUCT_BASIS: 0bd665860386e04ecd2efb589e58069a4d6da033
CURRENT_REJECTED_HEAD: 3d88935c5d26be30db167464eb3d9aaad60e888a
CURRENT_TASK: W04.T01A fix round 4
```

`80d1cedfce7f529df96ea2c4b2342ce466cc8806` is the documentation-only
acceptance of the clean-basis restore after `ce05e58`; it does not change the
last safe product tree. The current rejected implementation is already present
in published ancestors after that clean basis. This documentation checkpoint
does not alter it.

## Approved expectation

The accepted WP-17 owner law and final W04 ruling require:

- an admitted native owner to remain authoritative when it owns response order,
  execution, current state or resume semantics;
- Collaboration to return `RULE_OWNED_ORDERED` without mirroring the native
  responder set, queue, pending response, order, generation or continuation
  state;
- native owner/currentness evidence to be revalidated through its accepted route;
- no caller-shaped carrier, callback, token, registry or local second
  currentness/validation authority.

## Evidence

1. `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-canonical-spec.md:56-86`
   says the existing native owner always wins and explicitly forbids generic
   collaboration from mirroring Procedure/Continuation/Choice/Reaction order or
   continuation state.
2. `DEV/docs/superpowers/design/2026-09-21-w04-t01a-t05a-t07a-senior-design-rulings.md:102-123`
   requires `RULE_OWNED_ORDERED` when an existing native ordered owner applies;
   Collaboration may not mirror it, and a native basis must be owner-validated.
3. The rejected round-four implementation imports and calls the new public
   helper at `GAME/TOOLS/collaboration.py:24,566`. The helper is defined only
   by the rejected change at `GAME/TOOLS/mechanics.py:692-819` and manually
   interprets Procedure/Continuation state to return an ordering verdict.
4. The pre-existing mechanics functions at
   `GAME/TOOLS/mechanics.py:624-689` validate only Procedure/Continuation
   bindings within an execution call; they are not a complete public native
   ordering-owner admission route. `GAME/TOOLS/recovery_roots.py:482-529`
   validates operational-root eligibility, not Choice/Reaction/Continuation
   ordering authority.
5. The current schemas define serialized shapes, including the Continuation
   `pending_response` Choice/Reaction union, but do not identify an accepted
   owner-issued ordering validator or composition-root route:
   `DEV/SCHEMAS/runtime-procedure-state.schema.json`,
   `DEV/SCHEMAS/runtime-continuation-state.schema.json`, and
   `DEV/SCHEMAS/combat-minimal-procedure-state.schema.json`.
6. Repository symbol inspection found the proposed helper as the only
   `validate_native_ordering_owner` route. No approved complete
   Procedure/Continuation/Choice/Reaction validator was identified for T01A to
   consume.

## Affected owners and consumers

- W04 Collaboration admission and derived `RULE_OWNED_ORDERED` classification.
- The native `runtime.procedure` and `runtime.continuation` execution owners.
- Pending Choice/Reaction contracts embedded in Continuation state.
- `GAME/TOOLS/mechanics.py`, which the rejected change makes a new public
  cross-owner validation surface.
- `GAME/TOOLS/collaboration.py`, its owner-local tests and collaboration
  admission schemas.
- Downstream T01B-T04B collaboration consumers, which must not consume an
  unadmitted ordering verdict.
- Wave-05 shared/final-writer surfaces, which remain out of scope and
  unauthorized.

## Protected invariants

- Native Procedure/Continuation/Choice/Reaction ordering and resume semantics
  have one authoritative owner.
- Collaboration owns bounded human-input collection only; it does not own
  execution, mechanics, RNG, chronology, or native response order.
- A typed mapping, structural validator, current flag, callback, registry or
  public helper cannot mint native currentness or ordering authority.
- Invalid, stale, incomplete or unsupported native basis evidence fails closed.
- Collaboration cannot replace an admitted native ordered owner with generic
  collection or duplicate its state.
- No new persistent/interface owner, dependency direction, Wave-05 writer or
  runtime path is introduced by this stop.

## What can proceed without the disputed change

- Preserve the accepted T01A boundary and the finite collaboration dependency
  classes already ruled by Senior/design.
- Keep the ordered-owner branch stopped or fail closed until an admitted native
  route exists.
- Perform Senior/design evidence work to identify an existing complete owner
  validator, if one exists, or to specify the missing owner boundary.
- Restore the rejected production surface to the last safe product tree in a
  separately authorized execution slice; this brief does not perform that
  restoration.

## Safe options

1. **Identify an existing admitted route.** Senior/design must name the complete
   native Procedure/Continuation/Choice/Reaction validator, its producer and
   trusted composition/root boundary, and its currentness proof before T01A can
   consume it. The round-four review has not identified such a route.
2. **Return to design for the missing owner boundary.** Specify the owner,
   validator contract, composition root, persistence/currentness basis, consumers,
   tests and version impact before implementation resumes.
3. **Narrow/defer ordered classification.** With an explicit Senior ruling, keep
   T01A limited to admitted non-ordered collaboration outcomes and defer
   `RULE_OWNED_ORDERED` until its native route is accepted.
4. **Preserve the stop.** Do not replace the missing route with a local mirror,
   callback, protocol, registry or hand-written public validator.

## Recommendation

Keep W04.T01A at the System-Impact stop and do not use
`validate_native_ordering_owner()` as an authority route. Restore the rejected
production chain to the last safe product basis through the normal execution
owner, then choose option 1 or 2; option 3 requires an explicit scope ruling.

## Cost / risk if bypassed

If the local helper is accepted, Collaboration can decide that a caller-loaded
Procedure/Continuation record owns ordering without an admitted owner-issued
result. That creates a second validation/currentness authority, allows stale or
forged ordered state to suppress or replace collaboration, and can diverge from
the actual Choice/Reaction/Continuation execution owner during retry or
recovery. The safe cost of stopping is limited to the T01A lane schedule.

## Exact prior rejected checkpoint and version transitions

The following are historical rejected implementation checkpoints. They are
non-precedential and do not authorize dependent work.

### Earlier pre-ruling attempt, removed by the clean-basis restore

| Checkpoint | Exact transition | Disposition |
|---|---|---|
| `a300b23774f9ed31dfbc991be73211c338976955` | `GAME/TOOLS/collaboration.py` absent -> `1.0.1`; `runtime.collaboration_obligation` schema absent -> `1` | Rejected; removed by `6cbde6a4845376ee55e8e9c10a17f354111a276d` |
| `59b12a3075155c9f5984420691ff98be32562c6f` | collaboration module `1.0.1` -> `1.0.2`; local schema remained `1` | Rejected; removed by the same restore |
| `de3254041b1126a5f46f53e1b8fcbee27153f968` | collaboration module `1.0.2` -> `1.0.2`; schema/projection remained `1` | Rejected projection repair; removed by the same restore |

### Fresh post-ruling attempt from the clean product basis

| Checkpoint | Exact transition | Disposition |
|---|---|---|
| `0b6f5d6cd18a6ade75e74b4b8d59790832bfa80c` | collaboration module absent -> `1.0.1`; local collaboration schema `absent -> 1` | Rejected targeted reimplementation |
| `d687a9f08eafcc88fd5b5e71aea02e36dba7b9ef` | collaboration module `1.0.1 -> 1.0.2`; local schema remained `1` | Rejected ordered-owner repair |
| `6435bf914a00c9b4ef3896a4b749a8cd20583b2d` | collaboration module `1.0.2 -> 1.0.3`; local schema remained `1` | Rejected fail-closed repair |
| `58444e0fcd08ba7dce651cfb2c0799345b227591` | collaboration module `1.0.3 -> 1.0.4`; `GAME/TOOLS/mechanics.py` `1.0.5 -> 1.0.6`; local collaboration schema remained `1` | Rejected round-four route-validation change; introduced the disputed public helper |

`3d88935c5d26be30db167464eb3d9aaad60e888a` is the current published head
containing that rejected production chain plus a separate T05A documentation
brief. None of these aborted transitions is a current accepted version basis.

## Version Impact Gate

```text
VERSION_IMPACT: NONE
```

This checkpoint adds only this development design brief under
`DEV/docs/superpowers/design/`. It changes no production module, serialized
schema, campaign/storage generation, catalog generation, digest generation,
projection, cursor, `CURRENT_PROGRESS`, Wave-05 surface or version-bearing
owner. The prior rejected transitions above are recorded as history only; this
documentation does not repeat or extend them.

## Checkpoint state

```text
SYSTEM_IMPACT: SENIOR_REVIEW_REQUIRED
UNPUBLISHED_WORK: NONE after this documentation-only commit, publication and
  remote read-back; before that checkpoint, this brief is the only new local
  work. No production, cursor, CURRENT_PROGRESS, Wave-05 or .entire/ changes
  are made in this slice.
```
