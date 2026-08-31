# R2.7 WP-08 — LLM Role, Context and Instruction Realization — Canonical Specification

Status: **CANONICALIZATION CHECKPOINT — PENDING MANDATORY SENIOR AUDIT**

Date: 2026-08-31

## 1. Authority and scope

This specification canonically allocates the implementation-facing realization of
already accepted R2.1–R2.6 and Step-4/5 role/context/instruction law. It is
additive: the cited owners retain their semantic authority.

It is derived from the completed WP-08 Step-1 brief, Step-2 evidence, Step-3
decision, Step-4 collaborative review, Step-5 candidate, Step-6 adversarial
review, Step-7 resolution and Step-8 canonicalization record.

This specification does **not** authorize code, schema, catalog, CORE, prompt,
test or runtime changes. It does not reopen WP-07, create a role/agent/provider/
memory/result-bus topology, or select an implementation plan.

## 2. Canonical realization allocation

### LAW WP-08-1 — ONE PRIMARY SHIPPED CONTAINMENT-TEXT OWNER

The R2.6 behavioural-containment rule SHALL have one primary
ordinary-gameplay text owner: `GAME/CORE/AI_REASONING.md`.

Its implemented text SHALL be equivalent to:

```text
Use only information eligible to the active role under the current RoleContextBundle and lawful typed handoffs.
Physical presence elsewhere in the conversation does not make information eligible.
When information later becomes lawfully eligible, use it normally; prior ineligibility is not permanent forgetting.
```

`GAME/CORE/PLAY_POLICY.md` owns immutable CORE cache and module activation, and
`GAME/CORE/RUNTIME.md` owns invocation/turn order. They may invoke or reference
this rule but SHALL NOT create a competing ordinary-gameplay wording or eligibility
rule. Project Instructions remain package/bootstrap only.

### LAW WP-08-2 — ROLE/CONTEXT CONTROL IS RUNTIME-LOCAL

`TurnEnvelope`, `RoleContextRequest`, registered
`ContextNeedProfile` identity, `RoleContextBundle`, `ContextTrace`, allowed
typed prior-result references and terminal/degradation outcomes are bounded,
ephemeral runtime-control contracts under R2.3/R2.4.

They SHALL NOT be made campaign, session, checkpoint, generic-memory, generic
catalog or schema authorities merely to simplify implementation. Context trace is
protected diagnostic material, not role evidence or player output. S6D
`MechanicalContext` remains a separately owned mechanical invocation scope and
is not a substitute for role context or eligibility.

### LAW WP-08-3 — REBIND, SOURCE ESCALATION AND ACTOR BOUNDARIES

Before every material logical phase, the runtime SHALL bind the R2.4 tuple:
role; applicable subject/recipient; purpose; registered profile; bundle/basis;
allowed typed prior results; accepted deterministic references; authority limits;
and result/output contract.

R2.1 applies within that binding: derived Story/history/current-chat material may
orient an eligible role, but a material claim SHALL escalate to its proper current,
exact, knowledge, disclosure or accepted-history owner. Physical presence never
widens eligibility. Hidden reasoning, prompt text, private diagnostics, abandoned
drafts and unaccepted generated candidates SHALL NOT become continuity evidence or
lawful handoff material.

An Actor phase SHALL bind an explicit transient R2.2 assessment purpose and use
only bounded eligible evidence/current state. The purpose binding creates no durable
Actor, knowledge or session write. Source-Actor-private continuity remains under
the R2.2 `world.actor.continuity` contract when its lifecycle admits persistence;
`world.knowledge` remains exclusive proposition-stance authority.

### LAW WP-08-4 — MINIMUM TYPED HANDOFF AND PROTECTED OUTPUT

A cross-phase handoff SHALL contain only an accepted instance of a registered R2.4
phase/result family, scoped by purpose, subject, recipient and generation. It SHALL
NOT carry a raw private bundle, role frame, hidden reasoning, unaccepted draft or
generic role-result bus.

Actor, Chronicler and Narrator remain distinct phases. Chronicler has no
same-envelope Story feedback into gameplay roles. Narrator SHALL freshly rebind
after Chronicler service and receive only its recipient-eligible bundle plus
lawful typed results. Only its validated result may proceed to Step-5.12
`EMISSION_COMMIT`; trace, debug, tool and maintenance surfaces are not secret
delivery paths.

### LAW WP-08-5 — FINITE, OBSERVABLE ASSURANCE

Future implementation/TDD and integrated MVP evaluation SHALL prove:

1. behavioural containment despite physical shared-chat presence, and lawful later
   use after eligibility is granted;
2. R2.1 proper-source escalation and exclusion of hidden/unaccepted material;
3. explicit bounded Actor-purpose assessment and the Actor-private versus
   `world.knowledge` boundary;
4. rebind before every material phase and rejection of raw-bundle/trace transport
   or MechanicalContext substitution;
5. fresh Narrator rebind, no same-envelope Story feedback and recipient-safe
   `EMISSION_COMMIT`;
6. finite degraded/`UNSATISFIABLE` paths that retain required evidence floors
   and neither guess, loop nor replay mechanics/RNG/canon;
7. one active instruction/activation route through `AI_REASONING.md` and
   `PLAY_POLICY.md`, without a competing owner.

Existing CORE-cache, contamination and S6D structural checks are supporting
regression evidence only; they do not by themselves discharge this behavioural
assurance.

## 3. Non-goals and implementation boundary

This canonicalization does not select runtime module names, provider APIs, token
budgets, prompt DSL, storage layout, durable representation, catalog additions,
test file names, migration, background worker or implementation sequence.
Those choices remain for a separately authorized implementation-planning unit and
must preserve the laws above.

## 4. Traceability

| WP-08 obligation | Canonical basis | This specification |
|---|---|---|
| F01 | R2.3 Context Runtime | WP-08-2, WP-08-3 |
| F02 | R2.4 TurnEnvelope/rebind | WP-08-2, WP-08-3, WP-08-4 |
| F03 / WP-07 F06 | R2.6 host assurance | WP-08-1, WP-08-5 |
| F04 | Step-4/5, R2.4, Step-5.10/5.12 | WP-08-4 |
| V01 | R2.1/R2.2/R2.3/R2.4/R2.6 | WP-08-5 |

## 5. Audit gate

This is a completed Step-8 canonicalization checkpoint and requires mandatory
Senior audit before WP-09 or implementation planning begins.
