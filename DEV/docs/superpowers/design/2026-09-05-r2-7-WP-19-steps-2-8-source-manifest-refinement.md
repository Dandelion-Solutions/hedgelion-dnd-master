# R2.7 WP-19 — Steps 2–8 Source Manifest Refinement

Status: **STEP 2 EVIDENCE SET COMPLETE — COMPANION TO STEP-1 SOURCE MANIFEST**

Date: 2026-09-05

Execution basis: `aa9f23be5d7ee137bff107abc7199c3cf4236e66`

This artifact refines, but does not rewrite, the Step-1 Source Manifest after mandatory Senior GO. Historical Step-1 checkpoints retain the evidence they actually inspected.

## 1. Newly material dependencies discovered in Step 2

| Source | Role | Extracted claim / qualifier | Disposition |
|---|---|---|---|
| `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` | IMPLEMENTATION / CURRENT RUNTIME OWNER | Explicit New Game -> exact generator once -> complete generated scaffold -> one from-scratch publication -> only then player-facing setup. Infrastructure is invisible. PROVISIONAL_IDENTITY may persist early. | ADDED to creation/materialization evidence set. Its `first true live scene` wording is stale relative to progressive onboarding and is routed as realization debt, not semantic authority. |
| `DEV/TOOLS/release_builder.py` | IMPLEMENTATION / MACHINE CONTRACT | `RUNTIME_PACKAGE.yaml` carries exact package identity including `ruleset_set_sha256`, derived from the validated resolved ruleset lock. | ADDED to exact creation-identity chain. |
| `DEV/TESTS/test_release_builder.py` | TEST EVIDENCE | Release builder exercises resolved-set identity and package metadata generation. | SUPPORTING; tests do not replace owners. |
| `DEV/ARCHITECTURE/BRANCH_MODEL.md` | CURRENT DERIVATIVE ARCHITECTURE PROJECTION | Branch/root/creator rules remain useful, but current text still says Storage v2 / `baseline_version` and tag-derived campaign provenance. | STALE CURRENT PROJECTION. Must be mechanically repaired during Step 7; no upstream reopen. |
| `GAME/SCHEMA/event.schema.yaml` | MACHINE CONTRACT | SemanticEvent is append-only causal transition/history evidence, but has no explicit normalized event-time Actor decision-basis contract. | PHYSICAL SUPPORT / REALIZATION GAP; semantic owner remains Step-4 LOG/SemanticEvent. |
| `GAME/SCHEMA/campaign_manifest.schema.yaml` | MACHINE CONTRACT | Correct current engine/ruleset identity and `active` readiness law; stale phrase `unfinished pre-live onboarding` remains. | CURRENT WITH STALE VOCABULARY; downstream realization alignment. |
| `DEV/TESTS/test_runtime_identity_schema.py` | TEST EVIDENCE | Confirms Storage schema v3, current/created engine identity, required generator `--ruleset-set-sha256`. | CURRENT SUPPORTING. |
| `DEV/TESTS/test_runtime_package_provenance.py` | TEST EVIDENCE | Confirms exact package provenance behavior for tagged/clean/dirty builds. | CURRENT SUPPORTING. |

## 2. Retained owning dependency graph

### Creation / materialization

- `DEV/docs/superpowers/specs/2026-08-18-runtime-selection-and-storage-baseline-amendment.md` — Storage v3 `engine.baseline` is NEW-campaign default only.
- `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md` — physical roots/index routing; SemanticEvent history family route.
- `DEV/docs/superpowers/specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md` — deterministic one-ref publication, initial from-scratch exception, no-force/CAS semantics.
- `GAME/INSTALL/00_DND_BOOTSTRAP.md`, `GAME/CORE/BOOTSTRAP_RUNTIME.md`, `GAME/CORE/CAMPAIGN_SETUP.md`, `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md`, `GAME/TOOLS/init_campaign.py` — runtime realization/consumers.
- `GAME/SCHEMA/dnd_storage.schema.yaml`, `campaign_manifest.schema.yaml`, campaign card/config/current schemas — machine contracts.

### Readiness / persistence / multiplayer

- `DEV/docs/superpowers/specs/2026-08-24-r2-7-wp-04-progressive-ready-pc-owner-clarification.md` — progressive provisional play, READY_PC, no hard pre-live/live split.
- `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md` — durability boundaries/batching.
- `GAME/CORE/PERSISTENCE.md`, `DURABILITY_GUARD.md`, `SAVE_CONTRACT.md`, `SESSION.md` — current runtime persistence/session consumers.
- `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md`, `GAME/CORE/MULTIPLAYER.md`, `LIVE_SCENE.md`, `DEV/ARCHITECTURE/ACCESS_CONTROL.md` — player authority/live non-interference.

### Retrospective / historical evidence / performance

- PO-001/PO-002 accepted owner decision.
- PO-003 Historical Actor Decision Basis owner decision + immutable latency/interactivity amendment in `DEV/PRODUCT_OWNER_INPUT.md`.
- R2.2 Actor current cognition/directed relationships owner.
- Step-4 truth/knowledge/role-context/Story canonical spec: `world.knowledge` current epistemic owner; LOG/SemanticEvent historical causal evidence.
- R2.3 Context Runtime: registered purpose/need profile, bounded dependency-specific historical escalation.
- R2.4 Single-Context LLM Execution: role != model call, typed handoff, deterministic acceptance, no persistent COT.
- WP-10 durable record-family completeness: existing SemanticEvent/history family.
- WP-15 chronology: typed temporal/causal evidence, not motive/cognition authority.
- WP-18 Story/continuity: source-bound noncanonical retrospective orientation only.
- `GAME/CORE/PLAY_POLICY.md`: ordinary live turn local-first; no irrelevant retrieval/bookkeeping; situational modules do no work on unrelated turns.

## 3. Verification/scenario evidence dispositions

- `BOOTSTRAP_STORAGE_REGRESSION_CASES:B12/B22/B23` — STALE/SUPERSEDED; B25/B37-B45 are useful with progressive-onboarding qualifiers.
- `REGRESSION_CASES:T04/T08` — CURRENT SUPPORTING for knowledge eligibility/bounded history; `T13` STALE manifest-only menu discovery.
- `CHARACTER_READINESS_CASES:C08/C09/C10/C16/C17` — CURRENT SUPPORTING progressive/local-sufficiency behavior; any `true live` wording is superseded vocabulary.
- `DIEGETIC_ONBOARDING_CASES:DO02-DO07/DO11-DO14` — CURRENT SUPPORTING; `pre-live/true live` vocabulary is superseded while the underlying readiness constraints remain.
- `EXPLICIT_SAVE_CASES:S07/S15/S16/S17-S20` — CURRENT; `S08` applies only to genuine save-and-stop, not PO-002 exit-to-menu.
- `MULTIPLAYER_MEMBERSHIP_CASES:M01/M10-M12` — CURRENT; proves leave/removal is a distinct durable transition.
- `PERSISTENCE_TRANSACTION_CASES:PT01/PT02/PT10/PT14/PT15/PT30` — CURRENT; supports zero-I/O ordinary turns, batching, from-scratch initial exception.
- `PERFORMANCE_CASES:P01/P03/P07/P10`, `RUNTIME_CONTEXT_RESEARCH_CASES:C04/C07`, `RUNTIME_SCOPE_LATENCY_CASES:RL03-RL05` — CURRENT SUPPORTING latency/locality.
- Direct end-to-end PO-001, PO-002 and PO-003 cases remain absent and are downstream realization obligations.

## 4. Exact creation identity chain

```text
selected storage DND_STORAGE.engine.baseline
    -> exact locally available validated RUNTIME_PACKAGE
         version
         package_id
         truthful source_commit_sha | null
         package_sha256
         ruleset_set_sha256
    -> TOOLS/init_campaign.py --ruleset-set-sha256 ...
    -> MANIFEST.engine.created_with/current
    -> MANIFEST.ruleset.created_with/current
```

Current install/bootstrap/setup prose omits the required ruleset hash argument even though the builder/package and generator contracts require it. This is a downstream runtime-text realization gap, not a missing architecture owner.

## 5. Synthesis completeness gate

```text
[x] process/current-state/PO sources
[x] creation package/storage/provenance owners
[x] branch/root/creator/publication owners
[x] generator/template/runtime bootstrap consumers
[x] READY_PC/progressive onboarding/lifecycle owners
[x] persistence/session/save/live/multiplayer owners
[x] PO-001 ordinary Master retrospective consumer
[x] PO-002 save-and-exit composition
[x] PO-003 Actor/knowledge/history/Story/context/chronology graph
[x] event/storage/manifest machine schemas
[x] executable/scenario reverse-conformance evidence
[x] latency/context/LLM-call constraints
[x] stale/superseded test/runtime/index projections classified
[x] WP-20 migration/evolution boundary preserved
```

No unresolved evidence omission blocks synthesis.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
```