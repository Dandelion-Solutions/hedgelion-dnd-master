# R2.7 WP-19 — Bootstrap / Campaign Creation / Initial Materialization — Source Manifest

Status: **STEP 1 COMPLETE — PO-003 INTEGRATED / EVIDENCE BASIS EXPANDED — MANDATORY SENIOR REVIEW**

Date: 2026-09-05

Current Step-1 integration basis: `341cc592fbc53247d0d7f8d38eb07ec4297cd45d`

Domain:

> **Bootstrap / campaign creation / initial materialization**

This manifest is the current task-specific evidence route required by `DEV/DESIGN_PROCESS.md` and `DEV/ARCHITECTURE/DESIGN_PROCESS.md`. It retains the previously completed bootstrap/materialization, SR19-01 verification, and PO-001/PO-002 consumer evidence, then expands the current basis for Product Owner input `PO-003` — Historical Actor Decision Basis.

The PO-003 arrival checkpoint remains historical provenance. This manifest does not rewrite earlier checkpoints as if PO-003 existed before its acceptance.

Companion artifacts:

- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief-critic.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-po-003-arrival-integration-checkpoint.md` — historical arrival checkpoint only.

This Step-1 unit does not begin Step 2, WP-20, implementation planning, substantive implementation, runtime/schema/test realization, or Senior review.

---

## 1. Process and Product Owner authority

| Source | Role / disposition |
|---|---|
| `AGENTS.md` | Current repository/process constraints. |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | Connector-only remote transport/publication/verification overlay. |
| `DEV/DESIGN_PROCESS.md` | Canonical Source Manifest, evidence, synthesis and human-decision process. |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | Mandatory whole-project Step-1 critic and Senior stop. |
| `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md` | Current PO routing/classification/reopen/NEEDS_PO process. |
| `DEV/PRODUCT_OWNER_INPUT.md` | Product intent/routing ledger; `PO-001..PO-003` inspected. |
| `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md` | Accepted PO-001/PO-002 semantic authority. |
| `DEV/docs/superpowers/specs/2026-09-05-hdm-historical-actor-decision-basis-owner-decision.md` | Accepted PO-003 semantic authority. |
| `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-po-003-arrival-integration-checkpoint.md` | Historical arrival/cursor evidence; not architecture authority. |
| `DEV/CURRENT_PROGRESS.md` | Global current-state/gate authority. |
| `DEV/PROJECT_MAP.md` | Derivative routing aid used to reconstruct the direct and indirect subgraph. |

PO-003 already settles product semantics. Exact placement/schema/performance realization is technical architecture work and does not create `NEEDS_PO` by itself.

---

## 2. Retained pre-PO-003 evidence

The complete prior WP-19 evidence remains applicable unless explicitly qualified below.

### 2.1 Original Step-1 findings — retained / closed

1. `F19-S1-01 / BLOCKING` — exact `ruleset_set_sha256` propagation framing.
2. `F19-S1-02 / BLOCKING` — scaffold / provisional / READY_PC / PLAY_READY separation.
3. `F19-S1-03 / SIGNIFICANT` — branch/storage/access/current storage-v3 versus stale-v2 reconciliation.
4. `F19-S1-04 / SIGNIFICANT` — campaign identity/card/config/current projection ownership.
5. `F19-S1-05 / SIGNIFICANT` — first from-scratch publication versus later durability/session/resume.
6. `F19-S1-06 / SIGNIFICANT` — multiplayer initial authority.
7. `F19-S1-07 / SIGNIFICANT` — machine/template/schema/test reverse audit.
8. `F19-S1-08 / MINOR` — WP-20/dormant-neighbor boundary.

### 2.2 SR19-01 verification evidence — retained / closed

The independent verification/scenario expansion remains current. Material dispositions include:

- `BOOTSTRAP_STORAGE_REGRESSION_CASES:B12` — STALE/SUPERSEDED Storage-v2 expectation;
- `B22` — STALE/SUPERSEDED tag-derived runtime provenance;
- `B23` — STALE/SUPERSEDED visible technical setup staging;
- `B25` — CURRENT WITH QUALIFIER; readiness requires READY_PC + PLAY_READY and checkpoint is not inherently mandatory;
- `CAMPAIGN_CARD_CASES:C12` — STALE/SUPERSEDED paused icon expectation;
- `REGRESSION_CASES:T13` — STALE/SUPERSEDED manifest-only campaign discovery;
- access/storage-main guest cases — CURRENT WITH QUALIFIERS under current runtime-package/owner model;
- engine-update/migration cases — WP-20 downstream except creation-adjacent identity evidence;
- pre-release audit snapshot — HISTORICAL ONLY.

Passing tests remain evidence, not semantic authority.

### 2.3 PO-001/PO-002 evidence — retained / closed

PO-001 remains a NEW CONSUMER BINDING / EXTENSION: an authorized active player may ask retrospective/history questions through ordinary Master interaction, under existing bounded history retrieval and current disclosure/no-spoiler rules.

PO-002 remains a NEW NAVIGATION CONSUMER COMPOSITION: save succeeds first, then the selected gameplay context exits to the existing campaign-selection gate; exit alone does not pause/complete/archive/leave/deactivate/transfer control/stop multiplayer.

No PO-003 evidence reopens those resolved findings merely by overlap.

---

## 3. PO-003 dependency reconstruction

The independently reconstructed current subgraph is:

```text
material NPC/Actor decision or material cognitive transition
    -> R2.2 source-Actor current non-epistemic continuity
         -> current objective / next intention / commitments
         -> directed relationship facets
    -> Step-4 world.knowledge current epistemic stance
    -> current native world/resource/constraint owners as applicable
    -> R2.3 / WP-09 bounded role-context acquisition and eligibility
    -> R2.4 / WP-08 material Actor phase inside ordinary single-context turn envelope
    -> accepted material decision / transition
    -> LOG / runtime.semantic_event durable semantic history / causal evidence
         -> WP-10 existing history/delivery record-family allocation
         -> chronology refs/evidence under WP-15 where temporally material
         -> ordinary native persistence/publication under WP-13
    -> R2.1 continuity / WP-18 Story projection as optional source-bound orientation
    -> later explicit retrospective consumer
         -> ordinary active-player Master consumer from PO-001
         -> or authorized Commentator consumer
    -> R2.3/WP-09 bounded historical retrieval
    -> current player/principal/PC eligibility + world.knowledge/runtime.disclosure/no-spoiler filtering
    -> player/spectator-visible explanation or replay
```

The historical basis is retrospective evidence. It cannot become current Actor or `world.knowledge` authority and cannot restore/overwrite current cognition.

---

## 4. Owner-by-owner classification

| Boundary | Current owner evidence | PO-003 disposition |
|---|---|---|
| Current Actor cognition/intent | R2.2 source-Actor sparse continuity | **CURRENT / SUFFICIENT OWNER.** No historical store should be added here. |
| Directed relationships | R2.2 source-Actor directed sparse views | **CURRENT / SUFFICIENT CURRENT OWNER.** Historical consumer needs bounded then-value evidence, not a second relationship owner. |
| Current epistemic stance | Step-4 `world.knowledge` | **CURRENT / SUFFICIENT CURRENT OWNER.** Full transition history already routes to LOG/SemanticEvents. |
| Historical semantic/causal evidence | Step-4 `LOG/runtime.semantic_event` | **EXTENSION.** Existing owner/family is semantically capable of retaining bounded event-time decision basis. New consumer makes that evidence mandatory for qualifying material decisions where mutable state would otherwise be lost. |
| Durable record-family allocation | WP-10 history/delivery namespace incl. SemanticEvent | **SUFFICIENT.** No new durable psychology/history family is required. |
| Chronology | WP-15 typed chronology evidence | **SUFFICIENT SUPPORT.** Orders/anchors evidence but does not own motive/cognition. |
| Persistence/publication | WP-13 native-domain durability/publication | **SUFFICIENT TRANSPORT.** Required historical evidence participates in normal owner batching; no new save owner/publication boundary. |
| Story/continuity | R2.1 + WP-18 | **SUFFICIENT PROJECTION/ROUTING ONLY.** Story may orient but cannot establish private historical basis. |
| Master retrospective | PO-001 ordinary gameplay consumer | **NEW CONSUMER strengthened by PO-003.** Must use event-time basis for material historical claims. |
| Commentator retrospective | Step-4/WP-18 Commentator role | **NEW/EXISTING CONSUMER EXTENSION.** Still bound by Story/source and disclosure eligibility. |
| Context/disclosure | R2.3/WP-09 + Step-4 disclosure + WP-08 role containment | **SUFFICIENT.** Physical storage/repository visibility never widens eligibility. |

### Classification result

```text
PO003_CLASSIFICATION:
    NEW CONSUMER
    + EXTENSION

CLOSED_ARCHITECTURE_MATERIAL_INSUFFICIENCY: NO
CURRENT_MACHINE_TEST_REALIZATION_GAP: YES
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
```

The distinction is material. The closed semantic architecture already allocates durable semantic causal history to `LOG/SemanticEvent` and explicitly routes full knowledge transition history there. PO-003 does not require a different semantic owner. It requires the existing history owner to carry a bounded additional evidence obligation for a newly explicit consumer.

`GAME/SCHEMA/event.schema.yaml` is not direct proof of complete realization. Its append-only `semantic_event` shape has generic `delta.factual_changes[]` / `knowledge_changes[]`, causal refs and notes, but no explicit normalized contract that proves a qualifying material Actor decision retained all required then-values or immutable historical refs. That is a downstream realization/test gap under the existing owner, not evidence that the owner architecture is absent.

---

## 5. Historical-evidence sufficiency rule

For a qualifying material decision at event time `T0`:

```text
current mutable source at T0
    -> value/stance actually material to decision
    -> accepted decision/transition
    -> bounded event-time historical basis
```

The retained basis may use either:

1. bounded then-values; or
2. stable refs to immutable historical evidence that is sufficient to reconstruct those then-values.

A ref only to a mutable current Actor or `world.knowledge` record is insufficient if its meaning can later change.

The basis is situation-specific. It must not become:

- a full Actor snapshot;
- a per-turn psychology archive;
- a private plan graph;
- hidden chain-of-thought or reasoning trace;
- a duplicate current knowledge/relationship owner.

When surviving history is insufficient, later Master/Commentator output must report the supported limit rather than infer an exact historical motive from current state.

---

## 6. Mandatory performance / latency evidence

### 6.1 Candidate A — bounded basis inside the already-required Actor/Master decision path

**Direction:** capture the small set of material eligible source identities/then-values (or immutable historical refs) as a typed byproduct of the already-required material Actor decision/transition, validate deterministically, and retain it with ordinary SemanticEvent/history batching.

Live-turn cost target:

| Cost dimension | Required baseline |
|---|---|
| Additional sequential LLM calls | **0** |
| Additional serial remote/tool reads | **0 solely for history capture**; reuse already required role-context/current-owner reads. |
| Additional remote writes/publications | **0 separate publications**; basis joins the normal accepted LOG/native persistence batch. |
| Additional required context/output | Bounded structured identities/then-values for only materially relevant evidence; no full Actor state, raw bundle or hidden rationale. |
| Work on irrelevant turns | **0**; no capture work for trivial choices, `NO_CHANGE`, irrelevant Actors or unrelated turns. |

**Disposition:** preferred Step-2 candidate direction if Senior authorizes Step 2. It is compatible with R2.2 sparse/event-driven cognition, R2.4 role!=call, WP-09 bounded context, `PLAY_POLICY.md` latency law and `PERSISTENCE_TRANSACTION_CASES:PT01/PT02` zero-I/O/batched-publication expectations.

### 6.2 Candidate B — full Actor/knowledge snapshots

Would increase context, storage and serialization volume, create pressure toward per-turn writes, and duplicate current owners.

**Disposition:** REJECTED BY CURRENT OWNER + PO SEMANTICS.

### 6.3 Candidate C — reconstruct motive later from current state plus mutable refs

Can silently substitute `T1` cognition/knowledge/relationship state for `T0` and may require expensive history reconstruction.

**Disposition:** INSUFFICIENT unless every material then-value is independently recoverable from immutable admitted evidence.

### 6.4 Candidate D — separate post-decision LLM “historical rationale” pass

Adds a serial model round-trip on the gameplay critical path, invites hidden-reasoning retention and duplicates work already performed by the material Actor/Master decision phase.

**Disposition:** NOT BASELINE. If later evidence proves correctness cannot be met without an additional serial LLM/tool round-trip, that is a material architecture/performance problem requiring explicit alternative comparison; it must not be silently adopted.

---

## 7. Direct verification / acceptance obligations

Existing evidence is supporting but incomplete:

- `DEV/TESTS/test_r2_7_wp04_actor_asset_conformance.py` — CURRENT: proves one sparse current Actor continuity owner, directed relationship facets and no hidden-reasoning fields.
- `DEV/TESTS/REGRESSION_CASES.md:T04` — CURRENT SUPPORTING: NPC cannot use knowledge it lacks.
- `REGRESSION_CASES:T08` — CURRENT SUPPORTING: old-NPC retrieval is bounded; no all-history preload.
- `DEV/TESTS/PERFORMANCE_CASES.md:P01/P03/P07/P10` — CURRENT SUPPORTING: bounded local work while retaining nuanced Actor factors and correctness gates.
- `DEV/TESTS/RUNTIME_CONTEXT_RESEARCH_CASES.md:C04/C07` — CURRENT SUPPORTING: irrelevant modules/data add no retrieval work; campaign data remains lazy.
- `DEV/TESTS/RUNTIME_SCOPE_LATENCY_CASES.md:RL03/RL05` — CURRENT SUPPORTING: targeted schema access and no maintenance work at ordinary boundaries.
- `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md:PT01/PT02/PT14/PT15` — CURRENT SUPPORTING: zero remote I/O absent durability boundary and coherent batched publication when persistence is required.
- `DEV/TESTS/CHRONOLOGY_CASES.md:C03/C15` — CURRENT SUPPORTING: knowledge follows lawful source; chronology/history work stays bounded.
- current Step-3 mechanical-event and Story-retirement executable tests — OUTSIDE DIRECT PO-003 ACCEPTANCE; they do not prove Actor decision-basis retention.

### Missing direct acceptance case — downstream obligation

A later authorized realization must directly prove at least:

```text
T0:
  NPC decision D uses eligible current K0 knowledge stance
  + R0 directed relationship state
  + G0 objective/commitment/other situation-specific material basis
  -> accepted D retains bounded event-time basis

T1:
  current owners legitimately change to K1 / R1 / G1

retrospective:
  authorized Master or Commentator asks why/replays D
  -> uses retained T0 basis
  -> does not substitute K1/R1/G1
  -> respects current disclosure/no-spoiler/context eligibility
  -> if T0 evidence is incomplete, does not invent an exact historical motive
```

The same acceptance family must prove no extra serial LLM pass solely for decision-basis capture, no unrelated-turn bookkeeping/retrieval, and no separate remote publication requirement.

This missing case is a downstream verification obligation. Step 1 does not edit tests.

---

## 8. Product Owner / reopen gate

| Watch area | Result |
|---|---|
| Product semantics | Settled by PO-003. |
| Current Actor / knowledge / relationship ownership | Already allocated and sufficient; no duplicate owner needed. |
| Durable historical-evidence owner/family | Existing SemanticEvent/history owner is sufficient; requires bounded consumer-driven extension. |
| Compatibility policy | Unchanged; WP-20 remains future released-campaign evolution/migration. |
| Performance trade-off | Evidence supports zero-extra-serial baseline; no unresolved product preference. |
| Disclosure/no-spoiler | Existing owners remain controlling. |
| Risk acceptance | None surfaced. |

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
```

---

## 9. Completeness gate

```text
[x] PO-003 ledger entry, accepted owner decision, arrival checkpoint and current progress inspected.
[x] R2.2 current cognition/intent and directed-relationship owners inspected.
[x] Step-4 world.knowledge, disclosure, SemanticEvent/history and Master/Commentator role boundaries inspected.
[x] R2.1 continuity/history and WP-18 Story projection boundaries inspected.
[x] R2.3/R2.4 and WP-08/WP-09 context/execution/eligibility boundaries inspected.
[x] WP-10 record-family allocation inspected.
[x] WP-13 durability/publication and WP-15 chronology boundaries inspected.
[x] Current GAME/SCHEMA semantic-event realization inspected without treating physical extensibility as semantic proof.
[x] PLAY_POLICY/runtime latency boundary inspected.
[x] Direct and supporting DEV/TESTS consumers inspected; direct PO-003 acceptance gap recorded.
[x] NEW CONSUMER / EXTENSION / MATERIAL INSUFFICIENCY classification established per boundary.
[x] Candidate live-turn costs compared; zero-extra-serial baseline made explicit.
[x] Product Owner decision gate rerun; NEEDS_PO=NONE.
[x] Whole-project Task-Brief critic rerun on PO-003-expanded basis.
[x] All applicable BLOCKING/SIGNIFICANT framing defects repaired.
[x] Step 2 remains unauthorized/unstarted.
[x] WP-20 remains unstarted.
[x] Implementation planning and substantive implementation remain unstarted.
```

The package returns to **mandatory Senior review**. This artifact does not grant Senior GO.