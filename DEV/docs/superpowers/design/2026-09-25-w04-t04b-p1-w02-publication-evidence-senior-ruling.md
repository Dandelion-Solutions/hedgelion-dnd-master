# W04.T04B-P1 W02 publication-evidence Senior ruling

Status: **ACCEPTED — ADD BOUNDED W02 PREREQUISITE P0**

Date: 2026-09-25

Reviewed remote HEAD: `64eeb2a9fa876294b93e4d3267eec93f4ec03abb`

Role: HDM Senior Architect / targeted System-Impact Design Reviewer

Scope: only the new W02/W03 ancestry-evidence boundary discovered while implementing W04.T04B-P1. T04A, T07B and T07C remain accepted. T07D remains independently authorized. The unpublished P1 code remains unaccepted.

## Ruling

Select **Option 1** from the impact brief.

The defect is not in Step-5.8 semantics and does not require a Product-Owner decision. W02 already owns publication currentness and ancestry reconciliation. The defect is that W02 currently returns a caller-constructible `PublicationOutcome` after performing that proof and discards the provenance/proof binding needed by W03.

The accepted correction is therefore:

```text
raw PublicationOutcome
  = ordinary constructible result value
  != authority by itself

W02 CampaignPublicationService
  + exact FrozenCampaignPublicationAttempt
  + trusted direct/ref or closure/ancestry proof
  -> owner-issued acceptance evidence bound to that exact outcome instance

W03
  -> may classify composed absorption only after W02 validates that owner-issued evidence
```

W03 must not independently re-run or reinterpret Git ancestry.

This is a bounded implementation-boundary change. No public product semantics, persistence semantics or campaign authority law changes.

## New prerequisite

Introduce:

**W04.T04B-P0 — W02 verified campaign-publication acceptance evidence**

Dependency:

```text
T04A PASS
  -> T04B-P0
  -> independent PASS/read-back
  -> T04B-P1 resumes
  -> independent PASS/read-back
  -> T04B resumes
```

P0 does not reopen Wave 02. It realizes provenance for an already accepted W02 reconciliation decision.

Output checkpoint:

`W02_VERIFIED_CAMPAIGN_PUBLICATION_EVIDENCE_READY`

## Owner and allowed implementation surface

Semantic owner: W02 campaign publication / crash-reconciliation owner.

Primary Python owner:
- `GAME/TOOLS/publication.py`

Composition owner:
- `GAME/TOOLS/runtime_host.py`

Primary tests:
- `DEV/TESTS/test_rd06_durability_publication.py`
- `DEV/TESTS/test_runtime_host_composition.py`

No P0 production edits are authorized in:
- `GAME/TOOLS/live_state.py`;
- `GAME/TOOLS/collaboration.py`;
- `GAME/TOOLS/story.py`;
- `GAME/TOOLS/access_control.py`;
- RepositoryPort;
- persisted schemas;
- Wave-05 shared surfaces.

The worker's current unpublished P1 files remain separate/unaccepted until P0 PASS.

## Preserve PublicationOutcome as the common result value

Do **not** replace the current common `PublicationOutcome` contract and do not require existing Story/Collaboration consumers to change their ordinary success/error handling.

A raw `PublicationOutcome` remains constructible and remains useful as the transport/reconciliation result value.

Its fields are not authority for W03.

The W02 change adds owner-issued evidence **around the exact accepted instance** rather than turning public field equality into proof.

## Owner-issued acceptance evidence

W02 adds a typed immutable evidence record equivalent to:

```python
class PublicationAcceptanceKind(StrEnum):
    CONFIRMED_REF = "CONFIRMED_REF"
    RECONCILED_CURRENT_CLOSURE = "RECONCILED_CURRENT_CLOSURE"
    RECONCILED_ANCESTOR_CURRENT_CLOSURE = "RECONCILED_ANCESTOR_CURRENT_CLOSURE"

@dataclass(frozen=True, slots=True)
class PublicationAcceptanceEvidence:
    kind: PublicationAcceptanceKind
    attempt: FrozenCampaignPublicationAttempt
    intended_commit_sha: str
    observed_head_sha: str
    current_closure: PublicationCurrentClosureEvidence | None
    ancestry: CommitAncestryEvidence | None
```

Exact spelling may follow current module conventions, but these semantics are required.

Evidence is ephemeral. It is not serialized and creates no new persistent schema.

W02 keeps a nominal owner-issued binding from the **exact PublicationOutcome instance** to the evidence. Follow the existing project owner-issued pattern: private issuer/registry with exact-instance validation. A reconstructed/copy/equal-fields outcome must not inherit issuance.

Direct caller construction of:
- `PublicationOutcome`;
- `PublicationCurrentClosureEvidence`;
- `CommitAncestryEvidence`;

must not be enough to mint accepted evidence.

Arbitrary in-process mutation of private issuer state remains TCB compromise under the already accepted RuntimeHost trust model.

## W02 issuer / validator boundary

`publication.py` owns an internal issuance function used only after trusted W02 service work and a public owner-validator equivalent to:

```python
def validate_owner_issued_accepted_publication(
    outcome: PublicationOutcome,
    *,
    campaign_id: str,
    expected_pinned_head_sha: str,
    required_operation_digests: Mapping[str, str] | None = None,
) -> PublicationAcceptanceEvidence:
    ...
```

The validator:

1. requires the exact registered outcome instance;
2. requires `status == ACCEPTED`;
3. validates campaign/predecessor binding through the frozen attempt;
4. validates outcome intended/observed SHA against the evidence;
5. validates cause/proof-kind correspondence;
6. validates the W02 attempt's operation digests;
7. when `required_operation_digests` are provided, requires each required path/digest to be an exact subset of the joined W02 attempt;
8. returns the owner-issued evidence only after all checks pass.

The subset rule is required for T04B-P1: the W03 delta is one owner subset inside the later joined W02 transaction that also carries PLAYER/access and Collaboration operations.

No caller boolean or free-form cause string may substitute for this validator.

## Direct confirmed acceptance

For a trusted CampaignPublicationService ref update classified as:

`CONFIRMED_ACCEPTED`

W02 may issue `CONFIRMED_REF` evidence only when:

- `outcome.intended_commit_sha` is the actual commit created for this frozen attempt;
- `outcome.observed_head_sha == outcome.intended_commit_sha`;
- the result came through the bound CampaignPublicationService transport operation;
- no closure/ancestry proof is claimed.

Calling `classify_ref_transition(...)` directly with fabricated response bytes may produce a raw `PublicationOutcome`, but that raw object is **not owner-issued acceptance evidence**.

## Reconciled current closure

For:

`RECONCILED_CURRENT_CLOSURE`

W02 issues evidence only when the trusted RuntimeHost current-read path supplied the exact `PublicationCurrentClosureEvidence` consumed by `reconcile_indeterminate_publication(...)`, and:

- closure base == attempt pinned head;
- closure head == intended commit;
- closure operation digests exactly satisfy the existing W02 reconciliation law;
- outcome observed head == intended commit;
- no ancestry evidence is present.

A caller invoking the pure reconciliation function with self-constructed closure values does not automatically obtain owner-issued evidence. Issuance occurs at the trusted CampaignPublicationService boundary after the same evidence was actually read through its bound RepositoryPort.

## Reconciled ancestor current closure

For:

`RECONCILED_ANCESTOR_CURRENT_CLOSURE`

W02 issues evidence only when the trusted current-read path supplied **both**:

- the exact `PublicationCurrentClosureEvidence` used for bounded operation closure;
- the exact `CommitAncestryEvidence` produced from the bound RepositoryPort ancestry read.

Required bindings:

```text
ancestry.ancestor_sha == intended_commit_sha
ancestry.descendant_sha == observed_head_sha
closure.head_sha == observed_head_sha
closure.base_revision == attempt.pinned_head_sha
all attempted operation digests are present and equal
```

The existing W02 rule permitting additional disjoint paths at a descendant HEAD remains unchanged.

The ancestry proof is retained only as ephemeral W02 evidence attached to the accepted result; it does not become chronology or campaign semantics.

## RuntimeHost change

`CampaignPublicationService.publish_owner_delta(...)` continues to return a `PublicationOutcome`, preserving existing consumers.

However, for accepted outcomes it must arrange W02 owner issuance before returning.

For direct acceptance it binds the exact frozen attempt and direct ref result.

For indeterminate reconciliation, `CampaignPublicationService._reconcile_indeterminate(...)` must retain the actual closure/ancestry evidence obtained by its trusted `read_current` callback long enough to issue W02 acceptance evidence after `reconcile_indeterminate_publication(...)` returns ACCEPTED.

Non-accepted outcomes are not accepted-evidence-bearing.

No second ref update/read cycle is introduced merely to issue evidence.

## W03 consumption after P0 PASS

T04B-P1 keeps its W03 semantic owner.

Its composed classifier no longer treats:

```text
isinstance(publication, PublicationOutcome)
+ status/cause/observed fields
```

as sufficient.

It must call the W02 owner validator using:

- delta campaign id;
- delta expected campaign revision;
- delta operation digests as the required subset.

Only returned W02 owner-issued acceptance evidence can produce accepted `ComposedCampaignAbsorptionPublication`.

W03 may additionally enforce its own already-authorized bindings:
- direct/current acceptance observed HEAD must equal intended;
- ancestor evidence must use the W02-validated ancestor kind;
- exact source members/final route/delta remain W03-owned checks.

W03 does not inspect Git ancestry independently.

## Why a separate ancestry argument is rejected

Option 2 is not selected.

Passing a separately supplied ancestry object into W03:
- expands the consumer API unnecessarily;
- invites W03 to become a second proof combiner;
- makes it easier to mix evidence from different attempts;
- duplicates a proof W02 has already completed.

The W02-owned attestation keeps proof composition in the correct owner.

## Why ancestor acceptance is retained

Option 3 is not selected.

Step-5.6 already permits accepted recovery when the intended commit is an ancestor of current HEAD and the frozen operation closure remains exact. T04B-P1 must preserve that accepted recovery path without another write.

Failing all ancestor reconciliations would be a semantic regression in crash/retry behavior and is unnecessary.

## Required P0 RED/GREEN evidence

### publication.py / W02 tests

1. directly constructed accepted `PublicationOutcome` has no owner-issued evidence;
2. raw accepted result from direct `classify_ref_transition` alone has no owner-issued evidence;
3. raw accepted result from direct `reconcile_indeterminate_publication` alone has no owner-issued evidence, even with constructible closure/ancestry objects;
4. owner-issued direct acceptance validates only for the exact outcome instance/attempt;
5. copied/reconstructed/equal-fields outcome is rejected;
6. current-closure evidence binds exact attempt, intended HEAD and operation digests;
7. ancestor evidence binds exact attempt, closure HEAD and exact ancestor/descendant pair;
8. wrong ancestry pair, wrong closure base/head, missing attempted path or changed digest cannot be issued/validated;
9. required operation subset succeeds only when all required W03 paths/digests occur identically in the frozen W02 attempt;
10. foreign campaign/predecessor/attempt fails.

### RuntimeHost tests

1. CampaignPublicationService direct accepted path returns a normal `PublicationOutcome` that is also W02-owner-validatable;
2. reconciled-current path returns owner-validatable evidence with retained closure proof;
3. reconciled-ancestor path returns owner-validatable evidence with retained closure + ancestry proof;
4. conflict/rejected/unresolved-indeterminate results are not accepted-evidence-bearing;
5. no extra `update_ref` is dispatched to create the evidence;
6. trusted evidence is from the same bound repository/campaign root.

### P1 follow-up tests

After P0 independent PASS:
- the existing forged ancestor outcome reproduction must fail;
- genuine RuntimeHost ancestor reconciliation must still yield accepted composed absorption;
- direct/current acceptance remains accepted only when W02 owner-issued;
- no P1 second write/CAS is added.

## Version Impact

This Senior ruling/control publication:

`VERSION_IMPACT: NONE`

Expected P0 implementation impact, subject to fresh worker check:

```text
GAME/TOOLS/publication.py
  framework_module_version 1.0.4 -> 1.0.5

GAME/TOOLS/runtime_host.py
  framework_module_version 1.0.8 -> 1.0.9
```

No persistent schema, campaign-contract generation, storage generation, catalog generation, engine release or migration/dual-read change is expected.

T04B-P1 retains its already expected `live_state.py 1.0.20 -> 1.0.21` transition when it resumes, provided the baseline is still current.

If implementing P0 requires a persisted receipt/evidence record, a new RepositoryPort authority, a new external trust boundary or changes to Step-5.6 acceptance semantics, stop at a new System-Impact gate.

## Allowed P0 write surfaces

Production:
- `GAME/TOOLS/publication.py`;
- `GAME/TOOLS/runtime_host.py`.

Tests:
- `DEV/TESTS/test_rd06_durability_publication.py`;
- `DEV/TESTS/test_runtime_host_composition.py`.

Control/version bookkeeping required by the normal process is allowed.

No other production surface is authorized by this ruling.

## Resume sequence

```text
current impact brief
-> W04.T04B-P0 implementation
-> P0 independent PASS / publish / read-back
-> resume existing unpublished T04B-P1 work
-> P1 independent PASS / publish / read-back
-> resume T04B
-> T04B independent PASS
-> T05C eligible
```

No further Senior or PO gate is needed between these checkpoints unless a new System-Impact trigger fires.

T07D remains independent and may continue in parallel.

SYSTEM_IMPACT: **RESOLVED TO BOUNDED W02 PREREQUISITE**.
PO decision: **NOT REQUIRED**.
