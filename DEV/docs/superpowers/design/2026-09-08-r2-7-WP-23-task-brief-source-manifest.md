# R2.7 WP-23 — Release / Package / Version / Legal Readiness — Step-1 Task Brief and Source Manifest

Status: **STEP-1 FRAMING COMPLETE / WHOLE-PROJECT CRITIC REPAIRED / MANDATORY SENIOR REVIEW PENDING**

Date: 2026-09-08

Starting public branch/head examined:

```text
v1/engine-rearchitecture
a37c474e1da54be4a8f3e216e407e528f03cfed9
```

This artifact is Step-1 design provenance. It does not declare product release readiness, authorize a release, supersede accepted semantic owners, or authorize WP-23 Step 2.

---

## 1. Authorization and exact boundary

The Product Owner explicitly authorized launch of R2.7 WP-23 and only its complete Step-1 boundary:

```text
Task Brief
-> open-world Source Manifest / dependency discovery
-> whole-project Task-Brief critic
-> mechanically resolvable critic repairs
-> review-ready Step-1 checkpoint
-> STOP FOR SENIOR REVIEW
```

WP-23 remains one work package with three coupled audit lanes:

- **Lane A — Package & installation integrity**;
- **Lane B — Version & upgrade/release integrity**;
- **Lane C — Legal & provenance hygiene**.

The audit object is their composition, not three independent local checklists.

### Hard scope fences

This Step 1 SHALL NOT:

- create a release, tag, deployment, publication or GitHub Release asset;
- run gameplay or a real campaign bootstrap;
- migrate a real campaign;
- begin implementation planning or substantive implementation;
- reopen WP-20 merely because update/version topics overlap;
- invent new licensing policy or perform unbounded external legal research;
- import private-Lab provenance into public HDM;
- rewrite the root `README.md` opportunistically;
- split WP-23 into new workstreams without an explicit owner decision.

Release/build/install/runtime surfaces may be read and mechanically reasoned about only far enough to establish the Step-1 architecture/readiness framing.

---

## 2. Problem statement

WP-23 must determine whether the current release architecture forms one coherent, reviewable chain:

```text
current authoritative source state
-> versioned release identity
-> release/package construction
-> packaged GAME/runtime boundary
-> install/runtime consistency
-> update/migration eligibility
-> required legal/attribution payload
-> publishable distributable artifact
```

The Step-1 problem is **not** “can the current repository make a ZIP?” and is **not** “are a few release files present?”. It is to reconstruct the owners, consumers, machine/build paths, legal/provenance surfaces, verification routes, negative requirements and deferred obligations that jointly constrain that chain, then expose any composition defect before design work begins.

A local surface may be individually valid while the composed release chain remains incomplete or contradictory.

---

## 3. Authority discipline

### 3.1 Program and process authority

The following govern this Step 1 but do not become WP-23 semantic owners:

| ID | Source | Role / applicability |
|---|---|---|
| P01 | `AGENTS.md` | repository boundaries, public-write discipline, root-README fence, artifact placement |
| P02 | `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | GitHub Connector transport and publication fence |
| P03 | `DEV/DESIGN_PROCESS.md` | deep-work evidence/completeness process |
| P04 | `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | R2.7 Step-1 critic and mandatory Senior stop |
| P05 | `DEV/PROJECT_MAP.md` | dependency routing only; not semantic authority |
| P06 | `DEV/CURRENT_PROGRESS.md` | sole global current-position/gate owner |
| P07 | `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | WP sequencing/scope only |
| P08 | `DEV/PRODUCT_OWNER_INPUT.md` | applicable retained PO input; especially released-v1.0+ compatibility routing |

### 3.2 Mandatory R2.7 program boundary

| ID | Source | Role |
|---|---|---|
| R01 | `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md` | owning R2.7 audit boundary / authority clarification |
| R02 | `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md` | R2.7 scope-discovery provenance, including WP-23 inventory |

### 3.3 Closed predecessor owners that WP-23 consumes but does not casually reopen

| ID | Source | Role |
|---|---|---|
| B01 | `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md` | canonical version/namespace/compatibility semantics |
| B02 | `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-machine-realization-status-amendment.md` | supersedes only obsolete “machine realization deferred” temporal wording; current pre-release version normalization is realized and Senior-passed |
| B03 | `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md` | released-v1.0+ compatibility/migration composition owner |
| B04 | `DEV/docs/superpowers/specs/2026-09-07-r2-7-WP-22-verification-test-evaluation-completeness-canonical-spec.md` | verification-role/state and exact-current-route discipline |
| B05 | `DEV/docs/superpowers/specs/2026-08-18-runtime-package-provenance-amendment.md` | accepted artifact-provenance split; later machine realization must be read through current implementation/status evidence |

Finding a keyword overlap with B01–B05 is not reopening evidence. Reopen requires a contradiction, unsatisfied release consumer, or insufficiency of the accepted owner.

---

## 4. Reconstructed dependency subgraph / Source Manifest

The manifest is open-world over the task dependency graph. Path groups below are included because they own, realize, consume, verify, or negatively constrain the release chain.

### 4.1 Lane A — package and installation integrity

| ID | Source / family | Role / evidence question |
|---|---|---|
| A01 | `DEV/TOOLS/release_builder.py` | machine composition, manifest/tag/provenance/legal/install/link/layout validation, deterministic ZIP + checksum construction |
| A02 | `DEV/TOOLS/run_release_build.py` | canonical local/CI builder launcher and isolated DEV-tool environment |
| A03 | `.github/workflows/release-runtime.yml` | tag-triggered release construction/publication consumer; exact tagged checkout, tag mode, release asset upload |
| A04 | `.github/workflows/validate.yml` | current source validation route; maintenance audit + DEV unit suite, not release-readiness authority |
| A05 | `GAME/` recursively | exact runtime source tree; all valid files are package-facing by construction |
| A06 | `GAME/INSTALL/README.md` | human installation surface and embedded Project Instructions source copy |
| A07 | `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` | packaged Project Instructions copy validated for parity |
| A08 | `GAME/INSTALL/00_DND_BOOTSTRAP.md` | installed-package consumer: package shape, exact artifact identity, isolated runtime root, source-archive rejection |
| A09 | `GAME/TOOLS/init_campaign.py` | packaged standard-library consumer used by release integration smoke; no campaign was actually bootstrapped in this Step 1 |
| A10 | `DEV/RELEASE/CHECKLIST.md` | release-development gate inventory and release/install negative requirements |
| A11 | `DEV/TESTS/test_release_builder.py` | builder contract/safety/shape/tag/parity checks |
| A12 | `DEV/TESTS/test_release_game_passthrough.py` | open-world package-content proof: new valid `GAME/` files/directories automatically enter the archive |
| A13 | `DEV/TESTS/test_release_integration.py` | canonical builder -> reproducible flat package -> extracted packaged generator smoke |
| A14 | `DEV/TESTS/test_release_legal_boundary.py` | build fails on root/GAME legal-copy drift |
| A15 | `DEV/TESTS/test_release_local_output.py` | canonical launcher/local-output boundary and ignored build directories |
| A16 | `DEV/TESTS/test_release_timestamps.py` | archive timestamp provenance/reproducibility behavior |
| A17 | `DEV/TESTS/test_runtime_package_provenance.py` | tagged/clean/dirty/non-git package provenance and generated root metadata |
| A18 | `DEV/TESTS/test_multi_runtime_release_consistency.py` | generated provenance not tracked in `GAME/`; multi-runtime portable-identity consistency |
| A19 | `DEV/TESTS/test_engine_mismatch_recovery_contract.py` | installed-runtime mismatch/recovery consumer behavior |
| A20 | `DEV/TESTS/INSTALL_ONBOARDING_CASES.md`, `DEV/TESTS/ENGINE_CONSISTENCY_CASES.md` | scenario/acceptance neighbors for install/runtime consistency; presence is not execution result |

### 4.2 Lane B — version and upgrade/release integrity

| ID | Source / family | Role / evidence question |
|---|---|---|
| V01 | `DEV/ENGINE_DEVELOPMENT.yaml` | DEV release metadata superset |
| V02 | `GAME/ENGINE_VERSION.yaml` | shipped semantic engine/release identity |
| V03 | `DEV/RELEASE/VERSIONING.md` | release-facing version policy projection/routing |
| V04 | B01 + B02 | current canonical version taxonomy plus realized-status correction |
| V05 | B03 | released-v1.0+ compatibility/migration law consumed by release/runtime surfaces |
| V06 | `GAME/CORE/ENGINE_UPDATES.md` | packaged update/migration eligibility and exact-package consumer contract |
| V07 | `GAME/MIGRATIONS/README.md` | package-scoped explicit migration-edge architecture and deferred machine-realization boundary |
| V08 | builder-generated `RUNTIME_PACKAGE.yaml` | exact built-source/package provenance; generated artifact, not tracked `GAME/` source |
| V09 | final runtime ZIP SHA-256 sidecar / computed digest | exact immutable artifact identity; deliberately distinct from semantic version and package metadata |
| V10 | `DEV/TESTS/test_versioning_namespace_policy.py` | current namespace census, normalized engine manifest projection, stale-name rejection |
| V11 | `DEV/TESTS/test_engine_update_policy_contract.py` | current packaged update-policy contract checks |
| V12 | `DEV/TESTS/ENGINE_UPDATE_CASES.md` | update scenario/acceptance neighbor; does not itself prove future migrator realization |

### 4.3 Lane C — legal and provenance hygiene

| ID | Source / family | Role / evidence question |
|---|---|---|
| L01 | root `LICENSE` | repository primary license payload |
| L02 | root `NOTICE` | project notice and third-party notice routing |
| L03 | root `THIRD_PARTY_NOTICES.md` | declared third-party material/license routing |
| L04 | root `LICENSES/` | license/attribution payload currently containing the declared SRD attribution file |
| L05 | `GAME/LICENSE`, `GAME/NOTICE`, `GAME/THIRD_PARTY_NOTICES.md`, `GAME/LICENSES/` | distributable legal copies |
| L06 | `DEV/TOOLS/release_builder.py::validate_legal_copies` | exact root/GAME file-set and byte-parity release gate |
| L07 | `DEV/TESTS/test_release_legal_boundary.py` | executable negative proof for legal-copy drift |
| L08 | `GAME/CORE/SOURCES.md` | **distributable source/provenance document containing source-specific development provenance beyond license/notice payload** |
| L09 | `DEV/TOOLS/audit_engine.py` provenance/source checks | current maintenance audit positively requires selected source-specific anchors in L08, making that provenance machine-maintained rather than accidental prose |
| L10 | `DEV/TOOLS/requirements-dev-tools.txt` | build/verification-only dependency input; not itself shipped by the all-`GAME` runtime boundary |

### 4.4 Negative / stale / non-authority surfaces retained in discovery

| ID | Surface | Disposition |
|---|---|---|
| N01 | historical `research/`, `design/`, `plans/` material | provenance only unless current owner explicitly routes to it |
| N02 | obsolete temporal phrase “machine realization deferred” in B01 | superseded only for realization status by B02; semantic laws remain current |
| N03 | GitHub-generated repository source archives | public source artifacts, explicitly **not** installable runtime packages |
| N04 | root `README.md` | public overview with special editorial fence; not a Step-1 rewrite target |
| N05 | `release_status` field | bookkeeping/current metadata; current release law does not make it the tag-mode publication gate |
| N06 | pre-v1.0 historical campaign layouts/identities | outside released-v1.0+ compatibility horizon unless explicitly reintroduced by an owner |
| N07 | future migration transform/edge machine schema/runtime | architecture obligation, not current pre-release realization requirement |

---

## 5. Item-level lane coverage and present disposition

The following disposition vocabulary is used only for WP-23 Step-1 framing:

```text
SATISFIED_CURRENT
ARCHITECTURE_GAP_OR_CONFLICT
IMPLEMENTATION_ONLY_OBLIGATION
DEFERRED_UNTIL_REALIZATION_OR_RELEASE
HUMAN_OWNED_MATERIAL_DECISION
OUT_OF_SCOPE
```

### 5.1 Lane A

| ID | Requirement / negative law | Current Step-1 disposition |
|---|---|---|
| A-COV-01 | Package content derives from all valid `GAME/` files plus exactly one generated root `RUNTIME_PACKAGE.yaml`; no hand-maintained include list | `SATISFIED_CURRENT` |
| A-COV-02 | Runtime ZIP is flat; `GAME/`/`DEV/` source wrappers and source snapshots are not installable packages | `SATISFIED_CURRENT` |
| A-COV-03 | Builder validates required runtime directories, package metadata, integrated ruleset evidence, install-instruction parity, Markdown/destination links, legal copies and forbidden/junk/collision classes | `SATISFIED_CURRENT` at current realized builder boundary |
| A-COV-04 | Canonical build is reproducible for the same source/time basis and emits external SHA-256 identity | `SATISFIED_CURRENT` |
| A-COV-05 | New valid runtime files cannot silently miss the archive because `GAME/` passthrough is open-world | `SATISFIED_CURRENT`; also expands Lane-C exposure automatically |
| A-COV-06 | Installed runtime binds all reads to one exact validated package root; sibling versions cannot be mixed | `SATISFIED_CURRENT` as current packaged install/bootstrap contract |
| A-COV-07 | Release workflow uses tag-mode builder and immutable-asset behavior; builder requires tag identity and approved `origin/main` lineage | `SATISFIED_CURRENT` as current release-construction architecture, **not** evidence that this branch is releaseable now |
| A-COV-08 | Actual tag/release/upload and fresh-Project smoke of uploaded asset | `DEFERRED_UNTIL_REALIZATION_OR_RELEASE`; explicitly not executed in Step 1 |

### 5.2 Lane B

| ID | Requirement / negative law | Current Step-1 disposition |
|---|---|---|
| V-COV-01 | Semantic engine identity, exact built-source provenance and final ZIP digest remain distinct identities | `SATISFIED_CURRENT` |
| V-COV-02 | `recommended_tag` exactly projects `engine_version`; DEV/GAME shared metadata stays synchronized | `SATISFIED_CURRENT` |
| V-COV-03 | Version/generation namespaces are normalized and current pre-release machine realization is complete | `SATISFIED_CURRENT`; B02 prevents false historical-gap classification |
| V-COV-04 | Released-v1.0+ compatibility remains multi-axis and exact-target-package-scoped; version/order/ancestry alone is not compatibility | `SATISFIED_CURRENT` architecture; WP-20 is sufficient for this consumer boundary on evidence reviewed so far |
| V-COV-05 | Explicit target-package migration edges/path support are required when released persistent state needs transformation | `IMPLEMENTATION_ONLY_OBLIGATION` / `DEFERRED_UNTIL_REALIZATION_OR_RELEASE`; current `1.0-alpha` state does not activate released-v1.0+ migration realization |
| V-COV-06 | Unsupported newer/ambiguous/missing compatibility evidence fails closed; no guessed migration/downgrade | `SATISFIED_CURRENT` architecture/runtime-policy projection |
| V-COV-07 | `release_status` is not silently promoted into a contradictory publication gate | `SATISFIED_CURRENT`; tag identity/lineage are the operative current release gates |
| V-COV-08 | WP-20 reopen | `OUT_OF_SCOPE` absent contradiction/unsatisfied consumer/owner insufficiency; no such reopen evidence found in Step 1 |

### 5.3 Lane C

| ID | Requirement / negative law | Current Step-1 disposition |
|---|---|---|
| L-COV-01 | Root legal payload has distributable `GAME/` copies | `SATISFIED_CURRENT` |
| L-COV-02 | Root/GAME legal file contents and `LICENSES/` file set must remain byte-identical at build time | `SATISFIED_CURRENT`; builder + executable negative test enforce it |
| L-COV-03 | Current declared SRD attribution is routed through `THIRD_PARTY_NOTICES.md` and `LICENSES/` and is shipped | `SATISFIED_CURRENT` for the currently declared license payload; Step 1 does not make a broader legal sufficiency opinion |
| L-COV-04 | Build-only DEV dependency files do not enter the all-`GAME` runtime merely because builder/test tooling uses them | `SATISFIED_CURRENT` package-boundary fact; no general legal conclusion is inferred from it |
| L-COV-05 | Release-facing source/provenance material has a defined public hygiene policy distinct from mandatory license/notice attribution | **`HUMAN_OWNED_MATERIAL_DECISION` / `ARCHITECTURE_GAP_OR_CONFLICT` — WP23-S1-F01** |
| L-COV-06 | External legal research / invention of new licensing policy | `OUT_OF_SCOPE` for Step 1 |

---

## 6. Cross-lane release-chain synthesis

### 6.1 Current chain

```text
repository source state
    |
    | V01/V02 + canonical version policy
    v
semantic engine identity + recommended tag
    |
    | release_builder / tag-mode workflow
    v
validated package composition from all valid GAME content
    + generated exact package provenance
    + external final ZIP digest
    |
    v
flat runtime artifact
    |
    | install/bootstrap package-shape + exact-root binding
    v
isolated selected runtime root
    |
    | WP-20 / ENGINE_UPDATES / MIGRATIONS compatibility law
    v
exact-package update/migration eligibility
    |
    | root <-> GAME legal-copy parity
    | plus every other distributable GAME provenance surface
    v
publishable-distributable boundary
```

The composition is materially stronger than any single lane: all-`GAME` passthrough means **every** runtime source file is automatically a release/legal/provenance consumer, including files that were originally created for development/source provenance rather than ordinary gameplay.

### 6.2 Cross-lane contradiction candidate — `WP23-S1-F01`

**Severity:** SIGNIFICANT for WP-23 architecture/readiness; not a product-release verdict.

Current evidence composes as follows:

1. `GAME/` is the exact source tree shipped by the runtime builder.
2. The builder deliberately packages all valid `GAME/` files automatically.
3. `GAME/CORE/SOURCES.md` contains source-specific named external development/research provenance beyond the formal license/notice payload.
4. `DEV/TOOLS/audit_engine.py` currently requires selected source-specific provenance anchors to remain present, so this is an actively maintained distributable contract, not accidental stale text.
5. Root/GAME `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md` and `LICENSES/` define and validate the formal legal/attribution payload, but current public owners reviewed in Step 1 do not define the final **release-facing provenance policy** for non-license development/research provenance in shipped runtime content.

Therefore local success in Lane A (package faithfully includes all `GAME/`) and Lane C (formal legal copies are identical) can compose into an unresolved public-provenance question.

This finding **cannot be mechanically closed inside Step 1** because the choice among retaining, sanitizing, relocating or removing such source-specific provenance is a material public-product/legal-provenance policy decision. Step 1 must not invent that policy.

The finding does **not** require a new WP. It is naturally inside WP-23 Lane C/cross-lane scope unless the Product Owner or Senior explicitly inserts a separate architecture unit.

Downstream blocked until resolved:

- final WP-23 legal/provenance readiness law;
- final release-content/provenance boundary;
- any later claim that a production distributable is legally/provenance-ready.

Not blocked:

- completion of this Step-1 framing evidence;
- independent Senior review of the Step-1 package.

### Exact Product Owner decision boundary

```text
For public distributable runtime content, may HDM retain source-specific named
external development/research provenance beyond license/notice-required or
otherwise explicitly approved attribution, or must such development provenance
be sanitized/removed/kept outside the shipped runtime while preserving only
approved attribution and independently stated HDM semantics?
```

No external legal conclusion is asserted here.

---

## 7. Negative findings and scope limits

Step-1 discovery found **no evidence** that:

- root and `GAME/` formal legal copies currently drift;
- the release builder uses a stale manual include list that can silently omit newly added valid `GAME/` files;
- source-repository ZIP/TAR snapshots are accepted as installable runtime packages;
- current version normalization is still unrealized;
- WP-20 must be reopened for its released-v1.0+ compatibility/migration semantics;
- `engine_version`, package provenance and final ZIP digest have collapsed into one identity;
- current pre-release state must already realize a released-v1.0+ migration transform graph;
- `release_status` is a hidden release-authorization gate contrary to current accepted release law;
- a real release, campaign migration or gameplay bootstrap was performed by this audit.

Step 1 also makes **no claim** that:

- the current branch is production-release-ready;
- a tag could or should be created now;
- all legal questions are resolved merely because formal copies are byte-identical;
- current source CI proves the future uploaded Release asset or ChatGPT Project environment;
- future released-v1.0+ migration support is implemented;
- WP-23 itself is complete.

---

## 8. Whole-project critic result and repaired framing

Mandatory critic artifact:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-step-1-whole-project-critic.md`

Mechanically resolved critic findings incorporated here:

```text
CR23-S1-01 SIGNIFICANT — release-facing provenance surface undercounted
    -> repaired by L08/L09, L-COV-05 and WP23-S1-F01

CR23-S1-02 SIGNIFICANT — historical version-realization wording could create a false current gap
    -> repaired by B02 and V-COV-03/V-COV-05 split

CR23-S1-03 SIGNIFICANT — package-builder evidence alone undercounted actual publication workflow consumer
    -> repaired by A03/A04 and A-COV-07/A-COV-08

CR23-S1-04 MINOR — all-GAME passthrough expansion risk was not explicit
    -> repaired by A12/A-COV-05 and cross-lane synthesis
```

Post-repair critic state:

```text
CRITIC_UNRESOLVED_BLOCKING: 0
CRITIC_UNRESOLVED_SIGNIFICANT: 0
CRITIC_UNRESOLVED_MINOR: 0
```

`WP23-S1-F01` is not an unrepaired Task-Brief defect; it is a material evidence finding exposed by the repaired framing.

---

## 9. Step-1 gate result

```text
WP23_PROBLEM_STATEMENT_COMPLETE: YES
WP23_DEPENDENCY_SUBGRAPH_RECONSTRUCTED: YES
WP23_SOURCE_MANIFEST_OPEN_WORLD_FOR_DISCOVERED_GRAPH: YES
LANE_A_ITEM_LEVEL_COVERAGE: COMPLETE FOR STEP-1 FRAMING
LANE_B_ITEM_LEVEL_COVERAGE: COMPLETE FOR STEP-1 FRAMING
LANE_C_ITEM_LEVEL_COVERAGE: COMPLETE FOR STEP-1 FRAMING
CROSS_LANE_SYNTHESIS_COMPLETE: YES
NEGATIVE_FINDINGS_RETAINED: YES
DEFERRED_OBLIGATIONS_DISTINGUISHED_FROM_CURRENT_GAPS: YES
WHOLE_PROJECT_STEP1_CRITIC_COMPLETE: YES
MECHANICALLY_RESOLVABLE_CRITIC_FINDINGS_REPAIRED: YES

UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT_EVIDENCE_FINDINGS: 1 — WP23-S1-F01
HUMAN_DECISION_REQUIRED: YES
UPSTREAM_WP20_REOPEN_REQUIRED: NO
NEW_WORKSTREAM_REQUIRED_BY_WORKER: NO

WP23_FRAMING_READY_FOR_INDEPENDENT_SENIOR_REVIEW: YES
WP23_READY_FOR_STEP2_GO: NO — PO provenance decision + Senior GO required
NEXT_AUTHORIZED_UNIT: NONE
```

STOP after publication for mandatory independent Senior review.
