# Maintenance Audit Plan Amendment: Requirements Location

This amendment is approved and supersedes every root-level `requirements-maintenance.txt` path in `docs/superpowers/plans/2026-08-18-maintenance-audit-environment.md`.

## Canonical dependency file

Use only:

```text
TOOLS/requirements-maintenance.txt
```

The existing root-level `requirements-maintenance.txt` is moved to that path without changing its dependency content.

## Required plan substitutions

During implementation:

- fingerprint `TOOLS/requirements-maintenance.txt` bytes;
- install with the maintenance venv Python using `-r TOOLS/requirements-maintenance.txt`;
- construct test fixtures with `TOOLS/requirements-maintenance.txt` under the temporary root;
- verify a requirements change at the `TOOLS/` path invalidates the cache;
- verify root `requirements-maintenance.txt` is absent after publication;
- retain `.hdm-maintenance/` at repository root as the ignored rebuildable cache.

No other implementation-plan behavior changes. The canonical user/agent command remains:

```text
TOOLS/run_maintenance_audit.py
```
