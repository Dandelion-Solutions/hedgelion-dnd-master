# R2.7 WP-08 — LLM Role, Context and Instruction Architecture — mini-report

## Статус

**IN_PROGRESS — STEP 2 EVIDENCE EXTRACTION**

Глобальная авторизация и точный gate: `DEV/CURRENT_PROGRESS.md`.
Этот mini-report является task-local evidence/cursor artifact WP-08 и не заменяет
global current-progress authority.

## Краткий вывод

Принятая архитектура не требует нового владельца, отдельного агента, второго
физического LLM context, persistent role memory или новой canonical specification.
Первичные canonical owners совместимы с текущими CORE/package instruction surfaces,
но текущая evidence выборка ещё не доказывает machine realization R2.3/R2.4/R2.6.
Главная остающаяся работа Step 2 — полный reverse audit actual runtime/catalog/test
consumer graph и точное mapping WP-07/F06.

## Покрытые вопросы

- шесть logical roles, one-context rebind, typed-handoff и Narrator fencing;
- R2.1 source escalation/eligibility and no-hidden-reasoning continuity boundary;
- R2.2 Actor purpose, source-Actor-private continuity and `world.knowledge` boundary;
- R2.3 request/profile/discovery/packet/bundle/trace/outcome constraints;
- R2.4 TurnEnvelope, instruction hierarchy, fresh Narrator rebind and finite fallback;
- R2.5 recipient/catch-up/planning containment;
- R2.6 behavioral containment, lawful later uptake and explicit-instruction obligation;
- current package/bootstrap, CORE activation and selected schema/test surfaces.

## Source Manifest delta

Primary-owner evidence is recorded in:

- `DEV/docs/superpowers/research/2026-08-31-r2-7-WP-08-step-2-canonical-owner-evidence.md`;
- `DEV/docs/superpowers/research/2026-08-31-r2-7-WP-08-step-2-current-surfaces-evidence.md`.

Those artifacts list the exact canonical and current paths read. No historical
derivation document was used as a substitute for its current primary owner.

## Установленные факты

1. The Step-4 amendment, R2.3, R2.4 and R2.6 preserve one physical context with
   strict logical eligibility; physical presence never grants use.
2. R2.1 and R2.2 constrain context selection and Actor use without creating a
   new continuity/cognition authority.
3. Full CORE preload, semantic activation and role-local evidence are distinct.
4. Current `PLAY_POLICY.md`/`CORE_INDEX.md` already define full-CORE cache and
   header-driven activation; current operational prose is compatible with, but
   does not itself realize, R2.3/R2.4 contracts.
5. The inspected persistent schemas do not silently own durable role frames,
   complete private bundles or hidden reasoning.
6. WP-07 remains closed. F06 is a carried `IMPLEMENTATION_OBLIGATION`, not
   authority to change runtime/schema/catalog now.

## Architecture -> machine

| Accepted responsibility | Current evidence disposition |
|---|---|
| R2.3 RoleContextRequest/profile/bundle/trace/outcomes | required exact machine mapping not yet established |
| R2.4 TurnEnvelope/registered phases/rebind/minimum transport | required exact machine mapping not yet established |
| R2.6 explicit active-role eligibility/lawful-later-use instruction | WP-07/F06 carry-in; exact owner/wording/test route not yet established |
| CORE cache and module activation | partial supporting surface exists |
| Narrator/EMISSION_COMMIT/disclosure | adjacent owners established; current concrete route not yet reconciled |

## Machine -> architecture

| Current surface family | Classification |
|---|---|
| Project Instructions/bootstrap exact package selection | bootstrap boundary; no role authority |
| PLAY_POLICY/CORE_INDEX full cache and activation | compatible supporting mechanism; not role-context authority |
| AI_REASONING/INFORMATION/NPC/NARRATIVE/MULTIPLAYER | compatible operational guidance; mapping incomplete |
| current/session/player/checkpoint/live schemas | no generic durable role/context owner found in inspected set |
| runtime-* schemas and S6D mechanical context contract | candidate/implementation-only surfaces pending exact owner mapping |
| existing context/contamination tests | partial regression evidence; R2.6/role-handoff verification remains open |

## Конфликты / stale / negative findings

- No material contradiction requiring WP-07 reopening was found.
- No accepted source authorizes a second prompt/agent/memory subsystem.
- No current selected source is accepted as a persistent hidden-reasoning or
  generic RoleContext authority.
- A focused evidence set cannot establish repository-wide absence; remaining
  concrete consumer/reference reconciliation is required.

## Автоматически принятые технические решения

- Treat CORE cache, semantic activation and role-local evidence as three
  separate layers.
- Keep all unknown concrete mappings as obligations rather than inferring new
  authority or durable state.
- Keep F06 under existing R2.6/R2.7 owners; do not modify WP-07 artifacts.

## Implementation obligations

- `WP-08/F01`: map R2.3 request/profile/discovery/closure/bundle/trace/result
  responsibilities to exact machine destinations or explicit no-representation
  decisions.
- `WP-08/F02`: map R2.4 TurnEnvelope, registered phases, rebind and minimum
  typed transport to exact runtime/instruction destinations.
- `WP-08/F03`: discharge WP-07/F06 through the R2.6 active-role,
  RoleContextBundle and lawful-handoff instruction route.
- `WP-08/F04`: map protected Narrator/Chronicler/output boundaries without
  converting Story, trace or private drafts into evidence.

## Verification / MVP acceptance obligations

- prove behavioral containment and lawful later uptake;
- prove fresh Narrator rebind and no raw private handoff;
- prove no same-envelope Story feedback;
- prove recipient/catch-up/planning containment;
- prove bounded/degraded/UNSATISFIABLE paths and no hidden-reasoning dependency.

## Forward obligations

None is created yet. Candidate findings remain inside WP-08 until exact current
machine consumers are reconciled.

## Human decision

**NONE.** No product semantics, authority change, compatibility policy, risk
acceptance or scope choice is currently exposed.

## Closure verdict

**NOT READY FOR STEP 3.** Step 2 is incomplete.

## Точка продолжения

Read the actual runtime/catalog/test consumer graph at the current published ref.
Classify every material surface against `WP-08/F01`–`F04` as satisfied,
implementation obligation, verification obligation, stale debt, no-delta or
contradiction. Then publish the completed Step-2 reconciliation and proceed to
Step 3 without reopening WP-07.
