# RD-02 — Information / Knowledge / Disclosure / Message — Executable Implementation Plan

> For implementation workers: execute task-by-task under the current HDM execution process and Superpowers TDD workflow. No production implementation begins before independent Senior plan GO.

Goal: realize distinct v1 owner-native lore-fact, fictional knowledge, human disclosure and retained-message contracts, plus the positive evidence-normalization path that feeds those owners without creating a parallel epistemic/history authority.

RD unit: `RD-02`
Direct readiness: `R007,R008,R009,R017,R049,R052`.
Composite slices/parents: `R006.INFO,R016.INFO,R018.INFO,R053.INFO,R062.KNOWLEDGE,R062.DISCLOSURE,R062.RETAINED_MESSAGE`.
Canonical owners: Step-4 truth/knowledge/disclosure/history, host delivery boundary, WP-10, WP-11, exact Step-2 records.
Dependencies/joins: RD-04 supplies route/HOT mechanics after owner shapes; RD-09 supplies LIVE source/currentness evidence; RD-13 accepts native SemanticEvent/history drafts; RD-03/14 may supply bounded embedded-epistemic input at their accepted ingestion boundaries. No authority transfer.
Out of scope: HOT implementation, LIVE lifecycle ownership, Story authority, generic memory/state service, historical migration execution.

## Implementation Impact Envelope

SPEC / APPROVED DESIGN: Step-4 §§4–7, 12.2, 24.2; WP-10/11; exact readiness records.
BASELINE REF: fresh branch HEAD at execution.

EXPECTED OWNERS TO CHANGE:
- native information contracts;
- information-normalization runtime capability owned by the information boundary;
- active legacy GAME epistemic projections.

EXPECTED CONSUMERS TO CHANGE:
- RD-09 LIVE handoff/compaction adapter;
- RD-03 Actor epistemic transition consumer;
- RD-13 native SemanticEvent/history consumer;
- RD-14/bootstrap ingestion only where accepted embedded epistemic input exists.

ALLOWED INTERFACES / CONTRACTS TO CHANGE:
- Create `GAME/TOOLS/information.py`;
- create four owner schemas plus `DEV/SCHEMAS/information-normalization-result.schema.json`;
- replace/modify exact GAME schemas/projections named below;
- tests/audit/project-map projections.

PROTECTED INVARIANTS:
- `world.lore_fact`, `world.knowledge`, `runtime.disclosure`, retained Message and SemanticEvent/history remain distinct owners;
- disclosure never implies fictional knowledge;
- transcript/message exposure never implies objective truth;
- PC voluntary belief/suspicion/rejection is not silently chosen;
- normalization is deterministic validation/routing, not generic memory or truth inference;
- LIVE/legacy embedded evidence ceases to be parallel current authority after accepted normalization;
- recipient isolation is mandatory.

Version Impact: classify actual schema/API changes task-by-task. No historical campaign migration is activated by this plan.

## Shared-file coordination

`GAME/SCHEMA/location.schema.yaml` is shared with RD-04 R015. RD-04 removes only reverse `present_entity_ids`; RD-02 then removes epistemic `known_fact_ids` / `secret_ids` against the fresh file. This is a shared-file checkpoint order, not semantic serialization.

`GAME/SCHEMA/pc.schema.yaml`, `npc.schema.yaml`, `item.schema.yaml` are later retired by RD-03. RD-02 first removes forbidden epistemic authority so no intermediate accepted checkpoint preserves a parallel knowledge/Secret owner.

## Task 1 — RED: owner separation, normalization and contamination

**Files**
- Create: `DEV/TESTS/test_rd02_information_native_contracts.py`
- Inspect: the six named legacy GAME schemas and `GAME/CORE/INFORMATION.md`.

**Required interfaces to be absent at RED**
```text
normalize_information_evidence(evidence, source_basis, recipient_scope) -> InformationNormalizationResult
normalize_live_material_evidence(live_evidence, source_basis, recipient_scope) -> InformationNormalizationResult
normalize_embedded_epistemic_input(source_record, source_basis) -> InformationNormalizationResult
validate_knowledge_transition(candidate, current_relation, eligible_sources) -> KnowledgeTransitionResult
```

**RED groups**
- `NativeInformationSchemaTests`: required owner-native schemas absent and cross-owner identity substitution rejected;
- `InformationNormalizationTests`: positive claim/evidence -> typed owner mutation route absent;
- `LegacyInformationProjectionTests`: active embedded `secret_ids` / knowledge aliases remain;
- `RecipientIsolationTests`: no callable path yet proves player/subject separation.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts.NativeInformationSchemaTests -v
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts.InformationNormalizationTests -v
```
Expected RED for missing native contracts/normalizer. Do not publish RED-only checkpoint.

## Task 2 — GREEN: native owner machine contracts

**Files**
- Create: `DEV/SCHEMAS/world-lore-fact-state.schema.json`
- Create: `DEV/SCHEMAS/world-knowledge-state.schema.json`
- Create: `DEV/SCHEMAS/runtime-disclosure-state.schema.json`
- Create: `DEV/SCHEMAS/runtime-message-state.schema.json`
- Create: `DEV/SCHEMAS/information-normalization-result.schema.json`
- Modify: `DEV/TESTS/test_rd02_information_native_contracts.py`

**Normalization result contract**
```text
InformationNormalizationResult {
  lore_fact_candidates: tuple[LoreFactCandidate, ...]
  knowledge_transitions: tuple[KnowledgeTransitionCandidate, ...]
  disclosure_transitions: tuple[DisclosureTransitionCandidate, ...]
  semantic_event_drafts: tuple[SemanticEventDraft, ...]
  rejected_inputs: tuple[RejectedInformationEvidence, ...]
}
```
This object is ephemeral typed output. It is not a durable owner, transaction log or generic mutation bus.

GREEN schema requirements: complete native identities; knowledge key `(knower_id,fact_id)`; disclosure key `(player_id,fact_id)`; objective fact vs fictional stance vs human exposure vs retained communication remain structurally distinct; Message stays evidence, not ACL/knowledge/canon.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts.NativeInformationSchemaTests -v
```
Expected GREEN. Legacy and runtime-normalization test groups may remain RED until their own task, so the coherent checkpoint includes only the schema test group and must not claim whole-file suite green.

REFACTOR: follow existing DEV schema idioms; no generic state envelope.

Coherent checkpoint: five DEV contracts + schema-only focused test group. Published checkpoint is explicitly `RD02-TASK2`, not RD-02 completion.

## Task 3 — GREEN: deterministic information normalizer

**Files**
- Create: `GAME/TOOLS/information.py`
- Modify: `DEV/TESTS/test_rd02_information_native_contracts.py`
- Modify: `DEV/PROJECT_MAP.md`
- Modify: `DEV/TOOLS/audit_engine.py`

**Interfaces**
```text
normalize_information_evidence(evidence, source_basis, recipient_scope) -> InformationNormalizationResult
normalize_live_material_evidence(live_evidence, source_basis, recipient_scope) -> InformationNormalizationResult
normalize_embedded_epistemic_input(source_record, source_basis) -> InformationNormalizationResult
validate_knowledge_transition(candidate, current_relation, eligible_sources) -> KnowledgeTransitionResult
```

**Rules**
- evidence type and source basis determine which owner candidates are legal; the normalizer never infers truth merely from message/transcript/LIVE presence;
- objective proposition identity is created/reused only when Step-4 promotion threshold is met;
- knowledge transition is subject-local and validates eligible source refs;
- disclosure transition is player-local and records only delivered/exposed aspect actually supported by host evidence;
- SemanticEvent draft is causal/history evidence only and is handed to RD-13 native history owner;
- PC `believed/suspected/rejected` requires explicit player-authored or admitted cognition-constraining evidence;
- embedded legacy epistemic arrays are accepted only as bounded ingestion/migration input and cease to be writable authority after normalized output; no historical migration is executed here;
- output contains typed candidates, not commits; owner-specific commit APIs perform authoritative mutation.

**RED/GREEN cases**
- same claim disclosed to Player A creates no Player B disclosure and no automatic PC knowledge;
- NPC claim may produce `aware/believed` candidate only when eligible subject evidence supports it;
- objective-status disclosure requires exact truth transition ref;
- transcript/LIVE statement without truth evidence cannot create `truth.established`;
- embedded `known/belief/suspicion` input normalizes to subject relations without retaining writable arrays;
- rejected/ineligible evidence produces typed rejection and zero owner mutation candidates.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts.InformationNormalizationTests -v
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts.RecipientIsolationTests -v
```
Expected GREEN.

REFACTOR: owner-specific candidate builders may be private functions in `information.py`; do not split into generic mutation/event services.

Coherent checkpoint: normalizer + result schema integration + positive/negative normalization tests + audit/project-map projection.

## Task 4 — replace legacy GAME epistemic representation

**Files**
- Replace: `GAME/SCHEMA/lore.schema.yaml`
- Modify: `GAME/SCHEMA/pc.schema.yaml`
- Modify: `GAME/SCHEMA/npc.schema.yaml`
- Modify: `GAME/SCHEMA/faction.schema.yaml`
- Modify: `GAME/SCHEMA/location.schema.yaml` after RD-04 shared-file checkpoint
- Modify: `GAME/SCHEMA/item.schema.yaml`
- Modify: `GAME/SCHEMA/README.md`
- Modify conditionally only on test-proven contradiction: `GAME/CORE/INFORMATION.md`; otherwise inspect-only
- Modify: `GAME/TEMPLATE/STORAGE_README.md`
- Modify: `DEV/PROJECT_MAP.md`
- Modify: `DEV/TOOLS/audit_engine.py`
- Modify: `DEV/TESTS/test_rd02_information_native_contracts.py`

**RED**: enumerate every current legacy epistemic field in these six exact schemas and stale direct projections.

**GREEN**
- remove parallel writable epistemic/Secret authority, not alias it;
- `lore.schema.yaml` projects `world.lore_fact`, not combined truth/knowledge/dispute lifecycle;
- Location cleanup preserves RD-04 removal of `present_entity_ids`;
- no absent `world_state.schema.yaml` is resurrected.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts.LegacyInformationProjectionTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```
Expected GREEN.

Coherent checkpoint: all six coordinated GAME schema/projection edits + focused test/audit. This checkpoint must not knowingly leave one of those active schemas as a parallel epistemic authority.

## Task 5 — install the LIVE normalization consumer (`R053.INFO` / `R053.LIVE` join)

**Files**
- Modify: `GAME/TOOLS/information.py`
- Modify in RD-09 checkpoint: `GAME/TOOLS/live_state.py`
- Modify: `DEV/TESTS/test_rd02_information_native_contracts.py`
- Modify in RD-09 suite: `DEV/TESTS/test_rd09_access_live.py`
- Inspect/consume: RD-13 native SemanticEvent/history interface once published.

**Producer/consumer contract**
```text
RD-09 close/absorb/handoff
  -> extract typed material LIVE evidence at one exact selected source revision
  -> RD-02 normalize_live_material_evidence(...)
  -> owner-specific Lore/Knowledge/Disclosure candidates
  -> RD-13 SemanticEventDraft candidate where material history is required
  -> native owner validation/commit through ordinary owner transaction/durability routes
  -> only after accepted handoff may legacy LIVE epistemic arrays cease to participate as current source evidence
```

RD-09 owns LIVE lifecycle/currentness and source extraction. RD-02 owns information normalization semantics. RD-13 owns native SemanticEvent/history. RD-04 owns route/HOT mechanics. No participant can substitute for another.

**Integration cases**
- live-observed material knowledge becomes one native `world.knowledge` relation with source basis and no surviving second global LIVE relation after handoff;
- human disclosure normalizes to exact player only;
- material event history is handed to native history owner, not Story;
- close/absorb is blocked/retryable when required normalization candidate cannot be validated/committed;
- non-material/ephemeral LIVE evidence need not create durable relation;
- current source movement invalidates the extraction basis; no mixed-revision normalization.

Run after RD-09 consumer exists:
```bash
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts.InformationNormalizationTests -v
python3 -m unittest DEV.TESTS.test_rd09_access_live.LiveInformationNormalizationIntegrationTests -v
```
Expected GREEN before R053 parent can close.

Coherent checkpoint: cross-RD integration commit contains the smallest compatible RD-02/RD-09 consumer wiring + tests; it does not move LIVE or history authority.

## Task 6 — embedded-epistemic ingestion consumers

RD-03 Actor materialization and RD-14 bootstrap may encounter admitted embedded legacy/input epistemic state. They consume `normalize_embedded_epistemic_input(...)` before accepting native v1 state and must prove the source arrays are not retained as writable authority.

No migration scan/job is created. If execution currentness shows no admitted input path can still carry these fields, record the consumer as `NOT_APPLICABLE_CURRENT_V1` with evidence rather than inventing a compatibility path.

Focused acceptance is owned by the consuming RD tests and referenced from the package proof ledger.

## Task 7 — RD-02 closure / composite evidence

**Files**
- Modify: `DEV/TESTS/test_rd02_information_native_contracts.py`
- Modify: `DEV/TOOLS/audit_engine.py`
- Inspect active `GAME/**`/`DEV/**` only through bounded stale queries; arbitrary matches do not grant write authority.

Required evidence:
- R006/R016/R018 information slices have native schema + positive consumer routes;
- R053.INFO/LIVE integration test is GREEN;
- `R062.KNOWLEDGE`, `.DISCLOSURE`, `.RETAINED_MESSAGE` map to exact owner contracts/tests;
- no active embedded writable knowledge/Secret/disclosure shortcut remains;
- downstream context/history/routing joins are named without authority transfer.

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected PASS for all currently realized deterministic/scenario obligations.

Version Impact Gate: classify new/changed schema/API generations and synchronize required projections. System Impact Gate stops if implementation requires a new information/history/transaction owner or broader compatibility/migration policy.

Final coherent checkpoint: native schemas + normalizer + active legacy retirement + installed consumers + focused/integration proof. Pure proof/package parent closure remains in the package proof ledger, not pre-claimed here.