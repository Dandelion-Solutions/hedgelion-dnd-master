# R2.7 WP-25 Step 1 — Error / Degradation / Failure Semantics — Architecture Task Brief + Source Manifest

Status: **SECOND BOUNDED STEP-1 RECOVERY COMPLETE AT WORKER LEVEL — MANDATORY INDEPENDENT SENIOR STEP-1 RE-RE-REVIEW GO / STEPS 2–8 AUTHORIZED**

Date: 2026-09-08

Senior re-review baseline: `865b4b16cfcca4f27104eaeb3eb13e72de87b750`
Senior re-re-review baseline: `18fcf6efcada8a01c559362494291700ec4b637e`

This artifact is design-process provenance for **R2.7 WP-25 Step 1 only**. It is not a canonical WP-25 specification and does not replace any native failure, ruleset identity, catalog/admission, readiness, storage, persistence, recovery, maintenance, compatibility, multiplayer, disclosure, Story or verification owner.

The mandatory independent Senior Step-1 re-review of the first bounded-recovery checkpoint returned **HOLD — second bounded Step-1 recovery required** with 0 BLOCKING, 2 SIGNIFICANT and 1 MINOR unresolved findings. The second recovery below performed only the requested evidence/source-manifest/framing recovery and reran the whole-project Step-1 critic. Mandatory independent Senior Step-1 re-re-review of `18fcf6efcada8a01c559362494291700ec4b637e` subsequently returned **GO WITH REQUIRED NON-BLOCKING SOURCE-ROLE CORRECTION**, with 0 unresolved BLOCKING/SIGNIFICANT findings and WP-25 Steps 2–8 authorized. The source-role correction is incorporated in this artifact without rewriting historical Step-1 analysis as though the later review result had been known earlier.

## 1. Authorization and hard stop

Historical second-recovery work was limited to:

```text
WP-25 Step 1 second bounded recovery
    -> expand open-world Source Manifest for the remaining Senior findings
    -> trace current owners, superseding/representation amendments and machine/test consumers
    -> correct maintenance semantic-outcome naming
    -> update failure horizon / cascading attacks / later research questions only where owner evidence requires
    -> rerun mandatory whole-project Step-1 critic on the full graph
    -> mechanically repair resolvable Step-1 BLOCKING/SIGNIFICANT/MINOR framing defects
    -> publish/read back/exact-head verify
    -> STOP for mandatory independent Senior Step-1 re-re-review
```

Current post-review authorization is now:

```text
WP25_STEP2_AUTHORIZED: YES
WP25_STEPS_2_8_AUTHORIZED: YES
IMPLEMENTATION_PLANNING_AUTHORIZED: NO
NEXT_WP_AUTHORIZED: NO
NEXT_MANDATORY_GATE: independent WP-25 final Senior review after complete Step 8
```

Still not authorized:

```text
implementation planning
substantive implementation
runtime/schema/test realization
release or migration execution
next WP
gameplay/campaign bootstrap
```

## 2. Problem statement

HDM already has native outcome and failure semantics distributed across domain owners. WP-25 must later compose those outcomes without creating a universal error authority or flattening materially different failure, capability, readiness, compatibility and recovery states.

The full Step-1 problem horizon therefore includes at least:

```text
native outcome / failure cause
truthful surviving frontier
effective severity
gameplay impact
affected scope / blast radius
risk if ignored
legal continuation
temporal tolerance / semantic fence
bounded recovery
retry / idempotency semantics
prohibited fallback
recipient-safe user-visible disposition
verification / empirical-acceptance obligation
```

Required separation remains:

```text
FAILURE CAUSE
!= EFFECTIVE SEVERITY
!= GAMEPLAY DISPOSITION
!= RETRY POLICY
```

Starting effective severity vocabulary remains:

```text
S0 NOTICE
S1 DEGRADED
S2 GUARDED
S3 QUARANTINED
S4 CRITICAL
```

Severity is context-derived. `UNSUPPORTED` is an orthogonal capability/deployment/compatibility disposition, not shorthand for `S4`.

## 3. Product Owner direction

Mandatory direction inputs remain:

- `DEV/docs/superpowers/specs/2026-09-08-hdm-wp25-failure-degradation-durability-risk-owner-direction.md`;
- full `PO-008` in `DEV/PRODUCT_OWNER_INPUT.md`.

Accepted direction remains:

```text
OWNER-LOCAL NATIVE OUTCOMES
+ EPHEMERAL CROSS-OWNER FAILURE DISPOSITION
+ SCOPE-AWARE CONTINUATION
+ RISK-TRAJECTORY-AWARE DURABILITY PROTECTION
```

These inputs constrain WP-25 but are not substitutes for native semantic owners.

## 4. Goals

1. Preserve every materially distinct native failure/outcome space needed by WP-25.
2. Keep cross-owner failure composition ephemeral and non-authoritative unless a later owning decision proves persistence necessary.
3. Preserve exact authority/currentness, accepted mechanics/RNG, agency, disclosure and stable-identity invariants.
4. Distinguish package/set identity reconstruction failure from catalog capability gaps, execution validation failure, compatibility/migration results and ordinary gameplay outcomes.
5. Distinguish provisional local mechanical sufficiency, exact local mechanic blocking, READY_PC closure and package compilation failure.
6. Preserve storage-baseline authority separately from campaign creator/gameplay publication authority and from an existing campaign's adopted runtime.
7. Preserve maintenance routing/authorization/disclosure distinctions while treating current labels as semantic outcome categories rather than exact installed machine enum vocabulary.
8. Classify stale runtime/test realization as debt rather than accepted architecture authority.
9. Preserve proof-class separation and bounded-operation constraints.
10. Leave no mechanically resolvable BLOCKING/SIGNIFICANT Step-1 source/framing omission before the next Senior gate.

## 5. Non-goals

Step 1 does not:

- choose the final WP-25 disposition schema or master taxonomy;
- create a persisted global failure registry;
- create a new ruleset-package, catalog, readiness, storage, lifecycle, maintenance or recovery authority;
- turn failed attacks/checks/saves or other resolved gameplay outcomes into system failures;
- select exact host-capacity/time/token/message thresholds;
- create generic retry counts, schedulers, queues, heartbeats or workers;
- implement or repair runtime/schema/test realization;
- implement the proposed maintenance command surface;
- perform migration/release/runtime execution.

## 6. Existing invariants carried into WP-25

1. Native owners remain authoritative for their own outcomes and transitions.
2. Cross-owner failure composition does not reinterpret native results.
3. LLM prose/chat memory/Story/checkpoints/planning/indexes/caches/diagnostics are not campaign authority.
4. Accepted IDs and accepted exact ruleset-set identity are not silently replaced during recovery.
5. Accepted mechanics/RNG and voluntary player action are not replayed/rerolled/reinvented merely to repair transport, persistence or presentation.
6. Ordinary resolved gameplay failure is not system failure absent a separate native system failure.
7. Missing required evidence is not guessed; Context `UNSATISFIABLE` remains fail closed.
8. Publication/currentness remains non-force, exact-source/current-authority based; ambiguous authority-changing publication is never blind-retried.
9. Force push/ref rewind and HDM branch/ref deletion remain prohibited.
10. Git/arrival/timestamp order never creates fictional authority.
11. Recovery begins from current native authority and bounded required closure.
12. Unsupported/indeterminate compatibility fails closed; version order or ancestry alone never manufactures compatibility/migration.
13. Catalog search miss != proven capability gap; registered/dormant capability != active executable authority.
14. House-Rule/adjudication evidence is exact; missing is not false and stale/unauthorized/invalid inputs retain native typed outcomes.
15. Maintenance routing != authorization; authorization != recipient disclosure eligibility; diagnostic/error text != gameplay/recovery/currentness authority.
16. Generator/scaffold/initial-publication failure does not authorize LLM/per-file scaffold reconstruction or setup against a partial scaffold.
17. Campaign selection is explicit and preselection work is bounded.
18. Provisional gameplay may continue when the bounded local mechanic dependencies for the proposed outcome are sufficient.
19. An attempted mechanic whose exact local dependencies are insufficient is blocked locally; this does not by itself mean READY_PC is globally failed.
20. READY_PC false != package compilation failure; an initializing campaign is not globally failed merely because one local capability/dependency is absent.
21. Storage owner authority over `DND_STORAGE.engine.baseline` != campaign creator authority != gameplay publication authority.
22. Existing campaign runtime comes from `MANIFEST.engine.current`, never storage baseline.
23. Failed/rejected/indeterminate save-and-exit persistence does not permit clearing the strongest truthful recovery-safe selected-campaign context or claiming success.
24. Story failure/lag cannot replace native canon.
25. Ordinary recovery/diagnostics remains bounded; no WORLD/history/all-ref/all-LIVE scan is introduced.
26. No hidden background correctness worker/heartbeat is introduced.
27. Architecture coverage != machine realization != verification realization != empirical acceptance.

## 7. Durability / host-capacity framing

Two reasons for preservation remain distinct:

```text
CORRECTNESS HARD
    required postcondition of a named semantic edge

OPERABILITY / LOSS-PROTECTION FENCE
    coherent HOT/SOFT state remains semantically valid,
    but further single-copy unpublished exposure has become unacceptable risk
```

Risk trajectory remains conceptually:

```text
NORMAL
ELEVATED
DANGER
```

Exact thresholds remain open pending applicable evidence. Advisory capacity signals cannot become truth/currentness/authorization authority.

### 7.1 Stale one-hour realization debt

Current semantic authority remains Step-5.5 + WP-13 + accepted WP-25 direction. The following current GAME/test surfaces still project the retired one-hour proxy and are **stale realization debt**, not current product law:

- `GAME/CORE/DURABILITY_GUARD.md`;
- `GAME/CORE/SESSION.md`;
- `GAME/CORE/STORAGE.md` — its hot-frontier and working-set sections still reference the one-hour dirty-state ceiling;
- `DEV/TESTS/test_hourly_durability_contract.py`.

`STORAGE.md` remains authoritative for storage topology/read/working-set ownership where not superseded, but its one-hour durability wording is not authority over current Step-5.5/WP-13/WP-25 durability semantics.

## 8. Required failure horizon for later authorized work

The Step-1 graph must support at least:

1. host capability unavailable/degraded;
2. stale/currentness/moved authority;
3. authentication/identity/eligibility/control failure;
4. malformed/contradictory/dangling/integrity-defective native state;
5. Context degraded/`UNSATISFIABLE`;
6. publication rejection/ambiguity/partial success;
7. recovery source absence/incompatibility/exhaustion;
8. LIVE ownership/currentness/conflict ambiguity;
9. collaboration currentness/required-contribution failure while ordinary waiting remains non-failure;
10. compatibility/migration unsupported/indeterminate/path failure;
11. Story/planning/derived-state lag/stale basis/optional unavailability;
12. presentation/render/disclosure interruption after accepted semantics;
13. diagnostics/cleanup proof unavailable/indeterminate;
14. runtime-package/instruction-basis mismatch/loss/mixed-runtime risk;
15. exact ruleset package/set load or reconstruction failure;
16. catalog-context incompatibility with preserved native reason;
17. proven unsupported-capability/gap evidence distinct from search miss;
18. dormant/nonselectable/quarantined executable capability;
19. compiler/primitive validation rejection;
20. House-Rule policy conflict/realization gap;
21. adjudication input missing/unauthorized/invalid/stale and realization-reference defects;
22. maintenance authorization/currentness/recipient-withholding/unrealized-capability semantic outcomes;
23. bootstrap/selection/generator/initial-materialization/publication failure;
24. provisional local dependency insufficiency, READY_PC not-yet-satisfied and package compilation failure as separate conditions;
25. storage-baseline/runtime-selection/authority mismatch;
26. save-and-exit rejection/ambiguity/context-preservation requirement;
27. compound/cascading combinations of the above.

## 9. Exact ruleset identity / catalog-context distinction — SR25-S1-01 second recovery

`DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` is the canonical semantic owner for package snapshot identity, exact resolved-set identity and catalog-context fingerprint semantics. `RULESET_PACKAGE_MACHINE_CLOSURE.md` is the machine realization/closure owner and explicitly delegates identity semantics to it.

Current representation is amended by `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md` without replacing the underlying identity/authority semantics.

Required identity chain:

```text
RulesetPackageManifest + exact semantic bytes
    -> RulesetPackageSnapshot(content_sha256)

exact cycle-free dependency closure
    -> ResolvedRulesetSnapshotSet(
         ruleset_set_digest_generation,
         ruleset_set_sha256)

engine capability identity + exact typed ruleset set
+ campaign definition frontier + optional overlay frontier
    -> catalog_context_fingerprint
```

The catalog-context fingerprint is comparison/retry evidence, not a global state authority.

Current shipped machine owner `GAME/TOOLS/ruleset_package.py` has the closed load/reconstruction reason set:

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

Those reasons may be surfaced through the registered top-level `failure.catalog_context_incompatible` execution failure, but the reason distinctions remain native evidence and must not be erased by WP-25.

Additional distinctions:

```text
ruleset package/set load/reconstruction failure
    != runtime.catalog_gap_report
    != dormant/nonselectable capability
    != primitive/compiler rejection
    != same/different compatibility-generation result
    != WP-20 migration/adoption disposition
    != ordinary gameplay failure
```

Accepted Resolution/Continuation state pins `ruleset_set_digest_generation`, `ruleset_set_sha256`, `catalog_context_fingerprint_generation` and `catalog_context_fingerprint`. If accepted work's exact typed ruleset-set identity cannot be reconstructed, the current owner requires a **finite compatibility/prerequisite failure**. It forbids fuzzy substitution, current-package reinterpretation, mixed partial context and hidden migration.

Compatibility/migration remains separately owned: package revision/order is not compatibility; same compatibility generation is only eligibility for semantic proof; different generation/incompatible/diverged/ambiguous evidence routes through explicit adoption/migration/unsupported owners. Source ancestry, same-version equality or version labels are never standalone compatibility proof.

## 10. Deterministic execution / House Rules distinctions retained

Existing first-recovery distinctions remain valid:

```text
failure.catalog_context_incompatible
    != runtime.catalog_gap_report
    != DORMANT_NONSELECTABLE / quarantined realization
    != compiler or primitive validation rejection
    != ordinary gameplay action/check/save result

failure.policy_conflict
    != failure.policy_realization_gap
    != failure.adjudication_input_missing
    != failure.adjudication_input_unauthorized
    != failure.adjudication_input_invalid
    != failure.adjudication_context_stale
    != missing/stale/incompatible/dormant realization reference
```

No registered ID, package member, policy reference or physical byte grants execution authority by existence alone.

## 11. Maintenance/support distinction — SR25-S1-02 remains closed + Senior minor repair

`DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` remains the current DEV maintenance semantic/support contract and explicitly remains **not an installed runtime command surface**.

Preserve:

```text
operation routing != authorization
authorization != disclosure eligibility
diagnostic/error text != gameplay/recovery/currentness authority
```

The labels below are **required semantic outcome categories / semantic outcomes**, not an already established exact runtime machine enum vocabulary:

```text
NOT_AUTHORIZED
NOT_CURRENT_OR_UNRESOLVED
WITHHELD_OR_REDACTED
UNAVAILABLE_NOT_REALIZED
```

The maintenance owner explicitly permits a future authorized realization to choose exact machine enum names while preserving these semantics. Recipient-ineligible detail remains withheld/redacted; denial/unavailability creates no gameplay chronology/state merely to record the outcome.

`SR25-S1-02` remains PASS/CLOSED; this second recovery does not reopen it.

## 12. Bootstrap / READY_PC / storage distinction — SR25-S1-03 second recovery

WP-19 remains the bootstrap/creation composition owner; `CHARACTER_PROGRESSION_READY_PC_SEED.md` and `GAME/CORE/CHARACTER_READINESS.md` supply the current mechanical-readiness owner chain.

Required distinction:

```text
PROVISIONAL GAMEPLAY WITH SUFFICIENT LOCAL DEPENDENCIES
    proposed bounded outcome may proceed

ATTEMPTED MECHANIC BLOCKED BY EXACT LOCAL DEPENDENCY
    only that mechanical boundary/capability is blocked;
    do not guess missing mechanics

READY_PC NOT YET SATISFIED
    initial mechanical commitment frontier remains open;
    campaign/PC may remain honestly provisional/initializing

PACKAGE COMPILATION FAIL-CLOSED
    unresolved package definition/activity/asset/resource/proficiency/value ref,
    quarantined primitive, duplicate/illegal binding/choice, failed prerequisite,
    catalog-context mismatch, or other compiler closure defect
```

These are not one generic readiness error. READY_PC is dependency closure, not questionnaire completion and not a prerequisite for all provisional fiction/gameplay. A local missing capability does not globally fail the initializing campaign.

READY_PC evidence is bound to Actor identity/revision plus exact ruleset-set/catalog identity. Stale digest generation, missing transitive evidence, invalid spell binding or forged/unbound readiness evidence returns exact blockers rather than invented state.

### 12.1 Storage/runtime authority separation

`GAME/CORE/STORAGE.md` is the current primary storage/bootstrap persistence surface, while `PERSISTENCE.md` owns write transaction/transport semantics.

Preserve:

```text
DND_STORAGE.engine.baseline
    = storage-owner-approved portable runtime identity for NEW campaigns only

storage-owner authority
    != campaign creator authority
    != gameplay publication authority

existing campaign runtime
    = MANIFEST.engine.current
    != DND_STORAGE.engine.baseline

current_runtime_root
    = ephemeral local validated runtime path
    != either persistent identity authority
```

Only the authenticated storage owner may persist storage baseline changes. Singleplayer gameplay writes remain creator-authorized; multiplayer gameplay publication remains under its own PLAYER/LIVE authority; campaign engine adoption remains creator-authorized. Repository permission alone is insufficient application authority.

Storage-baseline and three-runtime-identity semantics are current only where incorporated by later current owners such as `STORAGE.md`, `BOOTSTRAP_RUNTIME.md`, `ENGINE_UPDATES.md`, `dnd_storage.schema.yaml`, campaign manifest/runtime identity schemas and executable tests. `DEV/docs/superpowers/specs/2026-08-18-runtime-selection-and-storage-baseline-amendment.md` is retained as **HISTORICAL / PARTIALLY SUPERSEDED DESIGN AMENDMENT / PROVENANCE**. Its older same-version runtime-refresh and ancestry/equality compatibility assumptions are not current compatibility authority after the 2026-09-05 versioning policy and final WP-20.

### 12.2 Bootstrap/save-exit semantics retained

```text
explicit campaign/new-game selection barrier
    -> bounded preselection evidence only

New Game
    -> exact selected runtime/package generator once
    -> complete scaffold
    -> one initialization tree/commit
    -> non-force create-if-absent publication
    -> only confirmed success permits setup against that scaffold

generator unavailable/failed OR scaffold incomplete OR publication fails
    -> no LLM reconstruction
    -> no partial per-file substitute
    -> no successful campaign creation/setup against partial scaffold

save-and-exit
    -> save closure first
    -> only confirmed durable closure permits clearing selected gameplay context
```

Rejected/indeterminate save publication retains the strongest truthful recovery-safe selected-campaign context until native publication/recovery semantics resolve it.

## 13. Cascading-failure attack routes

Later authorized work must attack at least:

- recovery fails while native currentness moves;
- repair succeeds locally but publication is indeterminate;
- remote publication succeeds but local adoption/rebind fails;
- retry reaches owner-bounded exhaustion;
- PLAYER/LIVE/creator/storage-owner authorization changes during recovery/maintenance;
- migration prepares successfully but authority moves before publication;
- accepted remote migration cannot rebind/rehydrate locally;
- accepted mechanics/RNG exists but persistence/presentation fails afterward;
- accepted semantics exist but rendering/disclosure delivery fails;
- Story/planning regeneration fails while native sources remain usable;
- cleanup evidence becomes stale during assessment;
- host-risk state moves toward DANGER while unpublished established state grows;
- instruction/package basis mismatch appears during continuation;
- accepted Resolution/Continuation needs exact prior `ruleset_set_sha256` but that set cannot be reconstructed: finite failure, no current-package reinterpretation;
- exact package manifest/member/dependency closure fails for one of the current native 11 reasons;
- ruleset set loads but compatibility/adoption proof is insufficient: do not collapse load success into compatibility success;
- true capability gap is proved while a similarly named capability is merely dormant/nonselectable;
- primitive compilation fails in a nested dependency: no partial mutation/event escapes;
- House-Rule policy remains active but realization reference is missing/stale/incompatible/quarantined;
- adjudication input was accepted under one exact rules/policy basis and that basis becomes stale before retry;
- maintenance routes correctly but principal/currentness cannot be proved: deny without mutation/sensitive disclosure;
- authorized maintenance output contains recipient-ineligible detail: withhold/redact without changing campaign truth;
- maintenance semantic contract exists but installed runtime command realization does not: do not invent dispatcher semantics;
- new-game generator succeeds locally but initial publication is rejected/ambiguous: no setup against prepared/unpublished scaffold;
- one plausible campaign exists before explicit selection: no implicit preload/recovery/update;
- provisional PC can support dialogue/movement but not an attack with unresolved exact attack dependencies: block only the attack boundary;
- READY_PC is false because one material initial choice is open while unrelated safe provisional play remains possible;
- package compilation fails closed: do not reframe it as ordinary READY_PC incompleteness;
- storage baseline points to runtime B while an existing campaign MANIFEST requires runtime A: campaign A remains authoritative; baseline cannot override it;
- storage owner may update NEW-campaign baseline but lacks campaign creator/gameplay publication authority solely by storage ownership;
- `STORAGE.md` one-hour wording conflicts with current Step-5.5/WP-13/WP-25 durability law: classify stale realization, do not revive timer authority;
- save-and-exit is locally complete but publication is rejected/indeterminate: selected recovery-safe context remains.

## 14. Quality attributes for later alternatives

- semantic correctness / truthful frontier;
- exact ruleset identity and accepted-work reproducibility;
- authority/currentness safety;
- bounded recovery/retry safety;
- local-dependency/readiness precision;
- storage/campaign authority separation;
- deterministic-rules/admission fidelity;
- agency/disclosure safety;
- bootstrap/creation atomicity;
- progress-loss containment;
- graceful local degradation rather than unnecessary campaign-global blocking;
- bounded ordinary-operation cost;
- debuggability/actionability without secret leakage;
- implementation reversibility/complexity;
- verification and empirical testability.

## 15. Open-world Source Manifest

Inspection vocabulary:

- `FULL` — current substantive task-relevant contract inspected.
- `TARGETED` — task-relevant owner/consumer portions inspected.
- `STRUCTURAL` — family/tree routed and selected material members inspected.

### 15.1 Process/current-stage/PO authority

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| `AGENTS.md` | repository/process authority | bootstrap, Connector-only transport, write/version/gate rules | FULL |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | runtime overlay | publication/currentness/verification mechanics | FULL |
| `DEV/DESIGN_PROCESS.md` | canonical design process | Source Manifest, critic, evidence completeness | FULL |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | HDM process adapter | whole-project critic + Senior stop | FULL |
| `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md` | PO-input process | PO direction vs semantic ownership | FULL |
| `DEV/PROJECT_MAP.md` | dependency locator | full open-world graph reconstruction | FULL |
| `DEV/CURRENT_PROGRESS.md` | global status authority | second Senior HOLD/recovery gate + post-review GO routing | FULL |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | sequencing | WP-25 placement | TARGETED |
| `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | derivative owner locator | routing only | TARGETED |
| `DEV/RELEASE/VERSIONING.md` | version-impact projection | Step-1 docs/status => no bump | FULL |
| WP-25 owner-direction spec + `PO-008` | Product Owner input | multidimensional failure/durability direction | FULL |

### 15.2 Durability/publication/recovery/integrity

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| Step-5.5 soft/hard-save durability canonical spec | canonical owner | `ESTABLISHED != DURABLE`, HARD/SOFT | FULL |
| WP-13 durability/save/publication canonical spec | canonical owner | publication/currentness/ambiguity | FULL |
| WP-14 recovery/checkpoint/session repair canonical spec | canonical owner | bounded recovery outcomes/current-authority-first | FULL |
| supported-ref publication/currentness amendment | canonical amendment | non-force/current closure | FULL |
| Step-5.14 integrated recovery/concurrency owner | integration owner | cascading recovery laws | FULL |
| `GAME/CORE/SAVE_CONTRACT.md` | runtime consumer | save completeness/truthful success | FULL |
| `GAME/CORE/PERSISTENCE.md` | runtime transport consumer | transaction/publication realization | FULL |
| `GAME/CORE/INTEGRITY.md`, `RUNTIME.md` | runtime consumers | integrity/recovery integration | FULL |
| `GAME/CORE/DURABILITY_GUARD.md`, `SESSION.md`, `STORAGE.md` | mixed current/stale runtime projections | storage/session semantics plus retired one-hour wording | FULL |
| `DEV/TESTS/test_hourly_durability_contract.py` | stale executable projection | retired one-hour timer law | FULL |

### 15.3 Context/host/instruction basis

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| R2.3 Context Runtime canonical spec | canonical owner | degraded/UNSATISFIABLE | FULL |
| R2.4 single-context execution | canonical owner | no hidden worker | FULL |
| R2.6 host assurance | canonical owner | host capability/proof boundary | FULL |
| WP-08 role/context instruction realization | realization owner | exact package cache/rehydration | FULL |
| WP-09 context-loading/resource bounds | realization owner | bounded context operations | FULL |
| WP-22 verification + WP-24 performance specs | proof/bounds owners | architecture vs machine vs empirical | FULL |

### 15.4 Authority/LIVE/collaboration/disclosure

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | authorization owner | creator/PLAYER/maintenance fail closed | FULL |
| `DEV/ARCHITECTURE/BRANCH_MODEL.md` | routing projection | storage/campaign/ref topology | FULL |
| creator-login continuity decision | PO decision | unresolved creator fail closed | FULL |
| branch/ref deletion prohibition decision | PO decision | no deletion/rewind | FULL |
| WP-16 multiplayer/LIVE spec | canonical owner | LIVE currentness/partial freeze | FULL |
| WP-17 collaboration/agency spec | canonical owner | dependent-scope blocking/no invented action | FULL |
| Step-5.12 delivery/disclosure spec | canonical owner | recipient eligibility/presentation repair | FULL |
| `GAME/CORE/LIVE_SCENE.md`, `MULTIPLAYER.md`, `CHRONOLOGY.md` | runtime consumers | currentness/conflict/partial chronology | FULL |

### 15.5 Ruleset identity, catalog/admission, deterministic mechanics — SR25-S1-01

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` | **canonical identity owner** | exact package snapshot/set identity, catalog-context fingerprint, finite reconstruction failure | FULL |
| `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md` | superseding representation amendment | package revision/family/generation + digest-generation representation | FULL |
| `DEV/ARCHITECTURE/RULESET_PACKAGE_MACHINE_CLOSURE.md` | machine closure owner | loader/lock/compatibility realization delegating identity semantics | FULL |
| `DEV/ARCHITECTURE/CATALOG_ADMISSION.md` | catalog admission owner | admitted/dormant/gap/incompatibility distinctions | FULL |
| `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md` | catalog resolution owner | exact context resolution/bounded discovery | FULL |
| `DEV/ARCHITECTURE/ACTIVITY_MODEL.md` | execution owner | invocation/retry/gameplay outcome distinction | FULL |
| `DEV/ARCHITECTURE/ACTIVITY_PRIMITIVE_CONTRACTS.md` | primitive owner | active/dormant/compiler validation | FULL |
| `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md` | deterministic input owner | selectors/accessors/adjudicated input | TARGETED |
| `GAME/RULES/.../ruleset-package-manifest.json` | package machine declaration | current package identity inputs | FULL |
| `GAME/TOOLS/ruleset_package.py` | shipped builder/loader | closed 11-reason load/reconstruction taxonomy | TARGETED/FULL TASK ROUTE |
| `DEV/TOOLS/validate_ruleset_package_closure.py` | build/conformance orchestrator | engine-contract inventory/validator reconstruction failure | TARGETED |
| `DEV/SCHEMAS/resolved-ruleset-lock.schema.json` | machine schema | exact typed resolved-set evidence | FULL |
| `DEV/SCHEMAS/runtime-resolution-state.schema.json` | accepted-work schema | exact set/context identity on Resolution | FULL |
| `DEV/SCHEMAS/runtime-continuation-state.schema.json` | accepted-work schema | exact set/context identity across suspension/resume | FULL |
| `DEV/TESTS/test_s6d_11_ruleset_package_closure.py` | executable consumer | exact lock, native 11 reasons, evidence/compatibility failure | TARGETED/FULL MATERIAL TESTS |
| catalog/primitive/execution conformance test families | executable consumers | admission/compiler/native outcome realization | STRUCTURAL |

### 15.6 House Rules/adjudication

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` | policy owner | policy/currentness/adjudication authority | FULL |
| `DEV/ARCHITECTURE/HOUSE_RULES_MECHANICAL_BOUNDARY.md` | execution-boundary owner | typed accepted input/native validation | FULL |
| `GAME/CORE/ADJUDICATION.md` | runtime adjudication owner/consumer | ordinary gameplay outcomes + frozen accepted inputs | FULL |
| `DEV/CATALOG/house-rules-mechanical-boundary.json` | machine projection | exact policy/realization links | FULL |
| House Rules schemas/tests | machine/executable consumers | conflicts/gaps/input failure/reference failure | TARGETED/STRUCTURAL |

### 15.7 Maintenance/support — SR25-S1-02 closed + minor repair

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` | current DEV semantic support contract | routing/auth/disclosure/unrealized semantic outcomes; future enum names open | FULL |
| `ACCESS_CONTROL.md` + Step-5.12 | auth/disclosure owners | fail closed + recipient-safe output | FULL |
| `GAME/CORE/PLAY_POLICY.md`, `RUNTIME.md`, `SESSION.md`, `INTEGRITY.md` | runtime neighbors | non-gameplay maintenance/continuation | FULL |
| `DEV/TESTS/test_maintenance_continuation_contract.py`, access-control cases | executable/scenario consumers | no fictional progression; auth distinction | FULL/TARGETED |
| DEV maintenance audit tools/tests | support tooling | repository audit, not campaign maintenance authority | STRUCTURAL |

### 15.8 Bootstrap/READY_PC/storage/save-exit — SR25-S1-03

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| WP-19 bootstrap/campaign-creation/initial-materialization canonical spec | composition owner | selection/generator/publication/readiness/save-exit | FULL |
| campaign-exit owner decision | PO/canonical decision | save closure/context preservation | FULL |
| `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md` | **canonical S6D-07 owner** | provisional/local sufficiency/READY_PC/package compile distinctions | FULL |
| `GAME/CORE/CHARACTER_READINESS.md` | runtime readiness owner | local mechanic dependency barrier + READY_PC predicate | FULL |
| `GAME/RULES/.../character-capabilities.json` | capability breadth projection | `ABSENT_NONSELECTABLE`, no identity authority | FULL |
| `DEV/TOOLS/validate_character_mvp_seed.py` | machine conformance tool | package compiler vs readiness evaluator | TARGETED |
| `DEV/TESTS/test_s6d_07_character_mvp_seed.py` | executable consumer | exact blockers, provisional play, stale identity, package closure | FULL MATERIAL TESTS |
| `GAME/CORE/STORAGE.md` | **current storage/bootstrap persistence owner** | baseline/current runtime/authority separation; stale timer debt | FULL |
| `DEV/docs/superpowers/specs/2026-08-18-runtime-selection-and-storage-baseline-amendment.md` | **HISTORICAL / PARTIALLY SUPERSEDED DESIGN AMENDMENT / PROVENANCE** | current only for storage-baseline / three-runtime-identity semantic portions incorporated by later current owners; **not current compatibility authority** | FULL / CURRENT PORTIONS RECONCILED |
| `GAME/SCHEMA/dnd_storage.schema.yaml` | persistent schema | NEW-only baseline/storage-owner writes | FULL |
| `DEV/TESTS/test_runtime_identity_schema.py` | executable consumer | storage baseline schema + campaign current identity | FULL |
| `DEV/TESTS/test_engine_update_policy_contract.py` | executable consumer | baseline/campaign authority independence | FULL |
| `GAME/INSTALL/00_DND_BOOTSTRAP.md`, `BOOTSTRAP_RUNTIME.md` | runtime bootstrap consumers | selection then existing-current/new-baseline resolution | FULL |
| `NEW_CAMPAIGN_FAST_PATH.md`, `CAMPAIGN_SETUP.md`, `init_campaign.py` | creation consumers | generator-first/atomic scaffold publication | FULL |
| `SAVE_CONTRACT.md`, `SESSION.md`, `PERSISTENCE.md` | save-exit neighbors | truthful durable closure | FULL |
| bootstrap/storage/save/readiness scenario/test families | executable/scenario consumers | selection/generator/no-fallback/readiness/save semantics | FULL/STRUCTURAL |

### 15.9 Compatibility/update/package/release

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md` | current canonical compatibility/versioning owner | compatibility identity axes; ancestry/equality are not standalone compatibility proof | FULL |
| WP-20 engine update/schema evolution/migration spec | canonical owner | compatibility/migration/currentness | FULL |
| `GAME/CORE/ENGINE_UPDATES.md` | runtime consumer | exact campaign runtime/mismatch recovery | FULL |
| WP-23 package/version/release readiness spec | canonical owner | exact package/provenance/proof | FULL |

### 15.10 Story/diagnostics/scale and general machine consumers

| Source | Role | Relevance | Inspection |
|---|---|---|---|
| WP-18 Story spec + Story integration contract | Story owners/consumer contract | derived/noncanonical lag/failure | FULL |
| WP-21 diagnostics/cleanup spec | canonical owner | diagnostics nonauthority/UNKNOWN | FULL |
| WP-22 verification spec | proof owner | completeness/evidence classes | FULL |
| WP-24 performance/scale spec | boundedness owner | no global scans/unowned SLA | FULL |
| `GAME/SCHEMA/*.schema.yaml`, selected LIVE/checkpoint/current/manifest schemas | machine family | avoid accidental authority/global error bucket | STRUCTURAL/TARGETED |
| `DEV/TESTS/` | executable/scenario family | realization consumers | STRUCTURAL |
| publication ref-fence + engine mismatch recovery tests | executable consumers | currentness/recovery | FULL |
| `.github/workflows/validate.yml` | hosted CI | exact-head maintenance audit + DEV unit tests | FULL |

## 16. Source-role reconciliation / current-owner rules

1. `RULESET_PACKAGE_IDENTITY.md` owns package/set identity semantics; machine closure realizes them and cannot replace the owner.
2. The 2026-09-05 versioning policy amends representation/version namespaces but preserves exact identity/content-addressing semantics and is current compatibility authority together with final WP-20 where update/migration semantics apply.
3. The 2026-08-18 runtime-selection/storage-baseline amendment is **HISTORICAL / PARTIALLY SUPERSEDED DESIGN AMENDMENT / PROVENANCE**. Only its storage-baseline / three-runtime-identity portions that are incorporated by later current owners remain applicable. Its same-version refresh, ancestry and equality assumptions do not independently prove compatibility.
4. The closed 11 load/reconstruction reasons remain native machine reason evidence even when surfaced through `failure.catalog_context_incompatible`.
5. WP-20 compatibility/migration outcomes are downstream/orthogonal to successful exact-set reconstruction and must not be collapsed into loader failure reasons.
6. Accepted Resolution/Continuation exact ruleset identity is fixed causal evidence; finite recovery failure is required if it cannot be reconstructed.
7. `CHARACTER_PROGRESSION_READY_PC_SEED.md` + `CHARACTER_READINESS.md` own progressive readiness distinctions; local dependency blocking does not imply global campaign failure.
8. `STORAGE.md` owns storage topology/baseline/current working-set semantics while `PERSISTENCE.md` owns write transport/transactions.
9. Storage baseline is NEW-only and storage-owner-controlled; existing campaigns use `MANIFEST.engine.current` under campaign authority.
10. `STORAGE.md` one-hour wording joins `DURABILITY_GUARD.md`, `SESSION.md` and the hourly test as stale realization debt under Step-5.5/WP-13/WP-25.
11. `MAINTENANCE_COMMANDS.md` labels are semantic outcomes/categories; future machine enum spelling remains open. `SR25-S1-02` remains closed.
12. Product Owner WP-25 direction constrains composition but does not replace native owners.
13. WP-16/live, access/disclosure, Story/diagnostics and proof-strength owners retain their prior precedence.
14. Stale/incomplete/unrealized realization is not automatically architecture conflict.

## 17. Step-2 research questions prepared by Step 1

Mandatory Senior Step-1 re-re-review has now given GO. Step 2 must answer with evidence, without limiting itself to this prepared list:

1. What minimal ephemeral cross-owner disposition composes native outcomes without becoming a second authority?
2. Which inputs derive `S0..S4` contextually and which remain owner-specific?
3. How do gameplay impact/blast radius/risk/tolerance/frontier compose across local, campaign and deployment failures?
4. What bounded retry/idempotency semantics apply to confirmed rejection, indeterminate authority-changing operation, reassembly, local post-remote adoption failure and exhaustion?
5. How does `UNSUPPORTED` compose without becoming universal terminal severity?
6. How should NORMAL/ELEVATED/DANGER derive from unpublished exposure and advisory host-risk evidence without fictitious capacity precision?
7. Which user-visible dispositions are actionable and recipient-safe?
8. What machine/test/empirical proof obligation corresponds to each material disposition?
9. How must exact package load/reconstruction reason, `failure.catalog_context_incompatible`, capability gap, dormant capability, compiler rejection and ordinary gameplay failure compose without flattening?
10. When accepted work pins an exact ruleset set that cannot be reconstructed, what truthful frontier and bounded finite recovery/user disposition follows under identity + recovery + compatibility owners?
11. How should compatibility/migration outcomes compose after successful exact-set reconstruction versus when reconstruction itself fails?
12. What exact evidence proves capability unsupported rather than undiscovered/dormant/unselected?
13. How should House-Rule/adjudication failures freeze only dependent mechanical scope while preserving exact accepted basis across retry?
14. How should maintenance semantic outcome categories map to future user-visible/machine realization without treating current labels as frozen enum names?
15. How does maintenance failure preserve gameplay continuation without fictional/canonical mutation?
16. How should provisional local sufficiency, local mechanic blocking, READY_PC false and package compilation failure map to distinct gameplay dispositions/severities?
17. What local-scope continuation remains legal when one READY_PC dependency is missing but unrelated provisional play is supported?
18. How should storage baseline/current campaign/runtime-root authority distinctions affect bootstrap failure composition and recovery?
19. How should generator/scaffold/initial-publication failure preserve explicit selection and zero partial-scaffold authority?
20. After rejected/indeterminate save-and-exit publication, what exact selected-campaign context must remain until native recovery resolves the outcome?
21. Which stale one-hour runtime/test projections are later realization repairs under accepted durability law, including `STORAGE.md`, rather than architecture reopen evidence?

## 18. Whole-project critic result after second recovery

The mandatory critic was rerun against the full graph above, not only the Senior-listed deltas.

Result:

```text
RERUN_CRITIC_BLOCKING_FOUND: 0
RERUN_CRITIC_SIGNIFICANT_FOUND: 2
RERUN_CRITIC_MINOR_FOUND: 1

NEW_BLOCKING_BEYOND_SENIOR_FINDINGS: 0
NEW_SIGNIFICANT_BEYOND_SENIOR_FINDINGS: 0

UNRESOLVED_BLOCKING_AFTER_WORKER_REPAIR: 0
UNRESOLVED_SIGNIFICANT_AFTER_WORKER_REPAIR: 0
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
```

Worker dispositions:

```text
SR25-S1-01: REPAIRED / WORKER-CLOSED / PENDING INDEPENDENT SENIOR RE-RE-REVIEW
SR25-S1-02: PASS / CLOSED — RETAINED, NOT REOPENED
SR25-S1-03: REPAIRED / WORKER-CLOSED / PENDING INDEPENDENT SENIOR RE-RE-REVIEW
SENIOR_MINOR: REPAIRED / WORKER-CLOSED / PENDING INDEPENDENT SENIOR RE-RE-REVIEW
```

The detailed critic is recorded at:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-25-step-1-whole-project-critic.md`.

## 19. Framing falsifiability / reopen conditions

Reopen/revise only if evidence shows, for example:

- a native owner cannot express a required truthful outcome without a new shared persistent authority;
- exact accepted ruleset identity cannot be preserved under any bounded supported recovery and current owners do not define a legal disposition;
- READY_PC/local-dependency owners genuinely contradict bootstrap/lifecycle semantics rather than merely expose missing realization;
- storage baseline/campaign runtime authorities are contradictory after current amendments are applied;
- safe recovery requires a forbidden global scan/background dependency;
- accepted durability intent is physically unrealizable on a supported host and requires deployment restriction/architecture reopening;
- current owner evidence contradicts Product Owner direction in a genuinely human-owned way.

Implementation inconvenience, dormant/unrealized capability and stale projections alone are not reopen evidence.

## 20. Step-1 second-recovery handoff and final Senior gate result

Historical second-recovery handoff at `18fcf6efcada8a01c559362494291700ec4b637e` was:

```text
WP25_STEP1_SENIOR_RE_REVIEW_PREVIOUS_RESULT: HOLD — SECOND BOUNDED STEP-1 RECOVERY REQUIRED
WP25_STEP1_SECOND_BOUNDED_RECOVERY: COMPLETE AT WORKER LEVEL
WP25_STEP1_SENIOR_RE_RE_REVIEW: REQUIRED / PENDING
WP25_STEP2_AUTHORIZED: NO
IMPLEMENTATION_PLANNING_AUTHORIZED: NO
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
NEXT_AUTHORIZED_UNIT: NONE
NEXT_GATE: mandatory independent WP-25 Step-1 Senior re-re-review
```

Mandatory independent Senior Step-1 re-re-review of that exact checkpoint returned:

```text
SENIOR_RE_RE_REVIEW_VERDICT: GO WITH REQUIRED NON-BLOCKING SOURCE-ROLE CORRECTION
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED_NOW: NO
WP25_STEP2_AUTHORIZED: YES
WP25_STEPS_2_8_AUTHORIZED: YES
IMPLEMENTATION_PLANNING_AUTHORIZED: NO
NEXT_WP_AUTHORIZED: NO
NEXT_MANDATORY_GATE: independent WP-25 final Senior review after complete Step 8
SOURCE_ROLE_CORRECTION: APPLIED IN §12.1 / §15.8 / §15.9 / §16
```

No additional Step-1 Senior stop is required.

## 21. Version Impact

```text
VERSION_IMPACT: NONE
```

This non-blocking source-role correction changes design provenance/source authority classification only. It does not modify any version-bearing runtime module, persistent/protocol schema, campaign/storage/catalog/ruleset generation, package/release format, migration law or executable gameplay/runtime realization.
