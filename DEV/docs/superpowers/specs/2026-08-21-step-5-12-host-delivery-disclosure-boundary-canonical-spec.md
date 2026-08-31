# Step 5.12 — Host Delivery / Disclosure Boundary — Canonical Specification

Status: **CANONICAL — STEP 5.12 ARCHITECTURE CLOSED**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Canonicalization basis:

- `../design/2026-08-21-step-5-12-host-delivery-disclosure-boundary-task-brief.md`
- `../design/2026-08-21-step-5-12-host-delivery-disclosure-boundary-research-draft.md`
- `../design/2026-08-21-step-5-12-host-delivery-disclosure-boundary-analytical-challenge.md`
- `../design/2026-08-21-step-5-12-host-delivery-disclosure-boundary-candidate-spec.md` — superseded candidate derivation
- `../design/2026-08-21-step-5-12-host-delivery-disclosure-boundary-adversarial-review.md` — derivation/review
- `../design/2026-08-21-step-5-12-minimal-host-delivery-owner-scope-decision.md`
- `../design/2026-08-21-step-5-12-host-delivery-disclosure-boundary-candidate-spec-v2.md`
- `../design/2026-08-21-step-5-12-host-delivery-disclosure-boundary-adversarial-review-addendum-v2.md`
- `../design/2026-08-21-step-5-12-host-delivery-disclosure-boundary-resolution-gate.md`

Owner-approved scope/product decision:

> **Normal uninterrupted Master responses are the supported baseline. HDM does not build a heavyweight reliability subsystem for interrupted output, host Retry/regeneration, editing old host history, or perfect recovery of partially/ambiguously delivered secrets. These are documented presentation-risk edges.**

Canonical architecture direction:

> **VALIDATED EMISSION-COMMIT / SOFT OUTBOUND DISCLOSURE CLOSURE / NO BASELINE DELIVERY-ACK SUBSYSTEM / DOCUMENTED INTERRUPTION RISK / RECIPIENT-SCOPED DISCLOSURE**

This specification resolves Step-4 human-disclosure host-emission semantics and the Step-5.11 outbound-message handoff. It does not choose physical six-role topology, physical ChatGPT message/revision APIs, exact context-isolation mechanism, generic GC or a future richer delivery service. Those remain Step 6 / Step 5.13 as assigned below.

---

# 1. Purpose

Step 5.12 answers one narrow semantic question:

> When may validated player-facing Master output become HDM historical outbound communication evidence and advance sparse human-player disclosure state, without turning ordinary gameplay into a delivery-queue/distributed-transaction system?

The answer deliberately optimizes for the actual HDM product constraints:

- ordinary gameplay must stay fast;
- no Work/Pro/Enterprise/background-worker prerequisite;
- no per-response Git round trip merely to prove delivery;
- no exactly-once visible-prose promise;
- gameplay/execution correctness must survive even when presentation is interrupted or forgotten.

---

# 2. Authority geometry

```text
OBJECTIVE / CURRENT GAMEPLAY TRUTH
    normal world/runtime owners

FICTIONAL KNOWLEDGE
    world.knowledge

HUMAN PLAYER EXPOSURE
    runtime.disclosure

ACCEPTED OUTBOUND COMMUNICATION HISTORY
    runtime.message

COMPACT SEMANTIC HISTORY
    SemanticEvent / LOG

NONCANONICAL DISCOURSE PROJECTION
    STORY/TRANSCRIPT

PLAYER-VISIBLE PRESENTATION PATH
    NarrationResult
    -> validation
    -> frozen supported delivery representation
    -> EMISSION_COMMIT
    -> host response path
```

`runtime.disclosure` does not own PC knowledge.

`runtime.message` does not prove the truth of propositions it contains.

Story does not become delivery or gameplay authority.

Host/chat history remains mutable presentation/context rather than campaign authority.

---

# 3. Supported baseline host-use contract

HDM baseline assumes the player normally allows the Master response to complete.

ChatGPT host controls may technically permit:

- stopping/interruption of generation;
- retry/regeneration;
- editing older user messages;
- branching from older conversation points;
- deleting host chat history.

These controls are not HDM campaign transactions.

## LAW 5.12-1 — HOST-HISTORY CONTROLS ARE NOT CAMPAIGN REWIND

Interrupting, retrying, regenerating, editing or branching host conversation history SHALL NOT by itself:

- undo accepted gameplay;
- replay RuntimeCommands;
- reroll RNG;
- refund/reconsume resources;
- mutate canonical world state;
- rewrite accepted `runtime.message`/Interaction history;
- rewind `runtime.disclosure`;
- select an older campaign recovery frontier.

Corrections to accepted gameplay use new ordinary HDM Interactions/transitions.

## LAW 5.12-2 — INTERRUPTION IS A DOCUMENTED PRESENTATION-RISK EDGE

Baseline HDM does not promise perfect recovery of which response prefix became visible after user interruption or abnormal host cutoff.

Player-facing help/manual SHOULD warn that interrupting the Master is technically possible but not recommended because important information may be missed.

This limitation SHALL NOT be used to justify a baseline delivery outbox, token/chunk ledger, background resend worker or per-response durability write.

---

# 4. `EMISSION_COMMIT`

The canonical baseline boundary is **EMISSION_COMMIT**.

Conceptually:

```text
resolved gameplay/current state
    -> NarrationResult
    -> validate eligible content
    -> validate material disclosure refs
    -> validate intended player recipient
    -> freeze the supported player-visible response representation
    -> EMISSION_COMMIT
    -> host player-facing output path
```

`EMISSION_COMMIT` is a logical semantic boundary, not a required serialized record/state machine.

It means the output is no longer a private/unemitted draft and HDM has committed that validated representation to its supported player-facing response path.

## LAW 5.12-3 — GENERATION IS NOT EMISSION COMMIT

The following alone SHALL NOT establish outbound communication/disclosure:

- private draft generation;
- hidden role reasoning;
- an unvalidated NarrationResult;
- a failed/abandoned response before the supported player-facing output is committed.

## LAW 5.12-4 — BASELINE DISCLOSURE USES EMISSION-COMMIT EVIDENCE

For the supported ordinary ChatGPT flow, `EMISSION_COMMIT` is sufficient host-side evidence for HDM to establish the corresponding outbound communication/disclosure semantics.

Baseline HDM does not require proof that every character subsequently rendered or that the human literally read/comprehended the message.

A richer future host MAY provide stronger acknowledgement, but baseline correctness does not depend on it.

## LAW 5.12-5 — INTERRUPTION AFTER EMISSION COMMIT MAY OVER-CONFIRM PRESENTATION

If the player interrupts after `EMISSION_COMMIT`, HDM may retain the full committed message/disclosure even though only a prefix was visible.

This is the explicit owner-accepted presentation limitation.

Do not add hidden partial-delivery machinery to “fix” it in baseline.

---

# 5. Pre-emission information integrity

The simplified host evidence standard does not weaken Step-4 information eligibility.

## LAW 5.12-6 — MATERIAL DISCLOSURE REFS ARE PRE-EMISSION INTEGRITY DATA

Before `EMISSION_COMMIT`, material reveal metadata required by Step 4 SHALL be structurally validated against the Narrator's eligible source basis.

For objective-status exposure, the exact truth-transition/revision evidence being disclosed remains identified.

Missing required material disclosure refs are an integrity defect, not evidence that the player remained undisclosed.

HDM SHALL NOT depend on generic post-hoc NLP over old prose to reconstruct ordinary disclosure state.

## LAW 5.12-7 — PLAYER-VISIBLE GAMEPLAY CONTENT MUST RESPECT THE NARRATOR BOUNDARY

The baseline intentional gameplay-delivery surface is the validated Master response.

Private role reasoning, tool internals, connector/debug traces, maintenance diagnostics and other auxiliary surfaces SHALL NOT intentionally carry campaign information that is ineligible for that player.

Step 6 must inventory which physical surfaces the selected deployment actually renders to the user.

If a future deployment intentionally uses another visible surface for gameplay content, it must satisfy equivalent eligibility/disclosure rules.

---

# 6. Outbound emission closure

At one `EMISSION_COMMIT`, deterministic runtime semantics establish one logical **OutboundEmissionClosure** for the applicable recipient/delivery unit.

Conceptually:

```text
outbound runtime.message evidence when admitted/required
+
runtime.disclosure transitions implied by validated material refs
+
required provenance / stable refs / bounded indexes
```

Exact physical records may be optimized later, but the semantic result cannot be split inconsistently.

## LAW 5.12-8 — OUTBOUND MESSAGE AND DISCLOSURE FORM ONE SEMANTIC CLOSURE

If an outbound communication occurrence is established and carries validated material disclosure refs, the corresponding recipient-scoped disclosure transitions are established in the same HOT semantic closure.

A state such as:

```text
confirmed/admitted outbound message M
but required material disclosure transition absent
```

or:

```text
disclosure points to outbound message M
but M never established
```

is invalid unless a narrower representation contract explicitly collapses both roles without losing provenance semantics.

## LAW 5.12-9 — DELIVERY CLOSURE IS NOT A HOST/REPOSITORY DISTRIBUTED TRANSACTION

HDM does not attempt atomic commit across Git campaign storage and ChatGPT rendering.

Host presentation and campaign durability are different domains.

The Step-5.12 closure is the HDM-side semantic consequence of committing validated output to the player-facing path.

---

# 7. Durability and ordinary-turn cost

After emission commit, ordinary outbound message/disclosure changes are normally:

```text
ESTABLISHED
+ VOLATILE_DIRTY
+ MAY_DEFER
```

therefore **SOFT** under Step 5.5.

## LAW 5.12-10 — ORDINARY MASTER OUTPUT CREATES NO GENERIC HARD PERSISTENCE EDGE

Do not publish a second campaign commit merely because narration/disclosure was emitted after a gameplay publication already completed.

Typical ordering is:

```text
resolve gameplay
-> publish gameplay only if an existing durability rule requires it
-> stage/validate narration
-> EMISSION_COMMIT
-> outbound/disclosure becomes new HOT/SOFT metadata
-> later ordinary durability boundary may publish it
```

## LAW 5.12-11 — SAVE/HANDOFF MAY INCLUDE DIRTY DISCLOSURE THROUGH EXISTING POLICY

When explicit save, controlled handoff or another existing HARD edge selects a scope containing dirty gameplay-significant outbound/disclosure metadata, normal Step-5.5/5.6 closure rules apply.

Step 5.12 introduces no independent save command or publication cadence.

## LAW 5.12-12 — LOSS OF UNSAVED DISCLOSURE IS ORDINARY RPO

If total host/process loss destroys unpublished outbound/disclosure HOT state, cold recovery uses actual durable sources only.

The recovered engine may under-remember what the human previously saw and later repeat currently eligible information.

It SHALL NOT replay mechanics/RNG or fabricate a second fictional event merely to repair lost meta-level exposure memory.

---

# 8. Gameplay communication obligations are independent

The simplified delivery contract is safe only because presentation does not own gameplay-significant pending work.

## LAW 5.12-13 — DELIVERY MAY NEVER SOLE-OWN A GAMEPLAY-SIGNIFICANT COMMUNICATION OBLIGATION

Anything that must survive until the player can validly act/respond remains owned by its native gameplay/runtime semantic owner.

Examples:

```text
pending Choice / response requirement
    -> Procedure / Continuation / Interaction owner

mandatory clarification needed to continue accepted input
    -> applicable Interaction/IntentPlan/Continuation semantics

fictional subject learned/heard a claim
    -> world.knowledge + semantic evidence

canonical NPC communication occurrence
    -> SemanticEvent / natural world/history owner

mechanically significant deadline/warning obligation
    -> owning process/procedure/policy
```

Loss or interruption of presentation may require re-explanation, but cannot erase the underlying requirement.

---

# 9. Re-presentation without replaying fiction

## LAW 5.12-14 — PRESENTATION REPAIR IS NOT A NEW FICTIONAL ACTION

If information from an already-established fictional event must later be repeated/clarified, the engine SHALL NOT create a second fictional event merely to compensate for presentation loss.

Examples:

- an NPC already said a line once;
- a clue was already perceived in fiction;
- an outcome already occurred;
- a pending choice already exists.

A later Master response may re-present the established state.

If exact wording remains protected under Step 5.11, it may be quoted exactly.

If only semantic meaning survives, summarize the prior occurrence without inventing an exact quotation.

A genuinely new in-fiction communication is a separate event and follows normal mechanics/history rules.

---

# 10. `runtime.message` exactness and Step 5.11

Step 5.11 defines exactness relative to HDM's accepted representation contract rather than undocumented physical-channel bytes/acoustics.

Step 5.12 resolves outbound exactness similarly.

## LAW 5.12-15 — OUTBOUND EXACTNESS IS EXACT TO THE EMISSION-COMMITTED HDM REPRESENTATION

For baseline outbound `runtime.message`, retained exact text/content means exact relative to the frozen representation committed by HDM at `EMISSION_COMMIT`.

It does not prove that every character was visibly rendered/read after unsupported interruption.

A Step-5.10/5.11 `STORY/TRANSCRIPT` projection may preserve that exact emission-committed representation with the same limitation.

No partial-render Transcript reconstruction is promised.

---

# 11. Recipient scope and multiplayer

## LAW 5.12-16 — HUMAN DISCLOSURE IS RECIPIENT-SCOPED

A delivery occurrence for Player A does not advance Player B's `runtime.disclosure` merely because:

- their PCs share a scene;
- the world fact is globally true;
- the same live state is readable by both Masters;
- the same output could have been generated for B.

Each material human exposure is attributed to the intended authenticated/bound recipient scope.

## LAW 5.12-17 — PLAYER EXPOSURE AND PC KNOWLEDGE REMAIN SEPARATE

Human output delivery does not automatically create or modify `world.knowledge`.

Fictional perception/knowledge comes from valid in-world channels and the owning semantic transition.

Conversely, a PC may know something that a human player has not yet been explicitly reminded/shown in the current presentation flow.

## LAW 5.12-18 — SHARED MULTI-HUMAN HOST SURFACES REQUIRE A HOST AUDIENCE CONTRACT

Baseline per-player disclosure assumes the runtime can resolve who the intended human recipient is for a response.

A single host surface simultaneously viewed by multiple humans cannot claim precise per-player disclosure without a Step-6 deployment/audience capability contract.

Do not invent per-person read receipts inside an undifferentiated shared UI.

---

# 12. Live/concurrent identity

Outbound message identity inherits Steps 5.8 and 5.11.

## LAW 5.12-19 — OUTBOUND MESSAGE IDENTITY IS SOURCE-NATIVE AND COLLISION-SAFE

Independently writable sessions/live scopes must be able to establish outbound message identity without a campaign-global pre-response sequential-ID reservation write.

Stable identity survives lawful live close/absorption.

The current legacy campaign-sequential `runtime.message` identifier policy is implementation debt where it conflicts with this law.

Story Transcript IDs remain separate Step-5.10 layer-local IDs.

## LAW 5.12-20 — DISCLOSURE MERGE USES SEMANTIC REVISION RELATIONS, NOT DELIVERY ORDER

Repeated exposures merge monotonically according to Step-4 fact/truth-transition semantics.

Do not choose “latest exposed objective status” from:

- Git commit order;
- host response order;
- wall-clock timestamp;
- lexical ID order.

Use the fact owner's semantic truth-transition/revision relation.

Contradictory/incomparable evidence where a linear relation is required is scoped integrity/reconciliation, not a transport tie-break.

---

# 13. Retry, regeneration, edit and branch

## LAW 5.12-21 — RETRY/REGENERATION DOES NOT RE-EXECUTE ACCEPTED GAMEPLAY

A host Retry/regeneration of an older Master response SHALL NOT be interpreted as permission to execute the underlying player action again.

No reroll, duplicate Resource spend, duplicate live mutation or second canonical consequence follows solely from presentation retry.

Reliable physical Retry ancestry/detection, when available, belongs to Step 6.

If a host cannot expose enough identity to guarantee coherent handling, that limitation belongs to the supported deployment profile; Step 5.12 does not compensate with a delivery journal.

## LAW 5.12-22 — OLD-MESSAGE EDIT/BRANCH IS NOT CANONICAL CORRECTION

Editing an old host message or branching from old host history cannot rewrite already accepted HDM history.

A current runtime must reconcile from current campaign authority before accepting new gameplay.

The normal player correction path is a new message/Interaction.

---

# 14. Story / Transcript handoff

Generated private Narrator drafts are not Transcript history.

An emission-committed outbound `runtime.message` is eligible as a Step-5.10/5.11 Transcript source candidate according to Selective Exact policy.

Step-5.10 layer coverage and Step-5.11 retention laws remain unchanged.

Story catch-up is never required before gameplay response delivery.

---

# 15. Auxiliary host surfaces

Step 5.12 does not create a universal render-tree or multimodal-delivery ledger.

The selected physical deployment still has a correctness obligation:

```text
PLAYER_VISIBLE surface
    -> must not contain material information outside that player's eligibility

NON_PLAYER_VISIBLE internal surface
    -> may carry private runtime material only if the host really guarantees invisibility
```

The exact surface inventory belongs Step 6.

---

# 16. Step-6 physical feasibility obligation

The most important unresolved **physical**, not semantic, question is whether the chosen ChatGPT/role topology can realize the Step-4/5.12 pre-player-visible validation boundary.

A host may stream tokens while a model response is being generated. Therefore Step 6 SHALL prove one supported mechanism equivalent to:

```text
material Narrator output complete enough for eligibility/disclosure validation
    BEFORE
that material output becomes player-visible
```

Possible physical realizations may include a staged internal Narrator result, host buffering, separate validated outer-render step or another equivalent topology.

Step 5.12 deliberately does not solve this by introducing an outbox, background agent or mandatory durable buffer.

If the chosen deployment cannot satisfy the logical information boundary, Step 6 must explicitly revisit physical topology/feasibility rather than silently weakening Step 4/5.12.

Step 6 also owns:

- physical model-call/role isolation;
- stable host invocation/message/revision identity feasibility;
- cheap Retry/edit/branch detection if exposed;
- player-visible auxiliary-surface inventory;
- authenticated recipient/audience mapping;
- optional stronger completed-message acknowledgement if cheaply available;
- latency/token/cost impact.

---

# 17. Explicit non-goals

Baseline Step 5.12 does **not** provide or require:

- durable delivery outbox;
- send queue;
- delivery worker/lease/heartbeat;
- background polling;
- post-render ACK state machine;
- `CONFIRMED / INDETERMINATE / FAILED` durable delivery lifecycle;
- per-token/per-prefix exposure tracking;
- exactly-once visible prose;
- human-read receipts;
- automatic replay of missed secrets;
- automatic reconstruction of interrupted responses;
- generic host Retry/edit/branch repair;
- generic multimodal render accounting;
- a second disclosure authority in live state;
- per-response Git publication solely for delivery bookkeeping.

---

# 18. Machine-realization debt

Later implementation work must realize at least:

1. `runtime.disclosure` catalog/schema/path contract;
2. outbound `runtime.message` schema/provenance/Step-5.11 compaction semantics;
3. typed NarrationResult disclosure refs;
4. deterministic eligibility/ref completeness validation;
5. logical/HOT `OutboundEmissionClosure` establishment;
6. Step-5.5/5.6 dirty publication/save/handoff integration;
7. collision-safe live/source-native outbound message IDs;
8. player/session recipient binding;
9. Step-5.10/5.11 Transcript source routing;
10. legacy live-state knowledge/disclosure cleanup;
11. auxiliary visible-surface fencing hooks as Step 6 determines necessary;
12. player-facing help/manual warning about interruption and host-history edit/Retry semantics;
13. tests covering normal emission, interruption limitation, crash RPO, Retry no-replay, multiplayer recipient isolation, exact/semantic re-presentation and zero-extra-write fast path.

The following are explicitly **not** machine-realization debt unless a future owner decision reopens them:

- durable delivery outbox;
- autonomous resend worker;
- partial-stream exposure ledger;
- generic delayed-delivery reconciliation;
- full host-history rewrite support.

---

# 19. Required regression cases

At minimum verify eventual realization against:

1. private/generated narration fails validation -> no emission closure;
2. invalid material disclosure ref -> block before supported emission boundary;
3. ordinary uninterrupted response -> outbound/disclosure closure establishes coherently;
4. ordinary response with no material disclosure -> no unnecessary disclosure record;
5. player interrupts after emission commit -> documented possible over-confirmation; no gameplay rollback/replay;
6. process loss after response but before disclosure durability -> recover durable state; later information may repeat;
7. pending Choice survives lost/interrupted presentation;
8. repeated explanation does not create a second NPC fictional utterance;
9. exact prior speech protected -> exact quotation allowed;
10. only semantic speech survives -> summary without invented quote;
11. one multiplayer player receives a secret while another does not;
12. concurrent outbound IDs do not require campaign-global reservation/write;
13. disclosure truth revision merge follows semantic lineage;
14. host Retry does not rerun command/mechanics/RNG;
15. old user-message edit does not retcon accepted Interaction;
16. branch from old host history reconciles from current campaign authority;
17. Story Transcript candidate comes from emission-committed outbound message, not private draft;
18. auxiliary visible surfaces cannot intentionally leak Narrator-ineligible facts;
19. gameplay publication followed by narration does not force a second repository commit;
20. clean ordinary response adds zero repository calls solely for delivery tracking.

---

# 20. Canonical exit statement

Step 5.12 is architecture-closed when the following invariant is accepted:

> **HDM validates material player-facing Master output before its supported emission-commit boundary, establishes recipient-scoped outbound communication/disclosure as a coherent normally-SOFT semantic closure, and keeps all gameplay-significant communication obligations with their native owners. Baseline play does not pay for a delivery-ack/outbox/partial-stream subsystem; interruption and host-history rewrite features are documented presentation-risk edges, while Step 6 must still prove a physical topology capable of enforcing the pre-player-visible information boundary.**

This closes Step 5.12 architecture and makes Step 5.13 / Garbage Collection & Orphan Cleanup the next numbered Step-5 slice after roadmap closure.