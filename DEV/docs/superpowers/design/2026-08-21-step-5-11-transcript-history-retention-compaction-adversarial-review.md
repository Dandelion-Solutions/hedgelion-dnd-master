# Step 5.11 — Transcript / History Retention & Compaction — Adversarial Review

Status: **NONCANONICAL ADVERSARIAL REVIEW — CANDIDATE SURVIVES WITH REQUIRED REFINEMENTS**

Date: 2026-08-21

Reviewed candidate:

- `2026-08-21-step-5-11-transcript-history-retention-compaction-candidate-spec.md`

Owner direction remains fixed:

> **S — SELECTIVE EXACT / SEMANTIC CONTINUITY**

No new product-level owner choice emerged. The review found mechanical/cross-system blockers that can be resolved within the approved direction.

---

# 1. Review method

The candidate was attacked against:

- Step-3 Interaction/command idempotency;
- Step-4 truth/knowledge/disclosure/Story separation;
- Step-5.1 domain typing;
- Step-5.5/5.6 durability/publication;
- Step-5.8 live-epoch ownership/identity;
- Step-5.9 chronology;
- Step-5.10 Story source coverage;
- current mutable ChatGPT host behavior;
- exact-wording, mixed IC/OOC, multiplayer, compaction and legacy scenarios from the task brief.

Focus was on irreversible-loss mistakes rather than cosmetic schema details.

---

# 2. Result summary

Candidate direction survives.

Required refinements:

```text
R1  semantic-content discharge before payload loss
R2  minimal exact-text refs/slices rather than whole-message overprotection
R3  verified Transcript exactness must be revocable after Story edits
R4  source candidate identity survives payload compaction
R5  live-born message identity/enumeration obeys Step 5.8 source scoping
R6  Step-3 "raw message linkage" means stable source linkage, not eternal raw payload
R7  outbound message occurrence waits for Step-5.12 qualification
R8  exact-protection routing itself participates in durability closure
```

No blocker requires permanent exact archive, TTL retention, generic event sourcing or Story truth authority.

---

# 3. Blocker R1 — message ID alone is insufficient semantic provenance

## Attack

Candidate allowed:

```text
knowledge/event owner
    -> source message_id

runtime.message
    -> compact envelope only
```

Suppose NPC said:

```text
"The duke is a vampire"
```

and a PC knowledge transition was caused by receiving that claim.

After exact payload deletion, a bare source ref proving only “message M existed” does not establish *which claim* supported the knowledge transition.

This would preserve occurrence identity but lose semantic provenance.

## Required refinement

Before exact payload is dropped, every retained semantic consumer must be independently sufficient for the semantic meaning it promises.

Examples:

```text
knowledge transition
    -> fact/proposition identity + source message ref

SemanticEvent
    -> durable communication/claim meaning + source message ref

contract owner
    -> exact/semantic terms + source message ref
```

A message ref is provenance, not a substitute for semantic content.

## Resolution

Add a **semantic-discharge prerequisite**:

> Payload compaction is legal only when all surviving consumers either require no content beyond occurrence/provenance identity, or independently retain the semantic proposition/content required by their contracts.

This is stronger than exact-text protection and prevents semantic amnesia.

---

# 4. Blocker R2 — whole-message exact protection over-retains mixed IC/OOC text

## Attack

Player writes:

```text
OOC: я тороплюсь сегодня.
PC says: "Серебряный волк".
```

If the password mechanic protects the whole `runtime.message` payload indefinitely, HDM keeps unrelated OOC text solely because one substring is mechanically important.

That contradicts the selected data-minimizing S posture.

The same issue appears with:

- quoted contract clause embedded in action prose;
- in-fiction letter embedded in OOC explanation;
- one exact puzzle answer inside a large mixed message.

## Required refinement

Exact protection must support the **smallest sufficient exact representation**.

Conceptually:

```text
ExactTextRef
    source_message_id
    scope = whole_payload | exact_slice
    stable accepted-text span/range semantics when slice
    expected digest
```

or immediate promotion/copy into the natural canonical owner.

Exact slice offsets are implementation detail, but the semantic rule is mandatory: do not retain unrelated payload when a smaller exact representation satisfies the consumer.

## Resolution

Prefer canonical-owner exact copy when exact text becomes an enduring game object. Use source slices only when source provenance itself remains materially useful.

---

# 5. Blocker R3 — editable Story cannot silently retain “verified exact” status

## Attack

Raw payload is compacted after exact `STORY/TRANSCRIPT` copy T is verified against source digest.

Later an editor improves punctuation or wording in T.

If T remains labeled/treated as exact, HDM can now produce a false verbatim quote.

Story is explicitly editable under Step 4/5.10.

## Required refinement

Exact archival status is content-specific.

Conceptually Transcript exact archival evidence includes:

```text
source ExactTextRef
archived_content_digest
verification_status
```

A material content edit must revalidate against surviving exact verification evidence.

If the new content no longer matches the source/slice digest:

```text
verified_exact = false
```

The record may remain valid editorial Story, but no longer supports a verbatim claim.

## Resolution

Story exactness is a deterministic validation property, not an editorial label.

---

# 6. Blocker R4 — payload compaction must not make Story source candidates disappear behind coverage

## Attack

Step 5.10 requires source-domain candidate enumeration to remain stable enough for coverage/catch-up.

If Transcript candidate identity is defined as “message with exact payload,” then compaction could make an old unprocessed candidate vanish before Story coverage reaches it.

A restarted Chronicler could no longer distinguish:

```text
never considered
```

from:

```text
source payload was compacted
```

## Required refinement

Transcript source candidate identity is the stable message/envelope position, not the presence of exact payload.

Candidate state may expose:

```text
exact_payload_available = true | false
```

For `MAY_OMIT`:

```text
payload unavailable
    -> legal terminal omission
    -> coverage may advance when candidate is considered
```

For `MUST_MATERIALIZE`:

```text
payload compaction forbidden until required output exists
```

## Resolution

Compaction changes payload availability, not source candidate identity/enumeration position.

---

# 7. Blocker R5 — campaign-scoped catalog ID policy conflicts with live-epoch birth

## Attack

Current catalog says `runtime.message` has campaign-scoped sequential ID policy.

Step 5.8 later canonically requires live-born accepted IDs to use collision-free epoch-qualified stable identity where independent live sources can allocate concurrently.

Messages may originate during live-scene ownership.

A single campaign sequential allocator would either create contention or conflict with Step 5.8.

## Required refinement

Step 5.8 supersedes the old machine policy where live-born message evidence exists.

Logical law:

```text
message identity is stable
source-native / live-epoch-safe when born in live source
survives close/absorption unchanged
```

Projection enumeration is likewise source-domain typed. Independent live message domains are not implicitly comparable.

After absorption, explicit routing/indexes may expose them without renumbering IDs.

## Resolution

Record current `runtime.message` campaign-sequential identifier policy as implementation debt requiring Step-5.8-compatible realization.

---

# 8. Blocker R6 — Step-3 “raw message reference” must not imply eternal raw payload

## Attack

Step 3 says `runtime.interaction` owns/references a raw input message.

A literal reading might imply that Step 5.11 cannot ever compact `runtime.message` exact text without violating Step 3.

But Step 3 did not decide retention and Step 5.11 exists precisely to do so.

## Required refinement

Interpret Step-3 linkage as:

```text
Interaction -> stable accepted message evidence identity
```

not:

```text
Interaction -> permanently retained full exact payload
```

The stable message envelope remains addressable after compaction.

Any command/mechanic still requiring exact input independently protects exact representation under Step 5.11.

## Resolution

No Step-3 reopening required; this is a later-slice retention clarification consistent with its ownership model.

---

# 9. Blocker R7 — generated outbound prose is not yet a historical delivered message

## Attack

Candidate has `direction = outbound`, but Step 5.12 owns exact host emission/delivery qualification.

If Step 5.11 creates durable outbound `runtime.message` evidence from `NarrationResult` generation alone, it could record dialogue the player never received.

## Required refinement

Step 5.11 defines the retention shape but not the qualifying edge.

Canonical handoff must remain:

```text
NarrationResult generated
    != outbound accepted/delivered message evidence

Step-5.12 qualification
    -> outbound runtime.message / Transcript candidate becomes eligible
```

Exact timing/acknowledgement/retry semantics remain 5.12.

## Resolution

No durable outbound “said/exposed” claim before Step-5.12 evidence authorizes it.

---

# 10. Blocker R8 — protection routing can itself be lost

## Attack

Suppose consumer C durably references exact text in message M, but the reverse protection routing/index update is lost or delayed.

A maintenance compactor sees M as unprotected and deletes its exact payload.

The forward consumer is correct; derived routing is stale; correctness is lost.

## Required refinement

When a correctness-relevant exact dependency becomes durable, sufficient bounded protection discovery/routing must become durable in the same required closure or before any compaction edge may rely on it.

The reverse index remains derivative authority-wise, but **retention eligibility cannot trust an unverified stale absence**.

Compaction must validate the relevant protection generation/basis against current authoritative owners/index contract.

## Resolution

Exact dependency enrollment/release is a correctness-critical lifecycle derivative similar to other routed recovery/dependency surfaces.

---

# 11. Strongest counterargument to Selective Exact after formalization

The strongest counterargument remains not correctness but future campaign quality:

> A seemingly mundane line can become emotionally or narratively important fifty sessions later, after exact text was lawfully compacted.

No semantic algorithm can perfectly predict future nostalgia.

The chosen S contract accepts this. The architecture should therefore make optional exact archival cheap and prospective expansion possible, but must not covertly turn that possibility into mandatory permanent transcript.

This does not justify reverting to broad archive without an owner policy change.

---

# 12. Mandatory scenario results

## Ordinary flavor dialogue

PASS if semantic state does not depend on exact line. Exact payload may compact; later exact quote may be unavailable.

## Mundane action declaration

PASS when normalized accepted intent/command/state consequences survive independently. Exact prose need not.

## Wish-like wording

PASS only if exact wording remains protected through all mechanics that depend on it or is copied into the canonical mechanic/event owner.

## Contract/oath

PASS when durable contract terms become natural-owner exact/semantic state before source payload release.

## Password

PASS when password value becomes appropriate canonical secret/fact/object state; source message need not remain permanent.

## Riddle/inscription

PASS when exact puzzle text lives with the world object/lore/document owner. Transcript is not required for gameplay correctness.

## Player-authored letter

PASS when exact letter content is promoted to durable document/asset owner.

## NPC lie later challenged

PASS if semantic claim/event survives. Exact quote available only if protected/archived. Transcript claim does not prove objective truth.

## Pre-acceptance clarification

PASS: unaccepted draft need not enter campaign history.

## Post-acceptance correction

PASS: new Interaction/message + lawful semantic correction/reversal; no rewrite of old accepted source.

## Host edit old user message

PASS: accepted `runtime.message` unchanged; host view divergence cannot retcon canon.

## Retry old assistant answer

PASS only if regenerated host prose cannot replay accepted mechanics or replace prior delivered evidence without Step-5.12/current-authority reconciliation.

## Branch old chat

PASS: branch recovers current campaign state; branch location not authority.

## Delete original chat

PASS: gameplay recovery uses campaign storage; optional lost host-only exact prose may remain unavailable.

## Voice input

PASS when exactness claims refer to accepted transcript text, never unverified original acoustics.

## Mixed IC/OOC input

PASS only after R2: protect minimal exact slice/canonical copy, not whole message by default.

## Private whisper / subset visibility

PASS if retention stores provenance but knowledge/disclosure/Story availability owners control visibility.

## Concurrent live messages

PASS only after R5: source-native live-safe IDs and typed enumeration domains.

## Host order vs fictional chronology

PASS: no relation inferred.

## Generated Narrator draft never emitted

PASS only after R7: no delivered/outbound historical occurrence.

## Story exact archive is sole surviving text

PASS after R3: archival text must still match source/slice digest to be called exact; compact canonical envelope provides occurrence/provenance identity.

## Story edited after source loss

PASS if exact certification is recomputed/revoked rather than silently retained.

## Story corrupted after source loss

Gameplay remains correct; historical exactness may become unavailable. Do not reconstruct quote.

## Digest only survives

PASS: equality may be checked against a candidate; prose cannot be reconstructed.

## Story lag + MAY_OMIT source compaction

PASS after R4: candidate envelope persists; later coverage may terminally omit.

## MUST_MATERIALIZE

PASS: compaction prohibited until required exact Story output exists or obligation lawfully ends.

## Semantic provenance after payload compaction

PASS only after R1: consumer keeps proposition/meaning independently.

## Compaction crash / CAS conflict

PASS if old exact payload remains authoritative until one coherent ref-selected result establishes compaction; ambiguous outcome uses Step-5.6 verification.

## Legacy no-transcript campaign

PASS: exact wording unavailable is legitimate; never fabricate.

## 100k-message campaign

PASS if normal gameplay performs no history scan and maintenance/projection work is bounded by typed enumeration/protection indexes.

---

# 13. Cross-step consistency result

With R1–R8 applied:

- Step 3 keeps stable Interaction/message linkage without eternal payload;
- Step 4 keeps transcript/claim/truth/knowledge/disclosure distinct;
- Step 5.1 domain typing remains intact;
- Step 5.5 creates no per-message durability boundary;
- Step 5.6 provides coherent compaction publication;
- Step 5.8 owns live-safe birth/absorption identity;
- Step 5.9 prevents host/message order from becoming fictional time;
- Step 5.10 retains source candidate/coverage continuity;
- Step 5.12 still owns outbound host qualification;
- Step 5.13 still owns physical envelope/orphan deletion;
- Step 6 still owns physical host retry/revision identity feasibility.

No canonical closed step requires reopening.

---

# 14. Review disposition

Candidate direction is accepted for resolution with mandatory refinements R1–R8.

No new owner decision is required.

Next artifact:

**Step 5.11 resolution gate**, incorporating R1–R8 before canonicalization.
