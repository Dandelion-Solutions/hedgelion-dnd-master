# R2.7 WP-25 Step 2 — Evidence / Research Reconciliation

Status: **STEP 2 COMPLETE — EVIDENCE RECONCILED / NO HUMAN DECISION REQUIRED**

Date: 2026-09-08

Starting authoritative checkpoint: `310bbf0e13d6d1900870b4e5f533c50b217d9a80`

Scope: WP-25 error / degradation / failure semantics only. This is design/evidence provenance, not the final canonical owner and not implementation authorization.

## 1. Method

Step 2 re-read current semantic owners and task-material consumers rather than treating the Step-1 question list as exhaustive. Evidence was reconciled by semantic responsibility:

```text
durability / publication / recovery
context / host / instruction basis
authorization / LIVE / collaboration / disclosure
ruleset identity / catalog / deterministic mechanics / compatibility
bootstrap / READY_PC / storage / save-exit
Story / planning / diagnostics / cleanup
performance / boundedness / verification proof classes
accepted mechanics / RNG / presentation repair
```

For each route the analysis preserved:

```text
native owner + native outcome/reason
currentness / authority / evidence basis
surviving truthful native basis
actual dependent scope
legal continuation
owner-defined semantic fence
native retry/recovery/idempotency constraints
forbidden fallbacks
recipient-safe visibility
proof class / realization state
```

No external research is required to choose the architecture semantics in this step: the current owners and accepted Product Owner direction already determine them. Host-capacity thresholds and production behavior remain intentionally empirical/deferred under R2.6/WP-22/WP-24 and therefore cannot be manufactured by desk research.

## 2. Source Manifest expansion / source-role reconciliation

The Step-1 manifest remains applicable with the mandatory post-Senior correction. Step 2 adds or elevates the following task-material sources in the synthesis graph:

| Source | Current role in WP-25 | Material evidence extracted |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-08-hdm-wp25-failure-degradation-durability-risk-owner-direction.md` | accepted PO/architecture direction, not native owner replacement | axes, S0–S4, R0–R4, semantic tolerances, gameplay-impact vocabulary, NORMAL/ELEVATED/DANGER, user-facing/default proof obligations |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md` | current durability semantic owner | ESTABLISHED/DURABLE/obligation independence, scope-owned durability, partial native success, failed SAVE continuation, risk-control != HARD |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md` | current implementation-facing publication owner | native result classes, tri-state ref epistemics, immutable attempt, bounded retry, semantic conflict footprint, partial success/current composition |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md` | current recovery owner | current-native-source-first recovery, READY/RETRY/BLOCKED, no replay, checkpoint/session nonauthority |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md` | integrated recovery/concurrency owner | domain-composed source basis, partial technical freeze != partial fiction, Story/presentation failure isolation, accepted mechanics continuity |
| `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md` | current Context Runtime owner | ASSEMBLED/ASSEMBLED_DEGRADED/UNSATISFIABLE, requiredness/task ownership, bounded non-looping fallback |
| `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md` | supported-host assurance owner | no exact hidden-capacity authority, profile restriction/unsupported route, later real-target empirical acceptance |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md` | current multiplayer/LIVE owner | domain-separated currentness, bounded claim-specific authority, accepted/rejected/indeterminate CAS, post-CAS local-adoption recovery |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-canonical-spec.md` | current collaboration/agency owner | positive dependency before waiting barrier, minimal required set, silence != consent, generation-local currentness |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` | current delivery/disclosure owner | EMISSION_COMMIT, presentation interruption limitation, recipient scope, presentation repair != new fiction |
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | current authorization owner | repository permission != application authority; creator/storage/player/policy authority separation; fail closed |
| `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` | canonical ruleset exact-identity owner | exact set identity, accepted-work binding, finite reconstruction failure, no fuzzy/current substitution |
| `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md` | current version/compatibility policy | equality/order/ancestry not compatibility proof; explicit directed migration; exact identity independent |
| `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md` | current released compatibility/migration owner | DIRECT_COMPATIBLE/MAINTENANCE_REFRESH/MIGRATION_REQUIRED/UNSUPPORTED_INCOMPATIBLE/INDETERMINATE; explicit ancestry supersession; partial authority outcomes |
| `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md` | canonical READY_PC/character seed owner | provisional local sufficiency, READY_PC closure, exact package compilation failures, absent/nonselectable capability |
| `GAME/CORE/STORAGE.md` | current storage/bootstrap owner with stale durability projection | NEW-only storage baseline; campaign/current runtime separation; owner separation; one-hour wording is stale debt |
| `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` | current DEV maintenance semantic proposal, runtime surface not realized | semantic outcome categories, auth/disclosure/currentness composition, no fictional mutation |
| `DEV/docs/superpowers/specs/2026-09-07-r2-7-WP-21-diagnostics-observability-cleanup-retirement-canonical-spec.md` | current diagnostics/cleanup owner | owner-qualified diagnostics, evidence classes, indeterminate reporting, uncertain cleanup retains, no global observability/GC authority |
| `DEV/docs/superpowers/specs/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-canonical-spec.md` | current Story/planning owner | Story lag/nonavailability cannot become canon/currentness failure; planning invalidates/recomputes under native owners |
| `DEV/docs/superpowers/specs/2026-09-07-r2-7-WP-22-verification-test-evaluation-completeness-canonical-spec.md` | current proof-completeness owner | architecture vs machine vs verification vs empirical separation; polarity coverage; stale tests never reactivate semantics |
| `DEV/docs/superpowers/specs/2026-09-08-r2-7-WP-24-performance-scale-operational-budget-canonical-spec.md` | current boundedness/performance owner | finite operation scope, no global scan, bounded retry without universal count, real-target proof classes |
| `GAME/CORE/MECHANICS_INTEGRITY.md` + `GAME/CORE/RANDOMNESS.md` | runtime mechanics/RNG consumers | mechanics must exist before narration; no fake RNG; accepted RNG never silently rerolled; unsupported pre-resolution narration correction remains distinct from downstream replay |

### Historical / partially superseded source role retained

`DEV/docs/superpowers/specs/2026-08-18-runtime-selection-and-storage-baseline-amendment.md` remains:

```text
HISTORICAL / PARTIALLY SUPERSEDED DESIGN AMENDMENT / PROVENANCE

current only for semantic portions incorporated by later owners;
not current compatibility authority
```

Its storage-baseline / three-runtime-identity semantics are used only through their later current owners. Its old same-version/ancestry compatibility inference is explicitly superseded by the current versioning policy and WP-20.

## 3. Evidence conclusion: composition is operation/use-boundary local

A single campaign-wide failure status is incompatible with current owners.

Evidence:

- Step-5.5 durability policy is scope/partition-owned and explicitly rejects one global dirty clock/frontier;
- WP-13 SAVE may have partial native success while only the unresolved dependent scope remains gated;
- WP-14 recovery is one bounded requested recovery closure, not a universal RecoveryCut;
- Context Runtime `UNSATISFIABLE` is terminal only for the current assembly attempt;
- WP-16 campaign currentness, LIVE currentness and local HOT currentness are independent domains;
- WP-17 collection barriers apply only to positive bounded human dependencies;
- Step-5.12 disclosure is recipient-scoped while accepted gameplay may remain established after presentation interruption;
- READY_PC permits unrelated provisional play when a local mechanic is not ready;
- WP-21 diagnostics are question-scoped and owner-qualified;
- WP-18 Story/planning failure is noncanonical and cannot globally block gameplay;
- WP-24 forbids correctness fallback to whole-campaign/global scans.

Therefore the cross-owner integration view must be derived for one **focus operation/use boundary** (or another explicitly bounded decision scope) from only the native conditions that can affect that focus.

Conceptually:

```text
FailureDispositionEvaluation(
    focus_operation_or_use,
    bounded_dependency_scope,
    current_native_conditions[]
)
    -> ephemeral disposition
```

Independent conditions may produce independent dispositions. They combine only when the current focus's actual dependency closure requires them to combine.

This is not a new semantic owner, health state, campaign lifecycle, scheduler or persisted registry.

## 4. Truthful frontier is owner-qualified, not one scalar

The PO direction's `truthful_frontier` requirement cannot mean one global revision/frontier because current architecture explicitly rejects such a value across campaign/LIVE/local/Story/checkpoint domains.

The required semantic content is instead an owner-qualified surviving basis:

```text
truthful_basis[] =
    native owner / domain
    exact accepted/current evidence relevant to the focus
    what remains established / current / usable
    what remains unresolved / cannot be relied upon
```

Examples:

- partial SAVE: confirmed native-domain publication remains real while overall SAVE is incomplete;
- confirmed LIVE CAS + local adoption failure: remote accepted semantics remain authoritative while local HOT must reload;
- post-EMISSION interruption: accepted gameplay and emission-committed disclosure remain established, exact visible prefix is not knowable;
- Story publication failure: native campaign state remains usable; unpublished Story candidate is not retained basis;
- migration preparation failure: current old campaign authority remains current; prepared target tree is non-authoritative.

No common timestamp, HEAD, generation, checkpoint or Story cursor may replace these owner-qualified bases.

## 5. Native outcome preservation

WP-25 may classify effects but must preserve source semantics verbatim enough for lawful follow-up.

### 5.1 Publication / currentness

Preserve at least:

```text
CONFIRMED_ACCEPTED
CONFIRMED_REJECTED
INDETERMINATE

plus dispatch/cause distinctions where applicable:
NO_WRITE_NEEDED
FAILED_PREPUBLICATION
REVALIDATION_REQUIRED
CAPABILITY_FAILURE
AUTHORIZATION_FAILURE
CONFIGURATION_FAILURE
INFRASTRUCTURE_FAILURE
```

`INDETERMINATE` cannot be converted to failure/rejection merely to choose a retry. Confirmed rejection must be classified before retry. Partial accepted native results remain real.

### 5.2 Recovery

Preserve `READY | RETRY | BLOCKED` and the native reason/basis. `RETRY` is not a global retry permission; `BLOCKED` may be dependent-scope only.

### 5.3 Context

Preserve `ASSEMBLED | ASSEMBLED_DEGRADED | UNSATISFIABLE`.

`ASSEMBLED_DEGRADED` has all required semantics and therefore normally affects quality, not correctness. `UNSATISFIABLE` forbids blind re-run of the same impossible assembly.

### 5.4 Compatibility

Preserve exactly:

```text
DIRECT_COMPATIBLE
MAINTENANCE_REFRESH
MIGRATION_REQUIRED
UNSUPPORTED_INCOMPATIBLE
INDETERMINATE
```

Successful parsing, equal version/generation, source ancestry and standalone load success do not establish direct compatibility.

### 5.5 Ruleset/canonical mechanics

Preserve native package/load/reconstruction reasons, including:

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

They may route through `failure.catalog_context_incompatible`, but must not collapse into capability gap, dormant capability, compiler failure or gameplay failure.

### 5.6 READY_PC / capability / compilation

Preserve:

```text
local mechanic has sufficient exact dependencies
local requested mechanic lacks an exact dependency
READY_PC not yet satisfied
unsupported content ABSENT_NONSELECTABLE
package compilation fail-closed
```

### 5.7 Maintenance

`NOT_AUTHORIZED`, `NOT_CURRENT_OR_UNRESOLVED`, `WITHHELD_OR_REDACTED`, `UNAVAILABLE_NOT_REALIZED` are semantic outcome categories, not fixed runtime enum spellings.

### 5.8 Diagnostics / Story / presentation

Diagnostic states such as `UNAVAILABLE`, `WITHHELD_OR_REDACTED`, `STALE_OR_INDETERMINATE`, and Story/planning usability/lag remain non-authoritative projections. Presentation interruption does not become gameplay rollback.

## 6. Effective severity derivation

The accepted severity vocabulary is retained:

```text
S0 NOTICE
S1 DEGRADED
S2 GUARDED
S3 QUARANTINED
S4 CRITICAL
```

Severity is derived for the current focus, never stored on a failure code.

### S0 NOTICE

Use when the condition changes no correctness, required capability or material current operation. Examples: non-authoritative residue; an irrelevant invalid optional projection; a NEW-only storage baseline issue while resuming an existing campaign whose `MANIFEST.engine.current` is healthy.

### S1 DEGRADED

Use when required correctness/authority/agency/canon remain satisfied but quality, convenience, optional projection or resilience is reduced. Examples: `ASSEMBLED_DEGRADED`; Story lag when native sources satisfy the current use; presentation-only repair; ELEVATED durability exposure before a state-growing fence is required.

### S2 GUARDED

Use when the requested operation/capability cannot honestly/lawfully complete now, but trustworthy independent gameplay/use remains available. Examples: one missing READY_PC dependency for an attempted mechanic; unavailable optional maintenance command; confirmed authorization denial for one operation; unsupported optional feature.

### S3 QUARANTINED

Use when integrity/currentness/authority of the affected dependency scope cannot be proven sufficiently for dependent use. Examples: LIVE source ambiguity for claimed owners; indeterminate authority-changing publication whose result affects a required current basis; accepted-work ruleset context cannot currently be reconstructed for that open work while unrelated owners remain usable.

### S4 CRITICAL

Use only when the required campaign/runtime/deployment gameplay contract has no safe basis at the scope needed to resume. Examples: the required baseline runtime/profile is unsupported or unavailable and no legal supported recovery exists; campaign resume requires unreconstructable current native authority with no independent safe continuation.

### Severity composition law

There is no campaign-wide `max(severity)`.

For one focus operation, derive the **minimum restrictive class sufficient to preserve every applicable native invariant** after filtering to the actual dependency closure. If several applicable contributors require different guards, the focus disposition must enforce the most restrictive guard needed for that focus, while retaining each native reason. This does not promote unrelated scopes.

## 7. Gameplay impact and affected scope

Accepted gameplay-impact vocabulary remains at least:

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

Affected scope is a typed set/association, not a total hierarchy. Candidate scope classes remain:

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

A physical record size/location does not determine semantic blast radius. Blast radius follows actual dependencies/current authority.

## 8. Risk-if-ignored derivation

Accepted risk vocabulary remains:

```text
R0 NONE
R1 QUALITY_OR_OPERABILITY_DEBT
R2 ACCUMULATING_LOSS_OR_PROGRESS_RISK
R3 CANON_CURRENTNESS_AGENCY_OR_AUTHORITY_RISK
R4 DISCLOSURE_SECURITY_OR_CONSTITUTIONAL_RISK
```

Like severity, risk is evaluated only for the focus/affected scope. There is no campaign-global highest-risk flag.

Where several risks apply to the same focus, expose the highest applicable risk class needed to constrain that focus while retaining the contributing native reasons. Risks in independent scopes do not promote one another.

Examples:

- Story lag with usable native source: R1;
- growing unpublished established HOT: R2;
- using stale LIVE/current rules basis: R3;
- bypassing authorization/disclosure eligibility or force/ref-delete constitutional rules: R4.

## 9. Temporal tolerance and semantic fences

Retain the accepted semantic classes:

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

Native owner-specific stronger fences always win for their dependency.

No generic seconds/turns/retry counts are introduced.

### 9.1 Durability risk trajectory

For each applicable durability-policy scope, preserve:

```text
NORMAL
ELEVATED
DANGER
```

This is operability/loss-protection state, not semantic validity.

- NORMAL: ordinary owner-permitted deferral.
- ELEVATED: at the next suitable safe established-state opportunity, proactive durability outranks optional Story/planning/enrichment.
- DANGER: before accepting another operation that materially enlarges the same exposed dirty semantic scope, attempt coherent durability/repair; if preservation cannot be obtained, guard that state-growing operation.

DANGER does not make current coherent HOT false, does not create a generic Step-5.5 HARD edge, and does not block operations proven not to enlarge/use the affected dirty scope.

Exact thresholds remain implementation/empirical work. Capacity/message/token/chat-age signals are advisory only.

## 10. Retry and recovery semantics

WP-25 needs a common **descriptor of lawful follow-up**, not a retry engine.

The descriptor must preserve at least:

```text
whether retry is currently allowed at all
what must change/revalidate before retry
which accepted identities/evidence must be preserved
whether the retry repeats transport/reassembly only versus semantic execution
whether current authority must be repinned/reloaded
whether external user/owner action is required
whether the condition is unsupported rather than retryable
owner-bounded exhaustion condition/result
```

Normative constraints:

1. ambiguous authority-changing publication: no blind retry; verify current authority first;
2. stale/disjoint publication base: transport-only rebuild may preserve accepted semantics where owner permits;
3. relevant overlap: owner-specific reconciliation/revalidation; no generic merge;
4. accepted mechanics/RNG/IDs: never replay/reroll/reallocate to repair downstream persistence/presentation/currentness;
5. accepted remote CAS/publication + local adoption failure: recover/reload local state from current native authority; do not retry the accepted semantic edge;
6. Context `UNSATISFIABLE`: caller chooses an admitted alternate path; no blind same-attempt loop;
7. unsupported compatibility/capability: no retry until support/evidence/profile changes;
8. authorization denial: no automatic retry until current authority/authorization changes;
9. finite ruleset reconstruction failure: no fuzzy/current-package substitution;
10. every retry/reassembly loop is bounded; exhaustion yields a typed unresolved owner result.

## 11. Accepted mechanics / RNG correction boundary

Two cases must remain separate:

```text
A. no valid accepted mechanics ever existed
   -> MECHANICS_INTEGRITY may correct unsupported narration from the last valid frontier
      using actual mechanics / legitimate fresh RNG as that owner allows

B. mechanics/RNG/semantic edge already accepted
   -> downstream failure/recovery/presentation/transport must preserve that accepted identity/evidence
   -> no replay/reroll merely to regenerate downstream work
```

WP-25 must not use the older correction rule for case A as permission to replay case B.

## 12. User-visible disposition

User-visible behavior is derived independently from severity.

Architecture requirements:

- routine successful recovery/persistence stays invisible;
- optional/internal degradation need not interrupt gameplay when no user action is required;
- player is told briefly when their requested operation is blocked, when loss exposure becomes materially actionable, or when external action is required;
- recipient-ineligible diagnostic detail is withheld/redacted even from an authorized operation;
- presentation repair may restate accepted state but not create a second fictional event;
- internal error detail/Connector traces are not promoted to player-facing truth;
- maintenance errors do not create fictional waiting/time/turns.

Exact UX strings and exact machine enum names remain downstream realization concerns.

## 13. Cascading / compound failure reconciliation

### 13.1 Partial native success

Confirmed native success remains real even when the aggregate operation fails. The disposition carries the surviving accepted basis and gates only unresolved dependent work.

### 13.2 Remote success / local adoption failure

Remote/current native authority wins. Local failure is recovery/reload work. Never roll back or repeat accepted remote semantics.

### 13.3 Authority movement during recovery

Invalidate the affected recovery attempt basis and repin current native authority. Do not reinterpret stale data or widen to a global scan.

### 13.4 Multiple independent failures

Create/evaluate separate focus dispositions unless the requested operation's real dependency closure joins them. Do not synthesize a campaign-global worst state.

### 13.5 Failure during failure handling

The new native failure is simply another owner-local condition contributing to a new bounded disposition. The error path does not gain privileged authority or unbounded retry rights.

### 13.6 Presentation after accepted semantics

Presentation interruption/Retry/regeneration repairs presentation only; accepted gameplay/disclosure semantics follow their native owner evidence and are not re-executed.

### 13.7 DANGER durability + publication failure

Coherent HOT remains truthful. Publication failure adds R2 loss exposure and may escalate effective guard for additional state-growing operations in the same durability scope. Independent/OOC/non-growing operations remain available when proven safe.

## 14. Unsupported disposition remains orthogonal

`UNSUPPORTED`/`UNSUPPORTED_INCOMPATIBLE` describes capability/profile/compatibility support, not severity.

Examples:

```text
optional unsupported maintenance facility
    -> FEATURE_UNAVAILABLE / normally local S2 when requested

required gameplay deployment profile unsupported
    -> DEPLOYMENT_PROFILE_UNSUPPORTED + S4 for resume under that profile

unsupported character option absent/nonselectable
    -> feature unavailable for that choice; does not make the campaign S4
```

No unsupported result authorizes alternate transport, downgrade, guessed compatibility or hidden substitution.

## 15. Proof reconciliation

WP-22/WP-24 require four independent proof dimensions:

```text
ARCHITECTURE COVERAGE
MACHINE REALIZATION
VERIFICATION REALIZATION
EMPIRICAL ACCEPTANCE
```

Current Step-2 architecture evidence does **not** prove a realized WP-25 integration helper/state machine because none is authorized/implemented by this work.

Future realization must map at least these polarities:

```text
positive path
negative / denied path
failure path
indeterminate / ambiguous path
partial success
recovery path
retry exhaustion
scope isolation
risk escalation
user-visible behavior
unsupported profile/capability
```

Deterministic machine tests are appropriate for realized derivation/currentness/retry guards. Scenario acceptance is appropriate for multi-owner cascades. Production-like empirical evaluation is required for host-capacity heuristics, long-context behavior and material user-visible/host failure behavior that deterministic tests cannot prove.

Green current CI proves only its actual current checks, including stale tests if they remain present; it does not make stale one-hour policy current architecture.

## 16. Stale / deferred realization classification

Current known realization debt materially relevant to WP-25 includes:

1. `GAME/CORE/DURABILITY_GUARD.md`, `GAME/CORE/SESSION.md`, `GAME/CORE/STORAGE.md` and `DEV/TESTS/test_hourly_durability_contract.py` still project the retired one-hour rule;
2. maintenance semantic categories have no installed runtime command realization;
3. portions of old runtime error/LIVE/presentation wording may predate current WP-13/WP-16/Step-5.12 laws;
4. `MECHANICS_INTEGRITY.md` correction wording applies to mechanically unsupported narration, not accepted-mechanics downstream replay; future realization/docs must preserve that distinction;
5. future WP-25 cross-owner composition machine/helper and verification coverage are not yet realized.

These are realization/debt mappings, not permission for Step 2 to edit runtime/schema/tests.

## 17. Architecture alternatives implied by evidence

Evidence leaves three meaningful implementation-facing architecture alternatives for Step 3:

### Alternative A — persisted/global failure state

One central failure/health record owns current failure status/severity/retry.

Evidence conflict: duplicates currentness/authority, falsely globalizes local failures, creates lifecycle/cleanup/migration/schema burdens and contradicts accepted PO direction.

### Alternative B — purely local owner outcomes with no integration projection

Every caller handles native results ad hoc.

Evidence conflict: cannot consistently derive gameplay impact, scope, durability-risk escalation, user-visible behavior or cross-owner cascading continuation.

### Alternative C — focus-scoped ephemeral disposition projection over owner-native conditions

Native outcomes remain authoritative. A bounded evaluator produces an ephemeral focus-specific integration view containing separated axes, legal continuation, native retry/recovery references and proof/user-disposition obligations.

Evidence fit: satisfies all current owner boundaries and accepted Product Owner direction without new persistent authority.

## 18. Step-2 conclusion

```text
STEP2_STATUS: COMPLETE
SOURCE_MANIFEST_REFINED: YES
CURRENT_COMPATIBILITY_SOURCE_ROLE_RECONCILED: YES
NEW_HUMAN_DECISION: NO
NEEDS_PO: NONE

EVIDENCE-PREFERRED_ARCHITECTURE:
    focus-scoped ephemeral failure disposition
    over owner-local native outcomes
    + scope-aware continuation
    + risk-trajectory-aware durability protection

REJECTED_BY_EVIDENCE:
    persisted/global error or health owner
    purely ad-hoc local-only handling without cross-owner integration projection
```

Step 3 may proceed automatically to the Decision Brief. No implementation planning or implementation is authorized.