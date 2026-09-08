# HDM WP-25 Failure / Degradation / Durability-Risk Product and Architecture Direction

Status: **ACCEPTED PRODUCT / ARCHITECTURE DIRECTION — BINDING INPUT TO R2.7 WP-25 — NOT WP-25 CLOSURE — IMPLEMENTATION NOT AUTHORIZED**

Date: 2026-09-08

Purpose: preserve the Product Owner-approved direction for R2.7 WP-25 so the worker does not have to reconstruct material product semantics from conversation history. This document is a binding input to WP-25 framing and later synthesis. It does not replace the current native owners, does not complete WP-25 Step 1, and does not authorize implementation.

Primary current owners that this direction composes rather than replaces include Step 5.5 durability semantics, R2.3 Context Runtime, R2.4 Turn Envelope/fallback law, R2.6 host assurance, WP-13 publication/durability, WP-14 recovery/repair, WP-16 LIVE/access/currentness, WP-17 collaboration/agency, WP-18 Story/planning, WP-20 migration/compatibility, WP-21 diagnostics/cleanup, WP-22 verification completeness and WP-24 performance/operability.

---

## 1. Product intent

WP-25 must define how HDM behaves when a required or optional part of the system is unavailable, stale, ambiguous, malformed, unauthorized, inconsistent, degraded or unsupported.

The target is not a catalog of exception strings and not a global `ErrorManager`.

For every material failure condition, the system must be able to establish:

```text
what failed
what is still trustworthy
what cannot be trusted or used
how dangerous continued use would be
which gameplay scope is affected
what can safely continue
how long / until which semantic fence deferral remains acceptable
what bounded recovery/retry is lawful
what is explicitly forbidden
whether the player needs to be told or act
what future verification must prove
```

Correctness and continuity of play are both product requirements. HDM must not stop the entire campaign for a local defect when an independent scope is safe, but it must never preserve apparent continuity by guessing, silently substituting authority, replaying accepted mechanics, inventing another player's action, leaking protected information or forcing repository state.

---

## 2. Selected architecture direction

The selected direction for WP-25 is:

> **OWNER-LOCAL NATIVE OUTCOMES + EPHEMERAL CROSS-OWNER FAILURE DISPOSITION + SCOPE-AWARE CONTINUATION + RISK-TRAJECTORY-AWARE DURABILITY PROTECTION**

Native owners retain their exact outcome vocabularies and semantics. Examples include `READY | RETRY | BLOCKED`, `ASSEMBLED | ASSEMBLED_DEGRADED | UNSATISFIABLE`, publication `CONFIRMED_ACCEPTED | CONFIRMED_REJECTED | INDETERMINATE`, and compatibility `DIRECT_COMPATIBLE | MAINTENANCE_REFRESH | MIGRATION_REQUIRED | UNSUPPORTED_INCOMPATIBLE | INDETERMINATE`.

WP-25 may define a common ephemeral integration view over those outcomes, but it must not flatten them into one persisted global error authority.

A conceptual integration result may contain fields equivalent to:

```text
FailureDisposition {
    native_owner
    native_outcome
    failure_family
    affected_scopes[]
    truthful_frontier

    effective_severity
    gameplay_impact
    risk_if_ignored
    temporal_tolerance

    allowed_operations[]
    prohibited_operations[]
    recovery_class
    retry_semantics
    user_visibility
    proof_obligations[]
}
```

Exact names, serialization and whether one literal machine type is useful remain WP-25/implementation questions. The architecture requirement is the information separation, not this exact schema.

### Rejected direction A — one global Error State Machine

Rejected as baseline because it would tend to:

- collapse owner-specific epistemic states;
- create a second currentness/health authority;
- turn local defects into campaign-wide stops;
- encourage one global retry policy where native owners differ;
- blur unsupported deployment, corruption, authorization denial, ordinary wait and optional degradation.

### Rejected direction B — local outcomes only, with no cross-owner composition

Rejected as insufficient because implementation would still lack one consistent answer to:

- may gameplay continue;
- what scope is blocked;
- how risky ignoring the condition is;
- when deferral must stop;
- what the player sees;
- which cross-owner proof is required before resumption.

---

## 3. Effective severity is contextual, not intrinsic to an error type

The same root cause may have different effective severity depending on current owner, semantic dependency, unpublished-loss exposure, recovery availability and affected gameplay scope.

Baseline architecture-level severity vocabulary:

```text
S0 NOTICE
S1 DEGRADED
S2 GUARDED
S3 QUARANTINED
S4 CRITICAL
```

### S0 — NOTICE

A diagnostic, residue, optional inconsistency or unavailable non-required facility that currently changes no gameplay correctness or required capability.

Gameplay effect: none.

### S1 — DEGRADED

Correctness, authority, agency and canon remain safe, but quality, convenience, optional projection, optimization or resilience is reduced.

Gameplay may continue. Repair/service may wait for a lawful opportunity.

### S2 — GUARDED

A particular requested operation/capability cannot currently be completed honestly or lawfully.

The affected operation is blocked or unavailable; independent gameplay is not automatically blocked.

### S3 — QUARANTINED

Integrity/currentness/authority of an affected scope cannot be proven sufficiently for dependent gameplay use.

The affected scope is frozen or excluded from dependent mutation/adjudication until currentness, integrity or authority is re-established. Independent scopes may continue when their dependency closure is proven independent.

### S4 — CRITICAL

The system lacks a safe basis for the required campaign/runtime/deployment gameplay contract at the necessary scope.

Dependent gameplay cannot resume until a lawful supported basis is restored, or the deployment/capability is explicitly classified unsupported.

### Severity law

```text
FAILURE CAUSE != EFFECTIVE SEVERITY
FAILURE CAUSE != GAMEPLAY DISPOSITION
FAILURE CAUSE != RETRY POLICY
```

Severity is derived from the current concrete operation and owner composition. It must not be stored as a permanent intrinsic property of a failure code.

---

## 4. `UNSUPPORTED` is a disposition, not the highest severity

`UNSUPPORTED`, `UNSUPPORTED_INCOMPATIBLE` or equivalent means the selected capability/target/profile is not supported under the applicable owner contract.

It is orthogonal to severity.

An unsupported optional maintenance function may produce only a guarded feature-unavailable outcome. An unsupported capability required by the baseline gameplay profile may block campaign/runtime operation.

HDM must never treat `UNSUPPORTED` as permission to probe an alternate forbidden transport, guess compatibility, downgrade silently or bypass the owning authority.

---

## 5. Risk if ignored is independent from immediate gameplay severity

WP-25 must separately classify the consequence of continuing to ignore or defer a condition.

Baseline vocabulary:

```text
R0 NONE
R1 QUALITY_OR_OPERABILITY_DEBT
R2 ACCUMULATING_LOSS_OR_PROGRESS_RISK
R3 CANON_CURRENTNESS_AGENCY_OR_AUTHORITY_RISK
R4 DISCLOSURE_SECURITY_OR_CONSTITUTIONAL_RISK
```

### R0 — NONE

Continued existence of the condition creates no material current product/correctness risk.

### R1 — QUALITY_OR_OPERABILITY_DEBT

Quality, navigation, optional service, performance or maintainability may degrade, but current canon/authority/agency remain safe.

### R2 — ACCUMULATING_LOSS_OR_PROGRESS_RISK

Continued deferral increases exposure to loss of established progress, future recovery difficulty, backlog pressure or inability to satisfy a later required boundary.

### R3 — CANON_CURRENTNESS_AGENCY_OR_AUTHORITY_RISK

Using the affected dependency despite the condition may create false canon, stale adjudication, replay, invalid player agency or unauthorized state mutation.

### R4 — DISCLOSURE_SECURITY_OR_CONSTITUTIONAL_RISK

Ignoring the guard may expose ineligible information, grant rights without authority, violate stable security/product boundaries or otherwise cross a fundamental HDM invariant.

Immediate severity and ignore-risk are not interchangeable. For example, a confirmed authorization denial may be only a locally guarded operation, while bypassing it is R4.

---

## 6. Gameplay impact and affected scope are separate axes

Baseline gameplay-impact vocabulary should distinguish at least:

```text
NONE
PRESENTATION_ONLY
QUALITY_DEGRADED
FEATURE_UNAVAILABLE
DEPENDENT_OPERATION_BLOCKED
DEPENDENT_SCOPE_FROZEN
CAMPAIGN_RESUME_BLOCKED
DEPLOYMENT_PROFILE_UNSUPPORTED
```

Affected scope must remain typed. Candidate scope classes include, where applicable:

```text
PRESENTATION / RECIPIENT
ONE OPERATION
OWNER RECORD / ENTITY
PROCEDURE / DECISION DEPENDENCY
SCENE
PLAYER / CONTROL SCOPE
LIVE CLAIM / PARTITION / EPOCH
CAMPAIGN
STORAGE
RUNTIME PACKAGE
HOST / DEPLOYMENT PROFILE
```

These are not assumed to form one total containment hierarchy.

A local S3 condition must not automatically become a campaign-global block. Conversely, a small physical record can be critical if it is a required authority/currentness dependency for a wider operation.

---

## 7. Temporal tolerance uses semantic fences, not invented global timeouts

WP-25 must distinguish how long a condition may be deferred without inventing one universal retry count, timeout or wall-clock SLA.

Baseline semantic tolerance classes:

```text
IGNORE_SAFE
DEFER_TO_SAFE_OPPORTUNITY
CONTINUE_UNTIL_OWNER_FENCE
CONTINUE_OUTSIDE_AFFECTED_SCOPE
MUST_RESOLVE_BEFORE_DEPENDENT_OPERATION
MUST_RESOLVE_BEFORE_GAMEPLAY_RESUME
EXTERNAL_ACTION_REQUIRED
UNSUPPORTED_IN_CURRENT_PROFILE
```

A native owner may define a stronger exact timing/count contract. Absent such an owner, WP-25 does not manufacture seconds, turns or retries as correctness law.

Ordinary waiting for another player's still-required input is not itself a failure. Neither silence nor technical arrival order is promoted into voluntary agency.

---

## 8. Product durability-risk clarification — proactive preservation before probable host incapacity

The historical one-hour durability rule was a rough proxy for a different product concern.

The accepted Product Owner intent is:

> **Do not allow a large amount of already-established but still-volatile HOT/SOFT gameplay state to remain the only copy inside the active host context until the host/context is so exhausted or impaired that HDM can no longer perform the durability operation needed to preserve that state.**

This is **not** an hourly-autosave product requirement.

The hard-coded `durable_frontier_time / one hour` behavior is not architecture authority for this concern.

### 8.1 Unpublished-loss exposure pressure

Risk control must reason about the actual still-relevant unpublished established state and the trajectory of its loss exposure.

Relevant signals may include, where lawfully available:

- amount and materiality of still-relevant dirty HOT/SOFT state;
- severity of progress loss if the local/host context disappears;
- size/complexity of the required future durability closure;
- time/age since still-relevant unpublished state began accumulating, as one weak signal rather than universal authority;
- repeated publication failures or inability to obtain durability;
- safe established-state opportunities where a flush is comparatively cheap;
- advisory host/context pressure signals such as long-chat/context-loss/compaction indicators, approximate message/token/chat-age/capacity heuristics, or future stronger host telemetry;
- whether continued gameplay is materially increasing the amount or complexity of exposed state.

No single approximate signal becomes durability/currentness authority.

### 8.2 Risk trajectory

Deferral has a feedback effect:

```text
more established unpublished state
    -> larger potential loss
    -> potentially larger/more complex future durability closure
    -> higher cost/risk of saving later
    -> less tolerance for continued state-growing deferral
```

WP-25 must therefore allow the operational consequence of the same publication/capability problem to escalate as exposure pressure increases, even when the established HOT state remains semantically valid.

### 8.3 Conceptual exposure zones

The final architecture may rename or refine these, but it must preserve the distinction:

```text
NORMAL
ELEVATED
DANGER
```

**NORMAL** — ordinary deferrable dirty state. Gameplay proceeds with sparse I/O.

**ELEVATED** — loss or host-capacity risk is materially growing. At the next suitable safe established-state opportunity, proactive durability should outrank optional Story service, optional planning/enrichment and other nonessential work.

**DANGER** — consciously extending the only ephemeral copy with more material established gameplay state is no longer an acceptable default product behavior. The runtime should attempt a coherent durability flush/repair before accepting another operation that materially enlarges the exposed state.

Exact machine thresholds are not selected here.

### 8.4 Operability safety fence is not semantic HARD

A DANGER exposure condition does not by itself make established HOT state false or corrupt and does not manufacture a Step-5.5 correctness `MUST_BE_DURABLE_BEFORE(edge)` obligation.

The architecture must preserve this distinction:

```text
CORRECTNESS HARD
    durability is part of the named semantic edge's required postcondition

OPERABILITY / LOSS-PROTECTION FENCE
    established state is still valid,
    but the product should not keep materially increasing the single-copy loss exposure
```

OOC/rules/diagnostic/history discussion and other operations proven not to enlarge the affected dirty semantic scope may remain available while a loss-protection fence is active.

### 8.5 Failed proactive durability under high exposure

If proactive publication fails while coherent HOT survives:

- established state remains valid unless another owner establishes a distinct integrity/currentness defect;
- the system must not claim saved;
- loss protection is degraded and risk is accumulating;
- bounded retry/repair remains expected;
- severity/gameplay disposition may escalate with exposure pressure;
- under DANGER, further materially state-growing gameplay may be guarded until preservation succeeds or the user/authorized owner takes a lawful recovery action;
- the player may receive a short actionable explanation when their action is affected;
- no mechanics/RNG/canon replay, fake rollback or invented state is allowed.

This refines the product handling of `MAY_DEFER`: deferrable correctness does not mean unlimited product willingness to accumulate unrecoverable single-copy progress.

### 8.6 Capacity heuristics and false-positive/false-negative asymmetry

The current supported host does not provide a trustworthy exact remaining-context value that HDM may use as semantic authority.

Approximate capacity heuristics therefore remain advisory evidence. They may request proactive preservation and increase exposure-risk classification but cannot by themselves decide truth/currentness/authorization.

The product trade-off is asymmetric:

> **An occasional early coherent save is preferable to losing a large amount of established campaign progress because preservation was deferred until no host/tool capacity remained to perform it.**

The implementation must remain conservative without inventing a false exact capacity contract.

---

## 9. Baseline failure families that WP-25 must audit

The Step-1 Source Manifest and both critics must be capable of accounting for at least these families, without treating the list as exhaustive:

1. host / required capability absence;
2. currentness / stale source / moved authority;
3. authorization / identity / eligibility / control failure;
4. integrity / malformed representation / schema mismatch / dangling required reference / contradictory canon;
5. Context Runtime degradation / required-evidence `UNSATISFIABLE`;
6. publication / durability prepublication failure, rejection, ambiguity and partial native success;
7. recovery / missing current source / incompatible interpretation closure / retry exhaustion;
8. LIVE / claim overlap / exact-source conflict / closed-unabsorbed state / ambiguity;
9. collaboration / stale or late human input / unsatisfied required contribution / obsolete generation, while normal waiting is not error;
10. migration / compatibility unsupported or indeterminate state;
11. Story / planning / derived projection lag, conflict, stale basis or unavailable optional service;
12. presentation / interrupted output / re-presentation / disclosure uncertainty;
13. diagnostics / cleanup evidence unavailability or indeterminate eligibility;
14. runtime package / instruction-basis loss, mismatch or mixed-runtime risk;
15. compound/cascading failure: failure during recovery, repair, retry, partial success or another failure response.

---

## 10. Absolute prohibited fallbacks

No failure/degradation/recovery path may authorize:

- LLM guessing to fill missing required evidence;
- silent substitution of another semantic/currentness/authorization owner;
- model/chat memory as campaign authority;
- mechanics, RNG, accepted command or accepted causal replay merely to regenerate downstream work;
- blind retry of an ambiguous authority-changing publication;
- force push, ref rewind or branch/ref deletion;
- alternate prohibited repository transport probing/fallback;
- generic last-writer-wins or Git/arrival order as fictional authority;
- invention of another player's voluntary action, consent, pass, speech or belief;
- disclosure/visibility promotion because material is technically present;
- Story/planning/checkpoint/index/cache/diagnostic material repairing missing native canon by implication;
- unbounded world/history/ref/LIVE scans as an ordinary recovery fallback;
- infinite retry/reassembly loops;
- hidden background worker/heartbeat correctness dependencies not supported by the accepted host/product.

---

## 11. User-facing failure behavior

WP-25 must distinguish technical/operator evidence from what a player should experience.

Default goals:

- keep routine successful persistence/recovery mechanics invisible;
- do not surface internal diagnostic detail merely because a recoverable condition occurred;
- when independent gameplay can continue, do not turn a local failure into a modal global error screen;
- when player action is blocked or progress-loss risk becomes materially actionable, provide a short truthful explanation and useful next action;
- never hide repository work by inventing in-world delay, rest, NPC behavior, elapsed fictional time or fictional consequences;
- presentation repair must not create a second fictional event for an already-established occurrence.

Exact UX wording remains downstream work.

---

## 12. Verification and whole-project critic obligations

WP-25 architecture closure is insufficient unless later verification mapping can distinguish at least:

```text
positive path
negative / denied path
failure path
indeterminate / ambiguous path
recovery path
retry exhaustion
partial success
scope-isolation behavior
risk-escalation behavior
user-visible behavior
behavior that requires production-like empirical host evaluation
```

Architecture coverage is not machine realization, verification realization or empirical acceptance.

The WP-25 Step-1 critic and later Step-6 critic must independently reconstruct the current owner graph through `DEV/PROJECT_MAP.md` and actual owning artifacts. They must specifically look for stale runtime/machine projections whose wording predates later accepted architecture and must not accidentally promote those stale projections back into authority.

Known examples that require explicit reconciliation rather than blind inheritance include:

- `GAME/CORE/DURABILITY_GUARD.md` historical one-hour / `durable_frontier_time` wording versus current Step-5.5/WP-13 exposure semantics;
- runtime LIVE wording that may predate final WP-16 stable `source_native_live` identity and exact selected-source CAS/currentness law;
- any local error/retry wording that conflicts with later publication ambiguity, no-replay, access, disclosure, recovery or supported-transport owners.

These are audit obligations, not a declaration that WP-25 itself owns the final repair of every stale machine/runtime projection.

---

## 13. Decision status and downstream routing

Product Owner decision required for this direction: **NONE**.

The Product Owner has accepted:

- context-derived severity rather than intrinsic per-error severity;
- separate gameplay impact, affected scope and ignore-risk axes;
- semantic-fence-based tolerance rather than invented universal timeout;
- selected owner-local + ephemeral cross-owner composition architecture direction;
- proactive durability preservation based on unpublished-loss exposure and host-survivability risk rather than an hourly autosave requirement;
- willingness to prefer occasional early coherent persistence over large avoidable loss of established progress;
- operability/loss-protection fencing under dangerous exposure without falsely redefining that condition as semantic corruption or a generic HARD edge;
- aggressive whole-project criticism before WP-25 canonicalization.

Current routing:

```text
R2.7 WP-25 Step 1
    -> ACTIVE CONSUMER / MUST INCLUDE THIS DIRECTION IN SOURCE MANIFEST

WP-25 Steps 2-8
    -> NOT AUTHORIZED UNTIL MANDATORY INDEPENDENT STEP-1 SENIOR GO

implementation planning / runtime / schema / test realization
    -> DEFERRED UNTIL R2.7 CLOSURE + EXPLICIT IMPLEMENTATION-PLANNING AUTHORIZATION
```

This direction does not itself authorize implementation or gameplay bootstrap.
