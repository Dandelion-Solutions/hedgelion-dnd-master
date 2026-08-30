# Step 5.12 — Host Delivery / Disclosure Boundary — Candidate Specification

Status: **CANDIDATE — REQUIRES ADVERSARIAL REVIEW**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Basis:

- Step-5.12 task brief;
- Step-5.12 research draft;
- Step-5.12 analytical challenge;
- canonical Steps 3, 4 and 5.1–5.11.

Candidate architecture direction:

> **CONFIRMATION-ONLY DISCLOSURE / MATCHED DELIVERY CANDIDATE + HOST EVIDENCE / SAFE UNDER-CONFIRMATION / SOFT CONFIRMED STATE / NO BASELINE DELIVERY OUTBOX / RECIPIENT-SCOPED OCCURRENCES / CAPABILITY-TIERED CONFIRMATION**

This candidate defines logical host-delivery and disclosure semantics. It does not select a physical ChatGPT message API, implement schemas/runtime code, define generic GC, or close Step-6 host/deployment feasibility.

---

# 1. Canonical intent of the candidate

HDM must never claim that a human player was exposed to material information merely because:

- Narrator generated it;
- core validated it;
- the engine intended to send it;
- an API model response completed;
- a host send was attempted;
- a previous response probably appeared;
- another player received the same payload.

Positive durable exposure authority requires evidence of a qualifying host-visible communication occurrence for that player.

At the same time, ordinary ChatGPT may not provide exactly-once delivery or a deterministic post-final callback. Therefore the architecture must remain safe when confirmation is unavailable.

The key recovery principle is:

> **When delivery cannot be confirmed, HDM under-confirms rather than inventing exposure. If the same currently eligible player later needs the information, HDM may communicate it again without replaying the underlying fiction or mechanics.**

---

# 2. Authority geometry

```text
CANONICAL / CURRENT SEMANTIC OWNERS

world/current owners
    objective/current game truth

world.knowledge
    fictional subject epistemic authority

runtime.disclosure
    confirmed material human-player exposure authority

runtime.message [outbound, qualified]
    stable historical communication evidence

LOG / SemanticEvent
    compact semantic/causal history

STORY/TRANSCRIPT
    noncanonical retained discourse projection


NON-AUTHORITATIVE / OPERATIONAL DELIVERY EVIDENCE

NarrationResult
ValidatedDeliveryCandidate
HostDeliveryEvidence
host UI/chat items
host retry/branch metadata
```

Neither `ValidatedDeliveryCandidate` nor `HostDeliveryEvidence` becomes current disclosure authority.

---

# 3. Core vocabulary

## 3.1 `NarrationResult`

Inherited Step-4 typed Narrator result:

```text
NarrationResult
    prose
    disclosure_refs[]
        fact_id
        aspect = statement | objective_status
        truth_transition_ref?   # required for objective_status
```

It is not proof of delivery.

## 3.2 `ValidatedDeliveryCandidate`

Deterministic core constructs a typed working value after NarrationResult validation and before host delivery qualification.

Conceptually:

```text
ValidatedDeliveryCandidate
    candidate_key              # host/runtime-local working identity
    source_interaction_ref?
    narration_source_refs[]
    delivery_units[]
        unit_local_key
        exact_payload
        payload_digest
        intended_recipient_player_ids[]
        disclosure_refs[]      # subset actually present in this unit
    host_profile
```

Properties:

- non-authoritative;
- not an outbound `runtime.message`;
- not `runtime.disclosure`;
- may remain purely volatile;
- losing it before confirmation is safe under-confirmation;
- a richer host may preserve equivalent structured metadata externally/durably.

A candidate exists to avoid reconstructing disclosure refs later through NLP over prose.

## 3.3 Delivery unit

A delivery unit is the smallest host-confirmable payload to which disclosure refs are bound.

Baseline may use one complete assistant message as one unit.

A host with discrete acknowledged segments may use smaller units.

Token-prefix inference is not a delivery unit.

## 3.4 `HostDeliveryEvidence`

Conceptual host-adapter evidence:

```text
HostDeliveryEvidence
    evidence_kind
    host_profile
    host_occurrence_ref?
    host_conversation_or_channel_ref?
    recipient_player_ids[] / audience evidence
    completed_unit_identity / payload_digest evidence
    outcome:
        CONFIRMED_EMITTED
        CONFIRMED_NOT_EMITTED
        INDETERMINATE
```

Exact physical fields are Step-6/implementation work.

Evidence is useful only under a documented host profile defining what its occurrence/status means.

## 3.5 Qualified delivery

A delivery unit is qualified only when deterministic core can establish:

```text
matching ValidatedDeliveryCandidate unit
AND
matching intended recipient(s)
AND
host evidence sufficient under current HostDeliveryPort profile
AND
complete unit/content binding
AND
outcome == CONFIRMED_EMITTED
```

Only qualified delivery can establish human exposure/history.

---

# 4. Delivery outcome law

## LAW 5.12-1 — DELIVERY OUTCOME IS NOT A BOOLEAN GUESS

Host-side outcome vocabulary is conceptually:

```text
CONFIRMED_EMITTED
CONFIRMED_NOT_EMITTED
INDETERMINATE
```

`INDETERMINATE` means exactly that: available evidence proves neither emission nor non-emission.

It SHALL NOT be silently converted into success/failure by timeout, retry count, model confidence, wall-clock duration, host UI intuition or repository order.

## LAW 5.12-2 — `runtime.disclosure` REMAINS POSITIVE CONFIRMED AUTHORITY

`runtime.disclosure` SHALL NOT add generic `possible/maybe` current states merely to represent delivery uncertainty.

Delivery uncertainty belongs to delivery evidence/working state.

Absence of confirmed disclosure means only:

> current durable/hot disclosure authority does not establish that this exact material exposure occurred.

It does not prove metaphysically that the human never saw it.

---

# 5. Disclosure advancement

## LAW 5.12-3 — ONLY QUALIFIED CONFIRMED EMISSION MAY ADVANCE DISCLOSURE

For each validated disclosure ref and each intended player recipient:

```text
qualified CONFIRMED_EMITTED occurrence
    -> runtime.disclosure may establish/advance exact aspect/revision exposure
```

No advancement from:

- generated prose;
- validated draft alone;
- prepared intent;
- send attempt;
- API `response.completed` without a host-delivery contract;
- next user message alone;
- payload hash alone;
- another recipient's confirmed delivery.

## LAW 5.12-4 — DISCLOSURE IS PER PLAYER

Human exposure is recipient-specific.

One physical payload may lead to:

```text
P1 confirmed
P2 rejected/not emitted
P3 indeterminate
```

Only P1 advances.

A host may prove one atomic shared-room occurrence for several recipients only if the host contract defines the relevant audience availability strongly enough. `runtime.disclosure` still materializes per player/fact as Step 4 requires.

## LAW 5.12-5 — CONFIRMED EXPOSURE DOES NOT IMPLY HUMAN COMPREHENSION

`CONFIRMED_EMITTED` means the host contract proves the complete delivery unit became an accepted player-facing host communication occurrence for the intended recipient/audience.

It does not prove:

- human read every word;
- human understood it;
- player agrees/believes it;
- controlled PC knows/believes it.

---

# 6. Outbound `runtime.message`

## LAW 5.12-6 — OUTBOUND MESSAGE IS ESTABLISHED ONLY AFTER QUALIFIED DELIVERY

A normal historical outbound `runtime.message` SHALL NOT be established merely because prose was generated or prepared.

On qualification, deterministic core may allocate/establish stable message evidence conceptually carrying:

```text
message_id
interaction/source linkage
direction = outbound
speaker/role/channel provenance
recipient/audience refs
exact payload while retained
payload digest
host occurrence/evidence ref where available
disclosure transition refs / semantic refs as provenance
payload_state under Step 5.11
source-domain enumeration identity
```

Exact wire fields remain implementation work.

## LAW 5.12-7 — MESSAGE IDENTITY IS NOT PAYLOAD HASH

Identical prose emitted twice may be two communication occurrences.

Same prose delivered independently to different host channels may be distinct occurrences.

Payload digest is a content-binding/integrity value, not the sole communication identity.

## LAW 5.12-8 — DELAYED CONFIRMATION DOES NOT REWRITE OCCURRENCE ORDER

If host evidence becomes available after the real host occurrence:

- confirmation/persistence time is not host occurrence time;
- campaign commit order is not host conversational order;
- neither becomes fictional chronology;
- preserve host occurrence identity/provenance where the profile supplies it.

---

# 7. Candidate/evidence matching

## LAW 5.12-9 — NO NLP RECONSTRUCTION OF DISCLOSURE REFS

Delayed confirmation SHALL NOT infer material exposure refs by re-reading old prose with an LLM/NLP classifier.

Qualification requires the validated structured candidate mapping to survive, or an equivalent trustworthy host-side structured binding.

If the binding is unavailable:

```text
no confirmed disclosure transition
```

Even if the human probably saw the prose.

## LAW 5.12-10 — CANDIDATE LOSS IS SAFE

`ValidatedDeliveryCandidate` need not be durable by default.

If it disappears before qualification:

- do not invent the old candidate;
- do not reconstruct exact refs from memory;
- do not establish outbound `runtime.message` for that lost occurrence;
- do not mark disclosure confirmed;
- future same-player presentation uses current eligible semantic sources as needed.

This is presentation/meta under-confirmation, not gameplay-state loss.

---

# 8. Durability semantics

## LAW 5.12-11 — NO BASELINE PRE-SEND DELIVERY OUTBOX

Step 5.12 introduces no mandatory durable `DeliveryIntent`, outbox queue, send job, worker claim, lease, heartbeat or background relay.

Rationale:

- prepared intent cannot prove external emission;
- no baseline background relay exists;
- losing an unconfirmed attempt is safely handled by under-confirmation;
- mandatory pre-send writes would add latency/contention to material reveals without protecting gameplay authority.

A future optional quality/audit feature may retain prepared delivery metadata if it does not alter confirmation semantics.

## LAW 5.12-12 — CONFIRMED DISCLOSURE MAY BE SOFT

Once host evidence qualifies delivery, current runtime may establish/update hot `runtime.disclosure` and outbound message evidence.

By default those established changes may be:

```text
ESTABLISHED + VOLATILE_DIRTY + MAY_DEFER
```

under Step 5.5 until an ordinary durability edge requires publication.

Step 5.12 does not create a universal per-reveal HARD commit.

## LAW 5.12-13 — CONTROLLED HANDOFF/SAVE HONORS CONFIRMED DIRTY DISCLOSURE

If a controlled handoff/save promise includes future context correctness dependent on confirmed exposure, the dirty confirmed disclosure/message evidence participates in the applicable Step-5.4/5.5 closure.

A controlled handoff may not knowingly discard an already established confirmed exposure relation required by the promised resume point.

## LAW 5.12-14 — UNEXPECTED LOSS MAY DEGRADE TO UNDER-CONFIRMATION

If confirmed exposure existed only in destroyed volatile state and had not reached a required durability edge:

- cold recovery returns to actual durable disclosure state;
- the lost exposure is not invented;
- same-player information may later be re-presented if current eligibility permits and the current task needs it;
- gameplay/world mechanics are not replayed.

This is the disclosure-specific application of Steps 5.4/5.5 unexpected-loss semantics.

---

# 9. Safe under-confirmation / re-presentation

## LAW 5.12-15 — ABSENCE OF DISCLOSURE NEVER GRANTS DELIVERY ELIGIBILITY

Under-confirmation repair does not mean “repeat every missing secret.”

Before presenting/re-presenting material X:

```text
current role/player eligibility
+ current source availability
+ current purpose/context
```

must independently authorize the presentation.

Old intended/possible delivery never bypasses current access/spoiler/role rules.

## LAW 5.12-16 — WHEN MATERIAL IS REQUIRED, SEMANTIC RE-PRESENTATION MAY BE AT-LEAST-ONCE

If the same authenticated eligible player needs X for meaningful continuation but confirmed exposure is absent/unknown:

- HDM MAY present X again;
- duplicate presentation is preferable to permanently assuming the player received something that may have failed;
- exact old prose need not be reproduced unless Step-5.11 exact retention independently requires/allows it.

No mechanics, RNG, fictional observation or world transition is replayed solely to communicate the already-established semantic information again.

## LAW 5.12-17 — NO GENERIC REPLAY LOOP

HDM SHALL NOT maintain a generic queue that repeatedly emits every old unconfirmed delivery attempt.

Re-presentation is demand/context driven from current authoritative/eligible semantics.

If the current player proceeds without needing a lost exposure, no repair write/message is required merely to close historical ambiguity.

---

# 10. Partial / interrupted output

## LAW 5.12-18 — QUALIFICATION UNIT MUST BE HOST-CONFIRMABLE AS COMPLETE

Because text generation may be stopped and voice may be interrupted, a planned full response is not confirmed merely because some prefix appeared.

Disclosure refs bind to one complete host-confirmable delivery unit.

If only full assistant-message completion can be proven:

```text
full message confirms together
partial message confirms nothing for runtime.disclosure
```

unless a stronger host profile supplies acknowledged sub-message segments.

## LAW 5.12-19 — ACKNOWLEDGED SEGMENTATION IS OPTIONAL, NOT TOKEN TELEMETRY

A richer profile MAY define multiple semantic delivery units, each with:

- exact payload/digest;
- disclosure-ref subset;
- discrete host occurrence evidence.

Do not infer disclosure from arbitrary token offsets or streamed prefixes without a host contract.

---

# 11. Host capability profiles

Step 5.12 defines semantic confirmation routes; Step 6 determines which are physically available.

## Profile route H1 — immediate acknowledged emission

Host operation returns sufficient evidence in the same runtime opportunity:

```text
exact occurrence/item identity
complete payload binding
recipient/audience binding
confirmed host-surface admission
```

Core can qualify immediately.

## Profile route H2 — interleaved acknowledged delivery unit

Host supports:

```text
emit discrete user-visible unit
    -> host confirms/adopts unit under documented contract
    -> deterministic/tool continuation remains available
```

Core may qualify before the turn ends.

Current development commentary/tool behavior is feasibility evidence only; Step 6 must prove portability and item semantics.

## Profile route H3 — deferred trusted host item evidence

A later invocation/adaptor supplies a completed exact host item/occurrence identity matching the still-available `ValidatedDeliveryCandidate`.

Core qualifies then.

A later user message alone does not qualify.

## Profile H0 — no qualifying evidence

Host supplies no evidence sufficient for confirmed delivery.

Consequences:

- no confirmed outbound message/disclosure from that occurrence;
- gameplay remains safe;
- historical/disclosure fidelity may degrade under host loss;
- current semantic information may be presented again when needed and eligible.

H0 is a safe degraded evidence profile, not permission to fabricate success.

## LAW 5.12-20 — HOST PROFILE CHANGES CONFIRMATION LATENCY, NOT DISCLOSURE MEANING

All profiles share the same Step-4 `runtime.disclosure` semantics.

A stronger host cannot redefine exposure truth; it merely provides better evidence sooner/more reliably.

---

# 12. Retry / Try again / regeneration

## LAW 5.12-21 — HOST REGENERATION IS PRESENTATION REGENERATION, NOT GAMEPLAY REPLAY

When a user requests Try again / Retry for an assistant answer whose gameplay result already exists:

```text
existing accepted/canonical result
    -> assemble lawful eligible presentation source
    -> new NarrationResult / delivery candidate
```

It SHALL NOT by itself:

- create another RuntimeCommand;
- reroll RNG;
- repeat resource costs;
- duplicate world transitions;
- duplicate live mutation;
- rewind campaign authority.

Physical recognition/fencing of retry invocations is a Step-6 host identity requirement layered on Step-3 idempotency.

## LAW 5.12-22 — EACH REGENERATED VARIANT IS A DISTINCT DELIVERY GENERATION

Different generated prose is not silently the same communication merely because it responds to the same original player action.

If variant A and B are both qualified emitted:

```text
confirmed exposure = monotonic union of material information actually emitted in A and B
```

A later visible variant cannot make the human unsee an earlier confirmed variant.

## LAW 5.12-23 — RETRY FROM STALE HOST CONTEXT MUST FENCE AGAINST CURRENT CAMPAIGN AUTHORITY

A host retry/old-context invocation cannot use old visible conversation as authority for new repository/gameplay writes.

Before any side effect that could affect campaign state, normal current-authority/idempotency/routing checks apply.

If the platform cannot expose sufficient invocation identity to distinguish retry safely, Step 6 must supply a conservative resync/presentation-only profile or declare the capability limitation.

---

# 13. Branching

## LAW 5.12-24 — HOST BRANCH DOES NOT BRANCH CAMPAIGN AUTHORITY

Branch in a new chat creates a host conversation lineage only.

New gameplay from that branch must resolve current campaign authority through Steps 5.7/5.8 before accepted mutation.

## LAW 5.12-25 — CONFIRMED HUMAN EXPOSURE IS NOT BRANCH-LOCAL

If player P was durably confirmed exposed to X, branching from before the visible message does not retract:

```text
runtime.disclosure(P,X)
```

The human cannot be made to unsee information by UI branching.

If exposure was real but not durably confirmed, the branch may conservatively under-confirm/re-present it later.

---

# 14. Multiplayer / live

## LAW 5.12-26 — PLAYER DELIVERY AND PC PERCEPTION REMAIN SEPARATE

Example:

```text
PC_A canonically perceives X
world.knowledge(PC_A,X) established
host delivery to player A fails/unconfirmed
```

This is valid.

Later narration to player A communicates already-established PC knowledge without rerunning the perception/event.

Human host delivery cannot itself create PC knowledge.

## LAW 5.12-27 — LIVE STATE MUST NOT BECOME SECOND GLOBAL DISCLOSURE AUTHORITY

Legacy live hot-state may retain operational observation/delivery routing evidence where needed, but current human-player exposure authority remains `runtime.disclosure`.

Live absorption shall normalize any required durable confirmed exposure/history according to the final Step-5.12/Step-5.8 implementation contract rather than preserving parallel writable truth.

## LAW 5.12-28 — DELIVERY FAILURE DOES NOT ROLLBACK LIVE/CAMPAIGN FACT

A shared fact already established under Step-5.8/live publication remains established even if player-facing narration fails.

The presentation may be retried from current authoritative state.

---

# 15. Story / Transcript

## LAW 5.12-29 — ONLY QUALIFIED OUTBOUND COMMUNICATION ENTERS TRANSCRIPT SOURCE DOMAIN

`STORY/TRANSCRIPT` SHALL NOT ingest:

- NarrationResult drafts;
- validated but unemitted candidates;
- indeterminate host attempts;
- partial/unconfirmed response prefixes.

A qualified outbound `runtime.message` is the normal source identity.

## LAW 5.12-30 — LOST UNCONFIRMED OUTPUT MAY BE ABSENT FROM STORY

If the human actually saw prose but host confirmation/candidate evidence was lost before establishment, Story may never receive that exact output.

Under Step-5.11 Selective Exact, this is lawful historical-fidelity loss and not canon loss.

## LAW 5.12-31 — LATER MESSAGE COMPACTION DOES NOT ERASE DISCLOSURE

After confirmed outbound message/disclosure establishment, Step 5.11 may compact exact payload while preserving sufficient source/provenance identity.

`runtime.disclosure` remains current authority; it does not depend on retaining every exact outbound byte forever.

---

# 16. OOC and objective-status exposure

## LAW 5.12-32 — OOC DISCLOSURE USES THE SAME DELIVERY QUALIFICATION

A player-facing OOC statement that exposes objective truth status advances disclosure only after qualified delivery, even if no PC knowledge changes.

Unexpected loss before durable confirmation may cause repeated OOC explanation later; it never changes objective truth.

---

# 17. Pending choices / prompts

## LAW 5.12-33 — DELIVERY DOES NOT OWN PENDING GAMEPLAY DECISIONS

If a player must choose/react/respond, the unresolved gameplay state remains with Procedure/Continuation/Interaction/native Step-3 owner.

Failed/lost delivery may require re-presenting the choice prompt.

It SHALL NOT cause:

- loss of the actual pending choice;
- duplicate execution;
- a generic delivery queue becoming execution authority.

---

# 18. Recovery protocol

Cold recovery does not scan host/chat history.

Conceptually:

```text
recover current campaign/native gameplay owners
recover durable runtime.disclosure
recover qualified outbound runtime.message evidence only when relevant
rebuild current Context Assembler

unconfirmed/lost delivery attempts
    -> not reconstructed as exposure
```

If current task for player P requires information X that current eligible semantics say P may receive but disclosure does not prove prior exposure:

```text
present/re-present X as needed
without replaying original mechanics/event
```

No generic delivery attempt registry is required for cold gameplay readiness.

---

# 19. Conflict / publication interaction

Confirmed delivery/disclosure publication uses ordinary Step-5.6 campaign publication semantics when it becomes due under Step 5.5.

A Git conflict while publishing disclosure/message evidence:

- does not undo actual human exposure;
- does not rerun host delivery automatically;
- refreshes current campaign state and reapplies/merges the monotonic disclosure transition when semantically compatible;
- uses stable recipient/fact/revision/message identities to avoid duplicate current rows;
- never replays mechanics/RNG.

If publication result is INDETERMINATE, resolve campaign ref/lineage under Step 5.6 before retrying the repository transition.

Host-delivery ambiguity and Git-publication ambiguity are separate domains.

---

# 20. Integrity conditions

Potential integrity defects include:

- disclosure row references a nonexistent/invalid fact;
- objective-status exposure lacks required truth transition ref;
- disclosure claims confirmed exposure from evidence that cannot qualify under its recorded host profile;
- outbound message marked qualified but source candidate/evidence digest mismatch is detected;
- one delivery occurrence attributed to wrong authenticated player;
- live/campaign duplicate writable disclosure authority appears;
- Story Transcript labeled verified delivered from only draft/unconfirmed source;
- Retry causes duplicate RuntimeCommand/world transition rather than presentation-only regeneration.

Not integrity defects by themselves:

- player likely saw material but disclosure is absent after crash;
- exact old outbound prose is unavailable under Selective Exact;
- duplicate same-player re-presentation after uncertainty;
- host delivery evidence is INDETERMINATE;
- one player confirmed while another did not.

---

# 21. Performance contract

Ordinary gameplay shall not add host-delivery maintenance scans.

Expected behavior:

```text
ordinary narration, no durable material disclosure transition
    -> no Step-5.12 repository write required

qualified disclosure in surviving host
    -> update sparse hot disclosure/message evidence
    -> ordinary later Step-5.5 publication unless another edge applies

strong immediate-ACK host
    -> qualification same invocation

deferred evidence host
    -> bounded matching by current candidate/host occurrence

H0 host
    -> no fabricated confirmation, no background polling
```

No campaign-wide message scan, chat-history scan, generic delivery queue, worker or heartbeat.

---

# 22. Baseline guarantees

HDM baseline SHALL guarantee:

1. no false confirmed human exposure from generation/intent alone;
2. no gameplay/RNG replay merely because presentation is retried;
3. confirmed disclosure remains player-specific and separate from PC knowledge;
4. confirmed exposure, once durable, survives host chat edit/retry/branch/delete;
5. under uncertainty, current disclosure authority stays conservative;
6. same-player eligible semantic re-presentation can repair omission;
7. partial response is not treated as complete without host proof;
8. Story Transcript never treats an unemitted draft as delivered history;
9. ordinary gameplay does not require background delivery processing.

HDM baseline does NOT guarantee:

```text
exactly-once host-visible prose
proof the human read/understood the output
no repeated information after an unexpected crash
permanent exact transcript of every output
immediate durable publication of every disclosure
host Retry/Branch machine identity on profiles that do not expose it
```

---

# 23. Step-6 capability requirements

Step 6 must determine for every supported physical host profile:

1. Is there a stable invocation identity sufficient for Step-3 idempotency?
2. Is Retry/regeneration machine-detectable?
3. Is branch/conversation identity machine-visible?
4. Does the host expose stable assistant output item/response identity?
5. Can it prove complete player-facing item admission?
6. Can exact payload/content digest be bound to that item?
7. Are recipient/audience semantics explicit?
8. Can delivery be acknowledged in the same invocation?
9. Can user-visible intermediate/discrete output be followed by deterministic/tool continuation?
10. Does any host operation accept an idempotency key/dedupe identity?
11. If only deferred confirmation exists, can `ValidatedDeliveryCandidate` remain trustworthy until evidence arrives?
12. If none of the above exists, confirm the H0 safe-degraded semantics and UX implications.

Step 6 may improve physical confirmation without changing Step-5.12 authority laws.

---

# 24. Step-5.13 handoff

Step 5.13 receives these retention/GC constraints:

- durable confirmed `runtime.disclosure` rows remain current authority until their own lifecycle says otherwise;
- qualified outbound message envelope may compact under Step 5.11 but cannot be deleted while a protected provenance/debug/Story consumer requires it;
- volatile/unqualified delivery candidates require no physical GC architecture after host loss;
- optional delivery evidence records, if a future profile persists them, need bounded lifecycle and cannot be retained forever merely because an attempt was ambiguous;
- no orphan prepared-delivery queue exists in baseline.

---

# 25. Required adversarial review matrix

Review MUST test at least:

```text
generation fails before validation
invalid disclosure ref rejected
canon commits, narration generation fails
host output fails before complete emission
host output partially streams then user stops
host output completes but immediate confirmation unavailable
host confirms exact item immediately
host returns confirmed rejection
host returns indeterminate
player closes app immediately after reveal
chat crashes after exposure before disclosure durability
controlled handoff after confirmed dirty exposure
explicit save after confirmed dirty exposure
new chat after under-confirmed reveal
same chat continues with exact completed host item evidence
same chat continues without deterministic host evidence
user asks about fact they saw but disclosure lost
current eligibility revoked before possible re-presentation
Retry same output
Retry different output
Retry reveals additional fact
Retry from stale campaign context
Branch from before confirmed reveal
Branch from before under-confirmed reveal
chat deletion after confirmed disclosure
chat deletion before durable confirmation
private P1 reveal
P1 confirm/P2 fail
P1 confirm/P2 indeterminate
PC knowledge established, player delivery fails
shared live fact commits, narration fails
live epoch closes with dirty confirmed disclosure
Story sees qualified outbound message
Story sees only candidate/unconfirmed output
message exact payload compacted after disclosure
publication conflict while persisting confirmed disclosure
Git publication ACK indeterminate after actual human exposure
100k-message campaign reconciles no global history
voice/interrupted output
interleaved visible unit profile
H0 host profile
```

---

# 26. Candidate status

No owner decision is currently required.

The candidate advances to adversarial review.

Confidence: **MEDIUM-HIGH**.

Main remaining risk:

> whether the boundary between “host-confirmable complete output unit” and ordinary ChatGPT's actual exposed runtime capabilities is precise enough to avoid a semantic spec that is safe but too degraded in practice.

That risk belongs partly to Step-6 feasibility, but Step-5.12 adversarial review must still ensure H0/deferred profiles produce coherent gameplay rather than merely avoiding false claims.
