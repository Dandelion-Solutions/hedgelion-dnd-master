# R2.7 WP-12 - HOT, SQLite and Transaction Realization - Source Manifest

Status: **STEP-1 SOURCE MANIFEST - INSPECTED FOR TASK-BRIEF FRAMING**

Purpose: auditable source selection for WP-12. `INSPECTED` means read on the
current ref deeply enough to frame Step 1; it does not claim Step-2 evidence or
whole-R2.7 coverage. Primary owners outrank routing aids and current machine
surfaces are evidence, not semantic overrides.

## 1. Governance, scope and routing

| Source | Authority role | Required scope | Status |
|---|---|---|---|
| `AGENTS.md` | GOVERNANCE | repository/process/publication constraints | INSPECTED |
| `DEV/DESIGN_PROCESS.md` | CANONICAL PROCESS | Source Manifest, Step-1 and critic obligations | INSPECTED |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | CANONICAL PROCESS ADAPTER | project-map reconstruction, repair and Senior stop | INSPECTED |
| `DEV/PROJECT_MAP.md` | DERIVATIVE LOCATOR | owner/consumer dependency discovery | INSPECTED FOR ROUTING |
| `DEV/CURRENT_PROGRESS.md` | CURRENT-PROGRESS AUTHORITY | WP-12 Step-1 completion and mandatory Senior gate | INSPECTED |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | SEQUENCING AUTHORITY | R2.7 order and no-implementation boundary | INSPECTED |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-execution-protocol.md` | EXECUTION PROTOCOL | durable R2.7 cursor and domain loop | INSPECTED |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md` | ACTIVE PROGRAM BRIEF | WP-12 matrix fields and bidirectional proof | INSPECTED |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md` | SCOPE INVENTORY | WP-12 questions and neighboring domains | INSPECTED |
| `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md` | OWNER DECISION | whole-project and no-broad-implementation scope | INSPECTED |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md` | TASK-LOCAL CURSOR | WP-12 topic and subordinate handoff state | INSPECTED |
| `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | DERIVATIVE LOCATOR | current canonical-owner routing | INSPECTED FOR ROUTING |

## 2. Canonical owner constraints

| Source | Authority role | Required scope | Status |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md` | CANONICAL | atomic segment contents, external-boundary prohibition, execution owners | INSPECTED |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md` | CANONICAL | native-owner recovery, routing, derived rebuild and lost HOT | INSPECTED |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md` | CANONICAL | SOFT/HARD, scope policy, dirty/exposure and stale timer debt | INSPECTED |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md` | CANONICAL | frozen attempt, complete closure, CAS and dirty generations | INSPECTED |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md` | CANONICAL | current-authority-first hydration and checkpoint boundary | INSPECTED |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md` | CANONICAL | live partitions, exact-source CAS and closed-source recovery | INSPECTED |
| `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md` | CANONICAL | SQLite-format non-authority and bounded retrieval | INSPECTED |
| `DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-09-context-loading-resource-bounds-realization-canonical-spec.md` | CLOSED UPSTREAM INPUT | runtime-local cache boundary; F05 to WP-12 | INSPECTED |
| `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-10-durable-campaign-record-family-completeness-canonical-spec.md` | CLOSED UPSTREAM INPUT | logical family allocation without HOT choice | INSPECTED |
| `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md` | CLOSED UPSTREAM INPUT | route-law hydration and derived-index separation; F01 | INSPECTED |
| `DEV/ARCHITECTURE/ACTOR_MODEL.md` | ARCHITECTURE CONTRACT | Actor SOFT working-state and publication boundary | REQUIRED STEP-2 INSPECTION |
| `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md` | ARCHITECTURE CONTRACT | admitted class/owner constraints | REQUIRED STEP-2 INSPECTION |

## 3. Current runtime, schema and machine consumers

| Source | Authority role | Required scope | Status |
|---|---|---|---|
| `GAME/CORE/RUNTIME.md` | SHIPPED RUNTIME CONSUMER | hot working set and persistence pipeline | INSPECTED |
| `GAME/CORE/STORAGE.md` | SHIPPED RUNTIME CONSUMER | cached frontier, lazy reads and campaign/live split | INSPECTED |
| `GAME/CORE/DURABILITY_GUARD.md` | SHIPPED RUNTIME DEBT EVIDENCE | one-hour frontier behavior versus Step-5.5 | INSPECTED |
| `GAME/CORE/PERSISTENCE.md` | SHIPPED RUNTIME CONSUMER | campaign transaction and dirty clearing | INSPECTED |
| `GAME/CORE/SAVE_CONTRACT.md` | SHIPPED RUNTIME CONSUMER | save materialization and local completeness | INSPECTED |
| `GAME/CORE/SESSION.md` | SHIPPED RUNTIME CONSUMER | restart, long-gap and checkpoint behavior | INSPECTED |
| `GAME/CORE/LIVE_SCENE.md` | SHIPPED RUNTIME CONSUMER | cached live state, CAS and compaction | INSPECTED |
| `GAME/SCHEMA/campaign_manifest.schema.yaml` | SHIPPED SCHEMA | root selectors, checkpoint pointer and runtime identity | INSPECTED |
| `GAME/SCHEMA/current_state.schema.yaml` | SHIPPED SCHEMA | compact current routing; no pending bucket | INSPECTED |
| `GAME/SCHEMA/live_scene.schema.yaml` | SHIPPED SCHEMA | current live overlay fields and single-file boundary | INSPECTED |
| `GAME/SCHEMA/checkpoint.schema.yaml` | SHIPPED SCHEMA / DEBT EVIDENCE | stale checkpoint fields against Step-5.7 | INSPECTED |
| `GAME/SCHEMA/dnd_storage.schema.yaml` | SHIPPED SCHEMA / DIRECT STORAGE DISCOVERY + RUNTIME-PROVENANCE CONTRACT | exact-root storage discovery, storage-format identity, baseline runtime provenance and the baseline-versus-existing-campaign runtime-selection/write boundary; inspect as current machine contract only and reconcile against owning storage/runtime semantics | REQUIRED STEP-2 INSPECTION |
| `GAME/TEMPLATE/STORAGE_README.md` | SHIPPED STORAGE-TEMPLATE SUPPORTING SURFACE | human-facing storage-main/per-campaign-branch model and storage workflow; inspect only for consistency with owning storage/branch/runtime contracts and never derive semantic authority from template prose | REQUIRED STEP-2 INSPECTION |
| `DEV/CATALOG/core-catalog.json` | DEV MACHINE CONTRACT | owner/runtime vocabulary and retired classes | REQUIRED STEP-2 INSPECTION |
| `DEV/CATALOG/identifier-policies.json` | DEV MACHINE CONTRACT | stable and composite ID constraints | REQUIRED STEP-2 INSPECTION |
| `DEV/SCHEMAS/runtime-command-state.schema.json` | DEV MACHINE CONTRACT | command lifecycle working-copy fields | REQUIRED STEP-2 INSPECTION |
| `DEV/SCHEMAS/runtime-resolution-state.schema.json` | DEV MACHINE CONTRACT | resolution execution/fixed-RNG fields | REQUIRED STEP-2 INSPECTION |
| `DEV/SCHEMAS/runtime-continuation-state.schema.json` | DEV MACHINE CONTRACT | suspended-generation working-copy fields | REQUIRED STEP-2 INSPECTION |
| `DEV/SCHEMAS/execution-segment.schema.json` | DEV MACHINE CONTRACT | segment atomicity evidence | REQUIRED STEP-2 INSPECTION |
| `DEV/TESTS/test_hourly_durability_contract.py` | TEST / DEBT EVIDENCE | stale timer assertions needing later disposition | INSPECTED FOR ROUTING |
| `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md` | SCENARIO CONSUMER | campaign transaction failure cases | REQUIRED STEP-2 INSPECTION |
| `DEV/TESTS/DURABILITY_BOUNDARY_CASES.md` | SCENARIO CONSUMER | exposure and boundary cases | REQUIRED STEP-2 INSPECTION |
| `DEV/TESTS/LIVE_SCENE_CASES.md` | SCENARIO CONSUMER | live currentness/CAS cases | INSPECTED |
| `DEV/TOOLS/run_maintenance_audit.py` | DEV VERIFICATION ENTRYPOINT | current audit coverage and future validation gap | REQUIRED STEP-2 INSPECTION |

## 4. Discovery and completeness route

Step 2 must inspect every `REQUIRED STEP-2 INSPECTION` row before making a
realization claim. It must also follow the command, resolution, continuation,
execution-segment, Actor/Asset/Effect and identifier references exposed by those
sources; inspect the actual current consumers for every proposed structure; and
add any discovered owner, schema, template, test or maintenance consumer to this
manifest before claiming coverage. No unlisted current structure is excluded
merely because it was not visible during Step 1.
