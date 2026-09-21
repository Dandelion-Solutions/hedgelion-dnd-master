# W04.T05A fix round 2 — Version Impact and verification evidence

Task: reject forged LIVE capabilities and close Context schema/runtime parity
gaps.

Base: `d687a9f08eafcc88fd5b5e71aea02e36dba7b9ef` (`v1/engine-rearchitecture`).

No cursor, `DEV/CURRENT_PROGRESS.md`, Wave-05, or `.entire/` content was
changed.

## Re-review repairs

- Context no longer accepts a callable LIVE reader at host composition, even
  when the callable also exposes a valid-looking reader method and payload.
- Context consumes the existing private history-owned
  `_SelectedLiveReadCapability`; the existing `BoundNativeHistoryRuntime`
  remains the host-composition authority and T07 integration is preserved.
- Context runtime validation now matches the registered schema for role/purpose
  bindings, identifier syntax, and typed optional `source_frontier` and
  `retrospective` fields.
- Differential negatives prove schema and runtime reject the same malformed
  scope and optional-field values; valid typed optional values remain accepted.

## Version Impact Gate

The current `context_runtime.py` revision at the task base is `1.0.6`, written
by the preceding T07 host-composition integration. This repair is materially
behavioral, so the module-local revision increments exactly once:

```text
GAME/TOOLS/context_runtime.py
framework_module_version: 1.0.6 -> 1.0.7
```

The T07 host-composition integration and its metadata are preserved. No
`history.py` revision, schema namespace, engine release, campaign generation,
storage/catalog/ruleset namespace, or shared projection requires a bump.

VERSION_IMPACT: `GAME/TOOLS/context_runtime.py` framework module
`1.0.6 -> 1.0.7`; all other affected HDM-owned namespaces: NONE.

## Verification evidence

TDD RED on the new tests: **6 failures**, covering callable forged-reader
acceptance, four schema/runtime parity gaps, and the expected revision bump.

GREEN verification:

```text
unittest DEV.TESTS.test_rd11_context_runtime                         34 passed
unittest rd11 + rd10 + rd13 + rd02 + rd09                          272 passed
```

Maintenance audit, JSON schema parsing, Python compilation, and
`git diff --check` pass.

The full local suite recorded **1063 passed, 6 skipped, 6 failed**. The six
failures are the known unrelated S6D mechanical/portable owner tests plus
runtime provenance/version-census checks contaminated by the protected
untracked `.entire/` workspace. No Context Runtime test failed.

SYSTEM_IMPACT: NONE CURRENT. The repair remains within SR-W04-T05A §2 and
does not add a reader interface, owner, transport boundary, persistent state,
or downstream task surface.
