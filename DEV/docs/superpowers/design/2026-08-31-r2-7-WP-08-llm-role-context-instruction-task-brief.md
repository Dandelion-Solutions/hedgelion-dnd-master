# R2.7 WP-08 — LLM Role, Context and Instruction Architecture — Task Brief

Status: **STEP-1 TASK BRIEF / WHOLE-PROJECT CRITIC REPAIRED AFTER SENIOR HOLD — PENDING SENIOR REVIEW**

## 1. Mandate

WP-08 is the R2.7 audit domain for the accepted logical LLM-role, role-context and
instruction architecture. Its purpose is to determine whether the current repository
can realize the already accepted architecture without inventing a second role,
context, prompt, memory, or authority subsystem.

The domain answers the four questions registered by the R2.7 scope discovery:

1. Are Interpreter, Dramaturg, Actor, Chronicler, Narrator and Commentator mapped
   as logical responsibilities without persistent hidden chain-of-thought?
2. Are `RoleContextRequest`, bounded discovery/packet closure,
   `RoleContextBundle`, `ContextTrace`, degradation outcomes and minimum typed
   handoffs mapped to deterministic support surfaces where required?
3. Is the behavioral rule below owned once and applied consistently?

   ```text
   ineligible now -> do not materially use or disclose
   lawfully eligible later -> may use normally
   ```

4. Do CORE activation and Project Instructions support one physical chat context with
   semantic role rebinding, without a duplicated giant prompt, unsafe raw-context
   inheritance, or role confusion?

This is an architecture-to-machine and machine-to-architecture conformance audit.
It does not reopen the accepted one-context topology merely because its current
machine mapping is incomplete.

## 2. Current authority, stage and upstream boundary

- Global current work and gate: `DEV/CURRENT_PROGRESS.md`.
- R2.7 scope and execution method:
  `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`,
  `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md` and
  `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-execution-protocol.md`.
- General and HDM architecture process: `DEV/DESIGN_PROCESS.md` and
  `DEV/ARCHITECTURE/DESIGN_PROCESS.md`.
- `DEV/PROJECT_MAP.md` is the discovery route; it is not a semantic owner.

`DEV/CURRENT_PROGRESS.md` authorizes only WP-08 Step 1. Step 2 may not begin
until the required Senior GO after this repaired Task Brief and critic.

WP-07 is a closed upstream input. Its Step-8 closure preserves the five-way
information boundary and records `WP-07/F06` as an implementation obligation:
an explicit active-role / `RoleContextBundle` / lawful typed-handoff instruction
must be realized under existing owners. WP-08 must map that obligation; it must not
reopen WP-07's truth, knowledge, disclosure, communication or retention findings
unless a real contradiction material to this domain is discovered.

The older `audit-status.md` still describes the pre-GO WP-07 checkpoint. It is a
task-local historical/recovery record and is subordinate to current progress for
global authorization. This framing package therefore does not edit it.

## 3. Accepted architecture to preserve

The audit starts from the following established constraints:

```text
one user request
-> one assistant turn
-> one physical conversational context
-> one or more registered logical role phases
-> deterministic/native-owner acceptance where required
-> validated Narrator output / EMISSION_COMMIT
```

- Logical roles are not separate agents, model calls, processes or chats.
- Physical presence in shared context does not make information logically eligible.
- Each material role phase rebinds role, purpose, subject/recipient scope, authority,
  admitted context and output/result contract.
- Context Runtime is a bounded ephemeral projection over native owners; its bundles,
  traces, indexes and caches do not become campaign truth or durable memory by
  convenience.
- Typed handoffs carry only the minimum accepted semantic result. Raw private bundles,
  role frames and hidden reasoning do not become downstream evidence.
- Deterministic/native owners validate mechanics, currentness, Story coverage,
  disclosure and publication. LLM output remains a proposal until accepted by the
  owning contract.
- `UNSATISFIABLE` and degradation are finite registered outcomes, not permission to
  guess, invent a new need profile or perform unbounded reassembly.
- Full preloaded CORE is an immutable in-chat instruction cache. It is distinct from
  semantic activation and from the narrower role-local evidence bundle.
- Project Instructions select/validate the runtime package and its startup boundary;
  they do not silently become a second ordinary-gameplay role/prompt owner.
- Behavioral containment, not physical/cognitive isolation, is the supported MVP
  guarantee. Lawful later eligibility restores ordinary use.
- Player-visible content is constrained by the Narrator / `EMISSION_COMMIT` boundary.
  Tool, trace, debug and maintenance surfaces may not intentionally deliver
  ineligible campaign information.

## 4. Scope

### 4.1 In scope

Step 2 must map and reverse-audit:

- `TurnEnvelope` role/phase control, registered phase/result vocabulary and protected
  Narrator capacity;
- role activation/rebinding for Interpreter, Dramaturg, Actor, Chronicler, Narrator
  and Commentator;
- `RoleContextRequest`, registered `ContextNeedProfile`, bounded discovery,
  routing/currentness/eligibility checks, packet closure, representation floors,
  `RoleContextBundle`, `ContextTrace` and terminal assembly results;
- R2.1 continuity/history use: eligibility-preserving Story/history orientation,
  broad-to-episodic/current/exact source escalation, and exclusion of hidden reasoning,
  prompts, abandoned generations and unaccepted candidates from continuity evidence;
- R2.2 Actor continuity/cognition use: one explicit Actor assessment purpose and bounded
  eligible evidence/current state per assessment; source-Actor-private continuity must
  remain distinct from current proposition stance under `world.knowledge`;
- purpose-, subject-, recipient- and generation-scoped typed handoffs, including
  boundaries where R2.5 collaboration, catch-up or Dramaturg planning enters a
  participant TurnEnvelope;
- the explicit R2.6 behavioral-containment instruction rule and its exact
  runtime/instruction owner(s), including the WP-07/F06 mapping;
- installed CORE activation semantics, `PROJECT_INSTRUCTIONS.txt`, the currently
  shipped gameplay instructions, their possible duplication/staleness and the
  precise distinction between instruction presence and role-local eligibility;
- Narrator output fencing, pre-emission validation and the relationship with
  Step-5.12 delivery/disclosure law;
- required ephemeral versus durable representation, diagnostic trace protection,
  machine schemas/catalogs/templates only where the accepted contract actually
  requires them, and relevant test/evaluation/maintenance ownership.

### 4.2 Out of scope

WP-08 does not:

- redesign truth, knowledge, disclosure, message, Story, Transcript or compaction
  semantics owned and closed through WP-07 and the Step-4/5 owners;
- choose a new physical multi-call, subagent, provider/API, prompt-DSL, background
  worker, role-result bus, generic memory database, vector database or prompt-cache
  architecture;
- turn transient `TurnEnvelope`, `RoleContextBundle` or `ContextTrace` into
  mandatory durable campaign records unless a current accepted owner proves a
  specific persistence requirement;
- decide full retrieval/storage topology, shard arithmetic, HOT/SQLite layout or
  estimator calibration; WP-09 and later storage domains own those physical mappings
  beyond the role/context interface boundary;
- redesign R2.5 collaboration/planning, Step-5.10 Story projection, Step-5.12
  delivery, or gameplay domain semantics;
- implement schemas, catalogs, tests, prompt text, CORE changes, or runtime behavior.

A discovered current surface is not presumed valid or invalid because it exists.
A missing persistent record is not presumed a gap when the accepted semantic object
is explicitly transient or diagnostic.

## 5. Quality attributes and failure probes

The later audit must distinguish mappings using:

- observable information-boundary correctness and lawful later uptake;
- deterministic authority and absence of duplicate writable owners;
- bounded normal-turn discovery/load behavior and protected visible-response capacity;
- recovery/retry safety without hidden-reasoning dependence or mechanics/RNG replay;
- testability/diagnosability without exposing protected trace material;
- instruction clarity without copied giant role prompts or accidental precedence;
- supported ChatGPT Plus / one-chat-per-player applicability without exact hidden token
  telemetry or unsupported host control assumptions.

The critic and Step 2 must challenge at least these failures:

- full CORE preload is misread as permission for every active role to use every
  physically present source;
- a raw Dramaturg/Actor/private adjudication bundle reaches Narrator or player catch-up;
- Story/history or current-chat visibility is treated as universal eligibility, avoids
  proper-source escalation for a material claim, or admits hidden reasoning, prompts,
  abandoned generations or unaccepted candidates as continuity evidence;
- Actor cognition runs as an ambient role with no explicit purpose, uses unbounded
  context, or duplicates/rewrites `world.knowledge` rather than bounded source-Actor
  private continuity;
- a role phase, prompt fragment, cache, trace, session field or schema becomes a second
  truth/knowledge/disclosure/Story/currentness authority;
- model-facing text creates a new phase, need profile, eligibility rule or executable
  operation without a registered deterministic owner;
- a context-pressure failure silently drops required evidence, guesses, or loops;
- a tool/debug/progress/auxiliary surface leaks Narrator-ineligible material;
- R2.5 planning/catch-up or WP-07 information owners are accidentally redefined.

## 6. Task-specific Source Manifest

This is the Step-1 manifest. “Inspect in Step 2” means read the stated exact
sections and reconcile them; it is not a claim that the source is itself new
authority.

### 6.1 Governance, sequencing and routing

| Source | Authority role | Required use |
|---|---|---|
| `AGENTS.md`; `DEV/DESIGN_PROCESS.md`; `DEV/ARCHITECTURE/DESIGN_PROCESS.md`; `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` | process / guardrail | framing, Step-1 critic, publication and later implementation boundary |
| `DEV/CURRENT_PROGRESS.md` | canonical global current-progress authority | current stage, authorized unit and mandatory Senior gate |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | sequencing/scope | R2.7 position and accepted operating constraints |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`; `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md`; `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-execution-protocol.md` | active R2.7 scope/method | exact WP-08 questions, proof direction, artifact and disposition rules |
| `DEV/PROJECT_MAP.md`; `DEV/docs/superpowers/design/2026-08-24-r2-7-global-semantic-owner-matrix.md` | derivative locator/evidence | dependency discovery and false-authority checks; owners above win |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md` | task-local historical cursor | recover pre-GO state only; do not override current progress |
| `DEV/docs/superpowers/design/2026-08-31-r2-7-WP-07-step-8-canonicalization.md`; `DEV/docs/superpowers/research/2026-08-24-r2-7-WP-07-truth-knowledge-disclosure-mini-report.md` | closed upstream audit input | preserve F06 handoff and verify no material contradiction before relying on it |

### 6.2 Canonical role, context and output owners

| Source | Authority role | Step-2 inspection scope |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md` | direct canonical constraint | source escalation, role/subject/recipient eligibility, Story/history orientation, no hidden reasoning as durable continuity, and bounded current/exact evidence acquisition |
| `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-canonical-spec.md` | direct canonical constraint | explicit Actor assessment purpose, source-Actor-private continuity, bounded eligible evidence, and separation from Step-4 `world.knowledge` epistemics |
| `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md` | canonical owner | six role contracts, Context Assembler request/bundle, typed handoffs, Narrator and Chronicler boundaries |
| `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md` | canonical amendment | superseding one-context logical eligibility and lawful handoff rule |
| `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md` | canonical owner | request/profile, discovery, packet closure, eligibility, allocation, outcomes and trace |
| `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md` | canonical owner | TurnEnvelope, rebinding, typed gateways, role phase/order, output fencing and `UNSATISFIABLE` caller behavior |
| `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md` | canonical downstream constraint | participant envelopes, recipient/catch-up, planning containment and cross-chat non-merge |
| `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md` | canonical assurance/amendment | observable containment, lawful uptake, instruction realization and supported host/profile limits |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-10-story-projection-durability-canonical-spec.md` | canonical neighbor | Chronicler non-authority, first-safe service inputs and Story publication boundary |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` | canonical neighbor | Narrator/`EMISSION_COMMIT`, recipient-scoped output and auxiliary-surface limits |

### 6.3 Current shipped instruction and runtime consumers

| Surface | Why it is in scope |
|---|---|
| `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`, `GAME/INSTALL/00_DND_BOOTSTRAP.md` | package/bootstrap instruction boundary versus ordinary role instruction |
| `GAME/CORE/PLAY_POLICY.md`, `GAME/CORE/CORE_INDEX.md` | full-CORE cache, header-driven activation and source-routing boundary |
| `GAME/CORE/RUNTIME.md`, `GAME/CORE/AI_REASONING.md`, `GAME/CORE/MECHANICS_INTEGRITY.md` | current turn order, authority and context/eligibility guards |
| `GAME/CORE/INFORMATION.md`, `GAME/CORE/NPC.md`, `GAME/CORE/NARRATIVE.md`, `GAME/CORE/PREP.md`, `GAME/CORE/GM_CRAFT.md`, plus implicated `GAME/CORE/LORE.md` and `GAME/CORE/SOURCES.md` | current role-facing information, cognition, preparation, narration and source consumers |
| `GAME/CORE/MULTIPLAYER.md`, `GAME/CORE/LIVE_SCENE.md`, `GAME/CORE/SESSION.md`, `GAME/CORE/STORAGE.md`, `GAME/CORE/PERSISTENCE.md` when reached through a concrete role/context edge | recipient/currentness/recovery consumers; do not preload as independent WP-08 owners |

### 6.4 Current machine/test surfaces

| Surface | Why it is in scope |
|---|---|
| `GAME/SCHEMA/current_state.schema.yaml`, `GAME/SCHEMA/session.schema.yaml`, `GAME/SCHEMA/player.schema.yaml`, `GAME/SCHEMA/event.schema.yaml`, `GAME/SCHEMA/checkpoint.schema.yaml`, `GAME/SCHEMA/live_scene.schema.yaml`; `GAME/CAMPAIGN/CHECKPOINTS/_TEMPLATE.yaml`, `GAME/CAMPAIGN/LOG/_TEMPLATE.yaml`, `GAME/CAMPAIGN/SESSIONS/_TEMPLATE.yaml` | prove whether they are native owners, coordination-only data, or unrelated to transient role control |
| `DEV/SCHEMAS/runtime-*.schema.json` and relevant catalog/entity/identifier contracts | inspect only admitted runtime/result representation and detect false authority or missing contract mapping |
| `DEV/TESTS/RUNTIME_CONTEXT_RESEARCH_CASES.md`, `test_step_5_0_contamination.py`, relevant Step-4/5, R2.3/R2.4/R2.6 and R2.7 tests | current regression evidence, missing negative/positive containment coverage and no-stale-test check |
| `DEV/TOOLS/run_maintenance_audit.py`, `DEV/TESTS/`, `.github/workflows/validate.yml` | validation/CI ownership; no implementation is authorized in this domain |

External/host documentation is not a default Step-2 source. Consult current primary
host documentation only if a proposed mapping relies on a changed platform capability;
R2.6 remains the accepted architectural applicability owner until contradicted by such
evidence.

## 7. Required Step-2 proof and exit criteria

For every material role/context/instruction surface, record:

```text
source/item
actual claim and authority class
eligibility / authority / currentness qualifiers
continuity source class and required broad/episodic/current/exact escalation; explicit exclusion of hidden reasoning and other unaccepted material
Actor phase purpose, source-Actor-private continuity boundary and `world.knowledge` non-duplication disposition
ephemeral, operational, durable, derived or explicit NO-DURABLE-RECORD disposition
architecture -> machine mapping
machine -> architecture mapping
consumer/test/evaluation route
conflict, stale, debt, implementation obligation, verification obligation or no-delta rationale
```

Step 2 must establish whether the current repository has:

- one coherent instruction/activation/rebinding route rather than a competing prompt
  architecture;
- explicit lawful typed-handoff boundaries for all material role transitions;
- continuity/history inputs that preserve role/subject/recipient eligibility, escalate to
  proper current or exact evidence when material, and never make hidden reasoning or
  unaccepted generation material durable continuity evidence;
- Actor assessments whose purpose and bounded eligible evidence are explicit, whose
  Actor-private continuity stays source-owned, and whose epistemic propositions remain
  on the `world.knowledge` path;
- a deterministic realization path for context request/profile/bundle/trace/outcome
  responsibilities, including intentional non-persistence;
- a correct explicit instruction realization of the R2.6 containment/later-uptake law;
- role-local and recipient-safe Narrator/emission behavior despite physical co-presence
  of broader material;
- bounded diagnostics/tests without hidden CoT, campaign-wide scans or data leakage;
- no incompatible current runtime/schema/catalog surface.

No human decision is requested at Step 1. If Step 2 exposes a material product,
authority, compatibility, scope or risk trade-off, stop with a decision-ready brief
rather than choosing a new architecture implicitly.
