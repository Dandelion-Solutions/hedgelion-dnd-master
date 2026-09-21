# W04.T05A fix round 1 — Version Impact and verification evidence

Task: trusted Context resolution and role/purpose eligibility repair.

Base: `e1dcc9b964bddc7c707b0acd56118f970109e8cd` (`v1/engine-rearchitecture`).

This record classifies the current coherent implementation slice. It does not
change the accepted Context architecture or any shared execution cursor.

## Accepted implementation scope

The slice is limited to:

- `GAME/TOOLS/context_runtime.py` — trusted RepositoryPort campaign pinning,
  private host composition, consumption of the existing history-owned
  `_SelectedLiveReadCapability`, forged-capability rejection, and finite
  role/purpose/profile dispatch;
- `DEV/SCHEMAS/context-need-profile.schema.json` — strict registered request
  and profile contract;
- `DEV/SCHEMAS/context-trace.schema.json` — finite registered profile IDs;
- `DEV/TESTS/test_rd11_context_runtime.py` — RED/GREEN witnesses for the
  ruling's caller-substitution, schema, capability and module-version laws.

The implementation remains inside SR-W04-T05A §2: Context is host-bound,
ephemeral and non-authoritative; discovery candidates are routing hints; native
owners remain responsible for currentness and eligibility.

## Version Impact Gate

`GAME/TOOLS/context_runtime.py` is an engine-bound runtime module. The current
clean-basis W04 implementation (`9f9fc4855958b4238ea7bdf304ec0f63a5544bdf`)
is the preceding material module change. Earlier W01 material changes are
history-reconstructed revisions `1.0.1` through `1.0.3`; the clean-basis W04
implementation is `1.0.4`. The current accepted repair is therefore:

```text
GAME/TOOLS/context_runtime.py
framework_module_version: 1.0.4 -> 1.0.5
```

The version header/value are synchronized in the same logical edit. Rejected
and restored attempts (`e55cc56`, `cdd1e67`, and `22e2495`) are not current
module revisions and do not increment this namespace.

No additional projection or namespace changes are required:

- `framework_module_version` is module-local; it has no DEV/GAME manifest
  projection;
- Context request/trace schemas are ephemeral contracts and have no existing
  `schema_version` namespace or persisted projection to bump;
- `engine_version`, campaign-contract generation, storage generation, catalog
  generation, ruleset identity/generation, and persistent-family schemas are
  outside the changed owner/consumer set;
- no migration/adoption edge is introduced.

## Verification evidence

Commands run on the local machine:

```text
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python DEV/TOOLS/run_maintenance_audit.py
OK: engine consistency audit passed

PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS -n auto
1054 passed, 6 skipped, 6 failed
```

The six full-suite failures are the known unrelated S6D mechanical/portable
owner tests plus runtime provenance/version-census checks contaminated by the
protected untracked `.entire/` workspace. No Context Runtime test failed in
the full run.

Focused Context and related owner verification remains green:

```text
unittest DEV.TESTS.test_rd11_context_runtime                         31 passed
unittest rd11 + rd10 + rd13                                          85 passed
unittest rd11 + rd10 + rd13 + rd02 + rd09                          267 passed
```

JSON schema parsing, Python compilation, and `git diff --check` also pass.

VERSION_IMPACT: `GAME/TOOLS/context_runtime.py` framework module
`1.0.4 -> 1.0.5`; all other affected HDM-owned namespaces: NONE.

SYSTEM_IMPACT: NONE CURRENT. The slice consumes the already accepted
RepositoryPort and history-owned LIVE capability boundary; it creates no new
owner, transport authority, persistent state, or downstream task surface.
