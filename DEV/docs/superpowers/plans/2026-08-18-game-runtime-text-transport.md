# Game Runtime Text Transport Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make HDM gameplay/runtime GitHub text transport use Connector UTF-8/text modes directly and forbid redundant LLM-visible Base64 encode/decode cycles for textual repository content.

**Architecture:** Add one concise pre-CORE guard to `INSTALL/00_DND_BOOTSTRAP.md` for the earliest storage writes, and one canonical detailed rule to `CORE/PERSISTENCE.md`, which already owns GitHub write transport semantics. Protect both paths with focused regression cases; do not duplicate the general policy into `LIVE_SCENE.md`, `CAMPAIGN_SETUP.md`, or Project Instructions.

**Tech Stack:** Markdown runtime instructions, GitHub Connector UTF-8 text interfaces, existing HDM regression-case documents, existing maintenance audit command when a complete local checkout is available.

## Global Constraints

- This is a transport-efficiency change only; do not alter campaign canon, persistence timing, transaction atomicity, concurrency semantics, access control, or gameplay behavior.
- For semantically textual repository content, use Connector UTF-8/text modes whenever a correct text mode exists.
- Do not manually perform `text -> Base64 -> text` for repository transport, chunking, staging, reconstruction, or verification.
- Connector-internal Base64 required by an underlying GitHub API is allowed and is not an LLM/runtime conversion.
- Base64 remains allowed for genuinely binary content or a required Connector operation that has no usable text mode.
- Do not add redundant general-policy wording to `LIVE_SCENE.md`, `CAMPAIGN_SETUP.md`, or `INSTALL/PROJECT_INSTRUCTIONS.txt`.
- All remote GitHub reads/writes use the GitHub Connector; do not use native Git remote, `gh`, curl, direct HTTP, credential injection, or manual Base64 transport.
- All changes remain on `feature/mechanical-runtime-hot-state` and remote writes are non-force.

---

## File Structure

**Modify:** `INSTALL/00_DND_BOOTSTRAP.md`
- Owns the early transport guard before the complete CORE cache is loaded.
- Must protect initial storage `README.md` and `DND_STORAGE.yaml` writes.

**Modify:** `CORE/PERSISTENCE.md`
- Owns the canonical detailed text-payload transport discipline for all normal persistence profiles.
- Applies to `CAMPAIGN_TREE_TXN`, `LIVE_STATE_CAS`, and `STORAGE_METADATA_SINGLE`.

**Modify:** `TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md`
- Adds explicit regression coverage for pre-CORE storage initialization without manual Base64.

**Modify:** `TESTS/PERSISTENCE_TRANSACTION_CASES.md`
- Adds explicit regression coverage for campaign/live/storage text publication without manual Base64.

**Do not modify:** `CORE/LIVE_SCENE.md`, `CORE/CAMPAIGN_SETUP.md`, `INSTALL/PROJECT_INSTRUCTIONS.txt`
- Existing specialized rules remain sufficient; the new general rule is inherited from bootstrap/persistence authority.

---

### Task 1: Add the pre-CORE bootstrap text transport guard

**Files:**
- Modify: `INSTALL/00_DND_BOOTSTRAP.md`, section `## 1. GitHub Connector`
- Test: `TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md`

**Interfaces:**
- Consumes: GitHub Connector read/write operations described by bootstrap.
- Produces: an early mandatory transport invariant that applies before CORE preload, including fresh storage initialization.

- [ ] **Step 1: Add the failing regression case first**

Append after existing `B44`:

```markdown
## B45 — Bootstrap text transport stays UTF-8
Fresh own-storage initialization writes root `README.md` and `DND_STORAGE.yaml` before complete CORE preload.
Pass: use Connector UTF-8/text interfaces for semantically textual repository payloads; do not manually Base64-encode/decode text for transport, chunking, staging, reconstruction or verification. Connector-internal Base64 required by an underlying API is allowed and is not an LLM/runtime conversion.
```

- [ ] **Step 2: Verify the regression requirement is not yet satisfied by the branch text**

Read `INSTALL/00_DND_BOOTSTRAP.md` from the exact branch and confirm that section `## 1. GitHub Connector` does not yet contain a general repository-text transport rule covering storage metadata writes. Existing engine-ZIP and scaffold-specific Base64 prohibitions do not satisfy this test.

Expected result: FAIL by inspection because the general early storage-write rule is absent.

- [ ] **Step 3: Add the minimal bootstrap guard**

Immediately after the opening paragraph of `## 1. GitHub Connector`, add:

```markdown
For semantically textual repository content, use Connector UTF-8/text interfaces whenever a correct text mode exists. Do not manually Base64-encode or Base64-decode text for GitHub transport, chunking, staging, reconstruction or verification. Connector-internal Base64 required by an underlying API is allowed; the runtime must not add its own redundant text-to-Base64-to-text cycle. Use explicit Base64 only for genuinely binary content or when a required Connector operation has no usable text mode.
```

Do not change the existing engine-package sentence `Never use base64 as a fallback.` or the existing new-campaign scaffold sentence `Never use explicit base64 or one commit per scaffold file.`

- [ ] **Step 4: Re-read bootstrap and regression case together**

Verify all of the following by exact text inspection:

```text
B45 exists.
Bootstrap rule explicitly says UTF-8/text interfaces.
Bootstrap rule forbids manual Base64 encode/decode for text.
Bootstrap rule permits Connector-internal Base64.
Bootstrap rule preserves a binary/no-text-mode exception.
Existing storage initialization order is unchanged.
Existing campaign initialization transaction shape is unchanged.
```

Expected result: PASS.

- [ ] **Step 5: Commit/publish the task**

Publish only these two file changes to `feature/mechanical-runtime-hot-state` through the GitHub Connector with a message such as:

```text
Guard bootstrap text transport from manual Base64
```

Before the write, verify the branch HEAD through the Connector. After the write, verify the resulting commit and branch HEAD.

---

### Task 2: Add the canonical persistence text-payload discipline

**Files:**
- Modify: `CORE/PERSISTENCE.md`, after `## Transport profiles` profile definitions and before `## Transaction snapshot`
- Test: `TESTS/PERSISTENCE_TRANSACTION_CASES.md`

**Interfaces:**
- Consumes: existing persistence profiles `CAMPAIGN_TREE_TXN`, `LIVE_STATE_CAS`, `STORAGE_METADATA_SINGLE`.
- Produces: one canonical text-payload rule inherited by campaign, live-state, and storage-metadata publication.

- [ ] **Step 1: Add the failing persistence regression case first**

Append after existing `PT30`:

```markdown
## PT31 — Text payload transport avoids manual Base64
Campaign-tree, live-state CAS and storage-metadata publication handle semantically textual payloads.
Pass: use Connector UTF-8/text modes whenever available; do not manually Base64-encode/decode text for reads, writes, chunking, staging or exactness checks. Connector-internal Base64 required by an underlying API is allowed and is not a runtime failure; genuine binary content or a required operation with no usable text mode remains an exception.
```

- [ ] **Step 2: Verify the persistence requirement is not yet satisfied**

Read `CORE/PERSISTENCE.md` from the exact branch and confirm that it defines transaction sequencing but contains no canonical general text-payload encoding discipline.

Expected result: FAIL by inspection because `PT31` has no corresponding persistence rule yet.

- [ ] **Step 3: Add the canonical persistence section**

Insert the following section after the three transport profiles and before `## Transaction snapshot`:

```markdown
## Text payload transport discipline

This rule applies to `CAMPAIGN_TREE_TXN`, `LIVE_STATE_CAS` and `STORAGE_METADATA_SINGLE` whenever the repository payload is semantically text, including YAML, JSON, Markdown, logs, checkpoints, indexes, configuration and generated campaign text.

Use Connector UTF-8/text interfaces directly whenever a correct text mode exists:
- read text as text;
- create/update text with ordinary UTF-8 text arguments;
- create Git-data text blobs with UTF-8 encoding rather than manually Base64-encoding them;
- keep large text textual when chunking or reconstructing it, using line/range or equivalent text-safe reads instead of Base64 merely to move chunks;
- verify exactness with actual file bytes, Git blob/content SHA or equivalent direct identity checks rather than a Base64 transform.

Do not create helper scripts whose purpose is to Base64-convert textual repository payloads. Do not add an LLM/runtime `text -> Base64 -> text` cycle around a Connector operation.

Connector-internal Base64 required by an underlying GitHub API is allowed and is not part of this prohibition. Explicit Base64 is allowed only for genuinely binary content or when the specific required Connector operation has no usable UTF-8/text mode; do not add extra encode/decode cycles beyond that technical boundary.
```

Do not alter any existing transaction profile, ref-check order, CAS behavior, non-force rule, base-tree preservation rule, or known-frontier behavior.

- [ ] **Step 4: Re-read persistence and regression case together**

Verify all of the following by exact text inspection:

```text
PT31 exists.
The new rule names all three existing transport profiles.
UTF-8/text mode is mandatory when available.
Manual Base64 is forbidden for text reads/writes/chunking/staging/exactness checks.
Git-data blobs explicitly use UTF-8.
Connector-internal Base64 is allowed.
Binary/no-text-mode exception remains.
No transaction sequence changed.
No save-boundary rule changed.
```

Expected result: PASS.

- [ ] **Step 5: Confirm specialized modules remain untouched**

Fetch current versions of:

```text
CORE/LIVE_SCENE.md
CORE/CAMPAIGN_SETUP.md
INSTALL/PROJECT_INSTRUCTIONS.txt
```

Verify their blob SHAs are unchanged from the implementation starting point. This confirms the general policy was not redundantly duplicated.

- [ ] **Step 6: Commit/publish the task**

Publish only `CORE/PERSISTENCE.md` and `TESTS/PERSISTENCE_TRANSACTION_CASES.md` to the same branch through the GitHub Connector with a message such as:

```text
Forbid manual Base64 in runtime text persistence
```

Before the write, re-read branch HEAD through Connector. After the write, verify resulting commit and branch HEAD.

---

### Task 3: Final verification against the approved spec

**Files:**
- Verify: `INSTALL/00_DND_BOOTSTRAP.md`
- Verify: `CORE/PERSISTENCE.md`
- Verify: `TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md`
- Verify: `TESTS/PERSISTENCE_TRANSACTION_CASES.md`
- Verify unchanged: `CORE/LIVE_SCENE.md`
- Verify unchanged: `CORE/CAMPAIGN_SETUP.md`
- Verify unchanged: `INSTALL/PROJECT_INSTRUCTIONS.txt`

**Interfaces:**
- Consumes: Tasks 1–2 published branch state.
- Produces: evidence that the runtime rule covers both bootstrap and normal persistence without gameplay/persistence semantic changes.

- [ ] **Step 1: Verify remote branch HEAD and changed-file scope**

Use Connector commit/compare data to verify that only the intended runtime instruction/regression files changed since the approved design-spec commit, aside from the implementation-plan document itself.

Expected implementation file set:

```text
INSTALL/00_DND_BOOTSTRAP.md
CORE/PERSISTENCE.md
TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md
TESTS/PERSISTENCE_TRANSACTION_CASES.md
```

- [ ] **Step 2: Verify policy coverage with targeted text assertions**

Confirm the branch contains all of these concepts in the intended authority layers:

```text
bootstrap: UTF-8/text Connector interfaces for semantically textual repository content
bootstrap: no manual Base64 encode/decode
bootstrap: Connector-internal Base64 exception
persistence: all three transport profiles named
persistence: direct UTF-8 Git-data blobs
persistence: no Base64 for chunking/reconstruction/exactness checks
persistence: binary/no-text-mode exception
B45 regression case
PT31 regression case
```

- [ ] **Step 3: Verify no forbidden duplication or semantic drift**

Confirm:

```text
CORE/LIVE_SCENE.md unchanged
CORE/CAMPAIGN_SETUP.md unchanged
INSTALL/PROJECT_INSTRUCTIONS.txt unchanged
CAMPAIGN_TREE_TXN algorithm unchanged
LIVE_STATE_CAS algorithm unchanged
STORAGE_METADATA_SINGLE transaction role unchanged
bootstrap storage initialization order unchanged
new-campaign scaffold transaction shape unchanged
```

- [ ] **Step 4: Run repository audit when execution environment permits**

If a complete local checkout of the exact branch is available, run only the canonical maintenance command:

```bash
TOOLS/run_maintenance_audit
```

Expected: exit 0 and `OK: engine consistency audit passed`.

If a complete local checkout or package-index access required by a cold maintenance environment is unavailable, do not fake this verification. Report the exact environment limitation and rely only on the remote text/commit verification actually performed.

- [ ] **Step 5: Verify final branch HEAD**

Use Connector ref/compare/commit data to verify the feature branch points at the final implementation commit and that publication was non-force.

---

## Self-review checklist

- Spec coverage: early pre-CORE storage writes are covered in Task 1; all normal persistence profiles are covered in Task 2; regression coverage and non-goals are verified in Task 3.
- Placeholder scan: no TBD/TODO/unspecified implementation steps remain.
- Interface consistency: the same three profile names and the same UTF-8/manual-Base64/binary-exception semantics are used throughout.
- Scope: no code/runtime mechanics refactor, no Project Instructions edit, no duplicate general rule in live/setup modules.
