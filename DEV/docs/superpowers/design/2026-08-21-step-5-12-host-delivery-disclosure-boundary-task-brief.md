# Step 5.12 — Host Delivery / Disclosure Boundary — Architectural Task Brief

Status: **TASK BRIEF — ARCHITECTURAL RESEARCH AUTHORIZED; NO DELIVERY MODEL DECIDED**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Classification: **ARCHITECTURAL / DEEP-WORK / EXTERNAL-SIDE-EFFECT CONSISTENCY**

Governing process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- Superpowers `using-superpowers` + `brainstorming`

Active roadmap slice: **Step 5.12 only**.

This brief authorizes research and architecture design for Step 5.12. It does not authorize GAME/schema/runtime implementation, Step 5.13 generic garbage collection, or Step 6 physical six-role orchestration/deployment design.

---

# 1. Purpose

Step 5.12 must define the smallest correct, crash-safe and retry-safe semantic boundary between:

```text
Narrator-generated player-facing output
        -> validated HDM output
        -> host emission attempt
        -> evidence of host-visible communication
        -> outbound historical message evidence
        -> runtime.disclosure advancement
```

The central architecture problem is not merely:

> Did the assistant generate a response?

It is:

> **What evidence is sufficient for HDM to claim that specific information was actually emitted onto the relevant player-facing host surface, when campaign persistence and ChatGPT host delivery are separate systems with no assumed distributed transaction, and how must ambiguity, retries, regeneration, branching, multiplayer recipient subsets and crash windows behave so HDM neither invents exposure nor replays gameplay?**

The final model must preserve all of these distinctions:

```text
model generation completed
HDM NarrationResult validated
host emission requested/attempted
host surface accepted/rendered the output
output is present in a later host branch/context
human literally read/understood it
runtime.message established
runtime.disclosure advanced
PC/NPC fictional knowledge changed
```

These are not automatically equivalent.

---

# 2. Baseline product/deployment constraint

Baseline HDM remains operable in one ordinary sequential ChatGPT conversation/execution stream.

Correctness MUST NOT require:

- ChatGPT Work;
- Pro/Enterprise-only features;
- a permanently running worker;
- scheduled/background tasks;
- a separate web application;
- a custom OpenAI API host;
- a post-response webhook unless ordinary ChatGPT demonstrably provides one in the supported profile.

Richer deployments MAY later provide stronger delivery evidence or lower latency, but Step 5.12 must separate semantic requirements from optional deployment capabilities.

If ordinary ChatGPT cannot physically satisfy some stronger guarantee, the design must state the exact capability gap and define the strongest safe baseline semantics rather than pretending the capability exists.

---

# 3. Current platform facts and observations to reverify

Platform facts are time-sensitive and MUST be reverified from official OpenAI sources during research and again before implementation depends on them.

Current official product documentation establishes at least:

1. users can edit earlier user messages;
2. users can retry/regenerate assistant responses;
3. users can branch a conversation from an earlier point;
4. chats can be deleted and then are not normally recoverable through UI/API/support;
5. Project/Memory context is not an HDM-owned immutable campaign ledger.

Current official OpenAI API documentation separately establishes model-generation concepts such as response IDs, output-message IDs, `response.completed`, conversations and streaming completion events. These API-generation events MUST NOT be assumed to prove ordinary ChatGPT UI delivery unless an official ChatGPT host contract explicitly makes that guarantee.

Current execution-harness observation to investigate:

> Tools/repository writes execute during the assistant invocation, while the final ordinary assistant message is rendered only after tool work completes. The currently exposed HDM development/gameplay environment does not expose an obvious post-render tool callback to the same invocation.

Treat this as an observation, not a permanent product fact. Verify what ordinary ChatGPT actually exposes to the runtime.

Research starting references include official OpenAI documentation for:

- Edit Message / Try again / Branch behavior;
- chat deletion and retention;
- Projects and project memory;
- Responses / Conversations / message IDs and completion events;
- Apps SDK / MCP lifecycle where relevant to ordinary ChatGPT tool execution.

Do not design against undocumented assumptions such as:

```text
response.completed == user-visible delivery
final answer render has an automatic post-send callback
runtime can query immutable ChatGPT message revision ancestry
runtime receives a stable host message ID on every ordinary invocation
retry preserves the same host/delivery identity
branch identity is exposed to tools
```

---

# 4. Inherited canonical laws

## 4.1 Step 3 — execution / Interaction

Preserve:

- `runtime.interaction` is one accepted external exchange/invocation identity;
- same prose in a later intentional turn is a new Interaction;
- transport retry of the same invocation must not replay accepted gameplay;
- accepted mechanics/RNG/commands are idempotent by their existing identities;
- presentation work does not become mechanical authority.

A host Retry/regeneration of an older assistant answer MUST NOT silently replay the old player Interaction or its canonical consequences.

## 4.2 Step 4 — disclosure authority

Preserve:

- `runtime.disclosure` is durable human-player exposure authority for material information whose prior exposure matters later;
- disclosure is keyed semantically to player + proposition/aspect, not to a generic chat cursor;
- statement exposure is distinct from objective-status exposure;
- disclosure does not imply PC knowledge/belief;
- Narrator returns validated `disclosure_refs[]`;
- generation/emission failure before the qualifying boundary must not create confirmed disclosure;
- HDM does not claim to know whether a human literally read the message.

## 4.3 Step 5.2 / 5.4 / 5.7 — cold recovery

A new chat/runtime cannot rely on remembered process/model state or old host conversation being available.

Any delivery state whose loss can change future secrecy/context correctness must either:

- be durably recoverable through an admitted native owner/evidence route;
- be explicitly semantically reconstructible;
- or remain an explicit ambiguous/recovery condition.

Do not create a generic pending-work queue merely for delivery.

## 4.4 Step 5.5 — durability edges

Do not create a per-response or per-message campaign save rule by default.

However, research MUST determine whether a **material disclosure attempt** creates a named durability edge for the minimum evidence required to survive the external side effect.

If such an edge is required, scope it to actual material disclosure/delivery correctness rather than ordinary narration.

## 4.5 Step 5.6 — publication epistemics

Preserve the distinction:

```text
CONFIRMED_ACCEPTED
CONFIRMED_REJECTED
INDETERMINATE
```

for authority-changing operations where applicable.

Do not equate lost acknowledgement with failure or success.

Do not replay gameplay mechanics/RNG because delivery or repository transport is retried.

Do not invent a distributed transaction across campaign Git authority and ChatGPT host delivery.

## 4.6 Step 5.8 — multiplayer/live ownership

Per-player delivery/disclosure cannot be widened merely because one shared scene/event exists.

Independent recipients or independently hosted chats may have different delivery outcomes.

Live/campaign technical order is not fictional chronology.

## 4.7 Step 5.10 — Story projection

Story may lag and is not gameplay authority.

Only Step-5.12-qualified outbound communication may become an admitted Transcript source candidate.

Story catch-up must never be required merely to emit gameplay narration.

## 4.8 Step 5.11 — message/retention contract

Preserve:

- visible ChatGPT history is mutable host context, not campaign authority;
- `runtime.message` owns stable HDM communication evidence identity once a communication is established;
- generated but unemitted Narrator drafts are not Transcript history;
- outbound `runtime.message` establishment waits for Step-5.12 qualification;
- later host edit/retry/branch/delete cannot retcon accepted campaign history;
- Selective Exact / Semantic Continuity remains the product memory contract;
- outbound exact text, if established, may later compact under Step 5.11 without changing disclosure truth.

---

# 5. Central semantic vocabulary to define

Research MUST define, without prematurely forcing these exact record names, the distinct concepts equivalent to:

```text
NARRATION DRAFT
    model/editorial candidate; no delivery authority

VALIDATED NARRATION RESULT
    exact prose + validated disclosure refs eligible to be sent

DELIVERY INTENT / PREPARATION
    stable intent to emit one exact validated payload to specified recipient set

DELIVERY ATTEMPT
    one host-side send/render attempt, if distinguishable

DELIVERY EVIDENCE
    what the host/runtime can actually prove about the result

QUALIFIED OUTBOUND COMMUNICATION
    communication sufficiently established to create outbound runtime.message/history

RUNTIME DISCLOSURE
    durable material player exposure relation

HUMAN READ/UNDERSTOOD
    outside the claimed baseline unless platform evidence explicitly supports it
```

The design must state which concepts are semantic owners, operational evidence, historical evidence, projections or transport metadata.

Do not create separate records for distinctions that can safely remain embedded state, but do not collapse materially different epistemic states for schema convenience.

---

# 6. The external-side-effect gap is mandatory research

Campaign persistence and host delivery are separate systems.

Research every relevant order, including:

```text
A. persist disclosure first -> emit later
B. emit first -> persist disclosure later
C. persist prepared-delivery evidence -> emit -> confirm later
D. host-side idempotent delivery key -> reconcile outcome
E. infer delivery from next invocation/current host branch
F. capability-specific hybrid
```

For each ordering, analyze crash windows:

```text
campaign write succeeds / host emission never happens
host emission happens / campaign write never records it
host ACK response is lost
host shows output / process dies before another tool call
repository publication is ambiguous
user retries/regenerates before delivery reconciliation
user branches from before/after the output
chat is deleted before reconciliation
```

A design is invalid if it silently converts any of these into false certainty.

---

# 7. Required alternative space

Research MUST compare at least the following materially distinct architecture families before recommending or hybridizing.

## Alternative A — optimistic precommit exposure

Persist outbound message/disclosure as delivered before final host emission.

Challenge:

- false-positive disclosure if emission fails;
- whether a recoverable pending-send state can repair this;
- whether user-facing latency is lower enough to justify epistemic risk.

## Alternative B — strict post-delivery commit

Emit first, then persist outbound message/disclosure only after a confirmed host callback/ACK.

Challenge:

- whether ordinary ChatGPT exposes any post-render execution hook;
- crash after emission before persistence;
- inability to run tools after final response;
- deployment portability.

## Alternative C — durable prepared delivery + later reconciliation

Before material emission, durably establish exact payload/recipient/disclosure intent; emit it; on later evidence promote to confirmed outbound communication/disclosure.

Challenge:

- additional write latency on material reveals;
- unresolved pending delivery if the chat ends;
- next-turn confirmation reliability;
- branch/retry ambiguity;
- avoiding a generic job queue.

## Alternative D — host-history-as-confirmation

Treat presence of an exact prior assistant payload in the later invocation's host context as evidence that it reached that conversational branch.

Challenge:

- host history mutability;
- stable identity and collision of identical text;
- Retry/edit/branch behavior;
- deletion/new-chat loss;
- whether current invocation exposes enough exact context to validate this deterministically.

## Alternative E — capability-tiered HostDeliveryPort

Define semantic delivery outcomes independent of host implementation; stronger deployment profiles may provide exact host IDs/callbacks/idempotency while ordinary ChatGPT uses the strongest safe weaker evidence protocol.

Challenge:

- avoid hiding an unusable baseline behind abstraction;
- no semantic divergence between profiles;
- profile capability must be testable, not aspirational.

## Alternative F — no durable disclosure / rederive from current context

Do not durably track human exposure.

This directly challenges Step 4 and is expected to fail unless research exposes a fundamental reason to reopen Step 4. Analyze it explicitly rather than dismissing it by habit.

Hybrids are encouraged when they are materially simpler/safer than any pure option.

---

# 8. Required evaluation matrix

Evaluate serious alternatives against at least:

```text
FALSE-POSITIVE DISCLOSURE RISK
FALSE-NEGATIVE / FORGOTTEN DISCLOSURE RISK
DUPLICATE DELIVERY RISK
SECRET / SPOILER SAFETY
GAMEPLAY REPLAY SAFETY
CRASH CONSISTENCY
ACK AMBIGUITY
RETRY / REGENERATE BEHAVIOR
BRANCH DIVERGENCE
CHAT DELETION / NEW-CHAT RECOVERY
OUTBOUND runtime.message INTEGRITY
STORY/TRANSCRIPT INTEGRATION
MULTIPLAYER RECIPIENT SUBSETS
LIVE/CAMPAIGN OWNERSHIP
LATENCY / REPOSITORY WRITE FREQUENCY
TOKEN / LLM COST
NO-BACKGROUND BASELINE FEASIBILITY
PLATFORM PORTABILITY
OBSERVABILITY / REPAIR
MIGRATION
YAGNI / CONCEPTUAL COMPLEXITY
```

Make trade-offs concrete with failure scenarios.

---

# 9. Disclosure false-positive versus false-negative policy

The design must explicitly analyze asymmetry between:

```text
FALSE POSITIVE
    HDM believes player saw X, but X never reached the host surface

FALSE NEGATIVE
    player saw X, but durable disclosure still says not confirmed
```

Potential consequences differ:

- false positive may cause HDM to omit information the player never received;
- false negative may cause redundant re-reveal or changed spoiler behavior;
- for some secrecy contexts, `POSSIBLY_EXPOSED` may need different treatment from both yes and no.

Do not introduce three-valued disclosure merely because it seems elegant. Determine whether ambiguity belongs in `runtime.disclosure` itself or in separate delivery evidence/pending state.

The human owner decides only if a genuine product-quality/risk trade-off remains after technical analysis.

---

# 10. Delivery identity and idempotency

Research the minimum stable semantic identity needed for one outbound communication/delivery attempt.

Candidate inputs include:

```text
source interaction / narration cause
recipient player identity or recipient set
delivery generation/ordinal
exact payload digest
validated disclosure set
host conversation/thread identity if trustworthy
host message/response identity if exposed
```

Distinguish:

```text
GAMEPLAY EXECUTION IDEMPOTENCY
DELIVERY IDEMPOTENCY
DISCLOSURE IDEMPOTENCY
```

A retry of delivery MUST NOT reroll, rerun or re-adjudicate gameplay.

If the host cannot accept an idempotency key, the architecture must state the limit rather than claim exactly-once host effects.

---

# 11. ChatGPT Retry/regeneration is not ordinary transport retry

This workstream is mandatory.

A user can invoke Retry/Try again on an earlier assistant answer. Research whether the resulting ChatGPT invocation exposes any stable relationship to the prior response or whether it merely re-executes from older conversational context.

Required safety rule to test:

> A host-triggered regeneration from an old conversational point cannot automatically re-execute accepted gameplay, repository side effects or disclosure transitions merely because the model is being asked to produce another assistant answer.

Research scenarios:

1. Retry immediately after a narration-only answer;
2. Retry an answer whose preceding player action already committed canon;
3. Retry an answer that performed a campaign save/publication before narration;
4. Retry an answer whose old narration revealed a secret;
5. regenerated answer reveals a different secret/ref set;
6. Retry after campaign state has advanced in later turns;
7. Retry after another multiplayer participant changed the world.

If ordinary ChatGPT does not expose enough invocation identity to distinguish retry from intentional new Interaction safely, record this as a Step-6 host capability blocker/deployment constraint, not as an assumption.

---

# 12. Branching from old conversational state

A host branch created from old visible history is not campaign authority.

Required behavior to design:

```text
old host branch context
        +
current campaign authority
        -> bounded reconciliation before accepting new gameplay/tool side effects
```

Research:

- whether branch metadata/identity is exposed;
- whether a new branch inherits old assistant output as visible context;
- how pending/confirmed delivery evidence from the original branch relates to the new branch;
- whether disclosure is player-global campaign exposure or branch-local host evidence;
- how to avoid treating branch absence of later messages as evidence that the human has "unseen" them.

A human cannot be made to unsee already delivered information by creating a branch.

---

# 13. Outbound message establishment

Step 5.11 requires:

```text
NarrationResult generated
    !=
qualified outbound runtime.message
```

Step 5.12 must define the exact qualification rule.

The design must answer:

1. when stable outbound message identity is allocated;
2. whether pre-emission prepared identity exists;
3. when exact payload becomes historical communication evidence;
4. what delivery evidence ref is stored;
5. how duplicate/retry attempts relate to one logical communication;
6. whether a regenerated different payload is the same or a new communication;
7. how payload compaction later preserves the delivery/disclosure provenance.

Do not let an unemitted draft become Transcript source merely because it has an ID.

---

# 14. `runtime.disclosure` advancement

For each validated disclosure ref, define when the durable relation may advance.

Required aspects:

```text
statement exposure
objective-status/revision exposure
recipient player identity
exact source outbound communication
validated source fact/revision
```

Research whether disclosure advancement can be:

- in the same campaign transaction as prepared-delivery evidence;
- delayed until delivery confirmation;
- represented as monotonic confirmation over a pending delivery;
- rebuilt from durable confirmed outbound message evidence.

Do not duplicate disclosure authority in message records.

Message/delivery records may evidence why disclosure advanced; `runtime.disclosure` remains the current sparse exposure owner.

---

# 15. Generated versus emitted versus read

Final design MUST state the strongest claim supported by each state.

At minimum:

```text
GENERATED
    model produced content

VALIDATED
    HDM considers payload eligible to emit

EMISSION ATTEMPTED
    host side effect was requested if observable

HOST-VISIBLE / EMITTED
    only when supported by sufficient host evidence

READ/UNDERSTOOD
    not claimed merely because output was emitted
```

If ordinary ChatGPT cannot provide a provable distinction between some adjacent states, collapse only those states whose collapse is semantically safe and explicitly document the weaker guarantee.

---

# 16. Material versus ordinary narration

Do not impose repository publication before every assistant message unless correctness proves it necessary.

Research at least:

```text
ordinary narration with no material new disclosure
material secret/reveal disclosure
OOC objective-status revelation
rules/mechanics explanation already public
private/subset disclosure
message whose exact historical retention is protected
```

If only material disclosure requires durable pre-send evidence, define the eligibility predicate and named edge.

No LLM importance judgment alone may create or remove a correctness-critical delivery edge.

---

# 17. Multiplayer / recipient subsets

Disclosure is per human player.

Required scenarios:

- one shared-scene narration visible to all current participants;
- private whisper to one player;
- two separate ChatGPT channels representing different players;
- one recipient disconnected/unavailable;
- one recipient delivery confirmed, another indeterminate;
- response resent to only failed/indeterminate recipient;
- spectator/Commentator recipient separate from gameplay player;
- host message order differs across recipients;
- live epoch closes while one recipient delivery is unresolved.

Do not use one group boolean when independent host outcomes are possible.

Do not infer fictional PC hearing/knowledge from human host delivery; world.knowledge remains separate.

---

# 18. Interaction with narration and gameplay causality

Research the correct causal order between:

```text
accepted player Interaction
canonical gameplay consequences
required canonical durability
NarrationResult generation
material delivery preparation
host emission
outbound message confirmation
disclosure confirmation
```

Do not roll back committed gameplay merely because narration delivery fails.

Do not generate new gameplay consequences merely to retry presentation.

If the PC canonically learned/heard something in fiction but human delivery failed, recovery must distinguish:

```text
PC KNOWS X
PLAYER DELIVERY OF X UNCONFIRMED
```

and provide a lawful way to communicate the already-established information later without re-executing the fictional event.

---

# 19. Crash / ambiguity scenario suite

Candidate and final design must survive at least:

```text
Narrator generation fails before validation
validation rejects a disclosure ref
campaign consequences commit, narration generation fails
material delivery preparation commit succeeds, host emission fails
host output appears, runtime dies before any post-send persistence
host ACK is indeterminate
repository pre-send publication ACK is indeterminate
retry after confirmed host failure
retry after unknown host outcome
same exact payload delivered twice
same logical result regenerated with different prose
old answer regenerated after later canon changes
old branch continues after campaign authority advanced
chat deleted with unresolved delivery evidence
new chat starts with confirmed disclosure
new chat starts with indeterminate/pending delivery
user responds after an apparently successful prior output
user responds from a branch containing a different retry variant
player closes app immediately after a major reveal
private reveal to P1 while P2 must remain undisclosed
P1 confirmed, P2 failed
P1 confirmed, P2 indeterminate
live scene closes with recipient delivery unresolved
Story Transcript catch-up sees confirmed outbound message
Story Transcript catch-up sees prepared/unconfirmed output
compaction of outbound exact payload after disclosure is confirmed
host output exists but no exact source text remains later
100k-message campaign performs no history scan to reconcile one delivery
```

Add cases discovered during platform research.

---

# 20. Analytical challenge requirements

Before candidate architecture, explicitly attack at least:

1. Why not persist disclosure before emitting and accept rare false positives?
2. Why not emit first and write disclosure on the next turn?
3. Why not treat `response.completed` as delivery?
4. Why not treat any next user message as proof the previous output was seen?
5. Why not use exact output text/hash as the only delivery identity?
6. Why not embed a visible/hidden delivery token in every response?
7. Why not always resend on ambiguous ACK?
8. Why not never resend on ambiguous ACK?
9. Why not make disclosure `NOT | POSSIBLE | CONFIRMED`?
10. Why not store ambiguity separately from disclosure?
11. Why not require a Git commit before every response?
12. Why not rely on ChatGPT chat history as the delivery ledger?
13. Why not use host Retry as delivery retry?
14. Can Retry replay gameplay/tool writes from an old point?
15. Can a branch make already exposed information appear undisclosed in local history?
16. Can confirmed disclosure survive host chat deletion?
17. Can false-positive disclosure cause information loss to the user?
18. Can false-negative disclosure leak a secret to a different recipient?
19. Does multiplayer require per-recipient delivery occurrence identity?
20. Can Story/Transcript accidentally archive an unemitted draft?
21. Can delivery persistence block ordinary gameplay?
22. Does the model invent a generic queue/outbox without a concrete need?
23. Is exactly-once host delivery actually achievable on the baseline platform?
24. What is the strongest safe guarantee if it is not?

State the strongest counterargument to the recommended model fairly.

---

# 21. External architecture research

Use primary/authoritative sources where possible.

In addition to OpenAI product documentation, research relevant established patterns for external side effects, including as useful:

- transactional outbox / inbox patterns;
- idempotency keys and duplicate suppression;
- at-least-once versus exactly-once external effects;
- acknowledgement ambiguity;
- monotonic confirmation records;
- per-recipient delivery state.

Do not cargo-cult messaging infrastructure. HDM has one ordinary sequential ChatGPT baseline and should not acquire Kafka/job queues merely because similar vocabulary exists elsewhere.

The research question is which *semantic lessons* apply, not which framework to import.

---

# 22. Assumption & evidence ledger requirements

Research must explicitly track at least assumptions equivalent to:

```text
A1 ordinary ChatGPT exposes/no-exposes post-render callback
A2 previous assistant output is/no-is available exactly on next invocation
A3 stable host message/response ID is/no-is visible to runtime/tools
A4 Retry identity/revision ancestry is/no-is exposed
A5 Branch identity is/no-is exposed
A6 host delivery attempt can/no-can accept idempotency key
A7 one assistant final response targets one human recipient in baseline profile
A8 campaign storage write can happen before but not after final render in same invocation
A9 a new chat has/no-has reliable access to prior host message evidence
A10 response/API completion semantics differ/do-not-differ from ChatGPT UI delivery
```

For each:

```text
status: FACT | ASSUMPTION | OPEN QUESTION
confidence
evidence
architecture impact if false
revisit trigger
```

---

# 23. Human decision rights

Do not ask the owner to choose message fields, retry counters, digest format, record nesting, index structure or state-machine spelling.

Escalate only if, after research/challenge, a material product/risk trade-off genuinely remains, such as:

- whether baseline HDM prefers possible duplicate re-delivery over possible silent omission under irreducible host ambiguity;
- whether a material reveal is allowed to incur a mandatory pre-emission repository durability write;
- whether a deployment profile lacking minimum host-delivery evidence is considered supported gameplay or degraded/unsupported;
- another irreducible guarantee/cost choice exposed by platform reality.

Before escalation provide:

```text
verified facts
constraints
assumptions
recommended option
strongest alternative
trade-offs
failure modes
reversibility
confidence
what would change the recommendation
```

Do not outsource unresolved technical analysis to the owner.

---

# 24. Reserved boundaries

## Step 5.13

Owns physical GC/orphan cleanup after 5.12 defines which delivery/message evidence remains protected.

Do not build a second GC system here.

## Step 6

Owns physical host/deployment feasibility, including:

- stable host invocation/message/revision identity availability;
- physical model-call topology;
- capability profiles;
- repository bridge implementation;
- actual context isolation;
- optional richer API/custom-host deployment.

Step 5.12 must define the semantic interface/correctness requirements Step 6 must satisfy, without assuming unavailable features.

---

# 25. Required design artifact chain

```text
TASK BRIEF                     this document
    ↓
RESEARCH DRAFT
    repository audit
    platform capability research
    assumption/evidence ledger
    failure-window inventory
    alternative matrix
    ↓
ANALYTICAL CHALLENGE
    attack guarantee, ordering, ambiguity, YAGNI
    ↓
DECISION BRIEF                 only if material owner choice remains
    ↓
OWNER DECISION                 only where required
    ↓
CANDIDATE SPECIFICATION
    ↓
ADVERSARIAL REVIEW
    full retry/crash/branch/multiplayer suite
    cross-Step consistency
    ↓
RESOLUTION GATE
    ↓
CANONICAL STEP-5.12 SPEC
    ↓
ROADMAP UPDATE
```

Do not skip analytical challenge or adversarial review.

---

# 26. Candidate specification must answer explicitly

A candidate cannot enter adversarial review until it answers all of:

1. What exact semantic event qualifies an outbound communication as established?
2. What is *not* sufficient evidence of delivery?
3. Is there a prepared-delivery identity before emission?
4. What host outcome vocabulary exists?
5. Where does delivery ambiguity live?
6. When is outbound `runtime.message` created/confirmed?
7. When may `runtime.disclosure` advance?
8. Can disclosure ever advance before confirmed host-visible evidence?
9. If not, how is crash-after-emission-before-persistence handled?
10. If yes in any baseline path, how are false positives repaired without pretending exposure?
11. How are exact payload and disclosure refs frozen for retry?
12. What makes one delivery retry the same logical communication?
13. What happens when retry produces different prose?
14. What happens when user invokes ChatGPT Try again on an old answer?
15. How does current campaign authority fence old-branch regeneration?
16. How does branch-from-old-message behave?
17. How does new-chat recovery behave with unresolved delivery?
18. Which delivery states are recovery-relevant roots/dependencies?
19. Does a material disclosure create a named durability edge?
20. Does ordinary narration avoid per-response writes?
21. How are per-recipient multiplayer outcomes represented?
22. How is human delivery distinct from PC knowledge?
23. How does confirmed delivery feed Step-5.11 Transcript admission?
24. How do later Transcript/message compaction rules preserve disclosure provenance?
25. What host capability does ordinary ChatGPT baseline require?
26. What stronger optional deployment capabilities can improve but not redefine semantics?
27. What is exactly-once, at-most-once, at-least-once, or merely best-effort in the final contract?
28. What is deliberately *not* promised?

---

# 27. Exit criteria

Step 5.12 closes only when:

- generation, validation, emission, delivery evidence, outbound message and disclosure are non-ambiguously separated;
- ordinary ChatGPT platform capabilities/limitations are researched from current official sources;
- no undocumented host callback/message-ID guarantee is assumed;
- campaign storage + host emission failure windows have explicit outcomes;
- retry/regeneration cannot replay accepted gameplay merely because presentation is retried;
- branch-from-old-context cannot become campaign authority;
- outbound `runtime.message` admission has a precise delivery qualification;
- `runtime.disclosure` advances only under the final accepted evidence law;
- any ambiguity state has bounded recovery/reconciliation semantics;
- per-recipient multiplayer outcomes do not collapse into a false group exposure;
- human delivery remains separate from fictional knowledge;
- Story/Transcript cannot ingest unemitted drafts as delivered history;
- ordinary narration does not require campaign-wide scans, background work or unnecessary repository writes;
- any mandatory material-disclosure pre-send durability edge is explicitly justified;
- Step 5.13 receives a precise protected-evidence/GC handoff;
- Step 6 receives precise deployment capability requirements rather than vague feasibility debt;
- the mandatory adversarial suite passes or all blockers are explicitly resolved;
- no unresolved owner-level product decision is hidden in implementation detail.

---

# 28. Non-goals

Step 5.12 does NOT:

- prove a human read or understood a message;
- provide universal exactly-once messaging infrastructure;
- add background workers/queues by default;
- solve six-role physical context isolation;
- use Story as disclosure authority;
- use transcript order as fictional chronology;
- rollback canon because presentation delivery failed;
- replay gameplay to regenerate presentation;
- make visible ChatGPT conversation history campaign authority;
- physically delete old delivery evidence;
- implement schemas/runtime code before Step-5 architecture sequence closes.
