# Step 6 — Physical LLM Orchestration & Final Architecture Closure — Pre-Design Framing Working Notes

Status: **NON-CANONICAL / WORKING THOUGHTS / PRE-DESIGN FRAME**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Purpose:

> Capture the current Step-6 framing, constraints, questions and preliminary hypotheses before the formal Step-6 task brief, platform research and architecture cycle begins.

This document is intentionally **not**:

- a Step-6 task brief;
- a canonical specification;
- an owner decision record;
- an approved physical topology;
- a prompt design;
- an implementation plan;
- evidence that a particular current AI platform capability exists.

Current sequencing authority remains `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`.

Step 6 remains **NEXT / NOT STARTED** while this artifact is only exploratory framing.

Primary inherited sources to reopen during formal Step-6 work:

- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-6-llm-role-isolation-feasibility-spike-notes.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-6-repository-port-transport-feasibility-spike.md`
- Step-4 canonical role/context/information architecture
- owning Steps 3–5 canonical specifications for execution, persistence, recovery, delivery and cleanup.

---

# 1. Why Step 6 is qualitatively different

Steps 1–5 mostly established deterministic semantic ownership and correctness for:

```text
mechanical state
execution
truth / knowledge / disclosure
persistence
recovery
concurrency
chronology
Story / transcript
cleanup
```

Step 6 must place a deliberately narrow nondeterministic LLM layer on top of that architecture without allowing the LLM layer to become a second semantic authority.

The central question is therefore not merely:

> Which prompts should the roles use?

It is closer to:

> How can HDM physically realize the gameplay LLM roles, with sufficiently separated contexts and bounded nondeterminism, inside the actual target AI product and its latency/tool constraints, while every accepted semantic consequence remains governed by the deterministic architecture already closed in Steps 1–5?

Step 6 is simultaneously:

- LLM-role physical architecture;
- context-security architecture;
- latency/cost architecture;
- host/platform capability feasibility;
- typed nondeterministic-interface design;
- degradation/error design;
- quality/evaluation design;
- provider/platform portability design;
- final migration/catalog/seed closure;
- final holistic architecture review before implementation planning.

---

# 2. Current owner-provided baseline product constraints

These are current framing constraints to carry into Step-6 research. They are inputs, not yet a complete architecture.

```text
BASELINE PRODUCT SURFACE
    ordinary consumer AI chat product
    current primary target: ChatGPT

PLAN BASELINE
    current primary target: ChatGPT Plus
    no baseline dependency on Pro / Enterprise / Edu-only capability

PLAYER EXPERIENCE
    one user-visible gameplay chat

GAMEPLAY LLM ROLES
    Interpreter
    Dramaturg
    Actor
    Narrator
    Chronicler

COMMENTATOR
    separate concern / mode
    its own context and serving design
    not part of the ordinary five-role gameplay hot path

BACKGROUND EXECUTION
    no required permanently running background worker
    no correctness dependency on ChatGPT Work or long-running background agents

TURN LATENCY
    hard practical expectation: within roughly one minute including tool calls
    preferred ordinary target: roughly 20–30 seconds when feasible

IMPLICATION
    five logical roles MUST NOT be assumed to mean five heavyweight sequential model calls every turn
```

Formal Step 6 must turn these into measurable budgets and supported-profile requirements rather than leave them as prose aspirations.

---

# 3. Inherited non-negotiable semantic laws

Step 6 may choose physical topology. It may not silently renegotiate Steps 3–5 because a host implementation is inconvenient.

## 3.1 Logical role != physical model call

The six Step-4 logical roles are responsibility/context/authority contracts:

1. Interpreter
2. Dramaturg
3. Actor
4. Narrator
5. Chronicler
6. Commentator

A logical role does not automatically require:

- its own persistent agent;
- its own chat;
- its own model;
- its own model call every turn.

Physical co-location is legal only where information eligibility and output contracts permit it.

## 3.2 Narrower-context role isolation must be real

Inherited Step-4 law:

> A narrower-context role SHALL NOT execute inside a physical model invocation that still contains source material ineligible for that role.

Therefore:

```text
"forget the secret and now act as Narrator"
```

is not proof of isolation if the same physical invocation/context still contains Dramaturg-only material.

Step 6 must prove a genuine physical/context boundary for incompatible eligibility envelopes or conclude that the proposed deployment profile cannot claim that isolation level.

## 3.3 LLM prose never becomes authority by itself

Examples:

```text
Interpreter output
    -> interpreted candidate / typed input to deterministic acceptance
    != gameplay consequence by prose

Dramaturg output
    -> preparation / proposal
    != canon

Actor output
    -> NPC proposal within eligible knowledge/motivation
    != world transition

Narrator output
    -> presentation candidate
    != objective truth

Chronicler output
    -> Story draft
    != Story publication authority
    != canon
```

## 3.4 Step-5.14 physical feasibility gates remain binding

Formal Step 6 must reverify and resolve at least:

```text
SD-1 deterministic authenticated RepositoryPort
SD-2 pre-player-visible Narrator staging / validation
SD-3 stable invocation/message/retry identity sufficient for supported profile
SD-4 authenticated acting-principal + recipient/audience mapping
SD-5 genuine role-context isolation/reset
SD-6 optional live-ref deletion capability
```

Failure of a required capability means:

```text
reject / restrict / refine deployment profile
OR explicitly reopen an owning architecture decision
```

not silently weaken the semantic contract.

---

# 4. Preliminary hot-path hypothesis

The first performance hypothesis should be:

> Invoke only the minimum nondeterministic roles required by the current gameplay situation.

Do not begin from this naive pipeline:

```text
EVERY TURN:
Interpreter
 -> Dramaturg
 -> Actor
 -> Narrator
 -> Chronicler
```

A more plausible starting point is role activation by necessity:

| Role | Preliminary activation intuition | Reason |
|---|---|---|
| Interpreter | usually required for materially free-form player input | translate natural language into bounded typed intent candidates |
| Dramaturg | conditional / amortized / preparation-driven | strategic/world-development reasoning need not occur every exchange |
| Actor | conditional | only where genuine NPC agency/choice is materially unresolved |
| Narrator | normally required for player-facing prose | narrow presentation role after mechanics/information validation |
| Chronicler | deferable / opportunistic | Step 5.10 permits Story lag and queue-free pull catch-up |
| Commentator | separate mode | not ordinary gameplay hot path |

This table is **not approved architecture**. Formal Step 6 must test quality and correctness consequences.

Potential ordinary-turn forms to evaluate:

```text
A. Interpreter -> deterministic core -> Narrator

B. Interpreter -> deterministic core -> Actor -> deterministic core -> Narrator

C. Interpreter -> Dramaturg (only if needed) -> deterministic core -> Narrator

D. deterministic/simple-input path -> Narrator

E. ordinary gameplay completes with Chronicler deferred
```

The architecture should optimize for the common path, not the theoretical maximum role graph.

---

# 5. Latency must be a first-class architecture constraint

Step 6 should create an explicit per-turn latency budget before prompt design.

Conceptual decomposition:

```text
T_total =
    T_context_reads
  + T_repository_reads
  + T_interpreter
  + T_deterministic_core
  + T_optional_dramaturg
  + T_optional_actor
  + T_narrator
  + T_required_persistence
  + T_other_tool_calls
  + host/tool orchestration overhead
```

Initial product target to validate:

```text
ordinary desired    ~20–30 s
practical ceiling   ~60 s
```

Formal design should likely distinguish:

- ordinary turn;
- complicated adjudication turn;
- multiplayer contention turn;
- explicit SAVE;
- recovery/new-chat hydration;
- controlled handoff;
- Story catch-up/maintenance;
- setup/administrative operations.

A slower exceptional operation must not silently redefine the ordinary gameplay latency contract.

Measure at least:

- number of model calls per hot path;
- sequential dependency depth;
- tool-call overhead;
- context assembly/read cost;
- repository publication cost;
- model latency variance;
- structured-output regeneration rate;
- role-specific context size;
- whether any work can be safely deferred after player-visible response.

---

# 6. Physical role compatibility matrix is required

Before choosing prompts/models/topology, formal Step 6 should build a matrix for every relevant pair/group of roles.

For each pair/group record:

```text
sources eligible to all
sources eligible only to role A
sources eligible only to role B
typed A -> B information allowed?
raw-context inheritance allowed?
genuine reset required?
physical co-location legal?
quality consequences of co-location?
latency benefit of co-location?
```

The important question is not whether two roles *can be instructed* in one prompt.

It is whether they can safely share one physical invocation **without violating either role's effective information envelope**.

Pairs that deserve particular scrutiny:

- Dramaturg -> Narrator;
- Actor -> Narrator;
- Interpreter -> Narrator;
- Interpreter -> Dramaturg;
- Dramaturg -> Actor;
- gameplay roles -> Chronicler.

---

# 7. Typed nondeterministic handoffs

A strong direction is to minimize raw prose/context transfer between roles.

Prefer conceptually:

```text
eligible source bundle
    -> ROLE
    -> typed result
    -> deterministic validation
    -> next owner / role
```

Candidate result families already implied by earlier architecture include:

```text
InterpreterResult / intent candidate
DramaturgPreparation
ActorProposal
NarrationResult
StoryProjectionDraft
```

Step 6 must decide physical/structured-output realization and error semantics.

Questions:

- required vs optional fields;
- deterministic validation rules;
- reference identity requirements;
- maximum payload sizes;
- whether free-form rationale is ever machine-consumed;
- which fields may cross information boundaries;
- whether one role can return multiple alternatives;
- how invalid output is repaired without replaying accepted mechanics;
- how hidden reasoning is prevented from becoming required persistence state.

Goal: not maximum JSON, but the **minimum typed interface sufficient to keep nondeterminism outside semantic authority**.

---

# 8. Pre-player-visible Narrator boundary

This is likely one of the hardest physical problems.

The logical law requires:

```text
Narrator produces material output
    -> validate recipient eligibility / disclosure refs / secret boundary
    -> freeze supported response
    -> only then player-visible emission
```

Step 6 must test whether the baseline one-chat topology can physically realize this boundary.

Important distinction:

```text
model generation complete
!=
validated NarrationResult
!=
player-visible render
```

Mechanisms to investigate without assuming any one works:

- staged internal Narrator invocation;
- real context-isolated internal role call followed by outer rendering;
- host buffering;
- structured output generated before user-visible prose;
- platform-provided hidden/non-visible tool/model boundary.

If no such boundary exists for a proposed baseline profile, that is an architectural feasibility result, not a prompt-writing problem.

---

# 9. Context strategy is not simply "fit everything in the chat"

Step 4/5 already require deterministic Context Assembler semantics.

Step 6 must determine physical context strategy:

```text
which canonical/current sources are loaded
which Story/history summaries are eligible
which exact text is needed
which typed previous-role results are carried
which host conversation material is ignored
what is rebuilt each invocation
what may be cached
what must never cross role boundaries
```

Maintain the distinction:

```text
physically retained
indexed/discoverable
eligible for role
selected for this call
actually loaded into model context
```

Questions include:

- chat-length/context-window growth over long campaigns;
- host conversation compaction/summarization behavior;
- new-chat recovery without old-chat authority;
- Project/product memory contamination risk;
- reusable context caching;
- token cost of role-specific bundles;
- bounded retrieval policies for long campaigns.

---

# 10. Failure and degradation semantics

LLM failure should not automatically become gameplay failure.

Preliminary examples:

```text
Chronicler failure
    -> Story remains lagged
    -> gameplay continues

Dramaturg unavailable / timeout
    -> possibly play from already prepared/current world state
    -> no invention of required preparation

Actor invalid output
    -> retry / deterministic safe fallback / block specific NPC decision
    -> never silently invent canonical action from malformed prose

Narrator invalid or secret-leaking output
    -> player-visible emission blocked
    -> mechanics already accepted must not be replayed

Interpreter ambiguity
    -> clarification or bounded reinterpretation
    -> not arbitrary mechanical commitment
```

Formal Step 6 should define:

- retry budget per role;
- timeout behavior;
- model unavailable behavior;
- malformed structured-output behavior;
- safe degraded modes;
- OOC technical failure messaging;
- when a turn must stop rather than guess;
- how repeated LLM calls preserve Step-3 idempotency and fixed RNG.

---

# 11. Repository/tool transport remains part of Step 6

Step 6 is not only prompt orchestration.

Step 5.6 requires conceptually:

```text
deterministic Python/core
    owns publication semantics
        -> authenticated RepositoryPort
            -> repository transport
```

The LLM must not regain semantic ownership over Git merely because the AI product mediates tool calls.

Formal Step 6 must reverify supported profiles for:

- campaign publication;
- live exact-source CAS;
- ambiguous ACK resolution;
- current-ref reads;
- optional ref cleanup;
- acting-principal authentication;
- payload/latency limits.

Existing feasibility spike is evidence, not final architecture.

---

# 12. Host identity, Retry/Edit/Branch and recipient identity

The physical runtime must know enough identity to preserve accepted semantic laws.

Questions:

```text
Who is the current authenticated human?
Which PLAYER_ binding applies?
Which PC(s) may they control?
Which recipient/audience is Narrator serving?
What physical request corresponds to a new Interaction?
Can host Retry be distinguished from a genuinely new player action?
What happens after edit/branch from old host history?
```

Step 6 must not promise more host-history repair than Step 5.12 requires.

Cheap identity support is useful; a heavy delivery-history subsystem is explicitly not baseline debt.

For secure multiplayer, authenticated acting-principal and recipient/audience mapping remain blocking requirements.

---

# 13. Quality architecture is required

A system can preserve every authority law and still be a poor Dungeon Master.

Step 6 therefore needs evaluation criteria for the nondeterministic layer.

At least four independent eval axes:

```text
CORRECTNESS
QUALITY
ISOLATION / SECURITY
LATENCY / COST
```

Role-specific questions:

### Interpreter

- Did it correctly understand actual intent?
- Does it preserve ambiguity rather than hallucinate commitment?
- Does it distinguish OOC from in-fiction action/speech?

### Dramaturg

- Does preparation create useful possibilities rather than railroad?
- Does it respect established canon and supported temporal mechanics?
- Does it avoid gratuitous unused complexity?

### Actor

- Does NPC behavior follow its own knowledge, goals, personality and constraints?
- Does it avoid inaccessible player/DM information?
- Is behavior varied without becoming arbitrary?

### Narrator

- Is prose clear, vivid and appropriately concise?
- Does it faithfully reflect accepted mechanics?
- Does it avoid leaking ineligible information?
- Does it distinguish observation from objective truth where required?

### Chronicler

- Does Story preserve factual compatibility and claim-vs-truth distinctions?
- Does it avoid converting literary inference into recorded history?
- Does it create useful long-term campaign memory without unnecessary verbosity?

Quality affects model selection, context size and call frequency; therefore it is an architectural input, not post-implementation polish.

---

# 14. Isolation, prompt-injection and role-confusion evals

Do not evaluate role isolation by reading a few normal responses.

Use explicit canary tests.

Example:

```text
Dramaturg-only source:
SECRET_CANARY_X = high-entropy unique value

Narrator eligibility:
SECRET_CANARY_X forbidden
```

Attack the proposed topology with:

- direct requests for the canary;
- indirect questions requiring it;
- prompt injection inside player text;
- encoded/transformed leakage attempts;
- role-confusion instructions;
- requests to summarize hidden context;
- adversarial tool output containing instructions;
- repeated calls after role changes;
- positive controls where typed eligible handoff intentionally exposes a permitted derived fact.

Distinguish:

```text
prompt compliance
from
actual context isolation
```

Prompt refusal alone does not prove the forbidden source was unavailable.

---

# 15. Cross-platform / alternative-AI portability track

Owner added an explicit research interest:

> Consider whether HDM should be able to move to another AI platform that exposes stronger orchestration/isolation/tool capabilities, preferably without requiring a roughly $200/month consumer tier.

This should be treated as a **separate Step-6 feasibility/comparison track**, not as a pre-decided migration away from OpenAI.

## 15.1 Architecture goal

Do not let accepted role semantics depend unnecessarily on ChatGPT-specific UI or provider-specific agent abstractions.

Prefer a conceptual separation such as:

```text
HDM deterministic core
HDM Context Assembler
HDM typed role contracts
HDM persistence/recovery laws
        |
        v
AI HOST / PROVIDER ADAPTER
        |
        +-- ChatGPT profile
        +-- alternative provider profile
        +-- future API/orchestrated profile
```

Provider adapters may differ physically, but may not alter canonical role authority or information eligibility.

## 15.2 Capability-first comparison

Do not compare platforms mainly by marketing labels or model benchmark scores.

First derive an HDM capability checklist, then compare candidate platforms against it.

Likely capability dimensions:

```text
one user-visible chat UX
hidden/internal model calls from one interaction
fresh isolated invocations / context reset
multiple logical roles
strict context partitioning
structured outputs
custom tools
Python / deterministic execution
repository/network access
credential/authentication model
recipient / user identity
pre-visible output staging
stream buffering/control
parallel or conditional calls
tool-call latency
model latency
context limits
persistent storage hooks
provider-side memory behavior
multimodal ingestion
retry/invocation identity
cost / subscription / API pricing
consumer usability
web/mobile availability
background execution (optional)
exportability / data portability
```

## 15.3 Candidate platform research should include more than one business model

Formal research may compare:

- consumer subscription products;
- developer/API-first platforms;
- platforms with built-in multi-agent/workflow features;
- local/self-hosted models where quality is sufficient;
- hybrid products where the user experience remains simple while orchestration runs elsewhere.

Do not assume a consumer subscription is automatically cheaper than API use for HDM's actual traffic pattern, and do not assume API is automatically cheaper either. Measure expected campaign usage.

## 15.4 Portability decision criteria

A platform switch is interesting only if the gain is material.

Evaluate at least:

- can it satisfy Step-4/5 semantic boundaries more cleanly?
- can it reduce ordinary-turn latency?
- can it reduce the number of externally visible orchestration compromises?
- can it provide genuine role isolation?
- can it support deterministic tools/repository transport?
- does it improve or worsen player UX?
- total user cost;
- deployment/maintenance burden;
- vendor lock-in;
- model quality for each HDM role;
- migration feasibility;
- durability of the provider capability contract.

## 15.5 Important portability law candidate

A likely desirable Step-6 design principle to test:

> Core role contracts, semantic authority and Context Assembler rules SHOULD be provider-neutral; provider-specific capabilities belong behind explicit deployment profiles/adapters unless doing so would impose disproportionate complexity.

This is not yet canonical. It must survive YAGNI review: HDM should not build a large abstract provider framework merely because migration is imaginable.

The useful target may be much smaller:

```text
stable internal role contracts
+
small explicit host capability interface
+
1 primary supported adapter
+
well-defined requirements for a future second adapter
```

instead of implementing multiple providers immediately.

## 15.6 Cost target

Formal research should explicitly search for viable alternatives that do **not** require a premium roughly-$200/month consumer plan merely to obtain essential orchestration/isolation capabilities.

This is a product/economic constraint to quantify, not a promise that such a platform necessarily exists.

---

# 16. Additional risks / easy-to-forget Step-6 topics

## 16.1 Model/version drift

- model availability can change;
- behavior/latency can change without campaign schema changes;
- determine what must be capability-tested or versioned;
- avoid making campaign correctness depend on one prose model version unless required.

## 16.2 Tool quotas, rate limits and tail latency

Average latency is insufficient.

Need at least p50/p90/p95 thinking for:

- role calls;
- tool calls;
- repository operations;
- retry amplification;
- Plus/consumer limits where observable.

## 16.3 Long-chat growth and host-managed context behavior

One-chat products may encounter:

- context truncation;
- provider summarization/compaction;
- changed retrieval of old messages;
- chat limits.

Correctness must continue to derive from campaign storage, not assumed host memory.

## 16.4 Multimodal / voice / attachments

If baseline gameplay accepts voice/images/uploaded handouts/generated media, Step 6 may need explicit ingestion/normalization boundaries.

Do not accidentally promise byte/verbatim fidelity where the platform supplies only an interpretation/transcript.

Potentially defer modalities from baseline if they materially destabilize the architecture.

## 16.5 Prompt/package versioning

Questions:

- Are role prompts/configurations engine-versioned assets?
- Which prompt changes are style-only vs semantic-interface changes?
- How are open Continuations handled across prompt/config updates?
- How do eval baselines follow prompt revisions?

## 16.6 Observability without leaking secrets

Need enough evidence to diagnose:

- malformed role outputs;
- context assembly mistakes;
- latency spikes;
- incorrect tool routing;
- isolation violations.

But diagnostics must not become a second secret archive or player-visible leak surface.

## 16.7 Prompt injection from campaign content/tools

Untrusted/instruction-bearing strings may come from:

- player text;
- uploaded documents;
- world text authored by users;
- tool responses;
- Story text;
- retrieved historical messages;
- external rule/source text.

Context Assembler and role prompts need a clear data-vs-instruction boundary.

## 16.8 Adaptive budget / graceful quality scaling

Potential direction:

```text
cheap/common turn
    -> minimal role graph

complex/high-stakes turn
    -> additional role call(s)

maintenance
    -> outside player-response critical path where allowed
```

Latency heuristics may reduce quality/optional work, but must not bypass correctness.

## 16.9 Output length as part of latency and gameplay quality

Narrator verbosity directly affects perceived latency and gameplay pacing.

Step 6 may need explicit style/length budgets by scene mode rather than unconstrained literary generation.

## 16.10 Deterministic vs LLM-owned routing decisions

Need to decide which role-activation decisions are deterministic policy and which, if any, may be proposed by an LLM.

Avoid circular behavior such as invoking an expensive role merely to ask whether that role was necessary.

## 16.11 Security/adversarial boundary for tools

LLM-generated tool arguments must not bypass deterministic authorization, repository currentness or campaign ownership rules.

## 16.12 Context/token accounting for private vs shared material

Role isolation may duplicate context across calls. Need to measure actual cost rather than assume architectural cleanliness is free.

---

# 17. Candidate Step-6 work decomposition

Exact numbering is not approved. A plausible research/design decomposition is:

```text
6.0  Step-6 task brief + capability/evidence ledger

6.1  Baseline product / host capability research
     - current ChatGPT Plus capabilities
     - current invocation/tool/context behavior
     - required direct experiments

6.2  Cross-platform / alternative-AI comparison
     - derive HDM capability matrix first
     - compare viable providers / business models
     - recommendation on primary platform and portability boundary

6.3  Role information / compatibility matrix
     - exact eligible sources per role
     - typed cross-role handoffs
     - legal physical co-location

6.4  Physical invocation and context-isolation topology
     - minimum call graph
     - reset/isolation mechanism
     - single-chat UX mapping

6.5  Typed role result contracts and validation
     - Interpreter
     - Dramaturg
     - Actor
     - Narrator
     - Chronicler

6.6  Role activation / fast-path policy
     - always / conditional / deferable
     - common path optimization
     - escalation for complex turns

6.7  Context/retrieval/cache strategy
     - role-specific bundles
     - long-campaign boundedness
     - host-memory exclusion

6.8  Model assignment / specialization
     - same vs different models
     - quality/latency/cost evidence

6.9  Latency / token / cost budget
     - p50/p90/p95 targets
     - ordinary vs exceptional operations
     - Plus/user economics

6.10 Failure / retry / degradation semantics
     - timeouts
     - invalid structured output
     - unavailable role/model
     - no mechanics replay

6.11 Narrator pre-visible validation / disclosure physical proof

6.12 RepositoryPort / host identity / recipient feasibility closure

6.13 Role-isolation + prompt-injection + quality eval suite

6.14 Commentator architecture
     - separate context
     - perspective/spoiler policy
     - serving/activation

6.15 Migration / catalogs / schemas / seeds / prompt-package closure

6.16 Final Steps 1–6 holistic architecture review

6.17 Architecture closure + implementation-obligation consolidation
```

This is a working decomposition only. Formal Step-6 task framing should challenge whether it is too granular, missing a dependency, or ordering research after decisions that depend on it.

---

# 18. Questions suitable for parallel exploration in a Work chat

The following can be explored without treating answers as canonical decisions:

1. Under the one-chat Plus constraint, what physical mechanisms could genuinely isolate role contexts?
2. Can the Narrator be staged/validated before player-visible rendering in a supported consumer-chat topology?
3. What is the minimum viable call graph for high-quality ordinary turns?
4. Which role pairs are actually context-compatible?
5. Can Dramaturg work be amortized across multiple turns without making the world stale or railroaded?
6. When does Actor add enough quality to justify another call?
7. How often does Chronicler need to run for Story to remain useful?
8. What exact quality failures appear if Interpreter/Narrator are co-located?
9. What latency budget should be assigned to every physical phase?
10. Which retry/degradation policies preserve mechanics while meeting the one-minute ceiling?
11. What host identity information is actually available for Interaction/Retry/recipient binding?
12. Can the current ChatGPT tool/runtime surface support a deterministic RepositoryPort cheaply enough?
13. Which alternative AI platforms currently offer stronger hidden-call, isolation, tool, identity or orchestration capabilities at reasonable cost?
14. Could an API-first or hybrid deployment be cheaper than a premium consumer subscription at realistic HDM usage?
15. What is the smallest provider-neutral boundary that keeps future migration possible without overengineering today?
16. What canary/prompt-injection tests should qualify a topology as actually isolated?
17. What eval set distinguishes a mechanically correct but boring Master from a genuinely good one?
18. Which multimodal capabilities belong in baseline vs later extension?
19. What engine/prompt/model versioning is needed so open campaigns remain compatible?
20. What final architecture surfaces from Steps 1–5 are still not represented in machine catalogs/schemas/seeds?

---

# 19. Current preliminary recommendation

Before designing role prompts in detail, Step 6 should first establish three things with direct evidence:

```text
1. PHYSICAL HOST / PROVIDER CAPABILITY
2. REAL CONTEXT ISOLATION / PRE-VISIBLE VALIDATION
3. END-TO-END LATENCY BUDGET
```

At the same time, platform research should not be artificially restricted to ChatGPT if another affordable AI platform can satisfy the inherited architecture materially better.

Only after those constraints are measured should HDM choose:

- physical role topology;
- role co-location;
- model assignment;
- prompt/result realization;
- fast-path activation policy.

The reason is simple:

> There is little value in perfectly designing five logical prompts around a physical topology that the baseline host cannot securely or quickly realize.

Likewise, there is little value in building a large provider abstraction before proving that a second platform is materially useful.

The intended design posture is therefore:

```text
capability-first
measurement-first
minimal hot path
strict semantic boundaries
provider-aware but not provider-overabstracted
quality evaluated explicitly
```

---

# 20. Reverification rule

AI product capabilities, plan limits, model availability, pricing, tool surfaces, context behavior and orchestration features are time-sensitive.

Before Step 6 relies on any such property:

1. prefer official current provider documentation;
2. run direct experiments where documentation does not establish the required semantic guarantee;
3. record date/profile/plan/surface tested;
4. distinguish product fact from inference;
5. state what architecture changes if the capability disappears or changes.

Do not turn these working notes into platform facts by repetition.
