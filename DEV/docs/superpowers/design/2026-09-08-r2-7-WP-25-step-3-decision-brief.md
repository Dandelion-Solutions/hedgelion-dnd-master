# R2.7 WP-25 Step 3 — Decision Brief

Status: **STEP 3 COMPLETE — ARCHITECTURE DECISION DETERMINED BY ACCEPTED DIRECTION + CURRENT OWNER EVIDENCE**

Date: 2026-09-08

Evidence basis:

- repaired Step-1 Task Brief / Source Manifest;
- mandatory independent Step-1 Senior re-re-review: GO;
- `2026-09-08-r2-7-WP-25-step-2-evidence-reconciliation.md`;
- current native owners named there.

This brief selects architecture only. It does not authorize implementation planning or implementation.

## 1. Decision to make

WP-25 needs one implementation-facing cross-owner contract that can answer, for a concrete blocked/degraded/failing use:

```text
what remains trustworthy
which scope is affected
what may continue
how severe the condition is for this use
what risk continued deferral creates
which semantic fence applies
what bounded recovery/retry is lawful
what user-visible action is required
what proof later realization must provide
```

The decision must preserve every native owner outcome and must not create a second currentness, persistence, lifecycle, compatibility, authorization or gameplay authority.

## 2. Established constraints

The following are already decided by accepted owners/Product Owner direction and are not open trade-offs:

1. native owner outcomes remain authoritative;
2. cross-owner composition is ephemeral;
3. failure cause != severity != gameplay impact != scope != ignore-risk != tolerance != retry/recovery != user-visible disposition;
4. `UNSUPPORTED` is orthogonal to severity;
5. severity is contextual, not intrinsic to a failure code;
6. independent scopes must continue when their dependency closure is independent;
7. accepted mechanics/RNG/IDs cannot be replayed to repair downstream failure;
8. publication ambiguity cannot be blind-retried;
9. exact historical accepted ruleset identity cannot be replaced by ambient/current mechanics;
10. authority/currentness/eligibility is owner-qualified, not one global frontier;
11. Story/planning/checkpoints/diagnostics/caches remain non-authoritative;
12. no universal retry count/timeout/global scan/background correctness service;
13. durability DANGER is an operability/loss-protection fence, not generic correctness HARD;
14. architecture/machine/verification/empirical proof classes remain distinct.

## 3. Alternatives

### Alternative A — persisted global error / health state machine

Concept:

```text
campaign/runtime health record
    owns active errors
    owns severity
    owns retry state
    owns global healthy/degraded/blocked lifecycle
```

Advantages:

- superficially simple introspection;
- one place to render status;
- straightforward global dashboards.

Material defects:

- duplicates owner currentness and lifecycle;
- cannot represent campaign/LIVE/HOT/disclosure/storage/Story domains without false global ordering;
- turns local READY_PC, maintenance or recipient failures into campaign state;
- creates cleanup/migration/persistence obligations for the error system itself;
- invites blind generic retry and stale error records;
- conflicts with accepted Product Owner direction.

Disposition: **REJECTED**.

### Alternative B — owner-local outcomes only, no common integration contract

Concept:

Every caller interprets each native owner result independently.

Advantages:

- maximal owner purity;
- no new common vocabulary.

Material defects:

- no consistent scope-aware continuation across owners;
- durability risk escalation cannot compose with publication failure;
- user-visible behavior becomes caller-specific/ad hoc;
- same native cause can be over-blocked or under-blocked by different callers;
- cross-owner partial-success and remote-success/local-failure handling lacks one explicit integration law;
- proof mapping becomes fragmented.

Disposition: **REJECTED**.

### Alternative C — session/campaign-wide ephemeral health aggregate

Concept:

Do not persist failures, but maintain one current in-memory aggregate containing the worst active severity/risk for the session/campaign.

Advantages:

- avoids durable authority;
- easier runtime diagnostics than Alternative B.

Material defects:

- still creates an implicit global currentness/health frontier;
- `max severity` across independent scopes over-blocks gameplay;
- recipient-only disclosure risk can contaminate unrelated gameplay state;
- Story/maintenance/local READY_PC issues can elevate campaign status without a dependency path;
- aggregate staleness requires its own invalidation/lifecycle logic.

Disposition: **REJECTED AS BASELINE**. A diagnostic UI may summarize multiple current dispositions as a non-authoritative projection, but such a summary cannot become continuation authority.

### Alternative D — focus-scoped ephemeral disposition over native conditions

Concept:

```text
focus operation/use boundary
+ bounded native dependency closure
+ current owner-native conditions
    -> ephemeral FailureDisposition
```

The disposition carries separated derived axes and references native outcomes/bases. It exists only to decide the current use/continuation/presentation/recovery behavior.

Advantages:

- preserves owner authority;
- naturally supports local versus campaign-wide effects;
- preserves partial native success;
- allows contextual severity/risk without intrinsic failure labels;
- supports durability exposure escalation without redefining HARD;
- gives one consistent user/proof/recovery integration contract;
- requires no persisted error lifecycle, queue or global frontier;
- can be implemented as a pure deterministic evaluator when later authorized.

Costs:

- callers must identify the correct focus and bounded dependency closure;
- native outcome adapters/descriptors must be explicit enough for the evaluator;
- diagnostics that want a dashboard must aggregate dispositions separately and non-authoritatively.

Disposition: **SELECTED**.

## 4. Selected architecture

> **FOCUS-SCOPED EPHEMERAL FAILURE DISPOSITION OVER OWNER-LOCAL NATIVE OUTCOMES + SCOPE-AWARE CONTINUATION + RISK-TRAJECTORY-AWARE DURABILITY PROTECTION**

This is a refinement of, not a change to, the accepted Product Owner direction.

### 4.1 Focus

Every disposition is evaluated for one concrete semantic decision/use boundary such as:

- execute one requested mechanic;
- assemble context for one role/task;
- publish one durability boundary;
- resume one campaign/requested operational closure;
- mutate one LIVE-owned scope;
- perform one maintenance operation;
- emit one recipient-facing response;
- adopt/migrate to one exact target package;
- create one campaign;
- save-and-exit one selected campaign.

A disposition is not “the state of the campaign”.

### 4.2 Contributors

Only native conditions in the focus's actual bounded dependency/currentness/authorization/eligibility/recovery closure contribute.

Each contributor retains:

```text
native owner/domain
native outcome/reason
native evidence/currentness basis
surviving truthful native basis
native legal retry/recovery/fence constraints
```

### 4.3 Derived axes

The evaluator derives, independently:

```text
effective severity: S0..S4
gameplay impact
affected scope(s)
risk if ignored: R0..R4
temporal tolerance / semantic fence
allowed operations
prohibited operations
recovery/retry descriptor
user-visible disposition
proof obligations
orthogonal support/compatibility disposition when applicable
```

No axis overwrites the native result.

## 5. Severity decision law

For one focus:

1. determine what must be trustworthy/available for that focus;
2. remove unrelated conditions from the composition;
3. identify the minimum restriction required by every applicable native invariant;
4. choose the severity class that corresponds to that restriction;
5. preserve all contributing native reasons.

The result is not `max(all session errors)`.

Interpretation:

```text
S0 — no material effect on the focus
S1 — correctness remains available; quality/resilience/optional service degraded
S2 — requested capability/operation cannot complete; independent work may continue
S3 — dependent use of an affected authority/integrity/currentness scope must freeze
S4 — no safe supported basis exists for required gameplay/resume at the focus scope
```

## 6. Risk decision law

Risk is independently derived from the consequence of ignoring/deferring the applicable condition for the focus:

```text
R0 — none
R1 — quality/operability debt
R2 — accumulating progress/loss/recovery exposure
R3 — canon/currentness/agency/authority risk
R4 — disclosure/security/constitutional risk
```

If several applicable risks affect the same focus, enforce the highest required risk protection for that focus. Independent-scope risks remain independent.

## 7. Truthful-basis decision law

The disposition does not own a scalar `truthful_frontier`.

It carries/references an owner-qualified truthful basis sufficient to answer:

```text
what is known accepted/current
what survived partial success
what is unresolved
what cannot be reused
what exact basis a retry/recovery must preserve or refresh
```

Examples:

- confirmed campaign publication remains real even if a second native durability domain failed;
- accepted LIVE CAS remains real after local HOT adoption failure;
- old campaign authority remains current after migration preparation/rejection;
- existing coherent HOT remains established after failed risk-control save;
- emitted gameplay remains accepted after presentation Retry/interruption.

## 8. Continuation decision law

Continuation is scope/dependency-based.

```text
unaffected/independent scope
    -> continue

optional/quality-only dependency degraded
    -> continue degraded

requested operation unavailable
    -> guard only that operation

affected authority/currentness/integrity scope unproven
    -> freeze dependent scope

required resume/deployment basis unavailable
    -> block resume for that required scope/profile
```

No local failure promotes itself to campaign-global blocking without a proven dependency path.

## 9. Durability risk decision law

For owner-permitted deferrable established dirty state:

```text
NORMAL
    ordinary deferral

ELEVATED
    proactive durability gets priority at next safe established-state opportunity
    over optional Story/planning/enrichment

DANGER
    before another operation materially enlarges the same exposed dirty scope:
        attempt coherent preservation/repair
        if unavailable, guard that state-growing operation
```

DANGER:

- does not invalidate coherent HOT;
- does not create generic HARD;
- does not prohibit OOC/diagnostic/non-growing independent work;
- uses advisory host/capacity signals only as risk evidence;
- requires later empirical threshold/calibration evidence.

## 10. Retry / recovery decision law

The common contract describes lawful follow-up but does not execute generic retries.

The descriptor must answer:

```text
retry allowed now?
precondition before retry?
repin/revalidate current authority?
preserve accepted semantic identity/RNG?
transport/reassembly-only retry?
external owner/user action required?
unsupported until profile/evidence changes?
what owner-bounded exhaustion result applies?
```

Absolute rules:

- no blind retry after indeterminate authority-changing operation;
- no force/rewind/delete/alternate transport;
- no accepted mechanics/RNG/ID replay;
- no fuzzy ruleset/context substitution;
- no generic semantic merge/LWW;
- no infinite retry/reassembly loop.

## 11. Support/unsupported decision law

`UNSUPPORTED`, `UNSUPPORTED_INCOMPATIBLE` or equivalent remains a native/orthogonal support disposition.

It does not equal S4.

The same unsupported condition may compose as:

- S2 for a requested optional feature;
- S4 when the unsupported profile is required for campaign/runtime resume.

## 12. User-visible decision law

Visibility is separately derived.

- routine internal recovery/success: no user interruption;
- quality-only optional degradation: generally silent unless material to request;
- blocked requested operation: short truthful explanation;
- external action required: explain exact actionable requirement without leaking ineligible detail;
- material DANGER loss exposure: concise preservation warning/guard explanation;
- recipient-ineligible detail: withhold/redact;
- presentation repair: re-present established information without creating new fiction.

Exact strings and machine enum spelling remain downstream work.

## 13. Proof decision law

Every later realized disposition path maps to the applicable proof class:

```text
semantic architecture law
machine realization status
verification state
empirical acceptance where host/LLM/heuristics are material
```

WP-25 architecture completion cannot claim realization of a generic evaluator or empirical calibration.

## 14. Rejected hidden variants

The selected architecture also rejects these disguised forms of a global subsystem:

- persisted active-error list;
- one session `health = degraded/blocked` authority;
- one global retry budget;
- one campaign-wide durability-danger clock;
- one total order of failure scopes;
- one universal currentness snapshot for diagnostics;
- one global unsupported flag;
- Story/checkpoint/session/diagnostic projection used as failure/currentness authority.

## 15. Decision and human gate

The Product Owner already accepted the underlying composition direction. Current evidence determines the focus-scoped refinement and exposes no material product trade-off requiring a new owner decision.

```text
SELECTED_ALTERNATIVE: D
HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
NEEDS_PO: NONE
```

Step 4 may proceed automatically.

## 16. Version Impact

```text
VERSION_IMPACT: NONE
```

This Step-3 design decision changes no version-bearing machine/runtime/schema/catalog/package surface.