# R2.7 WP-27 Steps 3–8 Audit Execution Plan

Status: **APPROVED EXECUTION DECOMPOSITION — NOT A STEP-3 START**

Date: 2026-09-11

## Goal

Complete the remaining WP-27 deep-design loop after the independently verified Step-2 evidence closure while preserving reviewer independence, traceability and the mandatory final Senior gate.

This plan does **not** authorize implementation planning, implementation, release execution, migration execution or gameplay bootstrap. It decomposes the already-authorized WP-27 Steps 3–8 into three execution runs so that synthesis, adversarial review and repair/canonicalization do not collapse into one self-confirming context.

## Current verified predecessor state

The execution plan starts from the current authoritative state in which:

```text
WP27_STEP2: COMPLETE
WP27_STEP3: NOT_STARTED
SOURCE_ITEMS: 224
READINESS_RECORDS: 145
EXPLICIT_NO_WORK_TERMINALS: 79
ROUND2_DIAMOND_STRONG: 82 / 82
PO001_010: 10 / 10
MACHINE_RESPONSIBILITIES: 59 / 59
MACHINE_EXCEPTION_MEMBERS: 31 / 31
HIGH_RISK_PROBES: 8 / 8 PASS
ARCHITECTURE_BLOCKER_CANDIDATES: []
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
VERSION_IMPACT: NONE
```

Primary predecessor evidence:

- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-evidence-ledger.md`;
- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-execution-amendment.md`;
- `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-2-independent-audit.md`;
- current `DEV/CURRENT_PROGRESS.md` and task-local audit cursor.

## Why the remaining work is split into three runs

Step 2 carried the expensive evidence extraction and reconciliation burden. Steps 3–5 are now primarily synthesis and formalization over that admitted evidence, so they benefit from continuity in one context.

Step 6 is different: the HDM process requires a whole-project adversarial critic and prefers a fresh reviewer context. Running it in the same context that authored the Decision Brief and candidate specification would weaken the independence of the critic and make self-confirmation more likely.

Steps 7–8 then need continuity again: findings must be dispositioned item-by-item, repairs propagated, any materially changed area re-criticized when necessary, and the final result canonicalized and verified before the mandatory Senior stop.

Therefore the approved execution decomposition is:

```text
RUN A — Steps 3–5
  Step 3 Decision Brief
    -> Step 4 collaborative-review disposition
    -> Step 5 candidate specification
    -> durable candidate checkpoint
    -> STOP

RUN B — Step 6 only, fresh context
  independent whole-project adversarial review
    -> durable findings checkpoint
    -> STOP

RUN C — Steps 7–8
  Step 7 finding resolution / propagation
    -> targeted 5->6->7 re-critic loop only where repairs create material new risk
    -> Step 8 canonicalization / verification / publication
    -> STOP at mandatory Senior review
```

## Global rules for all three runs

1. Fresh-bootstrap from the authoritative remote branch before substantive work. Do not trust remembered SHA, path, cursor or prior-chat summaries.
2. Use GitHub Connector / the applicable runtime overlay as the authoritative repository transport.
3. Do not create branches. Work only on the authorized current branch unless the Product Owner explicitly changes branch policy.
4. Treat the Step-2 evidence ledger as admitted predecessor evidence, not as a summary to be reconstructed from scratch.
5. Do not perform corpus-wide blind scans. Follow owner/dependency routes and expand only for a concrete unresolved dependency, contradiction, supersession question or critic requirement.
6. Preserve item-level semantics and lossless traceability from the 224 source items, 145 readiness records, 79 no-work terminals, 82 Round-2 DIAMOND/STRONG records, PO-001..010 and the machine reverse-conformance records.
7. Aggregation in later synthesis is allowed only when reverse mapping remains inspectable. A workstream summary must never make a source/readiness obligation disappear.
8. `ALREADY_REALIZED`, implementation obligation, verification obligation, empirical obligation, release-time obligation, dormant/deferred trigger and rejected/out-of-scope remain distinct classes.
9. Current green CI does not satisfy future scenario, Protocol-4, empirical or release-time proof obligations.
10. Do not reopen accepted architecture merely because Step-2 evidence overlaps it. Reopen only if later synthesis/criticism proves a concrete accepted owner insufficient or contradictory under the WP-27 blocker test.
11. If a genuine human-owned decision appears — product semantics, material architectural trade-off, authority change, compatibility policy, explicit risk acceptance, hard-to-reverse scope or equivalent — stop with a decision-ready artifact. Do not manufacture approval pauses when evidence already settles the matter.
12. Implementation planning remains unauthorized throughout WP-27. The Step-5 candidate is an architecture/readiness candidate, not an implementation plan.
13. Step 8 must stop for the mandatory Senior review. R2.7 final reconciliation begins only after WP-27 final Senior GO.

## Run A — Steps 3–5

Controlling task file:

`DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-steps-3-5-task.md`

### Step 3 — Decision Brief

Use the closed Step-2 ledger to answer whether any material architecture/product decision remains before a candidate implementation-planning-readiness specification can be formed.

Required result:

- concise decision-ready synthesis;
- explicit recommendation;
- real alternatives only where evidence supports materially different choices;
- strongest weakness/countercase;
- uncertainty and evidence that would change the recommendation;
- explicit `Human decision required: YES | NO`;
- explicit statement on whether any bounded architecture reopen is required.

Expected artifact:

`DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-3-decision-brief.md`

### Step 4 — Collaborative-review disposition

If Step 3 exposes a genuine human-owned decision, stop and return it to the Product Owner before Step 5.

If Step 3 concludes `Human decision required: NO`, do not manufacture an approval stop. Record that the current evidence/accepted owners settle the relevant choices and proceed mechanically to Step 5 under the existing WP-27 authorization.

Expected artifact:

`DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-4-review-disposition.md`

### Step 5 — Candidate specification

Produce one concrete candidate architecture for implementation-planning readiness. It must synthesize rather than duplicate the entire mega-ledger, while preserving lossless traceability back to Step-2 IDs.

At minimum the candidate must make inspectable:

- final readiness/workstream structure derived from the 145 readiness records;
- explicit terminal treatment of the 79 no-work records;
- prerequisite/dependency DAG without inventing one universal linear implementation sequence;
- owner and destination family for each material workstream;
- Version Impact / compatibility / migration routing;
- deterministic, scenario, empirical and release-time proof separation;
- dormant/revisit activation triggers;
- rejected/negative architecture that later planning must not revive;
- PO-001..010 consequences;
- 82-item Round-2 continuity and later deltas;
- current machine-realization/reverse-conformance consequences;
- the eight high-risk probe outcomes;
- implementation-detail choices that are intentionally left to later planning;
- any genuine architecture blockers, if newly discovered.

Expected artifact:

`DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-5-candidate-readiness-spec.md`

### Run-A checkpoint

Each Step 3, 4 and 5 artifact should be durably published as a coherent checkpoint so the later Step-6 critic can distinguish the candidate it is reviewing from subsequent repairs.

At the end of Run A:

```text
WP27_STEP3: COMPLETE
WP27_STEP4: COMPLETE
WP27_STEP5: COMPLETE
WP27_STEP6: NOT_STARTED
IMPLEMENTATION_PLANNING_STARTED: NO
```

Synchronize current/task-local recovery surfaces to point to Step 6 as the next eligible/authorized unit, but do not start Step 6 in Run A.

## Run B — Step 6 only, fresh context

Run B must start in a new context/session.

The Step-6 reviewer must independently reconstruct the relevant whole-project dependency subgraph through `DEV/PROJECT_MAP.md`, inspect the actual current owners/consumers that can constrain the candidate, and not simply trust the Run-A candidate's own Source Manifest or assertions.

The critic must specifically attack:

- dropped Step-2 qualifiers or source items;
- aggregation that breaks reverse traceability;
- duplicate/shifted semantic authority;
- closed repair resurrected as future work;
- rejected architecture revived for planning convenience;
- missing machine-to-owner consequences;
- PO route loss;
- DIAMOND/STRONG delta loss;
- Story/T0/control and zero-extra-serial constraints;
- WP-25 deferred-vs-rejected boundaries;
- partition/scale trigger activation mistakes;
- migration/version sequencing mistakes;
- proof-channel over-credit;
- release-time work pulled into planning;
- dormant empirical/host work activated prematurely;
- implementation detail accidentally promoted into architecture;
- architecture blocker hidden as delegated detail.

Expected artifact:

`DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-6-whole-project-adversarial-review.md`

Run B ends after publishing the critic findings. It does not repair the candidate and does not begin Step 7.

## Run C — Steps 7–8

### Step 7 — Resolution gate

Account for every Step-6 finding individually with severity, agreement/disagreement, rationale, exact repair/disposition, affected artifacts and whether a human decision is required.

Repair mechanically resolvable issues autonomously. Do not convert critic wording directly into architecture without reconciliation against accepted owners.

If a repair materially changes a candidate law or creates material new risk, run the smallest necessary targeted `candidate -> critic -> resolution` loop before declaring the finding closed.

All `BLOCKING` findings must be closed. All `SIGNIFICANT` findings must be resolved, explicitly accepted as risk/debt by the proper human authority, or safely deferred under an existing owner boundary.

The mandatory finding-propagation sweep must account for every affected current artifact and preserve historical rejected wording only when clearly marked as historical/non-current and routed to the final owner.

### Step 8 — Canonicalization

Only after Step 7 closes the critic findings:

- perform the final self-review;
- canonicalize the accepted WP-27 final architecture/machine-realization readiness result under `specs/`;
- synchronize current progress, task-local cursor, mini-report, routing/index/deferred/debt surfaces as actually affected;
- preserve final item-level traceability to Step 2;
- run required verification and Version Impact classification;
- publish a coherent checkpoint;
- obtain fresh remote read-back/currentness evidence;
- stop for mandatory final WP-27 Senior review.

At Run-C completion:

```text
WP27_STEP8: COMPLETE
WP27_FINAL_SENIOR_REVIEW: PENDING
R2_7_FINAL_RECONCILIATION: NOT_STARTED
IMPLEMENTATION_PLANNING_STARTED: NO
```

## Acceptance model

This decomposition is successful if it preserves both continuity and independence:

- Run A can hold the admitted Step-2 evidence and synthesis problem in one context;
- Run B critiques the Run-A candidate from a fresh context;
- Run C repairs and canonicalizes against a frozen critic record;
- a later Senior can independently inspect the original candidate, critic, resolutions and final canonical result without reconstructing hidden conversation state.
