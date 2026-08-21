# Step 4 Rerun — Truth, Knowledge, Role Contexts, Story, and Promotion — Architecture Task Brief

Status: **ACTIVE ARCHITECTURE TASK BRIEF — FULL-CYCLE RERUN**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Process authority:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Prior Step-4 artifacts remain research/history input but are superseded for the rerun by this brief and its descendants.

## 1. Classification

**Architectural / deep-work.**

The rerun changes the Step-4 framing from a generic secrecy/context problem into an explicit information-routing architecture for six accepted logical LLM roles. It still owns fundamental truth/knowledge/disclosure authority, durable promotion, LOG/STORY projection semantics, and retirement of legacy duplicate owners.

## 2. Why Step 4 is being rerun

The first Step-4 pass correctly identified normalized truth/knowledge/disclosure ownership, but it treated LLM context mostly as generic request classes. Subsequent owner discussion established six logical LLM roles with materially different epistemic needs and authority boundaries:

1. **Interpreter** — understands external natural language and produces bounded semantic interpretation;
2. **Dramaturg** — performs private non-canonical GM preparation;
3. **Actor** — reasons from one NPC/faction/world subject's own cognition and circumstances;
4. **Narrator** — produces current player-facing gameplay narration;
5. **Chronicler** — builds the non-canonical `STORY` read/presentation surface from occurred evidence;
6. **Commentator** — interactively retells/navigates `STORY` for a guest/spectator.

A role is a logical responsibility/context/authority contract, not necessarily a separate process, agent, model or model call. Physical call topology remains primarily Step 6.

The six-role model may resolve prior ambiguities automatically. Step 4 must therefore be re-evaluated from first principles against the accepted role set before canonicalization.

## 3. Accepted owner decisions entering the rerun

The following are **DECISIONS / CONSTRAINTS**, not options to reopen silently.

### 3.1 Truth / knowledge / disclosure split

The owner accepted the prior Alternative C semantic boundary:

```text
world.lore_fact
    objective proposition/truth authority

world.knowledge
    current in-fiction epistemic state
    PC/NPC/organization -> proposition

separate durable player-disclosure owner
    human PLAYER -> proposition exposure

Secret
    no independent truth/knowledge authority
```

Exact machine spelling of the disclosure owner remained provisional and may be mechanically fixed by this rerun if no semantic trade-off changes.

### 3.2 Repository secrecy boundary

- Deliberate human inspection of campaign Git is an accepted risk and is not treated as a confidentiality failure.
- Secrets are not encrypted or deliberately made unreadable merely to prevent repository browsing.
- The correctness boundary is **which information is assembled into a specific LLM role context and which role output may reach a player/guest/NPC-facing surface**.
- Repository visibility is not character knowledge or player disclosure.

### 3.3 Campaign branch topology

- One long-lived campaign branch contains durable campaign state/history/story.
- No durable spectator/public branch is introduced by default.
- Temporary `live/*` branches remain restricted to the accepted multiplayer shared-scene epoch synchronization protocol and compact back into the campaign branch.

### 3.4 Story surface

One campaign-root peer directory is accepted:

```text
STORY/
    TRANSCRIPT/
    EVENTS/
    MECHANICS/
    NARRATIVE/
```

All four layers are Git-backed **non-canonical presentation/history material**. None is recovery/world/mechanical authority.

Accepted intent:

- `TRANSCRIPT` — retained actual participant discourse useful for dialogue fidelity and reconstruction;
- `EVENTS` — human/LLM-friendly adaptation of semantic campaign history, not a second LOG;
- `MECHANICS` — curated player/spectator-relevant mechanics, not a state/checkpoint/trace dump;
- `NARRATIVE` — editable literary prose suitable for book-like reconstruction.

Story IDs are layer-local and cross-linked explicitly, e.g. `[T001452]`, `[E003562]`, `[M012644]`, `[N000087]`. Filename equality across layers is not a relation.

Default simplicity: one independently addressable Story record per file. Deterministic sharding keeps directory width bounded; a six-digit-or-longer sequence with thousand-slot shards is an accepted initial shape unless the rerun finds a concrete contradiction.

### 3.5 Chapters

The owner confirmed that old `world.chapter` was the early seed for the literary history feature now moving into Story.

- Retire `world.chapter`, `transition.chapter_append`, and `event.chapter.appended` from active world/mechanical authority.
- Do not silently repurpose the old machine ID.
- A literary Chapter is initially **index grouping over `STORY/NARRATIVE` records**, not a world entity and not a mandatory physical subdirectory.

### 3.6 Six logical LLM roles

The role set is approved in principle and recorded in:

- `DEV/docs/superpowers/specs/2026-08-20-llm-logical-roles-draft.md`

Step 4 owns the information/authority implications of these roles. Step 6 owns physical model/call topology, budget, model selection, and compatible role co-location.

## 4. Existing canonical constraints from Steps 1–3

The rerun must preserve:

- one mutable authority per semantic state;
- current world records remain current-state authority;
- `runtime.semantic_event` / LOG is compact durable history, not current-state authority and not a transcript;
- `runtime.mechanical_event` is an immutable committed mechanical fact;
- narration/projection cannot mutate mechanics or truth by prose alone;
- LLM outputs that affect execution are proposals/bounded semantic inputs validated by deterministic machinery;
- invocation-adjudicated facts do not automatically become durable lore;
- missing/unknown is distinct from false;
- durable references cannot escape to unpromoted local/ephemeral entities;
- retrieval/context hydration remains bounded and index-driven;
- no generic workflow/knowledge-graph/event-sourcing engine without a demonstrated current requirement.

## 5. Verified legacy conflicts to resolve

### 5.1 Truth vocabulary

Legacy `GAME/SCHEMA/lore.schema.yaml` mixes `canonical`, `superseded`, and `disputed_in_world` in one status while the machine catalog has truth statuses `undetermined`, `established`, `disputed`, `disproven`.

The rerun must separate objective truth from lifecycle/canonicality and in-world disagreement.

### 5.2 Duplicate knowledge ownership

Writable knowledge/belief currently appears in PC, NPC, Faction, Secret, Player visibility, live-scene perception/knowledge, and the newer `world.knowledge` concept.

The rerun must preserve only one durable current in-fiction knowledge owner while retaining historical perception/disclosure evidence where useful.

### 5.3 Secret mixes responsibilities

Legacy Secret combines objective truth, known/suspected subjects, revelation conditions and thread linkage.

The rerun must distribute those responsibilities to their real owners without creating a replacement generic Secret wrapper.

### 5.4 Roadmap/status drift

Current roadmap/status still describe a `SemanticEvent -> world.chapter -> public projection` chain and a possible private/public Git projection transport. Those statements predate the accepted Story/Commentator design and must be corrected after the architecture is resolved.

## 6. Step-4 scope after six-role discovery

Step 4 now owns five coupled architecture blocks.

### A. Durable information authority

- objective propositions/truth;
- current in-fiction epistemic state;
- durable human-player disclosure/exposure;
- provenance and historical change evidence;
- retirement/migration of legacy duplicate owners.

### B. Role-specific context assembly

Define a deterministic **Context Assembler** capability that builds bounded context envelopes from authoritative/derived sources for the six logical roles.

The assembler is not a seventh LLM role and is not itself a new canonical state owner.

It must answer:

- which role is requesting context;
- for which player/PC/NPC/faction/guest/session/purpose;
- at which pinned campaign/story frontier;
- which source classes are eligible;
- which source classes are explicitly forbidden;
- how the bundle exposes provenance/identity without copying authority.

### C. Typed role handoffs

A role may pass a **typed result**, never inherit another role's raw private context merely because the same physical model/process performed both roles.

Relevant conceptual handoffs include:

- Interpreter -> bounded interpretation / invocation facts;
- Dramaturg -> non-canonical preparation proposal;
- Actor -> subject intent and optional epistemic change proposal;
- core -> narration-safe settled bundle;
- Narrator -> prose plus structured disclosure evidence;
- source history -> Chronicler story-source bundle;
- Story indexes/records -> Commentator spectator bundle.

Exact wire types remain implementation detail unless semantics require them now.

### D. Story projection and spectator interaction

Specify Story record authority, provenance, cross-links, reveal/spoiler metadata, literary chapter grouping, and Commentator navigation semantics without turning Story into canon or requiring a second Git branch.

### E. Promotion closure

Specify when an invocation/local/preparation fact or entity becomes durable because future canonical consistency or durable references require it.

## 7. Non-goals

Step 4 does **not** own:

- final physical model-call topology or model selection;
- a permanent autonomous agent per role or NPC;
- token/cost/latency budgets (Step 6);
- Git transaction/CAS implementation and Story publication batching (Step 5);
- encryption/repository ACL redesign;
- spectator UI;
- generic role-message bus;
- general-purpose RDF/ontology/knowledge graph;
- full event sourcing;
- mandatory background polling;
- full SRD seed;
- implementation before architecture canonicalization and implementation planning.

## 8. Fitness criteria

The final architecture must satisfy all of the following.

### Authority

- one objective proposition has one objective truth owner;
- one durable current in-fiction epistemic relation has one owner;
- human-player exposure is not conflated with PC cognition;
- Story and role outputs never become alternate truth by being plausible prose;
- preparation is not future canon.

### Context correctness

- a fact loaded for Dramaturg/private binding work does not automatically enter Narrator or Actor context;
- Actor cannot use facts unavailable to its represented subject;
- Narrator receives only player/PC-eligible material plus newly authorized consequences;
- Commentator normally operates from Story rather than unrestricted current WORLD/STATE;
- physical co-location of roles does not merge their logical context eligibility.

### Agency

- the engine does not infer voluntary PC belief/emotion merely because information was presented;
- NPC/faction epistemic judgment may be proposed by Actor but commits through explicit world transition/validation;
- player disclosure never implies a controlled PC knows or believes the same proposition.

### Story

- deleting Story cannot alter canon/recovery;
- loss of Story may still lose non-canonical transcript/editorial material if source bodies were compacted; non-authority does not falsely imply byte-for-byte regenerability;
- Chapters can be reorganized without renaming/moving underlying NARRATIVE records;
- Commentator can navigate/rewind/style-shift without inventing facts;
- Story can support spoiler/reveal-frontier filtering without pretending Git files are confidential.

### Promotion

- no durable lore/knowledge/disclosure/LOG reference depends on an unpromoted local entity/fact;
- Story may mention noncanonical/local material but that mention cannot later serve as canonical identity evidence by itself.

## 9. Required investigation questions

### Truth and knowledge

1. What exact axes belong to `world.lore_fact`?
2. How is ordinary world change distinguished from correction/supersession of a proposition?
3. What minimal epistemic stance vocabulary supports correct PC/NPC/faction behavior without a generic epistemic logic engine?
4. How are PC voluntary beliefs protected from automatic inference?
5. What durable fields belong to player disclosure, especially when a player has heard a claim but not objective truth?

### Role context

6. What deterministic selector inputs define each role context?
7. Which roles may access objective secrets, subject knowledge, player disclosure, LOG, current world state, or Story?
8. How are role outputs sanitized/typed before another role consumes them?
9. What must be pinned to one campaign/story frontier to prevent mixed-context reads?
10. Which role errors are typed blockers versus simple omission/clarification?

### Dramaturg and revelation preparation

11. Which old `revelation_conditions` semantics are non-canonical preparation and which, if any, represent actual mechanical/world rules?
12. Where does preparation live semantically without becoming a new canon owner?

### Story / Chronicler / Commentator

13. What is the record contract for each Story layer?
14. What cross-layer/source references are required?
15. What record-level reveal/frontier metadata is required so later literary edits do not create accidental past spoilers?
16. What is Commentator's default information boundary, and which aspects may safely remain a Step-6 mode policy?
17. How is chapter grouping represented in NARRATIVE index metadata?
18. What Story data is replaceable versus merely non-canonical but potentially irreplaceable after source compaction?

### Promotion

19. When must a local fact become `world.lore_fact`?
20. When a durable knowledge/disclosure relation references a previously untracked claim, how is that claim promoted without asserting truth?
21. How do existing entity-promotion closure rules apply to Story provenance versus canonical records?

## 10. Alternatives/challenge required

The research must re-challenge at least:

- one generic omniscient LLM context versus role-specific context assembly;
- context-policy prompts alone versus deterministic source eligibility + typed handoffs;
- universal knowledge/disclosure relation versus separate player exposure owner;
- persistent Secret wrapper versus contextual secrecy + preparation/rule owners;
- Story as one monolithic book/log versus four cross-linked read-model layers;
- Commentator with direct WORLD access versus Story-first spectator context;
- atomic Story files versus multi-record containers;
- all preparation made durable versus bounded non-canonical preparation.

The recommendation must attack itself for duplicate authority, hidden context inheritance, role co-location leakage, player-agency violation, stale/mixed frontiers, Story spoiler drift, migration burden, global scans, and unnecessary agentic infrastructure.

## 11. Human decision rights for the rerun

Already accepted semantic decisions are not re-escalated unless new evidence materially changes their trade-off.

Escalate only if the rerun finds a genuinely new choice about:

- fundamental authority ownership;
- product semantics of player/PC/guest information;
- a new durable class with materially different behavior;
- costly compatibility or irreversible storage semantics;
- role boundaries that would alter player agency or campaign truth.

Agent owns mechanical vocabulary, exact schema shaping, role-context selector details implied by accepted boundaries, Story record fields/crossrefs, migration mapping, review findings, documentation correction, and implementation-plan decomposition.

## 12. Exit criteria

The rerun is ready for canonicalization when:

- truth/knowledge/disclosure ownership is revalidated with the six roles;
- Context Assembler semantics are explicit;
- raw cross-role private-context inheritance is prohibited and typed handoffs are defined conceptually;
- Dramaturg/Actor/Narrator/Chronicler/Commentator information boundaries are coherent;
- Secret/revelation semantics are resolved;
- Story four-layer contracts, IDs/sharding, provenance and chapter grouping are specified;
- spectator reveal/frontier semantics are sufficient for Commentator without a public branch;
- promotion closure is explicit;
- legacy Chapter and embedded knowledge/Secret owners have migration dispositions;
- candidate spec passes adversarial review and resolution gate;
- roadmap/status drift is corrected after the accepted architecture is consolidated;
- implementation does not begin until a canonical spec exists and `superpowers:writing-plans` is used.
