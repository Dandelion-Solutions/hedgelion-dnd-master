# HDM Repository Project Map

Status: **NON-NORMATIVE INTERNAL NAVIGATION INDEX**

Last structural inventory: 2026-08-21

## 1. Purpose

This file is a service map for development work. It answers:

- what major files/directories exist;
- what responsibility each area has;
- where to begin research for a concern;
- which neighboring surfaces are likely dependencies.

It is **not** a semantic source of truth. It intentionally does not restate full
contracts, schemas, decisions, or gameplay rules.

If this map conflicts with the referenced source file, schema, machine catalog,
canonical specification, current roadmap/status, or repository tree, the source
wins and this map is stale.

Use this file for discovery; read the actual owning artifacts for correctness.

## 2. Coverage convention

The map lists stable human-authored/runtime surfaces individually where their
responsibility matters. Large homogeneous families are grouped by path/pattern so
this index can scale without becoming a second manually maintained copy of the
repository:

- `DEV/SCHEMAS/*.schema.json` — development machine-contract schemas;
- `DEV/TESTS/test_*.py` — executable regression/contract tests;
- `DEV/TESTS/*_CASES.md` and related Markdown cases — scenario/acceptance case catalogs;
- `DEV/docs/superpowers/specs/*.md` — dated architecture/design derivation and canonical specs;
- `DEV/docs/superpowers/plans/*.md` — dated implementation plans created after approved designs.

When a task touches one of these families, inspect filenames/current references
rather than assuming this map enumerates every member.

## 3. Repository ownership geometry

```text
repository root
├── GAME/   exact source tree shipped in the runtime package
├── DEV/    development-only architecture, catalogs, schemas, tests, tools, plans
├── .github/ CI/release workflow infrastructure
└── root legal/metadata/repository governance
```

`AGENTS.md` owns repository placement/boundary rules. `GAME/` and `DEV/` must not
leak into one another merely for development convenience.

## 4. Start here by concern

| Concern | Primary surfaces | Frequent neighbors |
|---|---|---|
| Architecture process / current stage | `DEV/DESIGN_PROCESS.md`, `DEV/ARCHITECTURE/DESIGN_PROCESS.md`, `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`, relevant canonical specs in `DEV/docs/superpowers/specs/` |
| Integrated canonical architecture lookup (Steps 1–5) | `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | owning canonical specs/model contracts, `NEAR_TERM_ROADMAP.md`, Step-5.14 review artifacts |
| Catalog/class ownership | `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`, `CATALOG_INVENTORY.md`, `ENTITY_STRUCTURES.md`, `CATALOG_RESOLUTION.md`, `DEV/CATALOG/` | `DEV/SCHEMAS/`, Actor/Asset/Activity/Rule Element models, catalog tests |
| Deterministic mechanics/execution | `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`, `RULE_ELEMENT_MODEL.md`, accepted Step-2/Step-3 specs | `GAME/CORE/RUNTIME.md`, `MECHANICS_INTEGRITY.md`, `RANDOMNESS.md`, runtime/value schemas/tests |
| Persistence / durability / recovery | `GAME/CORE/STORAGE.md`, `PERSISTENCE.md`, `DURABILITY_GUARD.md`, `SAVE_CONTRACT.md`, `SESSION.md`, `INTEGRITY.md` | `RUNTIME.md`, `RANDOMNESS.md`, `LIVE_SCENE.md`, `MULTIPLAYER.md`, checkpoint/current/session schemas, Step-5 specs, `MAINTENANCE_COMMANDS.md` |
| Multiplayer / shared mutable state | `GAME/CORE/MULTIPLAYER.md`, `LIVE_SCENE.md` | `CHRONOLOGY.md`, `PERSISTENCE.md`, access control, live/session/player schemas, Step-5 specs |
| Chronology / temporal continuity | `GAME/CORE/CHRONOLOGY.md`, accepted Step-2 temporal specs | `RUNTIME.md`, `RANDOMNESS.md`, `LIVE_SCENE.md`, `MULTIPLAYER.md`, Step-5.1+ specs |
| Campaign bootstrap / creation | `GAME/INSTALL/00_DND_BOOTSTRAP.md`, `GAME/CORE/BOOTSTRAP_RUNTIME.md`, `NEW_CAMPAIGN_FAST_PATH.md`, `CAMPAIGN_SETUP.md`, `GAME/TOOLS/init_campaign.py` | `GAME/CAMPAIGN/`, campaign schemas, `BRANCH_MODEL.md`, `ACCESS_CONTROL.md` |
| Runtime packaging / versioning / update | `DEV/TOOLS/release_builder.py`, `run_release_build.py`, `DEV/RELEASE/`, `.github/workflows/release-runtime.yml`, `GAME/ENGINE_VERSION.yaml`, `GAME/CORE/ENGINE_UPDATES.md` | `GAME/INSTALL/`, `GAME/MIGRATIONS/`, release tests |
| Rules/source routing | `GAME/RULES/`, `GAME/CORE/SOURCES.md`, `PLAY_POLICY.md` | domain CORE modules, character readiness, prep/worldgen |
| LLM/runtime reasoning and presentation | `GAME/CORE/AI_REASONING.md`, `GM_CRAFT.md`, `PREP.md`, `NARRATIVE.md`, `INFORMATION.md`, `LORE.md` | Step-4 canonical spec and deferred Step-4 machine realization |
| Support / diagnostics / maintenance | `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` | `GAME/CORE/SESSION.md`, `INTEGRITY.md`, `STORAGE.md`, `PERSISTENCE.md`, checkpoint/session schemas, Step-5 recovery design |
| Access / repository/campaign ownership | `DEV/ARCHITECTURE/ACCESS_CONTROL.md`, `BRANCH_MODEL.md` | `GAME/CORE/MULTIPLAYER.md`, bootstrap, persistence, player/session schemas |
| Consistency verification | `DEV/TOOLS/run_maintenance_audit`, `audit_engine.py`, `DEV/TESTS/`, `.github/workflows/validate.yml` | catalogs/schemas/contracts being changed |

This table is a discovery aid. A deep task must still inspect the current tree and
follow references from the owning artifacts.

---

# 5. Root and CI infrastructure

- `AGENTS.md` — repository ownership boundaries, authoritative development/release workflow and placement rules.
- `.github/workflows/validate.yml` — CI validation: maintenance audit plus DEV unit tests.
- `.github/workflows/release-runtime.yml` — tagged/runtime release build and publication workflow.
- `.gitignore` — repository-local generated/cache exclusions.
- `README.md` — manually curated public repository overview; not an automatic development index.
- `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md` — root legal/attribution materials.
- `LICENSES/SRD-5.2.1-ATTRIBUTION.md` — SRD attribution source mirrored into runtime legal surface.

---

# 6. `DEV/` — development-only source

## 6.1 Process and version markers

- `DEV/DESIGN_PROCESS.md` — canonical generic architecture/deep-work procedure.
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md` — HDM-specific adapter/additional constraints.
- `DEV/ENGINE_DEVELOPMENT.yaml` — development engine/revision metadata; richer than the shipped runtime marker.
- `DEV/PROJECT_MAP.md` — this non-normative repository navigation/dependency map.
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` — derivative Steps-1–5 semantic locator/integration map optimized for cross-stage research and Step-5.14; never overrides its linked primary sources.

## 6.2 `DEV/ARCHITECTURE/`

Current durable architecture/navigation documents:

- `ACCESS_CONTROL.md` — engine repository authority, campaign creator/player authority and write-routing authorization boundaries.
- `ACTIVITY_MODEL.md` — executable declarative Activity definition and `runtime.resolution` invocation boundary.
- `ACTOR_MODEL.md` — progressive `world.actor` materialization, archetype/instance split and actor mechanical-state ownership.
- `ASSET_MODEL.md` — unified reusable/instance model for physical/conceptual assets and their placement/use/lifecycle boundary.
- `BRANCH_MODEL.md` — engine repository vs runtime package vs campaign-storage topology; campaign/live branch roles and package boundaries.
- `CANONICAL_ARCHITECTURE_INDEX.md` — non-normative cross-stage canonical locator, ownership/invariant map and Step-5.14 scenario router for Steps 1–5.
- `CATALOG_CONTRACTS.md` — universal definition/world/runtime class-admission and record-envelope contracts.
- `CATALOG_INVENTORY.md` — reviewed class inventory/classification; machine IDs live in `DEV/CATALOG/core-catalog.json`.
- `CATALOG_RESOLUTION.md` — deterministic `ResolvedCatalogContext`, definition-ID uniqueness and catalog evolution/resolution rules.
- `CRITICAL_ARCHITECTURE_AUDIT.md` — completed Step-1 audit history/findings and dispositions.
- `ENTITY_STRUCTURES.md` — minimum/expected field structures and definition-binding inventory for catalog/world records.
- `MAINTENANCE_COMMANDS.md` — internal, intentionally player-undocumented operator/support command contract proposal (`HDM_EXPORT_CURRENT_LOG`, `HDM_EXPORT_CHECKPOINT_LOG`, `HDM_RESET_LAST_CHECKPOINT`).
- `NEAR_TERM_ROADMAP.md` — sequencing authority for the active mechanical architecture program.
- `RULE_ELEMENT_MODEL.md` — pure embedded passive contribution model and bounded reactive binding boundary.

Historical/derivation/status surfaces that must not override newer accepted contracts:

- `CATALOG_DESIGN_STATUS.md` — historical architecture/catalog status snapshot; current sequencing comes from `NEAR_TERM_ROADMAP.md`.
- `CATALOG_MODEL.md` — initial catalog taxonomy/derivation; points to newer normative inventory/contracts.
- `MECHANICAL_RUNTIME_PROPOSAL.md` — early physical hot-state/runtime proposal; useful for provenance, not authority where later canonical Steps 2–5 supersede it.

## 6.3 `DEV/CATALOG/`

Machine-readable current catalog surfaces; coordinated versions move together:

- `core-catalog.json` — closed class/capability/protocol vocabulary and IDs.
- `entity-structures.json` — machine field/definition-binding structure inventory.
- `identifier-policies.json` — stable identity/allocation policies including campaign allocator rules.
- `mechanical-surfaces.json` — registered deterministic mechanical selectors/operations/surfaces.

Read their schemas/tests before changing them. Human-readable architecture docs
explain semantics; these JSON files are machine contracts, not prose summaries.

## 6.4 `DEV/SCHEMAS/`

Development-only JSON Schemas for machine contracts. Major families include:

- catalog/envelope schemas (`catalog-definition`, `core-catalog`, `entity-structures`, identifier policies, world-record);
- domain-definition/state schemas (Actor, Asset, Resource, Effect, Condition and related Step-2 structures);
- execution/runtime schemas (command, intent plan, resolution, procedure, continuation and related Step-3 records);
- embedded value/protocol schemas (duration, temporal binding, execution segment, pending child, invocation facts, receipts, boundary occurrences and similar values).

The directory is intentionally treated as a schema family in this map. For a
specific contract, follow the owning architecture/spec references and then open
the matching current schema(s).

## 6.5 `DEV/TESTS/`

Two complementary test families:

- `test_*.py` — executable unit/regression/contract tests run by CI and the maintenance audit workflow;
- Markdown case files such as `*_CASES.md` — scenario, acceptance and adversarial case catalogs used to reason about behavior/coverage.

Tests cover repository/runtime boundaries, release/package behavior, bootstrap,
storage/persistence, catalog contracts, Step-2 mechanics, Step-3 execution,
Step-4 retirement, Step-5 contamination/frontier contracts and other current
machine invariants. Search this directory whenever a contract is changed; do not
assume a prose spec is the only consumer.

## 6.6 `DEV/TOOLS/`

- `run_maintenance_audit` — canonical developer audit entry point.
- `audit_engine.py` — engine consistency/audit implementation used by that entry point.
- `dev_tool_environment.py` — isolated `.hdm-devtools` dependency/environment management.
- `requirements-dev-tools.txt` — pinned developer-tool dependencies.
- `run_release_build.py` — canonical release-build entry point.
- `release_builder.py` — runtime boundary validation, deterministic package composition and release artifact generation.

## 6.7 `DEV/RELEASE/`

- `CHECKLIST.md` — release-readiness checklist and required verification/migration/package checks.
- `VERSIONING.md` — development/runtime versioning policy.

## 6.8 `DEV/docs/superpowers/`

- `specs/` — dated design chain artifacts. Status inside each artifact determines whether it is research, candidate, review, resolution, canonical or historical derivation. Prefer the latest canonical/current status references from roadmap/status docs rather than filename recency alone.
- `plans/` — implementation plans produced after approved designs. They are execution guidance, not architecture authority when a later canonical spec supersedes assumptions.

The accepted architecture through Step 5.13 is indexed in
`DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`; use that file to locate the
owning primary specification, then read the primary source before making a
correctness-sensitive decision. Numbered architecture sequencing remains owned by
`NEAR_TERM_ROADMAP.md`.

---

# 7. `GAME/` — exact runtime source tree

`GAME/` contents are flattened into the runtime release package root. `DEV/` is
not shipped. Generated package provenance such as release-package metadata may be
created by the release builder and therefore need not exist as a tracked GAME
source file.

## 7.1 Runtime/version/legal root

- `ENGINE_VERSION.yaml` — shipped runtime engine identity/compatibility marker.
- `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md`, `LICENSES/` — runtime legal/attribution material; release validation keeps required root/runtime copies coherent.

## 7.2 `GAME/CORE/` — runtime behavior contracts

Local routing summary: `GAME/CORE/CORE_INDEX.md`. It is itself a routing index,
not an override of module headers/contracts.

Always-active/general runtime guards and routing:

- `RUNTIME.md` — turn pipeline, agency, causality, runtime lifecycle/routing.
- `AI_REASONING.md` — LLM-specific correctness and reasoning discipline.
- `PLAY_POLICY.md` — runtime CORE activation/research policy.
- `DURABILITY_GUARD.md` — ordinary gameplay durability-boundary classifier (WHEN publication is required).
- `MECHANICS_INTEGRITY.md` — pre-narration mechanical proof/consistency gate.
- `CHARACTER_READINESS.md` — readiness gate for mechanically usable PCs.
- `CORE_INDEX.md` — module activation/routing summary.
- `ANTIPATTERNS.md` — extended runtime/GM failure catalogue for audit/debug.

Bootstrap/campaign lifecycle:

- `BOOTSTRAP_RUNTIME.md` — storage discovery/startup/runtime-package routing.
- `ENGINE_UPDATES.md` — release discovery and safe campaign engine integration.
- `NEW_CAMPAIGN_FAST_PATH.md` — scaffold-first new-campaign ordering/transport/latency contract.
- `CAMPAIGN_SETUP.md` — substantive character/world setup after scaffold creation.
- `DIEGETIC_ONBOARDING.md` — story-first onboarding/provisional identity.
- `CAMPAIGN_IDENTITY.md` — evolving campaign title/overview identity.
- `CAMPAIGN_CARD.md` — compact campaign-menu projection and refresh discipline.
- `CAMPAIGN_OPERATIONS.md` — campaign/session organization and maintenance operations.
- `SESSION.md` — session start/resume/end and coordination/maintenance-continuation state.

Gameplay/domain modules:

- `CHARACTER.md` — PC creation/player-character guidance.
- `ADJUDICATION.md` — uncertain actions, consequences and local rulings.
- `RANDOMNESS.md` — authoritative RNG/dice integrity and fixed-randomness behavior.
- `INFORMATION.md` — clues/perception/knowledge-boundary runtime guidance; review against Step-4 canonical model when changing information architecture.
- `NPC.md` — NPC agency/knowledge/relationships/continuity.
- `DIALOGUE.md` — social/dialogue handling.
- `EXPLORATION.md` — locations/investigation/travel/time/resources.
- `ENCOUNTERS.md` — encounter objectives/difficulty/environment.
- `COMBAT.md` — combat runtime behavior.
- `MAGIC.md` — spell/magic adjudication.
- `PROCESSES.md` — long-running threats/projects/clocks/off-screen change.
- `CHRONOLOGY.md` — fictional relative/partial ordering when temporal constraints matter.
- `WORLDGEN.md` — bounded world creation/expansion.
- `LORE.md` — history/culture/disputed lore/reveal guidance.
- `REWARDS.md` — economy/payment/treasure/ownership.
- `ADVANCEMENT.md` — level/rest/downtime/long-term progression.
- `SAFETY.md` — campaign boundaries/tone safety.
- `NARRATIVE.md` — narration/pacing/information density.
- `PREP.md` — situation-based preparation and bounded enrichment.
- `GM_CRAFT.md` — GM setup/prep/design/audit craft.

Persistence/shared-world/source modules:

- `STORAGE.md` — canonical campaign storage organization, hot working set, targeted reads/checkpoints.
- `PERSISTENCE.md` — GitHub campaign publication transaction/transport protocol (HOW).
- `SAVE_CONTRACT.md` — explicit-save completeness/materialization semantics.
- `INTEGRITY.md` — bounded recovery/repair when canon is suspect or corrupt.
- `MULTIPLAYER.md` — shared-world concurrency/access behavior.
- `LIVE_SCENE.md` — temporary live-epoch one-file CAS synchronization for shared actionable scenes.
- `SOURCES.md` — provenance/reference appendix and bounded source-research routing.

## 7.3 `GAME/SCHEMA/` — persistent campaign/runtime formats shipped to runtime

- `README.md` — schema-layer principles and schema index.
- `campaign_manifest.schema.yaml` — campaign branch identity/mode/engine/storage roots.
- `campaign_config.schema.yaml` — premise/tone/boundaries/advancement/world mode.
- `campaign_card.schema.yaml` — compact campaign discovery/menu projection.
- `dnd_storage.schema.yaml` — campaign-storage repository marker/baseline format.
- `session.schema.yaml` — per-chat/session coordination data.
- `current_state.schema.yaml` — compact active-scene/global chronology routing state.
- `scene.schema.yaml` — one active scene/environment state.
- `player.schema.yaml`, `pc.schema.yaml`, `npc.schema.yaml` — player binding and character records.
- `location.schema.yaml`, `faction.schema.yaml`, `item.schema.yaml`, `lore.schema.yaml`, `thread.schema.yaml` — persistent world/domain records.
- `event.schema.yaml` — compact semantic history event record.
- `checkpoint.schema.yaml` — sparse recovery descriptor/boundary format.
- `index.schema.yaml` — entity/index routing entries.
- `live_scene.schema.yaml` — temporary live shared-scene operational state.

These are stable persistent formats, not a directory to preload wholesale during
ordinary play.

## 7.4 `GAME/CAMPAIGN/` — new-campaign template source

`GAME/TOOLS/init_campaign.py` copies the **contents** of this directory into the
root of a new campaign branch. There is no `CAMPAIGN/` wrapper in current
campaign storage.

Current template responsibilities:

- `MANIFEST.yaml` — campaign identity, engine provenance and selected checkpoint pointer/configuration roots.
- `CONFIG.yaml` — campaign setup/configuration defaults.
- `CAMPAIGN_CARD.yaml` — discovery/menu projection template.
- `README.md` — protected player-facing campaign overview/guide blocks.
- `STATE/CURRENT.yaml` — compact current routing/chronology state.
- `STATE/SCENES/` — per-scene state records.
- `WORLD/{PCS,NPC,PLAYERS,LOCATIONS,FACTIONS,ITEMS,LORE,THREADS}/` — world/domain record storage roots.
- `INDEX/*.yaml` — routing indexes for corresponding record families.
- `LOG/_TEMPLATE.yaml` — semantic history record template/root.
- `CHECKPOINTS/_TEMPLATE.yaml` — checkpoint template/root.
- `SESSIONS/_TEMPLATE.yaml` — runtime session record template/root.
- `RULES/HOUSE_RULES.md` — campaign-local durable rulings/house rules.

## 7.5 `GAME/INSTALL/`

- `00_DND_BOOTSTRAP.md` — package bootstrap procedure executed before campaign-specific work.
- `PROJECT_INSTRUCTIONS.txt` — exact runtime Project Instructions copy; release tests enforce parity with the install README block.
- `README.md` — player/host installation instructions and canonical Project Instructions presentation.

## 7.6 `GAME/RULES/`

- `README.md` — local rules-layer purpose and ordinary-play source/ruling order.
- `INDEX.md` — compact rules navigation index.
- `OFFICIAL_SOURCES.md` — official source references; presence is not automatic authorization to browse them.

The rules layer is routing/support, not a bundled copy of PHB/DMG/SRD content.

## 7.7 `GAME/MIGRATIONS/`

- `README.md` — migration contract/conventions. Concrete migration files are added only when an engine change requires persistent campaign-data transformation.

Migrations modify campaign data/provenance, not engine source copied into a
campaign repository.

## 7.8 `GAME/TEMPLATE/`

- `STORAGE_README.md` — template README for campaign-storage default branch; explains storage repository role to its owner/users.

## 7.9 `GAME/TOOLS/`

- `init_campaign.py` — standard-library campaign scaffold generator. Copies `GAME/CAMPAIGN/` contents to a new campaign root and fills identity/provenance fields. No GitHub access; publication is a separate bootstrap responsibility.

---

# 8. Dependency hot paths

These are common cross-file dependency routes to check before concluding that a
single located file owns a problem.

## 8.1 Persistence/recovery

```text
CANONICAL_ARCHITECTURE_INDEX -> owning Step-5 canonical specs
    -> RUNTIME / STORAGE / SESSION
    -> DURABILITY_GUARD / SAVE_CONTRACT
    -> PERSISTENCE / INTEGRITY
    -> RANDOMNESS
    -> MULTIPLAYER / LIVE_SCENE / CHRONOLOGY when applicable
    -> checkpoint/current/session/live schemas
    -> MAINTENANCE_COMMANDS for support/recovery diagnostics
    -> DEV runtime/value schemas + regression tests
```

## 8.2 Mechanical execution

```text
Catalog contracts/inventory
    -> Activity / Rule Element / Actor / Asset models
    -> accepted Step-2 + Step-3 canonical specs
    -> DEV machine catalogs + schemas
    -> GAME RUNTIME / MECHANICS_INTEGRITY / RANDOMNESS
    -> Step-2/Step-3 tests
```

## 8.3 Campaign creation/update

```text
INSTALL bootstrap + Project Instructions
    -> BOOTSTRAP_RUNTIME / NEW_CAMPAIGN_FAST_PATH
    -> BRANCH_MODEL / ACCESS_CONTROL
    -> TOOLS/init_campaign.py
    -> GAME/CAMPAIGN template + GAME/SCHEMA
    -> PERSISTENCE

engine update
    -> ENGINE_UPDATES
    -> DEV release/version policy
    -> GAME/MIGRATIONS if persistent format changes
```

## 8.4 Multiplayer

```text
ACCESS_CONTROL / BRANCH_MODEL
    -> MULTIPLAYER
    -> LIVE_SCENE
    -> player/session/live schemas
    -> PERSISTENCE
    -> CHRONOLOGY
    -> Step-5 frontier/recovery/publication/live design
```

## 8.5 LLM information/Story architecture

```text
Step-4 canonical spec
    -> Step-5.10 / 5.11 / 5.12 canonical specs
    -> AI_REASONING / INFORMATION / LORE / NARRATIVE / PREP / GM_CRAFT
    -> current entity schemas where legacy knowledge fields still exist
    -> deferred Step-6 physical role/context realization
```

---

# 9. Research/discovery rule for this map

For substantive repository work:

1. inspect the current branch/ref and current repository tree;
2. read this map to identify likely owners and neighboring dependency surfaces;
3. for cross-stage architecture questions, use `CANONICAL_ARCHITECTURE_INDEX.md` to locate the owning accepted specifications;
4. read the actual referenced owners/contracts/schemas/tests;
5. search the repository for concrete symbols/paths to find consumers and stale references;
6. treat a zero-result keyword search as **non-evidence of absence** until the relevant directory/tree and local indexes have also been checked;
7. update this map when a structural/responsibility change would make future discovery materially misleading.

A file move/addition/deletion does not automatically require a prose entry when
it belongs to an already covered homogeneous family. Update the map when the
responsibility map, primary entry point, source-of-truth status, or dependency
route changes.

Do not place a rule only in this map. If a statement affects runtime or
architecture correctness, it belongs in the owning contract/spec/schema and may
only be linked/summarized here.