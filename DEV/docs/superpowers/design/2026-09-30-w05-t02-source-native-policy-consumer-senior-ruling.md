# W05.T02 Source-Native Policy Consumer — Senior System-Impact Ruling

Status: **ACCEPTED SENIOR / BOUNDED PREREQUISITE AUTHORIZED**

Date: **2026-09-30**

Reviewed public basis:
`8fa7b76a1b795c9e6e046a3f6affbdc7db2b57d0`

Blocked task:
`W05.T02 — Shared catalog, wrapper and identifier writer`

Prerequisite:
`W05.T02-P0 — W03 source-native identifier-policy consumer cutover`

Output:
`W05_SOURCE_NATIVE_POLICY_CONSUMER_READY`

## 1. Disposition

```text
SYSTEM_IMPACT: RESOLVED
CLASSIFICATION: LATENT OWNER/CONSUMER REPRESENTATION MISMATCH
PRODUCT_OWNER_DECISION_REQUIRED: NO
W03 SEMANTICS: PRESERVED
W03 WAVE: NOT REOPENED
W05.T02-P0: AUTHORIZED
W05.T02: HELD UNTIL P0 INDEPENDENT PASS / READ-BACK
LOCAL T02 CANDIDATE 5fdc556c2abb5d4f37a9923b73ede03e16920383:
  PRESERVE LOCALLY
  DO NOT PUBLISH BEFORE P0 + REBASE/REVERIFY
```

The worker correctly stopped. The mismatch is real.

Accepted W03 specifies one scalar `live_birth` disposition for each admitted
family:

```text
SOURCE_NATIVE_LIVE | OWNER_EQUIVALENT | FORBIDDEN
```

and separately fixes source-native encoding to
`framed_base32hex_v1`.

Current `GAME/TOOLS/live_state.py::_source_native_policy_row(...)`, however,
expects a pre-final owner-local/test shape:

```text
live_birth:
  disposition: source_native_live
  encoding: framed_base32hex_v1
```

Passing the final scalar representation directly to that consumer fails closed
with "source-native LIVE disposition is missing".

No accepted adapter/compiler from scalar shared policy to this nested shape
exists in current public HDM.

## 2. Authority direction

The shared representation is not changed to satisfy the stale consumer.

W03 explicitly deferred physical identifier-policy publication to Wave 05 while
retaining a local closed admission table in LIVE. W05.T02 is the one final
shared identifier-policy writer.

Therefore the authority direction is:

```text
accepted W03 scalar disposition law
+ W05.T02 final shared identifier-policy row
        ->
W03 LIVE consumer validation
```

not:

```text
old W03 test fixture shape
        ->
redefine W05 shared catalog
```

The W03 nested fixture is implementation evidence from before the final shared
catalog cutover. It is not a second canonical identifier-policy representation.

## 3. Canonical final contract

For each final identifier-policy family row, `live_birth` is exactly one of:

```text
"SOURCE_NATIVE_LIVE"
"OWNER_EQUIVALENT"
"FORBIDDEN"
```

The exact closed family/disposition matrix remains the W03.T04 table.

For a family admitted as `SOURCE_NATIVE_LIVE`, the LIVE consumer:

1. resolves the exact family row;
2. requires scalar `row["live_birth"]` to equal the local
   `LIVE_BIRTH_ADMISSION_TABLE[family]` exactly;
3. requires the existing valid family prefix used by the source-native ID;
4. uses the owner-fixed
   `SOURCE_NATIVE_LIVE_ENCODING == "framed_base32hex_v1"`.

Encoding is **not** selected by catalog data, request/model input or a caller.
The final shared catalog does not need to repeat it inside a nested
`live_birth` object.

`OWNER_EQUIVALENT` and `FORBIDDEN` remain non-admitted for source-native
LIVE allocation even if a caller forges a different scalar value; the local
closed W03 admission table remains the semantic check.

## 4. No adapter / no dual representation

Do not introduce a separate generic scalar-to-nested policy adapter.

The correct final cutover is for the W03 LIVE consumer to read the accepted
scalar representation directly.

Because this is unreleased clean-slate v1:

- do not retain the nested `live_birth {disposition, encoding}` shape as
  compatibility input;
- do not dual-read scalar and nested forms;
- do not add migration or aliases for the owner-local test fixture;
- do not let arbitrary caller mappings choose source-native encoding.

## 5. Bounded prerequisite — W05.T02-P0

Semantic owner:
**W03 LIVE / source-native identity consumer**.

Scheduling owner:
**Wave 05 final-integration prerequisite**, because the mismatch becomes
observable only when W05.T02 materializes the deferred shared policy.

Allowed production/test writes:

- `GAME/TOOLS/live_state.py`;
- `DEV/TESTS/test_rd09_access_live.py`;
- mechanically required module-version/control bookkeeping;
- Wave-05 execution/progress evidence.

Read-only for P0:

- `DEV/CATALOG/identifier-policies.json`;
- `DEV/SCHEMAS/identifier-policies.schema.json`;
- shared catalog/wrapper/identifier-policy bytes;
- W05.T02 RD16/catalog-conformance implementation;
- retained GAME schemas and CORE.

P0 must not publish the final shared identifier-policy machine.

Mandatory RED/GREEN evidence:

- exact scalar `SOURCE_NATIVE_LIVE` family row is accepted by encode/parse,
  allocation, opening and persisted-history validation paths;
- missing scalar disposition fails closed;
- wrong scalar disposition fails closed;
- the former nested `live_birth` mapping is rejected rather than dual-read;
- a scalar forgery cannot make `OWNER_EQUIVALENT` or `FORBIDDEN` families
  source-native because the local closed table remains authoritative;
- invalid/missing prefix fails closed;
- encoding remains the fixed owner constant and is not caller/catalog selected;
- reordered creation/cursor/CAS/ambiguous-publication semantics remain unchanged.

## 6. Version Impact

`GAME/TOOLS/live_state.py` is currently:

`framework_module_version: 1.0.21`.

This prerequisite materially changes the admitted identifier-policy consumer
shape. Expected transition:

```text
live_state.py: 1.0.21 -> 1.0.22
```

A fresh Version Impact Gate is mandatory.

Expected P0 impacts:

```text
identifier-policies schema version: unchanged by P0
catalog generation: unchanged
campaign contract generation: unchanged
storage generation: unchanged
migration: NONE
dual-read: NONE
```

W05.T02 separately retains ownership of the planned final
`identifier-policies.schema_version 2 -> 3` cutover and shared policy bytes.

## 7. W05.T02 continuation

After P0 independent PASS and remote read-back:

1. fresh-read public HEAD and P0 result;
2. rebase/reconcile the preserved local T02 candidate;
3. keep scalar `live_birth` in the final shared identifier-policy machine;
4. turn the T02-owned RD16/source-native policy integration tests GREEN against
   the real runtime consumer;
5. run the normal T02 Version Impact Gate, independent review, full clean
   verification, maintenance, non-force publication and read-back;
6. only then claim `RD16_SHARED_MACHINE_INTEGRATION_READY`.

The local `5fdc556...` candidate is not reviewed or accepted by this ruling.

## 8. W02 discrepancy

The reported historical W02 recovery-label discrepancy is not a W05.T02 entry
dependency. T02 consumes the accepted W02 catalog-backed-command and
adjudication checkpoints named by the stable plan. This ruling does not reopen
W02.
