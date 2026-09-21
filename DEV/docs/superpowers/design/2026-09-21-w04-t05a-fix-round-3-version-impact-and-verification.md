# W04.T05A fix round 3 — Version Impact and verification evidence

Task: realize the selected-LIVE Step-5.8 capability at the existing LIVE owner
and complete Context request schema/runtime parity.

Base: `6435bf914a00c9b4ef3896a4b749a8cd20583b2d` (`v1/engine-rearchitecture`).

No cursor, `DEV/CURRENT_PROGRESS.md`, Wave-05, or `.entire/` content was
changed.

## Owner realization

The existing LIVE owner is `GAME/TOOLS/live_state.py`. It now issues the
private concrete `_SelectedLiveReadCapability` through the private
`_issue_selected_live_read_capability` host-composition function and records
issued instances in the LIVE-owner weak-reference registry. Context and the
existing T07 `BoundNativeHistoryRuntime` consume that exact owner-issued
type. No Context-owned protocol, registry, token, or authority was introduced.

Context rejects callable and non-callable reader substitutes, including a
non-callable object with a valid-looking reader method and payload, plus a
concrete capability-shaped object that was not issued by LIVE. The T07
native-history host-composition path remains intact.

## Schema/runtime parity

Runtime validation now enforces the existing schema's identifier pattern for
all scoped IDs and each `required_ids` item, plus the existing typed optional
`source_frontier` and `retrospective` fields. Differential negatives cover
role, purpose, subject, recipient, campaign, channels, candidate bound,
required IDs, relations, budget, source frontier, and retrospective typing.

No schema file changed: the required schema constraints already existed; this
round closes the runtime enforcement gap.

## Version Impact Gate

The actual changed owner/consumer set requires these module-local bumps:

```text
GAME/TOOLS/context_runtime.py  framework_module_version 1.0.7  -> 1.0.8
GAME/TOOLS/live_state.py       framework_module_version 1.0.20 -> 1.0.21
GAME/TOOLS/history.py          framework_module_version 1.0.8  -> 1.0.9
```

The prior T07 Context metadata is preserved and incremented once for this
material repair. History now consumes the LIVE-owner capability rather than
owning the structural Protocol, so its owner-consumer module revision also
increments. No DEV/GAME manifest projection, schema namespace, engine release,
campaign generation, storage/catalog/ruleset namespace, or migration edge
requires a bump.

VERSION_IMPACT: Context `1.0.7 -> 1.0.8`; LIVE owner `1.0.20 -> 1.0.21`;
history consumer `1.0.8 -> 1.0.9`; all other HDM-owned namespaces NONE.

## Verification evidence

TDD RED: **5 expected failures** before the initial production repair, covering
missing LIVE-owner issuance, callable/non-callable forged capability rejection,
required-ID parity, and the three module revisions. A subsequent focused RED
covered rejection of an unissued capability-shaped object before adding the
LIVE-owner issuance registry.

GREEN and cross-owner verification:

```text
unittest rd11 + rd10 + rd13 + rd02 + rd09  275 passed
maintenance audit                         PASS
full pytest                                1069 passed, 6 skipped, 6 failed
```

The six full-suite failures are the known unrelated S6D mechanical/portable
owner tests plus runtime provenance/version-census checks contaminated by the
protected untracked `.entire/` workspace. No Context, LIVE, or history test
failed. JSON parsing, Python compilation, and `git diff --check` pass.

SYSTEM_IMPACT: NONE CURRENT. This is the explicitly authorized T05A targeted
repair at the existing LIVE owner; no architecture reopen or downstream task
surface was created.
