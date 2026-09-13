# RD-10 — Role Containment / Typed Handoffs / Protected Emission — Executable Implementation Plan

Goal: realize one registered TurnEnvelope route for logical phase containment, explicit rebinding, minimum typed handoffs, finite fallback and Narrator-only protected visible emission inside one physical conversational context.

Direct readiness: `R054,R055,R056,R057,R118,R133,R137`.
Canonical owners: Step-4 role/context owner + single-context amendment, R2.4, WP-08, Step-5.12 delivery/disclosure. RD-11 owns Context Runtime selection/allocation; RD-05 owns mechanics/execution.

## Impact Envelope

- `NEW_CREATE GAME/TOOLS/turn_runtime.py`
- `NEW_CREATE GAME/TOOLS/emission.py`
- `EXISTING_MODIFY GAME/CORE/AI_REASONING.md` as primary containment-text owner
- `EXISTING_MODIFY GAME/CORE/RUNTIME.md` / `GAME/CORE/PLAY_POLICY.md` only for invocation/reference alignment where required
- `NEW_CREATE DEV/SCHEMAS/turn-envelope.schema.json`
- minimal registered phase-result schemas in `DEV/SCHEMAS` only where no current accepted equivalent exists; these validate ephemeral values and are never durable campaign records
- `NEW_CREATE DEV/TESTS/test_rd10_role_emission.py`
- direct audit/project-map projections only.

Forbidden: role=separate-call requirement, raw private bundle/frame handoff, hidden-reasoning persistence, generic role-result bus, TurnEnvelope semantic authority, same-envelope Story feedback, late-steering authority, physical-presence eligibility, second disclosure owner, visible trace/debug/tool leakage, sanitizer-only fencing.

## Task 1 — RED: registered phase/rebind containment

Create `DEV/TESTS/test_rd10_role_emission.py` proving:
- only registered phase/result families participate in ordinary execution;
- every material phase rebinds role, subject/recipient, purpose, profile/bundle identity, allowed typed prior results, accepted deterministic refs, authority limits and output contract;
- physical presence of another role's material never makes it eligible;
- instruction-like campaign/retrieved/player prose cannot self-promote to engine instruction or trigger role switch.

Expected RED: no shipped turn runtime exists.

## Task 2 — GREEN: `turn_runtime.py`

Implement ephemeral control interfaces equivalent to:
```text
start_turn(request_basis) -> TurnEnvelope
bind_phase(envelope, phase, subject, recipient, purpose, profile_ref, bundle_ref, allowed_results)
accept_phase_result(envelope, typed_result)
advance_phase(envelope, registered_transition)
select_fallback(envelope, UNSATISFIABLE) -> one registered finite alternative
```

TurnEnvelope may track legal phases, deterministic frontier refs, bundle/profile identities, allowed result refs, Story service-opportunity result and protected output reservation. It may not establish semantic state, knowledge, disclosure, mechanics or Story coverage.

Commit boundary: envelope/rebind/fallback + tests.

## Task 3 — minimum typed handoffs

Realize only registered result families needed by current owners (e.g. InterpreterResult, PreparationDraft, ActorProposal/NO_CHANGE, StoryProjectionDraft, NarrationResult) with purpose/subject/recipient/generation scoping.

Tests reject:
- raw RoleContextBundle transport as another phase's evidence;
- role frames/private source sets/private reasoning as handoff payload;
- unaccepted drafts as continuity/authority evidence;
- MechanicalContext substitution for role context.

Deterministic code owns validation, serialization/final IDs/bookkeeping; model-facing transport stays minimum-semantic.

## Task 4 — Chronicler / Narrator boundary and protected capacity

TurnEnvelope evaluates Story backlog opportunity on ordinary turns but reserves correctness/agency/mechanics and protected Narrator/output capacity first.

Rules:
- Story service may be `NO_BACKLOG | SERVICE(window) | DEFER(reason)`;
- current-envelope Story output cannot feed gameplay roles in that same envelope;
- after Chronicler service, Narrator always gets a fresh rebind and separately assembled eligible bundle;
- Story contention yields before protected visible response capacity.

RD-10 controls phase sequencing only; Story source/coverage authority stays its native owner/RD-13.

## Task 5 — protected emission boundary

Implement `GAME/TOOLS/emission.py`:
```text
validate_narration_result(result, recipient_scope, disclosure_basis)
commit_visible_payload(validated_result) -> EMISSION_COMMIT
```

Only validated Narrator player-facing payload intentionally crosses ordinary visible emission. Internal role frames, auxiliary drafts, ContextTrace, tool/debug/control metadata and maintenance payloads remain internal.

Tests include hidden Dramaturg fact, Actor-private cognition and debug/trace contamination negatives plus lawful positive disclosure controls.

Sanitization may run only as defense in depth after structural eligibility/role/output fencing; it cannot repair an invalid authority path.

## Task 6 — non-authoritative auxiliary work and late steering

Realize invisible auxiliary/internal logical work only through registered envelope phases/results. No mandatory subagent/background-worker topology is introduced.

Phase-local steering may adjust task/presentation emphasis but cannot alter source eligibility, role, authority, requiredness, accepted deterministic frontier or disclosure. Prompt position grants no authority.

This closes direct `R118,R133,R137` in the R2.4 role/emission owner rather than RD-05 execution.

## Task 7 — finite `UNSATISFIABLE` handling

When RD-11 reports `UNSATISFIABLE`, RD-10 chooses exactly one registered finite alternate path (deterministic path, narrower registered need/profile, genuinely blocking clarification, legal degradation/omission, typed BLOCKED/UNSUPPORTED) and terminates the failed attempt.

No blind reassembly loop, ad-hoc profile invention, silent guessing, mechanics replay or required-evidence drop.

## Task 8 — verification / Version Impact

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd10_role_emission -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Version Impact Gate classifies CORE instruction-contract and ephemeral machine-schema changes. No durable campaign migration is created by TurnEnvelope/phase-result contracts.

Negative stale proof: one primary containment wording owner (`AI_REASONING.md`), no competing CORE eligibility law, no raw handoff/result bus, no physical-presence eligibility, no Story same-envelope feedback, no late-steering authority, no visible internal surfaces and no sanitizer-only boundary.

## Currentness fence

Before execution, fresh-read R2.4, WP-08, Step-4 amendment, Step-5.12 and exact CORE/TOOLS/schema consumers. Mechanical path drift may be adapted and recorded; semantic owner/decomposition drift stops execution.

RD-10 completion records only its seven direct leaves. Downstream joins such as `R124` remain incomplete until RD-11 and RD-12 requirements are satisfied.