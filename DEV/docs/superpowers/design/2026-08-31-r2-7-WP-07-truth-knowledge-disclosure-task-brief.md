# R2.7 WP-07 — Truth, Knowledge, Disclosure and Communication Evidence — Task Brief

Status: **STEP-1 TASK BRIEF / WHOLE-PROJECT CRITIC COMPLETE — STEP-2 EVIDENCE EXTRACTION IN PROGRESS**

## 1. Mandate

WP-07 audits whether HDM's distinct information responsibilities remain semantically
and mechanically separable in the current repository:

```text
objective truth
!= fictional knowledge
!= human disclosure
!= accepted communication evidence
!= Story / Transcript projection
```

The domain must answer the four questions registered by the R2.7 scope discovery:

1. Are those responsibilities mechanically distinct?
2. Does every required durable or operational owner have a representation, or an
   explicit `NO DURABLE RECORD` result?
3. Are lawful transfer/update semantics representable without copying knowledge
   into Actor, live or session records?
4. Are exact-history/Transcript semantics and compaction limits preserved?

This is an architecture-to-machine and machine-to-architecture conformance audit.
It does not authorize a replacement information subsystem merely because a
surface is incomplete or stale.

## 2. Current authority and process route

- Global current work/gate: `DEV/CURRENT_PROGRESS.md`.
- R2.7 task-local cursor: `2026-08-24-r2-7-audit-status.md`.
- Domain method and mini-report contract:
  `2026-08-24-r2-7-audit-execution-protocol.md`.
- R2.7 scope/question owner:
  `2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md`.
- Whole-project evidence requirements:
  `2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`.
- General and HDM architecture process:
  `DEV/DESIGN_PROCESS.md` and `DEV/ARCHITECTURE/DESIGN_PROCESS.md`.

Step 1 ends only after the Source Manifest, this Task Brief and the mandatory
whole-project critic are complete. Step 2 requires Senior GO.

## 3. Source Manifest

### 3.1 Canonical semantic owners

| Source | Role in WP-07 |
|---|---|
| `2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md` | primary owner of `world.lore_fact`, `world.knowledge`, `runtime.disclosure`, role eligibility, Story and Transcript boundary |
| `2026-08-23-step-4-single-context-role-containment-canonical-amendment.md` | later Step-4 amendment; logical eligibility and physical shared-context constraints |
| `2026-08-21-step-5-10-story-projection-durability-canonical-spec.md` | Story authority, typed source coverage, availability and Transcript admission boundary |
| `2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md` | `runtime.message`, exactness, retention and compaction |
| `2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` | emission/disclosure closure, recipient scope and delivery limitations |
| `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md` | message-envelope retirement, survivor obligations and safe compaction |
| `2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md` | integrated currentness, disclosure merge and physical-feasibility constraints |
| `2026-08-24-r2-1-continuity-history-canonical-spec.md` | continuity/history/Story non-authority and exact-evidence boundary |
| `2026-08-24-r2-2-actor-continuity-canonical-spec.md` | Actor cognition boundary; Actor state must not duplicate `world.knowledge` |
| `2026-08-24-r2-3-context-runtime-canonical-spec.md` | bounded discovery, routed currentness and role-context loading |
| `2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md` | typed role gateways, deterministic acceptance and visible-output fencing |
| `2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md` | recipient catch-up and collaboration non-authority |
| `2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md` | supported host information-boundary and recipient/audience constraints |

### 3.2 Current machine contracts and representations

| Surface | Why it is in scope |
|---|---|
| `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`, `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md` | accepted catalog and entity-shape route |
| `DEV/CATALOG/core-catalog.json`, `entity-structures.json`, `identifier-policies.json`, `catalog-admission-ledger.json` | admitted owner kinds, fields, identifiers and realization claims |
| `DEV/SCHEMAS/` relevant catalog and identifier schemas | machine validation for the catalog contracts |
| `GAME/SCHEMA/README.md`, `lore.schema.yaml`, `pc.schema.yaml`, `player.schema.yaml`, `session.schema.yaml`, `live_scene.schema.yaml`, `event.schema.yaml`, manifest/index/storage schemas | installed campaign representation, recipient binding and declared semantic boundaries |
| `GAME/CAMPAIGN/` template roots and indexes | actual template topology / whether a claimed owner has a durable location |
| `GAME/CORE/STORAGE.md`, `PERSISTENCE.md`, `RUNTIME.md`, `DIALOGUE.md`, `CHRONOLOGY.md`, `LIVE_SCENE.md`, `MULTIPLAYER.md`, `SAVE_CONTRACT.md`, `DURABILITY_GUARD.md` | runtime write, communication, live, recovery and retention consumers |
| `DEV/SCHEMAS/runtime-interaction-state.schema.json` and related runtime interaction/continuation/trace schemas | accepted message identity, authenticated player binding and persistence handoffs |
| `GAME/CORE/AI_REASONING.md`, `INFORMATION.md`, `LORE.md`, `NARRATIVE.md`, `NPC.md`, `PREP.md`, `GM_CRAFT.md` | shipped instruction-layer consumers and leak/authority boundaries |
| `DEV/TESTS/test_step4_story_retirement_contract.py`, `REGRESSION_CASES.md`, relevant runtime/durability cases and maintenance audit | existing mechanical/regression evidence and missing-test discovery |

### 3.3 Derivative and historical routing evidence

`DEV/PROJECT_MAP.md`, `CANONICAL_ARCHITECTURE_INDEX.md`, the Step-4/5
design decisions and prior R2.7 closed-domain reports are routing/provenance
inputs only. They do not override the canonical sources above.

## 4. Initial evidence and audit hypotheses

The following are evidence-backed candidates to test, not accepted WP-07
findings yet:

1. `GAME/SCHEMA/lore.schema.yaml` uses a legacy `status` field that includes
   `disputed_in_world`, while the canonical Step-4 and current catalog contract
   distinguish objective `truth_status` from lifecycle/record status and place
   in-world disagreement under subject knowledge.
2. `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md` appears to describe
   `world.knowledge` with older `status`/`learned_from_id` wording, whereas
   `DEV/CATALOG/entity-structures.json` requires `stance` and names bounded
   supporting-source/current-change fields.
3. The DEV catalog declares `world.lore_fact`, `world.knowledge`,
   `runtime.message` and `runtime.disclosure` admitted, with identity
   policies; the audit must distinguish a deliberate implementation obligation
   from a missing required current machine representation.
4. PC and live-scene surfaces may carry bounded input/projection or
   epoch-local information. The audit must prove that none is a parallel writable
   global authority after its owning handoff/compaction boundary.

## 5. Required proof

For every material owner or machine surface in scope, record:

```text
source/item
actual claim
authority classification
qualifiers and failure limits
current physical representation or explicit NO DURABLE RECORD result
architecture -> machine disposition
machine -> architecture disposition
conflict / stale / debt / no-delta rationale
```

The audit must test at least:

- objective truth status versus in-world disagreement;
- knowledge relation identity, PC agency and Actor/NPC cognition;
- human-recipient disclosure versus fictional knowledge;
- accepted message evidence versus proposition truth;
- pre-emission validation and post-emission limitation;
- Transcript exactness, Story non-authority and safe compaction;
- live/multiplayer recipient scope and compaction normalization;
- role-context eligibility and absence of raw/transitive information leakage.

## 6. Boundaries

WP-07 does not reopen accepted information semantics, add a universal information
graph, introduce a delivery outbox/read-receipt system, or make Story a current
authority. It may classify an actual inconsistency as stale documentation,
implementation obligation, verification obligation, debt or a genuine owner
decision only after the required proof.

The full Story/Dramaturg planning lifecycle remains primarily WP-18. This domain
checks only the truth/knowledge/disclosure/message/Transcript boundary that
those later consumers must respect.

## 7. Step-1 completion criteria

The whole-project critic must confirm that this manifest includes:

- all accepted semantic owners and later amendments that can alter WP-07;
- direct GAME/DEV representations and their runtime consumers;
- Actor, context, multiplayer and host-assurance dependencies;
- current tests/maintenance routes;
- no hidden duplicate-owner or migration surface missed by filename-only search.

No human decision is requested at this framing point.
