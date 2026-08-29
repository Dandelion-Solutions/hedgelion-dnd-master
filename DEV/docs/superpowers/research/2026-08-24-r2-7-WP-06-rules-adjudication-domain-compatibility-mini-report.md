# R2.7 — WP-06 — Rules / adjudication / domain-module compatibility — мини-отчёт

Статус: **CLOSURE CANDIDATE — FINAL HOSTED VERIFICATION PENDING**

Дата: 2026-08-29

## Scope and evidence status

This report is the current post-S6D WP-06 record. The pre-pause state remains immutable historical evidence only:

```text
PRE_PAUSE_STATUS_BLOB_SHA: d486825dc5c9463b2e2159086e6c7102c3caf354
```

It is not a current cursor and is not reconstructed here. The prior in-file pre-S6D discovery text is superseded by this current report; its material incoming obligations are item-level reconciled below.

WP-06 has audited current accepted rules/adjudication/domain ownership against current machine/package/CORE consumers. It does not begin WP-07, invent a gameplay capability, or make runtime implementation work.

## Source Manifest delta

| Family | Current authority / machine evidence inspected |
|---|---|
| sequencing and prior obligations | R2.7 task brief/protocol/status, current roadmap, immutable pre-pause blob, WP-04/WP-05 reports |
| execution owners | Step-3 accepted boundary; `ACTIVITY_MODEL.md`, `RULE_ELEMENT_MODEL.md`, `ACTIVITY_PRIMITIVE_CONTRACTS.md`, WP-05 report |
| typed value / selector / context owners | `PORTABLE_ACTIVITY_VALUES.md`, `CALCULATION_SELECTOR_METADATA.md`, `MECHANICAL_CONTEXT.md`; portable-value, core, admission-ledger and mechanical-surfaces catalogs/schemas |
| post-pause rules closure | `CHARACTER_PROGRESSION_READY_PC_SEED.md`, `DOMAIN_RULES_COVERAGE.md`, `HOUSE_RULES_MECHANICAL_BOUNDARY.md`, `RULESET_PACKAGE_MACHINE_CLOSURE.md` |
| package and domain realization | the sole admitted `hdm.rules.dnd2024-srd52-core` manifest, character/gameplay/health seeds, resolved-lock/package closure, domain coverage and B′ binding |
| shipped consumers | `GAME/CORE/ADJUDICATION.md`, `RUNTIME.md`, `MECHANICS_INTEGRITY.md`, `RANDOMNESS.md`, `PLAY_POLICY.md`, `SOURCES.md`, and COMBAT/MAGIC/EXPLORATION/DIALOGUE/ENCOUNTERS/ADVANCEMENT/REWARDS |
| verification | S6D-05/07/09/10/11 focused contracts/validators, maintenance audit, all discovered `unittest` tests and hosted CI |

The source set is bounded by the current Project Map dependency route and expanded through actual package, catalog and CORE consumers; it is not inferred from the initial prompt list.

## Incoming-obligation reconciliation

### WP-04/F01 — character progression / READY_PC

| Required item | Disposition | Current evidence |
|---|---|---|
| advancement schema and stable choice IDs | **SATISFIED** | advancement and build-choice-slot schemas require owner-relative `choice_id`, bounded options/cardinality; S6D-07 package/compiler validates legal slots/options. |
| sparse Actor `choice_bindings` | **SATISFIED** | `world-actor-state.schema.json` holds selected option IDs and closed selection basis, rather than a flattened derived sheet. |
| progressive materialization | **EXTENDED** | provisional play is allowed only with local committed-dependency sufficiency; it remains the same Actor until readiness. |
| READY_PC initial mechanical frontier | **SATISFIED** | all material initial choices and dependencies must be closed/reconstructable; future advancement is not initial-build debt. |
| reconstructable Actor and no situational retrofit | **SATISFIED** | catalog → anchors/levels → grants/slots → bindings → admitted dependencies → derived readiness chain is explicit; post-exposure opportunistic initial selection is forbidden. |

**Verdict: WP-04/F01 = SATISFIED / EXTENDED BY S6D-07.** No WP-06 character surface is needed.

### WP-05/F01 — typed values and deterministic routing

| Item | Disposition | Current owner / realization |
|---|---|---|
| `target_spec`, `area_spec` | **SATISFIED** | S6D-05 embedded typed TargetSpec/AreaSpec; exact Activity consumers and bounded applicability facts. |
| `duration_spec` | **SATISFIED** | typed definition intent; concrete scheduled identity remains TemporalBinding-owned. |
| `cost_spec` | **SATISFIED** | declared embedded value; commit/reservation/refund remain primitive/Step-3 owned; no inferred generic cost primitive. |
| `roll_request` | **SATISFIED** | typed transient input consumed only by `op.roll`; RollResult is fixed retry/recovery evidence. |
| `signal`, `state_delta` | **SATISFIED** | explicit `EMBEDDED_NONOWNER / DORMANT_NONSELECTABLE`; neither creates an event bus nor a generic patch/mutation authority. |
| all material domain mechanics cross Step-3 | **EXTENDED** | finite S6D-09 coverage maps package/product/active-consumer sets; S6D-10 admits only bounded typed adjudicated inputs to an existing receiving surface. |

**Verdict: WP-05/F01 = SATISFIED / EXTENDED BY S6D-05/06/09/10.** Dormancy is an explicit negative disposition, not unfinished activation work.

## Architecture → machine audit

| Responsibility | Exact destination / disposition |
|---|---|
| action/check/save and procedure routes | Activity/ActionRequest → Step-3 Resolution or exact direct TransitionRequest; generic check/save retain event, receipt and segment evidence even when Mechanical-Null. |
| target/area/duration/cost/roll | closed embedded typed value roots; target selection is a bounded pre-commit calculation; actual mutation/RNG remain with their exact primitive/owner. |
| RNG | only `op.roll` owns generation; fixed results are retained by Resolution/Continuation and no retry rerolls. |
| mutations / no-mutation | active primitives or direct owner transitions produce exact owner changes; Mechanical-Null has zero authoritative mutation but genuine event/receipt where required. |
| selectors/calculations/context | current roster is exactly 10 selectors and 3 operations; all admitted selector inputs are `ENGINE_STATE`, permitted fact lists empty, dependency kinds closed. Only the seven exact `fiction.target_reachable` consumers may accept the bounded adjudicated fact. |
| character rules | owner-local stable slots and sparse bindings; deterministic/default/inherited/delegated precedence is closed before READY_PC and cannot be retrofitted from later fiction. |
| one-off ruling | GM may supply one declared bounded typed accepted input to an existing Activity/consumer. It cannot execute RNG, mutate canonical state, create another execution authority or force a permanent primitive. |
| recurring House Rule | policy adoption/currentness and realization refs remain separate from execution; prose never self-registers a primitive, selector or mutation. |
| domain coverage | every current package route is either exact direct transition, admitted Activity/primitive, bounded adjudication plus existing typed consequence, content/policy concern, or explicit unsupported space. |

No unusual player expression justified a new executable vocabulary. The strict six-part expansion test was not satisfied for any new surface.

## Domain-module routing dispositions

| Domain / consumer | Disposition |
|---|---|
| COMBAT | **SATISFIED** — active `runtime.procedure` owns timing/action/movement; attacks, saves, damage and effects use admitted Step-3 routes. |
| MAGIC | **SATISFIED** — natural wording may lower to existing capability or bounded adjudication; it does not grant spell/feature/cost/effect semantics. |
| EXPLORATION / hazards | **SATISFIED** — fiction may lower to generic check/save, existing movement or exact consequence; no generic spatial/pathfinding engine is introduced. |
| DIALOGUE / social | **SATISFIED** — obvious response remains fiction; uncertainty routes through adjudication and generic check/save without mind-control authority. |
| ENCOUNTERS | **SATISFIED** — framing has no independent mechanics authority; durable consequences use their natural owners. |
| ADVANCEMENT | **SATISFIED** — progression/choices route through the S6D-07 owner and READY_PC frontier. |
| REWARDS | **SATISFIED** — significant item ownership is `world.asset`; subjective identification is `world.knowledge`. |
| unsupported space | **OUT_OF_SCOPE / EXPLICIT NEGATIVE** — contest-specific resolution, generic reactions, broad defense/concentration/economy/crafting/teleportation/zones/entity creation and broad content corpora remain nonselectable. |

## Machine → architecture reverse audit

| Surface / finding | Disposition | Evidence-based outcome |
|---|---|---|
| 11 active Activity primitives; remaining primitive vocabulary | **SATISFIED / DORMANT** | only exact package consumers are active; dormant entries do not become capabilities by being named. |
| 10 active selectors / 3 active operations | **AUTO_RESOLVED** | current S6D-07 roster was valid, but `attack.roll + rule.grant_disadvantage` was still machine-allowed despite dormant ledger status. The pair was removed; the selector owner and focused check now match the ledger. |
| former S6D-03 focused test | **AUTO_RESOLVED** | it was plain-function style and absent from `unittest` discovery. It is now a discovered TestCase with current owner/pair/count assertions; hosted CI executes it. |
| portable `signal` / `state_delta` | **SATISFIED** | explicit dormant nonowner disposition; no semantic consumer may treat them as generic execution authority. |
| B′ domain-coverage binding | **SATISFIED** machine; **STALE_DEBT** prose | checked-in binding/schema/validator are current and complete, but two historical pre-realization lines in `DOMAIN_RULES_COVERAGE.md` still say it is not materialized/blocked. |
| CORE execution/policy wording | **SATISFIED** for current routing | no CORE module creates direct RNG/mutation/second execution authority. A narrow exploration wording conformance remains forward documentation work. |

The coverage artifact itself reports empty coverage-minus-required, required-minus-coverage, orphan-edge, unresolved-reference, duplicate-source and supported-gap sets. No current active machine surface lacks a semantic consumer/disposition.

## Typed forward obligations

| ID | Disposition | Owner / next handling |
|---|---|---|
| WP-06/F02 | **FORWARD_OBLIGATION** | WP-26 documentation conformance: remove the stale pre-realization B′ “not materialized / blocked” wording from `DOMAIN_RULES_COVERAGE.md`; current closure authority and machine binding remain controlling now. |
| WP-06/F03 | **FORWARD_OBLIGATION** | WP-26 documentation conformance: align `GAME/CORE/EXPLORATION.md` “spatial record/map” guidance with the current bounded location/procedure/applicability contract, without implying a new generalized spatial engine. |

These are wording/conformance debts, not current architectural blockers and not authorization for scope expansion.

## Final WP-06 candidate conclusion

```text
INCOMING_WP04_F01: SATISFIED / EXTENDED
INCOMING_WP05_F01: SATISFIED / EXTENDED
ARCHITECTURE_BLOCKERS: 0
OWNER_DECISIONS_REQUIRED: 0
NEW_EXECUTABLE_CAPABILITIES: 0
MACHINE_CONTRACT_CORRECTIONS: 1
FORWARD_OBLIGATIONS_CREATED: WP-06/F02, WP-06/F03
WP-07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```

The only current structural correction is mechanically implied by the accepted ledger: a dormant operation cannot remain an allowed executable selector pair. No product semantics, authority allocation, compatibility policy or scope change requires a human decision.

## Verification to complete closure

Before the audit cursor advances, publish this candidate, perform remote read-back, and require the applicable hosted workflow to pass. Then record WP-06 as closed and stop at the mandatory Senior review checkpoint before WP-07.
