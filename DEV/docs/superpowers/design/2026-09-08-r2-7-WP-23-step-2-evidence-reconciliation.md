# R2.7 WP-23 — Step 2 Evidence Extraction and Reconciliation

Status: **STEP 2 COMPLETE — EVIDENCE / OWNER RECONCILIATION**

Date: 2026-09-08

Starting exact public basis:

```text
branch: v1/engine-rearchitecture
head: 05effce1a4fab240c1bdba0967ebd760e66984f8
```

This is design evidence, not the final WP-23 implementation-facing owner. It consumes the approved Step-1 framing, independent Senior `PASS / GO`, and the Product Owner public-provenance decision. It does not authorize a release, tag, deployment, campaign migration, implementation planning, WP-24, or gameplay bootstrap.

---

## 1. Evidence method and source roles

Step 2 re-read current owners and current-tree consumers rather than treating the Step-1 Source Manifest as frozen.

Primary semantic/decision owners used for the current questions include:

- `DEV/docs/superpowers/specs/2026-09-08-hdm-public-research-provenance-attribution-owner-decision.md`;
- `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md`;
- the current HDM versioning policy and machine-realization status amendment;
- current runtime update/bootstrap/install owners under `GAME/CORE/` and `GAME/INSTALL/`;
- current repository/legal ownership rules in `AGENTS.md` and root/runtime legal files.

Machine/build/verification consumers include:

- `DEV/TOOLS/release_builder.py` and `run_release_build.py`;
- `.github/workflows/release-runtime.yml`;
- `.github/workflows/validate.yml`;
- `DEV/RELEASE/CHECKLIST.md` and `VERSIONING.md`;
- `DEV/TOOLS/audit_engine.py`;
- release/version/install/update tests routed by `DEV/PROJECT_MAP.md`.

Supporting/historical evidence was used only to determine current-tree consistency and retirement/sanitation consequences. It does not override current owners.

---

## 2. Coupled release-chain reconstruction

The current WP-23 audit object is one chain:

```text
current authoritative source state
-> semantic engine/release identity
-> exact release-build input and validation
-> flattened runtime-package construction
-> generated exact-package provenance
-> final archive digest
-> tag-triggered publication route
-> install/package-root validation
-> exact-runtime binding
-> update/migration eligibility
-> legal / approved attribution payload
-> public provenance hygiene
-> publishable distributable artifact
-> release-time / fresh-environment acceptance
```

No intermediate node alone proves final release readiness.

### Identity separation

Three identities remain intentionally non-equivalent:

```text
ENGINE_VERSION.yaml
    semantic engine/release contract

RUNTIME_PACKAGE.yaml
    exact built package source/provenance contract

final ZIP SHA-256
    exact archive-bytes identity
```

Tag/release metadata may prove publication facts but does not replace package-carried identity or final-byte digest.

---

## 3. Lane A — Package & installation integrity

### A-01 — Runtime source boundary

**State:** `SATISFIED_CURRENT / REALIZED_CURRENT`.

`GAME/` is the exact shipped runtime source boundary. `DEV/` is not packaged. The release builder flattens valid `GAME/` contents to the package root and adds exactly one generated top-level `RUNTIME_PACKAGE.yaml`.

**Negative rule:** repository wrappers such as `GAME/` or `DEV/` must not appear inside the installable runtime archive.

### A-02 — Open-world GAME passthrough

**State:** `SATISFIED_CURRENT`, with a cross-lane consequence.

The builder deliberately has no hand-maintained allowlist for ordinary `GAME/` payload. New valid `GAME/` files are automatically release-facing.

**Consequence:** every new `GAME/` artifact is automatically a package/install/legal/public-provenance consumer. Package correctness therefore cannot be audited independently from Lane C.

### A-03 — Package reproducibility and generated provenance

**State:** `SATISFIED_CURRENT / REALIZED_CURRENT`.

Current builder/test contracts cover deterministic package construction, generated package provenance, legal-copy parity and final checksum emission. Development and tagged package provenance are distinguished rather than falsely claiming tagged source identity for dirty/non-tagged builds.

### A-04 — Install shape and runtime-root isolation

**State:** `SATISFIED_CURRENT / REALIZED_CURRENT`.

Install/bootstrap owners require root `ENGINE_VERSION.yaml` + `RUNTIME_PACKAGE.yaml`, required runtime sibling directories, exact package-root binding, lazy extraction/reuse, and no cross-version file borrowing.

**Negative rules:** source-code archives are not runtime assets; missing extracted cache is not package incompatibility; runtime roots must not be mixed.

### A-05 — Actual production publication

**State:** `DEFERRED_UNTIL_REAL_RELEASE`.

The tag workflow is present and current, but WP-23 does not execute it. No tag, GitHub Release, asset upload or production publication is evidence from this architecture run.

### A-06 — Fresh-environment install acceptance

**State:** `RELEASE_TIME_OBLIGATION`.

The release checklist requires validation from an actually published asset in a fresh ChatGPT Project/environment. That cannot be replaced by source-tree build success or source CI.

---

## 4. Lane B — Version / upgrade / release integrity

### B-01 — Release identity projection

**State:** `SATISFIED_CURRENT / REALIZED_CURRENT`.

Current DEV/GAME manifests project the same shared semantic release fields while DEV-only development revision metadata remains excluded from `GAME/ENGINE_VERSION.yaml`.

Current pre-release identity is `1.0-alpha` with recommended version tag `v1.0-alpha` and campaign-contract generation `2`.

### B-02 — Version namespaces

**State:** `SATISFIED_CURRENT / REALIZED_CURRENT`.

Engine release, engine-bound module revision, contract/schema versions, campaign/storage generations, catalog generation, ruleset package/compatibility generations and artifact digests remain separate namespaces. Numeric equality/order across namespaces does not establish compatibility.

### B-03 — Exact artifact versus semantic version

**State:** `SATISFIED_CURRENT`.

Same semantic version/package ID/source ancestry is insufficient to authorize different released bytes. Exact digest proves exact artifact identity; different bytes require affirmative compatibility support from the exact candidate package.

### B-04 — Released-v1.0+ compatibility horizon

**State:** `ARCHITECTURE_COMPLETE / REALIZATION_DEFERRED_BY_OWNER`.

WP-20 owns released-v1.0+ compatibility/migration composition. Its architecture remains sufficient for the WP-23 release consumer. No contradiction, missing current consumer law, or insufficiency was found that justifies reopening WP-20.

The absence of future migration-edge machine realization before an actual released-v1.0+ evolution need is not a current pre-release defect.

### B-05 — Release workflow currentness

**State:** `REALIZED_CURRENT`, with release execution deferred.

The tag-triggered workflow checks out the exact tagged source, runs current source validation, builds in tag mode, then creates/uploads the release artifact. That workflow is a machine consumer; successful presence or source CI is not proof that a future tag-run/release succeeds.

### B-06 — Release-time gates

**State:** `RELEASE_TIME_OBLIGATION`.

A real release must bind claims to exact tag/head, actual workflow result, actual produced asset/checksum, legal payload and fresh-environment install/runtime acceptance.

---

## 5. Lane C — Repository-wide legal and public-provenance reconciliation

### 5.1 Governing classification

Current public `DEV/` + `GAME/` content is classified by purpose, not by path or age.

```text
REQUIRED_LEGAL_OR_APPROVED_ATTRIBUTION
    preserve

HDM_TECHNICAL_ARTIFACT_PROVENANCE
    preserve where current owners require it

HDM_NATIVE_SEMANTICS / INTERNAL HDM EVIDENCE
    preserve

SOURCE_SPECIFIC_DEVELOPMENT_RESEARCH_PROVENANCE
    prohibited in current public tree

MIXED_ARTIFACT
    preserve/rehome HDM-native conclusion; remove source-specific development trail
```

Historical placement under `research/`, `design/`, `specs/` or `DEV/ARCHITECTURE/` creates no exemption.

### 5.2 Required legal / approved attribution

**State:** `SATISFIED_CURRENT / MUST_PRESERVE`.

Root and runtime legal payload remains release-facing and builder-validated:

- `LICENSE`;
- `NOTICE`;
- `THIRD_PARTY_NOTICES.md`;
- `LICENSES/` and matching `GAME/` copies.

This material is not to be removed by public-research sanitation.

### 5.3 Required technical artifact provenance

**State:** `SATISFIED_CURRENT / MUST_PRESERVE`.

Allowed/required technical provenance includes exact commit/source SHA, tag/release identity, generated `RUNTIME_PACKAGE.yaml`, final package digest, version/generation identities, ruleset-set identity, migration/update lineage and deterministic currentness/publication evidence.

This evidence is not source-specific research provenance merely because it records origin/currentness.

### 5.4 Runtime development-source narrative

**Finding C-01 — SIGNIFICANT / MECHANICALLY RESOLVABLE.**

`GAME/CORE/SOURCES.md` is shipped by the all-`GAME` package rule and currently carries source-specific development/research history rather than only current HDM semantics/routing.

Current semantic owners already contain the derived HDM behavior. Therefore sanitation must not delete those semantics. The runtime file can be reduced to a source-neutral HDM provenance/routing boundary that points to:

- current HDM CORE/RULES owners for semantics;
- `GAME/RULES/OFFICIAL_SOURCES.md` only for current operational rules-source routing;
- runtime legal files for required attribution;
- package/version/digest markers for technical artifact provenance.

### 5.5 Stale machine protection of prohibited provenance

**Finding C-02 — SIGNIFICANT / MECHANICALLY RESOLVABLE.**

`DEV/TOOLS/audit_engine.py` currently requires source-specific development-reference markers from `GAME/CORE/SOURCES.md` as part of GM-guidance auditing.

That machine check now contradicts the Product Owner decision. It must be replaced by checks of the independently stated HDM behavior plus explicit public-provenance-hygiene checks. Removing the stale anchors must not weaken actual GM-craft/runtime semantic tests.

### 5.6 Current architecture documents with source-history sections

**Finding C-03 — SIGNIFICANT / MECHANICALLY RESOLVABLE.**

Exact-head review confirms source-specific design/research basis sections in current public architecture artifacts including:

- `DEV/ARCHITECTURE/ASSET_MODEL.md`;
- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`;
- `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md`;
- `DEV/ARCHITECTURE/CRITICAL_ARCHITECTURE_AUDIT.md`;
- `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md`.

Their independently stated HDM laws/decisions remain useful. The disposition is targeted sanitation of source-history/prior-art narrative while retaining HDM-native conclusions, exclusions, negative requirements and defer boundaries.

`MECHANICAL_RUNTIME_PROPOSAL.md` additionally contains an external implementation-candidate preference. Because it is noncanonical and source-specific, sanitation must not let that preference become a hidden implementation requirement.

### 5.7 External platform research documents

**Finding C-04 — SIGNIFICANT / MECHANICALLY RESOLVABLE.**

Current public research directory contains source-specific platform/economic research documents whose purpose is to retain external development research history:

- `DEV/docs/superpowers/research/2026-08-22-platform-feasibility-comparative-research.md`;
- `DEV/docs/superpowers/research/2026-08-22-platform-feasibility-economic-profile-amendment.md`;
- `DEV/docs/superpowers/research/2026-08-22-private-hosted-inference-economics.md`;
- `DEV/docs/superpowers/research/2026-08-24-chatgpt-plus-host-evidence.md`.

Current host/product requirements are already owned by current roadmap/R2.6 architecture. These development-source histories do not need to remain in the current public tree. Git history remains intact.

### 5.8 Mixed topology / transport evidence

**Finding C-05 — SIGNIFICANT / MECHANICALLY RESOLVABLE.**

Two research artifacts mix durable HDM constraints/evidence with source-specific development research/routing:

- `DEV/docs/superpowers/research/2026-08-22-infrastructure-topology-options.md`;
- `DEV/docs/superpowers/research/2026-08-20-step-6-repository-port-transport-feasibility-spike.md`.

They must not be deleted blindly. Source-neutral HDM conclusions, explicit limitations, safe defer/revisit triggers and deterministic HDM publication/currentness findings must be retained where still useful. Source-specific development narrative, external comparison trails and private-workspace provenance must not remain in current public material.

### 5.9 Source-neutral/internal research remains valid

**Negative finding:** research-path placement itself is not prohibited.

Current files that retain internal HDM experiment/evidence, owner reconciliation, version inventory or independently rewritten source-neutral idea inventories may remain when they do not preserve source-specific development provenance.

For example, the source-neutral architecture-idea dossier explicitly avoids external project/source histories and records HDM-formulated items/revisit triggers; it is not removed merely because its filename says `External`.

### 5.10 Operational external references are not automatically research provenance

**Negative finding:** external names/URLs are not globally forbidden.

`GAME/RULES/OFFICIAL_SOURCES.md` serves current runtime rules-source routing. Current host/platform names in accepted architecture may identify actual deployment dependencies. Legal files may identify licensors/material. These must be classified by current function, not removed by string matching.

Any historical-development phrasing inside an otherwise operational current owner should be rewritten to current operational semantics rather than deleting the owner.

---

## 6. Cross-lane contradiction analysis

### X-01 — all-GAME passthrough x public provenance

Before sanitation, the release builder correctly packages `GAME/`, but that correctness makes prohibited runtime development provenance automatically distributable. Lane A can therefore be locally correct while the composed release chain is not public-provenance compliant.

**Disposition:** repair Lane-C source boundary and machine checks; do not weaken all-GAME passthrough.

### X-02 — legal parity x provenance sanitation

Removing source-specific development provenance must not remove mandatory legal/approved attribution copied and validated into the runtime package.

**Disposition:** preserve explicit legal payload as a separate class.

### X-03 — technical provenance x research provenance

A naive provenance scrub could remove exact package/currentness evidence required by Lane B.

**Disposition:** explicit allow/required class for HDM technical artifact provenance.

### X-04 — version/currentness x release acceptance

Correct semantic version and exact package provenance still do not prove a published asset exists or installs in a fresh environment.

**Disposition:** preserve release-time acceptance obligations as future proof, not current defect and not current PASS claim.

### X-05 — WP-20 overlap

Current release/update consumers are satisfied by accepted WP-20 semantics. No release-specific contradiction was found.

**Disposition:** `WP20_REOPEN_REQUIRED: NO`.

---

## 7. Step-2 completeness matrix

| Item family | Current disposition |
|---|---|
| package source boundary | already satisfied / realized |
| generated package provenance | already satisfied / realized |
| final archive digest | already satisfied / realized |
| install root isolation | already satisfied / realized |
| release workflow definition | already satisfied / realized |
| actual tag/release execution | deferred until real release |
| fresh-environment release acceptance | release-time obligation |
| version namespace separation | already satisfied / realized |
| released-v1.0+ compatibility law | already satisfied architecture; future realization conditional |
| WP-20 reopen | not justified |
| required legal attribution | preserve / realized |
| required technical artifact provenance | preserve / realized |
| prohibited current public research provenance | current consistency gap; finite sanitation required |
| provenance-hygiene machine verification | current consistency gap; stale opposite check exists |
| new licensing policy | out of scope / not needed |
| root README rewrite | out of scope without explicit PO approval |
| actual production-release readiness | not claimable at Step 2 |

---

## 8. Human-decision / decomposition gate

The Product Owner has already resolved the only material provenance-policy choice found by Step 1.

Step-2 reconciliation found no new material product/licensing/authority/compatibility choice. The remaining Lane-C work is implementation of the accepted public boundary within the architecture-stage canonicalization/consistency allowance.

```text
HUMAN_DECISION_REQUIRED: NO
NEW_WORKSTREAM_REQUIRED: NO
WP23_REMAINS_ONE_COUPLED_WORK_PACKAGE: YES
WP20_REOPEN_REQUIRED: NO
STEP2_COMPLETENESS_GATE: PASS
NEXT_PROCESS_UNIT: STEP 3 DECISION BRIEF
```

This is not a product release-readiness verdict.
