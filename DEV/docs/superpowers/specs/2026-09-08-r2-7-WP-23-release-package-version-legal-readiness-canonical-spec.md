# R2.7 WP-23 — Release / Package / Version / Legal Readiness — Canonical Specification

Status: **CANONICAL IMPLEMENTATION-FACING ARCHITECTURE — STEP 8 COMPLETE / FINAL SENIOR REVIEW PENDING**

Date: 2026-09-08

This specification is the implementation-facing WP-23 architecture result produced by the approved Step-1 framing and Steps 2–8. It composes existing owners rather than replacing their native semantics. WP-23 is not closed until the mandatory independent final Senior review passes.

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

## 2. One coupled release-readiness chain

WP-23 remains one coupled work package across package/install, version/update/release, and legal/provenance concerns:

```text
current authoritative source state
-> semantic release identity
-> source/build validation
-> runtime package construction
-> exact built-package provenance
-> final archive digest
-> install/runtime-root conformance
-> update/migration eligibility
-> required legal / approved attribution
-> public provenance hygiene
-> actual release publication evidence when executed
-> fresh supported-environment acceptance when executed
```

No intermediate node has the proof power of a later node.

Normative non-equivalences:

```text
SUCCESSFUL_ZIP_BUILD != RELEASE_READINESS
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

Those proofs do not establish that an actual Release exists or that a fresh supported Project accepts the published asset.

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

At Step-8 canonicalization, the current tree realizes the following WP-23 consistency repairs:

- `GAME/CORE/SOURCES.md` is an HDM-native runtime source/provenance boundary rather than a development-research bibliography;
- `DEV/ARCHITECTURE/ASSET_MODEL.md`, `ACTIVITY_MODEL.md` and `ENTITY_STRUCTURES.md` retain their HDM semantics without development-source basis sections;
- historical `CRITICAL_ARCHITECTURE_AUDIT.md`, `MECHANICAL_RUNTIME_PROPOSAL.md` and `DEV/TESTS/PRE_RELEASE_AUDIT_0.1.0.md` retain useful HDM conclusions/history in source-neutral form;
- four source-history platform/economic research files are retired from the current public tree;
- the repository-port transport source-history spike is retired because current publication/currentness law is already canonical elsewhere;
- infrastructure topology research is retained source-neutral because its HDM constraints/options/revisit triggers remain useful;
- `DEV/PROJECT_MAP.md` routes host/platform architecture first to accepted R2.3/R2.4/R2.6 owners/current roadmap and only then to retained source-neutral/internal evidence when revalidation is needed;
- `DEV/TOOLS/audit_engine.py` no longer requires prohibited source-history markers and instead supplies bounded exact-surface regression guards while explicitly protecting legal and technical provenance.

This is repository-wide reconciliation of the current public `DEV/` + `GAME/` provenance boundary for the WP-23 audited current-tree frontier. The machine guard is deliberately bounded and does not eliminate owner-aware review for future ambiguous artifacts.

## 9. Verification and proof classes

### Current source/static/build verification

Current verification routes may establish only what they actually execute, including maintenance audit, unit/contract tests and release-build integration checks.

### Actual release publication evidence

A real release-readiness claim for one exact release must bind to the actual immutable tag/source basis, actual release workflow result, actual uploaded runtime asset and exact checksum/identity evidence required by current release owners.

### Fresh-environment acceptance

Where the release checklist requires the actual published runtime asset to be tested in a fresh supported ChatGPT Project/environment, that is a release-time empirical/acceptance obligation. Source-tree or locally built ZIP success cannot substitute for it.

### Post-implementation evaluation

Behavioral/production-like evaluation remains owned by the relevant assurance/verification contracts and occurs only against the actual implemented target when its owner activates that requirement.

## 10. Remaining obligations by class

### Current architecture requirements

This specification plus its composed package/version/update/legal owners define them.

### Current machine/build realization

Current source tree contains release metadata projection, builder/launcher, package provenance, archive checksum, flat-package validation, release workflow definition, legal-copy parity, source CI/tests, update/package-selection laws and bounded public-provenance regression verification.

### Remaining implementation-only obligations

Future runtime/migration machinery whose current owners have not activated remains implementation work, not a WP-23 architecture defect.

### Release-time obligations

- execute the exact release/tag workflow when authorized;
- verify actual uploaded asset/checksum/provenance;
- perform required fresh-environment published-asset acceptance;
- preserve legal/approved attribution and exact technical provenance in the actual release.

### Post-implementation acceptance/evaluation

Perform only when the relevant implementation/assurance owner activates it; do not infer it from source/build success.

## 11. Explicit fail-closed / negative requirements

HDM release/package/version/legal readiness must not:

1. package `DEV/` into the runtime;
2. accept source snapshots as installable runtime assets;
3. merge files from sibling runtime roots;
4. collapse semantic version, exact package provenance and final archive digest;
5. infer compatibility/migration from version order, generation adjacency, tags or Git ancestry alone;
6. treat source CI success as actual release publication proof;
7. treat reproducible ZIP construction as published-release acceptance;
8. treat legal-file parity alone as complete public-provenance hygiene;
9. delete legally required or explicitly approved attribution during sanitation;
10. delete required technical artifact provenance during sanitation;
11. use a global external-name/URL blacklist as semantic provenance authority;
12. exempt current historical/research/design/test files merely because of their age/path;
13. discard material HDM semantics or revisit/defer triggers while sanitizing mixed artifacts;
14. allow historical implementation preferences to constrain future implementation;
15. create a second release/currentness/compatibility owner;
16. reopen WP-20 without a proved reopen condition;
17. claim production release readiness before actual release-time and acceptance evidence exists.

## 12. Step-6 / Step-7 closure

```text
STEP6_BLOCKING_FOUND: 0
STEP6_SIGNIFICANT_FOUND: 5
STEP6_MINOR_FOUND: 2

STEP7_UNRESOLVED_BLOCKING: 0
STEP7_UNRESOLVED_SIGNIFICANT: 0
STEP7_UNRESOLVED_MINOR: 0

PROPAGATION_SWEEP_COMPLETE: YES
HUMAN_DECISION_REQUIRED: NO
WP20_REOPEN_REQUIRED: NO
NEW_WORKSTREAM_REQUIRED: NO
```

## 13. Version Impact

Actual realized WP-23 delta changes public documentation/routing/provenance hygiene and maintenance verification. `GAME/CORE/SOURCES.md` is a non-versioned runtime routing/documentation surface; its sanitation does not change gameplay mechanics or a versioned module contract.

No change was made to:

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
WP23_FINAL_SENIOR_REVIEW: REQUIRED / PENDING
WP23_CLOSED: NO

HUMAN_DECISION_REQUIRED: NO
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
WP20_REOPEN_REQUIRED: NO

WP24_NOT_STARTED: YES
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
RUNTIME_RELEASE_EXECUTED: NO
RUNTIME_MIGRATION_EXECUTED: NO
REAL_GAMEPLAY_BOOTSTRAP_STARTED: NO

NEXT_AUTHORIZED_UNIT: NONE
NEXT_GATE: MANDATORY INDEPENDENT FINAL SENIOR REVIEW OF COMPLETE WP-23 STEPS 2–8 PACKAGE
```
