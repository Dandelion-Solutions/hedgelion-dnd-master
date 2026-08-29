# Documentation Corpus Refactor — GitHub Connector Operations Note

Status: **ACTIVE OPERATIONAL NOTE — CENSUS ENUMERATION WORKAROUND VERIFIED**
Date: 2026-08-29
Branch: `v1/engine-rearchitecture`

This note preserves a GitHub Connector failure mode encountered during the Documentation Corpus Refactor and the working method used to continue the semantic census without guessing file-family membership.

It is **not** architecture authority, semantic census authority, or proof that the physical-migration inbound-reference gate is satisfied.

## 1. Problem: oversized recursive-tree responses are a trap for family enumeration

The tempting operation is:

```text
fresh branch HEAD
-> root tree SHA
-> GET /git/trees/<root>?recursive=1
-> search/find inside the returned response for one family prefix
```

On this repository that is unreliable as an operational workflow:

- the recursive repository tree is very large;
- the Connector/resource representation may serialize the tree payload as one giant JSON line;
- displayed output can be truncated by response budget even when the underlying GitHub tree response itself is not logically truncated;
- `find_in_resource` against that one-line JSON can return the entire giant line as one match instead of a compact exact path set;
- repeated search/find attempts consume substantial context and can look like a stalled session;
- GitHub code search is not sufficient evidence for branch-complete enumeration on the non-default `v1/engine-rearchitecture` branch.

Therefore:

> **Do not use repeated recursive-root-tree + text-find/code-search attempts as the completeness proof for a census family.**

Do not infer family membership from filenames remembered from a previous chat, rough counts, search snippets, or current-directory naming patterns.

## 2. Verified census-enumeration method

For the semantic census, enumerate against the frozen **pre-refactor baseline**, not against a later mutable post-census directory state.

Current durable baseline facts:

```text
PRE_REFACTOR_SPECS_COUNT: 375
PRE_REFACTOR_SPECS_TREE_SHA: 0fb176ec4cee7af3d6765a34174964679c99819d
```

Working method:

1. Fresh-read `v1/engine-rearchitecture` before substantive work.
2. Use the durable census checkpoint to recover the frozen baseline `specs/` tree SHA.
3. Fetch that **target directory tree directly and non-recursively**:

```text
GET /repos/Dandelion-Solutions/hedgelion-dnd-master/git/trees/0fb176ec4cee7af3d6765a34174964679c99819d
```

4. Confirm the returned Git tree says `truncated: false`.
5. Enumerate the exact direct-child paths for the target family prefix from that tree; do not substitute default-branch code search.
6. Fetch every exact family path with `GitHub.fetch_file` and perform full-content review, using line ranges when a file is too large for one response.
7. Treat later canonical/amendment files as a separate supersession/current-authority sweep. They increment the 375-file baseline census only when they themselves are part of the frozen baseline and receive full census review.
8. Publish the next durable census part only after the whole exact family is reviewed and later-authority relationships are checked.

Why this works better:

- it removes the unrelated rest of the repository from the path-enumeration payload;
- it uses the same immutable baseline tree that defines the 375-source census;
- `truncated: false` gives a complete direct-child listing for that baseline directory;
- exact `fetch_file` calls then provide authoritative branch content for semantic review.

If the flat `specs/` tree is still visually large, use the durable previous census `NEXT_UNREVIEWED_SOURCE` plus the exact family prefix to isolate entries in the complete baseline tree, then verify every candidate path with `fetch_file`. Do not go back to repeated recursive-root scanning.

## 3. Exact Step 5.12 family recovered with this method

The next family after Specs Census Part 15 contains exactly **10** frozen-baseline sources:

1. `2026-08-21-step-5-12-host-delivery-disclosure-boundary-task-brief.md`
2. `2026-08-21-step-5-12-host-delivery-disclosure-boundary-research-draft.md`
3. `2026-08-21-step-5-12-host-delivery-disclosure-boundary-analytical-challenge.md`
4. `2026-08-21-step-5-12-host-delivery-disclosure-boundary-candidate-spec.md`
5. `2026-08-21-step-5-12-host-delivery-disclosure-boundary-adversarial-review.md`
6. `2026-08-21-step-5-12-minimal-host-delivery-owner-scope-decision.md`
7. `2026-08-21-step-5-12-host-delivery-disclosure-boundary-candidate-spec-v2.md`
8. `2026-08-21-step-5-12-host-delivery-disclosure-boundary-adversarial-review-addendum-v2.md`
9. `2026-08-21-step-5-12-host-delivery-disclosure-boundary-resolution-gate.md`
10. `2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md`

Current in-session review state at the time of this note:

```text
DURABLE_PUBLISHED_CENSUS_CURSOR: 178 / 375   # Specs Census Part 15
STEP5_12_EXACT_BASELINE_SOURCE_COUNT: 10
STEP5_12_FULL_CONTENT_READ_IN_CURRENT_SESSION: 10 / 10
STEP5_12_PART_16_PUBLISHED: NO
DURABLE_CURSOR_MUST_NOT_ADVANCE_TO_188_UNTIL_PART_16_IS_WRITTEN_AND_READ_BACK
```

Pre-publication semantic result from the completed reads, to be revalidated when writing Part 16:

```text
STEP5_12_DESIGN_PROVENANCE_DESTINATIONS: 9
STEP5_12_CURRENT_CANONICAL_OWNER: 1
CURRENT_OWNER:
  specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md
```

Important authority relationship:

- the original confirmation-only candidate and its first adversarial review are superseded derivation;
- the owner-approved minimal-host-delivery scope decision materially changed the baseline to `EMISSION_COMMIT` with accepted interruption over-confirmation risk;
- candidate v2 + adversarial addendum + resolution gate are design provenance;
- the final canonical spec explicitly incorporates the owner-approved scope/product decision, so that decision is not the sole remaining carrier of current law;
- Part 16 must still perform/record the later-authority supersession sweep before claiming the canonical file remains unsuperseded.

## 4. This does NOT solve the physical-migration reference gate

The method above proves a complete **baseline directory inventory** for semantic census work.

It does **not** prove a complete repository-wide set of files that reference a path being moved.

DCR-016 therefore remains open:

```text
PHYSICAL_MIGRATION_STATUS: DEFERRED
BRANCH_COMPLETE_INBOUND_REFERENCE_METHOD: NOT YET PROVEN
```

Do not use the target-directory tree enumeration method as a substitute for inbound-reference/path-repair completeness.

In particular:

- GitHub code search on the non-default branch remains insufficient as the sole proof;
- moving a file still requires a separately proven branch-complete inbound-reference census;
- until then, semantic census may continue but physical moves remain blocked.

## 5. Fresh-chat continuation rule

A fresh chat resuming this work should read, in order after normal repository bootstrap/current roadmap/status owners:

1. Specs Census Part 15;
2. this Connector Operations Note;
3. the Conflict / Dual-Authority / Deferred-Debt Register;
4. the Migration Journal;
5. the ten Step-5.12 files above only as needed to revalidate/write Part 16.

It should **not** spend another cycle rediscovering the Step-5.12 family through recursive-root search.

Next durable action:

```text
revalidate current remote HEAD
-> finish Step-5.12 later-authority/supersession check
-> publish Specs Census Part 16 (S-179..S-188)
-> update Migration Journal with the Step-5.12 batch/cursor
-> fresh remote read-back
-> continue next semantic family
```

WP-07 substantive analysis remains **NOT STARTED** until the Documentation Corpus Refactor fully closes.