# Step 5.12 — Host Delivery / Disclosure Boundary — Adversarial Review Addendum v2

Status: **ADVERSARIAL ADDENDUM — SIMPLIFIED CANDIDATE SURVIVES WITH TIGHTENING / STEP-6 FEASIBILITY CARRY-FORWARD**

Date: 2026-08-21

Reviewed:

- `2026-08-21-step-5-12-host-delivery-disclosure-boundary-candidate-spec-v2.md`
- `2026-08-21-step-5-12-minimal-host-delivery-owner-scope-decision.md`

The owner deliberately rejects a heavyweight baseline delivery-reliability subsystem. This addendum attacks whether the simplified architecture remains coherent with Steps 3–5.11 and whether the accepted presentation-risk boundary has accidentally weakened gameplay correctness.

Result:

> **The simplified direction survives. No new owner decision is required. One important physical feasibility obligation remains for Step 6: the selected host/role topology must provide an equivalent safe pre-player-visible validation/staging boundary for material output, or Step 6 must explicitly revisit that physical realization.**

---

# 1. What the owner decision intentionally removes

The following are no longer candidate baseline mechanisms and SHALL NOT reappear through resolution wording:

```text
durable delivery outbox
HostDeliveryEvidence tri-state state machine
post-render acknowledgement requirement
delayed-confirmation ledger
per-token / per-prefix exposure accounting
autonomous resend worker
background delivery reconciliation
mandatory pre-send campaign publication
automatic host Retry/edit/branch repair
```

A future richer host may optionally improve evidence, but this is not Step-5.12 baseline debt.

---

# 2. A1 — physical streaming can occur before a whole response is frozen

**Severity: STEP-6 PHYSICAL FEASIBILITY BLOCKER, NOT STEP-5 SEMANTIC BLOCKER**

Candidate v2 describes:

```text
NarrationResult
-> validate
-> freeze full player-visible response
-> EMISSION_COMMIT
-> host streams/renders
```

But ordinary chat products may stream assistant output incrementally. If the same physical model invocation directly generates player-visible tokens, there may be no external deterministic core opportunity to inspect the complete prose after generation but before the first visible token.

This matters independently of interruption: Step 4 requires material disclosure refs/eligibility to be validated before emission.

## Resolution A1

Preserve the **logical** pre-player-visible validation requirement.

Do not solve it in Step 5 with buffering/outbox machinery.

Step 6 SHALL prove that the chosen physical role/host topology provides one of:

1. a staged Narrator result available to deterministic validation before outer player-visible emission;
2. an equivalent host mechanism that keeps material output non-player-visible until validation passes; or
3. another physical arrangement that satisfies the same Step-4/5.12 information-boundary semantics.

If no supported deployment can provide such a boundary, Step 6 must explicitly reopen physical realization rather than silently stream unvalidated secret-bearing prose.

This is already within Step-6 ownership of role-call topology, context isolation and host capability profiles.

**Disposition: semantics sound; explicit Step-6 carry-forward required.**

---

# 3. A2 — interruption can create false-positive disclosure after `EMISSION_COMMIT`

**Severity: OWNER-ACCEPTED PRODUCT LIMITATION**

Attack:

```text
response committed
runtime.disclosure advances HOT
player presses Stop after first line
important reveal was later in response
```

The runtime may now believe the reveal was emitted although the player missed it.

Candidate v1 tried to avoid this with confirmation-only delivery. Owner explicitly rejected the complexity required for robust support.

## Resolution A2

Keep the limitation explicit and narrow:

- normal uninterrupted Master output is the supported baseline;
- interruption after emission commit may produce over-confirmed disclosure/message history;
- no prefix ledger is created;
- player help/manual warns that interruption risks missing important information;
- gameplay obligations remain independently owned so missed presentation cannot delete a pending Choice/Procedure/etc.;
- when the player indicates confusion/missing context, ordinary current-eligible re-explanation is allowed.

Do not describe `runtime.disclosure` as a cryptographic/read receipt. It is the engine's exposure authority under the supported host-use contract.

**Disposition: accepted.**

---

# 4. A3 — outbound exact history after interrupted output can overstate what was seen

**Severity: REQUIRED SEMANTIC CLARIFICATION**

Step 5.11 defines outbound `runtime.message` as communication evidence after Step-5.12 qualification.

Under v2 an interrupted response may still leave the full emission-committed payload as the outbound message.

## Resolution A3

Clarify exactness:

> For baseline outbound delivery, `runtime.message.exact_text` is exact relative to the **emission-committed HDM response representation**, not proof that every character was visually rendered or read after an unsupported interruption.

This mirrors Step-5.11 voice exactness: exactness is always relative to the accepted HDM representation contract, not an undocumented physical channel beyond that contract.

A future richer host may tighten the evidence standard.

**Disposition: resolved.**

---

# 5. A4 — losing disclosure durability after a successful response

**Severity: EXPECTED STEP-5.5 RPO, NOT BLOCKER**

Scenario:

```text
normal response fully shown
OutboundEmissionClosure is SOFT in HOT state
host/chat crashes before later campaign publication
```

Cold recovery lacks durable disclosure evidence.

This may cause future repetition of information.

## Resolution A4

This is lawful under Step 5.5:

- disclosure/message evidence is normally SOFT;
- crash recovers actual durable sources only;
- absence after crash does not replay gameplay mechanics or fictional events;
- current Narrator may explain/restate currently eligible information when needed;
- explicit save/handoff may include dirty disclosure state according to existing scope policy.

No per-response HARD write is justified merely to eliminate this RPO.

**Disposition: pass.**

---

# 6. A5 — disclosure can accidentally become the only owner of “player must know X”

**Severity: BLOCKER IF ALLOWED; V2 ALREADY RESOLVES**

A pending choice, mandatory prompt, required clarification or other gameplay obligation cannot disappear merely because its presentation was missed.

Candidate v2 LAW 5.12-V2-5 correctly requires native ownership.

Resolution gate must preserve it as a primary law, not an example-only note.

**Disposition: pass.**

---

# 7. A6 — normal pipeline persists gameplay before narration

**Severity: REQUIRED FLOW CLARIFICATION**

Current runtime pipeline is:

```text
STATE -> INTENT -> RULES -> RANDOMNESS -> CONSEQUENCES -> PERSISTENCE -> NARRATION
```

The simplified disclosure closure is established at final player-visible emission, therefore commonly **after** any gameplay publication already required for that turn.

This is correct and should not cause a second publication.

## Resolution A6

State explicitly:

```text
required gameplay publication (if any)
    -> validated narration staging
    -> EMISSION_COMMIT
    -> outbound/disclosure becomes new HOT/SOFT metadata
    -> ordinary later durability boundary may publish it
```

Do not reopen the just-completed campaign transaction solely to append disclosure.

If an independent existing HARD edge later requires the disclosure metadata itself durable before some later operation, normal Step-5.5 closure applies.

**Disposition: resolved; reinforces no extra Git call.**

---

# 8. A7 — normal singleplayer SOFT gameplay itself may be lost after player saw narration

**Severity: EXISTING STEP-5 RPO, NOT NEW DELIVERY DEFECT**

A player may see narration of established SOFT gameplay that has not yet reached a durability boundary. If total host loss destroys that HOT/SOFT state, cold recovery returns to earlier durable canon.

Step 5.12 does not solve or worsen this by adding a delivery transaction.

The engine must not reconstruct lost canon merely because the user remembers the visible narration.

This remains the Step-5.2/5.5 lost-HOT contract.

**Disposition: pass.**

---

# 9. A8 — Retry/regeneration can create a second visible variant without HDM bookkeeping

**Severity: OWNER-ACCEPTED UNSUPPORTED HOST-HISTORY BEHAVIOR + STEP-6 FEASIBILITY**

Host Retry may cause another assistant generation from an older conversational point. If the platform bypasses current campaign synchronization/normal runtime guards, that action could produce prose inconsistent with current campaign authority.

The owner does not want a full Retry reconciliation subsystem.

## Resolution A8

Baseline contract:

- host Retry/regeneration is not a supported campaign correction/rewind path;
- help/manual recommends a new message instead;
- accepted gameplay is never replayed because of Retry;
- if the deployment exposes reliable Retry ancestry, Step 6 may cheaply detect/fence/reframe it;
- if it cannot, that limitation belongs to the deployment capability profile and is not “fixed” with Step-5 delivery storage machinery.

All player-visible generation must still respect role/context eligibility as far as the selected physical topology can enforce it.

**Disposition: accepted/deferred physical.**

---

# 10. A9 — auxiliary visible surfaces can leak secrets

**Severity: BLOCKER IF USED FOR GAMEPLAY CONTENT; V2 NARROWS THE SURFACE**

Owner simplification correctly avoids generic surface accounting by defining the validated Master response as the baseline intentional gameplay-delivery surface.

Resolution must preserve two rules:

1. private/tool/progress/debug surfaces SHALL NOT intentionally carry Narrator-ineligible campaign secrets;
2. Step 6 must inventory which physical surfaces the chosen host actually renders to the user.

If a future deployment intentionally uses another surface for gameplay information, it becomes a formal delivery surface and must obey the same information eligibility.

No generic widget/card disclosure ledger is required now.

**Disposition: pass with Step-6 inventory.**

---

# 11. A10 — multiplayer audience ambiguity

**Severity: REQUIRED HOST-PROFILE BOUNDARY**

Step 4 disclosure is keyed to a human player. Ordinary HDM multiplayer currently assumes independent player sessions/chats.

A single physical host surface shared by multiple humans would require trustworthy audience semantics not designed here.

## Resolution A10

Baseline 5.12 supports delivery where runtime can resolve the intended authenticated/bound player recipient scope.

A shared multi-human host conversation/channel requires a Step-6 host capability profile before it can claim precise per-player disclosure.

Do not invent per-person “read” tracking inside a shared UI.

**Disposition: resolved/deferred physical.**

---

# 12. A11 — live-state legacy “knowledge/disclosure” wording can become duplicate authority

**Severity: MACHINE-REALIZATION BLOCKER, SEMANTICALLY RESOLVED**

Legacy live runtime prose permits per-PC knowledge/disclosure information. Step 4 and v2 distinguish:

```text
fictional PC perception/knowledge
!=
human player disclosure
```

## Resolution A11

During eventual machine realization:

- live state may retain compact source-local fictional perception/knowledge evidence required by live ownership;
- it must not become a second campaign-wide writable `runtime.disclosure` authority;
- human exposure from each player's host response is established under Step 5.12 and later durably reconciled through the proper campaign owner/routing.

**Disposition: implementation debt.**

---

# 13. A12 — concurrent outbound identity and disclosure merge

**Severity: REQUIRED; V2 PRESERVES PRIOR REVIEW RESULTS**

The owner simplification does not remove concurrency requirements.

Retain:

- Step-5.8-compatible collision-safe source-native outbound message identity;
- no campaign-global pre-response ID reservation write;
- semantic disclosure merge under fact/truth-transition lineage rather than host/Git order.

These cost no extra ordinary delivery transaction and are necessary for correctness.

**Disposition: pass.**

---

# 14. A13 — presentation repair must not replay fiction

**Severity: REQUIRED; V2 PRESERVES PRIOR REVIEW RESULT**

If a player says “я не увидел / повтори”, the Master may re-present information from current eligible evidence.

It must not create a second NPC utterance or rerun the gameplay event solely to compensate for host presentation.

Step-5.11 exact/semantic distinction controls whether prior words may be quoted exactly.

**Disposition: pass.**

---

# 15. Simplified architecture quality check

Compared with candidate v1, v2 removes correctness machinery whose benefit is only stronger presentation-delivery fidelity:

| Concern | v1 | v2 |
|---|---|---|
| post-render ACK | semantic requirement | not baseline |
| delivery tri-state | explicit | removed baseline |
| delayed confirmation | supported | not baseline |
| durable outbox | rejected but analyzed | explicitly non-goal |
| partial stream | under-confirm | documented unsupported edge |
| normal-turn Git write | none | none |
| player-visible gameplay obligation | native owner | native owner |
| disclosure metadata validation | required | required |
| multiplayer recipient scope | required | required |
| message/disclosure semantic closure | required | required |
| gameplay replay on Retry/failure | forbidden | forbidden |

The simplification therefore removes state/control-flow complexity without removing semantic-owner protections.

---

# 16. Strongest counterargument

The strongest counterargument is that false-positive disclosure can be worse than duplicate information: an interrupted response might hide a key clue while `runtime.disclosure` says the player saw it, and future Narrator policy could avoid repeating it.

This is real.

Why v2 still survives:

1. the owner explicitly accepts this presentation risk to avoid heavy delivery reliability machinery;
2. the risk is concentrated on abnormal/actively interrupted host behavior, which documentation can discourage;
3. core gameplay obligations never depend solely on disclosure;
4. disclosure is sparse and used when future secrecy/context correctness matters, not as a rule that information may never be repeated;
5. a player can naturally ask for repetition/clarification;
6. stronger delivery evidence remains an optional future host-profile optimization if the platform later exposes it cheaply.

What would change the recommendation:

- if playtesting shows users commonly interrupt streaming responses unintentionally;
- if critical clue loss from false-positive disclosure materially harms campaigns;
- if ordinary ChatGPT exposes a cheap reliable completed-message acknowledgement usable without extra latency/writes;
- if multiplayer delivery requires precise per-recipient proof for a supported shared-host mode.

---

# 17. Review disposition

**Candidate v2 is ready for resolution gate** provided the gate incorporates:

1. owner-approved documented interruption/Retry/edit risk;
2. `EMISSION_COMMIT` as baseline supported-normal-flow evidence boundary;
3. native ownership of gameplay-significant communication obligations;
4. coherent `OutboundEmissionClosure`;
5. SOFT-by-default durability with no second per-turn publication;
6. pre-emission disclosure completeness validation;
7. baseline validated Master-response delivery surface only;
8. Step-5.11 exactness refinement for emission-committed outbound content;
9. live/concurrent identity and semantic merge rules;
10. explicit Step-6 feasibility requirement for a safe pre-player-visible staging/validation boundary and host Retry/surface identity.

No new human decision remains.