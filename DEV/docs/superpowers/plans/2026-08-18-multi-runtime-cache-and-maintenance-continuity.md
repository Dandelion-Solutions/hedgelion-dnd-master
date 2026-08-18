# Multi-runtime cache and maintenance continuity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Support multiple runtime ZIP versions per Project, portable campaign/storage runtime identity, silent compatible same-version refresh, creator-controlled semantic-version upgrades, transparent post-maintenance resume, and a one-hour durability ceiling for dirty HOT/SOFT state.

**Architecture:** Runtime ZIPs remain the durable package source; extracted packages are disposable, isolated by semantic version plus ZIP SHA-256, and bound through one ephemeral `current_runtime_root`. Runtime identity is persisted portably in `DND_STORAGE.yaml` for new-campaign baseline and `MANIFEST.yaml` for each campaign. The release builder injects one generated `RUNTIME_PACKAGE.yaml` provenance entry into the ZIP, while all other payload remains recursive passthrough of `GAME/`.

**Tech Stack:** Python 3.13, stdlib `zipfile/hashlib/subprocess/pathlib`, PyYAML in DEV tooling only, YAML runtime contracts, GitHub Connector/server-side compare, `unittest`, GitHub Actions.

**Spec:** `DEV/docs/superpowers/specs/2026-08-18-multi-runtime-cache-and-maintenance-continuity-design.md`, amended by `DEV/docs/superpowers/specs/2026-08-18-runtime-package-provenance-amendment.md` and `DEV/docs/superpowers/specs/2026-08-18-runtime-selection-and-storage-baseline-amendment.md`.

## Global Constraints

- Root `README.md` is human-curated and MUST NOT be edited without explicit owner instruction.
- No legacy/backward-compatibility work for the old campaign engine fields in this implementation cycle.
- Campaign canon remains only in campaign storage; engine files are never copied into campaign storage.
- Multiple `hedgelion-dnd-master-runtime-v<version>.zip` assets may coexist in Project Sources/current-chat attachments.
- Extracted runtime cache is disposable and never canonical.
- `current_runtime_root` is ephemeral and MUST NOT be persisted.
- Package-relative runtime reads after selection must remain inside one exact `current_runtime_root`.
- `RUNTIME_PACKAGE.yaml` exists only as a generated ZIP entry; it is never a tracked/staging worktree file.
- A semantic-version upgrade is creator-controlled; a proven descendant refresh within the same semantic version is silent.
- Storage baseline authority and campaign creator authority remain independent.
- No standalone cosmetic MANIFEST commit solely to refresh same-version provenance.
- Dirty HOT/SOFT state may not intentionally remain solely ephemeral beyond one hour of active work; clean state creates no heartbeat commit.
- Remote repository reads/writes use GitHub Connector only; no native remote Git.

---

### Task 1: Generated runtime package provenance

**Files:**
- Modify: `DEV/TOOLS/release_builder.py`
- Modify: `DEV/TESTS/test_release_builder.py`
- Modify: `DEV/TESTS/test_release_integration.py`
- Create: `DEV/TESTS/test_runtime_package_provenance.py`

**Interfaces:**
- Produces: `build_runtime_package_metadata(repo_root: Path, intended_tag: str, tag_mode: bool) -> dict`
- Produces: top-level ZIP member `RUNTIME_PACKAGE.yaml`
- Produces: `validate_runtime_package_metadata(data: dict) -> None`
- Existing `build_runtime_zip(...)` remains the package-composition authority.

- [ ] **Step 1: Write failing provenance tests**

Add tests that require:

```python
self.assertIn("RUNTIME_PACKAGE.yaml", zf.namelist())
meta = yaml.safe_load(zf.read("RUNTIME_PACKAGE.yaml"))
self.assertEqual(meta["schema_version"], 1)
self.assertEqual(meta["engine_version"], "0.8")
self.assertEqual(meta["package_id"], "v0.8")
self.assertEqual(meta["source_commit_sha"], expected_sha)
```

Also assert there is exactly one `RUNTIME_PACKAGE.yaml`, it is at archive root, and no tracked `GAME/RUNTIME_PACKAGE.yaml` is required.

- [ ] **Step 2: Run focused tests and verify RED**

Run in CI/full checkout:

```text
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_runtime_package_provenance -v
```

Expected: FAIL because the generated member/functions do not yet exist.

- [ ] **Step 3: Implement metadata classification**

Implement exact source states:

```python
{
    "schema_version": 1,
    "engine_version": str(game_manifest["engine_version"]),
    "package_id": intended_tag if tag_mode else development_package_id,
    "source_state": "tagged" | "clean_head" | "dirty_worktree" | "non_git",
    "source_ref": str | None,
    "source_commit_sha": str | None,
}
```

For `tagged`, require exact tag checkout and record the commit represented by the tag. For clean Git HEAD, record exact HEAD. For dirty worktree/non-Git, do not falsely claim exact source SHA.

- [ ] **Step 4: Inject deterministic YAML directly into ZIP**

Serialize with deterministic field ordering and UTF-8 bytes. Add exactly one root member after/among the sorted GAME members without creating a worktree file. Use the same deterministic timestamp/permission policy as other ZIP entries.

- [ ] **Step 5: Update package-root validation**

New-contract runtime packages require both:

```text
ENGINE_VERSION.yaml
RUNTIME_PACKAGE.yaml
```

with no `GAME/` or `DEV/` wrapper.

- [ ] **Step 6: Run focused + integration tests and verify GREEN**

Run:

```text
.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_runtime_package_provenance DEV.TESTS.test_release_integration -v
```

Expected: PASS.

- [ ] **Step 7: Commit**

Commit message:

```text
feat: embed runtime package provenance
```

---

### Task 2: Storage baseline v3 and campaign runtime identity schema

**Files:**
- Modify: `GAME/TEMPLATE/DND_STORAGE.yaml` if present, otherwise the exact storage-marker template/source used by bootstrap/generator
- Modify: `GAME/CAMPAIGN/MANIFEST.yaml`
- Modify: `GAME/SCHEMA/campaign_manifest.schema.yaml`
- Modify: `GAME/TOOLS/init_campaign.py`
- Modify/Create: applicable `DEV/TESTS/` manifest/generator tests

**Interfaces:**
- Storage `engine.baseline`: `version`, `package_id`, `source_commit_sha`, `package_sha256`, `adopted_at`
- Campaign `engine.created_with`: immutable `version`, `package_id`, `source_commit_sha`
- Campaign `engine.current`: `version`, `package_id`, `source_commit_sha`, `package_sha256`, `adopted_at`
- Campaign `engine.update_policy`: `ask|auto`

- [ ] **Step 1: Write failing schema/generator tests**

Require new campaign output matching:

```yaml
engine:
  created_with:
    version: "0.8"
    package_id: "v0.8"
    source_commit_sha: "<sha>"
  current:
    version: "0.8"
    package_id: "v0.8"
    source_commit_sha: "<sha>"
    package_sha256: "<digest>"
    adopted_at: "<timestamp>"
  update_policy: ask
```

Assert old `base_tag`, `base_sha`, `integrated_tag`, `integrated_main_sha` are absent from newly generated manifests.

- [ ] **Step 2: Verify RED**

Run the relevant generator/manifest tests and confirm failure is due to old engine fields.

- [ ] **Step 3: Update campaign template/schema**

Replace the old fields with the new nested objects. Preserve creator authority as Git-history-derived; do not add creator login as MANIFEST authority.

- [ ] **Step 4: Update `init_campaign.py` arguments/output**

Generator must receive/derive exact runtime identity from the validated package and emit both `created_with` and `current` equal at campaign creation. `created_with` is immutable thereafter.

- [ ] **Step 5: Update storage marker contract to v3**

Use:

```yaml
storage_format_version: 3
repository_role: campaign_storage
engine:
  baseline:
    version: "0.8"
    package_id: "v0.8"
    source_commit_sha: "<sha|null>"
    package_sha256: "<sha256>"
    adopted_at: "<timestamp>"
```

Do not persist environment paths.

- [ ] **Step 6: Verify GREEN**

Run focused schema/generator tests.

- [ ] **Step 7: Commit**

Commit message:

```text
feat: adopt portable runtime identity schema
```

---

### Task 3: Project Instructions and lazy multi-runtime package selection

**Files:**
- Modify: `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`
- Modify: `GAME/INSTALL/README.md` embedded Project Instructions block
- Modify: `GAME/INSTALL/00_DND_BOOTSTRAP.md`
- Modify: `GAME/CORE/BOOTSTRAP_RUNTIME.md`
- Modify/Create: applicable `DEV/TESTS/` bootstrap/project-instructions contract tests

**Interfaces:**
- Project Sources may contain multiple supported runtime ZIPs.
- `current_runtime_root = <session-cache>/hdm-runtime/<version>/<package_sha256>/`
- ZIP indexing may inspect filename + root `ENGINE_VERSION.yaml` + root `RUNTIME_PACKAGE.yaml` + SHA-256 without full extraction.

- [ ] **Step 1: Write failing text/contract tests**

Require Project Instructions to state that multiple runtime ZIPs may coexist, forbid eager extraction of all packages, and forbid assuming another chat's extracted cache survives.

Require bootstrap text to state that absent cache is silently re-extracted from the exact ZIP.

- [ ] **Step 2: Verify RED**

Run maintenance audit / focused contract tests; expected failure on the existing `exactly one ZIP` rule.

- [ ] **Step 3: Rewrite canonical Project Instructions minimally**

Replace the single-ZIP rule with supported multi-ZIP indexing. Preserve source-archive rejection, shape validation, no Base64, Connector-only campaign storage, and explicit campaign-choice gate.

- [ ] **Step 4: Regenerate/synchronize embedded block**

`GAME/INSTALL/README.md` must contain exactly the same canonical Project Instructions block as `PROJECT_INSTRUCTIONS.txt`.

- [ ] **Step 5: Implement runtime-root isolation contract in bootstrap prose**

After exact package selection, every package-relative read must resolve beneath one `current_runtime_root`; sibling caches are inert. Never globally search for a convenient `ENGINE_VERSION.yaml`, `CORE/`, or `TOOLS/init_campaign.py` after selection.

- [ ] **Step 6: Verify GREEN**

Run maintenance audit and parity tests.

- [ ] **Step 7: Commit**

Commit message:

```text
feat: support lazy multi-runtime bootstrap
```

---

### Task 4: Same-version refresh and semantic-version update policy

**Files:**
- Modify: `GAME/CORE/ENGINE_UPDATES.md`
- Modify: `GAME/CORE/BOOTSTRAP_RUNTIME.md`
- Modify: `GAME/INSTALL/00_DND_BOOTSTRAP.md`
- Create/Modify: applicable `DEV/TESTS/` policy regression cases

**Interfaces:**
- Semantic-version offer requires only version comparison plus available target ZIP.
- Same-version forward classification uses one bounded compare between recorded A and candidate B from `RUNTIME_PACKAGE.yaml`.
- Prompt state is ephemeral key `(campaign_identity, target_engine_version)`.

- [ ] **Step 1: Write failing policy tests**

Require these creator choices for a newer semantic version:

```text
1. Update now
2. Remind later
3. Do not remind about this version
```

Require `Remind later` = 24-hour current-environment suppression and `Do not remind` = current-environment suppression for only that campaign+target version.

- [ ] **Step 2: Write failing same-version classification tests/contracts**

Require:

```text
A == B + same digest -> exact
A == B + different digest -> suspicious
A ancestor B -> silent forward refresh
B ancestor A -> downgrade, no silent use
A diverged B -> ambiguous
null provenance -> no automatic ancestry classification
```

- [ ] **Step 3: Verify RED**

Run focused tests/contracts.

- [ ] **Step 4: Update engine-update authority**

Campaign creator controls campaign engine adoption. Storage owner controls only storage baseline. Repository write permission alone grants neither.

- [ ] **Step 5: Add prompt suppression semantics**

Explicitly keep reminder/suppression state out of Git, Memory, engine files, and campaign canon. It may vanish with the environment.

- [ ] **Step 6: Add silent same-version refresh semantics**

A unique proven descendant candidate is preferred over the old exact-digest candidate. Creator MANIFEST provenance refresh joins the next normal coherent transaction; non-creator may use compatible forward runtime but cannot persist MANIFEST changes.

- [ ] **Step 7: Verify GREEN**

Run focused policy tests and maintenance audit.

- [ ] **Step 8: Commit**

Commit message:

```text
feat: distinguish runtime refresh from engine upgrade
```

---

### Task 5: Mismatch recovery UX

**Files:**
- Modify: `GAME/INSTALL/00_DND_BOOTSTRAP.md`
- Modify: `GAME/CORE/BOOTSTRAP_RUNTIME.md`
- Modify: `GAME/CORE/ENGINE_UPDATES.md`
- Modify/Create: applicable regression-case docs/tests

**Interfaces:**
- Exact/current-version ZIP present -> select/re-extract automatically.
- Exact/current-version ZIP absent + non-creator -> request matching ZIP only.
- Exact/current-version ZIP absent + creator -> offer restore matching version OR update to available newer semantic version.

- [ ] **Step 1: Add failing regression cases**

Cases must assert the runtime never stops at a bare "cannot continue" when a valid restore/update path exists.

- [ ] **Step 2: Verify RED**

Run focused policy/audit checks.

- [ ] **Step 3: Implement player-facing decision flow**

Keep messages concise and action-oriented. Missing extracted cache is never player-facing; missing required ZIP is.

- [ ] **Step 4: Verify GREEN**

Run focused cases + audit.

- [ ] **Step 5: Commit**

Commit message:

```text
feat: add engine mismatch recovery paths
```

---

### Task 6: Transparent post-maintenance gameplay continuation

**Files:**
- Modify: `GAME/CORE/SESSION.md`
- Modify: `GAME/CORE/RUNTIME.md`
- Modify: `GAME/CORE/BOOTSTRAP_RUNTIME.md`
- Modify: `GAME/CORE/ENGINE_UPDATES.md`
- Modify/Create: applicable `DEV/TESTS/` regression cases

**Interfaces:**
- Ephemeral continuation frame: selected campaign, durable frontier, scene/location, last meaningful player action, last meaningful Master/NPC utterance/outcome, unresolved decision point.

- [ ] **Step 1: Write failing continuation regression cases**

Require a successful maintenance flow to return to the same unresolved gameplay point rather than end with only a maintenance status.

Require exact quotes only when current-chat evidence contains them; otherwise use durable semantic summary.

- [ ] **Step 2: Verify RED**

Run focused policy tests.

- [ ] **Step 3: Add continuation-frame contract**

Capture before refresh/migration, switch runtime atomically, invalidate/reload exact CORE, then restore the same gameplay point. Maintenance itself must not advance fictional time.

- [ ] **Step 4: Verify GREEN**

Run focused cases + audit.

- [ ] **Step 5: Commit**

Commit message:

```text
feat: resume gameplay after engine maintenance
```

---

### Task 7: One-hour dirty HOT/SOFT durability ceiling

**Files:**
- Modify: `GAME/CORE/DURABILITY_GUARD.md`
- Modify: `GAME/CORE/PERSISTENCE.md`
- Modify: `GAME/CORE/SESSION.md`
- Modify: `GAME/CORE/RUNTIME.md`
- Modify/Create: applicable durability regression cases under `DEV/TESTS/`

**Interfaces:**
- Forced boundary condition: `dirty_hot_or_soft && now - durable_frontier_time >= 1 hour`.
- No-op/heartbeat commit prohibited when no dirty canonical state exists.

- [ ] **Step 1: Write failing durability cases**

Require:

```text
dirty + durable frontier >= 1h old -> forced coherent publication boundary
clean + frontier >= 1h old -> no commit
inactive chat >1h -> re-evaluate on next interaction; no background promise
lost ephemeral state -> recover only durable canon, never invent lost unpublished canon
```

- [ ] **Step 2: Verify RED**

Run focused durability tests/cases.

- [ ] **Step 3: Update durability authority**

Make the one-hour ceiling additive to immediate critical-event and existing batching rules. It does not replace stronger boundaries.

- [ ] **Step 4: Update session/runtime startup behavior**

At the next interaction after a long gap, check stale dirty state before applying a new gameplay action when the dirty working set still exists.

- [ ] **Step 5: Verify GREEN**

Run focused durability cases + audit.

- [ ] **Step 6: Commit**

Commit message:

```text
feat: cap dirty hot state at one hour
```

---

### Task 8: Full consistency audit and release-package verification

**Files:**
- Modify: `DEV/TOOLS/audit_engine.py` only if new invariants are not already covered by tests
- Modify: `DEV/RELEASE/CHECKLIST.md`
- Modify/Create: `DEV/TESTS/` cross-cutting consistency tests
- Do NOT modify root `README.md`

**Interfaces:**
- Full source audit + full unittest suite are completion gates.
- Built runtime ZIP must contain all valid GAME files plus exactly one generated provenance manifest.

- [ ] **Step 1: Add cross-cutting RED tests**

Cover at minimum:

```text
multiple Project runtime ZIP contract
storage baseline v3 object
new campaign engine schema only
RUNTIME_PACKAGE required in built artifact
no tracked RUNTIME_PACKAGE.yaml in GAME
runtime-root isolation language
creator/storage authority separation
same-version silent descendant refresh
semantic-version reminder choices
maintenance continuation
one-hour dirty ceiling/no heartbeat
```

- [ ] **Step 2: Verify RED where gaps remain**

Run full audit + suite and inspect only genuine failures.

- [ ] **Step 3: Close any implementation gaps minimally**

Do not broaden scope into legacy migration or unrelated mechanical-runtime roadmap work.

- [ ] **Step 4: Build runtime ZIP twice from full checkout**

Run canonical launcher twice and verify deterministic bytes for unchanged source state. Inspect the ZIP root for `ENGINE_VERSION.yaml`, `RUNTIME_PACKAGE.yaml`, flattened GAME contents, and no DEV tree.

- [ ] **Step 5: Run generator smoke from extracted ZIP**

Use the extracted package's exact `TOOLS/init_campaign.py`; verify emitted campaign manifest uses only the new engine schema.

- [ ] **Step 6: Run full verification**

Run:

```text
DEV/TOOLS/run_maintenance_audit
.hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -v
```

Expected: all GREEN.

- [ ] **Step 7: Update release checklist**

Document multiple runtime assets, generated provenance, portable storage/campaign identity, and current builder behavior. Do not touch root README.

- [ ] **Step 8: Commit**

Commit message:

```text
test: verify multi-runtime maintenance contracts
```

---

## Self-review

- Spec coverage: all parent-spec sections and both amendments map to Tasks 1–8; legacy migration is explicitly excluded.
- Placeholder scan: no TBD/TODO/future implementation placeholders.
- Type/naming consistency: `version`, `package_id`, `source_commit_sha`, `package_sha256`, `adopted_at`, `created_with`, `current`, and `engine.baseline` match the approved amendments.
- Root README remains outside implementation scope.
- The plan preserves the distinction between semantic-version upgrade prompts and silent same-version descendant refreshes.
