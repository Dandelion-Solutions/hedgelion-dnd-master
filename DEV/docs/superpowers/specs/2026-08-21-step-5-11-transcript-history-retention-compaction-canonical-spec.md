# Step 5.11 — Transcript / History Retention & Compaction — Canonical Specification

Status: **CANONICAL — STEP 5.11 ARCHITECTURE CLOSED**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Canonicalization basis:

- `2026-08-21-step-5-11-transcript-history-retention-compaction-task-brief.md`
- `2026-08-21-step-5-11-transcript-history-retention-compaction-research-draft.md`
- `2026-08-21-step-5-11-transcript-history-retention-compaction-analytical-challenge.md`
- `2026-08-21-step-5-11-transcript-history-retention-compaction-decision-brief.md`
- `2026-08-21-step-5-11-selective-exact-semantic-continuity-owner-decision.md`
- `2026-08-21-step-5-11-transcript-history-retention-compaction-candidate-spec.md`
- `2026-08-21-step-5-11-transcript-history-retention-compaction-adversarial-review.md`
- `2026-08-21-step-5-11-transcript-history-retention-compaction-resolution-gate.md`

Owner-approved product direction:

> **S — SELECTIVE EXACT / SEMANTIC CONTINUITY**

Canonical architecture direction:

> **STABLE MESSAGE EVIDENCE / SELECTIVE EXACT PROTECTION / SEMANTIC-DISCHARGE COMPACTION / OPTIONAL VERIFIED TRANSCRIPT ARCHIVE**

This specification defines Transcript/history retention semantics only. It does not define the exact outbound host-delivery acknowledgement protocol (Step 5.12), generic physical GC/orphan cleanup (Step 5.13), or physical ChatGPT host/message revision identity feasibility (Step 6).

---

# 1. Product memory contract

HDM is designed to remember established campaign meaning extremely well without promising to act as a permanent verbatim recorder of every arbitrary conversation item.

Canonical product principle:

> **The Master may have excellent, effectively permanent memory in the human sense, but it is not a tape recorder.**

Therefore:

```text
SEMANTIC CONTINUITY
    is a baseline correctness/product promise

VERBATIM RECALL
    is a selective retained capability
```

If exact wording remains protected or deliberately archived, HDM may quote it exactly.

If exact wording has been lawfully compacted and no exact copy survives, HDM must say that the exact wording is no longer retained and use the strongest surviving semantic evidence. It must not invent a plausible quote and present it as verbatim.

## LAW 5.11-1 — SEMANTIC MEMORY IS STRONGER THAN VERBATIM ARCHIVE PROMISE

Loss of unprotected exact prose may be lawful.

Loss of materially established campaign meaning required by current-state, execution, knowledge, disclosure, chronology or historical owner contracts is not lawful.

---

# 2. Host conversation is not campaign authority

Visible ChatGPT conversation history is a mutable host/product surface.

Current product behavior permits old-message editing, assistant retry/regeneration, conversation branching and chat deletion. Project/chat memory is contextual product assistance, not HDM-owned immutable storage.

Therefore host history cannot be the sole durable campaign transcript authority.

## LAW 5.11-2 — HOST MUTATION DOES NOT RETCON ACCEPTED CAMPAIGN HISTORY

After a communication has crossed the accepted HDM Interaction boundary, later host edit/retry/branch/delete operations do not rewrite the accepted Interaction, message evidence, commands, events or canonical state.

Current campaign authority is resolved from campaign storage/routing under Steps 5.6–5.8, not from the host conversation cursor.

---

# 3. Authority geometry

```text
HOST CHAT ITEM
    mutable host presentation/context
        |
        v
runtime.interaction
    stable accepted external exchange identity
        |
        v
runtime.message
    stable accepted communication evidence identity
    exact accepted representation while retained
    compact provenance after payload compaction
        |
        +------------------------------+
        |                              |
        v                              v
CANONICAL / HISTORICAL OWNERS       STORY/TRANSCRIPT
world/runtime current owners         optional noncanonical exact archive
SemanticEvent / LOG                  dialogue/history fidelity
MechanicalEvent / receipt            presentation/reconstruction
world.knowledge                       never gameplay truth authority
runtime.disclosure
contract/document/clue/mechanic owner
```

A communication record may prove that a statement was accepted/said/exposed when applicable evidence establishes that occurrence. It does not prove the proposition inside the statement is objectively true.

---

# 4. `runtime.message` canonical responsibility

Step 3 already admits `runtime.message` and `runtime.interaction`.

`runtime.message` is canonically the stable HDM-owned historical/evidence identity for one accepted participant communication representation relevant to a durable Interaction/history contract.

Conceptually:

```text
RuntimeMessage
    message_id
    interaction_id
    direction                  inbound | outbound
    participant/player/speaker provenance
    channel / communication class
    accepted representation kind
    payload_state              EXACT_RETAINED | COMPACTED
    exact_text?                when retained
    content_digest
    compact provenance metadata
    source-domain enumeration identity/token
    semantic/history refs as needed
    delivery evidence ref?     outbound, Step-5.12 qualified
```

Exact machine fields remain implementation work.

## LAW 5.11-3 — MESSAGE IDENTITY SURVIVES PAYLOAD COMPACTION

Compacting exact text does not silently repurpose or remove the stable historical meaning of `message_id`.

The compact envelope remains the historical source identity until later lawful Step-5.13 physical cleanup.

## LAW 5.11-4 — STEP-3 RAW MESSAGE LINKAGE IS STABLE EVIDENCE LINKAGE

Step-3 `runtime.interaction -> raw input message reference` requires stable linkage to the accepted message evidence identity.

It does not require eternal retention of full exact payload after lawful Step-5.11 compaction.

Any consumer that still requires exact input retains its own Step-5.11 protection.

---

# 5. Exactness definition

Baseline exactness means **text-exact relative to the textual representation accepted by HDM**.

For ordinary text:

- exact accepted Unicode/text content is authoritative for verbatim claims;
- semantically visible formatting needed to distinguish content is preserved according to the accepted representation contract;
- byte identity with undocumented host UI/HTTP payloads is not promised.

For voice-mode interaction:

- exactness is relative to the accepted transcript text presented to HDM;
- HDM does not claim verbatim identity with original acoustic speech when the host transcription may differ.

For media/attachments:

- stable references/provenance may be retained;
- exact binary archival is not implied by Transcript retention;
- enduring in-fiction documents/images/objects must move into their proper world/asset owners when their content is itself canonical.

## LAW 5.11-5 — NO VERBATIM CLAIM WITHOUT EXACT EVIDENCE

A summary, SemanticEvent, hash alone, model memory, paraphrase or regenerated prose cannot be presented as exact historical wording.

---

# 6. Durable admission boundary

Not every host-visible item becomes durable HDM message history.

Possible durable communication evidence includes:

- accepted participant gameplay input linked to a durable Interaction/command/history contract;
- OOC input when a durable campaign/configuration/history owner requires provenance;
- delivered outbound player-facing content after Step-5.12 qualification;
- other explicitly admitted communication classes.

Excluded by default:

- hidden chain-of-thought;
- developer/system/project instructions;
- private tool traces;
- private Dramaturg/Actor reasoning;
- generated but never emitted Narrator drafts;
- repository plumbing/diagnostics;
- other non-participant internal material.

## LAW 5.11-6 — HOST VISIBILITY ALONE DOES NOT CREATE DURABLE TRANSCRIPT HISTORY

Durable admission follows HDM Interaction/history semantics, not “everything visible in ChatGPT”.

---

# 7. Durability timing

Step 5.11 creates no per-message save boundary.

An accepted textual payload may initially exist only in current HOT/execution context.

When resulting Interaction/command/canonical history becomes durable, its Step-5.5/5.6 required closure must include enough message/interaction evidence to preserve all retained dependencies of that durable result.

A message may first publish as `EXACT_RETAINED` or, if all exact and semantic requirements are already discharged, as `COMPACTED`.

## LAW 5.11-7 — MESSAGE ARRIVAL IS NOT A PUBLICATION EDGE

Durability continues to follow named semantic/correctness edges from Steps 5.3–5.6.

No heartbeat/write is created merely because a conversational message arrived.

---

# 8. Exact-text protection

Exact text is protected when a live/promised consumer requires exact form rather than only semantic meaning.

Examples include:

- wording-dependent adjudication;
- exact contract/oath terms before those terms are independently owned;
- password/passphrase content while the exact token itself remains material;
- riddle/inscription/code/poem text whose exact form is a game object;
- player-authored in-fiction document content;
- explicit durable exact-quote dependency;
- another registered owner-specific requirement.

Conceptually:

```text
EXACT_TEXT_PROTECTED(source)
    iff an admitted consumer still needs exact accepted form
    and no independent sufficient exact owner has discharged that need
```

## LAW 5.11-8 — EXACT PROTECTION IS OWNER-DECLARED, NOT LLM-IMPORTANCE AUTHORITY

The semantic consumer/contract owns the requirement.

Chronicler, Narrator or another LLM may recommend archival value but cannot by editorial judgment prove that correctness-critical exact evidence is deletable.

---

# 9. Minimal exact representation

Exact protection must retain the **smallest sufficient accepted-text representation**.

A consumer may require:

```text
whole accepted payload
OR
an exact slice/span of accepted payload
OR
an independently owned exact canonical copy
```

Conceptually an exact source reference may identify:

```text
ExactTextRef
    source_message_id
    scope = whole_payload | exact_slice
    stable slice/range semantics if applicable
    expected digest
```

Exact offset encoding remains implementation detail.

## LAW 5.11-9 — DO NOT OVER-RETAIN MIXED IC/OOC PAYLOAD

If only one exact phrase in a mixed message is material, HDM should not protect unrelated OOC/private prose merely because both occurred in one host message.

Prefer smallest exact slice or immediate promotion into the natural owner.

---

# 10. Semantic-content discharge

Exact-text protection and semantic-history sufficiency are separate questions.

A message may be unprotected verbatim while still being the only place that explains the meaning of an enduring semantic relation.

Example:

```text
knowledge owner -> source message_id
```

is insufficient after payload loss if no fact/proposition/event independently records which claim was received.

## LAW 5.11-10 — SEMANTIC CONSUMERS MUST BE CONTENT-SUFFICIENT BEFORE PAYLOAD LOSS

Before exact payload compaction, every surviving semantic consumer must satisfy one of:

```text
needs occurrence/provenance identity only

OR

independently retains the proposition/content/meaning
required by its own contract
```

A bare `message_id` cannot substitute for semantic content that would otherwise disappear.

This applies to knowledge/disclosure provenance, contracts, historical events, corrections and other retained consumers.

---

# 11. Natural-owner promotion

When exact wording becomes an enduring semantic property of a world/runtime object, that content should live with its natural canonical owner rather than forcing arbitrary chat retention.

Examples:

```text
contract terms
    -> world.contract

player-authored letter
    -> world.asset/document owner

riddle/inscription established in world
    -> applicable world asset/location/lore owner

persistent wording-dependent mechanic
    -> command/effect/event/contract owner required by that mechanic
```

`runtime.message` may remain provenance, but need not remain the only exact content holder.

## LAW 5.11-11 — CORRECTNESS-CRITICAL EXACT SEMANTICS MAY NOT BE DEMOTED INTO STORY

If gameplay correctness still depends on exact text, the required exact representation remains in canonical/runtime historical evidence or a proper canonical owner.

`STORY/TRANSCRIPT` alone cannot become the gameplay authority merely because it contains the same prose.

---

# 12. Bounded protection routing

Compaction cannot perform a campaign-wide search for possible textual consumers.

Protection-bearing owner kinds expose typed exact-text dependencies.

A rebuildable reverse routing/index may support:

```text
message/slice -> active exact-text consumer refs
```

Forward owner dependencies remain semantic authority.

## LAW 5.11-12 — PROTECTION ROUTING PARTICIPATES IN DURABLE CLOSURE

When a correctness-relevant exact dependency becomes durable, sufficient bounded protection routing/discovery must become durable in the same required closure or before any compaction edge may rely on its absence.

A stale derived index cannot authorize irreversible payload loss.

## LAW 5.11-13 — NO GENERIC GLOBAL REFERENCE COUNT

Only admitted owner-specific retention dependency classes participate. Step 5.11 does not create a universal GC/reference-count subsystem.

---

# 13. Payload lifecycle

Canonical payload lifecycle:

```text
EXACT_RETAINED
    exact accepted text available
    digest/provenance available

        |
        | exact protection discharged
        | semantic-content discharge satisfied
        | Story/source continuity satisfied
        v

COMPACTED
    no exact source payload
    stable message/interaction identity remains
    digest remains
    compact provenance remains
    source-enumeration identity remains
    required semantic/history refs remain
```

Physical removal of the compact envelope is Step 5.13.

## LAW 5.11-14 — COMPACTION IS IRREVERSIBLE LOSS OF SOURCE VERBATIM CAPABILITY

If no independent exact copy remains, `EXACT_RETAINED -> COMPACTED` permanently removes verbatim recovery from that source.

Later LLM reconstruction cannot restore exact-history status.

## LAW 5.11-15 — HASH DOES NOT STORE TEXT

Digest can validate equality against an available candidate copy. Digest alone cannot reconstruct deleted prose or satisfy a consumer requiring content.

---

# 14. `STORY/TRANSCRIPT` role

Under Selective Exact, `STORY/TRANSCRIPT` is an optional durable noncanonical exact/near-exact historical presentation archive.

Ordinary Transcript source candidates may be `MAY_OMIT`.

A typed archival request/policy may require:

```text
MUST_MATERIALIZE before source exact payload compaction
```

No unrelated Story layer must catch up.

Possible reasons include explicit archival/export requirements or a registered historical-presentation retention policy.

## LAW 5.11-16 — OPTIONAL STORY ARCHIVAL DOES NOT EXPAND THE GLOBAL PRODUCT PROMISE

Selected exact Transcript retention does not mean all gameplay discourse is permanently verbatim recoverable.

---

# 15. Verified exact Transcript archive

A Transcript record may remain the only surviving exact textual copy after raw message payload compaction.

To support a verbatim historical/presentation claim, its content must remain deterministically verifiable against surviving exact source evidence such as whole/slice digest and stable source identity.

Conceptually:

```text
Transcript exact archive
    source ExactTextRef
    archived content
    archived content digest
    verification status
```

## LAW 5.11-17 — STORY EXACTNESS IS CONTENT-SPECIFIC VALIDATION, NOT A PERMANENT LABEL

If a Story edit changes archived content such that it no longer matches the surviving source/slice digest:

```text
verified_exact = false
```

The edited record may remain valid editorial Story but cannot be used as a verbatim source.

## LAW 5.11-18 — VERIFIED STORY COPY DOES NOT PROVE OBJECTIVE CLAIM TRUTH

A verified Transcript can preserve exactly what was communicated. It does not establish that the communicated proposition is objectively true.

---

# 16. Step-5.10 source candidate continuity

Transcript projection candidate identity is the stable message/envelope source position, not “message while exact payload exists”.

Compaction changes payload availability but not source candidate identity.

Conceptually:

```text
candidate
    message identity
    exact_payload_available = true | false
```

For `MAY_OMIT`:

```text
exact payload unavailable
    -> candidate may terminally omit when considered
    -> coverage may advance
```

For `MUST_MATERIALIZE`:

```text
source compaction is blocked
until required compatible Transcript output exists
or obligation lawfully ends
```

## LAW 5.11-19 — PAYLOAD COMPACTION MUST NOT STRAND STORY COVERAGE

Source-domain identity, enumeration semantics and required cursor anchors remain interpretable after lawful payload compaction.

No all-history reconstruction is required merely because old exact payload was dropped.

---

# 17. Source enumeration is nonfictional

`runtime.message` may provide append-monotonic owner/source-local projection enumeration.

Its order means only source/history enumeration within that declared domain.

It does not imply:

- fictional causal order;
- fictional temporal order;
- simultaneity;
- order across independent live sources;
- narrative reading order.

Git commit order likewise gains no fictional meaning.

---

# 18. Live/multiplayer identity

Message evidence may be born under independently writable live epochs.

Step 5.8 governs identity/concurrency.

## LAW 5.11-20 — LIVE-BORN MESSAGE IDENTITY IS SOURCE-NATIVE AND COLLISION-SAFE

A message born in live-owned scope must use Step-5.8-compatible stable collision-free identity/allocation and retain that identity through close/absorption.

Independent source enumeration domains are not implicitly comparable.

The current legacy campaign-sequential `runtime.message` catalog policy is implementation debt where it conflicts with this law.

---

# 19. Inbound host edit/correction

### Before acceptance

A clarification/edit that occurs before HDM accepts an Interaction does not require the abandoned draft to become durable historical evidence.

### After acceptance

Later editing the visible host message does not mutate the accepted `runtime.message` or its established consequences.

To change campaign semantics, a new Interaction/correction must be accepted.

### Correction after canonical consequence

The new correction may cause a lawful new transition/reversal/supersession under the owning semantic contracts. It does not rewrite historical evidence in place.

## LAW 5.11-21 — HOST UI EDIT IS NOT CANONICAL CORRECTION

Only an accepted HDM correction path may change established campaign meaning.

---

# 20. Assistant retry/regeneration and branching

Retry/regeneration of an older assistant response cannot replay or replace accepted gameplay merely because different prose appears in the host UI.

A chat branched from an older conversational point must recover/reconcile against current campaign authority before new gameplay is accepted.

Deleting the original host chat does not delete campaign storage.

Stable host retry/edit revision identity exposure remains Step-6 feasibility work.

## LAW 5.11-22 — HOST BRANCH POSITION IS NOT RECOVERY AUTHORITY

Campaign storage/routing wins over visible branch history when they diverge.

---

# 21. Outbound delivery handoff to Step 5.12

Generated Narrator prose is not yet durable evidence that those words were emitted/exposed to a player.

Canonical handoff remains:

```text
NarrationResult generated
    !=
qualified outbound communication occurrence

Step-5.12 host-delivery qualification
    -> outbound runtime.message / Transcript candidate may become established
```

## LAW 5.11-23 — UNEMITTED DRAFTS ARE NOT TRANSCRIPT HISTORY

Step 5.11 defines retention shape only. Step 5.12 decides the authoritative emission/delivery boundary and retry/duplicate semantics.

---

# 22. In-fiction exact speech versus gist

A player can provide exact fictional speech or only describe communication intent.

Example:

```text
"Я говорю: 'Серебряный волк'"
```

may establish exact fictional wording when accepted as such.

But:

```text
"Я рассказываю стражнику всё про нападение"
```

establishes communication meaning without establishing an exact fictional quote.

## LAW 5.11-24 — GIST IS NOT BACKFILLED INTO VERBATIM FICTION

Narrator/Chronicler may present a paraphrase but may not later treat generated wording as the exact words spoken unless a separate accepted exact-utterance owner/evidence exists.

---

# 23. Knowledge, claim and disclosure separation

Example:

```text
Transcript/source establishes:
NPC said "The king is dead"
```

This does not automatically establish:

```text
the king is dead
listener believed it
every PC heard it
every human player was exposed to it
```

Current fictional epistemic state remains `world.knowledge`.

Human-player material exposure remains `runtime.disclosure` under Step 4/5.12.

Objective truth remains with world/lore/current owners.

SemanticEvent/LOG retains material history/claim meaning.

## LAW 5.11-25 — PROVENANCE MAY OUTLIVE PROSE

A canonical owner may retain a stable message/interaction source ref after exact payload compaction only when the surviving proposition/semantic evidence is independently sufficient for that owner's contract.

---

# 24. Multiplayer visibility

Retention may keep speaker/source/channel/audience provenance needed for routing or history.

It does not independently decide:

- which fictional subjects perceived the communication;
- which human players were materially disclosed a hidden fact;
- fictional order across independent scenes.

Those remain with knowledge/disclosure/chronology/live owners.

Private/subset-visible Transcript records must preserve availability/source refs sufficient to prevent Commentator/Story retrieval from widening visibility merely because the text is stored.

---

# 25. OOC / safety / personal information

Baseline S intentionally minimizes durable exact OOC retention.

Active campaign preferences, boundaries, safety settings, authorization and configuration belong to their proper persistent owners.

Ordinary rules discussion, incidental personal disclosure and meta chatter do not become permanent exact campaign archive by default.

If exact OOC wording is itself required by an admitted audit/policy contract, that contract may protect the minimum necessary exact representation.

## LAW 5.11-26 — TRANSCRIPT IS NOT THE SOLE OWNER OF ACTIVE META POLICY

Deleting/compacting old conversation text must not erase active safety/preferences/configuration semantics that belong elsewhere.

---

# 26. Maintenance selection versus semantic eligibility

Age, session count, storage pressure or maintenance windows may choose **which already-eligible records to compact first**.

They do not make a protected record safe merely because it is old.

Thus implementation may optimize:

```text
old + unprotected + semantically discharged first
```

without introducing a semantic TTL law.

---

# 27. Compaction transaction and crash consistency

Compaction obeys Step 5.6 campaign publication semantics.

Safe direction favors temporary redundancy over premature irreversible loss.

### Exact canonical-owner promotion

A coherent transaction may establish:

```text
new canonical exact owner content
+ required provenance/dependency updates
+ exact protection release
+ source payload compaction
```

when all paths belong to the same validated campaign publication closure.

### Story archive required

Prefer:

```text
verified Transcript + compatible Story coverage durable
    before
raw source payload compaction
```

A later compaction transaction can then drop the source payload.

If CAS/acknowledgement is ambiguous, resolve current authoritative state under Step 5.6. Do not assume deletion succeeded.

## LAW 5.11-27 — FAILURE BIASES TOWARD EXTRA RETENTION

When replacement evidence durability is uncertain, preserve/retry from surviving exact source rather than deleting first.

---

# 28. Recovery behavior

Gameplay cold recovery does not require arbitrary old exact Transcript payload.

It requires exact historical text only when a still-live accepted consumer depends on it.

Otherwise current owners + SemanticEvents/history + compact provenance are sufficient according to their contracts.

Historical exact-text query outcomes include:

```text
EXACT_AVAILABLE
    return verified exact content

SEMANTIC_ONLY
    exact wording no longer retained;
    return lawful semantic summary/evidence

NOT_ESTABLISHED
    surviving evidence is insufficient even for the requested historical proposition
```

Exact names are implementation detail; semantic distinction is normative.

---

# 29. Integrity

Examples requiring targeted integrity/repair analysis:

```text
protected exact dependency points only to COMPACTED source
semantic consumer lost the proposition meaning it promised to retain
MUST_MATERIALIZE source compacted before required Transcript existed
Transcript claims exact archival status but digest/source slice disagrees
message envelope lost enumeration identity required by active Story coverage
live-born message ID collides/was renumbered across absorption
host-edited prose is mistaken for mutation of accepted runtime.message
compact message provenance points to mismatched Interaction identity
```

Lawful loss of optional unprotected verbatim text is not corruption.

---

# 30. Legacy migration

Legacy campaigns may have no durable message records or Transcript and may already have lost exact wording.

Migration law:

> **Never invent exact historical text that was not durably retained.**

If SemanticEvents/current state survive but exact wording does not, migration records the semantic continuity and treats exact historical text as unavailable.

Old host text may be imported only when an authorized migration can establish trustworthy mapping to accepted historical interactions. Similar wording is not sufficient identity proof.

---

# 31. Performance and token contract

Ordinary gameplay cost remains independent of campaign age.

Normal turns require no:

- history scan;
- Transcript catch-up;
- compaction pass;
- LLM importance classification for mundane messages;
- repository-wide dependency scan;
- loading of retained old transcripts merely because they exist.

The architecture preserves four separate states:

```text
physically retained
indexed/discoverable
eligible for this role
loaded into this invocation
```

Storage retention does not imply token/context cost.

Maintenance and Story catch-up operate over bounded typed source/index windows.

---

# 32. Step-5.12 handoff

Step 5.12 must define:

- the exact host emission/delivery qualification edge for Narrator/player-facing output;
- duplicate/retry delivery handling;
- when outbound `runtime.message` evidence becomes established;
- how `runtime.disclosure` advances coherently with actual emission semantics;
- how host retry/regeneration after emission is distinguished from uncommitted generation.

Step 5.11 supplies the retention representation and nonauthority laws but does not pre-decide that host protocol.

---

# 33. Step-5.13 handoff

Step 5.13 owns physical deletion of compact message envelopes and other orphan/garbage artifacts.

Before physical envelope deletion it must preserve or migrate:

- any remaining provenance dependencies;
- Step-5.10 source cursor/enumeration continuity;
- required historical/source identity anchors;
- integrity/audit obligations;
- any policy-required retained Story relationship.

Step 5.13 must not invent a second retention semantics layer that overrides Step 5.11 eligibility.

---

# 34. Step-6 carry-forward

Step 6 must reverify physical host feasibility, including:

- whether stable host invocation/message/revision IDs are exposed;
- whether retry/edit lineage is machine-visible;
- how one accepted host invocation maps idempotently to `runtime.interaction` / `runtime.message`;
- branch/retry behavior in ordinary ChatGPT product topology;
- voice/text host representation details;
- role-context isolation and physical LLM call topology.

Absence of richer host IDs cannot change Step-5.11 semantic ownership after HDM acceptance.

---

# 35. Machine-realization debt

Later implementation planning must cover at least:

1. `runtime.message` schema/paths;
2. interaction/message publication closure;
3. accepted-text normalization/exactness contract;
4. whole/slice exact-text references;
5. cryptographic content/slice digest rules;
6. `EXACT_RETAINED -> COMPACTED` state transition;
7. compact provenance envelope;
8. semantic-content discharge validation;
9. typed exact dependency declaration by admitted owner kinds;
10. durable bounded reverse protection routing/index;
11. canonical-owner promotion for contracts/documents/puzzles/mechanics;
12. Story/Transcript source contract under Selective Exact;
13. `MAY_OMIT` and typed `MUST_MATERIALIZE` archival rules;
14. deterministic Transcript exact certification/revocation;
15. source-enumeration/cursor continuity through compaction;
16. Step-5.8-compatible live message IDs/routing;
17. host edit/retry/branch divergence hooks;
18. OOC/private/safety minimization policy;
19. multiplayer provenance/availability integration;
20. exact-unavailable historical query semantics;
21. legacy migration statuses;
22. Step-5.12 outbound qualification integration;
23. Step-5.13 envelope GC integration;
24. compaction CAS/ambiguous-ACK handling;
25. integrity/repair tooling;
26. bounded maintenance/performance tests.

The current legacy `runtime.message` campaign-sequential allocator policy is explicitly debt where independent live-source allocation requires Step-5.8-safe identity.

No broad implementation begins before the architecture sequence reaches its normal planning gate.

---

# 36. Required regression/adversarial realization cases

Later tests must include at least:

```text
ordinary flavor dialogue may lose exact text without semantic corruption
mundane action prose compacts after command/intent semantics survive
Wish-like wording remains exact while mechanics requires it
mixed IC/OOC message protects only minimal exact slice
contract exact terms promote before source compaction
password/passphrase survives in proper owner
riddle/inscription exact text survives in proper world owner
player-authored letter survives as canonical document
NPC false claim remains claim/history without becoming truth
knowledge provenance retains proposition meaning after message compaction
pre-acceptance correction does not create false durable history
post-acceptance correction creates new history rather than rewriting old
old user host message edit cannot retcon canon
assistant retry cannot replay established mechanics
old-point branch recovers current campaign authority
original chat deletion does not break gameplay recovery
voice exactness is transcript-relative, not acoustic
private whisper storage does not widen knowledge/disclosure/Story visibility
independent live messages use collision-safe source-native IDs
live close/absorption preserves message identity
host order never becomes fictional chronology
unemitted Narrator draft creates no outbound historical occurrence
MAY_OMIT candidate remains enumerable after source payload compaction
MUST_MATERIALIZE blocks exact payload compaction
verified Transcript + compact source supports exact historical quote
Transcript material edit revokes exact status when digest mismatches
Story loss after raw source compaction harms history quality, not canon
hash-only survivor cannot reconstruct prose
semantic-discharge failure blocks compaction
stale protection index cannot authorize deletion
compaction CAS loss retains safe old exact state
ambiguous compaction ACK uses Step-5.6 verification
legacy semantic history with no transcript does not invent quotes
100k-message campaign does no ordinary-turn history scan
retained history is not automatically loaded into LLM context
```

---

# 37. Canonical closure

Step 5.11 architecture is closed with this final statement:

> **HDM preserves stable accepted communication identity and materially established semantic history without promising permanent verbatim recording of all conversation. Exact accepted text remains only while a typed consumer requires it or a deliberate archival policy retains it. Before source payload compaction, correctness-critical exact semantics move to their natural canonical owners and every surviving semantic consumer becomes independently content-sufficient. `STORY/TRANSCRIPT` may preserve verified exact historical text without becoming gameplay authority. Host chat edits/retries/branches cannot rewrite accepted campaign history, and lawful loss of optional exact wording is reported explicitly rather than reconstructed.**

No material owner decision remains open in Step 5.11.

Next architecture slice after roadmap/status verification:

**Step 5.12 / Host Delivery & Disclosure Boundary.**
