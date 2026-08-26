# HDM Repository Project Map

Status: **NON-NORMATIVE INTERNAL NAVIGATION INDEX**

Last structural inventory: 2026-08-25

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

### 1.1 Fresh-session research route

For a fresh HDM development/architecture chat, this map participates in the
bootstrap chain defined by `AGENTS.md` and the design-process files:

```text
current remote ref/state
-> AGENTS.md
-> DEV/DESIGN_PROCESS.md
-> DEV/ARCHITECTURE/DESIGN_PROCESS.md
-> DEV/PROJECT_MAP.md
-> DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md when architecture sequencing matters
-> concern route below
-> task-specific Source Manifest
-> actual owning artifacts
-> relevant schemas/tests/runtime consumers/research evidence
```

Do not preload the whole repository merely because it is large. Use this map to
identify the relevant dependency subgraph, then inspect that subgraph deeply
enough to support the claims being made.

Do not stop at this map, an executive summary, a roadmap heading or a derivative
index. These are routing/compression surfaces. Correctness-sensitive conclusions
must return to the actual owning artifacts and relevant evidence.

**HARD CRITIC ROUTE:** both the Step-1 Task-Brief critic and the Step-6
adversarial/candidate critic must start from this map, reconstruct the complete
task-specific direct-and-indirect dependency subgraph, and inspect the actual
owners, accepted/superseding decisions, schemas, tests and consumers that can
change the conclusion. A module-local critique is incomplete. A discovered
conflict must be resolved by conforming the current block to established
architecture or, when a real material trade-off exists, by presenting an
explicit superseding decision to the human architect.

### 1.2 Source-role legend

When building a task-specific Source Manifest, distinguish these roles:

- **CANONICAL / OWNING** — current source of semantic authority for the concern;
- **CANONICAL AMENDMENT / OWNER DECISION** — later accepted change or explicit
  decision that can supersede earlier wording;
- **DERIVATIVE LOCATOR / INDEX** — navigation/integration aid that points to
  owners but does not override them;
- **RESEARCH INPUT** — evidence/candidate material that requires analysis before
  it can influence architecture;
- **HISTORICAL / SUPERSEDED DERIVATION** — provenance/background only unless a
  current question specifically depends on it;
- **IMPLEMENTATION / MACHINE CONTRACT / TEST** — concrete realization or
  executable/scenario evidence that may constrain or verify architecture.

A fresh chat should identify source roles before combining documents. Similar
terminology does not imply equal authority.

## 2. Coverage convention

The map lists stable human-authored/runtime surfaces individually where their
responsibility matters. Large homogeneous families are grouped by path/pattern so
this index can scale without becoming a second manually maintained copy of the
repository:

- `DEV/SCHEMAS/*.schema.json` — development machine-contract schemas;
- `DEV/TESTS/test_*.py` — executable regression/contract tests;
- `DEV/TESTS/*_CASES.md` and related Markdown cases — scenario/acceptance case catalogs;
- `DEV/docs/superpowers/research/*.md` — non-normative research, reconnaissance, evidence and feasibility-study inputs;
- `DEV/docs/superpowers/specs/*.md` — dated architecture/design, review, decision and canonicalization-chain artifacts;
- `DEV/docs/superpowers/plans/*.md` — dated implementation plans created after approved designs.

When a task touches one of these families, inspect filenames/current references
rather than assuming this map enumerates every member.

For an enumerated research/review/requirement set, the absence of every item from
this map is intentional: the map routes to the owning source. If later work
claims coverage of that set, item-level accounting belongs in the research/design
process, not in this navigation index.

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
| Architecture process / current stage | `DEV/DESIGN_PROCESS.md`, `DEV/ARCHITECTURE/DESIGN_PROCESS.md`, `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | Round-1 closure/rebaseline owner decision, Step-4 single-context amendment, `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`, relevant owning canonical specs |
| Architecture research / Round-2 idea pool | `DEV/docs/superpowers/research/HDM_External_Architecture_Idea_Dossier_2026-08-21.md` | current Round-2 roadmap, current canonical architecture, relevant owner decisions/amendments, applicable runtime/schema/test owners when evaluating candidates |
| Host/platform feasibility / LLM orchestration | `DEV/docs/superpowers/research/2026-08-22-platform-feasibility-comparative-research.md` | Step-4 single-context amendment, Round-1 closure/rebaseline decision, role-context protocols, R2.4/R2.7 roadmap scope; former Step-6 feasibility notes are historical inputs only |
| Role-context validation evidence | `DEV/docs/superpowers/research/2026-08-23-role-context-validation-protocol-1-sequential-containment.md`, `2026-08-23-role-context-validation-protocol-2-collapsed-multi-role.md`, `2026-08-23-role-context-validation-protocol-3-reasoning-budget.md` | Step-4 canonical spec + single-context amendment, Round-2 roadmap, `GAME/CORE/AI_REASONING.md`, `NPC.md`, `NARRATIVE.md`, `PREP.md`; former Step-6 isolation notes are derivation/provenance only |
| Integrated canonical architecture lookup (Round 1) | `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | owning canonical specs/model contracts, Step-4 single-context amendment, Round-1 closure/rebaseline decision, current `NEAR_TERM_ROADMAP.md` |
| Catalog/class ownership | `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`, `CATALOG_INVENTORY.md`, `ENTITY_STRUCTURES.md`, `CATALOG_RESOLUTION.md`, `RULESET_PACKAGE_IDENTITY.md`, `DEV/CATALOG/` | `DEV/SCHEMAS/`, runtime/release package provenance, campaign ruleset adoption, Resolution/Continuation, Actor/Asset/Activity/Rule Element models, catalog tests |
| Deterministic mechanics/execution | `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`, `RULE_ELEMENT_MODEL.md`, accepted Step-2/Step-3 specs | `GAME/CORE/RUNTIME.md`, `MECHANICS_INTEGRITY.md`, `RANDOMNESS.md`, runtime/value schemas/tests |
| Campaign House Rules / rulings / policy adoption | `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`, `GAME/CAMPAIGN/RULES/HOUSE_RULES.md`, `GAME/CAMPAIGN/RULES/HOUSE_RULES.yaml` | `DEV/ARCHITECTURE/ACCESS_CONTROL.md`, `GAME/CORE/ADJUDICATION.md`, R2.3 Context Runtime, Step-5.6/5.7/5.8, `GAME/SCHEMA/house_rules_policy.schema.yaml`, `GAME/SCHEMA/player.schema.yaml`, adjudicated-input/player-policy tests |
| Persistence / durability / recovery | `GAME/CORE/STORAGE.md`, `PERSISTENCE.md`, `DURABILITY_GUARD.md`, `SAVE_CONTRACT.md`, `SESSION.md`, `INTEGRITY.md` | `RUNTIME.md`, `RANDOMNESS.md`, `LIVE_SCENE.md`, `MULTIPLAYER.md`, checkpoint/current/session schemas, Step-5 specs, `MAINTENANCE_COMMANDS.md` |
| Multiplayer / shared mutable state | `GAME/CORE/MULTIPLAYER.md`, `LIVE_SCENE.md` | `CHRONOLOGY.md`, `PERSISTENCE.md`, access control, live/session/player schemas, Step-5 specs, Round-2 R2.5 when collaboration/scene topology exceeds inherited Step-5 scope |
| Chronology / temporal continuity | `GAME/CORE/CHRONOLOGY.md`, accepted Step-2 temporal specs | `RUNTIME.md`, `RANDOMNESS.md`, `LIVE_SCENE.md`, `MULTIPLAYER.md`, Step-5.1+ specs, Round-2 continuity work where derived state/history alignment is involved |
| Campaign bootstrap / creation | `GAME/INSTALL/00_DND_BOOTSTRAP.md`, `GAME/CORE/BOOTSTRAP_RUNTIME.md`, `NEW_CAMPAIGN_FAST_PATH.md`, `CAMPAIGN_SETUP.md`, `GAME/TOOLS/init_campaign.py` | `GAME/CAMPAIGN/`, campaign schemas, `BRANCH_MODEL.md`, `ACCESS_CONTROL.md` |
| Runtime packaging / versioning / update | `DEV/TOOLS/release_builder.py`, `run_release_build.py`, `DEV/RELEASE/`, `.github/workflows/release-runtime.yml`, `GAME/ENGINE_VERSION.yaml`, `GAME/CORE/ENGINE_UPDATES.md` | `GAME/INSTALL/`, `GAME/MIGRATIONS/`, release tests |
| Rules/source routing | `GAME/RULES/`, `GAME/CORE/SOURCES.md`, `PLAY_POLICY.md` | domain CORE modules, character readiness, prep/worldgen, campaign House Rules owner when campaign-specific policy applies |
| LLM/runtime reasoning and presentation | `GAME/CORE/AI_REASONING.md`, `GM_CRAFT.md`, `PREP.md`, `NARRATIVE.md`, `INFORMATION.md`, `LORE.md` | Step-4 canonical spec + single-context amendment, role-context protocols, Round-2 R2.1/R2.2/R2.3/R2.4 as relevant |
| Support / diagnostics / maintenance | `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` | `GAME/CORE/SESSION.md`, `INTEGRITY.md`, `STORAGE.md`, `PERSISTENCE.md`, checkpoint/session schemas, Step-5 recovery design |
| Access / repository/campaign ownership | `DEV/ARCHITECTURE/ACCESS_CONTROL.md`, `BRANCH_MODEL.md` | `GAME/CORE/MULTIPLAYER.md`, bootstrap, persistence, player/session schemas, House-Rules policy-adoption authority |
| Consistency verification | `DEV/TOOLS/run_maintenance_audit`, `audit_engine.py`, `DEV/TESTS/`, `.github/workflows/validate.yml` | catalogs/schemas/contracts being changed |

This table is a discovery aid. A deep task must still inspect the current tree and
follow references from the owning artifacts.

---

# 5. Root and CI infrastructure

- `AGENTS.md` — repository ownership boundaries, fresh-session bootstrap,
  documentation-evidence discipline, authoritative development/release workflow
  and placement rules.
- `.github/workflows/validate.yml` — CI validation: maintenance audit plus DEV unit tests; currently triggers on `main`, `feature/**`, version branches `v*/*`, and pull requests.
- `.github/workflows/release-runtime.yml` — tagged/runtime release build and publication workflow.
- `.gitignore` — repository-local generated/cache exclusions.
- `README.md` — manually curated public repository overview; not an automatic development index.
- `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md` — root legal/attribution materials.
- `LICENSES/SRD-5.2.1-ATTRIBUTION.md` — SRD attribution source mirrored into runtime legal surface.

---

# 6. `DEV/` — development-only source

## 6.1 Process and version markers

- `DEV/DESIGN_PROCESS.md` — canonical generic architecture/deep-work procedure,
  including the AI-architect/human-architect operating contract and repository
  evidence/synthesis completeness gate.
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md` — HDM-specific adapter/additional
  constraints, including HDM Source Manifest and item-level evidence rules.
- `DEV/ENGINE_DEVELOPMENT.yaml` — development engine/revision metadata; richer than the shipped runtime marker.
- `DEV/PROJECT_MAP.md` — this non-normative repository navigation/dependency map.
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` — derivative Round-1 semantic locator/integration map; never overrides linked primary sources, later canonical amendments/owner decisions or current roadmap sequencing.

## 6.2 `DEV/ARCHITECTURE/`

Current durable architecture/navigation documents:

- `ACCESS_CONTROL.md` — engine repository authority, campaign creator/player authority, House-Rules policy-adoption grants and write-routing authorization boundaries.
- `ACTIVITY_MODEL.md` — executable declarative Activity definition and `runtime.resolution` invocation boundary.
- `ACTOR_MODEL.md` — progressive `world.actor` materialization, archetype/instance split and actor mechanical-state ownership.
- `ASSET_MODEL.md` — unified reusable/instance model for physical/conceptual assets and their placement/use/lifecycle boundary.
- `BRANCH_MODEL.md` — engine repository vs runtime package vs campaign-storage topology; campaign/live branch roles and package boundaries.
- `CAMPAIGN_HOUSE_RULES.md` — canonical campaign House Rules/Rulings semantic-policy boundary, adoption authority, structured sidecar, typed adjudication and realization/currentness contract.
- `CANONICAL_ARCHITECTURE_INDEX.md` — non-normative Round-1 cross-stage canonical locator/ownership/invariant map. Where its sequencing/status text is stale, current roadmap and later owner decisions/amendments win.
- `CATALOG_CONTRACTS.md` — universal definition/world/runtime class-admission and record-envelope contracts.
- `CATALOG_INVENTORY.md` — reviewed class inventory/classification; machine IDs live in `DEV/CATALOG/core-catalog.json`.
- `CATALOG_ADMISSION.md` — S6D-02 admission/realization laws, evidence hierarchy, package admission-plan boundary and downstream closure routing.
- `CATALOG_RESOLUTION.md` — deterministic `ResolvedCatalogContext`, definition-ID uniqueness and catalog evolution/resolution rules.
- `RULESET_PACKAGE_IDENTITY.md` — S6D-01 content-addressed ruleset package snapshots, exact resolved-set identity, campaign/execution projections and compatible reconstruction boundary.
- `CRITICAL_ARCHITECTURE_AUDIT.md` — completed Step-1 audit history/findings and dispositions.
- `ENTITY_STRUCTURES.md` — minimum/expected field structures and definition-binding inventory for catalog/world records.
- `MAINTENANCE_COMMANDS.md` — internal, intentionally player-undocumented operator/support command contract proposal (`HDM_EXPORT_CURRENT_LOG`, `HDM_EXPORT_CHECKPOINT_LOG`, `HDM_RESET_LAST_CHECKPOINT`).
- `NEAR_TERM_ROADMAP.md` — sequencing/status authority for the active Round-2 architecture program.
- `RULE_ELEMENT_MODEL.md` — pure embedded passive contribution model and bounded reactive binding boundary.
- `CALCULATION_SELECTOR_METADATA.md` — S6D-03 selector selectability, selector/operation compatibility, result/subject/binding metadata and deterministic active resolver policies.
- `MECHANICAL_CONTEXT.md` — S6D-04 exact accessor/fact/derived-node dispositions, missing/input authority, exact consumer permissions, bound-instance DAG and recovery/query boundaries.

Historical/derivation/status surfaces that must not override newer accepted contracts:

- `CATALOG_DESIGN_STATUS.md` — historical architecture/catalog status snapshot; current sequencing comes from `NEAR_TERM_ROADMAP.md`.
- `CATALOG_MODEL.md` — initial catalog taxonomy/derivation; points to newer normative inventory/contracts.
- `MECHANICAL_RUNTIME_PROPOSAL.md` — early physical hot-state/runtime proposal; useful for provenance, not authority where later canonical Steps 2–5 supersede it.

## 6.3 `DEV/CATALOG/`

Machine-readable current catalog surfaces; coordinated versions move together:

- `core-catalog.json` — closed class/capability/protocol vocabulary and IDs.
- `catalog-admission-ledger.json` — exact bidirectional admission/realization trace for every core-catalog family/ID pair; not runtime authority.
- `entity-structures.json` — machine field/definition-binding structure inventory.
- `identifier-policies.json` — stable identity/allocation policies including campaign allocator rules.
- `mechanical-surfaces.json` — registered deterministic mechanical selectors/operations/surfaces; selectable selector keys are governed by `CALCULATION_SELECTOR_METADATA.md`; its inherited `INVOCATION_ADJUDICATED` graph state is completed in S6D-04.

Read their schemas/tests before changing them. Human-readable architecture docs
explain semantics; these JSON files are machine contracts, not prose summaries.

## 6.4 `DEV/SCHEMAS/`

Development-only JSON Schemas for machine contracts. Major families include:

- catalog/envelope schemas (`catalog-definition`, `core-catalog`, `catalog-admission-ledger`, `entity-structures`, identifier policies, world-record);
- domain-definition/state schemas (Actor, Asset, Resource, Effect, Condition and related Step-2 structures);
- execution/runtime schemas (command, intent plan, resolution, procedure, continuation and related Step-3 records);
- embedded value/protocol schemas (duration, temporal binding, execution segment, pending child, invocation facts, receipts, boundary occurrences and similar values);
- House-Rules richer adjudicated Activity parameter binding support (`activity-parameter-binding.schema.json` and related ActionRequest/Resolution/Continuation/receipt schemas).

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
machine invariants. House-Rules-specific current tests include
`test_house_rules_adjudicated_input_contract.py` and
`test_house_rules_policy_authority_contract.py`.
Search this directory whenever a contract is changed; do not assume a prose spec
is the only consumer.

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

- `research/` — non-normative research, reconnaissance, evidence gathering and feasibility-study inputs. These artifacts inform later architecture work but do not become accepted architecture merely by being retained here.
- `research/HDM_External_Architecture_Idea_Dossier_2026-08-21.md` — non-normative architecture research dossier and Round-2 idea pool. Its classifications, applicability qualifiers and revisit triggers are part of the research evidence; candidates are not accepted architecture or mandatory roadmap work merely because they are DIAMOND/STRONG.
- `research/2026-08-22-platform-feasibility-comparative-research.md` — comparative host-platform feasibility study; interpret it under the current product/deployment baseline in the Round-2 roadmap and later accepted decisions rather than mechanically inheriting superseded Step-6 premises.
- `research/2026-08-23-role-context-validation-protocol-1-sequential-containment.md` — completed first-stage evidence that sequential logical roles can preserve behavioral containment inside one shared conversational history; pilot/instrument evidence, not physical-isolation proof.
- `research/2026-08-23-role-context-validation-protocol-2-collapsed-multi-role.md` — completed collapsed-generation evidence for Dramaturg/Actor/Narrator role rebinding, hidden-to-eligible transitions and same-generation logical separation.
- `research/2026-08-23-role-context-validation-protocol-3-reasoning-budget.md` — completed matched reasoning-budget validation across 150 turns, including long-history secrets, multi-NPC dialogue, player-facing quality observations, creativity authority levels and the accepted high-reasoning working baseline.
- `specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md` — current canonical amendment replacing mandatory physical-role-isolation assumptions with logical role containment in one physical chat context while preserving Step-4 authority/knowledge boundaries.
- `specs/2026-08-23-round-1-step-6-closure-round-2-rebaseline-owner-decision.md` — owner-approved transition decision: former Step 6 is closed as a separate stage and useful unresolved scope is reallocated into Round 2 without claiming old Step-6 exit criteria were completed.
- `specs/2026-08-25-campaign-house-rules-step-3-owner-decision.md` — explicit human owner decision closing House-Rules responsibility/adoption authority gate.
- `specs/2026-08-25-campaign-house-rules-step-8-canonicalization-v2.md` — repaired House-Rules eight-step closure record and stop-before-S6D handoff.
- `specs/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-canonicalization.md` — S6D-01 eight-step closure record and stop-before-S6D-02 handoff.
- `specs/2026-08-25-s6d-02-catalog-admission-gap-closure-task-brief.md` — S6D-02 Step-1 framing: two-axis admission/realization ledger, registry strata, evidence hierarchy and stop-before-Step-2 boundary.
- `specs/2026-08-25-s6d-02-catalog-admission-gap-closure-brief-critic.md` — mandatory whole-project Step-1 critique and repair record; zero unresolved blocking/significant findings.
- `specs/2026-08-25-s6d-03-complete-calculation-selector-metadata-task-brief.md` — S6D-03 Step-1 framing for item-level selector/operation evidence, metadata completeness and downstream boundaries.
- `specs/2026-08-25-s6d-03-complete-calculation-selector-metadata-brief-critic.md` — mandatory whole-project Step-1 critique; both significant framing findings repaired, final PASS.
- `research/2026-08-25-s6d-03-complete-calculation-selector-metadata-research-architecture-draft.md` and matching decision/collaborative/candidate/adversarial/resolution/canonicalization specs — S6D-03 Steps 2–8 evidence chain.
- `specs/2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-task-brief.md` — S6D-04 Step-1 framing for the exact accessor/fact/derived-node census, input authority, missing semantics, scoped dependency graph and query exclusion.
- `specs/2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-brief-critic.md` — mandatory whole-project Step-1 critique; both significant framing findings repaired, final PASS.
- `research/2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-research-architecture-draft.md` and matching decision/collaborative/candidate/adversarial/resolution/canonicalization specs — S6D-04 Steps 2–8 evidence chain.
- `specs/2026-08-25-s6d-05-activity-parameters-targeting-costs-portable-values-task-brief.md` — S6D-05 Step-1 framing for embedded Activity/protocol values, declaration-binding compatibility and execution/recovery equality.
- `specs/2026-08-25-s6d-05-activity-parameters-targeting-costs-portable-values-brief-critic.md` — mandatory whole-project Step-1 critique; exact high-risk Source Manifest routes repaired, final PASS.
- `DEV/ARCHITECTURE/PORTABLE_ACTIVITY_VALUES.md` — canonical S6D-05 owner for Activity declarations/bindings, targeting/area/cost/duration and embedded roll/offer/Signal/StateDelta authority and recovery equality.
- `research/2026-08-25-s6d-05-activity-parameters-targeting-costs-portable-values-research-architecture-draft.md` and matching decision/collaborative/candidate/adversarial/resolution/canonicalization specs — S6D-05 Steps 2–8 evidence chain; final whole-project critic PASS.
- `DEV/CATALOG/portable-value-routes.json` and `portable-value-contracts.json` — exact 19-value embedding/disposition routing and catalog-aware portable-value vocabularies.
- `DEV/TESTS/test_s6d_05_portable_value_contract.py` — transitive schema closure, binding compatibility, targeting/cost/duration, retry/currentness and no-lifecycle verification.
- `DEV/TESTS/test_s6d_03_selector_metadata_contract.py` — exact 34/26 accounting, active/dormant equality, metadata/policy/input/dependency verification.
- `research/2026-08-25-s6d-02-catalog-admission-gap-closure-research-architecture-draft.md` and the matching decision/collaborative/candidate/adversarial/resolution/canonicalization specs — S6D-02 Steps 2–8 evidence chain.
- `DEV/TESTS/test_s6d_02_catalog_admission_contract.py` — exact ledger/core equality, legal state and package-plan boundary checks.
- `specs/` — other dated architecture/design, review, decision and canonicalization-chain artifacts. Prefer current roadmap/owner decisions and the actual owning canonical sources over filename recency alone.
- `plans/` — implementation plans produced after approved designs. They are execution guidance, not architecture authority when a later canonical spec supersedes assumptions.

Round-1 accepted architecture is located through
`DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` and its owning primary
specifications. Current sequencing/status is owned by
`DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`. Where the derivative canonical index
still describes the former Step 6 as next, the current roadmap and Round-1
closure/rebaseline owner decision supersede that sequencing/status text. The
Step-4 single-context amendment is current canonical law for role containment.

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
- `CAMPAIGN_CARD.md` — compact campaign discovery/menu projection and refresh discipline.
- `CAMPAIGN_OPERATIONS.md` — campaign/session organization and maintenance operations.
- `SESSION.md` — session start/resume/end and coordination/maintenance-continuation state.

Gameplay/domain modules:

- `CHARACTER.md` — PC creation/player-character guidance.
- `ADJUDICATION.md` — uncertain actions, local rulings, frozen semantic inputs and the live-ruling versus durable House-Rules adoption boundary.
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
- `campaign_manifest.schema.yaml` — campaign branch identity/mode/engine/storage roots; creator remains deliberately absent as authority duplication.
- `campaign_config.schema.yaml` — premise/tone/boundaries/advancement/world mode.
- `campaign_card.schema.yaml` — compact campaign discovery/menu projection.
- `dnd_storage.schema.yaml` — campaign-storage repository marker/baseline format.
- `house_rules_policy.schema.yaml` — narrow House-Rules identity/currentness/adoption/routing/realization companion schema.
- `session.schema.yaml` — per-chat/session coordination data; no House-Rules notification cursor.
- `current_state.schema.yaml` — compact active-scene/global chronology routing state.
- `scene.schema.yaml` — one active scene/environment state.
- `player.schema.yaml`, `pc.schema.yaml`, `npc.schema.yaml` — player binding/House-Rules mechanical-override grant and character records.
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
- `RULES/HOUSE_RULES.md` — normative campaign-local House Rules/Rulings business-policy surface.
- `RULES/HOUSE_RULES.yaml` — empty narrow machine-readable identity/currentness/adoption/realization companion for those policies.

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

engine/ruleset update
    -> ENGINE_UPDATES
    -> RULESET_PACKAGE_IDENTITY / CATALOG_RESOLUTION
    -> ACCESS_CONTROL creator authority versus non-creator compatible use
    -> runtime package provenance + embedded resolved ruleset lock
    -> campaign MANIFEST engine.current + sibling ruleset.current
    -> DEV release/version policy
    -> GAME/MIGRATIONS if persistent format changes
```

## 8.4 Multiplayer

```text
Round-1 canonical ownership / Step-5 shared-state specs
    -> ACCESS_CONTROL / BRANCH_MODEL
    -> MULTIPLAYER
    -> LIVE_SCENE
    -> player/session/live schemas
    -> PERSISTENCE
    -> CHRONOLOGY
    -> R2.5 collaboration/currentness when applicable
```

## 8.5 LLM information / continuity / Story / role-context architecture

```text
Round-1 canonical locator
    -> Step-4 canonical role/truth/knowledge/context spec
    -> Step-4 single-context canonical amendment
    -> Step-5.10 / 5.11 / 5.12 canonical specs as relevant
    -> role-context validation protocols 1-3
    -> current Round-2 roadmap
    -> R2.1 continuity / R2.2 Actor continuity / R2.3 Context Runtime / R2.4 turn machinery as relevant
    -> AI_REASONING / INFORMATION / LORE / NPC / NARRATIVE / PREP / GM_CRAFT
    -> current entity schemas/tests where machine realization is implicated
```

Former Step-6 physical-role-isolation notes are historical/derivation inputs. Do
not route new work through them as an active stage; the Round-1 closure decision
and Step-4 single-context amendment supersede that premise.

## 8.6 Campaign House Rules / rulings

```text
CAMPAIGN_HOUSE_RULES canonical owner
    -> Step-3 explicit owner decision
    -> ACCESS_CONTROL creator/PLAYER policy adoption authority
    -> GAME/CAMPAIGN/RULES/HOUSE_RULES.md normative policy
    -> GAME/CAMPAIGN/RULES/HOUSE_RULES.yaml structured companion
    -> GAME/SCHEMA/house_rules_policy.schema.yaml + player.schema.yaml
    -> R2.3 Context Runtime eligibility/retrieval/currentness
    -> Step-5.6 publication / Step-5.7 recovery / Step-5.8 multiplayer currentness
    -> ADJUDICATION + Activity/Rule Element deterministic handoff
    -> DEV richer adjudicated-input schemas/tests
```

Do not route House-Rules work through MANIFEST creator fields, a generic policy
ACL/graph, a new global policy frontier or a universal rules DSL unless later
owning evidence explicitly supersedes the current architecture.

---

# 9. Research/discovery rule for this map

For substantive repository work:

1. inspect the current branch/ref and current repository tree;
2. read this map to identify likely owners and neighboring dependency surfaces;
3. read the current roadmap/status authority when sequencing or accepted stage
   state matters;
4. build the task-specific Source Manifest required by `DEV/DESIGN_PROCESS.md`;
5. for cross-stage architecture questions, use `CANONICAL_ARCHITECTURE_INDEX.md`
   only to locate owning accepted specifications and then follow later
   amendments/owner decisions;
6. read the actual referenced owners/contracts/schemas/tests/research sources to
   the depth required by the claim;
7. search the repository for concrete symbols/paths to find consumers and stale
   references;
8. treat a zero-result keyword search as **non-evidence of absence** until the
   relevant directory/tree and local indexes have also been checked;
9. before a roadmap/specification/coverage claim, run the repository-evidence and
   synthesis completeness gate in the design process;
10. for either architecture critic, record the direct and indirect owners/routes
    checked and reject module-local review as incomplete;
11. update this map when a structural/responsibility change would make future
    discovery materially misleading.

A file move/addition/deletion does not automatically require a prose entry when
it belongs to an already covered homogeneous family. Update the map when the
responsibility map, primary entry point, source-of-truth status, dependency route
or bootstrap guidance changes.

Do not place a rule only in this map. If a statement affects runtime or
architecture correctness, it belongs in the owning contract/spec/schema and may
only be linked/summarized here.

Do not treat this map's coverage as semantic coverage of the repository. Its job
is to route the agent to the evidence needed to prove a task-specific conclusion.
