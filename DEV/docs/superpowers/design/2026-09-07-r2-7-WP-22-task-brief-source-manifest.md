# R2.7 WP-22 Step 1 — Task Brief + Source Manifest

Status: **STEP 1 COMPLETE — CRITIC REPAIRS INCORPORATED / MANDATORY SENIOR REVIEW PENDING**

Date: 2026-09-07

Domain: **Verification / test / evaluation completeness**

Product Owner launch: **EXPLICITLY AUTHORIZED 2026-09-07**.

Starting authoritative branch state used for Step 1:

```text
branch: v1/engine-rearchitecture
HEAD: 8679b9765c7978cc951871a6035e7c0347e5232f
```

This artifact owns only WP-22 Step-1 framing and Source Manifest. The independent Step-1 whole-project critic is recorded in:

- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-22-step-1-whole-project-critic.md`.

It does not authorize Step 2, WP-23, implementation planning, substantive implementation, runtime migration or gameplay bootstrap.

---

## 1. Mission

WP-22 is the whole-project verification-readiness audit immediately before later release/readiness work. Its purpose is not to maximize test count. Its purpose is to determine whether accepted architecture has **appropriate, current, non-misleading verification ownership** and to make every remaining proof obligation explicit before implementation planning.

The five scope-owner questions are mandatory:

1. does every important accepted architecture law map to an appropriate verification owner;
2. which existing tests are stale, contradict later accepted architecture or encode obsolete scaffolds;
3. are Protocol-4-derived MVP evaluations preserved as **post-implementation** behavioral/performance acceptance rather than fake architecture-stage implementation;
4. are important negative laws, rejected abstractions and fail-closed outcomes regression-protected where materially likely to regress;
5. can CI/maintenance audit mechanically validate the parts of architecture completeness that are actually machine-checkable without pretending that green CI proves behavioral/product evaluation completeness.

WP-22 must preserve a strict distinction between **architecture coverage**, **machine realization**, **executable verification** and **empirical product evaluation**.

---

## 2. Non-goals

Step 1 does not:

- implement missing runtime/schema/catalog behavior;
- create implementation plans;
- add broad new test suites merely because a future implementation obligation exists;
- treat a Markdown scenario catalog as executable proof merely because an audit reads the file;
- treat one passing CI workflow as proof that every accepted law has verification ownership;
- invent a global verification database/registry;
- manufacture a Protocol-4 source that is not present in current repository evidence;
- re-run historical LLM experiments as architecture work;
- perform release/package/legal readiness work owned by WP-23;
- change accepted runtime law to make an existing test pass;
- reopen closed architecture solely because a test name/fixture is old;
- convert deferred empirical/performance revisit triggers into current implementation work.

---

## 3. Verification proof taxonomy

Every coverage claim in WP-22 must classify the proof rather than treating all evidence as interchangeable.

```text
EXECUTABLE_CURRENT
    machine-executed test against current owners/surfaces; current CI may or may not run it

STATIC_AUDIT_CURRENT
    machine-executed structural/text/schema/catalog/source audit; useful for machine-checkable invariants but not behavioral proof

SCENARIO_ACCEPTANCE_CURRENT
    reviewed scenario/adversarial case specification; may define expected behavior without being directly executable

EMPIRICAL_EVALUATION_CURRENT
    measured LLM/runtime/product behavior from a controlled evaluation with stated applicability and limitations

DEFERRED_UNTIL_REALIZATION
    verification obligation is valid but its target machine/runtime behavior is intentionally not implemented yet

VERIFICATION_GAP
    an important realized/current law has no sufficient current proof owner after reconciliation

SUPERSEDED_OR_HISTORICAL
    useful provenance only; not current acceptance authority

NOT_MACHINE_CHECKABLE
    semantic/product judgment that cannot be honestly reduced to a deterministic CI guard at this stage
```

A single law may need more than one class. For example, a deterministic policy may have an executable contract test while its player-facing latency/quality consequence needs later empirical evaluation.

---

## 4. Required Step-2 coverage ledger

Before any whole-project verification-completeness claim, Step 2 must build an item-level **Verification Coverage Matrix** from current owning law, not from test filenames.

Minimum columns:

```text
law / requirement ID or bounded law family
current owning artifact
polarity:
    POSITIVE | NEGATIVE | FAILURE | INDETERMINATE | PERFORMANCE | BEHAVIORAL
machine-realization status
verification proof class
exact current verification artifact(s)
CI / maintenance-audit execution route if any
stale / supersession disposition
remaining verification gap
safe defer trigger / revisit condition where applicable
```

Coverage does not require one row per sentence when an owner-defined law family has one genuinely coherent proof contract, but aggregation must preserve item-level semantics, exceptions, negative cases and defer triggers. No architecture family may be marked covered solely because a similarly named `test_*.py` or `*_CASES.md` file exists.

---

# 5. Source Manifest

## 5.1 Process / current-state authority

| Source | Role in WP-22 | Step-1 disposition |
|---|---|---|
| `AGENTS.md` | repository governance, current-ref/write policy, Version Impact, fixed ref-delete prohibition | controlling process input |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | ChatGPT Work transport/current-ref constraints | controlling runtime overlay |
| `DEV/DESIGN_PROCESS.md` | eight-step architecture process, Source Manifest/evidence/synthesis gates | controlling process |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | HDM critic and mandatory Senior review gates | controlling process |
| `DEV/PROJECT_MAP.md` | dependency routing between architecture, GAME, schemas, tests, tools, release/CI | routing input; not semantic owner |
| `DEV/CURRENT_PROGRESS.md` | sole global cursor | WP-21 closed; current user authorization launches WP-22 Step 1 |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | sequencing only | WP-22 precedes WP-23; no current-progress authority |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md` | R2.7 scope owner | supplies the five mandatory WP-22 questions |
| `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-21-final-senior-review.md` | immediate predecessor closure | WP-21 PASS / closed; WP-22 was not started before explicit PO launch |

## 5.2 Current architecture-law universe

Step 2 must derive the verification ledger from **current accepted owners**, including the dependency-relevant law families below. Historical design provenance does not substitute for them.

### Round-1 / Steps 1–5 families

Current canonical Step-2/3/4 architecture plus Step-5.0..5.14 owners and their accepted amendments are in scope where they still own runtime semantics, including:

- authoritative truth/state and deterministic execution;
- rules/adjudication/mechanics and randomness;
- knowledge/disclosure/communication;
- persistence/durability/publication;
- session/recovery/checkpoint/currentness;
- LIVE/multiplayer/chronology;
- Story/history/retention;
- maintenance/cleanup/retirement;
- negative/fail-closed/ambiguous-outcome laws.

### Round-2 families

R2.1..R2.6 accepted canonical owners remain verification inputs where their semantics survive into current realization:

- bounded context discovery/eligibility;
- Actor cognition/relationship boundaries;
- role-context request/bundle/trace contracts;
- TurnEnvelope/instruction/rebind rules;
- recipient/catch-up/planning containment;
- behavioral containment/lawful later uptake.

### R2.7 families already closed

WP-08..WP-21 canonical/final-Senior-approved results remain current verification inputs, including:

- role/context instruction realization;
- context/resource bounds;
- durable record-family and physical topology allocation;
- HOT/SQLite realization boundaries;
- publication/recovery/chronology/LIVE/multiplayer/async collaboration;
- Story/Dramaturg planning;
- bootstrap/campaign creation;
- v1.0+ update/migration;
- diagnostics/observability/cleanup/retirement.

Accepted Product Owner decisions and superseding amendments must be used where they change the applicable law, including clean-slate v1.0 compatibility, creator-login fail-closed continuity and absolute Git branch/ref deletion prohibition.

**Step-1 completeness rule:** Step 2 must map current owners bidirectionally to verification. It must not use roadmaps, search snippets, historical status documents or test names as substitutes for current semantic ownership.

## 5.3 Machine/runtime surfaces that verification may target

Current machine/runtime targets include, as applicable:

- `GAME/CORE/*.md` current runtime contracts;
- `GAME/SCHEMA/*.schema.yaml` persistent/protocol machine contracts;
- `GAME/CAMPAIGN/` and `GAME/TEMPLATE/` current templates;
- `GAME/RULES/` and `GAME/TOOLS/` current machine/runtime tools;
- `DEV/CATALOG/` and `DEV/SCHEMAS/` development machine contracts;
- `DEV/ARCHITECTURE/` implementation-facing architecture interfaces;
- `GAME/ENGINE_VERSION.yaml` and `DEV/ENGINE_DEVELOPMENT.yaml` where a verification law concerns version identity;
- release/build surfaces **only as verification consumers** in WP-22; package/version/legal readiness remains WP-23.

Absence of a future machine surface explicitly deferred by a current owner is not automatically a WP-22 implementation defect. Its verification row is `DEFERRED_UNTIL_REALIZATION` with the exact trigger and future acceptance obligation.

---

## 6. Current verification/test/CI dependency subgraph

### 6.1 Executable Python regression/contract tests

`DEV/TESTS/test_*.py` is the principal executable unittest surface. Current families include:

- process/authority guards: current-progress authority, PO routing, branch/ref deletion/retirement;
- publication/currentness and versioning namespace guards;
- catalog/schema/mechanics/R2.7 conformance tests;
- persistence/session/bootstrap/update/recovery/LIVE/multiplayer tests;
- role/context/Story/planning and final-recovery tests;
- release-builder/version/provenance tests used as verification consumers.

Presence in `DEV/TESTS` establishes discoverability, **not correctness or semantic currency**. Every material test assumption must be reconciled against the current owner before it counts toward coverage.

### 6.2 Scenario/adversarial catalogs

`DEV/TESTS/*_CASES.md` and related Markdown artifacts contain reviewed scenario/acceptance contracts such as:

- access control;
- chronology;
- integrity/recovery;
- persistence transactions;
- LIVE/multiplayer;
- engine update;
- runtime context;
- performance and gameplay-quality cases.

These are `SCENARIO_ACCEPTANCE_CURRENT` only when their assumptions remain current. They do not become executable merely because a static audit checks that particular case IDs/text are present.

### 6.3 Maintenance audit

`DEV/TOOLS/run_maintenance_audit.py` invokes `DEV/TOOLS/audit_engine.py` as repository/source-tree validation.

Current `audit_engine.py` provides substantial machine-checkable verification of:

- current-progress routing;
- repository layout/version projections;
- CORE activation/runtime scope;
- stale-policy sentinels;
- persistence ownership;
- schemas/templates/catalog/package/source consistency;
- selected Markdown regression sentinel content and global case-ID uniqueness;
- other structural/release/tool smoke invariants.

It does **not** prove that every accepted architecture law owns verification, and it does not convert all Markdown scenario cases into executable behavioral tests.

### 6.4 Hosted CI

`.github/workflows/validate.yml` currently executes on the active version branch:

```text
Run full maintenance audit
DEV/TOOLS/run_maintenance_audit.py

Run DEV unit tests
.hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -v
```

Therefore a green workflow proves that the **currently admitted audit plus unittest suite executed successfully at that exact source head**. It is not, by itself, a proof that the suite is semantically complete, unstale or sufficient for behavioral/product evaluation.

---

## 7. Current evidence classes and representative dispositions

### Strong current negative-law executable guards

Representative examples already present and current:

- `DEV/TESTS/test_branch_ref_deletion_prohibition.py` — absolute no-delete/probe/fallback law;
- `DEV/TESTS/test_branch_ref_retirement_policy.py` — logical-only retirement semantics;
- `DEV/TESTS/test_publication_ref_fence_contract.py` — non-force/stale/current-closure publication behavior;
- `DEV/TESTS/test_versioning_namespace_policy.py` — fail-closed whole-repo version-like census and normalized version namespace guards;
- `DEV/TESTS/test_product_owner_routing_consistency.py` — stale routing to closed WPs;
- `DEV/TESTS/test_current_progress_authority.py` — one global progress authority.

These examples demonstrate that negative-law regression protection is feasible. They do **not** prove whole-project negative-law completeness; Step 2 must inventory remaining high-risk negative/failure laws explicitly.

### Current engine-update scenario surface

`DEV/TESTS/ENGINE_UPDATE_CASES.md` is already aligned to current v1.0+ compatibility law, including the clean-slate horizon and the rule that Git ancestry is provenance/order evidence rather than compatibility authority. It is not repaired in Step 1.

### Active stale executable test found by Step-1 critic

`DEV/TESTS/test_engine_update_policy_contract.py` contained a test named:

```text
test_same_version_descendant_refresh_is_silent_and_does_not_force_manifest_commit
```

Its broad lexical assertions could pass against current `GAME/CORE/ENGINE_UPDATES.md` while preserving the obsolete semantic implication that descendant ancestry itself authorizes silent use/refresh. Current law instead says:

```text
same-version ancestry -> candidate provenance/order only
silent preference -> candidate to evaluate only
use of different released bytes -> still requires affirmative compatibility classification
```

Step 1 mechanically repairs only that regression guard. Runtime law is unchanged.

---

## 8. Empirical / LLM evaluation evidence

### Current retained evidence

The repository currently contains Role-Context Validation Protocols 1–3. Protocol 3 is explicitly completed validation evidence with applicability limits and rejected/broken measurement channels. It also preserves deferred gameplay-quality validation dimensions such as:

- plot divergence without incoherence;
- NPC autonomy/identity;
- continuity of generated facts;
- delayed callbacks;
- player agency;
- pacing/artistic quality/canonical stability;
- reasoning-budget/creativity/persistence trade-offs.

The WP-08 mini-report separately preserves future verification/MVP obligations for:

- behavioral containment and lawful later uptake;
- fresh Narrator rebind / no raw private handoff;
- no same-envelope Story feedback;
- recipient/catch-up/planning containment;
- bounded/degraded/`UNSATISFIABLE` paths;
- no hidden-reasoning dependency.

`DEV/TESTS/PERFORMANCE_CASES.md` supplies scenario expectations, not measured post-implementation latency/quality evidence.

`DEV/TESTS/TODO_LONG_CAMPAIGN_SCALE.md` is explicitly deferred until meaningful real-campaign measurements exist and must not be counted as current performance proof.

### Protocol-4 source status

The WP-22 scope owner explicitly asks about **Protocol-4-derived MVP evaluations**. Current repository discovery found:

- Protocol 1;
- Protocol 2;
- Protocol 3;
- no current artifact named or identifiable as Protocol 4;
- no current commit search result for `Protocol-4` / `protocol 4`.

Disposition:

```text
PROTOCOL_4_SOURCE: INCOMPLETE_SURFACE / NOT FOUND IN CURRENT REPOSITORY EVIDENCE
PROTOCOL_1_3: SUPPORTING EVIDENCE ONLY
WP08_MVP_OBLIGATIONS: SUPPORTING CURRENT REQUIREMENTS
PO_DECISION_REQUIRED: NO
```

Step 2 must recover/reconcile the intended Protocol-4-derived evaluation requirement before any final post-implementation evaluation-completeness claim. Protocol 3 or WP-08 evidence must not be silently relabeled as Protocol 4.

If source recovery still fails and the missing semantics cannot be established from current accepted requirements without inventing product/evaluation criteria, that later state becomes a decision-routing question. Step 1 does not manufacture such a decision now.

---

## 9. Historical / deferred evidence discipline

Examples establish the required classification rule:

- `DEV/TESTS/PRE_RELEASE_AUDIT_0.1.0.md` explicitly labels itself historical and is `SUPERSEDED_OR_HISTORICAL`, not current runtime acceptance;
- `DEV/TESTS/TODO_LONG_CAMPAIGN_SCALE.md` is `DEFERRED_UNTIL_REALIZATION/MEASUREMENT`;
- `DEV/TESTS/PERFORMANCE_CASES.md` is a current scenario catalog, not empirical performance measurement;
- old version tokens such as `v0.8` inside an explicitly negative fixture/test do not make the test stale by token alone.

Staleness is semantic: compare the tested assumption with the current owner.

---

## 10. Step-2 mandatory evidence work

After Senior PASS/GO, Step 2 must perform all of the following before synthesis:

1. build the Verification Coverage Matrix from current accepted owners;
2. classify important laws by positive/negative/failure/indeterminate/performance/behavioral polarity;
3. distinguish realized current targets from `DEFERRED_UNTIL_REALIZATION` obligations;
4. inspect current executable tests for stale/superseded assumptions, prioritizing authority, persistence/currentness, compatibility/migration, knowledge/disclosure, LIVE/multiplayer and deterministic mechanics;
5. separately inventory important negative laws/rejected abstractions and map their regression protection;
6. map every executable test/audit proof to its actual CI/audit execution route or explicitly note that it is not automatically executed;
7. inventory Markdown scenario catalogs without falsely upgrading them to executable proof;
8. recover/reconcile the Protocol-4-derived post-implementation evaluation requirement; preserve empirical evaluation applicability/measurement validity;
9. preserve deferred implementation/evaluation triggers rather than activating them;
10. identify which machine-checkable architecture invariants can reasonably become CI/audit completeness guards in later implementation and which cannot;
11. report exact `VERIFICATION_GAP` rows rather than “test coverage percentage” without semantic ownership.

No Step-2 implementation or broad test addition is authorized by this Step-1 artifact.

---

## 11. Expected Steps 2–8 deliverables after Senior GO

Subject to mandatory independent Senior approval of Step 1, later WP-22 work should produce:

- refined research/evidence ledger and Verification Coverage Matrix;
- stale-test and obsolete-scenario dispositions;
- negative-law regression map;
- post-implementation behavioral/performance evaluation inventory;
- CI/audit machine-checkability boundary;
- Decision Brief and alternatives;
- reviewed candidate verification architecture/completeness contract if a durable implementation-facing owner is actually necessary;
- whole-project adversarial review and finding propagation;
- canonicalization/closure only after the normal gates.

WP-22 must not create implementation work merely to make the verification matrix look green.

---

## 12. Version Impact

Step-1 planned publication changes only:

- DEV design/status artifacts;
- one DEV regression test whose assertions are synchronized to already-current `GAME/CORE/ENGINE_UPDATES.md` semantics.

It changes no `GAME/CORE` runtime law, `GAME/SCHEMA` contract, engine release identity, framework module version, persistent schema/generation, catalog generation, ruleset identity or compatibility namespace.

```text
VERSION_IMPACT: VERIFIED
VERSION_BUMP_REQUIRED: NO
VERSION_IMPACT_DISPOSITION: NONE
VERSIONING_TAXONOMY_REOPENED: NO
```

---

## 13. Human / Product Owner decision

Current Step-1 evidence exposes no genuine product semantic, material architecture trade-off or risk acceptance requiring human judgment.

```text
HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
NEEDS_PO: NONE
```

The missing Protocol-4 artifact is an evidence/source-recovery obligation, not enough by itself to invent a Product Owner question.

---

## 14. Exact Step-1 stop

After coherent publication and exact-head verification/read-back:

```text
WP22_STEP1_TASK_BRIEF_COMPLETE: YES
WP22_STEP1_SOURCE_MANIFEST_COMPLETE: YES
WP22_STEP1_CRITIC_COMPLETE: YES
WP22_STEP1_MECHANICAL_REPAIRS_COMPLETE: YES
WP22_STEP1_COMPLETE: YES

WP22_STEP1_SENIOR_REVIEW: REQUIRED / PENDING
WP22_STEP2_STARTED: NO
WP23_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
NEXT_AUTHORIZED_UNIT: NONE
```
