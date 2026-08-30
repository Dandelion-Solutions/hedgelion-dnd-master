# Step 3 Execution Boundary Machine Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Materialize the canonical Step-3 execution architecture as machine-readable catalogs/schemas and focused TDD contracts without inventing a production Python execution engine that does not yet exist in this repository.

**Architecture:** Preserve the approved Alternative-C ownership split. Step-3 runtime records receive dedicated JSON Schemas; `ExecutionSegment`, invocation facts, clauses, receipts and pending-child descriptors remain embedded/protocol schemas rather than new runtime classes. `core-catalog.json` gains only the closed protocol vocabulary required by the canonical spec, while Step-2 world schemas are changed only where Step 3 now supplies compact causal evidence such as Effect application recency.

**Tech Stack:** JSON Schema Draft 2020-12, JSON machine catalogs, Python 3.13 `unittest`, `jsonschema`, existing `DEV/TOOLS/audit_engine.py`, GitHub Actions `Validate engine source`.

**Spec:** `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`

## Global Constraints

- Alternative C is canonical; do not collapse IntentPlan, RuntimeCommand, Resolution, Procedure or TransitionRequest into one workflow object.
- Do not add `runtime.execution_segment`, `runtime.resolution_chain`, scheduler/job/obligation classes, or a general workflow DSL.
- `runtime.procedure` is the sole live owner of procedure-local ResourceState.
- RuntimeCommand is the root mandatory execution-chain closure owner; Resolution owns one Activity invocation only.
- MechanicalEvent exists only for committed segments and does not replace current world state.
- Invocation-adjudicated facts are closed registered boolean inputs; missing is distinct from false; engine-owned facts are forbidden through this channel.
- No SQLite transaction may span an external choice/reaction boundary.
- Retry identities must resolve stored accepted context before ambient rebinding.
- Mandatory post-commit child obligation identity must be representable atomically with the triggering committed segment/Event.
- Effect recency uses an immutable target/application-family-local nonterminal episode ordinal, not wall-clock time, Effect ID order or retained trace order.
- Temporal Agenda remains derived; same-coordinate advancement cannot pass unresolved mandatory due work.
- Full transcript retention/publication and spectator projection are Step 4/5 work and must not be introduced by this implementation.
- A new closed catalog ID requires a coherent catalog-version bump across all machine catalogs.

---

### Task 1: Register Step-3 protocol vocabulary and bump the coherent catalog version

**Files:**
- Modify: `DEV/CATALOG/core-catalog.json`
- Modify: `DEV/SCHEMAS/core-catalog.schema.json`
- Modify: `DEV/CATALOG/entity-structures.json` — version only in this task
- Modify: `DEV/CATALOG/mechanical-surfaces.json` — version only in this task
- Modify: `DEV/CATALOG/identifier-policies.json` — version only in this task
- Test: `DEV/TESTS/test_step3_execution_catalog_contract.py`

**Interfaces:**
- Consumes: existing `catalog_version = 1.3.0`, runtime kind `runtime.procedure`, existing resolution/intent states.
- Produces: `catalog_version = 1.4.0`; closed registries `command_dispositions`, `execution_failure_codes`; protocol kinds for embedded Step-3 values.

- [ ] **Step 1: Write the failing catalog test**

Create `DEV/TESTS/test_step3_execution_catalog_contract.py` with checks equivalent to:

```python
import json
from pathlib import Path
import unittest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "DEV" / "CATALOG"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class Step3ExecutionCatalogContractTest(unittest.TestCase):
    def setUp(self):
        self.core = load_json(CATALOG / "core-catalog.json")
        self.schema = load_json(SCHEMAS / "core-catalog.schema.json")

    def test_step3_closed_vocabulary_is_registered(self):
        r = self.core["registries"]
        self.assertEqual(r["command_dispositions"], ["command.accepted", "command.settled"])
        required_failures = {
            "failure.idempotency_conflict",
            "failure.hydration_required",
            "failure.missing_reference",
            "failure.catalog_context_incompatible",
            "failure.continuation_conflict",
            "failure.continuation_stale",
            "failure.dependency_cycle",
            "failure.transition_requires_procedure",
            "failure.order_adjudication_required",
            "failure.execution_limit",
            "failure.invocation_fact_missing",
            "failure.invocation_fact_unauthorized",
        }
        self.assertTrue(required_failures <= set(r["execution_failure_codes"]))
        for kind in (
            "value.execution_segment", "value.pending_child_invocation",
            "value.invocation_fact", "value.boundary_occurrence",
        ):
            self.assertIn(kind, r["protocol_value_kinds"])

    def test_catalogs_move_as_one_version(self):
        versions = {
            load_json(CATALOG / name)["catalog_version"]
            for name in (
                "core-catalog.json", "entity-structures.json",
                "mechanical-surfaces.json", "identifier-policies.json",
            )
        }
        self.assertEqual(versions, {"1.4.0"})

    def test_core_catalog_schema_accepts_updated_catalog(self):
        Draft202012Validator(self.schema).validate(self.core)
```

- [ ] **Step 2: Run the focused test and confirm RED**

Run:

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_execution_catalog_contract -v
```

Expected: FAIL because the Step-3 registries/protocol kinds do not exist and catalogs still declare `1.3.0`.

- [ ] **Step 3: Add the minimal closed vocabulary**

In `core-catalog.json`, add exactly these registries:

```json
"command_dispositions": ["command.accepted", "command.settled"],
"execution_failure_codes": [
  "failure.idempotency_conflict",
  "failure.hydration_required",
  "failure.missing_reference",
  "failure.catalog_context_incompatible",
  "failure.continuation_conflict",
  "failure.continuation_stale",
  "failure.dependency_cycle",
  "failure.transition_requires_procedure",
  "failure.order_adjudication_required",
  "failure.execution_limit",
  "failure.invocation_fact_missing",
  "failure.invocation_fact_unauthorized"
]
```

Append protocol kinds:

```text
value.execution_segment
value.pending_child_invocation
value.invocation_fact
value.boundary_occurrence
```

Teach `core-catalog.schema.json` to require/validate the two new registries with the existing `idRegistry` definition. Change all four machine catalog `catalog_version` values to `1.4.0`; do not change identifier policies or unrelated catalog contents.

- [ ] **Step 4: Run the focused test and full maintenance audit**

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_execution_catalog_contract -v
DEV/TOOLS/run_maintenance_audit
```

Expected: both PASS.

- [ ] **Step 5: Commit**

```bash
git add DEV/CATALOG DEV/SCHEMAS/core-catalog.schema.json DEV/TESTS/test_step3_execution_catalog_contract.py
git commit -m "feat: register step 3 execution protocol vocabulary"
```

---

### Task 2: Add shared embedded Step-3 value schemas

**Files:**
- Create: `DEV/SCHEMAS/invocation-fact.schema.json`
- Create: `DEV/SCHEMAS/intent-clause.schema.json`
- Create: `DEV/SCHEMAS/boundary-occurrence.schema.json`
- Create: `DEV/SCHEMAS/pending-child-invocation.schema.json`
- Create: `DEV/SCHEMAS/execution-segment.schema.json`
- Create: `DEV/SCHEMAS/resolution-receipt.schema.json`
- Test: `DEV/TESTS/test_step3_execution_value_schemas.py`

**Interfaces:**
- Consumes: registered machine IDs, `command.*` dispositions and `failure.*` codes from Task 1.
- Produces: reusable closed schemas referenced by RuntimeCommand, IntentPlan, Resolution, Continuation and MechanicalEvent schemas.

- [ ] **Step 1: Write failing schema tests**

The test must construct a local `referencing.Registry` for all `DEV/SCHEMAS/*.json` exactly as `audit_engine.py` does and assert:

```python
valid_fact = {
    "fact_id": "fiction.target_visible",
    "value": False,
    "provenance_class": "INVOCATION_ADJUDICATED",
    "provenance_ref": "interaction-000001:fact:1",
}

valid_clause = {
    "clause_id": "clause-01",
    "order": 1,
    "mapping_outcome": "exact",
    "execution_state": "intent.ready",
}

valid_segment = {
    "segment_sequence": 1,
    "commit_state": "committed",
    "event_ids": ["event-00000001"],
}
```

Also assert rejection of:

- invocation fact without explicit `value`;
- `value: null` for invocation fact;
- clause guard with two prior-clause references or arbitrary expression key;
- execution segment that embeds arbitrary world-state documents;
- pending child descriptor without `firing_key`, `root_command_id`, `activity_id` and triggering occurrence reference.

- [ ] **Step 2: Run and confirm RED because schemas are absent**

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_execution_value_schemas -v
```

Expected: ERROR/FAIL on missing schema files.

- [ ] **Step 3: Implement the six closed schemas**

Use Draft 2020-12, `additionalProperties: false`, stable machine-ID patterns, and these minimum shapes:

```text
invocation-fact
  fact_id
  value: boolean
  provenance_class = INVOCATION_ADJUDICATED
  provenance_ref: non-empty stable string

intent-clause
  clause_id
  order >= 1
  mapping_outcome
  execution_state
  optional guard:
      prior_clause_id
      source = status | export
      optional export_id
      operator = eq | in
      literal scalar OR literal_values[]

boundary-occurrence
  boundary_id
  producer_id
  scope_subject_id
  occurrence_key
  causal_position

pending-child-invocation
  firing_key
  root_command_id
  activity_id
  trigger_ref
  optional procedure_id
  optional child_resolution_id
  reason = mandatory_followup | execution_limit

execution-segment
  segment_sequence >= 1
  commit_state = committed
  event_ids[]
  pending_child_invocations[]
  receipt_exports object of scalar typed outputs
  affected_revision_refs[]
  optional continuation_id

resolution-receipt
  execution_owner_id
  segment_refs[]
  status
  event_ids[]
  exports object
  pending_child_refs[]
  optional failure_code
```

Do not put mutable Procedure ResourceState or full world records into `execution-segment.schema.json` or receipt schemas.

- [ ] **Step 4: Run focused tests and maintenance audit**

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_execution_value_schemas -v
DEV/TOOLS/run_maintenance_audit
```

Expected: PASS; maintenance audit validates examples from the new schemas.

- [ ] **Step 5: Commit**

```bash
git add DEV/SCHEMAS DEV/TESTS/test_step3_execution_value_schemas.py
git commit -m "feat: define step 3 execution value schemas"
```

---

### Task 3: Define IntentPlan and RuntimeCommand machine contracts

**Files:**
- Create: `DEV/SCHEMAS/runtime-intent-plan-state.schema.json`
- Create: `DEV/SCHEMAS/runtime-command-state.schema.json`
- Test: `DEV/TESTS/test_step3_command_intent_contract.py`

**Interfaces:**
- Consumes: `intent-clause.schema.json`, `invocation-fact.schema.json`, `execution-segment.schema.json`, command disposition registry.
- Produces: machine-enforced non-atomic IntentPlan orchestration and root-command closure/idempotency shape.

- [ ] **Step 1: Write RED tests for ownership boundaries**

Tests must validate an IntentPlan containing three clauses where earlier clauses can be `intent.executed` while a later clause is `intent.failed`, and reject any plan-level fields named `world_delta`, `rng_state`, `procedure_resources`, or `transaction_state`.

For RuntimeCommand, validate a representative action command:

```python
{
  "interaction_id": "turn-000042",
  "intent_plan_id": "turn-000042-plan",
  "clause_id": "clause-01",
  "command_kind": "action",
  "catalog_context_fingerprint": "sha256:catalog-context-A",
  "input_fingerprint": "sha256:command-input-A",
  "disposition": "command.accepted",
  "invocation_facts": [],
  "root_resolution_id": "resolution-0000001",
  "pending_child_invocations": []
}
```

Reject:

- `command.settled` with non-empty `pending_child_invocations`;
- action command with direct-transition payload and no Resolution linkage;
- transition command that stores Resolution cursor/reaction state;
- unknown `command_kind`;
- LLM narration text inside `input_fingerprint` source fields.

- [ ] **Step 2: Run focused tests to confirm RED**

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_command_intent_contract -v
```

Expected: missing schema failure.

- [ ] **Step 3: Implement the two schemas**

`runtime-intent-plan-state.schema.json` requires `interaction_id` and non-empty `clauses`; clauses reference `intent-clause.schema.json`. It has no mechanical transaction/RNG/world-delta fields.

`runtime-command-state.schema.json` requires common IDs, `command_kind`, opaque `catalog_context_fingerprint`, `input_fingerprint`, `disposition`, and invocation fact array. Use conditional schemas:

```text
action
  requires root_resolution_id
  forbids transition_request

transition
  requires transition_request
  forbids root_resolution_id unless later mandatory child work creates child refs outside the direct root

command.settled
  requires pending_child_invocations absent or empty
```

Store pending mandatory work by reference/descriptor, not as a generic job list.

- [ ] **Step 4: GREEN and regression**

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_command_intent_contract -v
.hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add DEV/SCHEMAS/runtime-intent-plan-state.schema.json DEV/SCHEMAS/runtime-command-state.schema.json DEV/TESTS/test_step3_command_intent_contract.py
git commit -m "feat: define intent plan and root command contracts"
```

---

### Task 4: Define Procedure, Resolution and Continuation ownership schemas

**Files:**
- Create: `DEV/SCHEMAS/runtime-procedure-state.schema.json`
- Create: `DEV/SCHEMAS/runtime-resolution-state.schema.json`
- Create: `DEV/SCHEMAS/runtime-continuation-state.schema.json`
- Test: `DEV/TESTS/test_step3_execution_owner_contract.py`

**Interfaces:**
- Consumes: Resource spent-model semantics from `resource-definition-data.schema.json`; invocation facts; pending-child/receipt schemas.
- Produces: one portable Procedure owner and nonduplicating Resolution/Continuation schemas.

- [ ] **Step 1: Write failing ownership tests**

Validate a Procedure state with participant resources keyed by participant then Resource definition, storing only accepted spent-model state:

```python
{
  "participant_resources": {
    "actor-0001": {
      "resource.action": {"spent": 1},
      "resource.reaction": {"spent": 0}
    }
  }
}
```

Validate a Resolution referencing `procedure_id` and `root_command_id`, and a Continuation referencing the same Procedure but containing no `participant_resources`.

Reject:

- Procedure resource with stored `capacity`;
- Resolution or Continuation containing `procedure_resources` / `resource_state_copy`;
- Continuation containing `mechanical_context`, `temporal_agenda`, `prospective_deltas`, or `condition_index`;
- child Resolution without `root_command_id` or stable `causal_invocation_key` when `initiating_command_id` is absent;
- Continuation generation below 1.

- [ ] **Step 2: Run and confirm RED**

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_execution_owner_contract -v
```

- [ ] **Step 3: Implement minimal owner schemas**

`runtime-procedure-state.schema.json` owns only procedure-local operational state needed now: participant spent-model ResourceState plus optional world-context reference and explicit lifecycle/boundary metadata only where represented by registered IDs.

`runtime-resolution-state.schema.json` owns Activity invocation identity, root command, optional initiating command, optional Procedure, status, cursor/safe phase, fixed RNG array, prior exports, child refs, segment sequence, Continuation ref, trace ref and causal invocation key.

`runtime-continuation-state.schema.json` owns generation, Resolution/root command/catalog-context/Procedure refs, safe recompute cursor, accepted invocation facts, fixed RNG, prior exports, receipt refs, dependency frontier refs, pending choice/reaction descriptor, expected child refs, future RNG frontier and optional unconsumed advancement remainder.

Do not serialize copied Procedure state or derived caches.

- [ ] **Step 4: GREEN + full test suite**

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_execution_owner_contract -v
.hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -v
```

- [ ] **Step 5: Commit**

```bash
git add DEV/SCHEMAS/runtime-procedure-state.schema.json DEV/SCHEMAS/runtime-resolution-state.schema.json DEV/SCHEMAS/runtime-continuation-state.schema.json DEV/TESTS/test_step3_execution_owner_contract.py
git commit -m "feat: define step 3 execution owners"
```

---

### Task 5: Define committed MechanicalEvent identity and mandatory follow-up atomicity

**Files:**
- Create: `DEV/SCHEMAS/runtime-mechanical-event-state.schema.json`
- Test: `DEV/TESTS/test_step3_event_followup_contract.py`

**Interfaces:**
- Consumes: `execution-segment.schema.json`, `pending-child-invocation.schema.json`, Event kinds from core catalog.
- Produces: segment+ordinal Event identity fields and a machine-verifiable representation where mandatory selected follow-ups are part of the committed segment contract.

- [ ] **Step 1: Write RED tests**

Validate:

```python
{
  "segment_id": "resolution-0000001:segment:1",
  "event_ordinal": 1,
  "event_kind": "event.damage.applied",
  "root_command_id": "turn-000042-cmd-01",
  "causal_ref": "resolution-0000001",
  "payload": {"amount": 7, "target_id": "actor-0002"}
}
```

Assert that two Events may have identical payloads but require distinct `(segment_id, event_ordinal)` pairs.

Build a committed segment example containing both the damage `event_id` and a mandatory `pending_child_invocation` for a concentration-like post-damage save. Assert the schema accepts the atomic representation and rejects pending child descriptors without a triggering Event/occurrence reference.

- [ ] **Step 2: Run and confirm RED**

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_event_followup_contract -v
```

- [ ] **Step 3: Implement the MechanicalEvent schema and tighten shared value schemas**

Require `segment_id`, positive `event_ordinal`, registered-shaped `event_kind`, `root_command_id`, `causal_ref`, and compact typed payload object. Do not add current-state snapshots.

Update `execution-segment.schema.json` / `pending-child-invocation.schema.json` only as needed to require stable trigger/occurrence linkage for mandatory follow-up descriptors.

- [ ] **Step 4: GREEN and audit**

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_event_followup_contract -v
DEV/TOOLS/run_maintenance_audit
```

- [ ] **Step 5: Commit**

```bash
git add DEV/SCHEMAS/runtime-mechanical-event-state.schema.json DEV/SCHEMAS/execution-segment.schema.json DEV/SCHEMAS/pending-child-invocation.schema.json DEV/TESTS/test_step3_event_followup_contract.py
git commit -m "feat: bind committed events to mandatory followups"
```

---

### Task 6: Materialize Effect application recency without trace-history authority

**Files:**
- Modify: `DEV/SCHEMAS/world-effect-state.schema.json`
- Modify: `DEV/CATALOG/entity-structures.json`
- Test: `DEV/TESTS/test_step3_effect_recency_contract.py`

**Interfaces:**
- Consumes: Step-2 Effect application/arbitration contract.
- Produces: immutable positive `application_order_key` field on live Effect state when recency-sensitive arbitration requires it; no global chronology owner.

- [ ] **Step 1: Write RED tests**

Test schema acceptance of:

```python
{
  "target_id": "actor-0042",
  "application_order_key": 2,
  "lifecycle": {"state_id": "effect_lifecycle.active"}
}
```

Reject zero, negative, float, timestamp-shaped string, and an attempted mutable object `{ "counter": 2 }`.

Add a structural test that `entity-structures.json` lists `application_order_key` in `world.effect.expected` and does not add `created_at`, `recency_timestamp`, or `global_order`.

- [ ] **Step 2: Run focused test and confirm RED**

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_effect_recency_contract -v
```

- [ ] **Step 3: Add the minimal field**

In `world-effect-state.schema.json`:

```json
"application_order_key": {"type": "integer", "minimum": 1}
```

Do not make it universally required: only arbitration policies that use recency require runtime to materialize it. Add the field to `world.effect.expected` in `entity-structures.json`.

Do not encode family, target, timestamp or global counter into a second canonical field; family remains derived from accepted provenance.

- [ ] **Step 4: GREEN + Step-2 regression suite**

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_effect_recency_contract -v
.hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -p 'test_step2*.py' -v
```

- [ ] **Step 5: Commit**

```bash
git add DEV/SCHEMAS/world-effect-state.schema.json DEV/CATALOG/entity-structures.json DEV/TESTS/test_step3_effect_recency_contract.py
git commit -m "feat: persist effect application recency evidence"
```

---

### Task 7: Lock reaction resume, same-coordinate suspension and ordering failure contracts

**Files:**
- Modify: `DEV/SCHEMAS/runtime-continuation-state.schema.json`
- Modify: `DEV/SCHEMAS/resolution-receipt.schema.json`
- Create: `DEV/TESTS/test_step3_resume_ordering_contract.py`

**Interfaces:**
- Consumes: Continuation, receipt, failure-code registry.
- Produces: stable response-generation/offer identity, expected-child refs, explicit unconsumed advancement remainder and typed ordering/conflict outcomes.

- [ ] **Step 1: Write RED tests**

Cover these representations:

```text
Reaction suspension
  generation = 2
  pending_response.offer_id
  pending_response.kind = reaction
  expected_child_resolution_ids[]
  safe_recompute_phase

Same-coordinate suspension
  unconsumed_advancement:
      amount > 0
      unit_id
      context_id
```

Reject:

- reaction continuation without generation/offer identity;
- continuation that stores an old `prospective_delta` to resume after child;
- negative unconsumed advancement;
- receipt using an arbitrary ordering result instead of registered success or `failure.order_adjudication_required`.

- [ ] **Step 2: Confirm RED**

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_resume_ordering_contract -v
```

- [ ] **Step 3: Tighten schemas**

Use one closed `pending_response` object with `kind = choice | reaction`, `offer_id`, responder/candidate linkage, and safe recompute phase. Keep expected child IDs as references only.

Use one `unconsumed_advancement` value object with positive integer amount, registered unit and context ID. It records only requested remainder; authoritative local time remains with its accepted temporal owner.

Allow receipts to report registered Step-3 failure codes, including order adjudication, continuation conflict/stale and execution limit.

- [ ] **Step 4: GREEN + full unit suite**

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_resume_ordering_contract -v
.hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -v
```

- [ ] **Step 5: Commit**

```bash
git add DEV/SCHEMAS/runtime-continuation-state.schema.json DEV/SCHEMAS/resolution-receipt.schema.json DEV/TESTS/test_step3_resume_ordering_contract.py
git commit -m "feat: define reaction resume and due-boundary contracts"
```

---

### Task 8: Add integrated structural cases A–N and machine-contract cross-validation

**Files:**
- Create: `DEV/TESTS/test_step3_execution_examples.py`
- Modify: `DEV/TOOLS/audit_engine.py`

**Interfaces:**
- Consumes: every Step-3 schema produced by Tasks 1–7.
- Produces: one integrated assurance suite mirroring canonical cases A–N and maintenance-audit validation for the new machine files.

- [ ] **Step 1: Write integrated tests before changing audit**

Implement one test method per canonical case family:

```text
A ordinary action shape
B reaction suspension/resume shape
C post-commit mandatory follow-up
D partial IntentPlan completion
E direct deterministic transition
F ambiguous/no-command disposition
G exact retry fingerprint stability
H crash/suspended portable closure shape
I boundary multi-responder occurrence identity
J scheduled due child firing key
K reaction child shares Procedure without state copy
L incompatible catalog-context typed failure
M chain-limit pending child preserved
N Effect recency survives trace absence
```

These tests validate representability/invariants only; do not pretend to execute a runtime engine that is not present.

- [ ] **Step 2: Run integrated tests to find missing schema edges**

```bash
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_step3_execution_examples -v
```

Expected: any failure must identify a concrete missing/contradictory schema edge; fix only the narrow contract causing it.

- [ ] **Step 3: Extend maintenance audit cross-validation**

In `audit_json_schemas()`, keep automatic validation of every schema example and add explicit requirements that these Step-3 schema files exist:

```python
for required_schema in (
    "invocation-fact.schema.json",
    "intent-clause.schema.json",
    "runtime-intent-plan-state.schema.json",
    "runtime-command-state.schema.json",
    "runtime-procedure-state.schema.json",
    "runtime-resolution-state.schema.json",
    "runtime-continuation-state.schema.json",
    "execution-segment.schema.json",
    "runtime-mechanical-event-state.schema.json",
    "pending-child-invocation.schema.json",
    "resolution-receipt.schema.json",
    "boundary-occurrence.schema.json",
):
    require(required_schema in schemas, f"missing Step-3 schema: {required_schema}")
```

Also extend catalog cross-validation so the four machine catalog versions are checked together, not only core/entity/identifier.

- [ ] **Step 4: Run all local verification**

```bash
DEV/TOOLS/run_maintenance_audit
.hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -v
```

Expected: both PASS.

- [ ] **Step 5: Commit**

```bash
git add DEV/TESTS/test_step3_execution_examples.py DEV/TOOLS/audit_engine.py DEV/SCHEMAS DEV/CATALOG
git commit -m "test: cover integrated step 3 execution contracts"
```

---

### Task 9: Align architecture status and run the final Step-3 critical pass

**Files:**
- Modify: `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`
- Modify: `DEV/ARCHITECTURE/CATALOG_DESIGN_STATUS.md`
- Create: `DEV/docs/superpowers/design/2026-08-19-step-3-final-critical-review.md`

**Interfaces:**
- Consumes: canonical spec, adversarial review, Tasks 1–8 machine evidence.
- Produces: decision whether Step 3 satisfies its roadmap exit gate and exact continuation point into Step 4 or a bounded Step-3 repair.

- [ ] **Step 1: Perform a fresh critical review against the canonical spec**

Explicitly re-check:

```text
IntentPlan non-atomicity
root RuntimeCommand closure
Procedure sole ownership
Resolution one-Activity meaning
Transition direct path
Segment atomicity representation
Event+mandatory child crash safety
reaction child/recompute frontier
retry/context ordering
RNG fixed inputs
Effect recency without trace dependency
same-coordinate closure
scheduled due firing identity
LLM fact authority
checkpoint portability boundaries
narration/history non-authority
no workflow/scheduler/job class creep
```

The review artifact must classify every finding as BLOCKER / FIXED / LATER-OWNER and cite the exact schema/test evidence.

- [ ] **Step 2: Resolve any bounded mechanical finding immediately**

For a mechanical contradiction implied by the canonical spec, add the smallest failing test, confirm RED, patch the schema/catalog, confirm GREEN, and record the correction in the review. Do not reopen architecture unless a genuine new trade-off appears.

- [ ] **Step 3: Update roadmap/status only from fresh evidence**

If no unresolved Step-3 blocker remains and all verification passes:

```text
Step 3 -> COMPLETE
Step 4 -> IN PROGRESS
```

Set exact continuation to Step 4 lore/chapters/knowledge/secrets/promotion, carrying the transcript → SemanticEvent → Chapter spectator-safe projection requirement into that stage.

If a blocker remains, keep Step 3 IN PROGRESS and name the exact repair instead.

- [ ] **Step 4: Run fresh full verification on the final docs+machine HEAD**

```bash
DEV/TOOLS/run_maintenance_audit
.hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -v
```

Then require GitHub Actions `Validate engine source` on the same final commit to conclude `success` before claiming Step-3 closure.

- [ ] **Step 5: Commit**

```bash
git add DEV/ARCHITECTURE DEV/docs/superpowers/design/2026-08-19-step-3-final-critical-review.md DEV/CATALOG DEV/SCHEMAS DEV/TESTS DEV/TOOLS/audit_engine.py
git commit -m "docs: close step 3 execution architecture"
```

---

## Plan self-review

### Spec coverage

- Interaction/IntentPlan/guard boundary: Tasks 2–3, 8.
- RuntimeCommand root closure/idempotency/catalog context: Tasks 1, 3, 5, 8.
- Procedure sole ownership: Task 4, integrated Case K in Task 8.
- Resolution/child identity: Tasks 4–5.
- Embedded ExecutionSegment and atomic committed bundle: Tasks 2, 5, 8.
- Signal/BoundaryOccurrence/Event separation: Tasks 2, 5, 7–8.
- Continuation/reaction recomputation: Tasks 4, 7–8.
- RNG continuity representability: Tasks 4, 8.
- Mandatory child crash safety/chain limit: Tasks 2, 5, 8.
- Effect family-local recency evidence: Task 6, integrated Case N.
- Same-coordinate/scheduled due continuation: Task 7, integrated Cases I–J.
- LLM invocation facts: Tasks 1–4, integrated Case F.
- Typed failures: Tasks 1, 7–8.
- Catalog migration barrier: Tasks 3–4, integrated Case L.
- Checkpoint source payload boundaries: Task 4 plus integrated Case H; Git publication remains correctly deferred.
- Narrative/history mechanical firewall and spectator carry-forward: canonical spec + Task 9 status transition; no Step-3 runtime persistence invented.

### Placeholder scan

This plan contains no implementation placeholder such as `TBD`, `TODO`, “similar to Task N”, or unspecified “add tests”. Every task names exact files, RED command, minimum contract, GREEN command and commit scope.

### Type/name consistency

Shared names used throughout the plan are fixed as:

```text
catalog_context_fingerprint
input_fingerprint
root_command_id
procedure_id
segment_sequence
event_ordinal
firing_key
application_order_key
pending_child_invocations
unconsumed_advancement
```

Tasks must not introduce synonyms such as `chain_id`, `created_at`, `recency_timestamp`, `procedure_resource_copy` or `global_order` for these roles.
