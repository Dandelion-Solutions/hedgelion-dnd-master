# Step 4 Rerun — Truth, Knowledge, Role Contexts, Story, and Promotion — Research Draft

Status: **RESEARCH / ARCHITECTURE DRAFT — ACCEPTED DECISIONS REVALIDATED / NO NEW OWNER GATE FOUND YET**

Date: 2026-08-20

Task Brief:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-rerun-task-brief.md`

Related accepted-role draft:

- `DEV/docs/superpowers/design/2026-08-20-llm-logical-roles-draft.md`

## 1. Executive finding

The six-role model does not overturn the prior Step-4 Alternative C. It **explains why that split is necessary** and resolves several ambiguities that previously looked like independent design questions.

The recommended information architecture is:

```text
AUTHORITATIVE CURRENT INFORMATION

world/world-state owners
    current physical/mechanical/world facts

world.lore_fact
    durable proposition + objective truth status

world.knowledge
    current in-fiction epistemic relation
    fictional subject -> proposition

runtime.disclosure
    durable human-player exposure relation
    player -> proposition exposure

LOG / runtime.semantic_event
    durable historical/causal evidence

runtime.mechanical_event
    committed mechanical evidence

            |
            v
DETERMINISTIC CONTEXT ASSEMBLER
    role + subject/player + purpose + pinned frontier
    -> bounded role-specific source bundle

            |
            +--> Interpreter
            +--> Dramaturg
            +--> Actor
            +--> Narrator
            +--> Chronicler
            +--> Commentator

History/evidence
    -> Chronicler
    -> STORY/{TRANSCRIPT,EVENTS,MECHANICS,NARRATIVE}
    -> Commentator
```

The most important new architectural rule is:

> **A role may pass another role a typed result, but never implicitly passes the raw private context from which that result was produced.**

This remains true even if Step 6 later implements several logical roles inside one physical model invocation/process. Physical co-location cannot merge logical eligibility.

The six roles also resolve the legacy `Secret.revelation_conditions` ambiguity:

- non-canonical reveal/clue planning belongs to **Dramaturg preparation**;
- mechanically real reveal behavior belongs to the actual Activity/Feature/Effect/Trigger/world owner;
- current fictional cognition belongs to `world.knowledge`;
- human exposure belongs to `runtime.disclosure`;
- no generic Secret authority survives.

Recommendation confidence after rerun research: **HIGH**.

## 2. Verified project facts and constraints

### 2.1 AI correctness policy already requires compartments

`GAME/CORE/AI_REASONING.md` distinguishes canonical, inferred, undefined, unknown-to-runtime, secret and provisional-preparation facts. It explicitly requires separation among objective truth, DM/runtime knowledge, each NPC's knowledge/beliefs/lies, each PC's knowledge/beliefs, and information actually disclosed to each player.

It also requires smallest-needed authoritative context and forbids recent prose from outranking structured state.

The six-role design therefore formalizes existing correctness doctrine rather than introducing a new product requirement.

### 2.2 Player-facing narration is already projection

`GAME/CORE/NARRATIVE.md` states that narration is a projection of resolved state and cannot introduce unresolved material facts. Player agency stops the Master from authoring voluntary PC decisions, beliefs, emotions or speech.

Therefore Narrator cannot be an authority for truth or PC internal belief.

### 2.3 NPC cognition already has its own constraints

`GAME/CORE/AI_REASONING.md` says an NPC is not ChatGPT wearing a costume and constrains response by identity, goals, actual knowledge/beliefs, relationships, resources, incentives, risk tolerance and recent events.

That maps directly onto the accepted Actor logical role. Actor needs a subject-scoped epistemic context, not DM omniscience.

### 2.4 GM craft already separates preparation from future truth

`GAME/CORE/GM_CRAFT.md` says prepare situations rather than a plot. Potential scenes have no right to occur, and likely reactions/clues/pressures are preparation rather than canonical future events.

That maps directly onto Dramaturg. It also explains why generic Secret revelation conditions do not need to become a canonical executable owner when they are merely preparation possibilities.

### 2.5 Current storage is current-state oriented

`GAME/CORE/STORAGE.md` treats campaign Git as a versioned current-state store, keeps LOG as compact semantic history rather than transaction journal/transcript, and requires bounded exact-record retrieval.

Step 4 must not switch HDM to event sourcing or require whole-repository model context.

### 2.6 Legacy schemas still duplicate information ownership

Current PC/NPC/Faction/Secret/Player/live-scene structures contain overlapping knowledge, suspicion, visibility or perception lists while the newer catalog already admits `world.lore_fact` and `world.knowledge`.

These duplicate writes are incompatible with the one-authority invariant and must become migration inputs, transient live evidence, or derived/index projections.

## 3. Revalidated authority model

## 3.1 `world.lore_fact` — durable proposition/truth owner

Do not introduce a generic `world.proposition`; the existing `world.lore_fact` already has the right identity/lifetime role.

Recommended conceptual fields:

```text
fact_id
statement
truth_status = undetermined | established | disproven
record_status = active | superseded
subject_refs[]
scope / chronology when material
provenance_refs[]
superseded_by_fact_id?
importance?
```

### Semantics

- `undetermined` — the proposition has durable identity because claims/knowledge/future consistency may depend on it, but objective truth is not yet established;
- `established` — the proposition is objectively true in its declared scope;
- `disproven` — the proposition is objectively false in its declared scope;
- in-world disagreement is not an objective truth status;
- `canonical` is not a truth value;
- `superseded` is lifecycle/correction metadata, not truth value.

The machine-catalog `disputed` truth status should therefore be retired from the objective-truth axis during Step-4 implementation.

### Ordinary world change versus correction

A proposition must be scoped so ordinary fictional change is not mistaken for retcon.

Example:

```text
"King Arlen is alive during year 912"
```

may remain established even after the king later dies. A correction/supersession occurs only when the prior proposition itself was wrong or replaced as authoritative formulation, not merely because later world state differs.

Current state that already belongs naturally to Actor/Asset/Location/Effect/etc. remains owned there. HDM must not copy every HP/location/door-state value into lore facts. Create a lore proposition only when independent durable propositional identity is needed for knowledge, claims, mystery/history, causal reference or future consistency.

## 3.2 `world.knowledge` — one current fictional epistemic owner

Conceptual identity:

```text
(knower_id, fact_id) -> current epistemic stance
```

Recommended minimal stance vocabulary:

```text
known
believed
suspected
rejected
```

The exact IDs are mechanical follow-through after canonicalization.

Fields may include:

```text
knower_id
fact_id
stance
source_refs[]
confidence?             # optional, not universal
last_changed_event_id?
```

Absence means there is no durably tracked current relation. It does **not** mean false.

Historical acquisition/change belongs to LOG/provenance, not a growing history list inside the current relation.

### Player-character agency constraint

This rerun exposes a necessary refinement:

- the engine may establish that a PC **perceived/received** information through resolved events;
- the engine must not automatically choose a player's voluntary belief, suspicion, rejection or emotional interpretation;
- PC stance changes that represent voluntary interpretation require player-authored evidence interpreted through Interpreter, unless a genuine rules/world mechanism forces the cognitive state;
- NPC/faction stance changes may be proposed by Actor from subject-local evidence and then committed through explicit validated transition.

Thus the same `world.knowledge` owner serves PC/NPC/faction current state while role/agency rules constrain who may propose each transition.

## 3.3 `runtime.disclosure` — durable human exposure owner

The prior Alternative C is strengthened by the role model. Interpreter and Narrator may need to know what the human has already been shown even when the controlled PC does not know it.

Use `runtime.disclosure` as the campaign-durable meta-level owner.

Conceptual identity:

```text
(player_id, fact_id) -> exposure state
```

A minimal useful exposure model is not merely a boolean. It should distinguish at least:

```text
statement_exposed
objective_status_exposed
```

These can be monotonic flags/aspects in one relation.

Why:

- a player may hear that a claim exists without being told whether it is objectively true;
- later OOC truth revelation must be representable without implying the PC knows it;
- exact wording/claim polarity remains available from transcript/provenance when retained;
- the relation need not record every sentence, only exposure whose future context/secrecy correctness may matter.

Once an exposure aspect is delivered to the human, the system cannot make the human unsee it. Fiction may later change PC knowledge, but disclosure remains historical human exposure.

### Narrator recording rule

Do not reconstruct durable disclosure later by attempting deterministic NLP over arbitrary narration prose.

Narrator output should conceptually include:

```text
NarrationResult
    prose
    disclosed_fact_refs[]
        fact_id
        exposure_aspect
```

The host/core validates that each declared disclosure was eligible in the NarrationBundle and records it after successful delivery. This is evidence bookkeeping, not a second narration authority.

The absence of an explicit disclosure ref does not make hallucinated prose safe; the primary leak prevention remains that Narrator never receives ineligible hidden source facts.

## 4. Secret is contextual, not an authority class

The six roles remove the last practical justification for a generic Secret record.

A fact is secret relative to a context when the objective proposition exists but the relevant subject/player/role context lacks authorization/knowledge/disclosure to receive its material content.

Legacy Secret responsibilities split as follows:

```text
objective truth
    -> world.lore_fact / ordinary world owner

who knows/believes/suspects
    -> world.knowledge

what a human player has been shown
    -> runtime.disclosure

reveal/clue ideas
    -> Dramaturg non-canonical preparation

real automatic discovery/reveal mechanics
    -> actual Activity/Feature/Effect/Trigger/world owner

thread linkage
    -> existing Thread/relationship/ordinary refs when actually needed
```

`WORLD/SECRETS` therefore becomes legacy layout, not a required new-campaign authority root.

## 5. Context Assembler — new cross-cutting deterministic capability

## 5.1 Why it is needed

A prompt-level rule such as "do not reveal secrets" is insufficient if a player-facing role receives all DM truth. Conversely, full physical process isolation is not guaranteed because Step 6 may co-locate roles for latency/cost.

The architecture therefore needs a deterministic logical capability that constructs **role-specific bounded source bundles**.

This capability is called **Context Assembler** in the specification. It is not an LLM role, not a canonical record and not a generic ACL engine.

## 5.2 Logical request

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
    subject_id?          # Actor subject
    story_cursor?        # Commentator
    requested refs / bounded search intent?
```

The assembler resolves only the role-relevant bounded dependency set and returns source identity/provenance with the bundle.

## 5.3 Cross-role rule

A role consumes its own assembled bundle plus typed prior-role results.

It does **not** receive another role's source bundle by transitive inheritance.

Example:

```text
DramaturgContext
    includes true murderer
        -> PreparationDraft

later:
NarratorContext
    excludes true murderer
    includes only settled observable consequence
    + safe Preparation-derived cue if independently eligible
```

Even if the same physical model process performs both roles, the host must treat the logical phases as separate eligibility envelopes. Step 6 may choose true isolated calls where available, but Step 4 correctness does not depend on that optimization.

## 6. Role-by-role information contract

## 6.1 Interpreter

Purpose:

- understand external language, references, intent and bounded fiction-dependent invocation facts.

May receive:

- current user message;
- bounded recent discourse;
- authenticated player/PC/session identity;
- player disclosure needed to understand OOC references;
- PC-eligible scene/knowledge candidates;
- host-supplied entity/activity candidates;
- for one registered invocation fact, the smallest authoritative slice required to judge that fact.

Must not receive unrestricted DM truth.

Important distinction:

Interpreter may understand that the **human player** refers to an OOC-known secret while still annotating that the controlled PC lacks that knowledge. Understanding a reference is not authorization for the PC to act as if they know it.

Output remains Step-3 bounded interpretation/invocation facts and is revalidated by deterministic machinery.

## 6.2 Dramaturg

Purpose:

- private GM preparation, pressures, clue routes, possible manifestations, near-horizon developments if unopposed.

May receive the broadest DM information set when relevant:

- objective truth and undetermined propositions;
- hidden facts;
- NPC/faction goals/resources/knowledge summaries;
- active threads/processes;
- cross-player objective developments;
- player interests and disclosure state where useful to avoid redundant/incorrect reveal planning;
- tone/boundaries and existing preparation.

Output is **PreparationDraft**, not future canon.

No prepared scene/event has a right to occur.

### Preparation persistence

Do not introduce a new canonical preparation owner in Step 4.

Preparation may be ephemeral/soft/non-canonical host material. Step 6 may later define retention/caching if useful. Any prepared proposition/entity that becomes required by canonical future consistency must cross the normal promotion boundary before canonical reference.

## 6.3 Actor

Purpose:

- reason about non-formalizable intent/cognition for one NPC/faction/world subject.

May receive only subject-relevant:

- identity/traits/goals;
- subject `world.knowledge` relations;
- currently observable scene facts;
- relationships/resources/capabilities the subject can know/use;
- recent known events and commitments.

Must not receive DM-only truth merely because Dramaturg knows it.

Output may include:

```text
ActorIntentDraft
EpistemicDeltaDraft?     # when new evidence plausibly changes subject stance
SpeechIntent?
```

These are proposals. Mechanical actions and durable knowledge changes commit only through explicit validated core/world transitions.

## 6.4 Narrator

Purpose:

- current player-facing Master prose.

May receive:

- current PC perception/knowledge eligible for narration;
- relevant player disclosure;
- newly settled observable consequences;
- authorized Actor speech/actions;
- settled mechanical receipts at requested detail;
- tone/pacing context;
- explicitly safe preparation cues whose content is independently eligible.

Must not receive raw Dramaturg context, raw hidden adjudication context, or unrelated DM truth.

Output:

```text
NarrationResult
    prose
    disclosed_fact_refs[]
```

Narration is presentation, not canon creation.

## 6.5 Chronicler

Purpose:

- transform occurred evidence into durable non-canonical Story material.

May receive broader historical sources than Narrator because it is not a player-facing gameplay call:

- retained participant messages;
- SemanticEvents / LOG;
- selected MechanicalEvents/receipts;
- canonical entity/lore refs needed for coherence/provenance;
- knowledge/disclosure history needed to mark reveal eligibility;
- existing Story records for continuity/editorial work.

It does not receive hidden chain-of-thought/tool reasoning as transcript material.

Output is Story records/index updates only. Story never mutates canon.

## 6.6 Commentator

Purpose:

- interactive guest/spectator retelling and navigation.

Default source boundary:

- `STORY` first and normally `STORY` only;
- session-local story cursor/focus/style/detail/spoiler policy;
- no unrestricted current WORLD/STATE lookup in ordinary spectator mode.

Commentator may reorder presentation, rewind, compress, expand, change genre/style, explain mechanics and answer questions, but may not invent unsupported events/motives/dialogue/mechanics/causality.

Exact default spectator perspective/spoiler mode can remain a Step-6 mode-profile decision provided Step 4 supplies enough record metadata to enforce a chosen frontier.

## 7. Typed handoffs

The architecture needs logical typed handoffs, not a generic multi-agent bus.

Conceptual examples:

```text
Interpreter
    -> InterpretationDraft / accepted invocation facts

Dramaturg
    -> PreparationDraft

Actor
    -> ActorIntentDraft / optional EpistemicDeltaDraft

Core
    -> NarrationBundle

Narrator
    -> NarrationResult + disclosure refs

Core/history
    -> StorySourceBundle

Chronicler
    -> Story records/indexes

Story retrieval
    -> SpectatorStoryBundle

Commentator
    -> guest-facing prose
```

The host may optimize physical calls later, but only these role-appropriate results cross logical role boundaries.

## 8. Historical evidence versus current knowledge

Keep useful immutable evidence without allowing it to become a second current owner.

Examples:

- live `perceived_by_pc_ids` records epoch-local observation evidence;
- SemanticEvent may record knowledge/disclosure changes and participants;
- transcript records what was actually said;
- NarrationResult disclosure refs record what the host intended/delivered as player exposure;
- `world.knowledge` remains the current durable fictional relation;
- `runtime.disclosure` remains the current durable player exposure relation.

At live compaction, applicable live evidence produces normalized durable relations plus SemanticEvent history. The live lists do not survive as a parallel current global authority.

## 9. STORY architecture

## 9.1 Authority invariant

`STORY` is durable but non-canonical.

Deleting or corrupting Story cannot change current world/mechanics/recovery authority. However **non-canonical does not mean byte-for-byte regenerable**: if raw runtime messages are later compacted, a Story Transcript record may become the only retained copy of exact dialogue. Losing it loses presentation/history fidelity without changing canon.

This distinction corrects an overstrong earlier assumption that all Story must always be fully regenerable.

## 9.2 Physical shape

Accepted initial structure:

```text
STORY/
    TRANSCRIPT/
    EVENTS/
    MECHANICS/
    NARRATIVE/
```

Layer-local IDs use a minimum six-digit numeric sequence and fixed letter prefix:

```text
T001452
E003562
M012644
N000087
```

One record per file by default.

Deterministic thousand-slot sharding:

```text
STORY/EVENTS/003/E003562.yaml
STORY/MECHANICS/012/M012644.yaml
```

The shard derives from `floor(sequence / 1000)`, formatted with minimum width three. Numeric width is a minimum rather than a hard maximum, avoiding an artificial million-record ceiling.

## 9.3 Common Story record metadata

Each Story record should carry only presentation/retrieval metadata needed by its layer, including as applicable:

```text
id
source_refs[]
cross_refs[]
entity_refs[]
chronology/event refs
reveal_frontier / availability refs
content
```

Do not copy whole canonical records.

## 9.4 TRANSCRIPT

Default unit: one retained participant message/utterance record per file.

Purpose:

- dialogue fidelity;
- reconstruction;
- evidence of what was actually said/shown.

May reference source `runtime.message`/interaction when retained.

Exclude hidden chain-of-thought, private tool plumbing and internal runtime prompts.

A Transcript statement is not objective truth merely because a participant said it.

## 9.5 EVENTS

Purpose: human/LLM-friendly adaptation of LOG/SemanticEvents.

A Story Event represents one human-meaningful story beat. It may summarize several tightly related SemanticEvents or split a semantically overloaded source for presentation, but it must retain source refs.

It is not used to restore world state.

## 9.6 MECHANICS

Purpose: curated mechanics that players/spectators commonly track or ask about.

Typical inclusions:

- important roll/check/save/attack and result;
- HP/temp-HP changes;
- resource spend/recovery;
- Effect/Condition/LifeState transitions;
- meaningful duration/expiry/recovery;
- tactically meaningful movement/range/action-economy facts.

Exclude full state copies, checkpoint contents, dependency DAG/cache internals, complete trace/contribution stacks, and mechanically irrelevant runtime plumbing.

One Story Mechanics record represents one human-meaningful mechanical beat, not necessarily one raw MechanicalEvent.

## 9.7 NARRATIVE

Purpose: editable literary prose with explicit source/cross-layer refs.

A NARRATIVE record is independent from chapter grouping and may be rewritten for literary quality without mutating canon.

### Chapter index

Use NARRATIVE index metadata such as:

```text
chapter number/title
ordered N-record refs[]
optional part label
optional synopsis
```

Do not assume chapter membership is a contiguous numeric range; explicit ordered refs allow later insertion/reorganization without moving/renaming records.

No `world.chapter` or `story.chapter` entity is required initially.

## 9.8 Reveal/spoiler frontier

Interactive Commentator use exposes a subtle issue: a NARRATIVE record may later be edited using knowledge revealed after the historical events it describes. A guest rewinding to an earlier point must not automatically receive future spoilers merely because the current literary record was rewritten later.

Therefore Story records that can contain reveal-sensitive material need record-level **availability/reveal-frontier metadata** derived by Chronicler from their claims/source history.

Initial rule:

- record is eligible at a spectator frontier only when all material claims it contains are available under that frontier/perspective;
- if one record mixes claims with incompatible reveal eligibility, split the record rather than invent field-level redaction;
- Commentator's session-local cursor/spoiler policy determines which eligible records are assembled;
- exact default spectator mode belongs to Step 6.

This is a semantic presentation boundary, not repository security.

## 10. Promotion closure

## 10.1 Invocation/preparation does not imply canon

Step-3 invocation facts, Dramaturg preparation, Actor intent proposals, Narrator prose and Story prose do not become durable truth merely because they existed or were useful.

## 10.2 Promote only when durable canonical consistency requires identity

Create/update a `world.lore_fact` when:

- a proposition must be referenced durably by `world.knowledge`, `runtime.disclosure`, LOG or another canonical record;
- future world consistency materially depends on remembering the proposition;
- a mystery/history/claim needs stable referential identity across sessions;
- an accepted explicit lore transition commits it.

A previously untracked claim can be promoted with `truth_status=undetermined` so knowledge/disclosure can refer to it **without asserting that it is true**.

Later evidence may establish/disprove it.

## 10.3 Entity dependency closure

If a durable lore/knowledge/disclosure/LOG reference points to a local entity, the same publication closure must promote/publish the entity and required index entry or reject the durable reference.

Story may mention a local/noncanonical label without promotion, but Story-only mention cannot later be treated as canonical identity evidence.

## 11. Alternatives and analytical challenge

## 11.1 One omniscient LLM context

Benefit: simplest prompt plumbing.

Failure: Actor inherits DM knowledge, Narrator leaks secrets, Commentator sees unrestricted world truth, and physical role co-location silently becomes semantic authority merging.

Reject.

## 11.2 Prompt-only secrecy with all data loaded

Benefit: minimal deterministic context logic.

Failure: depends on the same generative model that creates prose to remember which of many loaded facts it must not use; contradicts current smallest-working-set policy and makes accidental leakage likely.

Reject.

## 11.3 Deterministic role-specific source eligibility + typed handoffs

Adds a Context Assembler capability and bounded bundle definitions but does not create new canonical owners or a general ACL framework.

Recommend.

## 11.4 Universal `world.knowledge` including PLAYER disclosure

Still viable in abstract, but six roles make the weakness clearer: Interpreter/Narrator need meta-level human exposure while Actor needs fictional cognition. Combining them increases the chance of scope confusion and gives a `world.*` record non-world semantics.

Keep separate `runtime.disclosure`.

## 11.5 Persistent Secret wrapper

Six-role preparation/context routing eliminates its remaining value. It would duplicate truth/knowledge or become a generic reveal-policy object with unclear ownership.

Reject.

## 11.6 Commentator with direct canonical WORLD access

Benefit: can answer any deep question.

Failure: undermines Story as spectator/read surface, expands hidden-context exposure, couples spectator UX to current engine layout and makes literary rewind/spoiler behavior difficult.

Default reject. Future explicit debug/deep-source mode may traverse provenance when intentionally requested.

## 11.7 Multi-record Story containers

Benefit: fewer files.

Cost: internal addressing, append conflicts, partial rewrites, cross-reference complexity and less independent retrieval.

No current scale evidence justifies it. Keep one record per file.

## 11.8 Persist all Dramaturg preparation

Benefit: continuity of planning.

Failure: grows stale noncanon, tempts later roles to treat prep as truth, adds another lifecycle/cleanup subsystem and conflicts with existing guidance not to preserve obsolete prep merely because it consumed context.

Reject as a Step-4 requirement. Retention/caching may be introduced later only when measured benefit exists.

## 12. Failure-scenario pass

### 12.1 Same physical call performs Dramaturg then Narrator

Risk: DM truth remains in model context.

Required architecture: logical role phases use separately assembled eligibility bundles; raw Dramaturg source context is not an allowed Narrator input. If the platform cannot provide meaningful context isolation inside one invocation, Step 6 must choose separate calls for those roles. The logical contract remains unchanged.

### 12.2 Player knows OOC secret, PC does not

`runtime.disclosure` records player exposure. `world.knowledge(PC, fact)` remains absent. Interpreter can understand OOC references, but binder/Narrator cannot treat the PC as informed without fictional knowledge/explicit OOC mode.

Pass.

### 12.3 PC learned something while player was absent

`world.knowledge(PC,fact)` exists; player disclosure may be absent. At next eligible narration, Narrator can tell the player what their PC knows and then record disclosure.

Pass.

### 12.4 NPC hears a convincing lie

Fact proposition may be `disproven` objectively while Actor proposes `believed` for NPC based on testimony. Objective truth does not change.

Pass.

### 12.5 Player refuses to believe a rumor

Receiving a claim can create awareness/source evidence, but engine does not silently set voluntary PC belief. Interpreter may capture an explicit player-authored rejection/suspicion if material.

Pass.

### 12.6 Rewritten early NARRATIVE contains later reveal

Chronicler updates/splits the record and sets reveal frontier no earlier than the later reveal. Commentator rewinding before that frontier cannot retrieve the spoiler-sensitive record.

Pass, provided record-level reveal metadata is implemented.

### 12.7 Story deleted after runtime messages compacted

Canon/recovery remains intact, but exact dialogue/literary editing may be lost. This is acceptable because Story is noncanonical, but must not be falsely advertised as fully regenerable.

Pass with explicit documentation.

### 12.8 Prepared clue never used

No canonical effect; preparation may expire/disappear. No cleanup of world truth is needed because it was never canon.

Pass.

### 12.9 Durable knowledge needs an untracked rumor

Create a stable `world.lore_fact` with `undetermined`; create knowledge relation to it. This records the claim without asserting truth.

Pass.

### 12.10 Live-scene perception compacts

Epoch-local perception evidence produces durable `world.knowledge`/`runtime.disclosure` only where persistence matters plus SemanticEvent evidence. Live arrays cease to be current authority after compaction.

Pass.

## 13. Strongest objection to the recommended architecture

The normalized model introduces more records/lookups than embedded knowledge arrays, and role-specific context assembly introduces more orchestration than one omniscient model prompt. A simple system could load NPC/PC records plus all nearby lore and rely on prompt discipline.

### Response

The extra complexity corresponds to already accepted semantic distinctions that materially affect correctness:

- human player versus controlled PC;
- NPC local cognition versus DM truth;
- preparation versus canon;
- player-facing Narrator versus private Dramaturg;
- Story author versus Story consumer.

HDM already has bounded indexes/hydration and explicitly rejects whole-campaign preload. Context Assembler is a narrow deterministic selector, not a new graph/ACL platform. The cost is therefore bounded and directly buys correctness.

## 14. Simplest viable design check

The recommendation intentionally does **not** add:

- a Secret entity;
- a generic knowledge graph;
- a generic context-policy language;
- a seventh LLM role;
- a multi-agent bus;
- per-NPC permanent agents;
- field-level Story redaction;
- public/spectator branch;
- universal preparation database;
- event-sourced current state.

The minimum new semantic machinery is:

```text
world.lore_fact
world.knowledge
runtime.disclosure
Context Assembler capability
role-specific typed handoff contracts
four Story layer schemas + indexes
promotion rules
```

## 15. Assumption/evidence ledger

### A1 — Role set is logical, not physical

Confidence: HIGH.

Evidence: owner-approved six-role draft and Step-6 ownership of call topology.

Impact if false: physical agent requirements move earlier and Step 4 would need deployment/cost semantics.

Revisit: only if a platform limitation makes role context isolation impossible without fixing physical topology now.

### A2 — Player disclosure is sparse

Confidence: HIGH.

Evidence: existing INFORMATION policy says persist distinctions only when future play may depend; recording every sentence would be unnecessary telemetry.

Impact if false: relation count grows, but authority design still holds.

### A3 — Record-level Story reveal metadata is sufficient initially

Confidence: MEDIUM-HIGH.

Evidence: Story records are already designed to be small/independently addressable and can be split when claim eligibility differs.

Impact if false: field-level claim segmentation may be needed later.

Revisit: if real narrative records routinely require mixed reveal eligibility that cannot be split without harming readability/retrieval.

### A4 — Commentator can be Story-first by default

Confidence: HIGH for architecture; exact default mode MEDIUM.

Evidence: owner explicitly defined Commentator as reading Story and interactively retelling it.

Impact if false: an explicit debug/deep-source spectator mode may need canonical provenance traversal.

Revisit: Step-6 mode design.

## 16. Recommendation and what would change it

Recommendation confidence: **HIGH**.

Proceed to candidate specification with:

1. `world.lore_fact` normalized proposition/truth authority;
2. `world.knowledge` sole durable current fictional epistemic authority;
3. separate `runtime.disclosure` human exposure authority;
4. no independent Secret owner;
5. deterministic role-specific Context Assembler;
6. typed results across role boundaries, never raw private-context inheritance;
7. six logical role context envelopes as specified above;
8. four-layer noncanonical Story surface with independent IDs, one-file records, thousand-slot sharding, provenance/crossrefs and reveal frontier metadata;
9. Chapter as NARRATIVE index grouping;
10. explicit minimal promotion closure;
11. Step-5/6 deferrals for physical publication and LLM call topology.

Evidence that would change the recommendation:

- a concrete requirement that player disclosure and fictional cognition must share identical lifecycle/queries;
- a demonstrated need for Secret as an independent lifecycle owner after truth/knowledge/preparation split;
- a platform constraint proving role contexts cannot be isolated except by a materially different architecture;
- measured Story workloads showing one-record-per-file or record-level reveal metadata is unworkable;
- a gameplay requirement that durable preparation itself must be canonical authority.

No such evidence was found in the current repository or accepted owner decisions.
