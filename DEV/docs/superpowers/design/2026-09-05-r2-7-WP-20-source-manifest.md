# R2.7 WP-20 Step 1 — Task-Specific Source Manifest

Status: **STEP 1 COMPLETE — REVIEW-READY / MANDATORY SENIOR REVIEW PENDING**

Date: 2026-09-05

Framing basis: `fb26b6d4ce9c07d2b561544eef90c488ffa76ad7` on the active development ref.

Scope: **engine update / schema evolution / migration** for campaigns created under released HDM v1.0+ versions.

This manifest is complete for **Step-1 problem framing and Task-Brief criticism**. It identifies the ownership/dependency subgraph that Step 2 must research to architecture depth. `DERIVATIVE`, `HISTORICAL`, `IMPLEMENTATION/TEST` and current scaffold sources do not gain normative authority by inclusion.

## 1. Program, process and current-state controls

| Source | Role | Why relevant / required scope | Step-1 inspection / disposition |
|---|---|---|---|
| `AGENTS.md` | PROCESS / REPOSITORY GOVERNANCE | bootstrap, evidence, taxonomy, public-write rules | Read current; governs work, not WP-20 semantics. |
| `DEV/DESIGN_PROCESS.md` | CANONICAL PROCESS | Source Manifest, Task Brief, whole-project critic, evidence gate | Read current; Step 1 follows it. |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | CANONICAL HDM PROCESS ADAPTER | whole-project critic + mandatory Senior stop | Read current. |
| `DEV/PROJECT_MAP.md` | DERIVATIVE LOCATOR | reconstruct update/persistence/ruleset/live dependency graph | Read current; dependency routes followed into actual owners. |
| `DEV/CURRENT_PROGRESS.md` | CURRENT-PROGRESS AUTHORITY | exact authorized unit/gate | Read current; WP-20 Step 1 only. |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | SEQUENCING/SCOPE | R2.7 sequence and program constraints | Read current; no sequence change identified. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md` | DESIGN PROVENANCE / R2.7 SCOPE | owns WP-20 audit questions | Read current taxonomy location; old `research/` path is not used. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md` | DESIGN PROVENANCE / PROGRAM BRIEF | bidirectional architecture↔machine proof and WP boundaries | Read relevant WP-20/program requirements. |

## 2. Product Owner compatibility authority

| Source | Role | Why relevant | Step-1 disposition |
|---|---|---|---|
| `DEV/PRODUCT_OWNER_INPUT.md` — `PO-004` | PRODUCT OWNER INTENT / ROUTING | controlling compatibility horizon | Read exact entry/routing. `PARTIALLY_INCORPORATED`; open PO decision `NONE`. |
| `DEV/docs/superpowers/specs/2026-09-05-hdm-v1-clean-slate-compatibility-owner-decision.md` | OWNER-APPROVED CANONICAL INPUT | no pre-release compatibility obligation; released v1.0+ evolution remains WP-20 | Controlling framing law. Pre-release/v0.8 compatibility is out of required surface. |

Required classification:

```text
PRE-RELEASE / 0.8 COMPATIBILITY
    -> OUT OF REQUIRED COMPATIBILITY SURFACE

RELEASED v1.0+ EVOLUTION
    -> CURRENT WP-20 ARCHITECTURE PROBLEM
```

No existing pre-release scaffold/schema/test creates a compatibility obligation merely by existing.

## 3. Creation/runtime identity boundary inherited from WP-19

| Source | Role | Why relevant | Step-1 disposition |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-canonical-spec.md` | FINAL CANONICAL OWNER | creation identity and first-authority boundary that later evolution consumes | Read identity/publication sections only. WP-19 is not reopened. |
| `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-final-senior-review.md` | FINAL SENIOR VERDICT | confirms exact identity/current-runtime boundary and routes future evolution to WP-20 | Read. PASS; creation architecture accepted. |

Inherited creation identity axes include `engine_version`, `package_id`, truthful `source_commit_sha`, exact `package_sha256`, and `ruleset_set_sha256`; version/tag alone is insufficient.

## 4. Runtime package, engine and ruleset identity/evolution

| Source | Role | Why relevant | Step-1 disposition |
|---|---|---|---|
| `GAME/CORE/ENGINE_UPDATES.md` | CURRENT RUNTIME UPDATE CONTRACT | package discovery, exact/same-version refresh, semantic-version adoption, package absence/failure | Read current. Same-version compatible refresh is inherited; incompatible released evolution remains WP-20. |
| `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` | CANONICAL OWNER | non-equivalent engine/package/ruleset/catalog identities; compatibility line; exact set retention | Read current. Explicitly routes incompatible released ruleset migration to WP-20. |
| `DEV/ARCHITECTURE/BRANCH_MODEL.md` | DERIVATIVE PROJECTION | compact storage/runtime/campaign identity routing | Read; does not own migration policy. |
| `DEV/docs/superpowers/specs/2026-08-18-runtime-package-provenance-amendment.md` | ACCEPTED PACKAGE-PROVENANCE OWNER/AMENDMENT | exact built-artifact provenance; mutable tag cannot identify old bytes | Read relevant identity rules. |
| `GAME/ENGINE_VERSION.yaml` | RUNTIME MACHINE METADATA | semantic engine/schema/update compatibility projection | Read current. `campaign_update.compatibility` is coarse metadata, not proven complete migration graph. |
| `DEV/ENGINE_DEVELOPMENT.yaml` | DEVELOPMENT/RELEASE METADATA | release bookkeeping + independent revision counters | Read current; machine/version evidence, not campaign migration owner. |
| `DEV/RELEASE/VERSIONING.md` | CURRENT RELEASE POLICY | release identity; `compatible` vs `maintenance_required`; independent schema/format revisions | Read current. Unknown currently maps conservatively to maintenance-required; Step 2 must determine final relation to unsupported/migration-path semantics. |
| `DEV/TOOLS/release_builder.py` | IMPLEMENTATION / PACKAGE MACHINE EVIDENCE | generated `RUNTIME_PACKAGE`, exact ruleset lock/conformance, package composition | Inspected relevant metadata/build path. Current package metadata has rich runtime/ruleset identity but no demonstrated released-campaign migration graph. |

## 5. Persistent campaign/storage schema identity

| Source | Role | Why relevant | Step-1 disposition |
|---|---|---|---|
| `GAME/SCHEMA/campaign_manifest.schema.yaml` | CURRENT MACHINE CONTRACT | engine created/current, ruleset created/current, campaign schema, roots/currentness metadata | Read current. Existing fields are evidence; no presumption they are sufficient for released migration. |
| `GAME/SCHEMA/dnd_storage.schema.yaml` | CURRENT MACHINE CONTRACT | storage format + new-campaign baseline identity | Read current. Baseline is NEW-only and cannot mutate existing campaigns. |
| `DEV/docs/superpowers/specs/2026-08-18-engine-version-split-amendment.md` | ACCEPTED/HISTORICAL VERSION DESIGN | separates engine release identity from independent schema/revision axes | Read relevant policy; old 0.8 examples are historical, not compatibility obligations. |
| `GAME/MIGRATIONS/README.md` | CURRENT SCAFFOLD / IMPLEMENTATION EVIDENCE | current intended migration directory semantics | Read. Thin scaffold, not architecture owner. Its `rollback/checkpoint requirement` wording cannot predetermine WP-20 rollback policy. |

Step 2 must inventory all persistent owner schemas/format identities reached through WP-10/WP-11 and determine which version identifiers are actually required for safe released evolution rather than treating one manifest `schema_version` as universal.

## 6. Durability, publication, recovery, HOT and semantic preservation

| Source | Role | Why relevant | Step-1 disposition |
|---|---|---|---|
| `GAME/CORE/PERSISTENCE.md` | CURRENT TRANSPORT OWNER | base-tree delta, pinned HEAD, non-force CAS, stale-head rebuild, checkpoint non-implication | Read current. Migration publication must compose with it. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md` | CANONICAL WP-13 OWNER | immutable publication attempt; tri-state final ref outcome; currentness/indeterminate behavior | Read relevant laws. Local transform success is not authoritative migration success before confirmed publication. |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md` | CANONICAL WP-14 OWNER | current-source recovery, accepted-work interpretation, checkpoint nonauthority | Read relevant laws. Checkpoint is not a guaranteed rewind/rollback slot. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md` | CANONICAL WP-12 OWNER | stable native identity; HOT/SQLite nonauthority; derived helpers; open-work interpretation | Read relevant laws. Representation migration cannot reassign semantic identity or reinterpret accepted work. |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md` | CANONICAL WP-15 OWNER | native-owner identity + chronology preservation | Read relevant laws. Git/storage ordering cannot replace fictional causal/temporal evidence. |

Step-2 expansion must include actual affected WP-10/WP-11 owner-family/path/schema contracts and Step-5 accepted-execution/recovery owners where migration changes their representation or interpretation context.

## 7. Authorization, multiplayer and LIVE currentness

| Source | Role | Why relevant | Step-1 disposition |
|---|---|---|---|
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | CURRENT ACCESS OWNER | campaign creator, storage owner, PLAYER authority, migration/adoption wording | Read. Contains wording requiring reconciliation: a broad storage-owner maintenance sentence vs later creator-only explicit engine/ruleset adoption list. Step 2 must resolve through current owners rather than invent a new authority. |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md` | CANONICAL WP-16 OWNER | distinct campaign/LIVE/HOT currentness, exact-source LIVE CAS, no fallback while live-owned | Read relevant laws. Migration cannot bypass selected LIVE authority or create mixed source truth. |
| Step-5.8 live owner and R2.5 collaboration owner | CANONICAL UPSTREAM OWNERS | authority transfer/agency constraints beneath WP-16 | Required Step-2 source expansion where exact migration/live policy depends on them. |

## 8. Install/runtime availability and machine consumers

| Source | Role | Why relevant | Step-1 disposition |
|---|---|---|---|
| `GAME/INSTALL/00_DND_BOOTSTRAP.md` | CURRENT RUNTIME INSTALL/SELECTION CONSUMER | exact ZIP availability, campaign-first runtime resolution, multi-runtime cache | Read relevant sections. Legacy nested-layout/backward-support prose is not a PO-004 compatibility obligation. |
| `DEV/TESTS/ENGINE_UPDATE_CASES.md` | SCENARIO/TEST EVIDENCE | current update/migration scenarios | Read. Mixed-quality evidence; U13/U14/U15/U18/U19/U20/U23 remain useful challenge cases, while U04/U06/U08 and especially U17 contain stale/legacy assumptions needing re-evaluation. |
| `DEV/TESTS/test_engine_update_policy_contract.py` | EXECUTABLE TEST EVIDENCE | current text-level update-policy assertions | Read; not architecture authority. |
| `DEV/TESTS/test_engine_mismatch_recovery_contract.py` | EXECUTABLE TEST EVIDENCE | exact-runtime absence and creator/non-creator flow | Read; not architecture authority. |
| `DEV/TESTS/test_multi_runtime_bootstrap_contract.py`, `test_multi_runtime_release_consistency.py`, `test_runtime_identity_schema.py`, `test_runtime_package_provenance.py` | EXECUTABLE TEST EVIDENCE | package/runtime identity and selection | Step-2 machine reverse-audit set. |
| `DEV/TESTS/test_release_builder.py`, `test_release_integration.py`, release tests | EXECUTABLE/RELEASE EVIDENCE | released package metadata/composition | Step-2 machine reverse-audit set. |
| `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md`, `LIVE_SCENE_CASES.md`, `CHRONOLOGY_CASES.md`, `ACCESS_CONTROL_CASES.md`, `EXPLICIT_SAVE_CASES.md` | SCENARIO EVIDENCE | failure/currentness/authority invariants | Step-2 targeted extraction set. |
| `DEV/TOOLS/run_maintenance_audit.py`, `DEV/TOOLS/audit_engine.py`, release checks / `.github/workflows/validate.yml` | IMPLEMENTATION/VERIFICATION EVIDENCE | final consistency and release verification consumers | Step-2 architecture→machine mapping and later WP-22/23 boundary. |

## 9. Downstream boundary sources

WP-21+ may constrain completeness but are not started. In particular:

```text
WP-21  install/bootstrap/startup composition consumers after migration
WP-22  verification/test completeness
WP-23  release/package/version readiness
WP-25  failure/degradation closure
WP-26  stale documentation/routing/supersession cleanup
WP-27  implementation-planning readiness
```

WP-20 must identify obligations for those consumers without executing their work.

## 10. Step-1 evidence synthesis

Established at framing depth:

1. Released v1.0+ is the only required compatibility horizon; pre-release/v0.8 migration is not required.
2. Compatibility is inherently multi-axis. Current owners explicitly separate engine semantic version, exact package/provenance/ZIP identity, ruleset compatibility/exact set identity, schema/format versions, and accepted-work interpretation context.
3. Existing same-version compatible refresh semantics are inherited and should not be reopened absent contradiction; incompatible released evolution is the unresolved WP-20 problem.
4. Safe migration must compose with existing owner/currentness/publication/recovery/live laws; it cannot create a second publication, identity, chronology, checkpoint, or LIVE authority.
5. Existing migration/update/schema/tests are evidence only. Several pre-release/legacy assumptions are already non-binding under PO-004.
6. Current evidence exposes no genuine Product Owner decision required to complete Step-1 framing.

```text
SOURCE_MANIFEST: COMPLETE FOR STEP-1 FRAMING
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
WP20_STEP2_AUTHORIZED: NO
```
