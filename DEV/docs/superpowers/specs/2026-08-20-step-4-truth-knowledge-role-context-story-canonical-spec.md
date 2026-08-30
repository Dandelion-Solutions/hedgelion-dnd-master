# Step 4 Canonical Specification — Truth, Knowledge, LLM Role Contexts, Story, and Promotion

Status: **CANONICAL ARCHITECTURE — IMPLEMENTATION PLANNING REQUIRED**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Canonicalization basis:

- `2026-08-20-step-4-rerun-task-brief.md`
- `2026-08-20-step-4-rerun-research-draft.md`
- `2026-08-20-step-4-rerun-decision-resolution.md`
- `2026-08-20-step-4-rerun-candidate-spec.md`
- `2026-08-20-step-4-rerun-adversarial-review.md`
- `2026-08-20-step-4-rerun-resolution-gate.md`
- `../design/2026-08-20-llm-logical-roles-draft.md`
- owner-approved Step-4 Alternative C;
- owner-approved six logical LLM roles;
- Step-3 canonical deterministic execution boundary.

Earlier Step-4 task/research/decision wording is historical derivation material where it conflicts with this consolidated specification.

This specification does not itself implement schemas/runtime code. Implementation planning SHALL use the required Superpowers planning/TDD workflow.

---

# 1. Canonical architecture invariant

HDM separates authoritative information by semantic lifetime and gives each logical LLM role only a bounded context assembled for that role.

```text
CANONICAL / CURRENT AUTHORITIES

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
       +--------+---------+---------+
       |        |         |         |
 Interpreter Dramaturg  Actor   Narrator
                         
 History/evidence -> Chronicler -> STORY -> Commentator
```

The complete accepted logical role set is:

1. Interpreter;
2. Dramaturg;
3. Actor;
4. Narrator;
5. Chronicler;
6. Commentator.

A logical role defines responsibility, source eligibility, authority, input and output semantics. It does **not** imply a separate long-lived agent, model, process or model call.

No LLM role can make a proposition canonical merely by stating it.

No Story record can become current-state/mechanical authority merely by accurately citing canon.

No role may inherit another role's ineligible source context transitively.

---

# 2. Repository visibility is not information authority

Campaign Git is not treated as a confidentiality boundary against a human who deliberately browses repository files.

HDM SHALL NOT require encryption, obfuscation or separate durable spectator branches merely to hide campaign secrets from repository readers.

The correctness boundary is **LLM context eligibility and player/subject disclosure**:

- repository readability does not imply PC knowledge;
- repository readability does not imply player disclosure;
- a fact loaded for private adjudication/preparation does not become narratable;
- an NPC cannot use DM-only truth merely because it exists in storage;
- Commentator does not receive unrestricted campaign truth merely because Story and canon coexist in one branch.

---

# 3. Current world state remains with existing owners

Step 4 does not turn HDM into a universal proposition database.

State that naturally belongs to an existing owner remains there, including examples such as:

- Actor HP/resources/location;
- Asset ownership/status;
- Effect/Condition lifecycle;
- Scene participation;
- Mission/Contract state;
- Connection/door state.

Do not duplicate ordinary current-state fields as `world.lore_fact` merely to make every value propositional.

A durable lore proposition is created when **independent propositional identity** is required for knowledge, claims, mystery/history, durable disclosure, causal reference, or future consistency.

---

# 4. `world.lore_fact` — objective proposition authority

## 4.1 Responsibility

`world.lore_fact` is the durable owner of an independently identified proposition about objective campaign reality.

Conceptual state:

```text
fact_id
statement
truth_status
record_status
subject_refs[]
material scope / chronology qualifiers?
provenance_refs[]
supersedes_fact_id?
superseded_by_fact_id?
importance?
last_truth_transition_ref?
```

Exact machine field spelling follows schema implementation, but semantics are normative here.

## 4.2 Objective truth status

Initial closed truth semantics:

```text
truth.undetermined
truth.established
truth.disproven
```

- `undetermined` — durable proposition identity exists, but objective truth is not established;
- `established` — proposition is objectively true in its declared scope;
- `disproven` — proposition is objectively false in its declared scope.

`truth.disputed` is retired from the objective truth axis.

In-world disagreement belongs to subject knowledge/belief relations, not objective truth status.

Missing fact identity is not equivalent to `undetermined`:

```text
missing
    no durable proposition exists

undetermined
    durable proposition exists and may already be referenced
```

## 4.3 Record lifecycle

Truth and lifecycle are separate.

Initial lifecycle semantics:

```text
active
superseded
```

Supersession is explicit historical/correction metadata. It does not erase the old record or silently change its ID meaning.

## 4.4 Proposition identity immutability

After a lore fact has a durable external reference, its identity-defining proposition payload SHALL NOT be semantically rewritten in place.

Identity-defining payload includes:

- statement meaning;
- material subject identity;
- material scope;
- material chronology qualifiers.

Allowed in-place changes for the same proposition include:

- `undetermined -> established|disproven` truth transition;
- explicit correction metadata where the proposition identity itself remains the same;
- lifecycle/provenance metadata;
- nonsemantic presentation metadata.

A materially different proposition receives a new fact ID and explicit supersession/relation to the old record.

This preserves the Step-1 rule that durable IDs are never silently repurposed.

## 4.5 Ordinary fictional change is not retcon

A proposition whose truth varies over time must carry adequate scope/chronology.

Example:

```text
"King Arlen is alive at timeline marker K"
```

may remain established after later death.

Do not supersede historical propositions merely because later world state changes.

## 4.6 Truth transition evidence

Every material objective truth-status change SHALL have stable causal/transition evidence usable as a revision reference.

Step 4 does not require a new generic revision-record class. Existing/implemented lore transition or SemanticEvent identity may serve this role.

---

# 5. `world.knowledge` — current fictional epistemic authority

## 5.1 Sole durable current owner

One material current fictional subject-to-proposition epistemic relation has one durable owner conceptually keyed by:

```text
(knower_id, fact_id)
```

`knower_id` may identify a PC, NPC, organization/faction or another admitted intentional fictional subject.

Human PLAYER exposure is not stored here.

Legacy embedded PC/NPC/Faction knowledge arrays are migration input/derived convenience only after Step-4 implementation; they do not remain parallel writable authority.

## 5.2 Initial stance vocabulary

Initial closed stance semantics:

```text
epistemic.aware
epistemic.known
epistemic.believed
epistemic.suspected
epistemic.rejected
```

Meaning:

- `aware` — subject is aware of the claim/proposition but no stronger current commitment is persisted;
- `known` — information is legitimately available to the subject as an established in-fiction fact through a qualifying source;
- `believed` — subject currently treats the proposition as true without the engine claiming reliable/objective knowledge;
- `suspected` — subject treats the proposition as a plausible/material possibility;
- `rejected` — subject currently treats the proposition as false/unreliable.

Objective truth remains independent.

Examples valid by design:

```text
fact P is disproven
NPC_A believed(P)

fact Q is established
NPC_B rejected(Q)
```

Do not create `unknown` rows for all subject/fact pairs. Absence means no material durable current relation is tracked.

## 5.3 Current provenance

Conceptual current relation:

```text
knower_id
fact_id
stance
supporting_source_refs[]
last_changed_event_id?
confidence?       # optional, only when useful
```

`supporting_source_refs` remains bounded to evidence useful for the **current** stance.

Full transition history belongs to LOG/SemanticEvents. `world.knowledge` is not a second epistemic event log.

## 5.4 PC agency

HDM SHALL distinguish information availability from voluntary PC interpretation.

The engine may establish PC `aware` when the PC receives a claim.

The engine may establish PC `known` when resolved fiction/rules provide a qualifying reliable knowledge channel.

The engine SHALL NOT silently choose voluntary PC:

- belief;
- suspicion;
- rejection;
- emotion;
- interpretation

merely because information was presented.

Voluntary belief/suspicion/rejection changes require explicit player-authored evidence interpreted through the ordinary Interaction/Interpreter boundary unless a genuine world/rules mechanism independently constrains cognition.

Narrator prose cannot create PC belief state.

## 5.5 NPC/faction cognition

Actor may propose subject-local epistemic changes using only its eligible context.

Conceptually:

```text
EpistemicDeltaDraft
    subject_id
    fact_id
    proposed_stance
    source_refs[]
    rationale/semantic basis as needed
```

The draft is non-authoritative. A validated transition commits `world.knowledge` and appropriate semantic history when material.

## 5.6 Derived retrieval indexes

Rebuildable indexes may support bounded retrieval, for example:

```text
knowledge_by_knower
knowers_by_fact
```

Indexes do not become writable semantic authority.

---

# 6. `runtime.disclosure` — human-player exposure authority

## 6.1 Responsibility

`runtime.disclosure` is the campaign-durable meta-level owner for material information actually emitted to a human player when future context/secrecy correctness depends on remembering that exposure.

Conceptual identity:

```text
(player_id, fact_id)
```

Disclosure does not imply any controlled PC knows/believes/suspects/rejects the proposition.

## 6.2 Sparse persistence

Do not create disclosure records for every sentence.

Persist only exposure whose future correctness may matter, for example:

- hidden/previously hidden proposition was shown;
- objective truth status was explicitly revealed OOC;
- future Narrator/Interpreter behavior needs to know the player has already been told the claim.

## 6.3 Claim exposure versus objective-status exposure

The relation must distinguish:

```text
statement exposed
objective truth status/revision exposed
```

Conceptual state:

```text
player_id
fact_id
statement_exposed: boolean
latest_exposed_truth_transition_ref?
source_refs[]
last_disclosed_interaction_id?
```

Example:

```text
NPC says: "The duke is a vampire."

statement_exposed = true
latest_exposed_truth_transition_ref = absent
```

The human has heard the claim but has not been told its objective truth.

## 6.4 Exposure is monotonic only for the exact delivered information

A human cannot be made to unsee a delivered statement, but later truth corrections do not become known automatically.

`latest_exposed_truth_transition_ref` references the exact committed objective-status transition/correction evidence that was exposed.

No exposure propagates automatically across:

- later truth-status changes;
- replacement/superseding fact IDs;
- corrected proposition meaning.

## 6.5 Narrator disclosure protocol

Narrator SHALL conceptually return:

```text
NarrationResult
    prose
    disclosure_refs[]
        fact_id
        aspect = statement | objective_status
        truth_transition_ref?  # required for objective_status
```

Before host emission, every disclosure ref is validated against the NarrationBundle.

After the response is accepted/emitted onto the player-facing host surface, disclosure may advance.

HDM does not claim to know whether a human literally read the message.

If generation/host emission fails before that boundary, disclosure must not be recorded as delivered.

Exact transport acknowledgement is Step 5/host implementation detail.

## 6.6 Disclosure refs are evidence, not leak prevention

The primary secret-leak prevention mechanism is Context Assembler source eligibility.

Structured disclosure refs avoid later NLP reconstruction of exposure and make delivery auditable.

An unsupported Narrator statement remains a correctness failure even if no disclosure ref accompanies it.

---

# 7. Secret is contextual; legacy Secret authority is retired

No independent `Secret` truth/knowledge class survives Step 4.

"Secret" means that material information exists but is not eligible for a particular subject/player/role context.

Legacy responsibilities route as follows:

| Legacy Secret responsibility | Canonical owner |
|---|---|
| objective truth | `world.lore_fact` or ordinary current world owner |
| known/believed/suspected subjects | `world.knowledge` |
| human player exposure | `runtime.disclosure` |
| reveal/clue preparation | Dramaturg non-canonical preparation |
| real automatic reveal mechanics | actual Activity/Feature/Effect/Trigger/world owner |
| thread linkage | existing Thread/ordinary refs when needed |

`WORLD/SECRETS` is legacy organization, not a required new-campaign authority root.

---

# 8. Dramaturg preparation

Dramaturg performs private non-canonical GM preparation.

Conceptual output:

```text
PreparationDraft
    pressures/problems
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

Step 4 SHALL NOT create a canonical plot/preparation/workflow owner.

Preparation may be ephemeral, cached or otherwise non-canonical according to later Step-6 policy.

If a prepared fact/entity later becomes necessary for canonical consistency, only the concrete fact/entity actually established by play crosses the normal promotion boundary. Never bulk-promote a PreparationDraft.

---

# 9. Deterministic Context Assembler

## 9.1 Responsibility

Context Assembler is a deterministic capability that selects the smallest role-eligible source set for one LLM task.

It is not:

- a seventh LLM role;
- canonical state authority;
- a generic ACL engine;
- a knowledge graph;
- a generic query language;
- permission for campaign-wide scans.

## 9.2 Context request

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
    spectator_state_ref/value?
    requested_refs / bounded discovery intent?
```

Enough subject/player/purpose identity must be provided to evaluate eligibility.

## 9.3 Pinned authoritative reads

One gameplay RoleContextBundle uses one coherent canonical campaign frontier.

Do not assemble a context from branch-relative reads that could observe different campaign HEADs.

Commentator Story retrieval likewise pins one coherent Story/campaign frontier for one response/edit view.

Transport details remain Step 5.

## 9.4 Context output and inspectability

Conceptually:

```text
RoleContextBundle
    role
    source_frontier
    subject/player identity
    eligible structured facts
    bounded prose excerpts where needed
    source_manifest[]
    typed prior-role results[]
```

`source_manifest` provides bounded source identities sufficient for testing/debug attribution.

The bundle/manifest is working/trace evidence, not a new canonical authority and need not be retained indefinitely.

## 9.5 No transitive raw-context inheritance

Typed role results may cross role boundaries. Raw source bundles do not.

Allowed:

```text
DramaturgContext -> Dramaturg -> PreparationDraft
NarratorContext + eligible typed cue -> Narrator
```

Forbidden:

```text
DramaturgContext -> Narrator
```

unless every source independently satisfies Narrator eligibility.

## 9.6 Physical context compatibility rule

A narrower-context role SHALL NOT execute inside a physical model invocation that still contains source material ineligible for that role.

Step 6 may physically co-locate roles only when:

1. effective source eligibility is compatible; or
2. the platform provides a genuine context reset/isolation boundary so ineligible prior source material is absent from the narrower role phase.

Otherwise Step 6 must use separate physical invocations.

A prompt phrase such as "now forget the secret and act as Narrator" is not a context reset.

---

# 10. Six role information contracts

## 10.1 Interpreter

Mission: understand external natural language and produce bounded semantic interpretation.

Eligible context may include:

- current external message;
- bounded recent discourse;
- authenticated player/PC/session identity;
- relevant player disclosure to resolve OOC references;
- PC-eligible scene/knowledge candidates;
- host-supplied bounded entity/activity candidates;
- smallest authoritative slice needed for one registered fiction-dependent invocation fact.

Interpreter must not receive unrestricted DM truth merely for language understanding.

If a human refers to an OOC-known secret the PC lacks, Interpreter may resolve the reference while preserving that player/PC distinction. It cannot grant the PC fictional knowledge.

Output remains a Step-3 bounded InterpretationDraft/accepted invocation-fact input subject to deterministic binding.

## 10.2 Dramaturg

Mission: prepare situations/pressures/possibilities, not future canon.

Eligible relevant context may include:

- objective truth and undetermined propositions;
- hidden facts;
- threads/processes/deadlines;
- NPC/faction goals/resources/constraints;
- subject knowledge summaries;
- cross-player objective developments;
- player interests/exposure useful for reveal planning;
- campaign tone/boundaries;
- currently retained non-canonical preparation.

Dramaturg may have the broadest DM-facing information set but still uses bounded preparation horizon rather than whole-repository preload by default.

Output is PreparationDraft only.

## 10.3 Actor

Mission: reason from one NPC/faction/intentional subject's own cognition and circumstances.

Eligible context may include only relevant:

- identity/traits/values;
- goals/pressures;
- subject `world.knowledge` relations;
- observable scene facts;
- relationships/social position;
- resources/capabilities known/available to subject;
- commitments/recent events known to subject.

Actor cannot inherit DM truth or Dramaturg plans unavailable to that subject.

Output may include ActorIntentDraft, speech intent and EpistemicDeltaDraft. Core validates/commits any durable consequence.

## 10.4 Narrator

Mission: player-facing current-game Master/frontman.

Eligible context may include:

- current PC perception/known information;
- relevant human-player disclosure;
- newly settled observable consequences;
- authorized Actor actions/speech;
- settled mechanics at selected explanation detail;
- tone/pacing context;
- preparation-derived cues only when their material content is independently Narrator-eligible.

Narrator does not receive raw Dramaturg/private adjudication source context.

Narration is projection of resolved/eligible state and cannot create voluntary PC actions, beliefs, emotions or canonical facts.

Output is NarrationResult.

## 10.5 Chronicler

Mission: transform occurred evidence into non-canonical Story.

Eligible historical context may include:

- retained participant messages;
- LOG/SemanticEvents;
- selected MechanicalEvents/receipts;
- canonical entity/lore refs needed for accurate provenance;
- historical knowledge/disclosure evidence needed to compute Story availability;
- existing Story records/indexes for editorial continuity.

Hidden chain-of-thought, internal prompts and private tool reasoning are not participant transcript.

Chronicler writes Story only and never mutates canon through literary inference.

## 10.6 Commentator

Mission: interactive spectator-facing retelling/navigation over Story.

Default context is Story-first and normally Story-only:

- eligible Story records;
- filtered Story indexes/crossrefs;
- spectator session cursor/focus/style/detail/spoiler state.

Commentator does not routinely query unrestricted current WORLD/STATE.

If eligible Story does not establish an answer, Commentator states that the retained Story does not establish it.

A future explicit deep-source/debug mode may traverse provenance into canonical sources; this is a Step-6 mode, not default authority.

---

# 11. Logical typed handoffs

HDM requires typed logical results, not a generic multi-agent message bus.

Conceptual handoffs:

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

Each receiving role receives its independently assembled eligible bundle plus typed prior results.

No handoff is canonical merely by being typed. Only the owning deterministic state transition can commit canonical state.

---

# 12. Historical evidence versus current authority

## 12.1 LOG / SemanticEvent

`runtime.semantic_event` / LOG remains compact durable semantic campaign history.

It may preserve:

- transition summary;
- causal/source refs;
- participant/player attribution;
- material knowledge/disclosure changes;
- chronology evidence;
- mechanical refs where useful.

It is not current-state authority and HDM does not become event-sourced.

## 12.2 Live-scene evidence

Live epoch perception/knowledge evidence remains operationally relevant for live-owned scope under existing LIVE_SCENE semantics.

At durable compaction, material current state normalizes into:

```text
world.knowledge
runtime.disclosure
SemanticEvent history
```

as appropriate.

After handoff, live arrays do not remain a second global current authority.

## 12.3 Transcript evidence

A statement in transcript proves that the statement was said/exposed, not that it is objectively true.

Transcript/SemanticEvent provenance can explain why knowledge/disclosure changed without owning the current relation.

---

# 13. STORY — durable non-canonical presentation/history surface

## 13.1 Campaign layout

One campaign branch contains:

```text
STATE/
WORLD/
LOG/
CHECKPOINTS/
...
STORY/
    TRANSCRIPT/
    EVENTS/
    MECHANICS/
    NARRATIVE/
```

No separate durable spectator branch is part of the default architecture.

Campaign manifest shall eventually expose a `story_root` peer of existing storage roots.

## 13.2 Non-authority

Story is durable but non-canonical.

Deleting Story cannot change world/mechanical truth or recovery state.

However, non-canonical does **not** imply guaranteed byte-for-byte regenerability. If raw messages are later compacted, Story may become the only retained copy of exact dialogue/editorial prose. Losing it harms historical/presentation fidelity without changing canon.

## 13.3 IDs

Story IDs are layer-local:

```text
T001452
E003562
M012644
N000087
```

Rules:

- fixed letter prefix by layer;
- minimum six-digit numeric formatting;
- numeric width is not a hard maximum;
- independent sequence per layer;
- equal numeric suffix across layers has no semantic meaning;
- relations are explicit refs.

## 13.4 One record per file

Default: one independently addressable Story record per file.

Do not introduce multi-record file addressing until measured requirements justify the additional complexity.

## 13.5 Thousand-slot deterministic sharding

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

Shard directories contain records only; indexes/manifests remain at the layer level.

This is a GitHub-aware bounded-directory layout, not a claim of a universal operating-system thousand-file limit.

---

# 14. Story availability model — dependency based, not total chronology

## 14.1 No scalar global reveal frontier

Story spoiler/reveal semantics SHALL NOT introduce a global total world chronology.

A scalar event ID/timestamp cannot determine disclosure eligibility across independent multiplayer scenes.

## 14.2 Availability requirements

Reveal-sensitive Story retrieval units carry dependency/reference-based availability metadata conceptually such as:

```text
availability:
    requires_story_refs[]
    requires_source_refs[]?   # where needed for derivation/audit
```

A record/index entry is eligible only when the active Commentator mode/session considers its required reveal anchors available.

Editorial NARRATIVE ordering may provide a simple linear reading UX but is presentation order, not canonical chronology.

## 14.3 Whole-unit eligibility

Availability applies to the whole retrieved presentation unit, including material:

- body content;
- titles;
- entity refs;
- crossrefs;
- chapter/index entries;
- labels that themselves reveal hidden identities/events.

If one record mixes incompatible availability requirements, split the record rather than introduce field-level redaction in the initial architecture.

## 14.4 Story edit rule

A material Story content/source edit must recompute/revalidate availability requirements before the edited projection is publishable by Story tooling.

Exact Git transaction atomicity belongs to Step 5.

## 14.5 Spectator session state

Commentator session state is non-canonical and may include:

```text
story_cursor
available/revealed Story anchors
focus refs
style/genre
mechanics detail
spoiler policy
```

Exact default spectator perspective/mode belongs to Step 6.

---

# 15. Common Story record principles

Story records carry only metadata useful to presentation/retrieval.

As applicable:

```text
id
source_refs[]
cross_refs[]
entity_refs[]
chronology/source refs[]
availability requirements
content
```

`source_refs` provide traceability to authoritative/historical evidence but do not transfer authority into Story.

Do not copy entire canonical source records into Story for convenience.

---

# 16. `STORY/TRANSCRIPT`

Purpose: retained participant discourse useful for dialogue fidelity and reconstruction.

Default granularity: one visible participant message/utterance per Story record/file.

Conceptually:

```text
id
speaker/participant ref
interaction_id?
runtime_message_ref?
content
source/delivery refs
cross_refs[]
availability requirements
```

Exclude:

- hidden chain-of-thought;
- private tool reasoning;
- internal prompts/runtime plumbing not presented as participant discourse.

Transcript is evidence of what was said, not objective truth.

---

# 17. `STORY/EVENTS`

Purpose: human/LLM-friendly adaptation of LOG/SemanticEvents.

One Story Event is one human-meaningful story beat.

It may:

- summarize several tightly related SemanticEvents;
- split an overloaded source event for presentation;
- use clearer human wording.

It must retain source refs sufficient to trace its factual spine.

It is not used to restore current world state.

---

# 18. `STORY/MECHANICS`

Purpose: curate mechanics real players/spectators commonly track or ask about.

Include when materially useful:

- important check/save/attack/roll result;
- HP/temp-HP changes;
- resource spend/recovery;
- Effect/Condition/LifeState transitions;
- material duration/expiry/recovery information;
- tactically significant movement/range/action-economy facts.

Exclude by default:

- full Actor/Asset/Effect state copies;
- checkpoints;
- dependency DAG/cache internals;
- full contribution stacks/traces when not needed;
- all MechanicalEvents merely because they exist;
- internal resolver bookkeeping without human planning/explanation value.

One Mechanics record represents one human-meaningful mechanical beat, not necessarily one raw MechanicalEvent.

---

# 19. `STORY/NARRATIVE`

Purpose: editable literary prose suitable for coherent reading and later interactive retelling.

Conceptually:

```text
id
content
source_refs[]
transcript_refs[]
event_refs[]
mechanics_refs[]
entity_refs[]
availability requirements
```

NARRATIVE may be rewritten for style, pacing, clarity or literary quality without changing canon.

Unsupported literary inference cannot be restated as factual history.

---

# 20. Chapters are NARRATIVE index grouping

No `world.chapter` or initial `story.chapter` entity exists.

A NARRATIVE index represents chapter grouping conceptually:

```text
chapters:
  - label/number
    title
    part_label?
    synopsis?
    availability requirements?
    narrative_refs:
      - N000001
      - N000004
      - N000006
```

Use explicit ordered N refs, not inferred contiguous numeric ranges.

Reordering, splitting, merging or renaming chapters must not move or rename underlying NARRATIVE records.

Chapter titles/index metadata are themselves subject to Story availability filtering when spoiler-bearing.

---

# 21. Chronicler

Chronicler builds/edits Story from occurred evidence.

It may adapt wording/granularity but must preserve:

- source/provenance traceability;
- factual compatibility;
- claim-versus-truth distinction;
- Story availability requirements.

Chronicler cannot:

- create canon by writing Story;
- change authoritative source state to fit prose;
- include hidden internal reasoning as participant transcript;
- write Dramaturg future preparation as occurred history;
- silently resolve conflicting evidence.

If sources are insufficient/conflicting, Chronicler omits/qualifies the claim or surfaces an editorial/consistency issue.

---

# 22. Commentator

Commentator is the spectator-facing interactive narrator over eligible Story.

It may:

- continue/rewind;
- jump to events/entities/chapters;
- summarize/expand;
- focus on one character/thread;
- change style/genre/tone;
- explain Story Mechanics;
- compare moments;
- answer questions grounded in eligible Story.

It has broad **presentation freedom** and no factual freedom.

If Story does not establish the answer, Commentator says so rather than inventing events, motives, dialogue, mechanics or causal links.

Interpretive commentary may be offered only when clearly framed as interpretation rather than recorded fact.

Default Commentator does not query unrestricted current WORLD/STATE.

---

# 23. Promotion boundary

## 23.1 Non-promoting sources

The following do not become canon merely by existing:

- invocation-adjudicated facts;
- Dramaturg preparation;
- Actor intent/epistemic drafts;
- Narrator prose;
- Chronicler prose;
- Commentator interpretation;
- Story-only labels/mentions.

## 23.2 Proposition promotion threshold

Create/promote `world.lore_fact` when durable canonical consistency requires proposition identity, including when:

- `world.knowledge` must reference the claim durably;
- `runtime.disclosure` must remember material exposure;
- LOG/another canonical record needs durable identity/reference;
- future mystery/history/lore consistency depends on the claim;
- an explicit authorized lore transition commits the proposition.

A previously untracked claim may be promoted as:

```text
truth_status = undetermined
```

so knowledge/disclosure can refer to it without asserting objective truth.

## 23.3 Entity dependency closure

A durable canonical reference to a local/promotable entity is valid only when the same publication closure promotes/publishes the entity and required index entry or rejects the reference.

This reuses existing local-entity promotion/dependency rules rather than introducing a new Step-4 promotion engine.

Story may mention local/noncanonical identities without forcing promotion, but Story-only mention is never canonical identity evidence.

---

# 24. Legacy retirement and migration semantics

## 24.1 Legacy lore status

Legacy `canonical | superseded | disputed_in_world` mixes axes.

Migration separates:

- objective truth;
- lifecycle/supersession;
- in-world disagreement/knowledge.

Do not infer objective truth from `disputed_in_world` without evidence.

## 24.2 Embedded PC/NPC/Faction knowledge

Legacy knowledge/belief/suspicion arrays are migration input.

Material surviving state becomes normalized `world.knowledge` relations.

After migration, embedded arrays cease to be writable current authority.

## 24.3 Player visibility lists

Legacy `private_record_ids` is not equivalent to proposition disclosure.

Use it only as migration evidence where semantics are clear. Do not guess exact human disclosure from path visibility alone.

## 24.4 Secret records

Legacy Secret is decomposed conservatively into its real owners.

Ambiguous truth/knowledge/reveal semantics produce a migration issue rather than invented canonical interpretation.

## 24.5 Chapter retirement

Retire from active catalogs/contracts:

```text
world.chapter
transition.chapter_append
event.chapter.appended
```

Old narrative body/coverage may migrate into non-canonical Story/NARRATIVE/index material, but old Chapter ID is not silently reused as a Story identity.

---

# 25. Context/output failure semantics

At minimum distinguish these conceptual failure classes:

- required source missing -> bounded hydration/retrieval or typed unresolved condition;
- source ineligible for requested role -> exclude or route/block rather than leak;
- mixed/stale canonical frontier -> reassemble from one pinned frontier;
- invalid role-output identity/ref -> deterministic validation failure;
- Narrator disclosure ref not eligible -> correct/regenerate before player-facing emission;
- Actor proposal uses unavailable fact -> reject proposal / diagnose context leak;
- Story factual conflict -> editorial/consistency issue, never canon rewrite;
- Commentator request beyond Story -> state that retained Story does not establish it or use future explicit deep-source mode.

Do not repair information failures by inventing reconciliation prose.

---

# 26. Residual generative limitation

Role-specific context assembly prevents deliberate supply of hidden source material to ineligible roles, but cannot mathematically guarantee that a generative model will never hallucinate an unsupported sentence from its priors.

Therefore:

- material narration should be grounded in eligible structured inputs;
- unsupported factual prose is a correctness error;
- Narrator/Commentator prose is never canonical input for later deterministic state mutation merely because it appeared in chat;
- optional semantic output verification/evaluation may be added in Step 6 without becoming truth authority.

This limitation is model-quality risk, not a reason to weaken information ownership.

---

# 27. Step-5 handoff

Step 5 owns physical persistence/transport consequences, including:

- Story publication batching/tree/CAS mechanics;
- coherent Story record/index/availability updates;
- layer-local Story ID allocation under concurrency;
- transcript/history retention and compaction policy;
- exact response-host delivery acknowledgement;
- checkpoint/publication interactions;
- migration transaction mechanics;
- live-scene compaction transport;
- multiplayer conflict semantics for new Story/index/disclosure files.

Step 5 SHALL NOT reintroduce a separate long-lived spectator/public campaign branch as the default architecture.

---

# 28. Step-6 handoff

Step 6 owns physical LLM orchestration and mode policy, including:

- which logical roles use separate model calls;
- physical role-call compatibility matrix derived from Step-4 source eligibility;
- model selection;
- context reset/isolation mechanisms;
- token/latency/cost budgets;
- preparation caching/retention if justified;
- default Commentator spoiler/perspective mode;
- optional deep-source/debug spectator mode;
- optional narration semantic verification/evaluation.

Step 6 may optimize physical topology but cannot weaken Step-4 role context/authority boundaries.

---

# 29. Canonical Step-4 result

The Step-4 semantic architecture is now:

```text
OBJECTIVE / CURRENT
    ordinary world state owners
    world.lore_fact

PERSPECTIVAL CURRENT
    world.knowledge

HUMAN EXPOSURE
    runtime.disclosure

HISTORY
    runtime.semantic_event / LOG
    runtime.mechanical_event

CONTEXT ROUTING
    deterministic Context Assembler
    six role-specific eligibility envelopes
    typed handoffs, no raw-context inheritance

NON-CANONICAL STORY
    STORY/TRANSCRIPT
    STORY/EVENTS
    STORY/MECHANICS
    STORY/NARRATIVE
    NARRATIVE chapter/index grouping
    dependency-based Story availability

PROMOTION
    explicit durable proposition/entity closure only when canonical references require it
```

Legacy Secret and world Chapter authority are retired.

The next engineering step is to create an implementation plan for catalog/schema/runtime/template/test alignment using `superpowers:writing-plans`, then implement through TDD. No implementation is authorized by this specification alone.
