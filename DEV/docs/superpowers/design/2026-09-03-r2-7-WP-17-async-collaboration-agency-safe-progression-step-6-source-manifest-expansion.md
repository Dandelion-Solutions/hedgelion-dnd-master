# R2.7 WP-17 — Async Collaboration / Agency-Safe Progression — Step-6 Independent Source Manifest Expansion

Status: **STEP 6 — INDEPENDENT WHOLE-PROJECT SOURCE RECONSTRUCTION COMPLETE**

Date: 2026-09-03

Candidate under attack:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-step-5-candidate-spec.md`.

This expansion was reconstructed independently from current `DEV/PROJECT_MAP.md` and the current repository owner/consumer graph. The Step-2 source list was not used as the review universe. Overlap exists only because independent routes reached the same owners.

The manifest remains open-world through Step 8.

---

## 1. Independent reconstruction routes

Step 6 rebuilt the relevant graph through six attack routes:

```text
A. durable runtime owner / recovery root
   PROJECT_MAP persistence/recovery
   -> Catalog Contracts / admission ledger / WP-11 / WP-14
   -> collaboration family route
   -> PLAYER/session/index discovery consumers

B. accepted human input / execution handoff
   PROJECT_MAP deterministic mechanics/execution
   -> Step-3 final spec
   -> Interaction / IntentPlan / IntentClause / RuntimeCommand schemas
   -> command + resume-ordering tests

C. shared mutable currentness
   PROJECT_MAP multiplayer/shared mutable state
   -> WP-16 final owner
   -> MULTIPLAYER / LIVE_SCENE / PERSISTENCE consumers
   -> campaign/LIVE currentness and no-distributed-transaction law

D. chronology / safe frontier
   PROJECT_MAP chronology
   -> WP-15 final owner
   -> CHRONOLOGY runtime consumer
   -> Step-3 accepted execution continuity

E. recipient information / catch-up
   PROJECT_MAP LLM reasoning/information/presentation
   -> Step 4 / R2.3 / Step 5.11 / Step 5.12
   -> INFORMATION / SESSION consumers

F. identity/class collision and machine alignment
   PROJECT_MAP catalog/class ownership
   -> Catalog Contracts / Entity Structures / admission ledger
   -> Rule Element model / core catalog
   -> current PLAYER and index machine surfaces
```

---

## 2. Newly material Step-6 sources / direct evidence

### 2.1 Runtime admission and recovery discovery

| Source | Role | Step-6 use |
|---|---|---|
| `DEV/CATALOG/catalog-admission-ledger.json` | `CURRENT_MACHINE_CONTRACT` | Confirms `runtime.collaboration_obligation` is actively admitted at catalog-class level; this does not supply exact recovery routing or lifecycle fields. |
| `GAME/SCHEMA/player.schema.yaml` | `CURRENT_MACHINE_CONTRACT` | Current PLAYER has identity/control/private-record/policy fields but no current collaboration-obligation routing companion. |
| `GAME/CAMPAIGN/INDEX/PLAYER_INDEX.yaml` | `CURRENT_MACHINE_CONTRACT / NEGATIVE_EVIDENCE` | Current baseline index is only the ordinary PLAYER index scaffold; it is not a collaboration reverse index or semantic authority. |
| WP-11 canonical spec | `CANONICAL_OWNER` | Collaboration family has direct known-ID route and **no baseline collaboration index**. |
| WP-14 canonical spec | `CANONICAL_OWNER` | Current recovery roots must be discoverable through typed bounded native routing; ordinary recovery cannot scan all runtime records/directories/history. |

Independent conclusion: candidate law WP17-56 names a bounded-discovery requirement but does not actually allocate the correctness-critical route that makes it possible.

### 2.2 Accepted input to execution boundary

| Source | Role | Step-6 use |
|---|---|---|
| Step-3 canonical execution spec | `CANONICAL_OWNER` | Every accepted executable root remains bound to an existing Interaction/IntentClause; RuntimeCommand/Procedure/Continuation own execution/idempotency/resume after acceptance. |
| `DEV/SCHEMAS/runtime-command-state.schema.json` | `CURRENT_MACHINE_CONTRACT` | Every command requires `interaction_id`, `intent_plan_id`, `clause_id`; accepted command is already an execution owner. |
| `DEV/SCHEMAS/intent-clause.schema.json` | `CURRENT_MACHINE_CONTRACT` | A clause can remain `intent.pending` with no `command_id`; this is the existing machine-compatible pre-command state. |
| `DEV/TESTS/test_step3_command_intent_contract.py` | `CURRENT_TEST_CONSUMER` | Verifies clause->command linkage and partial/non-transactional IntentPlan completion. |
| `DEV/TESTS/test_step3_resume_ordering_contract.py` | `CURRENT_TEST_CONSUMER` | Verifies native Choice/Reaction/Continuation ownership plus fixed RNG/committed segments across resume. |

Independent conclusion: a collaboration-held dependent `ACTIONABLE_INTENT` must remain a pending original clause with no accepted RuntimeCommand until release; collaboration cannot synthesize a new multi-Interaction command identity.

### 2.3 Shared-source/currentness and publication

| Source | Role | Step-6 use |
|---|---|---|
| WP-16 final canonical spec | `CANONICAL_OWNER` | Current principal/PLAYER/control and campaign/LIVE currentness remain separate; LIVE source movement cannot transfer voluntary agency. |
| `GAME/CORE/LIVE_SCENE.md` | `CURRENT_RUNTIME_CONSUMER / DEBT` | Confirms no background polling and no distributed multi-branch transaction; current shipped one-file/scene-centric wording is subordinate to WP-16. |
| `GAME/CORE/PERSISTENCE.md` | `CURRENT_RUNTIME_CONSUMER` | Campaign publication freezes one transaction snapshot; ref conflicts rebuild/revalidate; technical commit order is transport, not semantic order. |
| WP-13 canonical spec | `CANONICAL_OWNER` | Independent native successes remain real; no rollback/distributed transaction; current authorization/currentness revalidated. |

Independent conclusion: collaboration terminalization cannot be made atomically dependent on completion of another native execution domain. Handoff/discharge evidence must survive partial publication without replay.

### 2.4 Recipient-safe catch-up

| Source | Role | Step-6 use |
|---|---|---|
| Step-4 final spec | `CANONICAL_OWNER` | Truth, fictional subject knowledge and human-player disclosure are distinct. |
| R2.3 Context Runtime final spec | `CANONICAL_OWNER` | Recipient/task eligibility precedes semantic use; bounded required packet; no raw context inheritance/global scan. |
| Step-5.11 final spec | `CANONICAL_OWNER` | `runtime.message` exactness/prose retention is selective; semantic consumers must be content-sufficient. |
| Step-5.12 final spec | `CANONICAL_OWNER` | Recipient disclosure is scoped; message/delivery does not own gameplay obligation. |
| `GAME/CORE/INFORMATION.md` | `CURRENT_RUNTIME_CONSUMER` | Separates truth, character belief/knowledge and what a player was told. |

Independent conclusion: an obligation's knowledge of another participant's accepted input does not itself grant the returning recipient eligibility to see that input's semantic content.

### 2.5 Identity/class boundary

| Source | Role | Step-6 use |
|---|---|---|
| `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md` | `CANONICAL_OWNER` | `value.contribution` is deterministic Rule-Element calculation input. |
| `DEV/CATALOG/core-catalog.json` | `CURRENT_MACHINE_CONTRACT` | Registers existing `value.contribution` and `runtime.collaboration_obligation` separately. |
| `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md` | `CANONICAL_OWNER` | Stable IDs cannot be silently repurposed; runtime owners require independent lifecycle/addressability; forward refs preferred and derived backlinks require concrete need. |

Independent conclusion: SR17-01 remains closed; Step 6 found no reason to alter the selected Interaction/IntentClause identity direction.

---

## 3. Negative findings from independent routes

Step 6 found no evidence that requires:

- a generic collaboration queue/registry/scheduler;
- a global active-player owner;
- a campaign-global collaboration frontier;
- timeout/presence/heartbeat correctness;
- a new independent human-input record;
- reuse of `value.contribution`;
- a collaboration-owned fictional chronology;
- a campaign+LIVE distributed transaction;
- WP-18 planning to participate in collaboration currentness or player catch-up.

Step 6 also found no contradiction requiring R2.5, Step 3, Step 4, Step 5.11/5.12, WP-11, WP-13, WP-14, WP-15 or WP-16 reopening.

---

## 4. Machine gaps confirmed by independent reconstruction

Current machine/runtime realization still lacks:

1. exact `runtime.collaboration_obligation` schema;
2. collaboration-relevant IntentClause semantic class/content fields;
3. a correctness-complete bounded forward route from current required PLAYER to current relevant obligation IDs;
4. exact obligation lineage/generation fields;
5. accepted closed-generation handoff/discharge linkage into native execution;
6. recipient-safe obligation catch-up projection contract;
7. dedicated WP-17 executable test coverage.

Only items 3–6 are candidate-completeness findings for Step 6. Items 1–2/7 are expected downstream realization debt already acknowledged by the candidate.

---

## 5. Step-6 graph gate

```text
INDEPENDENT_FROM_STEP2_REVIEW_UNIVERSE:      YES
PROJECT_MAP_RECONSTRUCTION_USED:             YES
CATALOG_ADMISSION_ROUTE_INSPECTED:           YES
RECOVERY_DISCOVERY_ROUTE_INSPECTED:          YES
PLAYER_ROUTING_SURFACES_INSPECTED:           YES
STEP3_COMMAND_HANDOFF_INSPECTED:             YES
RESUME_RNG_IDEMPOTENCY_INSPECTED:            YES
LIVE_PUBLICATION_COMPOSITION_INSPECTED:      YES
RECIPIENT_INFORMATION_ROUTE_INSPECTED:       YES
VALUE_CONTRIBUTION_COLLISION_RECHECKED:      YES
WP18_BOUNDARY_RECHECKED:                     YES
SOURCE_MANIFEST_CLOSED_WORLD:                NO
UPSTREAM_REOPEN_REQUIRED:                    NO
HUMAN_DECISION_REQUIRED:                     NO
```
