# R2.7 WP-23 — Release / Package / Version / Legal Readiness — Canonical Specification

Status: **CANONICAL IMPLEMENTATION-FACING ARCHITECTURE — FINAL SENIOR RE-REVIEW PASS / WP-23 CLOSED**

Date: 2026-09-08

This specification is the single current implementation-facing WP-23 architecture owner produced by the approved Step-1 framing, Steps 2–8 and the targeted repair of final-Senior finding `SR23-FINAL-01`. It composes existing owners rather than replacing their native semantics. The mandatory independent final Senior re-review accepted the targeted repair; WP-23 is closed.

This specification does **not** authorize or claim:

- a real release, tag, GitHub Release, asset upload or deployment;
- production release readiness;
- implementation planning or substantive runtime implementation;
- campaign migration or gameplay/campaign bootstrap;
- WP-24;
- a new licensing policy;
- a new release/currentness/compatibility authority.

## 1. Design and authority chain

Process / design artifacts:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-task-brief-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-step-1-whole-project-critic.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-step-1-senior-review.md` — `PASS / GO`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-step-2-evidence-reconciliation.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-step-3-decision-brief.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-step-4-cross-system-review.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-step-5-candidate-specification.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-step-6-whole-project-adversarial-review.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-step-7-finding-resolution-propagation.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-step-8-canonicalization-checkpoint.md`.

Product Owner provenance boundary:

- `DEV/docs/superpowers/specs/2026-09-08-hdm-public-research-provenance-attribution-owner-decision.md`.

Version/update/migration composition remains owned by:

- `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md`;
- current HDM versioning policy and publication/currentness amendments.

Package/build/install/release realization remains owned by the current release builder, workflows, `DEV/RELEASE/`, `GAME/ENGINE_VERSION.yaml`, `GAME/INSTALL/`, `GAME/CORE/ENGINE_UPDATES.md`, legal payload and their tests/checks.

`DEV/RELEASE/CHECKLIST.md` remains the current release-owner checklist and explicitly requires the two fresh-Project acceptance boundaries restored below.

## 2. One coupled release-readiness chain

WP-23 remains one coupled work package across package/install, version/update/release, and legal/provenance concerns. The current release-readiness sequence is:

```text
final version-coherent source tree
-> build/validation evidence
-> pre-tag candidate artifact
-> fresh-Project acceptance of that pre-tag candidate
-> immutable release tag / tag-triggered publication
-> exact uploaded runtime asset + checksum/provenance verification
-> fresh-Project acceptance of the exact uploaded asset
-> release may be announced when all applicable release-owner obligations pass
```

This sequence composes, rather than replaces, the existing package/install/version/update/legal owners.

The two fresh-Project checks are **temporally and evidentially distinct acceptance boundaries**:

- the first is evidence about the pre-tag candidate produced from the final version-coherent tree before immutable tagging;
- the second is evidence about the exact uploaded runtime asset after tag-triggered publication and exact uploaded-asset identity/checksum/provenance verification.

The architecture does **not** require those two checks to use different physical Project instances. It requires separate evidence tied to the two distinct artifact/publication boundaries.

Current exact-head source CI/build verification satisfies neither empirical fresh-Project gate.

No intermediate node has the proof power of a later node.

Normative non-equivalences:

```text
SUCCESSFUL_ZIP_BUILD != PRE_TAG_FRESH_PROJECT_ACCEPTANCE
GREEN_SOURCE_CI != PRE_TAG_FRESH_PROJECT_ACCEPTANCE
PRE_TAG_FRESH_PROJECT_ACCEPTANCE != IMMUTABLE_TAG_PUBLICATION
IMMUTABLE_TAG_PUBLICATION != EXACT_UPLOADED_ASSET_VERIFICATION
EXACT_UPLOADED_ASSET_VERIFICATION != POST_UPLOAD_FRESH_PROJECT_ACCEPTANCE
PRE_TAG_FRESH_PROJECT_ACCEPTANCE != POST_UPLOAD_FRESH_PROJECT_ACCEPTANCE
GREEN_SOURCE_CI != PUBLISHED_RELEASE_ACCEPTANCE
SEMANTIC_VERSION != EXACT_PACKAGE_PROVENANCE
EXACT_PACKAGE_PROVENANCE != FINAL_ARCHIVE_DIGEST
SOURCE_COMMIT_ANCESTRY != ARTIFACT_IDENTITY
TAG/RELEASE_METADATA != PACKAGE-CARRIED_IDENTITY
```

WP-23 creates no universal readiness registry, scalar release epoch, compatibility database or second currentness owner.

## 3. Package and installation integrity

### WP23-A01 — `GAME/` is the shipped source boundary

All valid current runtime source under `GAME/` is release-facing. `DEV/` is development-only and must not be injected into the runtime package.

The builder may continue open-world recursive `GAME/` passthrough rather than maintaining an ordinary-file include list. Consequently, every future valid `GAME/` file is automatically a package/install/legal/public-provenance consumer.

### WP23-A02 — package root is flat and exact

An installable runtime ZIP exposes `ENGINE_VERSION.yaml`, generated `RUNTIME_PACKAGE.yaml` and required runtime directories at package root. Repository wrappers such as `GAME/` and `DEV/` are invalid runtime-package shape.

GitHub-generated source-code archives are source snapshots, not runtime installation artifacts.

Once selected, all runtime-relative reads remain bound to one exact validated runtime root. Sibling package roots are never merged or borrowed from.

### WP23-A03 — source/build evidence is bounded

Current build/integration realization may prove:

- source manifest consistency;
- reproducible runtime ZIP construction;
- flat package shape;
- generated package provenance;
- legal-copy parity;
- checksum emission;
- packaged campaign-generator smoke behavior.

Those proofs do not satisfy either fresh-Project acceptance gate and do not establish that an actual Release exists.

## 4. Release, package and version identity

### WP23-B01 — semantic release identity

`GAME/ENGINE_VERSION.yaml` is the shipped semantic engine/release contract. Shared DEV/GAME release fields remain synchronized; development-only revision bookkeeping does not leak into the shipped semantic manifest.

### WP23-B02 — exact built-package provenance

Generated root `RUNTIME_PACKAGE.yaml` identifies the exact built package source/provenance under its current schema. It is not a second semantic version owner.

### WP23-B03 — final archive digest

The final runtime ZIP SHA-256 identifies exact archive bytes. It is external to the ZIP and cannot be substituted by semantic version, package ID, tag spelling or source ancestry.

### WP23-B04 — independent version namespaces remain independent

Engine release, engine-bound module version, persistent/protocol schema version, campaign/storage generation, catalog generation, ruleset package/compatibility generation and exact artifact digest retain their own owners and meanings.

Cross-namespace equality/order has no compatibility meaning. Same generation may create eligibility for an owner-specific check but does not prove compatibility.

## 5. Update / migration composition and WP-20 boundary

WP-23 consumes WP-20 released-v1.0+ compatibility/migration architecture without redefining it.

The absence of migration-edge/transform machine realization before a concrete released-v1.0+ source/target obligation is not a current prerelease defect when the owning activation trigger has not occurred.

WP-20 may be reopened only if current evidence demonstrates at least one of:

- contradiction with the accepted owner;
- an unsatisfied current consumer;
- insufficiency of the accepted owner for the current problem.

Thematic overlap is insufficient. WP-23 found none of those reopen conditions.

Unsupported or indeterminate compatibility fails closed. Semantic version order, schema/generation adjacency, tag order and Git ancestry never manufacture compatibility or a migration path.

```text
WP20_REOPEN_REQUIRED: NO
```

## 6. Public legal and provenance boundary

The current public `DEV/` + `GAME/` tree is classified by function, not path, age or file taxonomy.

### WP23-C01 — prohibited public development/research provenance

Current public material must not retain source-specific development/research narrative whose purpose is to record which outside sites, authors, projects, products, articles, studies or analogous sources were consulted, compared, adopted, rejected or used as design inspiration/evidence.

Public HDM semantics are independently stated in HDM terminology.

Historical/research/design/test placement provides no exemption. Current-tree retirement does not rewrite Git history.

### WP23-C02 — required legal / approved attribution is preserved

Mandatory license/legal attribution and separately explicit Product-Owner-approved attribution remain required where their owners require them. Public-provenance sanitation must not remove them.

Current legal/release payload includes the root/runtime `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md` and `LICENSES/` surfaces under their existing owners and release validation.

### WP23-C03 — HDM technical artifact provenance is preserved

Technical artifact provenance is not prohibited development/research provenance. Where current owners require it, preserve applicable:

- exact source/commit SHA;
- release/tag identity;
- generated `RUNTIME_PACKAGE.yaml` provenance;
- final hashes/digests;
- version/generation identity;
- ruleset-set identity;
- migration/update lineage;
- deterministic publication/currentness evidence.

### WP23-C04 — operational facts are functionally classified

An external name/reference may remain when it is a current operational, product, transport, rules-source or legal fact rather than a development-source trail.

Therefore no global external-name/URL blacklist is provenance authority.

### WP23-C05 — internal/source-neutral research may remain

Internal HDM experiments, project-owner reconciliation, machine inventories and independently stated source-neutral HDM evidence may remain. A `research/` path is neither automatic permission nor automatic prohibition.

## 7. Sanitation / retirement law

When one artifact mixes useful HDM semantics with prohibited source history:

1. preserve/rehome the HDM-owned conclusions, exclusions, negative requirements, technical evidence and applicable revisit/defer triggers;
2. remove the source-specific development narrative;
3. reconcile live routing/check/test consumers in the same coherent repair.

A source-history file may be retired from the current tree when all material current HDM conclusions are already owned elsewhere and no unique current trigger/evidence depends on the file. Git history remains unchanged.

Historical external implementation preferences do not constrain future implementation. Tool/library/component selection belongs to authorized implementation planning against current HDM contracts and licensing requirements.

## 8. Current architecture-stage realization

At targeted-repair canonicalization, the current tree realizes the following WP-23 consistency repairs:

- `GAME/CORE/SOURCES.md` is an HDM-native runtime source/provenance boundary rather than a development-research bibliography;
- `DEV/ARCHITECTURE/ASSET_MODEL.md`, `ACTIVITY_MODEL.md` and `ENTITY_STRUCTURES.md` retain their HDM semantics without development-source basis sections;
- historical `CRITICAL_ARCHITECTURE_AUDIT.md`, `MECHANICAL_RUNTIME_PROPOSAL.md` and `DEV/TESTS/PRE_RELEASE_AUDIT_0.1.0.md` retain useful HDM conclusions/history in source-neutral form;
- four source-history platform/economic research files are retired from the current public tree;
- the repository-port transport source-history spike is retired because current publication/currentness law is already canonical elsewhere;
- infrastructure topology research is retained source-neutral because its HDM constraints/options/revisit triggers remain useful;
- `DEV/PROJECT_MAP.md` routes host/platform architecture first to accepted R2.3/R2.4/R2.6 owners/current roadmap and only then to retained source-neutral/internal evidence when revalidation is needed;
- `DEV/TOOLS/audit_engine.py` no longer requires prohibited source-history markers and instead supplies bounded exact-surface regression guards while explicitly protecting legal and technical provenance;
- `SR23-FINAL-01` repairs only the WP-23 synthesis of existing release-owner obligations and restores both fresh-Project acceptance boundaries without changing the underlying release owner.

This is repository-wide reconciliation of the current public `DEV/` + `GAME/` provenance boundary for the WP-23 audited current-tree frontier. The machine guard is deliberately bounded and does not eliminate owner-aware review for future ambiguous artifacts.

## 9. Verification and proof classes

### 9.1 Current source/static/build verification

Current verification routes may establish only what they actually execute, including maintenance audit, unit/contract tests and release-build integration checks.

A successful exact-head source workflow does **not** satisfy either fresh-Project acceptance gate.

### 9.2 Pre-tag candidate fresh-Project acceptance

After the final version-coherent tree has produced the candidate artifact and applicable source/build validation has passed, the **pre-tag candidate artifact** must be tested in a fresh supported Project before the immutable release tag is created.

This is an empirical acceptance boundary on the pre-tag candidate. It is distinct from source/static/build evidence and from the later uploaded-asset acceptance boundary.

### 9.3 Immutable tag / publication evidence

Only after the pre-tag candidate gate is satisfied may the immutable release tag / tag-triggered publication boundary be crossed under the current release owner.

A real release-readiness claim must bind to the actual immutable tag/source basis and actual release workflow outcome.

### 9.4 Exact uploaded runtime asset verification

After tag-triggered publication, the exact uploaded runtime asset must be identified and its required checksum/provenance verified under current release-owner rules. Reusing same-name assets is subject to the existing exact-byte/hash rules; source snapshots remain non-runtime artifacts.

### 9.5 Post-upload fresh-Project acceptance

The **exact uploaded runtime asset** must then be tested in a fresh supported Project before the release is announced.

This second acceptance boundary is evidence about the uploaded artifact, not a replay of the pre-tag proof. The architecture does not require a different physical Project instance; it requires independently attributable evidence for the uploaded asset.

### 9.6 Release announcement boundary

A release may be announced only when all applicable release-owner obligations have passed, including both fresh-Project acceptance boundaries and the intervening tag/publication/exact-uploaded-asset verification obligations.

### 9.7 Post-implementation evaluation

Behavioral/production-like evaluation remains owned by the relevant assurance/verification contracts and occurs only against the actual implemented target when its owner activates that requirement.

## 10. Remaining obligations by class

### Current architecture requirements

This specification plus its composed package/version/update/legal owners define them.

### Current machine/build realization

Current source tree contains release metadata projection, builder/launcher, package provenance, archive checksum, flat-package validation, release workflow definition, legal-copy parity, source CI/tests, update/package-selection laws and bounded public-provenance regression verification.

### Remaining implementation-only obligations

Future runtime/migration machinery whose current owners have not activated remains implementation work, not a WP-23 architecture defect.

### Release-time obligations

When actual release execution is authorized, preserve the following order:

1. finalize one version-coherent source tree;
2. obtain applicable build/validation evidence;
3. build the pre-tag candidate artifact;
4. obtain fresh-Project acceptance evidence for that pre-tag candidate;
5. create the immutable release tag / allow tag-triggered publication;
6. verify the exact uploaded runtime asset and required checksum/provenance;
7. obtain fresh-Project acceptance evidence for the exact uploaded runtime asset;
8. announce the release only when all other applicable release-owner obligations also pass.

Preserve legal/approved attribution and exact technical provenance throughout.

### Post-implementation acceptance/evaluation

Perform only when the relevant implementation/assurance owner activates it; do not infer it from source/build success.

## 11. Explicit fail-closed / negative requirements

HDM release/package/version/legal readiness must not:

1. package `DEV/` into the runtime;
2. accept source snapshots as installable runtime assets;
3. merge files from sibling runtime roots;
4. collapse semantic version, exact package provenance and final archive digest;
5. infer compatibility/migration from version order, generation adjacency, tags or Git ancestry alone;
6. treat source CI success as either fresh-Project acceptance gate;
7. treat reproducible ZIP construction as pre-tag candidate acceptance or published-release acceptance;
8. collapse the pre-tag candidate acceptance boundary into the post-upload uploaded-asset acceptance boundary;
9. cross the immutable tag/publication boundary without the pre-tag candidate acceptance required by the current release owner;
10. announce a release before exact uploaded-asset verification and post-upload fresh-Project acceptance pass;
11. treat legal-file parity alone as complete public-provenance hygiene;
12. delete legally required or explicitly approved attribution during sanitation;
13. delete required technical artifact provenance during sanitation;
14. use a global external-name/URL blacklist as semantic provenance authority;
15. exempt current historical/research/design/test files merely because of their age/path;
16. discard material HDM semantics or revisit/defer triggers while sanitizing mixed artifacts;
17. allow historical implementation preferences to constrain future implementation;
18. create a second release/currentness/compatibility owner;
19. reopen WP-20 without a proved reopen condition;
20. claim production release readiness before actual release-time and acceptance evidence exists.

## 12. Step-6 / Step-7 / final-Senior closure state

```text
STEP6_BLOCKING_FOUND: 0
STEP6_SIGNIFICANT_FOUND: 5
STEP6_MINOR_FOUND: 2

STEP7_UNRESOLVED_BLOCKING: 0
STEP7_UNRESOLVED_SIGNIFICANT: 0
STEP7_UNRESOLVED_MINOR: 0

WP23_FINAL_SENIOR_REVIEW_PREVIOUS_RESULT: HOLD — SR23-FINAL-01
SR23-FINAL-01: CLOSED / REPAIRED
SR23_FINAL_01_UNRESOLVED: NO
WP23_FINAL_SENIOR_RE_REVIEW: PASS / GO
WP23_FINAL_CLOSURE: PASS
WP23_CLOSED: YES
PROPAGATION_SWEEP_COMPLETE: YES
HUMAN_DECISION_REQUIRED: NO
WP20_REOPEN_REQUIRED: NO
WHOLESALE_WP23_REOPEN_REQUIRED: NO
NEW_WORKSTREAM_REQUIRED: NO
```

The final-Senior finding does not alter the historical Step-6 finding counts. It is a later review finding and is tracked separately.

## 13. Version Impact

The targeted `SR23-FINAL-01` repair changes only WP-23 design/canonical/status documentation by restoring an obligation already present in `DEV/RELEASE/CHECKLIST.md`. It does not change release product semantics, package bytes, runtime behavior or an implementation contract beyond accurately composing the existing release owner.

No change is made to:

- `engine_version` / release identity;
- a version-bearing CORE/runtime semantic module contract;
- persistent or protocol schema version;
- campaign/storage/catalog/ruleset generation;
- digest/canonicalization contract generation;
- package format/provenance schema;
- migration/update compatibility law;
- executable gameplay/runtime implementation.

Therefore:

```text
VERSION_IMPACT: VERIFIED
VERSION_BUMP_REQUIRED: NO
VERSION_IMPACT_DISPOSITION: NONE
VERSIONING_TAXONOMY_REOPENED: NO
```

## 14. Canonical gate

```text
WP23_STEPS_2_8_COMPLETE: YES
WP23_CANONICAL_SPEC_PUBLISHED: YES
WP23_FINAL_SENIOR_REVIEW_PREVIOUS_RESULT: HOLD — SR23-FINAL-01
SR23_FINAL_01_TARGETED_REPAIR_COMPLETE: YES
WP23_FINAL_SENIOR_RE_REVIEW: PASS / GO
WP23_FINAL_CLOSURE: PASS
WP23_CLOSED: YES

HUMAN_DECISION_REQUIRED: NO
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
WP20_REOPEN_REQUIRED: NO
WHOLESALE_WP23_REOPEN_REQUIRED: NO

WP24_NEXT_ELIGIBLE: YES
WP24_NOT_STARTED: YES
WP24_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
RUNTIME_RELEASE_EXECUTED: NO
RUNTIME_MIGRATION_EXECUTED: NO
REAL_CAMPAIGN_MIGRATED: NO
REAL_GAMEPLAY_BOOTSTRAP_STARTED: NO

NEXT_AUTHORIZED_UNIT: NONE
NEXT_GATE: EXPLICIT PRODUCT OWNER AUTHORIZATION TO LAUNCH WP-24
```
