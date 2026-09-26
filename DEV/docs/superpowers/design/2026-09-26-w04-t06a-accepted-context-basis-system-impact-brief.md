# W04.T06A Accepted Context-Basis Implementation Impact Brief

Task: W04.T06A — phase rebind and accepted Context basis

LAST_SAFE_SHA: `3113b43c345b10efacebcacb003eba98aa025b05` (fresh fetch confirmed this as `origin/v1/engine-rearchitecture`)

## Trigger

The T06A acceptance rule requires that matching `bundle_id`, recipient strings,
or a caller-shaped Context bundle cannot widen role eligibility. The current
Context producer exposes no owner-issued acceptance provenance that the
in-scope TurnRuntime can validate. Satisfying the rule by accepting fields or
shape would weaken the R2.3/R2.4 role-eligibility trust boundary; introducing
producer-issued proof would change an out-of-envelope owner/interface.

This triggers the System-Impact Gate for (1) changing a trust/authorization
boundary, (2) changing an interface between owners not admitted by this task's
Impact Envelope, and (3) requiring a broader owner/consumer set than the
approved decomposition.

## Approved expectation

T06A owns TurnRuntime phase-rebinding and accepted Context-basis controls only.
Its protected rules are that TurnEnvelope remains transient control,
caller-shaped data cannot authenticate eligibility, Actor remains
subject/purpose-local, Narrator gets a fresh bind after Chronicler, and only
minimum accepted typed results cross phases. `context_runtime.py` and
`runtime_host.py` are explicitly out of scope.

## Evidence

- R2.3 LAW 12 (`DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`)
  requires role/subject/player/purpose eligibility before semantic material
  enters the receiving role's logical evidence allocation; physical co-presence
  does not establish eligibility.
- R2.4 LAWs 14–17
  (`DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md`)
  require rebinding before each phase, a fresh Narrator rebind after Chronicler,
  no physical-presence eligibility, and no raw private handoff.
- WP-08-2/3/4
  (`DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-08-llm-role-context-instruction-realization-canonical-spec.md`)
  makes role/context controls ephemeral, requires the full rebind tuple, and
  permits only accepted typed handoffs. Step-4's single-context containment
  amendment is `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md`.
- `GAME/TOOLS/runtime_host.py::ContextService.assemble` returns the direct
  result of `_assemble_bound_context` without wrapping it in an owner-issued
  evidence type.
- `GAME/TOOLS/context_runtime.py::_assemble_bound_context` returns ordinary
  dictionaries shaped as `{"outcome": ..., "bundle": ..., "trace": ...}`;
  the assembled bundle is also a dictionary. No exact-instance acceptance
  evidence accompanies it.
- The local T06A test
  `test_matching_bundle_id_does_not_accept_a_shaped_context_basis` supplies a
  forged basis-shaped mapping with matching IDs. Focused RD10 execution reports
  that test failed because `bind_phase` did not raise, while the other 24 tests
  passed.

## Discovered implementation pressure

TurnRuntime can compare the role, profile, purpose, subject, recipient, bundle
and frontier fields, but those fields are reproducible by a caller. It cannot
prove that the bundle came from the accepted current Context assembly without
an authenticated producer artifact. A TurnRuntime-local seal would prove only
that TurnRuntime sealed a caller-supplied mapping; it would not prove accepted
Context eligibility and therefore would recreate the same trust defect.

## Affected owners and protected invariants

Affected owners if resolved through producer-issued evidence: Context Runtime
(`context_runtime.py`) and its RuntimeHost composition adapter (`runtime_host.py`),
plus TurnRuntime and the accepted Context result/basis contract. These producer
owners are outside T06A's direct write scope. No such change has been made.

At risk if implementation proceeds using shape/field equality: R2.3 role
eligibility, R2.4 phase rebinding/physical-presence separation, Step-4 logical
role containment, and T06A's prohibition on caller-shaped basis promotion.

## What can proceed without the disputed change

The existing local Actor-subject guard and its negative test are within the
T06A envelope and remain available for controller review. They do not satisfy
T06A's accepted-basis requirement and are not a complete or independently
accepted T06A checkpoint. T06B must not begin.

## Safe options and recommendation

1. The Senior/controller may authorize a bounded Context producer proof
   contract—such as exact-instance owner-issued evidence—and explicitly assign
   its producer/adapter changes and tests, with updated owner scope and review.
2. Alternatively, the Senior/controller may identify an already accepted
   producer-authenticity mechanism and document how TurnRuntime can validate it
   without changing Context/RuntimeHost ownership.

Recommendation: keep T06A stopped until one option is accepted. Do not use
caller shape, matching identifiers, or a TurnRuntime-only seal as proof of
Context assembly.

## Controller ruling

RULING: Continue within the approved T06A envelope by minting `AcceptedContextBasis` only inside a TurnRuntime operation that invokes the existing injected RuntimeHost `ContextService.assemble(request, candidates)` capability exactly once for that phase. Bind the resulting token to the current turn, role, purpose, profile, subject/recipient, accepted frontier and generated bundle identity. `bind_phase` and result acceptance require that token; a raw mapping, caller-shaped bundle, matching ID or recipient string is never accepted as provenance. The `ContextService` method and `_assemble_bound_context` owner contract remain unchanged, and their returned trace remains diagnostic-only.

WHY THIS IS IN SCOPE: T06A expressly owns phase rebinding and accepted Context-basis controls after T05C; the current ContextService capability is the existing owner-routed Context consumer interface. Invoking that existing capability is the planned Context-to-TurnRuntime data flow, not a new producer owner or a field-equality substitute. One bounded service call replaces the already-required assembly call; no extra repository round-trip is introduced.

COST IF WRONG: if the actual role executor cannot pass the existing RuntimeHost-owned ContextService capability into the T06A TurnRuntime operation, or if the T06A reviewer establishes that this capability call is not an accepted Context source, stop before publication and reopen the System-Impact Gate. No Context Runtime, RuntimeHost or producer interface changes are authorized by this ruling.

DISPOSITION: The documented pressure to create a new Context/RuntimeHost producer artifact is resolved by the existing capability call path; T06A resumes inside its recorded write envelope. The earlier recommendation to stop is superseded by this ruling.

## Verification and version impact

Command: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS/test_rd10_role_emission.py -q`

Result: 1 failed (the expected forged-basis RED), 24 passed. The failure shows
`bind_phase` succeeds without requiring or validating accepted Context
provenance while the envelope contains a caller-populated basis-shaped mapping
with matching identifiers. This is not T06A GREEN evidence.

VERSION_IMPACT: NONE for the current partial code/test delta. `turn_runtime.py`
is unversioned implementation support; no version-bearing or persistent schema
was changed. Reassess if a ruling authorizes a producer/interface change.

UNPUBLISHED_WORK: local T06A partial Actor-subject guard/test and the accepted
Context-basis RED remain uncommitted for controller review. No excluded owner
was changed. Do not commit or publish before the requested review.

## T06A implementation state after controller adjudication

The initial stop recommendation above is superseded by the controller ruling in
this brief and the synchronized Wave-04 execution cursor. The ruling has been
implemented within T06A's direct owner scope:

- `bind_phase_from_context` invokes the injected existing
  `RuntimeHost.context.assemble(request, candidates)` capability exactly once
  per successful phase assembly. The RD10 capability test uses a real composed
  RuntimeHost ContextService and observes one `assemble`, one campaign pin and
  one selected-LIVE read.
- Only the exact ContextService assembly result can produce the sealed,
  non-serializable `AcceptedContextBasis`. It binds turn identity, role,
  purpose, profile, subject, recipient, accepted frontier and a TurnRuntime-
  generated bundle ID. `bind_phase` and result acceptance reject raw IDs,
  mappings and caller-shaped bases.
- Context trace is not included in the basis; raw bundle/trace/private
  diagnostics fail closed. Accepted prior results are sealed to their source
  phase and exact minimum registered result shape; only explicitly admitted
  typed kinds cross, and Chronicler Story output is never a same-turn prior.
- Narrator acceptance requires a new Context assembly after Chronicler. A
  previous Narrator's phase-local execution handoff is discarded on the fresh
  bind and can be projected again from the same already-accepted W02 result;
  mechanics are not rerun. The existing `emission.py` consumer contract and
  Narrator-facing bundle/recipient/result keys remain compatible.
- The Actor-subject requirement remains in place; registered Context profile
  admission fixes Actor purpose, and Actor results/prior-result transfer remain
  subject-local.

## Pre-fixture verification snapshot (superseded below)

TDD RED evidence observed during this continuation:

- `bind_phase_from_context` was initially missing;
- forged Actor prior-result transfer across subjects, unselected typed prior
  results, stale Narrator Context after Chronicler, same-envelope Story-result
  transfer, trace/private diagnostic transport, serialization of sealed
  transient controls, and reusing a prior Narrator execution handoff after a
  fresh Context rebind each failed their new focused witness before repair.
- The earlier matching-bundle-id RED remained the supplied baseline witness.
- A final RED also showed that a consumed basis could be reused after its
  phase binding was replaced; a turn-local generated-bundle-ID consumption
  guard now rejects that replay.

Current verification:

- `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS/test_rd10_role_emission.py -q` — 38 passed.
- `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS/test_rd11_context_runtime.py -q` — 42 passed.
- RD05 `DeterministicExecutionTests.test_committed_execution_crosses_only_a_registered_narrator_handoff` remains an out-of-scope legacy caller: it calls `bind_phase` with raw `bundle_id` and fails because accepted Context basis is now mandatory. The RD10 integrated handoff/emission and fresh-rebind cases pass using the existing injected ContextService and the same accepted execution value. Do not weaken the new basis contract; controller review should decide any separately authorized RD05 fixture migration.
- Scoped Ruff check passed for `turn_runtime.py` and `test_rd10_role_emission.py`. Whole-file format check remains non-clean because of existing formatting in those files; broad formatting was not applied.
- Full DEV, maintenance audit and hosted CI were not run. Hosted CI is unavailable in this runtime.

VERSION_IMPACT: NONE — `turn_runtime.py` is unversioned support; the edited
TurnEnvelope and NarrationResult JSON schemas are transient, carry no HDM
`schema_version`, and are not persistent record families. Campaign/storage/catalog/
engine generations, migration and dual-read remain unchanged.

SYSTEM_IMPACT: REOPENED AFTER INDEPENDENT REVIEW. The current candidate passes
an arbitrary duck-typed `assemble` object through TurnRuntime; it does not prove
that the object is the existing RuntimeHost-owned ContextService capability.
No ContextService/RuntimeHost owner was changed to close this gap.

INDEPENDENT_REVIEW: **NOT PASS / HIGH FINDING** — TurnRuntime accepts any
caller-supplied object with a callable `assemble` attribute, so a lookalike
service can return a matching shaped mapping and obtain `AcceptedContextBasis`.
T06A changes remain uncommitted/unpublished; T06B remains blocked.

T06A_LATEST_VERIFICATION: RD10 39 passed; RD11 42 passed; RD05 40 passed after
the one-file fixture synchronization. Full DEV, maintenance audit, and hosted
CI were not run.

## RD05 mechanical fixture synchronization

The original RD05 failure was a stale test call site, not a missing Context
capability: the fixture called `bind_phase` with only `"bundle-1"`. As explicitly
authorized in the current W04.T06A task, only that test fixture was changed to
call `bind_phase_from_context` with a test ContextService capability that
returns one assembled, matching Narrator bundle. The fixture asserts exactly
one `assemble` call and retains its original W02 accepted-execution and
idempotent-handoff assertions. No production file outside TurnRuntime and no
W02 producer behavior changed.

TDD evidence: the exact node was first reproduced RED at the accepted-basis
guard; it is now GREEN. Final commands/results:

- `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS/test_rd05_runtime_execution.py -q` — 40 passed.
- `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS/test_rd10_role_emission.py -q` — 39 passed.
- `.hdm-devtools/venv/bin/ruff check GAME/TOOLS/turn_runtime.py DEV/TESTS/test_rd10_role_emission.py` — PASS. Whole-file RD05 Ruff reports eight pre-existing I001/F841/SIM117 findings outside the fixture hunk; `ruff check --ignore I001,F841,SIM117` across the three changed Python files — PASS. `git diff --check` — PASS.

The mechanical test-only synchronization is a bounded Impact Envelope
correction: no new product owner, interface, runtime producer, persistence, or
SYSTEM_IMPACT. VERSION_IMPACT remains NONE. The candidate remains uncommitted
and unpublished for controller review.

## Independent review finding — capability authenticity

REVIEW_BASE: `e428084382a84ce87ef1e8123a1c9b2d97e7cb2d`.
REVIEW_RESULT: **SPEC-COMPLIANCE NOT PASS / HIGH**.

Finding at `GAME/TOOLS/turn_runtime.py:111-119, 427-490`: `ContextAssembler` is
only a structural Protocol, and `bind_phase_from_context` accepts any caller
object whose `assemble` attribute is callable. It then mints the sealed
`AcceptedContextBasis` from the returned mapping after matching its fields. A
lookalike assembler can return caller-chosen `ASSEMBLED` data with matching
scope, so the seal proves TurnRuntime wrapped a result, not that the result came
from the existing RuntimeHost-owned ContextService capability. The RD05 test
fixture demonstrates that this structural injection path accepts a test-defined
assembler as well.

This does not satisfy the earlier controller ruling's requirement to mint a
basis only through the genuine injected RuntimeHost ContextService capability.
The TurnRuntime-only call path has not authenticated that capability. The
earlier disposition that T06A was inside its envelope is suspended for this
authenticity issue; the rest of the implementation has no PASS until it is
resolved.

SYSTEM_IMPACT: SENIOR_REVIEW_REQUIRED. Resolve one of these before continuing:

1. Authorize a bounded owner-issued proof/capability contract from the existing
   ContextService/RuntimeHost producer and assign its producer/consumer tests;
   update the T06A owner envelope and Version Impact assessment accordingly.
2. Identify an already accepted mechanism that authenticates the exact
   RuntimeHost ContextService call without changing Context/RuntimeHost owner
   contracts, and document that source/consumer path.

Do not accept caller shape, matching fields/IDs, Protocol conformance or a
TurnRuntime-local seal over a caller-provided assembler result as producer
provenance. T06B remains blocked; PO-011 separately must be consumed before its
RED.

UNPUBLISHED_WORK: T06A code/schema/test candidate and this gate record are
local/uncommitted for Senior/controller ruling. The code/test candidate has
not been published or accepted.
