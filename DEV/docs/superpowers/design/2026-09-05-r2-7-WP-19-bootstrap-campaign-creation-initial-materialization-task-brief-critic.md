# R2.7 WP-19 — Bootstrap / Campaign Creation / Initial Materialization — Whole-Project Task-Brief Critic

Status: **STEP 1 PO-003 WHOLE-PROJECT CRITIC RERUN COMPLETE — MANDATORY SENIOR REVIEW CANDIDATE**

Date: 2026-09-05

Original critic basis: `5fc24905be5c9e1b47929ee9e7b49ea8b9f2a053`

Senior-recovery basis: `df5fe6441c2b85e9cbffcb6f83caa885501da794`

PO-001/PO-002 expanded basis: `4b7411b10b30cc191141826aacb3b0c88e7eeb37`

PO-003 rerun basis: `341cc592fbc53247d0d7f8d38eb07ec4297cd45d`

This is the mandatory whole-project Step-1 Task-Brief critic rerun required after PO-003 invalidated the prior review basis. It follows `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md` and independently reconstructs the current Actor/knowledge/history/record-family/chronology/persistence/Story/context/retrospective/performance/test subgraph rather than treating the arrival checkpoint or prior critic as an answer key.

The critic does not perform Senior review, grant Senior GO, begin Step 2, reopen architecture, or implement the resulting downstream realization obligations.

---

## 1. Independent reconstruction

The critic retained the already-closed bootstrap/materialization, SR19-01 verification and PO-001/PO-002 consumer legs, then independently added:

```text
PO-003 product-semantic owner
    -> material Actor decision/transition
         -> R2.2 current Actor-private continuity
         -> R2.2 directed relationships
         -> Step-4 current world.knowledge
         -> other native current constraints/resources as applicable
         -> R2.3/WP-09 eligible bounded role context
         -> R2.4/WP-08 material Actor phase
    -> accepted decision/transition
    -> Step-4 LOG/runtime.semantic_event history owner
         -> WP-10 existing history record-family allocation
         -> WP-15 chronology evidence where applicable
         -> WP-13 ordinary native durability/publication
    -> R2.1/WP-18 Story/continuity projection/orientation
    -> PO-001 ordinary Master retrospective OR authorized Commentator
         -> bounded historical retrieval
         -> current player/PC/disclosure/no-spoiler eligibility
         -> truthful explanation/replay
```

The critic separately inspected the negative paths:

```text
full Actor snapshots
per-turn psychology history
second world.knowledge history owner
Story-as-motive-authority
mutable-current-ref substitution
separate post-decision LLM rationale pass
per-decision remote publication
unrelated-turn bookkeeping/history scans
```

---

## 2. Findings summary

Previously closed findings remain closed unless explicitly contradicted; none was contradicted.

PO-003 rerun findings:

```text
PO003_RERUN_BLOCKING:        1
PO003_RERUN_SIGNIFICANT:     6
PO003_RERUN_MINOR:           0

UNRESOLVED_BLOCKING:         0
UNRESOLVED_SIGNIFICANT:      0
HUMAN_DECISION_REQUIRED:     NO
NEEDS_PO:                    NONE
UPSTREAM_REOPEN_REQUIRED:    NO
ARCHITECTURE_REOPENED:       NO
WP19_STEP2_AUTHORIZED:       NO
STEP2_STARTED:               NO
WP20_STARTED:                NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
```

Every BLOCKING/SIGNIFICANT finding below was mechanically resolvable as Step-1 evidence/framing/status work and is closed in the current Source Manifest/Task Brief/status package. No runtime/schema/test implementation was used to hide a framing defect.

---

## 3. Retained closed findings

```text
F19-S1-01 BLOCKING    CLOSED
F19-S1-02 BLOCKING    CLOSED
F19-S1-03 SIGNIFICANT CLOSED
F19-S1-04 SIGNIFICANT CLOSED
F19-S1-05 SIGNIFICANT CLOSED
F19-S1-06 SIGNIFICANT CLOSED
F19-S1-07 SIGNIFICANT CLOSED
F19-S1-08 MINOR       CLOSED
SR19-01   SIGNIFICANT CLOSED

F19-PO-01 BLOCKING    CLOSED
F19-PO-02 SIGNIFICANT CLOSED
F19-PO-03 SIGNIFICANT CLOSED
F19-PO-04 SIGNIFICANT CLOSED
F19-PO-05 SIGNIFICANT CLOSED
F19-PO-06 MINOR       CLOSED AS ROUTING / DOWNSTREAM VERIFICATION OBLIGATION
```

PO-003 adds a new consumer/evidence obligation. Topic overlap alone does not reopen these findings.

---

## 4. PO-003 finding dispositions

### F19-PO003-01 — BLOCKING — current Step-1 basis omitted an applicable canonical Product Owner requirement

**Defect**

The PO-001/PO-002 Source Manifest/Task Brief/critic were review-ready only before PO-003 arrived. PO-003 directly changes the evidence needed to support the existing retrospective “why did the NPC act that way?” consumer. Continuing to Senior review on the old basis would omit a current canonical product requirement.

**Resolution**

CLOSED. The Source Manifest and Task Brief now include the PO-003 semantic owner, the entire current dependency subgraph, evidence classification, live-turn performance matrix, direct acceptance obligation and Product Owner/reopen result. The critic has been rerun on that expanded basis.

**Human decision required:** NO — semantics were already owner-approved.

---

### F19-PO003-02 — SIGNIFICANT — owner sufficiency and machine realization were at risk of being conflated

**Defect**

A weak audit could make either opposite error:

1. declare SemanticEvent fully sufficient merely because `event.schema.yaml` contains generic `factual_changes[]` / `knowledge_changes[]`; or
2. declare an upstream history owner missing merely because the current schema lacks an explicit decision-basis field.

Both ignore semantic ownership.

Current Step-4 already allocates `LOG/runtime.semantic_event` as compact durable semantic history / causal evidence and routes full `world.knowledge` transition history to it. WP-10 already allocates SemanticEvent in the durable history/delivery namespace. The owner therefore exists and can satisfy the consumer.

Current machine realization still lacks direct proof that a qualifying decision retains all material mutable T0 evidence. Generic physical extensibility is not acceptance evidence.

**Resolution**

CLOSED. The Task Brief now classifies PO-003 as:

```text
NEW CONSUMER + EXTENSION
CLOSED_ARCHITECTURE_MATERIAL_INSUFFICIENCY: NO
CURRENT_MACHINE_TEST_REALIZATION_GAP: YES
```

Exact schema/test realization remains downstream. No upstream reopen is declared.

---

### F19-PO003-03 — SIGNIFICANT — current-state owners could be duplicated or substituted for historical evidence

**Defect**

Without explicit separation, future work could:

- turn R2.2 Actor continuity into a psychology log;
- store a duplicate writable knowledge stance inside history;
- reference only a mutable current Actor/knowledge row and later resolve it at T1;
- restore current Actor state from historical evidence during replay.

That would violate R2.2, Step-4 and PO-003.

**Resolution**

CLOSED. The current framing requires:

- R2.2 remains current non-epistemic Actor-private authority;
- `world.knowledge` remains current epistemic authority;
- directed relationships remain source-Actor current views;
- SemanticEvent/history retains only bounded event-time evidence for qualifying material decisions;
- then-values or immutable historical refs must be sufficient to recover T0 semantics;
- retrospective evidence cannot mutate current owners.

---

### F19-PO003-04 — SIGNIFICANT — latency/performance could regress through an implicit second reasoning or I/O path

**Defect**

PO-003 can be implemented badly by adding:

- a serial post-decision LLM “why did you do that?” pass;
- rereads of Actor/knowledge state already loaded for the decision;
- a separate Git publication for each retained basis;
- bookkeeping/history work on unrelated turns.

This would violate R2.4 role!=call, R2.3/WP-09 bounded retrieval, `PLAY_POLICY.md` latency policy and current persistence batching expectations.

**Resolution**

CLOSED in framing. Candidate A is explicitly evaluated as the baseline:

```text
additional sequential LLM calls:                    0
additional serial remote/tool reads solely for basis: 0
additional separate remote publications:            0
additional context/output: bounded typed evidence only
irrelevant-turn work:                                0
```

The basis is captured as a typed byproduct of already-required material Actor/Master decision work and joins ordinary history persistence batching.

Full snapshots, later current-state reconstruction and a dedicated serial rationale pass are explicitly compared and rejected as baseline. If future correctness evidence requires a new serial round-trip, Step 2 must treat it as a material architecture/performance problem.

---

### F19-PO003-05 — SIGNIFICANT — no direct T0 -> T1 -> retrospective acceptance case exists

**Defect**

Current tests cover pieces but not the defining failure mode. In particular:

- `test_r2_7_wp04_actor_asset_conformance.py` protects sparse current Actor ownership and directed relationships;
- `REGRESSION_CASES:T04` prevents current NPC knowledge leakage;
- `T08` protects bounded old-NPC retrieval;
- performance/context/latency cases protect bounded/local work;
- persistence transaction cases protect zero-I/O ordinary turns and coherent batches;
- chronology cases protect lawful source ordering/locality.

None directly proves that an NPC decision made with K0/R0/G0 remains explainable from K0/R0/G0 after current owners become K1/R1/G1.

**Resolution**

CLOSED AS STEP-1 ROUTING / DOWNSTREAM VERIFICATION OBLIGATION. The Task Brief now requires an explicit acceptance case that mutates current state after T0 and verifies the retrospective answer/replay uses retained T0 basis, not current state. It also must test the zero-extra-serial performance contract.

Tests are not implemented in Step 1.

---

### F19-PO003-06 — SIGNIFICANT — private historical evidence could bypass current disclosure/no-spoiler eligibility

**Defect**

A correctly retained NPC motive/belief/relationship basis may itself be private. An implementation that equates “historically available to Master/Story” with “visible to current player/PC/Commentator session” would create a spoiler/knowledge leak.

Story also cannot establish an exact motive merely through derived prose when admitted historical evidence is insufficient.

**Resolution**

CLOSED. The current frame routes retrospective evidence through R2.3/WP-09 role/purpose/player/PC eligibility and current Step-4 knowledge/disclosure rules before visible output. Story remains orientation/projection; material historical claims escalate to admitted history. Missing basis produces a supported-limit answer rather than an invented exact motive.

---

### F19-PO003-07 — SIGNIFICANT — current cursor/status surfaces could return Senior to the pre-PO-003 package

**Defect**

`DEV/CURRENT_PROGRESS.md` correctly reopened Step 1 for PO-003, while the task-local durable audit cursor still identified the earlier PO-001/PO-002 package as the current Senior-review basis. Leaving any current locator in that state after integration would make the project cursor self-contradictory.

**Resolution**

CLOSED. Current WP-19 status surfaces are synchronized to:

```text
WP19 STEP 1 COMPLETE — MANDATORY SENIOR REVIEW
PO-003 INTEGRATED
WHOLE-PROJECT CRITIC RERUN COMPLETE
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
```

Historical checkpoints remain historical and are not rewritten to pretend PO-003 existed earlier.

---

## 5. Owner and reopen analysis

### R2.2 Actor / directed relationships

Current owner is sufficient. PO-003 explicitly does not ask R2.2 to become history. No reopen.

### Step-4 `world.knowledge`

Current owner is sufficient; Step-4 already assigns full epistemic transition history to LOG/SemanticEvents. No reopen.

### Step-4 LOG / SemanticEvent

This is the natural existing historical-evidence owner. Its current semantic scope includes durable semantic history and causal evidence. PO-003 adds a conditional bounded retention obligation for a new retrospective consumer. This is an **EXTENSION**, not a contradiction or material semantic-owner insufficiency.

### WP-10 record-family allocation

Already has the required history family. No new family and no reopen.

### WP-15 chronology

Supporting causal/order/time evidence only; no motive/cognition authority. No reopen.

### WP-13 persistence/publication

Existing owner can carry required history through normal durability batching. No new publication authority and no reopen.

### R2.1 / WP-18 Story

Projection/orientation consumer only. No new Story authority and no reopen.

### R2.3/R2.4/WP-08/WP-09

Existing bounded context and single-context logical-role execution can carry the required Actor decision result/evidence without requiring role=call. No reopen.

### Current machine/test realization

Needs downstream alignment under the existing owner. This does not reopen semantic architecture in Step 1.

```text
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
```

---

## 6. Product Owner boundary rerun

### Product semantics

Settled by PO-003: retain bounded event-time basis for qualifying material decisions; no full psychology archive; no current-state substitution; no invented exact motive when evidence is insufficient.

### Canonical authority / ownership

Evidence resolves placement to the existing historical-evidence owner family without a new owner.

### Compatibility policy

Unchanged. Future released-campaign schema/engine/ruleset migration remains WP-20.

### Hard-to-reverse lifecycle/product behavior

No new lifecycle state or mode is introduced.

### Material quality/performance trade-off

Current evidence supports the zero-extra-serial baseline. No product preference is required to choose between an unnecessary second model call and the existing decision path.

### Explicit risk acceptance

None.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
```

---

## 7. Verification/scenario dispositions

| Evidence | Disposition for PO-003 |
|---|---|
| `DEV/TESTS/test_r2_7_wp04_actor_asset_conformance.py` | CURRENT SUPPORTING — sparse current Actor/relationship owner and no hidden reasoning; not history proof. |
| `DEV/TESTS/REGRESSION_CASES.md:T04` | CURRENT SUPPORTING — NPC knowledge eligibility; not historical then-state proof. |
| `REGRESSION_CASES.md:T08` | CURRENT SUPPORTING — bounded old-NPC retrieval. |
| `DEV/TESTS/PERFORMANCE_CASES.md:P01/P03/P07/P10` | CURRENT SUPPORTING — bounded reasoning without flattening nuance/correctness. |
| `DEV/TESTS/RUNTIME_CONTEXT_RESEARCH_CASES.md:C04/C07` | CURRENT SUPPORTING — no irrelevant retrieval; lazy campaign data. |
| `DEV/TESTS/RUNTIME_SCOPE_LATENCY_CASES.md:RL03/RL05` | CURRENT SUPPORTING — targeted operations/no maintenance leakage. |
| `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md:PT01/PT02/PT14/PT15` | CURRENT SUPPORTING — zero remote I/O when no durability edge; coherent batching when one exists. |
| `DEV/TESTS/CHRONOLOGY_CASES.md:C03/C15` | CURRENT SUPPORTING — source-aware/local chronology. |
| `GAME/SCHEMA/event.schema.yaml` | CURRENT PHYSICAL SUPPORT / NOT COMPLETE SEMANTIC PROOF — append-only event can carry generic changes/refs but explicit decision-basis contract is not proven. |
| Step-3 mechanical-event executable tests | OUTSIDE DIRECT PO-003 ACCEPTANCE. |
| Story-retirement executable test | OUTSIDE DIRECT PO-003 ACCEPTANCE. |
| direct T0 decision -> T1 mutable-state change -> retrospective T0-basis test | MISSING / ROUTED DOWNSTREAM. |
| direct zero-extra-serial capture test | MISSING / ROUTED DOWNSTREAM. |

No test/schema file is changed by this Step-1 critic rerun.

---

## 8. Final critic gate

```text
PREVIOUS_F19_S1_FINDINGS:       RETAINED / CLOSED
SR19_01:                        RETAINED / CLOSED
PREVIOUS_F19_PO_FINDINGS:       RETAINED / CLOSED

F19_PO003_01 BLOCKING:          CLOSED — PO-003 integrated into current basis
F19_PO003_02 SIGNIFICANT:       CLOSED — semantic owner sufficiency separated from machine realization gap
F19_PO003_03 SIGNIFICANT:       CLOSED — current owners separated from historical basis / no T1 substitution
F19_PO003_04 SIGNIFICANT:       CLOSED — explicit zero-extra-serial performance baseline and alternatives
F19_PO003_05 SIGNIFICANT:       CLOSED AS ROUTING — direct T0/T1 acceptance obligation recorded downstream
F19_PO003_06 SIGNIFICANT:       CLOSED — disclosure/no-spoiler/history-source escalation framed
F19_PO003_07 SIGNIFICANT:       CLOSED — current status/cursor surfaces synchronized

PO003_RERUN_BLOCKING:           1
PO003_RERUN_SIGNIFICANT:        6
PO003_RERUN_MINOR:              0
UNRESOLVED_BLOCKING:            0
UNRESOLVED_SIGNIFICANT:         0
HUMAN_DECISION_REQUIRED:        NO
NEEDS_PO:                       NONE
UPSTREAM_REOPEN_REQUIRED:       NO
ARCHITECTURE_REOPENED:          NO
WP19_STEP2_AUTHORIZED:          NO
STEP2_STARTED:                  NO
WP20_STARTED:                   NO
IMPLEMENTATION_PLANNING_STARTED:NO
SUBSTANTIVE_IMPLEMENTATION_STARTED:NO
```

### Critic recommendation to Senior

The current WP-19 Step-1 package now includes PO-003, its complete directly affected owner/consumer/performance/test graph, explicit owner-versus-realization classification, the mandatory T0/T1 retrospective acceptance obligation, and zero unresolved BLOCKING/SIGNIFICANT framing defects.

**Recommendation:** return the package to the mandatory Senior review gate.

This critic does not grant Senior GO and does not perform Senior review itself.