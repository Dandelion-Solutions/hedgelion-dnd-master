# WP-02 — Global authority / duplicate-owner audit

Статус: **CLOSED — VERIFIED SUBJECT TO READ-BACK**

Date: 2026-08-24

## 1. Итог

WP-02 завершил двусторонний audit semantic ownership.

На уровне accepted architecture конфликтов владельцев не обнаружено. Round 1 + Round 2 последовательно различают:

- semantic/current owners;
- historical/evidence owners;
- narrow operational/noncanonical owners;
- derived/helper projections.

Проблема находится не в принятой semantic architecture, а в текущем machine scaffold: часть `GAME/SCHEMA`, campaign templates, DEV catalog vocabulary и CORE wording всё ещё отражает более ранние модели и может создать второй writable owner либо направить реализацию к superseded semantics.

Owner clarification дополнительно установил clean-slate правило: реальных кампаний нет, поэтому R2.7 удаляет/заменяет stale структуры без backward compatibility. К closure R2.7 должны существовать финальные самосогласованные models/catalogs/schemas/templates/folder scaffold; broad runtime code остаётся после implementation-planning gate.

---

## 2. Архитектурный результат

```text
ARCHITECTURE OWNER-LEVEL CONFLICTS: 0
MACHINE CONFORMANCE GAPS: MATERIAL / EXPECTED PRE-IMPLEMENTATION DEBT
OWNER DECISION REQUIRED: 0
BACKWARD-COMPATIBILITY BLOCKER: 0
```

Ключевой закон WP-02:

> Физическая копия, cache, LIVE packing, SQLite row, Story record, checkpoint hint или index не становится вторым owner автоматически. Конфликт существует тогда, когда representation может независимо отвечать/мутировать semantic concern, уже принадлежащий другому accepted owner.

---

## 3. Material machine findings

### WP02-M01 — legacy embedded epistemic stores

Текущие `npc.schema.yaml`, `pc.schema.yaml` и `faction.schema.yaml` содержат writable `knowledge` / belief / suspicion arrays. `item.schema.yaml` содержит `identified_by_pc_ids`; `thread.schema.yaml` содержит `known_by_pc_ids`.

Disposition: **STALE DUPLICATE OWNER**.

Final architecture routes current fictional proposition stance through common `world.knowledge`; PC voluntary mental state remains player-owned. Эти embedded arrays не сохраняются ради совместимости.

Targets: WP-04, WP-07, WP-10, WP-22.

### WP02-M02 — retired Secret remnants

`item.schema.yaml` и `location.schema.yaml` всё ещё содержат `secret_ids`, хотя standalone Secret record/root/schema уже retired.

Disposition: **STALE RETIRED SURFACE**.

Final: удалить поля; secrecy определяется eligibility над truth/knowledge/disclosure, а не отдельным Secret owner.

Targets: WP-07, WP-10, WP-19.

### WP02-M03 — stale objective-truth model

`lore.schema.yaml` использует общий `status = canonical|superseded|disputed_in_world`; `DEV/CATALOG/core-catalog.json` всё ещё допускает objective truth `disputed`.

Disposition: **CLASS MODEL MISMATCH / RETIRED VOCABULARY**.

Final: независимые axes objective `truth_status = undetermined|established|disproven` и record lifecycle; in-world dispute принадлежит `world.knowledge`.

Targets: WP-03, WP-07, WP-10, WP-22.

### WP02-M04 — missing accepted disclosure owner realization

`runtime.disclosure` принят Step 4/5.12, но отсутствует в текущем closed runtime catalog и не имеет final shipped persistent family/root.

Disposition: **MISSING REALIZATION**.

Targets: WP-03, WP-07, WP-10, WP-11.

### WP02-M05 — generic `world.relationship` superseded by R2.2

Старый catalog всё ещё содержит `world.relationship(subject_id, object_id, relation, attitude, strength, status)` и generic relationship transition/event vocabulary. Поздний R2.2 закрепляет subjective directed relationship view за source Actor; objective social facts остаются у natural typed owners.

Disposition: **STALE GENERIC OWNER**.

Final baseline: generic `world.relationship` в нынешней форме retired. Если будущий objective relationship действительно потребует independent lifecycle, он должен доказать отдельный конкретный typed owner; старый generic container не сохраняется как placeholder.

Targets: WP-03, WP-04, WP-05, WP-10.

### WP02-M06 — global chronology frontier scaffold

`current_state.schema.yaml`, `GAME/CAMPAIGN/STATE/CURRENT.yaml` и CORE `CHRONOLOGY.md` всё ещё используют `CURRENT.world_time.frontier` как globally reconciled chronology frontier.

Step 5.9 требует owner-anchored sparse chronology и не вводит mandatory global current fictional clock/frontier.

Disposition: **STALE AUTHORITY/CURRENTNESS SHAPE**.

Final: global-frontier semantics удалить/заменить точными owner/domain chronology relations/providers, которые будут закрыты WP-15; CURRENT остаётся compact routing/current-state surface, но не world-time authority.

Targets: WP-10, WP-14, WP-15, WP-19.

### WP02-M07 — checkpoint schema/template materially stale

Текущие checkpoint schema/template требуют/хранят:

- `valid_through_event_id`;
- `expected_commit_sha`;
- copied `world_time`;
- active PC/thread/scene lists.

Step 5.7 прямо отвергает первые два как canonical recovery semantics, а copied time/lists допускает только как optional non-authoritative hints при доказанной полезности.

Disposition: **STALE RETIRED / UNPROVEN HINT SURFACES**.

Clean-slate default: удалить; WP-14 может вернуть узкий hint только если докажет bounded recovery/diagnostic value.

Targets: WP-14, WP-19, WP-22.

### WP02-M08 — recovery instruction mismatch

`GAME/CORE/STORAGE.md` в `Canonical read order` ставит checkpoint/hot STATE раньше exact WORLD owner reads, что конфликтует с Step-5.7 `current-authority-first` recovery.

Disposition: **INSTRUCTION MISMATCH**.

Targets: WP-14, WP-26.

### WP02-M09 — runtime.message identity mismatch

`identifier-policies.json` всё ещё делает `runtime.message` campaign-global sequential ID. Step 5.12 требует collision-safe source-native identity для independently writable session/live scopes без global pre-response reservation.

Disposition: **IDENTITY MISMATCH**.

Targets: WP-03, WP-07, WP-11, WP-16.

### WP02-M10 — LIVE physical packing can become semantic mega-owner

`live_scene.schema.yaml` / `LIVE_SCENE.md` содержат generic live fact/knowledge/disclosure packing, provisional IDs и более старую write-fence модель. Step 5.8 позднее требует, чтобы physical LIVE partition не заменял native semantic owners; accepted live-born externally referenced identities должны быть stable; authoritative fencing uses exact live source revision.

Важно: `observable_events.perceived_by_pc_ids` может законно выжить как historical perception evidence, но не как current `world.knowledge`/`runtime.disclosure` authority. `live_facts.known_by_pc_ids` как current knowledge copy — stale.

Targets: WP-07, WP-11, WP-12, WP-13, WP-16.

### WP02-M11 — durable reverse presence risk

`location.schema.yaml -> state.present_entity_ids` хранит reverse presence while Actor/Asset natural owners carry current placement.

Disposition: **DUPLICATE-OWNER RISK**.

Clean-slate final default: не хранить второй writable current-presence owner. Если lookup требует reverse presence, использовать derived/rebuildable routing/index либо specifically proven scene membership contract.

Targets: WP-04, WP-09, WP-10, WP-11.

### WP02-M12 — accepted owner families still missing physical realization

Final shipped persistent/HOT representation ещё отсутствует для ряда уже принятых owners: common `world.knowledge`, `runtime.disclosure`, часть Step-3 operational records, Story projection progress, collaboration obligation, player-local/shared Dramaturg horizons и другие R2.x typed products.

Disposition: **MISSING REALIZATION**, не разрешение переиспользовать legacy fields.

Targets: WP-05, WP-07, WP-10..WP-12, WP-14, WP-17, WP-18.

---

## 4. Class-model mismatch, не duplicate owner

Существующие GAME schemas (`pc`, `npc`, `item`, `faction`, etc.) и accepted DEV catalog (`world.actor`, `world.asset`, `world.organization`, etc.) представляют разные поколения machine model.

Само наличие двух названий ещё не доказывает duplicate semantic writer, потому что physical/schema specialization может представлять один owner. Но финальная архитектура должна иметь один согласованный envelope/kind model. Clean-slate owner decision разрешает полностью заменить legacy schema family вместо поддержки обоих вариантов.

Targets: WP-03, WP-04, WP-10.

---

## 5. Adversarial false-positive check

Проверены потенциальные случаи, где audit мог ошибочно удалить допустимое evidence:

- Event/perception evidence может авторитетно доказывать факт восприятия, не становясь current knowledge owner.
- Checkpoint может хранить собственный immutable descriptor/provenance, но не current state/recovery completeness.
- Story projection state действительно владеет layer-local coverage/allocator progress, но не canon.
- LIVE source может физически содержать current native owner bytes, но не становится semantic mega-owner.
- Reverse indexes могут хранить copies только как derived/rebuildable structures с owner-based currentness.

После этой проверки новых owner trade-offs не появилось.

---

## 6. Existing test gap

`DEV/TESTS/test_step_5_0_contamination.py` защищает ранние retirement cases (`world.timeline_marker`, generic pending bucket, duplicate checkpoint pointer, old Secret root/schema, tactical bucket), но не проверяет новые post-Step-4/Step-5/R2 stale surfaces, перечисленные выше.

Forward obligation: WP-22 должен добавить whole-project static/schema regression class для duplicate-owner/retired-vocabulary запретов после structural canonicalization.

---

## 7. Negative findings

- Accepted architecture не создаёт generic memory database, universal RecoveryCut/snapshot, global scheduler, global active-player state, Story-as-canon или SQLite-as-canon.
- Active `WORLD/SECRETS/` root и `secret.schema.yaml` уже отсутствуют; Step-5.0 retirement частично реализован правильно.
- `index.schema.yaml` уже говорит, что index — routing, не entity database.
- `event.schema.yaml` уже отвергает mandatory campaign-global event order.
- `scene.schema.yaml` уже отвергает generic tactical-state owner и помечает local chronology frontier как non-global.

---

## 8. Forward obligations created by WP-02

```text
WP-02/F01 -> WP-03  final closed class/vocabulary cleanup, including disclosure, truth and relationship vocabulary
WP-02/F02 -> WP-04  unified Actor/Asset + Actor-private relationship/current-state model
WP-02/F03 -> WP-07  final truth/knowledge/disclosure/message semantic record model
WP-02/F04 -> WP-10  final persistent record families/schemas and removal of legacy parallel schema families
WP-02/F05 -> WP-11  roots/IDs/index/sharding for accepted owner families
WP-02/F06 -> WP-14  final checkpoint/session/recovery representation, current-authority-first
WP-02/F07 -> WP-15  remove global chronology-frontier authority and define exact sparse chronology realization
WP-02/F08 -> WP-16  final LIVE native-owner packing/identity/fencing/currentness
WP-02/F09 -> WP-19  final campaign scaffold emits only canonical structures
WP-02/F10 -> WP-22  duplicate-owner / retired-vocabulary regression suite
WP-02/F11 -> WP-26  remove stale CORE/schema-routing wording
```

All are final-closure blocking until discharged by their owning domains.

---

## 9. Round-2 Diamond / Strong disposition

No new D/S activation.

R2.2 directed source-Actor relationships and R2.3 SQLite/index non-authority are materially enforced by this audit. R2.5 planning remains narrow noncanonical state. Dormant items remain dormant.

---

## 10. Human decision

```text
NONE
```

The clean-slate structural-canonicalization decision supplied by the owner has been incorporated into the governing R2.7 owner clarification.

---

## 11. Closure verdict

```text
DOMAIN: WP-02
VERDICT: MAY CLOSE
ARCHITECTURE OWNER CONFLICTS: 0
MACHINE STALE/MISSING CLUSTERS: 12
OWNER_GATE: NONE
NEXT_DOMAIN: WP-03 — catalog/class/capability completeness
```
