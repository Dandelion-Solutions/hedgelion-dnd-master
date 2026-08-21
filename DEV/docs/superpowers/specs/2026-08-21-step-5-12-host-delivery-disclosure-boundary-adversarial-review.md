# Step 5.12 — Host Delivery / Disclosure Boundary — Adversarial Review

Status: **ADVERSARIAL REVIEW — BLOCKERS FOUND; RESOLUTION REQUIRED**

Date: 2026-08-21

Reviewed candidate:

- `2026-08-21-step-5-12-host-delivery-disclosure-boundary-candidate-spec.md`

Candidate direction:

> **CONFIRMATION-ONLY DISCLOSURE / MATCHED DELIVERY CANDIDATE + HOST EVIDENCE / SAFE UNDER-CONFIRMATION / SOFT CONFIRMED STATE / NO BASELINE DELIVERY OUTBOX / RECIPIENT-SCOPED OCCURRENCES / CAPABILITY-TIERED CONFIRMATION**

The high-level direction survives. Review found **11 required blockers/refinements** before canonicalization. None currently requires a new human product decision.

---

# 1. Review method

The candidate was attacked across:

```text
authority duplication
crash windows
delivery/persistence atomicity
delayed confirmation
truth revision changes
recipient authorization changes
partial output
host transformations
non-Narrator visible surfaces
Retry/Branch
multiplayer/live concurrency
ID allocation
Story/transcript
Selective Exact re-presentation
recovery
scale
```

Each finding below is classified as:

- **BLOCKER** — candidate cannot canonicalize without a normative resolution;
- **REQUIRED REFINEMENT** — direction is sound but wording/contract is incomplete;
- **DEFERRED PHYSICAL** — semantic law is clear; Step 6/implementation owns mechanics.

---

# 2. F1 — delivery must not be the sole owner of a gameplay-significant communication obligation

**Severity: BLOCKER**

Candidate permits losing an unconfirmed delivery candidate and relying on future re-presentation when needed.

Attack:

What if the only place that knows the player still needs to receive X is the volatile candidate itself?

Example:

```text
mechanic establishes a mandatory player choice
Narrator prepares prompt
candidate lost with host crash
no Procedure/Continuation/Interaction owner remembers choice
```

Then “safe under-confirmation” is not safe; the actual gameplay obligation was lost.

The candidate correctly says pending choice stays with Step-3 owners, but this law must be generalized.

## Required resolution R1

Add a law:

> **Any gameplay-significant obligation that must survive until communicated/answered must be owned by its native gameplay/execution/knowledge owner independently of delivery. Delivery evidence may carry presentation, never sole obligation authority.**

Examples:

- pending Choice -> Procedure/Continuation/Interaction;
- PC learned fact X -> world.knowledge + semantic evidence;
- deadline warning that mechanically gates action -> owning Procedure/process/policy;
- mandatory clarification -> accepted Interaction/IntentPlan recovery contract as applicable.

If only presentation fidelity is lost, under-confirmation is safe. If the content is semantically required, its requirement must survive elsewhere.

**Disposition: resolvable mechanically; no owner decision.**

---

# 3. F2 — confirmed outbound message + disclosure transition need one semantic closure

**Severity: BLOCKER**

Candidate says qualifying emission may establish both:

```text
outbound runtime.message
runtime.disclosure
```

but does not require their hot/durable closure to be coherent.

Attack:

```text
message established/published
disclosure row missing
```

or:

```text
disclosure says source message M
M never established
```

would create avoidable authority/provenance split.

## Required resolution R2

Define one logical **QualifiedDeliveryClosure** per confirmed recipient/unit:

```text
qualified host evidence
    -> outbound message occurrence evidence
    -> disclosure transitions implied by validated refs
    -> required indexes/provenance refs
```

They become established coherently in current hot state.

When durability is required, all dirty members of the closure publish in the same applicable campaign-domain transaction/Step-5.6 closure where they share that native source.

This is not a distributed transaction with the host; host effect already occurred/was evidenced separately.

If one physical record is not needed (e.g. a compact confirmed communication envelope suffices), machine realization may optimize representation, but the semantic closure must remain non-split.

**Disposition: blocker resolved by explicit closure law.**

---

# 4. F3 — delayed confirmation must preserve original validation basis, not revalidate content against current truth

**Severity: BLOCKER**

Scenario:

```text
T1: fact F truth transition R1 = established
Narrator validly says “F is true”, refs R1
host emits output
T2: later canon corrects/supersedes with R2
T3: host evidence for old output arrives late
```

If qualification revalidates old prose against current truth, it may reject a historically real exposure or incorrectly relabel it as exposure to R2.

## Required resolution R3

`ValidatedDeliveryCandidate` must bind to the exact accepted validation/source basis required by Step 4, conceptually:

```text
source campaign/native frontier(s)
validated fact refs
exact objective truth transition refs
recipient eligibility basis at generation
payload/disclosure mapping
```

Late qualification asks:

> Was this exact candidate valid/eligible when emitted under its frozen source basis, and does current evidence prove that host occurrence?

It does **not** ask whether the statement is still current truth now.

`runtime.disclosure.latest_exposed_truth_transition_ref` records the exact exposed transition; later correction is separately exposable.

**Disposition: blocker resolved.**

---

# 5. F4 — late confirmation must not require current recipient eligibility

**Severity: REQUIRED REFINEMENT**

Scenario:

```text
P was active/eligible at T1
valid candidate emitted at T1
P removed/deactivated at T2
host confirmation arrives at T3
```

The exposure happened while eligible. Current deactivation must not erase history.

Conversely, current eligibility is required for **future re-presentation**, not historical confirmation.

## Required resolution R4

Separate:

```text
QUALIFICATION OF PAST OCCURRENCE
    uses frozen candidate recipient/eligibility validation basis

NEW / RE-PRESENTED DELIVERY
    uses current authorization/eligibility
```

**Disposition: refinement.**

---

# 6. F5 — structured disclosure refs can be incomplete relative to actual visible leak

**Severity: BLOCKER / UPSTREAM INTEGRITY**

Scenario:

Narrator prose accidentally contains secret X but `disclosure_refs[]` omits X.

Host delivery is genuinely confirmed.

Candidate algorithm would record the message but not X exposure.

This means confirmation-only logic alone cannot guarantee disclosure completeness if Narrator structured metadata is wrong.

## Analysis

Step 4 already states that an unsupported Narrator statement is a correctness failure even if no disclosure ref accompanies it. Step 5.12 must not pretend it can infer the missing fact safely after delivery.

## Required resolution R5

Add laws:

1. `disclosure_refs[]` completeness for material reveal is a **pre-emission validation/integrity requirement** of the Narrator boundary;
2. Step 5.12 SHALL NOT run generic NLP after emission to infer missing refs;
3. if a leak is later detected by explicit evidence/repair, an authorized repair may append the corresponding disclosure/provenance without rewriting the past message;
4. a host message with missing required refs is an integrity defect, not proof that the player remained undisclosed.

The exact automatic validator remains implementation/Step-6 concern; the semantic obligation is normative.

**Disposition: blocker resolved by explicit integrity law.**

---

# 7. F6 — “payload” must cover the whole player-visible delivery unit, not prose text only

**Severity: BLOCKER**

Potential visible material may include:

- prose;
- generated tables/cards;
- image or attachment captions;
- tool/app UI presented to the player;
- link/title metadata that itself reveals a hidden entity;
- citations/source labels;
- progress/intermediate messages if they are actually player-visible.

A secret in a title/card cannot be excluded from disclosure merely because `NarrationResult.prose` is clean.

## Required resolution R6

Generalize candidate `exact_payload` to **player-visible delivery content representation** under the host profile.

For initial text-first HDM, exact text may remain the common representation, but the host contract must state which other visible surfaces are part of the unit.

Whole-unit material disclosure completeness applies to every player-visible content channel admitted by the host profile.

Internal tool results that the host guarantees are not player-visible are not delivery content.

**Disposition: blocker resolved; physical multimodal encoding deferred.**

---

# 8. F7 — visible tool/progress/commentary surfaces can bypass Narrator if not explicitly fenced

**Severity: BLOCKER**

The candidate treats NarrationResult as the normal player-facing source, but real ChatGPT hosts may display:

- tool cards;
- progress/commentary messages;
- connector source chips;
- generated artifacts;
- error text.

If private DM/tool content leaks through these surfaces, `runtime.disclosure` metadata will not prevent the human from seeing it.

## Required resolution R7

Host profile must classify every runtime output surface as one of:

```text
PLAYER_VISIBLE_DELIVERY_SURFACE
    content must independently satisfy role/player eligibility
    material reveals require disclosure metadata/qualification

NON_PLAYER_VISIBLE_INTERNAL_SURFACE
    host contract guarantees not exposed to player
```

No “debug/internal” label is sufficient if the actual product renders it.

Gameplay runtime SHALL NOT place Narrator-ineligible/private source material in any player-visible tool/progress/error surface.

If an interleaved commentary route H2 is used intentionally, that commentary becomes a formal delivery unit subject to all Step-5.12 laws.

**Disposition: blocker resolved. Physical surface inventory belongs Step 6.**

---

# 9. F8 — host transformation/moderation can break candidate-content equivalence

**Severity: REQUIRED REFINEMENT**

A host may theoretically:

- truncate;
- redact;
- transform markdown;
- replace response with an error/refusal;
- render a different structured representation.

Therefore evidence that “candidate was submitted to host” is not sufficient if the host can materially change player-visible content before establishing the item.

## Required resolution R8

`CONFIRMED_EMITTED` requires the host profile to prove equivalence at the **delivery-content representation level** relevant to disclosure.

Possible valid contracts:

- host guarantees candidate content is persisted without material semantic transformation;
- evidence returns the established item content/digest and it matches candidate;
- acknowledged segment identity is defined after transformation.

If equivalence cannot be proven, outcome for candidate qualification remains unconfirmed even if some host output occurred.

Presentation transformation that preserves exact accepted text representation under documented rendering rules may be normalized mechanically; do not require DOM byte identity.

**Disposition: refinement.**

---

# 10. F9 — concurrent outbound message ID allocation must respect Step 5.8

**Severity: BLOCKER / MACHINE-REALIZATION CONTRACT**

Current legacy ID policy says campaign-sequential `runtime.message` IDs.

But Step 5.11 already found that live/concurrent message identity must be collision-safe and source-native.

Scenario:

```text
P1 chat confirms outbound message
P2 chat confirms another outbound message concurrently
both allocate next campaign message number
```

A global sequential allocator would create contention/collision or force a campaign write merely to reserve IDs.

## Required resolution R9

Canonical 5.12 must inherit Step-5.11/5.8 law:

- delivery/message occurrence identity is stable and collision-safe across concurrently writable sources;
- no campaign-global message allocator is required on the hot path;
- physical live/source-qualified ID policy is implementation debt;
- Story Transcript IDs remain separate layer-local IDs from Step 5.10.

**Disposition: blocker resolved at semantic level.**

---

# 11. F10 — concurrent disclosure merge cannot use Git/host order as “latest truth revision”

**Severity: BLOCKER**

Scenario:

Two confirmed outputs to the same player reference different truth transitions of one fact due retries/concurrency.

`runtime.disclosure.latest_exposed_truth_transition_ref` must not choose by:

- later Git commit;
- later host message ID;
- lexicographic ID;
- wall-clock timestamp.

It should represent the most advanced exposed objective-status transition under the fact owner's own transition lineage/semantic revision contract.

If one exposure is an older transition delivered later, it does not make the player “unsee” the newer transition.

## Required resolution R10

Disclosure merge is monotonic and semantic:

```text
statement_exposed = OR
objective-status exposure refs accumulate/advance under owner-defined truth-transition relation
```

The exact compact representation may remain Step-4 implementation work, but candidate cannot imply transport order decides semantic “latest”.

If conflicting/incomparable revision evidence occurs where owner contract expects a line, raise scoped integrity/reconciliation rather than choose transport order.

**Disposition: blocker resolved.**

---

# 12. F11 — re-presentation must not invent a new fictional speech act

**Severity: BLOCKER**

This is the most important D&D-specific presentation issue.

Scenario:

```text
NPC canonically said exact line L at event E
human delivery failed/unconfirmed
later runtime re-presents the information
```

If Narrator simply speaks as the NPC again with different wording, it may accidentally create:

- a second fictional utterance;
- altered contract/oath wording;
- changed clue phrasing;
- new social consequences;
- false chronology.

## Required resolution R11

Re-presentation of already-established fiction is **presentation replay**, not a new fictional action.

Rules:

- if exact fictional wording is still protected by its natural owner, quote/use that exact wording;
- if only semantic meaning survives, summarize the past occurrence without invented quotation;
- do not create a second NPC action/event merely to repair host delivery;
- no new world.knowledge transition is created unless a genuinely new fictional communication occurs.

This directly composes Step 5.11 Selective Exact with Step 5.12 safe under-confirmation.

**Disposition: blocker resolved.**

---

# 13. Additional adversarial scenarios

## S1 — generation fails before validation

Expected:

- no candidate;
- no host occurrence;
- no outbound message;
- no disclosure.

**PASS.**

## S2 — disclosure ref fails validation

Expected:

- do not emit candidate containing unsupported material;
- no disclosure.

**PASS if R5 completeness/validation law added.**

## S3 — canon commits, Narrator fails

Expected:

- canon remains;
- later presentation from current authoritative result;
- no gameplay replay.

**PASS.**

## S4 — host emits partial prefix then user stops

Expected:

- full candidate not qualified;
- no confirmed refs absent acknowledged segment evidence;
- human may have seen prefix but engine under-confirms;
- future re-presentation allowed.

**PASS.**

## S5 — host complete item immediate ACK

Expected:

- candidate/evidence match;
- establish QualifiedDeliveryClosure;
- disclosure/message hot state.

**PASS after R2/R3.**

## S6 — host confirms rejection

Expected:

- no message/disclosure;
- later presentation can try again from current semantics.

**PASS.**

## S7 — host outcome indeterminate

Expected:

- no confirmed disclosure;
- volatile evidence may remain while useful;
- no blind gameplay retry;
- re-present only when needed/eligible.

**PASS.**

## S8 — user closes app immediately after reveal

If host did not provide qualifying ACK and hot candidate disappears:

- durable disclosure absent;
- later under-confirmation/re-presentation.

If host qualified exposure but disclosure dirty state was lost before durability:

- same durable fallback.

**PASS under Step-5.5 RPO.**

## S9 — controlled handoff after confirmed dirty exposure

Required:

- handoff closure includes dirty disclosure/message if relevant to promised future context.

**PASS.**

## S10 — explicit save after confirmed dirty exposure

Sparse gameplay-significant disclosure falls in selected save scope when required by current campaign context.

Do not require Story catch-up.

**PASS.**

## S11 — new chat after under-confirmed reveal

- campaign lacks proof;
- no host-history reconstruction;
- current eligibility/current PC knowledge may cause semantic information to be shown again.

**PASS.**

## S12 — current eligibility revoked before repair

- do not re-present merely due prior possible delivery;
- confirmed historical exposure, if later evidence arrives, may still be recorded under frozen original basis.

**PASS after R4.**

## S13 — user explicitly quotes a fact from a partial/unconfirmed answer

Can user self-report prove host delivery?

No. The user may know the fact from repository browsing, another source or prior session.

User message is evidence of current human knowledge in an informal sense, but Step-4 `runtime.disclosure` means HDM-qualified exposure occurrence. Do not forge host delivery provenance.

A separate future product concept of self-declared player knowledge is unnecessary for current correctness.

**PASS; no inference.**

## S14 — Retry same exact text

Two host occurrences may share digest.

- digest alone does not dedupe occurrence;
- if both confirmed, current disclosure unchanged after first because exposure relation is idempotent/monotonic;
- historical message retention may retain one/both under policy.

**PASS.**

## S15 — Retry different text revealing additional fact

- new candidate generation;
- new confirmed occurrence;
- additional disclosure advances.

**PASS.**

## S16 — Retry from stale world state

- no gameplay replay;
- current-authority/idempotency fence;
- presentation may use retained historical accepted result if available/appropriate, otherwise current lawful summary.

**PASS semantically; physical detection Step 6.**

## S17 — Branch from before confirmed reveal

- campaign disclosure remains;
- branch does not unsee.

**PASS.**

## S18 — chat deletion after confirmed durable exposure

- disclosure survives;
- outbound exact payload may survive/compact per S policy.

**PASS.**

## S19 — private P1 reveal, P2 not eligible

- candidate recipient set P1;
- only P1 qualifies;
- P2 Context Assembler not given secret.

**PASS.**

## S20 — P1 confirm / P2 failure

- per-recipient outcomes;
- no group widening.

**PASS.**

## S21 — PC knowledge true, player delivery false

- PC knowledge remains;
- later presentation from existing knowledge.

**PASS.**

## S22 — shared live fact commits, narration fails

- live truth remains;
- another PC may observe from live state according to their own channel;
- original player's message can be regenerated.

**PASS.**

## S23 — live epoch closes with dirty confirmed human disclosure

Human disclosure is not live scene truth.

Implementation may publish it in campaign closure/absorption or another ordinary campaign batch under Step-5.5 depending dirty scope. It must not remain as a second durable live-only authority after absorption.

**PASS after R2/R9 plus Step-5.8 realization.**

## S24 — Story catch-up sees candidate only

- not admitted.

**PASS.**

## S25 — Story sees qualified outbound message

- normal Transcript candidate under 5.11 policy.

**PASS.**

## S26 — exact outbound payload compacted later

- disclosure current relation remains;
- source provenance/digest envelope survives as required;
- exact quote unavailable if not archived/protected.

**PASS.**

## S27 — campaign publication conflict while persisting confirmed disclosure

Actual human exposure is already real.

- refresh campaign;
- apply monotonic transition on current state;
- do not resend just because Git conflicted;
- no gameplay replay.

**PASS.**

## S28 — Git publication ACK indeterminate

Resolve campaign ref/lineage under Step 5.6.

Host delivery outcome is a different domain and is not re-run because Git ACK is unclear.

**PASS.**

## S29 — host transforms candidate into safety refusal

Candidate digest/content does not match final host occurrence under a transforming profile.

- no candidate qualification;
- refusal itself may be an outbound host message only if separately modeled/qualified as its own delivery content;
- no planned secret disclosure.

**PASS after R8.**

## S30 — tool source chip exposes hidden NPC name

If chip is player-visible, this is a delivery surface leak.

Candidate current text-only model would miss it.

**FAIL without R6/R7; resolved by whole-surface classification.**

## S31 — progress commentary deliberately carries narration then tool persists disclosure

Under H2 profile:

- commentary must be formal delivery unit;
- host must prove its admission/content binding;
- only then post-emission tool work can confirm.

If profile cannot prove this, commentary remains unconfirmed even though likely visible.

**PASS after R7.**

## S32 — 100k-message campaign

No history scan required:

- current candidate is local;
- host evidence is direct/bounded;
- disclosure keyed by player/fact;
- message lookup by stable ID/index.

**PASS.**

## S33 — voice response interrupted

Without acknowledged audio/text segment completion:

- no full candidate qualification;
- under-confirm.

Exact spoken acoustics are not promised by Step 5.11.

**PASS.**

---

# 14. Cross-step contamination review

## Step 3

No duplicate execution owner introduced.

Retry presentation remains outside RuntimeCommand replay.

**PASS.**

## Step 4

`runtime.disclosure` remains sole current human exposure owner.

Need R5/R6/R7 to ensure actual visible surfaces cannot bypass structured disclosure semantics unnoticed.

**PASS AFTER RESOLUTION.**

## Step 5.1

No global delivery frontier/order introduced.

**PASS.**

## Step 5.2 / 5.4 / 5.7

No generic pending-delivery root required because unconfirmed candidate loss is safe.

R1 ensures actual gameplay obligations remain with native owners.

**PASS AFTER R1.**

## Step 5.5

Confirmed disclosure SOFT by default is legal.

No unjustified per-message HARD edge.

**PASS.**

## Step 5.6

Host ambiguity distinct from Git ambiguity.

Qualified message+disclosure durable closure needs R2.

**PASS AFTER R2.**

## Step 5.8

Recipient-scoped semantics compatible.

R9 required for concurrent IDs; legacy live disclosure wording must be normalized later.

**PASS AFTER R9.**

## Step 5.9

No transport/delivery order becomes fictional chronology.

R11 prevents re-presentation from creating false new fictional speech.

**PASS AFTER R11.**

## Step 5.10 / 5.11

Only confirmed messages feed Transcript; Selective Exact preserved.

R11 important for exact speech replay.

**PASS AFTER R11.**

---

# 15. Performance / YAGNI review

Candidate remains bounded:

- no background worker;
- no outbox queue;
- no campaign-wide history scan;
- no delivery heartbeat;
- no commit before every response;
- no three-valued current disclosure;
- no universal exactly-once protocol;
- no token-level streaming ledger.

Required additions R1–R11 do not introduce new baseline long-lived infrastructure.

The largest physical complexity remains in Step 6 host profile realization, as intended.

---

# 16. Required resolutions summary

| ID | Requirement | Severity | New owner decision? |
|---|---|---:|---|
| R1 | gameplay-required communication obligation must live outside delivery | blocker | no |
| R2 | QualifiedDeliveryClosure atomic/coherent message + disclosure establishment/publication | blocker | no |
| R3 | candidate binds original source/validation/truth-transition basis | blocker | no |
| R4 | late confirmation uses original eligibility; re-presentation uses current eligibility | refinement | no |
| R5 | disclosure-ref completeness is pre-emission integrity obligation; repair append-only | blocker | no |
| R6 | delivery unit covers whole player-visible content, not prose only | blocker | no |
| R7 | classify every visible/internal host surface; commentary/tool UI cannot bypass boundary | blocker | no |
| R8 | host transformation requires post-transform equivalence/content evidence | refinement | no |
| R9 | collision-safe source-native outbound message identity under concurrency | blocker | no |
| R10 | disclosure merge uses semantic truth-transition lineage, not transport order | blocker | no |
| R11 | re-presentation is past-event presentation, never invented second fictional speech/action | blocker | no |

---

# 17. Adversarial verdict

**DIRECTION SURVIVES — RESOLUTION GATE REQUIRED.**

No new human decision is required.

The candidate must be amended/consolidated with R1–R11 before canonicalization.

Confidence after review: **HIGH on semantic direction, MEDIUM on ordinary-ChatGPT physical confirmation quality**.

The remaining medium-confidence area is intentionally Step 6: which host delivery evidence routes ordinary ChatGPT can expose deterministically without custom API/application infrastructure.
