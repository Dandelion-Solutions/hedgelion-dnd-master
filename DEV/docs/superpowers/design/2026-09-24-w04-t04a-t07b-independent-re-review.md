# Independent re-review — W04.T04A and W04.T07B

Status: **CURRENT FINAL DISPOSITION — T04A PASS / T07B TARGETED REPAIR REQUIRED**

Date: 2026-09-24

## Exact review basis and scope

- Reviewed remote HEAD: `3c1a9ca1e31e46f8101944ee668a52bd3d3678ff`.
- Reviewed parent / combined code candidate: `dfca9bc45eecc05e2b7287c20954172e7921ffa7`.
- T04A repair: `0d190a9db11129a02f07c71a812996c78a8d33cf`, following implementation `20dd5301310bf5db250c229655ac957fe56e23c3`.
- T07B repairs: `0b4dde06d5bdc70fd85b4b6856da45c3f1147d59` and `dfca9bc45eecc05e2b7287c20954172e7921ffa7`, following candidate `5a53b8e4323f53cde2f3c718e477003a4da3ce29`.
- Role: independent task re-reviewer. No production code, executable tests, schema or accepted architecture is changed by this review publication.

The previous report remains verbatim at this same path in commit `8ca335f969f3ace1623356e1a6c2b835282ef26f`, blob `1e3af3550acbb715cd68405506219fea118e3627`. Its failures were against `b13496b19bc8a7f11b82a24e11508036e815596f`, not against the repaired HEAD. The current report supersedes its task dispositions only as stated below.

## Bounded source manifest and method

All repository evidence was read through GitHub Connector at the reviewed HEAD. The bounded review graph is W03 access/currentness -> T04A reconciliation -> T04B consumer, and Story source contracts -> T07B codec/schema -> T07C consumer. No whole-repository preload or local repository was used.

| Current artifact | Evidence use |
|---|---|
| `AGENTS.md`, `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md`, `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` | Role, transport, review and publication gates |
| Stable Wave-04 plan, blob `e64902d1b1df6ed8cebde411231a3d0ddee33be5` | Task scope, output checkpoints and downstream joins |
| `DEV/CURRENT_PROGRESS.md` and Wave-04 execution cursor | Current candidates, previous review and preserved qualifications |
| `GAME/TOOLS/collaboration.py`, blob `31f1a3ccdbd2054100a8f9979f9024005407d872` | Full-body reload, uncertainty failure, preserved historical hydration |
| `GAME/TOOLS/access_control.py`, blob `54e22e268026765892c9e82bdab6eb19a5e89ffe` | Unchanged W03 full-body comparison and revision-carrier semantics |
| `DEV/TESTS/test_rd12_collaboration.py` and exact T04A repair diff | Matching MANIFEST, changed/missing/added fields, OPEN/CLOSED uncertainty witnesses |
| `GAME/TOOLS/story.py`, blob `30b117efb231b0fa616aeb60de6d2d774ee4df5e` | M-SEG payload-link admission and selector comparison |
| `DEV/SCHEMAS/story-mechanics-unit.schema.json`, blob `8543eec4131e3f3cbea2b104c0979bd1f7fd3eb8` | MECHANICS v4 typed nonempty segment-owner link |
| `DEV/TESTS/test_rd13_story_t0_commentator.py`, blob `2c41253c00b347c5a95bef49a04f44ab0980cfea` | Shared validator fixture table and separate exact-segment tests |
| Prior review's WP-17 and baseline Story source-contract evidence | Retained semantics; no new owner decision or omission authorization |

The changed paths were checked against the previous findings, with local guard/call-path tracing and inspection of the new tests. Existing tests were independently verified in exact-head hosted CI. A new boolean-selector counterexample was traced through the actual current code; an isolated Python comparison/JSON-Schema type probe confirmed the primitive behavior. The complete new repository regression was **not executed by this reviewer**. No local run is represented as an exact-repository test.

## Exact-head hosted verification

```text
workflow: Validate engine source
head_sha: 3c1a9ca1e31e46f8101944ee668a52bd3d3678ff
run: 35951449546
job: 107480668040
status: completed
conclusion: success
Run full maintenance audit: success
Run DEV unit tests: success
command: .hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -v
Ran 1178 tests
OK (skipped=5)
VERSION_UNCLASSIFIED=[]
VERSION_LEGACY_HITS=[]
```

The logs include the new full-body drift test, OPEN/CLOSED singleplayer uncertainty tests, the historical-input regressions and the shared M-SEG validator table. The local protected `.entire/` census failure does not reproduce in this clean hosted checkout. That local issue is not claimed repaired, and capture files/permissions are untouched. This evidence belongs to the reviewed HEAD, not to a later documentation commit.

## Disposition of previous findings

| Finding | Re-review disposition | Exact reason |
|---|---|---|
| IRR-T04A-01 | CLOSED | `_read_current_campaign_body` independently reads full `MANIFEST.yaml` through the pinned RepositoryPort, retains unrelated fields and supplies that body to the unchanged W03 guard. Matching-body success plus changed/deleted/added-field negatives are present and run in hosted CI. |
| IRR-T04A-02 | CLOSED | Unknown singleplayer creator/agency validity raises a bounded `CollaborationAdmissionError`; it no longer returns a false invalidity verdict that produces OBSOLETE. OPEN and CLOSED tests verify failure without state mutation. Proven lost pending agency retains its positive OBSOLETE test. |
| IRR-T07B-01 | CLOSED for the original missing/empty-payload-link witness | M-SEG admission now requires payload `resolution_refs` or `receipt_refs`; an exact link only in `sources` no longer satisfies that requirement. The shared fixture table covers valid resolution/command links, absence, emptiness, wrong family and zero ordinal. A distinct remaining type mismatch is recorded below. |

### T04A acceptance

**W04.T04A: PASS / GO** at the exact reviewed state.

`W04_AUTHORITY_COLLAB_RECONCILIATION_READY` is accepted. The full native MANIFEST is independently read; the transport pin supplies the W03 revision carrier without turning a projected access-only subset into the full body. Unknown authority remains failure, and positively invalid pending agency remains a separate obsolescence path. Historical associations, author/PC linkage and existing fingerprints are retained; new input and recipient catch-up retain current authorization. Reconciliation remains read-only and route-bounded. W03 code is unchanged.

This accepts T04A, not T04B or the whole wave. Unknown singleplayer agency is still a bounded failure; this PASS does not claim a positive creator-resolution path that the candidate does not provide. Same-closure publication/recovery and its tests remain T04B-owned.

## Remaining finding

### IRR-T07B-02 — BLOCKING — boolean segment ordinal passes Python but fails schema

**Exact code path.** `story.py::_plain_json` preserves booleans. `_native_ref` passes a selector through that generic JSON normalization. The M-SEG path ultimately calls `exact_native_ref`, which compares the actual selector with an expected selector using ordinary mapping equality:

```python
return reference.get("selector") == selector
```

For candidate `["runtime.resolution","resolution-1",1]`, the expected selector contains integer `segment_sequence=1`. The current code does not validate the actual segment ordinal's type before that equality comparison.

**Counterexample.** Start with the existing valid `_registered_story_unit("MECHANICS")` fixture, keep the candidate and `segment_id` unchanged, and change only:

```python
unit["payload"]["resolution_refs"][0]["selector"]["segment_sequence"] = True
```

Keep `receipt_refs` absent. This is ordinary malformed input data, not a fabricated host or mutation of private TCB state.

The relevant selector is:

```json
{"segment_id":"resolution-1:segment:1","segment_sequence":true}
```

Python's current equality path accepts that selector as equal to the expected integer-1 selector. The MECHANICS v4 schema requires `segment_sequence` to be an integer of at least 1, so its only payload link is invalid. The structural contract and Python admission still disagree, now on type rather than field presence.

**Isolated probe result:** selector mapping equality `True`; the current selector-shape integer constraint rejects the boolean; the corresponding integer selector passes. Full validator outcome is established by static path tracing, not a claimed new repository test execution.

**Rule.** T07B strict owner-local serialized contract and exact typed segment identity. Successful semantic admission must not admit a boolean as a native positive segment ordinal.

**Minimal repair destination.** `GAME/TOOLS/story.py` M-SEG selector validation and `DEV/TESTS/test_rd13_story_t0_commentator.py`. Validate the selector's required fields and positive integer type before equality/binding. Do not coerce `True` to 1, weaken the schema, remove exact candidate binding, introduce a new validator authority or perform a whole-wave restore. Run the boolean witness through both validators for resolution and command/receipt routes; retain valid positive and negative/malformed cases.

**Important parity limit.** A structurally well-formed selector for segment 2 can legitimately pass structural JSON Schema while failing Python's exact candidate-1 binding. This review does not require JSON Schema to perform cross-field candidate decoding/equality or force both validators to be equally permissive. Preserve the separate semantic mismatch test. The blocking counterexample above is the opposite, invalid direction: Python admits a value that its declared structural schema rejects.

## Preserved qualifications and Version Impact

- T04A collaboration module `1.0.15 -> 1.0.16` is accepted; obligation schema remains v3. No new persistent field, campaign/storage/catalog/engine generation, migration or dual-read is required by this repair.
- T07B Story module `1.0.4 -> 1.0.5` and the submitted MECHANICS v4/projection-state v4 candidate remain recorded but are not a task PASS. A further material Python repair needs its normal fresh Version Impact assessment; do not silently reuse a spent module revision.
- The earlier SOURCE_CLASSIFIED omission qualification remains: blanket rejection of OMITTED is safe against caller-chosen omission but is not proof of a legal native-evidence-consuming omission route. No such support/completeness is credited here, and a caller MAY_OMIT/reason flag must never enable it.
- The recorded CLS-HDM preflight remains at its existing PASS, with its explicit semantic-change triggers intact. This targeted repair review neither reruns it nor waives future triggers.
- Accepted earlier tasks remain closed. No new host prerequisite, architectural boundary, migration policy or deployment capability is authorized.

## Continuation and final verdicts

```text
W04.T04A: PASS / GO
W04_AUTHORITY_COLLAB_RECONCILIATION_READY: ACCEPTED
W04.T04B: AUTHORIZED from accepted T04A; not yet implemented or accepted here

W04.T07B: FAIL / REPAIR REQUIRED
IRR-T07B-02: BLOCKING
W04.T07C: BLOCKED until repaired T07B independent PASS

W04.T05C: still waits for T04B plus accepted T02C and T05B
WAVE_04: NOT COMPLETE
WAVE_05: NOT AUTHORIZED
VERSION_IMPACT: NONE for this review/control-only publication
SYSTEM_IMPACT: NONE — routine bounded implementation/contract repair
```

T04B and the bounded T07B repair may run in parallel within their disjoint owner/test lanes. Do not replay T04A repairs or reopen earlier accepted work without a proven regression. Preserve exact-head verification, reviewer and publication/read-back gates. OpenCode reviewer permission denial is not permission for self-approval or bypass; publish coherent candidates and evidence for independent review here when necessary.
