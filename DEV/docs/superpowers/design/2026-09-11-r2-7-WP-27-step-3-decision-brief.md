# R2.7 WP-27 Step 3 — Decision Brief

Status: **COMPLETE — NO HUMAN DECISION REQUIRED / STEP 4 NOT STARTED**

Date: 2026-09-11

Controlling Run-A task:

- `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-steps-3-5-task.md`;
- `DEV/docs/superpowers/plans/2026-09-11-r2-7-WP-27-steps-3-8-audit-execution-plan.md`.

Admitted predecessor evidence:

- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-evidence-ledger.md`;
- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-execution-amendment.md`;
- `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-2-independent-audit.md`;
- current `DEV/CURRENT_PROGRESS.md` and task-local R2.7 cursor.

This Decision Brief consumes the independently closed Step-2 package as admitted predecessor evidence. It does not reconstruct Step 2, reopen accepted architecture, authorize implementation planning, or begin Step 6.

---

## 1. Decision question

Given the closed Step-2 readiness evidence, does any material architecture or Product Owner judgment remain that must be settled before one implementation-planning-readiness candidate can be specified?

**Answer: no.** The remaining work is composition and formalization of already accepted owner-local obligations, proof channels, activation triggers and negative laws. No surviving question crosses the WP-27 blocker threshold for semantic authority, persistent-interface policy, compatibility policy, hard-to-reverse product/risk trade-off, security/disclosure authority, release/publication authority, or another human-owned decision class.

---

## 2. Evidence basis and fixed classifications

The admitted Step-2 closure establishes the following lossless basis:

```text
SOURCE_ITEMS: 224 / 224
READINESS_RECORDS: 145 / 145
  exact set: R27-R001..R27-R003, R27-R005..R27-R146
EXPLICIT_NO_WORK_TERMINALS: 79 / 79
PO001_010: 10 / 10
ROUND2_DIAMOND_STRONG: 82 / 82
ROUND2_DELTAS: S14 / S53 / D15 reconciled
MACHINE_RESPONSIBILITIES: 59 / 59
MACHINE_EXCEPTION_MEMBERS: 31 / 31
HIGH_RISK_PROBES: 8 / 8 PASS
ARCHITECTURE_BLOCKER_CANDIDATES: []
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
```

The following classifications are fixed by current owners and are not open Step-3 choices:

1. Native semantic/runtime/persistence/release owners remain authoritative; WP-27 does not create a global readiness owner.
2. The 145 readiness records preserve owner, destination, dependency, activation, proof and future Version Impact/Migration gates. Their physical implementation detail is delegated only where the owner explicitly permits it.
3. The 79 no-work terminals remain `ALREADY_REALIZED`, deferred/dormant, release-forward-only, rejected/out-of-scope or otherwise explicit no-current-work routes. They are not latent implementation backlog.
4. Migration machinery remains released-v1.0+-conditional under WP-20; no current migration edge or global migration registry is selected.
5. Current source CI/audit, deterministic contract proof, scenario/adversarial acceptance, supported-target/Protocol-4 empirical evidence and release-time exact-asset/fresh-Project evidence are separate proof channels.
6. WP-23 release acceptance remains forward release work and is not discharged by current source CI or builder presence.
7. WP-24/PO-010 growth bands create writer-specific review/rollover triggers, not a universal partition project or preselected shard geometry.
8. WP-25/PO-008 permits focus-scoped owner-local failure realization and host-risk calibration while global failure/health/ACL/retry/replay/scheduler/queue authorities remain rejected.
9. PO-003/PO-009 requires Story-local recoverable qualifying T0/control for the baseline Commentator path, with native SemanticEvent/history, knowledge, disclosure and access remaining authoritative and with zero-extra-serial critical-path behavior preserved.
10. Machine presence is evidence of a bounded support/consumer role only. The `R27-M*`/`R27-X*` reverse-conformance ledger explicitly prevents stale or implementation-only surfaces from acquiring semantic authority.

---

## 3. Material quality axes for the candidate

The Step-5 candidate must preserve four axes simultaneously:

- **lossless traceability** — every readiness record remains reverse-mappable to its Step-2 source item and owner, and all 79 no-work terminals remain inspectable;
- **owner locality** — workstreams may aggregate planning concerns, but aggregation cannot merge semantic authority, invent a global sequence or create a cross-owner registry/service;
- **activation discipline** — active realization, realized support, deferred/dormant trigger, empirical obligation and release-time obligation remain distinct;
- **proof discipline** — deterministic, scenario, empirical/Protocol-4 and release-time evidence cannot substitute for one another.

The Step-2 owner-derived DAG already demonstrates that these axes are compatible. Therefore workstream grouping is a representation problem, not an unresolved architecture choice, provided the Step-5 mapping is exact and inspectable.

---

## 4. Implementation-selectable choices that are not blockers

The following remain intentionally selectable later and must not be escalated into new architecture decisions unless a concrete implementation choice violates an accepted owner boundary:

- local class/module/function decomposition and internal APIs;
- owner-local schema spelling and encodings where the accepted owner fixes semantics but delegates representation;
- HOT/SQLite table/index layout and rebuildable cache/index implementation;
- exact Story event/control-projection fields, storage layout, cache layout and shard geometry, subject to Story-local recoverability, source binding, filtering/currentness and PO-010 growth laws;
- writer-specific page/bucket/rollover geometry after the corresponding size/measurement trigger fires;
- WP-20 declaration/edge representation details when a qualifying released compatibility obligation actually exists;
- fixture organization, test harness mechanics and diagnostic formatting;
- bounded owner-local evaluator/adapter shapes for failure handling where WP-25 permits them.

These choices are reversible or owner-delegated implementation decisions. None currently changes semantic authority, compatibility policy, product semantics or the accepted persistent/interface law.

---

## 5. Eight high-risk probes — Step-3 challenge result

Step 3 explicitly challenged the recommendation against the eight admitted probes:

| Probe | Step-3 consequence |
|---|---|
| `R27-P01` Story-local T0/control | PASS preserved: delegated representation remains bounded by native-owner authority, local recoverability, filtering/currentness and zero-extra-serial law. |
| `R27-P02` WP-25 deferred vs rejected | PASS preserved: focus-scoped realization stays possible; rejected global abstractions remain rejected. |
| `R27-P03` writer-specific partition activation | PASS preserved: no universal partition workstream; geometry remains trigger- and owner-specific. |
| `R27-P04` migration/version order | PASS preserved: actual persistent/protocol delta precedes compatibility classification; no migration is selected now. |
| `R27-P05` proof-channel separation | PASS preserved: current CI is not credited as future scenario, empirical or release proof. |
| `R27-P06` release-time gates | PASS preserved: pre-tag, publication/exact-asset and post-upload acceptance remain forward ordered gates. |
| `R27-P07` dormant scale/host triggers | PASS preserved: structural support does not activate measurement/host work. |
| `R27-P08` reverse conformance | PASS preserved: all 59 material machine responsibilities and 31 exception members remain owner/classified; stale machine surfaces do not become authority. |

No probe produces a new blocker or human-owned choice during synthesis.

---

## 6. Recommendation

Proceed to one Step-5 candidate that treats the Step-2 readiness ledger as the lossless leaf layer and introduces only a **planning composition layer** above it:

```text
Step-2 source item
  -> exact Step-2 readiness record or explicit no-work terminal
  -> Step-5 candidate workstream grouping
  -> native current owner(s)
  -> destination family / activation state / prerequisite edges
  -> future Version Impact / compatibility route
  -> deterministic / scenario / empirical / release proof channels
```

The candidate should use a DAG of prerequisite relations rather than a global implementation sequence. Independent owner-local workstreams may remain parallel. Conditional branches for migration, empirical work, release acceptance and writer-specific partitioning must stay dormant until their accepted triggers fire.

No new semantic, runtime, persistence, compatibility, failure, partition, scheduling or release authority should be introduced by WP-27.

---

## 7. Strongest credible countercase

The strongest argument against proceeding without a new architecture decision is that PO-009 Story-local control/T0 persistence and PO-010 writer-specific growth handling can change persistent shape and therefore could appear too consequential to delegate.

That countercase does not cross the blocker threshold under the current owners. The accepted Story/Commentator contract fixes the semantic requirements and explicitly delegates exact event/control fields, persistence/version spelling, cache layout and shard topology. PO-010 similarly fixes measurement bands, reconstruction/currentness/atomicity constraints and activation conditions while deliberately leaving concrete geometry writer-specific. Every selected persistent/protocol shape must still pass the future Version Impact/compatibility gate before checkpoint completion. The architecture boundary is therefore fixed even though the physical realization is not.

A second credible concern is that 145 readiness records are too granular for later planning. That is a planning ergonomics issue, not an architecture gap: Step 5 can aggregate them only if it retains exact reverse membership and does not erase activation/proof/negative-law differences.

---

## 8. Confidence, uncertainty and change conditions

`RECOMMENDATION_CONFIDENCE: HIGH`.

The confidence basis is the independently repaired Step-2 package: all 224 source items have terminal routes, all 145 readiness records have accepted owners and blocker-test PASS, all 79 no-work terminals retain triggers/negative laws, the 82-item Round-2 set and PO-001..010 are reconciled, reverse conformance is complete, and all eight high-risk probes pass.

This recommendation would change only if later evidence establishes one of the following concrete conditions:

- a current accepted owner contradicts a Step-2 disposition or leaves a material semantic/authority boundary unresolved;
- an implementation-planning candidate cannot preserve exact readiness/no-work reverse traceability without merging incompatible owner/activation/proof semantics;
- a qualifying released compatibility obligation exists that changes the current WP-20 branch from deferred to active and exposes an unresolved policy choice;
- a newly discovered material machine responsibility has no accepted owner/classification;
- the independent Step-6 critic demonstrates qualifier loss, hidden authority shift, revived rejected architecture or another blocker that cannot be mechanically repaired under existing owners.

None of those conditions is established in Run-A Step 3.

---

## 9. Decision result

```text
MATERIAL_OPEN_ARCHITECTURE_OR_PRODUCT_DECISION: NONE
REAL_ALTERNATIVE_REQUIRING_HUMAN_SELECTION: NONE
RECOMMENDED_DIRECTION: OWNER-PRESERVING LOSSLESS READINESS COMPOSITION
ARCHITECTURE_BLOCKER_CANDIDATES: []
BOUNDED_ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
```

No additional approval pause is created. Under the existing WP-27 authorization, Step 4 may record the no-additional-decision disposition and then proceed to Step 5 if no new material unknown appears.

```text
WP27_STEP3: COMPLETE
RECOMMENDATION_CONFIDENCE: HIGH
HUMAN_DECISION_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
BOUNDED_ARCHITECTURE_REOPEN_REQUIRED: NO
WP27_STEP4: NOT_STARTED
```
