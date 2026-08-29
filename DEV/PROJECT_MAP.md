# HDM Repository Project Map

Status: **NON-NORMATIVE INTERNAL NAVIGATION INDEX**

Last structural inventory: 2026-08-29

## 1. Purpose

This file is a service map for development work. It answers:

- what major responsibility areas exist;
- where to begin research for a concern;
- which neighboring surfaces are likely dependencies;
- which artifact families are authority, evidence, provenance or implementation support.

It is **not** a semantic source of truth. It intentionally does not restate full contracts, schemas, decisions or gameplay rules. If this map conflicts with an owning source, current roadmap/status or the repository tree, the owner/tree wins and this map is stale.

### 1.1 Fresh-session research route

```text
current remote ref/state
-> AGENTS.md
-> DEV/DESIGN_PROCESS.md
-> DEV/ARCHITECTURE/DESIGN_PROCESS.md
-> DEV/PROJECT_MAP.md
-> DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md when sequencing matters
-> concern route below
-> task-specific Source Manifest
-> actual owning artifacts
-> relevant schemas/tests/runtime consumers/research evidence
```

Do not preload the whole repository merely because it is large. Use this map to construct the relevant dependency subgraph and then inspect that subgraph deeply enough for the claims being made.

**HARD CRITIC ROUTE:** both the Step-1 Task-Brief critic and the Step-6 adversarial/candidate critic reconstruct the task-specific direct-and-indirect dependency subgraph from this map and inspect actual owners, accepted/superseding decisions, schemas, tests and consumers. A module-local critique is incomplete.

### 1.2 Source-role legend

- **CANONICAL / OWNING** — current semantic authority.
- **CANONICAL AMENDMENT / OWNER DECISION** — accepted final change/decision that may supersede earlier wording.
- **DERIVATIVE LOCATOR / INDEX** — navigation/integration aid only.
- **RESEARCH INPUT** — durable evidence/findings/experiments/ideas; not architecture authority by retention alone.
- **DESIGN PROVENANCE** — process/history explaining how a result was reached; not default implementation-planning authority.
- **HISTORICAL / SUPERSEDED DERIVATION** — provenance/background only unless reopening or supersession requires it.
- **IMPLEMENTATION / MACHINE CONTRACT / TEST** — concrete realization/evidence that may constrain or verify architecture.

Similar terminology does not imply equal authority.

---

## 2. Coverage convention and Superpowers artifact taxonomy

Large homogeneous families are grouped by path/pattern rather than manually enumerated:

- `DEV/SCHEMAS/*.schema.json` — development machine-contract schemas;
- `DEV/TESTS/test_*.py` — executable regression/contract tests;
- `DEV/TESTS/*_CASES.md` and related Markdown cases — scenario/acceptance catalogs;
- `DEV/docs/superpowers/research/*.md` — durable research/experiment/idea results;
- `DEV/docs/superpowers/design/*.md` — design-process/provenance history;
- `DEV/docs/superpowers/specs/*.md` — final accepted implementation-facing specs/amendments/owner decisions;
- `DEV/docs/superpowers/plans/*.md` — implementation plans/execution state after approved design.

`DEV/docs/superpowers/README.md` is the short non-authoritative navigation entry for that four-directory taxonomy. Placement authority is `AGENTS.md`.

Default implementation-planning discovery is:

```text
current roadmap/status
-> current durable DEV/ARCHITECTURE owners
-> final accepted DEV/docs/superpowers/specs/
-> implicated machine contracts/tests/runtime consumers
```

`design/` and `research/` are read when provenance, reopening, evidence applicability or audit requires them. They are not bulk-read by default to reconstruct already accepted architecture.

The inserted **Documentation Corpus Refactor** is currently migrating the historical `research/` + `specs/` corpus into this taxonomy. During that work, exact physical placement of an old artifact is not evidence of its semantic class; the durable semantic census controls migration completeness, not this map.

---

## 3. Repository ownership geometry

```text
repository root
├── GAME/   exact source tree shipped in the runtime package
├── DEV/    development-only architecture, catalogs, schemas, tests, tools and Superpowers artifacts
├── .github/ CI/release workflow infrastructure
└── root legal/metadata/repository governance
```

`AGENTS.md` owns repository placement/boundary rules. `GAME/` and `DEV/` must not leak into one another for development convenience.

---

## 4. Start here by concern

| Concern | Primary surfaces | Frequent neighbors |
|---|---|---|
| Architecture process / current stage | `DEV/DESIGN_PROCESS.md`, `DEV/ARCHITECTURE/DESIGN_PROCESS.md`, `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | `CANONICAL_ARCHITECTURE_INDEX.md`, final accepted `specs/`, task-specific design/research only when required |
| Implementation execution | `DEV/DEVELOPMENT_EXECUTION_PROCESS.md`, approved spec + implementation plan | affected architecture owners, tests, machine contracts, execution-status file |
| Integrated accepted architecture lookup | `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | actual owning architecture documents + final accepted `specs/` + current roadmap |
| Architecture research / Round-2 idea pool | `DEV/docs/superpowers/research/HDM_External_Architecture_Idea_Dossier_2026-08-21.md` | current roadmap, accepted owners/decisions, applicable runtime/schema/test owners |
| Host/platform feasibility / LLM orchestration | durable feasibility/validation research under `research/` | Step-4 owner/amendment, R2.3/R2.4/R2.6 accepted specs, runtime role-context consumers |
| Catalog/class ownership | `CATALOG_CONTRACTS.md`, `CATALOG_INVENTORY.md`, `ENTITY_STRUCTURES.md`, `CATALOG_RESOLUTION.md`, `RULESET_PACKAGE_IDENTITY.md`, `DEV/CATALOG/` | `DEV/SCHEMAS/`, ruleset package provenance, Actor/Asset/Activity/Rule Element models, catalog tests |
| Deterministic mechanics/execution | `ACTIVITY_MODEL.md`, `RULE_ELEMENT_MODEL.md`, `ACTIVITY_PRIMITIVE_CONTRACTS.md`, Step-3 final spec | `RUNTIME.md`, `MECHANICS_INTEGRITY.md`, `RANDOMNESS.md`, runtime/value schemas/tests |
| Character progression / READY_PC | `CHARACTER_PROGRESSION_READY_PC_SEED.md` | Actor/Asset/Effect owners, character readiness/runtime modules, package seeds/schemas/tests |
| HP/LifeState/effects/recovery | `HEALTH_EFFECTS_RECOVERY.md` | Actor/Resource/Effect/Condition models, temporal/recovery owners, package seed/validator/tests |
| Domain rules coverage | `DOMAIN_RULES_COVERAGE.md` | package coverage machine artifacts, Step-3 execution, domain CORE modules, S6D package tests |
| Campaign House Rules / rulings | `CAMPAIGN_HOUSE_RULES.md`, `HOUSE_RULES_MECHANICAL_BOUNDARY.md`, `GAME/CAMPAIGN/RULES/HOUSE_RULES.*` | `ACCESS_CONTROL.md`, `ADJUDICATION.md`, Context Runtime, publication/recovery/currentness, policy schemas/tests |
| Ruleset package machine closure | `RULESET_PACKAGE_MACHINE_CLOSURE.md`, `RULESET_PACKAGE_IDENTITY.md` | catalog admission/resolution, package manifest/lock, validators/build/load paths/tests |
| Persistence / durability / recovery | `GAME/CORE/STORAGE.md`, `PERSISTENCE.md`, `DURABILITY_GUARD.md`, `SAVE_CONTRACT.md`, `SESSION.md`, `INTEGRITY.md` | `RUNTIME.md`, `RANDOMNESS.md`, live/multiplayer/chronology, checkpoint/current/session schemas, Step-5 final specs |
| Multiplayer / shared mutable state | `GAME/CORE/MULTIPLAYER.md`, `LIVE_SCENE.md` | chronology, persistence, access control, live/session/player schemas, Step-5 + R2.5 final specs |
| Chronology / temporal continuity | `GAME/CORE/CHRONOLOGY.md`, accepted temporal architecture | runtime/randomness/live/multiplayer, temporal schemas, Step-5.1/5.3/5.9 final specs |
| Campaign bootstrap / creation | `GAME/INSTALL/00_DND_BOOTSTRAP.md`, `BOOTSTRAP_RUNTIME.md`, `NEW_CAMPAIGN_FAST_PATH.md`, `CAMPAIGN_SETUP.md`, `GAME/TOOLS/init_campaign.py` | `GAME/CAMPAIGN/`, campaign schemas, branch/access/persistence owners |
| Runtime packaging / versioning / update | `DEV/TOOLS/release_builder.py`, `run_release_build.py`, `DEV/RELEASE/`, `.github/workflows/release-runtime.yml`, `GAME/ENGINE_VERSION.yaml`, `ENGINE_UPDATES.md` | install, migrations, release/version tests |
| Rules/source routing | `GAME/RULES/`, `GAME/CORE/SOURCES.md`, `PLAY_POLICY.md` | domain CORE modules, character readiness, prep/worldgen, campaign House Rules |
| LLM reasoning / information / presentation | `AI_REASONING.md`, `GM_CRAFT.md`, `PREP.md`, `NARRATIVE.md`, `INFORMATION.md`, `LORE.md`, `NPC.md` | Step-4 final spec/amendment, role-context research evidence, R2.1–R2.4 final specs |
| Support / diagnostics / maintenance | `MAINTENANCE_COMMANDS.md`, `DEV/TOOLS/run_maintenance_audit`, `audit_engine.py` | session/integrity/storage/persistence/checkpoint schemas/tests |
| Access / repository/campaign ownership | `ACCESS_CONTROL.md`, `BRANCH_MODEL.md` | multiplayer, bootstrap, persistence, player/session schemas, House-Rules adoption |
| Consistency verification | `DEV/TOOLS/run_maintenance_audit`, `DEV/TESTS/`, `.github/workflows/validate.yml` | every catalog/schema/contract/path family being changed |

The table is a discovery aid. Correctness-sensitive work follows actual owners and consumers.

---

## 5. Root and CI infrastructure

- `AGENTS.md` — repository boundaries, fresh-session bootstrap, evidence discipline, Superpowers artifact placement, GitHub transport and checkpoint rules.
- `.github/workflows/validate.yml` — maintenance audit + DEV unit tests for active branches/PRs.
- `.github/workflows/release-runtime.yml` — runtime release build/publication workflow.
- `.gitignore` — repository-local generated/cache exclusions.
- `README.md` — manually curated public overview with a special editorial contract; not an automatic development index.
- root/runtime legal files and `LICENSES/` — legal/attribution owners.

---

## 6. `DEV/` — development-only source

### 6.1 Process and version markers

- `DEV/DESIGN_PROCESS.md` — canonical generic architecture/deep-work process.
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md` — HDM-specific adapter/review gates.
- `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` — canonical implementation-execution process after approved design.
- `DEV/ENGINE_DEVELOPMENT.yaml` — development/release metadata.
- `DEV/PROJECT_MAP.md` — this navigation/dependency map.
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` — current Round-2 sequencing/status authority.
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` — derivative integrated semantic locator; never overrides owners/current roadmap.

### 6.2 `DEV/ARCHITECTURE/` durable owners

Major current architecture owners include:

- authority/topology: `ACCESS_CONTROL.md`, `BRANCH_MODEL.md`;
- catalogs/entities: `CATALOG_CONTRACTS.md`, `CATALOG_INVENTORY.md`, `CATALOG_ADMISSION.md`, `CATALOG_RESOLUTION.md`, `ENTITY_STRUCTURES.md`, `RULESET_PACKAGE_IDENTITY.md`;
- mechanical models: `ACTOR_MODEL.md`, `ASSET_MODEL.md`, `ACTIVITY_MODEL.md`, `RULE_ELEMENT_MODEL.md`;
- S6D deterministic contracts: `CALCULATION_SELECTOR_METADATA.md`, `MECHANICAL_CONTEXT.md`, `PORTABLE_ACTIVITY_VALUES.md`, `ACTIVITY_PRIMITIVE_CONTRACTS.md`;
- character/domain closure: `CHARACTER_PROGRESSION_READY_PC_SEED.md`, `HEALTH_EFFECTS_RECOVERY.md`, `DOMAIN_RULES_COVERAGE.md`;
- House Rules/rulings: `CAMPAIGN_HOUSE_RULES.md`, `HOUSE_RULES_MECHANICAL_BOUNDARY.md`;
- ruleset machine closure: `RULESET_PACKAGE_MACHINE_CLOSURE.md`;
- support/routing: `MAINTENANCE_COMMANDS.md`, `NEAR_TERM_ROADMAP.md`, `CANONICAL_ARCHITECTURE_INDEX.md`.

Historical/derivation documents such as `CATALOG_DESIGN_STATUS.md`, `CATALOG_MODEL.md`, `MECHANICAL_RUNTIME_PROPOSAL.md` and `CRITICAL_ARCHITECTURE_AUDIT.md` do not override later accepted owners merely because they remain under `DEV/ARCHITECTURE/`.

### 6.3 `DEV/CATALOG/`

Machine-readable current catalog/admission/identity/mechanical surfaces. Read their schemas/tests and owning architecture before changing them. JSON presence is machine contract/evidence, not prose authority by itself.

### 6.4 `DEV/SCHEMAS/`

Development-only JSON schemas for catalog/entity/domain/execution/runtime/value/protocol/package contracts. Follow owning architecture/spec references to the matching schemas rather than preloading the directory.

### 6.5 `DEV/TESTS/`

- `test_*.py` — executable unit/regression/contract tests run by CI/audit.
- `*_CASES.md` and related Markdown — scenario/acceptance/adversarial catalogs.

Search tests whenever a contract or path changes. Existing tests receive no presumption of correctness when a current owner supersedes their assumption.

### 6.6 `DEV/TOOLS/`

- `run_maintenance_audit` / `audit_engine.py` — consistency/audit entry point and implementation.
- `dev_tool_environment.py` / `requirements-dev-tools.txt` — isolated dev-tool environment.
- `run_release_build.py` / `release_builder.py` — release validation/composition.
- focused validators/builders/loaders for current S6D package/machine contracts.

### 6.7 `DEV/RELEASE/`

`CHECKLIST.md`, `VERSIONING.md` and related release-development policy.

### 6.8 `DEV/docs/superpowers/`

```text
README.md   non-authoritative taxonomy/navigation
research/   durable research/experiment/idea results
design/     design-process/provenance history
specs/      final accepted implementation-facing specs/amendments/owner decisions
plans/      implementation plans/execution status
```

Do not infer semantic role solely from an old filename/path during the active corpus refactor. The migration census reviews the historical `research/` + `specs/` content and may split/promote before moving. Final accepted law must not remain hidden only in `research/` or `design/`.

---

## 7. `GAME/` — exact runtime source tree

`GAME/` contents are flattened into the runtime release package root. `DEV/` is not shipped.

### 7.1 Runtime/version/legal root

- `ENGINE_VERSION.yaml` — shipped engine identity/compatibility marker.
- runtime legal/attribution files — release-validated legal surface.

### 7.2 `GAME/CORE/`

`CORE_INDEX.md` is the local routing summary, not a semantic override.

Always-active/general routing includes `RUNTIME.md`, `AI_REASONING.md`, `PLAY_POLICY.md`, `DURABILITY_GUARD.md`, `MECHANICS_INTEGRITY.md`, `CHARACTER_READINESS.md`, `ANTIPATTERNS.md`.

Bootstrap/lifecycle includes `BOOTSTRAP_RUNTIME.md`, `ENGINE_UPDATES.md`, `NEW_CAMPAIGN_FAST_PATH.md`, `CAMPAIGN_SETUP.md`, `DIEGETIC_ONBOARDING.md`, `CAMPAIGN_IDENTITY.md`, `CAMPAIGN_CARD.md`, `CAMPAIGN_OPERATIONS.md`, `SESSION.md`.

Gameplay/domain modules include `CHARACTER.md`, `ADJUDICATION.md`, `RANDOMNESS.md`, `INFORMATION.md`, `LORE.md`, `NPC.md`, `PREP.md`, `NARRATIVE.md`, `GM_CRAFT.md`, `COMBAT.md`, `MAGIC.md`, `EXPLORATION.md`, `DIALOGUE.md`, `ENCOUNTERS.md`, `ADVANCEMENT.md`, `REWARDS.md` and related modules.

Persistence/shared-state modules include `STORAGE.md`, `PERSISTENCE.md`, `SAVE_CONTRACT.md`, `INTEGRITY.md`, `MULTIPLAYER.md`, `LIVE_SCENE.md`, `CHRONOLOGY.md`, `SOURCES.md`.

### 7.3 `GAME/SCHEMA/`

Persistent campaign/runtime schemas: campaign identity/config/card/storage, House-Rules policy, session/current/scene/player/PC/NPC/world records, events/checkpoints/index/live-scene and related formats.

### 7.4 `GAME/CAMPAIGN/`

New-campaign template copied into campaign root by `GAME/TOOLS/init_campaign.py`: manifest/config/card/readme, state/scenes, world record roots, indexes, log/checkpoint/session templates and `RULES/HOUSE_RULES.md/.yaml`.

### 7.5 `GAME/INSTALL/`, `GAME/RULES/`, `GAME/MIGRATIONS/`, `GAME/TEMPLATE/`, `GAME/TOOLS/`

These own runtime installation/Project Instructions, rules/source routing, persistent migration conventions, storage-template docs and campaign scaffold tooling respectively.

---

## 8. Dependency hot paths

### 8.1 Persistence / recovery

```text
CANONICAL_ARCHITECTURE_INDEX -> owning final Step-5 specs
    -> RUNTIME / STORAGE / SESSION
    -> DURABILITY_GUARD / SAVE_CONTRACT
    -> PERSISTENCE / INTEGRITY / RANDOMNESS
    -> MULTIPLAYER / LIVE_SCENE / CHRONOLOGY when implicated
    -> checkpoint/current/session/live schemas
    -> MAINTENANCE_COMMANDS + DEV tests
```

### 8.2 Mechanical execution

```text
catalog contracts/inventory
    -> Actor / Asset / Activity / Rule Element owners
    -> S6D selector/context/value/primitive owners
    -> final Step-3 execution spec
    -> DEV catalogs/schemas
    -> GAME RUNTIME / MECHANICS_INTEGRITY / RANDOMNESS
    -> deterministic tests
```

### 8.3 Campaign creation / update

```text
INSTALL + Project Instructions
    -> BOOTSTRAP_RUNTIME / NEW_CAMPAIGN_FAST_PATH
    -> BRANCH_MODEL / ACCESS_CONTROL
    -> init_campaign.py
    -> GAME/CAMPAIGN + GAME/SCHEMA
    -> PERSISTENCE

engine/ruleset update
    -> ENGINE_UPDATES
    -> RULESET_PACKAGE_IDENTITY / CATALOG_RESOLUTION / machine closure
    -> ACCESS_CONTROL
    -> package provenance + resolved lock
    -> campaign version/ruleset currentness
    -> DEV release/version policy
    -> GAME/MIGRATIONS when persistent transformation is required
```

### 8.4 Multiplayer

```text
accepted shared-state architecture
    -> ACCESS_CONTROL / BRANCH_MODEL
    -> MULTIPLAYER / LIVE_SCENE
    -> player/session/live schemas
    -> PERSISTENCE / CHRONOLOGY
    -> R2.5 final collaboration/currentness spec
```

### 8.5 LLM information / continuity / role context / Story

```text
Step-4 final truth/knowledge/context spec
    -> accepted single-context amendment
    -> final Step-5 Story/transcript/disclosure specs
    -> final R2.1/R2.2/R2.3/R2.4 specs
    -> research protocols only when evidence/applicability must be inspected
    -> AI_REASONING / INFORMATION / LORE / NPC / NARRATIVE / PREP / GM_CRAFT
    -> current schemas/tests where machine realization is implicated
```

### 8.6 House Rules / rulings

```text
CAMPAIGN_HOUSE_RULES
    -> final accepted owner decision
    -> ACCESS_CONTROL
    -> HOUSE_RULES.md/.yaml + schemas
    -> Context Runtime eligibility/currentness
    -> publication/recovery/multiplayer currentness
    -> ADJUDICATION + deterministic Activity/Rule Element handoff
    -> richer typed-input schemas/tests
```

### 8.7 Ruleset package / domain closure

```text
CHARACTER_PROGRESSION_READY_PC_SEED
HEALTH_EFFECTS_RECOVERY
DOMAIN_RULES_COVERAGE
HOUSE_RULES_MECHANICAL_BOUNDARY
    -> RULESET_PACKAGE_MACHINE_CLOSURE
    -> RULESET_PACKAGE_IDENTITY / CATALOG_RESOLUTION / CATALOG_ADMISSION
    -> package manifest/lock/seed members
    -> validators/build/load paths
    -> focused + integrated tests
```

Do not generalize dormant/nonselectable vocabulary into current capability merely because a catalog name exists.

---

## 9. Research/discovery rule

For substantive repository work:

1. inspect current remote ref/tree;
2. use this map to identify likely owners and neighboring dependency surfaces;
3. read current roadmap/status when sequencing matters;
4. build the task-specific Source Manifest;
5. use derivative indexes only to locate owning accepted sources;
6. read actual owners/contracts/schemas/tests and, where needed, research/design provenance to the depth required by the claim;
7. search concrete symbols/paths for consumers and stale references after structural discovery;
8. treat zero-result keyword search as non-evidence of absence until the relevant tree/local indexes are checked;
9. run the evidence/synthesis completeness gate before roadmap/specification/coverage claims;
10. for either architecture critic, record direct and indirect owners/routes checked;
11. update this map when a responsibility/primary-entry/dependency/taxonomy change would make future discovery materially misleading.

A file move/addition/deletion inside an already covered homogeneous family does not require a per-file map edit. Do not place a correctness rule only in this map; put it in its owning contract/spec/schema and link/summarize here.