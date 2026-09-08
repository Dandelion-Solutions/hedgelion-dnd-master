# R2.7 WP-25 Step 1 — Error / Degradation / Failure Semantics — Architecture Task Brief + Source Manifest

Status: **STEP 1 BOUNDED RECOVERY COMPLETE — SR25-S1-01..03 WORKER-REPAIRED / PENDING MANDATORY INDEPENDENT SENIOR STEP-1 RE-REVIEW**

Date: 2026-09-08

Reviewed baseline: `ec1b8602840acf0c28b38cf2ab24fb1d3feee557`

This artifact is design-process provenance for **R2.7 WP-25 Step 1 only**. It is not a canonical WP-25 specification, does not authorize Step 2, and does not replace native failure, authority, deterministic-rules, persistence, recovery, bootstrap, maintenance, compatibility, multiplayer, disclosure, Story or verification owners.

The mandatory independent Senior Step-1 review of the reviewed baseline returned **HOLD — bounded Step-1 recovery required** with 0 BLOCKING and 3 SIGNIFICANT findings (`SR25-S1-01..03`). This revision expands the open-world dependency graph, reruns the whole-project Step-1 critic, and applies only mechanically supported framing/source-manifest repairs. It does not self-declare Senior PASS.

## 1. Authorization and hard stop

Authorized recovery work is limited to:

```text
WP-25 Step 1 bounded recovery
    -> expand open-world Source Manifest for SR25-S1-01..03
    -> trace actual owners plus machine/schema/test consumers
    -> update failure horizon / cascading attacks / later research questions
    -> rerun mandatory whole-project Task-Brief critic on the full graph
    -> mechanically repair resolvable BLOCKING/SIGNIFICANT framing gaps
    -> publish/read back/exact-head verify
    -> STOP for independent Senior Step-1 re-review
```

Not authorized:

```text
Step 2 or Steps 2–8
implementation planning
substantive implementation
runtime/schema/test realization
release or migration execution
next WP
gameplay/campaign bootstrap
```

## 2. Problem statement

HDM already has native outcome/failure semantics distributed across domain owners. These include persistence/publication/recovery, Context Runtime, deterministic rules/catalog/admission/execution, House Rules/adjudication, maintenance/support, bootstrap/creation/readiness/save-exit, compatibility/migration, LIVE/multiplayer, collaboration/agency, integrity, Story/derived state, diagnostics, package/runtime selection and presentation/disclosure.

WP-25 must later determine how material failures compose across those owners without creating a universal error authority.

The architecture problem is broader than an error enum. Later Steps 2–8 must be able to classify a material condition with enough independent dimensions to answer, at minimum:

```text
native failure / epistemic outcome
truthful frontier
effective severity
gameplay impact
affected scope / blast radius
risk if ignored
legal continuation
temporal tolerance / semantic fence
bounded recovery
retry / idempotency semantics
prohibited fallback
user-visible disposition
verification / empirical-acceptance obligation
```

The framing must survive cascading failures: failure during recovery/repair; ambiguity after partial success; retry exhaustion; authority/currentness movement while diagnosing/recovering; local adoption failure after remote semantic acceptance; deterministic rules/admission failure; failure after accepted mechanics/RNG; maintenance denial/redaction/unavailability; bootstrap/generator/initial-publication failure; and failure between accepted state and player-visible presentation or save-exit completion.

## 3. Product Owner / accepted direction input

Mandatory Product Owner inputs are distinct from native semantic owners:

- `DEV/docs/superpowers/specs/2026-09-08-hdm-wp25-failure-degradation-durability-risk-owner-direction.md` — accepted Product Owner / architecture-direction input for WP-25; binding direction but explicitly not WP-25 closure.
- `DEV/PRODUCT_OWNER_INPUT.md` — full `PO-008`, including its host-capacity/durability-risk amendment and routing state.

Accepted direction:

```text
OWNER-LOCAL NATIVE OUTCOMES
+ EPHEMERAL CROSS-OWNER FAILURE DISPOSITION
+ SCOPE-AWARE CONTINUATION
+ RISK-TRAJECTORY-AWARE DURABILITY PROTECTION

FAILURE CAUSE
!= EFFECTIVE SEVERITY
!= GAMEPLAY DISPOSITION
!= RETRY POLICY

S0 NOTICE
S1 DEGRADED
S2 GUARDED
S3 QUARANTINED
S4 CRITICAL
```

Severity is context-derived. `UNSUPPORTED` is an orthogonal capability/deployment/compatibility disposition, not shorthand for `S4`.

Gameplay impact, affected scope/blast radius, risk if ignored, semantic temporal tolerance, truthful frontier, recovery/retry semantics, user visibility and proof obligations remain separate dimensions.

## 4. Goals

1. Establish the complete WP-25 problem horizon without choosing a final master error taxonomy.
2. Preserve current native outcome owners and their existing distinctions.
3. Make severity, gameplay disposition, retry policy, scope, risk, tolerance, truthful frontier and user visibility independently reasoned dimensions.
4. Cover local and cascading failure chains, including deterministic rule/admission, maintenance/support and bootstrap/save-exit paths added by bounded recovery.
5. Preserve authority/currentness, agency, information/disclosure and accepted-mechanics/RNG invariants through failure handling.
6. Compose Product Owner durability-risk intent with Step-5.5 / WP-13 / host-assurance / WP-24 instead of restoring a timer product law.
7. Distinguish accepted semantic-owner conflict from stale/incomplete GAME/schema/test realization and from capability that is intentionally dormant/unrealized.
8. Preserve proof-class separation so architecture does not claim empirical host behavior without realized-target evidence.
9. Leave later authorized design work with a finite, auditable owner graph and falsifiable research questions.

## 5. Non-goals

WP-25 Step 1 does not:

- choose the final WP-25 architecture or canonical schema;
- create a persisted global error/failure registry;
- normalize every owner result into one enum;
- convert ordinary gameplay failure (failed attack/check/save, resisted effect, failed fictional attempt) into system failure;
- create a new deterministic-rules, House-Rules, maintenance, campaign-lifecycle or bootstrap authority;
- define exact host-capacity, token, message, context or time thresholds;
- create a generic timeout, lease, heartbeat, worker, queue or scheduler;
- define a universal retry count or duration;
- rewrite current persistence/recovery/LIVE/migration/Story/disclosure/bootstrap/rules owners;
- repair runtime/schema/test realization;
- implement the proposed maintenance command surface;
- add telemetry or diagnostics schemas;
- claim empirical ChatGPT/host capacity, reliability, latency or emergency-preservation success probability;
- perform migration/release/runtime execution.

## 6. Existing architecture invariants carried into WP-25

1. Native semantic owners remain authoritative for their own outcomes and transitions.
2. Cross-owner failure composition is ephemeral unless a future owning decision proves a persistence requirement; it is not a second semantic owner.
3. LLM prose, chat/model memory, Story, checkpoint, planning, cache, index and diagnostics are not campaign authority.
4. Accepted IDs are stable; recovery does not invent replacement identities.
5. Accepted mechanics/RNG and voluntary player actions are not replayed, rerolled or rewritten merely to repair persistence/presentation/transport.
6. Ordinary resolved gameplay failure is a gameplay outcome unless a native system owner separately reports a system failure.
7. Physical data visibility does not promote information eligibility or disclosure authority.
8. Publication/currentness uses pinned authority and the supported non-force exact-source fence; ambiguous authority-changing publication is never blind-retried.
9. Force push/ref rewind and HDM branch/ref deletion are prohibited.
10. Git order, arrival order, timestamps or last-writer-wins do not manufacture fictional authority/chronology.
11. Recovery begins from actual current native authority and bounded required closure.
12. Normal waiting for an authorized contribution is not automatically a failure; required missing contribution may freeze only its dependent scope.
13. Context `UNSATISFIABLE` must not be converted to guessed evidence.
14. Unsupported/indeterminate compatibility fails closed; version order/ancestry do not manufacture compatibility/migration paths.
15. A catalog search miss is not automatically an unsupported-capability gap; native catalog/admission evidence owns that distinction.
16. Dormant/nonselectable/quarantined executable capability is not silently activated by reference, policy text, registration or need.
17. Missing House-Rule/adjudication evidence is not guessed; missing is not false, and stale/unauthorized/invalid inputs retain their native typed outcome.
18. Maintenance operation routing is not authorization; authorization is not disclosure eligibility; diagnostic/error text is not gameplay/recovery/currentness authority.
19. A denied/unavailable maintenance attempt creates no gameplay event, fictional chronology/state, RNG or durable denial record merely because it was attempted.
20. Generator failure or incomplete/failed initial publication does not authorize LLM scaffold reconstruction or setup against a partial scaffold.
21. Campaign selection is explicit; bounded preselection discovery does not become implicit gameplay/campaign authority.
22. Unresolved readiness/mechanics blocks only the dependent capability under its owner; no state is invented to force readiness.
23. Failed/rejected/indeterminate save-and-exit persistence does not authorize clearing the strongest truthful recovery-safe selected-campaign context or claiming saved-and-exited success.
24. Story failure/lag cannot replace native canon and ordinarily cannot block/roll back gameplay/recovery readiness.
25. Ordinary operations remain bounded; no WORLD/history/all-ref/all-LIVE scans are introduced as recovery shortcuts.
26. No background worker/heartbeat correctness dependency is introduced for the supported product.
27. Architecture coverage, machine realization, verification realization and empirical acceptance are separate proof classes.

## 7. Durability / host-capacity framing

### 7.1 Correctness HARD versus operability/loss-protection fence

```text
CORRECTNESS HARD
    durability is a mandatory postcondition of a named semantic edge

OPERABILITY / LOSS-PROTECTION FENCE
    coherent HOT/SOFT state remains semantically correct,
    but allowing materially more single-copy unpublished exposure has become
    an unacceptable product risk
```

The second category does not make coherent HOT corrupt and does not redefine all SOFT state as HARD.

### 7.2 Risk trajectory

```text
NORMAL
ELEVATED
DANGER
```

Exact machine thresholds remain open pending applicable evidence. Approximate chat/context/message/token/capacity signals may later be advisory preservation evidence but cannot become truth/currentness/authorization authority or a fictional exact remaining-context contract.

At `DANGER`, later architecture must be able to guard before further materially state-growing gameplay when preservation/repair is required, without declaring the existing coherent HOT frontier corrupt solely because capacity risk is high.

### 7.3 Supersession discipline

The historical `GAME/CORE/DURABILITY_GUARD.md` / `SESSION.md` one-hour dirty ceiling and `DEV/TESTS/test_hourly_durability_contract.py` are realization evidence, not current product-law authority where they conflict with Step-5.5/WP-13 and accepted WP-25 direction. Their presence is realization debt, not an architecture reopen trigger.

## 8. Required failure horizon for later Steps 2–8

The source/critic route must support at least these families without assuming they are the final taxonomy:

1. host capability unavailable or degraded;
2. stale/currentness/moved authority;
3. authentication, identity, eligibility or control failure;
4. malformed, contradictory, dangling or integrity-defective native state;
5. Context assembly degraded/`UNSATISFIABLE`;
6. publication rejection, ambiguous outcome or partial success;
7. recovery source absence/incompatibility/retry exhaustion;
8. LIVE ownership/currentness/conflict ambiguity;
9. collaboration generation/currentness or required-contribution failure, while distinguishing ordinary waiting;
10. migration/update compatibility unsupported/indeterminate/path failure;
11. Story/planning/derived-state lag, stale basis, conflict or optional unavailability;
12. presentation/render/disclosure interruption or re-presentation uncertainty after accepted semantics;
13. diagnostics/cleanup proof unavailable or indeterminate;
14. runtime-package/instruction-basis loss, mismatch or mixed-runtime risk;
15. deterministic catalog/ruleset context incompatibility, preserving native incompatibility reasons;
16. bounded unsupported-capability/gap evidence distinct from a search miss or dormant capability;
17. dormant/nonselectable/quarantined executable capability distinct from compiler/primitive validation rejection;
18. compiler/primitive validation rejection, invalid dependency/argument/result contract or mutation validation failure;
19. House-Rule policy conflict or policy-realization gap;
20. adjudication input missing, unauthorized, invalid or stale, including missing/stale/incompatible/dormant realization references;
21. maintenance/support authorization failure, unresolved/currentness failure, recipient withholding/redaction, or capability-not-realized/unavailable;
22. campaign bootstrap/selection/generator/initial-materialization/publication failure;
23. readiness/mechanics dependency preventing only a dependent setup/gameplay capability;
24. save-and-exit persistence rejection/ambiguity or post-save-exit continuation-context preservation requirement;
25. compound/cascading failure combining several of the above.

For every material condition, later synthesis must ask what remains truthful and legally continuable rather than merely assign an error label.

### 8.1 Deterministic rules/admission distinction

Later design must preserve at least:

```text
failure.catalog_context_incompatible
    != runtime.catalog_gap_report
    != DORMANT_NONSELECTABLE / quarantined realization
    != compiler or primitive validation rejection
    != gameplay action/check failure

POLICY_CONFLICT
    != POLICY_REALIZATION_GAP
    != missing/unauthorized/invalid/stale adjudication input
    != missing/stale/incompatible/dormant realization reference
```

A registered ID, House-Rule reference or available package byte does not itself grant execution authority. A failed attack/check/save remains an ordinary mechanical/gameplay outcome unless a native system contract separately failed.

### 8.2 Maintenance/support distinction

The current DEV maintenance semantic contract is `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md`; it explicitly states that the installed GAME command registration/parser/dispatcher surface is not currently established. Therefore `UNAVAILABLE_NOT_REALIZED` is a valid capability state rather than evidence that a runtime command must be invented.

Preserve:

```text
operation routing != authorization
authorization != disclosure eligibility
diagnostic/error text != gameplay/recovery/currentness authority
```

Authorization/currentness failure must fail closed before mutation/sensitive disclosure. Recipient-ineligible detail is withheld/redacted. Denial/unavailability does not create fictional time/state or a gameplay event merely to log the failure.

### 8.3 Bootstrap / creation / save-exit distinction

WP-19 remains the composition owner. It does not create a second lifecycle or publication owner.

```text
explicit selection barrier
    -> bounded menu/preselection evidence only

New Game
    -> exact selected package generator once
    -> complete scaffold
    -> one initialization tree/commit
    -> non-force create-if-absent publication
    -> only confirmed success permits setup against that scaffold

generator unavailable/failed OR scaffold incomplete OR initial publication failed
    -> no LLM reconstruction
    -> no partial per-file substitute
    -> no successful campaign creation
    -> no setup against partial scaffold

save-and-exit
    -> save closure first
    -> only confirmed durable closure permits clearing selected gameplay context
```

Indeterminate/rejected save publication retains the strongest truthful recovery-safe selected-campaign context until native publication/recovery semantics resolve it.

## 9. Cascading-failure attack routes

Later authorized work must explicitly attack at least:

- recovery attempt fails while native currentness continues moving;
- repair succeeds locally but publication result is indeterminate;
- publication succeeded remotely but local adoption/rebind failed;
- retry reaches its owner-bounded exhaustion condition;
- authorization or PLAYER/LIVE ownership changes while recovery/diagnostics is in progress;
- migration/update prepares successfully but current authority moves before publication;
- migration is accepted remotely but local target-runtime rebind/rehydration fails;
- accepted mechanics/RNG exists but persistence/presentation fails afterward;
- accepted fictional/state transition exists but player-visible rendering is interrupted;
- disclosure acceptance/evidence differs from what was physically rendered;
- Story/planning regeneration fails while native sources remain usable;
- cleanup/retirement evidence becomes stale while assessment runs;
- host capacity moves from operable to dangerous while unpublished established state grows;
- instruction-context loss/mixed package basis is discovered while gameplay continuation is pending;
- exact ruleset/catalog context fails reconstruction after previously admitted state is loaded;
- bounded capability discovery proves a true gap while another similarly named capability is merely dormant/nonselectable;
- House-Rule policy remains semantically active but its realization reference is missing, stale, incompatible or quarantined;
- adjudication input was accepted under one exact rules/policy basis but currentness changes before execution/retry;
- primitive compilation succeeds until a nested dependency/argument/result contract fails; no partial mutation/event may escape;
- maintenance token routes correctly but creator/principal/currentness cannot be proved; operation must deny without mutation or sensitive diagnostics;
- maintenance operation is authorized but requested recipient is not eligible for part of the diagnostic result; output must withhold/redact without changing campaign truth;
- maintenance is requested where the semantic contract exists but runtime command realization does not; no invented dispatcher/operation is allowed;
- new-game generator succeeds locally but initial publication is rejected/ambiguous; no setup may continue against the prepared/unpublished scaffold;
- fresh-chat menu sees one plausible campaign but no explicit selection exists; no campaign preload/recovery/update work may start;
- character/setup state has unresolved mechanics/readiness evidence; only dependent capability remains unavailable and established facts remain intact;
- save-and-exit materialization is locally complete but publication is rejected/indeterminate; selected recovery-safe context must remain until native outcome is resolved.

## 10. Quality attributes for later alternatives

- semantic correctness and truthful frontier preservation;
- authority/currentness safety;
- bounded recovery and retry safety;
- deterministic-rules/admission fidelity without accidental activation;
- agency and disclosure safety;
- bootstrap/creation atomicity and honest readiness;
- loss containment for established unpublished state;
- graceful local degradation rather than unnecessary campaign-global blocking;
- deterministic/idempotent recovery where the owner permits it;
- debuggability and user-actionability without leaking secrets/internal noise;
- bounded ordinary-turn cost and absence of unbounded scans/background correctness work;
- compatibility with single-context supported-host constraints;
- reversibility and implementation complexity;
- verifiability and empirical testability.

No unowned numerical latency/capacity target is introduced.

## 11. Open-world Source Manifest

Inspection vocabulary:

- `FULL` — current substantive contract relevant to WP-25 inspected.
- `TARGETED` — relevant owner/consumer portions inspected; unrelated scope not required.
- `STRUCTURAL` — family/tree inspected to establish consumer route; selected members read directly.

### 11.1 Process / current-stage / routing authority

| Source | Role | WP-25 relevance | Inspection |
|---|---|---|---|
| `AGENTS.md` | repository/process authority | bootstrap, Connector-only transport, taxonomy, branch/write/version/checkpoint rules | FULL |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | runtime overlay | remote publication/currentness/verification mechanics | FULL |
| `DEV/DESIGN_PROCESS.md` | canonical design process | Step-1 Source Manifest, critic, evidence completeness | FULL |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | HDM process adapter | whole-project critic + mandatory Senior gate | FULL |
| `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md` | PO-input process owner | PO evidence vs semantic owner distinction | FULL |
| `DEV/PROJECT_MAP.md` | derivative locator | open-world dependency reconstruction | FULL |
| `DEV/CURRENT_PROGRESS.md` | current-progress authority | Senior HOLD / bounded recovery / re-review gate | FULL |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | sequencing/scope authority | R2.7 sequence and WP-25 placement | TARGETED |
| `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | derivative semantic locator | owner routing, never semantic override | TARGETED |
| `DEV/RELEASE/VERSIONING.md` | version-impact gate | confirms design/status-only repair has no namespace bump | FULL |

### 11.2 Mandatory Product Owner direction

| Source | Role | WP-25 relevance | Inspection |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-08-hdm-wp25-failure-degradation-durability-risk-owner-direction.md` | PO / accepted architecture direction | multidimensional failure direction, durability-risk intent, proof discipline | FULL |
| `DEV/PRODUCT_OWNER_INPUT.md` — `PO-008` | PO intent/routing evidence | original error/degradation request + host-capacity amendment | FULL ENTRY |

### 11.3 Durability, publication, recovery and integrity owners

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md` | canonical owner | `ESTABLISHED != DURABLE`, SOFT/HARD, named HARD edges | FULL |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md` | canonical owner | publication tri-state/currentness/ambiguity/no blind retry | FULL |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md` | canonical owner | `READY/RETRY/BLOCKED`, bounded recovery/current-authority-first | FULL |
| `DEV/docs/superpowers/specs/2026-09-06-hdm-publication-currentness-supported-ref-repair-amendment.md` | canonical amendment | parent + non-force fence, create-if-absent, ambiguity closure | FULL |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md` | integration owner | compound recovery/concurrency constraints | FULL |
| `GAME/CORE/SAVE_CONTRACT.md` | runtime consumer | save completeness/success semantics | FULL |
| `GAME/CORE/PERSISTENCE.md` | runtime consumer | publication/write realization | FULL |
| `GAME/CORE/INTEGRITY.md` | runtime consumer | integrity-suspect/repair behavior | FULL |
| `GAME/CORE/RUNTIME.md` | runtime consumer | fast-path/recovery/presentation integration | FULL |
| `GAME/CORE/DURABILITY_GUARD.md` | stale realization evidence | retired one-hour product rule | FULL |
| `GAME/CORE/SESSION.md` | stale/current consumer | one-hour dependency + continuation/recovery | FULL |

### 11.4 Context, instruction basis and supported-host owners

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md` | canonical owner | `ASSEMBLED/ASSEMBLED_DEGRADED/UNSATISFIABLE` | FULL |
| `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md` | canonical owner | single-context containment / no hidden correctness worker | FULL |
| `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md` | canonical owner | host capability fail-closed + empirical assurance | FULL |
| `DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-08-llm-role-context-instruction-realization-canonical-spec.md` | realization owner | exact-package instruction cache/rehydration | FULL |
| `DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-09-context-loading-resource-bounds-realization-canonical-spec.md` | realization owner | bounded Context realization | FULL |

### 11.5 Authority, LIVE, collaboration, chronology and disclosure

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | current owner | creator/PLAYER/maintenance authorization fail closed | FULL |
| `DEV/ARCHITECTURE/BRANCH_MODEL.md` | derivative projection | branch/storage/runtime routing | FULL |
| `DEV/docs/superpowers/specs/2026-09-06-hdm-creator-login-continuity-owner-decision.md` | PO decision | unresolvable creator identity fail closed | FULL |
| `DEV/docs/superpowers/specs/2026-09-06-hdm-branch-ref-deletion-prohibition-owner-decision.md` | PO decision | absolute ref deletion prohibition | FULL |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md` | canonical owner | LIVE authority/currentness | FULL |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-canonical-spec.md` | canonical owner | contribution/agency/dependent-scope freeze | FULL |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` | canonical owner | accepted semantics vs render/delivery; recipient eligibility | FULL |
| `GAME/CORE/LIVE_SCENE.md` | runtime realization evidence | LIVE failure/conflict/absorption consumer | FULL |
| `GAME/CORE/MULTIPLAYER.md` | runtime consumer | membership/currentness/conflict | FULL |
| `GAME/CORE/CHRONOLOGY.md` | runtime consumer | partial-order uncertainty / no global timeline | FULL |

### 11.6 Deterministic rules, catalog/ruleset admission and House Rules — SR25-S1-01 recovery

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| `DEV/ARCHITECTURE/CATALOG_ADMISSION.md` | current admission owner | admission dispositions, catalog incompatibility, capability-gap distinction | FULL |
| `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md` | current resolution owner | exact context resolution, bounded discovery, no LLM replacement | FULL |
| `DEV/ARCHITECTURE/RULESET_PACKAGE_MACHINE_CLOSURE.md` | ruleset machine closure owner | exact lock/compatibility/fail-closed package realization | FULL |
| `DEV/ARCHITECTURE/ACTIVITY_MODEL.md` | Activity owner | invocation validation, ordinary gameplay failure vs system failure, retry identity | FULL |
| `DEV/ARCHITECTURE/ACTIVITY_PRIMITIVE_CONTRACTS.md` | primitive contract owner | active vs dormant/quarantined primitives, compiler/validation rejection | FULL |
| `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md` | deterministic rule-element owner | registered selector/accessor inputs, missing adjudication, compile validation | TARGETED |
| `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` | House-Rule semantic/policy owner | policy authority, conflict, adjudication inputs, realization refs | FULL |
| `DEV/ARCHITECTURE/HOUSE_RULES_MECHANICAL_BOUNDARY.md` | House-Rule execution-boundary owner | typed accepted input -> native validation -> deterministic result/failure | FULL |
| `GAME/CORE/ADJUDICATION.md` | runtime adjudication consumer | frozen accepted input, gameplay outcome classes, failed-check semantics | FULL |
| `GAME/CORE/PLAY_POLICY.md` | runtime policy consumer | gameplay vs explicit maintenance boundary | FULL |
| `DEV/CATALOG/catalog-admission-ledger/manifest.json` | machine projection | admission dispositions + typed catalog incompatibility/gap mapping | FULL |
| `DEV/CATALOG/activity-primitive-contracts/manifest.json` | machine projection | exact primitive compiler/selection laws | FULL |
| `DEV/CATALOG/house-rules-mechanical-boundary.json` | machine projection | exact adjudicated edges + current/conformance realization refs | FULL |
| `GAME/SCHEMA/house_rules_policy.schema.yaml` | persistent machine consumer | lifecycle/authority/routing/realization gap semantics | FULL |
| `DEV/SCHEMAS/activity-parameter-binding.schema.json` | execution input schema | exact adjudicated value/provenance/basis evidence | FULL |
| `DEV/TESTS/test_s6d_02_catalog_admission_contract.py`, `test_catalog_admission_ledger_split.py` | executable consumers | admission/gap/currentness law | STRUCTURAL |
| `DEV/TESTS/test_s6d_06_activity_primitive_contract.py`, `test_r2_7_wp05_execution_conformance.py`, `test_r2_7_wp06_rules_conformance.py` | executable consumers | primitive/compiler/execution conformance | STRUCTURAL |
| `DEV/TESTS/test_house_rules_adjudicated_input_contract.py`, `test_house_rules_policy_authority_contract.py`, `test_s6d_10_house_rules_boundary_contract.py`, `test_s6d_11_ruleset_package_closure.py` | executable consumers | House Rules/adjudication/realization/package failures | TARGETED/STRUCTURAL |

Current native distinctions recovered from this route include:

```text
failure.catalog_context_incompatible
runtime.catalog_gap_report
ACTIVE_ADMITTED / DORMANT_NONSELECTABLE / quarantined realization
compiler/primitive validation rejection
failure.policy_conflict
failure.policy_realization_gap
failure.adjudication_input_missing
failure.adjudication_input_unauthorized
failure.adjudication_input_invalid
failure.adjudication_context_stale
missing/stale/incompatible/dormant realization reference
```

These are not interchangeable and do not reclassify ordinary failed gameplay resolution as system failure.

### 11.7 Maintenance / diagnostics / support — SR25-S1-02 recovery

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` | current DEV maintenance semantic/support contract | routing/auth/currentness/disclosure/unrealized outcomes; explicitly not installed runtime command surface | FULL |
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | authorization owner | creator-only campaign-global maintenance; unresolved principal fails closed | FULL |
| Step-5.12 delivery/disclosure owner above | disclosure owner | recipient-safe diagnostics and presentation boundary | FULL |
| `GAME/CORE/PLAY_POLICY.md` | runtime neighbor | explicit maintenance does not become ordinary gameplay | FULL |
| `GAME/CORE/RUNTIME.md`, `GAME/CORE/SESSION.md`, `GAME/CORE/INTEGRITY.md` | runtime neighbors | truthful continuation/recovery/integrity context | FULL |
| `DEV/TOOLS/run_maintenance_audit.py`, `DEV/TOOLS/audit_engine.py` | current development support tooling | repository maintenance/audit tooling, not campaign maintenance command authority | STRUCTURAL |
| `DEV/TESTS/test_maintenance_continuation_contract.py` | executable consumer | continuation frame/nonfictional maintenance transition | FULL |
| `DEV/TESTS/ACCESS_CONTROL_CASES.md` | scenario consumer | authorization/permission distinctions | TARGETED |
| `DEV/TESTS/test_maintenance_audit_bytecode_clean.py` | development tooling consumer | maintenance audit hygiene | STRUCTURAL |

Native maintenance outcomes preserved:

```text
NOT_AUTHORIZED
NOT_CURRENT_OR_UNRESOLVED
WITHHELD_OR_REDACTED
UNAVAILABLE_NOT_REALIZED
```

### 11.8 Bootstrap / initial materialization / save-exit — SR25-S1-03 recovery

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-canonical-spec.md` | canonical composition owner | selection barrier, generator/scaffold/initial publication/readiness/save-exit | FULL |
| `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md` | PO/canonical composition decision | save-and-exit preservation, no new lifecycle state | FULL |
| `GAME/INSTALL/00_DND_BOOTSTRAP.md` | install/bootstrap runtime consumer | exact package/storage discovery/explicit campaign selection | FULL |
| `GAME/CORE/BOOTSTRAP_RUNTIME.md` | runtime bootstrap consumer | exact runtime binding, bounded preselection, post-selection loading | FULL |
| `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` | runtime creation consumer | generator-first, no semantic reconstruction, one publication | FULL |
| `GAME/CORE/CAMPAIGN_SETUP.md` | runtime setup consumer | generator/publication success barrier + readiness staging | FULL |
| `GAME/TOOLS/init_campaign.py` | executable generator | exact scaffold materialization/validation, no GitHub authority | FULL |
| `GAME/CORE/SAVE_CONTRACT.md`, `GAME/CORE/SESSION.md`, `GAME/CORE/PERSISTENCE.md` | save/exit composition neighbors | completeness, truthful context, publication outcome | FULL |
| `DEV/TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md` | scenario consumer | explicit selection, bounded preselection, generator/no-fallback, one publication | FULL |
| `DEV/TESTS/test_multi_runtime_bootstrap_contract.py` | executable consumer | isolated exact runtime/bootstrap behavior | FULL |
| `DEV/TESTS/EXPLICIT_SAVE_CASES.md` | scenario consumer | complete save, partial failure/no false success, readiness preservation | FULL |
| `DEV/TESTS/INSTALL_ONBOARDING_CASES.md`, `CHARACTER_READINESS_CASES.md`, `CAMPAIGN_CARD_CASES.md` | scenario families | installation/onboarding/readiness projections | STRUCTURAL |

### 11.9 Update, compatibility, package and instruction continuity

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md` | canonical owner | compatibility outcomes/migration/currentness | FULL |
| `GAME/CORE/ENGINE_UPDATES.md` | runtime consumer | mismatch recovery/local adoption/mixed-runtime prohibition | FULL |
| `DEV/docs/superpowers/specs/2026-09-08-r2-7-WP-23-release-package-version-legal-readiness-canonical-spec.md` | canonical owner | exact package/provenance/release proof separation | FULL |

### 11.10 Story, planning, diagnostics and scale

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-canonical-spec.md` | canonical owner | Story derived/noncanonical lag/failure | FULL |
| `DEV/docs/superpowers/specs/2026-09-07-story-producer-persistence-retrospective-consumer-contract.md` | integration contract | native-basis Story consumer route | FULL |
| `DEV/docs/superpowers/specs/2026-09-07-r2-7-WP-21-diagnostics-observability-cleanup-retirement-canonical-spec.md` | canonical owner | diagnostics nonauthority/UNKNOWN/cleanup indeterminacy | FULL |
| `DEV/docs/superpowers/specs/2026-09-07-r2-7-WP-22-verification-test-evaluation-completeness-canonical-spec.md` | canonical owner | proof-class separation | FULL |
| `DEV/docs/superpowers/specs/2026-09-08-r2-7-WP-24-performance-scale-operational-budget-canonical-spec.md` | canonical owner | bounded operations/staged empirical proof | FULL |

### 11.11 General machine/schema/test consumers

| Source/family | Role | Relevance | Inspection |
|---|---|---|---|
| `GAME/SCHEMA/*.schema.yaml` | persistent/runtime contracts | avoid accidental new authority/global pending bucket | STRUCTURAL |
| `GAME/SCHEMA/live_scene.schema.yaml` | LIVE machine consumer | objective truth/knowledge + closed/absorbed distinction | FULL |
| `GAME/SCHEMA/checkpoint.schema.yaml` | recovery projection | not snapshot/current authority | FULL |
| `GAME/SCHEMA/current_state.schema.yaml` | current routing projection | no generic pending bucket | FULL |
| `GAME/SCHEMA/campaign_manifest.schema.yaml` | campaign identity/lifecycle projection | force-push false/current engine/ruleset identity | FULL |
| `DEV/TESTS/` | executable/scenario family | whole-project realization consumers | STRUCTURAL |
| `DEV/TESTS/test_hourly_durability_contract.py` | stale realization evidence | actively asserts retired one-hour product rule | FULL |
| `DEV/TESTS/test_publication_ref_fence_contract.py` | currentness evidence | stale sibling/ambiguity/rewind laws | FULL |
| `DEV/TESTS/test_engine_mismatch_recovery_contract.py` | package recovery evidence | restore/update paths/no arbitrary fallback | FULL |
| `.github/workflows/validate.yml` | hosted CI | exact-head maintenance audit + DEV unit tests | FULL |

## 12. Source-role reconciliation / current-owner rules

1. Product Owner direction constrains WP-25 but does not replace native semantic owners.
2. Step-5.5/WP-13 current durability law wins over stale hourly GAME/test realization.
3. WP-16 wins over older LIVE runtime wording where they differ.
4. The supported-ref amendment supplies current Git-backed currentness realization; logical exact-source law remains.
5. Catalog admission/resolution + ruleset package closure own catalog-context incompatibility and capability-gap evidence; a search miss or dormant registration does not substitute.
6. Activity/primitive/Rule-Element owners own deterministic validation and compilation; ordinary gameplay resolution remains separate.
7. `CAMPAIGN_HOUSE_RULES.md` + `HOUSE_RULES_MECHANICAL_BOUNDARY.md` own policy/adjudication/realization distinction; policy mention never activates missing/dormant execution.
8. `MAINTENANCE_COMMANDS.md` is the current DEV semantic support contract but explicitly not an installed GAME command surface; access and disclosure owners remain independent.
9. WP-19 composes bootstrap/creation/readiness/save-exit but does not replace generator, publication, lifecycle/readiness, persistence or campaign-selection native owners.
10. WP-20 owns compatibility/migration over package/version heuristics.
11. WP-22/WP-24/R2.6 control proof strength.
12. Story/diagnostics/checkpoints/indexes are evidence/projections/consumers, never missing-canon/currentness substitutes.
13. Stale runtime/schema/test projection or intentionally unrealized capability creates realization debt/state, not automatic accepted-architecture conflict.

## 13. Step-2 research questions prepared by Step 1

If and only if independent Senior Step-1 re-review later gives GO, Step 2 must answer with evidence:

1. What is the minimal ephemeral cross-owner disposition model that composes native outcomes without becoming a second authority?
2. Which inputs are sufficient to derive context-sensitive `S0..S4`, and which remain owner-specific?
3. How do gameplay impact and blast radius compose across local, dependent-scope, campaign-resume and deployment-profile failures?
4. Which risk dimensions distinguish operability debt, progress-loss exposure, canon/currentness/agency risk and disclosure/security risk?
5. For each native family, what truthful frontier survives and what continuation is legal now?
6. What semantic fences/tolerances are owner-specific, and where must WP-25 reject a universal timeout?
7. What bounded retry/idempotency rule applies after rejection, indeterminate authority-changing operation, recovery reassembly, local post-remote adoption failure and retry exhaustion?
8. How does `UNSUPPORTED` compose with severity/impact without becoming a universal terminal class?
9. How should NORMAL/ELEVATED/DANGER derive from unpublished established state plus advisory host-survivability evidence without fictitious exact capacity?
10. Which DANGER transitions guard further state growth and what preservation/repair outcome permits continuation?
11. Which user-visible notices are actionable/safe and which internal degradation details should remain invisible?
12. What machine/test/empirical obligations arise from each disposition without overclaiming proof strength?
13. Which stale runtime/test projections need later realization repair versus expose genuine architecture insufficiency?
14. How should catalog-context incompatibility, true capability gap, dormant/nonselectable capability, primitive/compiler rejection and ordinary gameplay failure compose without collapsing their native meanings?
15. What exact evidence is sufficient to call a capability unsupported rather than merely undiscovered, dormant or not selected?
16. How should House-Rule policy conflict, realization gap and adjudication-input failures affect only their dependent mechanical scope while preserving exact accepted policy/input basis across retry?
17. What user-visible maintenance disposition is safe for `NOT_AUTHORIZED`, `NOT_CURRENT_OR_UNRESOLVED`, `WITHHELD_OR_REDACTED` and `UNAVAILABLE_NOT_REALIZED`, given independent recipient eligibility?
18. How does maintenance failure preserve current gameplay continuation without creating fictional time/state or treating diagnostics as recovery authority?
19. How should generator/scaffold/initial-publication failures map to continuation while preserving the explicit selection barrier and zero partial-scaffold authority?
20. After rejected/indeterminate save-and-exit publication, what exact context must remain to preserve the strongest recovery-safe selected-campaign frontier until native publication/recovery resolves?
21. How should unresolved readiness/mechanics dependency expose a local unavailable capability without converting the entire initializing campaign into a generic failure state?

## 14. Framing falsifiability / reopen conditions

Revise/reject this framing if later evidence shows:

- a native owner cannot express a required truthful outcome without a new shared persistent authority;
- owner-local outcomes cannot compose without losing correctness/currentness/agency/disclosure semantics;
- safe bounded recovery requires a forbidden global scan/hidden background dependency;
- accepted durability intent cannot protect significant single-copy HOT/SOFT exposure without redefining correctness HARD or inventing host-capacity authority;
- deterministic rule/admission or House-Rule owners contain a real contradiction that this Step-1 composition currently masks;
- maintenance/support or bootstrap/save-exit has an unsatisfied semantic consumer that current owners cannot represent;
- an accepted owner directly contradicts mandatory Product Owner direction in a way not mechanically reconcilable;
- a real supported-host limitation makes an accepted semantic boundary physically unrealizable and requires deployment restriction or architecture reopening.

Implementation inconvenience, dormant capability, missing machine realization or stale projections alone are not reopen evidence.

## 15. Bounded Senior-HOLD recovery result

Independent Senior review of `ec1b8602840acf0c28b38cf2ab24fb1d3feee557` identified:

```text
SR25-S1-01 — deterministic rules/admission/House-Rules owners omitted
SR25-S1-02 — actual maintenance/diagnostics consumer omitted
SR25-S1-03 — bootstrap/initial-materialization/save-exit path omitted
```

The expanded Source Manifest and repaired framing above independently traced the owning graphs and machine/schema/test consumers for all three.

Worker disposition:

```text
SR25-S1-01: REPAIRED / WORKER-CLOSED / PENDING INDEPENDENT SENIOR RE-REVIEW
SR25-S1-02: REPAIRED / WORKER-CLOSED / PENDING INDEPENDENT SENIOR RE-REVIEW
SR25-S1-03: REPAIRED / WORKER-CLOSED / PENDING INDEPENDENT SENIOR RE-REVIEW
```

The rerun whole-project critic is recorded at:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-25-step-1-whole-project-critic.md`.

No Step 2 authority is implied.

```text
WP25_STEP1_SENIOR_REVIEW_PREVIOUS_RESULT: HOLD
WP25_STEP1_BOUNDED_RECOVERY: COMPLETE / PUBLISHED WHEN THIS PACKAGE IS COMMITTED
WP25_STEP1_SENIOR_RE_REVIEW: REQUIRED / PENDING
WP25_STEP2_AUTHORIZED: NO
UNRESOLVED_BLOCKING_IN_WORKER_RECOVERY: 0
UNRESOLVED_SIGNIFICANT_IN_WORKER_RECOVERY: 0
HUMAN_DECISION_REQUIRED: NO
NEXT_AUTHORIZED_UNIT: NONE
NEXT_GATE: mandatory independent WP-25 Step-1 Senior re-review
```

## 16. Version Impact

```text
VERSION_IMPACT: NONE
```

This bounded recovery changes design provenance and current progress only. It does not modify a version-bearing runtime module, persistent/protocol schema, campaign/storage/catalog/ruleset generation, package/release format, migration law or executable gameplay/runtime realization.