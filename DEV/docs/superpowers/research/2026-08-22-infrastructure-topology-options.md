# HDM Infrastructure Topology Options — Research Snapshot

**Status:** RESEARCH INPUT — NON-NORMATIVE / NOT CANONICAL  
**Date:** 2026-08-22  
**Purpose:** preserve the currently viable HDM infrastructure families, their known blockers, economic constraints, hypotheses, workarounds and required probes before the second architecture round.

This document is topology-focused. Platform-specific evidence and current product capability details belong in `2026-08-22-platform-feasibility-comparative-research.md`.

No option below is an accepted architecture decision.

---

# 1. Hard product constraints

The infrastructure study must respect the following product constraints.

1. HDM is a non-commercial project.
2. The baseline player experience must work within an ordinary individual consumer AI subscription in the approximate `$20/month` class.
3. Normal gameplay must have **zero marginal monetary cost per turn** beyond that subscription.
4. Baseline gameplay must not require:
   - Business / Enterprise / organization plans;
   - separate model API billing;
   - purchased task/agent/computer credits;
   - pay-as-you-go overflow;
   - automatic usage refill;
   - any other per-turn or metered inference charge.
5. Optional enhanced profiles may use more expensive capabilities, but baseline correctness and playability may not depend on them.
6. Every human player uses their own machine, their own AI host/chat/session/agent and their own conversational history.
7. HDM does not require or assume a shared multi-user AI chat.
8. The existing six LLM roles are **logical** responsibility/context/authority contracts:
   - Interpreter;
   - Dramaturg;
   - Actor;
   - Narrator;
   - Chronicler;
   - Commentator.
9. Six logical roles do **not** imply six model calls. Physical topology should use the minimum number of invocations that preserves source eligibility and role boundaries.
10. The inherited isolation requirement remains:

> A narrower-context role must not execute inside a physical model invocation that still contains source material ineligible for that role.

11. Prompt-only role switching is not a genuine context reset.
12. If HDM deploys a persistent server with its own database, that database becomes the natural shared runtime/state substrate for that deployment. GitHub is then **not required as shared campaign authority** and should be treated, if retained at all, as an optional export, backup, version-history or portability integration.

---

# 2. Cross-cutting finding: the problem separates cleanly into Core and Inference

A hosted HDM server can deterministically own almost every hard runtime concern without paying for LLM inference:

```text
HDM Server
├── authoritative campaign database
├── deterministic mechanics
├── identity / player / PC binding
├── Context Assembler
├── role eligibility and work scheduling
├── memory / retrieval / indexes
├── retry / branch / recovery state
├── multiplayer serialization / locks / CAS-equivalent transactions
├── chronology / scene frontiers
├── disclosure policy
├── background non-LLM jobs
├── observability / audit traces
└── optional export / backup integrations
```

This eliminates the need to force consumer chat sandboxes, project files or Git repositories to behave like a general-purpose database.

The remaining hard boundary is **subscription-backed inference control**:

> Can HDM cause the player's already-paid consumer AI host to execute an additional isolated model invocation with an HDM-selected context and return a controlled result, without separate API/credit billing?

A server can decide that an Actor or Dramaturg invocation is required. It cannot, merely by existing, force an ordinary consumer chat to create that invocation.

## 2.1 Important protocol dead end

A protocol-level mechanism in which an external tool/server asks the AI client to perform a completion would have been close to ideal for HDM. Current research does not establish such a mechanism as a portable consumer-host capability, and the relevant generic protocol direction is moving away from server-requested client sampling toward direct provider API calls.

Therefore the architecture must **not** assume:

```text
HDM server -> generic tool protocol -> consumer subscription -> hidden completion
```

as a portable foundation.

## 2.2 Host-native subagents remain materially different

Some consumer hosts expose their own child-agent/subagent execution surfaces. Those may provide the missing inference boundary, but they are host-specific and must satisfy all of:

- included in the ordinary subscription;
- sufficient practical quota for normal play;
- no marginal per-turn charge;
- genuine child-context isolation;
- controlled tool access;
- safe child -> parent handoff;
- acceptable latency;
- recoverable failure semantics.

Until those properties are proven, `subagents exist` is not equivalent to `HDM role isolation is solved`.

---

# 3. Option 1 — Distributed Consumer Host + GitHub

## 3.1 Shape

```text
Player A machine                 Player B machine
┌─────────────────┐             ┌─────────────────┐
│ consumer AI chat│             │ consumer AI chat│
│ HDM instructions│             │ HDM instructions│
│ local history   │             │ local history   │
└────────┬────────┘             └────────┬────────┘
         │                               │
         └──────────────┬────────────────┘
                        v
                 shared GitHub state
```

No HDM application server is required. Each player agent directly reads/writes the shared campaign repository through supported host integrations.

## 3.2 Ownership

- LLM inference: consumer host subscription.
- player-facing UI: consumer host.
- conversational history: each player's host.
- shared campaign state: GitHub.
- concurrency/publication: Git/ref/revision protocols.
- deterministic mechanics: executed through the player's runtime/tool environment.
- background work: host-native scheduling/agent surfaces where available.

## 3.3 Strengths

- smallest infrastructure footprint;
- no central HDM service to operate;
- no HDM-owned model API bill;
- user stays inside a familiar AI product;
- current repository architecture already explores deterministic Git publication and multiplayer convergence;
- campaign data is naturally exportable/versioned.

## 3.4 Main bottlenecks

### Physical LLM role isolation

The ordinary single conversation remains the dominant blocker. A tool call to GitHub or deterministic code does not create a fresh LLM context.

If a secret-bearing role and player-facing Narrator execute in one physical model context, a later prompt instruction cannot prove that the secret is inaccessible.

### GitHub is being asked to serve as a live state substrate

The design must carry complexity for:

- ref/currentness checks;
- exact-source CAS publication;
- ambiguous acknowledgements;
- multiplayer races;
- live epochs;
- partial/shared frontiers;
- higher-latency state reads/writes than a local database.

This is feasible but mechanically expensive compared with a normal transactional database.

### Host dependence

The runtime depends on whatever each consumer host exposes for:

- GitHub actions;
- write-capable custom integrations;
- local execution;
- scheduled work;
- stable IDs;
- context/project-memory behavior.

### Background work

Coarse scheduled work may be available, but current consumer surfaces commonly impose cadence/session constraints. Such mechanisms are suitable only for non-critical catch-up work.

## 3.5 Candidate workarounds

- co-locate only role-compatible logical responsibilities;
- minimize the number of privilege domains rather than mapping one call per logical role;
- ensure player-facing generation receives recipient-safe inputs where possible;
- keep Chronicler non-blocking and allow delayed catch-up;
- use typed deterministic intermediate results rather than raw hidden-role prose;
- retain GitHub-specific CAS/recovery machinery for shared state.

## 3.6 Core hypothesis

A useful baseline may exist with one main physical model invocation plus deterministic tools even if strict secret-bearing cross-role isolation is unavailable. Whether that degraded profile is acceptable is an architecture/product decision, not a feasibility fact.

## 3.7 Required research/probes

- exact role compatibility matrix;
- canary tests for same-conversation role contamination;
- host project-memory contamination;
- GitHub write idempotency under Retry/reconnect;
- realistic multiplayer race tests;
- normal-turn latency with repository round trips;
- available non-metered background work;
- whether player-safe Narrator projection removes the need for some secret-bearing stages.

---

# 4. Option 2 — Hosted HDM Core + Ordinary Consumer Chat

## 4.1 Shape

```text
Player A consumer chat ─┐
Player B consumer chat ─┼──── HDM Server
Player C consumer chat ─┘     ├── authoritative DB
                              ├── deterministic core
                              ├── Context Assembler
                              ├── memory / retrieval
                              ├── multiplayer / locking
                              ├── recovery / history
                              └── optional export / backup
```

Each player still receives LLM inference through their ordinary consumer subscription, but all shared/runtime state is centralized in the HDM service.

There is **no need for GitHub to remain authoritative shared storage** in this option.

## 4.2 Ownership

- LLM inference: player's ordinary consumer chat.
- player-facing UI: consumer host.
- shared campaign state: HDM server database.
- deterministic mechanics: HDM server.
- Context Assembler: HDM server.
- multiplayer concurrency: HDM server transactions/locking.
- memory/retrieval/indexes: HDM server.
- export/version history: optional secondary integrations.

## 4.3 Strengths

This option removes most physical-host constraints from the core architecture:

- normal transactional DB is available;
- HOT state is cheap and local to the server;
- authoritative concurrency can use ordinary database semantics;
- deterministic Context Assembler is centralized;
- player/PC identity can be server-owned;
- retry/idempotency can use HDM invocation IDs;
- memory/retrieval can be indexed normally;
- observability can be first-class;
- background deterministic jobs can run at arbitrary cadence;
- GitHub-specific live-state complexity becomes optional rather than foundational.

It also preserves the key economic advantage:

- model inference remains inside the player's already-paid consumer subscription;
- the HDM server itself does not need model API billing.

## 4.4 Dominant blocker

All LLM reasoning still occurs in the **same physical consumer conversation** unless the host provides another invocation primitive.

The server can say:

```text
next_required_role = Actor
role_context = <secret actor-only packet>
```

but an ordinary main chat that receives that packet now contains Actor-only material. The server cannot later make the same physical context genuinely forget it before Narrator execution.

The server therefore controls **what should be called**, but not **whether the host creates a new isolated model call**.

## 4.5 What the server can still improve

The hosted core can aggressively shrink the amount of LLM-owned work:

- deterministic mechanics move entirely server-side;
- retrieval and source selection move server-side;
- role eligibility is deterministic;
- state mutation validation is deterministic;
- LLMs return bounded semantic proposals/results;
- player-facing Narrator receives a safe projection wherever possible.

This may reduce the physical LLM requirement from `six roles` to a much smaller number of privilege domains.

Possible research-only grouping:

```text
PLAYER-SAFE DOMAIN
├── Interpreter-compatible work
├── Narrator
└── Commentator when safe/enabled

SECRET / INTERNAL DOMAIN
├── Dramaturg
└── Actor where private cognition is required

NONCRITICAL ASYNC
└── Chronicler
```

This grouping is a hypothesis, not an accepted role topology.

## 4.6 Candidate workarounds

### Workaround A — no secret-bearing secondary inference in baseline

Move as much internal decision work as possible into deterministic/structured state and let the main model operate only on player-safe projections.

Risk: may materially reduce generative NPC/world agency quality.

### Workaround B — accept weaker isolation profile

Allow compatible/secret-bearing work in the main context and rely on instructions not to disclose it.

Risk: violates the current strong isolation law and requires an explicit superseding architecture/product decision.

### Workaround C — defer optional roles

Keep Chronicler and other non-critical enrichment off the latency-critical path and run them only when a non-metered host mechanism is available.

### Workaround D — promote to Option 3 when the host can spawn an isolated child

The hosted server architecture can remain the same; only the inference transport changes.

## 4.7 Core hypothesis

A centralized deterministic core may make a single-consumer-context deployment good enough if most secret/internal reasoning can be eliminated, made deterministic, or converted into safe structured proposals.

## 4.8 Required research/probes

- derive minimum physical privilege domains from the six logical roles;
- measure how often a normal D&D turn truly needs secret-bearing generative cognition;
- test whether recipient-safe Narrator packets remove pre-visible disclosure dependence;
- test ordinary chat tool-loop latency against a hosted server;
- determine whether host-visible tool results can remain opaque enough to avoid accidental contamination;
- determine whether any normal-subscription host exposes a hidden/child completion primitive after all.

---

# 5. Option 3 — Hosted HDM Core + Host-Native Isolated Subagents

## 5.1 Shape

```text
Player main chat
      │
      │ begin_turn()
      v
HDM Server
├── DB / authoritative state
├── role scheduler
├── Context Assembler
└── creates opaque role_job_id
      │
      v
main chat asks host to spawn child agent
      │
      v
isolated child/subagent
      │
      │ get_role_context(role_job_id)
      v
HDM Server
      │
      │ exact role-eligible packet
      v
child/subagent
      │
      │ submit_role_result(role_job_id, typed result)
      v
HDM Server
      │
      │ validate / commit / derive safe continuation
      v
main chat
      │
      v
player
```

The critical idea is that the server owns the job and context, while the consumer host owns the physical model invocation and charges it against the user's ordinary subscription rather than an HDM API account.

## 5.2 Ownership

- shared state/core/memory/concurrency: HDM server database.
- role scheduling and context eligibility: HDM server.
- physical child model call: consumer host.
- inference economics: consumer subscription, **only if included without marginal charges**.
- player UI/main history: consumer host.

GitHub is optional export/backup/version history only.

## 5.3 Why this option is strategically important

If it works, it gives HDM most benefits of full API orchestration without owning the inference bill:

- distinct physical contexts for incompatible roles;
- server-controlled source eligibility;
- secret material can be fetched only by the intended child;
- role outputs can be server-validated before becoming visible;
- main player chat can remain player-safe;
- the server can preserve deterministic state/authority;
- background/noncritical roles can use separate execution paths;
- each player's consumer subscription funds their own inference.

## 5.4 Opaque role-job pattern

The main conversation should ideally receive only a non-secret work order:

```text
role_job_id = abc123
role_kind = actor
```

The child obtains secret context directly from the server:

```text
get_role_context(abc123)
```

and writes its result directly back:

```text
submit_role_result(abc123, typed_result)
```

The parent should receive no secret-bearing summary. Ideally it receives only a safe completion signal or a server-produced player-safe continuation.

## 5.5 Main bottlenecks

### Child context inheritance

A host may automatically copy parent conversation context into the child. If that includes ineligible material, role isolation may fail before HDM even supplies the role packet.

### Child -> parent leakage

A host may automatically summarize the child result back into the parent context. If the child had secret material, this defeats the architecture even if the child itself was isolated.

### Tool/connector availability

The child must be able to contact the HDM server and authenticate to the same campaign/player/job while preserving role-specific authorization.

### Host-owned orchestration

The host may decide:

- how many child agents to create;
- what model they use;
- what parent context they inherit;
- what result is summarized;
- how retries happen.

This weakens deterministic topology unless the platform exposes enough control.

### Economic endurance

This option is baseline-eligible only if child-agent execution:

- is included in the ordinary individual subscription;
- does not consume separately purchased credits;
- does not require pay-as-you-go overflow;
- can sustain realistic multi-hour gameplay without exhausting a tiny agentic quota.

A technically perfect subagent product that has non-zero marginal cost per normal turn is **DISQUALIFIED for baseline HDM**.

Metered agent loops also introduce a bad failure mode: a task can burn attempts/quota while failing to produce a valid result. Correctness-sensitive gameplay must not expose the user to financial loss from retry loops.

### Failure semantics

Need to distinguish:

- child never started;
- child started but never fetched context;
- child fetched secret context but failed before submit;
- child submitted result but parent did not receive completion;
- host retries child automatically;
- main chat retries the same work order.

Server-owned idempotent `role_job_id` semantics can mitigate these failures, but cannot control hidden host retries unless they are observable.

## 5.6 Candidate workarounds

- use only the minimum number of isolated child calls required by privilege boundaries;
- keep compatible roles in the main player-safe call;
- make child output commit directly to the server rather than through parent prose;
- give children opaque job IDs instead of embedding secrets in parent instructions;
- server-authorize every role-context read and result write;
- make role jobs idempotent and resumable;
- make Chronicler nonblocking and degradable;
- if the included quota is too small, fall back to Option 2 rather than silently charging money.

## 5.7 Core hypothesis

The missing bridge for full HDM role isolation may be **host-native isolated child execution**, not an external model API.

If a consumer host can provide a child call with controlled inheritance, connector access and safe parent handoff inside the standard subscription, Option 3 is the strongest current candidate for the desired hybrid architecture.

## 5.8 Required research/probes

Highest-priority probe set:

1. Can a main session spawn a child on demand during the current gameplay turn?
2. Does the child receive a fresh context or inherit parent history?
3. Can inherited context be explicitly limited?
4. Can the child use the HDM server connector/tool?
5. Does the child have the same authenticated player principal?
6. Can HDM additionally authorize a role-scoped `role_job_id`?
7. Can the child fetch secret context directly from the server?
8. Can it submit a typed result directly to the server?
9. What exactly is returned to the parent after child completion?
10. Can secret canaries be kept out of the parent context?
11. Can model/tool permissions be constrained per child?
12. What happens on child retry/failure/cancellation?
13. What is realistic turns/hour and hours/month before included subscription limits are reached?
14. Does any normal-turn workload trigger purchased credits or pay-as-you-go?
15. Can a complete representative session run with all extra-usage billing disabled?

---

# 6. Option 4 — Fully Controlled HDM Service + Direct Model Inference

## 6.1 Shape

```text
custom web/mobile/desktop client
            │
            v
        HDM Server
        ├── authoritative DB
        ├── deterministic core
        ├── Context Assembler
        ├── memory / retrieval
        ├── multiplayer
        ├── role scheduler
        ├── validation / disclosure
        └── model inference layer
              ├── provider API A
              ├── provider API B
              ├── self-hosted/open model
              └── future provider adapters
```

HDM owns the full request/response pipeline.

GitHub is not required for live/shared storage. It may remain optional for export, backups, releases, portability or human-readable version history.

## 6.2 Strengths

This is the technical control case.

HDM can own:

- exact role context;
- fresh invocation boundaries;
- model per role;
- parallelism;
- cancellation;
- typed outputs;
- retry/idempotency;
- prompt/cache strategy;
- pre-visible validation;
- secret isolation;
- background calls at arbitrary cadence;
- deterministic state commit order;
- complete observability;
- automated regression testing;
- custom player UI and multiplayer UX.

The six logical roles can be mapped onto the minimum legal physical call graph without consumer-host interference.

## 6.3 Dominant blocker: economics

With commercial model APIs, every model invocation has a marginal cost paid by whoever owns the API account.

That conflicts with the baseline product constraint:

> ordinary gameplay must have zero marginal monetary cost beyond the player's normal consumer subscription.

Because HDM is non-commercial, there is no subscription revenue pool that naturally pays the inference bill.

Therefore direct commercial API inference is **not baseline-economically eligible under current constraints**.

## 6.4 Possible non-baseline variants

### User-supplied API account/key

Technically straightforward, but violates the zero-additional-cost baseline and creates onboarding/security/billing burden.

### Project-funded API

Technically straightforward, economically unsustainable for an open public player base unless usage remains tiny or external funding appears.

### Self-hosted/open-weight inference

Could remove per-request provider billing if adequate inference hardware already exists, but introduces:

- GPU/capacity cost;
- model quality uncertainty;
- latency;
- concurrency limits;
- model operations/updates;
- safety and isolation concerns;
- hardware requirements.

This remains a separate feasibility path, not an assumed free solution.

### Mixed inference

Use consumer-host inference for player-facing work and self-hosted/API inference only for rare internal roles.

This may reduce cost but still fails the strict baseline if a correctness-required path can generate additional charges.

## 6.5 Core hypothesis

Option 4 establishes that the HDM architecture is technically feasible when HDM owns inference. Its main value today is to distinguish **host limitations** from **fundamental engine limitations**.

It becomes a practical baseline only if inference economics change materially: flat-rate programmable inference, sufficient self-hosted hardware, sponsorship, or another zero-marginal-cost mechanism.

## 6.6 Required research/probes

- realistic model calls per normal turn after role co-location optimization;
- token/context size per role;
- latency for sequential vs parallel physical topology;
- cheapest acceptable models per role;
- realistic monthly API cost for a multi-player campaign;
- feasibility and quality of self-hosted/open-weight models for secret/internal roles;
- operational burden of provider routing/fallbacks;
- whether any provider offers a genuinely flat programmable inference allowance compatible with the baseline economics.

---

# 7. Comparative matrix

| Property | Option 1: Distributed + GitHub | Option 2: Hosted Core + One Chat Context | Option 3: Hosted Core + Isolated Consumer Agents | Option 4: Full Controlled Inference |
|---|---|---|---|---|
| HDM server required | No | Yes | Yes | Yes |
| Shared authority | GitHub | Server DB | Server DB | Server DB |
| GitHub required for gameplay | Yes | No | No | No |
| Consumer host remains player UI | Yes | Yes | Yes | Optional / no |
| Model inference paid by consumer subscription | Yes | Yes | Yes if child agents are included | No, unless self-hosted/other flat mechanism |
| Marginal HDM inference bill | None | None | None **only if included quota is sufficient** | Yes with commercial APIs |
| Deterministic DB/runtime control | Limited/distributed | Strong | Strong | Strong |
| Strict role isolation | Weak/unknown | Weak/unknown | Potentially strong, requires probe | Strong by construction |
| Server can choose exact role context | No/partial | Yes, but same model context receives it | Yes | Yes |
| Server can force new physical model call | No | No | Indirectly via host child-agent primitive | Yes |
| Pre-visible validation | Host-limited | Host-limited but safe projections possible | Potentially strong if parent handoff is safe | Strong |
| Background deterministic jobs | Host-limited | Strong | Strong | Strong |
| Background LLM jobs | Host-limited | Host-limited | Host-agent dependent | Strong |
| Multiplayer concurrency | Git/ref protocol | Normal DB semantics | Normal DB semantics | Normal DB semantics |
| Operational burden for project | Lowest | Moderate | Moderate | Highest |
| Baseline economic eligibility today | Potentially yes | Potentially yes | **Unknown; hard endurance gate** | No with paid commercial APIs |
| Main architecture risk | role isolation + Git-as-live-DB complexity | same-context isolation | host child-context/handoff/economics | inference cost / service operations |

---

# 8. Decision-relevant observations

## 8.1 A server changes the storage question completely

Once HDM owns a persistent service and database, there is no architectural reason to keep GitHub in the latency-critical shared-state path merely because earlier designs used it as the only portable durable substrate.

A server-backed profile should normally use its database for:

- current authoritative state;
- transactional multiplayer coordination;
- indexes and retrieval;
- role jobs;
- idempotency;
- recovery metadata;
- session/frontier state.

GitHub may still be valuable for:

- user-owned exports;
- human-inspectable snapshots;
- backups;
- migration/portability;
- optional long-term version history.

Those are separate responsibilities from live authority.

## 8.2 The central feasibility question is now narrower

For server-backed consumer-host profiles, persistence, concurrency and deterministic execution are ordinary engineering problems.

The hard unknown is:

> Can HDM obtain enough programmable, isolated LLM invocations from the player's already-paid consumer subscription to preserve the role/context architecture with zero marginal charge?

Option 2 answers `no additional invocation`; Option 3 attempts to answer `yes, through host-native child agents`; Option 4 answers `yes, by paying/owning inference directly`.

## 8.3 The physical role count should be minimized before judging viability

A feasibility result such as `only one isolated child invocation is practical` may still be sufficient if the role compatibility matrix proves that only one secret/internal privilege domain must be physically separated from the player-safe main call.

Therefore the next architecture round should not assume six physical calls.

## 8.4 Background roles must remain degradable where architecture allows

Chronicler-like projection/catch-up work is a good candidate for:

- delayed execution;
- coarse scheduling;
- catch-up on next session;
- optional richer deployment profiles.

Correctness-critical Interpreter/mechanics/disclosure paths must not depend on scarce or separately billed background-agent quota.

## 8.5 Technical fit and economic eligibility are independent gates

Every platform capability must be evaluated on both axes:

```text
TECHNICAL FIT
    AND
BASELINE ECONOMIC ELIGIBILITY
```

A technically excellent agent surface that requires per-turn credits is a baseline failure.

---

# 9. Research agenda by priority

## Priority A — minimum physical role topology

Before expensive platform probing, derive from current Step-4 contracts:

- role source-eligibility matrix;
- compatible role groups;
- secret-bearing privilege domains;
- typed legal role handoffs;
- which roles are conditional/nonblocking;
- minimum number of independent physical contexts required for a representative turn.

This establishes the actual requirement that platform probes must satisfy.

## Priority B — hosted-core ordinary-chat viability

Build/probe the smallest server interaction conceptually equivalent to:

```text
begin_turn
-> server returns only current safe work packet
-> model interprets
-> submit proposal
-> deterministic resolve/commit
-> server returns player-safe narration packet
-> model narrates
```

Measure how much useful gameplay survives without any secret child invocation.

## Priority C — opaque child-agent canary

On every economically eligible consumer host with a child-agent primitive:

1. parent receives only opaque role job ID;
2. child fetches a unique secret canary from HDM server;
3. child performs role work;
4. child submits typed result to server;
5. parent resumes;
6. adversarially test whether parent can recover or infer the canary;
7. inspect what child summary/handoff the host injected into parent;
8. repeat under retry/failure/cancellation.

## Priority D — subscription endurance

With all pay-as-you-go / purchased credits / refill disabled:

- run realistic gameplay turns;
- record calls/subagents per turn;
- record effective quota consumption;
- measure turns/hour;
- measure sustained multi-hour session viability;
- determine whether normal monthly use stays inside the base subscription.

Any platform that requires extra payment for normal turns is disqualified from the baseline regardless of technical quality.

## Priority E — server runtime/storage prototype feasibility

This is lower risk than the inference boundary, but still verify:

- DB transaction/locking model;
- player/campaign authentication;
- idempotent role-job API;
- websocket/SSE/polling requirements if any;
- backup/export design;
- recovery and observability;
- migration from current GitHub-centered campaign data if a server profile is later selected.

---

# 10. Current research posture

No topology is selected yet.

- **Option 1** remains the lowest-infrastructure route but carries both role-isolation risk and GitHub-as-live-state complexity.
- **Option 2** removes almost all runtime/storage complexity but does not solve physical LLM isolation.
- **Option 3** is the most interesting zero-marginal-cost full-hybrid hypothesis if a normal consumer subscription provides genuinely isolated, safe and sufficiently abundant child-agent execution.
- **Option 4** proves the desired architecture is technically realizable under full orchestration control, but commercial API inference currently violates the baseline economic requirement.

The immediate research focus should therefore be:

1. derive the minimum physical privilege topology;
2. test Option 3 child-context/handoff isolation and subscription endurance;
3. measure how capable Option 2 remains when no secret child invocation exists;
4. retain Option 4 as the control architecture and future fallback if inference economics change.

These are research recommendations only. The second architecture round must make any actual product/topology decision.