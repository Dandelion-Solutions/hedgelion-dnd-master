# R2.7 WP-08 Step 5 — Candidate Specification

Status: **CANDIDATE — PENDING STEP-6 ADVERSARIAL REVIEW**

## 1. Purpose and non-goal

This candidate records a machine-realization allocation for the already accepted
R2.1–R2.6 and Step-4/5 architecture. It resolves the WP-08 mapping question
without creating a role, prompt, memory, provider, storage, catalog or semantic
authority.

It does not authorize runtime, schema, catalog, CORE or test changes. It does
not reopen WP-07. It is not a replacement for the R2.3 Context Runtime, R2.4
TurnEnvelope, R2.6 host-assurance, R2.1 continuity/history, R2.2 Actor
continuity/cognition, Step-4 knowledge/disclosure, Step-5.10 Story or Step-5.12
delivery specifications.

## 2. Preserved invariants

The candidate preserves all of the following:

- one physical conversational context, with logical rebind before every material
  phase; a logical role is not a model call or a separate agent;
- physical prompt/cache/chat presence never grants eligibility;
- Context Runtime is a bounded ephemeral projection, and its internal reads,
  routing, bundle and trace gain no truth, currentness, cognition, disclosure or
  continuity authority;
- R2.1 continuity may orient an eligible role but must escalate to the proper
  current/exact/source class for a material claim; hidden reasoning, prompts,
  abandoned generations and unaccepted candidates are not continuity evidence;
- an Actor assessment has an explicit R2.2 purpose and bounded eligible
  evidence/current state. Source-Actor-private continuity never becomes a
  duplicate writable proposition stance; `world.knowledge` remains that owner;
- typed handoffs carry only accepted minimum semantic results. Raw private
  bundles, role frames, diagnostics and hidden reasoning are never downstream
  evidence;
- Story has no same-envelope feedback into gameplay roles; Narrator is freshly
  rebound after Chronicler service and only its validated recipient-safe result
  reaches `EMISSION_COMMIT`;
- `UNSATISFIABLE` and degradation remain finite registered outcomes, never a
  licence to guess, silently omit required evidence or expand discovery.

## 3. Candidate realization allocation

### 3.1 One shipped instruction route — WP-08/F03

The exact R2.6 behavioural-containment instruction belongs in
`GAME/CORE/AI_REASONING.md`, the existing always-active LLM-correctness
module. Its future implementation amendment SHALL be equivalent to:

```text
Use only information eligible to the active role under the current RoleContextBundle and lawful typed handoffs.
Physical presence elsewhere in the conversation does not make information eligible.
When information later becomes lawfully eligible, use it normally; prior ineligibility is not permanent forgetting.
```

This is the sole ordinary-gameplay instruction owner for this rule.

`GAME/CORE/PLAY_POLICY.md` remains the owner of immutable CORE cache and
header-driven activation: it makes `AI_REASONING.md` active, but must not
duplicate or redefine the containment rule. `GAME/CORE/RUNTIME.md` remains the
owner of engine turn order and must invoke the registered role/context contract,
not restate a competing prompt. Project Instructions remain package/bootstrap
only. This allocation discharges the carried WP-07/F06 obligation when the
future CORE amendment and its verification are implemented.

### 3.2 Transient role/context control — WP-08/F01 and F02

`TurnEnvelope`, `RoleContextRequest`, registered
`ContextNeedProfile` identity, `RoleContextBundle`, `ContextTrace`,
eligible typed prior-result references and terminal/degradation outcome are
runtime-local control contracts for one attempted turn or phase. Their semantic
owners remain R2.3/R2.4; their implementation realization is a deterministic
runtime orchestration boundary.

The explicit representation decision is:

| Item | Representation | Prohibited substitute |
|---|---|---|
| `TurnEnvelope` | ephemeral, bounded runtime control | campaign/session/checkpoint record |
| request/profile/bundle identity | ephemeral typed runtime contract | generic prompt/memory record |
| `ContextTrace` | protected diagnostic/runtime trace | role evidence, Story, player output |
| terminal/degradation result | finite typed caller outcome | silent model repair or unlimited retry |
| Actor private continuity | existing source `world.actor.continuity` only when R2.2 lifecycle admits it | Envelope/bundle/trace or `world.knowledge` |
| proposition stance | existing `world.knowledge` owner | Actor continuity or role-local scratch state |

No persistent schema, generic catalog entry or campaign record is added for these
transient objects. Existing S6D `MechanicalContext` may remain an independently
owned mechanical invocation surface; it is neither a `RoleContextBundle` nor an
R2.3 eligibility authority.

Before each material Interpreter, Dramaturg, Actor, Chronicler or Narrator phase,
the runtime boundary must establish the R2.4 rebind tuple: role, applicable
subject/recipient, purpose, registered profile, bundle/basis, allowed typed prior
results, accepted deterministic references, authority limits and result/output
contract. An Actor phase additionally records its R2.2 assessment purpose and
uses only bounded eligible evidence/current state. This does not make Actor
continuity ambient or turn it into `world.knowledge`.

### 3.3 Source and handoff discipline

R2.1 source escalation is a required consumer behaviour of the candidate runtime
contract:

1. an eligible derived Story/history/current-chat item may supply broad or
   episodic orientation and a routing hint;
2. a material role claim escalates to its native current, exact, knowledge,
   disclosure or accepted-history owner as applicable;
3. the eligibility check precedes semantic use by the receiving role; an internal
   lookup to decide eligibility is not thereby role evidence;
4. hidden reasoning, prompt text, private diagnostics, abandoned drafts and
   unaccepted generated candidates are excluded from both continuity evidence and
   typed handoffs.

A handoff is purpose-, subject-, recipient- and generation-scoped. It exposes
only a registered accepted semantic result (for example the existing role/result
vocabulary where applicable), never the full upstream bundle, raw private
deliberation or a generic role-result bus. A recipient/catch-up or planning input
must therefore be assembled against its own eligibility contract; co-presence in
the shared chat does not merge it.

### 3.4 Protected output — WP-08/F04

The runtime orchestration boundary preserves distinct Actor, Chronicler and
Narrator phases:

- Actor produces only its allowed subject-local accepted result; it cannot
  disclose private continuity or create proposition stance by narrative force.
- Chronicler uses a separately eligible Step-5.10 source basis and may not feed
  newly created/changed Story back into a gameplay role in the same envelope.
- Narrator receives a fresh R2.4 rebind after Chronicler, a recipient-eligible
  bundle and only lawful typed prior results. Its validated result is the only
  candidate passed to Step-5.12 `EMISSION_COMMIT`.

No trace, tool/debug/progress surface, Chronicler draft or raw upstream context is
a player-delivery path.

### 3.5 Required implementation-facing verification — WP-08/V01

Future implementation/TDD must establish observable, not merely structural,
evidence for:

1. ineligible physically present information is neither materially used nor
   disclosed, while later lawfully eligible information is usable normally;
2. a material claim sourced from Story/history/current chat escalates to the
   appropriate owner, and prohibited hidden/unaccepted material cannot enter
   continuity or a handoff;
3. a material Actor phase requires a declared purpose, bounded eligible evidence
   and preserves Actor-private continuity versus `world.knowledge`;
4. every material phase is rebound; raw private bundle/trace transport and
   MechanicalContext substitution fail;
5. fresh Narrator rebind, no same-envelope Story feedback and recipient-safe
   `EMISSION_COMMIT` hold;
6. finite degraded/`UNSATISFIABLE` paths preserve required evidence floors and
   do not guess, loop or replay mechanics/RNG/canon;
7. the R2.6 instruction is active exactly through the `AI_REASONING` +
   `PLAY_POLICY` activation route, with no competing duplicate owner.

Existing CORE-cache and S6D structural tests are supporting regression evidence,
not a substitute for this behavioural suite.

## 4. Explicit exclusions

This candidate does not select code-module names, host APIs, token budgets,
provider abstractions, storage layout, durable schemas, catalog vocabulary,
prompt DSL, background worker, result bus or implementation order. Those are
outside WP-08 and must not be inferred from this allocation.

## 5. Candidate self-review

- **No new authority:** every semantic rule remains owned by its cited canonical
  owner; the only current file allocation selects the existing always-active
  `AI_REASONING.md` instruction owner.
- **No accidental persistence:** all role/context control objects are explicitly
  runtime-local; R2.2's admitted Actor continuity is the sole relevant durable
  exception and remains distinct from `world.knowledge`.
- **No hidden source widening:** R2.1 escalation and exclusion rules apply before
  Actor, handoff, Chronicler and Narrator use.
- **No implementation action:** all edits, tests and runtime work remain future
  obligations.

## 6. Next step

Run the Step-6 adversarial review against this candidate, especially duplicate
instruction authority, accidental durable state, actor/knowledge conflation,
raw-handoff leakage, Story feedback and degradation behaviour.
