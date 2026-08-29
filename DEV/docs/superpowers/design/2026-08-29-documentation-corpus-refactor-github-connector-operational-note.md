# Documentation Corpus Refactor — GitHub Connector Operational Note

Status: **ACTIVE WORKING NOTE — REQUIRED FOR CONTINUATION / NOT ARCHITECTURE AUTHORITY**
Date: 2026-08-29
Branch: `v1/engine-rearchitecture`

This note records a connector/repository-navigation failure mode encountered during the Documentation Corpus Refactor so a fresh continuation session does not repeat it.

It does **not** establish architecture law. Semantic authority remains with the architecture owners and the corpus census files.

## 1. Failure mode

### Symptom

While continuing the specs census on the non-default branch `v1/engine-rearchitecture`, attempts to discover the Step-5.12 family through ordinary GitHub code/file search returned no results even though the files exist on the branch.

A directory/Contents response for the whole `DEV/docs/superpowers/specs/` tree was also too large to use reliably as the primary discovery surface; downstream text search over the oversized response was inconsistent/unhelpful.

### Concrete reproduced case

GitHub repository search for:

```text
step-5-12-host-delivery-disclosure-boundary
```

returned no files.

The branch-scoped Git tree, however, proved that the files exist and enumerated the complete family.

Therefore:

> **GitHub code search on this non-default branch MUST NOT be used as proof that a file/reference does not exist, and an oversized Contents response MUST NOT be treated as the preferred exact-family discovery mechanism.**

This is also why code-search absence cannot satisfy the refactor's branch-complete inbound-reference/path-repair gate.

## 2. Verified reliable route for exact branch file discovery

Use the GitHub Connector only, with this sequence:

```text
1. Fetch the current branch:
   GET /repos/Dandelion-Solutions/hedgelion-dnd-master/branches/v1/engine-rearchitecture

2. Read the commit's root tree SHA.

3. Traverse Git Trees API by SHA, directory by directory:
   root tree
     -> DEV tree
     -> docs tree
     -> superpowers tree
     -> specs tree

4. Fetch the `specs` tree by its exact tree SHA.
   This returns the branch's exact filenames and blob SHAs.

5. Select the complete semantic family from those exact paths.

6. Fetch each selected file with branch-scoped `fetch_file(..., ref="v1/engine-rearchitecture")`
   for full-content semantic review.
```

For this checkpoint the branch chain was:

```text
BRANCH_HEAD:
  0139a14058f74147835e78db7d1634f50a9c8f71
ROOT_TREE:
  342a5f85a95f281aeaf4dab64ce631f7dc490f82
DEV_TREE:
  02d189b42f960937b79565790e00fac255be0082
DEV/docs_TREE:
  1c9eb50e8288dfaf14e2bd5001c17fa766ca4080
DEV/docs/superpowers_TREE:
  8d003c9266c4f1882d994d0dfdcc9a7cd6d0cce5
PRE_REFACTOR_SPECS_TREE:
  0fb176ec4cee7af3d6765a34174964679c99819d
```

Tree SHAs are checkpoint evidence only. A continuation session MUST fresh-read the branch HEAD before correctness-sensitive work and re-traverse if the tree changed.

## 3. Step-5.12 exact family recovered by the reliable route

The pre-refactor specs tree contains exactly these ten Step-5.12 family sources:

1. `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-task-brief.md`
2. `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-research-draft.md`
3. `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-analytical-challenge.md`
4. `DEV/docs/superpowers/specs/2026-08-21-step-5-12-minimal-host-delivery-owner-scope-decision.md`
5. `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-candidate-spec.md`
6. `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-adversarial-review.md`
7. `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-candidate-spec-v2.md`
8. `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-adversarial-review-addendum-v2.md`
9. `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-resolution-gate.md`
10. `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md`

Do not infer family cardinality from filenames remembered in chat. Re-read the tree.

## 4. Current durable continuation checkpoint

At the time this operational note was created:

```text
CORPUS_REFACTOR_STATUS: IN_PROGRESS
RESEARCH_CENSUS: 44 / 44 COMPLETE
SPECS_CENSUS: 178 / 375 COMPLETE
SPECS_REMAINING: 197
LATEST_PUBLISHED_SPECS_CENSUS:
  DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-15.md

ACTIVE_NEXT_FAMILY:
  Step 5.12 — Host Delivery / Disclosure Boundary

STEP5_12_CENSUS_STATUS:
  NOT YET PUBLISHED

NEXT_CENSUS_IDS:
  start at S-179

CONFLICT_DEBT_REGISTER:
  DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-conflict-debt-register.md
  existing IDs DCR-001..DCR-017
  every newly discovered dual owner / contradiction / stale wording / deferred obligation /
  missing realization / host capability gap / refactor operational debt must be added there
  or carried into the final frozen conflict/debt report.

PHYSICAL_MIGRATION_STATUS: DEFERRED
REFERENCE_AUDIT_GATE: NOT SATISFIED
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```

The older Migration Journal still contains an earlier execution cursor (`109 / 375`, next Step 5.4). Treat that cursor as stale operational text, not as current census truth. The latest Specs Census checkpoint (Part-15) and this note establish the current continuation cursor. Update/normalize the journal during the controlled journal-maintenance pass; do not infer that semantic work regressed.

The stale journal cursor itself is documentation/operational debt and belongs in the final conflict/debt inventory if not corrected before closure.

## 5. Required continuation procedure

A fresh session continuing this refactor should:

1. fresh-read remote `v1/engine-rearchitecture` HEAD;
2. perform repository bootstrap required by `AGENTS.md` and current design process;
3. read Specs Census Part-15;
4. read the conflict/debt register;
5. read this operational note;
6. use branch Git-tree traversal, not code-search absence, to establish exact family membership;
7. full-content review all 10 Step-5.12 sources;
8. check later canonical amendments/supersessions that materially affect Step 5.12;
9. classify S-179 onward with item-level semantics;
10. extract every new conflict/debt condition into the parallel DCR audit layer;
11. publish Specs Census Part-16 only after both semantic census and conflict/debt extraction gates are complete;
12. update the migration journal/batch queue without physically moving files until the branch-complete inbound-reference gate is actually proven;
13. fresh-read resulting remote HEAD and written files;
14. continue the corpus census; do **not** start substantive WP-07 before full Documentation Corpus Refactor closure.

## 6. Reference-audit consequence

The successful Git-tree traversal solves **exact branch file discovery**.

It does **not by itself solve branch-complete inbound-reference discovery** because Git Trees enumerate paths/blobs but do not search every blob's contents for references.

Therefore keep these two capabilities distinct:

```text
EXACT FILE/FAMILY DISCOVERY:
  SOLVED by branch-scoped Git Trees traversal + fetch_file

BRANCH-COMPLETE INBOUND REFERENCE CENSUS:
  STILL UNSOLVED / REQUIRED BEFORE PHYSICAL MIGRATION
```

Do not prematurely mark `DCR-016` or the migration reference gate resolved merely because family discovery now works.
