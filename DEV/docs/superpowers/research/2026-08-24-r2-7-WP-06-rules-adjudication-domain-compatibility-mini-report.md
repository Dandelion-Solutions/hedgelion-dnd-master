# R2.7 — WP-06 — Rules / adjudication / domain-module compatibility — мини-отчёт

Статус: **IN PROGRESS — POST-S6D INCOMING-OBLIGATION RECONCILIATION CHECKPOINT**

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


---

## Post-S6D reconciliation — incoming WP-04/F01 and WP-05/F01

**Evidence status:** COMPLETE for the two incoming obligations. The earlier source/gap-discovery material above is retained as **historical pre-S6D evidence**; it is not the current status of the machine contracts named below.

### Source Manifest delta for this reconciliation

| Source family | Role / inspected scope |
|---|---|
| `CHARACTER_PROGRESSION_READY_PC_SEED.md`, `CHARACTER_READINESS.md` | CANONICAL: definition-owned grants/slots, sparse Actor bindings, provisional play, READY_PC and anti-retrofit law. |
| advancement/build/Actor schemas; MVP seed; S6D-07 fixture/test | MACHINE/TEST: stable slots, strict binding shape, seed closure and readiness/advancement rejection cases. |
| Step-3 spec and WP-05 mini-report; `ACTIVITY_MODEL.md`, `RULE_ELEMENT_MODEL.md` | CANONICAL: accepted execution kernel and owner boundary. |
| `PORTABLE_ACTIVITY_VALUES.md`, portable-value catalogs/schemas and S6D-05 test | CANONICAL/MACHINE/TEST: seven embedded typed values, exact schema roots and recovery/equality dispositions. |
| `ACTIVITY_PRIMITIVE_CONTRACTS.md`, `CALCULATION_SELECTOR_METADATA.md`, `MECHANICAL_CONTEXT.md` | CANONICAL: closed primitive/selector/read/input authority; no arbitrary payload/query/state access. |
| `DOMAIN_RULES_COVERAGE.md` and S6D-09 package/coverage companions | CANONICAL/MACHINE: finite supported gameplay spine and Mechanical-Null disposition. |
| `HOUSE_RULES_MECHANICAL_BOUNDARY.md`, its ledger/schema/test, `ADJUDICATION.md` | CANONICAL/MACHINE/RUNTIME: one-off typed inputs only; policy prose has no execution, RNG or mutation authority. |
| `RULESET_PACKAGE_MACHINE_CLOSURE.md` and package closure chain | CANONICAL/MACHINE: identity-bound admitted package/lock closure; package text/identity does not itself execute mechanics. |

### WP-04/F01 — item reconciliation

| Required item | Disposition | Exact current evidence |
|---|---|---|
| advancement schema | **SATISFIED** | `advancement-definition-data.schema.json` requires `levels` and delegates every level choice to `build-choice-slot.schema.json`; S6D-07 seed/test compile its bounded Fighter 1→2 proof. |
| stable choice IDs | **SATISFIED** | Canonical S6D-07 law: each choice ID is stable in its owner definition revision and accepted catalog context; slot schema requires `choice_id` and option IDs; compiler test rejects duplicate slot/binding/option and illegal cardinality/default. |
| Actor `choice_bindings` | **SATISFIED** | `world-actor-state.schema.json` owns sparse `build.choice_bindings` with selected option IDs and a closed `selection_basis`; S6D-07 tests reject flattened-sheet substitution and verify sparse owner-relative bindings. |
| progressive character materialization | **EXTENDED** | Current owner permits provisional gameplay before READY_PC only under local committed-dependency sufficiency; same stable Actor may persist from PROVISIONAL_IDENTITY through readiness. This is more precise than the pre-pause obligation. |
| READY_PC initial commitment frontier | **SATISFIED** | S6D-07 law + `CHARACTER_READINESS.md`: uniquely reconstructable legal initial build, all material initial choices closed and admitted dependencies; not questionnaire completion. Tests distinguish unresolved Fighter style from valid READY_PC. |
| reconstructable Actor build | **SATISFIED** | Defined reconstruction chain is resolved catalog → anchors/levels → grants/slots → accepted sparse bindings/spells → admitted dependencies → derived capabilities/readiness evidence; attestation is actor/revision/ruleset/catalog-bound and forgery fails. |
| no situation-aware retrofit | **SATISFIED** | S6D-07 initial selections are fixed before relevant exposure. `CHARACTER_READINESS.md` forbids delaying proficiency/spell/stat/defense choices until an advantageous scene; post-READY gaps are integrity defects, not convenient selection. |

**WP-04/F01 verdict: SATISFIED / EXTENDED BY S6D-07.** No new advancement/Actor surface is authorized or needed in WP-06.

### WP-05/F01 — item reconciliation

| Typed value / requirement | Disposition | Exact current owner, realization and qualifier |
|---|---|---|
| `target_spec` | **SATISFIED** | S6D-05 canonical embedded nonowner; `target-spec.schema.json` via Activity `targeting`; portable route catalog marks `ACTIVE_STRUCTURAL`. Target IDs/state are excluded. |
| `area_spec` | **SATISFIED** | S6D-05 embedded under TargetSpec; exact shape/unit/dimension catalog contract; geometry is bounded runtime infrastructure, not content query authority. |
| `duration_spec` | **SATISFIED** | S6D-05 embedded definition intent with exact modes/units; concrete scheduled identity remains the separate TemporalBinding owner. |
| `cost_spec` | **SATISFIED** | S6D-05 embedded declared resource/payer/amount/commit point; S6D-06 owns reservation/mutation/refund/atomicity. `cost_commit.on_accept` remains explicitly dormant until an exact primitive contract—no inferred generic cost capability. |
| `roll_request` | **SATISFIED** | S6D-05 typed transient request; only S6D-06 `op.roll` consumes RNG; typed RollResult is fixed causal evidence reused over retry/recovery. |
| `signal` | **SATISFIED** | Explicit `EMBEDDED_NONOWNER / DORMANT_NONSELECTABLE`: root rejects every instance without an exact consumer; no lifecycle/event-bus authority. |
| `state_delta` | **SATISFIED** | Explicit `EMBEDDED_NONOWNER / DORMANT_NONSELECTABLE`: no generic patch/mutation or trusted continuation retention; a future exact variant needs an S6D-06 primitive/transition contract. |
| every material domain mechanic uses deterministic Step-3 boundary | **EXTENDED** | WP-05 kernel remains authoritative. S6D-09 derives finite package/active-consumer/product coverage, routes generic check/save through admitted Activities/primitives and permits Mechanical-Null only with its real Event/receipt. S6D-10 permits one-off adjudication only as declared typed accepted input to an existing consumer; it cannot execute RNG, mutate state, create a second authority or force a reusable primitive. The full per-domain/CORE reverse audit remains the next WP-06 slice. |

**WP-05/F01 verdict: SATISFIED / EXTENDED BY S6D-05, S6D-06, S6D-09 and S6D-10.** Dormant values remain intentionally nonselectable; their explicit negative disposition is closure, not unfinished activation work.

### Reconciled pre-S6D findings

1. broad selector vocabulary versus partial metadata — **SUPERSEDED** by S6D-03 finite active/dormant selectability ledger;
2. generic advancement/build data and unvalidated slots — **SUPERSEDED** by S6D-07 schemas, bounded package seed/compiler and readiness conformance;
3. undeclared Activity parameter source contract — **SUPERSEDED** by S6D-05 parameter declaration/binding schemas and S6D-10 policy-basis freeze;
4. uneven portable values — **SUPERSEDED** by S6D-05 exact 19-value route catalog, with Signal/StateDelta deliberately dormant;
5. House-Rule Markdown as potential mechanic path — **SUPERSEDED** by S6D-10 accepted-input boundary;
6. stale CORE wording candidates — **STILL OPEN AS DOCUMENT-CONFORMANCE INPUT** for WP-06 only where it misstates current rules/adjudication routing; otherwise preserve a typed WP-26 obligation.

### Remaining WP-06 work — not yet discharged

1. complete the current Source Manifest across every admitted rules/domain package, execution catalog/schema and runtime consumer;
2. assign an architecture→machine route or explicit negative disposition to each supported domain path, including Procedure/event/receipt/segment and mutation/no-mutation consequences;
3. perform the machine→architecture reverse pass for current catalogs, schemas, package members and implicated CORE/domain modules;
4. identify only proven stale/duplicate/no-consumer surfaces, preserve later-documentation issues as typed forward obligations, and run the required adversarial/reconciliation checks.

No WP-07 substantive analysis has begun. No new primitive, selector, catalog member, schema protocol, runtime behavior or House-Rule capability was added by this checkpoint.

## Current continuation after checkpoint

```text
CURRENT_DOMAIN: WP-06
CURRENT_SLICE: supported domain-route inventory + CORE/domain reverse audit
NEXT_DOMAIN: WP-07
OWNER_GATE: NONE
```
