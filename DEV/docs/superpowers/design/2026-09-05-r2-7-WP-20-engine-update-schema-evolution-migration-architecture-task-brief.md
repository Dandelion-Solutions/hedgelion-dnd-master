# R2.7 WP-20 — Engine Update / Schema Evolution / Migration — Architecture Task Brief

Status: **STEP 1 COMPLETE — MANDATORY SENIOR REVIEW**

Date: 2026-09-05

Source Manifest:
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-source-manifest.md`

Mandatory Task-Brief critic:
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-task-brief-critic.md`

## 1. Problem statement

WP-20 must determine the final architecture for **safe evolution of campaigns created under released HDM v1.0+ versions** when a later released runtime changes engine capability, ruleset identity, persistent schemas, storage formats, or another persistent interpretation contract.

The problem is broader than `GAME/MIGRATIONS/` and broader than semantic `engine_version`. A released campaign is interpreted through several existing independent identities and authorities. WP-20 must determine when a candidate runtime can consume current campaign state unchanged, when an explicit transformation/adoption is required, when no supported path exists, how a valid path is selected, and how authority changes safely without losing canon, stable identity, accepted historical interpretation, recovery evidence, currentness or multiplayer/LIVE ownership.

The current repository contains update/migration prose, version fields, schemas, tests and a migration directory. They are evidence and consumers, not presumed correct architecture.

## 2. Controlling compatibility horizon — PO-004

The Product Owner decision in `DEV/docs/superpowers/specs/2026-09-05-hdm-v1-clean-slate-compatibility-owner-decision.md` is controlling:

```text
PRE-RELEASE / 0.8 COMPATIBILITY
    -> OUT OF REQUIRED COMPATIBILITY SURFACE

RELEASED v1.0+ EVOLUTION
    -> CURRENT WP-20 ARCHITECTURE PROBLEM
```

Therefore:

- no v0.8→v1.0 migration is required;
- no dual reader/writer, adapter, rollback path, retained legacy layout, compatibility shim or obsolete schema is required solely for pre-release state;
- old scaffold/schema/migration/test artifacts gain no preservation right because they exist;
- clean-slate authority does **not** permit ignoring safe future evolution of campaigns created under released v1.0+ versions.

PO-004 remains `PARTIALLY_INCORPORATED` because WP-20 architecture is not yet complete. Step 1 exposes no open Product Owner decision.

## 3. Goals

WP-20 research/design must produce an architecture that makes all of these explicit and testable:

1. the exact identity/evidence needed to decide whether a released campaign can run under a candidate runtime;
2. compatibility classes including at least unchanged/no-transform use, migration-required use, and unsupported/incompatible state;
3. the relation among engine, exact runtime package, ruleset set/compatibility, persistent schema identities and storage-format identities;
4. deterministic migration-path selection and ordering/dependency rules;
5. the policy for forward, backward and other directionality, derived from evidence rather than assumed;
6. semantic invariants across migration: stable native IDs, authority/ownership, canon, accepted execution, history/chronology, currentness, recovery and authorization;
7. update/migration authorization and execution authority;
8. one safe authority-changing publication boundary with stale-head/concurrency handling;
9. explicit handling of partial local success, publication rejection and indeterminate publication outcome;
10. multiplayer/LIVE interaction and any required quiescence/absorption/blocking semantics;
11. exact-runtime and exact-migration-implementation availability/failure behavior;
12. older-runtime rejection behavior for unsupported newer campaign state;
13. rollback semantics only to the extent actually supportable/required;
14. architecture→machine and machine→architecture mappings sufficient to drive later realization/testing without making current implementation authoritative.

## 4. Non-goals / hard boundaries

WP-20 Step 1 and the later WP-20 architecture do not by default own:

- pre-release/v0.8 compatibility;
- creation/New Game materialization already closed by WP-19;
- redefinition of engine package build/release provenance unless WP-20 proves an insufficient consumer contract;
- redefinition of ruleset-package identity where current owner is sufficient;
- a new persistence/publication authority replacing WP-13;
- a new checkpoint/recovery owner replacing WP-14;
- a new semantic chronology owner replacing WP-15;
- a new access/LIVE authority replacing WP-16;
- implementation code, schemas, migration scripts or test fixes during architecture work;
- WP-21+ execution;
- implementation planning.

This Step-1 assignment specifically does not authorize any actual migration or real campaign mutation.

## 5. Established constraints and inherited owners

### 5.1 Existing campaign runtime identity

WP-19 and current runtime selection establish that an existing campaign resolves from `MANIFEST.engine.current`, not storage baseline, current public branch/tag, `main`, or “latest”. `DND_STORAGE.engine.baseline` is NEW-campaign-only.

Current exact package identity/provenance includes several independent axes. Candidate classification must not collapse them into one scalar.

### 5.2 Non-equivalent compatibility axes

`DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` already establishes that these are not interchangeable:

```text
engine_version
catalog_generation
runtime package_id / source provenance
runtime ZIP SHA-256
ruleset package_version
ruleset compatibility_id
ruleset content_sha256
ruleset_set_sha256
catalog_context_fingerprint
```

Persistent campaign/storage/schema/format identities add further independent compatibility axes. Open accepted work may also depend on exact compatible interpretation context.

The research must determine the **minimum sufficient compatibility envelope**; it must not create one universal version merely for convenience.

### 5.3 Same-version refresh is already partly settled

Current package/ruleset owners admit a narrowly proven same-engine-version forward refresh when exact provenance and strict monotonic semantic compatibility prove it safe. Changed digest alone neither means “migration” nor means “compatible”.

WP-20 must preserve that accepted distinction unless evidence demonstrates insufficiency. Topic overlap is not permission to reopen it.

### 5.4 Publication/currentness law is inherited

Existing-campaign authoritative publication remains base-tree derived, pinned to one current HEAD, non-force, and CAS/currentness guarded. The final authority-changing ref outcome has `CONFIRMED_ACCEPTED`, `CONFIRMED_REJECTED`, or `INDETERMINATE` epistemics.

A transformed local tree is not migrated campaign authority until the applicable final publication edge is confirmed accepted.

### 5.5 Stable semantic identity and accepted interpretation are preserved

A representation/schema transformation cannot use SQL row IDs, path order, timestamps, regenerated IDs or new runtime mechanics to silently replace existing semantic identity.

Accepted open execution cannot be rerolled/replayed/reallocated or reinterpreted through arbitrary newer mechanics. Missing required interpretation evidence is a compatibility failure, not permission to guess.

### 5.6 Checkpoint is not rollback authority

Checkpoint is optional descriptor/evidence and may assist risky maintenance, but it is not current authority, a RecoveryCut, guaranteed rewind slot or generic rollback mechanism. A rollback promise must therefore be justified by retained exact old state/runtime/path capability, not inferred from checkpoint existence.

### 5.7 LIVE/multiplayer authority remains independent

Campaign currentness, selected LIVE currentness and local HOT currentness are distinct. An ACTIVE or CLOSED-unabsorbed selected LIVE source remains current truth for its claims; campaign base cannot become fallback truth simply because migration wants one tree.

Migration must not bypass LIVE exact-source CAS or campaign authorization/routing authority.

### 5.8 Derived state stays derived

SQLite/HOT helper state, indexes, caches, Agenda/query projections and other derived structures do not become migration authority. Architecture must distinguish:

```text
native semantic persistent transformation
vs
non-authoritative derived invalidation/rebuild
```

## 6. Compatibility model questions Step 2 must answer

### Q20-01 — Exact campaign compatibility identity

What exact finite identity/evidence tuple determines whether current released campaign state is consumable by a candidate runtime?

The answer must distinguish at least:
- engine semantic/capability identity;
- exact runtime package/provenance where material;
- ruleset exact identity and declared compatibility line;
- schema identity per persistent owner/family where material;
- storage-format identity;
- accepted-open-work interpretation dependencies;
- any migration-format/protocol identity genuinely required.

### Q20-02 — Compatibility classes

Which changes are:

```text
COMPATIBLE_WITHOUT_PERSISTENT_TRANSFORMATION
MAINTENANCE_OR_REFRESH_WITHOUT_SEMANTIC_MIGRATION
MIGRATION_REQUIRED
UNSUPPORTED_OR_INCOMPATIBLE
INDETERMINATE / INSUFFICIENT_EVIDENCE
```

Exact names may differ, but architecture must not silently turn unknown into compatible or silently assume every maintenance-required state is migratable.

### Q20-03 — Engine/ruleset/schema/storage relation

How do engine version/capability, runtime package identity, ruleset set/compatibility, individual persistent schemas and storage format constrain one another without creating duplicate version authority?

Does the current coarse `campaign_update.compatibility` remain only a release-level hint/gate, participate in exact edge selection, or require a superseding bounded contract?

### Q20-04 — Deterministic migration graph/path

How is one valid path selected when more than one migration edge could exist?

Research must establish:
- exact source/target predicates;
- immutable identity/provenance of migration implementations;
- ordering and dependencies;
- ambiguity/cycle/gap behavior;
- whether composition of several edges is legal;
- whether path selection depends on target runtime package, package-contained migration metadata, or another admitted immutable owner;
- why mutable tags/current `main`/latest cannot select the path.

### Q20-05 — Directionality

Is released migration monotonic/forward-only, and if so on which ordered axis? If current evidence requires backward or lateral transformations, what exact semantics justify them?

Do not infer direction from lexical version strings, source timestamps, SHA magnitude or `adopted_at`.

### Q20-06 — Semantic preservation

What exactly must remain semantically identical through migration?

At minimum examine:
- campaign ID and creator provenance;
- stable PLAYER/PC/native owner IDs and bindings;
- native owner authority and lifecycle;
- accepted execution identity/RNG/Continuation/receipts;
- facts/knowledge/disclosure authority;
- history/SemanticEvent/chronology evidence;
- currentness/routing and LIVE claims;
- recovery dependencies and retained exact interpretation context;
- House Rules/campaign-local definitions;
- provenance required to explain the migrated state.

### Q20-07 — Authorization

Who may authorize and who may technically execute released-campaign migration?

The current source graph must reconcile:
- creator-only explicit engine/ruleset adoption and persistence wording;
- the older/broader `ACCESS_CONTROL.md` sentence describing campaign engine maintenance as storage-owner maintenance;
- storage-owner-only `DND_STORAGE.engine.baseline` maintenance;
- multiplayer PLAYER authority and any decisions that must remain player/creator-owned.

The result must separate storage baseline maintenance from mutation of an existing campaign and must fail closed when required principal/authority cannot be established.

### Q20-08 — Atomic authority-changing boundary

What must be frozen before transformation/publication, what can be computed locally, and which exact final publication edge changes campaign authority?

The architecture must compose with WP-13 rather than add a migration-specific force/update channel.

### Q20-09 — Local transform succeeded, publication failed

What state is authoritative when target-form data was produced locally but the ref transition is confirmed rejected? What may be safely retained as scratch/evidence, what must be rebuilt after repin, and what may not be announced as success?

### Q20-10 — Indeterminate publication

When the authority-changing publication outcome is indeterminate, what bounded verification resolves whether migration committed? No blind retry, force push, alternate transport or guessed rollback may create duplicate/contradictory authority.

### Q20-11 — Stale HEAD / concurrent activity

What happens if campaign HEAD, authorization dependencies, selected LIVE routing or relevant owner state moves after migration preparation?

Research must distinguish:
- disjoint movement that may permit rebase/rebuild;
- overlapping semantic movement requiring revalidation/retransform;
- ACTIVE/CLOSED-unabsorbed LIVE ownership that blocks or requires forward absorption/transfer;
- ordinary player activity that cannot be silently lost.

### Q20-12 — Exact runtime/migration unavailable

What happens when the campaign requires an exact old runtime/interpretation set or migration implementation that is absent from the current Project/cache/package set?

Architecture must define finite restore/add-package/update/unsupported outcomes without fetching mutable `main`, borrowing sibling runtime files, fuzzy matching or guessing.

### Q20-13 — Older runtime encounters newer state

Can an older runtime prove support for the newer campaign representation? If not, it must reject safely rather than interpret unknown fields/versions optimistically. Define how failure is recognized and presented without pretending corruption/recovery authority.

### Q20-14 — Rollback

Which rollback semantics are genuinely required and mechanically supportable?

Investigate separately:
- abort before authority-changing publication;
- recovery after confirmed rejection;
- resolution after indeterminate publication;
- later intentional downgrade/reverse migration, if any;
- access to exact old runtime/ruleset/migration implementation and retained old representation.

A checkpoint alone is not sufficient evidence for rollback support.

### Q20-15 — Derived/index/HOT effects

For each migrated native owner/path, which indexes/projections must change atomically with campaign publication, and which local/derived structures should simply be invalidated/rebuilt after adoption?

### Q20-16 — Machine surface insufficiency/staleness

Which current runtime/schema/migration/tool/test surfaces are current-owner-backed, insufficient, stale, obsolete due PO-004, or realization-only?

Known Step-1 challenge points include:
- `GAME/MIGRATIONS/README.md` as a thin non-owning scaffold;
- legacy nested `CAMPAIGN/` bootstrap fallback as non-binding pre-release compatibility;
- `ENGINE_UPDATE_CASES.md` U17 legacy-layout preservation as non-binding under PO-004;
- stale test vocabulary/paths such as U04/U06/U08;
- coarse release `campaign_update.compatibility` metadata;
- current MANIFEST/schema fields that may not be enough to encode all persistent owner format identities.

### Q20-17 — Architecture vs later realization

Which missing semantics must WP-20 settle canonically, and which are downstream realization details for later implementation/WP-22/23/26?

Architecture cannot defer questions of compatibility classification, migration authority, semantic preservation, failure epistemics or path-selection safety as “implementation detail”. Conversely, exact Python APIs, concrete DDL, file-writing loops and test code should not become architecture unless they encode a material invariant.

## 7. Evidence/research execution required for Step 2

Step 2, after Senior GO, must:

1. expand this manifest into item-level evidence for every implicated persistent owner family and format/schema identity;
2. map WP-10 durable families through WP-11 exact physical routes and current schemas/templates;
3. inspect current engine/ruleset package machine contracts and release metadata to determine what immutable compatibility/migration evidence can be shipped/resolved;
4. trace accepted execution/recovery dependencies that can survive across an update;
5. reconstruct authorization and LIVE/currentness transitions from current owners;
6. reverse-audit current migration/update/bootstrap/version/schema/test surfaces and classify each material responsibility;
7. use concrete failure scenarios: stale HEAD, active LIVE, missing exact runtime, missing migration edge, ambiguous path, local-success/publication-failure, indeterminate CAS, older-runtime/newer-state, open accepted procedure, corrupt/missing derived indexes;
8. compare the simplest viable design against richer migration-registry/graph/rollback mechanisms and apply YAGNI;
9. preserve PO-004 clean-slate boundary throughout the analysis;
10. stop and escalate only if a residual decision genuinely belongs to Product Owner/human architecture judgment after the evidence is exhausted.

External research is not currently required to frame Step 2; repository owners and machine consumers are the first evidence tier. If Step 2 exposes a technology/format/tool limitation not answerable from project sources, use official/primary external sources narrowly.

## 8. Quality attributes

The alternatives must be judged primarily on:

- correctness / no silent reinterpretation;
- deterministic compatibility/path selection;
- authority and stable-ID preservation;
- crash/currentness safety;
- recoverability and finite failure;
- multiplayer/agency safety;
- provenance/auditability;
- bounded runtime/repository work;
- testability;
- maintainability without speculative universal migration infrastructure;
- release/package reproducibility.

Do not invent numerical performance targets. Ordinary gameplay must not gain migration checks or remote work unrelated to an actual startup/update/migration boundary.

## 9. Architecture ↔ machine audit requirement

### Architecture → machine

For every accepted final WP-20 law, later canonicalization must identify its machine destination(s), as applicable:

```text
runtime/update instruction
runtime package/release metadata
campaign/storage/persistent schema identity
migration package/tool contract
publication/recovery/live integration
schema/template migration target
validation/failure contract
tests/audit/release checks
```

### Machine → architecture

For every material current responsibility found in:

```text
ENGINE_UPDATES / bootstrap
ENGINE_VERSION / RUNTIME_PACKAGE / release tooling
MANIFEST / DND_STORAGE / persistent schemas/templates
MIGRATIONS
ruleset package metadata/locks
migration/update tests
persistence/recovery/live consumers
```

identify one accepted owner, or classify it explicitly as `DERIVED`, `IMPLEMENTATION-ONLY`, `STALE`, `OBSOLETE PRE-RELEASE`, `HISTORICAL`, or `DEBT`.

No machine surface earns semantic authority from existence.

## 10. Step-1 exit criteria

Step 1 is complete only if:

- Source Manifest covers the direct/indirect dependency graph needed to frame WP-20;
- PO-004 is controlling and pre-release compatibility is excluded;
- the Brief makes every required migration/compatibility/authority/failure question answerable;
- architecture vs realization boundaries are explicit;
- whole-project critic independently attacks the framing;
- every BLOCKING/SIGNIFICANT framing defect is repaired or escalated as genuine `NEEDS_PO`;
- Step 2 remains unauthorized pending Senior review.

Current result after critic repairs:

```text
WP20_STEP1: COMPLETE — MANDATORY SENIOR REVIEW
SOURCE_MANIFEST: COMPLETE
ARCHITECTURE_TASK_BRIEF: COMPLETE
TASK_BRIEF_CRITIC: COMPLETE

UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE

WP20_STEP2_AUTHORIZED: NO
WP20_STEP2_STARTED: NO
WP21_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
RUNTIME_MIGRATION_EXECUTED: NO
REAL_CAMPAIGN_MIGRATED: NO

NEXT_AUTHORIZED_UNIT: NONE — MANDATORY SENIOR REVIEW
```
