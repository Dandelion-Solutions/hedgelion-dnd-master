## PO-013 — Complete local spell support with protected GAME responsiveness

Date: 2026-10-04  
Kind: SPELL COVERAGE / RUNTIME PERFORMANCE / ARCHITECTURE DIRECTION  
Status: ROUTED

### Product Owner clarification — VERBATIM / IMMUTABLE

```text
меня интересует только "производительность" - как эти все расчеты будут влиять на ход: на растянут ли они и без того медленный ответ LLM... Упрощать ради упрощения я не хочу. И да, изначально я хотел сделать мастера, который поможет погрузиться в мир DnD без этой хитроумной математики и знания тонн правил.

Ладно, где 6, там и 339. Какая разница когда их имплементировать. Что нужно чтобы сделать их поддержку с учетом YAGNI? Группы уже определены, можно взять это за основу...
```

### Product Owner architecture instruction — VERBATIM / IMMUTABLE

```text
я думаю надо сейчас потратить столько времени сколько потребуется (хоть целую неделю), что бы потом GAME работал быстро и ему не приходилось лезть в интернет за правилами и помощью! Единственное что я переживаю - не поздновато ли занялись архитектурой??? Уже производство началось! 

Как бы там ни было, займись сейчас проектированием архитектуры заклинаний - чтобы реализация позволила использовать их максимально эффективно.
```

### Agent-owned interpretation and routing

The Product Owner chooses accurate spell mechanics with hidden player-facing mathematics and protected runtime responsiveness, not rule simplification or a generic LLM mechanical fallback. The immediate authorization is architecture design. The bounded target corpus is the existing339-entry SRD5.2.1 inventory; non-SRD content, unrestricted homebrew, all class progression and arbitrary world simulation are not implied.

This is a content/admission extension over accepted Activity/native-owner execution, with production closure and shared capability gaps to establish. Do not reopen accepted state/durability/context owners without proven insufficiency. Ordinary spell resolution must use local admitted rules/supporting content and must not browse for rules or external help.

| Route | State | Obligation / trigger | Owner or current artifact |
|---|---|---|---|
| Spell architecture design | ACTIVE | direct design authorization; complete framing, evidence, candidate, reviews and final decision summary | `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/` |
| Exact content/consumer admission | DEFERRED | accepted spell specification and owner-local amendments; required closed dependency/failure/recovery proof | Activity/S6D-03..11/package owners;339-entry requirement map |
| Current P1A Sorcerer choice conflict | DISTINCT OPEN ROUTE | initial narrow-MVP recommendation is not chosen; reconcile real legal alternatives and selection semantics through the accepted owner/design route before revised P1A execution | S6D-07; current P1A Senior review; Wave-05 plan/cursor |
| Production implementation | DEFERRED | accepted architecture, implementation decomposition and required Senior plan GO; no production authority from this ledger | existing execution process and current global cursor |
| GAME latency and local rules closure | DEFERRED | realized supported target and meaningful benchmark/host acceptance; structural design is not measured latency | Activity Model; WP-24; Context/TurnRuntime/native storage owners |
| Non-SRD seed content | DEFERRED | provenance/contract reconciliation of existing Thunderclap seed entry; no automatic removal/replacement | admitted package/legal owners |

Existing P0/S1/S2 and independently eligible P2/P3 routes remain under their current dependency gates. Story/T07/T08/W06 are not activated by this direction. Final candidate acceptance remains pending; no new initial product-scope question is required merely to repeat this instruction.

Product Owner judgment remaining: review the concrete final architecture decision summary where the design exposes a material trade-off; no task-boundary reauthorization.

---
