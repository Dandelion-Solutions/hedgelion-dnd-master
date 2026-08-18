# GAME / DEV Release Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate HDM engine 0.8 to a physically separated `GAME/` runtime distribution tree and `DEV/` development tree, with a canonical deterministic runtime release builder and tag-triggered GitHub Release asset publication.

**Architecture:** `GAME/` is the exact source tree of the installed runtime package; the release ZIP contains the contents of `GAME/` at archive root. `DEV/` owns architecture, tests, release policy, development catalogs/schemas, Superpowers artifacts and all non-runtime tooling. Repository-root files remain only repository infrastructure/metadata. Runtime and development version metadata are split into unique `GAME/ENGINE_VERSION.yaml` and full-superset `DEV/ENGINE_DEVELOPMENT.yaml`.

**Tech Stack:** Python 3 standard library for runtime tooling; Python 3 + pinned `jsonschema` and `PyYAML` in an isolated DEV-tools environment; GitHub Actions for tag-triggered publication; GitHub Connector Git-data API for remote publication from ChatGPT/Codex.

**Spec:** `DEV/docs/superpowers/specs/2026-08-18-game-dev-release-boundary-design.md`, `DEV/docs/superpowers/specs/2026-08-18-engine-version-split-amendment.md`, `DEV/docs/superpowers/specs/2026-08-18-game-dev-boundary-audit-amendment.md`, `DEV/docs/superpowers/specs/2026-08-18-release-migration-safety-addendum.md`

## Global Constraints

- Engine release becomes `0.8`; recommended tag becomes `v0.8`; development work remains `release_status: development` until release preparation.
- `GAME/` is the package root in source; ZIP members are the contents of `GAME/`, with no `GAME/` wrapper.
- `GAME/` files never use `GAME/` as part of installed-package paths.
- Publishable campaign/storage templates are validated relative to their destination repository layouts.
- Exactly one tracked file is named `ENGINE_VERSION.yaml`: `GAME/ENGINE_VERSION.yaml`.
- `DEV/ENGINE_DEVELOPMENT.yaml` retains the complete current engine bookkeeping model.
- Current `CATALOG/` and plural `SCHEMAS/` are DEV-only until the mechanical runtime defines shipping forms.
- Deprecated `TEMPLATE/CAMPAIGN_MANIFEST.yaml` is removed.
- Runtime GAME contains installation/setup/templates/migrations/schema/runtime tools required to install and operate the game, but no development tests/audits/architecture/release tooling.
- Runtime package metadata is authoritative; runtime Markdown must not duplicate machine-authoritative repository/owner/version compatibility fields unnecessarily.
- Superpowers artifacts use only `DEV/docs/superpowers/specs/` and `DEV/docs/superpowers/plans/`; repository-root `docs/` is forbidden after cutover.
- Remote GitHub transport from ChatGPT/Codex is Connector-only; no manual Base64 for text.
- The large source-tree cutover is published as one coherent Git tree transition from a freshly verified parent.
- Runtime `GAME/TOOLS/init_campaign.py` remains standard-library-only.
- Release-builder YAML parsing is DEV-only and may use pinned PyYAML.
- Tag assets are immutable; an existing different same-name asset must not be clobbered.

---

### Task 1: Add RED migration/release regression tests

**Files:**
- Create: `DEV/TESTS/test_game_dev_layout.py`
- Create: `DEV/TESTS/test_release_builder.py`
- Move/update later in Task 6: current `TESTS/test_run_maintenance_audit.py`

**Interfaces:**
- Consumes: filesystem fixture roots passed as `pathlib.Path`.
- Produces: executable regression contract for root geometry, version projection, package validation, destination links, build-output safety and deterministic ZIP behavior.

- [ ] **Step 1: Write failing layout/version tests**

Create tests that assert a migrated fixture has exactly the approved source ownership, a unique `ENGINE_VERSION.yaml`, `DEV/ENGINE_DEVELOPMENT.yaml`, no root `docs/` or old root content trees, absent deprecated manifest stub, and matching shared version fields with GAME excluding all development revision counters.

- [ ] **Step 2: Write failing builder tests**

Tests must cover: archive root flattening; deterministic member order/metadata; output-inside-GAME rejection; symlink/case-collision/build-junk rejection; source-archive-shaped package rejection; embedded Project Instructions parity; package-relative and destination-relative Markdown link validation; immutable asset naming derived from `v0.8`; and development-status rejection in tag mode.

- [ ] **Step 3: Run RED tests**

Run:
```bash
python -m unittest DEV.TESTS.test_game_dev_layout DEV.TESTS.test_release_builder -v
```
Expected: failures because the migration helpers/builder and migrated layout do not yet exist.

---

### Task 2: Introduce shared DEV tool environment and canonical release builder

**Files:**
- Create: `DEV/TOOLS/dev_tool_environment.py`
- Create: `DEV/TOOLS/requirements-dev-tools.txt`
- Create: `DEV/TOOLS/release_builder.py`
- Create executable: `DEV/TOOLS/run_release_build`
- Later move/update: `TOOLS/run_maintenance_audit`, `TOOLS/audit_engine.py`
- Modify: `.gitignore`

**Interfaces:**
- `dev_tool_environment.ensure_environment(repo_root: Path) -> Path`
- `release_builder.build_release(repo_root: Path, output_dir: Path, intended_tag: str, tag_mode: bool) -> BuildResult`
- `BuildResult.runtime_zip: Path`
- `BuildResult.sha256_file: Path`
- `BuildResult.asset_name: str`

- [ ] **Step 1: Implement the minimum DEV environment required by RED tests**

Use one isolated `.hdm-devtools/venv`, fingerprinted by exact `requirements-dev-tools.txt` bytes plus Python major/minor. Pin `jsonschema==4.26.0` and a concrete PyYAML version. No global-environment fallback.

- [ ] **Step 2: Implement builder validation and deterministic ZIP generation**

Builder reads `DEV/ENGINE_DEVELOPMENT.yaml` and `GAME/ENGINE_VERSION.yaml`, validates the exact approved GAME projection/shared equality/tag coherence, validates source/destination links and package shape, then archives all GAME contents at ZIP root with deterministic ordering/timestamps/metadata and writes SHA-256 sidecar outside GAME.

- [ ] **Step 3: Implement `run_release_build` self-provisioning entry point**

The entry point resolves `REPO_ROOT`, provisions DEV dependencies itself, invokes `release_builder.py`, and prints machine-readable asset paths/names for the workflow. It rejects output paths under GAME.

- [ ] **Step 4: Run builder tests GREEN**

Run:
```bash
python -m unittest DEV.TESTS.test_release_builder -v
```
Expected: all builder-unit tests pass.

---

### Task 3: Prepare 0.8 GAME/DEV version metadata and runtime contract edits

**Files:**
- Create: `GAME/ENGINE_VERSION.yaml`
- Create: `DEV/ENGINE_DEVELOPMENT.yaml`
- Modify/move runtime files under `GAME/CORE/`, `GAME/INSTALL/`, `GAME/MIGRATIONS/`
- Remove: deprecated `GAME/TEMPLATE/CAMPAIGN_MANIFEST.yaml`

**Interfaces:**
- GAME manifest exact shared runtime fields: `engine_version`, `release_status`, `repository`, `engine_owner_login`, `rules_baseline`, `schema_version`, `campaign_update.compatibility`, `recommended_tag`.
- DEV manifest is the complete current superset with those shared fields set to 0.8/v0.8.

- [ ] **Step 1: Create the two version manifests**

GAME contains only runtime/package fields. DEV contains every prior bookkeeping field. Set `engine_version: 0.8`, `recommended_tag: v0.8`, keep `release_status: development` during implementation.

- [ ] **Step 2: Remove runtime duplicate authority**

Update bootstrap/runtime metadata so repository/owner/version compatibility authority comes from package `ENGINE_VERSION.yaml`; keep human-readable project naming only where it is prose, not a competing machine field.

- [ ] **Step 3: Rewrite runtime scope positively**

`PLAY_POLICY.md` must describe only package areas that actually exist in GAME and their activation boundaries; remove references to DEV-only directories/tools from runtime policy.

- [ ] **Step 4: Correct migration semantics**

Rewrite `MIGRATIONS/README.md` so engine updates migrate campaign data/schema/provenance only and never describe merging engine `main` into campaign branches.

- [ ] **Step 5: Update active custom-runtime-asset language**

Update GAME install/update instructions and related runtime text from GitHub-generated Source code ZIP to the custom runtime asset. Project Instructions validate archive-root shape before bootstrap.

- [ ] **Step 6: Keep embedded Project Instructions identical**

Make `GAME/INSTALL/README.md` embedded block byte/text-equivalent under the audit normalization rule to `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`.

---

### Task 4: Perform physical source-tree classification and move

**Files moved to GAME:**
- `CORE/` -> `GAME/CORE/`
- `RULES/` -> `GAME/RULES/`
- singular `SCHEMA/` -> `GAME/SCHEMA/`
- `CAMPAIGN/` -> `GAME/CAMPAIGN/`
- `TEMPLATE/` -> `GAME/TEMPLATE/` except deprecated manifest stub deleted
- `MIGRATIONS/` -> `GAME/MIGRATIONS/`
- `INSTALL/` -> `GAME/INSTALL/`
- `TOOLS/init_campaign.py` -> `GAME/TOOLS/init_campaign.py`
- runtime legal copies -> `GAME/LICENSE`, `GAME/NOTICE`, `GAME/THIRD_PARTY_NOTICES.md`, `GAME/LICENSES/`

**Files moved to DEV:**
- `ARCHITECTURE/` -> `DEV/ARCHITECTURE/`
- `TESTS/` -> `DEV/TESTS/`
- `RELEASE/` -> `DEV/RELEASE/`
- `CATALOG/` -> `DEV/CATALOG/`
- plural `SCHEMAS/` -> `DEV/SCHEMAS/`
- maintenance tools -> `DEV/TOOLS/`
- existing `docs/superpowers/` -> `DEV/docs/superpowers/`

**Repository-root retained:** `.github/`, `AGENTS.md`, `README.md`, `.gitignore`, canonical legal files/`LICENSES/`.

- [ ] **Step 1: Preserve bytes/modes for pure moves**

Use existing Git blob SHAs and modes when no content edit is required; do not round-trip unchanged text.

- [ ] **Step 2: Remove old root ownership paths in the same tree**

The resulting structural tree has no root `CORE`, `RULES`, `SCHEMA`, `CAMPAIGN`, `TEMPLATE`, `MIGRATIONS`, `INSTALL`, `TOOLS`, `ARCHITECTURE`, `TESTS`, `RELEASE`, `CATALOG`, `SCHEMAS`, `docs`, or root `ENGINE_VERSION.yaml`.

- [ ] **Step 3: Duplicate legal distribution files into GAME and validate equality**

Root legal files remain repository-canonical; GAME copies are standalone distribution copies and must match exactly.

---

### Task 5: Update repository instructions, active docs, release policy and GitHub workflow

**Files:**
- Modify: `AGENTS.md`
- Modify: root `README.md`
- Move/update: `DEV/RELEASE/CHECKLIST.md`, `DEV/RELEASE/VERSIONING.md`
- Create: `.github/workflows/release-runtime.yml`

**Interfaces:**
- `AGENTS.md` overrides Superpowers paths to `DEV/docs/superpowers/{specs,plans}/` and forbids root `docs/superpowers/`.
- GitHub workflow invokes one canonical release build entry point and publishes its returned assets.

- [ ] **Step 1: Update root AGENTS development geometry**

Change maintenance command to `DEV/TOOLS/run_maintenance_audit`; document REPO/GAME/DEV roots; preserve Connector-only/no-manual-Base64 policy; explicitly scope GitHub Actions as a separate token-backed execution surface; require Superpowers artifacts under DEV.

- [ ] **Step 2: Update root README source-browser links and installation wording**

Use custom runtime asset, link installation/runtime docs through `GAME/...`, development tests through `DEV/...`, and distinguish GitHub-generated source archives from installable runtime asset.

- [ ] **Step 3: Rewrite release checklist/versioning for custom assets and split manifests**

Checklist uses DEV manifest for release bookkeeping, GAME manifest for runtime projection, exact tag/build/archive verification, immutable assets and pre-tag candidate verification.

- [ ] **Step 4: Add thin tag workflow**

On `v*` tag push: checkout exact tag; set up Python; invoke `DEV/TOOLS/run_release_build --tag "$GITHUB_REF_NAME" --tag-mode ...`; get-or-create matching Release; upload runtime ZIP/checksum only if absent/identical; never clobber different bytes. Workflow contains no GAME include list or package-specific dependency install.

---

### Task 6: Migrate maintenance audit and tests to GAME/DEV semantics

**Files:**
- Move/modify: `DEV/TOOLS/audit_engine.py`
- Move/modify: `DEV/TOOLS/run_maintenance_audit`
- Move/modify: `DEV/TESTS/test_run_maintenance_audit.py`
- Modify active DEV regression documents where paths/contracts changed
- Preserve historical documents without rewriting their historical meaning

**Interfaces:**
- `REPO_ROOT`, `DEV_ROOT`, `GAME_ROOT` are explicit.
- Audit invokes exact `GAME/TOOLS/init_campaign.py` with `GAME_ROOT` as source root.

- [ ] **Step 1: Update launcher/environment tests RED**

Tests model `DEV/TOOLS/requirements-dev-tools.txt`, shared `.hdm-devtools/` cache and explicit repo/dev roots.

- [ ] **Step 2: Update maintenance launcher GREEN**

Reuse `dev_tool_environment.py`; maintenance entry point provisions shared DEV environment then launches audit.

- [ ] **Step 3: Rewrite audit source ownership semantics**

Audit GAME runtime files via GAME_ROOT, development catalogs/JSON schemas/tests/release docs via DEV_ROOT; forbid old root trees/docs; require unique runtime marker; remove old requirement for deprecated manifest stub; derive smoke engine tag from GAME version metadata.

- [ ] **Step 4: Add package/link/release checks to audit**

Audit manifest projection/coherence, Project Instructions parity, GAME build-junk/collision/symlink rules, destination-relative copied-template links, active DEV/root relative links, legal copy equality and generated release ZIP validation.

- [ ] **Step 5: Run maintenance/unit suite**

Run:
```bash
python -m unittest discover -s DEV/TESTS -v
DEV/TOOLS/run_maintenance_audit
```
Expected: all unit tests pass; maintenance audit exits 0.

---

### Task 7: Build and validate the actual 0.8 development runtime asset

**Files:** generated only under ignored `.hdm-release/` or temp output.

- [ ] **Step 1: Build through canonical entry point**

Run:
```bash
DEV/TOOLS/run_release_build --tag v0.8 --output .hdm-release/
```
This is pre-tag candidate mode while `release_status` is still development only if builder explicitly supports a development smoke mode; release-candidate/tag mode must remain unavailable until status is deliberately changed later in the release lifecycle.

- [ ] **Step 2: Inspect ZIP member layout**

Confirm `ENGINE_VERSION.yaml`, `CORE/`, `INSTALL/`, `TOOLS/init_campaign.py` are at archive root; `GAME/`, `DEV/`, `AGENTS.md`, development tests/tools are absent.

- [ ] **Step 3: Extract ZIP and run campaign-generator smoke test from extracted package**

Use extracted `TOOLS/init_campaign.py`; confirm generated campaign root layout and destination links/paths.

- [ ] **Step 4: Rebuild and compare SHA-256**

Build twice from same tree/parameters and require byte-identical ZIP/checksum.

---

### Task 8: Publish one coherent structural commit and verify remote state

**Files:** entire migration tree.

- [ ] **Step 1: Re-read feature branch HEAD through Connector immediately before write**

Expected parent is the latest verified design/plan commit; abort/reconcile if it moved.

- [ ] **Step 2: Build one Git tree from that parent**

Reuse original blob SHAs/modes for pure moves; use UTF-8 Connector blobs for edited/new text; delete old root paths in the same tree.

- [ ] **Step 3: Create one migration commit and non-force update feature ref**

Suggested commit message:
```text
feat: split GAME and DEV release trees for engine 0.8
```

- [ ] **Step 4: Verify remote feature HEAD and tree geometry**

Connector compare/fetch must show the new commit as HEAD and no forbidden old root trees.

- [ ] **Step 5: Re-run verification against the published tree**

Materialize/read the committed files through Connector as needed and repeat the unit/audit/build checks from Tasks 6–7 on the exact committed content before claiming completion.
