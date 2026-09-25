# W04.T04B post-publication recovery evidence implementation impact brief

Status: **SENIOR_REVIEW_REQUIRED — T04B CANDIDATE NOT ACCEPTED**

Date: 2026-09-25

LAST_SAFE_SHA: `250120a7b7c886ffb7174990a77fa4cd02c149d`

CURRENT_TASK: W04.T04B — same-closure authority/Collaboration publication and recovery

## Trigger

The current T04B recovery path requires the exact in-memory W03 `ComposedCampaignAbsorptionPublication`. That result is ephemeral and owner-issued through an in-process nominal registry. If the process is lost after the W02 commit but before that result is retained/returned, a restarted caller cannot reconstruct it from fields or equality. `recover_collaboration_access_reconciliation(...)` accepts the reconciliation and RuntimeHost, but has no W02 owner path to revalidate the already-published attempt and reissue accepted evidence without a write.

Same-process recovery is covered: it succeeds when the exact owner-issued composed result is retained, the final route is current, and every required owner after-image matches. Missing or reconstructed evidence fails closed.

## Approved expectation

The stable T04B plan requires crash-before/after-publication verification and recovery that reproduces the same after-authority view. The accepted P1 ruling requires recovery to re-pin current authority and rederive the W03 delta from exact final LIVE sources/predecessor evidence; exact matching final owner after-images and final route may recover the result without another ref update.

P0 deliberately makes W02 acceptance evidence ephemeral and binds it to the exact `PublicationOutcome` instance. It is not serialized and creates no persistent schema. P1 composed evidence is also ephemeral and nominally owner-issued. These laws remain in force.

## Discovered implementation pressure

P0's `validate_owner_issued_accepted_publication(...)` accepts only the exact registered outcome instance. A reconstructed/equal-fields outcome after process loss has no W02 registry entry. RuntimeHost currently issues direct/current-closure/ancestor evidence only within `CampaignPublicationService.publish_owner_delta(...)` and its bounded `_reconcile_indeterminate(...)` path. There is no current read-only W02 operation to reissue exact closure/ancestry acceptance evidence for a previously committed attempt after restart.

The T04B candidate accepts a reconciliation only when its `composed_absorption` field contains owner-issued P1 evidence. A rehydrated T04A reconciliation has no such evidence; T04B rejects it. The current T04B tests cover recovery with retained composed evidence, not reconstruction after process loss.

## Affected owners and consumers

- W02 publication/evidence: `GAME/TOOLS/publication.py`;
- W02 bound repository/service composition: `GAME/TOOLS/runtime_host.py`;
- W03 LIVE owner-issued delta/composed evidence: `GAME/TOOLS/live_state.py`;
- W04 same-closure consumer/recovery: `GAME/TOOLS/collaboration.py`;
- relevant verification: `DEV/TESTS/test_rd06_durability_publication.py`, `DEV/TESTS/test_runtime_host_composition.py`, `DEV/TESTS/test_rd09_access_live.py`, and `DEV/TESTS/test_rd12_collaboration.py`.

The current T04B implementation envelope authorizes Collaboration production/test changes only. A W02 evidence-reissuance operation would cross that consumer boundary into the W02 publication/RuntimeHost owners.

## Protected invariants at risk

- Reconstructed or caller-shaped values cannot create W02 or W03 owner authority.
- Recovery must not dispatch a second `update_ref` merely to recreate evidence.
- W03 must not perform Git ancestry validation itself.
- `CLOSED_UNABSORBED` alone remains incomplete, and recovery must preserve exact source membership/final route and owner after-images.
- No evidence receipt/schema may be added under the current no-persistence ruling.

## What can proceed without the disputed change

The current T04B implementation joins P1 W03/native writes with access/PLAYER and Collaboration effects and submits the union once through W02. Same-process recovery with a retained P1 composed result validates exact final routing and after-images without another update. The no-LIVE path remains separate. T04B cannot claim the accepted crash-after-publication recovery contract until the missing-evidence case has an authorized path.

## Safe options for Senior disposition

1. **Recommended:** authorize a bounded W02-owned read-only revalidation/reissuance path for an already-published attempt. It would use the bound RepositoryPort to verify current ref, exact operation closure, and (when needed) bounded ancestry, then return fresh owner-issued evidence without an `update_ref`. W03 can rederive its delta from exact final sources and use the reissued W02 proof. This expands the P0/W02 evidence API and requires explicit owner authorization and tests.
2. Retain/reattach the exact ephemeral W02/P1 evidence across restart through an existing trustworthy host channel, if one can be established without persistence and without trusting caller-shaped values. No such current channel was found in the inspected W02/RuntimeHost/T04B contracts.
3. Revise the process-loss recovery expectation to remain blocked when ephemeral evidence is gone. This weakens the accepted Step-5.8/T04B recovery target and needs explicit architecture disposition.
4. Persist an acceptance receipt/schema. This adds a durable owner/lifecycle and is outside the current ruling; it would require a separate System-Impact/design gate.

Do not implement one of these options inside the current Collaboration-only T04B scope. Senior must settle the evidence-reissuance/authority boundary first. No Product-Owner semantic change is proposed by this brief.

## Cost / risk if the recommendation is wrong

If W02 reissuance is added unnecessarily, it broadens a stable publication interface and introduces a bounded read-only recovery path. If the missing-evidence case is treated as success from current field equality, callers could manufacture accepted absorption. If recovery is permanently blocked when a process loses the ephemeral result, the accepted crash/retry contract is not fulfilled. A persisted receipt adds schema, ownership and lifecycle consequences not presently authorized.

## Current evidence

```text
Fresh remote HEAD / LAST_SAFE_SHA: 250120a7b7c886ffb7174990a77fa4cd02c149d
P0 output: W02_VERIFIED_CAMPAIGN_PUBLICATION_EVIDENCE_READY; independent PASS/read-back
P1 output: W03_COMPOSABLE_CAMPAIGN_ABSORPTION_DELTA_READY; independent PASS/read-back
RD12 focused unittest after T04B candidate: 142 passed
T04B worker combined relevant suites: 404 passed
Independent T04B review: TARGETED_REPAIR_REQUIRED for process-loss reissuance
T04B maintenance audit: blocked by ignored GAME/TOOLS/__pycache__ release-boundary finding
T04B full clean-tree suite: not yet available; candidate remains uncommitted
Hosted CI: unavailable in this runtime
```

T04B's unpublished candidate is confined to `GAME/TOOLS/collaboration.py` and `DEV/TESTS/test_rd12_collaboration.py`. Its provisional module impact is Collaboration `1.0.18 -> 1.0.19` if the baseline remains current; schema v3 is unchanged. No T04B checkpoint or acceptance is claimed.

`VERSION_IMPACT: NONE` for this impact brief and current-progress/status synchronization.
