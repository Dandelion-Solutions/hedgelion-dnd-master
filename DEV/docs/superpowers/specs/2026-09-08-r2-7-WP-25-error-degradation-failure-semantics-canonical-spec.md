# R2.7 WP-25 — Error / Degradation / Failure Semantics — Canonical Specification

Status: **CANONICAL WP-25 SEMANTIC OWNER — FINAL SENIOR HOLD RECOVERY APPLIED AT WORKER LEVEL / MANDATORY INDEPENDENT FINAL SENIOR RE-REVIEW PENDING**

Date: 2026-09-08

Canonical direction:

> **FOCUS-SCOPED EPHEMERAL FAILURE DISPOSITION OVER OWNER-LOCAL NATIVE OUTCOMES + SCOPE-AWARE CONTINUATION + RISK-TRAJECTORY-AWARE DURABILITY PROTECTION**

Design chain:

- repaired Step-1 Task Brief / open-world Source Manifest;
- mandatory independent Step-1 Senior re-re-review: **GO WITH REQUIRED NON-BLOCKING SOURCE-ROLE CORRECTION**;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-25-step-2-evidence-reconciliation.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-25-step-3-decision-brief.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-25-step-4-cross-system-review.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-25-step-5-candidate-specification.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-25-step-6-whole-project-adversarial-review.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-25-step-6-propagation-qualification-addendum.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-25-step-7-finding-resolution-propagation.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-25-step-8-canonicalization-checkpoint.md`.

Where earlier Step-3/4/5 wording differs from the Step-6/7 qualifications incorporated here, this canonical specification controls.

Mandatory independent final Senior review of baseline `f3c2c978cd150dbc1be510def34d14fe61067c7c` returned HOLD with three bounded realization/traceability findings and explicitly required no canonical WP-25 architecture reopen. Sections 1–22 below therefore remain semantically unchanged; Sections 23–25 record only the mechanically synchronized realization/debt/version/gate state.

This specification does not authorize implementation planning, generic FailureDisposition implementation, release/migration execution, gameplay bootstrap or WP-26. The bounded final-Senior recovery recorded here authorizes only the mechanically implied runtime/test/traceability synchronization required to remove contradictions with already-settled law.

---

# 1. Responsibility and non-authority boundary

WP-25 owns only the cross-owner composition needed to answer, for one bounded current focus:

```text
what native condition exists
what remains trustworthy
what use/scope is affected
what may continue
what effective severity applies
what risk continued ignoring/deferral creates
what semantic fence/tolerance applies
what bounded native recovery/retry is lawful
what the user may need to know/do
what future proof class applies
```

WP-25 does not own:

- native failure/outcome semantics;
- campaign/LIVE/storage/ruleset/currentness authority;
- gameplay lifecycle;
- persistence/publication state;
- compatibility/migration classification;
- authorization or disclosure eligibility;
- READY_PC or deterministic mechanics validity;
- Story/planning/diagnostic currentness;
- retry execution;
- a global health/error lifecycle;
- a persisted error registry;
- a universal operation ACL;
- a scheduler/worker/queue/heartbeat;
- a global diagnostic/currentness frontier.

## LAW WP25-1 — Native owner outcome precedes disposition

A common failure disposition consumes an already established native result/condition/evidence basis. It never manufactures, replaces, reclassifies away or becomes the source of that native result.

## LAW WP25-2 — Failure disposition is ephemeral

Baseline `FailureDisposition` is one ephemeral integration projection for one current focus. It is not required to be persisted, published, indexed, recovered, migrated, compacted, cleaned or treated as campaign state.

A future durable failure-related artifact requires a separately proven native consumer/owner requirement and explicit architecture authorization.

## LAW WP25-3 — Failure disposition is not authority or a lease

A disposition does not:

```text
authorize an operation
reserve authorization or eligibility
prove currentness for a later mutation
waive a native prerequisite
act as a permission token
act as a currentness lease
```

Every protected operation still passes its applicable native current owner/currentness/authorization/eligibility contract at the owner-required boundary.

---

# 2. Focus and owner-proven bounded closure

Conceptual focus input may be represented equivalently to:

```text
FailureFocus {
    operation_or_use_identity_or_class
    requested capability / semantic boundary
    recipient / player / control scope when material
    owner-defined dependency/currentness/authorization/eligibility/recovery closure
}
```

Exact names/serialization remain implementation work.

## LAW WP25-4 — One disposition is evaluated for one bounded focus

A focus is one concrete operation/use/resume/presentation/maintenance/publication boundary whose legal continuation must be decided now.

Examples include:

- one requested mechanic/action;
- one RoleContext assembly;
- one SAVE/durability boundary;
- one recovery/resume attempt;
- one LIVE mutation;
- one maintenance operation;
- one recipient-facing emission;
- one exact-target compatibility/adoption evaluation;
- one New Game creation attempt;
- one save-and-exit boundary.

A focus is not “campaign health”.

## LAW WP25-5 — Input discovery remains owner-routed and bounded

WP-25 does not scan for failures. Inputs come only from the admitted bounded dependency/currentness/authorization/eligibility/recovery footprint required by the focus.

Failure evaluation SHALL NOT require ordinary:

- WORLD/campaign-wide scans;
- all-ref/all-LIVE scans;
- whole Story/history scans;
- global active-error enumeration;
- broad Git-history walks;
- hidden background monitoring.

## LAW WP25-6 — Focus-closure completeness must be owner-proven

A disposition is valid only when the required focus closure is established by the applicable native owner/consumer contract or another owner-valid completeness relation.

```text
caller omission != irrelevance
unproven required closure != healthy/empty closure
```

If required closure completeness cannot be established, preserve the applicable native unresolved / `UNSATISFIABLE` / `INDETERMINATE` / `BLOCKED` result for the dependent focus.

Boundedness never authorizes omission of correctness-required dependencies. Failure to prove bounded completeness never authorizes a global scan.

## LAW WP25-7 — Unrelated conditions do not contribute

A condition that cannot affect the current focus through an accepted owner/dependency relation is excluded regardless of its severity/risk elsewhere.

If a proposed focus contains independent subscopes with materially different continuation semantics, split it into actual dependent subfocus evaluations instead of manufacturing a broad aggregate state.

---

# 3. Native contributor and truthful-basis contract

A contributor may be represented conceptually as:

```text
NativeCondition {
    native_owner
    native_domain
    native_outcome
    native_reason?
    evidence/currentness_basis[]
    affected_native_scope[]
    surviving_truthful_basis[]
    native_fence/retry/recovery_constraints
    support_or_compatibility_disposition?
}
```

This is a logical integration contract, not a required persisted schema.

## LAW WP25-8 — Native reason semantics are retained

Common composition must retain enough native outcome/reason/evidence identity for lawful recovery, diagnostics and verification.

Material distinctions include, without flattening:

```text
publication:
    CONFIRMED_ACCEPTED != CONFIRMED_REJECTED != INDETERMINATE

recovery:
    READY != RETRY != BLOCKED

Context:
    ASSEMBLED != ASSEMBLED_DEGRADED != UNSATISFIABLE

compatibility:
    DIRECT_COMPATIBLE
    != MAINTENANCE_REFRESH
    != MIGRATION_REQUIRED
    != UNSUPPORTED_INCOMPATIBLE
    != INDETERMINATE

maintenance semantic categories:
    NOT_AUTHORIZED
    != NOT_CURRENT_OR_UNRESOLVED
    != WITHHELD_OR_REDACTED
    != UNAVAILABLE_NOT_REALIZED
```

Exact maintenance machine enum spelling remains future realization-owned.

## LAW WP25-9 — Failure cause and derived axes remain different

```text
FAILURE CAUSE
!= EFFECTIVE SEVERITY
!= GAMEPLAY IMPACT
!= AFFECTED SCOPE
!= RISK IF IGNORED
!= TEMPORAL TOLERANCE
!= RETRY/RECOVERY SEMANTICS
!= USER-VISIBLE DISPOSITION
```

No native outcome code carries intrinsic S0–S4, R0–R4 or universal retry behavior.

## LAW WP25-10 — Truthful basis is owner-qualified, not scalar

The Product Owner concept of `truthful_frontier` is realized as the bounded owner-qualified surviving basis required by the focus.

No scalar campaign HEAD, timestamp, checkpoint, session revision, Story cursor, local generation or diagnostic snapshot becomes a universal truthful frontier.

## LAW WP25-11 — Partial native success remains real

If one native domain confirms success while another participating domain fails/rejects/remains unresolved:

- confirmed success remains real according to its owner;
- overall focus success may remain unavailable;
- the surviving accepted basis remains explicit;
- no rewind/force/pretend-old-authority simplification is allowed.

## LAW WP25-12 — Accepted bases survive successor failure dispositions

Every successor/recovery/failure-handler disposition carries forward all still-applicable already accepted native bases/identities from the causal chain.

A new downstream failure may narrow continuation but cannot erase or replay:

- confirmed native publication/CAS success;
- accepted mechanics/RNG;
- stable accepted IDs;
- accepted migration/adoption publication;
- other accepted owner-native semantic edges.

## LAW WP25-13 — Remote/native accepted authority survives local adoption failure

After confirmed accepted remote/native authority movement, later local HOT/cache/rebind failure is a recovery condition. It never turns the accepted edge back into unaccepted state and never authorizes semantic replay.

---

# 4. Effective severity

Canonical architecture vocabulary:

```text
S0 NOTICE
S1 DEGRADED
S2 GUARDED
S3 QUARANTINED
S4 CRITICAL
```

## LAW WP25-14 — Severity is focus-derived

Severity is derived only after the focus's required dependency/authority/currentness/eligibility basis is known.

### S0 NOTICE

No material restriction to correctness, required capability or the current focus.

### S1 DEGRADED

The focus remains semantically/correctly legal, but quality, optional projection, convenience, resilience or operability is reduced.

### S2 GUARDED

The requested operation/capability cannot lawfully complete now while independent/unaffected use remains available.

### S3 QUARANTINED

Integrity/currentness/authority/interpretation of an affected dependency scope cannot be proven sufficiently for dependent use. That dependent scope remains frozen/excluded until lawful recovery/revalidation.

### S4 CRITICAL

The required campaign/runtime/deployment gameplay closure for this focus has no safe supported basis to proceed/resume.

## LAW WP25-15 — No campaign-wide max severity

Never compute a session/campaign severity by taking the maximum of unrelated active conditions.

Within one proven focus closure, enforce the strongest restriction required by its applicable contributors while retaining native reasons. Independent scopes do not promote one another.

S4 requires a proven required-basis failure, not merely an alarming internal error.

---

# 5. Gameplay impact and affected scope

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

Baseline affected-scope categories may include:

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

Exact machine enum spelling remains realization work unless a native owner already fixes it.

## LAW WP25-16 — Scope is semantic, not physical

File, branch, commit, chat, cache or directory co-location does not determine semantic blast radius.

## LAW WP25-17 — Blast radius follows proven dependencies

A condition blocks wider use only when that use actually depends on the affected owner/currentness/authority/capability basis.

A local READY_PC/mechanic condition, recipient disclosure condition, optional Story lag or maintenance failure is not campaign-wide by convenience.

---

# 6. Risk if ignored

Canonical vocabulary:

```text
R0 NONE
R1 QUALITY_OR_OPERABILITY_DEBT
R2 ACCUMULATING_LOSS_OR_PROGRESS_RISK
R3 CANON_CURRENTNESS_AGENCY_OR_AUTHORITY_RISK
R4 DISCLOSURE_SECURITY_OR_CONSTITUTIONAL_RISK
```

## LAW WP25-18 — Risk is independent of severity

Risk describes the consequence of ignoring/deferring the applicable condition. It does not restate current operation blockage.

Examples:

- optional Story lag with sufficient native truth -> R1;
- growing unpublished established HOT -> R2;
- using stale LIVE/current rules basis -> R3;
- bypassing authorization/disclosure/force/ref-deletion boundaries -> R4.

## LAW WP25-19 — No global max risk

Risk remains focus/scope-relative. Within one focus enforce the strongest required protection while retaining contributing native reasons. Independent-scope risks do not promote one another.

---

# 7. Temporal tolerance and semantic fences

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

## LAW WP25-20 — Semantic fence replaces generic timeout

The applicable native owner/dependency determines the semantic fence. WP-25 introduces no universal seconds, turns, messages, retry count or wall-clock SLA.

A stronger owner-defined correctness fence cannot be weakened by a lower derived severity/risk.

---

# 8. Legal continuation without a new ACL

## LAW WP25-21 — Continue outside the affected dependency

An independent scope that does not consume the affected dependency remains eligible to continue under its own native owners.

## LAW WP25-22 — S2 guards the requested operation, not the campaign by default

S2 means the concrete requested capability is unavailable until its prerequisite changes. It does not imply generic campaign quarantine.

## LAW WP25-23 — S3 freezes only dependent use of unproven basis

S3 excludes/fences dependent use of the affected authority/currentness/integrity/interpretation basis. It expands only when a wider requested focus proves dependency on that basis.

## LAW WP25-24 — Continuation classification is not authorization

Candidate concepts such as `allowed_operations[]` / `prohibited_operations[]` are derived continuation classifications for one current focus/basis only.

WP-25 requires no universal operation namespace, global ACL registry or duplicated operation catalog. Equivalent realization may use focus-specific decisions, typed continuation categories or native-operation references.

The classification never grants native authorization/currentness/eligibility.

---

# 9. Durability exposure trajectory

For each owner-permitted deferrable durability scope preserve:

```text
NORMAL
ELEVATED
DANGER
```

This is an operability/loss-protection trajectory, not a replacement durability status.

## LAW WP25-25 — Exposure is based on still-relevant unpublished established state

Relevant evidence may include, where lawfully available:

- amount/materiality of still-relevant established unpublished state;
- loss severity;
- future durability-closure complexity;
- weak age/time signal;
- repeated durability/publication failure;
- safe low-cost preservation opportunities;
- advisory host/context pressure;
- whether continued play materially enlarges exposure.

No one signal becomes durability/currentness authority.

## LAW WP25-26 — ELEVATED prioritizes proactive preservation

At the next suitable safe established-state opportunity, proactive durability should outrank optional Story service, planning/enrichment and other nonessential work for the affected durability scope.

## LAW WP25-27 — DANGER guards further material state growth

At the current admitted execution opportunity, before accepting another operation that materially enlarges the same exposed dirty scope, request one owner-valid bounded preservation/recovery attempt.

If preservation remains unavailable/unsuccessful, guard that state-growing operation and expose the applicable native/external-action disposition.

Operations proven not to enlarge/use the affected dirty scope may remain available.

## LAW WP25-28 — DANGER is not HARD, corruption or a scheduler

DANGER alone does not:

- make coherent HOT false;
- create `MUST_BE_DURABLE_BEFORE(edge)` as a correctness law;
- declare campaign corruption;
- require rollback;
- create a global autosave timer/frontier;
- create an automatic retry loop;
- create a worker/scheduler/heartbeat/polling requirement;
- create an exact wall-clock trigger or universal retry count.

## LAW WP25-29 — Advisory host/context pressure cannot alone establish a gameplay-affecting DANGER fence

Approximate token/message/chat-age/context-pressure/capacity evidence remains advisory.

It may request conservative proactive preservation and contribute to exposure-risk assessment, but cannot by itself establish currentness, corruption, authorization, exact remaining capacity or a gameplay-affecting DANGER fence.

A gameplay-affecting DANGER guard additionally requires owner-valid still-relevant unpublished-state/loss-exposure evidence for the affected durability scope.

Exact thresholds/calibration remain realization and real-target empirical acceptance work under R2.6/WP-22/WP-24.

---

# 10. Retry / recovery semantics

WP-25 defines a common descriptor of lawful follow-up, not a retry engine.

A realization must be able to represent, equivalently:

```text
whether retry is currently lawful
what must change/revalidate before retry
which accepted identities/evidence must survive
transport/reassembly retry vs semantic execution
whether native current authority must be repinned/reloaded
whether external user/owner action is required
unsupported rather than retryable disposition
owner-bounded exhaustion outcome/route
```

## LAW WP25-30 — Native retry semantics control

The disposition never grants a retry the native owner forbids.

## LAW WP25-31 — Indeterminate authority change is never blind-retried

First perform owner-supported bounded current authority/lineage/current-closure verification. Until resolved, dependent success acknowledgement/release remains unavailable.

## LAW WP25-32 — Proven-disjoint transport rebuild does not replay semantics

Where the owner proves movement disjoint and permits transport-only rebuild, preserve accepted semantic result, stable IDs and fixed RNG while rebasing only transport/current-source basis.

## LAW WP25-33 — Relevant overlap uses native-owner reconciliation only

No generic YAML/JSON/text merge, last-writer-wins, Git order or arrival order may reconcile semantic overlap unless the native owner already defines a deterministic safe relation.

## LAW WP25-34 — Retry/recovery/reassembly is finite

Every retry/recovery/reassembly loop terminates under an owner-defined or implementation-bounded condition admitted by that owner. WP-25 defines no universal count.

Exhaustion exposes the native unresolved/blocked/unsupported result and derives the current focus disposition from it.

---

# 11. Accepted mechanics / RNG / causal identity

## LAW WP25-35 — Accepted mechanics/RNG are never replayed for downstream repair

Persistence, publication, local adoption, Context, presentation, Story, diagnostics or transport failure after accepted mechanics does not authorize reroll, re-resolution, reallocation or replacement accepted IDs.

The `MECHANICS_INTEGRITY.md` correction path for narration produced **without any valid accepted mechanics** remains a separate pre-acceptance correction case. It does not weaken accepted-work continuity.

## LAW WP25-36 — Failure-handler failure preserves accepted causal bases

A new failure encountered while repairing/recovering creates another owner-local condition for a new bounded focus. It does not erase prior accepted mechanics/RNG/publication/identity evidence or gain privileged retry authority.

---

# 12. Ruleset identity / catalog / deterministic execution

## LAW WP25-37 — Exact accepted ruleset identity cannot be substituted

Accepted Resolution/Continuation interpretation remains bound to its exact typed ruleset-set/catalog context.

If that exact dependency cannot be reconstructed, recovery terminates finitely according to current identity/recovery/compatibility owners. No fuzzy current-package interpretation, hidden migration or mixed partial context is allowed.

## LAW WP25-38 — Ruleset reconstruction reasons remain native evidence

Preserve the current closed reason set where material:

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

A common `failure.catalog_context_incompatible` route cannot erase a reason required for recovery/diagnosis/proof.

## LAW WP25-39 — Native rules/capability/compiler/gameplay distinctions do not collapse

```text
ruleset reconstruction failure
!= catalog-context incompatibility reason
!= catalog search miss
!= proven capability gap
!= dormant/nonselectable/quarantined capability
!= compiler/primitive rejection
!= House-Rule policy conflict
!= policy realization gap
!= adjudication missing/unauthorized/invalid/stale input
!= ordinary failed gameplay action/check/save
```

A normal resolved failed check/save/attack outcome is gameplay semantics, not system failure merely because the result is failure-shaped in natural language.

---

# 13. Compatibility / migration / unsupported

## LAW WP25-40 — Compatibility classification remains WP-20-owned

WP-25 consumes but does not rewrite:

```text
DIRECT_COMPATIBLE
MAINTENANCE_REFRESH
MIGRATION_REQUIRED
UNSUPPORTED_INCOMPATIBLE
INDETERMINATE
```

Version equality, generation equality, source ancestry, package revision/order, successful parsing or standalone load success cannot manufacture compatibility.

## LAW WP25-41 — Historical same-version/ancestry amendment is not current compatibility authority

`DEV/docs/superpowers/specs/2026-08-18-runtime-selection-and-storage-baseline-amendment.md` is:

```text
HISTORICAL / PARTIALLY SUPERSEDED DESIGN AMENDMENT / PROVENANCE
```

Its storage-baseline / three-runtime-identity semantic portions apply only where incorporated by later current owners.

Current compatibility authority is the 2026-09-05 versioning namespace/compatibility policy plus final WP-20.

## LAW WP25-42 — UNSUPPORTED is orthogonal to severity and generic failure-family shorthand

Native support/capability/profile/compatibility disposition remains first-class and orthogonal to S0–S4.

WP-25 does not require every unsupported state to become a generic system-failure family/record.

Examples:

```text
optional unsupported facility requested
    -> normally local S2 + FEATURE_UNAVAILABLE

required deployment profile unsupported
    -> S4 + DEPLOYMENT_PROFILE_UNSUPPORTED
```

No unsupported result authorizes alternate transport, hidden downgrade, guessed compatibility or substitution.

---

# 14. Authorization / disclosure / maintenance

## LAW WP25-43 — Authorization denial is operation-scoped

Denied application authority blocks that operation. Repository permission or error-handler privilege never widens HDM application authority.

Attempting to bypass authorization/currentness/disclosure constitutional law is R4 regardless of the original operation's severity.

## LAW WP25-44 — Authorization does not grant disclosure

An operation may be authorized while requested output contains recipient-ineligible material. Withhold/redact/partial-safe-output semantics remain owned by the disclosure boundary.

## LAW WP25-45 — Maintenance labels remain semantic categories

`NOT_AUTHORIZED`, `NOT_CURRENT_OR_UNRESOLVED`, `WITHHELD_OR_REDACTED`, `UNAVAILABLE_NOT_REALIZED` are semantic outcomes/categories, not frozen future machine enum spellings.

## LAW WP25-46 — User-visible failure projection grants no disclosure authority

A generated explanation is recipient-safe presentation only. It grants no eligibility and does not independently advance `runtime.disclosure`.

Any real emission/disclosure consequence follows the existing Step-5.12/R2.6 emission and recipient contract.

## LAW WP25-47 — Failure handling creates no fictional delay/action

Maintenance/recovery/diagnostic/tool failure does not create turns, fictional elapsed time, NPC behavior, player consent/pass/speech, resource spend or other canonical consequence merely to explain technical work.

---

# 15. Collaboration / ordinary waiting / agency

## LAW WP25-48 — Ordinary waiting is not system failure

```text
ordinary waiting/silence != failure
```

Only a positive owner-proven still-open human dependency may block its dependent focus.

Absence never synthesizes pass, consent, voluntary action, speech or immunity.

Late/stale collaboration input cannot replay already accepted mechanics or mutate a successor generation automatically.

---

# 16. READY_PC / bootstrap / storage / save-exit

## LAW WP25-49 — Local mechanical availability, READY_PC and compilation remain separate

```text
provisional play with sufficient local dependencies
!= attempted mechanic blocked by missing exact dependency
!= READY_PC not yet satisfied
!= package compilation fail-closed
```

A missing dependency blocks only the dependent mechanic unless a broader focus proves it required.

## LAW WP25-50 — Creation failure creates no partial campaign authority

Generator/scaffold/initial-publication failure cannot be repaired by LLM scaffold reconstruction, per-file fallback or setup against prepared/unpublished partial scaffold.

## LAW WP25-51 — Storage baseline is NEW-only

`DND_STORAGE.engine.baseline` is storage-owner-approved runtime identity for NEW campaigns only.

Existing campaign runtime comes from `MANIFEST.engine.current`.

Storage-owner authority, campaign creator authority and gameplay publication authority remain separate.

A broken storage baseline may be irrelevant to an existing-campaign focus and material to New Game.

## LAW WP25-52 — Failed/indeterminate save-and-exit does not pretend durable closure

Save-and-exit clears selected gameplay context only after the native save/durability promise is confirmed.

Rejected/indeterminate publication preserves the strongest truthful recovery-safe selected-campaign context allowed by the native owner until the outcome/recovery is resolved.

---

# 17. Story / planning / diagnostics / checkpoint nonauthority

## LAW WP25-53 — Derived service failure never replaces native truth

Story/planning/index/checkpoint/cache/diagnostic failure or lag cannot reconstruct, override or invalidate usable native truth merely because the projection is missing/stale.

## LAW WP25-54 — Optional Story/planning failure does not block sufficient native gameplay

Where the current focus has sufficient native sources, Story/planning unavailability is quality/operability degradation only.

Planning incompatibility causes omission/revalidation/recompute under its native owner; canon never changes to restore a plan.

## LAW WP25-55 — Diagnostic indeterminacy remains a diagnostic limitation

A diagnostic projection unable to prove a cross-owner conclusion reports indeterminate/limited evidence. It does not manufacture a universal currentness snapshot or authorization token.

Checkpoint/session/ambient context remain evidence/projections and cannot become truthful-basis authority.

---

# 18. Presentation and user-visible disposition

## LAW WP25-56 — User visibility is derived independently

Severity does not directly prescribe message verbosity.

Baseline goals:

- routine successful persistence/recovery: invisible;
- optional/internal degradation: silent unless material to current request;
- requested operation blocked: concise truthful explanation;
- external action required: concise actionable requirement;
- material DANGER guard affecting requested state growth: concise preservation/guard explanation;
- recipient-ineligible detail: withhold/redact;
- internal Connector/tool detail: not player-facing truth by default.

Exact UX text remains downstream work.

## LAW WP25-57 — Presentation repair is not a new fictional event

Re-presenting already-established state does not create another event/action/mechanical resolution. Host Retry/regeneration never means gameplay replay.

---

# 19. Cascading failure semantics

## LAW WP25-58 — Failure during failure handling is another native condition

Error/recovery paths gain no privileged semantics. New failures are evaluated through another bounded focus while preserving prior accepted bases.

## LAW WP25-59 — Independent failures remain independent

Do not create one aggregate worst state unless the concrete requested focus actually depends on all contributors.

A diagnostic/UI summary may list multiple current dispositions only as non-authoritative projection.

## LAW WP25-60 — Authority movement invalidates only affected attempt basis

If current authority moves during recovery/publication/diagnostics, re-pin/revalidate the affected bounded footprint. Do not widen to campaign/history/global scans.

## LAW WP25-61 — Partial technical freeze is not partial fiction

Multi-source prerequisite closure may leave sources technically frozen while the intended cross-scope semantic result remains unestablished. Preserve that distinction.

---

# 20. Absolute prohibited fallbacks

No WP-25 path authorizes:

- guessing missing required evidence;
- silent semantic/currentness/authorization owner substitution;
- chat/model memory as campaign authority;
- replay/reroll/reallocation of accepted mechanics/RNG/IDs;
- blind retry of ambiguous authority-changing publication;
- force push, ref rewind or branch/ref deletion;
- alternate prohibited repository transport;
- Git/LWW/arrival order as fictional authority;
- invention of voluntary player action/consent/pass/speech;
- disclosure promotion from physical visibility;
- Story/planning/checkpoint/index/cache/diagnostics as canon substitute;
- ordinary unbounded WORLD/history/all-ref/all-LIVE scanning;
- infinite retry/reassembly loops;
- hidden background correctness worker/heartbeat;
- generic compatibility inference from version/order/ancestry;
- generic rollback/rewind failure handler;
- global unsupported flag;
- session/campaign global health state used as continuation authority.

---

# 21. Conceptual deterministic evaluation procedure

A future authorized realization may implement an equivalent pure/bounded evaluator:

```text
1. identify concrete focus boundary
2. obtain owner-proven bounded required closure
3. collect current native outcomes/conditions from that closure
4. if closure completeness is unresolved, preserve native unresolved result
5. discard unrelated conditions
6. preserve native outcomes/reasons and all still-applicable accepted truthful bases
7. derive affected scope(s)
8. derive gameplay impact
9. derive effective severity S0..S4
10. derive risk-if-ignored R0..R4
11. derive native semantic tolerance/fence
12. derive non-authoritative continuation classification
13. attach owner-native retry/recovery descriptor
14. attach orthogonal support/compatibility disposition when applicable
15. derive recipient-safe user-facing disposition
16. attach future proof obligations
17. emit ephemeral FailureDisposition
```

The evaluator does not discover the world, authorize operations or execute retries.

---

# 22. Verification / realization / empirical proof contract

The following remain independent:

```text
ARCHITECTURE COVERAGE
MACHINE REALIZATION
VERIFICATION REALIZATION
EMPIRICAL ACCEPTANCE
```

## LAW WP25-62 — Future verification must cover polarity and cascades

When realization is authorized, coverage must include as applicable:

```text
positive path
negative / denied path
failure path
indeterminate / ambiguous path
partial native success
recovery path
retry exhaustion
scope isolation
risk escalation
unsupported capability/profile
user-visible behavior
closure-completeness failure
post-accepted-success downstream failure
DANGER bounded-attempt/no-scheduler behavior
```

## LAW WP25-63 — Host-risk calibration is empirical where material

Exact long-chat/context-pressure/DANGER heuristics, false-positive/false-negative behavior and material user-visible host behavior require the real implemented supported target where deterministic proof is insufficient.

No preimplementation surrogate establishes production-like acceptance.

Green source CI proves only the checks it actually executes on the exact head.

---

# 23. Current realization/debt map after final-Senior bounded recovery

Mandatory independent final Senior review identified three significant closure defects in then-current realization/traceability, with no canonical architecture reopen and no human decision required. The bounded recovery synchronizes only those mechanically implied surfaces.

## SR25-FINAL-01 — retired fixed-time durability realization

Worker status: **REPAIRED / FINAL SENIOR RE-REVIEW PENDING**.

Current active/current surfaces synchronized include:

```text
GAME/CORE/DURABILITY_GUARD.md
GAME/CORE/SESSION.md
GAME/CORE/STORAGE.md
GAME/CORE/RUNTIME.md
GAME/CORE/PERSISTENCE.md
GAME/CORE/CAMPAIGN_SETUP.md
DEV/RELEASE/CHECKLIST.md
DEV/TESTS/test_durability_risk_contract.py
DEV/TESTS/DURABILITY_BOUNDARY_CASES.md
DEV/TESTS/test_multi_runtime_release_consistency.py
```

The prior exact fixed-time forced/HARD/autosave realization and `durable_frontier_time`-only state are no longer current runtime authority. Current realization now reflects only the already-settled `NORMAL / ELEVATED / DANGER` loss-protection trajectory needed for internal consistency:

```text
DANGER -> one owner-valid bounded preservation/recovery attempt
          before another operation materially enlarges the same exposed dirty scope
failure/unavailability -> guard that state-growing operation in affected scope
DANGER != correctness HARD
no exact wall-clock replacement
no exact token/message/context thresholds
no background scheduler/worker/heartbeat/polling
no automatic retry loop
advisory host/context pressure alone != gameplay-affecting DANGER
clean state -> no heartbeat/no-op persistence
```

Stronger owner-defined HARD edges remain unchanged. Historical occurrences of the old fixed-time policy remain only as provenance, supersession/negative evidence or historical design state where retention is appropriate.

## SR25-FINAL-02 — mechanics replay boundary

Worker status: **REPAIRED / FINAL SENIOR RE-REVIEW PENDING**.

`GAME/CORE/MECHANICS_INTEGRITY.md`, `DEV/TESTS/MECHANICS_INTEGRITY_CASES.md` and `DEV/TESTS/test_mechanics_replay_boundary_contract.py` now distinguish:

```text
genuinely mechanically unsupported pre-acceptance narration
AND no valid accepted mechanics/RNG consequence ever existed
    -> honest re-resolution may use fresh legitimate RNG

accepted mechanics/RNG/IDs/semantic consequence exists
AND downstream trace/persistence/publication/presentation/Context/diagnostic/recovery evidence fails
    -> preserve accepted mechanics/RNG/IDs/consequences
    -> NO replay / reroll / reallocation
```

Missing/corrupt/unavailable resolution trace alone does not prove that accepted mechanics never existed.

## SR25-FINAL-03 — routing / traceability

Worker status: **REPAIRED / FINAL SENIOR RE-REVIEW PENDING**.

```text
DEV/PROJECT_MAP.md: REQUIRED / UPDATED
DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md: REQUIRED / UPDATED
Step-7 propagation ledger: UPDATED WITH POST-STEP-8 SENIOR RECOVERY ACCOUNTING
Step-8 canonicalization checkpoint: UPDATED / ORIGINAL NO-EDIT DISPOSITION CORRECTED
DEV/CURRENT_PROGRESS.md: UPDATED / FINAL RE-REVIEW GATE
DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md: NO EDIT REQUIRED
```

Project Map/index remain derivative routing surfaces and do not duplicate native owner law.

## Remaining deferred obligations

The following remain deferred and are not authorized by this recovery:

```text
focus-scoped FailureDisposition evaluator/adapters
exact common FailureDisposition machine type/enum representation
new persisted failure schema/registry
global health state / generic ACL or operation registry
universal retry engine
installed maintenance command realization
exact DANGER / host-risk thresholds and host-capacity estimator
real-target DANGER calibration / empirical acceptance
broad cross-owner failure/cascade/scope-isolation machine realization beyond focused Senior repairs
WP-26
implementation plan
release execution
gameplay bootstrap
```

Architecture coverage, focused mechanical synchronization, verification realization and empirical acceptance remain separate proof classes.

---

# 24. Version impact — final-Senior recovery

The original Steps 2–8 architecture/design/status publication was document-only and correctly carried `VERSION_IMPACT: NONE` at that time. The later bounded final-Senior recovery materially changes version-bearing CORE/runtime modules, so a fresh gate applies.

Current engine semantic version remains `1.0-alpha`.

Under current Category-B component law, materially changed version-bearing modules use engine prefix `1.0` and increment component-local revision exactly once:

```text
GAME/CORE/DURABILITY_GUARD.md      1.0.1 -> 1.0.2
GAME/CORE/SESSION.md               0.4.0 -> 1.0.1
GAME/CORE/STORAGE.md               0.7.0 -> 1.0.1
GAME/CORE/RUNTIME.md               0.8.0 -> 1.0.1
GAME/CORE/PERSISTENCE.md           1.0.2 -> 1.0.3
GAME/CORE/CAMPAIGN_SETUP.md        0.8.1 -> 1.0.2
GAME/CORE/MECHANICS_INTEGRITY.md   0.1.0 -> 1.0.1
```

```text
VERSION_IMPACT: CATEGORY_B_MODULE_REVISIONS
VERSION_BUMP_REQUIRED: YES — COMPONENT-LOCAL framework_module_version ONLY
ENGINE_VERSION_BUMP_REQUIRED: NO
PERSISTENT_SCHEMA_OR_GENERATION_BUMP_REQUIRED: NO
MIGRATION_REQUIRED_BY_THIS_RECOVERY: NO
RELEASE_EXECUTION_REQUIRED: NO
VERSIONING_TAXONOMY_REOPENED: NO
```

No `GAME/ENGINE_VERSION.yaml`, campaign/storage/catalog/ruleset generation, persistent protocol shape, migration law or release format is changed by this bounded recovery.

---

# 25. Final worker disposition after bounded recovery

```text
SELECTED_ARCHITECTURE:
    FOCUS-SCOPED EPHEMERAL FAILURE DISPOSITION
    + OWNER-LOCAL NATIVE OUTCOMES
    + SCOPE-AWARE CONTINUATION
    + RISK-TRAJECTORY-AWARE DURABILITY PROTECTION

PERSISTED_GLOBAL_ERROR_AUTHORITY: NO
GLOBAL_HEALTH_STATE: NO
UNIVERSAL_RETRY_ENGINE: NO
GENERIC_WP25_ACL: NO
CAMPAIGN_WIDE_ERROR_LIFECYCLE: NO
BACKGROUND_FAILURE_MONITOR: NO

STEP6_BLOCKING_FOUND: 0
STEP6_SIGNIFICANT_FOUND: 6
STEP6_MINOR_FOUND: 3
STEP7_UNRESOLVED_BLOCKING: 0
STEP7_UNRESOLVED_SIGNIFICANT: 0
STEP7_UNRESOLVED_MINOR: 0
FINDING_PROPAGATION_SWEEP_COMPLETE: YES

FINAL_SENIOR_REVIEW_BASELINE: f3c2c978cd150dbc1be510def34d14fe61067c7c
FINAL_SENIOR_VERDICT: HOLD — BOUNDED FINAL-CLOSURE RECOVERY REQUIRED
FINAL_SENIOR_UNRESOLVED_BLOCKING: 0
FINAL_SENIOR_UNRESOLVED_SIGNIFICANT: 3

SR25_FINAL_01: REPAIRED AT WORKER LEVEL / RE-REVIEW PENDING
SR25_FINAL_02: REPAIRED AT WORKER LEVEL / RE-REVIEW PENDING
SR25_FINAL_03: REPAIRED AT WORKER LEVEL / RE-REVIEW PENDING
UNRESOLVED_BLOCKING_AT_WORKER_RECOVERY: 0
UNRESOLVED_SIGNIFICANT_AT_WORKER_RECOVERY: 0

HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
NEEDS_PO: NONE
CANONICAL_WP25_ARCHITECTURE_REOPEN_REQUIRED: NO
WHOLESALE_UPSTREAM_REOPEN_REQUIRED: NO

WP25_STEPS_2_8_COMPLETE_AT_WORKER_LEVEL: YES
WP25_FINAL_SENIOR_HOLD_RECOVERY: COMPLETE AT WORKER LEVEL
WP25_FINAL_SENIOR_RE_REVIEW: REQUIRED / PENDING
WP25_CLOSED: NO
IMPLEMENTATION_PLANNING_AUTHORIZED: NO
NEXT_WP_AUTHORIZED: NO
NEXT_AUTHORIZED_UNIT: NONE
```

Next mandatory gate: **independent WP-25 final Senior re-review**.