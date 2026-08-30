# Step 5.11 — Transcript / History Retention & Compaction — Architectural Task Brief

Status: **TASK BRIEF — ARCHITECTURAL RESEARCH AUTHORIZED; NO RETENTION MODEL DECIDED**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Classification: **ARCHITECTURAL / DEEP-WORK**

Governing process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- Superpowers `using-superpowers` + `brainstorming`

Active roadmap slice: **Step 5.11 only**.

This brief authorizes research and design for Step 5.11. It does not authorize runtime/schema implementation, Step 5.12 host-delivery architecture, Step 5.13 generic physical garbage collection, or Step 6 physical LLM orchestration.

---

# 1. Purpose

Step 5.11 must define the minimum sufficient durable historical-retention model for HDM.

The core question is not merely:

> How long should chat messages be kept?

The actual architecture problem is:

> **Which exact or reduced historical evidence must survive, under which owner and for which consumers, so HDM can preserve gameplay correctness, legitimate historical fidelity, Story projection, provenance, knowledge/disclosure distinctions and bounded recovery without turning the campaign into an eternal raw-chat archive or treating host conversation history as authority?**

The final model must distinguish at least:

```text
what was submitted / emitted
what was accepted as gameplay input
what was actually said in fiction
what was merely claimed
what became objective canon
what a fictional subject learned/believed
what a human player was exposed to
what Story retained for presentation
what exact wording remains available
what can be compacted or deleted
```

These are different semantics and MUST NOT collapse into one transcript/log abstraction.

---

# 2. Owner direction and design philosophy

The governing design principle is:

> **necessary and sufficient**

Do not introduce complexity merely to support hypothetical archival perfection.

In particular:

- do not assume all conversation text must survive forever;
- do not assume exact text may always be discarded once a summary exists;
- do not make LLM summaries authority for deletion eligibility;
- do not make Story a truth source merely because it may become the last surviving exact-text copy;
- do not create a generic permanent event store merely to answer arbitrary future historical questions;
- do not require background agents/workers, ChatGPT Work, Pro/Enterprise-only capabilities, or cross-chat automation for correctness;
- do not load retained history into ordinary LLM context merely because it is physically stored;
- do not solve physical six-role context isolation here;
- do not solve every class of repository garbage collection here;
- do not silently move Step 5.12 or Step 5.13 into this slice.

If a stronger historical-fidelity promise materially changes storage, privacy, complexity or user expectations, surface it as a decision-ready owner trade-off rather than choosing it mechanically.

---

# 3. Baseline deployment constraint

The baseline HDM environment for this architecture remains:

> **one ordinary sequential ChatGPT conversation/execution stream, with no required Work usage, no Pro/Enterprise-only dependency and no permanently running independent/background process.**

Step 5.11 must therefore work if:

- the current chat ends;
- a new chat starts later;
- no process continues after the assistant turn;
- host/project memory is unavailable, disabled, incomplete or later deleted;
- the campaign repository is the only durable HDM-owned campaign storage available at recovery.

Richer future deployment may improve convenience but cannot weaken these semantics.

---

# 4. Current platform facts that must shape the investigation

These facts are time-sensitive and MUST be reverified from current official OpenAI documentation during Step-5.11 research and again if implementation depends on them.

Current official ChatGPT documentation establishes at least:

1. users can edit their own earlier messages;
2. users can retry/regenerate assistant responses;
3. users can branch a conversation from an earlier point into a new chat;
4. users can delete chats, after which they are removed from visible history and are not recoverable through normal product use;
5. Project/chat memory is product context assistance, not an HDM-owned immutable campaign evidence store.

Research starting references:

- OpenAI Help: ChatGPT model/help material describing Edit Message, Retry and Branch in a new chat;
- OpenAI Help / release notes: Branch conversations;
- OpenAI Help: Chat and File Retention Policies in ChatGPT;
- OpenAI Help: Projects in ChatGPT / project memory.

Architectural consequence to investigate, not pre-decide:

> **The visible ChatGPT conversation cannot automatically be treated as immutable durable transcript authority. HDM may need to capture accepted ingress/egress evidence at explicit runtime boundaries before later host edits, retries, branches or deletion make host history unsuitable as the sole source.**

Do not assume the host exposes stable immutable message IDs, revision ancestry, programmable older-chat retrieval or exact delivery acknowledgements. Verify every such capability before relying on it.

Exact outbound host-emission acknowledgement remains Step 5.12.

---

# 5. Inherited canonical laws that 5.11 must preserve

## 5.1 Step 4 — truth / knowledge / disclosure / Story

Preserve all of the following:

- objective truth is not transcript text;
- `world.knowledge` is current fictional epistemic authority;
- `runtime.disclosure` is human-player exposure authority;
- transcript proves that a statement was said/exposed only when the relevant accepted/delivery evidence actually establishes that;
- a transcripted claim does not prove the claim is objectively true;
- Story is durable but non-canonical;
- `STORY/TRANSCRIPT` is retained participant discourse useful for dialogue fidelity and reconstruction;
- hidden chain-of-thought, private tool reasoning and internal prompts/runtime plumbing are not participant transcript;
- Chronicler may transform occurred evidence into Story but cannot create canon by literary inference;
- Story may become the only retained exact copy of some dialogue after source compaction without becoming objective-truth authority.

## 5.2 Step 5.1 — no generic global frontier

Every retention/cursor/frontier/coverage construct MUST be typed to its semantic domain.

Do not create:

```text
global_history_frontier
global_transcript_frontier
one campaign-wide message sequence with fictional meaning
```

merely to simplify retention.

## 5.3 Step 5.2 / 5.4 / 5.7 — recovery independence from chat memory

A fresh runtime must recover gameplay-significant state from durable sources, not from remembered chat/model/process context.

Chat context and ChatGPT Memory are not campaign storage.

Loss of nonessential transcript fidelity must not silently become loss of current gameplay authority.

## 5.4 Step 5.6 — deterministic publication and crash consistency

Any durable retention/compaction transition eventually published on the campaign ref must obey Step-5.6 publication semantics:

- deterministic Python/core owns repository transport;
- one coherent resulting-tree transaction per logical publication boundary;
- non-force CAS publication;
- no gameplay replay or RNG reroll because storage transport conflicts;
- prepared objects are nonauthority until selected by the authoritative ref.

## 5.5 Step 5.9 — chronology remains independent

Transcript/message order MUST NOT become fictional chronology implicitly.

Possible orders include:

```text
host/conversational order
source-enumeration order
repository publication order
fictional causal order
fictional temporal order
narrative reading order
```

They are not interchangeable.

## 5.6 Step 5.10 — Story projection handoff

Preserve:

- queue-free pull catch-up;
- layer-local Story coverage;
- source-domain-native projection watermarks;
- campaign HEAD is not Story source watermark;
- `MUST_MATERIALIZE` versus `MAY_OMIT` terminal disposition;
- source provenance identity may survive after full source payload compaction;
- source cursor interpretability/continuity must survive lawful compaction;
- Story catch-up is not a SAVE/RRC/gameplay requirement;
- source deletion may require typed Story projection closure only when Step-5.11 policy says so.

## 5.7 Step 5.12 reserved boundary

Step 5.11 may specify what kind of delivered/accepted textual evidence would be retention-relevant, but MUST NOT pre-decide the exact outbound host-delivery acknowledgement protocol.

In particular:

```text
NarrationResult generated
!=
NarrationResult actually emitted to player
```

Step 5.12 owns the authoritative emission/delivery boundary and retry/duplicate-delivery semantics.

## 5.8 Step 5.13 reserved boundary

Step 5.11 owns semantic retention classes, protection/eligibility conditions, compaction transformations and required surviving evidence for transcript/history.

Step 5.13 owns the broader physical GC/orphan-cleanup system and deletion coordination across all artifact classes.

Do not create two independent GC architectures.

---

# 6. Current repository/runtime audit required before recommending a design

Research MUST inspect current remote branch state and at least:

- Step-4 canonical truth/knowledge/role/Story spec;
- Step-5.0 contamination result;
- Step-5.1 frontier model;
- Steps 5.2, 5.4, 5.6, 5.7 where recovery/publication affects history;
- Step-5.9 chronology canonical spec;
- Step-5.10 Story projection canonical spec;
- `GAME/CORE/RUNTIME.md`;
- `GAME/CORE/STORAGE.md`;
- `GAME/CORE/PERSISTENCE.md`;
- `GAME/CORE/SESSION.md` where host/session continuity matters;
- `GAME/CORE/INFORMATION.md`, `NARRATIVE.md`, `DIALOGUE.md` where speech/knowledge/presentation semantics may constrain retention;
- current runtime schemas/catalogs for `runtime.message`, `runtime.interaction`, SemanticEvent, disclosure/message/session surfaces, if admitted/implemented;
- current tests/case catalogs mentioning transcript, messages, history, Story, disclosure, correction, recovery or compaction;
- current campaign template/layout to determine whether transcript/history storage already exists or is only conceptual.

Do not infer absence from one failed keyword search. Follow `DEV/PROJECT_MAP.md` and inspect the actual owning surfaces.

Produce an explicit current-state inventory:

```text
concept
semantic owner
current physical representation
stable identity?
mutable or append-only?
current retention promise
current consumers
known duplicate/stale authority
later-slice owner if deferred
```

---

# 7. Required external/platform research

Because this subsystem is hosted through ChatGPT, research must verify current public product behavior relevant to transcript reliability.

At minimum investigate from official OpenAI sources:

1. user-message editing semantics;
2. assistant Retry/regeneration semantics;
3. branch-in-new-chat semantics;
4. chat deletion/archive/retention semantics;
5. Projects availability on Free/Go and project-memory behavior;
6. whether past project chats are automatically/programmatically retrievable by an active runtime or merely product memory/context;
7. whether stable host message/interaction/revision IDs are exposed to the runtime environment;
8. whether edits/retries preserve any machine-visible revision lineage;
9. whether deleting/branching/editing a chat can change what a later model invocation sees;
10. whether voice/multimodal input creates transcript text with a stable representation relevant to HDM, if current baseline gameplay supports it.

Do NOT design against undocumented behavior.

External research may also examine authoritative primary material on:

- event/log compaction;
- provenance preservation;
- append-only evidence versus replaceable read models;
- retention tiers;
- hash/content-address evidence limitations;
- audit-log versus transcript distinctions.

Generic best practice is evidence only. It must be tested against HDM's actual semantics.

---

# 8. Central semantic distinctions the design must make explicit

The research must define the relationships among at least these concepts without assuming they collapse into one record:

```text
HOST MESSAGE
    visible product conversation item

ACCEPTED PARTICIPANT INPUT
    exact input accepted into one HDM interaction boundary

RUNTIME MESSAGE / INTERACTION EVIDENCE
    durable or operational evidence that a specific participant communication occurred

FICTIONAL UTTERANCE
    words actually spoken/written/perceived in fiction, if established

SEMANTIC EVENT
    durable causal/history meaning

MECHANICAL EVENT
    committed mechanical evidence

WORLD KNOWLEDGE
    current fictional epistemic relation

RUNTIME DISCLOSURE
    human exposure relation

STORY/TRANSCRIPT
    durable noncanonical exact/near-exact participant discourse projection

STORY/EVENTS/NARRATIVE
    derived presentation/history forms
```

The design must answer which transitions are deterministic and which require interpretation.

---

# 9. Define what “exact wording” means

Do not use “exact transcript” without defining exactness.

Research at least these possible levels:

```text
byte-exact host payload
Unicode/text-exact submitted content
normalized textual content
rendered visible content
speaker + exact textual payload
content + attachments/media refs
content + message role/channel metadata
```

Questions include:

- Does Markdown formatting matter?
- Do whitespace/Unicode normalization differences matter?
- Are edited host messages new identities/revisions or replacements?
- Is quoted text part of the speaker's utterance or a reference?
- How are attachments/images/voice represented without forcing full binary archival into Transcript?
- What minimum metadata is needed to preserve “who said what, in which interaction/channel”?

The final architecture should preserve the least exactness sufficient for the promised semantics.

---

# 10. Transcript candidate admission

The design MUST explicitly classify candidate sources rather than treating every host-visible token as transcript.

Investigate at least:

### Candidate-positive classes

- player textual message submitted to HDM;
- player in-character speech embedded in a broader action declaration;
- player OOC statement when durable historical retention is intended;
- player-authored letters/messages/documents when exact wording matters;
- emitted Narrator prose after Step-5.12 delivery qualification;
- NPC dialogue actually emitted to participant(s);
- system-visible dice/mechanics text only when transcript semantics justify it rather than `STORY/MECHANICS`.

### Candidate-negative classes

- hidden chain-of-thought;
- internal reasoning summaries not shown as participant discourse;
- tool calls/results not presented as participant discourse;
- developer/system/project instructions;
- private Dramaturg preparation;
- Actor private cognition;
- generated but never emitted Narrator drafts;
- repository plumbing;
- hidden validation/retry diagnostics.

### Ambiguous classes requiring research

- rules/OOC questions;
- safety/boundary discussions;
- user corrections/retractions;
- retries/duplicates caused by host/network behavior;
- messages edited after a response exists;
- branched conversations;
- voice transcription;
- uploaded documents used as in-fiction letters versus out-of-fiction reference material;
- spectator/Commentator exchanges.

Do not resolve these by intuition alone. Map each to actual consumers and promises.

---

# 11. Exact-wording dependency analysis

The design must identify when exact wording is correctness-relevant versus merely useful for historical quality.

Required examples include:

- magical wording where phrasing affects adjudication (`Wish`-like or contract-like mechanics);
- oath, bargain, legal agreement or promise where terms matter;
- password/passphrase;
- riddle, clue, poem, inscription or code where exact text is part of the puzzle;
- player-authored letter/document intended to exist in fiction;
- quoted NPC testimony where later contradiction depends on wording;
- social deception where “what exactly was said” may matter;
- player declaration where exact scope/conditions affect accepted intent;
- ordinary flavor dialogue whose exact wording has no current mechanical dependency;
- OOC rules discussion whose exact wording should not become fictional evidence;
- safety/boundary instruction whose active policy must live with its proper owner rather than relying on transcript retention.

The research must determine:

```text
who/what declares an exact-wording dependency?
when does that dependency begin?
when may it end?
what durable reference protects the payload?
can a semantic replacement discharge it?
can Story/TRANSCRIPT become the protected copy?
```

Do not allow Chronicler prose to discharge a correctness-critical exact-wording dependency unless the contract explicitly proves that the retained representation is exact enough.

---

# 12. Retention promise — likely owner-level decision area

The research must distinguish technical possibility from the user-facing historical promise HDM makes.

At minimum evaluate whether baseline HDM promises:

- exact full participant transcript forever;
- exact transcript for a bounded horizon only;
- exact retention only for selected dependency-bearing/important utterances;
- exact player-facing discourse copied into Story before source compaction;
- semantic history only unless exact wording is explicitly protected;
- another hybrid.

Do NOT ask the owner to choose before performing the analysis.

Produce a decision-ready brief if multiple materially different promises remain credible after challenge, including:

- expected historical fidelity;
- storage growth;
- repository churn/file-count impact;
- privacy/data-minimization implications;
- token/context consequences;
- Story quality;
- debugging/audit usefulness;
- multiplayer consequences;
- migration consequences;
- reversibility;
- what is irretrievably lost after compaction.

The agent must recommend one baseline.

---

# 13. Required alternative space

Research MUST compare at least five materially different retention architectures before selecting or hybridizing.

At minimum include variants equivalent in substance to:

## Alternative A — Permanent exact archive

Retain all admitted participant transcript payloads indefinitely.

Challenge:

- storage/file growth;
- privacy/data minimization;
- accidental dependency of retrieval on raw transcript;
- whether this is actually necessary for D&D fidelity.

## Alternative B — Rolling exact window + semantic compaction

Keep recent exact discourse, then retain only semantic/history evidence unless explicitly protected.

Challenge:

- what sets the window without arbitrary age authority;
- delayed puzzles/agreements discovered much later;
- historical quote fidelity.

## Alternative C — Typed retention classes

Classify admitted evidence into retention/protection categories with different compaction rules.

Challenge:

- classification authority;
- schema/LLM burden;
- misclassification risk;
- whether categories become needless bureaucracy.

## Alternative D — Dependency-driven retention closure

Retain exact payload while any current/promised consumer holds a typed dependency; otherwise compact aggressively.

Challenge:

- late unknown future questions;
- discovering consumers only after deletion;
- bounded dependency enumeration;
- relation to Story and chronology protection rules.

## Alternative E — Story/TRANSCRIPT archival transfer

Use raw runtime message evidence only transiently; materialize admitted exact discourse into durable `STORY/TRANSCRIPT`, then allow raw source payload compaction while preserving provenance anchors.

Challenge:

- Story is noncanonical;
- exact-text evidence versus truth authority;
- projection lag;
- loss/correction of Story;
- `MUST_MATERIALIZE` semantics.

## Alternative F — Hybrid minimum-sufficient model

Combine dependency-driven exact protection, selective Story archival and semantic compaction.

Challenge:

- prove every retained mechanism has a concrete consumer;
- avoid creating both a permanent raw archive and a duplicate Story archive;
- minimize classification and migration complexity.

Additional alternatives are encouraged if research reveals a stronger model.

Do not force exactly one pure alternative if a smaller hybrid is clearly superior.

---

# 14. Required evaluation matrix

Evaluate each serious alternative against at least:

```text
GAMEPLAY CORRECTNESS
EXACT-WORDING FIDELITY
HISTORICAL / STORY QUALITY
KNOWLEDGE / DISCLOSURE SEPARATION
HOST EDIT / RETRY / BRANCH RESILIENCE
COLD RECOVERY
MULTIPLAYER
CHRONOLOGY SAFETY
STORY 5.10 INTEGRATION
SOURCE-COMPACTION SAFETY
BOUNDEDNESS / NO GLOBAL SCANS
REPOSITORY FILE / STORAGE GROWTH
PUBLICATION CONTENTION
TOKEN / LLM COST
PRIVACY / DATA MINIMIZATION
MIGRATION / VERSIONING
OBSERVABILITY / REPAIR
REVERSIBILITY
YAGNI / CONCEPTUAL COMPLEXITY
```

Make trade-offs concrete with scenarios, not adjectives.

---

# 15. Accepted input versus host mutation

This workstream is mandatory.

ChatGPT allows earlier-message editing, response retry and conversation branching. The design must therefore determine what happens when the host-visible conversation no longer matches previously accepted campaign interaction evidence.

Required cases:

### User edits an earlier message after HDM already accepted consequences

The edit MUST NOT silently rewrite established campaign history.

Investigate whether:

- the original accepted payload must have been durably captured;
- the edit becomes a new/corrective interaction if intentionally applied;
- the visible host branch is merely presentation context after canonical divergence.

### User retries/regenerates an earlier assistant response after canon advanced

The regenerated prose cannot automatically rerun or replace already accepted gameplay state.

Determine how the runtime detects/recoverably handles this host branch divergence.

### User branches a new chat from an old point

A new host branch beginning at old conversational context MUST NOT be assumed to represent the current campaign authority.

It must reconcile/recover against current campaign storage under existing Step-5 recovery rules.

### User deletes the original chat

Loss of host-visible transcript must not destroy durable gameplay state. Determine which historical fidelity may lawfully be lost if HDM had not promised durable exact retention.

This analysis may expose Step-5.4/5.7 or Step-6 carry-forward requirements but must not reopen those slices without an actual contradiction.

---

# 16. Correction, retraction and retcon semantics

Distinguish at least:

```text
TYPO / CLARIFICATION BEFORE ACCEPTANCE
    no accepted old semantic consequence yet

NEW PLAYER MESSAGE CORRECTING PRIOR STATEMENT
    both utterances may be historical evidence

CORRECTION AFTER CANONICAL CONSEQUENCE
    requires lawful new transition/reversal if fiction changes

EDITORIAL TRANSCRIPT CORRECTION
    presentation repair only

HOST MESSAGE EDIT
    product UI mutation; not automatically a campaign rewrite
```

Research how exact historical evidence should represent “what was originally said” versus “what the player intended to replace before acceptance”.

Never let Transcript editing silently rewrite SemanticEvent/current-state authority.

---

# 17. Claim, truth and speech-act separation

Required invariant family:

```text
Transcript: NPC said "The king is dead"
    proves an utterance if accepted/delivered evidence establishes it

NOT automatically:
    king is dead

NOT automatically:
    listener believed it

NOT automatically:
    every player was exposed to it
```

The design must preserve this separation after source compaction.

If raw source is deleted and `STORY/TRANSCRIPT` becomes the only retained exact copy, define precisely what that Story record can still evidence and what it cannot.

---

# 18. OOC, safety and personal/meta information

Research OOC retention separately from in-fiction discourse.

Questions include:

- Should ordinary OOC rules questions be retained in durable campaign Transcript?
- Should campaign-management statements be retained?
- Should safety/boundary discussions be copied verbatim, summarized into their proper policy owner, or both?
- Should accidental personal/meta disclosures be retained merely because they appeared in the chat?
- What historical/debug value justifies durable OOC retention?
- Can OOC text create player disclosure evidence without creating PC knowledge?

Do not use Transcript as the sole authority for active safety/preferences/campaign configuration if another proper owner exists.

If privacy/data-minimization trade-offs remain material, escalate them as an owner decision with recommendation.

---

# 19. Multiplayer and visibility

Required multiplayer scenarios:

- two players speak in one live scene nearly simultaneously;
- players act in independent scenes;
- one message is visible/audible to only a subset of PCs/players;
- private whisper versus public speech;
- one participant disconnects before receiving later narration;
- shared scene absorbed after dialogue occurred;
- host message ordering differs from fictional action order;
- duplicate/retried delivery reaches different participants differently;
- spectator/Commentator view must not gain hidden discourse merely because Transcript stores it.

Retention metadata may need speaker/channel/audience/provenance identity, but MUST NOT become fictional chronology or disclosure authority accidentally.

The design must state which layer owns visibility/disclosure truth and how Transcript references it.

---

# 20. Story / Transcript integration

Step 5.10 intentionally left Transcript admission/retention to this slice.

Step 5.11 must define when a source candidate is:

```text
not admitted to STORY/TRANSCRIPT
MAY_OMIT
MUST_MATERIALIZE before source payload deletion
already materialized with sufficient exactness
```

Research whether `STORY/TRANSCRIPT` is:

- a convenience copy;
- the normal long-term exact-text archive;
- only one possible exact-text retained representation;
- or some narrower role.

Avoid mandatory catch-up of unrelated Story layers.

If source deletion depends on Transcript materialization, the protection should be typed to exactly that source/layer requirement rather than to “Story current”.

---

# 21. Compaction transformations

The final design must define allowed semantic transforms, not merely “delete old messages”.

Candidate transformations to investigate include:

```text
FULL EXACT SOURCE
    -> retained unchanged

FULL EXACT SOURCE
    -> exact Story/Transcript copy + compact provenance anchor

FULL EXACT SOURCE
    -> semantic event/interaction evidence + compact provenance anchor

FULL EXACT SOURCE
    -> compact identity/hash/metadata only

FULL EXACT SOURCE
    -> physical deletion with no survivor
        only if no promise/dependency requires any retained evidence
```

For every transform specify:

- what facts remain provable;
- what fidelity is lost;
- which consumers remain valid;
- whether source refs remain resolvable;
- whether 5.10 projection cursor continuity survives;
- whether correction/integrity diagnosis remains possible;
- whether the transform is reversible.

A hash proves equality to a later candidate payload only if the original payload is available for comparison; it does not itself preserve the lost prose. Do not overstate hash semantics.

---

# 22. Compaction eligibility and protection predicate

Research a bounded typed protection model.

Conceptually test whether eligibility can be expressed as something like:

```text
EXACT_PAYLOAD_PROTECTED if any live/promised consumer requires exact form

SEMANTIC_EVIDENCE_PROTECTED if any live/promised consumer requires the historical occurrence/provenance

PROJECTION_PROTECTED if retention policy requires durable Transcript materialization before source compaction

CURSOR_ANCHOR_PROTECTED if deletion would make existing source-domain coverage uninterpretable
```

Do not canonicalize these names prematurely.

The important question is whether deletion eligibility can be proved from bounded owner/dependency routes rather than campaign-wide scanning.

Avoid generic reference-counting if ownership-specific protection is simpler.

---

# 23. Late questions and historical analytics

Challenge the model with late user questions such as:

- “What exactly did the witch say in session one?”
- “Did I promise to return the sword, or only say I would try?”
- “What exact wording did the inscription use?”
- “Who first used the name Black Gate?”
- “Show me every time this NPC lied.”

Separate three cases:

```text
EXACT ANSWER PROMISED BY RETENTION CONTRACT
BEST AVAILABLE ANSWER FROM RETAINED STORY/EVIDENCE
NOT ESTABLISHED / EXACT WORDING NO LONGER RETAINED
```

Do not silently convert a desired future question into an eternal archival requirement.

If the product should promise exact historical recall broadly, this is a material owner decision and must be costed honestly.

---

# 24. Retrieval/context is not retention

The design MUST distinguish:

```text
PHYSICALLY RETAINED
    bytes/evidence still exist in campaign storage

INDEXED / DISCOVERABLE
    bounded retrieval can locate them

ELIGIBLE FOR CURRENT ROLE
    Context Assembler may provide them to this role

LOADED INTO CURRENT MODEL CALL
    actual token/context cost now
```

Keeping a transcript does not authorize loading it into every role call.

Deleting something from hot context does not imply physical deletion.

The final design should support campaign age scaling without whole-history prompt growth.

---

# 25. Source-enumeration and cursor continuity

Step 5.10 coverage requires source-domain cursors/anchors to remain interpretable after lawful source compaction.

Research at least:

```text
retain lightweight enumeration anchors/index
retain source identity records while dropping payload
translate coverage atomically to a compacted generation/domain
use sparse coverage where contiguous cursor continuity cannot be preserved
```

Compaction MUST NOT create a state where Chronicler restart cannot tell which source candidates were already terminally considered.

Campaign Git commit order is not an acceptable replacement source cursor unless the owning projection-source contract explicitly proves suitable domain semantics.

---

# 26. Crash consistency and partial compaction

Required failure scenarios:

1. Transcript projection materialized but raw source not yet deleted;
2. raw source deletion planned but Story publication loses CAS;
3. source compacted but projection coverage not coherently migrated;
4. crash after compact provenance anchor written but before payload deletion;
5. concurrent Story catch-up while retention compaction is prepared;
6. concurrent gameplay publication touches semantic evidence referenced by compaction;
7. ambiguous acknowledgement of compaction publication;
8. correction arrives while source is being compacted.

Design must prefer safe redundancy over irreversible premature deletion.

Do not invent distributed transactions.

---

# 27. Migration and legacy campaigns

Research migration from current/older campaigns where:

- no `STORY/` exists;
- no durable Transcript exists;
- old host chat may or may not still exist;
- runtime message identities may be absent or incomplete;
- SemanticEvents exist but exact player wording is gone;
- old Story prose may contain quotes without exact-source provenance;
- old campaign fields imply history that newer contracts no longer treat as authority.

Migration law:

> **Never invent exact historical text that was not durably retained.**

Possible migration status may need to express “exact wording unavailable” rather than fabricating reconstruction.

---

# 28. Performance / scale requirements

The final model must make ordinary gameplay cost independent of campaign age.

Challenge against:

- years-long campaign;
- tens of thousands of messages;
- many Story records;
- multiplayer;
- no transcript maintenance during an unresolved ordinary turn;
- bounded catch-up/maintenance windows;
- repository directory/file-count growth;
- publication conflicts caused by maintenance churn;
- token cost of any LLM-assisted classification.

Prefer deterministic classification/routing when semantics allow it.

Do not require an LLM call merely to decide whether every mundane message may age out.

---

# 29. Analytical challenge requirements

Before a candidate architecture is presented, explicitly attack at least:

1. Why not keep all admitted exact transcript forever?
2. Why not keep only SemanticEvents and delete transcript quickly?
3. Why not make `STORY/TRANSCRIPT` the sole permanent archive?
4. Why not use time/age/session-count TTLs?
5. Why not use a generic dependency/reference count?
6. Why not let Chronicler decide importance?
7. Why not use ChatGPT's own chat history as storage?
8. Why not hash everything and delete text?
9. Why not retain only player messages, not Narrator/NPC text?
10. Why not retain all emitted Narrator output forever?
11. Can exact wording become mechanically important only *after* it looked unimportant?
12. Can a user edit/retry/branch host history after canon has committed?
13. What is the smallest evidence needed to survive such host mutation?
14. Does any design accidentally make transcript order fictional chronology?
15. Does any design accidentally make Story truth authority?
16. Can deletion strand 5.10 projection coverage?
17. Can deletion invalidate knowledge/disclosure provenance?
18. Can a new chat resume with no host history?
19. Can maintenance be postponed without blocking gameplay?
20. Does the model create unbounded campaign scans?
21. Does it duplicate current-state authority?
22. What is irreversibly lost, and is that loss explicitly within the product promise?

The strongest counterargument to the recommended model must be stated fairly.

---

# 30. Mandatory adversarial scenario suite

Candidate and final design must survive at least:

```text
ordinary flavor dialogue
player action declaration with no exact-word dependency
Wish-like exact magical wording
contract/oath with exact terms
password/passphrase
riddle/poem/inscription clue
player-authored in-fiction letter
NPC lie later challenged by exact quote
player says one thing then clarifies before acceptance
player corrects after canonical consequence
player edits an old ChatGPT message after canon advanced
player retries/regenerates an old assistant response after canon advanced
player branches a new chat from an old point
original chat is deleted
new chat cold-recovers only from campaign storage
OOC rules question
OOC secret known to player but not PC
safety/boundary discussion
private whisper
public speech in multiplayer scene
nearly simultaneous player messages
independent-scene messages with unrelated fictional chronology
speaker/message visible to only subset of participants
generated Narrator draft never emitted
duplicate/retried host delivery
Transcript record is only surviving exact-text copy
Story is missing but gameplay recovery succeeds
Story Transcript lags behind source
raw source cannot delete until required Transcript materialization
raw source deleted after safe archival transfer
Story record later edited for presentation
Story record deleted/corrupted after raw source compacted
SemanticEvent survives while exact wording does not
source hash survives but text does not
5.10 cursor crosses compacted source range
compaction crash halfway through replacement publication
concurrent Story catch-up and compaction
concurrent gameplay and maintenance publication
legacy campaign has no exact transcript
user asks years later for exact quote that retention contract did not promise
campaign with 100k messages does no all-history scan on ordinary turn
```

Add scenarios discovered during research.

---

# 31. Human decision rights

Do not ask the owner to decide mechanical fields, cursor encoding, file sharding or index implementation.

Escalate only decisions that remain materially value-laden after research, likely including some subset of:

- baseline promise of exact conversational history;
- default inclusion/exclusion of OOC discourse in durable transcript;
- whether exact player-facing transcript is an expected long-term product feature or best-effort Story quality;
- privacy/data-minimization versus archival-fidelity trade-offs;
- any irreversible loss policy that materially changes user expectations.

For each escalated decision provide:

```text
verified facts
constraints
assumptions
recommended choice
strongest alternative
trade-offs
failure modes
reversibility
confidence
what would change the recommendation
```

Do not present raw options without a recommendation.

---

# 32. Agent-owned mechanical work

Once owner semantics are decided, the agent owns:

- exact retention vocabulary;
- owner mapping;
- protection/eligibility rules;
- provenance/reference semantics;
- compaction state machine;
- examples;
- cursor-continuity rules;
- Story 5.10 integration;
- 5.12/5.13 handoff clauses;
- migration semantics;
- integrity states;
- test matrix;
- machine-realization debt;
- documentation consistency;
- roadmap/debt bookkeeping.

The owner must not be asked to manually validate a giant mechanical specification after the substantive decisions are approved.

---

# 33. Required design artifact chain

Step 5.11 must follow the full deep-design cycle.

Expected chain:

```text
TASK BRIEF                     this document
    ↓
RESEARCH DRAFT
    repository audit
    platform research
    source/consumer inventory
    alternative matrix
    assumption/evidence ledger
    ↓
ANALYTICAL CHALLENGE
    attack alternatives / YAGNI / failure modes
    ↓
DECISION BRIEF                 if material owner choice remains
    ↓
OWNER DECISION                 only where required
    ↓
CANDIDATE SPECIFICATION
    ↓
ADVERSARIAL REVIEW
    full scenario suite
    cross-Step consistency
    ↓
RESOLUTION GATE
    all blockers disposed
    ↓
CANONICAL STEP-5.11 SPEC
    ↓
ROADMAP UPDATE
```

Do not skip adversarial review. Transcript deletion is irreversible enough that a plausible-looking design is insufficient.

---

# 34. Candidate specification must answer explicitly

A candidate cannot proceed to adversarial review until it answers all of:

1. What is the durable source identity of one accepted participant communication?
2. Which host-visible messages are not admitted as durable historical evidence?
3. What does exactness mean?
4. When does exact wording become protected?
5. Who owns that protection?
6. How is protection discovered boundedly?
7. What evidence may replace raw payload?
8. What can never replace exact wording when exactness remains material?
9. What does Story/TRANSCRIPT prove after source deletion?
10. What does it explicitly not prove?
11. When may raw source payload become compaction-eligible?
12. What remains after compaction?
13. How is source identity/provenance preserved?
14. How does 5.10 coverage remain interpretable?
15. How do corrections/retractions work?
16. How do host edit/retry/branch operations interact with already accepted campaign history?
17. How does multiplayer visibility remain separate from transcript retention?
18. How does transcript order remain separate from fictional chronology?
19. How do knowledge/disclosure survive source compaction without duplicate authority?
20. How does a cold runtime behave when exact historical text is gone?
21. What fidelity does the product promise to the user?
22. What is deliberately not promised?
23. What work is handed to 5.12?
24. What work is handed to 5.13?
25. What remains Step-6 deployment/orchestration work?

---

# 35. Exit criteria

Step 5.11 closes only when all of the following are true:

- transcript/history source identities and authority boundaries are explicit;
- host ChatGPT history is not silently treated as immutable campaign authority;
- exact-wording semantics are defined;
- retention promise is owner-approved if it contains a material product trade-off;
- exact/semantic/provenance retention responsibilities are unambiguous;
- compaction eligibility is bounded and machine-decidable enough for later implementation;
- no LLM prose/summary can authorize deletion of correctness-critical evidence by itself;
- Story/TRANSCRIPT can be used without becoming objective-truth authority;
- Step-5.10 projection-before-delete and cursor-continuity requirements are satisfied;
- knowledge/disclosure/chronology semantics remain intact;
- host edit/retry/branch/delete scenarios have defined safe behavior;
- multiplayer visibility and transcript ordering do not become duplicate authorities;
- legacy/missing-transcript campaigns do not invent exact history;
- ordinary gameplay requires no all-history scan and no transcript-maintenance LLM call;
- 5.12 delivery boundary remains explicitly deferred but has a precise handoff;
- 5.13 physical GC remains explicitly deferred but has a precise semantic deletion-eligibility handoff;
- implementation/schema/catalog/test obligations are recorded as later debt rather than prematurely implemented;
- no unresolved architectural blocker remains.

Final target statement, to be validated rather than assumed:

> **HDM retains exact historical text only where the accepted product promise or a typed live dependency justifies it; otherwise it may compact redundant raw discourse into sufficient durable semantic/provenance/Story evidence without changing canon, knowledge, disclosure, chronology or recoverability. Host chat history is convenience/context, never the sole campaign authority.**

This target is a hypothesis for the design cycle, not a pre-approved canonical decision.

---

# 36. Sequencing gate

While Step 5.11 is active:

```text
Step 5.10 = CLOSED
Step 5.11 = IN PROGRESS
Step 5.12 = NOT STARTED
Step 5.13 = later dependency only
Step 6    = blocked by Step 5
```

Later slices may be inspected only where necessary to expose dependencies or contradictions.

Do not begin Step 5.12 architecture until Step 5.11 closes.
