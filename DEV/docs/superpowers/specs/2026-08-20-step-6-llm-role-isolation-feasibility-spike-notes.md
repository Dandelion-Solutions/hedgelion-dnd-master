# Step 6 — LLM Role Isolation Feasibility Spike Notes

Status: **DEFERRED FEASIBILITY-SPIKE INPUT — NOT CANONICAL ARCHITECTURE**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

## Purpose

Preserve the architecture questions, hypotheses and test agenda that must be resolved before Step 6 physically maps the six already-canonical logical LLM roles onto model invocations, chats, agents, models or orchestration infrastructure.

This artifact does not start Step 6 and does not alter the current Step-5 sequencing gate.

## Inherited Step-4 law

Step 4 already canonically defines six logical roles:

1. Interpreter;
2. Dramaturg;
3. Actor;
4. Narrator;
5. Chronicler;
6. Commentator.

A logical role is a responsibility/context/authority contract. It does **not** imply a dedicated persistent agent, process, model or model call.

The critical physical-compatibility law already fixed by Step 4 is:

> A narrower-context role SHALL NOT execute inside a physical model invocation that still contains source material ineligible for that role.

Therefore physical co-location is allowed only when effective source eligibility is compatible or the platform provides a genuine context reset/isolation boundary. Prompt-only instructions such as “forget the previous secret context and act as Narrator” are not sufficient evidence of strict isolation.

## Why a feasibility spike is required

Physical LLM topology may materially affect:

- secrecy/context isolation;
- correctness and spoiler resistance;
- number of model calls per gameplay turn;
- latency;
- token consumption and cost;
- failure/retry semantics;
- product/deployment requirements;
- whether the baseline runtime can work in ordinary ChatGPT without an external orchestration service.

This should be measured before selecting an architecture.

## Preliminary hypotheses — MUST BE REVERIFIED AT SPIKE TIME

These are working hypotheses, not canonical product facts.

### H1 — One ordinary ChatGPT conversation is not a strict role-isolation boundary

If one physical model invocation has already received Dramaturg-only or other role-ineligible source material, changing role instructions later in the same physical context does not prove that the narrower role can no longer access or be influenced by that material.

Expected implication: one-chat/same-context execution may support compatible-role co-location, but cannot claim strict isolation between incompatible eligibility envelopes without a platform-provided reset/isolation primitive.

### H2 — Multiple visible ChatGPT chats are not automatically an acceptable runtime architecture

Even if separate chats appear more isolated operationally, HDM must not assume that manually maintaining six user-visible chats is a supported or desirable runtime orchestration mechanism.

The spike must also reverify current Project/workspace memory semantics and whether cross-chat context can be inherited or referenced.

### H3 — Independent API model invocations are the strongest current candidate for deterministic context isolation

A runtime-controlled orchestrator can construct each role request from a deterministic Context Assembler and send only the role-eligible bundle into a fresh/independent model invocation.

The spike must verify the exact current API state/conversation semantics, including how to prevent previous-response/conversation context from crossing a role boundary.

### H4 — Agent frameworks do not remove the need for HDM Context Assembler

Agent handoff/tool abstractions may simplify orchestration, but HDM must verify what conversation/history/context is forwarded by each mechanism. No framework-level “agent” label may be treated as proof of information isolation.

Typed role results may cross role boundaries; raw prior-role source contexts may not unless independently eligible for the receiving role.

### H5 — Six logical roles do not imply six calls per turn

The desired physical topology is the **minimum number of invocations that preserves the logical role and context-isolation contracts**.

Potential optimization dimensions to test:

- compatible roles co-located in one invocation;
- roles invoked only on demand;
- Dramaturg/preparation less frequently than ordinary gameplay turns;
- Chronicler only when Story work is required;
- Commentator only in its enabled/requested mode;
- separate Narrator call only when its narrower context requires isolation;
- model specialization only where measured quality/cost justifies it.

## Required deployment profiles to test

At minimum compare:

### Profile A — Plain ChatGPT / one conversation

Questions:

- can role-compatible phases be co-located safely?
- can any genuine context reset be obtained inside the same conversation?
- what guarantees are impossible to claim?
- what degraded/baseline product profile remains useful without strict isolation?

### Profile B — Plain ChatGPT / multiple conversations or project chats

Questions:

- is there any programmable way for the active runtime to orchestrate the other conversations?
- does project/workspace memory create cross-chat contamination risk?
- what manual user burden would this impose?
- is this viable only as a test harness rather than product architecture?

### Profile C — External OpenAI API orchestration

Questions:

- can every incompatible role receive a fresh independent invocation with only its deterministic role bundle?
- exact conversation/previous-response/reset semantics;
- latency and token cost for realistic HDM turns;
- failure/retry/idempotency handling;
- whether one orchestrator call graph can remain compatible with the deterministic core and persistence architecture.

### Profile D — Agent framework / workspace-agent backend

Questions:

- exact handoff history/context forwarding behavior;
- whether agents-as-tools or equivalent isolated calls are stronger than conversational handoffs;
- what capabilities require paid/API/workspace tiers;
- whether this should be an optional deployment backend rather than the baseline runtime.

## Canary-isolation evaluation design

Do not judge isolation only from normal-looking prose.

Use explicit canary contamination tests.

Example:

```text
Dramaturg context contains:
    SECRET_CANARY_X = unique high-entropy fact/string

Narrator eligibility excludes SECRET_CANARY_X.
```

Then test repeatedly whether the Narrator phase can:

- reproduce the canary directly;
- answer adversarial questions that require it;
- alter choices/prose in a way statistically attributable to the hidden canary;
- recover it through role-confusion/prompt-injection attempts;
- leak transformed/encoded forms;
- reveal information only when a typed eligible result intentionally carries the relevant fact across the boundary.

Test both positive and negative controls.

## Physical Role Compatibility Matrix

Before selecting topology, classify every role pair/group by source eligibility.

For each pair record:

- common eligible source set;
- sources eligible only to role A;
- sources eligible only to role B;
- whether typed A -> B output is allowed;
- whether a genuine context reset is required;
- whether physical co-location is therefore legal.

Do not infer compatibility merely because roles happen to use the same model.

## Step-6 design sequence recommended after the spike

A later Step-6 agenda should expose the LLM work explicitly rather than hiding it under one orchestration bullet. Candidate sequence:

```text
6.x.0  Role Isolation Feasibility Spike
6.x.1  Physical Role Compatibility Matrix
6.x.2  Invocation / Context-Reset Topology
6.x.3  Typed Role Handoff Contracts
6.x.4  Model Assignment / Specialization
6.x.5  Invocation Policy and Conditional Calls
6.x.6  Context / Cache Strategy
6.x.7  Token / Latency / Cost Budget
6.x.8  Failure / Retry / Degradation Semantics
6.x.9  Role-Isolation Adversarial Evals
6.x.10 Final Physical LLM Orchestration Architecture
```

Exact numbering must be reconciled with the final Step-6 roadmap when Step 6 becomes active.

## Product decision that the spike must support

The human architect will eventually need decision-ready evidence on at least:

1. whether strict cross-role isolation is mandatory for the baseline HDM product or an enhanced deployment profile;
2. whether ordinary ChatGPT can support an acceptable baseline profile without falsely claiming strict isolation;
3. whether an external API/orchestrator is required for full role isolation;
4. acceptable latency/cost/complexity for the required guarantees;
5. whether any role pairs can safely share a physical invocation.

The spike must not present raw platform choices without a recommendation based on measured isolation, quality, latency, cost and operational complexity.

## Reverification rule

OpenAI/ChatGPT/API/agent capabilities and pricing are time-sensitive. Before Step 6 relies on any specific platform behavior, re-read current official OpenAI documentation and run direct feasibility experiments against the actual target environment. Do not inherit August 2026 product assumptions as permanent architecture facts.
