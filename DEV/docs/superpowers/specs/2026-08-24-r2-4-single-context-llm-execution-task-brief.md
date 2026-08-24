# R2.4 — Single-Context LLM Execution & Instruction Architecture — Task Brief

Status: **TASK BRIEF / IN PROGRESS**

Date: 2026-08-24

Roadmap owner:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Depends on:

- R2.1 continuity canonical specification;
- R2.2 Actor continuity canonical specification;
- R2.3 Context Runtime canonical specification;
- accepted Round-1 Steps 3–5 architecture;
- Step-4 single-context role-containment canonical amendment.

## 1. Problem statement

HDM's current baseline is one ChatGPT Plus ordinary public chat, one physical LLM conversational context, one user request and one assistant turn.

Within that physical turn, one model may need to perform several sequential logical responsibilities while preserving different information/authority/output contracts:

```text
Player input
    -> Interpreter
    -> optional Dramaturg
    -> zero or more Actor[subject]
    -> deterministic/core interactions as required
    -> Narrator
    -> validated player-facing response
```

Chronicler and Commentator remain separate logical responsibilities whose physical placement must be decided only where the current baseline requires it.

R2.4 must define the minimum logical/physical execution and instruction machinery that makes this topology operational without:

- turning physical context co-presence into fictional knowledge/authority;
- requiring one model call/process/agent per logical role;
- asking the model to own large transport JSON or deterministic bookkeeping;
- replaying accepted mechanics/RNG when presentation or a later nondeterministic phase fails;
- allowing hidden operational protocol/tool output to leak through the player-facing surface;
- making hidden chain-of-thought or prior unstructured role prose a persistence/recovery dependency;
- overengineering provider abstraction or background orchestration outside the current product baseline.

## 2. Human decision boundary

The agent must do the technical evidence work and return only material architecture choices.

Do not ask the owner to choose prompt wording, field names, serialization syntax, module filenames or retry bookkeeping details unless they encode a genuine product/semantic trade-off.

Likely owner-level questions include only decisions such as:

- baseline one-turn phase topology if multiple materially different topologies remain viable;
- whether a nondeterministic phase/result must be retained/frozen across a specific failure/retry boundary;
- whether a visible-output limitation is acceptable when the baseline host cannot prove a stronger boundary;
- whether a logical role belongs in the ordinary hot path or remains opportunistic/separate mode.

## 3. Current non-negotiable constraints

### C1 — One physical context / logical role containment

Step-4 amendment is canonical:

- physical availability != logical eligibility;
- rebind before each logical role phase;
- no transitive raw-role inheritance;
- lawful typed/observable transfer only;
- invented != canonical;
- physical separation is optional defense/fallback, not baseline semantic requirement.

### C2 — Context Runtime already owns source selection

R2.3 owns bounded discovery, currentness, eligibility, required packet closure, legal representations and `RoleContextBundle` assembly outcomes.

R2.4 must consume those results. It must not create a second retrieval/eligibility system inside prompts.

### C3 — Deterministic core owns accepted execution

Step 3 owns binding/validation/mechanics/RNG/accepted state transition/idempotency.

LLM phases may interpret/propose/narrate only through typed boundaries.

### C4 — Narrator/output boundary already has Step-5 semantics

Step 5.12 owns `EMISSION_COMMIT`, recipient-scoped disclosure and the distinction:

```text
private draft generation
!= validated NarrationResult
!= EMISSION_COMMIT
```

R2.4 must define the logical turn choreography that reaches this boundary; it must not create a second delivery authority.

### C5 — Entire CORE instruction set is physically preloaded

Current `PLAY_POLICY.md` preloads all `CORE/*.md` once into the chat context and distinguishes `present` from `active`.

R2.4 therefore designs deterministic semantic activation/rebinding over a physically present instruction corpus. It does not assume situational CORE modules are reread/removed every role phase.

Campaign/world/entity data remains lazy under R2.3.

### C6 — Model should not own large transport envelopes

Protocol 2 observed avoidable malformed-output/repair risk when the model produced large strict structured envelopes. Deterministic code should own serialization, validation and bookkeeping; model hot-path interfaces should be the minimum typed semantic contract.

### C7 — Current baseline does not require nested subagents/background workers

Platform feasibility evidence does not establish personal ordinary ChatGPT text chat as a user-controlled nested subagent surface. The accepted single-context amendment removes any need to depend on such a feature for baseline correctness.

Current architecture must work without direct API calls, private hosting, ChatGPT Work or permanently running background execution.

## 4. Task-specific Source Manifest

| Source | Role | R2.4 use |
|---|---|---|
| current roadmap | sequencing authority | stage scope/status |
| Step-4 base canonical spec | canonical owner | role contracts, handoff/result families, Context Assembler, disclosure/promotion boundaries |
| Step-4 single-context amendment | later canonical amendment | shared-context role containment, rebinding, physical topology correction |
| R2.1 canonical | upstream owner | continuity/Story eligibility and escalation |
| R2.2 canonical | upstream owner | Actor cognition/relationship/private-state semantics |
| R2.3 canonical | upstream owner | need profiles, bundles, packet closure, currentness, eligibility, assembly outcomes |
| Step-3 canonical | canonical owner | LLM -> deterministic binder/execution boundary, retries/idempotency/RNG |
| Step-5.12 canonical | canonical owner | NarrationResult -> validation -> EMISSION_COMMIT, visible-surface/disclosure constraints |
| `GAME/CORE/PLAY_POLICY.md` | shipped runtime owner | immutable CORE cache, present != active, runtime-scope/latency policy |
| `GAME/CORE/AI_REASONING.md` | shipped always-active instruction | authority/evidence/context/agency/knowledge correctness layer |
| `GAME/CORE/NPC.md` | shipped role consumer | Actor behavior/private cognition semantics |
| `GAME/CORE/PREP.md` | shipped role consumer | Dramaturg-like preparation semantics/provisionality |
| `GAME/CORE/NARRATIVE.md` | shipped role consumer | Narrator projection/pacing/agency/output obligations |
| Protocol 1 | empirical evidence | persistent-history sequential role containment |
| Protocol 2 | empirical evidence | collapsed same-generation multi-role containment; transport-envelope failure evidence |
| Protocol 3 | empirical evidence | long-history/reasoning-profile containment + gameplay-quality risks |
| platform feasibility study | research input | current consumer-host capability/limits; reinterpret under later single-context amendment |
| external idea dossier D16/S21/S28 | research input | invisible auxiliary work, late steering separation, visible-output sanitation |
| former Step-6 framing notes | historical derivation | preserve still-unsolved result lifecycle/emission/instruction questions; discard superseded physical-isolation premise |
| relevant tests/evaluation cases | implementation/evidence | identify existing regression expectations before canonical closure |

Before Decision Brief, all materially relevant claims from the active D/S items and the owning sources above must have an explicit disposition.

## 5. Required design questions

### 5.1 One-turn phase topology

Determine:

- which logical phases are baseline, conditional or separate mode;
- whether Interpreter/Dramaturg/Actor/Narrator are always explicit phases or may collapse/skip when no unresolved semantic work exists;
- how multiple Actor subjects execute sequentially without private-state inheritance;
- how deterministic/core operations interleave with LLM phases;
- where the turn stops at a meaningful player decision point.

Do not equate one logical phase with one physical model call.

### 5.2 Role activation / rebinding

Define the minimum phase frame required to rebind:

- active logical role;
- subject/player identity;
- purpose;
- applicable `ContextNeedProfile` / `RoleContextBundle`;
- permitted prior-role typed results;
- authority limits;
- output contract;
- current deterministic state/result references where applicable.

Avoid persona/theatrical role-play machinery. This is correctness framing.

### 5.3 Typed nondeterministic results and lifecycle

For Interpreter, Dramaturg, Actor, Narrator and any admitted auxiliary semantic result, decide:

- minimum typed semantic payload;
- validation boundary;
- whether exact result identity/prose needs retention;
- when regeneration is legal;
- what happens if host/model failure occurs before acceptance;
- what happens if accepted mechanics already exist and a later LLM phase fails;
- what a host retry/regeneration may never replay.

No hidden reasoning persistence requirement.

### 5.4 Deterministic gateway/interleaving

Specify how logical LLM phases call into or receive results from deterministic owners without allowing:

- LLM prose -> direct state authority;
- replayed mechanics/RNG due to later presentation failure;
- arbitrary tool access from every role;
- raw tool output becoming role/player evidence without eligibility/validation.

### 5.5 Narrator / visible output

Integrate Step 5.12:

- Narrator receives only eligible/settled evidence;
- private role/operational material cannot be emitted intentionally;
- material disclosure refs are validated before `EMISSION_COMMIT`;
- determine the minimum internal `NarrationResult` boundary compatible with ordinary ChatGPT one-turn delivery;
- preserve owner-accepted interruption limitations rather than inventing a delivery subsystem.

### 5.6 Instruction hierarchy and activation

Determine the minimum stable hierarchy among:

- system/developer/project-level host instructions;
- Project Instructions;
- always-present shipped CORE Markdown;
- current module activation state;
- role/phase frame;
- current `RoleContextBundle` and typed handoffs;
- late turn-local steering/presentation goal.

Clarify precedence/conflict behavior and versioning responsibility without building a generic prompt-programming framework.

### 5.7 Injection / role confusion

Treat player/campaign/world/Story text as data, not executable engine instruction.

Specify defenses against:

- campaign text pretending to be engine instruction;
- Story/prose injecting role switches;
- Actor dialogue/tool output changing system authority;
- raw prior-role output being interpreted as a new instruction;
- operational markers leaking to visible Narrator output.

### 5.8 Context Runtime failure integration

R2.3 `UNSATISFIABLE` must have a caller policy that does not loop.

R2.4 must classify safe responses such as:

- deterministic path without LLM phase;
- narrower registered task/reassembly;
- explicit player clarification where genuinely blocking;
- bounded degradation/omission where allowed;
- typed unsupported/blocked outcome.

Do not let the LLM silently guess missing required context.

## 6. Active research candidates

### D16 — invisible auxiliary generation/work

Active delta:

- maintenance/classification/cognition/preparation work should not appear as player turns or narrative history;
- under current baseline this does **not** imply separate model calls/subagents/background workers;
- R2.4 must define invisible logical internal phases/results where needed.

### S21 — late steering as separate channel

Trigger is active because R2.4 now designs physical instruction topology.

Question:

> How should turn-local narrative/task steering remain distinguishable from world facts, engine law and role eligibility without relying on provider-specific positional magic as a semantic guarantee?

### S28 — sanitize operational protocol from visible output

Trigger is active before auxiliary/role protocols become canonical.

Question:

> How does HDM prevent control markers, typed internal payloads, tool/debug text and private-role reasoning from intentionally reaching the player-facing surface, while recognizing that string stripping alone is not a security boundary?

## 7. Negative / YAGNI boundaries

R2.4 must not create without new evidence:

- required multi-agent/subagent framework;
- direct API provider abstraction;
- background job scheduler;
- generic extension/plugin system;
- large universal role-result JSON protocol;
- persistent chain-of-thought store;
- generic prompt DSL;
- separate instruction files merely to mirror every logical phase if existing CORE ownership suffices;
- mandatory physical context isolation already superseded by the Step-4 amendment.

## 8. Exit criteria

R2.4 closes only when:

1. ordinary one-request/one-assistant-turn phase choreography is explicit;
2. baseline/conditional/separate-mode role activation is explicit;
3. role rebinding inputs and no-raw-inheritance rules are explicit;
4. typed nondeterministic result families have minimum lifecycle/retry semantics;
5. deterministic mechanics/tool/commit interleaving cannot replay or accept LLM prose as authority;
6. Narrator/EMISSION_COMMIT integration is explicit;
7. instruction hierarchy/activation/conflict boundaries are explicit;
8. `UNSATISFIABLE` caller behavior is bounded/non-looping;
9. injection/operational-output leak boundaries are explicit;
10. Chronicler/Commentator placement is resolved to the extent required by current baseline;
11. D16/S21/S28 have item-level disposition;
12. Protocols 1–3 and platform-feasibility evidence are reconciled under the current amendment rather than copied with superseded assumptions;
13. adversarial review finds no unresolved role-contamination, replay, hidden-authority or visible-output blocker;
14. downstream R2.6/R2.7 obligations are explicit without prematurely implementing them.

Broad implementation remains blocked.
