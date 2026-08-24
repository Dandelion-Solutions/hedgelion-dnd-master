# R2.7 — WP-06 — Rules / adjudication / domain-module compatibility — мини-отчёт

Статус: **IN PROGRESS — SOURCE/GAP DISCOVERY SLICE CHECKPOINT**

Дата: 2026-08-24

## Краткий вывод

Первый slice WP-06 подтвердил, что принятая Activity/Rule-Element/Step-3 архитектура подходит как единый механический kernel, но текущая machine realization ещё не готова к implementation planning.

Главные gaps:

1. `core-catalog.json` регистрирует полный набор `rule_selectors`, но `mechanical-surfaces.json` структурно описывает только малую часть; это бывший Step-6 debt, который теперь обязан закрыть WP-06.
2. `definition.class/subclass/species/background/advancement/feat/feature/spell` зарегистрированы, но их mechanically material `data` сейчас в основном проходит через generic `data: object`; stable advancement/build choice slots и их validation отсутствуют.
3. `ActionRequest.parameter_bindings` существует, но Activity definition не объявляет closed typed parameter contract/source class; это оставляет недоопределённым легальный канал для invocation-specific adjudicated values (например bounded quick ruling inputs) и может превратить произвольный LLM scalar в скрытую mechanical authority.
4. `value.target_spec`, `value.area_spec`, `value.cost_spec`, `value.roll_request`, `value.signal`, `value.state_delta` зарегистрированы неравномерно: часть имеет machine shape, часть остаётся только vocabulary. Их нужно либо материализовать как embedded typed interface, либо дать explicit implementation-only/abstract disposition; independent record class не требуется.
5. Domain CORE в целом соблюдает pre-narration mechanics и local-first latency policy, но несколько модулей используют stale ownership wording (`COMBAT` operational state vs Procedure, `REWARDS` ITEM/identified-by-PC).
6. Campaign `HOUSE_RULES.md` существует как durable policy prose, но executable mechanics не могут законно обходить catalog/Activity/Rule-Element/Step-3 kernel только потому, что правило записано в Markdown. Нужна точная policy->machine boundary.

Architecture blocker пока не обнаружен; gaps технически закрываемы внутри принятой архитектуры.

Human decision: **NONE**.

---

## Покрытые вопросы текущего slice

- owning Activity model;
- owning Rule Element / Trigger Binding model;
- Step-3 execution handoff;
- current `core-catalog.json` mechanical registries;
- current `mechanical-surfaces.json` + schema;
- current `catalog-definition.schema.json`;
- current Actor `choice_bindings`/READY_PC contract;
- campaign rules/house-ruling surface;
- initial reverse audit of ADJUDICATION / COMBAT / MAGIC / EXPLORATION / DIALOGUE / ENCOUNTERS / ADVANCEMENT / REWARDS / RUNTIME / MECHANICS_INTEGRITY / RANDOMNESS / CORE_INDEX.

---

## Source Manifest delta

Owning/current:

- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`;
- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`;
- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`;
- Step-3 canonical deterministic execution spec;
- WP-04 progressive READY_PC owner clarification and current `CHARACTER_READINESS.md`;
- WP-05 deterministic execution mini-report;
- `DEV/CATALOG/core-catalog.json`;
- `DEV/CATALOG/mechanical-surfaces.json`;
- `DEV/CATALOG/entity-structures.json`;
- `DEV/SCHEMAS/catalog-definition.schema.json`;
- `DEV/SCHEMAS/activity-definition-data.schema.json`;
- `DEV/SCHEMAS/rule-element.schema.json`;
- `DEV/SCHEMAS/mechanical-surfaces.schema.json`;
- current domain CORE modules listed above;
- `GAME/RULES/README.md`;
- `GAME/CAMPAIGN/RULES/HOUSE_RULES.md`.

`CATALOG_MODEL.md` is derivational/background where superseded by current inventory/model-specific owners; it is not used to resurrect retired classes.

---

## Установленные факты

### F1 — единый rule execution boundary уже принят

Material mechanics must route through:

```text
intent/adjudication
    -> ActionRequest(Activity) OR deterministic TransitionRequest
    -> Step-3 execution kernel
    -> accepted state/event/receipt evidence
    -> narration
```

Domain CORE may decide/adjudicate what mechanic applies; it cannot make prose narration itself the state transition.

### F2 — Rule Elements чистые и owner-local

Rule Elements/Trigger Bindings remain embedded under rules-bearing definitions and cannot mutate state, query arbitrary world data or invoke code/network/SQL/GitHub. Mutating consequence is always Activity/Step-3 work.

### F3 — structured selector metadata incomplete

`core-catalog.json` contains a broad closed `rule_selectors` registry (ability/test/save/attack/DC/AC/damage/healing/resource/activity/target/effect/health/condition/movement/sense/proficiency/trait), while current `mechanical-surfaces.json` describes only a small state-sensitive subset.

The current Step-2 model explicitly deferred full expansion to the former Step 6. Since that stage no longer exists as an architecture stage and R2.7 is the final gate, WP-06 owns closure of this debt.

### F4 — current build-choice validation is insufficient

Actor stores stable `build.choice_bindings`, but there is no strict machine contract proving:

- which active choice slots exist for selected class/species/background/subclass/advancement sources;
- stable `choice_id`;
- legal options/cardinality;
- which current-level choices must already be closed before READY_PC/level-up completion.

`definition.advancement` is catalogued and `entity-structures.json` expects level data, but `catalog-definition.schema.json` does not bind it to a strict data schema.

### F5 — quick rulings need a typed invocation channel

CORE intentionally permits a quick fair local ruling to preserve play flow when exact RAW is not locally available. That does not authorize a free-form mechanical bypass.

`ActionRequest.parameter_bindings` can carry scalar values, but the Activity currently lacks an exact parameter declaration/source contract. WP-06 must make any adjudicated parameter explicit, bounded, fingerprinted/traceable through Step 3 and impossible to confuse with engine-owned state.

### F6 — house-rule prose is policy authority, not mutation authority

`GAME/CAMPAIGN/RULES/HOUSE_RULES.md` is a durable campaign policy source. A recurring house mechanic must, where executable, map to existing registered capabilities/definitions/Rule Elements/Activities or an explicit typed adjudication contract. Markdown cannot invent new `op.*`, selector or direct state mutation semantics.

If a desired recurring rule requires an unregistered executable primitive, the correct result is a catalog-gap/engine-change path, not prose execution.

### F7 — domain CORE largely preserves local-first smoothness

ADJUDICATION, MECHANICS_INTEGRITY, RANDOMNESS and RUNTIME already require local/bounded resolution, actual RNG when needed, no retrospective tuning, and no routine web/GitHub verification round-trip. WP-06 changes must preserve this.

### F8 — COMBAT ownership wording is stale/ambiguous

`COMBAT.md` lists initiative/order and other operational combat state without explicitly routing Procedure-local timing/action budget state to `runtime.procedure`. `world.encounter` may remain a world-facing referent, but cannot become generic Procedure authority.

### F9 — REWARDS contains legacy storage vocabulary

`REWARDS.md` still speaks about significant magic items receiving ITEM records and storing what each PC has identified. Current architecture requires `world.asset` plus Step-4 truth/knowledge/disclosure ownership; exact epistemic correction belongs to WP-07.

### F10 — other domain modules do not presently prove a new owner

MAGIC, EXPLORATION, DIALOGUE, ENCOUNTERS and ADVANCEMENT contain domain policy but their material mechanics can be routed through the accepted kernel. Their stale/underspecified parts require machine/interface clarification, not new independent semantic owners.

---

## Architecture -> machine — current partial verdict

| Responsibility | Current status |
|---|---|
| Activity definition envelope | PARTIAL — parameter/target/cost contracts incomplete |
| Rule Element / Trigger Binding | SATISFIED baseline; full selector metadata missing |
| selector/accessor/input-class registry | GAP — selector coverage incomplete |
| stable build/advancement choice slots | GAP |
| Actor choice binding validation | GAP |
| quick local adjudicated mechanical value | GAP — typed Activity parameter source contract needed |
| house-rule routing | PARTIAL — semantic policy exists, execution boundary must be explicit |
| domain CORE -> deterministic execution | PARTIAL — mostly aligned; stale ownership wording found |
| gameplay latency | SATISFIED baseline; must remain invariant through machine closure |

---

## Machine -> architecture — current partial verdict

- `ActionRequest.parameter_bindings`: legitimate accepted-invocation input surface, but **must be definition-declared/typed**; not open LLM authority.
- generic `value.state_delta`: must not become arbitrary JSON patch/mutation capability. Either operation-owned typed mutation-plan interface or abstract implementation-only value; no independent authority.
- `value.signal`: transient timing/calculation context; no durable owner.
- `value.roll_request`: transient deterministic RNG request; accepted raw result belongs to Resolution/Continuation when continuity requires it.
- `value.target_spec` / `value.area_spec` / `value.cost_spec`: embedded rule-definition/request contracts, not records.
- `HOUSE_RULES.md`: campaign rule-policy source, not world/runtime record and not executable mutation language.

---

## Конфликты / stale / negative findings

1. Full selector registry vs partial structured metadata — **GAP, current WP-06**.
2. Mechanically material definition families with generic unvalidated `data` — **GAP, current WP-06**.
3. Actor choice IDs with no owning choice-slot schema — **GAP, current WP-06**.
4. Open Activity parameter bindings without declaration/provenance class — **GAP, current WP-06**.
5. COMBAT operational ownership ambiguity — **STALE DOC/MAPPING**, WP-06/WP-26.
6. REWARDS ITEM/identified-by-PC wording — **STALE DOC/MAPPING**, WP-07/WP-26.
7. `CORE_INDEX.md` still contains retired pre-live/first-true-live READY_PC wording — already known WP-04/WP-26 debt; not reopened here.
8. No requirement discovered for arbitrary executable house-rule/plugin language — **REJECTED / NOT NEEDED**.

---

## Автоматически принятые технические решения текущего slice

1. Do not add a new rule-execution owner; preserve Activity/Rule-Element/Step-3 kernel.
2. Stable advancement/build choices must be definition-owned and Actor must retain only stable instance selections/current state.
3. Quick local rulings must remain possible without web lookup, but every mechanical scalar/ref accepted from adjudication must be declared by the Activity and become fixed causal execution input.
4. Do not allow generic `state_delta` JSON-patch authority.
5. Preserve normal-turn local/bounded execution; selector/parameter validation must compile/cache on definition load, not add repeated LLM/network work.
6. Campaign house-rule prose may govern adjudication but cannot self-register executable capabilities.

---

## Forward obligations currently visible

- WP-05/F01 is **ACTIVE IN WP-06**.
- WP-04/F01 is **ACTIVE IN WP-06**.
- Exact stale CORE wording cleanup may be completed here where owner-local, otherwise typed to WP-26.
- REWARDS identification/disclosure correction is additionally routed to WP-07.
- Operation/schema executable tests remain WP-22 final execution gate.
- Performance consequences remain WP-24 final proof.

---

## Human decision

`NONE`.

No material product semantic or architecture trade-off has emerged from this slice.

---

## Точка продолжения

```text
CURRENT_DOMAIN: WP-06
CURRENT_SLICE: advancement/build-choice contract + Activity parameter/target/cost contract
AFTER_THAT: full mechanical selector metadata + activity operation-contract closure
THEN: domain CORE reverse-conformance closure + Russian final mini-report
NEXT_DOMAIN: WP-07
OWNER_GATE: NONE
```
