# Step 4 — Lore, Knowledge, Disclosure, Story Projection, and Promotion — Research Draft

Status: **RESEARCH / ARCHITECTURE DRAFT — HUMAN DECISION REQUIRED BEFORE CANDIDATE SPEC**

Task Brief:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-lore-knowledge-story-task-brief.md`

Target branch: `feature/mechanical-runtime-hot-state`

## 1. Executive finding

The existing architecture contains the right high-level distinctions but several early schemas duplicate ownership:

- objective truth exists in `lore.schema.yaml`, `secret.schema.yaml`, and the newer `world.lore_fact` catalog concept;
- current knowledge/belief is embedded in PC/NPC/Faction schemas, duplicated in Secret known/suspected lists, and separately represented by the newer `world.knowledge` catalog concept;
- player disclosure/visibility is partly stored in player records, SemanticEvent visibility metadata, and live-scene perception data;
- old `world.chapter` machinery was an early attempt to build a book-like history and has no independent world-state responsibility that survives the accepted `STORY/NARRATIVE` design.

The core recommendation is therefore **normalization by semantic lifetime**, not a new generic knowledge graph:

```text
objective proposition / truth
    -> world.lore_fact

in-fiction current epistemic state
    -> world.knowledge

human-player disclosure state
    -> separate campaign-durable runtime.disclosure relation

historical evidence of observation/disclosure/change
    -> LOG / SemanticEvents / transcript refs

non-canonical reconstruction/presentation
    -> STORY/{TRANSCRIPT,EVENTS,MECHANICS,NARRATIVE}
```

`Secret` should cease to be an independent truth/knowledge owner. Secrecy becomes contextual: a proposition may be established objective truth while absent from a particular character/player context. Mechanically meaningful revelation behavior, when proven, belongs to the actual rule/world owner rather than to a generic Secret callback object.

Confidence before human gate: **HIGH** on truth/knowledge normalization and retirement of old Chapter; **MEDIUM-HIGH** on the separate `runtime.disclosure` class because it adds one class but preserves a real player-vs-PC semantic distinction.

## 2. Verified repository facts

### 2.1 Accepted reasoning policy already separates truth and perspective

`GAME/CORE/INFORMATION.md` requires explicit separation among objective truth, NPC knowledge, NPC false beliefs, PC knowledge, and information actually told to players. Knowledge requires a source and may be wrong without changing objective truth.

`GAME/CORE/AI_REASONING.md` separately classifies canonical, inferred, undefined, unknown-to-runtime, secret, and provisional-prep information. A fact loaded for adjudication does not become narratable.

`GAME/CORE/LORE.md` requires objective history to remain distinct from official accounts, faction claims, NPC belief, rumor/myth/propaganda, and PC learning.

These are strong semantic constraints; Step 4 should formalize them rather than invent another model.

### 2.2 Existing truth representations conflict

`GAME/SCHEMA/lore.schema.yaml`:

```text
status = canonical | superseded | disputed_in_world
```

The newer Step-1 catalog registers:

```text
truth_status = undetermined | established | disputed | disproven
```

and `world.lore_fact` requires `statement + truth_status`.

The two vocabularies mix three different axes:

- durable/canonical record status;
- objective truth value;
- in-world disagreement.

### 2.3 Existing knowledge is multiply owned

Writable current knowledge/belief currently appears in:

- PC `knowledge.known_fact_ids / belief_records / discovered_location_ids`;
- NPC `knowledge.known_fact_ids / beliefs / suspicions`;
- Faction `knowledge.known_fact_ids / beliefs`;
- Secret `known_by_entity_ids / suspected_by_entity_ids`;
- Player `visibility.private_record_ids`;
- live-scene `live_facts.known_by_pc_ids` and observable-event perception;
- the newer Step-1 `world.knowledge` record kind.

This is a direct duplicate-authority problem if these are all persisted as current truth.

### 2.4 Existing history evidence need not be current knowledge authority

`event.schema.yaml` may record visibility/player IDs and `knowledge_changes` as historical facts.

`live_scene.schema.yaml` records which PCs perceived a live event and which PCs know an epoch-local fact. During an active live epoch this is the operational source for the live-owned scene scope; on compaction it can produce durable knowledge/disclosure updates.

These facts can remain immutable provenance/evidence without also being the current global knowledge owner.

### 2.5 Secret schema currently mixes four responsibilities

`secret.schema.yaml` owns:

1. objective `truth`;
2. known/suspected subject lists;
3. revelation conditions;
4. thread/event linkage.

The first two conflict with normalized proposition/knowledge ownership. The third may be either preparation guidance or real rules behavior and therefore cannot safely remain an untyped generic callback surface.

### 2.6 Old Chapter has no independent world responsibility

Current inventory gives `world.chapter` only narrative/history fields: title/body, entity/scene refs, timeline span, visibility. Historical design notes add order, event frontier, source checkpoint/revision, and text body.

No mechanics, recovery, chronology authority, or independent gameplay lifecycle depends on Chapter. The owner has confirmed it was an early seed for the book-like story function now moving under `STORY/NARRATIVE`.

## 3. External sanity checks

### 3.1 Provenance

W3C PROV-O separates entities, activities, agents and derivation/attribution relationships. HDM does not need PROV-O itself, but the useful applicable pattern is narrow:

> store provenance as references to the source/event/activity/agent responsible for a claim or projection; do not copy the claim into a second provenance-owned truth record.

Source: W3C Recommendation `PROV-O: The PROV Ontology`.

### 3.2 Unknown is not false

The W3C OWL 2 Primer explicitly contrasts ordinary closed-world database reasoning with open-world semantics where absence may mean unknown rather than false.

HDM is not adopting OWL. The applicable lesson is already an HDM invariant: missing/undefined/unknown evidence must not be silently interpreted as false.

Source: W3C Recommendation `OWL 2 Web Ontology Language Primer`.

### 3.3 Projection versus authority

Microsoft's Event Sourcing/CQRS guidance distinguishes an authoritative write model/event store from query-optimized materialized views and warns that full event sourcing adds substantial complexity and long-term constraints.

HDM should reuse only the projection lesson:

> STORY can be a durable, replaceable read/presentation model without making LOG the universal source of current world state.

Current world records remain current-state authority; LOG remains compact semantic history; STORY remains non-canonical.

## 4. Objective proposition model

### 4.1 Alternatives

#### T1 — Introduce a new `world.proposition`

Pros:
- semantically clean name for true, false, or unresolved claims.

Cons:
- new class plus migration;
- duplicates the role already assigned to `world.lore_fact` by the Step-1 catalog;
- little behavioral benefit.

**Reject: unnecessary class churn.**

#### T2 — Keep `world.lore_fact` as the durable proposition/truth owner

The existing catalog already describes it as a canonical proposition with truth status. Keep the machine ID and clarify the contract:

```text
statement
truth_status = undetermined | established | disproven
lifecycle = active | superseded          # exact machine spelling later
subject_ids / chronology / importance
provenance refs
supersession refs when applicable
```

Interpretation:

- `undetermined` = proposition exists as a durable claim/question but objective truth has not been established;
- `established` = objective truth is true in its declared scope;
- `disproven` = objective truth is false in its declared scope;
- in-world disagreement is **not** an objective truth status;
- `canonical` is not a truth value; canonicality/durability is a different axis;
- `superseded` is record lifecycle/repair, not truth value.

A transition `undetermined -> established|disproven` may occur when the world actually establishes the answer. A correction/retcon of an already established proposition must be explicit and traceable, never a silent wording rewrite.

**Recommend T2.**

#### T3 — Store truth only in arbitrary world entity fields

Fails for historical, relational, causal, cultural, identity, mystery and belief-referenced propositions that do not naturally belong to one entity field.

**Reject.**

### 4.2 Why `disputed` leaves objective truth status

Repository policy already says contradictory legends/accounts can coexist while objective history remains one thing or remains undefined. Therefore:

- disagreement among subjects belongs to knowledge/belief relations;
- lack of established answer is `undetermined`;
- a corrupted/contradictory canonical store is an integrity problem, not a valid `disputed` objective state.

## 5. In-fiction knowledge model

### 5.1 Required semantics

We need current perspectival state such as:

```text
PC_A knows P
NPC_B believes P
Faction_C suspects P
NPC_D rejects P
```

where proposition P may independently be established, disproven, or undetermined.

Knowledge requires provenance/source when material. Current state and historical acquisition are separate: LOG/event evidence can preserve how a relation changed without forcing the current Actor/Faction record to carry history.

### 5.2 Alternatives

#### K1 — Keep embedded knowledge arrays in every owner

Pros:
- direct local reads;
- familiar document shape.

Cons:
- four or more schemas duplicate semantics;
- difficult provenance and lifecycle consistency;
- updates contend with unrelated Actor/Faction state;
- reverse lookup is expensive;
- Secret known/suspected lists create another copy;
- no clean player-vs-PC boundary.

**Reject.**

#### K2 — One normalized `world.knowledge` current relation

Conceptual identity:

```text
(knower_id, proposition_id) -> current epistemic stance
```

Initial stance vocabulary should be closed and small, e.g.:

```text
known
believed
suspected
rejected
```

Exact machine names belong to specification/TDD after approval.

Possible fields:

```text
fact_id / proposition_id
knower_id
stance
source/provenance refs
confidence?              # only where meaningful
last_changed_event_id?
```

Absence means no durable tracked relation; HDM does not create `unknown` rows for every possible subject/fact pair.

Embedded PC/NPC/Faction knowledge fields become migration inputs and then disappear as writable authority. HOT indexes may project `knowledge by knower` or `knowers by proposition` for bounded retrieval.

**Recommend K2 for in-fiction knowledge.**

## 6. Player disclosure is not PC knowledge

This is the main material ownership question.

A human player may:

- be told something OOC that no controlled PC knows;
- control several PCs with different knowledge;
- learn a fact through one PC while another PC remains ignorant;
- retain knowledge even if a PC later forgets through fiction/magic;
- have been shown a proposition in a prior message even when the current PC context does not include it.

Disclosure to a human is also effectively monotonic: the system cannot make the human *unsee* information, even if it later stops presenting it.

That lifecycle is materially different from in-world knowledge/belief.

### 6.1 Alternatives

#### D1 — Treat PLAYER as another `world.knowledge.knower_id`

Pros:
- one record kind;
- minimal registry growth.

Cons:
- mixes meta-level human exposure with fictional cognition;
- `world.*` now owns non-world UI/user state;
- stance/lifecycle differ (`disclosed` is not `known/believed/suspected`);
- easy for queries to accidentally turn player knowledge into PC knowledge.

**Not recommended.**

#### D2 — Keep disclosure as arrays on PLAYER records

Pros:
- no new record class.

Cons:
- one increasingly large mutable list per player;
- poor provenance;
- unrelated disclosures contend on one file;
- current `private_record_ids` is record/path oriented rather than proposition oriented;
- awkward multiplayer incremental updates.

**Reject.**

#### D3 — Separate campaign-durable `runtime.disclosure` relation

Conceptual identity:

```text
(player_id, proposition_id) -> disclosed
```

Properties:

- meta-level, not fictional cognition;
- durable campaign state because future narration/context filtering depends on it;
- normally monotonic once disclosed;
- provenance may reference message/event/interaction that performed the disclosure;
- does not imply any PC knows the proposition;
- can be indexed by player or proposition;
- ordinary unimportant prose does not need a disclosure record; only persist disclosure when future secrecy/context correctness may depend on it.

The exact runtime/world classification and machine ID is a material decision because it changes the class inventory. **Current recommendation: D3 / `runtime.disclosure`.**

## 7. What happens to `Secret`

### 7.1 Alternatives

#### S1 — Keep current Secret entity

Fails because `truth` and known/suspected lists duplicate proposition/knowledge authority. Generic `revelation_conditions` are also too weakly typed to own executable behavior safely.

**Reject.**

#### S2 — Redesign Secret as a pure wrapper around a proposition

For example:

```text
secret -> proposition_id + reveal policy
```

This removes truth duplication but still introduces an entity whose only purpose is to say that another fact is currently restricted. Since secrecy varies by subject/player, it is not one global lifecycle property.

**Usually redundant; not recommended.**

#### S3 — No independent Secret authority

A "secret" is a contextual classification:

```text
objective proposition exists
AND target context lacks the relevant knowledge/disclosure
```

If a reveal mechanism is merely GM preparation, keep it as preparation rather than canon. If it is mechanically automatic, the actual Feature/Effect/Activity/Trigger/world owner holds the rule. Clues/documents/observations remain ordinary sources that can cause knowledge/disclosure transitions.

`WORLD/SECRETS` becomes legacy storage organization rather than an authority surface and should not survive as a required new-campaign root unless a later concrete storage need appears.

**Recommend S3.**

## 8. Historical visibility/perception remains evidence

The normalized model does **not** delete useful event evidence.

Examples:

- live `observable_event.perceived_by_pc_ids` records who perceived an epoch event;
- a SemanticEvent may record who was exposed to an event at commit time;
- transcript records what was actually said to a player;
- knowledge/disclosure transition events preserve causal history.

These are immutable historical facts. They can generate/update current `world.knowledge` / `runtime.disclosure`, but are not themselves the sole current query authority.

At live-epoch compaction:

```text
live perception/knowledge evidence
    -> durable proposition promotion if required
    -> world.knowledge updates
    -> runtime.disclosure updates where actual human disclosure occurred
    -> SemanticEvent/history evidence
```

No duplicate current list remains on Actor/Faction/Secret.

## 9. LLM context architecture

### 9.1 Context eligibility, not repository secrecy

The repository may physically contain objective secrets. The context assembler decides which information enters a given working context.

Recommended logical request classes:

```text
ADJUDICATION
NPC_COGNITION
PLAYER_NARRATION
STORY_RECONSTRUCTION
```

Exact machine names are deferred.

### 9.2 Required separation

#### Adjudication

May retrieve hidden objective truth **only when materially required** to resolve the action/world state.

#### NPC cognition/speech

Receives the NPC's knowledge/beliefs/suspicions plus currently observable information, not unrestricted DM truth.

#### Player narration

Receives information legitimate for the current PC/player plus newly resolved observable consequences and settled mechanical receipts. A fact needed privately for adjudication is not automatically copied into this view.

#### Story reconstruction

Uses allowed STORY records plus authorized source evidence as requested. STORY is never used to adjudicate current canon.

### 9.3 Important limitation

This is an accidental-leak/correctness boundary, not cryptographic isolation from a model that has already been shown a secret. HDM therefore prioritizes:

- do not preload restricted campaign information wholesale;
- retrieve hidden truth only when required;
- do not retain raw private material in broad conversation summaries/context;
- rebuild the player-facing/narration bundle from authorized information rather than asking the model to "remember not to mention" everything it saw.

Where the host/platform can perform genuinely isolated model calls, a private adjudication call may return only a typed/sanitized result to the narration call. Step 4 should not require such a platform feature for correctness of canonical mechanics.

## 10. Semantic LOG versus STORY

### 10.1 LOG remains its current authority

`LOG` / `runtime.semantic_event` remains compact durable campaign-history evidence/projection. It is not current-state authority and is not a transcript.

HDM must **not** switch to full event sourcing in Step 4. Current state remains in world/state owners.

### 10.2 STORY is a replaceable presentation/read model

```text
STORY/
    TRANSCRIPT/
    EVENTS/
    MECHANICS/
    NARRATIVE/
```

Deleting or regenerating STORY must not alter canon or recovery.

### 10.3 TRANSCRIPT

Purpose: dialogue fidelity and reconstruction.

Recommended record unit: one retained visible conversational message/utterance per Story record/file by default.

Include only material intended for transcript/history (player/Master discourse and selected OOC when useful), not tool calls, hidden reasoning, or internal runtime plumbing.

A Story transcript record may outlive a compacted `runtime.message` source body; it remains non-canonical historical material.

### 10.4 EVENTS

Purpose: story-facing adaptation of LOG.

One Story Event may summarize/merge several SemanticEvents when they form one human-meaningful story beat; it may also split an overly technical source event if required for presentation. It must carry source refs.

It is not used to restore world state.

### 10.5 MECHANICS

Purpose: retain the subset of mechanics humans routinely ask about when following/planning play.

Include when materially useful, for example:

- significant check/attack/save roll and outcome;
- HP/temp-HP changes;
- resource spend/recovery;
- Effect/Condition/LifeState transitions;
- player-relevant duration/expiry/recovery information;
- important movement/range/action-economy facts when they shaped the decision.

Exclude:

- full Actor/Asset state copies;
- checkpoints;
- dependency DAG/cache data;
- full contribution stacks when not requested;
- internal resolver bookkeeping;
- all MechanicalEvents merely because they exist.

One Story Mechanics record represents one human-meaningful mechanical beat, not necessarily one raw MechanicalEvent.

### 10.6 NARRATIVE

Purpose: editable literary prose derived from transcript/events/mechanics and canonical references.

`NARRATIVE` records are independent from chapter grouping. Reordering/rebuilding chapters must not move or rename the underlying files.

A narrative record may be corrected/rephrased for literary quality without changing canon.

### 10.7 Chapters as index grouping

No `world.chapter` or `story.chapter` entity is initially required.

A NARRATIVE index can hold an ordered grouping such as:

```text
chapter number/title
ordered NARRATIVE record refs
optional synopsis/part label
```

Explicit ordered refs are safer than assuming contiguous numeric ID ranges because later editing/insertion may create non-contiguous IDs.

### 10.8 Cross-layer IDs

Accepted conceptual form:

```text
T001452
E003562
M012644
N000087
```

IDs are local to each Story layer. Cross-layer relationships live inside records/indexes rather than filename equality.

Default record granularity remains one Story record per file; batching multiple independently addressable records into one file is deferred unless measured scale requires it.

## 11. Story visibility/context

STORY is physically readable in the repository by anyone with repository read access; this is accepted.

For normal ChatGPT/player/spectator use, records must still be context-filterable. The simplest initial rule is record-level eligibility:

- a record's audience/disclosure metadata is derived from the claims it contains;
- a context may retrieve the record only if all material claims in it are narratable for that context;
- if a literary record would mix incompatible audiences, split the record rather than inventing field-level redaction machinery.

This is a presentation/context rule, not repository ACL.

## 12. Promotion boundary

### 12.1 Invocation facts are not durable lore

A Step-3 invocation-adjudicated fact remains execution input. It is not retroactively treated as world truth simply because it affected one resolution.

### 12.2 Promotion occurs only when durability/reference requires it

If future canonical consistency requires a proposition, create/update `world.lore_fact` explicitly.

If a durable knowledge record must reference a previously untracked claim, the claim may be promoted as a `world.lore_fact` with `truth_status=undetermined` without asserting that it is true.

If later objective evidence establishes it, transition to established/disproven through normal causal history.

### 12.3 Entity dependency closure

If durable lore/knowledge/LOG references a local/promotable entity, the same publication closure must promote that entity or reject the durable reference, consistent with Steps 1–3.

STORY may reproduce a noncanonical mention without promoting it, but such a Story-only mention cannot be used as canonical identity evidence later.

## 13. Migration / retirement consequences if recommendation accepted

Mechanically implied later work:

- retire `world.chapter` from active world-record kinds;
- retire `transition.chapter_append` and `event.chapter.appended`;
- remove Chapter fields/identifier policy and old chapter prose authority;
- add `STORY` manifest/layout contract and Story schemas outside canonical world authority;
- normalize lore truth status and separate lifecycle/supersession;
- make `world.knowledge` the sole durable in-fiction knowledge owner;
- migrate/remove embedded PC/NPC/Faction knowledge arrays as writable authority;
- retire Secret truth/known/suspected authority and legacy new-campaign `WORLD/SECRETS` requirement;
- treat legacy thread/player visibility lists as migration/projection inputs, not parallel current truth, where Step-4 scope reaches them;
- add player disclosure owner if D3 is accepted;
- align live compaction and SemanticEvent visibility/history with the normalized owners;
- add machine schemas/tests only after architecture approval.

These changes require a catalog version bump because catalog IDs are retired/added; exact version is mechanical implementation detail.

## 14. Analytical challenge

### 14.1 Strongest case against normalization

Embedded knowledge is locally convenient: loading an NPC record immediately reveals what the NPC knows, without a second lookup. A separate knowledge relation increases record count and requires an index/hydration join. Adding `runtime.disclosure` adds another class and another source to retrieve before narration.

This is the strongest practical argument against the recommendation.

### 14.2 Response

The local-read convenience is purchased with semantic duplication and write contention. HDM already accepts rebuildable HOT indexes and bounded hydration. A `knowledge by knower` index makes the additional lookup bounded without copying authority into each NPC/PC/Faction record.

The player disclosure class is justified by a real lifecycle difference: player exposure is meta-level and effectively monotonic; PC/NPC knowledge is fictional state and can differ/change independently.

### 14.3 Simplest viable alternative

The simplest viable design is **not** a generic knowledge graph. It is only:

```text
world.lore_fact
world.knowledge
runtime.disclosure  # if approved
```

plus typed provenance refs and derived indexes.

No RDF, ontology engine, rule-based epistemic inference, ACL graph, full text secrecy system, or generic claim algebra is required.

### 14.4 Failure scenarios

#### False rumor

P = "The duke is a vampire"

```text
world.lore_fact(P).truth_status = disproven or undetermined
NPC_A world.knowledge = believed(P)
PC_B world.knowledge = suspected(P)
PLAYER_B runtime.disclosure = disclosed(P) if actually told
```

No contradictory truth copies are needed.

#### Secret objective fact loaded for mechanics

P is established, no relevant PC/player relation exists. Adjudication may retrieve P; narration bundle excludes P. Mechanics can still resolve from objective truth.

#### Player knows OOC, PC does not

`runtime.disclosure(PLAYER_A,P)` exists; `world.knowledge(PC_A,P)` does not. Player-facing OOC answer may acknowledge P where allowed; PC/NPC cognition may not use it.

#### PC knows, player has not yet been told

`world.knowledge(PC_A,P)=known` can exist after off-screen/shared-world changes. On the next appropriate presentation, narration may disclose P and create/update the player disclosure relation. The two states are not forced to be simultaneous.

#### Live epoch perception

PC_A perceives event X, PC_B does not. Live state is operational authority during the epoch. Compaction emits durable history and updates only PC_A's relevant knowledge. Human disclosure is recorded only for players actually shown the event.

#### STORY error

NARRATIVE says the sword was silver; canon says iron. Repair/regenerate Story only. No world transition occurs.

#### Old secret revealed

Revelation does not move a fact from a Secret file to Lore. The proposition already exists; knowledge/disclosure changes. STORY projections may become newly eligible/rewriteable.

### 14.5 Local-versus-global optimization

The recommendation moves knowledge out of Actor/Faction files, making those files slightly less self-contained, but removes repeated semantics from every entity kind and makes one context selector/index reusable everywhere. This is a net reduction in global complexity.

### 14.6 Reversibility

- Story schemas/layout are highly reversible because Story is non-canonical.
- Retiring old Chapter is low migration risk before deployed compatibility exists.
- Normalizing knowledge is more constraining but fixes an existing duplicate-authority defect; retaining duplicates would create harder migration later.
- Adding `runtime.disclosure` is reversible but would require migrating disclosure relations if later unified.

### 14.7 What would change the recommendation

Recommendation confidence: **HIGH** for T2/K2/S3 and Story structure; **MEDIUM-HIGH** for D3.

Evidence that would change D3:

- a demonstrated requirement that PLAYER and PC knowledge always move together, making separate disclosure redundant; or
- an existing accepted campaign identity model showing `world.knowledge` was intentionally designed to include non-world human players with distinct typed stance semantics.

Neither is present in the current repository; existing CORE explicitly distinguishes what a PC knows from what a player was told.

## 15. Decision-ready recommendation

Adopt the following ownership graph:

```text
world.lore_fact
    objective proposition + truth status

world.knowledge
    current in-fiction epistemic relation
    PC / NPC / organization -> proposition

runtime.disclosure
    current/monotonic human-player exposure relation
    PLAYER -> proposition

LOG / SemanticEvent
    historical causal/visibility/knowledge-change evidence

STORY
    non-canonical human/LLM read projections
```

Retire the independent Secret truth/knowledge owner and the old world Chapter machinery.

The first material human gate is therefore:

> **Should player disclosure remain a separate durable meta-level owner (`runtime.disclosure`) rather than being folded into `world.knowledge`?**

Recommendation: **YES — keep them separate.**
