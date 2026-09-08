# R2.7 WP-25 Step 6 — Whole-Project Adversarial Review

Status: **STEP 6 COMPLETE — 0 BLOCKING / 6 SIGNIFICANT / 3 MINOR FINDINGS — ALL MECHANICALLY RESOLVABLE / STEP 7 REQUIRED**

Date: 2026-09-08

Reviewed candidate:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-25-step-5-candidate-specification.md`

Selected architecture under attack:

> **FOCUS-SCOPED EPHEMERAL FAILURE DISPOSITION OVER OWNER-LOCAL NATIVE OUTCOMES + SCOPE-AWARE CONTINUATION + RISK-TRAJECTORY-AWARE DURABILITY PROTECTION**

This review independently reconstructed the task-specific direct and indirect dependency graph from current `DEV/PROJECT_MAP.md`, then attacked the candidate against current owners, consumers, negative/indeterminate/cascading cases, stale realization and the architecture/machine/verification/empirical proof boundary.

No private Lab/audit source is used.

---

## 1. Review method

The review attacked whether candidate wording could accidentally create or imply:

1. a second semantic/currentness/authorization authority;
2. an unbounded completeness requirement or global failure scan;
3. a hidden ACL through `allowed_operations` / `prohibited_operations`;
4. a universal retry engine or background durability scheduler;
5. semantic authority from advisory host/context-capacity heuristics;
6. rollback/replay after partial or already accepted native success;
7. global severity/risk state from independent scopes;
8. compatibility inference from version/equality/ancestry;
9. Story/checkpoint/diagnostic/current-context promotion to native truth;
10. stronger machine/verification/empirical claims than current evidence supports.

Direct and indirect owner routes included durability/publication/recovery, Context/host/instructions, access/LIVE/collaboration/disclosure, ruleset/catalog/mechanics/House Rules, compatibility/migration, bootstrap/READY_PC/storage/save-exit, Story/planning/diagnostics/cleanup, boundedness/performance and proof completeness.

---

## 2. Result summary

```text
STEP6_BLOCKING_FOUND: 0
STEP6_SIGNIFICANT_FOUND: 6
STEP6_MINOR_FOUND: 3

HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
NEEDS_PO: NONE
SELECTED_ARCHITECTURE_CHANGED: NO
WHOLESALE_UPSTREAM_REOPEN_REQUIRED: NO
```

All findings are mechanical qualification/propagation defects. None changes Product Owner semantics or accepted native ownership.

---

## 3. SIGNIFICANT findings

### F25-06-01 — Focus input completeness must be owner-proven, not caller-asserted

Severity: **SIGNIFICANT**

Attack:

Candidate LAW WP25-4 says the caller/native orchestration supplies the bounded footprint, but does not state strongly enough how the evaluator knows the supplied focus closure is sufficient. A caller could omit a required currentness/authorization/recovery dependency and then derive an artificially low severity or permissive continuation.

Current-owner evidence:

- R2.3 required packet/closure is consumer-contract-owned and missing required evidence yields finite failure;
- WP-13/WP-14/WP-16 use bounded semantic/currentness footprints with explicit owner obligations;
- WP-24 boundedness never permits omission of correctness-required dependencies merely to remain cheap.

Required repair:

```text
A FailureDisposition is valid only when the focus's required dependency/currentness/
authorization/eligibility/recovery closure is established by the applicable owner/consumer
contract or another owner-valid completeness relation.

Unproven completeness cannot be treated as an empty/healthy closure.
If required completeness cannot be established, preserve the native unresolved/
UNSATISFIABLE/INDETERMINATE/BLOCKED result for the dependent focus.
```

The repair must not require a global scan.

Affected artifacts:

- Step 5 candidate — normative qualification required;
- final canonical WP-25 owner — normative law required;
- Step 7 resolution ledger — explicit closure required.

### F25-06-02 — FailureDisposition-derived continuation is advisory integration output, not authorization/currentness authority

Severity: **SIGNIFICANT**

Attack:

Candidate wording says the disposition identifies legal continuation and allowed/prohibited operations. Without a hard boundary, an implementation could treat the disposition itself as a reusable permission token/currentness lease.

Current-owner evidence:

- access control authorizes operations from current native identity/owner state;
- WP-16 explicitly rejects stale authorization evidence as a permission lease;
- WP-21 diagnostics/dry runs never reserve authority;
- native currentness must be re-established at owner-required mutation boundaries.

Required repair:

```text
FailureDisposition does not authorize an operation, reserve eligibility, prove currentness,
or waive native preconditions.

`allowed_operations` / `prohibited_operations` are derived continuation classifications for
this focus/basis only. Every later protected operation still passes its native current
owner/currentness/authorization/eligibility contract.
```

Affected artifacts:

- Step 5 candidate — normative qualification required;
- Step 3 Decision Brief — selected design should self-identify this restriction;
- Step 4 cross-system review — access/LIVE/diagnostic sections should self-identify it;
- final canonical owner.

### F25-06-03 — Derived allowed/prohibited-operation sets must not become a new generic ACL vocabulary

Severity: **SIGNIFICANT**

Attack:

A literal generic list of operation IDs could become a central authorization registry or duplicate every native owner's operation grammar.

Required repair:

The canonical contract must permit an equivalent continuation classification without requiring a universal operation registry. Implementations may represent continuation as typed categories, focus-specific decisions or references to native operations. No generic WP-25 operation namespace/ACL is required.

Affected artifacts:

- Step 5 candidate;
- final canonical owner;
- future implementation/debt wording only — no implementation authorized now.

### F25-06-04 — DANGER durability behavior must not imply automatic retry loop, scheduler or hidden execution opportunity

Severity: **SIGNIFICANT**

Attack:

Candidate LAW WP25-26 says to attempt coherent durability/repair before state growth. If interpreted mechanically without the host-execution constraints, this could produce repeated automatic retries, background polling or a hidden scheduler until persistence succeeds.

Current-owner evidence:

- Step-5.5 has no exact background wall-clock flush guarantee;
- R2.4/R2.6 support one-request/one-turn ordinary execution and no hidden worker correctness dependency;
- WP-13/WP-24 require bounded retries and no universal retry count.

Required repair:

```text
DANGER requests one owner-valid bounded preservation/recovery opportunity at the current
admitted execution point.
It does not create a loop, background retry, heartbeat, scheduler or exact wall-clock trigger.
If the bounded attempt remains unavailable/unsuccessful, guard further material state growth
for the affected scope and expose the appropriate native/external-action disposition.
```

Affected artifacts:

- Step 5 candidate;
- final canonical owner;
- Step 7 finding ledger.

### F25-06-05 — Advisory host/context pressure cannot establish DANGER or severity by itself

Severity: **SIGNIFICANT**

Attack:

The candidate lists token/message/chat-age/context pressure among exposure inputs. Although it calls them advisory, it still permits an implementation to let a heuristic alone promote the scope to DANGER and thereby guard gameplay, effectively turning non-authoritative telemetry into a semantic fence.

Current-owner evidence:

- R2.6 explicitly rejects exact hidden-capacity dependency;
- Product Owner direction permits advisory heuristics to request proactive preservation but not decide truth/currentness/authorization;
- WP-22/WP-24 route calibration to real-target empirical acceptance.

Required repair:

```text
Approximate host/context-pressure evidence may increase confidence that proactive
preservation should be attempted and may contribute to a conservative exposure-risk
assessment, but it cannot by itself establish currentness, corruption, authorization,
or a false exact remaining-capacity threshold.

A gameplay-affecting DANGER guard must also be grounded in owner-valid still-relevant
unpublished-state/loss-exposure evidence for the affected durability scope.
```

Exact calibration remains deferred and empirical.

Affected artifacts:

- Step 5 candidate;
- final canonical owner;
- proof/realization/debt sections.

### F25-06-06 — Partial/accepted native success must survive recomposition and later failure-handler failure

Severity: **SIGNIFICANT**

Attack:

Candidate LAW WP25-9/10 correctly preserves partial and remote success, but cascading LAW WP25-52 could be read as creating a fresh disposition that forgets prior accepted bases when failure handling itself fails. That could re-enable retry/replay or falsely restore the older authority.

Current-owner evidence:

- WP-13 partial native success remains real;
- WP-16 confirmed LIVE CAS survives local adoption failure;
- WP-20 accepted migration publication survives local rebind failure;
- Step-5.14 accepted mechanics/remote semantics never replay to repair downstream work.

Required repair:

```text
Every successor/recovery disposition must carry forward all still-applicable already accepted
native bases/identities from the causal chain.
A new failure condition may narrow what can continue, but cannot erase accepted publication,
accepted mechanics/RNG, stable IDs or other native success.
```

Affected artifacts:

- Step 5 candidate;
- final canonical owner;
- future verification polarity requirements.

---

## 4. MINOR findings

### F25-06-M1 — Ordinary waiting must remain explicitly non-failure in final common semantics

Severity: **MINOR**

WP-17 already owns ordinary unsatisfied human waiting. Add a compact explicit negative invariant so an implementation does not create S1/S2 merely because a participant has not yet replied. A positive owner-defined dependency may block its dependent focus, but waiting itself is not system failure.

### F25-06-M2 — User-visible disposition is a recipient-safe projection, not disclosure evidence/authority

Severity: **MINOR**

The final contract should state that a generated failure explanation does not itself grant eligibility or advance `runtime.disclosure` except through the existing Step-5.12 emission/disclosure owner when a real emission is committed.

### F25-06-M3 — `UNSUPPORTED` remains orthogonal not only to severity but also to generic `failure_family`

Severity: **MINOR**

An unsupported capability/profile/compatibility result may coexist with or explain an unavailable focus, but WP-25 must not require all unsupported states to be represented as generic system failures. Native support/compatibility disposition remains first-class and orthogonal.

---

## 5. Negative-invariant attack sweep

Result after required repairs: **PASSABLE / NO NEW BLOCKER**.

The architecture continues to prohibit:

- guessing missing required evidence;
- silent semantic/currentness/authorization source substitution;
- chat/model memory as campaign authority;
- replay/reroll/reallocation of accepted mechanics/RNG/IDs;
- blind retry of ambiguous authority-changing publication;
- force push/ref rewind/branch-ref deletion;
- alternate forbidden transport;
- Git/LWW/arrival order as fictional authority;
- invention of voluntary player action/consent/pass/speech;
- recipient-disclosure promotion from physical visibility;
- Story/planning/checkpoint/index/cache/diagnostic substitution for canon;
- ordinary unbounded WORLD/history/all-ref/all-LIVE scanning;
- infinite retry/reassembly;
- hidden background correctness worker/heartbeat.

---

## 6. Cascading and indeterminate attack matrix

| Attack | Required repaired disposition |
|---|---|
| incomplete caller-supplied dependency closure | fail/defer with native unresolved completeness; never assume healthy empty closure |
| authorization changed after disposition | revalidate native authorization; old disposition grants no lease |
| LIVE route/current source changed after disposition | re-pin/revalidate affected native footprint |
| remote publication accepted, local adoption fails, then reload fails | preserve remote acceptance; new local recovery failure cannot roll back/replay |
| one SAVE domain accepted, second indeterminate | accepted domain remains real; overall SAVE unresolved; no blind retry |
| DANGER durability attempt fails | one bounded attempt; guard only further state growth in affected scope; no loop/worker |
| approximate context-pressure warning only, no material dirty exposure | may request conservative save opportunity; cannot fabricate corruption/currentness or exact-capacity law |
| Story/diagnostic failure during gameplay | native gameplay continues when sufficient; projections remain nonauthority |
| unsupported optional facility | feature unavailable; no automatic S4/global health state |
| ordinary human wait | not system failure; only native positive dependency controls dependent continuation |
| failure explanation contains secret detail | disclosure owner withholds/redacts before emission |
| accepted RNG followed by presentation Retry | re-present; no reroll/re-resolution |

---

## 7. Architecture vs realization vs verification vs empirical proof

Current Step-6 evidence establishes only architecture findings and owner reconciliation.

It does **not** establish:

- a realized `FailureDisposition` type/evaluator;
- a realized generic operation vocabulary;
- DANGER threshold implementation;
- corrected one-hour runtime/test realization;
- installed maintenance command handling;
- integrated failure-path executable verification;
- empirical long-chat/context-risk calibration;
- production-like user-visible behavior acceptance.

These remain explicitly downstream until implementation planning/execution is separately authorized.

---

## 8. Finding propagation requirements for Step 7

Every finding must be handled item-by-item:

| Finding | Step 5 | Step 3 | Step 4 | Canonical spec | Other current owner |
|---|---|---|---|---|---|
| F25-06-01 | repair | historical decision retained | no change required | incorporate | none |
| F25-06-02 | repair | qualify | qualify | incorporate | none |
| F25-06-03 | repair | no change required | no change required | incorporate | none |
| F25-06-04 | repair | no change required | no change required | incorporate | none |
| F25-06-05 | repair | no change required | no change required | incorporate | none |
| F25-06-06 | repair | no change required | no change required | incorporate | none |
| F25-06-M1 | repair/final negative invariant | no change required | already materially present | incorporate | none |
| F25-06-M2 | repair/final qualification | no change required | already materially present | incorporate | none |
| F25-06-M3 | repair/final qualification | no change required | no change required | incorporate | none |

Historical native owners and old provenance are not rewritten as though WP-25 existed earlier.

---

## 9. Step-6 disposition

```text
STEP6_STATUS: COMPLETE
STEP6_BLOCKING_FOUND: 0
STEP6_SIGNIFICANT_FOUND: 6
STEP6_MINOR_FOUND: 3

UNRESOLVED_BLOCKING_BEFORE_STEP7: 0
UNRESOLVED_SIGNIFICANT_BEFORE_STEP7: 6
UNRESOLVED_MINOR_BEFORE_STEP7: 3

HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
SELECTED_ARCHITECTURE_RETAINED: YES
STEP7_REQUIRED: YES
```

Step 7 must mechanically resolve and propagate all nine findings before canonicalization.