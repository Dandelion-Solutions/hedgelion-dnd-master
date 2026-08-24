# R2.4 Evidence Ledger — Single-Context LLM Execution & Instruction Architecture

Status: **RESEARCH EVIDENCE / PRE-DECISION SYNTHESIS**

Date: 2026-08-24

Task brief:

- `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-task-brief.md`

This ledger preserves owning constraints, empirical evidence, research-candidate qualifiers and current synthesis before an owner decision.

---

## 1. Source Manifest completion

For the baseline R2.4 decision, the following source set has been inspected to task depth:

| Source family | Authority role | Status |
|---|---|---|
| current roadmap/task brief | sequencing/scope | exhausted-for-current-decision |
| Step-4 base canonical spec | canonical owner | inspected for role/context/result contracts |
| Step-4 single-context amendment | later canonical amendment | exhausted-for-current-decision |
| R2.1/R2.2/R2.3 canonical specs | upstream canonical owners | inspected for active handoffs |
| Step-3 canonical | deterministic execution owner | inspected for binder/acceptance/retry authority |
| Step-5.12 canonical | emission/disclosure owner | exhausted for Narrator boundary |
| `PLAY_POLICY.md` | shipped runtime owner | exhausted for instruction-presence/activation contract |
| `AI_REASONING.md` | shipped always-active correctness layer | exhausted for authority/context discipline |
| `NPC.md`, `PREP.md`, `NARRATIVE.md` | shipped role consumers | exhausted for Actor/Dramaturg/Narrator responsibility |
| Protocols 1–3 | empirical evidence | exhausted for current containment/topology decision |
| platform-feasibility research | noncanonical external research | inspected; superseded isolation premise excluded |
| D16, S21, S28 dossier records | research candidates | item-level reconciled below |
| former Step-6 framing | historical derivation | inspected only for still-unsolved lifecycle/emission questions |
| runtime context research cases | test/evidence | inspected for full-CORE present-vs-active and lazy campaign data invariants |

No current evidence requires provider abstraction, direct API orchestration, nested subagents or background workers to decide R2.4 logical architecture. Concrete current ChatGPT feature/limit validation remains R2.6 unless a later R2.4 finding makes a specific host fact architecture-blocking.

---

## 2. Established canonical/current constraints

### C01 — Logical roles are contracts, not physical calls

Step 4 defines Interpreter, Dramaturg, Actor, Narrator, Chronicler and Commentator as responsibility/context/authority contracts.

The later amendment explicitly permits multiple logically incompatible role phases inside one physical context and one user-request/assistant-turn execution.

Disposition: **NON-NEGOTIABLE**.

### C02 — Physical presence does not imply logical eligibility

Before each logical phase, role/subject/authority/output contract must be rebound. Raw private frame material does not transfer merely because it remains physically visible.

Disposition: **NON-NEGOTIABLE**.

### C03 — Context selection already belongs to R2.3

R2.3 now owns registered `ContextNeedProfile`, bounded discovery, routed currentness, eligibility, required typed packet closure, legal representation floors and `RoleContextBundle` assembly outcomes.

R2.4 must not reimplement relevance/eligibility inside ad-hoc prompts.

Disposition: **UPSTREAM BOUNDARY**.

### C04 — Deterministic core owns accepted execution

Step 3 keeps LLM output at interpretation/proposal boundaries. Deterministic binder/runtime owns valid IDs, rules, RNG, accepted world/runtime mutations, idempotency and replay semantics.

A later LLM failure cannot justify replaying accepted mechanics or consuming new RNG merely because presentation failed.

Disposition: **NON-NEGOTIABLE**.

### C05 — Narrator has an existing emission boundary

Step 5.12 distinguishes private draft generation, validated `NarrationResult`, frozen representation and `EMISSION_COMMIT`.

Material disclosure refs and intended recipient are validated before emission commit. Ordinary interruption/retry has an owner-accepted presentation-risk limitation; baseline does not add a delivery-ack subsystem.

Disposition: **NON-NEGOTIABLE / R2.4 INTEGRATION ONLY**.

### C06 — Entire CORE instruction corpus is physically present

Current `PLAY_POLICY.md` preloads complete `CORE/*.md` once and explicitly distinguishes `loaded` from `active`.

Situational modules activate from headers/current situation without reread or physical removal. Campaign data remains lazy.

R2.4 consequence:

> instruction activation must work by semantic precedence/activation/rebinding over a physically present corpus, just as role containment works over physically present information.

Disposition: **CURRENT RUNTIME CONSUMER REQUIREMENT**.

### C07 — Always-active correctness layer already exists

`AI_REASONING.md` is always active and already owns evidence-before-plausibility, state-before-story, knowledge compartmentalization, context discipline, bounded deliberation and correction behavior.

R2.4 should compose with it rather than create a duplicate universal role constitution.

Disposition: **REUSE OWNER**.

### C08 — Actor/Dramaturg/Narrator responsibilities already exist in shipped guidance

- `NPC.md`: significant NPC behavior follows identity/goals/knowledge/relationships/resources; cognition should not inherit generic assistant helpfulness.
- `PREP.md`: preparation is provisional situations/actors/pressures, not required plot or automatic canon.
- `NARRATIVE.md`: narration projects resolved/perceivable state, preserves player agency, advances play in the same response when safe and stops at meaningful player decision points.

R2.4 consequence:

> role frames should bind/activate existing responsibilities, not duplicate them as separate giant role prompts.

Disposition: **REUSE OWNER**.

### C09 — Protocol 1 supports sequential rebinding in persistent history

Naturalistic semantic probes: 64/64 PASS. It is strong pilot evidence, not proof of cognitive absence.

Disposition: **SUPPORTS SHARED HISTORY / EXPLICIT REBINDING**.

### C10 — Protocol 2 supports collapsed multi-role execution but rejects large model transport envelopes

Strongest channels:

- hidden target 0/11;
- eligible controls 4/4;
- dynamic eligible controls 4/4;
- private-branch affinity 0/12 supporting evidence.

The protocol also observed malformed/repair-prone large structured responses and concluded deterministic Python should own serialization/validation/bookkeeping.

Disposition: **SUPPORTS ONE-TURN MULTI-ROLE + MINIMAL MODEL INTERFACES**.

### C11 — Protocol 3 supports long-history containment across reasoning profiles

Across 150 turns, no systematic role-boundary collapse appeared. High reasoning remains owner-selected working baseline but is replaceable and not game-state semantics.

Protocol 3 also found over-completion risk: deeper synthesis can fill missing transitions if authority boundaries are weak.

Disposition: **SUPPORTS SHARED CONTEXT; REQUIRES COMMIT GATE**.

### C12 — Current personal baseline does not prove nested subagent orchestration and no longer needs it

Platform-feasibility research did not establish ordinary consumer ChatGPT text chat as a user-controlled nested role-subagent runtime.

The later Step-4 amendment makes such physical isolation/subagent topology unnecessary for baseline semantics.

Disposition: **NO DEPENDENCY / R2.6 REVERIFY ONLY AS OPTIONAL PROFILE**.

### C13 — Old Step-6 physical-isolation premise is superseded, lifecycle questions remain useful

Former Step-6 notes contain still-valid questions about:

- typed result lifecycle;
- regeneration after deterministic acceptance;
- Narrator validation/emission;
- hidden reasoning not becoming persistence;
- visible host surfaces;
- instruction/versioning topology.

Their mandatory fresh-context/isolation premise is superseded by the Step-4 amendment.

Disposition: **HISTORICAL INPUT, SELECTIVE RETENTION**.

---

## 3. Research candidate disposition

### D16 — Invisible auxiliary generation/work

Research claim:

- classification, summarization, cognition, repair and similar internal work should not look like gameplay turns or contaminate narrative history;
- original research allowed separate calls/budgets/permissions where host permits.

Current qualifier/reconciliation:

- current baseline is one physical chat context and one assistant turn;
- direct API/private orchestration/background workers are out;
- Step-4 amendment supports internal logical role phases in the same physical turn.

R2.4 synthesis:

> Adopt **invisible logical internal phases/results**, not mandatory auxiliary model calls. Internal role/result material is not player-facing history unless it crosses the Narrator/EMISSION_COMMIT boundary or another existing durable owner explicitly admits it.

Disposition: **ADOPT DELTA / REJECT MANDATORY EXTRA-CALL INTERPRETATION**.

### S21 — Late steering as separate channel

Research claim:

- current narrative task/tone/constraint should remain distinguishable from world facts/campaign essentials and may benefit from proximity to generation frontier;
- risk: position effects are model-dependent.

Trigger: active because R2.4 designs physical instruction topology.

R2.4 synthesis:

> Adopt a typed/semantically separate **phase-local steering** concept for presentation/task emphasis. Its authority class is explicitly noncanonical/non-evidentiary; it cannot override system/project/CORE law, role eligibility or accepted state. Physical prompt position may optimize quality but is not a semantic guarantee.

Disposition: **ADOPT PRINCIPLE / REJECT POSITION-AS-AUTHORITY-LAW**.

### S28 — Sanitize operational protocol from visible output

Research claim:

- internal control markers/JSON/maintenance artifacts must not reach players;
- string stripping alone is not a security boundary.

Trigger: active before auxiliary protocols become canonical.

R2.4 synthesis:

> Adopt structural output fencing: only the Narrator's validated player-facing payload may intentionally cross `EMISSION_COMMIT`; role frames, typed internal results, tool/debug traces and operational markers remain internal. Any final string sanitization is defense in depth only.

Disposition: **ADOPT / STRUCTURALIZE**.

---

## 4. Material architecture tensions

### T01 — Model-owned choreography versus deterministic/registered envelope

Pure model self-orchestration is simple but lets the model decide that a phase/dependency is unnecessary without a typed contract, weakening diagnostics and making skipped Actor/Dramaturg work hard to distinguish from ordinary creative synthesis.

A fully rigid deterministic phase FSM would overengineer creative work and require deterministic predicates for inherently semantic needs.

Synthesis candidate:

> registered bounded phase envelope; deterministic/typed contracts own legal phases, contexts, authority and commit gateways; model may propose optional semantic phase activation, but cannot self-grant new eligibility/authority.

### T02 — Explicit phase outputs versus one blended hidden reasoning pass

A single integrated reasoning pass is token-efficient but weakens Actor-local boundaries, multiple-Actor diagnostics and result lifecycle semantics.

Large explicit JSON per phase is also undesirable due Protocol-2 evidence.

Synthesis candidate:

> explicit logical phase boundaries with **minimal typed semantic handoffs**, while rationale/private chain-of-thought remains transient and non-required.

### T03 — Narrator candidate inside same turn versus separate physical call

Step-4 amendment permits same physical context. Step 5.12 requires logical validation before emission commit, but baseline ordinary ChatGPT does not require a separate hidden model call.

Synthesis candidate:

> Narrator is a final logical phase in the same assistant turn; it produces a bounded internal `NarrationResult`/disclosure intent that deterministic validation checks before the supported response representation is committed. Physical host buffering/streaming capabilities are R2.6 profile validation, not reason to reintroduce mandatory separate calls here.

### T04 — Instruction duplication versus activation over existing CORE

Separate giant Interpreter/Dramaturg/Actor/Narrator prompt packs would duplicate `AI_REASONING`, `NPC`, `PREP`, `NARRATIVE` and create drift.

Synthesis candidate:

> stable instruction constitution/procedure corpus remains in existing host/project/CORE layers; role frame activates/narrows responsibilities and output contract; it does not restate the full engine.

---

## 5. Preliminary synthesis laws

Candidate laws before owner decision:

1. one assistant turn may contain multiple sequential logical phases without one model call per role;
2. a registered TurnEnvelope owns legal phase types/order constraints; the model may propose optional phase activation but cannot grant itself context/authority;
3. each phase rebinds role/subject/purpose/context/allowed handoffs/authority/output contract;
4. phases communicate through minimum typed semantic results, not raw private role context;
5. private rationale/chain-of-thought is never required persistence/recovery evidence;
6. deterministic owners validate/accept every material state/mechanics/disclosure transition;
7. after accepted mechanics, later LLM failure/regeneration is presentation/semantic retry only and does not replay mechanics/RNG;
8. Narrator is the only ordinary gameplay logical phase allowed to produce the supported player-facing payload;
9. operational/tool/internal role material is structurally excluded from emission; string sanitization is secondary defense;
10. existing CORE is physically present; activation is semantic and phase-scoped;
11. late steering is non-authoritative phase-local guidance, not world evidence;
12. Chronicler remains opportunistic/non-hot-path under Step 5.10 unless explicitly invoked; Commentator remains separate mode;
13. R2.3 `UNSATISFIABLE` is handled by a finite caller policy, not silent guess/retry loops.

---

## 6. Completeness status

The active R2.4 D/S candidates D16/S21/S28 are individually accounted.

Protocols 1–3 are reconciled with the later canonical amendment rather than used to resurrect physical isolation.

The current owning runtime instruction surfaces are reconciled with the one-context model.

The remaining material owner question is the baseline phase-choreography shape, captured in the companion Decision Brief.
