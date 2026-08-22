# HDM Host-Platform Feasibility Comparative Research

**Status:** RESEARCH INPUT — NON-NORMATIVE / NOT CANONICAL  
**Date:** 2026-08-22  
**Scope:** ChatGPT / OpenAI consumer host, Claude consumer host, Perplexity consumer host, API-controlled reference  
**Purpose:** establish platform capability envelopes and architecture-killing constraints before the second HDM architecture round.

---

## 0. Correct HDM deployment premise

This study does **not** assume or seek one shared AI group chat.

The multiplayer premise is:

```text
Player A -> own machine -> own AI chat/session/agent/history
Player B -> own machine -> own AI chat/session/agent/history
Player C -> own machine -> own AI chat/session/agent/history
                              |
                              v
                     shared GitHub frontier
```

Each player owns a separate conversational host context. GitHub remains the current shared campaign/live convergence and authority surface unless a later explicit architecture decision supersedes that choice.

Therefore platform multiplayer feasibility is mainly about:

1. whether one player's host can safely and efficiently realize HDM's logical LLM roles;
2. whether that host can read/write and synchronize the GitHub-backed shared world correctly;
3. whether player-local auxiliary work can be executed inline, on demand out of band, or on a schedule;
4. whether host-local runtime/storage can improve working-state behavior without silently becoming shared authority or a portability trap.

A platform's collaborative-project or group-chat features are not treated as the target multiplayer transport.

---

## 1. Existing HDM constraints that drive this study

The current architecture already defines six **logical** LLM roles:

1. Interpreter;
2. Dramaturg;
3. Actor;
4. Narrator;
5. Chronicler;
6. Commentator.

A logical role is a responsibility/context/authority contract, not a promise of one process, persistent agent, model, or physical model call per role.

The inherited isolation law is:

> A narrower-context role must not execute inside a physical model invocation that still contains source material ineligible for that role.

Prompt-only role switching is therefore not evidence of strict isolation. The physical target remains the **minimum invocation topology that preserves role/context eligibility**.

The platform study also carries forward these HDM concerns:

- deterministic Context Assembler and role-specific source eligibility;
- hidden/private auxiliary generation;
- pre-player-visible disclosure safety;
- stable invocation/message/retry identity;
- deterministic GitHub publication and CAS/recovery behavior;
- authenticated acting principal where the host can supply it;
- player-local working state and possible embedded storage;
- multiplayer concurrency through the shared GitHub frontier;
- token/latency/cost;
- failure/retry/degradation;
- observability/testability;
- portability and host-magic dependence.

The second-round external idea dossier adds pressure for actor cognition, layered memory, history-aligned state, context tracing, selective retrieval, asynchronous Chronicler work and other role-like auxiliary operations. This study evaluates whether hosts can physically support those patterns; it does not accept them as architecture.

---

## 2. Evaluation method

### 2.1 Evidence labels

- **DOCUMENTED** — current first-party documentation explicitly supports the claim.
- **INFERRED** — the documented primitives make the claim plausible, but the exact HDM guarantee is not documented.
- **UNKNOWN** — current documentation does not establish the claim.
- **REQUIRES PROBE** — a hands-on canary/failure/latency test is required before architecture may rely on it.

### 2.2 Capability outcome labels

For every important HDM capability distinguish:

1. **Native** — host exposes the primitive directly.
2. **Thin adapter** — feasible with a small host/plugin/MCP adapter.
3. **External service** — feasible only if substantial orchestration is moved outside the consumer host.
4. **Unreliable / unsupported** — cannot currently support the required guarantee.
5. **Architecture consequence** — what HDM must change, preserve, degrade or profile.

### 2.3 Research dimensions

The study covers all previously agreed dimensions:

1. LLM/context/role orchestration;
2. runtime substrate / local state / persistence;
3. GitHub, MCP, tools and external integration;
4. identity, security, disclosure and credentials;
5. multiplayer/concurrency under the per-player-chat + shared-GitHub topology;
6. failure semantics, recovery, retry/idempotency and observability;
7. scheduling/background/parallel work;
8. caching and actual-context inspectability;
9. streaming and pre-visible staging;
10. model routing and heterogeneous models;
11. testability and reproducible evaluation;
12. resource ceilings, latency, rate limits and cost;
13. data ownership/export/migration;
14. operational burden;
15. graceful degradation;
16. capability maturity/stability and host-magic dependence.

---

# 3. Core question: multiple LLM roles inside one player's host

This is the most important near-term feasibility question.

## 3.1 ChatGPT

### Ordinary Chat

**Current evidence:** no current public consumer documentation exposes a primitive by which one normal text chat can instantiate several user-defined, separately-contexted subagents and obtain their typed results invisibly inside the same gameplay turn.

Compatible logical responsibilities can be co-located in one model invocation, but that does not solve incompatible source eligibility. A later instruction such as "now be Narrator and forget the secret" is not a context reset.

**Status:** strict role isolation in one ordinary Chat conversation = **UNKNOWN / not exposed**.

### ChatGPT Work

Work is a longer-running agentic surface that can use files/apps, execute extended tasks, continue in the background and integrate with Scheduled Tasks. Public Work documentation does not currently expose a user-definable subagent topology comparable to Claude Cowork plugins/subagents or Perplexity Computer Skills.

**Status:** user-controlled same-session role subagents = **UNKNOWN**.

### Enhanced managed-workspace surfaces

Two stronger surfaces exist, but they are not the ordinary personal baseline:

- ChatGPT Voice in Work/Codex on supported Business/Enterprise/Edu desktop workspaces can start, steer and **coordinate multiple agents through one conversation**, including across active conversations/projects.
- ChatGPT Workspace Agents on Business/Enterprise can be separately configured with models, tools, files, MCPs, memory and schedules, and can be invoked from a normal ChatGPT conversation with `@agent-name`.

These facts establish that the platform has multi-agent infrastructure. They do **not** establish that a normal HDM text gameplay turn can programmatically dispatch several role-isolated nested agent calls with deterministic context bundles and typed handoffs.

**Architecture consequence:** ChatGPT currently remains the weakest documented consumer surface for strict, inline, user-configurable physical role orchestration. It needs direct product probes before one-chat strict isolation can be claimed.

---

## 3.2 Claude

### Ordinary Claude Chat

Plugins can be installed in Chat, but Anthropic explicitly states that plugin **sub-agents and hooks run only in Cowork**; in ordinary Chat they are unavailable/grayed out.

**Status:** ordinary Chat as a user-defined subagent execution surface = **NO, documented for plugin subagents**.

### Claude Cowork

Cowork is the first strong consumer candidate for the HDM problem.

Current first-party documentation states that Cowork:

- breaks complex work into subtasks;
- coordinates multiple workstreams in parallel;
- can coordinate several subagents simultaneously;
- supports plugins that bundle skills, connectors and sub-agents;
- is available to paid plans, including Pro;
- keeps the work in one Cowork session that the user can steer.

This is qualitatively different from a scheduled background task. The main Cowork task can dispatch subagents during the active session and receive their results before producing the final output.

**Documented capability:** same-session parallel subagent orchestration = **YES**.

**Still unproven for HDM:**

- whether a custom subagent can be guaranteed a genuinely fresh source context rather than inheriting parent material;
- exact parent -> child context forwarding;
- whether tools can be allow/deny-scoped per role;
- whether model assignment can be fixed per subagent;
- whether handoff output can be restricted to a typed schema rather than prose;
- whether a Narrator canary remains inaccessible after a secret-bearing Dramaturg/Actor subagent ran;
- invocation count, latency and usage under realistic gameplay.

**Architecture consequence:** Claude Cowork is currently the strongest documented consumer-host candidate for realizing multiple logical roles without requiring a bespoke API application, but strict isolation remains **REQUIRES PROBE**.

---

## 3.3 Perplexity

### Ordinary Ask/Search

Ordinary Ask/Search is not the interesting physical orchestration surface for this study.

### Perplexity Computer + Skills

Perplexity's current Computer Skills documentation is unusually explicit:

- a Skill is more than stored instructions; it **deploys agents**;
- Computer dispatches dedicated subagents for the work;
- several subagents often run in parallel;
- they report back to the orchestrator;
- Skills activate **on demand based on the current query**;
- custom Skills can be created and reused in future Computer conversations;
- multiple Skills and their agents can collaborate in one task.

Therefore an HDM-like active Computer conversation can, at least at the product level, trigger specialist agents inside the current task rather than waiting for a scheduled run.

**Documented capability:** on-demand same-conversation parallel subagents = **YES**.

**Still unproven for HDM:**

- exact child-context isolation;
- deterministic source bundles per role;
- exact tool permissions per subagent;
- exact helper-model selection/control;
- typed-only handoffs;
- canary isolation from secret-bearing roles;
- predictable invocation/cost topology instead of host-owned adaptive orchestration.

**Architecture consequence:** Perplexity Computer is another serious one-session multi-role candidate. Compared with Claude, its orchestration appears more strongly host-owned and adaptive; this may help quality but weakens deterministic topology claims until probed.

---

## 3.4 API-controlled reference

With an HDM-controlled API orchestrator, each logical role can receive an independently constructed request containing only its eligible Context Assembler bundle. Calls can be sequential, parallel, conditional, cancelled or retried according to HDM policy.

**Status:** full physical control = **YES by construction**, subject to chosen provider API semantics.

This profile remains the control case that separates a **consumer-host limitation** from a fundamental model limitation. It is not an automatic product recommendation.

---

# 4. Background, scheduled and on-demand auxiliary work

This is distinct from inline role orchestration.

A Chronicler is the clearest example: it may be useful after a scene or persistence boundary, but it does not necessarily belong in the latency-critical Narrator turn.

## 4.1 ChatGPT Scheduled Tasks

Current documentation establishes:

- one-off and recurring scheduled tasks;
- monitoring tasks;
- runs can occur while the user is offline;
- maximum recurring frequency: **once per hour**;
- Plus currently allows up to 5 active tasks; Pro up to 15;
- each task is associated with a task chat; deleting the associated chat pauses it;
- a task created in a Project that has files **cannot access those Project files**;
- Tasks do not currently support GPTs;
- current Scheduled Tasks documentation does not expose webhooks;
- the current Scheduled page documents management/edit/pause/resume, but not a general "run this stored scheduled task now" execution primitive.

Therefore:

- **periodic Chronicler / maintenance:** possible;
- **scene-boundary immediate Chronicler:** not naturally solved by Scheduled Tasks;
- **sub-hourly recurring maintenance:** impossible through Scheduled Tasks;
- **same-gameplay-turn hidden role:** not what Scheduled Tasks are.

An immediate out-of-band Work task can of course be started manually, but that is a separate Work thread/task rather than a hidden nested call in the gameplay chat.

**HDM implication:** ChatGPT Scheduled Tasks are a fallback for coarse periodic consolidation, not a good primary physical mapping for role orchestration.

## 4.2 Claude Cowork Scheduled Tasks

Current documentation establishes:

- available to paid Cowork plans;
- schedules include hourly, daily, weekly, weekdays and **manual**;
- saved scheduled tasks can be **run on demand**;
- **each run is its own Cowork session**;
- remote runs continue while the device sleeps;
- runs can use Cowork connectors, skills and plugins;
- optional model and folder can be configured.

Therefore Claude exposes two different useful mechanisms:

```text
inline active gameplay work
    -> Cowork subagents inside the current session

out-of-band Chronicler / maintenance
    -> saved scheduled task
    -> run manually/on-demand after a scene
    -> separate Cowork session
```

This is currently much closer to the desired HDM split between latency-critical roles and auxiliary asynchronous work.

## 4.3 Perplexity Computer Scheduled Tasks

Current documentation establishes:

- recurring cadence no more frequent than **once per hour**;
- hourly/daily/weekdays/weekly/monthly/custom;
- each Computer conversation can own up to 15 scheduled tasks;
- scheduled work can use the same tools/connectors/subagents as ordinary Computer work;
- most background runs start a **fresh isolated agent with no prior conversation context**;
- tasks that require creator-conversation context or richer attended capabilities may run attended instead;
- each scheduled run consumes Computer credits;
- current task-management documentation does not document a generic "run now" action.

For immediate scene-boundary work, the stronger Perplexity primitive is therefore not scheduling but an **on-demand Skill/subagent inside the current Computer task**.

## 4.4 API-controlled

No platform cadence floor is required. HDM can trigger:

- inline calls during the turn;
- immediate post-scene jobs;
- queue-backed asynchronous calls;
- cron/scheduled work;
- condition/event-driven work.

The main constraints become provider rate limits, cost and the operational system HDM chooses to own.

---

# 5. Role-orchestration comparison

| Need | ChatGPT personal baseline | Claude Pro / Cowork | Perplexity Pro / Computer | API-controlled |
|---|---|---|---|---|
| Compatible logical roles in one main call | Yes | Yes | Yes | Yes |
| User-defined nested subagents in ordinary chat | Not documented | Plugin subagents do not run in ordinary Chat | Not the Ask/Search model | Yes |
| Same active session can dispatch subagents | Work: not documented | **Yes, Cowork** | **Yes, Computer Skills** | Yes |
| Parallel subagents | Enhanced/workspace infrastructure exists; personal text Work contract unclear | **Yes, documented** | **Yes, documented** | Yes |
| Custom reusable role definitions | Instructions/plugins, but nested execution unclear | **Plugins with subagents** | **Custom Skills** | Yes |
| Strict fresh-context guarantee per role | Not documented | Requires canary probe | Requires canary probe | Yes by explicit request construction |
| Typed-only role handoff | Not documented | Requires probe | Requires probe | Yes |
| Exact model per role | Limited/host-owned on consumer surface | Needs plugin/subagent probe | Mostly host-owned/adaptive | Yes |
| Immediate post-scene auxiliary work | Manual/new Work task or inline same model | Inline subagent or separate scheduled task run on demand | Inline Skill/subagent | Yes |
| Recurring background minimum cadence | 1 hour | Hourly built-in; manual/on-demand also supported | 1 hour | Architecture-owned |
| Background run shares current gameplay session | No | No for scheduled task; yes for inline subagents | Usually no for scheduled task; yes for inline Skills | Choice of HDM |

---

# 6. Runtime substrate and player-local state

The current architecture still assumes GitHub as the shared authority/convergence point. Local host storage is therefore evaluated first as **player-local working state/cache/index/runtime substrate**, not as a replacement shared canon.

## 6.1 ChatGPT Work

Desktop Work can open a local folder/project and read/write files with permission. Local Work outputs remain on that machine unless explicitly shared.

This makes host-local files plausible, but current public documentation does not establish SQLite-specific properties such as:

- stable process lifetime;
- file locking;
- WAL;
- concurrent access;
- crash recovery;
- whether the execution environment can keep a DB open across turns/sessions.

**SQLite status:** **INFERRED POSSIBLE / REQUIRES PROBE**.

## 6.2 Claude Cowork

Claude documents both remote and local execution:

- remote sessions use a per-session **temporary isolated sandbox**, destroyed when the session ends;
- sessions/files saved to the Claude account are separate from arbitrary sandbox persistence;
- local desktop sessions run the agent loop on-device and execute code in an isolated local VM;
- connected local folders are accessible according to user permissions.

A SQLite file in a connected local folder may therefore be feasible in a local profile, but the exact DB locking/lifecycle/restart behavior still needs direct testing.

A SQLite DB created only inside a remote Cowork temporary sandbox must **not** be treated as durable authority.

**SQLite local status:** **INFERRED POSSIBLE / REQUIRES PROBE**.  
**Remote sandbox DB as durable state:** **NO**.

## 6.3 Perplexity

Perplexity has the strongest explicit local-language evidence:

- desktop app can read/create/change files in permitted folders;
- current local MCP support on macOS explicitly includes interaction with **files, databases, applications and services**;
- local MCP server is launched on the user's machine;
- Windows/Mac desktop local-file surfaces exist, although local MCP is currently macOS-only.

This is strong evidence that a player-local SQLite/MCP runtime is physically plausible on macOS.

Still required before relying on it:

- persistence over app/OS restart;
- locking/WAL behavior;
- two concurrent agent/tool callers;
- crash while transaction active;
- migration/backup/export;
- behavior when desktop helper/MCP restarts.

**SQLite status:** **strongest consumer candidate, but still REQUIRES PROBE for HDM guarantees**.

## 6.4 API-controlled

HDM owns the runtime and can choose SQLite/Postgres/other storage under normal application semantics.

---

# 7. GitHub as shared multiplayer convergence

Because each player has their own host, the platform does not need to provide shared group-chat state. It needs reliable per-user access to the GitHub-backed shared world.

## ChatGPT

The current HDM development environment proves that GitHub write-capable apps can exist on ChatGPT. However, generic **custom full MCP write/modify** support is currently documented for Business/Enterprise/Edu; personal Pro custom MCP remains read/fetch in developer mode. Published app capabilities and plan availability must be evaluated separately from private custom MCP development.

This makes consumer deployment/distribution of an HDM-specific GitHub write bridge a material feasibility question.

## Claude

Remote custom MCP connectors are documented for Free/Pro/Max/Team/Enterprise. They can connect Claude to arbitrary tools and can take actions in those services.

This gives Claude a relatively clean path to an HDM/GitHub bridge if direct GitHub capabilities are insufficient.

## Perplexity

The built-in GitHub connector is documented for Pro/Max and can perform at least some GitHub actions. Perplexity also supports custom API credentials in Computer and local MCP on macOS. Remote MCP is announced but not yet generally available.

The connector requests broad GitHub permissions, so HDM must verify the exact available action vocabulary and whether it can implement deterministic branch/ref publication semantics rather than assuming permission breadth equals semantic suitability.

## API-controlled

GitHub access can be implemented directly by the HDM runtime using explicit least-privilege credentials and exact publication logic.

---

# 8. Multiplayer implications under the correct topology

The platform comparison must test the following, but **per player host**, not via a shared AI conversation:

- authenticated user -> stable `PLAYER_` binding;
- player-specific GitHub credentials/authority;
- stale-head detection;
- race-sensitive publication;
- shared live-epoch synchronization;
- player-local current scene/context;
- split-party: different players may intentionally hold different scene/context projections;
- recipient/PC-specific knowledge and secrets;
- rejoin/catch-up from the shared GitHub frontier;
- no action for another player's PC merely because that PC appears in context;
- observational finality after shared publication/visibility;
- no use of network/tool arrival order as fictional chronology.

The key architecture question is whether the host can support **one player's** private and role-scoped execution while the deterministic/shared state remains synchronized through GitHub.

---

# 9. Remaining cross-platform dimensions and current posture

## 9.1 Context control / inspectability

Consumer hosts still do not generally expose a complete deterministic trace of the exact final model context after host memory, project retrieval, system layers and truncation.

This is a major difference from API-controlled orchestration.

**Required probe:** canary contamination + source-eligibility tests per physical role.

## 9.2 Pre-visible staging / streaming

No consumer-host documentation reviewed so far proves a universal HDM-controlled boundary that guarantees arbitrary assistant prose is fully generated, deterministically validated by HDM and only then emitted to the player.

A safer alternative worth evaluating in Round 2 is to make the player-facing Narrator receive only a **recipient-safe projection** in the first place. This is a research hypothesis, not a superseding decision.

## 9.3 Failure / retry / idempotency

For every host test:

- tool succeeded but model/host timed out;
- write acknowledged ambiguously;
- user retries/regenerates;
- host repeats tool invocation;
- model fails after mutation but before narration;
- local execution process restarts;
- scheduled/background job retries;
- another player's GitHub frontier advances concurrently.

Provider or host message IDs are not automatically equivalent to HDM invocation identity.

## 9.4 Caching

Consumer-host prompt caching is largely host-owned. API providers expose more direct cache controls/usage telemetry.

For multi-role HDM, cache behavior may materially affect whether isolated calls are affordable, especially when each role shares a large stable world/rules prefix.

## 9.5 Model routing

Claude Cowork and Perplexity Computer may internally route or parallelize models/agents, but host-owned adaptive routing is not the same as HDM-owned role assignment.

The study must distinguish:

- "the platform can use multiple models";
- "HDM can choose the exact model for role R";
- "HDM can prove the role saw only eligible context."

## 9.6 Testability

Before accepting a consumer profile, build adversarial probes for:

- secret canary isolation;
- tool/write idempotency;
- Retry/Edit;
- two-player unique-object race through GitHub;
- split-party context contamination;
- scene-boundary Chronicler;
- local SQLite crash/restart;
- host project-memory contamination;
- exact latency/cost per realistic turn.

A surface that works interactively but cannot be reproducibly regression-tested is a weak foundation for correctness-sensitive architecture.

## 9.7 Capability maturity

Every relied-upon feature must be tagged stable/beta/preview, plan, platform and region. Cowork cloud/mobile, ChatGPT full MCP, Workspace Agents, Perplexity Computer/Skills and local MCP are moving quickly in 2026. Feature presence today is not a permanent contract.

---

# 10. Preliminary comparative conclusions

These are **research conclusions, not architecture decisions**.

### C1 — The original hard problem remains role orchestration inside one player's host

The corrected multiplayer premise does not reduce the Step-4 isolation problem. Each player's agent still needs to map six logical roles onto a small number of legal physical invocations.

### C2 — Claude Cowork materially changes the feasibility landscape

It is currently the strongest documented consumer surface for explicit same-session parallel subagents on an individual paid plan. This deserves direct HDM canary/context/handoff experiments before assuming an external API orchestrator is mandatory.

### C3 — Perplexity Computer is also a serious role-orchestration candidate

Custom Skills can deploy on-demand specialist agents, including parallel agents, in the current Computer conversation. Its larger risk is host-owned adaptive orchestration: excellent capability is not automatically deterministic capability.

### C4 — ChatGPT's personal baseline still lacks an equally explicit inline subagent primitive

Scheduled Tasks help only with coarse out-of-band work because of the one-hour recurring floor and separate-task semantics. Work is agentic but the public contract does not currently expose role-configurable nested subagents. Stronger multi-agent controls exist in managed-workspace surfaces and should be tracked separately.

### C5 — Scheduled/background and inline role work must stay separate in the architecture

A platform can be weak at scheduled tasks but strong at inline subagents, or vice versa. Chronicler-like work may have multiple physical profiles:

```text
inline after scene
manual/on-demand auxiliary session
hourly/daily background consolidation
API/event-driven job
```

They must not be collapsed into one "background agents: yes/no" checkbox.

### C6 — GitHub remains a valid shared-convergence hypothesis

Nothing in the first platform pass requires abandoning the existing per-player-chat + shared-GitHub topology. Host-local SQLite or agent sandboxes are best treated as optional player-local working infrastructure until a separate architecture decision changes authority.

### C7 — API-controlled remains the control case, not the default winner

Its purpose is to prove which requirements are possible when HDM owns context and invocation topology. A consumer host that can satisfy enough of those requirements with low user friction may remain the better product deployment.

---

# 11. Required next probes

Documentation is no longer enough for the following questions.

## Role isolation

For Claude Cowork and Perplexity Computer, define custom subagent/Skill canaries:

```text
secret-bearing role:
    SECRET_CANARY_X = high-entropy fact

Narrator eligibility:
    excludes SECRET_CANARY_X
```

Test direct extraction, adversarial extraction, transformed leakage and behavioral influence. Positive control passes the fact only through an explicit typed eligible handoff.

## Invocation topology

Measure for one realistic HDM turn:

```text
player input
-> Interpreter
-> optional Dramaturg/Actor work
-> deterministic mechanics/tool work
-> Narrator
-> GitHub publication
-> optional Chronicler
```

Record physical calls/subagents, wall-clock latency, visible intermediate UI, token/credit usage and failure behavior.

## Background work

Test:

- ChatGPT: whether any current Work/Scheduled surface can fire an existing auxiliary job immediately from gameplay without hourly scheduling and without manual chat navigation;
- Claude: manual/on-demand scheduled task handoff from gameplay state through GitHub;
- Perplexity: inline Skill vs scheduled task, including context difference between fresh background and attended runs.

## GitHub

For each consumer host:

- authenticate as one player;
- read exact campaign ref;
- prepare deterministic base-derived write;
- non-force CAS/update equivalent;
- handle stale ref;
- recover ambiguous acknowledgement;
- repeat the same intent and prove no double application.

## Local storage

Where local file/database access exists:

- create SQLite DB in persistent permitted folder;
- WAL mode;
- commit/read across session restart;
- concurrent readers/writer;
- kill process mid-transaction;
- restart host/helper;
- validate integrity and recover.

---

# 12. Primary current documentation consulted

## OpenAI / ChatGPT

- Scheduled Tasks in ChatGPT: https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt
- ChatGPT Work and Codex: https://help.openai.com/en/articles/20001275/
- ChatGPT Voice: https://help.openai.com/en/articles/20001274
- ChatGPT Workspace Agents: https://help.openai.com/en/articles/20001143/
- Developer mode and MCP apps: https://help.openai.com/en/articles/12584461-developer-mode-and-full-mcp-connectors-in-chatgpt-beta

## Anthropic / Claude

- Get started with Claude Cowork: https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
- Use plugins in Claude: https://support.claude.com/en/articles/13837440-use-plugins-in-claude
- Schedule recurring tasks in Claude Cowork: https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork
- Claude Cowork architecture overview: https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview
- Custom connectors using remote MCP: https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp

## Perplexity

- What is Computer?: https://www.perplexity.ai/help-center/en/articles/13837784-what-is-computer
- How to use Computer Skills: https://www.perplexity.ai/help-center/en/articles/13914413-how-to-use-computer-skills
- Scheduled Tasks in Computer: https://www.perplexity.ai/help-center/en/articles/11521526-perplexity-tasks
- Local and Remote MCPs: https://www.perplexity.ai/help-center/en/articles/11502712-local-and-remote-mcps-for-perplexity
- Work with Local Files and Folders: https://www.perplexity.ai/help-center/en/articles/19800004-work-with-local-files-and-folders
- Connecting Perplexity with GitHub: https://www.perplexity.ai/help-center/en/articles/12275669-github-connector-for-enterprise
- Custom API credentials in Computer: https://www.perplexity.ai/help-center/en/articles/20260716-using-custom-api-credentials-in-computer

---

## 13. Research status

The documentation reconnaissance has established enough evidence to justify hands-on platform probes, but **not** enough to select the second-round architecture or a winning host.

The most important unresolved gate is no longer simply "does the platform have agents?" It is:

> Can HDM prove source/context isolation, deterministic tool/state boundaries and acceptable latency/cost while those agents are orchestrated inside one player's normal host experience?
