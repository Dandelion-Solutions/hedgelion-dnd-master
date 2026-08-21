# Step 5.11 — Transcript / History Retention & Compaction — Candidate Specification

Status: **NONCANONICAL CANDIDATE — OWNER DIRECTION FIXED; ADVERSARIAL REVIEW REQUIRED**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Owner-approved product direction:

> **S — SELECTIVE EXACT / SEMANTIC CONTINUITY**

Candidate architecture direction:

> **STABLE MESSAGE EVIDENCE / SELECTIVE EXACT PROTECTION / SEMANTIC OWNER PROMOTION / PAYLOAD COMPACTION / OPTIONAL VERIFIED TRANSCRIPT ARCHIVE**

This candidate formalizes the Step-5.11 owner decision. It does not decide Step-5.12 host-delivery acknowledgement, Step-5.13 generic physical GC, or Step-6 physical host/message identity feasibility.

---

# 1. Central invariant

HDM distinguishes durable memory from permanent verbatim recording.

```text
accepted communication identity
    may survive indefinitely

material semantic consequences/history
    survive in their proper owners

exact accepted text
    survives only while protected
    or deliberately archived
```

Loss of unprotected exact prose is lawful. Loss of materially established semantic campaign history is not.

If exact text is unavailable, HDM reports that limitation and uses surviving semantic evidence. It never fabricates a likely quotation.

---

# 2. Authority geometry

```text
HOST CHAT ITEM
    mutable product presentation/context
        |
        v
ACCEPTED HDM INTERACTION
    runtime.interaction
        |
        v
RUNTIME MESSAGE EVIDENCE
    runtime.message
    stable accepted communication identity
    exact payload while retained
    compact provenance after payload compaction
        |
        +------------------------------+
        |                              |
        v                              v
CANONICAL SEMANTIC OWNERS          STORY/TRANSCRIPT
world/runtime state               optional exact archival projection
SemanticEvent / LOG               non-canonical
MechanicalEvent / receipt         presentation/history fidelity
knowledge / disclosure            never gameplay truth authority
contract / document / clue owner
```

`runtime.message` is historical/interaction evidence. It does not become objective world truth merely because it records accepted words.

---

# 3. `runtime.message` responsibility

Step 3 already admits `runtime.message` and `runtime.interaction`.

This candidate assigns `runtime.message` the narrow responsibility:

> one stable HDM-owned identity for one accepted participant communication representation relevant to campaign interaction/history.

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
    exact_text?                present only when retained
    content_digest
    compact provenance metadata
    source-domain enumeration identity/token
    semantic/history refs as needed
    delivery evidence ref?     outbound, Step-5.12 qualified
```

Exact machine fields are implementation planning work.

## LAW 5.11-1 — STABLE MESSAGE IDENTITY DOES NOT DEPEND ON VISIBLE CHAT MUTABILITY

After an HDM communication has been accepted under an Interaction identity, later host edit/retry/branch/delete operations do not rewrite that `runtime.message` identity or its accepted meaning.

## LAW 5.11-2 — MESSAGE EVIDENCE IS NOT WORLD TRUTH

A retained statement proves only the accepted/delivered communication occurrence supported by its provenance.

It does not independently prove:

- truth of the statement;
- listener belief;
- PC/NPC knowledge;
- player disclosure to every participant;
- fictional chronology.

Those remain with their canonical owners.

---

# 4. What “exact text” means

Baseline exactness is **text-exact relative to the textual representation accepted by HDM**.

For ordinary text input this means the exact Unicode/text content admitted into the runtime interaction boundary, preserving semantically visible textual content and formatting required by the host representation.

It does not promise byte identity with undocumented UI/HTTP payloads.

For voice-mode input, exactness is relative to the accepted transcript text supplied to HDM, not to original acoustic speech. If product voice transcription differs from spoken audio, HDM does not claim a verbatim audio record.

Attachments/media are represented through stable admitted references/derived campaign objects as their owning semantics require. Step 5.11 does not require permanent binary archival merely because a host message referenced media.

## LAW 5.11-3 — NO VERBATIM CLAIM BEYOND RETAINED REPRESENTATION

HDM may say “exact wording” only when the relevant retained representation establishes it.

A summary, SemanticEvent, hash alone, model memory or reconstructed prose cannot be presented as a verbatim quotation.

---

# 5. Admission boundary

Not every host-visible token becomes durable `runtime.message` history.

Eligible admitted communications include participant inputs or player-facing outputs that become relevant to a durable Interaction/history/source contract.

Candidate-negative material includes:

- hidden chain-of-thought;
- internal prompts/developer instructions;
- private tool traces;
- private Dramaturg/Actor reasoning;
- generated but never emitted narration;
- repository transport diagnostics;
- other non-participant internal plumbing.

Ordinary OOC chatter with no durable campaign effect need not become durable exact message history merely because it exists in the host chat.

If an OOC statement changes durable campaign configuration, preferences, boundaries, authorization or another proper owner, that owner persists the active semantics. Exact OOC prose remains separately protected only when a concrete contract requires it.

## LAW 5.11-4 — HOST VISIBILITY ALONE DOES NOT CREATE DURABLE HISTORY

Visible ChatGPT history is neither the admission rule nor the durable authority for HDM historical evidence.

---

# 6. Initial exact payload lifetime

During interpretation/adjudication, the accepted textual payload may exist in current execution/HOT state before any campaign publication.

When an Interaction or resulting canonical/history state becomes durable, the publication closure must include enough message/interaction evidence to support every retained dependency of that durable result.

A message may therefore first become durable as either:

```text
EXACT_RETAINED
```

or, if no exact-text obligation remains and no archival transfer is required:

```text
COMPACTED
```

provided semantic/provenance continuity is already sufficient.

There is no rule requiring one repository write merely because one conversational message arrived.

## LAW 5.11-5 — DURABILITY FOLLOWS SEMANTIC EDGES, NOT MESSAGE ARRIVAL

Step-5.5 durability edges remain authoritative. Step 5.11 does not create per-message save/publication boundaries.

---

# 7. Exact-text protection

Exact payload is protected when at least one live/promised consumer requires exact form rather than only semantic meaning.

Conceptually:

```text
EXACT_TEXT_PROTECTED(message_id)
    iff an admitted current/prospective consumer
    requires exact accepted text
    and no independent sufficient exact owner has discharged that dependency
```

Protection authority belongs to the consuming semantic owner/contract, not to Chronicler importance judgment.

Examples:

- unresolved wording-dependent adjudication;
- contract/oath exact terms before promotion into canonical contract/document state;
- password/passphrase while the exact token itself remains a required game object;
- riddle/inscription/code before or while the exact text remains the puzzle evidence;
- player-authored document before canonical document text exists;
- explicit durable exact-quote dependency.

## LAW 5.11-6 — EXACT PROTECTION IS OWNER-DECLARED AND TYPED

A consumer that requires exact text must expose a typed stable dependency on the source exact representation or independently own an exact semantic copy.

Natural-language importance alone is not a protection contract.

## LAW 5.11-7 — COMPACTION CANNOT DROP THE LAST REQUIRED EXACT REPRESENTATION

If any live/promised correctness consumer still requires exact wording, raw message payload cannot be compacted unless that consumer is atomically/safely rebound to another canonical exact owner whose semantics are sufficient.

---

# 8. Semantic owner promotion

Whenever exact wording becomes part of a durable game object, prefer moving that semantic responsibility to the natural canonical owner rather than keeping an arbitrary chat message forever.

Examples:

```text
contract terms
    -> world.contract

player-authored in-fiction letter
    -> world.asset/document content owner

inscription/riddle text established as world object
    -> applicable world asset/location/lore owner

wording-dependent persistent mechanic
    -> command/effect/contract/event owner required by that mechanic
```

The historical `runtime.message` may continue to prove provenance, but it need not remain the sole holder of the text.

## LAW 5.11-8 — EXACT SEMANTICS FOLLOW THEIR NATURAL OWNER

Do not preserve exact chat indefinitely merely because a proper canonical owner has not been modeled. If exact content is an enduring semantic property of an established world/runtime object, that owner must carry the necessary exact content or stable exact evidence dependency.

---

# 9. Bounded protection discovery

Compaction may not scan the whole campaign looking for possible textual dependencies.

Protection-bearing owner kinds must expose typed dependency routing.

Implementation may use a rebuildable reverse protection index conceptually equivalent to:

```text
message_id -> exact-text consumer refs
```

The index is routing/derivative evidence, not semantic authority. Forward consumer dependencies remain authoritative.

Creating/releasing a durable exact dependency must update the required bounded routing in the same coherent publication closure where correctness requires it.

## LAW 5.11-9 — NO CAMPAIGN-WIDE REFERENCE COUNT

Step 5.11 does not introduce a generic universal reference-counting GC subsystem.

Only admitted exact-text dependency classes participate in exact protection routing.

---

# 10. Payload compaction

Message payload compaction is a semantic retention transition, not generic physical GC.

Baseline transition:

```text
RuntimeMessage(EXACT_RETAINED)
    exact_text
    digest
    provenance
    refs

        |
        | only when exact payload is not protected
        v

RuntimeMessage(COMPACTED)
    no exact_text
    digest
    stable message/interaction identity
    participant/channel/provenance metadata
    source-enumeration continuity
    semantic/history refs needed by retained consumers
```

The compact envelope remains an HDM historical source identity.

Physical deletion of the envelope itself belongs to Step 5.13.

## LAW 5.11-10 — COMPACTION IS MONOTONIC LOSS OF VERBATIM CAPABILITY

Once exact payload is lawfully removed and no exact archive/canonical copy exists, HDM must treat verbatim form as unavailable.

Later LLM reconstruction cannot restore exact-history status.

## LAW 5.11-11 — HASH IS VERIFICATION EVIDENCE, NOT TEXT STORAGE

A digest may verify that a retained candidate copy matches the historical payload when that candidate text exists.

Digest alone cannot reconstruct deleted prose and cannot satisfy an exact-text consumer requiring the actual content.

---

# 11. `STORY/TRANSCRIPT` under Selective Exact

`STORY/TRANSCRIPT` remains a durable noncanonical historical/presentation projection.

It may preserve exact accepted/delivered text even after the raw `runtime.message` payload is compacted.

Baseline candidate disposition for ordinary Transcript projection may be `MAY_OMIT`.

A typed archival policy/request may promote a source candidate to:

```text
MUST_MATERIALIZE before exact source payload compaction
```

No unrelated Story layer must catch up.

## LAW 5.11-12 — STORY ARCHIVE DOES NOT BECOME GAMEPLAY AUTHORITY

A Transcript copy may preserve historical exact text but cannot satisfy a correctness-critical gameplay exact-text dependency unless a canonical owner separately carries/validates the required semantics.

## LAW 5.11-13 — VERIFIED ARCHIVAL COPY MAY SURVIVE RAW PAYLOAD LOSS

When compact `runtime.message` provenance retains a content digest/identity and `STORY/TRANSCRIPT` retains matching exact text with compatible source refs, HDM may treat Transcript as the retained exact historical/presentation copy of that communication.

This establishes archival fidelity, not objective truth of the uttered claim.

---

# 12. Story catch-up after source compaction

A compact message envelope remains visible to the Step-5.10 source-domain contract even if exact payload is gone.

For a `MAY_OMIT` candidate whose exact payload was lawfully compacted before Transcript materialization, Chronicler may terminally omit it and advance compatible coverage.

For a `MUST_MATERIALIZE` candidate, exact payload compaction is blocked until the required Transcript output is durably published or the archival requirement is lawfully revoked.

## LAW 5.11-14 — COMPACTION CANNOT STRAND STORY COVERAGE

Compaction must preserve source-domain identity/enumeration semantics needed for Step-5.10 coverage to remain interpretable and catch-up to continue without an all-history scan.

---

# 13. Source enumeration

`runtime.message` may provide an owner-local append-monotonic projection enumeration domain.

The exact token may be a declared message sequence/ID component or another domain-native cursor. Its meaning is only:

> projection/history enumeration order within this source domain.

It is not fictional chronology, causal order or universal campaign order.

Compacting payload does not remove the enumeration position.

Any future physical deletion of message envelopes must preserve/migrate cursor continuity under Steps 5.10/5.13.

---

# 14. Host edit semantics

## User edit before HDM acceptance

Only the representation actually accepted by the runtime becomes the relevant Interaction/message evidence. Unaccepted draft text need not become campaign history.

## User edit after HDM acceptance

The visible host edit does not mutate established `runtime.message`, Interaction, commands, SemanticEvents or world state.

To change campaign semantics, the user must generate a new accepted interaction/correction under ordinary rules.

## LAW 5.11-15 — HOST EDIT IS NOT RETCON

Changing product conversation text after acceptance cannot silently rewrite durable campaign history.

---

# 15. Retry/regeneration and branch semantics

Assistant retry/regeneration of an older visible answer cannot rerun or replace established gameplay merely because the host shows different prose.

A new chat branched from an old conversational point must recover/reconcile against current campaign authority. Old branch context is non-authoritative evidence at best.

Host chat deletion does not delete campaign storage.

Stable host retry/revision identity availability is a Step-6 deployment feasibility concern; Step 5.11 relies only on HDM-owned accepted Interaction/message identities after acceptance.

## LAW 5.11-16 — CURRENT CAMPAIGN AUTHORITY BEATS HOST BRANCH POSITION

No host conversation branch cursor becomes campaign recovery authority.

---

# 16. Correction and retraction

Distinguish:

```text
pre-acceptance clarification
    -> accepted final representation only

post-acceptance player correction
    -> new Interaction/message evidence
    -> may cause lawful new semantic transition/reversal

editorial Story correction
    -> presentation/history edit only

host UI edit
    -> no automatic campaign semantic change
```

Accepted old historical evidence is not silently rewritten in place.

If a correction changes the meaning of a durable canonical object, the owning object's correction/supersession/transition contract applies.

---

# 17. In-fiction speech versus action gist

Player messages may contain exact quoted speech, summarized speech intent, action declaration and OOC material together.

The Interpreter may establish semantic speech/action meaning, but Step 5.11 does not pretend a gist is an exact fictional quotation.

Example:

```text
player: "Я рассказываю стражнику всё про нападение"
```

may establish a communication act/knowledge transfer without establishing exact fictional wording.

Conversely:

```text
player: "Я говорю: 'Серебряный волк'"
```

may establish exact fictional text when the interaction/adjudication treats those words as the actual utterance.

Any durable exact fictional utterance requirement must be represented explicitly rather than inferred later from narrative prose.

---

# 18. Claims, knowledge and disclosure after compaction

Payload compaction does not alter canonical knowledge/disclosure/current-state relations.

If an NPC statement caused a knowledge transition, the current stance remains with `world.knowledge` and historical change with SemanticEvent/provenance as required.

If a human player was materially exposed to a fact, `runtime.disclosure` remains the authority under Step 4/5.12.

A compact message envelope may remain a provenance source, but it does not become current epistemic authority.

## LAW 5.11-17 — PROVENANCE MAY OUTLIVE PROSE

A semantic owner may retain a stable source message/interaction ref after exact source text is compacted, provided the surviving evidence remains sufficient for that owner's contract.

If the owner requires the actual text, the payload remains protected or exact semantics move to an appropriate canonical owner.

---

# 19. Multiplayer visibility

Message retention metadata may record participant/source/channel identity needed for provenance and routing.

It must not independently decide:

- which fictional characters heard/understood the speech;
- which human players were actually disclosed a hidden fact;
- fictional temporal order among concurrent scenes.

Those remain with world knowledge, runtime disclosure, chronology and live-scene owners.

Host/conversational ordering can be preserved for reconstruction without becoming fictional chronology.

Private whispers and subset-visible communication require source/delivery/availability refs sufficient for Story access filtering, but Transcript storage does not itself broaden audience eligibility.

---

# 20. OOC / meta / safety material

Baseline S intentionally minimizes durable exact OOC retention.

Active campaign preferences, boundaries, safety policy, permissions and configuration belong to their proper durable owners.

Ordinary rules questions, incidental personal disclosures and meta chatter do not become permanent exact campaign archive by default.

When OOC wording is itself materially required for a durable policy/audit contract, that specific owner may protect exact evidence.

This preserves semantic continuity without turning the campaign repository into a general archive of personal conversation.

---

# 21. Maintenance scheduling is not retention authority

Age, session count, repository size or maintenance opportunity may be used to **select already-eligible records for compaction work**.

They do not make a protected message eligible merely because it is old.

Thus a maintenance implementation may prefer:

```text
old + unprotected first
```

without defining:

```text
older than N days => safe to delete
```

as semantic law.

---

# 22. Crash consistency

Compaction uses Step-5.6 coherent campaign publication.

Safe preferred direction is redundancy before irreversible loss.

Examples:

### Transcript archive required

```text
publish verified Transcript + compatible Story coverage
    BEFORE / coherently with
allowing exact source payload to become unprotected
```

A separate later compaction transaction may then remove raw exact payload.

### Canonical semantic owner promotion

```text
publish exact canonical owner content/ref
+ update/release exact dependency
+ compact source payload
```

may occur in one coherent transaction when all affected paths share the campaign publication domain and resulting closure is validated.

If a CAS/conflict/ambiguous ACK leaves uncertainty, do not assume irreversible deletion succeeded. Resolve current authoritative state under Step 5.6.

## LAW 5.11-18 — FAILURE BIASES TOWARD EXTRA COPIES

When uncertain whether replacement evidence is durably established, retain/retry from surviving exact source rather than deleting first.

---

# 23. Recovery

Gameplay cold recovery does not require old exact transcript payload.

Recovery requires exact message content only when a live accepted consumer still depends on it.

Otherwise compact message provenance/semantic history is sufficient according to the owning contracts.

If a fresh runtime receives a historical query for text that is no longer retained, the correct result is an explicit exact-text-unavailable outcome plus the strongest permissible semantic summary/evidence.

No host memory is consulted as hidden campaign authority.

---

# 24. Integrity states

Examples of Step-5.11 integrity problems:

```text
protected exact dependency points to COMPACTED source with no sufficient canonical exact owner
MUST_MATERIALIZE source was compacted before required Transcript existed
Transcript claims exact archival match but digest/source identity disagrees
message envelope lost source-enumeration identity needed by live Story coverage
host-edited text is mistaken for mutation of accepted runtime.message
compact provenance points to impossible/mismatched Interaction identity
```

If only optional historical exactness was lawfully lost, that is not corruption.

---

# 25. Legacy migration

Older campaigns may have:

- no `runtime.message` records;
- no Transcript;
- surviving SemanticEvents only;
- host chats that may or may not still exist.

Migration must never invent exact historical text.

Legacy state may explicitly represent:

```text
exact historical wording unavailable
semantic evidence available
```

If old host text is still accessible during an authorized migration, it may be imported only under a trustworthy mapping to accepted historical interactions. Mere textual similarity is insufficient to fabricate stable historical identity.

---

# 26. Performance contract

Ordinary gameplay must remain independent of campaign age.

Normal turn requirements do not include:

- scanning historical messages;
- Story catch-up;
- compaction;
- transcript classification LLM calls;
- repository-wide exact dependency discovery.

Exact protection is established from the current accepted operation and bounded typed owner dependencies.

Compaction runs only at maintenance opportunities and over bounded candidate windows/index routes.

Long-term retained storage does not imply long-term prompt growth.

---

# 27. Machine-realization debt

Later implementation planning must cover at least:

1. `runtime.message` schema and physical routing;
2. interaction/message durability closure integration;
3. accepted-text normalization/exactness rules;
4. inbound/outbound representation kinds;
5. payload-state transition `EXACT_RETAINED -> COMPACTED`;
6. stable content digest rules;
7. compact provenance envelope fields;
8. typed exact-text dependency declarations by admitted owner kinds;
9. bounded reverse protection routing/index;
10. natural-owner promotion for contracts/documents/puzzles/mechanics;
11. Story/Transcript source contract under Selective Exact;
12. `MAY_OMIT` / typed `MUST_MATERIALIZE` archival selection;
13. digest/source verification for retained Transcript copy;
14. source enumeration/cursor continuity through payload compaction;
15. host-edit/retry/branch divergence handling hooks;
16. OOC/private/safety retention policy realization;
17. multiplayer visibility/provenance refs without duplicate disclosure authority;
18. exact-text-unavailable query/result semantics;
19. legacy migration/unknown exact-history status;
20. Step-5.12 outbound qualification integration;
21. Step-5.13 envelope GC integration;
22. compaction conflict/ambiguous-ACK handling;
23. integrity/repair tooling;
24. bounded maintenance indexes and performance tests.

No broad runtime implementation begins before the architecture sequence reaches its normal planning gate.

---

# 28. Candidate adversarial cases

The adversarial review must test at least:

```text
ordinary mundane action message compacts without semantic memory loss
flavor dialogue loses exact text lawfully
Wish-like wording remains exact through adjudication
long-lived contract terms move to contract owner before message compaction
password remains usable after source message compaction through proper owner
riddle exact wording moves to puzzle/world owner
player-authored letter becomes durable document
NPC lie retains semantic occurrence but optional exact quote disappears
Transcript exact archive + compact envelope verify historical quote
Transcript edited after raw source deletion
Transcript corrupted after raw source deletion
hash survives with no text
host user edits old accepted message
assistant old response is retried after canon advanced
new chat branches from old point
original chat deleted
pre-acceptance correction
post-acceptance correction
mixed IC/OOC player message
summarized speech with no exact fictional words
private whisper
multiplayer subset visibility
host order differs from fictional chronology
Story lags until exact payload already compacted for MAY_OMIT candidate
MUST_MATERIALIZE blocks compaction
Story coverage survives compact envelope
compaction CAS loses to gameplay
ambiguous compaction ACK
crash after archive copy before raw compaction
crash after canonical owner promotion before later cleanup
legacy campaign with SemanticEvent but no transcript
100k-message campaign compacts boundedly without ordinary-turn scan
```

---

# 29. Candidate decision summary

The architecture deliberately separates four persistence outcomes:

```text
1. EXACT REQUIRED FOR GAMEPLAY/CANON
   -> retain runtime exact payload or move exact semantics to canonical owner

2. EXACT DELIBERATELY ARCHIVED FOR HISTORY
   -> optional verified STORY/TRANSCRIPT copy may survive source payload compaction

3. ONLY SEMANTIC HISTORY REQUIRED
   -> compact runtime.message envelope + proper semantic owners

4. NO DURABLE HISTORICAL REQUIREMENT
   -> later physical cleanup may remove eligible evidence under Step 5.13
```

This is the concrete implementation of the owner-approved principle:

> **The Master remembers established meaning extremely well; verbatim recording is selective rather than universal.**

Candidate remains noncanonical until adversarial review and resolution gate complete.
