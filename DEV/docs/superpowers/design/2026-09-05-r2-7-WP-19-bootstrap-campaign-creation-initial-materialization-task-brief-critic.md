# R2.7 WP-19 — Bootstrap / Campaign Creation / Initial Materialization — Whole-Project Task-Brief Critic

Status: **STEP 1 SENIOR RECOVERY COMPLETE — SR19-01 CLOSED — MANDATORY SENIOR RE-REVIEW CANDIDATE**

Date: 2026-09-05

Original critic basis: `5fc24905be5c9e1b47929ee9e7b49ea8b9f2a053`

Senior-recovery basis: `df5fe6441c2b85e9cbffcb6f83caa885501da794`

This is the mandatory Step-1 whole-project Task-Brief critic required by `DEV/DESIGN_PROCESS.md` and `DEV/ARCHITECTURE/DESIGN_PROCESS.md`, recovered after Senior review identified `SR19-01 / SIGNIFICANT`.

The recovery independently reconstructed the verification/scenario subgraph from current `DEV/PROJECT_MAP.md`, actual owners and the full current `DEV/TESTS/` directory. The Senior-provided minimum file list was treated as evidence to verify, not as an answer key.

Companion artifacts:

- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief.md`.

---

## 1. Independent reconstruction method

Original Step-1 reconstruction followed:

```text
Project Instructions / install bootstrap
    -> explicit campaign-choice barrier
    -> storage discovery / storage v3 baseline
    -> exact runtime package selection
    -> ruleset package identity / release metadata
    -> branch ancestry / creator / access authority
    -> New Campaign fast path / Campaign Setup
    -> init_campaign materializer
    -> GAME/CAMPAIGN template tree
    -> MANIFEST / CONFIG / CARD / CURRENT schemas
    -> initial from-scratch publication
    -> normal persistence/currentness boundary
    -> campaign identity/card projections
    -> PLAYER / PC / provisional onboarding
    -> READY_PC / PLAY_READY / lifecycle active
    -> session/resume / first true live scene
    -> multiplayer mode/join policy/PLAYER authorization
    -> House-Rules default materialization
    -> release-builder + integration-test consumer
    -> future migration/evolution boundary in WP-20
```

SR19-01 recovery expanded the last machine/verification leg independently:

```text
DEV/PROJECT_MAP verification route
    -> enumerate DEV/TESTS
    -> bootstrap/storage/install/menu scenario catalogs
    -> package/provenance/build/integration executable tests
    -> campaign identity/card scenario catalogs
    -> character readiness / diegetic onboarding / durability / explicit-save cases
    -> persistence/access/multiplayer/runtime-latency cases
    -> S6D READY_PC + ruleset-package executable evidence
    -> engine-update/mismatch neighbors
    -> historical pre-release evidence
    -> item-level expectation -> current owner -> disposition
```

The critic applies this rule:

```text
TEST OR SCENARIO IS A CONSUMER / EVIDENCE SURFACE
NOT A SEMANTIC OWNER BY EXISTENCE OR PASS STATUS
```

---

## 2. Findings summary

Senior independently confirmed the original findings. They remain closed and are not reopened.

```text
ORIGINAL_STEP1_BLOCKING:       2
ORIGINAL_STEP1_SIGNIFICANT:    5
ORIGINAL_STEP1_MINOR:          1

SENIOR_RECOVERY_BLOCKING:      0
SENIOR_RECOVERY_SIGNIFICANT:   1   # SR19-01
SENIOR_RECOVERY_MINOR:         0

UNRESOLVED_BLOCKING:           0
UNRESOLVED_SIGNIFICANT:        0
HUMAN_DECISION_REQUIRED:       NO
UPSTREAM_REOPEN_REQUIRED:      NO
ARCHITECTURE_REOPENED:         NO
STEP2_STARTED:                 NO
STEP2_AUTHORIZED:              NO
IMPLEMENTATION_PLANNING_STARTED: NO
```

No additional independent BLOCKING or SIGNIFICANT architecture defect was found beyond `SR19-01`. The stale expectations found during recovery are item-level verification-consumer defects routed under SR19-01 and existing current owners; they do not create new semantic owners or human decisions.

---

## 3. Original finding dispositions — confirmed

### F19-S1-01 — BLOCKING — CLOSED

Exact ruleset-set identity was missing from bootstrap framing. Current owner chain remains:

```text
selected validated runtime package
    -> RUNTIME_PACKAGE.ruleset_set_sha256
    -> init_campaign --ruleset-set-sha256
    -> MANIFEST.ruleset.created_with/current
```

Senior review confirmed the finding. Recovery found additional current executable support (`test_release_builder.py`, `test_release_integration.py`, S6D package closure) and no contradiction.

### F19-S1-02 — BLOCKING — CLOSED

Scaffold, PROVISIONAL_IDENTITY, READY_PC and PLAY_READY remain distinct states. Readiness/onboarding/durability executable/scenario evidence confirms rather than contradicts the accepted lifecycle owners.

### F19-S1-03 — SIGNIFICANT — CLOSED

Branch/storage/access and stale-v2 reconciliation remains required. SR19-01 adds concrete reverse-conformance evidence: `BOOTSTRAP_STORAGE_REGRESSION_CASES.md:B12` is stale v2 while current executable/schema evidence is v3.

### F19-S1-04 — SIGNIFICANT — CLOSED

Campaign identity/card/config/current projections remain in scope. SR19-01 adds `CAMPAIGN_CARD_CASES.md:C12` as a stale projection expectation against current fixed icon/status semantics.

### F19-S1-05 — SIGNIFICANT — CLOSED

Initial from-scratch publication versus later setup/durability/session/resume remains correctly separated. Persistence/durability/save cases confirm the distinction; no new owner conflict found.

### F19-S1-06 — SIGNIFICANT — CLOSED

Initial multiplayer authority remains creator/PLAYER controlled. Access/membership test expansion found stale/qualified wording but no new unsatisfied authority consumer requiring WP-16 reopen.

### F19-S1-07 — SIGNIFICANT — CLOSED, EVIDENCE PROOF RECOVERED BY SR19-01

The original finding correctly required machine/template/schema/test reverse audit, but the published evidence proof was incomplete because it named only a narrow executable subset and did not independently inspect the directly relevant scenario/test graph.

SR19-01 closes that **evidence-completeness defect** without reopening the original architecture finding.

### F19-S1-08 — MINOR — CLOSED

WP-20/dormant neighbor boundary remains explicit. Engine-update/mismatch test families inspected during recovery confirm why update/evolution cases must not become current WP-19 work.

---

## 4. SR19-01 — SIGNIFICANT — verification/test reverse-conformance evidence incomplete

### Defect

The original Source Manifest and critic claimed machine/template/schema/test coverage after inspecting the materializer/package producer and a narrow integration-test slice. That was insufficient for a whole-project reverse-conformance claim because `DEV/PROJECT_MAP.md` routes verification through both executable `test_*.py` and scenario/regression `*_CASES.md`, and those consumers can themselves be stale.

The defect is material because future implementation could follow a current-looking test expectation that contradicts a later/current owner even while the executable CI suite remains green.

### Independently expanded verification families

Recovery directly inspected these material families:

**Bootstrap / storage / install / menu**
- `DEV/TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md`;
- `DEV/TESTS/INSTALL_ONBOARDING_CASES.md`;
- `DEV/TESTS/CAMPAIGN_CARD_CASES.md`;
- `DEV/TESTS/CAMPAIGN_IDENTITY_CASES.md`;
- `DEV/TESTS/GM_TONE_ONBOARDING_CASES.md`;
- WP-19-relevant `DEV/TESTS/REGRESSION_CASES.md` cases.

**Readiness / onboarding / durability / save**
- `DEV/TESTS/CHARACTER_READINESS_CASES.md`;
- `DEV/TESTS/DIEGETIC_ONBOARDING_CASES.md`;
- `DEV/TESTS/DURABILITY_BOUNDARY_CASES.md`;
- `DEV/TESTS/EXPLICIT_SAVE_CASES.md`;
- `DEV/TESTS/ENGINE_CONSISTENCY_CASES.md`;
- `DEV/TESTS/test_s6d_07_character_mvp_seed.py`.

**Runtime/package/provenance/release**
- `DEV/TESTS/test_multi_runtime_bootstrap_contract.py`;
- `DEV/TESTS/test_multi_runtime_release_consistency.py`;
- `DEV/TESTS/test_runtime_identity_schema.py`;
- `DEV/TESTS/test_runtime_package_provenance.py`;
- `DEV/TESTS/test_release_builder.py`;
- `DEV/TESTS/test_release_integration.py`;
- `DEV/TESTS/test_release_game_passthrough.py`;
- `DEV/TESTS/test_destination_template_boundary.py`;
- `DEV/TESTS/test_game_dev_layout.py`;
- `DEV/TESTS/test_s6d_11_ruleset_package_closure.py`.

**Publication / access / multiplayer / runtime-boundary**
- `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md`;
- `DEV/TESTS/ACCESS_CONTROL_CASES.md`;
- `DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md`;
- `DEV/TESTS/RUNTIME_SCOPE_LATENCY_CASES.md`.

**Downstream/historical routing**
- `DEV/TESTS/ENGINE_UPDATE_CASES.md`;
- `DEV/TESTS/test_engine_mismatch_recovery_contract.py`;
- `DEV/TESTS/test_engine_update_policy_contract.py`;
- `DEV/TESTS/PRE_RELEASE_AUDIT_0.1.0.md`.

### Material item-level dispositions

#### V19-01 — `BOOTSTRAP_STORAGE_REGRESSION_CASES.md:B12`

**Expectation:** fresh storage initialization creates a “v2 DND_STORAGE.yaml”.

**Current owner:** `GAME/SCHEMA/dnd_storage.schema.yaml` schema v3; current bootstrap/storage owners use exact `engine.baseline` package identity. `test_multi_runtime_release_consistency.py` explicitly proves storage schema v3 and absence of retired `baseline_version` in active runtime contracts.

**Disposition:** **STALE / SUPERSEDED**.

**Routing:** existing F19-S1-03 / WP-19 storage-currentness reconciliation. No compatibility or Product Owner decision.

#### V19-02 — `BOOTSTRAP_STORAGE_REGRESSION_CASES.md:B22`

**Expectation:** normal release package resolves its published tag to exact commit SHA before new campaign/migration.

**Current owner:** selected ZIP `RUNTIME_PACKAGE.source_commit_sha` owns built-artifact source provenance. Current bootstrap/engine-update contracts explicitly prohibit inferring an old package's source SHA solely from the current position of a mutable tag.

**Disposition:** **STALE / SUPERSEDED**.

**Routing:** WP-19 creation provenance; migration aspect remains WP-20. No new identity policy.

#### V19-03 — `BOOTSTRAP_STORAGE_REGRESSION_CASES.md:B23`

**Expectation:** after scaffold publication tell player setup has visible character -> minimal world -> first scene stages.

**Current owner:** `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` has precedence for scaffold ordering/player handoff and explicitly requires successful infrastructure to remain invisible; do not expose internal setup stages/installation progress by default. `GM_TONE_ONBOARDING_CASES.md:GT01-GT07` supports the human opening.

**Disposition:** **STALE / SUPERSEDED**.

**Routing:** existing low-friction product semantics; no Product Owner decision.

#### V19-04 — `BOOTSTRAP_STORAGE_REGRESSION_CASES.md:B25`

**Expectation:** once PC/minimal situation are ready, create first scene/**checkpoint** and begin play.

**Current owner:** campaign setup/durability owners make checkpoint optional unless recovery policy independently requires it; launch requires READY_PC + PLAY_READY semantics.

**Disposition:** **CURRENT WITH QUALIFIER**.

**Routing:** WP-19 launch/readiness composition; do not turn checkpoint into ceremony.

#### V19-05 — `CAMPAIGN_CARD_CASES.md:C12`

**Expectation:** paused or initializing candidate renders 🟡.

**Current owner:** `GAME/CORE/CAMPAIGN_CARD.md` fixed mapping: initializing 🟡, paused ⏸️.

**Disposition:** **STALE / SUPERSEDED**.

**Routing:** existing F19-S1-04 projection consistency; no lifecycle reopen.

#### V19-06 — `REGRESSION_CASES.md:T13`

**Expectation:** new-game discovery scans `campaign/*` and reads manifests only.

**Current owner:** bootstrap/card owners use card-first menu discovery, MANIFEST only as fallback.

**Disposition:** **STALE / SUPERSEDED**.

**Routing:** current menu/latency path; no product decision.

#### V19-07 — `ACCESS_CONTROL_CASES.md:A26/A27/A29/A30`

**Expectation:** storage-main owner separation.

**Current owner:** storage default branch remains storage-owner-only for storage initialization/baseline metadata. Campaign engine/ruleset adoption authority is independent and creator-controlled.

**Disposition:** **CURRENT WITH QUALIFIER**. Authority boundary is current; old wording that suggests copied-engine/campaign-engine maintenance on storage main is not a current semantic owner.

**Routing:** existing F19-S1-03 + current `ENGINE_UPDATES.md`/access owners.

#### V19-08 — `ACCESS_CONTROL_CASES.md:A28`

**Expectation:** guest performs no release discovery/storage-main upgrade/campaign integration and uses a “campaign-integrated engine”.

**Current owner:** guest lacks storage-baseline and creator-only adoption authority, but runtime package discovery/use, missing-package recovery and compatible same-version behavior follow current `ENGINE_UPDATES.md`; engine bytes are local runtime package bytes, not integrated into campaign storage.

**Disposition:** **SUPERSEDED IN PART / CURRENT WITH QUALIFIER**.

**Routing:** current access + runtime identity owners; future semantic migration remains WP-20.

#### V19-09 — `ENGINE_UPDATE_CASES.md`

**Expectation family:** update/migration policy.

**Disposition:** **OWNED DOWNSTREAM / WP-20** except creation-adjacent package identity boundaries. In particular old U04/U08/U10 wording must not be imported into WP-19 as current authority (`Always update automatically`, `baseline_version`, old tag-resolution provenance style).

#### V19-10 — `PRE_RELEASE_AUDIT_0.1.0.md`

**Expectation family:** old 0.1.0 bootstrap/skeleton snapshot.

**Disposition:** **HISTORICAL ONLY**. The file explicitly marks itself non-normative.

### Current verification evidence confirmed

The expansion also confirmed substantial current evidence:

- `INSTALL_ONBOARDING_CASES.md:I01-I08` — CURRENT;
- `CHARACTER_READINESS_CASES.md:C01-C17` — CURRENT for current readiness/onboarding semantics, with legacy-repair cases not implying compatibility preservation;
- `DIEGETIC_ONBOARDING_CASES.md:DO01-DO14` — CURRENT;
- creation-relevant `DURABILITY_BOUNDARY_CASES.md` — CURRENT;
- creation-relevant `EXPLICIT_SAVE_CASES.md` — CURRENT;
- `ENGINE_CONSISTENCY_CASES.md:EC07/08/10/14/15` — CURRENT;
- `PERSISTENCE_TRANSACTION_CASES.md:PT30` and related non-force/currentness cases — CURRENT;
- `RUNTIME_SCOPE_LATENCY_CASES.md:RL04` and negative maintenance leakage cases — CURRENT;
- executable multi-runtime/package/release/readiness/ruleset tests listed above — CURRENT or current supporting evidence under their natural owner.

A key reverse-conformance result is therefore:

```text
EXECUTABLE CURRENTNESS: substantially current for v3/package/readiness contracts
SCENARIO CATALOG CURRENTNESS: mixed; explicit stale items remain
```

### Resolution

**SR19-01: CLOSED.**

Recovery actions:

1. Source Manifest now contains the independently reconstructed verification/test subgraph.
2. Material expectations receive item-level current/stale/qualified/downstream/historical disposition.
3. Task Brief now requires Step-2 verification reverse-conformance across both executable tests and scenario catalogs.
4. Stale scenarios are explicitly barred from acting as future implementation truth.
5. No test/scenario files were rewritten because Step-1 evidence recovery does not require design-realization changes and Step 2 is unauthorized.
6. Product Owner boundary was rerun; no human-owned decision was found.

**Human decision required:** NO.

---

## 5. Product Owner boundary re-review

### Product semantics

Stale B23/C12/T13 expectations conflict with already accepted current owners for invisible setup, fixed card status presentation and card-first menu discovery. There is no unresolved choice between viable product semantics.

### Canonical authority / ownership

Storage v3, package provenance, creator/PLAYER/PC/readiness/persistence and projection owners are already allocated. Tests/scenario catalogs cannot become semantic owners by age, naming or pass status.

### Meaningful compatibility policy

Current unreleased scaffold remains clean-slate by owner decision; WP-20 owns future released-campaign evolution. Legacy/test references do not recreate a compatibility requirement.

### Hard-to-reverse lifecycle/product behavior

Readiness/onboarding/durability evidence confirms the accepted scaffold -> provisional -> READY_PC -> PLAY_READY distinction.

### Material quality trade-off

Low-friction invisible setup, bounded I/O and card-first menu are already accepted. Recovery exposed stale verification consumers, not an open trade-off.

### Explicit risk acceptance

No new material risk requires Product Owner acceptance.

```text
HUMAN_DECISION_REQUIRED: NO
```

---

## 6. Closed-upstream architecture review after recovery

No current evidence requires upstream reopen:

- stale Storage-v2/test expectations lose to current storage v3 owners;
- stale tag-derived package provenance loses to package-owned `RUNTIME_PACKAGE.source_commit_sha`;
- stale setup/menu/card expectations lose to current runtime projection/fast-path owners;
- readiness/durability tests confirm accepted owners;
- multiplayer/access qualifiers are mechanically routed to current closed owners;
- update/migration tests remain downstream rather than becoming WP-19 work.

```text
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
```

---

## 7. Recovered Step-1 critic gate

```text
F19-S1-01 BLOCKING    CLOSED — exact ruleset-set propagation framing confirmed
F19-S1-02 BLOCKING    CLOSED — scaffold/provisional/READY_PC/PLAY_READY separation confirmed
F19-S1-03 SIGNIFICANT CLOSED — branch/storage/access/stale-v2 reconciliation retained
F19-S1-04 SIGNIFICANT CLOSED — identity/card/config/current projections retained
F19-S1-05 SIGNIFICANT CLOSED — publication/durability/session/resume route retained
F19-S1-06 SIGNIFICANT CLOSED — multiplayer initial authority route retained
F19-S1-07 SIGNIFICANT CLOSED — machine/template/schema/test reverse-audit requirement retained; evidence proof expanded by SR19-01
F19-S1-08 MINOR       CLOSED — WP-20/dormant-neighbor boundary retained
SR19-01   SIGNIFICANT CLOSED — verification/scenario reverse-conformance evidence expanded and itemized

NEW_BLOCKING:              0
NEW_SIGNIFICANT:           1   # SR19-01 only
NEW_MINOR:                 0
UNRESOLVED_BLOCKING:       0
UNRESOLVED_SIGNIFICANT:    0
HUMAN_DECISION_REQUIRED:   NO
UPSTREAM_REOPEN_REQUIRED:  NO
STEP2_STARTED:             NO
STEP2_AUTHORIZED:          NO
WP20_STARTED:              NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
```

### Critic recommendation to Senior

The recovered Step-1 package now supports its claimed verification/test reverse-conformance framing. `SR19-01` is closed with explicit evidence and item-level dispositions. No residual blocking/significant framing omission, Product Owner decision, or upstream reopen is currently identified.

**Recommendation:** mandatory Senior **re-review** may grant or withhold GO for WP-19 Step 2. This critic does not grant GO itself.
