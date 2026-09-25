# W04.T04B post-publication recovery evidence Senior ruling

Status: **ACCEPTED — AUTHORIZE BOUNDED W02 READ-ONLY REVALIDATION / REISSUANCE**

Date: 2026-09-25

Reviewed remote HEAD: ed3131681955830ee640ed79bca8398d2de86c53

Role: HDM Senior Architect / targeted System-Impact Design Reviewer.

Scope: only the process-loss recovery evidence gap discovered after independently accepted T04B-P0 and T04B-P1. T04A, P0, P1, T07B and T07C remain accepted. The unpublished T04B candidate remains unaccepted.

## Decision

Select option 1 from the implementation-impact brief.

Authorize a bounded W02-owned read-only post-publication revalidation/reissuance path.

Reject option 3 / same-process-only recovery. Step-5.6 already states that when remote publication succeeds and the process crashes before local clearing, repository/native source is authority and cold recovery must reconstruct from actual source without gameplay replay. Restricting T04B to retained in-memory evidence would weaken an accepted durability guarantee.

Reject durable receipt persistence for this boundary. W02 can re-prove the same publication closure from repository authority. Persisting a derivative acceptance receipt would introduce a redundant journal/owner/lifecycle and a new schema without evidence that it is necessary.

No Product-Owner decision is required. This is a machine recovery-boundary realization of already accepted Step-5.6 and Step-5.8 semantics.

## New prerequisite

Introduce W04.T04B-P0R — W02 read-only post-publication acceptance revalidation.

Output checkpoint: W02_POSTPUBLICATION_REVALIDATION_READY.

Current dependency sequence becomes:

    T04B-P0 PASS
    T04B-P1 PASS
      -> T04B-P0R implementation
      -> independent PASS / remote read-back
      -> resume T04B recovery implementation
      -> T04B independent PASS
      -> T05C eligible through its existing join

P0R does not reopen Wave 02 or invalidate P0. It extends the accepted W02 ephemeral-evidence model with a cold-recovery issuer that re-proves authority from repository state.

## Semantic owner and allowed write surfaces

Semantic owner: W02 campaign publication / crash reconciliation.

Primary production owners:
- GAME/TOOLS/publication.py
- GAME/TOOLS/runtime_host.py

Primary tests:
- DEV/TESTS/test_rd06_durability_publication.py
- DEV/TESTS/test_runtime_host_composition.py

Normal version/control bookkeeping is permitted.

No P0R production edits are authorized in live_state.py, collaboration.py, access_control.py, story.py, durability.py, RepositoryPort protocol, persisted schemas, or Wave-05 shared writers.

The current unpublished T04B candidate remains local/unaccepted and must not enter the P0R checkpoint.

## Preserve the P0/P1 trust model

PublicationOutcome remains an ordinary constructible value and is never authority from field equality.

P0 owner-issued evidence remains ephemeral and exact-instance bound.

P1 ComposedCampaignAbsorptionPublication remains ephemeral and owner-issued.

P0R does not persist either evidence object. It performs new read-only proof from repository authority and then issues a fresh exact-instance W02 accepted PublicationOutcome/evidence pair that the unchanged P1 classifier can consume.

A caller-supplied expected predecessor or intended commit SHA is only a nomination. W02 must prove it from the bound repository before issuing authority.

## Required W02 recovery basis

P0R may introduce an ephemeral W02 recovery-attempt/basis type equivalent in semantics to:

    campaign_id
    repository_id
    target_ref
    pinned_head_sha
    base_tree_sha
    intended_commit_sha
    routed_operation
    exact normalized path_operations / operation_digests
    owner_generations
    publication_reason

It is not a persisted PublicationPlan and carries no gameplay authority.

Do not fabricate or pretend to reconstruct the original acting principal after process loss. Recovery is proving an already-authoritative repository closure; it is not re-authorizing or re-executing the original write.

Normal in-process P0 evidence continues to retain the original FrozenCampaignPublicationAttempt. Recovery evidence may bind the new W02 recovery-basis type instead. validate_owner_issued_accepted_publication must preserve its existing campaign/predecessor/operation-subset semantics for both owner-issued paths.

## RuntimeHost read-only API

CampaignPublicationService may add an owner-neutral read-only operation equivalent to:

    revalidate_published_owner_delta(
        routed_operation,
        path_operations,
        owner_generations,
        publication_reason,
        expected_pinned_head_sha,
        intended_commit_sha,
    ) -> PublicationOutcome

Exact spelling may follow current conventions.

The method MUST NOT call create_tree, create_commit or update_ref.

It uses only the already accepted RepositoryPort/read capability and the existing publication transport read side where needed.

## Exact proof algorithm

Let H be expected_pinned_head_sha, C be nominated intended_commit_sha, and D be current authoritative HEAD.

1. Validate campaign/ref/repository identity from the bound RuntimeHost.
2. Read exact commit H and recover its exact tree identity.
3. Construct an exact predecessor PinnedCampaign at H and read predecessor MANIFEST/CAMPAIGN_CARD through read_exact_path.
4. Validate the rederived routed operation and full normalized path-operation set against that predecessor basis. The recovery path must not add a newly discovered semantic path.
5. Read exact commit C.
6. Require C to be a single-parent direct child of H.
7. Require exact commit/tree evidence for C and require its bounded changed-path set to equal the rederived normalized W02 path set. A direct child that contains an extra path is not this publication attempt.
8. Read every attempted path at C and require exact operation digests/body closure.
9. Read current authoritative HEAD D and exact current closure for every attempted path.
10. If D == C and closure is exact, issue a fresh accepted PublicationOutcome with RECONCILED_CURRENT_CLOSURE semantics and fresh owner-issued W02 evidence.
11. If D != C, require existing RepositoryPort ancestry proof C -> D. If C is an ancestor and D preserves the complete attempted operation closure, issue RECONCILED_ANCESTOR_CURRENT_CLOSURE plus exact owner-issued closure/ancestry evidence.
12. If C is absent from current lineage, if a required path differs at D, or if exact H/C commit proof is incompatible, return conflict/revalidation-required semantics and issue no accepted evidence.
13. If exact commit/tree/changed-path/ancestry evidence is unavailable or ambiguous, fail closed / return indeterminate; never infer success.

Step-5.6 already requires exact commit/tree/path reads and bounded changed-path/ancestry comparison. P0R adds no new RepositoryPort method or authority. The implementation may normalize richer read_exact_commit evidence into a private typed commit-proof value. If the deployment adapter cannot prove the exact parent/tree/changed-path facts required above, P0R is unavailable for that profile and fails closed; do not add a second repository authority.

## Owner-issued evidence after revalidation

After the proof above, W02 creates a fresh PublicationOutcome and registers fresh owner-issued acceptance evidence using the existing P0 exact-instance mechanism.

For D == C:
- outcome cause semantics are RECONCILED_CURRENT_CLOSURE;
- dispatched is false;
- intended == observed == C;
- closure base is H and closure head is C.

For C ancestor of D:
- outcome cause semantics are RECONCILED_ANCESTOR_CURRENT_CLOSURE;
- dispatched is false;
- intended is C;
- observed is D;
- closure base is H and closure head is D;
- ancestry binds exactly C -> D.

The fresh result is not claiming that the current process performed the original write. It is a W02 read-only revalidation of already-authoritative repository state.

Directly constructing the same result/evidence fields remains non-authoritative.

## P1 and T04B consumption

No P1 production change is required if P0R returns a normal fresh owner-issued PublicationOutcome accepted by validate_owner_issued_accepted_publication.

During T04B cold recovery:

1. re-pin/reload exact current authority;
2. rederive the W03 FrozenCampaignAbsorptionDelta from exact final sources and predecessor evidence under the accepted P1 law;
3. rederive the complete joined W02 path_operations: W03 absorption/final routing + PLAYER/access + Collaboration;
4. call P0R with H = the exact predecessor and C = the rederived delta proposed campaign revision;
5. pass the freshly W02-issued outcome through the unchanged P1 classify_composed_campaign_absorption;
6. validate final route, source members and every owner after-image;
7. recover the T04B result without any second ref update, LIVE close, mechanics replay or source CAS.

CLOSED_UNABSORBED alone remains insufficient.

If T04B cannot deterministically rederive the exact joined operation set or intended commit candidate from its accepted durable/native evidence, that is a new System-Impact event; do not weaken P0R into field-equality acceptance.

## Required P0R RED/GREEN evidence

### W02 / RuntimeHost

1. exact C current at D == C revalidates and issues owner evidence with zero create_tree/create_commit/update_ref calls;
2. exact C ancestor of D with unchanged required closure revalidates and issues owner ancestry evidence with zero writes;
3. caller-nominated C that is not a direct single-parent child of H fails;
4. C with an extra changed path fails even if all requested operation paths match;
5. missing/changed requested path at C fails;
6. D that changes any required operation path fails;
7. C not in current lineage fails;
8. unavailable/ambiguous parent/tree/changed-path/ancestry evidence fails closed;
9. wrong campaign/ref/repository/predecessor fails;
10. copied/reconstructed/equal-fields reissued outcome is rejected by the existing owner validator;
11. exact reissued outcome passes required-operation-subset validation;
12. no technical acting-principal reauthorization is required or treated as proof of the historical writer;
13. no create_tree, create_commit or update_ref occurs in the revalidation path.

### T04B follow-up after P0R PASS

1. process-loss recovery with no retained P0/P1 objects succeeds from exact already-published current closure;
2. process-loss recovery also succeeds when the intended T04B commit is an ancestor of a compatible disjoint descendant;
3. overlapping descendant change fails closed;
4. forged/reconstructed P0/P1 values still fail;
5. recovery dispatches no second W02 write and no LIVE CAS/mechanics replay;
6. same-process retained-evidence recovery remains valid.

## Version Impact

This Senior ruling/control publication: VERSION_IMPACT NONE.

Expected P0R implementation impact, subject to fresh worker check:
- publication.py framework_module_version 1.0.5 -> 1.0.6;
- runtime_host.py framework_module_version 1.0.9 -> 1.0.10.

No persistent schema, campaign-contract generation, storage/catalog/engine generation, migration or dual-read change is expected.

live_state.py 1.0.21 / accepted P1 remains unchanged.

After P0R PASS, T04B resumes from its current fresh baseline and owns its normal Collaboration module bump once.

If implementation requires a persisted receipt, new RepositoryPort method/authority, new trust boundary, or alteration of Step-5.6 publication-success semantics, stop at a new System-Impact gate.

## Final disposition

    RECOVERY OPTION: W02 READ-ONLY REVALIDATION / REISSUANCE
    SAME-PROCESS-ONLY: REJECTED
    DURABLE RECEIPT PERSISTENCE: NOT AUTHORIZED / NOT REQUIRED
    PO DECISION: NOT REQUIRED
    T04B-P0R: AUTHORIZED
    T04B: PAUSED UNTIL P0R INDEPENDENT PASS / READ-BACK
    T05C: BLOCKED
    T07D: INDEPENDENTLY AUTHORIZED
    WAVE 05: NOT AUTHORIZED

SYSTEM_IMPACT: RESOLVED TO BOUNDED W02 READ-ONLY PREREQUISITE.
