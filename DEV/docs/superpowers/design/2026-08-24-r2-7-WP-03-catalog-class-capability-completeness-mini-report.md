# WP-03 — Catalog / class / capability completeness

Статус: **CLOSED — VERIFIED SUBJECT TO READ-BACK**

Date: 2026-08-24

## 1. Итог

WP-03 завершил whole-project audit закрытого machine vocabulary и class-admission boundary.

Главный результат:

```text
ACCEPTED ARCHITECTURE -> CLOSED MACHINE CLASS/VOCABULARY: MAPPED
STALE GENERIC OWNER CLASSES: RETIRED
KNOWN LATE-ROUND VOCABULARY GAPS: MATERIALIZED
NEW PRODUCT/ARCHITECTURE DECISION REQUIRED: 0
```

Каталог переведён на clean-slate unreleased generation `2.0.0`. Это намеренно несовместимая рабочая generation финальной R2.7 архитектуры; backward compatibility с прежним `1.6.0` не поддерживается, поскольку owner установил отсутствие реальных кампаний, зависящих от старого scaffold.

Параллельно owner поднял pre-release identity приложения до `v1.0-alpha` (`engine_version: 1.0-alpha`, `release_status: development`). Catalog generation и engine version являются разными version axes и не обязаны совпадать численно.

---

## 2. Source Manifest delta

Owning sources текущего WP:

- `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`;
- `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md`;
- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`;
- `DEV/ARCHITECTURE/CATALOG_DESIGN_STATUS.md`;
- Step-3 accepted execution vocabulary;
- Step-4 canonical truth/knowledge/disclosure/role contracts;
- Step-5.5 durability semantics;
- Step-5.6 repository outcome semantics;
- later Step-5 chronology/recovery/Story/message-retention owners;
- R2.2 Actor continuity/cognition/directed relationship owner;
- R2.3 Context Runtime owner;
- R2.4 TurnEnvelope/roles/Chronicler owner;
- R2.5 collaboration/planning owner;
- WP-02 global authority/duplicate-owner findings.

Machine surfaces audited/changed:

- `DEV/CATALOG/core-catalog.json`;
- `DEV/CATALOG/entity-structures.json`;
- `DEV/CATALOG/identifier-policies.json`;
- `DEV/CATALOG/mechanical-surfaces.json`;
- `DEV/SCHEMAS/core-catalog.schema.json`;
- `DEV/SCHEMAS/identifier-policies.schema.json`;
- catalog architecture prose/status;
- catalog regression tests.

---

## 3. Class-admission result

The canonical class-admission hierarchy remains:

```text
engine capability/protocol registry
  -> executable closed vocabulary

definition.*
  -> reusable validated content

world.*
  -> particular campaign thing/fact with independent identity/lifecycle

runtime.*
  -> independently addressable operational owner with proven lifecycle

value.* / enum
  -> embedded typed protocol/value without independent owner lifecycle
```

R2.7 does not promote every later architecture noun into a new record.

### Retired

- generic `world.relationship`;
- `transition.relationship_change`;
- `event.relationship.changed`;
- `truth.disputed` on objective truth axis;
- old `knowledge_modes` abstraction;
- old global `canonicality_classes`;
- intrinsic `durability.soft|hard` class vocabulary;
- generic publication lifecycle `local|queued|prepared|published|blocked` as a semantic owner model.

### Added independent record classes

- `runtime.disclosure` — accepted Step-4 durable human-player exposure owner;
- `runtime.collaboration_obligation` — narrow R2.5 recoverable contribution-collection/current-generation owner.

No additional Story/Dramaturg/Context records were created merely because their concepts exist.

### Added protocol/value families

Later typed handoffs are registered as `value.*`, including:

- `value.epistemic_delta`;
- `value.role_context_request`;
- `value.context_need_profile`;
- `value.role_context_bundle`;
- `value.context_trace`;
- `value.context_budget_envelope`;
- `value.turn_envelope`;
- `value.interpreter_result`;
- `value.preparation_draft`;
- `value.actor_proposal`;
- `value.story_projection_draft`;
- `value.narration_result`;
- `value.story_service_decision`.

Это не создаёт новую semantic authority.

---

## 4. Closed vocabulary additions

`core-catalog.json` теперь явно содержит:

- `truth_statuses` = `truth.undetermined | truth.established | truth.disproven`;
- independent lore lifecycle statuses;
- `epistemic.*` stances;
- disclosure aspects;
- Step-5 semantic-survival/current-durability/edge-obligation axes;
- repository ref outcomes `CONFIRMED_ACCEPTED | CONFIRMED_REJECTED | INDETERMINATE` в machine-ID spelling;
- R2.2 Actor continuity lifetimes, cognition purposes and directed relationship facets;
- six logical LLM roles;
- R2.3 discovery channels, representation classes and assembly outcomes;
- R2.4 Story-service outcomes;
- R2.5 coordination/input/collaboration/planning classifications;
- chronology relation vocabulary;
- recovery outcome vocabulary;
- Story-layer/candidate vocabulary;
- retained/compacted message payload vocabulary.

`core-catalog.schema.json` требует эти registries и forbids unknown registry keys.

---

## 5. Identifier boundary

Current `identifier-policies.json` generation `2.0.0` removes the retired generic relationship ID policy and introduces:

```text
world.knowledge
    composite_key(knower_id, fact_id)

runtime.disclosure
    composite_key(player_id, fact_id)

runtime.collaboration_obligation
    independently addressable operational identity
```

Это **не является финальным whole-project identity audit**.

В частности `runtime.message` и ряд других currently sequential policies остаются explicitly provisional until WP-11/WP-16 review independently writable/source-native identity requirements. WP-03 does not grant campaign-global allocator authority merely because an early policy survived into generation `2.0.0`.

---

## 6. Entity-structure boundary

`entity-structures.json` generation `2.0.0` now:

- excludes `world.relationship`;
- represents `world.lore_fact` with separate `truth_status` + `record_status`;
- represents `world.knowledge` as `(knower_id, fact_id, stance)` with bounded current supporting evidence.

Field inventory is **not yet declared globally final**. Owning downstream domains must still inspect state fields for duplicate authority. Example already identified: `world.hazard.detected_by_actor_ids` may encode epistemic state and therefore must be resolved in WP-07 rather than silently accepted as a second knowledge owner.

---

## 7. Engine/catalog version decision

Owner decision during WP-03:

```text
ENGINE PRE-RELEASE IDENTITY: v1.0-alpha
engine_version: 1.0-alpha
release_status: development
recommended_tag: v1.0-alpha

CATALOG GENERATION: 2.0.0
```

Release tooling already accepts generic prerelease suffixes; no release-code change was required for `-alpha`.

No tag/release publication was performed.

---

## 8. Verification / TDD evidence

A WP-03 regression contract was added before machine catalog changes:

- `DEV/TESTS/test_r2_7_wp03_catalog_conformance.py`.

RED was established against exact pre-change repository state: `1.6.0`, `world.relationship`, `truth.disputed`, missing `runtime.disclosure` and old durability/publication registries directly violated the new assertions.

Fresh post-change repository read-back confirms the intended GREEN source state:

- all four DEV catalog artifacts use `2.0.0`;
- `world.relationship` is absent from closed world kinds;
- `runtime.disclosure` and `runtime.collaboration_obligation` are admitted;
- objective truth has exactly three accepted states;
- new closed registries are represented in `core-catalog.schema.json`;
- DEV/GAME engine manifests both use `1.0-alpha` / `v1.0-alpha`.

Limitation: current GitHub Actions `validate.yml` is configured for `main` and `feature/**`, not `v1/engine-rearchitecture`. No new audit branch or CI workaround was created. Therefore WP-03 does **not** claim executable full-suite GREEN evidence from CI. Executable whole-repository validation remains a final-closure obligation under WP-22.

---

## 9. Forward obligations

| ID | Target | Obligation |
|---|---|---|
| WP-03/F01 | WP-04 | finalize Actor/Asset state field vocabulary and Actor-private continuity/relationship representation |
| WP-03/F02 | WP-05 | verify execution record/protocol vocabularies against complete deterministic pipeline schemas |
| WP-03/F03 | WP-07 | finalize lore/knowledge/disclosure/message shapes; eliminate remaining epistemic duplicate fields such as hazard detection lists where applicable |
| WP-03/F04 | WP-10 | materialize all accepted durable/runtime record families into final schemas/roots or explicit NO-DURABLE-RECORD dispositions |
| WP-03/F05 | WP-11 | final whole-project identity policy, including independently writable/source-native IDs; do not assume current sequential policies survive |
| WP-03/F06 | WP-16 | align LIVE/session identities and currentness/fencing with final source-native rules |
| WP-03/F07 | WP-17 | define exact collaboration-obligation schema/identity/current-generation representation |
| WP-03/F08 | WP-18 | define physical Story/planning record families without promoting them into gameplay authority |
| WP-03/F09 | WP-20 | define future post-release catalog/schema evolution policy; current 1.6.0 -> 2.0.0 transition requires no migration |
| WP-03/F10 | WP-22 | execute/extend regression and schema-validation suite for catalog generation 2.0.0 |
| WP-03/F11 | WP-23 | verify release/package metadata and v1.0-alpha manifest parity in final package audit |
| WP-03/F12 | WP-26 | remove stale active prose/version references that still present old catalog inventory as current authority |

---

## 10. Diamond / Strong disposition

WP-03 is not a new Round-2 evidence-selection stage. Relevant previously accepted items are realized as machine vocabulary only where they already have an owning architectural consumer.

- R2.2 Actor continuity / directed relationship concepts: **APPLIED** without generic `world.relationship`.
- R2.3 Context Runtime vocabulary: **APPLIED** as closed protocol/enums, not authority records.
- R2.4 role/TurnEnvelope/Story-service vocabulary: **APPLIED** as logical/protocol vocabulary.
- R2.5 collaboration: **APPLIED NARROWLY** through one admitted operational owner plus protocol vocabulary.
- R2.5/S14 Dramaturg planning: **NOT PROMOTED** to world/runtime authority; physical noncanonical representation remains WP-18.
- Dormant generic extension/plugin machinery remains **DORMANT/REJECTED FOR BASELINE**.

---

## 11. Closure verdict

```text
VERDICT: CLOSED
CATALOG_GENERATION: 2.0.0 / UNRELEASED R2.7 WORKING FINAL ARCHITECTURE
ENGINE_IDENTITY: 1.0-alpha / development
CLASS_ADMISSION_BLOCKERS: 0
OWNER_GATE: NONE
EXECUTABLE_FULL_SUITE_VERIFICATION: DEFERRED TO WP-22
NEXT_DOMAIN: WP-04
```

WP-04 may proceed. It owns Actor / Asset / mechanical-state model realization and must treat the WP-03 class set as routing/classification authority while remaining free to refine field-level state shapes within accepted semantic ownership.
