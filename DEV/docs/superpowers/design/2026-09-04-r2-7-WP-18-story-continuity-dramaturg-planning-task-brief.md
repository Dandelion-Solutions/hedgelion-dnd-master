# R2.7 WP-18 — Story / Continuity / Dramaturg Planning — Architecture Task Brief

Status: **STEP 1 SENIOR RECOVERY CANDIDATE — MANDATORY SENIOR STEP-1 RE-REVIEW REQUIRED**

Date: 2026-09-04

Original Step-1 starting public state: `0b6cde38eb188713ac50ab7690f73eeab524e693`

Senior-recovery basis: `e35d96a08c73a818b62b0e799bc9d9fc3fc3e54e`

This is the **Architecture Task Brief** required by `DEV/DESIGN_PROCESS.md` for WP-18 Step 1. It replaces the incorrectly classified Step-1 Decision Brief. It frames research/evidence work only: it does not select WP-18 architecture, authorize Step 2, begin WP-19, begin implementation planning, or change runtime/schema/template/catalog/test behavior.

Companion evidence/routing artifacts:

- `DEV/docs/superpowers/design/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-task-brief-critic.md`.

---

## 1. Problem statement

WP-18 must reconcile accepted Story, continuity, source-Actor intentional-state and Dramaturg-planning semantics with current R2.7 runtime/machine realization without creating a second gameplay authority or reopening already accepted architecture without evidence of contradiction or insufficiency.

Three different semantic directions must remain distinct:

```text
CURRENT IN-WORLD INTENTIONAL STATE
    source Actor / NPC
    goals, current objective, next intention,
    material commitments, reconsideration cues
    -> canonical/current source-Actor-owned state

FUTURE / PROVISIONAL PREPARATION
    Dramaturg preparation / retained planning
    -> prospective, private/noncanonical guidance
    -> no entitlement to occur

PAST / OCCURRED EVIDENCE
    Story / continuity projections
    -> retrospective, noncanonical orientation/presentation/history
```

The same Actor, thread, process, lore fact or event may appear in all three families, but appearance never transfers authority between them.

The controlling R2.7 scope-discovery questions remain:

1. Where do Story records, indexes, coverage/source basis and Chronicler service state live?
2. Are Story, continuity projections and prospective Dramaturg planning physically and semantically distinct?
3. Where do player-local and multiplayer-only shared Dramaturg horizons live; how are generation, CAS/rebase, discovery, invalidation and lifecycle represented?
4. Is `preparation has no entitlement to occur; canon invalidates preparation` enforced in instruction/runtime/test mapping?
5. Can any retained planning/Story state become required canon/recovery authority accidentally?

Step 1 frames how Step 2 must answer those questions; it does not answer them by prematurely selecting representation.

---

## 2. Established constraints and owners

### 2.1 Story is retrospective and noncanonical

Step 4 and Step 5.10 already define Story as durable noncanonical presentation/history with layer-local projection state, source-domain coverage, candidate disposition, IDs and publication rules.

Accepted layers remain:

```text
STORY/TRANSCRIPT
STORY/EVENTS
STORY/MECHANICS
STORY/NARRATIVE
```

Story is not current world state, mechanics authority, objective truth, Actor cognition, `world.knowledge`, human disclosure, fictional chronology or gameplay recovery authority. Missing or stale legacy Story files do not reopen these semantics.

`world.chapter`, `transition.chapter_append` and `event.chapter.appended` remain retired. Literary grouping may exist only as Story presentation/indexing and cannot recreate canonical chapter authority.

### 2.2 Source Actor owns current non-epistemic intentional continuity

R2.2 is a current controlling owner, not an unanswered WP-18 question.

Source-Actor-owned sparse durable cognition may include:

```text
long_term_goal
current_objective
next_intention
material_commitments[]
reconsideration_cues[]
```

with foundation and directed relationship continuity under the same source Actor where applicable. `world.knowledge` separately owns proposition stance.

Current R2.7 machine realization already exposes this boundary through:

- `DEV/ARCHITECTURE/ACTOR_MODEL.md`;
- `DEV/SCHEMAS/world-actor-state.schema.json`;
- `DEV/SCHEMAS/world-record.schema.json`;
- `DEV/CATALOG/entity-structures.json`;
- `DEV/TESTS/test_r2_7_wp04_actor_asset_conformance.py`.

WP-18 must not create a Dramaturg or Story field that acts as a hidden duplicate of Actor goals/objectives/intentions/commitments/reconsideration semantics. It must not reopen R2.2 absent demonstrated contradiction, a newly unsatisfied consumer, or material insufficiency.

### 2.3 Dramaturg preparation is prospective and noncanonical

Step 4, R2.4, R2.5 and current prep/craft runtime doctrine establish:

- `PreparationDraft` is a typed handoff, not automatically a durable owner;
- prepared scenes/events/reveals/actions have no entitlement to occur;
- accepted player decisions, Actor decisions, mechanics and native owner transitions may invalidate preparation;
- planning adapts to canon, never the reverse;
- planning loss is quality loss, not canon loss;
- repeated/copied provisional direction cannot self-promote to fact.

R2.5 proves a retained-planning consumer for multiplayer:

```text
player-local Dramaturg horizon
+
multiplayer-only shared Dramaturg horizon
```

Both are noncanonical. Single-player durable retention remains unadmitted by default unless a concrete accepted consumer proves that ephemeral recomputation is insufficient.

### 2.4 Actor state, Dramaturg preparation and Story projection are separate authority classes

The required boundary is:

```text
Actor / NPC canonical in-world intentional state
    -> source Actor owner
    -> may constrain/invalidate preparation

Dramaturg noncanonical preparation
    -> conditional future possibilities/constraints
    -> may reference Actor state
    -> cannot author/override Actor current intention

Story / continuity retrospective projection
    -> occurred/source-bound history/orientation
    -> may inform bounded retrieval
    -> cannot establish current Actor intention or future canon
```

A Dramaturg prediction such as “NPC A is likely to betray B if X occurs” is not the Actor's current canonical intention unless the source Actor owner independently establishes the relevant intention/commitment. Conversely, a current Actor intention does not guarantee that a prepared scene will occur.

### 2.5 Currentness/physical representation never creates authority

R2.3, WP-08, WP-09, WP-12, WP-13 and WP-14 prohibit authority from arising merely because bytes are in:

- one physical ChatGPT context;
- `RoleContextBundle` / `ContextTrace` / `PreparationDraft`;
- HOT/SQLite/cache;
- an index/session/checkpoint;
- a Story file;
- a retained planning file;
- a newer local or Git representation.

Material reliance must resolve the applicable current routed semantic owner and eligibility.

### 2.6 R2.6 host assurance constrains mapping but does not activate implementation

R2.6 requires observable behavioral containment on the supported host and explicit R2.7 mapping for role/context/instruction behavior. WP-18 therefore must identify implementation-facing obligations for at least:

- Dramaturg/Actor/Chronicler -> Narrator containment;
- local/shared Dramaturg planning -> Narrator/catch-up containment;
- no same-envelope Story feedback;
- stale/ambient context losing to current owners;
- local/shared Dramaturg coherence and lazy retrieval;
- shared-horizon conflict/rebase and no-plot-restoration.

But R2.6 explicitly keeps production-like integrated evaluation on the **implemented MVP**. Step 1/architecture work must not build a parallel MVP, activate implementation, or claim those acceptance obligations have already passed.

---

## 3. Current machine/routing reality to reconcile

### 3.1 Story route already accepted

WP-11 accepts exceptional Story routing equivalent to:

```text
STORY/<layer>/PROJECTION_STATE.yaml
STORY/<layer>/<floor(sequence/1000)>/<story_id>.yaml
```

Story mutable progress remains Story-owned. `MANIFEST.storage.story_root`, when realized, is static routing only.

### 3.2 Current public Story realization remains incomplete

At the Senior-recovery basis:

- `GAME/CORE/STORY.md` is absent;
- `DEV/SPECS/story-architecture.md` is absent;
- `GAME/SCHEMA/story.schema.yaml` is absent;
- current `GAME/SCHEMA/` has no dedicated Story/planning schema;
- `GAME/SCHEMA/campaign_manifest.schema.yaml` lacks `storage.story_root`;
- catalog 2.0 contains Story layers/service/candidate and planning-entry vocabulary without thereby admitting new canonical owners;
- executable tests preserve retired chapter removal.

These are machine/routing facts, not evidence that accepted Story semantics are absent.

### 3.3 Actor machine realization is current positive evidence

The current R2.7 `world.actor` development schema contains typed source-Actor continuity including `long_term_goal`, `current_objective`, `next_intention`, `material_commitments`, and `reconsideration_cues`. Current catalog inventory and executable conformance tests preserve that ownership boundary.

Legacy/runtime NPC surfaces are consumers/projections and must be reconciled to this current owner; they do not authorize a new planning owner.

---

## 4. Reconstructed direct runtime consumer subgraph

The Step-1 Source Manifest and critic must not treat a short Story/Prep file list as the runtime consumer graph. `DEV/PROJECT_MAP.md` and current owners/consumers establish the following material direct cluster for WP-18 reconstruction.

### 4.1 Role, reasoning, preparation and presentation

- `GAME/CORE/RUNTIME.md` — turn/phase execution route;
- `GAME/CORE/AI_REASONING.md` — primary role/source containment behavior;
- `GAME/CORE/PLAY_POLICY.md` — instruction-cache versus campaign-data activation boundary;
- `GAME/CORE/PREP.md` — preparation doctrine;
- `GAME/CORE/GM_CRAFT.md` — situations/pressure/anti-railroad preparation behavior;
- `GAME/CORE/NARRATIVE.md` — player-facing presentation consumer;
- `GAME/CORE/INFORMATION.md` — information/knowledge/reveal handling;
- `GAME/CORE/LORE.md` — lore/current-fact consumer boundary;
- `GAME/CORE/NPC.md` — NPC/Actor behavior and current intentional-state consumer;
- `GAME/CORE/DIALOGUE.md` — Actor intent/knowledge/speech consumer.

### 4.2 World continuity and off-screen development

- `GAME/CORE/PROCESSES.md` — owner/objective/next-development causal process state;
- `GAME/CORE/WORLDGEN.md` — bounded reachable-horizon creation/prep;
- `GAME/CORE/CAMPAIGN_OPERATIONS.md` — campaign/session operational organization;
- `GAME/CORE/SESSION.md` — resume/handoff/next-horizon behavior.

### 4.3 Currentness, durability, recovery and shared-state boundaries

- `GAME/CORE/DURABILITY_GUARD.md`;
- `GAME/CORE/STORAGE.md`;
- `GAME/CORE/PERSISTENCE.md`;
- `GAME/CORE/SAVE_CONTRACT.md`;
- `GAME/CORE/INTEGRITY.md`;
- `GAME/CORE/MULTIPLAYER.md`;
- `GAME/CORE/LIVE_SCENE.md`;
- `GAME/CORE/CHRONOLOGY.md`;
- `GAME/CORE/SOURCES.md`.

These modules do not all own WP-18 semantics. They are direct current runtime consumers/boundaries whose assumptions can change the correct Story/planning mapping. Step 2 must extract only material clauses and keep the Manifest open-world if another actual consumer appears.

No positive repository-global completeness claim follows from this reconstruction.

---

## 5. In scope

### 5.1 Story physical/runtime reconciliation

Prove implementation-facing mapping for:

- Story records/layers and layer-local IDs;
- projection state and source-domain coverage/basis;
- indexes/editorial ordering where actually required;
- candidate disposition;
- Chronicler service/backlog derivation;
- bounded discovery/retrieval and currentness/eligibility;
- publication/CAS;
- cold recovery/corruption/loss;
- exact transcript/history interaction;
- cleanup/retention.

### 5.2 Actor/Preparation/Story boundary

For every current or proposed planning/continuity field or runtime path, classify whether it is:

- source-Actor canonical current intentional state;
- `world.knowledge`/another native current owner;
- noncanonical Dramaturg preparation;
- retrospective Story/history projection;
- derived routing/index/control/diagnostic support.

No planning or Story surface may silently duplicate source-Actor goals/objectives/intentions/commitments/reconsideration state.

### 5.3 Retained Dramaturg owner admission

For every proposed retained planning surface, prove:

1. concrete consumer;
2. why ephemeral recomputation is insufficient;
3. exact planning semantic class;
4. scope and recipient/role eligibility;
5. source/currentness basis;
6. generation semantics;
7. invalidation/rebase semantics;
8. bounded discovery/loading;
9. lifecycle/discard conditions;
10. failure/recovery semantics;
11. why it cannot become gameplay/recovery or Actor-intent authority.

### 5.4 Multiplayer planning

For R2.5's proven local/shared horizons investigate:

- local vs shared scope;
- authenticated writer eligibility;
- private/recipient-safe visibility;
- generation/exact-base fencing;
- semantic rebase/conflict handling without blind LWW/merge;
- source/Actor/current-owner invalidation;
- mode transitions;
- bounded discovery;
- cleanup/recovery;
- campaign/LIVE/HOT/currentness composition without a universal frontier.

### 5.5 Instruction/runtime/test and R2.6 mapping

Map accepted WP-18 laws to current instruction/runtime/schema/catalog/test surfaces, and classify each obligation as:

- architecture/current mapping to define now;
- already-satisfied machine evidence;
- implementation obligation;
- post-implementation MVP acceptance obligation under R2.6;
- downstream WP responsibility.

Do not claim production-like behavioral acceptance before the implemented MVP exists.

---

## 6. Explicit non-goals

Step 1 does not authorize:

- runtime/schema/template/catalog/test changes;
- implementation or implementation planning;
- a new Story scheduler/job queue/worker lease/heartbeat;
- generic memory/vector/graph/narrative state;
- restoration of chapter authority;
- a duplicate Actor-goal/intention/commitment store;
- a new truth/knowledge/disclosure/currentness owner;
- generic planning merge/global generation authority;
- single-player durable planning for convenience;
- mandatory persistence of `PreparationDraft`, `StoryProjectionDraft`, `TurnEnvelope` or `ContextTrace`;
- WP-19, WP-20 or later implementation work;
- a pre-implementation parallel MVP/evaluation harness.

---

## 7. Mandatory Step-2 evidence questions

Step 2 may begin only after explicit Senior GO and must answer with item-level evidence at least:

1. What owner/representation controls Story projection state, coverage, IDs and indexes?
2. What Story metadata is durable projection state versus derived/rebuildable support?
3. What source-domain contracts feed each Story layer and which candidates are `MUST_MATERIALIZE` / `MAY_OMIT`?
4. How do Story publication/recovery compose with WP-13/WP-14 without becoming gameplay authority?
5. Which consumers may use Story as orientation, and when must they escalate to proper current/exact owners?
6. For each Actor/NPC planning-looking datum, is it source-Actor state, another native owner, or noncanonical preparation?
7. How are R2.2 source-Actor goals/objectives/intentions/commitments/reconsideration protected from planning duplication?
8. Does any single-player consumer actually require retained Dramaturg state?
9. What exact owner/route realizes player-local and shared multiplayer planning, if any?
10. What constitutes planning generation/currentness and how is shared conflict/rebase fenced?
11. How are source-anchored planning constraints and Actor refs revalidated without copying authority into planning?
12. How are obsolete planning entries/generations made undiscoverable/retired even if bytes remain?
13. How do PLAYER/control/recipient and LIVE changes affect planning reads/writes?
14. Which current CORE consumers enforce non-entitlement, canon-invalidates-prep, Actor-state precedence, role containment and no same-envelope Story feedback?
15. What current schema/catalog/tests already prove parts of the contract and what remains an implementation obligation?
16. Which R2.6 obligations are architecture mapping now versus post-implementation production-like acceptance later?
17. Which stale Story/root/template/schema surfaces belong to WP-18 versus downstream WP-19/WP-20?

Every answer must preserve negative findings, dormant/conditional status, scope limits and reopen triggers.

---

## 8. Required completeness proof

### 8.1 Architecture -> machine

For each activated WP-18 obligation:

```text
accepted semantic owner/law
-> physical/runtime representation
-> currentness/eligibility/lifecycle rule
-> concrete instruction/runtime/catalog/schema/test consumer
-> verification route
```

### 8.2 Machine -> architecture

Reverse-audit every material current/proposed Story/planning/Actor-adjacent surface as one of:

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

Physical convenience cannot create semantic authority.

### 8.3 Open-world rule

The reconstructed direct runtime consumer graph is a current evidence route, not a closed-world proof. Expand it whenever an owning source or actual consumer reveals another material dependency. Do not write a positive completeness claim until the relevant claim has been demonstrated by owner/consumer accounting.

---

## 9. Required adversarial states

Later evidence/design must survive at least:

1. Story deleted while canon and Actor state remain healthy;
2. Story contradicts current Actor/world owner;
3. planning says NPC will do X while current source Actor objective/intention changed;
4. a Dramaturg prediction is accidentally persisted into Actor continuity;
5. Actor current intention is accidentally inferred from Story prose;
6. Story layers lag independently;
7. Story publication conflicts with gameplay publication;
8. Chronicler repeatedly defers;
9. Transcript exactness is needed after source compaction;
10. `PreparationDraft` survives context loss;
11. planning enum exists with no admitted durable owner;
12. canon or Actor decision invalidates prepared scene immediately before use;
13. shared planning update races another update;
14. PLAYER/control/recipient authorization changes during planning;
15. LIVE routing moves during planning;
16. multiplayer disable/re-enable encounters stale shared planning;
17. private local planning is visible to another participant;
18. obsolete planning bytes survive cleanup;
19. Story/plan/file/ref order is mistaken for fictional chronology;
20. `story_root`/Story schema remains unrealized;
21. newly generated Story is physically present before Narrator;
22. host ambient context contains stale plan/Actor state;
23. post-implementation R2.6 behavioral-containment acceptance has not yet run.

---

## 10. Step-1 exit criteria

Step 1 is fit for Senior re-review only when:

1. artifact taxonomy is Architecture Task Brief + Task-Brief critic;
2. source-Actor intentional-state owner and machine realization are explicitly included;
3. Actor / Dramaturg / Story boundaries are explicit without reopening R2.2;
4. actual material direct runtime consumer subgraph has been reconstructed from `DEV/PROJECT_MAP.md` plus current owners/consumers;
5. no unsupported positive completeness claim remains;
6. R2.6 architecture-stage vs post-implementation assurance distinction is explicit;
7. Story/planning accepted owners and current R2.7 boundary owners are represented;
8. no architecture alternative is selected;
9. no implementation or downstream WP is activated;
10. mandatory whole-project Task-Brief critic has zero unresolved BLOCKING/SIGNIFICANT findings.

---

## 11. Gate

The only requested decision after this recovery is:

> **Is the recovered WP-18 Architecture Task Brief, Source Manifest and Task-Brief critic complete enough to authorize Step 2?**

```text
STEP_1_STATUS:              RECOVERED CANDIDATE
ARCHITECTURE_SELECTED:      NO
IMPLEMENTATION_CHANGED:     NO
HUMAN_DECISION_REQUIRED:    NO
UPSTREAM_REOPEN_REQUIRED:   NO
WP_19_AUTHORIZED:           NO
IMPLEMENTATION_PLANNING:    NO
STEP_2_AUTHORIZED:          NO
NEXT_GATE:                  MANDATORY SENIOR STEP-1 RE-REVIEW
```