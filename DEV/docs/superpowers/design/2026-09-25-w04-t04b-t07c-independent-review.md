
# Independent review — W04.T04B repair and W04.T07C

Status: FINAL DISPOSITION — T04B TARGETED REPAIR REQUIRED / T07C TARGETED REPAIR REQUIRED

Date: 2026-09-25

## Exact review basis

Reviewed remote HEAD: 959de8e2d91e46ff326b046ee39045afa04b952d
T04B repair candidate: 6bb8723ff5ef8f3508d53303ba614d42222393d3
T07C actual feature commit: f5732ed31c7b3b5288dd43b62bf6847dc96f4702
T07C exact-page correction: 0c5cbc78174ca3545d4342674ba9afe9ae50622c

The previously recorded full T07C SHA f5732ed6e259f4ea0fa71764c153b61a54cc1082 does not identify a GitHub commit in this repository. Current control state must use f5732ed31c7b3b5288dd43b62bf6847dc96f4702.

Role: independent reviewer. No production code, executable tests, schemas or architecture owners are changed by this review.

Previously accepted T04A and T07B checkpoints remain accepted.

## Bounded Source Manifest

- GAME/TOOLS/collaboration.py blob f04775f8592b35d2b69a2bc62686bc84204e0a6b
- DEV/TESTS/test_rd12_collaboration.py blob 82af416a3e44937230a8da60fd5e00ac3add5495
- GAME/TOOLS/history.py blob 8d4d059f6bfc6504bd15aa429aee01a0ea8e22fa
- GAME/TOOLS/story.py blob 6166bf35af10c47b23dcee0c7375d3b6e16ec2ed
- DEV/TESTS/test_rd13_story_t0_commentator.py blob cdcea89731ae8520972a9a1b795bd5af36ff64ee
- semantic-event-t0-basis schema blob e67f70c67c9ff3f2d059b9547ef28da4149c6e7f
- Story EVENTS schema blob 5cf750aa57f2af03b544e18f42ff737793d07bf8
- Story projection-state schema blob 9da7c1fbc161dc17494104745bca4674f3b4f3cc
- SemanticEvent schema blob 0b98c2c56f3b0b4874e1b0363fa20889dcc7ad7c
- stable Wave-04 plan
- Step-5.8 LIVE ownership canonical spec
- Step-5.10 Story projection durability canonical spec
- Story self-contained corpus owner decision

Review graph:

    W03 access/LIVE owner
      -> accepted T04A preparation
      -> T04B physical same-boundary publication/recovery
      -> T05C

    native SemanticEvent / History
      -> accepted T07B source contracts
      -> T07C Story-local T0 + EVENTS publication/currentness
      -> T07D

## Exact-head hosted verification

GitHub has exact-head evidence even though the worker runtime could not see it:

    workflow: Validate engine source
    head_sha: 959de8e2d91e46ff326b046ee39045afa04b952d
    run: 36063512416
    job: 107847776125
    status/conclusion: completed / success
    maintenance audit: PASS
    DEV unit tests: Ran 1213 tests in 32.209s
    result: OK, skipped=5
    VERSION_UNCLASSIFIED=[]
    VERSION_LEGACY_HITS=[]

The local protected .entire census failure did not reproduce in the clean hosted checkout. This does not claim the local capture/scanning issue is repaired.

The findings below are established by exact code/contract tracing. The reviewer did not add or execute the new negative witnesses proposed below.

# T04B re-review

Disposition:

    W04.T04B: FAIL / TARGETED_REPAIR_REQUIRED
    IRR-T04B-01: CLOSED
    IRR-T04B-02: BLOCKING / PARTIALLY REPAIRED
    W04_AUTHORITY_COLLABORATION_RECONCILED: NOT ACCEPTED
    W04.T05C: BLOCKED

## IRR-T04B-01 — CLOSED — complete effect set is independently rederived

The repair no longer treats agreement between carrier fields as completeness proof.

_rederive_access_reconciliation_effects now reloads the exact predecessor campaign and PLAYER state, reproduces the W03 after-authority view, derives the complete obligation set from predecessor PLAYER route refs, reloads predecessor obligations by known ID, recalculates opportunity/agency effects, checks exact current obligation and terminal route cleanup state, then compares that independently derived set with the reconciliation carrier.

RD12 contains empty, subset, extra-effect and partially-applied-state witnesses. No generic scan or caller complete flag was introduced.

## IRR-T04B-02 — BLOCKING — close proof exists, but absorption/final routing is absent from the same campaign closure

The repair correctly blocks ACTIVE, partial/indeterminate, stale and missing selected-LIVE cases and invokes existing W03 forward semantics.

The positive path still does not establish the complete Step-5.8 boundary.

The positive LIVE regression explicitly asserts that:

    MANIFEST has no live_routing
    MANIFEST.yaml is absent from T04B path_operations

The implementation calls W03 publish_forward_transition as a proof, then removes access_transition and live_routing from that forward campaign result before comparing it to the access proposed campaign. The eventual W02 write-set contains access/PLAYER, collaboration obligation and route-ref cleanup, but no W03 absorption/finalization/current-routing delta.

Recovery also accepts a selected route whose sources are CLOSED_UNABSORBED.

Under Step-5.8, CLOSED_UNABSORBED remains current LIVE truth with zero ordinary writers; it is not absorbed campaign state. The revocation boundary requires applicable absorption/finalization, authorization removal and route changes in the same campaign transition.

Therefore the repair closes the source-freeze prerequisite but not the positive same-boundary transfer.

### Required repair

Preserve all new negative source-close checks and complete effect-set proof.

For a LIVE-sensitive positive path, the same W02 campaign closure that establishes access/collaboration effects must also carry the applicable W03-owned absorption/final-routing delta. Recovery succeeds only from the corresponding absorbed/final routed campaign state; CLOSED_UNABSORBED alone is insufficient.

Do not synthesize Collaboration-owned LIVE routing, an absorbed boolean, ad-hoc MANIFEST semantics, source reopen, or a second campaign commit.

If current accepted W03 code has no concrete owner-local write-set/adapter capable of realizing the already accepted forward absorption into this W02 closure, stop T04B at a System-Impact gate and record that exact missing producer interface. Do not invent it inside Collaboration.

Required witnesses include:
- ACTIVE/partial/indeterminate/stale cases remain zero-write failures;
- closed-but-unabsorbed recovery is not accepted as completed revocation;
- positive LIVE publication performs one ref update with both W03 absorption/routing and access/collaboration effects;
- recovery proves that same absorbed/final routed state;
- no-LIVE path remains unchanged;
- crash/indeterminate publication never repeats LIVE mechanics/CAS.

# T07C independent review

Disposition:

    W04.T07C: FAIL / TARGETED_REPAIR_REQUIRED
    IRR-T07C-01: BLOCKING
    IRR-T07C-02: BLOCKING
    W04_T0_STORY_READY: NOT ACCEPTED
    W04.T07D: BLOCKED

The candidate correctly:
- copies T0 from the exact accepted SemanticEvent rather than Actor T1;
- re-reads the exact native bounded page before publication;
- requires every selected E-EVT candidate to materialize;
- publishes records, lookup, allocator and coverage in one W02 transaction;
- rejects stale native/current campaign movement;
- preserves selected LIVE origin without LOCAL fallback;
- accepts no caller omission flag.

These properties must remain.

## IRR-T07C-01 — BLOCKING — retained T0 drops required availability/protection classification

The self-contained Story owner requires each qualifying retained T0 factor to remain Story-locally recoverable with factor identity, event-time value/stance, provenance/source binding, and availability classification/correct protection metadata.

The stable T07C plan also requires private/off-screen material to remain retained but availability-filtered.

Current T0 factor shape contains only:

    owner_family
    factor_id
    t0_value
    provenance_refs

Neither semantic-event-t0-basis.schema.json nor history.validate_t0_basis has a protection/availability field.

The materialized Story EVENTS unit copies that incomplete basis. Its unit-level availability merely points back to the SemanticEvent and does not encode protection of individual retained T0 factors.

The current positive test even marks the native event private_offscreen=true, persists the secret T0 factors, and expects only a generic SemanticEvent source reference as availability.

T07D cannot reconstruct historical T0 protection from mutable current native state without breaking the self-contained corpus law. T07D may own reader filtering, but T07C must persist the historical protection input required for that filtering.

### Required repair

Extend the retained native/Story-local T0 representation with the accepted event-time protection/availability classification, or an equivalent immutable representation derived from existing information/access owners. Story copies it unchanged from the accepted native event; it must not derive historical protection from current Actor/knowledge/disclosure state.

Required witnesses:
- private/off-screen factor retained with restrictive protection metadata;
- public factor retained with its admitted classification;
- later T1/access drift does not rewrite historical T0 protection;
- missing/malformed protection on a qualifying retained factor fails closed;
- an ineligible reader does not cause the secret factor to disappear from the comprehensive Story corpus.

This is within existing T07C/SCC semantics. No new Story layer or ACL owner is authorized.

Because this repair changes persisted T0/Story contract semantics, rerun the Version Impact Gate. The candidate assumption that schema versions remain unchanged is not accepted for the repaired shape.

## IRR-T07C-02 — BLOCKING — an older exact already-covered page is rejected instead of idempotently discarded

Step-5.10 makes coverage the baseline catch-up idempotency evidence.

Current code recognizes ALREADY_COVERED only when page upper equals persisted coverage. If page upper is lower than persisted coverage, it raises that the source upper moved behind coverage.

For a bounded page, that is not necessarily a source rewind.

Concrete current sequence:

    publish evt page 1 -> coverage evt:1
    publish evt page 2 -> coverage evt:2
    retry exact evt page 1 -> current code raises

Page 1 is an exact already-covered prefix. Step-5.10 coverage says it is idempotently covered; it must not allocate IDs or publish again.

The existing retry test retries page 1 only while coverage remains exactly evt:1, so it misses this case.

### Required repair

After exact native page revalidation and compatible source-domain/contract validation, a page wholly at or behind compatible persisted coverage is an already-covered prefix. Return an idempotent result with zero Story write.

Do not weaken source revalidation: a mutated/stale older page must still reject before covered-prefix acknowledgement.

Required witnesses:
- page1 -> page2 -> retry exact page1 => ALREADY_COVERED, zero write;
- mutated page1 after coverage advanced still rejects;
- incompatible coverage generation rejects;
- uncovered gap/noncontiguous next page rejects.

# Version and scope disposition

Candidate versions remain unaccepted task closure:

    collaboration 1.0.18
    History 1.0.4
    durability 1.0.4
    Story 1.0.7

Accepted T07B Story 1.0.6 remains the last accepted Story task checkpoint.

IRR-T07C-01 requires a fresh persisted-schema Version Impact assessment; this review does not pre-select the exact schema numbers or migration disposition.

No campaign/storage/catalog/engine generation or migration execution is changed by this review.

Final scheduling:

    T04B repair and T07C repair may run in parallel if write sets remain disjoint.
    T05C waits for T04B independent PASS.
    T07D waits for T07C independent PASS.
    Wave 04 remains incomplete.
    Wave 05 remains unauthorized.

VERSION_IMPACT: NONE for this review/control publication.
