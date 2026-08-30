# Step 5.11 — Transcript / History Retention & Compaction — Research Draft

Status: **NONCANONICAL RESEARCH — NO RETENTION PROMISE DECIDED**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Governing task brief:

- `DEV/docs/superpowers/design/2026-08-21-step-5-11-transcript-history-retention-compaction-task-brief.md`

This artifact is research input for Step 5.11. It does not authorize implementation, does not settle the product-level historical-fidelity promise, and does not pre-decide Step 5.12 host delivery or Step 5.13 physical GC.

---

# 1. Executive research result

The repository and platform evidence strongly reject both extremes:

1. **ChatGPT visible chat history as the durable transcript authority** is unsafe because host history is mutable/deletable and is not an HDM-owned immutable evidence store.
2. **Permanent exact archival of every host-visible message** is not required by existing HDM semantics and would create avoidable storage/privacy/file-count obligations.

The strongest current direction is a selective hybrid:

> **Stable HDM-owned `runtime.message` / `runtime.interaction` historical identity + exact payload retained only while a typed correctness or explicitly promised archival consumer requires it + promotion of gameplay-significant exact text into the natural semantic owner + optional/selective `STORY/TRANSCRIPT` exact archival + compact provenance envelope after payload compaction.**

This direction preserves Step-3 interaction identity, Step-4 truth/knowledge/disclosure separation, Step-5.10 Story projection, and the project principle of necessary-and-sufficient persistence.

A material owner-level decision likely remains: **what exact-history fidelity HDM promises by default when no gameplay correctness dependency requires exact wording.**

---

# 2. Verified repository facts

## FACT R1 — `runtime.interaction` already owns accepted external exchange identity

Step 3 canonically defines one `runtime.interaction` as one accepted external exchange/invocation identity and raw message linkage.

It requires/reference concepts including:

```text
stable host invocation identity
raw input message reference
authenticated player/session/campaign context
resulting IntentPlan
response linkage when retained
```

Same prose in a later intentional turn is a new Interaction; transport retry of the same invocation is supposed to reuse Interaction identity.

Consequence: Step 5.11 should not create a parallel `AcceptedUtterance` identity when existing `runtime.message` / `runtime.interaction` can own the needed historical edge.

## FACT R2 — `runtime.message` is admitted but structurally unfinished

Current machine catalog admits:

```text
runtime.message
runtime.interaction
```

Current identifier policy already gives:

```text
runtime.message      campaign-scoped sequential stable ID
runtime.interaction  campaign-scoped sequential stable ID
```

However current DEV schemas contain no `runtime.message` or `runtime.interaction` schema and current entity-structure machine inventory does not yet define runtime-record structures.

Consequence: 5.11 has room to define narrow historical semantics without migrating an already entrenched message payload model.

## FACT R3 — current shipped schema has no transcript store

`GAME/SCHEMA/README.md` says historical details belong in LOG and lists no persistent transcript/message schema.

The current campaign template also predates the Step-4 `STORY/` realization.

Consequence: current runtime has no competing durable full-transcript authority that must be preserved.

## FACT R4 — current session semantics deliberately do not rely on old chat history

`GAME/CORE/SESSION.md` explicitly says session startup should not begin by rereading old chat history.

Its maintenance-continuation rule says:

```text
if exact previous utterance is still in current chat context:
    it may be repeated accurately
else:
    use durable semantic evidence
    summarize meaning
    never fabricate an exact quote
```

It also states session journals are compact operational/semantic history, not transcripts.

Consequence: baseline HDM currently does **not** promise arbitrary durable exact recall of every old line.

## FACT R5 — dialogue semantics already favor semantic consequence over permanent line archival

`GAME/CORE/DIALOGUE.md` says to persist socially consequential dialogue facts such as promises, threats, lies, agreements and durable commitments, and explicitly says not to archive every line of casual speech into permanent state.

This concerns canonical/current persistence, not necessarily optional Story archival, but it is strong evidence against treating every utterance as correctness-critical forever.

## FACT R6 — Step 4 separates utterance evidence from truth

Step 4 states:

```text
transcript statement proves that statement was said/exposed
NOT that its claim is objectively true
```

Transcript/SemanticEvent provenance may explain why knowledge/disclosure changed without owning current epistemic state.

## FACT R7 — Step 4 intentionally allows Story to become the last exact-text copy

Step 4 says Story is durable but noncanonical and may become the only retained copy of exact dialogue/editorial prose after raw-message compaction.

Loss of such Story harms historical/presentation fidelity but does not change canon.

`STORY/TRANSCRIPT` is defined as retained participant discourse useful for dialogue fidelity and reconstruction, with source/delivery references and no truth authority.

## FACT R8 — Step 5.10 leaves source retention explicitly to 5.11

Step 5.10 fixes:

```text
source_refs preserve provenance identity
full source payload retention is NOT automatically promised
Story source coverage/cursor must remain interpretable after compaction
source deletion may require typed Transcript materialization when 5.11 says so
```

This is a direct design handoff.

---

# 3. Verified current ChatGPT platform facts

Sources rechecked from current official OpenAI Help Center/release documentation on 2026-08-21.

## FACT P1 — earlier user messages are editable

Current ChatGPT allows users to edit earlier messages. Editing can establish a different visible conversation branch/context than the text originally acted upon.

## FACT P2 — assistant responses can be retried/regenerated

Current ChatGPT allows retry/regeneration of earlier assistant responses.

The visible host prose for an earlier point therefore cannot itself be assumed immutable campaign history.

## FACT P3 — conversations can branch from an earlier message

`Branch in new chat` creates a separate conversation beginning from an earlier point.

A host branch created from stale conversational context therefore cannot imply an older campaign branch is current authority.

## FACT P4 — chats are user-deletable and deletion is not recoverable through normal product use

Chats remain in account history until deleted. Deleted chats disappear from visible history immediately and are scheduled for permanent deletion within the documented retention window, subject to legal/security exceptions. Product help states deleted chats cannot be recovered through normal UI/API/support flows.

Consequence: campaign correctness cannot depend on later host-chat availability.

## FACT P5 — Project memory is contextual assistance, not exact durable history

Projects are available across Free and paid ChatGPT plans. Project memory may reference other chats/files, subject to settings and plan behavior.

However current Memory documentation explicitly says chat-history memory does not remember every detail. Project memory is also user-controlled/configurable and is not an HDM-owned immutable evidence log.

Consequence: Project memory may improve convenience but cannot satisfy exact transcript/recovery requirements.

## FACT P6 — exact project-chat retrieval is a product UI capability, not an HDM runtime contract

Current ChatGPT exposes product search/opening of prior chats, but no official documentation establishes a runtime-programmable exact message-history interface available to ordinary HDM execution.

The current assistant/tool surface used for HDM development likewise does not expose stable ChatGPT message revision IDs or edit ancestry to the runtime.

Consequence: Step 5.11 must not rely on host message IDs/revision lineage unless Step 6 later proves a deployment-specific capability.

## FACT P7 — Voice transcripts are not verbatim

Current official ChatGPT Voice documentation says voice transcripts are not verbatim records and may differ from what participants actually said.

Current voice dictation is different: speech is transcribed to editable text before the user sends it as a message.

Consequence:

```text
baseline textual exactness can mean:
    exact text accepted by HDM runtime

it cannot generally mean:
    exact physical spoken audio words
```

without a separately retained/audio-qualified source contract.

---

# 4. Platform/repository tension exposed by research

Step 3 currently requires a stable host invocation identity for exact retry semantics, while ordinary ChatGPT product documentation does not expose a runtime-stable host message/revision identity suitable for that contract.

Content equality cannot replace host invocation identity because Step 3 deliberately says:

```text
same prose in later intentional turn = new Interaction
transport retry of same invocation = same Interaction
```

A content hash cannot distinguish those cases.

Disposition:

- this is a **Step-6 host/deployment feasibility carry-forward**;
- Step 5.11 shall define HDM-owned stable message/interaction identities and retention independently of the physical host identity primitive;
- Step 5.11 shall not claim that ordinary ChatGPT Retry deduplication is solved by text hashing.

This is not currently evidence that Step 3 must reopen; it is an implementation/deployment prerequisite already consistent with Step 6's role/host feasibility responsibilities.

---

# 5. Current-state concept inventory

| Concept | Semantic owner | Current physical representation | Stable ID? | Current retention promise | Key consumers / gap |
|---|---|---|---|---|---|
| accepted external exchange | `runtime.interaction` | canonical Step-3 concept; schema not realized | yes, policy exists | durable when required by execution/history closure | IntentPlan, commands, raw message linkage |
| raw participant message | `runtime.message` | admitted catalog concept; schema not realized | yes, policy exists | not yet specified | Interaction, Transcript, exact-word evidence |
| semantic history | `runtime.semantic_event` / LOG | current schema/runtime contract exists | yes | compact append-only semantic history | recovery, causality, knowledge provenance, Story EVENTS |
| mechanical history | `runtime.mechanical_event` / receipts | DEV architecture/schemas | yes | committed mechanical evidence as required | mechanics/audit/recovery |
| current fictional knowledge | `world.knowledge` | canonical Step-4 owner; realization debt | stable owner relation | current stance only + bounded provenance | Actor/Narrator/context |
| human disclosure | `runtime.disclosure` | canonical Step-4 owner; realization debt | conceptual stable relation | sparse only where future secrecy correctness matters | Context Assembler/Narrator |
| session continuity | runtime session + durable semantic sources | `SESSION.md` + session schema | yes session | semantic continuity; exact old quote not guaranteed | cold/new-chat orientation |
| visible host chat | ChatGPT product | external mutable host UI/history | host-controlled | user-controlled, editable/branchable/deletable | convenience only, unsafe as sole evidence |
| Story Transcript | `STORY/TRANSCRIPT` | canonical Step-4/5.10 concept; not implemented | layer-local Story IDs | retained discourse policy deferred to 5.11 | dialogue fidelity, Chronicler, Commentator |
| Story other layers | Story projections | canonical concept; not implemented | layer-local IDs | laggable/regenerable under 5.10 | presentation/history |

---

# 6. Exactness model — research recommendation

Do not promise byte/UI/render exactness the runtime cannot observe.

For ordinary typed/dictated text, the useful baseline exactness is:

> **ACCEPTED TEXT EXACTNESS — the exact Unicode textual payload presented to the HDM interaction boundary for that accepted message, plus typed speaker/direction/channel/interaction metadata.**

This does not claim:

- original HTTP bytes;
- exact UI rendering;
- pre-autocorrect text;
- text typed then edited before Send;
- exact physical spoken audio;
- attachment binary identity unless separately referenced/retained.

Possible content forms must remain distinguishable:

```text
VERBATIM_ACCEPTED_TEXT
    exact accepted text exists

EXTRACTED_VERBATIM_SPAN
    exact span from accepted message is identified as in-fiction utterance/document text

SEMANTIC_PARAPHRASE
    player described gist; no exact fictional wording was established

NONVERBATIM_VOICE_TRANSCRIPT
    host transcription exists but is not a verbatim-audio promise
```

The exact final vocabulary is candidate-spec work.

---

# 7. Important distinction: exact input text versus exact fictional utterance

A player's exact submitted message is not always an exact in-fiction quote.

Example:

```text
Player message:
    "I tell the guard that we need to enter and show him the writ."

accepted text is exact
fictional speech wording is NOT established exactly
```

Contrast:

```text
Player message:
    "I say: 'By order of the Queen, open this gate now.'"

accepted text is exact
quoted span may establish exact PC utterance if Interpreter accepts that reading
```

This prevents Transcript from fabricating precise dialogue where the player only supplied gist.

---

# 8. Exact-wording dependency analysis

A raw message should not remain permanently exact merely because some later consequence once referenced the interaction.

Instead distinguish:

```text
SOURCE EXACTNESS
    runtime.message currently contains exact accepted payload

SEMANTIC EXACTNESS OWNER
    exact wording has been promoted into the natural durable owner because wording itself matters

HISTORICAL ARCHIVE EXACTNESS
    Story/Transcript or another noncanonical archive retains an exact copy for fidelity
```

## Examples

### Wish-like wording

If adjudication depends on exact accepted wording, the accepted execution/semantic evidence must retain the material exact text or a stable exact-text owner/ref as part of the command's correctness closure.

A future raw-message compaction cannot remove the only exact evidence used by the adjudication.

### Contract/oath terms

Once exact terms become a canonical contract/commitment, promote the actual terms into `world.contract`, an in-fiction document Asset, lore proposition(s), or another proper semantic owner.

The raw message need not remain the sole authority forever.

### Password / riddle / inscription / code

If the exact string is a durable world fact or document content, establish it in the relevant canonical owner. Do not depend indefinitely on the chat message that first introduced it.

### Player-authored in-fiction letter

If the letter exists in fiction with exact player-authored wording, the document/Asset content becomes the durable semantic owner of that exact text once accepted.

### NPC lie / testimony

Semantic history can preserve that testimony occurred and knowledge/belief effects. Exact wording remains protected only when future semantics explicitly require exact wording or an archival policy retains it.

Research inference:

> **Natural-owner promotion is the preferred way to discharge long-lived correctness-critical raw-message exactness.**

This avoids turning `runtime.message` into a universal canonical text archive.

---

# 9. Retention dimensions should remain orthogonal

One scalar `retention_class` is likely too blunt.

Research indicates at least three distinct questions:

```text
IDENTITY / PROVENANCE
    must the historical message identity remain resolvable?

EXACT PAYLOAD
    must the exact accepted text remain available?

ARCHIVAL / STORY FIDELITY
    do we promise an exact/near-exact presentation copy after raw source compaction?
```

A message may therefore lawfully be:

```text
identity retained
exact raw payload compacted
semantic effects retained elsewhere
Story exact copy retained
```

without contradiction.

The candidate should prefer typed protection predicates/dependencies over one omnibus retention enum unless a small enum clearly reduces complexity.

---

# 10. Candidate compaction states

Conceptually investigate a `runtime.message` lifecycle such as:

```text
FULL
    stable message envelope + exact accepted payload

COMPACT
    stable message/provenance envelope
    exact raw payload absent
    semantic/source refs retained as required
    optional digest/length/type metadata
```

Physical deletion of the remaining compact envelope is Step 5.13 and is allowed only if no surviving reference/provenance/cursor promise requires its identity.

A hash/digest may support integrity/equality checks but does **not** preserve lost prose and shall never be presented as a substitute for exact text.

---

# 11. Story/Transcript evidence after raw source deletion

Step 4 already permits Story to become the only retained exact-copy source for some dialogue.

Research interpretation:

A `STORY/TRANSCRIPT` record may truthfully establish, for historical/presentation purposes:

```text
"this retained Story record contains the exact accepted/qualified text copied from source message M"
```

when deterministic projection/copy validation actually guarantees that fidelity.

It still does **not** establish:

```text
that a proposition stated in the text is objectively true
that a listener believed it
that every player received it
that fictional chronology follows Story order
```

Important boundary:

> A noncanonical Story copy should not become the **only correctness-critical exact-text authority** for an active mechanic. If exact wording remains mechanically/canonically required, preserve/promote it in the applicable historical/semantic owner closure first.

Story may safely be the last exact copy only where loss would affect historical/presentation fidelity rather than gameplay correctness.

---

# 12. Alternative A — Permanent exact archive

Model:

```text
all admitted participant messages
    -> immutable exact HDM archive forever
```

Strengths:

- maximal quote fidelity;
- simplest answer to late exact-history questions;
- good forensic/debug value;
- no premature exact-text loss classification.

Weaknesses:

- contradicts current session/dialogue baseline that exact old lines are not generally promised;
- repository/file-count growth is campaign-age proportional;
- data-minimization/privacy burden grows permanently;
- creates temptation for Context Assembler/LLMs to depend on raw historical prose rather than semantic owners;
- duplicates much of `STORY/TRANSCRIPT` if that layer also retains text;
- correction/deletion policy becomes harder;
- one-record-per-file Story/raw duplication may be substantial in long campaigns.

Verdict: **technically simple but semantically and operationally over-retentive for current HDM goals. Not recommended baseline.**

---

# 13. Alternative B — Rolling exact window + semantic compaction

Model:

```text
recent messages exact
older messages semantic-only after age/session threshold
```

Strengths:

- bounded exact raw storage;
- easy operational rule;
- recent dialogue fidelity retained.

Weaknesses:

- arbitrary TTL/session age has no semantic relation to exact-wording need;
- long-delayed contracts/puzzles/testimony can outlive the window;
- clock/session count becomes accidental deletion authority;
- historical fidelity varies by wall/session age rather than explicit promise.

Verdict: **useful physical maintenance heuristic only after semantic eligibility is proven; unsafe as primary retention authority.**

---

# 14. Alternative C — Typed retention classes

Model:

```text
message classified into exact/archive/semantic/ephemeral tiers
```

Strengths:

- explicit and inspectable;
- can encode product fidelity policy;
- easier maintenance filtering.

Weaknesses:

- one class may conflate identity, exactness and Story archival;
- classification can become LLM bureaucracy;
- misclassification can cause irreversible loss;
- difficult cases change over lifecycle.

Verdict: **useful only if reduced to a very small machine vocabulary or derived from concrete protections. Not sufficient alone.**

---

# 15. Alternative D — Dependency-driven retention closure

Model:

```text
exact payload stays while a typed current/promised consumer requires it
otherwise exact payload may compact
```

Strengths:

- strongest necessary-and-sufficient correctness model;
- maps to Step-5.9/5.10 protection philosophy;
- avoids TTL and global scans;
- natural-owner promotion can discharge old source dependency.

Weaknesses:

- does not guarantee arbitrary future exact quote questions;
- late previously-unanticipated exact-text use becomes impossible after deletion;
- protection discovery must be bounded and complete;
- user-facing fidelity promise must be explicit.

Verdict: **strong correctness core. Needs an explicit archival/fidelity policy beside it.**

---

# 16. Alternative E — Story/Transcript archival transfer

Model:

```text
raw runtime message exact
    -> deterministic/qualified STORY/TRANSCRIPT copy
    -> raw payload may compact
```

Strengths:

- separates runtime evidence from long-term presentation archive;
- aligns with Step 4 statement that Story may become last exact copy;
- Story can lag/catch up under Step 5.10;
- enables raw evidence compaction without losing selected dialogue fidelity.

Weaknesses:

- Story is noncanonical and may be edited/corrected as presentation;
- cannot safely become sole active correctness authority;
- if all messages MUST_MATERIALIZE, Story becomes a permanent full transcript archive anyway;
- projection lag can delay compaction;
- exact-copy fidelity must be machine-validated, not inferred from Chronicler prose.

Verdict: **excellent archival/presentation complement, not a complete correctness model.**

---

# 17. Alternative F — Hybrid minimum-sufficient model

Model:

```text
runtime.message stable identity + exact accepted payload while needed
        |
        +--> semantic/current consequences promoted to proper owners
        |
        +--> correctness-critical exact text promoted/protected in proper owner/evidence
        |
        +--> selected exact discourse optionally/MUST projected to STORY/TRANSCRIPT
        |
        v
when all exact protections discharged:
    raw payload -> COMPACT provenance envelope

later physical envelope GC -> Step 5.13
```

Strengths:

- correctness exactness and archival exactness remain separate;
- reuses existing admitted runtime identities;
- bounded dependency-driven eligibility;
- Story can be last exact copy where only presentation fidelity is at stake;
- supports safe source compaction/cursor continuity;
- does not require LLM classification for every mundane message;
- no full-history scan on ordinary turns.

Weaknesses:

- needs careful protection/discharge semantics;
- user-facing archival promise still must be chosen;
- implementation must distinguish source payload, semantic owner and Story copy;
- more concepts than “keep everything forever.”

Preliminary verdict: **strongest architecture direction.**

---

# 18. Alternative matrix

| Criterion | A Permanent | B Rolling | C Typed classes | D Dependency | E Story transfer | F Hybrid |
|---|---|---|---|---|---|---|
| gameplay correctness | strong | risky | strong if correct | very strong | insufficient alone | very strong |
| arbitrary exact quote fidelity | maximal | weak after TTL | policy-dependent | weak unless protected | policy-dependent | policy-dependent |
| host edit/retry resilience | strong after capture | strong within retained range | strong | strong | strong after qualified copy | strong |
| cold recovery | strong | strong semantically | strong | strong | Story not RRC | strong |
| Story integration | duplicates archive | possible | possible | explicit dependency | native fit | native fit |
| no global scans | possible | easy | possible | natural | natural | natural |
| repository growth | worst | bounded-ish | medium | low | medium | low-medium |
| privacy/data minimization | worst | better | configurable | strongest | depends on archive policy | strong/configurable |
| late exact unknown query | best | poor | policy-dependent | not promised | policy-dependent | explicit best-available |
| conceptual simplicity | superficially simple | simple but semantically arbitrary | medium | medium | medium | medium |
| reversibility after deletion | n/a | poor | class-dependent | poor if exact gone | exact may survive Story | explicit/controlled |
| YAGNI fit | weak | medium | medium | strong | strong | strongest |

---

# 19. Preliminary retention promise options

This is the likely human-decision axis.

## Promise P1 — Full exact participant archive

HDM promises exact accepted player-facing participant transcript for the life of the campaign unless explicitly deleted.

Pros: strong historical UX; simple expectation.

Cons: maximal storage/privacy burden; conflicts with current runtime's weaker exact-recall expectation; likely overkill.

## Promise P2 — Selective exact archival + semantic continuity

HDM guarantees:

```text
current gameplay correctness and semantic history survive
exact text survives when a typed gameplay/canonical dependency requires it
selected/qualified Transcript text may survive for historical fidelity
arbitrary old exact wording is NOT universally promised
```

When exact text is unavailable, runtime says so and uses retained semantic evidence without invented quotes.

Pros: matches current SESSION/DIALOGUE laws and necessary/sufficient principle; lowest correctness complexity.

Cons: some old exact dialogue may be irretrievably unavailable.

## Promise P3 — Broad in-fiction exact archive, OOC selective

All qualified in-fiction participant utterances are long-term Transcript `MUST_MATERIALIZE`; ordinary narration/action/OOC remain selective.

Pros: strong dialogue fidelity without archiving all host text.

Cons: still substantial file growth; determining exact fictional utterance spans/paraphrase fidelity adds interpretation complexity; may exceed current requirements.

### Preliminary recommendation

**Recommend P2 — Selective exact archival + semantic continuity** as baseline.

Reasoning:

1. it matches existing canonical/runtime behavior rather than silently expanding the product promise;
2. correctness-critical exact text remains fully protected;
3. Story can retain valuable dialogue without becoming universal raw archive;
4. privacy/data minimization is better;
5. arbitrary historical quote perfection is not currently a stated HDM requirement;
6. if later user demand proves broad exact transcript valuable, moving from P2 to broader retention is forward-compatible for future messages, while moving from permanent archive to aggressive deletion is socially/policy-sensitive and does not recover past privacy/storage costs.

Irreversible consequence: text compacted under P2 cannot later be reconstructed exactly unless another exact copy survived. This must be explicit to the owner/user.

Confidence before challenge: **MEDIUM-HIGH**.

---

# 20. OOC / safety preliminary result

Default durable Transcript should not automatically archive all OOC text.

Reasons:

- ordinary rules/debug chatter has little long-term fictional value;
- personal/meta disclosures should not be retained just because they entered the host conversation;
- safety/preferences must be normalized into their proper campaign/configuration owner when persistence is needed;
- OOC human disclosure can still matter without becoming PC knowledge.

Candidate direction:

```text
OOC text exact retention
    opt-in / typed-dependency / specific-history need

active safety/config semantics
    proper canonical/config owner

not:
    transcript as sole safety authority
```

Material privacy/product trade-off remains part of the owner decision brief if needed.

---

# 21. Host mutation behavior — preliminary contract

## Old user message edited after canon advanced

Previously accepted campaign history remains tied to HDM-owned interaction/message evidence.

The host edit is not an in-place rewrite of campaign evidence.

If the edited text is intentionally applied to current play, it must enter through a new/corrective Interaction and normal semantics.

## Assistant Retry after canon advanced

Regenerated host prose cannot automatically rerun or replace accepted mechanics/canon.

Current campaign authority wins; host branch must reconcile/recover before new consequences.

## Branch from old point

Old conversational prefix is not a rollback operation. A new branch must resolve current campaign authority under Step 5.7/5.8/5.9 rules.

## Deleted original chat

Gameplay continues from campaign storage. Exact historical wording is available only to the extent HDM's retention contract preserved it.

---

# 22. Voice/multimodal preliminary contract

Do not call voice transcript “verbatim.”

Baseline candidate should define:

```text
TEXT / DICTATION
    exactness relative to accepted sent text

VOICE CONVERSATION
    accepted transcript text may be historical evidence of runtime interpretation
    but NOT guaranteed verbatim audio wording
```

If exact audio wording ever becomes gameplay-significant, the user/runtime must establish an exact textual formulation or separately retained authoritative media evidence before relying on wording.

Attachments/documents:

- file/media identity is separate from message exactness;
- an in-fiction document whose exact content matters should promote that content into the appropriate Asset/world owner;
- retaining an attachment merely because it once accompanied a message is not automatically required by Transcript.

---

# 23. Bounded protection discovery

The design should avoid campaign-wide reference counting.

Candidate approach:

A message envelope owns/derives bounded typed outbound protection refs such as:

```text
semantic/execution exact-text consumer refs
Story Transcript materialization requirement/status
source/projection cursor anchor requirements
knowledge/disclosure provenance refs that still require source identity
```

Compaction eligibility is decided from the message's direct typed dependents / registered owner indexes, not from scanning all campaign records.

Natural semantic owners that copy/promote exact text should explicitly release/discharge the source exact-text dependency once the promoted owner is durably sufficient.

---

# 24. Compaction transform semantics

## T1 — FULL -> FULL

Nothing removed.

All exact/history consumers survive.

## T2 — FULL -> exact Story copy + COMPACT source envelope

Safe only if:

- no correctness-critical owner still requires source exact payload; and
- the relevant historical-fidelity promise permits Story to carry the remaining exact copy; and
- Story copy fidelity/source identity is validated and durable; and
- Step-5.10 cursor/coverage continuity remains valid.

Lost: raw-source exact payload location, not exact text itself.

## T3 — FULL -> semantic owner(s) + COMPACT source envelope

Safe when exact wording no longer promised/required.

Lost: arbitrary exact quote reconstruction.

Retained: message identity/provenance and canonical semantic consequences.

## T4 — FULL -> COMPACT identity/hash/metadata only

Safe only when no semantic exactness or archival requirement remains and all required downstream semantics already live elsewhere.

Hash does not permit reconstructing text.

## T5 — COMPACT envelope -> physical deletion

Not Step 5.11 execution. Eligibility semantics feed Step 5.13.

Only legal when no surviving ref/provenance/cursor promise requires message identity.

---

# 25. Step-5.10 cursor continuity

Compaction cannot make projection coverage uninterpretable.

Preferred solutions, in order:

1. retain small immutable source enumeration envelope/anchor while dropping payload;
2. keep message identity and source-domain ordinal/cursor semantics independent from content bytes;
3. if a source-domain compaction generation changes cursor semantics, migrate coverage atomically;
4. use sparse typed coverage only where contiguous enumeration cannot survive.

Do not substitute Git commit order for source-domain cursor.

---

# 26. Crash/concurrency preliminary model

Compaction is a same-ref deterministic campaign maintenance transaction.

Safe ordering prefers redundancy:

```text
required semantic promotion / Story exact copy becomes durable first
        ↓
compaction publication removes raw payload in a later coherent transaction
```

or one coherent same-ref transaction when all dependencies and paths can be validated together.

Never delete raw exact payload first and hope projection catches up later.

If CAS loses to gameplay/Story movement:

- re-pin current authority;
- revalidate protection closure;
- retry boundedly;
- never replay gameplay or regenerate Story merely because transport changed unless semantic dependencies actually changed.

Ambiguous acknowledgement uses Step-5.6 lineage/current-state verification.

---

# 27. Legacy/migration preliminary result

Legacy campaigns may have:

```text
SemanticEvents but no exact message payload
old visible ChatGPT chat still available or already gone
old Story prose with unverified quotes
```

Migration must never reconstruct exact wording from prose/semantic summaries and label it exact.

Allowed status:

```text
EXACT_TEXT_UNAVAILABLE
```

Old host chat may be offered as optional migration evidence only if the current deployment can explicitly import/capture it and the owner chooses to do so; it is not silently trusted as canonical history.

---

# 28. Assumption / evidence ledger

## A1 — broad arbitrary exact quote recall is not a baseline HDM product requirement

Confidence: MEDIUM-HIGH.

Evidence:

- existing `SESSION.md` falls back to semantic summary when exact current-chat wording is unavailable;
- `DIALOGUE.md` rejects permanent storage of every casual line;
- project direction emphasizes necessary-and-sufficient persistence.

Impact if false: retention recommendation changes toward P3/P1 and Story/source storage grows substantially.

Revisit trigger: owner explicitly chooses broad exact-history fidelity or user testing shows exact quote recall is core product value.

## A2 — runtime can eventually persist an HDM-owned `runtime.message` record independent of host history

Confidence: HIGH architecturally, implementation pending.

Evidence: runtime.message admitted in catalog + ID policy; Step 3 already requires raw message linkage.

Impact if false: exact host mutation resilience would require another durable source identity, reopening machine realization.

## A3 — no current ordinary ChatGPT runtime API exposed to HDM can be assumed to provide immutable message/revision lineage

Confidence: HIGH for baseline design.

Evidence: official product docs document user features, not such runtime contract; current tool environment exposes no such host identity primitive.

Impact if false: Step 6 may simplify retry/branch mapping, but retention architecture remains valid.

## A4 — exact gameplay-significant text can usually be promoted to a natural semantic owner

Confidence: MEDIUM-HIGH.

Evidence: contracts, documents, lore facts, command/execution evidence already have owner concepts.

Impact if false: some classes may require longer-lived exact `runtime.message` payload protection.

Revisit trigger: adversarial cases expose important exact wording with no lawful natural owner/evidence location.

---

# 29. Strongest counterargument to the leading hybrid

The strongest case for permanent exact archival is epistemic humility:

> At the moment a line is spoken, HDM cannot always predict what exact wording will become important 50 sessions later. Deleting text is irreversible; storage is cheap relative to losing campaign history; therefore keeping all admitted exact discourse may be the safer and simpler product.

This counterargument is real.

The response is not “storage is expensive,” because that alone is weak. The stronger response is:

1. HDM already distinguishes semantic correctness from arbitrary historical analytics;
2. making every utterance permanent because future importance is unknowable turns one uncertainty into an unbounded privacy/storage/product promise;
3. truly exact future dependence should be established when the text becomes a semantic object (contract/document/password/etc.); if a later mechanic tries to depend on an old line whose exact wording was never preserved/promised, the correct result may be “exact wording not established,” not invented reconstruction;
4. selected Story archival can preserve much historical value without making raw host text canonical or universal.

Whether this trade-off is acceptable is still owner-level product semantics.

---

# 30. Preliminary recommendation heading into analytical challenge

Working direction:

> **HDM-OWNED STABLE MESSAGE EVIDENCE / NATURAL-OWNER EXACTNESS PROMOTION / TYPED EXACT-PAYLOAD PROTECTION / SELECTIVE STORY ARCHIVAL / COMPACT PROVENANCE ENVELOPE**

Key properties:

```text
ChatGPT history = convenience evidence only, never sole durable authority
runtime.message = stable accepted communication evidence identity
runtime.interaction = accepted exchange/invocation identity
exact payload = retained only while correctness or selected archive policy protects it
semantic meaning/current effects = proper owners, never transcript authority
Story/Transcript = noncanonical exact/near-exact archive when explicitly qualified
message order != fictional chronology
OOC exact archive not default
voice transcript != verbatim audio
late unpromised exact quote may be unavailable
no all-history scan
no LLM call required for mundane retention eligibility
physical GC remains Step 5.13
host delivery acknowledgement remains Step 5.12
host Retry/edit identity feasibility remains Step 6 carry-forward
```

Before candidate design, analytical challenge must attack this direction, especially:

- late exact importance;
- whether selective archive is too weak for expected D&D experience;
- whether natural-owner promotion can actually discharge every correctness case;
- whether Story can safely be last exact copy;
- whether runtime.message compact envelope deserves independent persistence or becomes over-modeling;
- whether OOC exclusion loses useful campaign-management evidence;
- whether source/cursor continuity can stay bounded after large-scale compaction.
