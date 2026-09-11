# R2.7 WP-27 Step 2 — Independent Audit

Status: **HOLD — NARROW REPAIR REQUIRED BEFORE STEP-2 ACCEPTANCE**

Date: 2026-09-11

Reviewed artifact:

- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-evidence-ledger.md`

Controlling Step-2 execution contract:

- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-execution-amendment.md`

Related recovery/currentness surfaces:

- `DEV/docs/superpowers/research/2026-09-09-r2-7-WP-27-final-implementation-planning-readiness-mini-report.md`;
- `DEV/CURRENT_PROGRESS.md`;
- `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md`.

This review is a Step-2 audit artifact only. It does **not** replace semantic owners, change the global cursor, reopen accepted architecture, authorize Step 3, start implementation planning, or modify the reviewed ledger.

---

## 1. Verdict

```text
WP27_STEP2_INDEPENDENT_REVIEW: HOLD
SEMANTIC_EVIDENCE_QUALITY: STRONG
STRUCTURAL_COMPLETENESS: PROVISIONALLY_PASS
STEP2_CLOSURE_VERIFICATION: FAIL
ARCHITECTURE_REOPEN_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO

BLOCKING: 1
SIGNIFICANT: 2
MINOR: 3 editorial/currentness-normalization findings
```

The Step-2 evidence work should **not** be restarted. The current ledger is materially stronger than the earlier summary-level approach and provides a usable item-level basis for later planning. The HOLD is narrow: one closure-verification defect, one unsupported readiness obligation, and one recovery-surface currentness defect must be repaired and rechecked.

Step 3 should not consume this Step-2 package as accepted evidence until the findings below are closed and the repaired Step-2 closure is independently re-reviewed.

---

## 2. What passed substantive review

The following evidence structure is accepted provisionally and is not a target for wholesale rework:

```text
SOURCE_ITEMS: 224
WP01_07: 64 item-level records
WP08_26: 68 item-level records
PO001_010: 10 / 10
ROUND2_DIAMOND_STRONG: 82 / 82 individually represented
ROUND2_REQUIRED_DELTAS: S14 / S53 / D15 explicitly reconciled
READINESS_RECORDS: 146 before any repair-driven recount
EXPLICIT_NO_WORK_TERMINALS: 78 before any repair-driven recount
MACHINE_MATERIAL_RESPONSIBILITIES: 59
MACHINE_GROUPS: 19
MACHINE_EXCEPTION_RECORDS: 14
MACHINE_EXCEPTION_MEMBERS: 31
HIGH_RISK_PROBES: 8 / 8 traceable
```

Strong points confirmed by review:

1. WP-01..WP-07 are recovered through asymmetric provenance -> current-owner -> later-amendment -> consumer chains rather than forced into a false late-WP filename pattern.
2. WP-08..WP-26 are decomposed into material owner items rather than one summary record per WP.
3. The Round-2 DIAMOND/STRONG set is represented item-by-item, with current disposition, supersession, activation, proof consequence, defer trigger and negative law retained.
4. `S14`, `S53` and `D15` later changes are explicitly reconciled, and additional later refinements are retained where discovered.
5. Readiness composition preserves source-level traceability rather than merging unlike obligations for compactness.
6. Machine -> owner reconciliation separates artifact census from semantic completeness and uses explicit `R27-X###` exceptions for stale/mixed surfaces.
7. WP-20 compatibility/migration, WP-22 proof classes, WP-23 release gates, WP-24 sizing/partition activation, WP-25 deferred-vs-rejected failure semantics, and WP-26 completed repairs are materially better separated than in the earlier summary-level attempt.
8. The eight high-risk probes are linked to concrete source/readiness/machine records instead of being free-standing prose conclusions.

No evidence found in this audit justifies a wholesale architecture reopen or a repeat of S2-A through S2-H.

---

# 3. Blocking finding

## IA27-S2-B01 — S2-J does not have valid durable closure verification

Severity: **BLOCKING**

### Observed condition

The Step-2 ledger declares:

```text
WP27_STEP2: COMPLETE
```

but its S2-J closure block records a pre-publication state:

```text
STEP2_FINAL_HEAD: UNCOMMITTED
current committed checkpoint: 309fc3ac63e87a9d89f7436149c005c589b0b196
remote read-back: NOT APPLICABLE
DEV unit suite: 456 / 458 PASS
```

The later published Step-2 closure commit is:

```text
9d40029357e475e0287f53c1aa37190b911bb428
"docs: close WP-27 Step 2 evidence"
```

The hosted `Validate engine source` run for that exact closure commit, run `#1987`, completed with `failure`: maintenance audit passed, but `Run DEV unit tests` failed.

The later branch head observed during this audit also had failing source CI, but it contains unrelated agent-skill/governance changes and therefore is not used to attribute additional failure to the WP-27 worker. The exact Step-2 closure commit failure is sufficient for this finding.

### Why this blocks acceptance

The Step-2 execution amendment requires S2-J to be a durable closure checkpoint with fresh verification/publication evidence. A locally known dirty-worktree failure or a later publication does not make a failed exact published closure verification equivalent to PASS.

This is a **closure/verification blocker**, not a semantic architecture blocker.

### Required repair

1. Fresh-check the current remote branch and inspect the exact failing DEV test(s) relevant to the Step-2 closure/current branch.
2. Distinguish Step-2 defects from unrelated repository/tooling changes. Do not repair unrelated surfaces merely to make the WP-27 ledger look green.
3. Repair the owner-valid cause of any failure that is in scope. If a failure is caused by a later unrelated repository change, establish that explicitly and validate the repaired Step-2 state on a clean current published HEAD rather than silently exempting it.
4. Run the full required maintenance audit and full DEV unit suite on the clean candidate closure state.
5. Publish the repaired Step-2 documentation checkpoint through the normal repository transport.
6. Verify the exact published HEAD through remote read-back.
7. Require hosted `Validate engine source` success for that exact repaired HEAD. Do not classify a failing mandatory check as acceptable merely because its cause is understood, unless a controlling process owner explicitly defines an exception.
8. Replace the stale S2-J `UNCOMMITTED` closure evidence with the actual published repaired closure SHA and exact verification evidence.
9. Re-run only the affected S2-I/S2-J closure accounting. Do not repeat S2-A..S2-H unless a repair changes their evidence materially.

### Acceptance criteria

```text
S2J_PUBLISHED_HEAD: exact SHA recorded
REMOTE_READ_BACK: PASS on exact SHA
MAINTENANCE_AUDIT: PASS on exact candidate/published state
FULL_DEV_UNIT_SUITE: PASS on exact candidate/published state
HOSTED_VALIDATE_ENGINE_SOURCE: SUCCESS on exact published SHA
STALE_UNCOMMITTED_CLOSURE_CLAIM: REMOVED / HISTORICALLY_LABELLED
STEP2_COMPLETE_CLAIM: supported by the repaired S2-J evidence
```

---

# 4. Significant findings

## IA27-S2-S01 — `WP01-F05 -> R27-R004` manufactures a current implementation debt unless a public owner is produced

Severity: **SIGNIFICANT**

### Observed condition

`WP01-F05` preserves a valid public/private evidence-separation constraint, but then classifies the absence of a general public governance route as:

```text
current_disposition: STALE_DEBT
implementation_consequence: add a concise public governance route
readiness_ids[]: [R27-R004]
```

The cited chain includes WP-01 provenance and `R2.6 §9`.

The accepted R2.6 canonical owner does not establish the claimed current public-documentation obligation: its §9 concerns architecture-stage versus post-implementation evidence and does not require adding a general private-research routing rule to public governance documentation.

The defensible surviving constraint is narrower:

```text
private/external exploratory evidence is not a public semantic owner;
public architecture may consume only accepted, independently expressed public conclusions under the project provenance policy.
```

That constraint does not by itself imply a new public-documentation implementation task.

### Why this matters

WP-27 exists partly to prevent dormant, external, historical or process evidence from being manufactured into future implementation work. An unsupported `STALE_DEBT -> R27-R004` route would contaminate the implementation-planning entry graph even though the rest of the ledger correctly avoids this failure mode.

### Required repair

1. Search the **accepted public owner chain** for an explicit current requirement to add the claimed public governance surface.
2. If such an owner exists, cite the exact public file/section/law and narrow `WP01-F05` / `R27-R004` to exactly what that owner requires.
3. If no such owner exists:
   - reclassify `WP01-F05` as an explicit no-current-work/process-boundary terminal using the ledger's existing vocabulary;
   - preserve the negative provenance/public-authority constraint;
   - remove `R27-R004` as a readiness/implementation obligation;
   - mechanically recompute all affected source/readiness/no-work counters, backreferences and S2-I predicates instead of hand-editing the previous totals.
4. Do not introduce a new architecture/governance owner to justify the old readiness record.
5. Do not use a private research artifact as public semantic authority.

### Acceptance criteria

```text
WP01_F05_PUBLIC_OWNER: exact accepted owner cited OR no-current-work verdict
UNSUPPORTED_PUBLIC_GOVERNANCE_DEBT: 0
R27_R004: retained only with explicit accepted owner; otherwise removed
NEGATIVE_PUBLIC_PRIVATE_EVIDENCE_LAW: preserved
COUNTS_AND_BACKREFERENCES: mechanically reconciled after disposition change
```

This repair does **not** require Product Owner judgment unless the worker discovers a genuinely new governance/product policy choice rather than an existing owner.

---

## IA27-S2-S02 — WP-27 mini-report contains competing current-looking cursor states

Severity: **SIGNIFICANT**

### Observed condition

The current WP-27 mini-report correctly opens with:

```text
STEP 2 COMPLETE — S2-J DURABLE CLOSURE RECORDED / STEP 3 NOT STARTED
```

but retained earlier sections still contain unqualified statements such as:

```text
WP-27 STEP 2: NEXT ACTIVE SLICE
Step 2 должен item-wise классифицировать ...
WP27_STEP2_STARTED: NO AT THIS CHECKPOINT
```

Later S2-A..S2-J sections again describe Step 2 as complete.

### Why this matters

The mini-report is a required WP-local recovery surface. Historical checkpoint text may be retained, but it must not compete visually or semantically with the current recovery cursor. A fresh agent should not need to infer which of two apparently current states wins.

`DEV/CURRENT_PROGRESS.md` remains the global cursor authority; this finding does not claim the global cursor itself is corrupt.

### Required repair

1. Preserve useful historical checkpoint text, but mark each old status block unambiguously, e.g.:

```text
HISTORICAL STEP-1 CLOSE SNAPSHOT — NOT CURRENT
```

2. Currentize or relabel statements that still read as present-tense current state.
3. Ensure the mini-report has exactly one unambiguous current status/cursor route, consistent with `DEV/CURRENT_PROGRESS.md` and the repaired S2-J.
4. Do not rewrite historical evidence facts merely to make the document shorter.

### Acceptance criteria

```text
MINI_REPORT_CURRENT_STATE: exactly one unambiguous current cursor
HISTORICAL_STATUS_BLOCKS: explicitly labelled non-current
GLOBAL_CURSOR_AUTHORITY: still DEV/CURRENT_PROGRESS.md
HISTORICAL_EVIDENCE: preserved
```

---

# 5. Minor normalization findings

These are not semantic blockers but should be repaired in the same narrow documentation pass.

## IA27-S2-M01 — historical S2-B/S2-C records retain time-relative composition wording

Some earlier ledger text says `readiness_ids[]` is intentionally empty because S2-F has not started, while the final document now contains populated readiness backreferences. Where this wording is historical, label it as a checkpoint snapshot; where it purports to describe the final record state, currentize it.

Do not erase the historical sequencing evidence.

## IA27-S2-M02 — historical S2-F/S2-G "later slices not started" blocks are not uniformly labelled

The ledger already labels some preserved blocks as historical snapshots, but the convention is not uniform. Apply one consistent marker to retained slice-close snapshots so `S2_G_AND_LATER: NOT_STARTED`, `S2_H_AND_LATER: NOT_STARTED`, etc. cannot be mistaken for the final current state.

## IA27-S2-M03 — S2-J still identifies an uncommitted checkpoint as `STEP2_FINAL_HEAD`

This overlaps the blocking verification issue but is also a direct currentness/editorial defect. After a repaired closure is published, the final S2-J block must identify the actual published closure SHA. If the old uncommitted checkpoint is retained for provenance, label it historical and do not call it the final head.

---

# 6. Explicit non-findings / do-not-rework constraints

The repair must not turn this HOLD into a new architecture cycle.

```text
NO wholesale WP-01..WP-26 reopen
NO repeat of the 82-item Round-2 extraction merely for reassurance
NO replacement of the 224-item source ledger with summaries
NO collapse of 146 readiness records merely to reduce document size
NO new global readiness owner
NO new migration registry
NO new Story/history/ACL authority
NO global failure/health/retry subsystem
NO universal partition topology
NO release execution
NO migration execution
NO implementation planning
NO gameplay bootstrap
NO opportunistic root README edit
```

If repair of `WP01-F05` changes one record's terminal route, only the affected readiness/count/backreference/accounting surfaces should change unless the mechanical recheck reveals a real secondary inconsistency.

---

# 7. Required repair sequence

Use the existing Step-2 owner/evidence process; this is not a new design process.

```text
1. fresh-check current remote state and controlling owners
2. resolve IA27-S2-S01 from accepted PUBLIC owner evidence
3. normalize mini-report / historical ledger status labelling
4. mechanically recompute affected source/readiness/no-work/backreference counters
5. rerun affected S2-I completeness predicates
6. repair S2-J with a real published candidate/final SHA
7. run fresh maintenance + full DEV unit verification
8. publish through normal repository transport
9. remote read-back exact published SHA
10. obtain hosted Validate engine source SUCCESS on that exact SHA
11. update only evidence needed to record the verified closure
12. stop for independent Step-2 re-review; do not start Step 3 as part of this repair assignment
```

If the worker discovers a genuine human-owned semantic/trade-off/authority/risk decision while repairing these findings, stop only for that decision under the normal process. None is known at audit time.

---

# 8. Re-review scope

The independent re-review should be narrow and evidence-based. It must verify:

1. `IA27-S2-B01` closure verification on the exact published repair SHA;
2. `IA27-S2-S01` owner evidence or no-work reclassification and all resulting count/backreference changes;
3. `IA27-S2-S02` one-current-state recovery semantics;
4. minor historical-snapshot normalization;
5. S2-I mechanical totals/predicates after repair;
6. no accidental changes to accepted architecture, implementation authorization, release state, migration state or gameplay state.

Unless a repair changes substantive evidence, the reviewer need not re-read all 224 source records or reperform S2-A..S2-H.

---

# 9. Review disposition

```text
WP27_STEP2_AUDIT_RESULT: HOLD
REPAIR_SCOPE: NARROW
RESTART_STEP2: NO
ARCHITECTURE_REOPEN: NO
PRODUCT_OWNER_DECISION: NO CURRENTLY
STEP3_CONSUMPTION_OF_STEP2_AS_ACCEPTED: HOLD UNTIL RE-REVIEW PASS
EXPECTED_NEXT_REVIEW: repaired S2-I/S2-J + affected record/currentness deltas only
```

The Step-2 mega-ledger is substantively strong enough to preserve as the basis for repair. Acceptance is withheld because the final closure evidence is not yet valid and one readiness obligation is not established by its cited accepted public owner chain.
