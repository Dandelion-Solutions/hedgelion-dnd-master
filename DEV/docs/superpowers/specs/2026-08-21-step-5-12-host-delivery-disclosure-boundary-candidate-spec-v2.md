# Step 5.12 — Host Delivery / Disclosure Boundary — Candidate Specification v2

Status: **CANDIDATE V2 — OWNER-SIMPLIFIED; REQUIRES ADVERSARIAL ADDENDUM**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Supersedes for further Step-5.12 review:

- `2026-08-21-step-5-12-host-delivery-disclosure-boundary-candidate-spec.md`

Owner scope decision:

- `2026-08-21-step-5-12-minimal-host-delivery-owner-scope-decision.md`

Canonical prerequisites remain Steps 3, 4 and 5.1–5.11.

Candidate direction:

> **VALIDATED EMISSION-COMMIT / SOFT OUTBOUND DISCLOSURE CLOSURE / NO BASELINE DELIVERY-ACK SUBSYSTEM / DOCUMENTED INTERRUPTION RISK / RECIPIENT-SCOPED DISCLOSURE**

This candidate deliberately trades perfect host-delivery reconstruction for a substantially simpler ordinary-turn path. It does not define final physical host identity/API support, generic GC, or Step-6 orchestration.

---

# 1. Supported baseline product contract

HDM baseline supports **normal uninterrupted Master responses**.

A player may technically interrupt output, use host Retry/regeneration, edit old host messages or branch old host history because the ChatGPT product permits such actions, but those are not campaign rewind or reliable delivery-repair mechanisms.

Player documentation shall discourage interruption during active Master output and advise using a new message for correction/clarification.

The accepted risk is presentation-level:

- a player may miss part of an interrupted response;
- abnormal host behavior may cause repeated or missing presentation information;
- HDM does not promise exact reconstruction of which prefix was visible.

This acceptance does **not** weaken canonical gameplay/execution ownership.

---

# 2. Authority geometry

```text
GAMEPLAY / SEMANTIC AUTHORITY

world/current owners
world.knowledge
Step-3 execution owners
SemanticEvent / LOG
runtime.disclosure
runtime.message


PRESENTATION PATH

resolved current state
    -> NarrationResult
    -> deterministic validation
    -> frozen player-visible Master response
    -> EMISSION_COMMIT
    -> host response path
```

No durable delivery outbox, delivery queue, worker, segment ledger or post-render acknowledgement state is baseline authority.

---

# 3. Baseline delivery boundary

## 3.1 `EMISSION_COMMIT`

`EMISSION_COMMIT` is the baseline semantic boundary at which:

1. the final player-visible Master response content has been frozen;
2. all material disclosure refs for that content have been validated;
3. intended recipient/player eligibility for that response has been validated;
4. the runtime commits that frozen response to the player-facing host output path and no longer treats it as a private/unemitted draft.

Conceptually:

```text
NarrationResult generated
    -> validate content + disclosure refs + recipient
    -> freeze final delivery content
    -> EMISSION_COMMIT
    -> host renders/streams response
```

The baseline does not require a later post-render callback.

## 3.2 Supported-normal-flow assumption

For the supported ordinary flow, an `EMISSION_COMMIT` is the point HDM treats the communication as emitted for `runtime.message` / `runtime.disclosure` semantics.

The product explicitly accepts that user interruption or unusual host failure after this boundary may make actual visible content incomplete. Such a case is a documented presentation limitation, not a trigger for a mandatory reconstruction subsystem.

A richer future host may strengthen this boundary with trustworthy acknowledgement without changing semantic owners.

---

# 4. Outbound semantic closure

At one `EMISSION_COMMIT`, deterministic core establishes one logical **OutboundEmissionClosure** for the affected delivery unit/recipient scope:

```text
outbound runtime.message evidence
+
runtime.disclosure transitions implied by validated disclosure refs
+
required provenance / stable refs / bounded indexes
```

The closure is established coherently in current HOT state.

This is not a repository transaction with the host. It is the HDM-side semantic result of committing the validated response to the host-visible path.

## LAW 5.12-V2-1 — MESSAGE AND DISCLOSURE DO NOT SPLIT SEMANTICALLY

If an outbound message occurrence is established as an HDM delivery occurrence, all material disclosure transitions validated for that occurrence and recipient scope are established in the same logical closure.

A later durability boundary publishes the dirty members coherently under Step 5.5/5.6.

---

# 5. `runtime.disclosure` semantics under the baseline host contract

`runtime.disclosure` remains sparse human-player exposure authority from Step 4.

For baseline ordinary ChatGPT, its host evidence standard is the supported `EMISSION_COMMIT` contract rather than a perfect proof of literal human reading or full post-render completion.

## LAW 5.12-V2-2 — DISCLOSURE ADVANCES ONLY AFTER VALIDATED EMISSION COMMIT

Generation alone is insufficient.

Validation alone is insufficient.

A private draft is insufficient.

Only the final frozen player-facing response crossing `EMISSION_COMMIT` may establish the corresponding disclosure transitions.

## LAW 5.12-V2-3 — DISCLOSURE DOES NOT CLAIM LITERAL READING

As in Step 4, HDM does not claim that the human literally read/comprehended a response merely because the output was emitted/committed to the player-facing host path.

## LAW 5.12-V2-4 — INTERRUPTION AFTER EMISSION COMMIT IS AN ACCEPTED PRESENTATION-RISK EXCEPTION

Baseline HDM does not reconstruct which exact response prefix rendered after a player interrupt or abnormal host cutoff.

The resulting discrepancy may cause the engine to believe a material disclosure was emitted when the player missed it.

This risk is owner-approved and must be documented to players; it SHALL NOT be “fixed” by adding baseline token/chunk ledgers, delivery outboxes or background retry infrastructure.

---

# 6. Gameplay obligations remain independent of delivery

## LAW 5.12-V2-5 — DELIVERY NEVER SOLE-OWNS A GAMEPLAY-SIGNIFICANT OBLIGATION

Anything that must survive until the player can act/respond remains owned by its proper gameplay/runtime owner independently of outbound delivery.

Examples:

```text
pending Choice                 -> Procedure / Continuation / Interaction owner
mandatory clarification        -> accepted Interaction/IntentPlan owner as applicable
PC fictional knowledge         -> world.knowledge
mechanical deadline/warning     -> owning process/procedure/policy
canonical NPC utterance/event   -> SemanticEvent / natural owner
```

If presentation fails or is interrupted, the underlying requirement remains recoverable and can be re-presented when needed.

Delivery bookkeeping is not a pending-work authority.

---

# 7. Durability semantics

An `OutboundEmissionClosure` is normally **ESTABLISHED + VOLATILE_DIRTY + MAY_DEFER** after emission commit unless another existing semantic edge makes it mandatory.

Therefore it is normally SOFT under Step 5.5.

No per-response repository write is created merely because the Master spoke.

## LAW 5.12-V2-6 — EMISSION DOES NOT CREATE A GENERIC HARD SAVE EDGE

Ordinary disclosure/message evidence may batch with later campaign persistence.

It joins a HARD/SAVE/handoff closure only when existing Step-5 policies require that affected scope to become durable.

## LAW 5.12-V2-7 — CRASH MAY LOSE UNSAVED DISCLOSURE MEMORY

If confirmed/established outbound disclosure exists only in destroyed volatile state, cold recovery returns to actual durable campaign evidence.

The engine may then conservatively repeat eligible information later.

It SHALL NOT replay mechanics or fabricate a second fictional event merely because meta-level disclosure memory was lost.

This is ordinary Step-5.5 RPO behavior, not a delivery journal requirement.

---

# 8. Recipient scope and multiplayer

Each outbound closure is scoped to the actual intended human player/audience supported by the current host/session binding.

## LAW 5.12-V2-8 — ONE PLAYER'S EMISSION DOES NOT DISCLOSE TO ANOTHER

A response committed to Player A does not advance Player B's `runtime.disclosure` merely because:

- both PCs share a scene;
- the same fact exists in shared live state;
- another Master could theoretically say the same thing;
- the campaign repository is readable by both users.

Human exposure remains player-scoped.

## LAW 5.12-V2-9 — DELIVERY DOES NOT OWN FICTIONAL PERCEPTION

PC/NPC perception and fictional knowledge remain `world.knowledge`/semantic-event responsibilities.

`runtime.disclosure` records human-player exposure only.

Legacy live-state wording that mixes “knowledge/disclosure” must be realized so it does not become a second campaign-wide `runtime.disclosure` authority.

---

# 9. Disclosure-ref completeness and visible surfaces

The simplification does not permit leaks around the Narrator boundary.

## LAW 5.12-V2-10 — MATERIAL DISCLOSURE METADATA IS A PRE-EMISSION INTEGRITY REQUIREMENT

Before `EMISSION_COMMIT`, every material fact/truth-status reveal whose future exposure state matters must have valid structured disclosure metadata.

Do not rely on later NLP over emitted prose to reconstruct missing refs.

A later discovered untracked leak is an integrity/repair case; append honest repair evidence rather than rewriting history.

## LAW 5.12-V2-11 — BASELINE GAMEPLAY DELIVERY SURFACE IS THE MASTER'S VALIDATED PLAYER-FACING RESPONSE

Intentional gameplay secrets/reveals SHALL be delivered through the validated Master response path.

Tool traces, connector internals, progress text, debug output, private role reasoning and other auxiliary surfaces SHALL NOT carry Narrator-ineligible campaign secrets.

Step 6 must inventory which physical surfaces are actually player-visible for the chosen deployment.

If a future deployment intentionally admits another player-visible delivery surface for gameplay content, that surface must join the same eligibility/disclosure laws.

This avoids building generic multimodal delivery accounting into the Step-5 baseline.

---

# 10. Host interruption, Retry, edit and branch

## LAW 5.12-V2-12 — HOST INTERRUPTION IS NOT A SUPPORTED CAMPAIGN TRANSACTION

Stopping Master output does not roll back already established gameplay/canon and does not create a campaign correction event.

Baseline provides no prefix-exposure ledger or automatic “resume exactly where rendering stopped” protocol.

When important information appears missing, the player may ask the Master to repeat/clarify it through a new message.

## LAW 5.12-V2-13 — HOST RETRY/REGENERATION DOES NOT REPLAY GAMEPLAY

Retrying/regenerating an old assistant response is not permission to:

- recreate the RuntimeCommand;
- reroll;
- spend resources again;
- repeat live mutations;
- rewind campaign authority.

Where a host/deployment cannot reliably distinguish such a retry from a normal invocation, that is Step-6 host-topology/identity feasibility debt.

## LAW 5.12-V2-14 — EDITING OLD HOST HISTORY DOES NOT RETCON HDM

An old user-message edit or branch from old chat history does not rewrite accepted `runtime.message`, Interaction, canon or disclosure state.

Corrections use a new accepted Interaction under ordinary HDM rules.

Visible host-history divergence is not recovery authority.

---

# 11. Re-presentation after uncertain/missed presentation

Baseline has no automatic undelivered-secret queue.

However, if a current gameplay/presentation need independently requires communicating information again, ordinary Narrator generation may re-present it subject to current eligibility.

## LAW 5.12-V2-15 — PRESENTATION REPAIR DOES NOT CREATE NEW FICTION

If an NPC already canonically spoke, a later reminder/re-presentation is not automatically a second NPC speech act.

- if exact fictional wording remains protected, it may be quoted exactly;
- if only semantic meaning survives, summarize the prior occurrence without invented exact quotation;
- no new `world.knowledge`/fictional event is created unless a genuinely new in-fiction communication occurs.

---

# 12. Message identity and concurrency

Outbound `runtime.message` identity inherits Step 5.8/5.11 collision-safe source-native requirements.

## LAW 5.12-V2-16 — NO CAMPAIGN-GLOBAL HOT-PATH MESSAGE RESERVATION

Concurrent sessions/live scopes must be able to establish distinct outbound communication identity without requiring a campaign-global sequential ID reservation write before every response.

The legacy campaign-sequential message ID policy is machine-realization debt where incompatible with this law.

Story Transcript IDs remain Step-5.10 layer-local IDs and are not runtime-message identity.

---

# 13. Disclosure merge semantics

Repeated communication of the same fact is not a problem to “dedupe” through transport order.

`runtime.disclosure` merges under Step-4 semantic meaning:

```text
statement exposure: monotonic OR
objective-status exposure: preserve/advance by fact-owner truth-transition semantics
```

Git order, host message order, wall-clock time or lexical ID order does not define which truth transition is semantically newer.

If required transition lineage is contradictory/incomparable under its owner contract, use scoped integrity/reconciliation rather than transport order.

---

# 14. Story / Transcript integration

An outbound `runtime.message` established at `EMISSION_COMMIT` becomes eligible as a Step-5.11/5.10 Transcript source candidate according to Selective Exact policy.

Generated private/uncommitted NarrationResult drafts are not transcript history.

If an interrupted response caused the player to see only a prefix, baseline may still retain the committed full response as outbound message history under the documented interruption limitation. No partial-Transcript reconstruction is promised.

This is an explicit consequence of the owner-approved simplification.

---

# 15. Richer host capability is optional

A future host profile MAY provide stronger evidence such as:

- exact established-message identity;
- complete-render acknowledgement;
- acknowledged segment delivery;
- idempotent host-send key;
- post-emission callback.

A deployment may use such evidence to reduce presentation ambiguity.

It SHALL NOT:

- introduce a second disclosure authority;
- require Work/Pro/Enterprise/background workers for baseline HDM;
- make ordinary campaigns unreadable/unrecoverable without that capability;
- force a durable outbox unless a future explicit product decision adopts one.

The exact host capability profile and physical invocation identity remain Step 6.

---

# 16. Explicit non-goals

Step 5.12 baseline does not provide:

- exactly-once visible prose;
- human-read receipts;
- per-token/per-chunk exposure tracking;
- durable send queue/outbox;
- autonomous resend worker;
- full reconstruction of interrupted output;
- automatic repair of Retry/edit/branch history;
- host DOM/byte identity;
- generic multimodal transcript accounting;
- gameplay rewind through ChatGPT history controls.

---

# 17. Required machine-realization debt

Later integrated implementation must define at least:

1. `runtime.disclosure` machine/catalog/schema realization;
2. outbound `runtime.message` representation from Step 5.11;
3. collision-safe source-native message IDs compatible with live concurrency;
4. typed `NarrationResult` disclosure metadata realization;
5. deterministic pre-emission validation/completeness guard;
6. atomic-enough HOT `OutboundEmissionClosure` establishment;
7. Step-5.5/5.6 dirty publication integration;
8. player/session recipient binding;
9. Step-5.10/5.11 Transcript candidate routing;
10. auxiliary player-visible surface fencing;
11. Step-6 host Retry/edit/branch identity feasibility;
12. player-facing help/manual warning for interruption and host-history editing/retry limitations.

No baseline delivery outbox, worker, lease, heartbeat or partial-stream ledger is implementation debt.

---

# 18. Required regression/adversarial cases

At minimum:

1. generation fails before response freeze -> no outbound closure;
2. disclosure ref invalid -> response blocked before emission commit;
3. normal uninterrupted emission -> message + disclosure establish together;
4. emission with no material disclosure -> message only as required by retention policy;
5. interrupt after emission commit -> documented possible over-confirmation; no crash/canon corruption;
6. crash after emission before disclosure durability -> durable under-confirmation allowed; no gameplay replay;
7. pending Choice survives even if its prompt presentation is lost;
8. same fact repeated later -> no duplicate fictional event;
9. exact prior NPC wording protected -> exact re-presentation possible;
10. only semantic prior speech survives -> summary, not invented quote;
11. one multiplayer player receives secret, another does not;
12. concurrent outbound message creation -> no ID collision/global reservation requirement;
13. objective truth revision exposure merge follows truth lineage, not delivery order;
14. host Retry does not rerun mechanics/RNG;
15. edited old user message does not retcon accepted Interaction;
16. Story Transcript candidate arises only from emission-committed outbound message;
17. tool/progress/private-role content cannot leak a Narrator-ineligible secret;
18. clean ordinary turn adds no extra repository call solely for disclosure delivery.

---

# 19. Candidate exit statement

If the adversarial addendum validates this simplification, Step 5.12 may close with the following product-level invariant:

> **HDM validates and freezes player-facing Master output before committing it to the host response path, establishes recipient-scoped outbound/disclosure evidence at that emission-commit boundary, and keeps gameplay obligations independent of presentation. Baseline ordinary play does not pay for a delivery-ack/outbox subsystem; interruption and host-history rewrite features are documented presentation-risk edges rather than campaign transaction mechanisms.**
