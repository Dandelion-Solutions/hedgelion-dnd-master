# R2.7 WP-26 Step 6 — Documentation / Routing / Supersession Consistency — Whole-Project Adversarial Review

Status: **STEP 6 COMPLETE — FINDINGS REQUIRE TARGETED STEP-7 PROPAGATION / NO HUMAN DECISION REQUIRED**

Date: 2026-09-09

Scope: mandatory whole-project adversarial review of the Step-5 WP-26 candidate. This review treats the candidate as untrusted, reconstructs current owner/consumer routes independently, and attacks omission, stale-currentness, accidental authority creation, implementation smuggling and incomplete propagation.

## 1. Critic method

The critic did not ask only whether the Step-5 laws were internally consistent. It attacked whether a fresh future agent could still reach the wrong conclusion from another current-looking source or executable guard.

Attack classes:

```text
A. stale semantic owner / later amendment hidden
B. current router still points around the amendment
C. current runtime projection says something materially different
D. test/audit guard enforces old law
E. canonical status lies about current closure
F. Product Owner route sends work to a closed/future owner incorrectly
G. historical provenance is accidentally rewritten as current truth
H. accepted architecture is falsely presented as realized
I. deferred realization is accidentally pulled into WP-26
J. root README/editorial boundary is violated
K. version-bearing runtime edit lacks version-impact propagation
L. release/install mirrors retain stale law
```

All currentness-sensitive conclusions use exact-ref repository reads. Search-index results are not treated as current authority.

## 2. Independent attack results

### S6-26-01 — PO-009 baseline native-fallback leakage remains multi-source

Severity: **SIGNIFICANT**

The candidate correctly names PO-009, but closure requires more than a new canonical WP-26 law. Two current implementation-facing Story specifications still state the superseded baseline:

- producer/persistence/retrospective consumer contract allows baseline Commentator insufficiency to escalate to native `ACTOR_DECISION_BASIS`;
- baseline projection source contracts allow required T0 values to remain native-only behind navigation/reference.

A future planner could read either without the later owner and implement the wrong fallback.

Required Step-7 repair:

1. add explicit PO-009 targeted supersession/current-law note to both sources;
2. replace baseline Commentator/native-only T0 wording with Story-local support locality;
3. preserve native capability for Master/deep-source consumers;
4. do not invent schema fields.

Disposition: **OPEN / STEP-7 REPAIR**.

### S6-26-02 — PO-010 hard-cap leakage remains owner + Story + WP-24 + regression

Severity: **SIGNIFICANT**

The candidate correctly rejects the old hard cap, but four current-looking surfaces can still enforce/revive it:

- September-4 size owner decision;
- Story growth/sharding owner decision;
- WP-24 LAW WP24-13;
- `DEV/TESTS/PERFORMANCE_CASES.md` P13.

Required Step-7 repair:

- clearly mark the September-4 threshold law as superseded by PO-010 while retaining historical provenance;
- replace current Story/WP-24 exact hard cutoff with the current bands;
- update P13 to test preferred/review/partition expectations rather than `10241 => reject`;
- preserve exact UTF-8 measurement, no truncation and owner-valid partition/currentness.

Disposition: **OPEN / STEP-7 REPAIR**.

### S6-26-03 — readiness/lifecycle propagation set was underspecified

Severity: **SIGNIFICANT**

The Step-5 candidate said “current affected CORE projections” but exact-current attack found multiple stale phrases that must be explicitly included:

- `GAME/CORE/RUNTIME.md` equates `initializing` with pre-live and `active` with normal live play in one lifecycle section;
- `GAME/CORE/CAMPAIGN_SETUP.md` uses `pre-live vignette`, `first true live scene`, `begin true live play`, `Durable pre-live onboarding`, and similar first-live cutover language;
- `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` says first `true live scene` only after READY_PC;
- `GAME/CORE/SAVE_CONTRACT.md` uses `unfinished pre-live onboarding/setup` and `campaign is still pre-live`;
- `GAME/CORE/CORE_INDEX.md` describes `DIEGETIC_ONBOARDING` as `pre-live`, requires READY_PC before the `first true live scene`, and says missing durable mechanics are stored `before play`.

These conflict with current `CHARACTER_READINESS.md` / `DIEGETIC_ONBOARDING.md`, where bounded provisional onboarding is gameplay.

Required Step-7 repair: correct all five current CORE projections and bump their component/module revisions where version-bearing.

Disposition: **OPEN / STEP-7 REPAIR**.

### S6-26-04 — executable audit guard requires stale `pre-live` phrase

Severity: **SIGNIFICANT**

`DEV/TOOLS/audit_engine.py` currently requires `SAVE_CONTRACT.md` to contain either `unfinished pre-live setup` or `unfinished pre-live onboarding` as evidence that initializing lifecycle is preserved.

This is an executable false proxy. Once SAVE_CONTRACT is corrected, the audit would fail unless it too is reconciled.

Required Step-7 repair:

```text
assert unfinished pre-PLAY_READY/provisional onboarding save remains initializing
without requiring the phrase pre-live
```

Retain paused/post-PLAY_READY checks.

Disposition: **OPEN / STEP-7 REPAIR**.

### S6-26-05 — regression prose still creates a false first-play gate

Severity: **SIGNIFICANT**

Current regression cases include stale play-boundary wording:

- `DEV/TESTS/CHARACTER_READINESS_CASES.md` describes the READY_PC contract as used before entering live D&D play and contains a `fails closed before play` case that is too broad;
- `DEV/TESTS/EXPLICIT_SAVE_CASES.md` labels save during `pre-live onboarding`;
- `DEV/TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md` contains `before first live scene` lifecycle language.

The cases already contain some correct provisional-play behavior, which makes the corpus internally contradictory.

Required Step-7 repair: rewrite only the stale boundary wording to distinguish provisional gameplay from full-active/post-PLAY_READY gameplay. Do not weaken exact mechanic blockers.

Disposition: **OPEN / STEP-7 REPAIR**.

### S6-26-06 — closed canonical status headers still claim pending review

Severity: **SIGNIFICANT**

Exact current reads confirm:

- WP-21 canonical spec header: final Senior pending;
- WP-22 canonical spec header: final Senior pending;
- WP-24 canonical spec header: final Senior pending.

`DEV/CURRENT_PROGRESS.md` records all three closed after final Senior PASS.

Required Step-7 repair: update current canonical status/header/intro only. Do not rewrite historical Step/review artifacts.

Disposition: **OPEN / STEP-7 REPAIR**.

### S6-26-07 — derivative routing can still bypass PO-009/PO-010

Severity: **SIGNIFICANT**

`DEV/PROJECT_MAP.md` Story route lists older Story and size sources but lacks direct PO-009/PO-010 current-owner routing. `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` likewise requires current locators.

Required Step-7 repair:

- add PO-009/PO-010 current owner/amendment routes;
- after Step 8, add final WP-26 canonical owner;
- preserve explicit non-normative locator status.

Disposition: **OPEN / STEP-7 REPAIR**.

### S6-26-08 — Product Owner ledger route aging survives closed WP-24

Severity: **SIGNIFICANT**

PO-006 agent-owned routing still says retained-ref operational cost is a future consumer `when WP-24 opens`. WP-24 is already closed and consumed the prohibition/operational boundary.

Required Step-7 repair:

- mark that WP-24 consumer incorporated/closed;
- route future realized measurement/planning through current proof/planning owners where applicable;
- preserve deletion prohibition unchanged;
- edit only agent-owned routing/current-impact prose, never the verbatim PO quotation.

Disposition: **OPEN / STEP-7 REPAIR**.

### S6-26-09 — accepted PO-009/010 architecture can be mistaken for machine completion

Severity: **SIGNIFICANT**

The opposite failure is also possible: after repairing docs/tests, a future reader may infer that PO-009 Story schema/control projection and PO-010 concrete writer partition topology now exist.

Current exact evidence does not support that claim:

- current `GAME/SCHEMA/event.schema.yaml` has no selected PO-009-specific representation;
- PO-009 deliberately leaves concrete schema/cache topology for later implementation design;
- PO-010 deliberately leaves concrete physical writer partition topology owner-specific/deferred.

Required Step-7/8 propagation:

```text
architecture decision = accepted/incorporated
machine realization = explicitly deferred where representation is not selected
```

This must be visible in final canonical WP-26 + routers/WP-27 handoff.

Disposition: **OPEN / STEP-7/8 PROPAGATION**.

### S6-26-10 — focused machine regression is missing

Severity: **SIGNIFICANT**

The current suite has general routing tests, but none directly protects the full WP-26 supersession surface as one currentness contract. Without a focused guard, later edits can reintroduce:

- hard `10240` rejection;
- future-WP24 PO-006 route;
- native-only baseline Commentator T0 fallback;
- stale canonical closure headers;
- `pre-live` audit proxy.

Required Step-7 repair: add a focused WP-26 routing/supersession regression test over current sources. It must test only mechanically fixed current-law/routing invariants and must not assert deferred PO-009/010 machine representation as already implemented.

Disposition: **OPEN / STEP-7 REPAIR**.

### S6-26-11 — release/install surfaces do not add a new stale-law obligation

Severity: **NEGATIVE FINDING / CLOSED**

Exact-current review of `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` found no READY_PC `pre-live` cutoff or 10 KiB hard-cap law. It delegates detailed runtime semantics to selected CORE.

`GAME/INSTALL/00_DND_BOOTSTRAP.md` uses `initializing` menu label `unfinished setup` but does not establish that no provisional gameplay can occur before PLAY_READY. No new install/bootstrap semantic repair is proven from the inspected surface.

Disposition: **NO REPAIR**.

### S6-26-12 — root README mismatch remains report-only

Severity: **MINOR**

Known mismatch:

```text
README: DEV/TOOLS/run_release_build
canonical path: DEV/TOOLS/run_release_build.py
```

Root README editing remains outside current authorization.

Disposition: **REPORT ONLY**.

## 3. Architecture-overreach attacks

### Attack: make Story canonical because it must be self-contained

Rejected. Self-contained support locality does not change gameplay authority.

### Attack: remove native `ACTOR_DECISION_BASIS` capability globally

Rejected. PO-009 narrows baseline Commentator fallback only.

### Attack: select concrete Story eligibility schema now

Rejected. This is deferred representation and would be implementation/design smuggling.

### Attack: replace 10 KiB with a new universal 16 KiB hard cap

Rejected. PO-010 defines decision bands, not a new exact validity cutoff.

### Attack: let oversized files grow without review because there is no hard cap

Rejected. >~16 KiB is a default review/partition/rollover expectation and retained operability/currentness constraints still apply.

### Attack: make READY_PC irrelevant because provisional gameplay exists

Rejected. READY_PC remains the full-active/unrestricted mechanics frontier and exact missing mechanic blockers remain fail-closed.

### Attack: add a lifecycle `provisional_play` state

Rejected. Current lifecycle states are sufficient; only interpretation vocabulary is stale.

### Attack: rewrite all historical docs

Rejected. Historical provenance remains history; only current-looking authority/routing/realization is reconciled.

### Attack: introduce a global supersession registry

Rejected. Existing owner-first routing is sufficient.

## 4. Version-impact attack

Current affected CORE set proven by exact-current semantics:

```text
GAME/CORE/RUNTIME.md
GAME/CORE/CAMPAIGN_SETUP.md
GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md
GAME/CORE/SAVE_CONTRACT.md
GAME/CORE/CORE_INDEX.md
```

All carry `framework_module_version` metadata. Step-7 semantic wording corrections therefore require patch-level component revisions.

No persistent schema/generation change is authorized or required by WP-26 itself.

Expected:

```text
ENGINE_VERSION_BUMP_REQUIRED: NO
MODULE_PATCH_REVISIONS_REQUIRED: YES — five CORE modules
PERSISTENT_SCHEMA_OR_GENERATION_BUMP_REQUIRED: NO
MIGRATION_REQUIRED: NO
```

## 5. Finding summary

```text
STEP6_BLOCKING_FOUND: 0
STEP6_SIGNIFICANT_FOUND: 10
STEP6_MINOR_FOUND: 1
NEGATIVE_FINDINGS_RECORDED: YES
HUMAN_DECISION_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
WHOLESALE_UPSTREAM_REOPEN_REQUIRED: NO
```

The ten SIGNIFICANT findings are not ten new architecture decisions. They are propagation/current-realization obligations derived from already accepted law.

## 6. Mandatory Step-7 propagation checklist

Every SIGNIFICANT finding must be closed explicitly:

```text
S6-26-01 -> Story producer + baseline projection current specs
S6-26-02 -> old size owner + Story growth owner + WP-24 + PERFORMANCE_CASES
S6-26-03 -> RUNTIME + CAMPAIGN_SETUP + NEW_CAMPAIGN_FAST_PATH + SAVE_CONTRACT + CORE_INDEX
S6-26-04 -> audit_engine.py
S6-26-05 -> readiness/save/bootstrap regression prose
S6-26-06 -> WP-21 + WP-22 + WP-24 canonical headers
S6-26-07 -> PROJECT_MAP + CANONICAL_ARCHITECTURE_INDEX
S6-26-08 -> PRODUCT_OWNER_INPUT PO-006 routing/current impact
S6-26-09 -> final WP-26 canonical + explicit WP-27 realization handoff
S6-26-10 -> focused WP-26 regression test
```

Minor:

```text
S6-26-12 -> final report only; no README write
```

## 7. Step-6 gate

```text
STEP6: COMPLETE
UNRESOLVED_BLOCKING_BEFORE_STEP7: 0
UNRESOLVED_SIGNIFICANT_BEFORE_STEP7: 10
HUMAN_DECISION_REQUIRED: NO
NEXT_STEP: Step 7 finding resolution + propagation
```
