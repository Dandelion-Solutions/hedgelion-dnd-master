# W05.T05 Initial Campaign Publication Boundary — Senior Architecture Ruling

Status: **ACCEPTED SENIOR / BOUNDED PREREQUISITE AUTHORIZED**

Date: **2026-10-01**

Reviewed public basis:
`16e647d8775d8218e04c765521c990ce090fe138`

Blocked slice:
`W05.T05 — blank scaffold / initial campaign publication`

Prerequisite:
`W05.T05-P1 — initial campaign publication capability`

Output:
`W05_INITIAL_CAMPAIGN_PUBLICATION_READY`

## 1. Disposition

```text
SYSTEM_IMPACT: RESOLVED
CLASSIFICATION: MISSING MACHINE-REALIZATION SEAM
PRODUCT_OWNER_DECISION_REQUIRED: NO
W02 SEMANTICS: PRESERVED / NOT REOPENED
W04 RUNTIMEHOST SEMANTICS: PRESERVED / NOT REOPENED
W05_BOUNDED_CAMPAIGN_DISCOVERY_READY: PRESERVED / ACCEPTED
W05.T05-P1: AUTHORIZED
W05.T05 scaffold completion: HELD UNTIL P1 PASS / READ-BACK
W05.T06: NOT AUTHORIZED
```

The worker correctly stopped. There is no current callable that can safely
publish a campaign ref that does not yet exist.

The missing seam is physical/machine realization. Product and persistence
semantics are already accepted.

## 2. Existing accepted semantics

Canonical Step 5.6 separates ordinary existing-campaign publication from
initial scaffold creation:

- ordinary publication is based on an accepted campaign HEAD `H` and
  `T(H)`;
- initial scaffold creation is a separately owned **from-scratch exception**;
- repository mutation remains deterministic Python/RepositoryPort-owned;
- prepared objects have no gameplay authority;
- authority changes only through a non-force ref transition;
- ambiguous outcomes require bounded exact-authority reconciliation.

Current product contracts additionally require:

```text
generated scaffold
  -> one tree built FROM SCRATCH
  -> one initialization commit
       parent = selected storage default-branch HEAD
  -> one create-if-absent campaign ref publication
  -> only then player-facing campaign setup
```

The first campaign-specific initialization commit is also the accepted creator
provenance anchor.

These semantics are not reopened.

## 3. Why the current W02/W04 callable cannot be reused directly

`CampaignPublicationService.publish_owner_delta(...)` is intentionally
campaign-bound:

- it lives under a `RuntimeHost(selected_campaign_id, ...)`;
- it begins from a pinned existing campaign;
- it reads existing MANIFEST/CAMPAIGN_CARD authority;
- it builds a base-tree-derived delta;
- its transport exposes `update_ref(..., force=False)`, not ref creation.

Using that service before the campaign ref exists would invert the accepted
composition order.

Calling `update_ref` on an absent ref is also forbidden. Existing-ref update
and initial create-if-absent are distinct authority transitions.

## 4. Selected machine-realization seam

Use a **bootstrap-specific capability view over the same authenticated
RepositoryPort/deployment adapter**.

This is not a second repository owner and not an alternate transport.

The capability is consumed before a campaign-bound RuntimeHost exists and is
owned by the W05 bootstrap path. The eventual deployment adapter may implement
both the existing campaign publication view and this bootstrap view, but the
bootstrap view has its own narrow pre-campaign operation set.

Do not add initial-ref creation to `CampaignPublicationService` or require a
synthetic selected campaign merely to reach transport.

Do not add write methods to the read-side
`policy_basis.RepositoryPort` protocol solely for this task.

## 5. Required bootstrap publication capability

The exact local protocol spelling is implementation-selectable, but it must
provide no more than the following semantic capabilities:

```text
repository_identity()

resolve_authenticated_storage_principal(
    storage_repository,
    pinned_storage_head
)

read_ref_state(target_campaign_ref)
    -> ABSENT | PRESENT(exact_head)

create_tree_from_scratch(exact_generated_files)
    -> exact_tree_sha

create_single_parent_commit(
    parent_sha = pinned_storage_head,
    tree_sha,
    target_ref
)
    -> exact_commit_sha

create_ref_if_absent(
    target_campaign_ref,
    exact_commit_sha
)
    -> W02-compatible accepted/rejected/conflict/indeterminate outcome

read_exact_commit / exact ref evidence sufficient for bounded reconciliation
```

The same physical adapter/repository identity must back discovery/storage reads
and initial publication. A T05 caller cannot nominate an unrelated repository
writer.

The authenticated principal resolved at the publication boundary must match
the already frozen bootstrap creator identity. Technical write permission alone
does not authorize campaign creation.

## 6. Initial publication algorithm

T05-P1 must realize the following bounded algorithm.

### Freeze

Before remote mutation freeze:

- selected storage repository identity;
- pinned storage default-branch HEAD;
- target technical campaign ref;
- frozen creator identity;
- campaign ID / branch / creation time;
- exact generated scaffold file map;
- exact content/tree fingerprint;
- exact engine/package/ruleset identity needed by the generated scaffold.

### Existing target preflight

Read the exact target campaign ref.

If it is already present, perform bounded adoption/reconciliation only.
Never update, overwrite, force or rebuild on top of that campaign ref.

An existing ref may be adopted as the result of the same initialization only
after exact proof that its initialization commit/tree/parent and generated
campaign identity satisfy the frozen attempt. Otherwise return conflict.

### Prepare

If the target ref is absent:

1. create exactly one tree **from scratch** from the complete generator output;
2. prove no storage-root marker/README leakage;
3. create exactly one initialization commit with:
   `parent == pinned storage default-branch HEAD`;
4. the commit is prepared/non-authoritative until ref publication succeeds.

### Authority transition

Publish using exactly one atomic semantic operation:

`create_ref_if_absent(target_campaign_ref, initialization_commit)`.

Never:

- call ordinary `update_ref` for absent-ref creation;
- first expose a campaign ref at the storage default HEAD and then mutate it;
- force update;
- create per-file commits;
- fall back to Contents API/per-file creation;
- create a second campaign ref-writing authority.

### Outcome / ambiguity

Reuse the W02 outcome vocabulary and fail-closed law.

After an indeterminate create-if-absent result, perform bounded exact target-ref
and initialization-commit/tree reconciliation:

- target points to the intended initialization commit and exact frozen tree:
  confirmed accepted;
- target is absent under authoritative post-attempt ref evidence:
  confirmed not published / retry may be planned from the same frozen semantic
  identity;
- target points elsewhere:
  conflict;
- evidence cannot establish one of the above:
  remain indeterminate.

A retry never overwrites an existing target ref and never invents a fresh
campaign identity merely to hide an unresolved prior attempt.

## 7. T05-P1 implementation envelope

Direct production/test writes:

- `GAME/TOOLS/bootstrap.py`;
- `DEV/TESTS/test_rd14_bootstrap.py`;
- task-local execution/progress evidence;
- a new bounded DEV-only schema/fixture only if required to machine-check the
  initial-publication outcome, with no new semantic owner.

Inspect/read-only:

- `GAME/TOOLS/runtime_host.py`;
- `GAME/TOOLS/publication.py`;
- `GAME/TOOLS/policy_basis.py`;
- W02 publication/durability/recovery tests and owners;
- T04/T07/T08 physical writers.

Do not modify RuntimeHost/CampaignPublicationService in P1 unless a concrete
test-first contradiction proves that the bootstrap-specific capability cannot
be expressed without doing so. Such a contradiction returns to System Impact.

## 8. Mandatory P1 RED/GREEN evidence

Tests must cover at least:

1. target ref absent -> from-scratch tree -> one parented initialization commit
   -> create-if-absent accepted;
2. storage default HEAD is the initialization commit's only parent;
3. generated tree contains exactly the scaffold and no storage marker/README;
4. target ref already exists before mutation -> no write;
5. existing ref matching the exact frozen initialization may be adopted;
6. existing ref with different commit/tree/campaign identity -> conflict;
7. create-if-absent race loses -> no overwrite / no force;
8. indeterminate result + target points intended commit -> accepted;
9. indeterminate result + target absent -> not falsely acknowledged;
10. indeterminate result + target points elsewhere -> conflict;
11. unavailable create-if-absent capability -> typed fail-closed result;
12. ordinary `update_ref` cannot substitute for ref creation;
13. authenticated publication principal/repository identity mismatch -> reject;
14. retry preserves frozen campaign identity and does not duplicate campaign
    creation.

Use W02 publication outcome semantics; do not invent a second generic retry or
transaction framework.

## 9. Version / migration impact

Expected architecture-level classification:

```text
VERSION_IMPACT: likely bootstrap module revision only if implementation changes
                 its material callable contract
persistent schema generation: NONE
campaign contract generation: NONE
storage generation: NONE
catalog generation: NONE
migration: NONE
dual-read: NONE
```

The implementation worker must run the fresh Version Impact Gate against the
actual code delta.

## 10. Resuming W05.T05

After `W05_INITIAL_CAMPAIGN_PUBLICATION_READY` receives independent PASS and
remote read-back, resume the held scaffold slice.

The resumed T05 must still close:

- `CURRENT.yaml` v2 -> v3;
- removal of `world_time.frontier`;
- generator/scaffold validation synchronization;
- blank owner-native root completeness;
- initial scaffold publication through the accepted P1 capability.

Only then may T05 claim:

`W05_BLANK_SCAFFOLD_READY`.

The already accepted
`W05_BOUNDED_CAMPAIGN_DISCOVERY_READY` is not reopened.

T07 retains `campaign_manifest` v5 and membership retirement. T06 remains
held until T05 closes under its normal dependency gate.
