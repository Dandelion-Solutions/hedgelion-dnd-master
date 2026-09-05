# R2.7 WP-19 — Bootstrap / Campaign Creation / Initial Materialization — Architecture Task Brief

Status: **STEP 1 COMPLETE — PO-003 INTEGRATED / WHOLE-PROJECT CRITIC RERUN COMPLETE — MANDATORY SENIOR REVIEW**

Date: 2026-09-05

Original Step-1 execution basis: `5fc24905be5c9e1b47929ee9e7b49ea8b9f2a053`

Senior-recovery basis: `df5fe6441c2b85e9cbffcb6f83caa885501da794`

PO-001/PO-002 integration basis: `4b7411b10b30cc191141826aacb3b0c88e7eeb37`

PO-003 integration basis: `341cc592fbc53247d0d7f8d38eb07ec4297cd45d`

This Task Brief is the current Step-1 framing for WP-19. It retains the recovered bootstrap/materialization and PO-001/PO-002 interaction/navigation framing, and now incorporates the canonical `PO-003` historical Actor decision-basis requirement after a fresh owner/evidence/performance/test reconstruction.

It does not authorize or begin Step 2, Senior review, WP-20, implementation planning, gameplay bootstrap, campaign creation, or substantive runtime/schema/template/test implementation.

Companion artifacts:

- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief-critic.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-po-003-arrival-integration-checkpoint.md` — historical arrival checkpoint.

Accepted Product Owner authorities:

- `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md`;
- `DEV/docs/superpowers/specs/2026-09-05-hdm-historical-actor-decision-basis-owner-decision.md`.

---

## 1. Problem statement

WP-19 audits the campaign entry/creation/initial-materialization path and immediately adjacent interaction/navigation consumers. The current scope also has to ensure that a later retrospective consumer can explain a material historical NPC decision from the **event-time basis actually relevant then**, not from mutable current Actor/knowledge/relationship state that changed later.

Creation remains:

```text
storage selection / baseline
    -> explicit campaign/New Game choice
    -> exact runtime + exact ruleset-set resolution
    -> neutral branch / creator provenance
    -> exact scaffold materialization
    -> first campaign-specific publication
    -> initializing
    -> low-friction setup / optional PROVISIONAL_IDENTITY
    -> READY_PC
    -> PLAY_READY
    -> active normal play
```

Interaction routing remains:

```text
selected active + gameplay authorized
    -> ordinary D&D Master gameplay
    -> retrospective/history questions remain ordinary gameplay

selected active + readable but gameplay denied
    -> read-only Commentator

selected completed + readable
    -> read-only Commentator
```

PO-003 adds this historical-evidence obligation:

```text
material NPC/Actor decision at T0
    -> uses bounded eligible then-current cognition / knowledge / relationships / circumstances
    -> accepted decision retains enough bounded historical basis

current state later changes at T1

retrospective explanation/replay
    -> uses T0 basis
    -> does not silently substitute T1 current state
    -> remains disclosure/no-spoiler/context eligible
```

This does **not** authorize a full NPC-psychology history, per-turn Actor snapshots, hidden chain-of-thought retention, or a second current cognition/knowledge owner.

---

## 2. Goals

If and only if Senior later authorizes Step 2, WP-19 must establish or preserve:

1. explicit campaign/New Game selection before campaign-specific work;
2. exact runtime/ruleset creation identity including `ruleset_set_sha256`;
3. branch/materializer/first-publication provenance and failure/currentness contract;
4. complete initial materialization ownership across generated roots, fields and projections;
5. scaffold / PROVISIONAL_IDENTITY / READY_PC / PLAY_READY lifecycle separation;
6. creator/PLAYER/PC/multiplayer authority under closed access owners;
7. low-friction setup with invisible infrastructure and no broad pre-generation;
8. architecture ↔ machine ↔ verification reverse-conformance;
9. post-selection gameplay versus read-only Commentator routing;
10. PO-001 ordinary-gameplay retrospective consumer with bounded retrieval and no-spoiler eligibility;
11. PO-002 save-and-exit composition back to the existing campaign-selection gate without lifecycle/membership/control/global-live side effects;
12. PO-003 event-time historical decision-basis retention for material NPC decisions/changes where mutable current state would otherwise erase the causal basis;
13. a zero-extra-serial live-turn baseline for PO-003 unless correctness evidence proves that impossible;
14. direct downstream acceptance coverage for T0 decision basis → T1 current-state mutation → later accurate eligible explanation/replay;
15. technically precise downstream realization obligations without starting implementation planning.

---

## 3. Non-goals and hard boundaries

WP-19 Step 1/2 must not:

- run a real campaign;
- begin Step 2 before explicit Senior GO;
- begin WP-20 or implementation planning;
- reopen accepted architecture merely because PO-003 overlaps Actor/history/Story topics;
- create a generic `memory`, `psychology_history`, Actor snapshot archive or parallel history subsystem;
- persist every thought, rationale, possible plan, `NO_CHANGE`, trivial choice or transient feeling;
- retain chain-of-thought, hidden reasoning traces, raw role bundles or private prompt state;
- turn `LOG/SemanticEvent` into current Actor/knowledge authority;
- turn R2.2 Actor continuity into an event log;
- turn `world.knowledge` into a second epistemic transition log;
- let Story establish historical private motive merely because it is readable;
- widen player/PC disclosure because the engine can retrieve private historical evidence;
- require a separate model invocation solely to summarize historical motive;
- require a separate Git/remote publication solely because a decision-basis record was captured;
- add decision-basis work on unrelated turns;
- select exact schema field spelling/physical layout during Step 1;
- modify runtime/schema/template/test realization merely to make Step-1 framing clean.

---

## 4. Established constraints retained from earlier WP-19 Step 1

All prior closed findings and PO-001/PO-002 framing remain controlling unless this brief explicitly adds a qualifier.

### 4.1 Creation/materialization

- campaign choice is explicit;
- New Game resolves storage schema-v3 `engine.baseline` to one exact runtime package;
- first campaign-specific tree is generated from the exact materializer output, distinct from neutral branch ancestry;
- creator derives from first campaign-specific commit provenance;
- `GAME/TOOLS/init_campaign.py` requires exact runtime identity plus `ruleset_set_sha256`;
- stale Storage-v2/tag-derived provenance expectations are not compatibility authority;
- card/README are projections;
- campaign discovery is card-first with authoritative revalidation;
- no force-push;
- setup infrastructure is normally invisible;
- no compatibility obligation exists for obsolete unreleased scaffold state;
- WP-20 remains future released-campaign evolution/migration.

### 4.2 Interaction/navigation

- active + gameplay allowed -> ordinary gameplay;
- active readable/non-playable -> read-only Commentator;
- completed readable -> read-only Commentator;
- active-player retrospective remains ordinary Master interaction;
- save-and-exit requires successful existing save/session/live closure before the selected gameplay context is cleared;
- exit-to-menu is not pause/completion/archive/membership leave/PLAYER deactivation/PC-control transfer/global multiplayer stop.

### 4.3 Verification evidence remains consumer evidence

Earlier SR19-01 stale/qualified scenario dispositions remain current. CI green and generic schema extensibility do not prove that a new semantic obligation is realized.

---

## 5. PO-003 owner classification

The evidence supports a boundary-specific classification rather than a topic-level reopen.

### 5.1 NEW CONSUMER

PO-003 strengthens the already accepted retrospective Master/Commentator consumer: when the question is about **why an NPC acted then** or replaying that historical decision, current-state plausibility is not enough.

### 5.2 EXTENSION

The natural durable owner is the existing Step-4 `LOG/runtime.semantic_event` historical-evidence family. Step-4 already defines it as compact durable semantic history / causal evidence and routes full `world.knowledge` transition history there. WP-10 already allocates SemanticEvent inside the history/delivery namespace.

The new requirement therefore extends the existing history owner with a conditional obligation:

> for a qualifying material Actor decision/transition, retain bounded event-time evidence sufficient for later historical explanation/replay when mutable Actor-private or epistemic state would otherwise be lost.

### 5.3 NO CLOSED-ARCHITECTURE MATERIAL INSUFFICIENCY

The semantic owner/family exists and is capable of satisfying the consumer without violating its current laws. No new owner, family, Story authority or current-state contract is required.

There **is** a current realization gap: `GAME/SCHEMA/event.schema.yaml` exposes generic causal/transition structures but does not itself prove a normalized event-time Actor decision-basis contract, and no direct current acceptance test proves the PO-003 scenario. That is downstream machine/test realization debt under the existing owner, not a reason to reopen closed semantic architecture.

```text
PO003_CLASSIFICATION: NEW CONSUMER + EXTENSION
MATERIAL_INSUFFICIENCY_OF_CLOSED_ARCHITECTURE: NO
CURRENT_REALIZATION_GAP: YES
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
```

---

## 6. Exact semantic boundaries PO-003 must preserve

### 6.1 R2.2 Actor continuity

R2.2 remains the sole current owner for sparse non-epistemic Actor-private continuity. Historical basis can cite/copy bounded then-values as evidence, but cannot become a competing writable Actor record.

### 6.2 `world.knowledge`

`world.knowledge` remains the current `(knower, fact)` stance owner. Its current `supporting_source_refs` describe the current stance. Full transition history belongs to LOG/SemanticEvents. A historical decision may therefore retain the then-stance/value or an immutable evidence ref sufficient to recover it.

### 6.3 Directed relationships

`A -> B` remains source-Actor-owned and independent from `B -> A`. Historical evidence may retain only the material then-facets used for the qualifying decision; it cannot infer reciprocity or create a relationship snapshot history for every interaction.

### 6.4 Semantic/history events and record-family allocation

No new record family is needed. The event/history owner may carry a bounded decision-basis payload or equivalent immutable evidence refs; exact representation waits for later authorized design/realization.

### 6.5 Chronology

Chronology establishes typed causal/order/time evidence where required. It does not prove motive, belief, relationship stance or Actor intent.

### 6.6 Persistence/publication

Once the history owner declares a basis required for a material transition, it participates in the same coherent owner/native persistence batch as the associated LOG transition. No dedicated per-decision Git commit/publication is implied.

### 6.7 Story/continuity

Story may project/orient/rout toward historical evidence. It remains noncanonical and cannot manufacture a missing exact motive. If source evidence is insufficient, the retrospective answer must say so.

### 6.8 Master/Commentator and disclosure

A later Master/Commentator may consume the basis only through its registered eligible context. Private historical evidence does not automatically become player-visible. Current principal/player/PC eligibility, `world.knowledge`, `runtime.disclosure` and no-spoiler rules still control delivery.

---

## 7. Performance / latency criterion

Performance is a mandatory design criterion, not an implementation afterthought.

### Candidate A — bounded typed basis from already-required decision work — preferred candidate

For a material Actor/Master decision, the role-context work already had to identify the eligible current factors that mattered. Candidate A carries only the bounded material subset into accepted history and deterministic persistence.

Baseline cost:

```text
ADDITIONAL_SEQUENTIAL_LLM_CALLS: 0
ADDITIONAL_SERIAL_REMOTE_TOOL_READS_SOLELY_FOR_BASIS: 0
ADDITIONAL_REMOTE_WRITES/PUBLICATIONS: 0 separate
ADDITIONAL_CONTEXT/OUTPUT: bounded structured then-values/source refs only
IRRELEVANT_TURN_WORK: 0
```

The basis should be formed as part of the existing material decision result/accepted transition, not by a second “explain your reasoning” pass. Deterministic code owns validation/serialization/bookkeeping.

### Candidate B — full Actor snapshots

Reject: unbounded storage/context growth, duplicate current ownership, per-turn write pressure and direct conflict with PO-003/R2.2 sparse semantics.

### Candidate C — reconstruct later from current state

Reject unless immutable history independently proves every required then-value. Otherwise it causes exactly the forbidden T1-for-T0 substitution and can make retrospective retrieval more expensive.

### Candidate D — separate post-decision LLM/tool round-trip

Not baseline. It adds critical-path serial latency and hidden-reasoning pressure. If future evidence demonstrates this is required for correctness, Step 2 must record it as a material architecture/performance problem and compare alternatives explicitly rather than accepting it silently.

---

## 8. Mandatory Step-2 evidence questions after Senior GO

The previous creation, PO-001 and PO-002 question sets remain required. Add:

69. Which exact class of material Actor decisions/transitions requires event-time basis retention, and which trivial/`NO_CHANGE` cases are excluded?
70. What typed Actor decision result/handoff can expose the bounded material source identities/then-values without carrying hidden reasoning?
71. Which SemanticEvent/history payload semantics can retain then-values versus stable immutable evidence refs?
72. How does deterministic validation prove every retained source was eligible to the Actor at T0 and materially relevant without requiring a full snapshot?
73. How are `world.knowledge` then-stances represented without creating a second current epistemic owner?
74. How are source-Actor directed relationship then-facets retained without implying reciprocity or a general relationship log?
75. How does ordinary persistence batching make required decision-basis evidence durable without introducing a per-decision remote publication?
76. How does a retrospective request retrieve only the bounded relevant history rather than scanning a campaign-wide event archive?
77. How is private historical evidence filtered for current player/PC disclosure/no-spoiler eligibility before Master/Commentator output?
78. What is the truthful terminal behavior when the retained basis is absent or insufficient?
79. Which current schema/catalog/runtime surfaces need realization alignment under the existing SemanticEvent owner?
80. Which direct acceptance tests prove T0 basis is used after T1 current-state changes?
81. How do performance tests prove zero extra serial LLM/tool operations solely for capture and zero unrelated-turn work?
82. Does any concrete Step-2 evidence invalidate the current `UPSTREAM_REOPEN_REQUIRED: NO` conclusion? If so, identify the exact owner and minimal insufficiency before reopening anything.

---

## 9. Failure scenarios later architecture must survive

The previously recorded creation and PO-001/PO-002 cases remain. Add at minimum:

39. NPC betrays the party based on `believed(P)` at T0; later NPC learns P was false; retrospective explanation incorrectly says the NPC knew it was false when deciding.
40. NPC acts because trust toward PC was `high` at T0; relationship later becomes `low`; replay substitutes the current low-trust state.
41. historical event stores only a ref to the mutable Actor/current-knowledge record; later mutation changes what the ref resolves to, so T0 basis cannot be recovered.
42. implementation stores a full Actor snapshot for every decision despite only two fields being material.
43. trivial NPC choices and `NO_CHANGE` assessments create decision-basis records and publication work.
44. implementation adds a second serial LLM call after each material Actor decision solely to generate historical rationale.
45. decision-basis capture performs extra remote reads even though the required T0 values are already in the bound Actor context.
46. each captured basis triggers a separate Git commit rather than normal persistence batching.
47. private NPC historical motive is stored correctly but leaked to a player whose current disclosure/PC eligibility does not permit it.
48. Story says why an NPC acted, but surviving admitted source evidence does not establish that exact motive; Master presents Story prose as canonical history.
49. historical evidence is incomplete; engine fills the gap by inferring a precise old motive from current Actor state.
50. chronology ordering is treated as proof of cognition/motive.
51. current Actor/world.knowledge state is overwritten/restored from retrospective evidence merely to replay history.
52. direct acceptance suite passes current Actor ownership tests but never mutates current state after T0, so current-state substitution remains undetected.

---

## 10. Direct acceptance obligation

Later authorized verification must exercise the complete scenario:

```text
T0:
  accepted NPC decision D
  based materially on a situation-specific subset of:
    K0 = current epistemic stance
    R0 = directed relationship facet(s)
    G0 = objective/goal/intention/commitment
    C0 = other eligible constraint/resource/circumstance

  -> retained historical basis B0 is sufficient to recover the material T0 subset

T1:
  legitimate current owner transitions produce K1 / R1 / G1 / C1

retrospective request:
  -> bounded retrieval of D/B0
  -> no substitution from K1/R1/G1/C1
  -> no hidden/private evidence leaked outside current eligibility
  -> if B0 insufficient, exact old motive is reported as not established
```

Verification must also establish:

- no additional LLM invocation solely to produce B0;
- no extra serial remote read solely to snapshot already-loaded T0 state;
- no separate remote publication solely for B0;
- no capture work on irrelevant turns;
- current Actor/knowledge owners remain unchanged by retrospective replay.

Existing `test_r2_7_wp04_actor_asset_conformance.py`, `REGRESSION_CASES:T04/T08`, performance/context/latency cases, persistence transaction cases and chronology cases are supporting evidence only. None currently proves this complete sequence.

---

## 11. Product Owner and reopen status

PO-003 already decides the product semantics. The evidence found no remaining human-owned product alternative, quality trade-off, compatibility choice or risk acceptance.

The technical conclusion is that the existing SemanticEvent/history owner can satisfy the new consumer with a bounded extension; current exact machine/test realization must later be aligned under normal authorized design/implementation work.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
```

---

## 12. Step-1 exit criteria

```text
[x] PO-003 canonical sources and arrival checkpoint inspected.
[x] Full directly affected owner/consumer subgraph reconstructed from current Project Map and owning artifacts.
[x] R2.2 Actor/current relationship boundary established.
[x] world.knowledge current versus LOG history boundary established.
[x] SemanticEvent/history owner and WP-10 family allocation assessed for sufficiency.
[x] Chronology, persistence/publication, Story/continuity and disclosure/context boundaries assessed.
[x] Master/Commentator retrospective consumers assessed.
[x] Current event schema and direct/supporting tests assessed without treating them as authority.
[x] PO-003 classified NEW CONSUMER + EXTENSION; no closed-architecture material insufficiency found.
[x] Current machine/test realization gap recorded downstream.
[x] Live-turn cost matrix and zero-extra-serial baseline recorded.
[x] Direct T0->T1 retrospective acceptance obligation recorded.
[x] Mandatory whole-project Task-Brief critic rerun on PO-003-expanded basis.
[x] All mechanically resolvable BLOCKING/SIGNIFICANT framing defects repaired.
[x] Product Owner gate rerun: HUMAN_DECISION_REQUIRED=NO / NEEDS_PO=NONE.
[x] UPSTREAM_REOPEN_REQUIRED=NO / ARCHITECTURE_REOPENED=NO.
[x] Step 2 unauthorized/unstarted.
[x] WP-20 unstarted.
[x] Implementation planning/substantive implementation unstarted.
```

Terminal state:

```text
WP19 STEP 1 COMPLETE — MANDATORY SENIOR REVIEW
```

Only explicit Senior GO may authorize WP-19 Step 2.