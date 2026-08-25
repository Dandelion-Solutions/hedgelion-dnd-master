# Campaign House Rules — Step 2 Auditor-Reopen Evidence / Source Manifest Delta

Status: **STEP 2 REOPEN DELTA COMPLETE / MACHINE CONTRACT MATERIALIZED / STEP 3 HUMAN GATE NEXT**

Date: 2026-08-25

Governing task brief:

- `DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md`

Earlier Step-2 draft:

- `DEV/docs/superpowers/research/2026-08-25-campaign-house-rules-step-2-research-architecture-draft.md`

Senior whole-project audit disposition:

```text
HOUSE_RULES: HOLD / REOPEN AT STEP 2–3 GATE
S6D: DO NOT START YET
R2.7 WP-06: REMAINS PAUSED
```

This artifact supplements and corrects the earlier Step-2 evidence. It does **not** reopen Step 1 and does not reactivate Step 4–8.

---

## 1. Why the prior Step 2 was incomplete

The earlier synthesis correctly established the semantic/execution split, Context Runtime reuse, instruction/data fencing, publication/currentness reuse and the rejection of a second rules engine. It was incomplete in three material ways:

1. it did not inspect the current richer invocation machine-contract subgraph deeply enough;
2. it did not explicitly disposition the Step-1 responsibility alternatives A–E;
3. it treated campaign write/publication authorization as if it also answered the semantic right to adopt a new campaign-wide normative policy.

The third item is a real human architecture decision. The first two are evidence/completeness work.

---

# 2. Source Manifest delta

`SOURCE_MANIFEST_DELTA_STATUS: COMPLETE`

## 2.1 Current machine-contract sources newly inspected

| Source | Current fact established | Disposition |
|---|---|---|
| `DEV/CATALOG/mechanical-surfaces.json` | registered `INVOCATION_ADJUDICATED` **context facts are boolean** (`fiction.target_visible`, `fiction.target_reachable`) | KEEP BOOLEAN / NO CATALOG MUTATION REQUIRED |
| `DEV/SCHEMAS/mechanical-surfaces.schema.json` | context-fact metadata intentionally fixes `value_type = boolean`; selector input classes remain reviewed/closed | KEEP |
| `DEV/SCHEMAS/invocation-fact.schema.json` | accepted invocation facts carry boolean value + explicit provenance | KEEP AS BOOLEAN FACT CHANNEL |
| `DEV/TESTS/test_step2_evaluation_input_contract.py` | executable Step-2 tests enforce registered boolean invocation facts and forbid them from state-sensitive selectors | KEEP |
| `DEV/SCHEMAS/activity-parameter-spec.schema.json` | WP-06 already admits `INVOCATION_ADJUDICATED` Activity parameters with richer scalar types | EXTEND/TIGHTEN |
| `DEV/SCHEMAS/activity-definition-data.schema.json` | Activity definitions may declare invocation-specific typed parameters, including a DC-like integer parameter | EXISTING RICHER CONSUMER |
| `DEV/SCHEMAS/action-request.schema.json` | parameter bindings were raw scalar/array values with no per-binding adjudication provenance/current rules/eligibility basis | GAP |
| `DEV/SCHEMAS/runtime-command-state.schema.json` | accepted command already owns typed request + catalog context + `input_fingerprint`; ActionRequest is part of that accepted input | REUSE |
| `DEV/SCHEMAS/runtime-resolution-state.schema.json` | Resolution preserved raw parameter values but no richer adjudication evidence | GAP / REPAIRED |
| `DEV/SCHEMAS/runtime-continuation-state.schema.json` | Continuation preserved raw parameter values but no richer adjudication evidence | GAP / REPAIRED |
| `DEV/SCHEMAS/resolution-receipt.schema.json` | failure vocabulary lacked richer adjudication stale/conflict/realization-gap outcomes | GAP / REPAIRED |
| `DEV/TESTS/test_r2_7_wp06_rules_conformance.py` | current WP-06 tests explicitly recognize richer adjudicated Activity parameters as distinct from engine-owned state | REUSE |
| `DEV/TESTS/test_step3_execution_value_schemas.py` | Step-3 machine tests still intentionally enforce boolean invocation facts | KEEP |
| `DEV/TESTS/test_step3_execution_examples.py` | RuntimeCommand/Resolution/Continuation schemas are the current machine consumers for accepted/frozen execution input | REUSE |
| `DEV/TESTS/test_step3_execution_owner_contract.py` | Resolution/Continuation own fixed causal inputs and must not become copies of unrelated state owners | REUSE |
| `DEV/ARCHITECTURE/ACTIVITY_MODEL.md` | boolean context facts and Activity invocation parameters are distinct concepts; arbitrary code/query access is forbidden | KEEP / EXTEND BY CURRENT MACHINE CONTRACT |
| `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md` | Rule Element predicates read only registered boolean invocation facts/accessors; no arbitrary path/query/eval; state-sensitive selectors forbid invocation-only facts | KEEP |
| `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md` | accepted command fingerprinting, deterministic binder validation and frozen invocation input semantics already exist | INHERIT FREEZE/IDEMPOTENCY DISCIPLINE |

### Machine-currentness conclusion

The audit statement “existing `INVOCATION_ADJUDICATED` context facts are boolean” is correct, but boolean context facts are **not the only current invocation-adjudication structure**.

WP-06 already introduced richer `INVOCATION_ADJUDICATED` **Activity parameters**. Therefore the smallest repair is not to widen `context_facts` into a universal semantic-value language. It is to close the admission/provenance/freeze contract of the already-existing richer Activity-parameter consumer.

This preserves the Step-2 three-surface architecture:

```text
boolean invocation fact
    -> registered fact predicate input

Activity parameter
    -> bounded invocation-specific typed value

engine-owned accessor/state
    -> deterministic MechanicalContext authority
```

No channel may impersonate another.

## 2.2 Policy-adoption authority sources newly reconciled

| Source | What it owns | What it does NOT establish |
|---|---|---|
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | repository role, creator identity, campaign write authorization, PLAYER binding, creator-only maintenance operations | semantic right to make a new House Rule/ruling campaign-wide normative |
| `GAME/CORE/ADJUDICATION.md` | local adjudication, temporary ruling semantics, statement that a table-adopted permanent rule should be persisted | who constitutes adoption authority / how delegation works |
| `GAME/CORE/PLAY_POLICY.md` | rules decision order and duty to preserve material reusable precedent | semantic adoption principal or consent model |
| `GAME/CORE/MULTIPLAYER.md` | creator/member/write/currentness rules for multiplayer | policy-legislative authority merely from PLAYER/write capability |

Therefore:

> **repository/campaign publication permission is necessary enforcement infrastructure, but is not itself policy-adoption authority.**

This is an unresolved product-semantic/authority decision and is carried to amended Step 3.

---

# 3. Richer adjudication machine contract — derivable result

This section is mechanical detail derived from accepted execution/ownership laws plus the already-existing Activity parameter consumer. It does not decide who may adopt campaign policy.

## 3.1 Legal richer consumer

The initial richer semantic-value channel is **only** an Activity parameter whose selected Activity declaration explicitly says:

```text
source_class = INVOCATION_ADJUDICATED
```

A richer value is not automatically:

- a Rule Element context fact;
- an accessor value;
- a world-state value;
- a TransitionRequest mutation payload with adjudication authority;
- a generic LLM variable.

## 3.2 Initial admitted value classes

For `INVOCATION_ADJUDICATED` Activity parameters the initial machine contract admits only:

```text
boolean
integer       with finite allowed_values OR both minimum + maximum
number        with finite allowed_values OR both minimum + maximum
machine_id    with finite allowed_values
              OR allowed_definition_kinds + bounded deterministically admitted candidate set
```

Initial exclusions:

```text
free-form adjudicated string     FORBIDDEN
adjudicated cardinality=many     FORBIDDEN
arbitrary JSON/object value      FORBIDDEN
unbounded numeric domain         FORBIDDEN
unbounded machine-id namespace   FORBIDDEN
```

These exclusions are YAGNI/security/correctness constraints, not a claim that future evidence can never justify another reviewed class.

## 3.3 Accepted binding evidence

An accepted richer adjudicated parameter binding is no longer a naked scalar. It carries:

```text
source_class = INVOCATION_ADJUDICATED
value
provenance_ref
eligibility_basis_fingerprint
rules_context_fingerprint
policy_basis_refs[]
candidate_set_fingerprint?       # required by binder when dynamic bounded candidate selection is used
```

Semantics:

- `provenance_ref` identifies the accepted adjudication/input evidence;
- `eligibility_basis_fingerprint` binds the decision to the R2.3/Step-4 eligible source basis used for that consumer/purpose;
- `rules_context_fingerprint` binds the decision to the current validated rules context used before acceptance;
- `policy_basis_refs[]` records applicable durable campaign-policy source/revision references; it may be empty for lawful local adjudication without durable policy basis;
- `candidate_set_fingerprint` identifies the bounded candidate set when a machine-id value came from dynamic candidate discovery rather than a static enum.

These fields are causal execution evidence. They are not new world truth, policy authority, context authority or a global policy epoch.

## 3.4 Deterministic admission

Before RuntimeCommand acceptance the deterministic binder must establish all of the following:

1. selected Activity and parameter declaration are current and legal under the accepted catalog context;
2. the parameter exists and its source class is `INVOCATION_ADJUDICATED`;
3. value type/cardinality/range/finite enum/domain matches the declaration;
4. any dynamic machine-id candidate belongs to the deterministically admitted bounded candidate set;
5. the information basis used for adjudication was eligible for the exact role/consumer/purpose;
6. the rules-context basis is still current for this new affected command;
7. policy references, where present, resolve to current authoritative published policy rather than stale/unpublished text;
8. no same-precedence unresolved policy conflict exists for the affected semantic decision;
9. the selected result maps only to an already admitted deterministic consumer/capability.

The binder does not execute a natural-language predicate language and does not infer authority from the presence of an object in the request.

## 3.5 Frozen identity / retry / resume

The Step-3 `RuntimeCommand.input_fingerprint` already includes the typed ActionRequest payload. Therefore the full enriched adjudicated binding participates in accepted command identity without inventing another global input ID.

Once accepted:

```text
RuntimeCommand accepted input
    -> Resolution.parameter_bindings
    -> Continuation.parameter_bindings if suspended
```

preserves the same accepted binding evidence.

Later policy publication is forward-looking and does not rewrite the stored accepted input of an existing Resolution generation.

A **new** affected command assembled under a stale eligibility/rules/policy basis must not be accepted under that stale basis.

## 3.6 Finite failure behavior

The current closed failure vocabulary now includes:

```text
failure.adjudication_input_missing
failure.adjudication_input_unauthorized
failure.adjudication_input_invalid
failure.adjudication_context_stale
failure.policy_conflict
failure.policy_realization_gap
```

Interpretation:

- missing — required reviewed adjudicated input was not supplied;
- unauthorized — input source/consumer/eligibility class is not allowed;
- invalid — wrong type/range/domain/candidate or malformed accepted evidence;
- stale — eligibility/rules context ceased to be current before new command acceptance;
- policy conflict — applicable active policy cannot be lawfully resolved under current precedence;
- realization gap — current policy semantic result has no admitted deterministic realization.

These outcomes never authorize prose fallback mutation.

## 3.7 Explicit security/authority prohibitions

The richer contract does not introduce and explicitly forbids:

- arbitrary JSON-path/state reads;
- generic `eval`, expression, query, callback or predicate DSL;
- free-form state injection;
- arbitrary object payloads as adjudicated values;
- LLM assertion of engine-owned HP/Resource/Effect/etc. as trusted adjudication input;
- use of an adjudicated parameter to bypass Activity/operation/owner validation;
- direct policy-prose mutation;
- global policy epoch/frontier;
- generic natural-language rule compiler.

---

# 4. Current machine materialization

Owner authorization for clean-slate pre-release structural changes is applied here. `2.0.0` was inspected and was **not** treated as a compatibility freeze.

TDD sequence:

1. `c8ed8c1059b5391597e9fb74eaa4311128cfe4ad` — added failing contract tests first;
2. focused RED reproduced seven expected contract failures on the current schema shapes;
3. `dcd19c60796825af79baa3e3b8de4227e018dfd0` — materialized the structural repair;
4. the same focused contract assertions are GREEN after the schema change.

Current changed machine surfaces:

- **NEW** `DEV/SCHEMAS/activity-parameter-binding.schema.json`;
- **UPDATED** `DEV/SCHEMAS/activity-parameter-spec.schema.json`;
- **UPDATED** `DEV/SCHEMAS/action-request.schema.json`;
- **UPDATED** `DEV/SCHEMAS/runtime-resolution-state.schema.json`;
- **UPDATED** `DEV/SCHEMAS/runtime-continuation-state.schema.json`;
- **UPDATED** `DEV/SCHEMAS/resolution-receipt.schema.json`;
- **NEW TEST** `DEV/TESTS/test_house_rules_adjudicated_input_contract.py`.

`DEV/CATALOG/mechanical-surfaces.json` and its schema were inspected and deliberately **not** changed: their boolean fact contract remains correct and should not be widened merely to satisfy House Rules.

The repository `validate.yml` runs only for `main`, `feature/**` and pull requests; this authoritative `v1/engine-rearchitecture` push therefore provides no branch-push CI run to cite. Final closure must not claim full repository test-suite success until an applicable runner/implementation-validation gate executes it. Focused schema-contract RED/GREEN evidence is recorded above.

---

# 5. Step-1 responsibility alternatives A–E — explicit disposition

These are responsibility shapes, not cosmetic variants.

## A — existing-owner runtime contract + minimal campaign policy conventions

**Disposition: SELECT AS PRIMARY SHAPE — AGENT RECOMMENDATION, HUMAN APPROVAL REQUIRED AT STEP 3.**

Evidence already supplies the required owners:

- PLAY_POLICY/ADJUDICATION for live rules/adjudication behavior;
- Step-4/R2.3 for eligible bounded context;
- R2.4 for instruction/data/role boundary;
- Step-5.6/5.7/5.8 for publication/recovery/currentness;
- Activity/Rule Element/Step-3 for deterministic execution.

No current requirement proves a new runtime policy subsystem is necessary.

## B — dedicated narrow runtime policy owner

**Disposition: REJECT FOR CURRENT BASELINE / REOPEN ONLY IF HUMAN ADOPTION DECISION CANNOT BE EXPRESSED CLEANLY THROUGH EXISTING OWNERS.**

A new owner would be justified only if existing PLAY_POLICY/ADJUDICATION + campaign authority surfaces cannot represent the selected policy-adoption semantics without duplicate authority. Current evidence does not prove that.

## C — structured identity/currentness sidecar

**Disposition: COMPOSE NARROWLY WITH A.**

Machine linkage is required for stable durable policy identity/revision/currentness and for accepted policy-dependent input basis. The structured part remains supporting identity/currentness evidence, not a second semantic-policy owner and not a global frontier.

Exact durable policy-adoption fields wait for the human authority decision because their authorization semantics are not mechanically derivable.

## D — predominantly structured campaign policy

**Disposition: REJECT.**

It would force intrinsically contextual Master judgment into structured predicates/mechanics and drift toward a second rules engine. Structured mechanics remain a later optional promotion target when a rule becomes sufficiently formalizable.

## E — prose-only policy with no machine linkage

**Disposition: REJECT AS COMPLETE ARCHITECTURE.**

It cannot provide stable currentness/frozen-input linkage, conflict/supersession identity or bounded deterministic handoff evidence. Human-readable prose remains the normative semantic content, but it requires narrow machine linkage around identity/currentness/adjudicated inputs.

### Responsibility-shape synthesis

Recommended composition:

```text
A as primary runtime responsibility shape
+
C only for narrow identity/currentness/accepted-input linkage
```

This is still a material owner/subsystem choice and is therefore presented, not self-approved, in amended Step 3.

---

# 6. GAME/CAMPAIGN/RULES/HOUSE_RULES.md classification

**Classification: A — intentional runtime-facing business-policy projection, not runtime implementation.**

Governing basis:

- Step 1 explicitly requires the runtime Master to know the purpose/limits of the campaign policy layer; a DEV-only architecture statement is insufficient;
- the current GAME text states only already-preserved semantic boundaries: policy scope, deterministic handoff, no RNG/state authority, one-off ruling not automatically permanent, and instruction/data subordination;
- it does not implement policy retrieval, adoption authorization, persistence, conflict detection, typed binding validation or publication/currentness machinery.

Required correction while the design is on HOLD:

- the GAME file must not claim that the previously closed DEV House-Rules artifact is a final canonical contract;
- it must not imply that “authorized adoption” is already defined;
- it must remain self-contained as shipped runtime policy rather than depend on DEV content being present.

This classification does **not** use the word “documentation” to grant GAME write authority; the semantic projection is justified by Step-1 runtime-consumer requirements and limited to already accepted boundaries.

---

# 7. Remaining evidence gap is human, not technical

The machine consumer gap described by the Senior Auditor is now structurally closed at the current pre-release contract level.

The remaining blocking issue is semantic authority:

> **Who may transform a lawful local adjudication or proposed House Rule into campaign-wide normative policy, and under what delegation/consent scope?**

Current ACCESS_CONTROL/publication mechanisms can enforce a selected answer, but they do not select the answer.

This is carried to the amended Step-3 Decision Brief.

---

# 8. Step-2 result

```text
STEP_1: PRESERVED / NOT REOPENED
STEP_2_EVIDENCE_DELTA: COMPLETE
MACHINE_CONTRACT_GAP: MATERIALIZED AT CURRENT PRE-RELEASE STRUCTURAL LAYER
A_E_RESPONSIBILITY_COVERAGE: COMPLETE
POLICY_ADOPTION_AUTHORITY: UNRESOLVED HUMAN DECISION
STEP_3: HUMAN DECISION GATE REQUIRED
STEP_4_PLUS: BLOCKED
S6D: NOT STARTED
R2_7_WP06: PAUSED
```
