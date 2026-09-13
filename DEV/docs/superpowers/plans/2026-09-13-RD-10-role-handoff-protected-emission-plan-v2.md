# RD-10 — Role Containment / Typed Handoffs / Protected Emission — Executable Plan v2

Status: **AUTHOR REPAIR — SUPERSEDES THE EARLIER RD-10 PLAN FOR EXECUTION**

Goal: realize registered logical-phase containment, explicit rebinding, minimum typed handoffs, finite fallback and protected Narrator-visible emission inside one physical conversational context.

Direct readiness: `R054,R055,R056,R057,R118,R133,R137`.
Owners: Step-4 role/context + single-context amendment, R2.4, WP-08, Step-5.12. RD-11 owns Context Runtime selection/allocation; RD-05 owns mechanics/execution.

## Exact impact

- `NEW_CREATE GAME/TOOLS/turn_runtime.py`
- `NEW_CREATE GAME/TOOLS/emission.py`
- `EXISTING_MODIFY GAME/CORE/AI_REASONING.md` as primary ordinary-gameplay containment wording owner
- `INSPECT_ONLY GAME/CORE/RUNTIME.md`, `GAME/CORE/PLAY_POLICY.md`
- `NEW_CREATE DEV/SCHEMAS/turn-envelope.schema.json`
- `NEW_CREATE DEV/SCHEMAS/interpreter-result.schema.json`
- `NEW_CREATE DEV/SCHEMAS/preparation-draft.schema.json`
- `NEW_CREATE DEV/SCHEMAS/actor-proposal.schema.json`
- `NEW_CREATE DEV/SCHEMAS/story-projection-draft.schema.json`
- `NEW_CREATE DEV/SCHEMAS/narration-result.schema.json`
- `NEW_CREATE DEV/TESTS/test_rd10_role_emission.py`
- direct `DEV/PROJECT_MAP.md` / `DEV/TOOLS/audit_engine.py` projections only.

All DEV result schemas are ephemeral validation contracts, not durable campaign owners. No role-result bus, semantic authority in TurnEnvelope, private-context transfer, same-envelope Story feedback, late-steering authority, physical-presence eligibility or sanitizer-only emission boundary may be introduced.

Every checkpoint is `RED -> GREEN -> REFACTOR -> focused VERIFY -> commit`; no RED-only checkpoint.

## Checkpoint 1 — envelope/rebind/fallback

Test class: `TurnEnvelopeContainmentTests`.

Interfaces:
```text
start_turn(request_basis) -> TurnEnvelope
bind_phase(envelope, phase, subject, recipient, purpose, profile_ref, bundle_ref, allowed_results)
accept_phase_result(envelope, typed_result)
advance_phase(envelope, registered_transition)
select_fallback(envelope, unsatisfiable) -> RegisteredFallback
```

Prove only registered phase/result families participate; every material phase rebinds role/subject/recipient/purpose/profile/bundle/allowed-results/authority/output contract; retrieved/player/campaign prose cannot self-promote to engine instruction; physical prompt presence is not eligibility.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd10_role_emission.TurnEnvelopeContainmentTests -v
```

## Checkpoint 2 — exact typed handoffs

Test class: `TypedHandoffTests`.

Implement the five result schemas in the impact list. `actor-proposal` includes `NO_CHANGE`; do not create another generic result family. Each result carries only the minimum semantic payload required by its registered consumer and applicable subject/recipient/purpose/generation identity.

Reject raw RoleContextBundle handoff, role frames/private source sets/private reasoning, unaccepted drafts as authority, MechanicalContext substitution and model-invented result families.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd10_role_emission.TypedHandoffTests -v
```

## Checkpoint 3 — Chronicler/Narrator protected capacity

Test class: `ProtectedCapacityTests`.

Story opportunity is `NO_BACKLOG | SERVICE(window) | DEFER(reason)`. Correctness, agency, mechanics and visible-response capacity are reserved first. Story output from the current envelope cannot feed gameplay phases in that envelope. After optional Chronicler work, Narrator gets a fresh rebind and separately assembled eligible bundle. RD-13 remains Story authority.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd10_role_emission.ProtectedCapacityTests -v
```

## Checkpoint 4 — protected emission / R054-R057

Test class: `ProtectedEmissionTests`.

Interfaces in `GAME/TOOLS/emission.py`:
```text
validate_narration_result(result, recipient_scope, disclosure_basis) -> ValidatedNarration
commit_visible_payload(validated_result) -> EMISSION_COMMIT
```

Only validated Narrator player-facing payload may cross ordinary visible emission. Tests include hidden Dramaturg fact, Actor-private cognition, internal trace/debug/control metadata negatives and lawful positive disclosure. Sanitization is defense-in-depth only after structural role/eligibility/output validation.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd10_role_emission.ProtectedEmissionTests -v
```

## Checkpoint 5 — auxiliary work / late steering / finite UNSATISFIABLE

Test class: `AuxiliaryFallbackTests`.

Invisible auxiliary work uses registered phases/results only. Late steering may alter presentation/task emphasis but cannot change role, source eligibility, requiredness, authority, deterministic frontier or disclosure. `UNSATISFIABLE` selects exactly one registered finite alternative and terminates the failed attempt; no blind reassembly loop, ad-hoc profile or evidence drop. This owns `R118,R133,R137` in the role/emission boundary, not RD-05.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd10_role_emission.AuxiliaryFallbackTests -v
```

## Checkpoint 6 — instruction owner alignment

Test class: `InstructionOwnerTests`.

Modify `GAME/CORE/AI_REASONING.md` as the primary ordinary-gameplay containment wording owner. Inspect `RUNTIME.md` and `PLAY_POLICY.md`; if either currently contradicts accepted containment semantics, stop and return to planning rather than silently widening write scope. Prove no competing active role-eligibility wording owner.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd10_role_emission.InstructionOwnerTests -v
```

## Final verification

```bash
python3 -m unittest DEV.TESTS.test_rd10_role_emission -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Version Impact classifies the instruction contract and ephemeral validation schemas; no durable campaign migration follows from TurnEnvelope/result contracts.

Before each checkpoint fresh-read R2.4, WP-08, Step-4 amendment, Step-5.12 and exact touched current files. Mechanical path drift may be recorded; semantic owner drift returns to planning.

RD-10 closes only its seven direct leaves. `R124` and other downstream joins remain gated on RD-11/RD-12/package closure.