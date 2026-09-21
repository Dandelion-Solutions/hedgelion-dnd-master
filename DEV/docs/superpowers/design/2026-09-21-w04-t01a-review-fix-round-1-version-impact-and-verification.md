# W04.T01A review fix round 1 — Version Impact and verification evidence

Status: **TARGETED REVIEW REPAIR — READY FOR CHECKPOINT REVIEW**

Base published HEAD: `c37c517136a78dd57edde09320e7f1dc0fd3cb0e`.

This task-local evidence records the bounded T01A repair. It does not modify the
Wave-04 execution cursor or `DEV/CURRENT_PROGRESS.md`.

## Repair scope

- `GAME/TOOLS/runtime_execution.py` rejects incomplete Resolution, Continuation
  and linked Procedure owner records before producing ordered evidence.
- `GAME/TOOLS/collaboration.py` revalidates the host basis and sends the native
  ordering producer the one basis already used for admission; a changed pin
  fails closed instead of combining evidence from two operations.
- `DEV/TESTS/test_rd12_collaboration.py` contains RED/GREEN witnesses for both
  incomplete owner records and a changing campaign pin.

The repair preserves the Step-3 native ordering producer in
`GAME/TOOLS/runtime_execution.py`; no mechanics helper, new owner, persistent
field, callback, registry or semantic family is introduced.

## Version Impact Gate

| Owner / namespace | Before | After | Classification |
|---|---:|---:|---|
| `GAME/TOOLS/collaboration.py` `framework_module_version` | `1.0.1` | `1.0.2` | Material module-local repair: basis revalidation and single-basis producer routing change admission behavior. |
| `GAME/TOOLS/runtime_execution.py` `framework_module_version` | `1.0.5` | `1.0.6` | Material module-local repair: native ordering owner records now require the fields already required by their schemas. |
| `runtime.collaboration_obligation` schema | `1` | `1` | No serialized shape or lifecycle change. |
| `runtime.command` schema | `3` | `3` | No command acceptance or serialized command shape change. |
| Resolution / Continuation / Procedure owner schemas | existing | existing | No schema file or accepted record shape changes; malformed records that were already outside the owner schemas now fail closed. |
| IntentClause schema/fields | unchanged | unchanged | No clause vocabulary or persisted shape change. |
| `campaign_contract_generation` | `2` | `2` | No aggregate persistent-contract interpretation or migration change. |
| `storage_format_generation` | `3` | `3` | No route/layout/marker change. Development-only storage revision bookkeeping is also unchanged. |
| `catalog_generation` | `2` | `2` | No catalog or machine-vocabulary change. |
| `engine_version` | `1.0-alpha` | `1.0-alpha` | Pre-release engine identity does not advance for this owner-local repair. |

**VERSION_IMPACT:** `GAME/TOOLS/collaboration.py` `1.0.1 -> 1.0.2` and
`GAME/TOOLS/runtime_execution.py` `1.0.5 -> 1.0.6`; all other affected
namespaces remain unchanged.

## Compatibility and migration conclusion

No compatibility or migration edge is required. The repair does not change the
shape or interpretation of any valid persisted Resolution, Continuation,
Procedure or collaboration-obligation record. It removes fail-open acceptance
of records that were already invalid against the existing owner schemas and
rejects mixed-operation evidence before admission. Existing valid records need
no rewrite or adoption step; incomplete/stale records remain unsupported and
must fail closed.

## Verification evidence

RED before production changes:

```text
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_rd12_collaboration
Ran 20 tests ...
FAILED (failures=3)
```

The three expected failures were the new Resolution-missing-field,
Continuation-missing-field and changing-pin negatives.

GREEN/focused verification:

```text
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m unittest \
  DEV.TESTS.test_rd12_collaboration \
  DEV.TESTS.test_runtime_host_composition \
  DEV.TESTS.test_step3_resume_ordering_contract
Ran 33 tests ...
OK

.hdm-devtools/venv/bin/ruff check \
  GAME/TOOLS/collaboration.py GAME/TOOLS/runtime_execution.py \
  DEV/TESTS/test_rd12_collaboration.py
All checks passed!

.hdm-devtools/venv/bin/ruff format --check DEV/TESTS/test_rd12_collaboration.py
1 file already formatted

git diff --check
PASS
```

The scoped version-policy unittest was also attempted. Its namespace checks
reported no legacy hits, but the census test failed on untracked protected
`.entire/` metadata (12,619 unclassified hits); that workspace was not read,
modified or removed. This is unavailable clean-checkout evidence, not a
T01A implementation failure.

**SYSTEM_IMPACT: NONE.** The repair remains within the accepted T01A
Collaboration/Step-3 producer envelope and changes no shared cursor or
downstream owner.
