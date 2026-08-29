# Documentation Corpus Refactor — Migration Journal

Status: **ACTIVE OPERATIONAL JOURNAL — PHYSICAL MIGRATION DEFERRED**
Date: 2026-08-29
Branch: `v1/engine-rearchitecture`
Initial verified HEAD: `584322f640a14b05e4cbfcaa63d8349187cd3780`

This file is the operational continuation surface for the owner-approved Documentation Corpus Refactor. It does **not** establish architecture law and does not replace the semantic census.

Semantic classification remains owned by:

- `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-census.md`
- `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-*.md`

Connector/path-enumeration operational guidance is preserved separately in:

- `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-connector-operations-note.md`

The journal records only migration readiness, batching, path-repair obligations and verification state. Individual source semantics must not be re-derived from this journal when a census entry or current canonical owner is available.

## 1. Current baseline

Current durable semantic checkpoint is Specs Census Part 18.

```text
PRE_REFACTOR_SPECS_BASELINE:               375
SPECS_FULL_CONTENT_REVIEWED:               200
UNAMBIGUOUS_DESIGN_DESTINATIONS:           164
SPECS_TO_RESEARCH_DESTINATIONS:              1
CONFIRMED_CURRENT_SPEC/AMENDMENT_OWNERS:     30
PENDING_FINAL_SUPERSESSION_CHECK:             5
SPECS_REMAINING_UNREVIEWED:                 175

PHYSICAL_MOVES_PERFORMED:                    0
MIGRATED_VERIFIED:                            0
REFERENCE_AUDIT_GATE:           NOT SATISFIED
```

These semantic move candidates are **not** migration-ready files. Every candidate is currently blocked by the same repository-wide path/reference gate unless a later batch proves otherwise.

Specs Census Part 18 was published at `86f421fe7b25f322ef429043d3cc8f2733f461d6` and read back from the remote branch. Its stale Step-5.14 physical role-isolation/reset wording was subsequently recorded as `DCR-020`.

## 2. Stable migration dispositions

Use these operational dispositions without changing the semantic class in the census:

- `KEEP_IN_SPECS_CURRENT_OWNER` — current accepted implementation-facing specification/owner decision remains in `specs/`.
- `KEEP_IN_SPECS_CURRENT_AMENDMENT` — current canonical amendment/supplement remains in `specs/` with normative-parent links preserved.
- `MOVE_TO_DESIGN_PROVENANCE` — semantic review proves the artifact is process/derivation/review/closure provenance and current law exists elsewhere.
- `SUPERSEDED_CANONICAL_TO_DESIGN` — artifact was once canonical but a later owner explicitly supersedes it; preserve as provenance, never delete.
- `RESEARCH_SPLIT_OR_EXTRACTION` — census requires a controlled split/extraction before relocation/closure.
- `PENDING_SUPERSESSION_CHECK` — no physical move until later owner/amendment relationships are fully resolved.
- `BLOCKED_REFERENCE_AUDIT` — semantic destination is known but branch-complete inbound references and path repairs are not yet proven.

## 3. Migration state machine

```text
CENSUS_PENDING
    -> SEMANTIC_READY
    -> BLOCKED_REFERENCE_AUDIT
    -> REFERENCE_SET_PROVEN
    -> READY_TO_MOVE
    -> MIGRATION_COMMIT_PUBLISHED
    -> MIGRATED_VERIFIED
```

A file may enter `SEMANTIC_READY` only from a completed item-level census disposition.

`MIGRATED_VERIFIED` requires fresh remote read-back after publication. Conversation state, an intended patch, or a returned write SHA alone is not sufficient.

## 4. Mandatory physical-move gate

Before any move batch:

1. Fresh-read the current remote branch HEAD.
2. Re-read the batch census entries and every current owner/amendment that controls their semantic disposition.
3. Confirm no later canonical owner, amendment or supersession has changed the disposition.
4. Obtain a **branch-complete inbound-reference census** for every source path in the batch.
5. Enumerate every path repair before writing; unresolved or unenumerable inbound references block the batch.
6. Check outbound links inside each moved artifact and preserve derivation/current-owner routes.
7. Build one coherent relocation + reference-repair batch. Do not mix unrelated semantic edits into the move.
8. Publish only to `v1/engine-rearchitecture`; do not create a branch and do not force-update history.
9. Verify from fresh remote state:
   - every new destination path exists with expected content;
   - every old source path intended for relocation is absent;
   - all enumerated inbound path references are repaired;
   - canonical/current-owner paths remain unchanged unless the batch explicitly and independently proves a canonical relocation requirement;
   - applicable documentation/link/schema/tests pass.
10. Fresh-read the resulting remote HEAD and relevant files, then mark the batch `MIGRATED_VERIFIED`.

If step 4 cannot prove completeness, stop at `BLOCKED_REFERENCE_AUDIT`.

## 5. Refactor safety invariants

- **Move, do not erase provenance.** Historical reasoning, rejected alternatives, review findings and superseded canonical artifacts remain available under `design/` when classified there.
- **Authority is semantic, not directory-derived.** Moving an artifact into `design/` does not itself supersede it; supersession must already be proven by current owning sources.
- **No hidden law loss.** If a purported provenance file is the only remaining carrier of accepted implementation-relevant law, relocation is blocked until that law is consolidated into a current owner.
- **No opportunistic rewriting.** Path repair and minimal provenance/current-owner pointers are allowed; semantic modernization belongs in a separately justified change.
- **Canonical parents survive.** Current canonical specifications and canonical amendments remain in `specs/` unless a later census proves explicit supersession.
- **Reference correctness is batch-wide.** A move is not complete merely because the source and destination files exist correctly.
- **No broad fallback scan as proof.** Missing branch-complete reference evidence cannot be replaced by confidence from filename search snippets.
- **Coherent family batches are preferred.** Keep derivation chains and their current owner together in one repair analysis where practical.

## 6. Batch record schema

Every executed batch must record:

```text
BATCH_ID
CENSUS_IDS
SOURCE_PATHS
DESTINATION_PATHS
SEMANTIC_DISPOSITIONS
CURRENT_OWNER_OR_AMENDMENT
SUPERSESSION_EVIDENCE
INBOUND_REFERENCE_AUDIT_METHOD
INBOUND_REFERENCE_SET
OUTBOUND_PATH_REPAIRS
OTHER_PATH_REPAIRS
PRE_WRITE_HEAD
MIGRATION_COMMIT_SHA
POST_WRITE_HEAD
VERIFICATION_COMMANDS_OR_HOSTED_CHECKS
REMOTE_READBACK_EVIDENCE
FINAL_STATUS
NOTES / DEFERRED FOLLOWUPS
```

The census IDs are the durable join key. Do not duplicate full semantic analyses here.

## 7. Migration queue

### M-001 — Research corpus realization

- **Source of truth:** R-001..R-044 in `2026-08-29-documentation-corpus-refactor-census.md`.
- **Scope:** only entries whose final destination differs from the source path and any explicitly required split/extraction work.
- **Special case:** preserve exact census-controlled extraction boundaries where research evidence and design disposition are interleaved; do not promote accepted architecture law into research.
- **Status:** `BLOCKED_REFERENCE_AUDIT` for relocation; extraction work remains separately gated by its census entry and coherent-write requirements.

### M-002 — Early specs candidate pool

- **Source of truth:** S-001..S-060 in Specs Census Part 01.
- **Scope:** only rows already classified with an explicit changed destination.
- **Exclusions:** all `PENDING_SUPERSESSION_CHECK` rows and all current owners.
- **Status:** `BLOCKED_REFERENCE_AUDIT`; the five cumulative pending supersession cases remain non-movable until later-owner review resolves them.

### M-003 — Step-4 / Step-5.0 derivation families

- **Source of truth:** S-061..S-078 in Specs Census Parts 02–03.
- **Move candidates:** derivation/provenance rows only; consolidated current owners remain in `specs/`.
- **Status:** `BLOCKED_REFERENCE_AUDIT`.

### M-004 — Step-5.1 Frontier Model

- **Source of truth:** S-079..S-087 in Specs Census Part 04.
- **Move candidates:** S-079..S-086 -> corresponding `design/` paths.
- **Keep:** S-087 `2026-08-20-step-5-1-frontier-model-canonical-spec.md` in `specs/`.
- **Current owner:** S-087.
- **Status:** `SEMANTIC_READY / BLOCKED_REFERENCE_AUDIT`.

### M-005 — Step-5.2 Resumable Runtime Closure

- **Source of truth:** S-088..S-099 in Specs Census Part 05.
- **Move candidates:** S-088..S-098 -> corresponding `design/` paths.
- **Important superseded former canonical:** S-096 `2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec.md` -> `design/`; S-099 explicitly supersedes it.
- **Keep/current owner:** S-099 `2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md` in `specs/`.
- **Status:** `SEMANTIC_READY / BLOCKED_REFERENCE_AUDIT`.

### M-006 — Step-5.3 Temporal & Pending-Obligation Continuity

- **Source of truth:** S-100..S-109 in Specs Census Part 06.
- **Move candidates:** S-100..S-107 -> corresponding `design/` paths.
- **Keep/base current owner:** S-108 `2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md`.
- **Keep/current supplement:** S-109 `2026-08-21-step-5-3-5-9-temporal-agenda-chronology-integration-canonical-amendment.md`.
- **Relationship:** S-109 supplements, and does not supersede, S-108 and Step-5.9 canonical authority.
- **Status:** `SEMANTIC_READY / BLOCKED_REFERENCE_AUDIT`.

### M-007 — Step-5.12 Host Delivery / Disclosure Boundary

- **Source of truth:** S-179..S-188 in Specs Census Part 16.
- **Move candidates:** S-179..S-187 -> corresponding `design/` paths.
- **Important supersession chain:** S-182 confirmation-only candidate is superseded by S-185 after S-183 review + S-184 owner scope decision; S-184 is an accepted historical owner decision fully consolidated into S-188 rather than reversed.
- **Keep/current owner:** S-188 `2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` in `specs/`.
- **Later-authority result:** Step 5.13 consumes/preserves the contract; Step 5.14 supplements without replacing detailed owners; R2.5/R2.6 preserve/realize the boundary; no later supersession found.
- **Status:** `SEMANTIC_READY / BLOCKED_REFERENCE_AUDIT`.
- **Deferred debt:** `DCR-018` preserves Step-5.12-specific machine/host-profile realization obligations; this does not activate them during the refactor.

### M-008 — Step-5.13 Garbage Collection / Orphan Cleanup

- **Source of truth:** S-189..S-195 in Specs Census Part 17.
- **Move candidates:** S-189..S-194 -> corresponding `design/` paths.
- **Keep/current owner:** S-195 `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md` in `specs/`.
- **Later-authority result:** Step 5.14 explicitly supplements earlier detailed owners rather than replacing them and preserves Step-5.13 cleanup semantics; no later supersession found.
- **Status:** `SEMANTIC_READY / BLOCKED_REFERENCE_AUDIT`.
- **Deferred debt:** `DCR-019` preserves cleanup-contract/protection-routing/reference-survival/cross-source/ref-delete and Git-retention realization obligations; this does not activate them during the refactor.

### M-009 — Step-5.14 Full Recovery / Concurrency Adversarial Review

- **Source of truth:** S-196..S-200 in Specs Census Part 18.
- **Move candidates:** S-196..S-199 -> corresponding `design/` paths.
- **Keep/current owner:** S-200 `2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md` in `specs/`.
- **Later-authority qualification:** 2026-08-23 Step-4 single-context amendment + Round-1 Step-6 closure supersede only the physical role-isolation/reset baseline implication embedded in the Step-5.14 forward-looking feasibility ledger; Step-5.14 integration laws and Step-5 closure remain current.
- **Status:** `SEMANTIC_READY / BLOCKED_REFERENCE_AUDIT`.
- **Documentation debt:** `DCR-020` preserves the stale SD-5/role-isolation wording so future planning does not resurrect the retired topology requirement.

The queue still does not duplicate every reviewed family from Parts 07–15. Those census parts remain authoritative for their semantic destinations; append their coherent migration batches before physical execution. Do not infer that an omitted queue batch means the corresponding reviewed files remain in `specs/`.

## 8. Queue extension rule

Each later census checkpoint appends or updates a migration batch only after its semantic family is closed. Do not create a physical-move batch from partially read filenames.

If later review changes a previously recorded supersession relationship, update this journal by census ID and current owner before any migration write. The semantic census/current owner remains authoritative over the journal.

### 8.1 Connector census-enumeration rule

Do not rediscover baseline families by repeatedly fetching the full repository recursive tree and text-searching the resulting giant one-line JSON payload.

For semantic census enumeration use the frozen pre-refactor `specs/` tree directly:

```text
PRE_REFACTOR_SPECS_TREE_SHA: 0fb176ec4cee7af3d6765a34174964679c99819d
GET /repos/Dandelion-Solutions/hedgelion-dnd-master/git/trees/0fb176ec4cee7af3d6765a34174964679c99819d
require: truncated == false
```

Then fetch every exact family path with `GitHub.fetch_file` for full semantic review.

Full failure mode and continuation procedure are recorded in `2026-08-29-documentation-corpus-refactor-connector-operations-note.md`.

This method solves baseline family inventory for census work only. It does **not** satisfy the branch-complete inbound-reference requirement for physical migration; DCR-016 remains open.

## 9. Current execution cursor

```text
CORPUS_REFACTOR_STATUS: IN_PROGRESS
DURABLE_SPECS_CENSUS_CURSOR: 200 / 375
DURABLE_LAST_CHECKPOINT: Specs Census Part 18
LAST_CLOSED_SEMANTIC_FAMILY: Step 5.14 — Full Recovery / Concurrency Adversarial Review
PART18_PUBLICATION_SHA: 86f421fe7b25f322ef429043d3cc8f2733f461d6
PART18_REMOTE_READBACK: VERIFIED
STEP5_14_DEBT_EXTRACTION: COMPLETE / DCR-020
NEXT_DURABLE_SEMANTIC_FAMILY: 2026-08-23 Round-1 closure / Step-4 single-context amendment / Step-6 working-note group
PHYSICAL_MIGRATION_STATUS: DEFERRED
CENSUS_ENUMERATION_METHOD: TARGET BASELINE TREE VERIFIED
REFERENCE_AUDIT_STATUS: BRANCH-COMPLETE INBOUND-REFERENCE METHOD NOT YET PROVEN
NEXT_ACTION: full-content 2026-08-23 specs census -> later-authority/supersession sweep -> publish/read back Part 19 -> continue semantic census
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```