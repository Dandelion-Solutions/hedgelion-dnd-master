# R2.7 WP-18 — Story / Continuity / Dramaturg Planning — Source Manifest

Status: **STEP-1 OPEN-WORLD SOURCE MANIFEST — COMPLETE FOR SENIOR REVIEW / REMAINS EXPANDABLE**

Date: 2026-09-04

Pinned starting public state: `0b6cde38eb188713ac50ab7690f73eeab524e693`

This Source Manifest supports only WP-18 Step 1. It is an open-world routing/evidence artifact, not a claim that the repository contains no other relevant source. Step 2 must expand it when evidence exposes another material owner, consumer, exception or contradiction.

Classification vocabulary:

- `CONTROL` — current process/status/scope authority;
- `DIRECT` — directly owns Story/continuity/planning semantics in WP-18;
- `BOUNDARY` — neighboring owner that constrains eligibility/currentness/publication/recovery/cleanup;
- `MACHINE` — current executable/catalog/schema/runtime consumer or inventory surface;
- `NEGATIVE` — verified absence/stale-surface evidence;
- `DOWNSTREAM` — later work that WP-18 must not activate.

---

## 1. Process, status and scope authorities

| ID | Classification | Path | Why it is in the manifest |
|---|---|---|---|
| P01 | CONTROL | `AGENTS.md` | Repository-wide authority, transport and workflow constraints. |
| P02 | CONTROL | `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | ChatGPT/GitHub Connector transport and multi-file publication discipline. |
| P03 | CONTROL | `DEV/DESIGN_PROCESS.md` | Current 8-step design loop, Source Manifest and mandatory Senior gates. |
| P04 | CONTROL | `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | Architecture evidence/decision/reopen discipline. |
| P05 | CONTROL | `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` | Implementation/TDD boundary after architecture; not activated here. |
| P06 | CONTROL | `DEV/PROJECT_MAP.md` | Current navigation map; also contains a stale Story route that must be treated as routing debt, not ownership. |
| P07 | CONTROL | `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | Current R2.7 sequence/one-active-stage rule. |
| P08 | CONTROL | `DEV/CURRENT_PROGRESS.md` | Global current cursor: WP-18 Step 1. |
| P09 | CONTROL | `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md` | Task-local R2.7 cursor. |
| P10 | CONTROL | `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md` | Exact WP-18 five-question scope. |
| P11 | CONTROL | `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-execution-protocol.md` | Per-WP machine/architecture/reverse-audit/checkpoint protocol. |

---

## 2. Primary Story / continuity / planning owners

| ID | Classification | Path | WP-18 relevance |
|---|---|---|---|
| A01 | DIRECT | `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md` | Story noncanonical layer model, retired chapter architecture, Dramaturg/Chronicler roles, preparation non-entitlement. |
| A02 | DIRECT | `DEV/docs/superpowers/specs/2026-08-21-step-5-10-story-projection-durability-canonical-spec.md` | Story source contracts, coverage, projection state, IDs, queue-free catch-up, publication/currentness. |
| A03 | DIRECT | `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md` | Message/history exactness, compaction, semantic sufficiency and optional Story transcript archive. |
| A04 | DIRECT | `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md` | Typed continuity/history, Story orientation and proper-source escalation. |
| A05 | DIRECT | `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md` | Bounded Story/history discovery, currentness/eligibility, no generic memory authority. |
| A06 | DIRECT | `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md` | Dramaturg/Chronicler activation, `PreparationDraft`, Story service opportunity and no same-envelope feedback. |
| A07 | DIRECT | `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md` | Proven player-local/shared Dramaturg horizons, generation/CAS/rebase/lifecycle, privacy and canon-invalidates-prep laws. |
| A08 | BOUNDARY | `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` | Recipient-scoped disclosure, Story/Transcript handoff, private draft versus emitted evidence. |
| A09 | BOUNDARY | `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md` | Owner-gated retirement, Story/retention blockers and physical-residue versus semantic-liveness separation. |

---

## 3. R2.7 implementation-facing/currentness owners

| ID | Classification | Path | WP-18 relevance |
|---|---|---|---|
| R01 | DIRECT | `DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-08-llm-role-context-instruction-realization-canonical-spec.md` | Exact instruction/role-context realization; Story source escalation; Chronicler/Narrator containment. |
| R02 | DIRECT | `DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-09-context-loading-resource-bounds-realization-canonical-spec.md` | Runtime-local bounded context loading; Story/Dramaturg consumer lifecycle explicitly routed to WP-18. |
| R03 | DIRECT | `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-10-durable-campaign-record-family-completeness-canonical-spec.md` | Story admitted as noncanonical projection; single-player planning dormant; multiplayer planning conditional. |
| R04 | DIRECT | `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md` | Accepted Story root/sharding/projection-state route; multiplayer Dramaturg deferred to WP-18. |
| R05 | BOUNDARY | `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md` | HOT/SQLite physical realization cannot create owner/currentness; transient control remains ephemeral. |
| R06 | BOUNDARY | `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md` | Current durability/publication composition that Story/planning realization must not override. |
| R07 | BOUNDARY | `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md` | Current-authority-first recovery and checkpoint/session non-authority. |
| R08 | BOUNDARY | `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md` | Fictional chronology/temporal ownership; Story/planning technical order cannot become fictional order. |
| R09 | BOUNDARY | `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md` | Stable principal/PLAYER/control authorization, campaign/LIVE/HOT currentness and exact-source CAS. |
| R10 | BOUNDARY | `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-canonical-spec.md` | Recipient-safe projections and no planning/session/cache/index authority across asynchronous participants. |

The exact current WP-13/WP-14/WP-15 owner paths are pinned here. Step 2 must extract the applicable clauses; it must not substitute roadmaps or summaries for those owners.

---

## 4. Catalog / schema / executable machine evidence

| ID | Classification | Path/surface | WP-18 relevance |
|---|---|---|---|
| M01 | MACHINE | `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md` | Contract boundary: Story/Dramaturg projections remain outside canonical/current world/runtime authority unless explicitly admitted later. |
| M02 | MACHINE | `DEV/ARCHITECTURE/CATALOG_INVENTORY.md` | Current registry inventory and conditional realization evidence. |
| M03 | MACHINE | `DEV/CATALOG/core-catalog.json` | Current roles, typed drafts/service decisions, Story layers/candidate states and planning-entry vocabulary. |
| M04 | MACHINE | `DEV/CATALOG/catalog-admission-ledger.json` | Shows embedded protocol values are non-owner vocabulary; catalog presence is not durable-owner admission. |
| M05 | MACHINE | `GAME/SCHEMA/campaign_manifest.schema.yaml` | Current storage-root schema; lacks the future Story root selector. |
| M06 | MACHINE | `DEV/TESTS/test_step4_story_retirement_contract.py` | Executable regression against canonical chapter resurrection. |
| M07 | MACHINE | current `GAME/SCHEMA/` directory inventory at pinned ref | Negative/positive schema inventory; no dedicated Story/planning schema currently present. |

Catalog entries requiring explicit Step-2 classification include at least:

```text
role.dramaturg
role.chronicler
role.commentator

value.preparation_draft
value.story_projection_draft
value.story_service_decision

story_service.no_backlog
story_service.service
story_service.defer

planning.source_anchored_constraint
planning.provisional_dramaturgic_direction

story.transcript
story.events
story.mechanics
story.narrative

story.must_materialize
story.may_omit
```

Presence of these values is vocabulary/evidence only. It does not prove an independently durable record owner.

---

## 5. Current CORE/runtime consumer surfaces

These are not substitutes for canonical specs. They are current implementation-facing consumers whose behavior/routing must be reverse-audited in Step 2.

| ID | Classification | Path | Consumer question |
|---|---|---|---|
| C01 | MACHINE | `GAME/CORE/PREP.md` | Does current prep doctrine enforce situations-not-plots, provisional scenes and discardable prep? |
| C02 | MACHINE | `GAME/CORE/SESSION.md` | Does session/recovery behavior avoid old-chat/Story/planning authority and retain only useful next-horizon prep? |
| C03 | MACHINE | `GAME/CORE/AI_REASONING.md` | Does role eligibility/source escalation prevent Story/planning contamination? |
| C04 | MACHINE | `GAME/CORE/RUNTIME.md` | Where are Dramaturg/Chronicler phases/service opportunities invoked? |
| C05 | MACHINE | `GAME/CORE/PLAY_POLICY.md` | Does immutable CORE activation remain distinct from campaign/Story/planning data? |
| C06 | MACHINE | `GAME/CORE/PERSISTENCE.md` | Does persistence path preserve native authority and Story/planning soft/noncanonical behavior? |
| C07 | MACHINE | `GAME/CORE/STORAGE.md` | What current physical roots/routing expectations exist? |
| C08 | MACHINE | `GAME/CORE/CAMPAIGN_OPERATIONS.md` | Session/campaign organization consumer of prep/continuity. |
| C09 | MACHINE | `GAME/CORE/GM_CRAFT.md` | High-level Dramaturg/preparation doctrine and anti-railroad consumer. |
| C10 | MACHINE | `GAME/CORE/LIVE_SCENE.md` | Multiplayer/current-source neighbor where planning must not become LIVE authority. |

Step 2 must verify each path still exists and read the relevant current clauses before relying on it.

---

## 6. Verified negative / stale-surface evidence

Negative evidence constrains implementation assumptions; it never proves semantic absence.

| ID | Classification | Verified current result | Meaning |
|---|---|---|---|
| N01 | NEGATIVE | `GAME/CORE/STORY.md` -> not found at pinned HEAD | `DEV/PROJECT_MAP.md` Story route is stale; do not recreate this file by memory. |
| N02 | NEGATIVE | `DEV/SPECS/story-architecture.md` -> not found at pinned HEAD | Optional legacy architecture route is absent; canonical Step-4/5.10 owners still control. |
| N03 | NEGATIVE | `GAME/SCHEMA/story.schema.yaml` -> not found at pinned HEAD | No legacy monolithic Story schema may be assumed. |
| N04 | NEGATIVE | current `GAME/SCHEMA/` inventory has no dedicated Story/planning schema | Current machine realization remains incomplete; exact representation must be derived from accepted owners. |
| N05 | NEGATIVE | current `campaign_manifest.schema.yaml` lacks `storage.story_root` | WP-11 route is not yet scaffolded into current manifest schema; root-selector work remains downstream. |
| N06 | NEGATIVE | catalog/test surfaces exclude retired `world.chapter` / `transition.chapter_append` architecture | WP-18 must preserve retirement rather than revive it under a new route. |
| N07 | NEGATIVE | no current catalog canonical world/runtime record family is established merely by `value.preparation_draft` or planning-entry vocabulary | Durable planning owner admission remains a WP-18 evidence/design question, not a catalog inference. |

---

## 7. Dependency / consumer subgraph

The current Step-1 dependency graph is:

```text
Step 4 Story + Dramaturg semantics
    |
    +-> Step 5.10 Story durability/currentness
    |      +-> Step 5.11 exact history / compaction
    |      +-> Step 5.12 disclosure / Transcript handoff
    |      +-> Step 5.13 cleanup / retention
    |
    +-> R2.1 continuity / proper-source escalation
    +-> R2.3 bounded retrieval / eligibility
    +-> R2.4 phases / typed drafts / Chronicler service
    +-> R2.5 multiplayer retained Dramaturg horizons
            |
            +-> WP-16 principal/control/LIVE currentness
            +-> WP-17 recipient-safe async boundary

R2.7 realization
    WP-08 instruction containment
    -> WP-09 context loading
    -> WP-10 durable-family admission
    -> WP-11 Story topology / conditional planning
    -> WP-12 HOT/SQLite boundary
    -> WP-13 publication
    -> WP-14 recovery
    -> WP-15 chronology
    -> WP-16/WP-17 multiplayer boundaries
    -> WP-18 current work

Machine consumers
    catalog contracts / catalog generation
    manifest schema / schema inventory
    CORE PREP/SESSION/AI_REASONING/RUNTIME/...
    executable Story retirement regression
```

The graph is deliberately not reduced to `Story -> files` or `Dramaturg -> planning files`, because currentness, recipient eligibility, exact history, cleanup and multiplayer coordination are separate consumers.

---

## 8. Open-world search obligations for Step 2

Step 2 must expand this manifest whenever:

- a cited owner references another material owner not already represented;
- a current CORE/schema/catalog/test consumer has a behavior assumption not explained by the current set;
- a durable/reference/cleanup dependency needs another owner;
- an executable regression reveals a hidden compatibility contract;
- a negative finding exposes a replacement owner;
- a material contradiction/reopen trigger appears.

Required search directions include:

1. Story/Chronicler references across current CORE, schemas, catalogs and tests;
2. Dramaturg/preparation/planning references across the same surfaces;
3. `story_root`, projection-state, coverage/source-basis and Story-layer routing references;
4. planning generation/currentness/CAS/rebase/invalidation references;
5. recipient/private/disclosure references involving Story or planning;
6. recovery/checkpoint/session references that could accidentally promote Story/planning;
7. cleanup/retention references that can preserve or retire Story/planning dependencies;
8. legacy `chapter` references that could reintroduce retired architecture.

Search snippets are discovery aids only. Material claims must be recovered from the owning current source.

---

## 9. Downstream boundaries

| ID | Classification | Work package | WP-18 boundary |
|---|---|---|---|
| D01 | DOWNSTREAM | WP-19 | Campaign template/scaffold/root-selector realization; not activated by Step 1. |
| D02 | DOWNSTREAM | WP-20 | Migration/backward-compatibility realization; not activated by Step 1. |
| D03 | DOWNSTREAM | WP-22 | Cross-system integrated regression realization; WP-18 may define obligations, not implement them here. |
| D04 | DOWNSTREAM | WP-24 | Performance/latency/context quantitative evaluation. |
| D05 | DOWNSTREAM | WP-25 | Broader failure/recovery taxonomy beyond WP-18 owner-specific design. |

---

## 10. Step-1 sufficiency statement

For the current obvious primary/neighbor set:

```text
OBVIOUS_PRIMARY_OWNER_PATHS_PINNED:      YES
CURRENT_R2_7_BOUNDARY_PATHS_PINNED:      YES
MACHINE_CATALOG_SCHEMA_TEST_SURFACES:    INCLUDED
CURRENT_CORE_CONSUMER_SET:               INCLUDED FOR STEP-2 VERIFICATION
NEGATIVE_LEGACY_SCHEMA_ROUTE_EVIDENCE:   INCLUDED
OPEN_WORLD_EXPANSION_REQUIRED_IN_STEP_2: YES
```

No source in this manifest authorizes Step 2 before mandatory Senior Step-1 review.

The manifest makes no claim that current Story/planning implementation is complete. It establishes the evidence graph from which Step 2 must prove what is already satisfied, conditional/dormant, safely deferred, missing or contradictory.
