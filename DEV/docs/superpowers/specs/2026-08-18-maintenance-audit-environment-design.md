# Maintenance Audit Environment Design

## Status

Approved design direction: repository-local self-bootstrap launcher for HDM development maintenance.

This design is development infrastructure only. It MUST NOT alter gameplay architecture, gameplay bootstrap, campaign runtime, or campaign persistence behavior.

## Problem

`TOOLS/requirements-maintenance.txt` pins maintenance-only dependencies, currently including `jsonschema==4.26.0`, while `TOOLS/audit_engine.py` is normally launched with whichever `python` happens to be selected by the environment.

That makes the audit depend on incidental interpreter state. A Work/Codex/scratch environment can be recreated, a previously prepared virtual environment can disappear, and another Python on `PATH` may not have the maintenance dependencies installed. Requiring a human or agent to rediscover a usable Python, create a virtual environment, install dependencies, remember its path, and retry the audit is not a stable project workflow.

The project therefore needs one reproducible repository-native entry point that owns preparation and reuse of the maintenance Python environment.

## Goals

The maintenance audit entry point must:

- work from a clean checkout with no pre-existing project virtual environment;
- avoid relying on maintenance packages installed in the system Python;
- create an isolated environment automatically on first use;
- reuse a valid environment on warm runs without reinstalling dependencies;
- rebuild the environment when `TOOLS/requirements-maintenance.txt` changes;
- also invalidate the environment when the Python major/minor version used to build it changes;
- keep the environment and bookkeeping files out of Git;
- preserve real package-index/network installation errors instead of hiding them;
- run `TOOLS/audit_engine.py` only after environment preparation succeeds;
- provide the same command to humans and agents;
- remain independent from the HDM gameplay runtime.

## Non-goals

This change will not:

- install maintenance dependencies globally;
- introduce Docker, Poetry, a standalone service, or a general build system;
- require `uv`, `pipx`, or another non-standard bootstrap tool;
- merge maintenance dependencies into runtime/game dependencies;
- make a cold offline environment succeed without a package source;
- change gameplay Project Instructions, `INSTALL/00_DND_BOOTSTRAP.md`, CORE runtime policy, or campaign behavior.

## Canonical command

The project-native maintenance command will be:

```text
TOOLS/run_maintenance_audit.py
```

The launcher will be an executable Python script that uses only the Python standard library until the isolated maintenance environment has been prepared.

Calling `python TOOLS/audit_engine.py` directly remains technically possible, but project documentation and agent instructions will treat `TOOLS/run_maintenance_audit.py` as the canonical audit entry point.

## Maintenance dependency location

Maintenance dependencies belong to development tooling, not to the repository root. Their canonical declaration is:

```text
TOOLS/requirements-maintenance.txt
```

The previous root-level `requirements-maintenance.txt` is removed as part of this change. The launcher, tests, documentation, and cache fingerprint all use the `TOOLS/` path.

## Environment location

The launcher will own a repository-local cache directory:

```text
.hdm-maintenance/
```

with an isolated virtual environment beneath it:

```text
.hdm-maintenance/venv/
```

The whole `.hdm-maintenance/` directory will be ignored by Git.

This directory is a rebuildable cache, not authoritative project state. Its disappearance after Work/Codex/container recreation is expected and safe.

## Bootstrap interpreter

The launcher will execute under the Python that starts `TOOLS/run_maintenance_audit.py` and use that interpreter only to:

1. inspect its own major/minor version;
2. create the virtual environment using the standard-library `venv` module;
3. invoke the virtual environment's Python and pip;
4. launch `TOOLS/audit_engine.py` once preparation succeeds.

The bootstrap interpreter is not required to contain `jsonschema` or other maintenance packages.

If the interpreter cannot create a `venv`, the launcher will fail with a concise diagnostic rather than installing packages globally or silently selecting another dependency manager.

## Environment fingerprint

A prepared environment is valid only for the exact maintenance dependency specification and Python compatibility tuple used to create it.

The launcher will compute a fingerprint from:

- SHA-256 of the complete `TOOLS/requirements-maintenance.txt` bytes;
- bootstrap Python major/minor version.

After a successful environment build, the launcher will store the fingerprint in `.hdm-maintenance/`.

A warm run will compare the current fingerprint with the stored fingerprint before running pip.

### Matching fingerprint

If the virtual environment exists, its Python is executable, and the stored fingerprint matches the current fingerprint, the launcher will skip dependency installation completely and run the audit immediately.

### Missing or mismatching fingerprint

If the environment is absent, incomplete, unusable, or has a different fingerprint, the launcher will rebuild the maintenance environment from scratch and install exactly:

```text
<venv-python> -m pip install -r TOOLS/requirements-maintenance.txt
```

using the new virtual environment's Python.

Rebuilding rather than incrementally mutating a stale environment avoids leftover packages from previous requirements sets.

The new fingerprint will be written only after dependency installation completes successfully.

## Failure semantics

Environment preparation is a prerequisite for the audit.

If virtual-environment creation fails, the launcher will stop and print a short message identifying that preparation step.

If pip cannot resolve or download dependencies because of DNS, network policy, package-index availability, TLS, or package resolution, the launcher will:

- return a non-zero exit code;
- identify dependency installation as the failed phase;
- preserve the meaningful pip error output;
- not write a success fingerprint;
- not run `TOOLS/audit_engine.py`.

The launcher will not turn a network failure into a misleading `jsonschema`-missing message and will not retry through a different package manager.

If environment preparation succeeds but `TOOLS/audit_engine.py` fails, the launcher will propagate the audit's non-zero result instead of treating it as an environment-bootstrap failure.

## Repository integration

The implementation is expected to touch only development-maintenance surfaces:

- create `TOOLS/run_maintenance_audit.py`;
- move root `requirements-maintenance.txt` to `TOOLS/requirements-maintenance.txt` without changing the pinned dependency content;
- create or extend root `.gitignore` to ignore `.hdm-maintenance/`;
- update the maintenance guidance in `TOOLS/audit_engine.py` so missing-dependency diagnostics direct users to the canonical launcher rather than a manual install command;
- update `RELEASE/CHECKLIST.md` to invoke the canonical launcher instead of requiring a separate install step plus direct audit invocation;
- update root `AGENTS.md` so development agents use the canonical launcher for the engine maintenance audit.

No gameplay Project Instructions, gameplay bootstrap, CORE runtime files, campaign schemas, or gameplay behavior are part of this change.

## Human and agent workflow

Both a human developer and an agent run exactly:

```text
TOOLS/run_maintenance_audit.py
```

The caller does not need to know the virtual-environment path and must not need to remember whether the current Work/Codex environment was previously prepared.

A Codex environment setup script MAY run the same command to prewarm the rebuildable cache while package-index access is available, but that is an optional optimization. The repository command remains authoritative and must work independently whenever the current execution environment permits dependency download.

## Verification requirements

Implementation must demonstrate all of the following:

1. **Cold checkout:** with `.hdm-maintenance/` absent, one command creates the isolated environment, installs the pinned requirements from `TOOLS/requirements-maintenance.txt`, and runs the audit.
2. **Pinned dependency:** the created environment contains the versions required by `TOOLS/requirements-maintenance.txt`.
3. **Successful audit:** after preparation, `TOOLS/audit_engine.py` completes successfully on a valid repository tree.
4. **Warm run:** a second invocation with an unchanged fingerprint does not invoke pip installation again.
5. **Requirements invalidation:** changing `TOOLS/requirements-maintenance.txt` changes the fingerprint and causes a clean environment rebuild before audit execution.
6. **Python invalidation:** changing the bootstrap Python major/minor compatibility tuple invalidates the cache.
7. **Git cleanliness:** `.hdm-maintenance/`, its virtual environment, fingerprints, and temporary preparation files do not appear in Git status.
8. **Installation failure:** simulated or real package-index/network failure yields a concise phase-level diagnostic, preserves useful pip failure information, leaves no success fingerprint, and does not run the audit.
9. **Audit failure propagation:** a failure from `TOOLS/audit_engine.py` is returned unchanged after successful environment preparation.
10. **Root cleanup:** root `requirements-maintenance.txt` is absent and `TOOLS/requirements-maintenance.txt` contains the unchanged pinned maintenance dependencies.

## Design rationale

A repository-local stdlib launcher is preferred because the repository already has a narrow maintenance dependency file and audit script but no general task runner. The missing abstraction is therefore only the reproducible execution boundary around those existing pieces.

Keeping the requirements file beside maintenance tooling makes its development-only scope explicit without changing its role as the declarative dependency source of truth.

Using standard-library `venv` keeps the bootstrap requirement to Python itself, while a fingerprint prevents unnecessary repeated installation. Treating the environment as an ignored rebuildable cache makes the workflow resilient to Work/Codex container recreation without pretending that scratch storage is durable.

`uv`, `pipx`, Poetry, Docker, and similar tools would add another bootstrap dependency without solving a demonstrated requirement that `venv` cannot satisfy.
