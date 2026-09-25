# W04.T04B-P1 W02 ancestry-evidence implementation impact brief

Status: **SENIOR_REVIEW_REQUIRED — P1 CANDIDATE NOT ACCEPTED**

Date: 2026-09-25

LAST_SAFE_SHA: `c9dd3f4a8f33dbb48d228308a8457bb140b3a5e5`

CURRENT_TASK: W04.T04B-P1 — W03 composable absorption/final-routing producer

## Trigger

The W03 classifier cannot distinguish a genuine W02 `RECONCILED_ANCESTOR_CURRENT_CLOSURE` outcome from a caller-constructed `PublicationOutcome` carrying the same public fields. `PublicationOutcome` currently contains status, intended commit SHA, observed HEAD SHA, cause, dispatched, and retry-with-force; it carries neither owner-issued provenance nor the ancestry evidence that W02 checked. Its dataclass constructor is public.

The issue was independently reported during P1 review and reproduced locally: a constructed accepted outcome with the P1 intended commit, cause `RECONCILED_ANCESTOR_CURRENT_CLOSURE`, and a different observed SHA with no ancestry evidence supplied was classified as accepted composed absorption evidence.

## Approved expectation

The accepted T04B-P1 Senior ruling requires:

- W03 issues group absorption evidence only from the exact typed W02 outcome of the joined publication;
- W02-reconciled ancestor-current-closure acceptance remains valid without another write;
- conflict, rejection, and unresolved indeterminate outcomes never become accepted absorption.

The ruling limits P1 production writes to `GAME/TOOLS/live_state.py` and expressly excludes `GAME/TOOLS/publication.py`, `runtime_host.py`, and their other owner surfaces. It names the classifier input as `PublicationOutcome` and does not define how W03 authenticates a W02-produced ancestor result.

## Discovered implementation pressure

W02 `reconcile_indeterminate_publication(...)` checks exact operation-digest closure and, when current HEAD differs from the intended commit, requires `CommitAncestryEvidence` establishing intended-commit ancestry before returning `RECONCILED_ANCESTOR_CURRENT_CLOSURE`. The returned `PublicationOutcome` does not retain that proof or otherwise certify that it came from W02. W03 receives only that ordinary constructible value, so checking its type and `cause` string cannot establish the required origin or ancestry relation.

The direct-confirmation/current-closure mismatch defect was repaired in the unpublished candidate: those accepted causes now require observed HEAD to equal the intended commit, with an RD09 regression. The valid W02 ancestor path is exercised. The follow-up independent review correctly found that a constructed ancestor-cause outcome with a different observed SHA and no ancestry evidence still passes; the candidate remains **TARGETED_REPAIR_REQUIRED**.

## Affected owners and consumers

- W02 publication/reconciliation evidence owner: `GAME/TOOLS/publication.py`;
- W02 service composition: `GAME/TOOLS/runtime_host.py`;
- W03 producer/classifier: `GAME/TOOLS/live_state.py`;
- consumers of the shared outcome contract include `GAME/TOOLS/collaboration.py` and `GAME/TOOLS/story.py`;
- relevant verification surfaces include `DEV/TESTS/test_rd09_access_live.py`, `DEV/TESTS/test_rd12_collaboration.py`, and W02 publication/recovery tests.

## Protected invariants at risk

- A false accepted result would let W03 represent absorption without proof that the same W02 campaign closure was current.
- Rejecting all ancestor outcomes would contradict the ruling’s required W02 ancestor-current-closure recovery behavior.
- Any evidence change must preserve one W02 transaction, exact operation closure, no second ref transition, and no LIVE replay.

## What can proceed without the disputed change

The existing unpublished P1 work prepares a deterministic owner-issued W03 delta, materializes native after-images and the final LIVE route, fails closed on unrepresentable pack/handoff contributions, and covers exact direct acceptance, exact-current-closure reconciliation, non-acceptance, member binding, forged delta/result, and CLOSED_UNABSORBED rejection. These pieces do not authorize P1 readiness while the ancestor-outcome boundary remains unresolved.

## Safe options for Senior disposition

1. **Recommended for review:** define the smallest W02-owned way to authenticate its outcome and carry/attest the exact ancestry proof, bound to the W02 attempt. W03 can then accept only owner-issued direct/current-closure results or verified ancestor results. This would expand P1’s owner/consumer impact beyond the ruling’s current write surface and requires a new authorization.
2. Change the W03 classifier contract to receive a separately owner-issued W02 ancestry proof and identify how T04B obtains/passes it. This changes the accepted classifier interface and consumer contract.
3. Disallow ancestor-current-closure acceptance at the W03 boundary. This fails closed but rejects a recovery result the current ruling explicitly requires W03 to classify; choosing it requires revising that expectation.

Do not implement one of these options until Senior resolves the owner/evidence boundary. No Product-Owner semantic change is proposed by this brief.

## Cost / risk if the recommendation is wrong

If a W02-issued proof is added unnecessarily, the implementation broadens a stable publication owner contract and may require consumer synchronization. If typed `PublicationOutcome` fields are treated as sufficient without verifiable W02 origin, forged ancestor-cause input can produce accepted absorption. If ancestor outcomes are rejected, a valid W02 reconciled campaign closure cannot complete the accepted T04B flow.

## Current evidence

```text
Fresh remote fetch: origin/v1/engine-rearchitecture == LAST_SAFE_SHA
P1 class: 21 passed
RD09 module: 192 passed
Scoped Ruff (F811, I, B009, TRY004, PIE810): PASS
P1-range Ruff format checks: PASS
Maintenance audit: PASS
Independent review: TARGETED_REPAIR_REQUIRED; direct mismatch addressed, ancestor provenance unresolved
Full local DEV pytest: 1253 passed, 5 skipped, 9 failed before environment triage
  - 4 S6D catalog/contract tests reproduced sequentially and are outside P1 write scope
  - 3 release-builder failures were caused by GAME __pycache__ created by local test imports; after removing those generated caches, all 3 passed sequentially with bytecode writing disabled
  - clean-checkout metadata test observed the expected dirty candidate worktree
  - version-census test included ignored `.entire` session logs and needs the repository-required clean exact-tree surface
Hosted CI: not available in this runtime
```

The P1 candidate remains uncommitted and unpublished in `GAME/TOOLS/live_state.py` and `DEV/TESTS/test_rd09_access_live.py`. Current candidate module impact is `framework_module_version 1.0.20 -> 1.0.21`; LIVE routing schema v4, native-state-pack schema v2, absorption-attempt schema v1, campaign-contract generation, and storage generation remain unchanged. No P1 candidate acceptance or T04B resume is claimed.

`VERSION_IMPACT: NONE` for this design/control brief and cursor synchronization; they do not change a version/revision/schema/generation namespace.
