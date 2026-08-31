# Step 4 — Lore, Knowledge, Disclosure, Story Projection, and Promotion — Architecture Task Brief

Status: **ACTIVE ARCHITECTURE TASK BRIEF**

Target branch: `feature/mechanical-runtime-hot-state`

Process authority:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

## 1. Classification

**Architectural / deep-work.**

This stage fixes ownership and interfaces across durable world truth, perspectival knowledge, disclosure, LLM context selection, semantic history, non-canonical story projections, and minimum promotion semantics. Wrong ownership here would create duplicate truth, secret leakage through model context, or narrative projections that silently become canon.

## 2. Problem statement

HDM already has partial and overlapping models for:

- objective lore and hidden facts;
- PC/NPC/faction knowledge and beliefs;
- player-visible/private record hints;
- live-scene per-PC disclosure;
- `LOG` / semantic campaign history;
- runtime messages and mechanical events;
- an early `world.chapter` concept intended to build a book-like campaign history;
- canonicality/promotion constraints from Steps 1–3.

These pieces were designed at different times and are not yet one coherent authority graph. Step 4 must reconcile them without weakening accepted runtime/mechanical boundaries.

In parallel, the owner has now explicitly selected a durable but **non-canonical** campaign `STORY/` projection surface intended for literary reconstruction and adjacent/spectator ChatGPT use.

## 3. Accepted constraints entering Step 4

The following are **DECISIONS / CONSTRAINTS**, not options to reopen silently.

### 3.1 Repository and secrecy boundary

- Campaign Git storage is not treated as a confidentiality/security boundary against a human who deliberately browses repository files.
- Secrets are not encrypted or made intentionally unreadable merely to prevent repository inspection.
- The critical boundary is **knowledge-aware LLM context selection and narration**: a secret loaded for adjudication must not leak into a player/NPC/guest-facing context merely because the model had access to it.
- Repository visibility is not character/player knowledge.

### 3.2 Campaign branch topology

- One long-lived campaign branch remains the durable campaign history/state branch.
- No separate durable spectator/public branch is introduced by default.
- Temporary `live/*` branches exist only for the already-accepted multiplayer shared-scene epoch protocol and later compact back into the campaign branch.

### 3.3 Story projection

Add one campaign-root peer directory:

```text
STORY/
    TRANSCRIPT/
    EVENTS/
    MECHANICS/
    NARRATIVE/
```

All four layers are durable Git-backed **non-canonical projections** intended for human/LLM reconstruction and presentation. They must not become alternate world/mechanical authority.

Layer intent:

- `TRANSCRIPT` — retained actual discourse/message material useful for dialogue fidelity and reconstruction;
- `EVENTS` — story-facing adaptation of canonical/semantic history, not a second `LOG` authority;
- `MECHANICS` — curated player-relevant mechanical history (e.g. material rolls, HP/resource/effect/lifecycle changes, durations), not a dump of STATE/checkpoints/traces;
- `NARRATIVE` — literary prose/history suitable for book-like reconstruction.

Cross-layer references are explicit and many-to-many, e.g. `[E003562]`, `[M012644]`, `[T001452]`, with independent numbering per layer.

Default simplicity rule: one story record per file unless evidence later proves batching necessary. Chapter grouping is index metadata over `NARRATIVE` records; a Chapter is not automatically a standalone entity/file boundary.

### 3.4 Retirement of early Chapter model

`world.chapter`, `transition.chapter_append`, and `event.chapter.appended` are treated as an early seed for the now-separate STORY/NARRATIVE functionality. Step 4 must retire them from active world/mechanical authority and migrate any useful metadata semantics (coverage/provenance/order/visibility) only where still justified.

Do not silently repurpose `world.chapter` into a new meaning.

### 3.5 Existing accepted invariants

- One semantic fact has one mutable authority.
- Narration/projection never becomes mechanical truth.
- `LOG` is compact semantic history, not transcript or transaction journal.
- MechanicalEvent is a committed runtime fact from Step 3; SemanticEvent is a durable campaign-history projection, not current world state.
- LLM may adjudicate bounded fiction-dependent invocation facts but cannot inject deterministic engine-owned mechanics.
- Durable references cannot depend on unpromoted local/ephemeral entities.
- Retrieval remains bounded/index-driven; no routine campaign-wide scans/full-context loading.

## 4. Current repository conflicts/gaps already verified

These are **FACTS / findings to resolve**, not yet final design choices except where constrained above.

### 4.1 Truth-status vocabulary conflict

`GAME/SCHEMA/lore.schema.yaml` currently uses:

```text
canonical | superseded | disputed_in_world
```

while the Step-1 machine catalog registers:

```text
undetermined | established | disputed | disproven
```

and `world.lore_fact` expects `truth_status`.

Step 4 must establish one coherent truth/lifecycle model and migration relation.

### 4.2 Duplicate knowledge authority

Knowledge/belief is currently writable in several places:

- `world.knowledge` in the Step-1 catalog;
- `npc.schema.yaml -> knowledge`;
- `pc.schema.yaml -> knowledge`;
- `faction.schema.yaml -> knowledge`;
- `secret.schema.yaml -> known_by_entity_ids / suspected_by_entity_ids`;
- `player.schema.yaml -> visibility.private_record_ids` may overlap disclosure/access semantics;
- live-scene state carries per-PC knowledge/disclosure during an active epoch.

Step 4 must choose one durable authority and classify the rest as projections/caches/legacy fields or distinct non-overlapping concepts.

### 4.3 Secret model mixes authorities

`secret.schema.yaml` currently combines objective hidden truth, knowledge/suspicion lists, revelation conditions, and thread linkage. Step 4 must determine whether a separate durable Secret entity is still needed after truth/knowledge separation, or whether secrecy is a property/context over ordinary facts plus discovery logic.

### 4.4 Machine schemas incomplete for Step-4 owners

The Step-1 catalog admits `world.lore_fact` and `world.knowledge`, but current DEV `world-record.schema.json` has kind-specific schemas only for a subset of world kinds and does not yet close lore/knowledge shapes. Step 4 must provide machine-verifiable contracts once semantics are approved.

### 4.5 Transcript/runtime-message boundary incomplete

`runtime.message` is catalogued as a raw user/Master/tool message for transcript/audit, while campaign session/log contracts explicitly state they are not full chat history. Exact retention, projection, addressing, and durability semantics remain open.

## 5. Scope

Step 4 owns the semantic architecture for:

1. objective proposition/truth authority;
2. belief/knowledge/suspicion/disclosure authority;
3. knowledge-safe bounded context selection for LLM calls;
4. relation between hidden truth and secrecy/revelation;
5. SemanticEvent compaction/authority boundary;
6. the non-canonical `STORY/` projection model;
7. transcript retention semantics sufficient for reconstruction;
8. curated story-facing mechanics projection semantics;
9. literary `NARRATIVE` and chapter/index grouping semantics;
10. minimum promotion contract from situational/local facts/entities into durable referenced canon;
11. migration/retirement semantics for the old Chapter model and other duplicate knowledge fields.

## 6. Non-goals

Step 4 does **not** own:

- Git transport/CAS/tree publication details already owned by Step 5/current persistence contracts;
- a new repository-access security/encryption subsystem;
- generic ACL infrastructure for Git;
- spectator UI;
- a universal knowledge-graph/query language;
- full SRD seed population;
- final transcript compaction/retention tuning based on measured volume;
- changing the accepted multiplayer live-branch topology;
- using STORY as recovery authority;
- implementation before the architecture decision/review gates close.

## 7. Quality attributes / fitness criteria

The design must maximize, in order of materiality:

- correctness of truth/knowledge separation;
- no duplicate writable authority;
- resistance to accidental LLM secret leakage;
- deterministic/mechanically bounded promotion and references;
- bounded retrieval/context size;
- recoverability from canonical authority without STORY dependence;
- useful narrative reconstruction for players/guests;
- traceable provenance/cross-layer references;
- low authoring/storage complexity;
- evolvability without turning lore/knowledge into a generic graph engine.

Concrete fitness criteria:

- deleting/rebuilding `STORY/` cannot alter canonical world/mechanical truth;
- a loaded secret is not narratable unless the target context is entitled to it;
- one durable knowledge claim has one writable authority;
- a belief can be wrong without creating a conflicting objective truth;
- a player can be told a fact without implying their PC knows it unless the disclosure semantics say so;
- an NPC can know/believe something the player does not know;
- a durable canonical record/event cannot reference an unpromoted local entity;
- STORY records may cite authority but cannot be used as authority to mutate canonical state;
- chapter reorganization must not require moving/reidentifying underlying NARRATIVE records.

## 8. Required investigation

### 8.1 Repository authority review

Inspect at minimum:

- `GAME/CORE/AI_REASONING.md`
- `GAME/CORE/INFORMATION.md`
- `GAME/CORE/LORE.md`
- `GAME/CORE/STORAGE.md`
- `GAME/CORE/PERSISTENCE.md`
- `GAME/CORE/MULTIPLAYER.md`
- `GAME/CORE/LIVE_SCENE.md`
- `GAME/SCHEMA/lore.schema.yaml`
- `GAME/SCHEMA/secret.schema.yaml`
- `GAME/SCHEMA/player.schema.yaml`
- `GAME/SCHEMA/pc.schema.yaml`
- `GAME/SCHEMA/npc.schema.yaml`
- `GAME/SCHEMA/faction.schema.yaml`
- `GAME/SCHEMA/event.schema.yaml`
- campaign manifest/template layout;
- Step-1/2/3 catalogs and canonical specs.

### 8.2 Targeted external research

Research only patterns that can materially challenge/clarify the design, prioritizing primary/authoritative sources. Candidate questions:

- provenance models for assertions versus beliefs;
- distinction among truth, claim, source, observer and disclosure in comparable knowledge systems;
- event-sourcing/projection boundaries relevant to LOG vs STORY;
- append-only/projection indexing strategies when useful;
- retrieval/context-isolation patterns for LLM systems only where authoritative documentation/research exists.

Do not import a general RDF/knowledge-graph/event-sourcing framework unless HDM requirements demonstrate need.

## 9. Questions the architecture must answer

### Truth / claims

1. What exactly is a durable objective proposition in HDM?
2. How are `undetermined`, established, disproven, retconned/superseded, and in-world disputed accounts represented without conflating objective truth with beliefs?
3. When does an undefined/situationally adjudicated fact become durable lore?
4. How is provenance recorded without storing a second truth copy?

### Knowledge / disclosure

5. What is the sole durable owner of `knower -> proposition -> epistemic state`?
6. Are knowledge, belief, suspicion, misinformation and player disclosure one record family with distinct states, or separate owners?
7. How are PC knowledge and player disclosure distinguished where needed?
8. How does live-scene per-PC knowledge compact into the durable model without duplicate authority?
9. What, if anything, remains as embedded summary/reverse projection on Actor/Faction/Player records?

### Secrets

10. Is `Secret` an independent entity/lifecycle or simply an objective fact whose disclosure is restricted plus optional discovery/revelation machinery?
11. Where do revelation conditions belong if they have actual mechanics/lifecycle?

### LLM context

12. What typed request/context identity determines what a specific LLM call may receive?
13. Which facts may be loaded for adjudication but excluded from narration/NPC cognition?
14. How does retrieval remain bounded and explainable?
15. How are context/provenance errors surfaced rather than silently guessed?

### LOG / STORY

16. What exact authority remains in `runtime.semantic_event` / `LOG`?
17. How is `STORY/EVENTS` derived/adapted without becoming a duplicate log?
18. Which mechanical facts belong in `STORY/MECHANICS` and which are deliberately excluded?
19. What exact source does `STORY/TRANSCRIPT` project from, and what fidelity/retention guarantee does it make?
20. What is the minimal `STORY/NARRATIVE` record contract?
21. How does a separate index represent chapters/parts/coverage without making Chapter an entity?
22. Which provenance/cross-layer references are required versus optional?
23. Which story records/fields are filtered for a given consumer context, without pretending repository files themselves are secret?

### Promotion

24. What closes the dependency graph when a local entity/fact becomes referenced by durable lore, knowledge, LOG or STORY provenance?
25. Which promotion actions are deterministic engine operations versus LLM-authored content requiring validation?

## 10. Required architecture alternatives/challenge

At minimum compare:

- normalized proposition + separate knowledge/disclosure records;
- embedded per-owner knowledge with canonical proposition IDs;
- a hybrid in which one normalized durable authority exists and embedded data is explicitly derived/index-only.

For secrets compare:

- independent Secret entity;
- ordinary proposition + knowledge/disclosure only;
- ordinary proposition plus separate discovery/revelation rule owner where actually needed.

For STORY compare only viable storage/record granularities and avoid speculative compression.

Challenge every recommendation for:

- duplicate authority;
- secret leakage through overly broad context hydration;
- player-vs-PC conflation;
- belief-vs-truth conflation;
- inability to preserve historical belief without rewriting current truth;
- STORY accidentally becoming a recovery/canon dependency;
- mandatory global chronology/order that prior architecture rejected;
- campaign-wide scans;
- generic graph/query abstraction with no proven need;
- migration of old schemas and live-state compaction.

## 11. Human decision rights

Escalate only material choices such as:

- fundamental truth/knowledge ownership;
- whether a distinct Secret entity survives;
- product semantics of PC knowledge versus player disclosure where alternatives remain genuinely viable;
- material retention/fidelity trade-offs that affect the intended STORY experience;
- costly compatibility/migration choices.

Agent owns mechanical consequences, schemas, identifiers, cross-reference details, migration mapping, tests, documentation alignment, and retirement of old IDs after accepted decisions.

## 12. Exit criteria

Step 4 can close only when:

- one coherent truth/proposition authority is canonical;
- one coherent durable knowledge/disclosure authority is canonical;
- LLM context filtering is explicit and testable;
- Secret semantics are resolved without duplicate authority;
- `world.chapter` / chapter transition/event are retired or explicitly superseded;
- `STORY/{TRANSCRIPT,EVENTS,MECHANICS,NARRATIVE}` semantics and non-authority are specified;
- chapter grouping/index semantics are specified;
- minimum promotion closure is specified;
- migration/legacy fields have an owned disposition;
- candidate spec has passed adversarial review and resolution gate;
- machine schemas/catalogs/tests are aligned only after the accepted design;
- unresolved persistence/transport concerns are explicitly handed to Step 5.
