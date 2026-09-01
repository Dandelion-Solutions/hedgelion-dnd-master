# R2.7 WP-10 — Durable Campaign Record-Family Completeness — Architecture Task Brief

Status: **STEP-1 TASK BRIEF / WHOLE-PROJECT CRITIC REPAIRED — READY FOR MANDATORY SENIOR REVIEW**

## 1. Mandate

WP-10 is the R2.7 audit domain for exact durable campaign record-family
completeness. It determines whether every accepted durable/current semantic owner
has one exact native record family/root/schema or an explicit no-native-durable-
record verdict; whether the generated campaign scaffold can materialize that
model; and whether manifest/config/current/session/checkpoint/event/world records
contain only their own responsibilities.

The scope-discovery owner fixes these mandatory questions:

1. Does every accepted durable/current semantic owner map to an exact native
   record family/root/schema, or explicitly to no native durable record?
2. Are current campaign template families sufficient for all Steps 1–5 and
   Round-2 requirements?
3. Which existing scaffold roots are historical/insufficient and require
   replacement/addition?
4. Do manifest/config/current/session/checkpoint/event/world records contain
   only responsibilities they actually own?

This is a complete architecture-to-machine and machine-to-architecture record
audit. It does not authorize implementation, schema/template/catalog/CORE edits,
data migration, physical sharding, HOT/SQLite design, bootstrap rewrite, WP-11,
or implementation planning.

## 2. Current authorization and closed/upstream input

- Global authority: `DEV/CURRENT_PROGRESS.md`.
- R2.7 scope/method: `2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`,
  `2026-08-24-r2-7-audit-execution-protocol.md` and
  `2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md`.
- Sequencing: `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`.
- This branch authorizes **WP-10 Step 1 only**. Step 2 requires mandatory Senior
  GO after this completed package.

WP-08 and WP-09 are closed upstream inputs. WP-08 keeps role-context control
runtime-local; WP-09 establishes that role-context bundle/profile/trace/source
basis and estimator control have **no durable WP-09 record**. That explicit
no-representation verdict is an input to the record-family matrix, not a reason
to recreate context control as a campaign record.

The historical task-local `audit-status.md` is provenance only. It must not be
rewritten to mirror WP-10 global state.

## 3. Accepted constraints WP-10 preserves

- Every mutable/current semantic concern has one native owner. Persistence,
  useful projections, caches, indexes, checkpoints, prepared objects, Story or
  execution evidence do not silently become a second current owner.
- `world.*` is a concrete campaign entity/fact with its own lifecycle; a
  `runtime.*` record is an independently addressable operational/evidence owner
  only where the accepted owner contract requires it. Definitions/catalogs do not
  own mutable campaign state.
- R2.2 Actor private continuity is source-Actor-owned; `world.knowledge`
  remains the distinct proposition-stance owner. R2.1 continuity/Story may
  orient, project or retain history but cannot replace current native authority.
- Step-3 execution owners, Step-4 truth/knowledge/disclosure/Story owners and
  Step-5 recovery/durability/currentness/chronology/live/publication owners keep
  their established lifecycles and no-representation verdicts.
- Campaign storage uses root `MANIFEST.yaml` as layout discriminator; selected
  manifest roots route campaign data. The local runtime `GAME/CAMPAIGN/` tree
  is a template source copied by `GAME/TOOLS/init_campaign.py`, not a
  `CAMPAIGN/` wrapper in a new campaign branch.
- CURRENT, cards, indexes, checkpoints, HOT/SQLite and derived runtime
  structures have only their accepted compact/projection/operational/evidence
  roles. In particular, checkpoint is not current-state/recovery authority and
  an index is not a duplicate entity database.
- Current pre-release clean-slate authorization permits an owner-conforming
  replacement only after actual owner, supersession and consumer inspection; it
  does not turn stale-looking scaffolds into automatically replaceable law.
- WP-09/F03 asks WP-10 to assess a durable root/template only if a concrete later
  realization exposes a need. It does not pre-authorize one.

## 4. Scope boundary

### 4.1 In scope

Step 2 shall build item-level two-way accounting for:

- every accepted `world.*`, `runtime.*`, campaign metadata, Story/projection,
  semantic-history, disclosure, temporal, live and session/current owner
  implicated by Steps 1–5 and R2.1–R2.6;
- explicit no-native-durable-record outcomes, including ephemeral role-context
  control and derived/cache/index/projection contracts;
- exact current GAME schema and generated-template path/family, its fields and
  invariants, native owner, currentness/durability route, consumers and tests;
- current `MANIFEST`, `CONFIG`, card, CURRENT, session, checkpoint, log,
  event, scene, player, PC/NPC, location, faction, item, lore, thread, House
  Rules and index family responsibilities;
- DEV catalog/record/runtime schema evidence and the distinction between
  development contract versus shipped campaign representation;
- existing root/scaffold insufficiency, duplicate-owner/stale field and missing
  family evidence, with a precise disposition.

### 4.2 Explicitly out of scope / routing

| Boundary | WP-10 disposition |
|---|---|
| Flat/sharded placement, path arithmetic, index partition and directory/API scale | Map logical family only; WP-11 owns physical topology. |
| HOT/SQLite hydration, dirty tracking, transaction realization | Preserve owner/no-authority constraint; WP-12 owns realization. |
| Durable recovery/currentness protocol, checkpoints, live-epoch mechanics | Inspect representation compatibility only; Steps 5.5–5.14 and WP-13/14/16 own policy/realization. |
| Schema/version migration and engine update | Identify a potential compatibility consequence only; WP-20 owns migration policy. |
| Bootstrap/generator ordering and first-play lifecycle | Inspect template completeness only; WP-19 owns bootstrap realization. |
| Story and Dramaturg representation/lifecycle | Map present owner/family only; WP-18 owns physical mapping/lifecycle. |
| Numeric scale and performance | Preserve bounded-read constraints; WP-24 owns targets. |
| Full error/cleanup taxonomy | Preserve owner/failure requirements; WP-21/WP-25 own realization. |
| Runtime/schema/catalog/CORE/test changes or implementation planning | Forbidden in WP-10. |

## 5. Task-specific Source Manifest and discovery route

All exact paths below were opened for readability on the verified Step-1 ref.
The manifest distinguishes semantic owners from derivative/machine evidence.
A later-discovered owner or consumer is added before a coverage claim.

### 5.1 Governance, process and current routing

| Exact source | Authority role | Step-2 use |
|---|---|---|
| `AGENTS.md`; `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md`; `DEV/DESIGN_PROCESS.md`; `DEV/ARCHITECTURE/DESIGN_PROCESS.md`; `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` | process/transport guardrails | evidence/critic/Senior gates, Connector publication and no-implementation boundary |
| `DEV/CURRENT_PROGRESS.md` | global current-progress | WP-10 authorization and exact gate |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`; `DEV/PROJECT_MAP.md`; `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | sequencing and derivative discovery | reconstruct direct/indirect owner and consumer graph; owners win |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`; `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-execution-protocol.md`; `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md` | active R2.7 owner/method | exact WP-10 questions, evidence/disposition/checkpoint method |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-global-semantic-owner-matrix.md`; `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-source-manifest.md` | derivative traceability evidence | complete concern inventory and prior coverage; no semantic supersession |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md` | historical task-local cursor | provenance only; never current authorization |

### 5.2 Direct semantic and durable-owner sources

| Exact source group | Authority role | Required inspection |
|---|---|---|
| `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`; `CATALOG_INVENTORY.md`; `CATALOG_RESOLUTION.md`; `ENTITY_STRUCTURES.md`; `ACTOR_MODEL.md`; `ASSET_MODEL.md`; `ACTIVITY_MODEL.md`; `RULE_ELEMENT_MODEL.md`; `ACCESS_CONTROL.md`; `BRANCH_MODEL.md`; `CAMPAIGN_HOUSE_RULES.md`; `HOUSE_RULES_MECHANICAL_BOUNDARY.md`; `RULESET_PACKAGE_IDENTITY.md` | direct architecture owners | natural `world.*`/definition/record classes, owner boundaries, package/manifest/Player/House-Rules constraints |
| `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md` | direct canonical owner | `runtime.command`, interaction, intent-plan, procedure, resolution, continuation, event/receipt/trace durable/evidence owners |
| `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`; `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md` | canonical owner/amendment | `world.lore_fact`, `world.knowledge`, disclosure, message/Story and role/proposal boundary |
| `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md`; `2026-08-24-r2-2-actor-continuity-canonical-spec.md`; `2026-08-24-r2-3-context-runtime-canonical-spec.md`; `2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md`; `2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md`; `2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md` | Round-2 canonical constraints | durable/ephemeral boundary, Actor cognition, context no-representation, collaboration/currentness and supported-host qualifiers |
| Step-5 canonical set: `2026-08-20-step-5-0-authority-contamination-final.md`; `2026-08-20-step-5-1-frontier-model-canonical-spec.md`; `2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`; `2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md`; `2026-08-21-step-5-3-5-9-temporal-agenda-chronology-integration-canonical-amendment.md`; `2026-08-20-step-5-4-host-lifecycle-session-handoff-canonical-spec.md`; `2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md`; `2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md`; `2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`; `2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md`; `2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md`; `2026-08-21-step-5-10-story-projection-durability-canonical-spec.md`; `2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md`; `2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md`; `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`; `2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md` (all under `DEV/docs/superpowers/specs/`) | direct canonical durable/currentness/recovery owners | exhaustively map record/no-record requirement, exact owner, currentness and recovery qualification; no Step-5 decision is reopened by overlap |
| `DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-08-llm-role-context-instruction-realization-canonical-spec.md`; `DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-09-context-loading-resource-bounds-realization-canonical-spec.md` | closed upstream realization input | protect runtime-local no-record context controls and route WP-09/F03 only when actual durable need appears |

### 5.3 Current GAME campaign schema and scaffold family

Exact schema contracts to inspect:

`GAME/SCHEMA/campaign_card.schema.yaml`; `campaign_config.schema.yaml`;
`campaign_manifest.schema.yaml`; `checkpoint.schema.yaml`;
`current_state.schema.yaml`; `dnd_storage.schema.yaml`; `event.schema.yaml`;
`faction.schema.yaml`; `house_rules_policy.schema.yaml`; `index.schema.yaml`;
`item.schema.yaml`; `live_scene.schema.yaml`; `location.schema.yaml`;
`lore.schema.yaml`; `npc.schema.yaml`; `pc.schema.yaml`;
`player.schema.yaml`; `scene.schema.yaml`; `session.schema.yaml`;
`thread.schema.yaml`; and `GAME/SCHEMA/README.md`.

Exact local campaign-template sources to inspect:

`GAME/CAMPAIGN/MANIFEST.yaml`; `CONFIG.yaml`; `CAMPAIGN_CARD.yaml`;
`README.md`; `STATE/CURRENT.yaml`; `CHECKPOINTS/_TEMPLATE.yaml`;
`LOG/_TEMPLATE.yaml`; `SESSIONS/_TEMPLATE.yaml`;
`RULES/HOUSE_RULES.md`; `RULES/HOUSE_RULES.yaml`;
`INDEX/EVENT_INDEX.yaml`; `FACTION_INDEX.yaml`; `ITEM_INDEX.yaml`;
`LOCATION_INDEX.yaml`; `LORE_INDEX.yaml`; `NPC_INDEX.yaml`;
`PC_INDEX.yaml`; `PLAYER_INDEX.yaml`; `SCENE_INDEX.yaml`;
`THREAD_INDEX.yaml`.

The critic must check the absence/presence of a template file separately from its
semantic adequacy. A directory with no seed record is not proof of
no-representation or a permission to invent a new owner.

### 5.4 Runtime, bootstrap and storage consumers

Inspect actual current consumer contracts:

`GAME/CORE/STORAGE.md`; `PERSISTENCE.md`; `DURABILITY_GUARD.md`;
`SAVE_CONTRACT.md`; `SESSION.md`; `INTEGRITY.md`; `MULTIPLAYER.md`;
`LIVE_SCENE.md`; `CHRONOLOGY.md`; `RUNTIME.md`;
`BOOTSTRAP_RUNTIME.md`; `NEW_CAMPAIGN_FAST_PATH.md`;
`CAMPAIGN_IDENTITY.md`; `CAMPAIGN_CARD.md`; `CAMPAIGN_SETUP.md`;
`CAMPAIGN_OPERATIONS.md`; `ENGINE_UPDATES.md`; and
`GAME/TOOLS/init_campaign.py`.

These files route the actual format/path consumers. They cannot make a
currently-present record authoritative contrary to the canonical owner.

### 5.5 DEV machine contracts and verification consumers

Inspect exact current development surfaces:

`DEV/CATALOG/core-catalog.json`; `entity-structures.json`;
`mechanical-surfaces.json`;
`DEV/SCHEMAS/world-record.schema.json`; `world-actor-state.schema.json`;
`world-asset-state.schema.json`; `world-effect-state.schema.json`;
`world-location-state.schema.json`; `runtime-command-state.schema.json`;
`runtime-continuation-state.schema.json`; `runtime-intent-plan-state.schema.json`;
`runtime-interaction-state.schema.json`; `runtime-procedure-state.schema.json`;
`runtime-resolution-state.schema.json`; `runtime-resolution-trace-state.schema.json`;
`temporal-binding.schema.json`.

Focused verification/consumer route:

`DEV/TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md`;
`PERSISTENCE_TRANSACTION_CASES.md`; `CHRONOLOGY_CASES.md`;
`LIVE_SCENE_CASES.md`; `CAMPAIGN_CARD_CASES.md`;
`CAMPAIGN_IDENTITY_CASES.md`; `test_destination_template_boundary.py`;
`test_maintenance_continuation_contract.py`;
`test_step2_resource_storage_contract.py`;
`test_step3_execution_value_schemas.py`;
`DEV/TOOLS/run_maintenance_audit.py`; and `.github/workflows/validate.yml`.

## 6. Required Step-2 proof and exit criteria

For every material concern/family, record:

```text
accepted semantic owner and source
current/durable/no-representation classification
exact native record family/root/schema or explicit no-record verdict
template/generator path and bootstrap/materialization route
currentness/durability/recovery/publication qualifier
allowed helper/projection/index/cache role and false-authority rejection
actual GAME/DEV consumer and test/audit route
architecture -> machine disposition
machine -> architecture classification
cross-domain forward obligation, safe-defer trigger or no-delta rationale
```

Step 2 is complete only when it can account for each accepted owner and every
current template/schema family without thematic sampling, and can distinguish:

- current native owner from event/history/checkpoint/Story/card/index/cache;
- campaign branch record from storage-default metadata and local runtime template;
- durable native state from HOT/SOFT operational state and ephemeral chat/control;
- a missing physical family from an explicit no-record verdict;
- a historical/stale scaffold field from an accepted current owner;
- an actual representation gap from a WP-11/12/18/19/20/21/24/25 concern.

Evidence belongs in `research/`. It must not create a canonical specification
merely by copying audit tables.

## 7. Mandatory failure probes

At minimum challenge:

- a semantic owner is silently placed in MANIFEST, CONFIG, CURRENT, SESSION,
  CHECKPOINT, event, card, index or log because that file is convenient;
- a derived/helper surface becomes a writable current owner;
- Actor private continuity is merged into `world.knowledge`, Story or role
  context; or disclosure/message is confused with truth/knowledge;
- current campaign branch, storage default, local template and runtime cache are
  conflated;
- a checkpoint/card/index/template omission is treated as proof that owner data
  does not exist;
- a current schema/template gets credit merely because its name resembles an
  owner; or a DEV schema is mistaken for shipped persistence format;
- record-family completeness secretly chooses sharding/HOT/migration/bootstrap
  implementation;
- WP-09 role-context control is made durable without a concrete, owner-conforming
  requirement;
- a stale pre-release scaffold is replaced without current owner/supersession/
  consumer evidence.

## 8. Decision gate and next step

No human-owned product, architecture, authority, compatibility, risk-acceptance
or scope choice is exposed by Step-1 sources. Existing owners determine the
baseline. If Step 2 reveals an actual unsatisfied durable-owner choice or
incompatible accepted owner contract, stop with a decision-ready brief.

Otherwise, this completed Step-1 package requires mandatory Senior review. Do
not begin Step 2, WP-11 or implementation planning without explicit Senior GO.
