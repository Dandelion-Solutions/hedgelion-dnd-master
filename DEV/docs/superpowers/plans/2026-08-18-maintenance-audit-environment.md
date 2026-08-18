# Maintenance Audit Environment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one repository-native `TOOLS/run_maintenance_audit` command that self-bootstraps and reuses an isolated maintenance virtual environment before running `TOOLS/audit_engine.py`.

**Architecture:** The launcher is a standard-library-only executable Python script. It owns `.hdm-maintenance/venv`, fingerprints the exact `requirements-maintenance.txt` bytes plus bootstrap Python major/minor, rebuilds only when that fingerprint is invalid, and delegates the real consistency audit to the venv Python. Automated tests use only `unittest`/`unittest.mock`; remote repository reads/writes continue to use the GitHub Connector, while local Git is permitted only for local inspection/conflict/status work under root `AGENTS.md`.

**Tech Stack:** Python standard library (`venv`, `hashlib`, `json`, `pathlib`, `subprocess`, `shutil`), `unittest`, existing `jsonschema==4.26.0` maintenance dependency.

## Global Constraints

- This is development-maintenance infrastructure only; do not alter gameplay architecture, gameplay Project Instructions, `INSTALL/00_DND_BOOTSTRAP.md`, CORE runtime policy, campaign schemas, or campaign behavior.
- Canonical command: `TOOLS/run_maintenance_audit`.
- Do not install maintenance dependencies globally.
- Do not introduce Docker, Poetry, `uv`, `pipx`, a service, or a general task runner.
- `.hdm-maintenance/` is an ignored rebuildable cache, never authoritative project state.
- A valid cache requires both the exact SHA-256 of `requirements-maintenance.txt` and the bootstrap Python major/minor tuple.
- Warm runs with a valid fingerprint must not invoke pip installation.
- Requirements or Python major/minor changes must cause a clean environment rebuild.
- Dependency-install failures must remain visible and must not produce a success fingerprint or run the audit.
- Audit failures after successful preparation must propagate the audit exit code unchanged.
- Remote GitHub transport is Connector-only. Do not use `git fetch`, `git pull`, `git push`, `git ls-remote`, `gh`, direct GitHub HTTP, or credential workarounds.

---

## File Structure

- Create `TOOLS/run_maintenance_audit` — canonical executable launcher and environment lifecycle owner.
- Create `TESTS/test_run_maintenance_audit.py` — stdlib automated tests for fingerprinting, cold/warm behavior, invalidation, failure semantics, and audit exit propagation.
- Create `.gitignore` — ignore `.hdm-maintenance/`.
- Modify `TOOLS/audit_engine.py` — point missing-dependency diagnostics to the canonical launcher.
- Modify `RELEASE/CHECKLIST.md` — replace manual install + direct audit with the canonical launcher.
- Modify `AGENTS.md` — require development agents to invoke the canonical launcher for the maintenance audit.

## Task 1: Build the deterministic launcher core with fingerprint/cache tests

**Files:**
- Create: `TOOLS/run_maintenance_audit`
- Create: `TESTS/test_run_maintenance_audit.py`
- Create: `.gitignore`

**Interfaces:**
- `compute_fingerprint(requirements_path: Path, python_version: tuple[int, int]) -> dict[str, str]`
- `venv_python_path(venv_dir: Path) -> Path`
- `load_fingerprint(path: Path) -> dict[str, str] | None`
- `cache_is_current(venv_dir: Path, fingerprint_path: Path, expected: dict[str, str]) -> bool`
- `rebuild_environment(root: Path, expected: dict[str, str]) -> Path`
- `main() -> int`

- [ ] **Step 1: Add failing fingerprint/cache tests using stdlib unittest**

Create `TESTS/test_run_maintenance_audit.py` with a loader for the extensionless Python launcher and tests equivalent to:

```python
from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "TOOLS" / "run_maintenance_audit"


def load_launcher():
    loader = importlib.machinery.SourceFileLoader("hdm_run_maintenance_audit", str(LAUNCHER))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class MaintenanceAuditLauncherTests(unittest.TestCase):
    def test_fingerprint_changes_with_requirements_bytes_and_python_version(self):
        m = load_launcher()
        with tempfile.TemporaryDirectory() as td:
            req = Path(td) / "requirements-maintenance.txt"
            req.write_bytes(b"jsonschema==4.26.0\n")
            a = m.compute_fingerprint(req, (3, 13))
            req.write_bytes(b"jsonschema==4.27.0\n")
            b = m.compute_fingerprint(req, (3, 13))
            c = m.compute_fingerprint(req, (3, 14))
            self.assertNotEqual(a, b)
            self.assertNotEqual(b, c)
            self.assertEqual(a["python"], "3.13")

    def test_cache_is_current_requires_python_and_exact_fingerprint(self):
        m = load_launcher()
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            venv_dir = base / "venv"
            py = m.venv_python_path(venv_dir)
            py.parent.mkdir(parents=True)
            py.write_text("", encoding="utf-8")
            fp = base / "fingerprint.json"
            expected = {"requirements_sha256": "abc", "python": "3.13"}
            fp.write_text(json.dumps(expected), encoding="utf-8")
            self.assertTrue(m.cache_is_current(venv_dir, fp, expected))
            self.assertFalse(m.cache_is_current(venv_dir, fp, {**expected, "python": "3.14"}))
```

- [ ] **Step 2: Run the focused tests and confirm RED**

Run:

```bash
python3 -m unittest TESTS.test_run_maintenance_audit -v
```

Expected: import/load failure because `TOOLS/run_maintenance_audit` does not yet exist.

- [ ] **Step 3: Implement the minimal launcher core**

Create executable `TOOLS/run_maintenance_audit` beginning with:

```python
#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / ".hdm-maintenance"
VENV_DIR = CACHE_DIR / "venv"
FINGERPRINT_PATH = CACHE_DIR / "fingerprint.json"
REQUIREMENTS = ROOT / "requirements-maintenance.txt"
AUDIT = ROOT / "TOOLS" / "audit_engine.py"


def compute_fingerprint(requirements_path: Path, python_version: tuple[int, int]) -> dict[str, str]:
    digest = hashlib.sha256(requirements_path.read_bytes()).hexdigest()
    return {
        "requirements_sha256": digest,
        "python": f"{python_version[0]}.{python_version[1]}",
    }


def venv_python_path(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def load_fingerprint(path: Path) -> dict[str, str] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None
    if not isinstance(value, dict):
        return None
    return value


def cache_is_current(venv_dir: Path, fingerprint_path: Path, expected: dict[str, str]) -> bool:
    return venv_python_path(venv_dir).is_file() and load_fingerprint(fingerprint_path) == expected
```

Add `.gitignore` containing exactly:

```gitignore
.hdm-maintenance/
```

Do not implement installation/audit behavior beyond what is needed for the current tests yet.

- [ ] **Step 4: Run focused tests and confirm GREEN**

Run:

```bash
python3 -m unittest TESTS.test_run_maintenance_audit -v
```

Expected: fingerprint/cache tests pass.

- [ ] **Step 5: Verify ignore behavior locally**

Run from a valid local checkout:

```bash
mkdir -p .hdm-maintenance/venv
: > .hdm-maintenance/probe

git status --short
git check-ignore -v .hdm-maintenance/probe
```

Expected: `.hdm-maintenance/probe` is ignored and does not appear in `git status --short`.

- [ ] **Step 6: Publish Task 1 through the GitHub Connector**

Before publication, re-read the target branch HEAD through the Connector. Publish `TOOLS/run_maintenance_audit`, `TESTS/test_run_maintenance_audit.py`, and `.gitignore` as one commit based on the verified parent. Do not use native Git as remote transport. Verify the resulting branch ref through the Connector.

Suggested commit message:

```text
Add maintenance audit environment launcher core
```

## Task 2: Add cold bootstrap, warm reuse, invalidation, and failure semantics

**Files:**
- Modify: `TOOLS/run_maintenance_audit`
- Modify: `TESTS/test_run_maintenance_audit.py`

**Interfaces:**
- `rebuild_environment(root: Path, expected: dict[str, str], *, builder_factory=venv.EnvBuilder, runner=subprocess.run) -> Path`
- `ensure_environment(root: Path, *, python_version: tuple[int, int] | None = None, builder_factory=venv.EnvBuilder, runner=subprocess.run) -> Path`
- `run_audit(venv_python: Path, *, runner=subprocess.run) -> int`
- `main() -> int`

- [ ] **Step 1: Add failing lifecycle tests**

Extend `TESTS/test_run_maintenance_audit.py` with tests that inject a fake venv builder and runner, including these behaviors:

```python
from unittest import mock


def test_warm_cache_skips_builder_and_pip(self):
    m = load_launcher()
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "requirements-maintenance.txt").write_text("jsonschema==4.26.0\n", encoding="utf-8")
        cache = root / ".hdm-maintenance"
        venv_dir = cache / "venv"
        py = m.venv_python_path(venv_dir)
        py.parent.mkdir(parents=True)
        py.write_text("", encoding="utf-8")
        expected = m.compute_fingerprint(root / "requirements-maintenance.txt", (3, 13))
        cache.mkdir(exist_ok=True)
        (cache / "fingerprint.json").write_text(json.dumps(expected), encoding="utf-8")
        builder = mock.Mock()
        runner = mock.Mock()
        result = m.ensure_environment(root, python_version=(3, 13), builder_factory=builder, runner=runner)
        self.assertEqual(result, py)
        builder.assert_not_called()
        runner.assert_not_called()


def test_requirements_change_rebuilds_before_writing_fingerprint(self):
    m = load_launcher()
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        req = root / "requirements-maintenance.txt"
        req.write_text("jsonschema==4.26.0\n", encoding="utf-8")
        cache = root / ".hdm-maintenance"
        cache.mkdir()
        (cache / "fingerprint.json").write_text(
            json.dumps({"requirements_sha256": "old", "python": "3.13"}), encoding="utf-8"
        )
        created = []
        class FakeBuilder:
            def __init__(self, **kwargs):
                pass
            def create(self, path):
                created.append(Path(path))
                py = m.venv_python_path(Path(path))
                py.parent.mkdir(parents=True)
                py.write_text("", encoding="utf-8")
        runner = mock.Mock(return_value=mock.Mock(returncode=0))
        py = m.ensure_environment(root, python_version=(3, 13), builder_factory=FakeBuilder, runner=runner)
        self.assertEqual(created, [root / ".hdm-maintenance" / "venv"])
        self.assertEqual(runner.call_count, 1)
        self.assertEqual(json.loads((cache / "fingerprint.json").read_text()), m.compute_fingerprint(req, (3, 13)))
        self.assertEqual(py, m.venv_python_path(cache / "venv"))


def test_pip_failure_leaves_no_success_fingerprint_and_does_not_run_audit(self):
    m = load_launcher()
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "requirements-maintenance.txt").write_text("jsonschema==4.26.0\n", encoding="utf-8")
        class FakeBuilder:
            def __init__(self, **kwargs):
                pass
            def create(self, path):
                py = m.venv_python_path(Path(path))
                py.parent.mkdir(parents=True)
                py.write_text("", encoding="utf-8")
        runner = mock.Mock(return_value=mock.Mock(returncode=7))
        with self.assertRaises(m.PreparationError) as cm:
            m.ensure_environment(root, python_version=(3, 13), builder_factory=FakeBuilder, runner=runner)
        self.assertEqual(cm.exception.exit_code, 7)
        self.assertFalse((root / ".hdm-maintenance" / "fingerprint.json").exists())
```

Also add tests that Python `(3, 13)` -> `(3, 14)` invalidates the cache and that `run_audit()` returns the child audit return code unchanged.

- [ ] **Step 2: Run focused tests and confirm RED**

Run:

```bash
python3 -m unittest TESTS.test_run_maintenance_audit -v
```

Expected: failures because environment preparation and audit delegation are not yet implemented.

- [ ] **Step 3: Implement lifecycle behavior**

Implement a small typed preparation failure and the lifecycle functions:

```python
class PreparationError(RuntimeError):
    def __init__(self, message: str, exit_code: int = 2):
        super().__init__(message)
        self.exit_code = exit_code


def rebuild_environment(
    root: Path,
    expected: dict[str, str],
    *,
    builder_factory=venv.EnvBuilder,
    runner=subprocess.run,
) -> Path:
    cache_dir = root / ".hdm-maintenance"
    venv_dir = cache_dir / "venv"
    fingerprint_path = cache_dir / "fingerprint.json"
    requirements = root / "requirements-maintenance.txt"

    cache_dir.mkdir(parents=True, exist_ok=True)
    if venv_dir.exists():
        shutil.rmtree(venv_dir)
    try:
        builder_factory(with_pip=True, clear=True).create(venv_dir)
    except Exception as exc:
        raise PreparationError(f"virtual environment creation failed: {exc}") from exc

    py = venv_python_path(venv_dir)
    cp = runner([str(py), "-m", "pip", "install", "-r", str(requirements)])
    if cp.returncode != 0:
        fingerprint_path.unlink(missing_ok=True)
        raise PreparationError(
            f"maintenance dependency installation failed (exit {cp.returncode})",
            cp.returncode,
        )

    tmp = fingerprint_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(expected, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(fingerprint_path)
    return py


def ensure_environment(
    root: Path,
    *,
    python_version: tuple[int, int] | None = None,
    builder_factory=venv.EnvBuilder,
    runner=subprocess.run,
) -> Path:
    version = python_version or (sys.version_info.major, sys.version_info.minor)
    expected = compute_fingerprint(root / "requirements-maintenance.txt", version)
    venv_dir = root / ".hdm-maintenance" / "venv"
    fingerprint_path = root / ".hdm-maintenance" / "fingerprint.json"
    if cache_is_current(venv_dir, fingerprint_path, expected):
        return venv_python_path(venv_dir)
    return rebuild_environment(root, expected, builder_factory=builder_factory, runner=runner)


def run_audit(venv_python: Path, *, runner=subprocess.run) -> int:
    return runner([str(venv_python), str(AUDIT)]).returncode


def main() -> int:
    try:
        py = ensure_environment(ROOT)
    except PreparationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return exc.exit_code
    return run_audit(py)


if __name__ == "__main__":
    raise SystemExit(main())
```

Important behavior: do not capture pip stderr/stdout. Let pip's meaningful DNS/TLS/index/resolution error remain visible, with only one concise launcher-level `ERROR:` line added after failure.

- [ ] **Step 4: Run focused tests and confirm GREEN**

Run:

```bash
python3 -m unittest TESTS.test_run_maintenance_audit -v
```

Expected: all launcher tests pass.

- [ ] **Step 5: Exercise a real no-network/invalid-index failure without touching global Python**

From a disposable copy or with `.hdm-maintenance/` removed, run:

```bash
PIP_INDEX_URL=http://127.0.0.1:9/simple PIP_RETRIES=0 TOOLS/run_maintenance_audit
```

Expected:
- non-zero exit;
- pip connection/index failure remains visible;
- launcher prints `ERROR: maintenance dependency installation failed ...`;
- `.hdm-maintenance/fingerprint.json` is absent;
- audit success text is absent.

Then remove the partial cache before subsequent verification:

```bash
rm -rf .hdm-maintenance
```

- [ ] **Step 6: Publish Task 2 through the GitHub Connector**

Re-read current remote HEAD through the Connector immediately before publication. Publish launcher + tests in one commit based on the current parent. Verify resulting remote ref through the Connector.

Suggested commit message:

```text
Complete maintenance audit environment lifecycle
```

## Task 3: Make the launcher canonical in development/release guidance

**Files:**
- Modify: `TOOLS/audit_engine.py`
- Modify: `RELEASE/CHECKLIST.md`
- Modify: `AGENTS.md`
- Test: `TESTS/test_run_maintenance_audit.py`

**Interfaces:**
- Human/agent canonical entry point remains exactly `TOOLS/run_maintenance_audit`.
- Direct `python TOOLS/audit_engine.py` remains executable but is no longer the documented normal workflow.

- [ ] **Step 1: Add failing documentation-contract tests**

Extend `TESTS/test_run_maintenance_audit.py` with repository-text assertions:

```python
def test_repository_guidance_uses_canonical_launcher(self):
    audit = (ROOT / "TOOLS" / "audit_engine.py").read_text(encoding="utf-8")
    release = (ROOT / "RELEASE" / "CHECKLIST.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    self.assertIn("TOOLS/run_maintenance_audit", audit)
    self.assertIn("TOOLS/run_maintenance_audit", release)
    self.assertIn("TOOLS/run_maintenance_audit", agents)
    self.assertNotIn("Maintenance dependencies installed with `python -m pip install -r requirements-maintenance.txt`", release)
```

- [ ] **Step 2: Run the contract test and confirm RED**

Run:

```bash
python3 -m unittest TESTS.test_run_maintenance_audit.MaintenanceAuditLauncherTests.test_repository_guidance_uses_canonical_launcher -v
```

Expected: failure because current guidance still points to manual pip/direct audit.

- [ ] **Step 3: Update `TOOLS/audit_engine.py` guidance only**

Change its module docstring from the manual install instruction to wording equivalent to:

```text
Run this audit through `TOOLS/run_maintenance_audit`, which prepares the isolated
maintenance environment and then executes this script. Exits non-zero on
normative contradictions, invalid JSON Schema/catalog data, or scaffold smoke
failure.
```

Change the `ImportError` diagnostic to:

```python
print(
    "ERROR: missing maintenance dependency 'jsonschema'; "
    "run: TOOLS/run_maintenance_audit",
    file=sys.stderr,
)
```

Do not change audit logic.

- [ ] **Step 4: Update release checklist**

Replace the two current regression checklist entries:

```text
- [ ] Maintenance dependencies installed with `python -m pip install -r requirements-maintenance.txt`.
- [ ] In explicit engine-maintenance/release mode, `python TOOLS/audit_engine.py` passes on the exact release tree.
```

with one canonical entry:

```text
- [ ] In explicit engine-maintenance/release mode, `TOOLS/run_maintenance_audit` prepares/reuses the isolated maintenance environment and passes on the exact release tree.
```

- [ ] **Step 5: Update development agent instructions**

Add a development-only section to root `AGENTS.md`, near other development operating rules:

```markdown
## Maintenance audit environment

For the HDM engine maintenance consistency audit, use exactly:

```text
TOOLS/run_maintenance_audit
```

Do not invoke `python TOOLS/audit_engine.py` as the normal audit workflow and do
not install `requirements-maintenance.txt` into the system Python. The launcher
owns the ignored `.hdm-maintenance/` virtual environment, dependency fingerprint,
and rebuild/reuse decision.

If dependency installation fails because package-index/network access is
unavailable, report that actual failure. Do not switch to global installation or
another package manager as a workaround.
```

Keep this section development-only; do not copy it into gameplay Project Instructions, bootstrap, or CORE runtime context.

- [ ] **Step 6: Run the complete stdlib test suite for the launcher**

Run:

```bash
python3 -m unittest TESTS.test_run_maintenance_audit -v
```

Expected: all tests pass.

- [ ] **Step 7: Run real cold and warm audits where package-index access is available**

Cold run:

```bash
rm -rf .hdm-maintenance
TOOLS/run_maintenance_audit
```

Expected:
- venv created;
- pinned dependencies installed;
- fingerprint written;
- `OK: engine consistency audit passed`.

Verify pinned version:

```bash
.hdm-maintenance/venv/bin/python -c 'import jsonschema; print(jsonschema.__version__)'
```

Expected: `4.26.0` (or use `importlib.metadata.version("jsonschema")` if the package deprecates `__version__`).

Warm run:

```bash
TOOLS/run_maintenance_audit
```

Expected: successful audit without pip-install output and without rebuilding the venv.

If the current execution phase has no package-index access, do not claim the cold real-install check passed. Record the network limitation and rely on the deterministic unit tests plus the explicit invalid-index failure test until the command is run in an environment/setup phase with package access.

- [ ] **Step 8: Verify requirements invalidation in a disposable working copy**

In a disposable local copy, save the original requirements, append a harmless comment (comments change exact bytes and therefore must invalidate the fingerprint), run the launcher, and confirm rebuild occurs:

```bash
cp requirements-maintenance.txt /tmp/requirements-maintenance.txt.hdm-backup
printf '\n# fingerprint-invalidation-test\n' >> requirements-maintenance.txt
TOOLS/run_maintenance_audit
mv /tmp/requirements-maintenance.txt.hdm-backup requirements-maintenance.txt
rm -rf .hdm-maintenance
```

Expected: fingerprint changes and pip preparation is attempted again before audit. Never publish the temporary requirements edit.

- [ ] **Step 9: Verify Git cleanliness**

Run:

```bash
git status --short
git check-ignore -v .hdm-maintenance/venv
```

Expected: `.hdm-maintenance/` is ignored; only intentional source/doc/test changes appear.

- [ ] **Step 10: Publish Task 3 through the GitHub Connector**

Re-read remote HEAD through the Connector, publish only `TOOLS/audit_engine.py`, `RELEASE/CHECKLIST.md`, `AGENTS.md`, and the test update, and verify the resulting remote branch ref. Do not modify gameplay instructions/bootstrap/CORE.

Suggested commit message:

```text
Make maintenance audit launcher canonical
```

## Final Verification Gate

Before claiming completion, invoke `superpowers:verification-before-completion` and gather fresh evidence for each applicable item:

```bash
python3 -m unittest TESTS.test_run_maintenance_audit -v
TOOLS/run_maintenance_audit
git status --short
git check-ignore -v .hdm-maintenance/venv
```

Also verify through the GitHub Connector that:

- the target branch contains the intended files and commits;
- no gameplay Project Instructions, `INSTALL/00_DND_BOOTSTRAP.md`, or CORE runtime files changed;
- remote HEAD is the commit being reported;
- published diffs contain no temporary requirements mutation or `.hdm-maintenance/` contents.

If package-index access prevents the real cold audit in the current execution phase, state that limitation precisely rather than converting the unit-test result into an end-to-end success claim.
