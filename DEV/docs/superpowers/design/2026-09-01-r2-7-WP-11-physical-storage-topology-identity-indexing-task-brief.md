# R2.7 WP-11 — Physical Storage Topology, Identity and Indexing — Architecture Task Brief

Status: **STEP-1 TASK BRIEF / WHOLE-PROJECT CRITIC REPAIRED — READY FOR MANDATORY SENIOR REVIEW**

## 1. Mandate

WP-11 is the R2.7 domain for the project-wide physical mapping of accepted
logical record families: flat versus deterministically sharded storage,
stable-ID-to-route rules, and bounded non-authoritative indexes.

The scope-discovery owner fixes these questions:

1. Which record families are flat versus deterministically sharded across the
   entire project, rather than only for Round-2 additions?
2. What exact routing/shard arithmetic is required for every high-cardinality
   family?
3. Are stable IDs semantic identity while paths are routing only?
4. Does every lookup compose with monolithic `*_INDEX.yaml` without large
   directory enumeration?
5. Are indexes bounded, non-secret-bearing where required, rebuildable and
   non-authoritative?
6. Are GitHub directory/API constraints accounted for for every potentially
   large family?

WP-11 maps logical families to physical-topology and index contracts. It does
not change semantic ownership, create a record family, select HOT/SQLite
representation, change a schema/template/catalog/CORE file, implement route
math, add an index, migrate campaigns, alter bootstrap, or begin implementation
planning.

## 2. Current authorization and upstream boundaries

- Global authority: `DEV/CURRENT_PROGRESS.md`.
- R2.7 scope and execution: the whole-project Task Brief v2, execution
  protocol and scope-discovery owner in the Source Manifest below.
- Sequence authority: `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`.

WP-10 is a closed upstream input. Its Alternative-A logical allocation matrix
defines the record-family vocabulary and explicitly leaves physical placement,
paths, schemas, topology, migration, template/generator and bootstrap
unselected. WP-11 may assign topology only without merging any member's semantic
authority. WP-09 remains an upstream runtime-local no-record boundary; it is
not an index or campaign-storage family.

WP-12 owns HOT/SQLite hydration/dirty transaction realization; WP-13 owns
durability/publication; WP-14 recovery/checkpoints; WP-18 Story/Dramaturg
lifecycle; WP-19 bootstrap materialization; WP-20 migration; WP-21 cleanup;
WP-24 scale budgets. WP-11 may state a forward obligation but may not decide
any of those domains.

The historical task-local audit-status artifact is provenance only and must not
be rewritten to mirror global state.

## 3. Accepted constraints to preserve

- Stable IDs are semantic identity. A path, shard, index entry, Git ref,
  directory order or generated card is routing/projection evidence only.
- Physical normalization, sharding or co-location does not transfer semantic
  ownership. A native owner, event/history, disclosure, Story, cache, index,
  checkpoint and session remain distinct under their accepted contracts.
- Campaign branches have root-layout data selected by root MANIFEST; local
  GAME/CAMPAIGN is a generator template and storage-default metadata is a
  different lifecycle. WP-11 must preserve this separation.
- Indexes are bounded routing aids. They must be rebuildable from authoritative
  sources and cannot be writable current authority or closed-world negative
  proof unless a specific owner contract supplies that guarantee.
- Discovery metadata must obey eligibility and non-secret-bearing constraints;
  index availability never widens disclosure/role/subject eligibility.
- R2.2 Actor continuity and directed relationships remain source-Actor-owned;
  A-to-B does not imply B-to-A. A topology may normalize a high-cardinality
  relation only without changing that semantic boundary.
- Temporal Agenda, Story and Dramaturg projections, Context Runtime controls,
  caches and HOT copies retain their existing derived/no-record/conditional
  qualifications. No generic registry, global graph or scheduler follows from
  an index need.
- Git/repository order is not fictional chronology. A topology must not create
  a global chronology clock or make ref/path order fictional authority.
- Every normal lookup must remain bounded: no broad campaign directory scan,
  whole-tree load or large-directory enumeration merely to find a record.

## 4. Step-2 evidence plan and exit criteria

Step 2 will account for every WP-10 logical family and all current campaign
families that can be large or participate in lookup/routing. For each, record:

```text
semantic owner and primary source
stable identity namespace / admissible ID form
flat or sharded physical family, or explicit no-physical-family verdict
deterministic shard/routing rule and lookup inputs
monolithic index interaction and bounded lookup path
index payload, boundedness, secret/eligibility qualifier and rebuild source
campaign branch / template / storage-default / HOT distinction
actual GAME/DEV consumer and test/audit route
GitHub directory/API constraint and safe fallback
cross-domain forward obligation without implementation leakage
```

The evidence must distinguish native record route from derived index, cache,
card, Story, event/log, checkpoint and local working set. It must also account
for template/generator shape separately from authoritative topology law.

Step 2 is complete only when all potentially high-cardinality families and
lookup routes have an item-level topology/index disposition; all index contents
have authority/eligibility/rebuild qualifications; and no route relies on
directory enumeration or physical order as semantic identity.

## 5. Task-specific Source Manifest and discovery route

All exact paths are primary owners or current machine/consumer evidence. The
project map, roadmap and whole-project ledgers route discovery only; primary
owners win on conflict. Step 2 must add any owner or consumer exposed by these
sources before claiming coverage.

### 5.1 Governance, scope and routing

- `AGENTS.md`
- `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md`
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/PROJECT_MAP.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`
- `DEV/CURRENT_PROGRESS.md`
- `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-execution-protocol.md`
- `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`
- `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md`
- `DEV/docs/superpowers/design/2026-08-24-r2-7-global-semantic-owner-matrix.md`
- `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-source-manifest.md`

### 5.2 Canonical semantic and topology owners

- `DEV/ARCHITECTURE/BRANCH_MODEL.md`
- `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`
- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`
- `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md`
- `DEV/ARCHITECTURE/ACTOR_MODEL.md`
- `DEV/ARCHITECTURE/ASSET_MODEL.md`
- `DEV/ARCHITECTURE/ACCESS_CONTROL.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-09-context-loading-resource-bounds-realization-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-10-durable-campaign-record-family-completeness-canonical-spec.md`

### 5.3 Current runtime, campaign and schema consumers

- `GAME/CORE/STORAGE.md`
- `GAME/CORE/PERSISTENCE.md`
- `GAME/CORE/CAMPAIGN_IDENTITY.md`
- `GAME/CORE/INTEGRITY.md`
- `GAME/CORE/LIVE_SCENE.md`
- `GAME/CORE/CHRONOLOGY.md`
- `GAME/CORE/BOOTSTRAP_RUNTIME.md`
- `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md`
- `GAME/TOOLS/init_campaign.py`
- `GAME/SCHEMA/campaign_manifest.schema.yaml`
- `GAME/SCHEMA/dnd_storage.schema.yaml`
- `GAME/SCHEMA/index.schema.yaml`
- `GAME/SCHEMA/current_state.schema.yaml`
- `GAME/SCHEMA/event.schema.yaml`
- `GAME/SCHEMA/live_scene.schema.yaml`
- `GAME/SCHEMA/pc.schema.yaml`
- `GAME/SCHEMA/npc.schema.yaml`
- `GAME/SCHEMA/session.schema.yaml`
- `GAME/CAMPAIGN/MANIFEST.yaml`
- `GAME/CAMPAIGN/STATE/CURRENT.yaml`
- `GAME/CAMPAIGN/INDEX/EVENT_INDEX.yaml`
- `GAME/CAMPAIGN/INDEX/NPC_INDEX.yaml`
- `GAME/CAMPAIGN/INDEX/PC_INDEX.yaml`
- `GAME/CAMPAIGN/INDEX/SCENE_INDEX.yaml`

### 5.4 Development contracts and verification consumers

- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/entity-structures.json`
- `DEV/CATALOG/identifier-policies.json`
- `DEV/SCHEMAS/world-record.schema.json`
- `DEV/SCHEMAS/world-actor-state.schema.json`
- `DEV/SCHEMAS/world-asset-state.schema.json`
- `DEV/SCHEMAS/world-effect-state.schema.json`
- `DEV/SCHEMAS/runtime-command-state.schema.json`
- `DEV/SCHEMAS/runtime-continuation-state.schema.json`
- `DEV/SCHEMAS/temporal-binding.schema.json`
- `DEV/TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md`
- `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md`
- `DEV/TESTS/CHRONOLOGY_CASES.md`
- `DEV/TESTS/test_destination_template_boundary.py`
- `DEV/TOOLS/run_maintenance_audit.py`
- `.github/workflows/validate.yml`

## 6. Mandatory failure probes

At minimum, challenge whether:

- a path/shard/index or directory order becomes semantic identity;
- a monolithic index or directory listing becomes an unbounded lookup or
  authoritative absence proof;
- sharding transfers ownership or makes a relation symmetric;
- a non-secret index leaks protected Actor, knowledge, disclosure, Story or
  player-specific planning content;
- a topology conflates campaign branch, storage default, template, HOT cache,
  checkpoint or live state;
- a physical route becomes chronology, publication or recovery authority;
- an index for a no-record/derived concern creates a new durable subsystem;
- a route requires a generic graph, registry, scheduler or campaign-wide scan;
- a proposed topology silently chooses WP-12/13/14/18/19/20/24 realization;
- existing index/template names are credited without consumer and owner proof.

## 7. Step-1 decision and next gate

No human-owned product, semantic-owner, compatibility-policy, risk-acceptance or
scope decision is exposed by the framing sources. Existing owners determine the
constraints; Step 2 must expose any real topology trade-off as a decision-ready
package rather than choose it implicitly.

This completed Step-1 package requires mandatory Senior review. Do not begin
WP-11 Step 2, WP-12 or implementation planning without explicit Senior GO.
