# Step 5.12 — Host Delivery / Disclosure Boundary — Research Draft

Status: **RESEARCH DRAFT — NOT CANONICAL**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Task brief:

- `2026-08-21-step-5-12-host-delivery-disclosure-boundary-task-brief.md`

This document records repository findings, current platform evidence, assumptions, failure windows, alternative evaluation and preliminary architecture hypotheses. It intentionally does not yet select a canonical model.

---

# 1. Executive research result

Step 5.12 is a two-system epistemic problem:

```text
HDM CAMPAIGN / RUNTIME EVIDENCE
        != atomic with
CHATGPT HOST-VISIBLE OUTPUT
```

No evidence found supports treating the two as one distributed transaction.

The most important early result is asymmetric risk:

```text
FALSE POSITIVE DISCLOSURE
    HDM says player saw X
    but X never reached a qualifying host-visible surface

    consequence:
        future context may omit X permanently
        spoiler/disclosure logic may assume exposure that never occurred
        user may lose necessary information

FALSE NEGATIVE DISCLOSURE
    player did see X
    but HDM has not durably confirmed it

    consequence:
        HDM may repeat X to the same player
        hide material the player already knows
        require re-confirmation/re-delivery
```

Under existing Step-4 authority semantics, false positive is materially more dangerous.

This strongly favors a **confirmation-only `runtime.disclosure`** model:

> absence/unconfirmed means HDM must not assume the human was exposed.

However, this does not yet answer how confirmation is obtained in ordinary ChatGPT, nor whether durable pending/prepared delivery evidence is justified. Those remain under challenge.

---

# 2. Verified repository facts

## FACT R1 — Step 4 already fixed disclosure ownership

`runtime.disclosure` is the sole campaign-durable current human-player exposure owner for material information whose prior exposure matters later.

It is distinct from:

- `world.knowledge`;
- objective truth;
- Transcript;
- Narrator prose;
- host chat history.

Narrator returns structured `disclosure_refs[]`; those refs are validated before emission.

Step 4 explicitly states:

```text
generation/emission failure before the qualifying boundary
    -> disclosure must not be recorded as delivered
```

and:

```text
host-visible exposure
    != proof the human literally read/understood it
```

## FACT R2 — Step 3 gives Interaction stable external-exchange identity

`runtime.interaction` owns one accepted external exchange/invocation identity and raw-message linkage.

Transport retry of the same accepted invocation must not replay gameplay.

Same prose in a later intentional turn is a new Interaction.

Therefore delivery retry, disclosure retry and gameplay execution retry are separate identities/problems.

## FACT R3 — Step 5.6 already has correct acknowledgement epistemics

Campaign publication recognizes:

```text
CONFIRMED_ACCEPTED
CONFIRMED_REJECTED
INDETERMINATE
```

A lost acknowledgement is not silently success or failure.

The conceptual lesson transfers to host delivery: external side-effect uncertainty must not collapse into a boolean merely because the schema would be easier.

## FACT R4 — Step 5.11 reserves outbound message establishment for 5.12

Step 5.11 canonical law:

```text
NarrationResult generated
    !=
qualified outbound communication occurrence
```

Only Step-5.12-qualified delivery may establish outbound `runtime.message` / Transcript source candidacy.

Generated-but-unemitted drafts are excluded.

## FACT R5 — `runtime.message` exists conceptually but its machine shape is absent

Current DEV catalog admits:

```text
runtime.message
runtime.interaction
```

Current identifier policy gives `runtime.message` a legacy campaign-sequential allocator.

No current DEV message schema was found in `DEV/SCHEMAS/`.

Step 5.11 already marks legacy campaign-only message allocation as incompatible debt where live-born identities require Step-5.8-safe source-native IDs.

## FACT R6 — `runtime.disclosure` is not yet realized in current machine catalog/schema

Step 4 canonical semantics exist, but current `core-catalog.json` runtime kinds do not yet include `runtime.disclosure` and no current disclosure schema was found.

This is machine-realization debt, not authority ambiguity.

## FACT R7 — session records are intentionally sparse and non-transcript

Current `session.schema.yaml` says session metadata is coordination/recovery data, not full chat history, and is updated at persistence boundaries rather than every turn.

This makes `runtime.session` a poor candidate to become the sole semantic owner of delivery/disclosure facts.

## FACT R8 — legacy live runtime mixes old wording that must not become duplicate disclosure authority

Current legacy `LIVE_SCENE.md` prose permits compact `per-PC knowledge/disclosure information`, while Step 4 later establishes `runtime.disclosure` as human exposure authority and `world.knowledge` as fictional epistemic authority.

Step 5.12 must preserve live-local operational evidence/recipient routing where useful, but eventual machine realization must not leave a second writable global disclosure owner in live hot-state.

## FACT R9 — live gameplay already follows commit-before-reveal for shared canonical facts

Legacy live runtime requires newly established actionable shared facts to become live-canonical before narration exposes them.

This does not solve human-delivery acknowledgement, but it fixes one ordering law:

```text
shared canonical fact establishment
    before
narration that claims that fact
```

Delivery failure must never roll back the already accepted shared fact.

## FACT R10 — controlled handoff and unexpected crash have intentionally different guarantees

Step 5.4 allows unexpected loss to fall back to actual durable state and forbids invented lost volatile state.

A controlled handoff must durably materialize every promised semantic dependency before acknowledgement.

This distinction can apply to dirty confirmed disclosure state:

```text
unexpected crash before disclosure publication
    may lose unpersisted confirmation if policy permits

controlled handoff
    cannot promise continuity while knowingly dropping required confirmed disclosure state
```

---

# 3. Verified/current OpenAI platform evidence

These are product facts as of 2026-08-21 and must be reverified before implementation.

## FACT P1 — users can Edit / Retry / Branch

OpenAI Help currently documents that ChatGPT users can:

- edit an earlier user message;
- choose Try again / Retry on an assistant response;
- choose Branch in a new chat and continue from an earlier point.

This means host conversation position is mutable presentation lineage, not immutable campaign history.

Source:

- OpenAI Help Center, current GPT-5.5 in ChatGPT article, “Editing messages and retrying responses”.

## FACT P2 — chats can be deleted and are not recoverable through normal product use

OpenAI Help documents:

- chats remain until deleted;
- deleted chats disappear from visible history immediately;
- deletion from systems is scheduled within 30 days subject to stated exceptions;
- deleted chats cannot be recovered through UI/API/support.

Source:

- OpenAI Help Center, “Chat and File Retention Policies in ChatGPT”;
- “How to Delete and Archive Chats in ChatGPT”.

## FACT P3 — project/memory is contextual assistance, not exact immutable delivery evidence

OpenAI Help documents project memory and saved/chat-history memory as contextual features. Memory can be updated/combined/removed and chat-history reference does not retain every detail.

Therefore it cannot be used as the exact durable delivery ledger required by Step 4.

Sources:

- OpenAI Help Center, “Projects in ChatGPT”;
- “Memory FAQ” / chat-history memory documentation.

## FACT P4 — API `response.completed` means model response completed

OpenAI Responses API documentation defines `response.completed` as an event emitted when the model response is complete. API response objects and assistant output items have stable IDs in that API surface.

No official source found says this API event proves that an ordinary ChatGPT UI successfully rendered/persisted the output to the intended human-facing surface.

Therefore:

```text
Responses API generation completion
    != documented ordinary ChatGPT delivery acknowledgement
```

Sources:

- OpenAI Developers API reference for Responses;
- response create / streaming event documentation.

## FACT P5 — ordinary ChatGPT can produce incomplete/interrupted responses

OpenAI Help explicitly instructs users to click “Stop generating” and then regenerate when a response is stuck.

Voice documentation also permits interruption while ChatGPT is speaking.

Therefore:

```text
next user activity
    != automatically proof that the entire prior planned payload was emitted
```

unless the host can prove prior output completion/exact content.

Sources:

- OpenAI Help Center, “Troubleshooting ChatGPT Error Messages”;
- “ChatGPT Voice”.

## FACT P6 — richer API/custom-host surfaces have stronger identity than currently documented ordinary ChatGPT runtime

Responses API/Conversation surfaces expose response/output-item IDs. A custom application can retain those IDs and control request/stream processing.

This is evidence that a stronger `HostDeliveryPort` profile is feasible in custom/API deployments.

It is not evidence that ordinary ChatGPT exposes those IDs to HDM runtime/tool code.

---

# 4. Current harness observation — useful but not yet portable fact

## OBSERVATION H1 — user-visible intermediate assistant updates can precede later tool calls in this development harness

In the current ChatGPT development conversation, the assistant can emit user-visible commentary/progress text and then continue invoking tools before the final answer.

This suggests a possible host profile in which:

```text
visible emission unit
    -> deterministic/tool continuation
    -> disclosure persistence
```

could be physically possible within one turn.

However:

- this is not yet an official ordinary-ChatGPT gameplay contract;
- commentary/progress UI may have different persistence/branching semantics from a normal assistant answer;
- shipped GAME instructions may not be able to require the same channel behavior on every supported plan/product surface.

Therefore H1 is a **Step-6 feasibility input**, not a Step-5.12 baseline fact.

---

# 5. External systems research

## FACT X1 — dual write is a recognized consistency problem

AWS and Microsoft transactional-outbox guidance both describe the same core failure:

```text
write business state to system A
send external event to system B
```

cannot be treated as atomically successful when the systems are independent; a crash between operations can leave one side advanced and the other not.

Sources:

- AWS Prescriptive Guidance, Transactional Outbox Pattern;
- Microsoft/Azure transactional outbox design pattern.

## FACT X2 — classic outbox depends on a later relay

Traditional transactional outbox solves lost notification by atomically storing an outbox event with business state, then having another process/change-feed relay it.

HDM ordinary ChatGPT baseline has no required background worker.

Therefore importing an outbox queue literally would add infrastructure without supplying the normal relay assumption.

The applicable lesson is narrower:

> freeze durable side-effect intent when no later reconstruction is safe; never confuse prepared intent with confirmed external effect.

## FACT X3 — exactly-once retry needs receiver cooperation or equivalent coordination

Stripe documents idempotency keys as the mechanism that makes ambiguous retries safe: the server recognizes the same request and returns/reuses the first outcome.

Without a host-controlled idempotency key or equivalent message identity/dedupe contract, HDM cannot honestly claim exactly-once host-visible delivery.

Sources:

- Stripe API, Idempotent Requests;
- Stripe error handling documentation.

## FACT X4 — indeterminate external result is a legitimate state

Stripe error guidance explicitly treats some connection/API errors as indeterminate rather than assuming success/failure.

This supports the same epistemic rule already present in Step 5.6:

```text
unknown outcome remains unknown until evidence resolves it
```

---

# 6. Assumption / evidence ledger

| ID | Statement | Status | Confidence | Impact if false / revisit |
|---|---|---|---|---|
| A1 | Ordinary ChatGPT exposes a deterministic post-final-render callback to HDM in the same invocation. | **OPEN / NO PUBLIC CONTRACT FOUND** | medium-high that baseline cannot rely on it | Strict post-final commit cannot be baseline unless Step 6 finds a supported mechanism. |
| A2 | A later invocation may contain the prior assistant output as conversation context. | **PRODUCT BEHAVIOR / NOT YET A DETERMINISTIC CORE INTERFACE** | high | Useful only if Step 6 can expose trustworthy host evidence to core; LLM recollection alone is insufficient. |
| A3 | Ordinary ChatGPT exposes stable assistant message/response IDs to runtime/tools. | **OPEN / NO PUBLIC CONTRACT FOUND** | medium-high that baseline cannot rely on it | Host-history confirmation and dedupe need weaker fallback or Step-6 capability requirement. |
| A4 | Retry exposes machine-readable identity/ancestry tying regenerated answer to previous answer. | **OPEN / NO PUBLIC CONTRACT FOUND** | medium-high that baseline cannot rely on it | Retry must be fenced conservatively; Step 6 may need explicit host capability. |
| A5 | Branch exposes machine-readable branch identity to HDM runtime. | **OPEN / NO PUBLIC CONTRACT FOUND** | medium-high that baseline cannot rely on it | Campaign current authority must win regardless; host lineage optimization optional. |
| A6 | Ordinary ChatGPT assistant delivery accepts an HDM-supplied idempotency key. | **NO EVIDENCE / DO NOT ASSUME** | high | Exactly-once host delivery cannot be baseline guarantee. |
| A7 | One ordinary gameplay ChatGPT conversation normally corresponds to one human player binding. | **PROJECT DESIGN ASSUMPTION TO VALIDATE IN STEP 6** | medium | Group/shared host surfaces require per-recipient or audience semantics. |
| A8 | Repository/tool writes can occur before the ordinary final answer in one invocation. | **OBSERVED IN CURRENT HARNESS** | high for this harness | Useful for pre-send state; not proof of post-send persistence ability. |
| A9 | A new chat cannot be trusted to reconstruct exact previous host output from host history. | **SUPPORTED BY RECOVERY CONTRACT / PRODUCT MUTABILITY** | high | New-chat baseline must rely on campaign evidence, not exact old host chat. |
| A10 | API response completion is different from documented human-visible ChatGPT delivery. | **FACT / NO DOCUMENTED EQUIVALENCE** | high | Do not use `response.completed` as ordinary ChatGPT delivery proof. |
| A11 | A next user message proves the entire prior assistant payload completed. | **FALSE IN GENERAL** | high | Stop-generating/partial output invalidates naive next-turn confirmation. |
| A12 | User-visible intermediate messages can be followed by tools in all target ChatGPT gameplay profiles. | **OBSERVED HERE, NOT PORTABLE CONTRACT** | low-medium | Treat as optional host profile until Step 6 verifies. |

---

# 7. Current-state ownership inventory

| Concept | Semantic owner | Current physical state | 5.12 disposition |
|---|---|---|---|
| accepted player invocation | `runtime.interaction` | canonical concept; realization partial | preserve |
| inbound communication evidence | `runtime.message` | catalog/ID concept, no final schema | Step 5.11 owns retention |
| NarrationResult | Narrator typed result, non-authority | conceptual | input to delivery |
| material disclosure ref | Narrator typed output validated by core | conceptual | freeze before qualifying delivery |
| human player exposure | `runtime.disclosure` | Step-4 canonical; machine realization absent | sole current owner |
| outbound historical communication | `runtime.message` after qualification | not machine-realized | 5.12 defines admission |
| Story Transcript | noncanonical Story projection | conceptual/no final machine surface | confirmed message only |
| current host UI item | ChatGPT product | external/mutable | evidence source only, never campaign authority |
| live PC perception | `world.knowledge` / live native evidence before normalization | legacy live structures | separate from human disclosure |
| live human delivery | no finalized live owner | legacy wording ambiguous | must not create duplicate `runtime.disclosure` authority |
| pending/ambiguous host emission | **not yet owned** | absent | central design question |

---

# 8. Failure-window inventory

## W1 — canon commits, narration never generates

```text
canonical consequences = established
human disclosure = none
outbound message = none
```

Correct behavior:

- do not roll back canon;
- later Narrator may describe the already-established result;
- no gameplay replay.

## W2 — NarrationResult validated, final host output fails before qualifying emission

Correct behavior:

- no confirmed disclosure;
- no established outbound message;
- retained draft/preparation only if an independent recovery contract deliberately owns it.

## W3 — host output actually becomes visible, process/runtime cannot persist confirmation

This is the central false-negative window.

Safe fallback:

- campaign remains unaware/unconfirmed;
- later runtime must not assume exposure;
- same-player re-disclosure is allowed when needed;
- do not rerun gameplay.

Open question:

- should any pre-send durable preparation exist to improve fidelity/recovery?

## W4 — disclosure is persisted before host output, but output never becomes visible

This is false-positive exposure.

Preliminary result:

- unacceptable as default current-authority transition;
- a pre-send record may say only `prepared/intended`, never `confirmed disclosed`.

## W5 — host ACK is lost/indeterminate

Correct behavior:

- outcome remains indeterminate at delivery-evidence layer;
- do not blindly resend if duplicate costs are material;
- do not mark disclosure confirmed without qualifying evidence.

If re-delivery to the same player is semantically safe, the system may prefer duplicate presentation over permanent omission, but this is a retry policy, not proof that the first attempt failed.

## W6 — user stops response mid-stream

Potential result:

- some prefix may be visible;
- later disclosure refs may never have appeared;
- next user action alone does not prove complete delivery.

Therefore final-payload-level confirmation requires completion/exact-message evidence, or disclosure must be segmented at a host boundary the adapter can actually acknowledge.

## W7 — user retries/regenerates old assistant answer

Potential result:

- multiple distinct prose variants may become human-visible;
- each variant may expose different facts;
- the human cannot be made to unsee earlier variant merely because UI now shows another branch/version;
- Retry must not rerun old gameplay/tool side effects.

If multiple variants are genuinely confirmed emitted, disclosure is the monotonic union of the material information each actually exposed.

## W8 — branch created before/after reveal

Branch history may omit later original-chat messages, but branch creation does not erase human exposure already established elsewhere.

Campaign `runtime.disclosure` remains player-global campaign authority, not branch-local cursor state.

A branch cannot roll campaign world state back.

## W9 — chat deleted after reveal

Confirmed durable disclosure survives.

Unconfirmed volatile exposure may be forgotten and re-revealed later. This is a false-negative presentation loss, not canon loss.

## W10 — multiplayer: one recipient succeeds, another fails

Required state:

```text
P1 confirmed exposed
P2 unconfirmed/not exposed
```

No group boolean may widen one recipient’s outcome to another.

## W11 — PC canonically learns X, human delivery fails

Required separation:

```text
world.knowledge(PC, X) = current true epistemic relation
runtime.disclosure(player, X) = not confirmed
```

Later narration may communicate X again from already-established knowledge without replaying the fictional observation/event.

---

# 9. Alternative analysis — first pass

Legend:

```text
+++ strong
++  good
+   acceptable
-   material weakness
--  severe weakness
```

## A — optimistic precommit disclosure

Persist `runtime.disclosure` as confirmed before the final host output.

| Criterion | Result |
|---|---|
| false-positive safety | -- |
| crash after precommit | -- |
| ordinary ChatGPT feasibility | + |
| latency | - if each reveal forces write |
| conceptual simplicity | + superficially |

**Research disposition: reject as current-authority baseline.**

Prepared intent is not confirmed effect.

## B — strict post-final host callback

Host emits normal final response, then runtime receives callback/ACK and persists message/disclosure.

| Criterion | Result |
|---|---|
| semantic cleanliness | +++ |
| false-positive safety | +++ |
| duplicate control with host ID | +++ |
| ordinary ChatGPT documented feasibility | -- / open |
| custom/API host feasibility | +++ |

**Research disposition: ideal capability profile, not yet ordinary-ChatGPT baseline.**

## C — durable prepared delivery + later reconciliation

Persist exact payload/recipient/disclosure intent before emission, then later confirm/reject/resolve.

| Criterion | Result |
|---|---|
| recovery fidelity | +++ |
| false-positive safety if prepared != disclosed | +++ |
| no-background baseline | + with later interaction reconciliation |
| write frequency | - |
| latency | - |
| state-machine complexity | - |
| need proven relay/confirmation | - |

This solves “what might have been sent?” but not “was it sent?” by itself.

**Research disposition: reserve for stronger guarantee or narrow high-value cases; challenge whether baseline needs it.**

## D — later host-history confirmation

At a later invocation, use exact prior host message identity/content/status to confirm the earlier output.

| Criterion | Result |
|---|---|
| false-positive safety | +++ if host evidence is exact/trusted |
| ordinary UX | +++ |
| extra pre-send write | none |
| branch/retry handling | + if stable host identity exists |
| documented ordinary ChatGPT core interface | -- / open |
| naive “next user turn” variant | -- because partial stop exists |

**Research disposition: excellent if Step 6 exposes a trustworthy exact host evidence adapter; naive text/context inference is insufficient.**

## E — capability-tiered HostDeliveryPort

Keep semantic states host-independent; richer hosts supply direct ACK/IDs, ordinary ChatGPT uses only evidence it can actually provide.

| Criterion | Result |
|---|---|
| semantic portability | +++ |
| ordinary ChatGPT honesty | +++ |
| custom host quality | +++ |
| abstraction risk | - if made too generic |
| implementation burden | + / - |

**Research disposition: strong supporting architecture, but must not hide an unusable baseline.**

## F — remove durable disclosure entirely

Rely on host context/current messages.

| Criterion | Result |
|---|---|
| Step-4 consistency | -- |
| new-chat recovery | -- |
| spoiler/context correctness | -- |
| simplicity | ++ |

**Research disposition: reject; no evidence justifies reopening Step 4.**

## G — interleaved visible emission unit + continued tool execution

Emit player-visible text before turn completion, continue deterministic/tool work, then persist disclosure.

| Criterion | Result |
|---|---|
| post-emission write opportunity | +++ in observed harness |
| false-positive safety | ++/+++ depending host admission guarantee |
| pre-send write | potentially none |
| crash window | smaller but nonzero |
| ordinary final-message UX | - / unknown |
| portable documented ChatGPT capability | open |
| segmented/partial disclosure control | potentially +++ |

**Research disposition: important Step-6 feasibility candidate, not safe to assume as Step-5 baseline yet.**

---

# 10. Preliminary architecture hypothesis H-A — confirmation-only disclosure

The leading semantic hypothesis is:

```text
NarrationResult
    -> validated disclosure refs
    -> host delivery attempt
        -> delivery evidence outcome
            CONFIRMED_EMITTED
            CONFIRMED_NOT_EMITTED
            INDETERMINATE

ONLY CONFIRMED_EMITTED
    -> outbound runtime.message established
    -> runtime.disclosure may advance
    -> Story Transcript candidate admitted
```

Important:

- `CONFIRMED_NOT_EMITTED` and `INDETERMINATE` are not disclosure states;
- they belong to delivery evidence/operational attempt semantics;
- `runtime.disclosure` remains a positive sparse authority for confirmed exposure.

This keeps Step 4 clean and avoids infecting every disclosure query with three-valued logic.

Challenge still required:

- does ambiguity require its own durable native owner?
- when can it remain volatile and simply degrade to false-negative after crash?

---

# 11. Preliminary architecture hypothesis H-B — safe under-confirmation is a lawful crash fallback

Suppose:

```text
player actually saw X
but no confirmed disclosure became durable
```

After cold recovery:

```text
runtime.disclosure does not prove X was seen
```

The engine therefore must not assume exposure.

Safe consequences:

- hide/restrict material whose display depends on prior confirmed exposure;
- re-disclose X to the same authenticated player when necessary;
- answer using current campaign semantics if the player explicitly asks about X;
- never infer PC knowledge from player exposure.

This may cause repetition but does not corrupt world truth or leak a secret to a different player when recipient binding is respected.

This is analogous Step-5 unexpected-loss semantics: unpublished presentation/meta state may be lost, but recovery never invents a newer state.

**Preliminary recommendation:** prefer false-negative/under-confirmation over false-positive disclosure.

Potential owner decision only if the owner considers rare repeated material after crashes unacceptable enough to justify mandatory pre-send durable delivery preparation.

---

# 12. Preliminary architecture hypothesis H-C — no mandatory pre-send write for ordinary or material disclosure unless stronger promise is required

A pre-send durable `DeliveryIntent` improves exact recovery of an ambiguous final response, but it adds:

- campaign write latency before reveal;
- additional repository contention;
- new independently active operational state;
- recovery routing/lifecycle;
- cleanup obligations;
- still no proof the host actually emitted the output.

Under the confirmation-only + safe-under-confirmation model, its main benefit is presentation fidelity, not gameplay correctness:

- if lost exposure is forgotten, same-player material can be repeated;
- semantic truth/PC knowledge already lives elsewhere;
- S does not promise universal verbatim transcript.

Therefore baseline may not need a durable outbox/prepared-delivery owner at all.

Challenge required against:

- OOC objective-status reveals with no PC-knowledge transition;
- very large/expensive reveal payloads where re-generation is undesirable;
- controlled handoff after confirmed-but-unpublished exposure;
- cross-session use of one player's disclosure before that player's next turn.

---

# 13. Preliminary architecture hypothesis H-D — confirmed disclosure may be SOFT before ordinary durability boundary

Once qualifying host evidence exists in a live runtime, `runtime.disclosure` can become an established dirty semantic owner state.

Step-5.5 then determines durability:

```text
ESTABLISHED + VOLATILE_DIRTY + MAY_DEFER
    = ordinary SOFT candidate
```

unless a concrete edge proves stronger durability is necessary.

Unexpected crash may lose that unpersisted confirmation and recover to under-confirmed state.

Controlled handoff/save must include dirty confirmed disclosure when it is part of the promised continuation closure.

This avoids a campaign commit merely because one material sentence was displayed.

Challenge required against future secrecy/context consumers in another concurrent session.

---

# 14. Preliminary architecture hypothesis H-E — delivery evidence should not become a second disclosure authority

If a delivery record exists, it should answer:

```text
what exact payload/recipient occurrence did host evidence establish?
```

`runtime.disclosure` still answers:

```text
what material fact/aspect is currently known to have been exposed to player P?
```

Thus delivery/message evidence is historical/provenance support for disclosure transitions, not a parallel current query surface.

Current exposure queries do not scan historical delivery attempts.

---

# 15. Retry/regeneration findings

Retry is not equivalent to network retry.

The user deliberately asks ChatGPT to generate another assistant response from an earlier conversational point.

A safe semantic model must treat this as a **presentation regeneration invocation**, not permission to rerun the underlying player action.

Required invariant:

```text
accepted gameplay result exists
    -> regenerate/retry presentation from stored/current-authoritative result
    -> NO command replay
    -> NO reroll
    -> NO duplicate canonical transition
```

If variant A and variant B are both actually emitted and expose different facts:

```text
human exposure = monotonic union of confirmed A and confirmed B disclosures
```

Replacing the visible branch item does not make the human unsee variant A.

Physical detection of Retry versus new Interaction remains a Step-6 host identity feasibility requirement.

If the host cannot expose sufficient identity, every tool-capable invocation from old context must still run the normal current-campaign/idempotency fence before side effects.

---

# 16. Branch findings

Campaign disclosure is player-global within the campaign, not branch-local.

If player P confirmed saw X in original chat and then branches from before X:

```text
runtime.disclosure(P,X) remains true
```

Branch creation does not unsee information.

A branch may have older visible world history, but new gameplay must rehydrate/reconcile current campaign authority before any accepted mutation.

If X was only actually seen but never durably confirmed before branch/new-chat loss, under-confirmation may cause X to be repeated. This is acceptable fallback under the leading hypothesis.

---

# 17. Partial/streaming delivery findings

Because ChatGPT supports Stop generating and Voice supports interruption, one long output cannot safely be treated as an indivisible delivered payload merely because the host accepted the turn.

Three possible solutions exist:

1. host provides completed-message identity/status after full output;
2. delivery is divided into host-acknowledged semantic segments;
3. no exact completion proof => final disclosure remains unconfirmed.

A naive rule:

```text
next user input => previous full output delivered
```

is rejected.

If future host adapter exposes exact completed assistant item on next invocation, option 1 is preferred.

If the current interleaved commentary/tool capability proves portable, option 2 may allow immediate segment confirmation for material reveals.

---

# 18. Multiplayer findings

Delivery outcome is at least recipient-scoped.

Conceptually:

```text
logical response payload R
    recipient P1 -> CONFIRMED_EMITTED
    recipient P2 -> CONFIRMED_NOT_EMITTED
    recipient P3 -> INDETERMINATE
```

Only P1's `runtime.disclosure` advances.

The same world event/PC perception may already be canonical for P2's character; if human delivery to P2 failed, later output communicates the existing PC knowledge without replaying the event.

A physical host that atomically publishes one shared room message may supply one host occurrence with several intended recipients, but human disclosure still remains separate per player as required by Step 4.

No technical host message order becomes fictional chronology.

---

# 19. Story / Transcript findings

Step 5.11 Selective Exact remains compatible with confirmation-only delivery.

Only:

```text
CONFIRMED_EMITTED outbound communication
```

may enter the normal outbound Transcript source domain.

Prepared/validated/attempted/unconfirmed prose cannot become “what the player was told” merely because Chronicler can see it.

If a final response was actually visible but confirmation was lost, Story may omit it after cold loss. Under S this is acceptable historical-fidelity loss; it does not change canon.

A richer host profile can retain more exact confirmed outbound history without changing baseline authority semantics.

---

# 20. Performance implications

A healthy baseline should target:

```text
ordinary narration with no material disclosure
    -> zero new Step-5.12 repository writes

confirmed material disclosure
    -> dirty sparse runtime.disclosure/message evidence
    -> publish under ordinary Step-5.5 boundary unless stronger edge proven

host profile with direct immediate ACK
    -> qualification in same turn

host profile with deferred exact evidence
    -> qualification when bounded evidence becomes available
```

Do not scan chat history or campaign history to reconcile one delivery.

Any durable ambiguous-delivery owner must be boundedly reachable by player/session/interaction identity, not by campaign-wide search.

---

# 21. Primary open questions entering analytical challenge

1. Is safe under-confirmation after unexpected crash sufficient to satisfy Step-4 product semantics, or does “campaign-durable disclosure authority” imply a stronger no-lost-confirmation guarantee?
2. Does any concrete ordinary gameplay scenario require another concurrent session to rely on player P's just-emitted disclosure before P's next interaction/persistence boundary?
3. Is a durable pre-send delivery intent ever correctness-required, or only quality/audit enhancement?
4. If a pre-send intent is introduced, does its independent lifetime justify a new native owner, or can it remain bounded response state under an existing Interaction?
5. Is `INDETERMINATE` delivery evidence worth persisting when the safe fallback is simply “do not mark disclosed”?
6. What exact host evidence is sufficient to qualify `CONFIRMED_EMITTED` in ordinary ChatGPT?
7. Can current interleaved visible commentary + subsequent tools provide a portable enough same-turn post-emission boundary, or only an optional Step-6 profile?
8. How should completed-vs-partial streaming output bind disclosure refs if no message completion status is exposed?
9. How should old-response Retry be represented so presentation can regenerate without command replay?
10. Does controlled handoff require materializing all confirmed-but-dirty disclosure before `RECOVERY_SAFE_HANDOFF`? Preliminary answer: yes when future context correctness depends.
11. Can outbound message evidence become established later than the human exposure occurrence? Preliminary answer: yes; occurrence time and engine confirmation time are distinct.
12. What exactly is the baseline delivery guarantee: confirmed-at-most-once authority, at-least-once re-disclosure after uncertainty, or another hybrid wording?

---

# 22. Preliminary recommendation before challenge

The current strongest candidate direction is:

> **CONFIRMATION-ONLY DISCLOSURE / HOST-EVIDENCE-TYPED DELIVERY / SAFE UNDER-CONFIRMATION / NO BASELINE OUTBOX / RECIPIENT-SCOPED OCCURRENCES**

with a narrow host capability interface that may support:

```text
IMMEDIATE CONFIRMED EMISSION
DEFERRED CONFIRMATION FROM TRUSTED HOST ITEM
CONFIRMED FAILURE
INDETERMINATE / NO SUFFICIENT EVIDENCE
```

and with these preliminary laws:

1. never precommit `runtime.disclosure` as delivered;
2. only confirmed host-visible occurrence establishes outbound `runtime.message` and advances disclosure;
3. ambiguous/unproven delivery does not become three-valued current disclosure;
4. unexpected loss of unpersisted confirmation degrades to under-confirmation, not invented exposure;
5. same-player re-disclosure is the safe repair for under-confirmation;
6. ordinary narration creates no Step-5.12 write edge;
7. a pre-send durable delivery owner is rejected unless analytical challenge finds a concrete correctness consumer;
8. Retry/regeneration is presentation replay only, never gameplay replay;
9. per-recipient results remain independent;
10. stronger host delivery IDs/callbacks improve confirmation latency/fidelity but do not change the semantic model.

Confidence before analytical challenge: **MEDIUM**.

The largest uncertainty is not distributed-systems theory; it is the exact ordinary-ChatGPT host evidence that Step 6 can expose deterministically to runtime/core.

---

# 23. Sources / evidence notes

Repository sources reviewed include:

- `AGENTS.md`
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/PROJECT_MAP.md`
- Step-3 canonical execution spec
- Step-4 truth/knowledge/disclosure/Story canonical spec
- Steps 5.2, 5.4, 5.6, 5.7, 5.8 context as relevant
- Step-5.11 canonical retention spec
- `GAME/CORE/RUNTIME.md`
- `GAME/CORE/PERSISTENCE.md`
- `GAME/CORE/SESSION.md`
- `GAME/CORE/NARRATIVE.md`
- `GAME/CORE/MULTIPLAYER.md`
- `GAME/CORE/LIVE_SCENE.md`
- `GAME/SCHEMA/session.schema.yaml`
- `GAME/SCHEMA/live_scene.schema.yaml`
- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/identifier-policies.json`
- `DEV/SCHEMAS/` inventory
- `DEV/TESTS/` inventory.

External primary/authoritative sources reviewed include:

- OpenAI Help Center — current ChatGPT Edit/Retry/Branch documentation;
- OpenAI Help Center — Chat and File Retention Policies;
- OpenAI Help Center — Projects in ChatGPT;
- OpenAI Help Center — Memory FAQ / chat-history memory;
- OpenAI Help Center — Troubleshooting ChatGPT Error Messages (`Stop generating`);
- OpenAI Help Center — ChatGPT Voice interruption behavior;
- OpenAI Developers — Responses API reference (`response.completed`, response/output-item IDs, Conversations);
- AWS Prescriptive Guidance — Transactional Outbox Pattern;
- Microsoft Learn — Transactional Outbox design pattern/sample;
- Stripe API — Idempotent Requests and error handling.

No external source is treated as HDM authority; these sources constrain host/deployment assumptions and inform failure-model analysis only.
