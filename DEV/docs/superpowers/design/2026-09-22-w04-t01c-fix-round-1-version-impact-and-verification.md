# W04.T01C Fix Round 1 — Version Impact and Verification Evidence

Status: **TARGETED REVIEW REPAIR — READY FOR CHECKPOINT REVIEW**

Base published HEAD: `03b9ce649b34f66ea423dd21f5302e03d819086e`.

This evidence records the bounded W04.T01C repair. It does **not** accept T01C;
independent reviewer PASS remains required before T02A/T03A may start.

## Root-cause and repair scope

The initial frontier implementation accepted caller-provided pending contributors
and replayed basis references, so a structurally valid empty pending set or old
basis could replace the obligation's missing-holder/currentness result. Visible
validation then compared evidence only with the caller's frontier, allowing a
forged/deserialized foreign frontier to authorize a consequence.

The repair stays inside the accepted Collaboration/RuntimeHost boundary:

- pending contributors are always derived from the obligation's accepted input
  contributors and required-holder set;
- the bounded native basis is re-read by known ID through the existing
  RuntimeHost/exact-read route and its admitted revisions are checked;
- the host basis is revalidated after those reads;
- visible validation recomputes the current frontier and compares identity,
  generation, campaign scope, dependency scope, native basis and pending set
  before accepting visible evidence.

No new authority, interface, scan, capability override, persistence owner or
shared final-writer surface was introduced.

## Version Impact Gate

| Owner / namespace | Before | After | Classification and result |
|---|---:|---:|---|
| `GAME/TOOLS/collaboration.py` `framework_module_version` | `1.0.5` | `1.0.6` | Material T01C owner repair: safe-frontier currentness and visible-consequence authority are fail-closed. |
| `runtime.collaboration_frontier` local schema | absent | `1` | New owner-local serialized frontier contract introduced by T01C. |
| `runtime.collaboration_obligation` local schema/projection | `2` | `2` | No obligation shape or lifecycle change in this repair. |
| `campaign_contract_generation` | `2` | `2` | No aggregate persistent-contract or migration change. |
| `storage_format_generation` | `3` | `3` | Existing exact known-ID route is unchanged. |
| `catalog_generation` | `2` | `2` | No catalog vocabulary change. |
| `engine_version` | `1.0-alpha` | `1.0-alpha` | No engine release bump for this owner-local repair. |

**VERSION_IMPACT:** `GAME/TOOLS/collaboration.py` `1.0.5 -> 1.0.6`;
new `runtime.collaboration_frontier` schema `1`; all other affected
namespaces unchanged.

## TDD and verification evidence

Baseline before the new REDs:

```text
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_rd12_collaboration
Ran 62 tests ... OK
```

RED before the production repair:

```text
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_rd12_collaboration.CollaborationFrontierTests
Ran 11 tests ... FAILED (failures=3)
```

The three expected failures were caller-empty pending override, post-admission
native-basis drift, and forged foreign frontier visible-consequence acceptance.

Focused GREEN:

```text
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_rd12_collaboration
Ran 65 tests ... OK
```

Cross-owner focused regression:

```text
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m unittest \
  DEV.TESTS.test_rd12_collaboration \
  DEV.TESTS.test_runtime_host_composition \
  DEV.TESTS.test_step3_resume_ordering_contract
Ran 78 tests ... OK
```

Additional checks:

```text
.hdm-devtools/venv/bin/ruff check GAME/TOOLS/collaboration.py DEV/TESTS/test_rd12_collaboration.py
All checks passed!

.hdm-devtools/venv/bin/ruff format --check GAME/TOOLS/collaboration.py DEV/TESTS/test_rd12_collaboration.py
2 files already formatted

git diff --check
PASS
```

**SYSTEM_IMPACT: NONE.** The candidate remains in T01C final review and is not
an acceptance of the downstream dependency gate.
