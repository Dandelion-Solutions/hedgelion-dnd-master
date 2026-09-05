# HDM Development Execution Process

Status: **AGREED — CANONICAL IMPLEMENTATION EXECUTION PROCESS**

## 1. Purpose and scope

This document governs implementation work after the relevant architecture or bounded design has been approved.

It complements:

- `AGENTS.md` — repository-wide development instructions;
- `DEV/DESIGN_PROCESS.md` — generic design/deep-work and decision-rights process;
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md` — HDM-specific architecture process and review gates.

It does not replace those owners. Architecture is decided before implementation. This process exists to make implementation highly autonomous while still stopping before an implementation mistake silently becomes new system architecture.

For substantial plan-based implementation, the intended human/Senior interaction is normally:

```text
approved architecture/spec
-> implementation plan
-> Senior plan review / GO
-> autonomous implementation
-> Senior final integration audit
-> accepted implementation
```

Intermediate Senior intervention is exceptional and event-driven. Ordinary RED tests, bugs, local refactors and mechanically resolvable plan details do not create a Senior review stop.

Small genuinely bounded changes may use the proportionate bounded workflow from `DEV/DESIGN_PROCESS.md` rather than creating a large formal plan. The moment implementation exposes cross-module or architectural impact, the task must ratchet upward and follow the escalation rules below.

---

## 2. Superpowers execution model

Implementation agents must use the applicable current Superpowers skills.

For substantial implementation with an approved spec:

1. use `superpowers:writing-plans` to produce the implementation plan before production-code changes;
2. use `superpowers:test-driven-development` for feature, bug-fix, refactor and behavior-change implementation;
3. when the execution environment supports subagents and plan tasks are suitable, prefer `superpowers:subagent-driven-development`;
4. otherwise use `superpowers:executing-plans` or another applicable current Superpowers execution skill;
5. use `superpowers:systematic-debugging` for unexpected failures before proposing fixes;
6. use the applicable code-review skill(s) during execution and before completion;
7. use `superpowers:verification-before-completion` before any completion/correctness/PASS claim.

The repository process remains authoritative when a generic skill conflicts with an explicit HDM owner, repository-transport rule, or human instruction.

Do not turn Superpowers narration into human ping-pong. An approved execution assignment is authorization to continue through mechanically implied tasks without asking "should I continue?" after each task or commit.

---

## 3. Implementation-plan gate

A substantial implementation plan is an executable argument from an approved spec to a sequence of independently testable changes.

The plan must satisfy the current `superpowers:writing-plans` requirements and additionally contain an **Implementation Impact Envelope**.

### 3.1 Implementation Impact Envelope

Record at least:

```text
SPEC / APPROVED DESIGN:
BASELINE REF OR SHA:

EXPECTED OWNERS TO CHANGE:
EXPECTED CONSUMERS TO CHANGE:
ALLOWED INTERFACES / CONTRACTS TO CHANGE:

PROTECTED ARCHITECTURE INVARIANTS:
ARCHITECTURE-SENSITIVE SURFACES:
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION:

KNOWN OUT-OF-SCOPE OWNERS / SURFACES:
```

The envelope is not a prediction that every changed filename is known in advance. It establishes the expected semantic blast radius so later execution can distinguish normal implementation discovery from architecture drift.

The plan must also identify coherent task/checkpoint boundaries. Each task should produce an independently testable result and should be small enough that a reviewer can meaningfully approve or reject it without reconstructing the whole implementation.

### 3.2 Senior plan review

For substantial/cross-module implementation, the complete implementation plan is a routine Senior review gate before production implementation begins.

The Senior review checks primarily:

- conformance to the approved spec/design;
- task decomposition and dependency order;
- Impact Envelope completeness;
- protected owner/authority boundaries;
- test and integration-verification mapping;
- whether any task silently introduces a new architectural decision.

After Senior GO, the worker proceeds autonomously until completion unless an escalation trigger occurs.

Do not repeatedly seek approval for individual plan tasks whose behavior is already settled by the approved spec and plan.

---

## 4. Autonomous task execution loop

For each implementation-plan task, use the applicable TDD/review workflow. The normal sequence is:

```text
read current published HEAD and plan/task state
-> RED: write the smallest test for the intended behavior
-> verify RED fails for the expected reason
-> GREEN: implement the minimum correct behavior
-> verify focused tests GREEN
-> refactor without changing accepted semantics
-> re-run focused verification
-> run task-local integration/contract checks required by the plan
-> compare actual impact with the Impact Envelope
-> run the mandatory Version Impact Gate and synchronize required bumps/projections
-> code/spec review for the task
-> resolve local findings
-> coherent checkpoint commit
-> publish
-> remote read-back
-> update durable execution state when required
-> next task
```

A worker does not stop merely because:

- a new test is RED as expected;
- an implementation attempt fails;
- an existing test reveals a normal local bug;
- a refactor needs another iteration;
- the plan contains a mechanically incorrect local detail but the approved spec unambiguously determines the correct result;
- a reviewer finds a local code-quality/spec-compliance defect that can be repaired without changing architecture.

Those are normal implementation events. Resolve them through TDD, systematic debugging, review and the governing spec.

### 4.1 Mandatory Version Impact Gate

The repository-wide Version Impact Gate in `AGENTS.md` applies to **every implementation task and coherent checkpoint**, including tasks whose final result is `VERSION_IMPACT: NONE`.

Use `DEV/RELEASE/VERSIONING.md` and its referenced detailed canonical owner to classify the actual changed owner/consumer set.

For each task/checkpoint:

1. identify affected HDM-owned version/revision/schema/generation namespaces and their owners/projections;
2. classify each relevant edit against the namespace-specific bump rule;
3. apply every required bump exactly once for the logical change;
4. synchronize every required projection/consumer in the same coherent checkpoint;
5. when no bump is required, verify that the edit is non-material under the owning rule rather than inferring this from filename, file type, diff size or passing CI;
6. record `VERSION_IMPACT: NONE` or the affected namespace old -> new transitions in task review/completion evidence.

A task is not checkpoint-ready while required version metadata or a required projection is stale. Machine checks are supporting evidence, not a substitute for the semantic classification.

If determining the correct bump would require changing an architectural compatibility/migration rule not already settled by the approved design and versioning owners, that is a System-Impact Gate event. Ordinary mechanically implied bumps and projection synchronization are not Senior escalation events.

---

## 5. Coherent checkpoint and recovery discipline

The repository-wide checkpoint rules in `AGENTS.md` apply throughout implementation.

Do not wait for the whole large assignment before publishing completed coherent work. Equally, do not publish arbitrary micro-commits that leave a half-migrated contract.

A task or slice is checkpoint-ready when another qualified worker could continue from the published HEAD without hidden chat-local state and without first completing an unpublished second half required to make the repository valid.

For long or interruption-prone implementation, maintain a durable execution cursor associated with the plan. Preferred path:

```text
DEV/docs/superpowers/plans/<plan-basename>-execution-status.md
```

The cursor is execution state, not architecture authority. Keep it compact.

Minimum useful form:

```text
PLAN:
SPEC:
BASE_SHA:

STATUS: EXECUTING | SENIOR_REVIEW_REQUIRED | FINAL_REVIEW | COMPLETE
CURRENT_TASK:
LAST_COMPLETED_TASK:
LAST_SAFE_SHA:

COMPLETED_TASKS:
  Task N -> <sha>

CURRENT_VERIFICATION_STATE:
VERSION_IMPACT: NONE | concise affected namespaces / transitions
SYSTEM_IMPACT: NONE | SENIOR_REVIEW_REQUIRED
NEXT_EXACT_TASK:
KNOWN_BLOCKERS:
UNPUBLISHED_WORK: NONE | exact description
```

Update it at meaningful durable checkpoints, not after every individual test command.

---

## 6. System-Impact Gate

After each substantial task/coherent slice, compare the **actual semantic impact** with the approved Implementation Impact Envelope.

The controlling question is:

> Is this still implementation of the approved architecture, or has implementation discovered a requirement to change an architectural/system boundary?

If the answer remains within the approved envelope, continue automatically.

If a trigger below occurs, do not improvise the cross-boundary change merely to keep coding.

### 6.1 Mandatory system-impact escalation triggers

Escalate when implementation requires or appears to require one or more of the following beyond the approved plan/design:

- changing a public/internal interface or contract used by another owner/module when that change was not admitted by the Impact Envelope;
- introducing a new dependency direction between architectural owners/components;
- changing ownership or authority over canonical state;
- changing the deterministic-engine versus LLM/GM reasoning authority boundary;
- adding a new persistent field/record/state class whose lifecycle, durability or ownership is not already specified;
- adding or activating a new executable primitive, selector, catalog/protocol member, operation, enum value or reusable capability not already admitted by the approved architecture;
- creating a second execution, validation, RNG, mutation, policy, package-identity or persistence authority;
- changing transaction, atomicity, concurrency, retry, idempotency, replay, recovery or durability semantics beyond the approved contract;
- changing RNG ownership, draw/reuse identity or deterministic-replay behavior;
- changing authorization/security/trust boundaries;
- introducing a migration or compatibility policy with material consequences that the approved design did not settle;
- requiring a materially broader owner/consumer set than the Impact Envelope anticipated, such that the original decomposition is no longer trustworthy;
- weakening/removing an existing invariant test, conformance assertion or protected contract in order to make implementation pass when the approved design did not authorize that weakening;
- adding a new ordinary-path network call, LLM pass, repository round-trip, unbounded/broad scan or other material runtime-cost/availability dependency not admitted by the design;
- coupling previously independent owners through shared mutable authority or shared lifecycle;
- discovering that the approved architecture cannot be implemented without changing its semantics or a material quality-attribute trade-off.

This list is semantic, not filename-based. A small diff can trigger escalation; a large generated/mechanical diff may remain inside the envelope.

### 6.2 Events that are not system-impact escalations by themselves

Do not escalate merely for:

- expected TDD RED;
- ordinary unit/integration failures during development;
- local bugs;
- test-fixture drift mechanically caused by an approved contract change;
- local refactors preserving the approved interface/ownership/semantics;
- implementation details that the approved spec settles unambiguously;
- code-review findings repairable within the existing contract;
- mechanical schema/catalog/generated-artifact synchronization already required by the approved design;
- version/revision/schema/generation bumps and projection synchronization mechanically required by the current versioning owners.

Use systematic debugging and normal review for those cases.

---

## 7. Escalation protocol

When a system-impact trigger occurs:

1. stop before making the unapproved cross-boundary change;
2. finish and verify the nearest safe coherent slice if doing so does not itself cross the disputed boundary;
3. publish that safe checkpoint and obtain remote read-back;
4. update the plan execution-status file to `SYSTEM_IMPACT: SENIOR_REVIEW_REQUIRED`;
5. record a concise **Implementation Impact Brief**;
6. stop for Senior review.

The brief should contain evidence, not private reasoning narration:

```text
TRIGGER:
LAST_SAFE_SHA:
CURRENT_TASK:

APPROVED SPEC / PLAN EXPECTATION:
DISCOVERED IMPLEMENTATION PRESSURE:
AFFECTED OWNERS / CONSUMERS:
PROTECTED INVARIANTS AT RISK:

WHAT CAN PROCEED WITHOUT THE CHANGE:
SAFE OPTIONS:
RECOMMENDATION:
COST / RISK IF RECOMMENDATION IS WRONG:

UNPUBLISHED_WORK:
```

Do not ask the human/Senior to reconstruct the problem from chat history. The durable repository state and impact brief must be sufficient to inspect the event.

If the Senior determines that no architecture change is actually required, record the ruling in the execution state/plan context and resume.

If a real architecture change is required, return to the applicable design/architecture process before implementing it. Do not treat the impact brief itself as authorization to change canonical architecture.

---

## 8. Automated review layer

Human/Senior review is not the per-task code-review mechanism.

When subagents are available, prefer the Superpowers subagent-driven pattern:

```text
implementation Task N
-> fresh implementer context
-> tests / implementation / self-review
-> task reviewer
-> local fix / scoped re-review as needed
-> accepted coherent checkpoint
-> Task N+1
```

The task reviewer should check ordinary spec/code quality, **Impact Envelope drift**, and the task's **Version Impact Gate** result.

Reviewer findings that remain inside approved architecture are resolved autonomously. A reviewer finding becomes a Senior event only when it satisfies a system-impact trigger or another existing mandatory human/safety stop.

Where subagents are unavailable, use the strongest applicable self-review/code-review workflow available in the environment, plus executable tests/CI. Do not fabricate a claim that an independent reviewer ran when it did not.

---

## 9. Machine gates and CI

Prefer executable checks over repeated prose review when a system invariant can be checked deterministically.

During early implementation, semantic Impact Envelope review may identify recurring failure classes. When a check becomes stable, low-noise and mechanically expressible, promote it into the appropriate maintenance audit, validator, test or CI gate.

Examples may include:

- forbidden dependency directions;
- schema/catalog/currentness mismatch;
- generated artifact drift;
- duplicate identity projections;
- missing or inconsistent mechanically enforceable version/generation projections;
- forbidden `GAME -> DEV` runtime dependency;
- undeclared protocol/catalog expansion;
- package/currentness/provenance mismatch.

Do not pre-build a universal architecture-impact linter based only on hypothetical future risks. Promote checks from observed/reproducible invariants so CI signal remains useful.

---

## 10. Final implementation verification

Before reporting a substantial implementation complete, the worker must obtain fresh evidence required by the plan and current repository contracts. As applicable this includes:

- focused task/unit tests;
- cross-module/integration tests;
- relevant scenario/conformance tests;
- full DEV test suite;
- maintenance audit;
- build/package checks when in scope;
- final code review;
- completed Version Impact Gate with required bumps/projections synchronized;
- hosted CI when it is an acceptance surface;
- remote publication/read-back of the final ref.

The execution status then moves to `FINAL_REVIEW` and records at least:

```text
BASE_SHA:
FINAL_SHA:
COMPLETED_TASKS:
VERIFICATION EVIDENCE:
FINAL REVIEW EVIDENCE:
VERSION_IMPACT: NONE | affected namespaces / transitions
SYSTEM_IMPACT EVENTS / RULINGS:
KNOWN REMAINING DEBT / FORWARD WORK:
UNPUBLISHED_WORK: NONE
```

Do not mark `COMPLETE` merely because the worker reached the end of the plan. Completion is an evidence-backed state.

---

## 11. Senior final integration audit

For substantial/cross-module implementation, final worker verification is followed by a routine Senior integration audit.

The Senior's primary job is not to repeat line-by-line code review. Compare:

```text
approved architecture/spec
vs implementation plan + Impact Envelope
vs BASE_SHA..FINAL_SHA actual delta
vs actual changed owners/consumers/interfaces
vs protected architecture invariants
vs verification/review evidence
```

The audit asks especially:

- Did implementation conform to the accepted design?
- Did the actual blast radius remain within or receive explicit rulings against the Impact Envelope?
- Was version impact assessed against the actual changed owner/consumer set, and were every required bump/projection synchronized?
- Did any implementation convenience create hidden new architecture or duplicate authority?
- Were system-impact events surfaced before the disputed change rather than normalized after the fact?
- Are all required machine contracts, tests, catalogs/schemas and runtime consumers synchronized?
- Is remaining debt/forward work explicitly owned rather than hidden inside passing tests?

Outcomes:

```text
PASS
TARGETED_REPAIR_REQUIRED
ARCHITECTURE_REVIEW_REQUIRED
```

A targeted repair may return directly to implementation when architecture is unchanged. `ARCHITECTURE_REVIEW_REQUIRED` returns to the applicable design process before further cross-boundary implementation.

After Senior PASS, update durable execution state to `COMPLETE` and advance the owning implementation roadmap/status as applicable.

---

## 12. Human-interaction budget

The intended routine interaction for a substantial implementation is deliberately small:

```text
ROUTINE STOP 1:
  complete implementation plan + Impact Envelope
  -> Senior GO

AUTONOMOUS EXECUTION:
  TDD + debugging + task review + checkpoint commits + CI
  -> no per-task human approval

EXCEPTIONAL STOP:
  only when a System-Impact Gate or another existing mandatory human/safety gate fires

ROUTINE STOP 2:
  fully verified final implementation
  -> Senior integration audit
```

Do not turn recoverability checkpoints into approval checkpoints. A worker publishes coherent progress so another agent can continue safely; publication does not require the human to acknowledge every commit.

The goal is **high implementation autonomy with explicit system-risk interception**, not either continuous supervision or unsupervised architecture-by-implementation.