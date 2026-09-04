# R2.7 WP-18 — Story / Continuity / Dramaturg Planning — Step-1 Decision Brief

Status: **STEP 1 COMPLETE CANDIDATE — MANDATORY SENIOR REVIEW REQUIRED**

Date: 2026-09-04

Starting verified public state: `0b6cde38eb188713ac50ab7690f73eeab524e693`

This artifact is the Step-1 scope/decision brief for WP-18 only. It does not select the WP-18 architecture, authorize Step 2, begin WP-19, begin implementation planning, or change runtime/schema/catalog/CORE behavior.

The companion open-world Source Manifest is:

- `DEV/docs/superpowers/design/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-source-manifest.md`

The mandatory Step-1 whole-project critic is:

- `DEV/docs/superpowers/design/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-decision-brief-critic.md`

---

## 1. Problem statement

WP-18 must reconcile the already accepted Story/continuity/Dramaturg semantics with current R2.7 physical/currentness/runtime surfaces without creating a second gameplay authority or reviving retired Story architecture.

The domain has two deliberately different directions of derived information:

```text
PAST / OCCURRED EVIDENCE
    -> Story / continuity projections
    -> retrospective, noncanonical orientation / presentation / history

FUTURE / PROVISIONAL PREPARATION
    -> Dramaturg preparation / retained planning
    -> prospective, private/noncanonical coordination and guidance
```

They may reference the same accepted owners, but their source meaning, lifecycle, visibility, invalidation and failure semantics are different. WP-18 must not collapse them into a generic `memory`, `story_state`, `planning_state`, `narrative_state`, `timeline` or session-memory authority.

The current R2.7 scope discovery asks five concrete questions:

1. Where do Story records, indexes, coverage/source basis and Chronicler service state live?
2. Are Story, continuity projections and prospective Dramaturg planning physically and semantically distinct?
3. Where do player-local and multiplayer-only shared Dramaturg horizons live; how are generation, CAS/rebase, discovery, invalidation and lifecycle represented?
4. Is `preparation has no entitlement to occur; canon invalidates preparation` enforced in instruction/runtime/test mapping?
5. Can any retained planning/Story state become required canon/recovery authority accidentally?

Step 1 frames the evidence/design problem. It does not answer those questions by choosing a new representation.

---

## 2. Established upstream constraints that WP-18 must preserve

These are already accepted boundaries, not WP-18 design choices.

### 2.1 Story is a retrospective noncanonical projection

Step 4 defines Story as durable noncanonical presentation/history. It is not current world state, mechanics, truth, knowledge, disclosure or recovery authority.

The accepted logical layer family is:

```text
STORY/
  TRANSCRIPT/
  EVENTS/
  MECHANICS/
  NARRATIVE/
```

Story may orient an eligible role, but material current/source-specific reliance must escalate to the applicable proper owner. Story omission is not semantic absence.

`world.chapter`, `transition.chapter_append` and `event.chapter.appended` are retired architecture. Chapter-like literary grouping, where useful, is Story/NARRATIVE indexing/presentation only and may not recreate a canonical chapter owner.

### 2.2 Story durability/currentness is already strongly closed

Step 5.10 already owns the Story projection lifecycle:

```text
typed source-domain basis/watermark
    - compatible Story-layer coverage
    -> bounded uncovered window
    -> source bundle
    -> deterministic/Chronicler transform
    -> final layer-local IDs
    -> validated Story transaction
    -> compatible coverage advancement
```

Important fixed boundaries include:

- `MUST_MATERIALIZE | MAY_OMIT` candidate disposition;
- layer-local projection state and layer-local ID allocation;
- coverage typed by source domain and semantic contract generation;
- queue-free pull catch-up;
- no Story scheduler/job queue/background-worker correctness dependency;
- no mandatory cross-layer atomicity;
- Story conflict/contention yields to current gameplay;
- Story failure cannot roll back or block accepted gameplay;
- Chronicler/LLM output does not own final IDs, coverage or publication.

WP-18 may reconcile physical/runtime realization with those laws. It may not reopen them merely because stale files/routes exist.

### 2.3 Continuity is not a generic memory owner

R2.1/R2.3 establish continuity/history as typed retrieval over accepted owners and admitted projections. Story can provide broad orientation, but material claims must resolve to current/exact/knowledge/disclosure/history owners as required by the consumer.

Context bundles, traces, recaps, current-chat continuity and retrieval hints remain projections/control values. Their physical survival does not create semantic authority.

### 2.4 Dramaturg preparation is prospective and noncanonical

Step 4, R2.4, R2.5 and `GAME/CORE/PREP.md` establish:

- Dramaturg work is provisional preparation, not future fact;
- `PreparationDraft` is a typed phase handoff, not a durable owner merely because it can be serialized;
- prepared scenes/events/reveals have no entitlement to occur;
- accepted canon/current owners invalidate incompatible preparation;
- planning may be discarded/rebuilt without canon loss;
- no plot restoration is allowed merely to preserve preparation investment.

R2.5 proves one multiplayer consumer for retained planning:

```text
player-local Dramaturg horizon
+
multiplayer-only shared Dramaturg horizon
```

Both remain noncanonical. Shared current generation requires fencing/revalidation; planning generation never outranks current owners.

### 2.5 Story and retained planning have different lifecycle direction

R2.5 explicitly separates:

```text
Story
    retrospective history/presentation projection

Dramaturg horizon
    prospective conditional preparation
```

Story coverage cannot prove planning currency. Planning generation cannot advance Story coverage. Copying/restating a provisional claim cannot promote it to fact.

### 2.6 Physical representation never creates authority

WP-08/WP-09/WP-12 and the broader R2.7 currentness work prohibit authority from arising because bytes are:

- in the shared ChatGPT context;
- in a `RoleContextBundle` or `PreparationDraft`;
- in HOT/SQLite;
- newer locally;
- present in an index/cache/session/checkpoint;
- persisted under a convenient file path.

The semantic owner/currentness/eligibility/lifecycle contract remains controlling.

---

## 3. Current machine/routing reality that Step 2 must reconcile

### 3.1 Already accepted physical Story route

WP-11 accepted Story routing equivalent to:

```text
STORY/<layer>/PROJECTION_STATE.yaml
STORY/<layer>/<floor(sequence/1000)>/<story_id>.yaml
```

Mutable Story progress remains Story-owned. A future `MANIFEST.storage.story_root` is only a static routing selector, not projection currentness or coverage authority.

### 3.2 Current public machine surfaces are incomplete relative to accepted design

At the pinned Step-1 basis:

- `GAME/CORE/STORY.md` does not exist;
- `DEV/SPECS/story-architecture.md` does not exist;
- `GAME/SCHEMA/story.schema.yaml` does not exist;
- the current `GAME/SCHEMA/` inventory contains no dedicated Story/planning schema;
- current `campaign_manifest.schema.yaml` does not yet expose `storage.story_root`;
- `DEV/PROJECT_MAP.md` still contains stale Story routing through absent legacy files;
- catalog 2.0 contains Story layers, Story service values, planning entry classes and typed handoff vocabulary;
- those catalog values do not by themselves admit a durable semantic owner;
- dedicated regression already prevents resurrection of retired canonical chapter identifiers.

These are machine/routing facts. They do **not** establish that Story semantics are missing, and they do **not** authorize recreating deleted legacy surfaces. Step 2 must reconcile them against the current canonical owners.

### 3.3 Retained Dramaturg realization remains intentionally incomplete

WP-10/WP-11 preserve:

- no campaign-native single-player Dramaturg record in the current baseline;
- multiplayer retained planning as a conditional/proven consumer deferred to WP-18.

Therefore Step 2 must begin with owner/consumer admission, not with a schema/path assumption.

---

## 4. In scope

WP-18 evidence/design work must cover all of the following.

### 4.1 Story physical/runtime reconciliation

Prove the exact implementation-facing mapping for:

- Story layer records;
- layer-local IDs;
- projection state;
- source-domain coverage/basis;
- indexes/editorial order where required;
- candidate disposition;
- Chronicler service decision and backlog derivation;
- bounded discovery/retrieval;
- publication/currentness/CAS;
- cold recovery and corruption/loss behavior;
- exact transcript/history interaction;
- cleanup/retention interaction.

### 4.2 Continuity consumer boundary

Prove where Story/derived continuity may be used as orientation and where a consumer must escalate to a stronger owner.

The design must prevent:

```text
Story says X
therefore current world/knowledge/mechanics/history owner says X
```

unless the proper source is independently resolved and supports the claim.

### 4.3 Retained Dramaturg owner admission

For each proposed retained planning surface, prove:

1. the concrete consumer;
2. why ephemeral recomputation is insufficient;
3. exact semantic class:
   - `SOURCE_ANCHORED_CONSTRAINT`, or
   - `PROVISIONAL_DRAMATURGIC_DIRECTION`;
4. scope and recipient/role eligibility;
5. source/currentness basis;
6. generation semantics;
7. invalidation/rebase semantics;
8. discovery and bounded loading;
9. lifecycle and discard conditions;
10. failure/recovery semantics;
11. why the representation cannot become gameplay/recovery authority.

Single-player durable retention remains **not admitted by default**. It may be activated only by concrete evidence that an accepted consumer requires durable retention.

### 4.4 Multiplayer shared planning horizon

For the proven R2.5 shared horizon, Step 2 must investigate the exact machine contract for:

- shared versus player-local scope;
- authenticated/authorized writer eligibility where a write is operation-sensitive;
- private/recipient-safe visibility;
- current-generation/exact-base fencing;
- compatible update/rebase behavior;
- conflict handling without blind merge/LWW;
- selective invalidation after canon/current-owner movement;
- mode transitions singleplayer <-> multiplayer;
- bounded discovery without full planning preload;
- lifecycle/cleanup of obsolete generations/entries;
- recovery where planning is lost/stale/corrupt;
- interaction with campaign/LIVE/HOT currentness without creating a universal frontier.

### 4.5 Instruction/runtime/test enforcement

WP-18 must establish implementation-facing proof that:

- `preparation has no entitlement to occur`;
- `canon invalidates preparation`;
- planning cannot self-promote by repetition/persistence;
- Story cannot become current truth/recovery authority;
- Story/Planning physical presence does not widen role/recipient eligibility;
- Chronicler service does not become a durable scheduler;
- newly produced Story has no same-envelope feedback into gameplay;
- obsolete planning bytes cannot reactivate themselves merely because cleanup lagged;
- retired canonical chapter architecture cannot return under a different spelling.

This proof must reach current instruction, runtime, catalog/schema and executable-test consumers, not only prose specs.

---

## 5. Explicit non-goals

WP-18 Step 1 does not authorize:

- code, schema, catalog, CORE, template or test changes;
- a new Story scheduler, durable job queue, worker lease, heartbeat or background correctness service;
- a generic memory/vector/graph/narrative database;
- a generic `story_state` / `planning_state` / `session_memory` authority;
- restoration of `world.chapter` or chapter-append transitions/events;
- a new truth/knowledge/disclosure/currentness owner;
- a generic planning merge engine;
- a global planning generation/currentness scalar;
- single-player durable planning merely for convenience;
- mandatory persistence of `PreparationDraft`, `StoryProjectionDraft`, TurnEnvelope or ContextTrace;
- WP-19 scaffold/template work;
- WP-20 migration design;
- WP-22 integrated regression implementation;
- WP-24 quantitative evaluation;
- WP-25 broader failure taxonomy;
- implementation planning.

---

## 6. Mandatory Step-2 evidence questions

Step 2 may begin only after Senior Step-1 GO and must answer, with item-level evidence, at least these questions.

1. What exact current owner is authoritative for each Story layer's projection state, coverage, ID allocator and indexes?
2. Which Story metadata is durable semantic projection state versus derived/rebuildable routing/editorial support?
3. What exact source-domain contracts feed each Story layer and which candidate states are `MUST_MATERIALIZE` versus `MAY_OMIT`?
4. How does Story publication compose with WP-13 durability without creating a second gameplay commit obligation?
5. How does cold recovery behave if Story is absent, stale, corrupt or ahead/behind another projection layer?
6. Which continuity consumers may use Story directly as orientation, and what exact trigger requires source escalation?
7. What exact role/recipient eligibility gates apply to Story retrieval and planning retrieval?
8. Does any accepted single-player consumer require retained Dramaturg state? If not, preserve no durable single-player planning owner.
9. What exact durable owner, if any, realizes player-local multiplayer planning?
10. What exact durable owner, if any, realizes shared multiplayer planning?
11. What constitutes a planning generation, and what exact currentness/CAS/rebase evidence selects one current shared basis?
12. How are `SOURCE_ANCHORED_CONSTRAINT` references revalidated without copying authority into planning?
13. What invalidates a provisional direction and how is invalidation visible to bounded discovery?
14. How are obsolete planning entries/generations retired without treating physical residue as active planning?
15. Can campaign/LIVE/HOT/source movement race with planning read/write, and what bounded revalidation is required?
16. What current instruction/runtime surfaces actually enforce non-entitlement, canon-invalidates-prep, role containment and no same-envelope Story feedback?
17. What executable regressions already prove parts of the contract and what implementation obligations remain unproved?
18. Which stale navigation/schema/template surfaces belong to WP-18 reconciliation versus downstream WP-19/WP-20 work?

Every answer must preserve scope limits, negative findings, dormant/conditional status and reopen triggers.

---

## 7. Required bidirectional completeness proof

WP-18 cannot close by proving only that canonical architecture can be described in machine terms.

### 7.1 Architecture -> machine

For every activated WP-18 obligation, later synthesis must identify:

```text
accepted semantic owner/law
-> exact physical/runtime representation
-> currentness/eligibility/lifecycle rule
-> catalog/schema/instruction/runtime/test consumer
-> verification path
```

No requirement may disappear because no legacy file exists.

### 7.2 Machine -> architecture

Every current or newly proposed machine surface touching Story/planning must be reverse-audited:

```text
file/root/schema field
catalog enum/value
runtime control value
index/cache
HOT/SQLite row
instruction route
test fixture
cleanup route
```

and classified as:

```text
semantic owner
noncanonical projection
derived routing/index
ephemeral runtime control
diagnostic evidence
conditional/dormant surface
legacy/stale routing
downstream scaffold/migration concern
```

No convenient machine field may acquire authority merely because code needs somewhere to store it.

---

## 8. Required adversarial states

Later evidence/design must survive at least these states:

1. Delete all Story while canon/current owners remain healthy.
2. Story record contradicts a newer current owner.
3. Story layer A is caught up while layer B is far behind.
4. Story publication conflicts with current gameplay publication.
5. Chronicler repeatedly defers under heavy turns.
6. A Story `MUST_MATERIALIZE` candidate exists while ordinary presentation Story is optional.
7. `STORY/TRANSCRIPT` exact archive survives after source-message payload compaction.
8. Exactness required by a semantic consumer is about to be lost but only Story retains a paraphrase.
9. A `PreparationDraft` survives host/context loss.
10. A planning catalog enum exists with no admitted durable owner.
11. Canon invalidates a prepared scene immediately before it would be used.
12. A source-anchored planning constraint points to a source whose current revision moved.
13. A provisional direction is copied across many generations.
14. A shared plan update races with another participant's update.
15. A PLAYER/control/recipient authorization changes during a shared planning operation.
16. LIVE/current routing moves while a planning read or write is in flight.
17. Multiplayer is disabled while shared planning still exists physically.
18. Multiplayer is re-enabled with stale retained shared planning.
19. A local planning horizon contains material private information not eligible to another participant.
20. Obsolete planning bytes survive current-namespace cleanup.
21. Story sequence/ID/file order is accidentally used as fictional chronology.
22. `campaign_manifest.schema.yaml` still lacks `story_root`.
23. `DEV/PROJECT_MAP.md` points at missing Story legacy files.
24. Newly generated Story is physically present in the same ChatGPT context before Narrator runs.

Any design that makes one of these states select gameplay truth, grant visibility, replay mechanics, force plot restoration, invent a scheduler or depend on a global scan fails the WP-18 boundary.

---

## 9. Step-1 acceptance criteria

The Step-1 package is decision-safe for Senior review only if:

1. scope is limited to Story/continuity/Dramaturg physical/runtime reconciliation;
2. Story and prospective planning are treated as distinct lifecycle families;
3. existing Step-4/5.10 Story architecture is treated as controlling rather than reopened by missing legacy files;
4. R2.5 retained planning is treated as conditional/proven only for multiplayer consumers;
5. `PreparationDraft`/`StoryProjectionDraft` are not presumed durable owners;
6. instruction/context/disclosure/cleanup/currentness owners are included in the dependency graph;
7. current catalog/schema/test and negative machine evidence are included;
8. architecture->machine and machine->architecture proof obligations are explicit;
9. no current machine surface is silently promoted to authority;
10. no architecture alternative is selected at Step 1;
11. no implementation, WP-19 or implementation planning is activated;
12. the whole-project critic has zero unresolved BLOCKING/SIGNIFICANT findings.

---

## 10. Evidence sufficiency and stop conditions

Step 2 must keep the Source Manifest open-world. Discovery continues when evidence reveals a new material owner/consumer/exception.

Escalate to the human architect only if evidence exposes:

- a genuine product-semantics choice;
- two materially different valid UX/authority models;
- a security/privacy tradeoff requiring explicit risk acceptance;
- incompatibility with an accepted external contract;
- a contradiction that would require reopening accepted architecture.

Do **not** escalate ordinary storage naming, field layout, deterministic CAS composition, bounded index/routing mechanics, schema shape or test placement when one option is clearly safer under existing accepted semantics.

---

## 11. Senior Step-1 gate

The only decision requested at this checkpoint is:

> **Is this WP-18 scope, dependency graph and evidence plan complete enough to authorize Step 2 evidence extraction?**

This brief selects no WP-18 architecture.

```text
STEP_1_STATUS:              COMPLETE CANDIDATE
ARCHITECTURE_SELECTED:      NO
IMPLEMENTATION_CHANGED:     NO
HUMAN_DECISION_REQUIRED:    NO
WP_19_AUTHORIZED:           NO
IMPLEMENTATION_PLANNING:    NO
STEP_2_AUTHORIZED:          NO
NEXT_GATE:                  MANDATORY SENIOR STEP-1 REVIEW
```
