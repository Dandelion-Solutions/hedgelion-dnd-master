# Step 4 Rerun — Truth, Knowledge, Role Contexts, Story, and Promotion — Candidate Specification

Status: **CANDIDATE ARCHITECTURE — ADVERSARIAL REVIEW REQUIRED BEFORE CANONICALIZATION**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Basis:

- `2026-08-20-step-4-rerun-task-brief.md`
- `2026-08-20-step-4-rerun-research-draft.md`
- `2026-08-20-step-4-rerun-decision-resolution.md`
- owner-approved prior Alternative C;
- owner-approved six logical LLM roles;
- Step-3 canonical deterministic execution boundary.

This specification describes one concrete Step-4 architecture. Machine schemas/catalog changes are not implemented by this document.

---

# 1. Architecture invariant

HDM SHALL separate authoritative information by semantic lifetime and assemble role-specific LLM context from those authorities rather than giving one omniscient working context to every LLM task.

```text
CURRENT / DURABLE AUTHORITIES

world and runtime state owners
    current concrete world/mechanical state

world.lore_fact
    durable proposition identity + objective truth

world.knowledge
    current fictional subject epistemic relation

runtime.disclosure
    durable human-player exposure relation

LOG / runtime.semantic_event
    durable semantic history / causal evidence

runtime.mechanical_event
    committed mechanical evidence

          |
          v
DETERMINISTIC CONTEXT ASSEMBLER
    role + subject/player + purpose + pinned frontier
          |
          +--> Interpreter
          +--> Dramaturg
          +--> Actor
          +--> Narrator
          +--> Chronicler
          +--> Commentator

Occurred evidence
    -> Chronicler
    -> STORY/
         TRANSCRIPT
         EVENTS
         MECHANICS
         NARRATIVE
    -> Commentator
```

No role output becomes canonical merely because an LLM stated it.

No Story record becomes canonical merely because it accurately cites canon.

No role may inherit another role's hidden source context merely because the roles are physically co-located in one future model/process.

---

# 2. Information classes and authority

## 2.1 Concrete current world state

Facts that naturally belong to an existing current-state owner SHALL remain there.

Examples:

- Actor HP/resources/location;
- Asset ownership/status;
- Effect lifecycle;
- Scene participants;
- Mission state;
- Connection/door state.

Step 4 SHALL NOT duplicate ordinary current-state values as `world.lore_fact` records simply to make every fact propositional.

Create an independently identified lore proposition only when future consistency, knowledge, claims, mystery/history, or durable causal reference requires proposition identity distinct from one current-state field.

## 2.2 `world.lore_fact`

`world.lore_fact` SHALL be the durable owner of an independently identified objective proposition.

Conceptual state:

```text
fact_id
statement
truth_status
record_status
subject_refs[]
scope? / chronology?
provenance_refs[]
supersedes_fact_id?
superseded_by_fact_id?
importance?
```

### 2.2.1 Objective truth status

Initial closed semantics:

```text
truth.undetermined
truth.established
truth.disproven
```

Exact catalog spelling may mechanically preserve/adjust the current namespace, but semantics SHALL match the above.

`truth.disputed` SHALL NOT remain an objective truth state.

- `undetermined` means the proposition has stable identity but objective truth has not been established;
- `established` means the proposition is objectively true in its declared scope;
- `disproven` means the proposition is objectively false in its declared scope.

Missing fact identity and `undetermined` are different:

- missing = no durable proposition currently exists;
- undetermined = a durable claim/question exists and may already be referenced by knowledge/history.

### 2.2.2 Record lifecycle

Truth status SHALL be separate from record lifecycle.

Initial lifecycle semantics:

```text
active
superseded
```

A superseded record remains historical/provenance evidence. Its old ID SHALL NOT silently change meaning.

### 2.2.3 Ordinary world change is not correction

A proposition SHOULD include sufficient scope/chronology when truth varies over fictional time.

Example:

```text
"King Arlen is alive at timeline marker K"
```

can remain established after the king later dies.

Do not mark a proposition superseded merely because the world later changes. Supersession is for correction/reformulation/replacement of the proposition's authoritative meaning, not ordinary temporal evolution.

### 2.2.4 In-world disagreement

Contradictory beliefs/accounts SHALL be represented through `world.knowledge` relations or ordinary source records, never by making objective truth internally contradictory.

If canonical objective records themselves conflict, that is an integrity/correction problem.

---

# 3. `world.knowledge` — current fictional epistemic authority

## 3.1 Identity

One material current fictional epistemic relation SHALL have one durable owner conceptually keyed by:

```text
(knower_id, fact_id)
```

The knower may be a PC, NPC, organization/faction, or another admitted intentional world subject.

PLAYER identity SHALL NOT use `world.knowledge` for meta-level human exposure.

## 3.2 Minimal stance vocabulary

The initial stance model SHALL remain deliberately small:

```text
epistemic.aware
epistemic.believed
epistemic.suspected
epistemic.rejected
```

Semantics:

- `aware` — subject is aware that the proposition/claim exists but no stronger current commitment is persisted;
- `believed` — subject currently treats the proposition as true for cognition/action;
- `suspected` — subject considers it plausible/material without committing to belief;
- `rejected` — subject currently treats the proposition as false/unreliable.

The objective `truth_status` remains independent. A subject may believe a disproven proposition or reject an established one.

Do not create rows merely to state `unknown` for every subject/fact pair. Absence means no durable tracked relation.

## 3.3 Knowledge provenance

Conceptual fields:

```text
knower_id
fact_id
stance
source_refs[]
last_changed_event_id?
confidence?     # optional, only when materially useful
```

Source refs may point to observation, testimony, document, SemanticEvent, interaction, spell/effect, or other established source identity.

Historical stance transitions belong to LOG/provenance, not an append-only history copied into the current relation.

## 3.4 PC agency

The system SHALL distinguish **information receipt/awareness** from voluntary player-character interpretation.

The engine MAY deterministically establish `aware` when resolved fiction makes a PC receive/perceive the proposition as a claim.

The engine SHALL NOT silently choose a PC's voluntary `believed`, `suspected`, or `rejected` stance merely because information was presented.

A voluntary PC stance transition requires one of:

- explicit player-authored evidence interpreted through the ordinary Interaction/Interpreter boundary;
- a previously established player-controlled durable stance;
- a genuine rules/world mechanism that constrains cognition independently of voluntary belief.

Narrator prose SHALL NOT infer voluntary PC belief/emotion as a side effect.

## 3.5 NPC/faction cognition

Actor may propose an `EpistemicDeltaDraft` when new evidence or circumstances plausibly change the represented subject's stance.

The proposal is not authority. A validated world transition commits the resulting `world.knowledge` state and corresponding semantic history when persistence is material.

Actor cannot use facts absent from its assembled subject context.

## 3.6 Derived indexes

To preserve bounded local retrieval without duplicate authority, HDM MAY maintain rebuildable indexes such as:

```text
knowledge_by_knower
knowers_by_fact
```

These indexes SHALL NOT become writable sources of semantic truth.

Legacy embedded PC/NPC/Faction knowledge arrays SHALL be retired as current writable authority after migration.

---

# 4. `runtime.disclosure` — durable human-player exposure

## 4.1 Purpose

`runtime.disclosure` SHALL represent information actually exposed to a human campaign player when future context/secrecy correctness may depend on remembering that exposure.

It is meta-level campaign state, not fictional cognition.

Conceptual identity:

```text
(player_id, fact_id)
```

It does not imply any controlled PC knows, believes, suspects, or rejects the proposition.

## 4.2 Exposure is sparse and monotonic by delivered revision

Do not create disclosure records for every sentence.

Persist disclosure when later narration/context correctness may depend on knowing what the human has already been shown.

Human exposure cannot be undone, but the proposition's authoritative record may later be corrected/superseded. Therefore a single timeless boolean `objective_status_exposed=true` is insufficient.

Conceptual state:

```text
player_id
fact_id
statement_exposed: boolean
latest_exposed_truth_revision_ref?
source_refs[]
last_disclosed_interaction_id?
```

`latest_exposed_truth_revision_ref` identifies the fact revision/provenance frontier whose objective status was actually revealed to that player.

If the fact is later corrected/superseded, the player is not assumed to know the correction until the new status/replacement is actually disclosed.

## 4.3 Claim exposure versus truth exposure

A player may be exposed to:

- the statement/claim itself;
- the objective truth status of that statement;
- both.

These are different.

Example:

```text
Player hears NPC claim: "The duke is a vampire."

statement_exposed = true
latest_exposed_truth_revision_ref = absent
```

Later an explicit OOC reveal may expose that the claim is objectively disproven without implying the PC learned that fact in fiction.

## 4.4 Narrator delivery protocol

HDM SHALL NOT attempt to reconstruct durable disclosure by later parsing arbitrary narration prose.

Narrator conceptually returns:

```text
NarrationResult
    prose
    disclosure_refs[]
        fact_id
        aspect = statement | objective_status
        truth_revision_ref?     # required for objective_status
```

Before delivery, the host validates every declared disclosure against the NarrationBundle eligibility.

After successful user-visible delivery, the host updates `runtime.disclosure` and emits appropriate historical evidence when persistence is material.

If delivery fails before the player receives the response, disclosure must not be falsely recorded as delivered.

## 4.5 Disclosure is not the primary leak-prevention mechanism

Structured disclosure refs are bookkeeping/evidence. The primary protection remains **not giving Narrator ineligible hidden source material**.

A Narrator hallucination that states a hidden fact absent from its bundle is an invalid output/correctness failure even if no disclosure ref accompanies it.

---

# 5. Secret semantics and legacy Secret retirement

No independent `Secret` truth/knowledge entity SHALL exist in the new architecture.

"Secret" is a contextual classification, not one global boolean lifecycle.

A proposition can simultaneously be:

```text
established objective truth
believed by NPC_A
unknown/untracked by PC_B
statement-exposed OOC to PLAYER_C
not exposed to PLAYER_D
```

Legacy Secret responsibilities SHALL route as follows:

| Legacy responsibility | New owner |
|---|---|
| objective truth | `world.lore_fact` or ordinary world owner |
| known/suspected subjects | `world.knowledge` |
| human exposure | `runtime.disclosure` |
| reveal/clue planning | Dramaturg non-canonical preparation |
| real reveal mechanics | actual Activity/Feature/Effect/Trigger/world owner |
| thread linkage | Thread/ordinary references when semantically needed |

`WORLD/SECRETS` SHALL cease to be a required new-campaign authority root. Legacy migration may read it as source material.

---

# 6. Dramaturg preparation

## 6.1 Authority

Dramaturg output is **non-canonical preparation**.

Conceptual output:

```text
PreparationDraft
    pressures
    involved actors/goals
    likely reactions under conditions
    possible manifestations
    clue/evidence routes
    opportunities/constraints
    near-horizon developments if unopposed
    dependencies/assumptions
    invalidation/expiry cues
```

Prepared scenes/events have no right to occur.

## 6.2 No mandatory persistent preparation owner in Step 4

Step 4 SHALL NOT introduce a new canonical `runtime.preparation`/plot/workflow owner.

Preparation may remain ephemeral, cached, session-local, or otherwise non-canonical according to later Step-6 policy.

Obsolete preparation may disappear without world repair because it was never truth.

If a prepared fact/entity later becomes necessary for durable canonical consistency, it crosses the ordinary promotion boundary before canonical reference.

---

# 7. Deterministic Context Assembler

## 7.1 Responsibility

HDM SHALL define a deterministic **Context Assembler** capability that selects the smallest role-eligible authoritative/derived source set for an LLM task.

It is:

- not a seventh LLM role;
- not a canonical record;
- not a general-purpose ACL engine;
- not a graph query language;
- not permission for campaign-wide scans.

## 7.2 Context request

Conceptually:

```text
RoleContextRequest
    role
    campaign_id
    pinned_campaign_frontier
    purpose
    session_id?
    player_id?
    pc_id?
    subject_id?
    story_frontier?
    requested_refs / bounded discovery intent?
```

A request SHALL identify enough subject/purpose information to evaluate role eligibility.

## 7.3 Pinned reads

One assembled gameplay context SHALL be based on one coherent campaign frontier for canonical sources.

Do not build a role context from branch-relative reads that may observe multiple different campaign HEADs.

Story retrieval used by Commentator SHOULD similarly pin a coherent Story/campaign frontier for one response so navigation does not mix pre/post-edit records unpredictably.

The exact persistence transport remains Step 5.

## 7.4 Output

Conceptually:

```text
RoleContextBundle
    role
    source_frontier
    subject/player identity
    eligible structured facts/refs
    bounded prose/context excerpts where needed
    provenance/source identities
    typed prior-role results
```

The bundle is working input, not an authority record.

## 7.5 No transitive raw-context inheritance

A role SHALL NOT consume another role's raw source bundle merely because it consumes that role's output.

Allowed:

```text
DramaturgContext -> Dramaturg -> PreparationDraft
NarratorContext + safe typed Preparation cue -> Narrator
```

Forbidden:

```text
DramaturgContext -> Narrator
```

without independently satisfying Narrator eligibility.

This invariant applies even when future implementation uses one physical model/process for both roles.

If a host/platform cannot preserve the logical context boundary within one invocation, Step 6 SHALL use separate invocations for the incompatible roles rather than weaken the Step-4 contract.

---

# 8. Six role context contracts

## 8.1 Interpreter

Interpreter MAY receive:

- current external message;
- bounded recent discourse;
- authenticated player/PC/session identity;
- player disclosure required to resolve OOC references;
- PC-eligible current scene/knowledge candidates;
- host-supplied bounded entity/activity candidates;
- smallest additional authoritative slice needed for a registered fiction-dependent invocation fact.

Interpreter SHALL NOT receive unrestricted DM truth merely to improve language understanding.

A human player may refer to an OOC-known secret that the PC does not know. Interpreter may resolve the reference while preserving a typed distinction that the claim is player-known only; binder/runtime cannot silently grant the PC fictional knowledge.

Interpreter output remains bounded interpretation/invocation-fact proposal under Step 3.

## 8.2 Dramaturg

Dramaturg MAY receive broad relevant DM context:

- objective truth and undetermined propositions;
- hidden facts;
- active threads/processes;
- NPC/faction goals/resources/constraints;
- subject knowledge summaries where useful;
- cross-player objective developments;
- player interests and exposure state where useful to plan reveals;
- campaign tone/boundaries;
- currently valid preparation.

It still SHOULD receive a bounded preparation horizon rather than the entire repository by default.

Dramaturg output is PreparationDraft only.

## 8.3 Actor

Actor is scoped to one represented intentional world subject.

Actor MAY receive:

- stable identity/traits/values;
- current goals/pressures;
- that subject's `world.knowledge` relations;
- current facts observable by that subject;
- relationships/social position;
- resources/capabilities available/known to that subject;
- prior commitments/recent events known to that subject.

Actor SHALL NOT receive unrestricted objective truth, other subjects' private cognition, or Dramaturg-only planning unavailable to the represented subject.

Actor returns intent/speech/epistemic proposals. Core validates/commits any durable consequence.

## 8.4 Narrator

Narrator MAY receive:

- current PC perception and eligible fictional knowledge;
- relevant human-player disclosure;
- newly settled observable consequences;
- authorized Actor action/speech results;
- settled mechanical receipts at selected presentation detail;
- tone/pacing context;
- explicitly safe preparation cues whose material content is independently eligible.

Narrator SHALL NOT receive raw Dramaturg context, unrestricted DM truth, or raw hidden adjudication context merely because another phase required them.

Narrator produces NarrationResult and returns control at the next meaningful voluntary player decision consistent with existing NARRATIVE/agency policy.

## 8.5 Chronicler

Chronicler MAY receive occurred historical evidence broader than Narrator's live context:

- retained participant messages;
- LOG/SemanticEvents;
- selected MechanicalEvents/receipts;
- canonical entity/lore refs needed for accurate provenance;
- historical knowledge/disclosure evidence needed to compute reveal availability;
- existing Story records/indexes for editorial continuity.

Chronicler SHALL NOT treat hidden chain-of-thought, private tool reasoning, or internal prompts as participant transcript.

Chronicler writes/edits Story only; it cannot mutate canon by literary inference.

## 8.6 Commentator

Default Commentator mode SHALL be Story-first and normally Story-only.

It MAY receive:

- eligible Story records at a pinned Story/campaign frontier;
- Story indexes/crossrefs;
- spectator session cursor/focus/style/detail/spoiler policy;
- optional requested mechanics detail already present in Story.

It SHALL NOT routinely read unrestricted current WORLD/STATE merely to answer spectator questions.

If requested information is absent from eligible Story, it says the retained story does not establish it.

A future explicit debug/deep-source mode MAY traverse Story provenance to canonical records. That is a separate Step-6 mode/capability, not default Commentator authority.

---

# 9. Typed logical handoffs

HDM SHALL define typed logical handoffs sufficient to prevent raw-context leakage without introducing a generic multi-agent message bus.

Conceptual contracts:

```text
Interpreter
    -> InterpretationDraft / accepted invocation facts

Dramaturg
    -> PreparationDraft

Actor
    -> ActorIntentDraft
       optional EpistemicDeltaDraft

Core
    -> NarrationBundle

Narrator
    -> NarrationResult

Core/history
    -> StorySourceBundle

Chronicler
    -> Story records/index updates

Story retrieval
    -> SpectatorStoryBundle

Commentator
    -> guest-facing prose
```

Each receiving phase assembles its own eligible sources plus the typed handoff.

No handoff is automatically canonical. Only the consuming deterministic transition/state owner can commit canonical state.

---

# 10. Historical evidence versus current authority

## 10.1 SemanticEvent / LOG

`runtime.semantic_event` / LOG SHALL remain compact durable semantic campaign history.

It may record:

- world transition summary;
- causal event refs;
- participant/player attribution;
- knowledge/disclosure changes;
- chronology evidence;
- source/mechanical refs when materially useful.

It SHALL NOT become a second current world-state owner.

## 10.2 Live-scene evidence

During an active live epoch, epoch-local perception/knowledge evidence may remain operationally authoritative for the live-owned scope under the existing live protocol.

At compaction, durable material knowledge/disclosure SHALL be normalized into `world.knowledge` / `runtime.disclosure`, with SemanticEvent history as appropriate.

After handoff, live arrays are historical/operational evidence, not parallel current global authority.

## 10.3 Transcript evidence

What someone says can be evidence of exposure/testimony without being objective truth.

Transcript and SemanticEvent history may explain why a knowledge/disclosure relation changed while the current relation remains the current authority.

---

# 11. Story authority and storage model

## 11.1 Non-canonical invariant

`STORY` SHALL be durable presentation/history material but SHALL NOT be required to recover or adjudicate canonical current state.

Deleting Story cannot change canon.

However, Story is not guaranteed byte-for-byte regenerable after source compaction. Exact dialogue/editorial prose may be presentation history whose loss harms fidelity without corrupting canon.

## 11.2 Directory structure

```text
STORY/
    TRANSCRIPT/
    EVENTS/
    MECHANICS/
    NARRATIVE/
```

The campaign manifest SHALL eventually expose `story_root` as a peer of state/world/log/checkpoint roots. Exact persistence/write plumbing belongs to Step 5 implementation planning.

## 11.3 IDs and files

Initial Story IDs:

```text
T001452
E003562
M012644
N000087
```

Rules:

- IDs are local to one Story layer;
- numeric sequence width is a minimum, not a maximum;
- one independently addressable Story record per file by default;
- relations are explicit refs, never inferred from equal numbers across layers.

## 11.4 Deterministic sharding

Use thousand-slot shards:

```text
shard = floor(sequence / 1000)
```

with minimum three-digit shard formatting.

Examples:

```text
STORY/TRANSCRIPT/001/T001452.yaml
STORY/EVENTS/003/E003562.yaml
STORY/MECHANICS/012/M012644.yaml
STORY/NARRATIVE/000/N000087.yaml
```

Shard directories contain Story records; layer-level indexes/manifests remain above the shard so a nominal 1000-record shard is not accidentally widened by metadata files.

This initial layout is chosen for bounded GitHub directory operations and simple path derivation, not because the operating system has a universal thousand-file limit.

---

# 12. Common Story metadata

A Story record SHALL carry only metadata useful to its presentation/retrieval role.

Common conceptual fields, as applicable:

```text
id
source_refs[]
cross_refs[]
entity_refs[]
chronology_refs[]
reveal_frontier
content
```

Layer schemas may narrow these fields.

`source_refs` anchor the Story projection to authoritative/historical evidence without making the Story record itself authoritative.

Do not copy entire source records merely for convenience.

---

# 13. Story layer contracts

## 13.1 TRANSCRIPT

Purpose: retained participant discourse useful for dialogue fidelity and reconstruction.

Default granularity: one visible participant message/utterance per Story record/file.

Conceptual fields:

```text
id
speaker_ref / participant role
interaction_id?
runtime_message_ref?
content
source/delivery refs
cross_refs[]
reveal_frontier
```

Exclude:

- hidden chain-of-thought;
- private tool reasoning;
- internal prompts/runtime plumbing not shown as participant discourse.

Transcript content is evidence of what was said, not proof that the statement is objectively true.

## 13.2 EVENTS

Purpose: human/LLM-friendly story adaptation of LOG/SemanticEvents.

One Story Event is one human-meaningful story beat.

It MAY:

- summarize several tightly related SemanticEvents;
- split a semantically overloaded source event for presentation;
- use clearer human-readable wording.

It SHALL retain source refs sufficient to trace its factual spine.

It SHALL NOT become state recovery authority.

## 13.3 MECHANICS

Purpose: curated mechanics that real players/spectators commonly track or ask about.

Include when material:

- important checks/saves/attacks/roll outcomes;
- HP/temp-HP changes;
- resource spend/recovery;
- Effect/Condition/LifeState transitions;
- durations/expiry/recovery information;
- tactically meaningful movement/range/action-economy facts.

Exclude by default:

- full Actor/Asset/Effect state copies;
- checkpoint snapshots;
- dependency DAG/cache internals;
- complete contribution stacks;
- all MechanicalEvents merely because they exist;
- resolver bookkeeping with no human planning/explanation value.

One Mechanics record is one human-meaningful mechanical beat, not necessarily one raw MechanicalEvent.

## 13.4 NARRATIVE

Purpose: editable literary prose derived from occurred evidence and Story crossrefs.

Conceptual fields:

```text
id
content
source_refs[]
transcript_refs[]
event_refs[]
mechanics_refs[]
entity_refs[]
reveal_frontier
```

NARRATIVE may be rewritten for style, clarity, pacing or literary quality without changing canon.

A literary inference unsupported by sources must not be stated as factual history.

---

# 14. Chapters and NARRATIVE index

Chapter is an editorial grouping, not a world entity.

A layer-level NARRATIVE index SHALL represent ordered grouping conceptually as:

```text
chapters:
  - chapter_id_or_index_label
    number_or_label
    title
    part_label?
    synopsis?
    narrative_refs:
      - N000001
      - N000004
      - N000006
```

Use explicit ordered refs rather than relying on contiguous numeric ranges.

Reordering, splitting, merging or renaming chapters SHALL NOT require moving or renaming underlying NARRATIVE files.

No initial `story.chapter` class is required.

---

# 15. Story reveal frontier and spoiler-safe rewind

## 15.1 Problem

Current NARRATIVE may be edited after later revelations. A guest who rewinds to an earlier historical point must not automatically receive later spoilers merely because an older scene was rewritten with hindsight.

## 15.2 Record-level reveal availability

Story records containing reveal-sensitive material SHALL carry a record-level `reveal_frontier`/availability descriptor derived from their material claims and source history.

Initial invariant:

> A Story record is eligible at a spectator frontier only if all material claims in that record are available under that frontier/perspective.

If one record would mix incompatible reveal eligibility, split the Story record rather than introduce field-level redaction in the initial design.

## 15.3 Spectator session state

Commentator session state is non-canonical and may include:

```text
story_cursor
focus refs
style/genre
mechanics_detail
spoiler_policy
allowed reveal frontier
```

This state need not become durable campaign truth.

Exact default spectator policy (chronological no-spoiler, full-history, player-perspective, etc.) belongs to Step 6 mode/profile design.

Step 4 only requires sufficient Story metadata to enforce a chosen policy.

---

# 16. Chronicler contract

Chronicler SHALL build/maintain Story from occurred evidence.

It MAY adapt wording and granularity but SHALL preserve:

- source/provenance traceability;
- factual compatibility with sources;
- distinction between transcript claim and objective truth;
- reveal availability needed by Commentator.

Chronicler SHALL NOT:

- create a canonical fact by writing Story;
- rewrite authoritative sources to fit prose;
- include hidden internal reasoning as participant transcript;
- treat future Dramaturg preparation as occurred history.

If sources conflict or are insufficient for a factual Story claim, Chronicler must omit/qualify the claim or surface a consistency issue rather than invent a reconciliation.

---

# 17. Commentator contract

Commentator SHALL provide interactive retelling/navigation over eligible Story.

Allowed presentation operations include:

- continue;
- rewind;
- jump by event/entity/chapter/ref;
- summarize or expand;
- focus on one character/thread;
- change style/genre/tone;
- answer questions from eligible Story;
- explain Story Mechanics;
- compare moments/events.

Commentator has broad presentation freedom but no factual freedom.

If Story does not establish an answer, it SHALL state that the retained Story does not establish it rather than invent a plausible event/motive/dialogue/mechanic.

A distinct explicit deep-source/debug mode may later follow provenance into canonical records; default Commentator does not.

---

# 18. Promotion contract

## 18.1 Sources that do not imply promotion

The following do not become canon merely by existing:

- Step-3 invocation facts;
- Dramaturg PreparationDraft;
- Actor intent/epistemic proposals;
- Narrator prose;
- Chronicler Story prose;
- Commentator interpretation;
- Story-only local labels.

## 18.2 Proposition promotion threshold

Create/promote a stable `world.lore_fact` when durable canonical consistency requires proposition identity, including when:

- `world.knowledge` must refer to the claim across persistence boundaries;
- `runtime.disclosure` must remember human exposure to the claim;
- LOG/another canonical record needs durable causal/reference identity;
- future mystery/history/lore consistency materially depends on remembering the claim;
- an explicit authorized lore transition commits the proposition.

A previously untracked claim MAY be promoted with `truth_status=undetermined` without asserting it is objectively true.

## 18.3 Entity dependency closure

A durable canonical reference to a local/promotable entity is valid only if the same publication closure promotes/publishes the referenced entity and required index entry or rejects the durable reference.

This extends the existing Step-1/3 local-entity dependency rule; Step 4 does not create a second promotion mechanism.

Story may mention a local/noncanonical entity without forcing promotion, but Story-only mention cannot later be used as canonical identity proof.

## 18.4 Preparation promotion

If a Dramaturg-prepared possibility becomes materially real through subsequent play, only the concrete facts actually established by world action/adjudication are promoted/committed.

Do not bulk-promote the whole PreparationDraft.

---

# 19. Legacy migration and retirement

The implementation plan SHALL include migration/disposition for the following legacy surfaces.

## 19.1 Lore

Legacy `lore.status = canonical | superseded | disputed_in_world` SHALL be mapped into separate objective truth/lifecycle/epistemic concepts.

Migration SHALL NOT infer objective truth merely from `disputed_in_world` without evidence.

## 19.2 PC/NPC/Faction knowledge

Embedded knowledge/belief/suspicion arrays SHALL be read as migration input and converted into `world.knowledge` relations where still material.

After migration they cease to be writable current authority.

## 19.3 Player visibility

Legacy `player.visibility.private_record_ids` SHALL not be treated as equivalent to proposition disclosure.

Where possible it may seed migration evidence, but exact disclosure must be reconstructed conservatively from available sources rather than guessed.

## 19.4 Secret

Legacy Secret records SHALL be decomposed conservatively:

- objective truth -> lore/world owner;
- known/suspected -> knowledge relations;
- revelation conditions -> preparation or actual rule owner only when semantics are clear;
- thread refs -> ordinary references.

Ambiguous migration must surface a migration issue rather than silently invent truth/knowledge.

## 19.5 Chapter

Retire from active catalogs/contracts:

```text
world.chapter
transition.chapter_append
event.chapter.appended
```

Useful old narrative bodies/coverage may migrate into Story/NARRATIVE and its index as non-canonical content, but old Chapter identity SHALL NOT silently become a new Story machine identity.

## 19.6 Template/layout

New campaign layout SHALL add `STORY` and eventually remove required `WORLD/SECRETS`/old Chapter assumptions where present.

Exact Git write/migration transaction details belong to Step 5 implementation and migration planning.

---

# 20. Context and output error semantics

Step 4 SHALL distinguish at least these classes conceptually:

- **missing required authority/source** — hydrate/retrieve or return typed unresolved/missing-source condition;
- **ineligible source for role** — exclude; if indispensable to requested role task, block/route to correct role rather than leak it;
- **mixed/stale frontier** — reject/reassemble from one pinned frontier;
- **invalid role output identity/ref** — deterministic validation failure;
- **Narrator disclosure ref not eligible** — reject/regenerate/correct before delivery;
- **Actor proposal uses unavailable fact** — reject proposal/context bug;
- **Story factual conflict** — do not canonicalize Story; surface editorial/consistency issue;
- **Commentator asks beyond Story** — answer that retained Story does not establish it or use explicit later deep-source mode if authorized.

Do not repair these failures by inventing prose.

---

# 21. Step-5 and Step-6 handoff

## 21.1 Step 5 owns physical durability/transport

Step 5 SHALL own:

- Story publication batching and Git tree/CAS mechanics;
- transcript/history retention and compaction policy;
- checkpoint/publication interactions;
- multiplayer revision/conflict semantics for new files/indexes;
- migration transaction mechanics;
- recovery consequences of missing non-canonical Story;
- live-scene compaction transport details.

Step 5 SHALL NOT reintroduce a separate durable spectator branch as the default architecture.

## 21.2 Step 6 owns physical LLM orchestration

Step 6 SHALL own:

- whether logical roles are separate model calls;
- model selection by role;
- role co-location only where logical context boundaries remain enforceable;
- token/latency/cost budgets;
- preparation cache/retention policy if needed;
- spectator mode defaults and deep-source/debug mode;
- mode profiles and final context-budget behavior.

Step 6 may optimize physical topology but may not weaken Step-4 authority/context contracts.

---

# 22. Candidate exit assertions

This Candidate claims the following architecture properties for adversarial review:

1. objective proposition truth has one owner;
2. current fictional epistemic state has one owner;
3. human-player exposure is a separate owner;
4. no generic Secret authority remains;
5. PC voluntary belief remains player-controlled;
6. Actor cognition is subject-scoped;
7. Narrator receives separately assembled eligible context;
8. raw private contexts do not flow transitively between roles;
9. Story is non-canonical and four-layered;
10. Chronicler and Commentator have different responsibilities;
11. Story supports rewind/spoiler eligibility through record-level reveal frontier;
12. Chapters are index grouping, not entities;
13. promotion permits stable undetermined claims without asserting truth;
14. canonical durable references close local-entity dependencies;
15. implementation can defer physical model topology and Git transport to Steps 6 and 5 respectively.

The next required step is an independent adversarial architecture review.
