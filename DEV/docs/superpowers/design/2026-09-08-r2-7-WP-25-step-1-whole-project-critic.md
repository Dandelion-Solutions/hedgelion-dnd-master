# R2.7 WP-25 Step 1 — Mandatory Whole-Project Task-Brief Critic

Status: **SECOND BOUNDED RECOVERY RERUN COMPLETE — PENDING MANDATORY INDEPENDENT SENIOR STEP-1 RE-RE-REVIEW**

Date: 2026-09-08

Senior re-review baseline: `865b4b16cfcca4f27104eaeb3eb13e72de87b750`

Scope: mandatory whole-project rerun of WP-25 Step-1 framing and open-world Source Manifest after the independent Senior re-review returned HOLD. This artifact is design provenance only. It does not authorize Step 2 or create a canonical WP-25 specification.

## 1. Recovery trigger

Senior re-review verdict supplied for the baseline:

```text
HOLD — SECOND BOUNDED STEP-1 RECOVERY REQUIRED
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 2
UNRESOLVED_MINOR: 1
HUMAN_DECISION_REQUIRED_NOW: NO
WP25_STEP2_AUTHORIZED: NO
IMPLEMENTATION_PLANNING_AUTHORIZED: NO
WHOLESALE_UPSTREAM_REOPEN_REQUIRED: NO
```

Senior finding state entering this rerun:

```text
SR25-S1-01: OPEN / SIGNIFICANT
    canonical ruleset-package identity owner omitted from deterministic rules graph

SR25-S1-02: PASS / CLOSED
    maintenance/support route accepted

SR25-S1-03: OPEN / SIGNIFICANT
    READY_PC owner + primary STORAGE owner omitted from bootstrap/readiness/storage graph

SENIOR_MINOR: OPEN / MINOR
    maintenance semantic outcomes were described too strongly as exact runtime vocabulary
```

The critic did not assume those findings were exhaustive.

## 2. Critic method

For every material native failure family the rerun reconstructed:

```text
native owner outcome/reason
    -> exact authority/currentness/evidence basis
    -> truthful surviving frontier
    -> severity inputs
    -> gameplay impact / affected scope
    -> legal continuation
    -> semantic fence / temporal tolerance
    -> bounded recovery / retry / idempotency
    -> prohibited fallback
    -> recipient-safe visible disposition
    -> verification / empirical obligation
```

Primary dependency routes independently rechecked:

```text
persistence/durability
    -> Step-5.5
    -> WP-13
    -> publication-currentness amendment
    -> WP-14
    -> Step-5.14
    -> STORAGE / PERSISTENCE / SAVE / SESSION / INTEGRITY
    -> durability/publication/save/storage tests

host/context
    -> R2.3 Context Runtime
    -> R2.4 single-context execution
    -> R2.6 host assurance
    -> WP-08 instruction/package cache
    -> WP-09 resource bounds
    -> WP-22/WP-24 proof and scale constraints

authority/LIVE/agency/disclosure
    -> ACCESS_CONTROL
    -> WP-16
    -> WP-17
    -> Step-5.12
    -> creator/ref owner decisions
    -> LIVE/MULTIPLAYER/CHRONOLOGY projections/tests

ruleset exact identity
    -> RULESET_PACKAGE_IDENTITY
    -> versioning representation amendment
    -> RULESET_PACKAGE_MACHINE_CLOSURE
    -> ruleset manifest / resolved lock
    -> Resolution + Continuation exact-set projections
    -> shipped loader / conformance orchestrator
    -> ruleset closure tests

catalog/deterministic execution
    -> CATALOG_ADMISSION
    -> CATALOG_RESOLUTION
    -> ACTIVITY_MODEL
    -> ACTIVITY_PRIMITIVE_CONTRACTS
    -> RULE_ELEMENT_MODEL
    -> catalog/primitive/execution machine/tests

House Rules/adjudication
    -> CAMPAIGN_HOUSE_RULES
    -> HOUSE_RULES_MECHANICAL_BOUNDARY
    -> ACCESS_CONTROL
    -> ADJUDICATION
    -> policy/binding schemas + tests

maintenance/support
    -> MAINTENANCE_COMMANDS
    -> ACCESS_CONTROL
    -> Step-5.12
    -> PLAY_POLICY / RUNTIME / SESSION / INTEGRITY
    -> maintenance/access tests

bootstrap/readiness/storage/save-exit
    -> WP-19
    -> campaign-exit decision
    -> CHARACTER_PROGRESSION_READY_PC_SEED
    -> CHARACTER_READINESS
    -> STORAGE
    -> runtime-selection/storage-baseline amendment
    -> INSTALL/BOOTSTRAP/NEW_CAMPAIGN/CAMPAIGN_SETUP
    -> generator / dnd_storage schema / runtime identity schemas
    -> character seed + bootstrap/storage/save tests

accepted mechanics -> persistence/presentation
    -> MECHANICS_INTEGRITY / RANDOMNESS / ADJUDICATION
    -> Step-5.12 / Step-5.14

update/package
    -> WP-20
    -> WP-08
    -> ENGINE_UPDATES
    -> WP-23

Story/diagnostics
    -> WP-18
    -> Story integration contract
    -> WP-21
    -> WP-22/WP-24
```

The critic keeps these categories distinct:

```text
accepted semantic-owner conflict
!= stale/incomplete realization
!= intentionally dormant/nonselectable capability
!= semantic contract whose runtime command surface is not realized
!= local READY_PC/dependency incompleteness
!= package/set reconstruction failure
```

## 3. Owner/consumer evidence expansion

### 3.1 SR25-S1-01 — exact ruleset identity owner

The first recovery included `RULESET_PACKAGE_MACHINE_CLOSURE.md` but omitted the owner to which that document explicitly delegates package/set identity semantics:

- `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` — canonical package snapshot/resolved-set/catalog-context identity owner;
- `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md` — superseding representation/version-namespace amendment while preserving exact identity semantics;
- `DEV/ARCHITECTURE/RULESET_PACKAGE_MACHINE_CLOSURE.md` — machine realization/closure owner;
- `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/ruleset-package-manifest.json` — current package declaration;
- `GAME/TOOLS/ruleset_package.py` — shipped exact builder/loader;
- `DEV/TOOLS/validate_ruleset_package_closure.py` — build/conformance orchestration;
- `DEV/SCHEMAS/resolved-ruleset-lock.schema.json` — typed exact-set evidence;
- `DEV/SCHEMAS/runtime-resolution-state.schema.json` and `runtime-continuation-state.schema.json` — accepted-work carriers of exact typed ruleset set and catalog-context identity;
- `DEV/TESTS/test_s6d_11_ruleset_package_closure.py` — exact identity/load/compatibility/reconstruction executable evidence.

The shipped loader's current closed load/reconstruction reasons are exactly:

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

`test_closed_load_failure_taxonomy` mechanically asserts that exact set.

The canonical identity owner further requires accepted Resolution/Continuation to retain the exact typed resolved-set identity. If that accepted set cannot be reconstructed, recovery terminates in a finite compatibility/prerequisite failure rather than substituting current package bytes, fuzzy matching, hidden migration or mixed partial context.

Reconciliation result:

```text
native ruleset load/reconstruction reason
    may map through failure.catalog_context_incompatible
    but reason semantics remain preserved

ruleset load/reconstruction failure
    != catalog capability gap
    != dormant capability
    != compiler/primitive validation rejection
    != ordinary gameplay outcome
    != compatibility/migration result
```

No duplicate package/global error authority is required.

### 3.2 SR25-S1-02 — maintenance remains closed

No contradictory evidence was found. `SR25-S1-02` remains PASS/CLOSED.

The current owner remains `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md`, with independent access/disclosure authority and no installed runtime parser/dispatcher command realization.

The second-recovery MINOR correction is precise: the owner says a future realization may choose exact machine enum names. Therefore:

```text
NOT_AUTHORIZED
NOT_CURRENT_OR_UNRESOLVED
WITHHELD_OR_REDACTED
UNAVAILABLE_NOT_REALIZED
```

are required **semantic outcome categories / semantic outcomes**, not frozen exact runtime enum vocabulary.

This correction changes no maintenance semantics and does not reopen SR25-S1-02.

### 3.3 SR25-S1-03 — READY_PC + storage owners

Missing canonical/current owners recovered:

- `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md` — canonical S6D-07 character/READY_PC owner;
- `GAME/CORE/CHARACTER_READINESS.md` — current runtime readiness owner;
- current package `character-capabilities.json` — bounded supported content projection with `ABSENT_NONSELECTABLE` policy and no identity authority;
- `DEV/TOOLS/validate_character_mvp_seed.py` — package compiler + readiness evaluator realization;
- `DEV/TESTS/test_s6d_07_character_mvp_seed.py` — exact readiness blocker/provisional-play/package closure evidence;
- `GAME/CORE/STORAGE.md` — current primary storage/bootstrap persistence surface;
- `DEV/docs/superpowers/specs/2026-08-18-runtime-selection-and-storage-baseline-amendment.md` — current baseline/runtime-identity amendment;
- `GAME/SCHEMA/dnd_storage.schema.yaml`;
- `DEV/TESTS/test_runtime_identity_schema.py`;
- `DEV/TESTS/test_engine_update_policy_contract.py`;
- existing bootstrap/generator/save owners and tests from the first recovery.

Recovered readiness distinction:

```text
provisional gameplay + sufficient exact local dependencies
    -> bounded outcome may proceed

attempted mechanic lacks exact local dependency
    -> only that mechanic boundary is blocked

READY_PC false
    -> initial mechanical commitment frontier is not yet closed
    -> does not prohibit all provisional gameplay

package compilation fail-closed
    -> package/definition/primitive/reference closure failed
    -> not merely READY_PC false
```

Tests confirm exact blockers such as unresolved material choice, stale ruleset digest generation, spell binding mismatch, missing transitive readiness evidence and forged/unbound readiness evidence while preserving provisional play where locally supported.

Recovered storage distinction:

```text
DND_STORAGE.engine.baseline
    = storage-owner-approved runtime identity for NEW campaigns only

MANIFEST.engine.current
    = runtime currently adopted by an existing campaign

current_runtime_root
    = ephemeral local validated package path
```

And authority separation:

```text
storage-owner authority
!= campaign creator authority
!= gameplay publication authority
```

`dnd_storage.schema.yaml` and runtime identity/update tests mechanically preserve that separation.

The critic also found a stale realization omission: `GAME/CORE/STORAGE.md` still names the retired one-hour dirty-state ceiling in hot-frontier/working-set wording. It belongs with `DURABILITY_GUARD.md`, `SESSION.md` and `test_hourly_durability_contract.py` as stale realization debt under current Step-5.5/WP-13/WP-25 durability semantics.

No new campaign lifecycle/error authority is needed.

## 4. Full-graph rerun finding summary

The critic independently reconstructed the whole graph rather than checking only the Senior deltas.

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
ACCEPTED_SEMANTIC_OWNER_CONFLICT_FOUND: NO
WHOLESALE_UPSTREAM_REOPEN_REQUIRED: NO
```

The two SIGNIFICANT findings are the two still-open Senior findings. The MINOR is the Senior maintenance naming correction. No additional BLOCKING/SIGNIFICANT omission was found.

## 5. Finding dispositions

### SR25-S1-01 — ruleset identity graph incomplete

Severity: **SIGNIFICANT — CONFIRMED**

Mechanical repair:

- canonical `RULESET_PACKAGE_IDENTITY.md` added as identity owner;
- versioning representation amendment and machine closure precedence reconciled;
- exact loader reason vocabulary and machine/test consumers added;
- accepted Resolution/Continuation exact set identity added to recovery horizon;
- finite reconstruction failure added;
- load/reconstruction vs catalog gap/dormancy/compiler/gameplay/compatibility distinctions added.

Disposition:

```text
SR25-S1-01: REPAIRED / WORKER-CLOSED / PENDING INDEPENDENT SENIOR RE-RE-REVIEW
```

### SR25-S1-02 — maintenance/support

No new contradictory evidence.

Disposition:

```text
SR25-S1-02: PASS / CLOSED — RETAINED / NOT REOPENED
```

### SR25-S1-03 — READY_PC/storage graph incomplete

Severity: **SIGNIFICANT — CONFIRMED**

Mechanical repair:

- canonical READY_PC owner and runtime/machine/test consumers added;
- provisional-local-sufficiency vs local mechanic block vs READY_PC false vs package compilation failure explicitly separated;
- `STORAGE.md` added as current storage/bootstrap owner;
- NEW-only baseline vs existing campaign current runtime vs ephemeral local root separated;
- storage-owner/campaign-creator/gameplay-publication authority separation added;
- `STORAGE.md` one-hour wording classified as stale realization debt;
- failure horizon/cascades/later questions updated without global campaign failure semantics.

Disposition:

```text
SR25-S1-03: REPAIRED / WORKER-CLOSED / PENDING INDEPENDENT SENIOR RE-RE-REVIEW
```

### Senior MINOR — maintenance outcome naming

Severity: **MINOR — CONFIRMED**

Mechanical repair:

Task Brief and critic now explicitly call the four maintenance labels semantic outcome categories/outcomes and record that exact machine enum names remain a future authorized realization choice.

Disposition:

```text
SENIOR_MINOR: REPAIRED / WORKER-CLOSED / PENDING INDEPENDENT SENIOR RE-RE-REVIEW
```

## 6. Regression against all prior Step-1 concerns

The rerun rechecked the original Step-1 critic and first bounded recovery:

1. **Second semantic authority risk:** closed; composition remains ephemeral and owner-local outcomes authoritative.
2. **Durability timer supersession:** closed and strengthened; `STORAGE.md` joins the known stale one-hour surfaces.
3. **Post-accepted mechanics/RNG:** closed; no reroll/replay for persistence/presentation repair.
4. **LIVE/ref currentness:** closed under WP-13/currentness amendment/WP-16/access/ref-deletion law.
5. **Package/instruction/migration basis:** closed and strengthened by exact ruleset identity owner inclusion.
6. **Derived state/diagnostics nonauthority:** closed.
7. **Host-capacity proof strength:** closed under R2.6/WP-22/WP-24.
8. **Deterministic catalog/admission/House Rules:** closed after exact identity owner repair; ordinary gameplay failure remains separate.
9. **Maintenance route:** remains closed; only naming precision changed.
10. **Bootstrap/scaffold/save-exit:** remains closed and strengthened by explicit READY_PC/storage owners.
11. **Ordinary collaboration waiting:** remains non-failure unless native dependent scope requires blocking.
12. **No global pending/error bucket:** remains intact.

## 7. Cascading/negative-invariant attack rerun

The repaired framing still forbids:

```text
guessing missing required evidence
silent source/authority substitution
chat/model memory as campaign authority
replacement accepted IDs or ruleset-set identity
reroll/replay of accepted mechanics/RNG
blind retry after ambiguous authority-changing publication
force push / ref rewind / branch-ref deletion
forbidden alternate repository transport
Git/LWW/arrival order as fictional authority
invented voluntary player action/consent/pass/speech
disclosure promotion from physical visibility
Story/planning/checkpoint/index/cache/diagnostics as missing-canon substitute
unbounded WORLD/history/all-ref/all-LIVE recovery scans
infinite retry/reassembly loops
hidden background correctness worker/heartbeat
silent activation of dormant/nonselectable capability
current-package reinterpretation of accepted work when exact historical ruleset set is unavailable
collapsing exact ruleset loader reason into capability gap or gameplay failure
collapsing successful exact-set load into compatibility/adoption success
LLM fallback for catalog/ruleset/compiler/adjudication evidence
classifying failed attack/check/save as generic system failure
maintenance routing as authorization
maintenance authorization as disclosure eligibility
recipient-ineligible diagnostics leakage
fictional state mutation merely to record maintenance denial/error
inventing exact maintenance enum vocabulary before realization owns it
LLM/per-file scaffold reconstruction after generator failure
setup against partial/unpublished initial scaffold
implicit campaign selection
inventing readiness/mechanics to force READY_PC
turning one blocked local mechanic into global campaign failure
using storage baseline to override existing MANIFEST.engine.current
using storage ownership as campaign creator/gameplay publication authority
reviving STORAGE/DURABILITY_GUARD/SESSION one-hour wording as current product law
clearing recovery-safe selected context after failed/rejected/indeterminate save-exit publication
```

No current owner requires relaxing these invariants.

## 8. Accepted owner conflict vs realization debt

Accepted semantic-owner conflicts found:

```text
0
```

Current stale/incomplete/intentionally unavailable realization debt/state relevant to WP-25 includes:

1. `GAME/CORE/DURABILITY_GUARD.md` — retired one-hour proxy.
2. `GAME/CORE/SESSION.md` — consumes retired one-hour proxy.
3. `GAME/CORE/STORAGE.md` — also contains retired one-hour proxy wording while remaining current for storage semantics.
4. `DEV/TESTS/test_hourly_durability_contract.py` — executable stale timer projection.
5. selected older LIVE/error/retry/presentation wording predating later owners.
6. maintenance semantic contract with no installed GAME parser/dispatcher realization.
7. deliberately dormant/nonselectable/quarantined catalog/primitive/House-Rule surfaces.

None of these is by itself accepted-architecture conflict. Step 1 does not repair realization.

## 9. Human judgment check

All second-recovery corrections are mechanically determined by current owners and current Senior findings.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
```

No artificial Product Owner gate is created.

## 10. Completeness gate

```text
[x] Fresh remote HEAD matched Senior re-review baseline before substantive recovery.
[x] Current process owners and CURRENT_PROGRESS restored.
[x] PROJECT_MAP used for open-world reconstruction.
[x] Prior Step-1/first-recovery owner routes rechecked.
[x] RULESET_PACKAGE_IDENTITY canonical owner inspected and added.
[x] Superseding versioning representation amendment reconciled.
[x] Shipped ruleset loader, resolved-lock, Resolution/Continuation carriers and tests inspected.
[x] Closed native 11-reason load/reconstruction set preserved.
[x] Accepted-work finite exact-set recovery failure captured.
[x] Load/reconstruction vs compatibility/migration/capability/compiler/gameplay distinctions preserved.
[x] SR25-S1-02 maintenance finding left closed absent contradictory evidence.
[x] Maintenance labels corrected to semantic outcomes/categories, not frozen exact machine enum names.
[x] CHARACTER_PROGRESSION_READY_PC_SEED canonical owner inspected and added.
[x] CHARACTER_READINESS runtime owner + validator/capability/test consumers inspected.
[x] Provisional/local-block/READY_PC/package-compile distinctions preserved.
[x] STORAGE current owner + storage baseline amendment/schema/tests inspected.
[x] Storage-owner/campaign-creator/gameplay-publication authority separation preserved.
[x] Existing campaign MANIFEST.engine.current remains independent from NEW-only storage baseline.
[x] STORAGE one-hour wording classified with stale realization debt.
[x] Full failure horizon/cascading attacks/later questions repaired only where materially required.
[x] Full-graph critic rerun found no new BLOCKING/SIGNIFICANT beyond Senior findings.
[x] All mechanically resolvable Step-1 Senior findings repaired at worker level.
[x] No human-owned decision remains.
```

## 11. Rerun critic verdict

```text
RERUN_CRITIC_BLOCKING_FOUND: 0
RERUN_CRITIC_SIGNIFICANT_FOUND: 2
RERUN_CRITIC_MINOR_FOUND: 1
NEW_BLOCKING_BEYOND_SENIOR_FINDINGS: 0
NEW_SIGNIFICANT_BEYOND_SENIOR_FINDINGS: 0

SR25-S1-01: REPAIRED / WORKER-CLOSED / PENDING INDEPENDENT SENIOR RE-RE-REVIEW
SR25-S1-02: PASS / CLOSED — RETAINED / NOT REOPENED
SR25-S1-03: REPAIRED / WORKER-CLOSED / PENDING INDEPENDENT SENIOR RE-RE-REVIEW
SENIOR_MINOR: REPAIRED / WORKER-CLOSED / PENDING INDEPENDENT SENIOR RE-RE-REVIEW

UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
WHOLESALE_UPSTREAM_REOPEN_REQUIRED: NO

WP25_STEP1_SENIOR_RE_REVIEW_PREVIOUS_RESULT: HOLD — SECOND BOUNDED STEP-1 RECOVERY REQUIRED
WP25_STEP1_SECOND_BOUNDED_RECOVERY: COMPLETE AT WORKER LEVEL / PUBLISHED WHEN THIS PACKAGE IS COMMITTED
WP25_STEP1_SENIOR_RE_RE_REVIEW: REQUIRED / PENDING
WP25_STEP2_AUTHORIZED: NO
NEXT_AUTHORIZED_UNIT: NONE
NEXT_GATE: mandatory independent WP-25 Step-1 Senior re-re-review
```

This is a worker recovery verdict only, not independent Senior PASS.

## 12. Version Impact

```text
VERSION_IMPACT: NONE
```

This critic and repaired Task Brief change Step-1 design/status provenance only. No version-bearing runtime/schema/catalog/protocol/package/migration or executable gameplay surface is changed.
