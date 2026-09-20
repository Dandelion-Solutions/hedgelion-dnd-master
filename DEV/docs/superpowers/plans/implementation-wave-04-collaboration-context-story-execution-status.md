# Wave 04 Execution Status

PLAN: DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md
SPEC: DEV/docs/superpowers/specs/2026-09-11-r2-7-WP-27-final-implementation-planning-readiness-canonical-spec.md
BASE_SHA: b751436e81fc817dfdcc694584fb84c734ec204c

STATUS: EXECUTION_AUTHORIZED
CURRENT_TASK: Wave-04 decomposed orchestration bootstrap; initial independent lanes are T01A and T05A, with T07A gated by mandatory fresh CLS-HDM preflight
LAST_COMPLETED_TASK: Wave-04 stable-plan decomposition and Wave-03 closed-cursor reconciliation
LAST_SAFE_SHA: b751436e81fc817dfdcc694584fb84c734ec204c

## Execution policy

MAX_CONFIGURED_HDM_WORKERS: 5
MAX_SAFE_WAVE04_PRODUCTION_WORKERS: 4
REVIEWER_LIMIT: NONE
SAME_PRODUCTION_OR_PRIMARY_TEST_FILE_WRITERS: SERIALIZED
DEPENDENT_TASK_START: only after producer independent reviewer PASS is published/read back
SYSTEM_IMPACT: stops only affected lane; independent lanes continue
VERSION_SYNC: shared/global version owners are reserved and serialized before publication

The detailed execution decomposition, write sets, mandatory REDs and protected boundaries are owned by the stable Wave-04 plan. This cursor records scheduling/currentness only and does not override it.

## Lane graph

COLLABORATION:
T01A -> T01B -> T01C
T01C -> T02A -> T02B -> T02C -> T04A -> T04B
T01C -> T03A in parallel with T02A-T02C

CONTEXT / EMISSION:
T05A -> T05B
T05B + T04B -> T05C -> T06A -> T06B

STORY / COMMENTATOR:
T07-PREFLIGHT -> T07A -> T07B -> T07C -> T07D -> T07E -> T07-INTEGRATION
No T07A RED before the mandatory fresh cross-project preflight is recorded.

FINAL CONSUMERS:
T04B + T02C + T07-INTEGRATION -> T08A
T06B -> T08B
T08A + T08B + T03A -> T08C
T08C + all lane checkpoints -> FINAL_REVIEW

## Initial scheduler

READY_NOW:
- W04.T01A — collaboration coordination-family admission and exact participant authority
- W04.T05A — Context routed currentness and eligibility admission

COORDINATOR_GATE_READY_NOW:
- W04.T07-PREFLIGHT — perform only immediately before first T07A RED; on PASS, T07A becomes READY

NOT_READY:
- T01B waits T01A reviewer PASS
- T05B waits T05A reviewer PASS
- T07A waits mandatory preflight disposition
- T03A/T02A wait T01C reviewer PASS
- T04A waits complete T02C
- T05C waits T05B + T04B
- T06A waits T05C
- T08A/T08B/T08C wait their named joins

Recommended initial production occupancy is two workers, increasing to three immediately if T07 preflight passes. After T01C, T03A may occupy a fourth independent slot while the collaboration lane continues. Do not manufacture work merely to fill slot five.

## Write-set reservations

COLLABORATION LANE:
- GAME/TOOLS/collaboration.py
- DEV/TESTS/test_rd12_collaboration.py
- collaboration obligation/closed-basis/handoff/frontier/catch-up schemas
- DEV/SCHEMAS/intent-clause.schema.json where owned by the subtask
Only one collaboration-lane worker at a time.

PLAYER DELTA:
- DEV/TESTS/test_rd16_world_family_machine_integration.py
- bounded Wave-05 player delta evidence only
No physical shared PLAYER schema write.

CONTEXT LANE:
- GAME/TOOLS/context_runtime.py
- GAME/TOOLS/context_budget.py when required
- DEV/TESTS/test_rd11_context_runtime.py
- Context owner-local schemas
Only one Context-lane worker at a time.

EMISSION LANE:
- GAME/TOOLS/turn_runtime.py
- GAME/TOOLS/emission.py
- DEV/TESTS/test_rd10_role_emission.py
- owner-local turn/handoff/narration schemas
Starts only after Context integration.

STORY LANE:
- GAME/TOOLS/history.py
- GAME/TOOLS/story.py
- GAME/TOOLS/commentator.py
- GAME/TOOLS/dramaturg.py
- DEV/TESTS/test_rd13_story_t0_commentator.py
- owner-local Story/T0/Commentator/Dramaturg schemas
Only one Story-lane implementation worker at a time because the primary test file is shared.

FINAL CONSUMERS:
T08A and T08B use disjoint focused test/delta surfaces and may execute in parallel after their inputs are GREEN. T08C is the convergence checkpoint.

## Pre-implementation risk controls learned from Wave 03

1. TYPED_OBJECT_IS_NOT_AUTHORITY
   - Every new collaboration/history/context/control carrier must prove its producer/currentness boundary.
   - Public constructor, Protocol, subclass, structural shape, token/registry or caller-provided validator cannot substitute for native owner admission.

2. CURRENTNESS_IS_FULL_BASIS
   - Same revision with changed relevant body/basis must fail closed.
   - Projection/current flags cannot substitute for exact source/owner currentness.

3. NO_REVERSE_AUTHORITY
   - Collaboration cannot authorize PLAYER/access.
   - Context cannot establish truth/knowledge/access.
   - Story/Commentator cannot establish native history/access.
   - Dramaturg cannot establish canon.
   - Session cannot establish campaign/LIVE/PLAYER authority.

4. NO_SHARED_FINAL_WRITER_THEFT
   - W04 emits deltas only for Wave-05-owned shipped CORE/shared schemas/catalogs.

5. NO_LATE_VERSION_SURPRISE
   - Persistent collaboration and Story/PO-009 schema impacts are evaluated at the first material row, not at wave end.
   - Durable Context/Turn control introduced for convenience is a System-Impact event.

## Story completeness gate

T07B is not allowed to close with an EVENTS-only implementation.

Required baseline registrations:
- T-MSG and T-ARCH -> TRANSCRIPT
- E-EVT and E-REL -> EVENTS
- M-SEG and M-OUT -> MECHANICS
- N-EVT and N-REL -> NARRATIVE

The current owner-local schema set lacks a Story TRANSCRIPT unit schema; T07B owns the missing owner-local machine contract and the complete eight-registration coverage tests. Coverage/currentness remains per source-domain/generation/cardinality, never one global Story frontier.

## CLS planning evidence — NOT THE MANDATORY T07 PREFLIGHT

Planning-only reads on 2026-09-20 observed:
- CLS audit branch audit/cls-project-audit-workspace at 6273260c55107bc769d355875da749c9ef3c9296: AUDIT CLOSED / PASS / ZERO OPEN CLASS-A FINDINGS
- CLS feature branch feature/commentator-language-stack at a064e6738945390fcc3766653c79ba2a6048b6e7: WP12-03 active, PUBLIC_HDM_WRITE_REQUIRED=NO, no current architecture/PO blocker
- private integration graph classifies the current public dependency as compatible and identifies W04.T07 as the later public producer boundary

These observations support scheduling only. Immediately before T07A RED, repeat the exact stable-plan preflight with then-current public/private refs and record one of PASS_TO_IMPLEMENT, PRIVATE_CLS_REPAIR_DEBT_ONLY, SYSTEM_IMPACT_GATE or PREFLIGHT_UNAVAILABLE.

## Verification / completion state

CURRENT_VERIFICATION_STATE:
- Wave 03 is globally CLOSED / Senior PASS; post-closure F63-F65 targeted repair is independently Senior PASS with hosted validation 992 passed / 6 skipped.
- Wave-04 stable plan decomposition is published.
- No Wave-04 production RED or implementation is claimed by this cursor.
- No Wave-05 final-writer surface has been authorized for W04.

VERSION_IMPACT: NONE — planning/cursor metadata only.
SYSTEM_IMPACT: NONE — this decomposition refines execution checkpoints and scheduling without changing accepted architecture.
NEXT_EXACT_TASK: start W04.T01A and W04.T05A in parallel. Immediately before starting W04.T07A, execute and record the mandatory fresh CLS-HDM preflight; if PASS, start the Story lane independently.
KNOWN_BLOCKERS: none for T01A/T05A. T07A is preflight-gated. All other rows are dependency-gated as listed above.
UNPUBLISHED_WORK: NONE after publication/read-back.
