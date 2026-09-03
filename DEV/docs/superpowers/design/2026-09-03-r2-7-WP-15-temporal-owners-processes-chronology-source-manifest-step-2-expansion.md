# R2.7 WP-15 — Source Manifest Step-2 Expansion

Status: **STEP-2 OPEN-WORLD EXPANSION COMPLETE — READY FOR SYNTHESIS**

Date: 2026-09-03

Base Step-1 manifest:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-source-manifest.md`

Step-2 evidence:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-step-2-evidence-extraction.md`

This file extends, and does not close, the Step-1 Source Manifest. The manifest remains open-world through Step 8.

---

## 1. Newly reached canonical/catalog owners

| Source | Classification | Why reached / disposition |
|---|---|---|
| `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md` | `CANONICAL DOMAIN / OWNING PROSE COMPANION WITH KNOWN STALE ROWS` | Required by Senior GO through WP-07/catalog traversal. Supplies concrete Effect/Resource/LifeState/rest owner semantics and demonstrates stale `world.knowledge` prose relative to exact JSON; does not override exact catalog shape. |
| `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md` | `CANONICAL / OWNING` | Class-admission/lifecycle rule, current-state-vs-evidence split, composite relation identity and machine/prose authority boundary. Controls whether the independently persistent process family qualifies as a world owner. |
| `DEV/ARCHITECTURE/CATALOG_INVENTORY.md` | `CANONICAL CLASSIFICATION / OWNING` | Current catalog-2.0 world/runtime owner set. Its omission of `world.thread` exposes coordinated machine-alignment debt against WP-11/current scaffold rather than defeating the already-proved independent process lifecycle. |
| `DEV/ARCHITECTURE/CATALOG_ADMISSION.md` | `CANONICAL ADMISSION / OWNING` | Registration != realization; no placeholder class; admission requires current owner/lifecycle evidence. Supports mechanical reconciliation without human product choice. |
| `DEV/CATALOG/entity-structures.json` | `IMPLEMENTATION / EXACT MACHINE CONTRACT` | Exact current field inventory; confirms `world.knowledge` fields and absence of `world.thread`; later coordinated WP-15 realization alignment required. |
| `DEV/CATALOG/identifier-policies.json` | `IMPLEMENTATION / EXACT MACHINE CONTRACT` | Confirms knowledge/disclosure composite identities and no current thread identity policy; ID ordering never chronology. |
| `DEV/TESTS/test_r2_7_wp03_catalog_conformance.py` | `IMPLEMENTATION / TEST CONTRACT` | Protects catalog generation and knowledge/disclosure relation identities; currently lacks `world.thread` coverage, creating later conformance obligation. |

---

## 2. Newly reached process-routing/scaffold surfaces

| Source | Classification | Step-2 treatment |
|---|---|---|
| `GAME/CAMPAIGN/INDEX/THREAD_INDEX.yaml` | `DERIVATIVE INDEX / IMPLEMENTATION` | Confirms shipped THREAD discovery family; never state/temporal/absence authority. |
| `GAME/CAMPAIGN/WORLD/THREADS/` | `IMPLEMENTATION SCAFFOLD` | Confirms dedicated durable process root in current scaffold. Empty scaffold does not by itself prove semantics; combined with PROCESSES/thread schema/WP-11 it supports independent family realization. |
| `GAME/CAMPAIGN/STATE/CURRENT.yaml` | `IMPLEMENTATION / ROUTING SUMMARY` | `active_threads` is bounded routing/current-summary evidence only; not temporal root registry or scheduler. `world_time.frontier` remains stale chronology debt. |
| `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md` | `R2.7 UPSTREAM / OWNING` | Explicitly establishes `world.thread` as native routed family at `WORLD/THREADS` with discovery-only `THREAD_INDEX`; paths/indexes never authority. This is decisive physical-family evidence for the process-owner reconciliation. |

---

## 3. Newly reached information consumers under SR15-03

| Source | Classification | Treatment |
|---|---|---|
| `GAME/SCHEMA/pc.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | Explicitly declares legacy PC knowledge arrays non-authoritative projection/input surfaces; supports retirement of writable thread knowledge projection. |
| `GAME/SCHEMA/event.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | `delta.knowledge_changes` and event visibility are historical semantic/communication evidence, not current `world.knowledge` or `runtime.disclosure`; also direct chronology-field consumer. |
| `GAME/SCHEMA/live_scene.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | epoch-local `known_by_pc_ids` / `perceived_by_pc_ids` are perception/knowledge evidence and normalization input only; live revision remains currentness. |
| `GAME/CORE/MULTIPLAYER.md` | `IMPLEMENTATION / MACHINE CONTRACT` | repository visibility != PC knowledge; Git winner != fictional winner; contains stale global-frontier prose requiring later consistency repair. |
| `GAME/CORE/LIVE_SCENE.md` | `IMPLEMENTATION / MACHINE CONTRACT` | owner-bound live knowledge normalization, currentness/CAS, fixed-RNG retry and no-fiction-on-rollover constraints. |

Closed WP-07 Step-3/5/6/7/8 and mini-report routes already in the Step-1 manifest remain controlling upstream audit evidence and are fully consumed; no WP-07 reopening occurs.

---

## 4. Newly reached technical-order / recovery / retention consumers

| Source | Classification | Treatment |
|---|---|---|
| `GAME/CORE/INTEGRITY.md` | `IMPLEMENTATION / MACHINE CONTRACT` | bounded suspect diagnosis; stale/incomplete evidence != corruption; no invented chronology/retcon. |
| `GAME/CORE/STORAGE.md` | `IMPLEMENTATION / MACHINE CONTRACT` | HEAD/tree/cache/durability metadata are currentness/technical state only; no chronology; checkpoint optional. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md` | `R2.7 UPSTREAM / OWNING` | SQL row/timestamp/order cannot create identity/chronology; HOT owner state remains typed/native; no generic pending owner. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md` | `R2.7 UPSTREAM / OWNING` | durability currentness/timers/operation order are not fictional chronology; retries do not replay accepted mechanics. |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md` | `R2.7 UPSTREAM / OWNING` | current-source recovery, armed-owner discovery, Agenda rebuild, no duplicate materialization/reroll, checkpoint/session/time non-authority. |
| `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | `DERIVATIVE LOCATOR / INDEX` | Search-confirmation locator only; explicitly points to Step-5.9 retirement of global/singleton chronology frontiers. Not used as primary proof. |

---

## 5. Newly completed machine-schema traversal

The following Step-1 listed schemas were consumed directly during Step 2 and now have explicit dispositions:

| Source | Result |
|---|---|
| `DEV/SCHEMAS/temporal-binding.schema.json` | useful typed binding shape; provider/current-position semantics still governed by Step-5.9 |
| `DEV/SCHEMAS/duration-spec.schema.json` | reusable duration value only; not a timer/current clock |
| `DEV/SCHEMAS/boundary-occurrence.schema.json` | transient occurrence value with stable occurrence key/causal position; no lifecycle owner |
| `DEV/SCHEMAS/signal.schema.json` | explicit nonowner/transient negative evidence |
| `DEV/SCHEMAS/trigger-binding.schema.json` | embedded event/signal trigger; `schedule` spelling cannot create scheduler authority |
| `DEV/SCHEMAS/rest-policy-definition-data.schema.json` | policy duration/completion semantics, not active rest-progress owner |
| `DEV/SCHEMAS/world-effect-state.schema.json` | current owner-local temporal binding/scheduled-trigger realization conforms materially |
| `DEV/SCHEMAS/runtime-procedure-state.schema.json` | under-realizes already-owned Procedure timing/order state; later machine realization debt |
| `DEV/SCHEMAS/runtime-continuation-state.schema.json` | fixed RNG/dependency/segment continuity useful; generic required `future_rng_frontier` is stale debt; `unconsumed_advancement` must remain exact typed execution remainder only |

The remainder of Step-1 DEV schema set remains part of the active subgraph by reference; no new contradiction requiring synthesis delay was discovered.

---

## 6. Chronology/test search expansion

Direct search/reference traversal confirmed current uses of:

- `chronology_frontier_event_id` in CORE/schema and historical/candidate/canonical chronology material;
- the Step-5.9 canonical source explicitly supersedes the singleton semantic assumption;
- `DEV/TESTS/CHRONOLOGY_CASES.md` C12/C13 retain stale singleton/global-frontier expectations, while C01-C11/C14-C15 remain useful with typed-owner interpretation.

No current primary owner was discovered that restores a campaign-global fictional clock/frontier or authorizes total ordering of independent scopes.

---

## 7. Open-world dependency result

The Step-2 traversal expands the active dependency subgraph to include:

```text
Step-3 / Step-5.1/5.2/5.3/5.8/5.9/5.12/5.13/5.14
+ temporal-agenda chronology amendment
+ forward-extensible time owner decision
+ HEALTH_EFFECTS_RECOVERY
+ WP-07 closed information chain
+ CATALOG_CONTRACTS / ENTITY_STRUCTURES / CATALOG_INVENTORY / CATALOG_ADMISSION
+ exact catalog field/identity contracts
+ WP-11..WP-14 machine-realization constraints
+ PROCESSES / ADVANCEMENT / EXPLORATION / COMBAT / ENCOUNTERS
+ CHRONOLOGY / RUNTIME / RANDOMNESS / MULTIPLAYER / LIVE_SCENE / INFORMATION / INTEGRITY / STORAGE
+ current CURRENT/event/scene/live/thread/PC schemas and scaffold/index roots
+ temporal/execution DEV schemas
+ chronology/catalog regression evidence
```

This remains an open-world set. Step 6 must refresh `DEV/PROJECT_MAP.md`, current branch and actual references/searches and add any newly material owner/consumer before adversarial closure.

---

## 8. Step-2 manifest gate

```text
SOURCE_MANIFEST_OPEN_WORLD:        YES
STEP1_MANIFEST_SUPERSEDED:         NO — EXTENDED
ENTITY_STRUCTURES_ADDED:           YES
CATALOG_CONTRACTS_ADDED:           YES
FURTHER_CATALOG_OWNERS_ADDED:      YES
THREAD_ROUTE_SCAFFOLD_ADDED:       YES
INFORMATION_CONSUMERS_ADDED:       YES
RECOVERY_DURABILITY_CONSUMERS:     COMPLETE
SR15_01_03_FULLY_CONSUMED:         YES
NEW_HUMAN_DECISION:                NO
UPSTREAM_REOPEN_REQUIRED:          NO
BLOCKING_EVIDENCE_GAP:             NO
READY_FOR_STEP_3:                  YES
```
