# R2.7 — WP-05 — Deterministic execution / resolution / RNG / retry — мини-отчёт

Статус: **CLOSED — READ-BACK VERIFICATION REQUIRED BEFORE CURSOR ADVANCE**

Дата: 2026-08-24

## Краткий вывод

WP-05 свёл принятый Step-3 deterministic execution contract к одной machine-realization модели без новых semantic owners и без replay принятой механики.

Итоговый execution graph:

```text
Interaction
    -> IntentPlan
        -> IntentClause
            -> RuntimeCommand
                -> ActionRequest
                    -> Resolution(Activity)
                        -> ExecutionSegment[]
                        -> MechanicalEvent[]
                        -> Continuation? / child Resolution[]
                OR
                -> TransitionRequest
                    -> direct ExecutionSegment[] when commit occurred
                    -> embedded direct-transition receipt
```

`runtime.command`, `runtime.procedure`, `runtime.resolution`, `runtime.continuation`, `runtime.mechanical_event`, `runtime.interaction`, `runtime.intent_plan` и `runtime.resolution_trace` остаются самостоятельными владельцами ровно своих принятых lifetime/authority responsibilities.

`ExecutionSegment`, receipt, `ActionRequest`, `TransitionRequest`, `ChoiceRequest`, `ReactionOffer`, RNG result, pending-child descriptor, invocation fact и boundary occurrence остаются embedded typed values; отдельные `runtime.execution_segment`, `runtime.receipt` или `runtime.resolution_chain` не вводятся.

Architecture blockers: **0**.

Human decision: **NONE**.

---

## Покрытые вопросы

1. Полная цепочка `Interaction -> IntentPlan -> RuntimeCommand -> Resolution/direct transition -> segment -> events/receipt -> mutation`.
2. Independent owner boundaries и embedded-only values.
3. Concrete actor/source/target/parameter bindings.
4. Accepted catalog context / invocation facts / input fingerprint.
5. Fixed RNG identity и retry/resume reuse.
6. Continuation portability и safe recompute boundary.
7. Mandatory child/firing identity и root-command closure.
8. Direct-transition success, post-commit pending child и pre-commit typed failure.
9. Diagnostic ResolutionTrace vs current-state authority.
10. No-mechanics-replay composition с R2.4.
11. CORE conformance: `RUNTIME.md`, `MECHANICS_INTEGRITY.md`, `RANDOMNESS.md`.
12. Registered execution protocol values и downstream ownership.
13. Runtime-latency/smoothness consequence: safety evidence должно возникать внутри локального execution edge, а не как дополнительный сетевой verification phase.

---

## Source Manifest delta

Owning / canonical:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`;
- `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md` — no-mechanics-replay / accepted-frontier laws;
- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`;
- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`;
- `DEV/CATALOG/core-catalog.json`.

Current machine contracts inspected/changed:

- `DEV/SCHEMAS/action-request.schema.json`;
- `DEV/SCHEMAS/transition-request.schema.json`;
- `DEV/SCHEMAS/roll-result.schema.json`;
- `DEV/SCHEMAS/choice-request.schema.json`;
- `DEV/SCHEMAS/reaction-offer.schema.json`;
- `DEV/SCHEMAS/runtime-interaction-state.schema.json`;
- `DEV/SCHEMAS/runtime-intent-plan-state.schema.json`;
- `DEV/SCHEMAS/runtime-command-state.schema.json`;
- `DEV/SCHEMAS/runtime-procedure-state.schema.json`;
- `DEV/SCHEMAS/runtime-resolution-state.schema.json`;
- `DEV/SCHEMAS/runtime-continuation-state.schema.json`;
- `DEV/SCHEMAS/runtime-mechanical-event-state.schema.json`;
- `DEV/SCHEMAS/runtime-resolution-trace-state.schema.json`;
- `DEV/SCHEMAS/execution-segment.schema.json`;
- `DEV/SCHEMAS/resolution-receipt.schema.json`;
- `DEV/SCHEMAS/pending-child-invocation.schema.json`;
- `DEV/SCHEMAS/invocation-fact.schema.json`;
- `DEV/SCHEMAS/boundary-occurrence.schema.json`;
- `DEV/SCHEMAS/intent-clause.schema.json`.

Current CORE consumers:

- `GAME/CORE/RUNTIME.md`;
- `GAME/CORE/MECHANICS_INTEGRITY.md`;
- `GAME/CORE/RANDOMNESS.md`.

Regression/conformance consumers:

- `DEV/TESTS/test_r2_7_wp05_execution_conformance.py`;
- `DEV/TESTS/test_step3_command_intent_contract.py`;
- `DEV/TESTS/test_step3_execution_owner_contract.py`;
- `DEV/TESTS/test_step3_execution_examples.py`;
- `DEV/TESTS/test_step3_execution_value_schemas.py`;
- `DEV/TESTS/test_step3_event_followup_contract.py`;
- `DEV/TESTS/test_step3_resume_ordering_contract.py`;
- `DEV/TESTS/test_step3_execution_catalog_contract.py`.

Historical machine plan was used only to locate old consumers; it does not override the canonical Step-3 spec.

---

## Установленные факты

### F1 — RuntimeCommand остаётся root closure owner

RuntimeCommand владеет accepted executable-clause identity/fingerprint, accepted context/input, root execution linkage и mandatory descendant closure disposition. Он не копирует detailed Resolution/Procedure state.

### F2 — Resolution = ровно один Activity invocation

Resolution хранит concrete invocation bindings:

```text
activity_id
actor_id
source_id?
target_ids[]?
parameter_bindings?
```

а также accepted catalog context, invocation facts, cursor/safe phase, fixed RNG, prior exports, children, segments и Continuation/trace refs.

### F3 — ExecutionSegment не является record class

Segment identity определяется owning execution + local sequence. Его embedded contract теперь содержит минимально достаточную immutable receipt evidence:

```text
segment_sequence
commit_state = committed
resulting_execution_state
event_ids[]
pending_child_invocations[]
receipt_exports
affected_revision_refs[]
continuation_id?
```

Он не хранит world snapshot и не получает independent lifecycle.

### F4 — Receipt также не становится record class

`value.resolution_receipt` является immutable observable result/evidence. Для action-backed execution текущая execution state остаётся у Resolution; direct transition может хранить embedded receipt на Command.

### F5 — Direct transition различает три случая

1. accepted, ещё не committed — segment/receipt могут отсутствовать;
2. committed и/или имеет post-commit mandatory child — committed segment evidence + receipt обязательны;
3. terminal typed failure до первого commit — receipt обязателен, fake segment запрещён.

### F6 — Fixed RNG является execution history

RNG результат получил typed identity (`roll_id`, expression, raw values, source/provenance where applicable). Уже committed fixed RNG переносится Resolution/Continuation и не reroll-ится при retry/resume.

### F7 — Continuation переносит irreducible historical inputs, а не derived snapshots

Continuation сохраняет accepted context/bindings/facts/fixed RNG/prior exports/committed segment refs/dependency frontier/pending choice-or-reaction/future RNG frontier и safe recompute position. Procedure ResourceState, MechanicalContext, Temporal Agenda, condition indexes, DAG cache и trusted prospective deltas туда не копируются.

### F8 — Pending human response получил portable typed contract

`ChoiceRequest` и `ReactionOffer` теперь отдельные embedded schemas и могут быть сохранены внутри Continuation без создания independent record class.

### F9 — Typed failure evidence не теряется

Resolution/receipt machine contracts требуют registered `failure_code` для material typed failure states, где он необходим. Direct transition может сохранить typed failure receipt без фиктивного committed edge.

### F10 — MechanicalEvents остаются immutable evidence, не current-state owner

Current Actor/Asset/Effect/Procedure owners остаются authoritative current state. Event/receipt/trace обеспечивают causality, retry/audit/reconstruction evidence.

### F11 — R2.4 no-replay law совместим с Step-3 correction behavior

После accepted mechanics/RNG Narrator/Chronicler/presentation failure не может повторно выполнить механику. Если же ранее была только narration без действительного mechanical acceptance, `MECHANICS_INTEGRITY.md` может вернуться к последнему реально valid mechanical frontier; это не replay принятой механики.

### F12 — Smoothness / latency boundary

Нормальный игровой ход не должен превращаться в `verify -> execute -> network verify -> narrate`.

Execution safety должна использовать уже загруженный HOT/SQLite state и локальные typed checks/atomic segment commit. Дополнительный GitHub/network read, broad integrity scan, отдельный LLM adjudication pass или repository publication допускается только при конкретном slow-path trigger: missing required source, stale shared state, durability edge, integrity suspicion, recovery/conflict и т.п.

Existing `RUNTIME.md` и `MECHANICS_INTEGRITY.md` уже требуют bounded/local fast path; WP-24 обязан проверить, что окончательная physical realization это не нарушает.

---

## Architecture -> machine

| Accepted responsibility | Machine destination | Disposition |
|---|---|---|
| Interaction | `runtime-interaction-state.schema.json` | SATISFIED |
| IntentPlan / IntentClause | `runtime-intent-plan-state.schema.json` + `intent-clause.schema.json` | SATISFIED |
| RuntimeCommand | `runtime-command-state.schema.json` | SATISFIED |
| ActionRequest | `action-request.schema.json` embedded | SATISFIED |
| TransitionRequest | `transition-request.schema.json` embedded | SATISFIED |
| Procedure | `runtime-procedure-state.schema.json` | SATISFIED |
| Resolution | `runtime-resolution-state.schema.json` | SATISFIED |
| ExecutionSegment | `execution-segment.schema.json` embedded under Resolution/Command | SATISFIED |
| MechanicalEvent | `runtime-mechanical-event-state.schema.json` | SATISFIED |
| ResolutionTrace | `runtime-resolution-trace-state.schema.json` | SATISFIED |
| Continuation | `runtime-continuation-state.schema.json` | SATISFIED |
| ChoiceRequest / ReactionOffer | embedded schemas referenced by Continuation | SATISFIED |
| fixed RNG result | `roll-result.schema.json`, reused by Resolution/Continuation | SATISFIED |
| pending mandatory child | `pending-child-invocation.schema.json` embedded | SATISFIED |
| invocation fact | `invocation-fact.schema.json` | SATISFIED |
| BoundaryOccurrence | `boundary-occurrence.schema.json` | SATISFIED |
| receipt | `resolution-receipt.schema.json` embedded/protocol | SATISFIED |
| no mechanics replay | R2.4 law + owner-local accepted execution evidence | SATISFIED AT ARCHITECTURE LEVEL |

`value.runtime_command` is treated only as an optional serialized/transport view of the authoritative `runtime.command`; it has **NO INDEPENDENT AUTHORITY / NO INDEPENDENT LIFECYCLE** and does not require another persistent owner.

---

## Machine -> architecture

No admitted Step-3 machine surface now requires a new semantic owner.

Explicit negative dispositions:

```text
runtime.execution_segment  -> NOT ADMITTED
runtime.receipt            -> NOT ADMITTED
runtime.resolution_chain   -> NOT ADMITTED
receipt_ref as record ref  -> RETIRED
committed_receipt_refs     -> RETIRED
scalar/untyped fixed RNG   -> RETIRED
Procedure state copy in Resolution/Continuation -> FORBIDDEN
world snapshot in receipt/segment -> FORBIDDEN
```

`ResolutionTrace` remains diagnostic/audit evidence only.

---

## Конфликты / stale / negative findings

### S1 — старые receipt-record-like refs

Old machine fixtures/schemas used `receipt_ref` / `committed_receipt_refs` without an admitted receipt record lifecycle. Replaced by owner-local embedded segments/receipts and stable segment refs.

Disposition: **AUTO_RESOLVED**.

### S2 — incomplete Resolution/Continuation invocation snapshot

Older schemas omitted actor/source/target/parameter bindings required for deterministic resume.

Disposition: **AUTO_RESOLVED**.

### S3 — scalar RNG

Older fixtures stored fixed RNG as bare numbers, insufficient to distinguish several generated rolls safely.

Disposition: **AUTO_RESOLVED**.

### S4 — direct-transition crash window

Old shape allowed a post-commit mandatory child to survive while committed root transition evidence was absent.

Disposition: **AUTO_RESOLVED**.

### S5 — typed pre-commit transition failure

Old shape required committed segment evidence for every settled transition, making honest pre-commit typed failure awkward/impossible.

Disposition: **AUTO_RESOLVED** through embedded direct-transition receipt.

### S6 — CORE RNG wording is under-specified for suspended execution

`RANDOMNESS.md` correctly says not to Git-persist every trivial roll and favors compact in-memory traces, but suspended/recovery-relevant fixed RNG must follow Resolution/Continuation durability when required by Step 3/5.2. This is a wording/mapping obligation, not a requirement to add Git writes to every ordinary roll.

Disposition: **FORWARD_OBLIGATION -> WP-14/WP-26**.

### S7 — registered transient protocol values are not all durable schemas

`target_spec`, `area_spec`, `duration_spec`, `cost_spec`, `roll_request`, `signal`, `state_delta` are rule/kernel typed values whose exact operation semantics belong to WP-06. Their absence as durable records is correct. `contribution` belongs to WP-17. `publication_manifest` belongs to WP-13. `validation_issue` belongs to WP-21/WP-25.

Disposition: **TYPED FORWARD OWNERSHIP; NO NEW RECORD CLASS**.

---

## Автоматически принятые технические решения

1. Сохранить Segment/receipt embedded, не создавать новые runtime classes.
2. Хранить committed segments у actual execution owner: Resolution для action, Command для direct transition.
3. Typed direct-transition receipt хранится на Command и допускает pre-commit failure without fake segment.
4. Fixed RNG представлен typed raw-result values с stable roll identity.
5. Concrete bindings дублируются в Resolution/Continuation только как irreducible accepted invocation input, а не как второй world-state owner.
6. Choice/Reaction portable payload materialized as embedded schemas.
7. Failure reason сохраняется typed, а не выводится из prose/trace.
8. `value.runtime_command` не является новым owner; это implementation/transport view only.
9. Normal-turn correctness checks должны оставаться local/bounded; network/repository/extra-LLM checks — conditional slow path only.

---

## Implementation obligations

- Реализовать deterministic binder/command acceptance/idempotency lookup before rebinding.
- Реализовать one local atomic ExecutionSegment commit kernel.
- Реализовать stable segment/event/firing identities.
- Реализовать fixed RNG capture/reuse и future RNG continuation state.
- Реализовать single-consume Continuation generation и stale-generation failure.
- Реализовать expected-reaction-child re-pin/recompute без rollback accepted parent history.
- Реализовать command root closure с mandatory descendant obligations.
- Не делать ResolutionTrace/current narration частью mechanical authority.
- Не добавлять сетевой/repository round-trip в normal execution path только ради дублирующей verification.

---

## Verification / MVP acceptance obligations

WP-22 должен реально исполнить schema/unit/integration suite и включить как минимум:

- schema examples/registry validation;
- exact retry returns same outcome;
- same identity + different fingerprint -> idempotency conflict;
- fixed RNG never rerolls on retry/resume;
- stale Continuation generation does not execute;
- mandatory child survives crash boundary;
- direct transition pre-commit failure creates no fake segment;
- post-commit transition with child cannot lose root segment evidence;
- expected reaction child changes frontier without parent rollback;
- Narrator/Chronicler failure after acceptance cannot replay mechanics;
- ResolutionTrace compaction cannot destroy required live execution evidence;
- no forbidden `runtime.receipt` / `runtime.execution_segment` class reintroduction.

Current repository state has source-level conformance tests, but **no fresh executable CI run is claimed for this branch**. The available Connector surface does not provide a new workflow-dispatch operation for this branch; executable verification remains WP-22 work.

---

## Forward obligations

| ID | Target | Exact obligation | Blocking final closure |
|---|---|---|---|
| WP-05/F01 | WP-06 | finalize `target_spec`, `area_spec`, `duration_spec`, `cost_spec`, `roll_request`, `signal`, `state_delta` semantics/interfaces and prove all gameplay domain modules route material mechanics through Step-3 execution | YES |
| WP-05/F02 | WP-10 | assign final durable/native record families/roots for recovery-relevant execution owners; no receipt/segment standalone family | YES |
| WP-05/F03 | WP-11 | finalize identities/routing for Interaction/Command/Resolution/Continuation/Event and segment/event/firing derived identities | YES |
| WP-05/F04 | WP-12 | map execution owners/segments/RNG/dirty state to HOT/SQLite and atomic transaction boundaries | YES |
| WP-05/F05 | WP-13 | map accepted execution frontier to durability/SAVE/publication without commit-every-turn behavior | YES |
| WP-05/F06 | WP-14 | prove cold recovery of active execution, fixed RNG, Continuation and committed segment frontier with no accepted-mechanics replay; reconcile `RANDOMNESS.md` wording | YES |
| WP-05/F07 | WP-15 | integrate BoundaryOccurrence, temporal due work and mandatory child/firing identity with chronology/Agenda without generic scheduler authority | YES |
| WP-05/F08 | WP-16 | bind authenticated participant/session/live currentness into Interaction/execution without transport order or stale live state becoming mechanics authority | YES |
| WP-05/F09 | WP-22 | execute/extend WP-05 deterministic/schema/retry/RNG/no-replay regression and add new schemas to global maintenance audit | YES |
| WP-05/F10 | WP-24 | prove normal-turn execution checks are bounded/local and do not introduce unnecessary GitHub/network/extra-LLM round-trips; quantify slow-path triggers/costs | YES |
| WP-05/F11 | WP-25 | reconcile execution failure codes with whole-project error/degradation taxonomy and finite failure behavior | YES |
| WP-05/F12 | WP-26 | align CORE prose with fixed-RNG suspension/recovery and final deterministic execution terminology without creating verbose per-turn trace requirements | YES |
| WP-05/F13 | WP-17 | materialize `value.contribution` only inside collaboration owner contract; do not route ordinary gameplay response through generic contribution queue | YES |
| WP-05/F14 | WP-13 | materialize `value.publication_manifest` under publication contract, not deterministic execution authority | YES |
| WP-05/F15 | WP-21/WP-25 | assign `value.validation_issue` to diagnostics/error surfaces without gameplay authority | YES |

Discharge:

- `WP-03/F02` -> **DISCHARGED BY WP-05**: deterministic execution record/protocol vocabulary now has concrete machine destinations or explicit downstream typed ownership/no-record dispositions.

---

## Round-2 Diamond / Strong delta

No new Round-2 item is activated by WP-05.

Relevant inherited composition:

- D17 (`LLM intent; deterministic mechanics`) remains satisfied and gains exact machine execution mapping;
- R2.4 no-mechanics-replay laws are preserved;
- no new provider/worker/background execution architecture is introduced.

---

## Human decision

`NONE`.

No residual product-semantic, authority, compatibility, risk-acceptance or material architecture trade-off remains inside WP-05.

---

## Closure verdict

```text
WP-05 VERDICT: CLOSED SUBJECT TO FRESH READ-BACK
ARCHITECTURE_BLOCKERS: 0
OWNER_GATE: NONE
STEP3_OWNER_GRAPH: MACHINE-MAPPED
FIXED_RNG/RETRY: MACHINE-MAPPED
NO_MECHANICS_REPLAY: PRESERVED
RUNTIME_SMOOTHNESS: EXPLICIT DOWNSTREAM PERFORMANCE INVARIANT
EXECUTABLE CI CLAIM: NOT MADE; WP-22 REQUIRED
```

## Точка продолжения

После fresh read-back этого mini-report и ключевых schemas/tests:

```text
LAST_CLOSED_DOMAIN: WP-05
CURRENT_DOMAIN: WP-06
CURRENT_DOMAIN_TOPIC: Rules / adjudication / domain-module compatibility
CURRENT_SLICE: owning rule-domain graph + CORE/domain reverse audit
NEXT_DOMAIN: WP-07
OWNER_GATE: NONE
```
