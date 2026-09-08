# R2.7 WP-25 Step 5 — Candidate Implementation-Facing Specification

Status: **STEP 5 COMPLETE — CANDIDATE SPECIFICATION / PENDING STEP-6 WHOLE-PROJECT ADVERSARIAL REVIEW**

Date: 2026-09-08

Selected architecture:

> **FOCUS-SCOPED EPHEMERAL FAILURE DISPOSITION OVER OWNER-LOCAL NATIVE OUTCOMES + SCOPE-AWARE CONTINUATION + RISK-TRAJECTORY-AWARE DURABILITY PROTECTION**

This is an architecture candidate only. It defines logical implementation-facing contracts without authorizing runtime/schema/test implementation.

---

# 1. Scope and ownership

WP-25 owns only the cross-owner composition required to answer, for one bounded focus:

```text
what native condition exists
what remains trustworthy
what exact use/scope is affected
what may continue
what severity applies to that focus
what risk continued deferral/ignoring creates
what semantic fence applies
what bounded owner-native recovery/retry is lawful
what user-facing disposition is required
what future proof class applies
```

WP-25 does **not** own:

- the native failure/outcome itself;
- campaign/LIVE/storage/ruleset/currentness authority;
- gameplay lifecycle;
- persistence or publication state;
- compatibility/migration classification;
- authorization or disclosure eligibility;
- READY_PC or mechanics validity;
- Story/planning currentness;
- retry execution;
- a global health/error registry;
- a scheduler/worker/queue/heartbeat;
- a global diagnostic or cleanup frontier.

## LAW WP25-1 — NATIVE OWNER OUTCOME PRECEDES FAILURE DISPOSITION

A `FailureDisposition` consumes an already established native result/condition/evidence basis. It never manufactures or replaces that native result.

## LAW WP25-2 — FAILURE DISPOSITION IS EPHEMERAL

The baseline `FailureDisposition` is one ephemeral integration projection for one current focus. It is not required to be persisted, published, indexed, recovered, migrated, compacted, cleaned or treated as campaign state.

Persisting a future failure-related artifact requires a separately proven native consumer/owner requirement.

---

# 2. Focus and bounded input closure

Conceptual input:

```text
FailureFocus {
    operation_or_use_identity/class
    requested capability / semantic boundary
    recipient / player / control scope when material
    owner-defined dependency/currentness/authorization/eligibility closure
}
```

Exact machine naming remains implementation work.

## LAW WP25-3 — ONE DISPOSITION IS EVALUATED FOR ONE BOUNDED FOCUS

A focus is one concrete operation/use/resume/presentation/maintenance/publication boundary whose legality must be decided now.

Examples:

- one requested action/mechanic;
- one RoleContext assembly;
- one SAVE/durability boundary;
- one campaign resume attempt;
- one LIVE mutation;
- one maintenance operation;
- one recipient-facing emission;
- one exact-target compatibility/adoption evaluation;
- one campaign-creation attempt;
- one save-and-exit boundary.

A focus is not “the campaign's health”.

## LAW WP25-4 — INPUT DISCOVERY REMAINS OWNER-ROUTED AND BOUNDED

WP-25 does not scan for failures.

The caller/native orchestration supplies only conditions from the already admitted bounded dependency/currentness/authorization/eligibility/recovery footprint needed by the focus.

The evaluator SHALL NOT require:

- WORLD/campaign-wide scans;
- all-ref/all-LIVE scans;
- whole Story/history scans;
- global error enumeration;
- broad repository history;
- hidden background monitoring.

## LAW WP25-5 — UNRELATED CONDITIONS DO NOT CONTRIBUTE

A condition that cannot affect the current focus through an accepted owner/dependency relation is excluded from that disposition regardless of its severity/risk elsewhere.

---

# 3. Native contributor contract

One contributor is conceptually equivalent to:

```text
NativeCondition {
    native_owner
    native_domain
    native_outcome
    native_reason?                 # owner-defined, where material
    evidence/currentness_basis[]
    affected_native_scope[]
    surviving_truthful_basis[]
    native_fence/retry/recovery constraints
    support/compatibility disposition?  # only when the native owner defines it
}
```

This is a logical contract, not a required persisted schema.

## LAW WP25-6 — NATIVE REASON SEMANTICS ARE RETAINED

A common disposition may summarize a contributor but must retain enough native reason/evidence identity for lawful recovery, diagnostics and verification.

Examples that must not be flattened include:

```text
CONFIRMED_REJECTED != INDETERMINATE
UNSATISFIABLE != ASSEMBLED_DEGRADED
UNSUPPORTED_INCOMPATIBLE != INDETERMINATE
ruleset content_mismatch != missing_dependency != unreconstructable_context
catalog gap != dormant capability != compiler rejection
policy conflict != policy realization gap
READY_PC false != package compilation failure
NOT_AUTHORIZED != WITHHELD_OR_REDACTED
```

## LAW WP25-7 — FAILURE CAUSE IS NOT DERIVED SEVERITY

No native failure/outcome code carries intrinsic `S0..S4`, gameplay impact, blast radius, ignore-risk or retry policy.

The same native condition may compose differently for different focuses.

---

# 4. Owner-qualified truthful basis

The integration view must answer what can still be trusted without inventing one universal frontier.

Conceptually:

```text
TruthfulBasisItem {
    owner/domain
    accepted/current evidence reference
    usable_for_this_focus
    unresolved_or_excluded aspect
}
```

## LAW WP25-8 — TRUTHFUL BASIS IS OWNER-QUALIFIED COMPOSITION

The PO requirement commonly called `truthful_frontier` is realized as the bounded owner-qualified surviving basis required by the focus.

No scalar campaign HEAD, timestamp, checkpoint, session revision, Story cursor, local generation or diagnostic snapshot becomes a universal truthful frontier.

## LAW WP25-9 — PARTIAL NATIVE SUCCESS REMAINS TRUE

When one participating native domain confirms success while another fails/rejects/remains unresolved:

- the confirmed success remains real according to its owner;
- overall focus success may remain unavailable;
- the disposition records the surviving accepted basis;
- no rollback/rewind/pretend-old-authority simplification is permitted.

## LAW WP25-10 — REMOTE ACCEPTANCE OUTRANKS LOCAL ADOPTION FAILURE

After confirmed accepted remote/native authority movement, a later local HOT/cache/rebind failure is a recovery condition. It never turns the remote edge back into unaccepted state and never authorizes semantic replay.

---

# 5. Effective severity

Closed architecture vocabulary:

```text
S0 NOTICE
S1 DEGRADED
S2 GUARDED
S3 QUARANTINED
S4 CRITICAL
```

## LAW WP25-11 — SEVERITY IS FOCUS-DERIVED

Severity is derived only after the focus's required dependency/authority/currentness/eligibility basis is known.

### S0 NOTICE

No material restriction to correctness, required capability or the current focus.

### S1 DEGRADED

The focus remains semantically/correctly legal but quality, optional projection, convenience or resilience is reduced.

### S2 GUARDED

The requested operation/capability cannot lawfully complete now, while independent/unaffected operation remains available.

### S3 QUARANTINED

The integrity/currentness/authority/interpretation basis of an affected dependency scope is insufficient for dependent use; that scope remains frozen/excluded until lawful recovery/revalidation.

### S4 CRITICAL

No safe supported basis exists for the required gameplay/runtime/deployment closure needed to proceed/resume at the focus scope.

## LAW WP25-12 — NO CAMPAIGN-WIDE MAX SEVERITY

Never compute a session/campaign severity by taking the maximum of unrelated active conditions.

For one focus, enforce the strongest restriction required by applicable contributors in that focus's dependency closure. Independent scopes remain outside the calculation.

## LAW WP25-13 — SPLIT INCOMPARABLE INDEPENDENT SCOPES

If a proposed focus is too broad and contains independent subscopes with materially different continuation semantics, split the evaluation by actual dependent subfocus rather than manufacturing one over-broad severity.

A UI/diagnostic summary may list several dispositions but remains non-authoritative.

---

# 6. Gameplay impact and affected scope

Baseline gameplay-impact semantic categories:

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

Baseline affected-scope categories include, when applicable:

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

Exact machine enum spellings remain realization work unless a current native owner already fixes them.

## LAW WP25-14 — SCOPE IS SEMANTIC, NOT PHYSICAL

File, branch, commit, chat, cache or directory co-location does not determine affected semantic scope.

## LAW WP25-15 — BLAST RADIUS FOLLOWS PROVEN DEPENDENCIES

A condition blocks a wider scope only when the wider focus actually depends on the affected owner/currentness/authority/capability basis.

A local READY_PC/mechanics problem, recipient disclosure condition, optional Story lag or maintenance failure does not become campaign-wide by convenience.

---

# 7. Risk if ignored

Closed architecture vocabulary:

```text
R0 NONE
R1 QUALITY_OR_OPERABILITY_DEBT
R2 ACCUMULATING_LOSS_OR_PROGRESS_RISK
R3 CANON_CURRENTNESS_AGENCY_OR_AUTHORITY_RISK
R4 DISCLOSURE_SECURITY_OR_CONSTITUTIONAL_RISK
```

## LAW WP25-16 — RISK IS INDEPENDENT OF SEVERITY

Risk describes the consequence of ignoring/deferring the applicable condition for the focus. It does not restate current operation blockage.

Examples:

- optional Story lag -> R1;
- growing unpublished established HOT -> R2;
- stale LIVE/current rules basis -> R3;
- authorization/disclosure/force/ref-deletion bypass -> R4.

## LAW WP25-17 — NO GLOBAL MAX RISK

Risk is scope/focus relative. Where several applicable risks affect the same focus, enforce the highest protective class required for that focus while retaining the contributor reasons. Independent-scope risks do not promote one another.

---

# 8. Temporal tolerance / semantic fence

Baseline semantic categories:

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

## LAW WP25-18 — SEMANTIC FENCE REPLACES GENERIC TIMEOUT

The applicable native owner/dependency determines the fence. WP-25 introduces no universal seconds/turns/messages/retry threshold.

## LAW WP25-19 — STRONGER OWNER FENCE WINS

If the native owner supplies a stronger correctness-critical requirement, the disposition cannot weaken it merely because severity/risk would otherwise be lower.

---

# 9. Legal continuation

A disposition must identify what operations remain legal for the focus/affected scope.

## LAW WP25-20 — CONTINUE OUTSIDE THE AFFECTED DEPENDENCY

When an independent scope does not consume the failed/unresolved dependency, it remains eligible to continue under its own native owners.

## LAW WP25-21 — S2 GUARDS THE REQUESTED OPERATION, NOT THE CAMPAIGN BY DEFAULT

S2 means the concrete requested capability/operation is unavailable until its prerequisite changes. It does not imply general campaign quarantine.

## LAW WP25-22 — S3 FREEZES DEPENDENT USE OF UNPROVEN BASIS

S3 means the affected authority/currentness/integrity/interpretation basis cannot safely be consumed. Only dependent use is frozen unless the dependency is itself required for broader resume.

## LAW WP25-23 — S4 REQUIRES A PROVEN REQUIRED-BASIS FAILURE

S4 requires that the focus's required campaign/runtime/deployment closure lacks a safe supported basis. It cannot be assigned merely because a subsystem reports an alarming internal error.

---

# 10. Durability exposure trajectory

For each owner-permitted deferrable durability scope, preserve:

```text
NORMAL
ELEVATED
DANGER
```

This is an operability/loss-protection trajectory, not a replacement durability status.

## LAW WP25-24 — EXPOSURE INPUT IS STILL-RELEVANT UNPUBLISHED STATE

Risk evaluation may consider, where lawfully available:

- amount/materiality of still-relevant established unpublished state;
- loss severity;
- future durability closure complexity;
- weak age/time signal;
- repeated durability/publication failures;
- safe low-cost preservation opportunities;
- advisory host/context pressure;
- whether continued gameplay materially enlarges exposure.

No one signal becomes currentness/durability authority.

## LAW WP25-25 — ELEVATED PRIORITIZES PROACTIVE PRESERVATION

At the next suitable safe established-state opportunity, proactive durability should outrank optional Story service, planning/enrichment and other nonessential work for the affected durability scope.

## LAW WP25-26 — DANGER GUARDS FURTHER MATERIAL STATE GROWTH

Before accepting another operation that materially enlarges the same exposed dirty scope:

```text
attempt coherent durability/repair
if preservation remains unavailable:
    guard that state-growing operation
```

Operations proven not to enlarge/use the affected dirty scope may remain available.

## LAW WP25-27 — DANGER IS NOT GENERIC HARD OR CORRUPTION

DANGER alone does not:

- make coherent HOT false;
- create `MUST_BE_DURABLE_BEFORE(edge)` as a correctness law;
- declare the campaign corrupt;
- require rollback;
- create a campaign-wide autosave timer.

## LAW WP25-28 — EXACT DANGER THRESHOLDS ARE NOT ARCHITECTURE-CLOSED NUMBERS

Exact trigger/calibration rules remain later realization/empirical acceptance work under R2.6/WP-22/WP-24. Approximate token/message/chat-age/capacity heuristics remain advisory only.

---

# 11. Retry / recovery descriptor

The common contract describes lawful follow-up. It does not execute retries.

Conceptually the disposition must be able to answer:

```text
retry_allowed_now
preconditions_before_retry[]
currentness_or_authority_revalidation_required
accepted_identity/evidence_preservation[]
retry_kind: owner-native semantic retry | transport/reassembly retry | recovery/reload | external action | none
exhaustion_result/route
```

Exact realization names remain implementation detail.

## LAW WP25-29 — NATIVE RETRY SEMANTICS CONTROL

The descriptor points to owner-native retry/recovery rules. It never grants a retry that the native owner forbids.

## LAW WP25-30 — INDETERMINATE AUTHORITY CHANGE IS NEVER BLIND-RETRIED

First perform the owner-supported bounded current authority/lineage/current-closure verification. Until resolved, dependent success acknowledgement/release remains unavailable.

## LAW WP25-31 — DISJOINT TECHNICAL REBUILD DOES NOT REPLAY SEMANTICS

Where an owner proves external movement is disjoint and permits transport-only rebuild, preserve accepted semantic result, stable IDs and fixed RNG while rebasing only the transport/current source basis.

## LAW WP25-32 — RELEVANT OVERLAP USES OWNER RECONCILIATION ONLY

No generic YAML/JSON/text merge, LWW, Git order or arrival order may reconcile a semantically overlapping change unless the native owner already defines a deterministic safe relation.

## LAW WP25-33 — ACCEPTED MECHANICS/RNG ARE NEVER REPLAYED FOR DOWNSTREAM REPAIR

Persistence, publication, local adoption, Context, presentation, Story, diagnostics or transport failure after accepted mechanics does not authorize reroll/re-resolution/reallocation.

The `MECHANICS_INTEGRITY.md` correction path for narration produced without any valid accepted mechanics is a separate pre-acceptance correction case and does not weaken this law.

## LAW WP25-34 — RETRY/REASSEMBLY IS FINITE

Every retry/recovery/reassembly loop terminates under the native owner's bounded condition. WP-25 defines no universal count.

On exhaustion, expose the native unresolved/blocked/unsupported result and derive the current focus disposition from it.

---

# 12. Exact ruleset / catalog / mechanics preservation

## LAW WP25-35 — EXACT ACCEPTED RULESET IDENTITY CANNOT BE SUBSTITUTED

Accepted Resolution/Continuation interpretation remains bound to its exact typed ruleset-set/catalog context. If that exact dependency cannot be reconstructed, recovery terminates finitely according to current identity/recovery/compatibility owners.

No fuzzy current-package interpretation, hidden migration or mixed partial context is admitted.

## LAW WP25-36 — RULESET LOAD REASONS REMAIN NATIVE EVIDENCE

The current closed load/reconstruction reason set remains distinct, including:

```text
invalid_manifest
content_mismatch
missing_dependency
ambiguous_dependency
dependency_cycle
package_id_ambiguity
namespace_conflict
engine_incompatibility
catalog_incompatibility
resolved_set_mismatch
unreconstructable_context
```

A common `failure.catalog_context_incompatible` route cannot erase the exact reason when it is required for recovery/diagnosis/proof.

## LAW WP25-37 — CATALOG/CAPABILITY/COMPILER/GAMEPLAY OUTCOMES DO NOT COLLAPSE

```text
ruleset reconstruction failure
!= catalog-context incompatibility reason
!= proven capability gap
!= dormant/nonselectable capability
!= compiler/primitive rejection
!= ordinary failed gameplay action/check/save
```

---

# 13. Compatibility / unsupported

## LAW WP25-38 — COMPATIBILITY CLASSIFICATION REMAINS WP-20-OWNED

WP-25 consumes but does not rewrite:

```text
DIRECT_COMPATIBLE
MAINTENANCE_REFRESH
MIGRATION_REQUIRED
UNSUPPORTED_INCOMPATIBLE
INDETERMINATE
```

Version equality, source ancestry, package revision/order, successful parsing or load success cannot manufacture compatibility.

## LAW WP25-39 — UNSUPPORTED IS ORTHOGONAL TO SEVERITY

A native unsupported/capability/profile/compatibility disposition remains separate from `S0..S4`.

Examples:

```text
optional unsupported feature requested
    -> typically S2 + FEATURE_UNAVAILABLE

required deployment profile unsupported
    -> S4 + DEPLOYMENT_PROFILE_UNSUPPORTED
```

The exact severity depends on the focus dependency, not the word `UNSUPPORTED`.

---

# 14. Authorization / disclosure / maintenance

## LAW WP25-40 — AUTHORIZATION DENIAL IS OPERATION-SCOPED

Denied application authority blocks that operation. Repository permission or error-handler privilege cannot widen it.

Trying to bypass authorization/currentness/disclosure constitutional law is R4 regardless of whether the original requested operation would otherwise be low severity.

## LAW WP25-41 — AUTHORIZATION DOES NOT GRANT DISCLOSURE

A maintenance/diagnostic operation may be authorized while its requested output contains recipient-ineligible material. The correct outcome remains withhold/redact/partial safe output under the disclosure owner.

## LAW WP25-42 — MAINTENANCE OUTCOME LABELS ARE SEMANTIC CATEGORIES

`NOT_AUTHORIZED`, `NOT_CURRENT_OR_UNRESOLVED`, `WITHHELD_OR_REDACTED`, `UNAVAILABLE_NOT_REALIZED` are required semantic outcomes/categories. They are not frozen future runtime enum spellings.

## LAW WP25-43 — FAILURE HANDLING CREATES NO FICTIONAL DELAY

Maintenance/recovery/diagnostic/tool failure does not create turns, fictional elapsed time, NPC behavior, consent, pass, resource spend or other canonical consequence merely to explain technical work.

---

# 15. READY_PC / bootstrap / storage

## LAW WP25-44 — READY_PC AND LOCAL MECHANIC AVAILABILITY REMAIN SEPARATE

```text
provisional play with sufficient local dependencies
!= attempted mechanic blocked by missing exact dependency
!= READY_PC not yet satisfied
!= package compilation failure
```

A missing dependency blocks only the dependent mechanic unless the broader focus requires it.

## LAW WP25-45 — CREATION FAILURE DOES NOT CREATE PARTIAL CAMPAIGN AUTHORITY

Generator/scaffold/initial-publication failure cannot be repaired by LLM scaffold reconstruction, per-file fallback or setup against prepared/unpublished content.

## LAW WP25-46 — STORAGE BASELINE IS NEW-ONLY

`DND_STORAGE.engine.baseline` is storage-owner-approved identity for NEW campaigns only. It never overrides `MANIFEST.engine.current` for an existing campaign.

Storage owner, campaign creator and gameplay publication authorities remain independent.

A storage-baseline defect may be irrelevant to an existing-campaign focus and material to a New Game focus.

---

# 16. Story / planning / diagnostics nonauthority

## LAW WP25-47 — DERIVED SERVICE FAILURE DOES NOT REPLACE NATIVE TRUTH

Story/planning/index/checkpoint/cache/diagnostic failure or lag cannot reconstruct, override or invalidate usable native truth merely because the projection is missing/stale.

## LAW WP25-48 — OPTIONAL STORY/PLANNING FAILURE DOES NOT BLOCK GAMEPLAY

Where the current focus has sufficient native sources, Story/planning unavailability is quality/operability degradation only.

## LAW WP25-49 — DIAGNOSTIC INDETERMINACY REMAINS A DIAGNOSTIC LIMIT

A diagnostic projection unable to prove a cross-owner conclusion reports indeterminate/limited evidence. It does not manufacture a universal currentness snapshot.

---

# 17. Presentation and user-visible disposition

## LAW WP25-50 — USER VISIBILITY IS DERIVED INDEPENDENTLY

Severity does not directly prescribe message verbosity.

Baseline policy:

- routine successful recovery/persistence: invisible;
- optional/internal quality degradation: silent unless material to the current request;
- requested operation blocked: concise truthful explanation;
- external action required: concise actionable requirement;
- material DANGER loss exposure affecting requested state growth: concise preservation/guard explanation;
- recipient-ineligible detail: withhold/redact;
- internal tool/Connector detail: not player-facing truth by default.

Exact UX copy is downstream work.

## LAW WP25-51 — PRESENTATION REPAIR DOES NOT CREATE NEW FICTION

Re-presenting an already-established occurrence does not create another event/action/mechanics resolution. Retry/regeneration never means gameplay replay.

---

# 18. Cascading failures

## LAW WP25-52 — FAILURE DURING FAILURE HANDLING IS ANOTHER NATIVE CONDITION

Error/recovery paths gain no privileged semantics. A new owner-local failure during repair/recovery is evaluated as another bounded contributor for the new focus.

## LAW WP25-53 — MULTIPLE INDEPENDENT FAILURES REMAIN INDEPENDENT

Do not create one aggregate worst state unless the concrete requested focus actually depends on all contributors.

## LAW WP25-54 — AUTHORITY MOVEMENT INVALIDATES ONLY THE AFFECTED ATTEMPT BASIS

If current authority moves during recovery/publication/diagnostics, re-pin/revalidate the affected bounded footprint. Do not widen to campaign/history/global scan.

## LAW WP25-55 — PARTIAL TECHNICAL FREEZE IS NOT PARTIAL FICTION

Multi-source prerequisite closure may leave some sources technically frozen while the intended semantic cross-scope result remains unestablished. The disposition must preserve that distinction.

---

# 19. Proof / realization contract

## LAW WP25-56 — FOUR PROOF DIMENSIONS REMAIN SEPARATE

```text
ARCHITECTURE COVERAGE
MACHINE REALIZATION
VERIFICATION REALIZATION
EMPIRICAL ACCEPTANCE
```

The canonical architecture may require later proof but cannot claim it has already occurred.

## LAW WP25-57 — FUTURE VERIFICATION MUST COVER POLARITY

A later realized evaluator/integration mapping must cover at least:

```text
positive
negative/denied
failure
indeterminate/ambiguous
partial success
recovery
retry exhaustion
scope isolation
risk escalation
unsupported capability/profile
user-visible behavior
```

## LAW WP25-58 — HOST-RISK CALIBRATION IS EMPIRICAL WHERE MATERIAL

Exact capacity/long-chat/DANGER heuristics, false-positive/false-negative behavior and material user-facing host behavior require the real implemented supported target where deterministic proof is insufficient.

No preimplementation surrogate establishes that acceptance.

---

# 20. Stale/deferred realization map

Current architecture records but does not repair:

```text
GAME/CORE/DURABILITY_GUARD.md
GAME/CORE/SESSION.md
GAME/CORE/STORAGE.md
DEV/TESTS/test_hourly_durability_contract.py
    -> stale one-hour durability projection

DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md
    -> semantic contract present / installed runtime command surface not realized

focus-scoped FailureDisposition evaluator/adapters
    -> architecture-only / implementation deferred

cross-owner failure integration tests/scenarios
    -> future realization/verification obligation

host-risk/DANGER thresholds
    -> exact policy calibration deferred to realized/empirical evidence
```

Current stale tests/projections do not reactivate superseded semantics.

---

# 21. Prohibited baseline designs

The following are nonconforming absent a future explicit owner decision proving need:

- persisted global Error/Failure record;
- session/campaign `health` authority;
- global active-error list used for continuation;
- universal retry engine/count;
- generic rollback/rewind handler;
- global durability danger timer/frontier;
- global unsupported flag;
- failure-driven branch/ref deletion or force;
- alternate transport fallback;
- error-handler WORLD/history/all-ref/all-LIVE scan;
- background failure monitor required for correctness;
- Story/checkpoint/session/diagnostic state promoted to truth/currentness;
- generic error-handler gameplay replay/reroll;
- generic compatibility inference from version/order/ancestry.

---

# 22. Candidate derivation procedure

A later implementation may realize an equivalent deterministic pure evaluation procedure:

```text
1. identify focus operation/use boundary
2. obtain bounded owner-native dependency/currentness/authorization/eligibility closure
3. collect current native conditions/results from that closure
4. discard unrelated conditions
5. preserve native outcomes/reasons + owner-qualified surviving truthful basis
6. derive affected scope(s)
7. derive gameplay impact
8. derive effective severity for the focus
9. derive risk-if-ignored
10. derive native semantic fence/tolerance
11. derive allowed/prohibited continuation classes
12. attach owner-native retry/recovery descriptor
13. attach orthogonal unsupported/compatibility disposition when applicable
14. derive recipient-safe user-visible disposition
15. attach future proof obligations
16. emit ephemeral FailureDisposition
```

If Step 6 proves that a candidate field/step creates duplicate authority or requires an unbounded/global source, repair the candidate before canonicalization.

---

# 23. Step-5 result

```text
STEP5_STATUS: COMPLETE / CANDIDATE SPECIFICATION
SELECTED_ARCHITECTURE: FOCUS-SCOPED EPHEMERAL FAILURE DISPOSITION
PERSISTED_GLOBAL_ERROR_AUTHORITY: NO
GLOBAL_HEALTH_STATE: NO
UNIVERSAL_RETRY_ENGINE: NO
CAMPAIGN_WIDE_ERROR_LIFECYCLE: NO
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
VERSION_IMPACT: NONE
```

Next: mandatory Step-6 whole-project adversarial review. No implementation planning or implementation is authorized.