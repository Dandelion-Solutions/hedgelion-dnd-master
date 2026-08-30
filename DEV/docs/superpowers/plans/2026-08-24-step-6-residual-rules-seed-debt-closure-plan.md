# S6D Residual Rules/Seed Debt Closure — Architecture Execution Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use `superpowers:executing-plans` when this plan is started. Apply `superpowers:test-driven-development` to every machine-contract change and `superpowers:verification-before-completion` before every closure claim.

**Goal:** Close all still-applicable rules/catalog/seed obligations historically deferred to Step 6 before resuming R2.7 WP-06.

**Architecture:** S6D is a bounded architecture/machine-contract closure workstream. It derives a complete supported rules seed from accepted HDM ownership laws, closes metadata/schema/catalog gaps, and validates representative D&D mechanics without creating a second execution engine or restoring retired physical-LLM Step-6 requirements.

**Tech Stack:** Markdown architecture/specs, JSON catalogs, JSON Schema Draft 2020-12, Python `unittest`/`jsonschema`, existing HDM validation/audit tooling, GitHub Connector for remote state/writes.

**Spec:** `DEV/docs/superpowers/design/2026-08-24-step-6-residual-rules-seed-debt-closure-task-brief.md`

## Global Constraints

- Work only on existing `v1/engine-rearchitecture`; do not create an audit/probe branch.
- Remote GitHub operations use the GitHub Connector only.
- R2.7 remains paused until S6D closure gate.
- Do not resurrect retired physical role-isolation requirements.
- No backward-compatible migration layer is required for the current unreleased campaign scaffold.
- Preserve one semantic owner per fact/state.
- LLM adjudication may supply only explicitly authorized non-engine-owned inputs/proposals; deterministic mechanics/RNG/state commit remain kernel-owned.
- Normal gameplay must remain bounded/local; no ordinary-turn global scans, mandatory web lookups or unnecessary extra LLM/network round trips.
- Structural catalog/schema/rules-package canonicalization is authorized; broad runtime implementation is not.
- Public HDM material must remain independently worded and legally conservative.

---

## Task 1 — Freeze the interruption and reconstruct the complete Step-6 residual debt ledger

**Files:**
- Create: `DEV/docs/superpowers/research/2026-08-24-s6d-source-manifest-and-residual-debt-ledger.md`
- Read: Steps 1–3 owning artifacts, Steps 1–2 assurance closure, former Step-6 working artifacts, Round-1 Step-6 closure decision, current WP-06 checkpoint.

**Produces:** item-level `S6D-Dxxx` debt IDs with source, qualifier, current applicability, machine status and target S6D domain.

- [ ] Re-read current remote ref, process owners, roadmap, S6D owner decision/task brief and R2.7 pause checkpoint.
- [ ] Enumerate every explicit `Step 6 owns/must/close/deferred` statement from accepted Steps 1–2 and assurance artifacts.
- [ ] Reconcile each item against later Steps 3–5 and Round-2 decisions; classify `SATISFIED`, `SUPERSEDED`, `ACTIVE_S6D`, `DORMANT`, or `N/A_CLEAN_SLATE`.
- [ ] Add every machine gap already discovered in WP-06, preserving its owning source and whether it is old debt or newly exposed conformance debt.
- [ ] Run synthesis-completeness check: every active S6D requirement must have exactly one target task below.
- [ ] Publish/read-back the ledger before Task 2.

## Task 2 — Close ruleset/package/catalog snapshot identity

**Files:**
- Modify: `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md`
- Modify/create as evidence requires: package/catalog manifest schema/catalog artifacts under `DEV/SCHEMAS/` and `DEV/CATALOG/`.
- Test: focused S6D package-context regression under `DEV/TESTS/`.

**Produces:** exact machine-validatable identity sufficient to reconstruct a compatible `ResolvedCatalogContext`.

- [ ] Write failing tests showing current metadata cannot uniquely reconstruct the intended engine/ruleset/catalog snapshot.
- [ ] Verify RED from current exact-source state.
- [ ] Define minimal package-level identity fields; reject per-record package-version duplication.
- [ ] Add/modify machine schema and catalog/package manifest artifacts.
- [ ] Add compatible/incompatible snapshot examples and validation assertions.
- [ ] Verify GREEN by source/schema validation available on the branch; record executable-CI limitation if dispatch remains unavailable.
- [ ] Publish/read-back checkpoint.

## Task 3 — Complete selector metadata registry

**Files:**
- Modify: `DEV/CATALOG/mechanical-surfaces.json`
- Modify: `DEV/SCHEMAS/mechanical-surfaces.schema.json`
- Modify as required: `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`
- Test: `DEV/TESTS/test_step2_machine_contracts.py` and focused S6D selector coverage test.

**Produces:** registry equality and complete typed metadata for every supported selectable selector.

- [ ] Write RED assertion: supported `core-catalog.rule_selectors == mechanical-surfaces.selectors`.
- [ ] Build selector-by-selector evidence matrix: consumer, contribution type, legal operations, input classes, dependencies, resolver ownership.
- [ ] Remove selectors that are stale/unproven rather than inventing semantics.
- [ ] Fill complete metadata for supported selectors.
- [ ] Tighten schema enums/types only to proven needs; avoid generic escape hatches.
- [ ] Add adversarial assertions against arbitrary override/query/input-class leakage.
- [ ] Verify and publish checkpoint.

## Task 4 — Complete MechanicalContext accessors, invocation facts and dependency metadata

**Files:**
- Modify: `DEV/CATALOG/core-catalog.json`
- Modify: `DEV/CATALOG/mechanical-surfaces.json`
- Modify: relevant accessor/predicate schemas under `DEV/SCHEMAS/`.
- Test: Step-2 evaluation-input and S6D dependency tests.

**Produces:** complete safe input/read graph for the supported seed.

- [ ] Enumerate every accessor/fact actually required by supported selectors/operations/domain seed cases.
- [ ] Write RED assertions for missing metadata/unknown dependencies.
- [ ] Add only proven accessors/facts; engine-owned values remain inaccessible through `INVOCATION_ADJUDICATED`.
- [ ] Test true/false/missing fact distinction and transitive input-class legality.
- [ ] Test concrete cycle rejection for representative combined definitions.
- [ ] Preserve runtime domain queries as nonserializable implementation capabilities.
- [ ] Verify and publish checkpoint.

## Task 5 — Close reusable Activity protocol value contracts

**Files:**
- Modify/create: `DEV/SCHEMAS/target-spec.schema.json`, `area-spec.schema.json`, `cost-spec.schema.json`, `roll-request.schema.json`, Activity parameter schemas and other proven embedded protocol schemas.
- Modify: `DEV/SCHEMAS/activity-definition-data.schema.json`
- Modify: `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`
- Test: Step-2/3 activity examples plus focused S6D protocol tests.

**Produces:** exact typed value interfaces; no hidden arbitrary JSON execution channel.

- [ ] Inventory every `value.*` consumed by supported Activity/runtime mechanics.
- [ ] Classify each as `EMBEDDED_MACHINE_SCHEMA`, `EPHEMERAL_IMPLEMENTATION_ONLY`, or `REMOVE_STALE`.
- [ ] Write RED examples for currently underconstrained parameters/targeting/costs/roll requests.
- [ ] Implement minimal strict schemas.
- [ ] Ensure Activity parameter declarations constrain binding type/source/range before runtime accepts them.
- [ ] Verify that no embedded value becomes an independent semantic owner.
- [ ] Verify and publish checkpoint.

## Task 6 — Close registered Activity primitive operation contracts

**Files:**
- Create/modify: operation-contract machine catalog/schema artifacts under `DEV/CATALOG/` / `DEV/SCHEMAS/` as selected by evidence.
- Modify: `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`
- Test: focused operation compilation/execution-contract tests.

**Produces:** exact argument/result/read/mutation metadata for each supported `op.*`.

- [ ] Map every supported primitive to actual domain consumers and owner mutations.
- [ ] Remove/quarantine unneeded primitive IDs instead of designing hypothetical behavior.
- [ ] Define exact args/results/bindings/RNG/export/failure/suspension contracts.
- [ ] Define allowed mutation-owner classes and atomic segment expectations.
- [ ] Add compile-time rejection tests for unknown args, illegal owners and arbitrary query/code capabilities.
- [ ] Verify and publish checkpoint.

## Task 7 — Close character progression and READY_PC rules seed

**Files:**
- Modify: strict character definition schemas already introduced during WP-06.
- Modify: `DEV/SCHEMAS/world-actor-state.schema.json`
- Modify: relevant `DEV/CATALOG/entity-structures.json` entries.
- Modify: `GAME/CORE/CHARACTER_READINESS.md` / `ADVANCEMENT.md` only where S6D evidence exposes contract mismatch.
- Test: WP-04 + S6D character progression seed tests.

**Produces:** deterministic definition-owned choice inventory and reconstructable Actor selection state.

- [ ] Build representative initial-build and level-up seed cases across class/subclass/species/background/feat/spell choice patterns.
- [ ] RED-test stable `choice_id`/`option_id` validation and unresolved-choice READY_PC failure.
- [ ] Close grants/choices/prerequisites sufficiently for supported seed reconstruction without a flattened sheet owner.
- [ ] Prove deterministic/default/delegated initial choices cannot be opportunistically chosen after relevant situation exposure.
- [ ] Distinguish initial commitment frontier from genuine future advancement choices.
- [ ] Verify and publish checkpoint.

## Task 8 — Close HP/LifeState/Resource/Effect/Condition/temporal D&D seed

**Files:**
- Modify only owning architecture/catalog/schema artifacts exposed by seed gaps.
- Test: existing Step-2 examples plus S6D representative rules-seed matrix.

**Produces:** concrete rules cases demonstrating that accepted state ownership can realize the supported baseline.

- [ ] Enumerate representative seed cases for HP/temp HP/death/rest/recovery/resources/conditions/concentration/durations/periodic effects.
- [ ] For each case trace semantic owner -> selector/accessor -> Activity/primitive/boundary -> accepted mutation.
- [ ] RED-test any actual representation gap before changing schemas/catalogs.
- [ ] Extend scheduled-trigger/invocation-fact shapes only if a real supported case cannot be represented otherwise.
- [ ] Verify Long Rest and similar boundaries invoke owner-local responders rather than RestPolicy mutation authority.
- [ ] Verify no background scheduler or global scan is required.
- [ ] Publish/read-back checkpoint.

## Task 9 — Build the whole supported D&D domain coverage matrix

**Files:**
- Create: `DEV/docs/superpowers/research/2026-08-24-s6d-supported-rules-seed-coverage-matrix.md`
- Consume: CORE domain modules and all machine contracts closed above.

**Produces:** item-level domain coverage proof with one execution route per supported mechanic family.

- [ ] Cover checks/saves/contests, attacks/damage/healing/death, action economy/reactions, movement/targeting/areas, effects/conditions/concentration, spellcasting/resources, equipment, rests, advancement, hazards/exploration, social mechanics and supported economy/reward mechanics.
- [ ] For each item classify `FORMALIZED_DETERMINISTIC`, `BOUNDED_LLM_ADJUDICATED_INPUT_TO_DETERMINISTIC`, or `OUT_OF_MVP_SEED`.
- [ ] Preserve exact qualifiers; do not claim full D&D-book coverage beyond the supported public rules seed.
- [ ] Open a debt item for every unsupported-but-required case; do not hide it under prose adjudication.
- [ ] Publish/read-back checkpoint.

## Task 10 — Integrate Campaign Rulings / House Rules mechanical boundary

**Files:**
- Read: approved standalone Campaign Rulings / House Rules architecture artifact.
- Modify only S6D machine contracts that need explicit adjudicated parameter/binding support.

**Produces:** proof that nonformalizable LLM judgment can enter deterministic mechanics without becoming engine authority.

- [ ] Verify one-off adjudication/ruling inputs have declared typed receiving surfaces.
- [ ] Verify engine-owned HP/resources/capabilities/RNG cannot be supplied as ruling authority.
- [ ] Verify formalizable recurring mechanics have a typed Feature/Rule Element/Activity/policy path.
- [ ] Verify prose ruling policy cannot execute arbitrary mutation/code/query.
- [ ] If the House Rules architecture is not yet approved, stop this task as a dependency gate without guessing.

## Task 11 — Run integrated machine-contract and seed adversarial review

**Files:**
- Create: `DEV/docs/superpowers/specs/2026-08-24-s6d-integrated-adversarial-review.md`
- Update focused tests for every discovered defect before fixing it.

**Produces:** zero unresolved architecture blockers or an exact owner Decision Brief.

- [ ] Attack duplicate owners, selector gaps, untyped parameters, arbitrary query/code, LLM engine authority, hidden schedulers, dependency cycles, retry/RNG ambiguity, stale catalog IDs, nonreconstructable package identity and hot-path scale violations.
- [ ] Trace representative domain cases end-to-end through Step-3 execution.
- [ ] Check negative space: unsupported dormant features are not accidentally selectable.
- [ ] Run all locally/CI executable validation available through supported tooling; record exact evidence.
- [ ] If a real product/architecture trade-off remains, write a Decision Brief and stop for owner judgment.

## Task 12 — S6D canonical closure and R2.7 resume gate

**Files:**
- Create: `DEV/docs/superpowers/specs/2026-08-24-s6d-canonical-closure.md`
- Create: `DEV/docs/superpowers/specs/2026-08-24-s6d-resolution-gate.md`
- Update: `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`
- Update: `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md`

**Produces:** explicit permission to resume R2.7 WP-06.

- [ ] Reconcile every `S6D-Dxxx` item to final disposition/evidence.
- [ ] Verify every task-brief exit criterion.
- [ ] Fresh-read canonical machine artifacts and tests from remote branch.
- [ ] Write canonical closure and resolution gate with no completion claim unsupported by fresh evidence.
- [ ] Move roadmap from `S6D ACTIVE` to `S6D CLOSED; R2.7 WP-06 RESUMED` only after verification.
- [ ] Restore durable R2.7 cursor to the exact saved WP-06 point plus S6D results/forward obligations.
