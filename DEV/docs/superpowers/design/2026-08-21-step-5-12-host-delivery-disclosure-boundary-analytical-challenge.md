# Step 5.12 — Host Delivery / Disclosure Boundary — Analytical Challenge

Status: **ANALYTICAL CHALLENGE — PRE-CANDIDATE**

Date: 2026-08-21

Basis:

- Step-5.12 task brief;
- Step-5.12 research draft;
- canonical Steps 3, 4 and 5.1–5.11;
- current repository/runtime/catalog audit;
- current official ChatGPT/OpenAI platform research;
- authoritative distributed-systems/idempotency references.

This challenge attacks the preliminary direction:

> **CONFIRMATION-ONLY DISCLOSURE / HOST-EVIDENCE-TYPED DELIVERY / SAFE UNDER-CONFIRMATION / NO BASELINE OUTBOX / RECIPIENT-SCOPED OCCURRENCES**

The goal is to falsify or tighten it before any candidate specification.

---

# 1. Strongest counterargument

The strongest argument against the preliminary direction is:

> Step 4 calls `runtime.disclosure` campaign-durable human exposure authority. If the player sees an important secret, but a crash before durable confirmation causes HDM to forget that exposure, then the durable owner is not actually preserving the real human-history fact. A durable pre-send delivery manifest plus a robust reconciliation protocol would reduce this loss and produce better continuity, so perhaps every material reveal should force a write before emission.

This is not a strawman. Long-running D&D quality benefits from remembering what each player has already been told.

The challenge must therefore prove that safe under-confirmation is a deliberate RPO-compatible fallback rather than an accidental weakening of Step 4.

---

# 2. Attack: does Step 4 require no-loss disclosure across unexpected crash?

## Observation

Step 4 defines semantic ownership, not a unique physical durability cadence.

Step 5.5 later explicitly allows established semantic state to be:

```text
ESTABLISHED + VOLATILE_DIRTY + MAY_DEFER = SOFT
```

and explicitly states that if SOFT is lost through total host/process/context loss before publication, recovery returns to actual durable state rather than inventing the lost progress.

Therefore “campaign-durable owner” does not mean every transition has an immediate HARD publication edge.

## Counterexample test

```text
P sees secret X
runtime knows/qualifies exposure in current host
confirmed disclosure is dirty SOFT
host hard-crashes before next durability boundary
```

Recovery sees no durable X exposure.

Can it continue safely?

Yes, if all of these hold:

1. absence of disclosure never means “must omit information the player is entitled to know”;
2. disclosure is not PC knowledge;
3. current delivery eligibility is recomputed independently;
4. if the same player needs X again and current eligibility permits, X may be re-disclosed;
5. no gameplay mechanic is replayed merely to repeat presentation.

The result is duplicate/repeated presentation, not invented world state.

## Finding F1

**SAFE UNDER-CONFIRMATION IS COMPATIBLE WITH STEP-5.5 UNEXPECTED-LOSS RPO.**

A no-loss guarantee would be a stronger new durability promise, not an already inherited law.

Controlled handoff/save remain different: once a confirmed disclosure transition is established and dirty, a promised handoff/save closure must include it when future context correctness depends on it.

**Disposition: preliminary direction survives.**

---

# 3. Attack: can false-negative disclosure ever leak a secret?

A false negative means:

```text
player P saw X
campaign does not prove P saw X
```

Could later “repair” re-delivery expose X when P is no longer authorized?

It must not.

Safe repair rule is not:

```text
missing disclosure -> always repeat old secret
```

It is:

```text
missing disclosure
AND current role/player/source eligibility independently permits X
AND current task needs X
    -> X may be presented/re-presented
```

If authorization/mode/perspective changed, under-confirmation does not create permission.

Examples:

- removed player: no new gameplay delivery merely because old pending exposure was forgotten;
- spectator spoiler mode revoked: no re-delivery without current spoiler eligibility;
- PC no longer controls same character: player exposure remains player-global if confirmed, but absent exposure does not grant new fictional knowledge.

## Finding F2

**UNDER-CONFIRMATION IS SECRECY-CONSERVATIVE ONLY WHEN RE-DELIVERY RECHECKS CURRENT ELIGIBILITY.**

This must become a candidate law.

---

# 4. Attack: does another session need P's disclosure immediately?

Suppose P1 is shown X and P1's disclosure is not yet durable.

Could P2's concurrent session need that fact before P1 acts again?

Search across existing owner semantics finds no ordinary gameplay correctness consumer that should infer world/PC state from P1's human exposure.

- `world.knowledge` owns fictional subject knowledge;
- current world state owns objective mechanics;
- P2's disclosure is independent;
- another Master cannot autonomously push a new message to P1 in baseline ChatGPT;
- Commentator/spoiler retrieval for P1 occurs when serving P1 and can use current/durable evidence then;
- group decisions must be represented in world/player actions, not inferred from whether a human saw prose.

Therefore an ordinary P2 action does not require a HARD flush of P1's human exposure.

## Finding F3

**NO ORDINARY CROSS-SESSION CONSUMER JUSTIFIES A PRE-SEND HARD DISCLOSURE EDGE.**

If a future feature introduces autonomous outbound push or collective human-exposure mechanics, that feature must declare its own dependency/edge.

---

# 5. Attack: delayed confirmation loses structured disclosure refs

Research initially suggested later host-history confirmation.

Problem:

```text
host proves exact assistant message M was completed
```

is insufficient by itself to advance `runtime.disclosure` if the runtime no longer has the validated structured mapping:

```text
M -> disclosure_refs[]
```

Re-running NLP over old prose would defeat Step 4's structured-disclosure design and could invent/omit exposures.

Three ways exist:

### Option 1 — durable pre-send DeliveryIntent

Strong continuity but forces writes and operational lifecycle.

### Option 2 — host message metadata stores validated refs

Excellent if host supports it; no ordinary ChatGPT contract currently proves this capability.

### Option 3 — volatile `ValidatedDeliveryCandidate`

Deterministic core constructs during the current host lifetime:

```text
candidate-local identity
exact payload/digest
recipient(s)
disclosure_refs[]
source NarrationResult / Interaction refs
```

If candidate + matching later host evidence both survive, confirmation may occur.

If candidate is lost before confirmation, do not reconstruct refs from prose; fall back to under-confirmation.

## Finding F4

**A MATCHING VALIDATED DELIVERY CANDIDATE IS REQUIRED FOR DELAYED CONFIRMATION; ITS BASELINE LIFETIME MAY BE VOLATILE BECAUSE LOSS IS SAFE.**

This candidate is working evidence, not a new current-state authority and not automatically a durable record.

A richer host may durably/externally bind equivalent metadata.

---

# 6. Attack: why not persist the candidate anyway?

Benefits of durable prepared candidate:

- exact knowledge of what might have been sent after crash;
- possible exact retry;
- better audit;
- better Transcript fidelity.

Costs:

- write before every protected/material reveal;
- campaign ref contention;
- latency before player sees output;
- a new active lifecycle requiring routing/recovery/cleanup;
- prepared state still cannot prove emission;
- no background worker exists to guarantee completion;
- Selective Exact explicitly does not promise every final prose payload forever.

Most importantly, no current gameplay correctness property is lost when the prepared candidate disappears: recovery simply lacks proof and does not mark exposure.

## Finding F5

**DURABLE PRE-SEND DELIVERY PREPARATION IS NOT BASELINE-CORRECTNESS-REQUIRED.**

It remains an optional future quality/audit feature or a capability-profile implementation choice if measured value justifies the write.

YAGNI therefore favors no baseline persistent outbox/DeliveryIntent owner.

---

# 7. Attack: can `INDETERMINATE` simply disappear on crash?

If an in-memory attempt returns `INDETERMINATE`, retaining it could help avoid duplicate resend.

But current authority implications are:

```text
INDETERMINATE
    -> cannot confirm disclosure
```

If lost on crash, durable state is still:

```text
not confirmed disclosed
```

which is the same safe decision for current exposure queries.

Persisting indeterminate attempt state is useful only for presentation optimization/audit, not truth of `runtime.disclosure`.

Exception:

- if exact once-only external effect existed beyond human-readable presentation, the ambiguity might be correctness-critical;
- Step 5.12 scope is host-visible communication/disclosure, whose safe fallback is re-presentation to the same eligible player.

## Finding F6

**BASELINE NEED NOT DURABLY PERSIST INDETERMINATE DELIVERY ATTEMPTS.**

They may remain volatile operational evidence.

If a deployment can query/reconcile stable host item identity later, it may retain bounded attempt metadata as an optimization, without making it disclosure authority.

---

# 8. Attack: is a boolean `runtime.disclosure` still sufficient?

Could we change current disclosure into:

```text
NOT_EXPOSED
POSSIBLY_EXPOSED
CONFIRMED_EXPOSED
```

This looks attractive because delivery has uncertainty.

Problems:

1. `runtime.disclosure` Step-4 meaning is actual established exposure, not transport uncertainty;
2. `POSSIBLY_EXPOSED` would infect every Context Assembler disclosure query;
3. lack of a disclosure row already provides the conservative result needed for spoiler safety;
4. delivery uncertainty is occurrence/evidence metadata, not current relation authority;
5. on unexpected loss, possible state may disappear lawfully without changing the safe query result.

## Finding F7

**DO NOT TURN `runtime.disclosure` INTO A THREE-VALUED DELIVERY STATE.**

Keep positive sparse confirmed exposure authority. Put attempt uncertainty in delivery evidence when available.

---

# 9. Attack: next user turn as confirmation

Naive rule:

```text
new user message arrives
    -> previous assistant response was delivered
```

fails because ChatGPT permits stopping generation. Voice also allows interruption.

A user can continue after only a prefix/partial response.

Therefore a later input proves at most that some conversational state exists, not that every disclosure ref in the planned full payload was emitted.

A valid deferred confirmation must bind to stronger host evidence, e.g. equivalent of:

```text
completed assistant item identity
exact payload/content digest
recipient/channel identity
relation to matching ValidatedDeliveryCandidate
```

or to a host-acknowledged smaller segment.

## Finding F8

**NEXT-TURN CAUSALITY ALONE IS NOT SUFFICIENT DELIVERY PROOF.**

A host profile lacking completed-item/segment evidence cannot convert the prior candidate into confirmed disclosure merely because the user spoke again.

---

# 10. Attack: content hash as delivery identity

Suppose exact payload digest is used as the only identity.

Problems:

- identical prose may be legitimately emitted twice;
- same payload to P1 and P2 are distinct human exposures;
- a retry can reuse exact text but be a distinct delivery occurrence;
- hash proves content equality, not host occurrence;
- hash cannot prove which conversational branch/item was displayed.

## Finding F9

**PAYLOAD DIGEST IS A BINDING CHECK, NOT DELIVERY OCCURRENCE IDENTITY.**

Qualified host evidence needs occurrence/recipient identity or a host contract strong enough to imply it.

---

# 11. Attack: exactly-once delivery guarantee

Could HDM promise exactly-once player-visible output?

Not on the baseline platform without host cooperation.

Exactly-once external effect normally requires one of:

- receiver-supported idempotency key/dedupe;
- atomic shared transaction;
- a durable broker/protocol with matching semantics;
- equivalent host-controlled stable occurrence identity.

No ordinary ChatGPT contract found gives HDM an idempotency key for assistant UI messages.

Therefore retry after indeterminate delivery can duplicate visible prose.

The safe semantic goal is not exactly-once output. It is:

```text
NO GAMEPLAY REPLAY
NO FALSE CONFIRMED DISCLOSURE
DUPLICATE-SAFE SAME-PLAYER PRESENTATION WHEN UNCERTAIN
```

## Finding F10

**BASELINE HOST DELIVERY IS NOT EXACTLY-ONCE.**

The candidate spec must state this explicitly.

---

# 12. Attack: never resend after ambiguity

Policy:

```text
unknown prior outcome -> never send again
```

avoids duplicates but risks permanently omitting information the player never received.

For D&D presentation, omission can block understanding/actionability more severely than duplicate same-player explanation.

Therefore when current eligibility permits and the information is required for meaningful continuation, re-presentation is allowed/expected.

Do not necessarily resend the exact full prose. Reconstruct the minimum semantically sufficient presentation from current canonical/knowledge state unless exact wording remains independently protected.

## Finding F11

**UNDER IRREDUCIBLE AMBIGUITY, PREFER AT-LEAST-ONCE SEMANTIC COMMUNICATION OVER AT-MOST-ONCE PROSE.**

This preference applies to the same authenticated eligible recipient and does not authorize broader disclosure.

No owner escalation appears necessary: this follows from existing correctness/knowledge/disclosure separation and the Selective Exact product memory decision.

---

# 13. Attack: always resend after ambiguity

The opposite extreme is also wrong.

Repeatedly sending every unconfirmed old reveal on every turn can produce loops and poor UX.

Re-presentation should happen only when:

- the current task/decision needs the information;
- current eligibility permits it;
- there is no confirmed durable exposure sufficient for the purpose;
- and current presentation can resolve the omission without replaying mechanics.

If the player is proceeding coherently without needing the fact, under-confirmed old delivery can simply remain absent from durable disclosure.

## Finding F12

**NO GENERIC PENDING-DELIVERY REPLAY LOOP.**

This is another reason not to introduce a baseline outbox queue.

---

# 14. Attack: partial streaming and disclosure granularity

One NarrationResult may contain:

```text
paragraph A -> reveals X
paragraph B -> reveals Y
paragraph C -> flavor only
```

If output is stopped after A, full-message confirmation is false, but X may genuinely have been exposed.

Without host segment completion evidence, HDM cannot safely infer X from partial raw stream after the fact.

Options:

- host complete-message confirmation only -> either all full-message refs confirm or none;
- host provides acknowledged semantic segments -> confirm per segment;
- host streams token offsets with durable receipt -> potentially finer, but unnecessary baseline complexity.

## Finding F13

**BASELINE DISCLOSURE QUALIFICATION UNIT SHOULD BE ONE HOST-CONFIRMABLE OUTPUT UNIT, NOT ARBITRARY TOKEN PREFIX.**

If ordinary final message is the only confirmable unit, partial response remains unconfirmed even if the human may have seen a prefix.

If Step 6 proves interleaved discrete user-visible messages can be acknowledged and followed by tools, those may become smaller qualification units without changing semantics.

---

# 15. Attack: interleaved visible commentary as baseline solution

Current harness demonstrates visible commentary before later tool calls.

Could Step 5.12 simply require narration to be emitted there, then persist disclosure afterward?

Problems:

- no official baseline contract reviewed yet guarantees that commentary/progress items are durable normal conversation items;
- UX may differ from ordinary final answers;
- GAME-level prompts may not be able to require the same channel behavior across product surfaces;
- host/client disconnect can still make “visible to human” weaker than server-side emitted;
- Step 4 only needs host-surface emission, not literal read, but the host must define what counts as accepted item.

## Finding F14

**INTERLEAVED EMIT-THEN-CONTINUE IS A STRONG OPTIONAL HOST PROFILE, NOT YET BASELINE SEMANTICS.**

Step 6 should test whether ordinary ChatGPT can lawfully implement this profile.

---

# 16. Attack: Retry/regeneration union semantics

Suppose:

```text
variant A emitted -> reveals X
user clicks Retry
variant B emitted -> reveals Y, omits X
```

Could current disclosure become only Y because B replaced A in visible branch?

No.

Human exposure is monotonic for exact information actually emitted. The user must have interacted with A sufficiently to request Retry; even without relying on that UI detail, if host evidence confirms A and B separately, both exposures remain real.

Therefore:

```text
confirmed(A:X) + confirmed(B:Y)
    -> disclosure X and Y
```

A UI branch replacement does not retract exposure.

## Finding F15

**RETRY/REGENERATE CREATES A NEW DELIVERY GENERATION/OCCURRENCE, NOT A RETROACTIVE EDIT OF HUMAN MEMORY.**

Gameplay consequences remain tied to stored Step-3 execution and are not replayed.

Physical retry identity detection remains Step 6.

---

# 17. Attack: could Retry re-execute tools/gameplay from old context?

Yes, physically, if the host re-invokes the model from an old conversation point and the runtime cannot distinguish presentation regeneration from a new accepted player Interaction.

This is not solved by disclosure state.

Inherited Step-3 laws require stable invocation/idempotency identity. Step-5.11 already carried stable host invocation/message/revision feasibility to Step 6.

Step-5.12 must add a presentation safety requirement:

```text
host-triggered response regeneration
    -> presentation-only regeneration over accepted/current-authoritative evidence
    -> must not create a new RuntimeCommand solely because old player prose reappears
```

If ordinary ChatGPT does not expose sufficient identity to enforce this mechanically, Step 6 must classify the host profile accordingly and impose a resync/no-side-effect guard.

## Finding F16

**RETRY SIDE-EFFECT FENCING IS A STEP-6 HOST CAPABILITY REQUIREMENT, NOT A REASON TO DUPLICATE EXECUTION AUTHORITY IN 5.12.**

---

# 18. Attack: branch-local disclosure

Could each ChatGPT branch maintain its own disclosure history?

No.

A human who saw X cannot be made not to know it by branching from an earlier point.

Therefore durable human exposure is player-global inside the campaign.

Host branch identity is evidence/provenance only.

## Finding F17

**`runtime.disclosure` IS NOT BRANCH-LOCAL.**

New branch recovery uses current campaign disclosure and current campaign authority.

If an actual prior exposure was never durably confirmed, branch may conservatively under-confirm/repeat it; it never rolls back confirmed exposure.

---

# 19. Attack: multiplayer group delivery

Could one outbound group message use one boolean delivered state?

Only if the host contract truly makes message availability atomic for the entire intended audience and Step 4 intentionally defines group accessibility as each player's exposure.

Baseline cannot assume that.

Independent ChatGPT sessions clearly allow:

```text
P1 success
P2 failure
P3 unknown
```

## Finding F18

**DELIVERY EVIDENCE IS RECIPIENT-SCOPED AT THE SEMANTIC BOUNDARY.**

Physical implementations may share one host occurrence ID where appropriate, but `runtime.disclosure` advances independently per player.

---

# 20. Attack: can `runtime.message` be created before confirmation?

Step 5.11 defines runtime message as stable accepted communication evidence and reserves outbound establishment for Step 5.12 qualification.

Creating a normal outbound message record while merely `PREPARED` would blur:

```text
intended communication
vs
historical communication that occurred
```

A separate draft/preparation object would then be needed to keep queries safe.

Given Finding F5, baseline needs no durable prepared owner anyway.

## Finding F19

**BASELINE OUTBOUND `runtime.message` IS ALLOCATED/ESTABLISHED ONLY ON QUALIFIED CONFIRMED EMISSION.**

A volatile delivery candidate may have an ephemeral local key before that point. Rich hosts may have an external host response/item ID before HDM message allocation.

---

# 21. Attack: confirmation can arrive later than occurrence

Suppose host emitted response at real time T1, but trusted evidence is observed at next invocation T2.

Does creating `runtime.message` at T2 falsely say communication happened at T2?

Only if confirmation time is confused with occurrence time.

The message/evidence model must separate:

```text
host occurrence identity/provenance
confirmation/evidence-observation time/order
fictional chronology
repository publication order
```

No scalar timestamp is required for correctness.

## Finding F20

**DELIVERY OCCURRENCE AND HDM CONFIRMATION/PERSISTENCE ARE DISTINCT EVENTS.**

Late confirmation must preserve host occurrence provenance where available and never turn repository commit order into fictional or conversational order.

---

# 22. Attack: exact outbound message after delayed confirmation

If the host confirms an exact completed message and the matching candidate survives, core can establish exact outbound `runtime.message` and optionally make it a Transcript source.

If exact candidate/payload no longer survives but host evidence proves only semantic exposure, should core invent the old exact message text?

No.

Step 5.11 Selective Exact applies:

- exact outbound text only when exact evidence survives;
- otherwise a compact message/provenance/disclosure transition may be recorded if the owner contract supports it;
- never reconstruct a verbatim quote from semantic memory.

## Finding F21

**DELIVERY CONFIRMATION DOES NOT CREATE AN EXACT TRANSCRIPT PROMISE.**

---

# 23. Attack: do confirmed disclosures require immediate publication?

Once host evidence confirms exposure, is publication before any further operation mandatory?

Potential dependent operations:

- next Context Assembler for same player;
- controlled handoff/new host;
- explicit save;
- another recipient's unrelated gameplay.

Within a surviving host, confirmed exposure can update hot authoritative `runtime.disclosure` immediately and be used for same-player context without being durable yet.

Step 5.5 permits SOFT established state.

Before controlled handoff/save, ordinary closure includes it when selected/promise-relevant.

Another player's independent gameplay does not require it.

## Finding F22

**CONFIRMED DISCLOSURE IS ORDINARY SOFT BY DEFAULT; NO UNIVERSAL POST-DELIVERY HARD COMMIT EDGE IS JUSTIFIED.**

A future feature may declare a stronger edge if it depends externally on that exposure before ordinary durability.

---

# 24. Attack: what about one-time choice prompts?

Suppose Narrator asks player to choose A/B, output is lost/unconfirmed, then runtime restarts.

The unresolved choice itself must already live in Procedure/Continuation/Interaction owner state if recovery promised it.

Recovery can re-present the same bounded choice without replaying mechanics or depending on disclosure.

Thus delivery reliability must not own gameplay pending-choice semantics.

## Finding F23

**PENDING GAMEPLAY CHOICE/REACTION REMAINS WITH STEP-3 OWNERS; DELIVERY MAY RE-PRESENT IT.**

This prevents a generic “pending response queue” from becoming execution authority.

---

# 25. Attack: OOC objective-status disclosure

Step 4 specifically allows durable human exposure of objective truth status even when no PC knowledge changes.

If such an OOC reveal is seen but lost before durable confirmation, new chat may fail to remember the user already saw it.

Safe effects:

- do not assume exposure;
- current player may be told again if the task warrants and current eligibility permits;
- objective truth itself remains canonical;
- no fictional knowledge is inferred.

No gameplay correctness state is lost.

## Finding F24

**OOC DISCLOSURE DOES NOT FORCE PRE-SEND DURABILITY; ITS CRASH FALLBACK IS ALSO UNDER-CONFIRMATION.**

---

# 26. Challenge against architecture families

## A — optimistic precommit

**Rejected.** Creates false-positive authority.

## B — strict post-final callback

**Semantically excellent, capability-dependent.** Use when host provides it, but cannot be required from ordinary ChatGPT without Step-6 proof.

## C — durable prepared delivery/outbox

**Rejected as baseline.** Stronger RPO but no correctness consumer justifies always paying the write/lifecycle cost. May be optional future feature/profile.

## D — host-history later confirmation

**Accepted only with trustworthy completed-item evidence + matching candidate.** Naive next-turn/context inference rejected.

## E — capability-tiered HostDeliveryPort

**Accepted as supporting architecture with strict rule:** capability profile may improve how quickly confirmation is obtained but must not change what `runtime.disclosure` means.

## F — no durable disclosure

**Rejected.** Step 4 remains valid.

## G — interleaved visible unit + tool continuation

**Retained as optional strong host profile.** Step 6 must prove its host-item/continuation guarantees and UX suitability.

---

# 27. Resulting pre-candidate architecture

After challenge, the direction tightens to:

> **CONFIRMATION-ONLY DISCLOSURE / MATCHED DELIVERY CANDIDATE + HOST EVIDENCE / SAFE UNDER-CONFIRMATION / SOFT CONFIRMED STATE / NO BASELINE DELIVERY OUTBOX / RECIPIENT-SCOPED OCCURRENCES / CAPABILITY-TIERED CONFIRMATION**

Core flow:

```text
NarrationResult
    |
    v
validate prose + disclosure_refs
    |
    v
ValidatedDeliveryCandidate       # typed working evidence
    exact payload/digest
    recipients
    validated disclosure refs
    source refs
    local generation key
    |
    v
host emission
    |
    +--> qualifying matching evidence
    |       -> CONFIRMED_EMITTED
    |       -> establish outbound runtime.message
    |       -> establish/update runtime.disclosure for each confirmed recipient
    |       -> confirmed state may remain SOFT until ordinary durability edge
    |
    +--> confirmed host failure
    |       -> no message / no disclosure
    |
    `--> no sufficient evidence / ambiguous / interrupted
            -> no confirmed message / no disclosure
            -> candidate may remain volatile while host survives
            -> loss is safe under-confirmation
```

No persistent pending-delivery queue is required.

---

# 28. Host capability contract entering candidate spec

A host profile may support one or more confirmation routes:

## Route H1 — IMMEDIATE ACKNOWLEDGED EMISSION

Host operation returns evidence binding:

```text
host occurrence/item identity
recipient/channel identity
completed payload identity/digest
successful host-surface admission
```

Core may confirm in same invocation.

## Route H2 — INTERLEAVED ACKNOWLEDGED UNIT

Host guarantees a discrete visible output unit is admitted, then permits deterministic continuation/tool work.

Core may confirm that unit after the host continuation boundary.

Current development commentary behavior is only feasibility evidence; Step 6 must prove support.

## Route H3 — DEFERRED EXACT HOST ITEM OBSERVATION

Later invocation supplies trustworthy completed host item identity/content/status matching the retained candidate.

Core confirms then.

## Route H0 — NO QUALIFYING EVIDENCE

No confirmation is established.

Gameplay remains supported under conservative under-confirmation, but disclosure fidelity may degrade after host loss/restart.

This is a **safe degraded delivery-evidence profile**, not permission to fake confirmation.

---

# 29. Does a human owner decision remain?

The challenge searched specifically for an irreducible owner trade-off between:

```text
mandatory durable pre-send reveal preparation
vs
safe under-confirmation with possible duplicate re-disclosure after crash
```

Current conclusion: **no new owner decision is required**.

Reason:

- Step 5.5 already owner-approved deferrable SOFT state and unexpected-loss rollback to actual durable state;
- false-positive avoidance is a correctness requirement, not preference;
- re-disclosure is constrained to the same currently eligible player and does not alter world/PC state;
- Selective Exact already rejects universal exact-output recovery;
- mandatory pre-send outbox adds substantial write/lifecycle cost without closing a correctness gap.

A future owner decision would be required only if product direction changes to a stronger promise such as:

> “Once any material information appears on screen, HDM guarantees that fact of exposure survives even an immediate unexpected host crash with no later host evidence.”

No such promise currently exists.

---

# 30. Candidate requirements derived from challenge

The candidate specification must now explicitly include:

1. positive sparse confirmed `runtime.disclosure` only;
2. delivery evidence outcome separate from disclosure;
3. `ValidatedDeliveryCandidate` typed working evidence;
4. exact candidate/evidence matching before confirmation;
5. full-message or acknowledged-segment qualification; no token-prefix inference;
6. host occurrence/recipient identity distinct from payload digest;
7. outbound `runtime.message` established only on confirmed emission;
8. delayed confirmation permitted;
9. confirmed exposure may remain SOFT until ordinary edge;
10. unexpected crash may degrade to under-confirmation;
11. controlled handoff/save must include confirmed dirty disclosure when promised;
12. no baseline durable prepared-delivery/outbox owner;
13. no generic pending-delivery replay loop;
14. same-player semantic re-presentation under uncertainty only with current eligibility;
15. Retry variants are separate delivery generations and confirmed exposures union monotonically;
16. Retry cannot replay gameplay;
17. branch cannot roll back disclosure or canon;
18. recipient-scoped multiplayer outcomes;
19. PC knowledge separate from player delivery;
20. Story Transcript consumes only confirmed outbound message evidence;
21. capability profiles affect confirmation route, not semantic meaning;
22. baseline does not claim exactly-once host-visible output;
23. no current platform evidence => no confirmed exposure, not failure/success guess;
24. Step 6 gets explicit stable host item/retry/branch/interleaved-emission feasibility requirements.

---

# 31. Challenge verdict

**PASS TO CANDIDATE WITH TIGHTENING.**

No owner-level decision gate is required at this point.

Confidence in direction: **MEDIUM-HIGH**.

Confidence is not HIGH because ordinary ChatGPT's exact deterministic host-item evidence available to shipped HDM remains a Step-6 feasibility question. The architecture remains safe if that evidence is weak, but historical/disclosure fidelity may degrade to conservative under-confirmation more often.
