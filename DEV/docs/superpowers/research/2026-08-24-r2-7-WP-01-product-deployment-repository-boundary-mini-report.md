# WP-01 — Product / deployment / repository boundary

Статус: **CLOSED**

Date: 2026-08-24

## 1. Краткий вывод

Архитектурный product/deployment baseline согласован и достаточно определён для дальнейшего аудита: MVP поддерживает ChatGPT Plus, ordinary Project-capable chat, один физический chat/context на игрока, High reasoning как рекомендацию, а не семантическую зависимость, и фиксированный repository transport `deterministic Python/core -> GitHub Connector -> non-force ref transition`.

`GAME/` концептуально и машинно отделён от `DEV/`: установленный runtime должен быть self-contained, release builder архивирует валидное содержимое `GAME/`, а DEV machine/contracts участвуют только в разработке/сборке/проверке и не являются runtime dependency.

Новых product/architecture trade-offs не обнаружено. Есть три implementation/documentation gaps, все однозначно следуют из уже принятых решений:

1. shipped bootstrap/Project Instructions используют слабые формулировки `default transport`, `do not ... first`, которые допускают неверное чтение как «после Connector можно попробовать fallback»;
2. user-facing `GAME/INSTALL/README.md` не заявляет ChatGPT Plus как поддерживаемый MVP plan, хотя R2.6 canonical это фиксирует;
3. общий routing «эксперименты/probes/prototypes -> private HDM Lab; public HDM -> sanitized durable conclusions» не находится в public `AGENTS.md`; правило существует в R2.6 для host probes и в private Lab, но general development-governance discoverability недостаточна.

Ни один gap не требует owner decision. Они превращаются в implementation/documentation/test obligations и forward obligations к профильным domains.

---

## 2. Покрытые вопросы

```text
WP-01/Q1 Supported MVP product profile consistent?          GAP (documentation realization only)
WP-01/Q2 GAME complete shipped runtime, no DEV dependency? SATISFIED at architecture/boundary level
WP-01/Q3 Public HDM vs private Lab responsibilities clear?  GAP (public governance discoverability)
WP-01/Q4 Forbidden transport fallbacks stated consistently? GAP (stale weak wording)
WP-01/Q5 Host assumptions classified correctly?             SATISFIED
```

### Q1

R2.6 canonical однозначно задаёт ChatGPT Plus / Project-capable ordinary chat / per-player own context. Runtime/install architecture этому не противоречит, но `INSTALL/README.md` сообщает только `ChatGPT Project`, не фиксируя Plus как supported MVP profile. Это deployment-documentation gap, не semantic conflict.

### Q2

`AGENTS.md`, GAME/DEV boundary design, `PLAY_POLICY.md` и release builder согласованы: GAME — shipped runtime tree; DEV — development-only; runtime не должен читать DEV. `release_builder.py` использует DEV metadata только на build-time для validation/coherence, что не создаёт runtime dependency.

Полный reverse package audit всё равно обязан пройти в WP-23/WP-26; текущий domain не делает из локального structural finding глобальный release-readiness claim.

### Q3

R2.6 canonical уже устанавливает: exploratory probes/prototype harnesses/raw transcripts/instrumentation belong in HDM Lab by default; public HDM получает sanitized/promoted conclusions/test obligations. Private Lab README подтверждает независимую laboratory роль и отсутствие production engine/campaign state.

Однако общий public development guard (`AGENTS.md`) не содержит discoverable rule, поэтому будущий agent может не получить правильный routing вне контекста R2.6. Это governance gap.

### Q4

Canonical owner decision запрещает не только fallback, но и саму попытку альтернативного transport path.

Текущие shipped mismatches:

```text
GAME/INSTALL/PROJECT_INSTRUCTIONS.txt
    "default transport"
    "Do not substitute ... first"

GAME/INSTALL/README.md embedded Project Instructions
    same text

GAME/INSTALL/00_DND_BOOTSTRAP.md
    "Do not try ... first"

GAME/CORE/BOOTSTRAP_RUNTIME.md
    "Do not first use ..."
```

Это stale realization. В отличие от них `PERSISTENCE.md`, `NEW_CAMPAIGN_FAST_PATH.md`, `RUNTIME.md` уже используют fixed/no-fallback semantics или fail safely.

### Q5

R2.6 canonical достаточно чётко делит:

```text
semantic correctness requirement
    observable behavioral containment
    deterministic authority/currentness
    fixed repository path

deployment prerequisite/profile
    ChatGPT Plus
    Project-capable ordinary chat
    required Connector capability

recommendation
    High reasoning when available

post-implementation acceptance
    Protocol-4-derived integrated behavioral/load/security evaluation
```

Exact model ID, exact cross-player reasoning equality, hidden cognitive isolation и exact hidden token capacity не становятся campaign semantics.

---

## 3. Source Manifest delta

Полный WP-01 source set и inspection statuses записаны в:

- `DEV/docs/superpowers/research/2026-08-24-r2-7-whole-project-source-manifest.md`

Ключевые owning/consumer sources:

| Source | Authority role | Inspection |
|---|---|---|
| R2.6 MVP host assurance canonical spec | CANONICAL / OWNING | current inspected |
| R2.6 fixed repository transport clarification | OWNER DECISION / SUPERSEDING | current inspected |
| GAME/DEV release boundary design + audit amendment | accepted boundary design/amendment | inspected |
| `AGENTS.md` | repository governance | current inspected |
| `GAME/CORE/PLAY_POLICY.md` | shipped runtime firewall | current inspected |
| `GAME/CORE/BOOTSTRAP_RUNTIME.md` | shipped bootstrap/runtime | current inspected |
| `GAME/INSTALL/00_DND_BOOTSTRAP.md` | shipped bootstrap | current inspected |
| `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` | shipped host instruction | current inspected |
| `GAME/INSTALL/README.md` | shipped install/user instruction | current inspected |
| `GAME/CORE/PERSISTENCE.md` | publication HOW owner | current inspected |
| `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` | new-campaign publication | current inspected |
| `GAME/CORE/RUNTIME.md` | runtime routing | current inspected |
| `GAME/CORE/ENGINE_UPDATES.md` | runtime distribution/update | current inspected |
| `DEV/TOOLS/release_builder.py` | development/release machine contract | relevant portion inspected |
| private Lab `README.md` | Lab boundary evidence | current inspected |

---

## 4. Установленные факты и ограничения

### WP01-F01 — supported host profile

**DECISION.** Supported MVP baseline = ChatGPT Plus + ordinary Project-capable chat + each human in own chat/context. High reasoning recommended, not required semantic identity.

### WP01-F02 — runtime distribution boundary

**DECISION / CONSTRAINT.** `GAME/` is exact shipped runtime source tree; `DEV/` must not become runtime correctness dependency.

### WP01-F03 — fixed repository transport

**OWNER DECISION.** Runtime repository path is fixed. Alternate remote transports are outside supported contract and MUST NOT be probed/fallen back to during play/setup/save/recovery/multiplayer.

### WP01-F04 — GitHub Actions is separate execution surface

**CONSTRAINT.** Release workflow may use its GitHub-hosted scoped execution environment. This exception does not authorize GitHub Actions as gameplay persistence bridge and does not relax interactive Connector-only policy.

### WP01-F05 — Lab/public research boundary

**DECISION / GOVERNANCE.** Raw experiments/prototypes/instrumentation belong in private Lab by default; public HDM receives independently rewritten, sanitized durable conclusions/specs/test obligations.

### WP01-F06 — implementation validation is downstream

**DECISION.** Integrated production-like host behavior is tested on implemented MVP; abstract pre-implementation recreation is not architecture gate.

---

## 5. Architecture -> machine

| Semantic responsibility | Accepted owner/source | Machine/runtime destination | Representation verdict | Status |
|---|---|---|---|---|
| Supported ChatGPT Plus profile | R2.6 canonical | `GAME/INSTALL/README.md` user prerequisite; host setup docs | INSTRUCTION/DOC ONLY | GAP: Plus omitted |
| One-context/per-player host topology | R2.6 + R2.4/R2.5 | Project Instructions + CORE role/context contracts | INSTRUCTION ONLY | OWNED; deeper audit WP-08 |
| Runtime package self-containment | GAME/DEV boundary + AGENTS | GAME tree + release builder + PLAY_POLICY | STRUCTURAL/RUNTIME CONTRACT | SATISFIED at boundary level |
| No DEV runtime dependency | GAME/DEV boundary | release builder validation + runtime firewall | STRUCTURAL NEGATIVE LAW | SATISFIED at boundary level; full reverse audit later |
| Fixed Connector transport | R2.6 transport clarification | `PERSISTENCE.md`, bootstrap, Project Instructions | INSTRUCTION + TOOL CONTRACT | PARTIAL GAP in bootstrap wording |
| Missing Connector capability | R2.6 transport clarification | runtime failure/degradation path | EPHEMERAL/ERROR RESULT | MAPPED; detailed failure audit WP-25 |
| Lab experiment routing | R2.6 canonical + project governance | development agent instructions/process | DEVELOPMENT INSTRUCTION ONLY | GAP: general AGENTS routing absent |
| Post-MVP Protocol-4 evaluation | R2.6 canonical | DEV test/evaluation catalog/release gate | POST-MVP EVALUATION ONLY | FORWARD WP-22 |

---

## 6. Machine -> architecture

| Existing surface | Current responsibility | Accepted owner | Classification | Action |
|---|---|---|---|---|
| `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` | host bootstrap + transport guard | R2.6 fixed transport + bootstrap contracts | STALE PARTIAL | strengthen absolute no-fallback wording |
| `GAME/INSTALL/README.md` | install prerequisites + PI copy | R2.6 profile + GAME/DEV install design | STALE PARTIAL | state Plus; keep PI exact parity after wording repair |
| `GAME/INSTALL/00_DND_BOOTSTRAP.md` | package/storage bootstrap | bootstrap + R2.6 fixed transport | STALE PARTIAL | remove `first` loophole |
| `GAME/CORE/BOOTSTRAP_RUNTIME.md` | runtime/bootstrap routing | bootstrap + R2.6 fixed transport | STALE PARTIAL | remove `first` loophole |
| `GAME/CORE/PERSISTENCE.md` | GitHub publication sequence | Step 5 + R2.6 fixed transport | OWNED | no WP-01 change |
| `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` | blank scaffold publication | accepted fast-path contract | OWNED | no fallback redesign |
| `GAME/CORE/PLAY_POLICY.md` | runtime/package firewall | GAME/DEV boundary | OWNED | preserve self-contained runtime law |
| `DEV/TOOLS/release_builder.py` | package composition/validation | GAME/DEV boundary/release design | IMPLEMENTATION-ONLY / OWNED | detailed release audit WP-23 |
| private Lab README | private research boundary | Lab governance | OWNED PRIVATE | no promotion/copy into public runtime |

---

## 7. Конфликты, stale surfaces и negative findings

### WP01-G01 — weak Connector wording

Observed:

```text
"default transport"
"do not ... first"
```

Material because fixed R2.6 owner law explicitly says alternate transport is not a degraded/fallback path and must not even be probed.

Disposition: **STALE_DEBT / IMPLEMENTATION_OBLIGATION**.

Blocking now: **NO** — canonical owner is unambiguous.

### WP01-G02 — Plus prerequisite omitted

`INSTALL/README.md` names ChatGPT Project but not ChatGPT Plus.

Disposition: **IMPLEMENTATION_OBLIGATION**.

Blocking now: **NO**.

### WP01-G03 — Lab routing not general in public AGENTS

Public repository search exposes no general `HDM Lab` routing rule in `AGENTS.md`; only R2.6-specific canonical text carries the rule.

Disposition: **STALE/GOVERNANCE DEBT**.

Blocking now: **NO**.

### Negative findings

- No evidence supports reopening transport selection.
- No evidence supports introducing provider abstraction.
- No evidence supports making exact model identity persistent campaign state.
- No evidence supports shipping DEV artifacts merely because implementation planning later needs them.
- No evidence supports using GitHub Actions as gameplay persistence fallback.

---

## 8. Автоматически принятые технические решения

### AUTO-01-01 — absolute Connector language

Replace all active shipped transport guards that say `default` / `first` with an absolute fixed-path rule equivalent to:

> Use the defined GitHub Connector path. Do not attempt or probe alternate Git transports. Missing required Connector capability is a supported-profile capability failure.

Why no owner gate: exact semantics already owner-approved in R2.6.

### AUTO-01-02 — Plus in install prerequisite

`GAME/INSTALL/README.md` must identify ChatGPT Plus as the supported MVP plan/profile. It need not be persisted into campaign state or repeated in every CORE module.

Why no owner gate: R2.6 canonical already fixes the plan.

### AUTO-01-03 — general Lab routing guard

Public `AGENTS.md` should gain a concise general rule: exploratory probes/prototypes/instrumentation requiring repository mutation belong in HDM Lab by default; public HDM receives reviewed/sanitized durable conclusions. Do not expose private provenance/source identities unnecessarily.

Why no owner gate: owner already established this repository-role contract; this is discoverability/guardrail realization.

### AUTO-01-04 — preserve execution-surface distinction

Do not "fix" release tooling's legitimate local/Actions Git usage merely because interactive runtime/development sessions are Connector-only. Execution-surface scope is material and already accepted.

---

## 9. Implementation obligations

### IMP-01-01 — fix active shipped transport wording

Targets:

- `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`;
- matching embedded block in `GAME/INSTALL/README.md`;
- `GAME/INSTALL/00_DND_BOOTSTRAP.md`;
- `GAME/CORE/BOOTSTRAP_RUNTIME.md`.

Acceptance: no wording implies that alternate Git transport may be tried after Connector failure.

### IMP-01-02 — state supported Plus profile

Target: `GAME/INSTALL/README.md` prerequisites/support statement.

Acceptance: supported MVP plan is explicit without turning model/plan identity into campaign state.

### IMP-01-03 — add Lab routing to public governance

Target: `AGENTS.md` development/research governance.

Acceptance: experiment/probe/prototype/instrumentation path is discoverable before repository mutation; no public disclosure of sensitive/private provenance required.

---

## 10. Verification / MVP acceptance obligations

### VER-01-01 — forbidden transport regression

Class: `unit / static contract / scenario`.

Assert active runtime/install instructions do not contain fallback-semantics equivalent to:

```text
try Connector first, then git/gh/direct API
Connector is merely default/preferred
```

### VER-01-02 — Project Instructions parity

Class: `release/static contract`.

Existing parity check between `INSTALL/README.md` embedded block and `PROJECT_INSTRUCTIONS.txt` must continue to pass after wording changes.

### VER-01-03 — runtime package independence

Class: `release/package integration`.

Discharge in WP-23: built runtime must operate from GAME/package-root contents without DEV runtime dependency.

### VER-01-04 — fixed Connector failure behavior

Class: `integration / MVP acceptance`.

Discharge in WP-25/WP-22: missing/denied/failing Connector capability must block/degrade safely without alternate transport probing.

---

## 11. Forward obligations

### WP-01/F01 -> WP-08

Exact obligation: map the absolute fixed-Connector instruction into the final Project Instructions / CORE instruction architecture without duplicated conflicting owners.

Blocking relation: `NON_BLOCKING_CURRENT`, `BLOCKS_FINAL_CLOSURE`.

### WP-01/F02 -> WP-19

Exact obligation: verify/finalize bootstrap/new-campaign surfaces so `00_DND_BOOTSTRAP.md` and `BOOTSTRAP_RUNTIME.md` contain no alternate-transport loophole.

Blocking relation: `NON_BLOCKING_CURRENT`, `BLOCKS_FINAL_CLOSURE`.

### WP-01/F03 -> WP-22

Exact obligation: define static/integration regression coverage for absolute no-fallback semantics and preserve Project Instructions parity.

Blocking relation: `NON_BLOCKING_CURRENT`, `BLOCKS_FINAL_CLOSURE`.

### WP-01/F04 -> WP-23

Exact obligation: complete reverse release/package proof that the built runtime is self-contained under GAME and has no DEV correctness dependency; verify Plus/install support presentation where release readiness covers user prerequisites.

Blocking relation: `NON_BLOCKING_CURRENT`, `BLOCKS_FINAL_CLOSURE`.

### WP-01/F05 -> WP-25

Exact obligation: verify capability-denied/missing Connector error semantics are finite, explicit and never activate alternate transport probing.

Blocking relation: `NON_BLOCKING_CURRENT`, `BLOCKS_FINAL_CLOSURE`.

### WP-01/F06 -> WP-26

Exact obligation: repair public governance/document routing: add general experiment->Lab rule to `AGENTS.md`; identify all active stale `default/first` transport wording; preserve historical text where it is genuinely historical rather than current instruction.

Blocking relation: `NON_BLOCKING_CURRENT`, `BLOCKS_FINAL_CLOSURE`.

---

## 12. Round-2 Diamond / Strong delta

`NO DELTA`.

R2.6 S53 remains resolved as capability/behavior envelope; D15 remains dormant; no dormant candidate is activated by WP-01.

---

## 13. Human decision

```text
NONE
```

Все material findings однозначно следуют из уже принятых owner decisions и не создают новой viable architecture alternative.

---

## 14. Closure verdict

```text
DOMAIN: WP-01
VERDICT: CLOSED
UNRESOLVED_ARCHITECTURE_BLOCKERS: 0
OWNER_GATE: NONE
FORWARD_OBLIGATIONS: 6
NEXT_DOMAIN: WP-02
```

WP-01 закрывается **с implementation/documentation/test obligations**, а не с утверждением, что текущий runtime уже исправлен. R2.7 implementation gate остаётся закрыт.

---

## 15. Точка продолжения

Перейти автоматически к `WP-02 — Global authority / duplicate-owner audit`.

Recovery route:

```text
R2.7 audit-status
-> this WP-01 report only if predecessor context is needed
-> whole-project Source Manifest
-> WP-02 scope questions
-> canonical Round-1 authority/ownership sources
-> later amendments/Round-2 owners
-> current GAME/DEV machine/state surfaces
```