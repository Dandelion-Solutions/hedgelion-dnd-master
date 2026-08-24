# WP-02 — Global authority / duplicate-owner audit

Статус: **IN PROGRESS**

Date: 2026-08-24

## 1. Краткий вывод текущего slice

Первый slice (`canonical owner inventory + authority taxonomy`) завершён.

Принятая архитектура Round 1 + Round 2 внутренне последовательно различает:

1. **semantic/current owners** — единственные writable/current владельцы своих семантических concerns;
2. **historical/evidence owners** — владеют фактом принятого события/сообщения/результата, но не текущим world state;
3. **narrow operational/noncanonical owners** — владеют только собственным bounded progress/control lifecycle (например Story projection progress или collaboration generation), не gameplay truth;
4. **derived/helper projections** — indexes, Agenda, ContextTrace, MechanicalContext и другие ускорители/представления без самостоятельной semantic authority.

На уровне accepted architecture owner-level противоречия не найдено. Следующий обязательный slice — reverse audit текущих machine/runtime surfaces: существуют ли в `GAME/SCHEMA`, campaign templates, CORE, DEV catalogs/schemas или legacy fields физические представления, которые нарушают эту taxonomy либо создают второй writable owner.

Полная derivative owner matrix:

- `DEV/docs/superpowers/research/2026-08-24-r2-7-global-semantic-owner-matrix.md`

---

## 2. Покрытые вопросы

```text
WP-02/Q1 every mutable/current concern exactly one accepted authority?
    ARCHITECTURE LAYER: SATISFIED
    MACHINE LAYER: NOT YET AUDITED

WP-02/Q2 definition/current/derived/Story/planning/session separation?
    ARCHITECTURE LAYER: SATISFIED
    MACHINE LAYER: NOT YET AUDITED

WP-02/Q3 can YAML/SQLite/index/chat/Story/checkpoint/prep become second owner?
    CANONICAL LAW: NO
    CURRENT MACHINE CONFORMANCE: NEXT SLICE

WP-02/Q4 deterministic acceptance distinct from LLM proposal/narration?
    ARCHITECTURE LAYER: SATISFIED
    CURRENT CORE/MACHINE CONFORMANCE: NEXT SLICE / WP-05/WP-08 deeper follow-up
```

---

## 3. Source Manifest delta

Current primary owners inspected for this slice:

| Source | Authority role | Slice use |
|---|---|---|
| `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md` | AGREED semantic/model contract | class admission; definition/world/runtime/value boundaries; metadata placement; no duplicate state |
| `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md` | AGREED Step-1 architecture | ResolvedCatalogContext, no same-ID shadowing, discovery != authority |
| `DEV/ARCHITECTURE/ACTOR_MODEL.md` | AGREED Actor machine/model contract | Actor HP/resources/lifestate/derived inventory/condition boundaries |
| `DEV/ARCHITECTURE/ASSET_MODEL.md` | AGREED Asset model | definition/instance/placement/resource ownership, derived access/possession |
| Step-3 execution canonical spec | CANONICAL | Interaction/IntentPlan/Command/Procedure/Resolution/Continuation/Event/receipt authority |
| Step-4 truth/knowledge/context/Story canonical spec | CANONICAL | lore/knowledge/disclosure separation; context non-authority; preparation noncanonical |
| Step-5.0 authority contamination final | CANONICAL CLOSED REVIEW | retired duplicate/premature owners; preserved runtime owners |
| Step-5.7 recovery canonical | CANONICAL | current-authority-first; checkpoint optional/non-authoritative; derived rebuild |
| Step-5.8 live ownership canonical | CANONICAL | live physical partition != semantic mega-owner; routing selects source authority |
| Step-5.9 chronology canonical | CANONICAL | sparse relation evidence; no global clock/time owner |
| Step-5.10 Story canonical | CANONICAL | Story layer-local projection ownership only; Chronicler no IDs/progress/canon |
| Step-5.11 transcript canonical | CANONICAL | runtime.message evidence vs truth/current state; selective exact |
| Step-5.12 delivery/disclosure canonical | CANONICAL | message/disclosure/knowledge/truth separation; EMISSION_COMMIT |
| Step-5.14 integrated canonical final | CANONICAL INTEGRATION | cross-slice false-authority sweep |
| R2.1 continuity canonical | CANONICAL | no generic memory authority; Story orientation only |
| R2.2 Actor continuity canonical | CANONICAL | source-Actor private continuity; `world.knowledge` remains epistemic owner |
| R2.3 Context Runtime canonical | CANONICAL | context/index/trace/SQLite authority boundaries |
| R2.4 single-context execution canonical | CANONICAL | TurnEnvelope control only; typed drafts; deterministic acceptance |
| R2.5 multiplayer canonical | CANONICAL | collaboration collection-only; planning noncanonical |

The current derivative `CANONICAL_ARCHITECTURE_INDEX.md` was used only to locate owners and identify the integrated invariant set; correctness claims above were then checked against primary sources.

---

## 4. Установленные факты и ограничения

### WP02-F01 — one owner means one semantic writer, not one physical copy

Hydration, sharding, LIVE packing, SQLite/HOT working copies and derived views may move/duplicate bytes without transferring semantic ownership.

### WP02-F02 — historical evidence has bounded authority

Events/messages/receipts can authoritatively prove their own accepted occurrence/evidence semantics while still being unable to answer current-state questions.

### WP02-F03 — noncanonical state may own noncanonical progress

Story projection state, collaboration generation and Dramaturg planning generation may be real persistent state. Their persistence does not promote them to gameplay canon/current authority.

### WP02-F04 — accepted LLM products require downstream acceptance

Interpretation/proposal/editorial/narrative output remains non-authoritative until the relevant deterministic/native acceptance boundary establishes the owned consequence.

### WP02-F05 — physical currentness may precede durability

HOT/SQLite can contain newer `ESTABLISHED` SOFT owner state than Git. This does not make SQLite format the authority and does not make Git automatically newer semantically.

### WP02-F06 — current routing can select another physical native source

During LIVE, current campaign routing may select a live source for claimed owners. The underlying Actor/Asset/Procedure/etc owner remains the same semantic owner.

---

## 5. Architecture -> machine

Current slice establishes the semantic side only. Exact physical destinations are intentionally deferred to later WP domains.

The global matrix already records all currently identified owner classes and explicit non-owner relations. Machine realization status remains `TO AUDIT` where existing schemas/templates may still encode older assumptions.

---

## 6. Machine -> architecture

`NOT YET COMPLETE`.

Next slice must inspect at minimum:

- `GAME/SCHEMA/*.schema.yaml`;
- `GAME/CAMPAIGN/` current templates/indexes;
- `DEV/CATALOG/*.json` and relevant `DEV/SCHEMAS/*.schema.json`;
- current `GAME/CORE` storage/session/live/current/persistence modules;
- legacy/stale fields known from Step-5.0 and later canonical amendments;
- current machine surfaces corresponding to Story, message/disclosure/knowledge and R2.2–R2.5 additions.

---

## 7. Конфликты / stale / negative findings

### Negative finding WP02-N01

No accepted architecture-level duplicate-owner conflict was found in the canonical model.

### Negative finding WP02-N02

No accepted architecture authorizes a generic `memory`, universal snapshot/frontier, global scheduler, global chronology clock, global active-player state, Story-as-canon, checkpoint-as-current-state or SQLite-as-canon abstraction.

### Machine findings

Pending next slice.

---

## 8. Автоматически принятые технические решения

### AUTO-02-01 — four-class ownership taxonomy

Use the four classes `SEMANTIC_CURRENT`, `HISTORICAL_EVIDENCE`, `NARROW_OPERATIONAL_NONCANONICAL`, `DERIVED_HELPER` in R2.7 ledgers where classification clarity is needed.

This is a derivative audit vocabulary only; it creates no runtime classes/schemas.

Why no owner gate: it summarizes already accepted semantic distinctions without changing them.

### AUTO-02-02 — local authority must be named with scope

Future mappings must not label Story/collaboration/checkpoint merely `NON_AUTHORITATIVE`. They must state the narrow concern they do own, then explicitly state the stronger semantics they do not own.

Why no owner gate: avoids losing accepted local lifecycle semantics during implementation.

---

## 9. Implementation obligations

No new implementation obligations are closed in slice A. Exact stale/duplicate machine surfaces are identified in later slices.

---

## 10. Verification / MVP acceptance obligations

Pending machine reverse audit. Likely regression classes will include duplicate-owner schema/static checks and runtime acceptance-boundary tests, but no coverage claim is made yet.

---

## 11. Forward obligations

No new forward obligations from slice A yet.

Existing WP-01 forward obligations remain open in the durable status ledger.

---

## 12. Round-2 Diamond / Strong delta

`NO DELTA` in slice A.

R2.1/R2.2/R2.3/R2.5 owner distinctions are preserved; no dormant item is activated.

---

## 13. Human decision

```text
NONE
```

---

## 14. Closure verdict

```text
DOMAIN: WP-02
VERDICT: IN_PROGRESS
COMPLETED_SLICE: canonical owner inventory + authority taxonomy
OWNER_LEVEL_CONFLICTS: 0
NEXT_SLICE: derived/helper/non-owner taxonomy + current machine reverse inventory
OWNER_GATE: NONE
```

---

## 15. Точка продолжения

```text
read audit-status
-> global semantic-owner matrix
-> inspect current GAME/SCHEMA + GAME/CAMPAIGN + DEV/CATALOG/SCHEMAS
-> inspect current storage/session/live/index/current runtime consumers
-> classify every apparent owner/copy against the owner matrix
-> checkpoint machine reverse findings before adversarial WP-02 closure
```