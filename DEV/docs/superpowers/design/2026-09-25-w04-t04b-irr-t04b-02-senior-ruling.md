# W04.T04B IRR-T04B-02 Senior System-Impact ruling

Status: **ACCEPTED — BOUNDED W03 PREREQUISITE REQUIRED**

Date: 2026-09-25

Reviewed remote HEAD: `186da5a81a9bc760ebf7cc87ccbf629cf0f630aa`

Role: HDM Senior Architect / targeted System-Impact Design Reviewer

Scope: IRR-T04B-02 only. T04A, T07B and T07C remain accepted and are not reopened. T07D is independent and remains authorized.

## Ruling

**YES.** The accepted Step-5.8 semantics can be realized without changing product semantics or creating a second authority by adding one bounded, LIVE/W03-owned composable campaign-absorption/final-routing preparation boundary before T04B resumes.

This is not a Product-Owner decision. Step-5.8 already fixes the required semantics and atomicity:

```text
required LIVE freeze
-> absorption/final routing
-> PLAYER/access + Collaboration transition
-> one same-campaign W02 transaction
```

The missing piece is an implementation-boundary contract between the already accepted W03 LIVE owner and the existing W02 campaign publication owner. Collaboration must consume that contract; it must not synthesize it.

The prerequisite is named **W04.T04B-P1 — W03 composable absorption/final-routing producer**. It is a Wave-04 prerequisite with W03 semantic ownership; it does not reopen Wave-03 closure or any accepted W04 task.

T04B **does not resume yet**. It may resume immediately after T04B-P1 is implemented, independently reviewed PASS, published/read back, and the checkpoint below is present. No additional PO or Senior gate is required unless implementation hits a new System-Impact trigger described here.

## Bounded Source Manifest

| Source | Authority / use in this ruling | Qualifier |
|---|---|---|
| `AGENTS.md` | repository transport, checkpoint, review and Version Impact rules | current branch owner |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | GitHub Connector publication/read-back discipline | runtime overlay |
| `DEV/DESIGN_PROCESS.md` | decision rights and bounded/deep-design rules | canonical process |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | HDM owner/authority and architecture review gates | canonical HDM process |
| `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` | System-Impact escalation/resolution and resume law | canonical execution process |
| `DEV/CURRENT_PROGRESS.md` | global current cursor | current authority |
| Wave-04 stable plan + execution status | T04B owner, dependencies and current stop | current task owner |
| `2026-09-25-w04-t04b-t07c-independent-review.md` | IRR-T04B-02 evidence | accepted review evidence |
| Step-5.8 canonical spec | LIVE lifecycle, revocation, one-campaign-transaction law | semantic owner |
| Step-5.6 canonical spec | W02 one-tree/one-commit publication, conflict/retry/recovery | durability/publication owner |
| Wave-03 stable plan + execution status | accepted W03 routing/packing/absorption and T06 same-closure handoff | producer history/owner |
| `GAME/TOOLS/live_state.py` | W03 LIVE absorption/currentness owner | production source |
| `GAME/TOOLS/access_control.py` | multi-LIVE close/forward proof | read-only producer |
| `GAME/TOOLS/collaboration.py` | T04B consumer and current incomplete join | consumer under review |
| `GAME/TOOLS/publication.py` + `durability.py` | W02 frozen publication and recovery | existing owner, no semantic change |
| `GAME/TOOLS/runtime_host.py` | existing bound W02 publication service | no API broadening required by ruling |
| `GAME/TOOLS/native_storage.py` | deterministic native-owner path derivation | read-only dependency |
| `STATE/RUNTIME/LIVE_ROUTING.yaml` + live-routing schema | existing persisted W03 campaign route | schema v4 unchanged |
| live-native-state-pack + live-absorption-attempt schemas | current W03 frozen inputs | schemas v2/v1 unchanged |
| `test_rd09_access_live.py` + `test_rd12_collaboration.py` | producer and integration/recovery witnesses | required TDD surfaces |
| `DEV/RELEASE/VERSIONING.md` | module/schema/generation bump rules | Version Impact owner |

No release package, gameplay bootstrap, Wave-05 implementation or closed T04A/T07B/T07C work was inspected or reopened.

## Dependency / consumer result

The accepted dependency direction remains:

```text
Step-5.8 semantic law
  -> W03 live_state
       FrozenCampaignAbsorption
       -> NEW FrozenCampaignAbsorptionDelta
  -> T04B Collaboration consumer
       + W03 access/PLAYER transition
       + Collaboration obligation/route cleanup
  -> existing RuntimeHost CampaignPublicationService
  -> W02 FrozenCampaignPublicationAttempt
  -> one tree + one commit + one non-force ref transition
  -> W03 owner-issued composed absorption evidence
  -> T04B after-authority recovery/result
```

`native_storage` remains a deterministic routing utility, not an authority. There is no reverse dependency from LIVE into Collaboration and no second campaign-currentness owner.

## Exact producer owner and interface

Semantic owner: **W03 LIVE absorption / final-routing owner**.

Python owner: **`GAME/TOOLS/live_state.py`**.

The new preparation type is:

```python
@dataclass(frozen=True, slots=True, weakref_slot=True)
class FrozenCampaignAbsorptionDelta:
    campaign_id: str
    expected_campaign_revision: str
    proposed_campaign_revision: str
    selected_route: LiveRouting
    final_route: LiveRouting
    source_attempts: tuple[FrozenCampaignAbsorption, ...]
    path_operations: Mapping[str, object | None]
    operation_digests: Mapping[str, str]
    delta_digest: str
```

The issuing interface is:

```python
def freeze_campaign_absorption_delta(
    sources: Sequence[LiveEnvelope],
    *,
    route: LiveRouting,
    packed_states: Mapping[LiveSourceKey, LiveNativeStatePack],
    campaign_state: Mapping[str, object],
    expected_campaign_revision: str,
    proposed_campaign_revision: str,
) -> FrozenCampaignAbsorptionDelta:
    ...
```

The returned object is **ephemeral owner-issued preparation evidence**, not a persisted record. The LIVE owner must mark/recognize its own issued instance in the same nominal manner already used for accepted absorption evidence; direct caller construction must not become authority.

### What it contains

It contains only the complete W03-owned campaign-domain after-image required to absorb the exact final closed source set:

- exact campaign/predecessor/proposed-revision binding;
- the exact complete selected final-source route;
- one rederived `FrozenCampaignAbsorption` witness per source;
- one final route with exactly the absorbed source set removed and every unaffected selected source preserved;
- exact W03/native campaign `path_operations`, including `STATE/RUNTIME/LIVE_ROUTING.yaml = final_route.as_mapping()`;
- immutable operation digests plus a bundle digest for deterministic retry/inclusion checks.

The producer must derive every native path from typed owner identity using existing deterministic native routing. It must prove that every non-empty absorption contribution that is required by the accepted W03 packing/handoff laws is represented by an existing admitted owner path or existing W03 handoff projection. If any provenance/privacy/chronology/unresolved-work/native-owner contribution cannot be represented losslessly on an existing admitted campaign owner surface, preparation fails closed.

That last rule is deliberate: T04B must not make a false Step-5.8 claim by silently dropping an abstract `candidate_state` component. If implementation discovers that a new persistent owner/schema is actually required, that is a **new System-Impact event** and this ruling does not authorize inventing one.

### What it MUST NOT contain

It must not contain or create:

- a Collaboration-owned LIVE decision, route or lifecycle assertion;
- a caller boolean `absorbed` acknowledgement;
- a second campaign CAS, second ref transition or post-publication mutation;
- a LIVE source write, reopen, replay, mechanics execution or source CAS;
- PLAYER/access policy decisions or Collaboration obligation writes;
- a generic campaign-currentness oracle;
- a new persistent absorption aggregate, generic snapshot or surrogate authority;
- a `MANIFEST.yaml.live_routing` substitute;
- successor-opening/gameplay work or fictional chronology.

## Derivation from FrozenCampaignAbsorption

For every source in the exact affected final-source set, W03 reselects the source from `selected_route`, verifies CLOSED/CLOSED_UNABSORBED and exact source revision, verifies its `LiveNativeStatePack`, and internally rederives the per-source `FrozenCampaignAbsorption` from the same exact predecessor campaign body.

For a multi-LIVE transition, these per-source attempts are **parallel semantic witnesses over one predecessor**, not intermediate campaign commits. The bundle computes one set-wise final route by removing the complete absorbed source set at once. It does not pretend that N serial campaign states existed.

Native/path contributions are folded deterministically. Any conflicting contribution, duplicate owner identity with a non-identical after-image, incomplete pack, route mismatch, source-revision mismatch or non-routable required state fails closed before W02 publication.

The materialization order is deterministic engineering order only; it is not chronology.

## Predecessor and current LIVE binding

T04B may consume the delta only when all of the following bind exactly:

```text
delta.campaign_id
  == pinned campaign
  == access transition campaign

delta.expected_campaign_revision
  == T04B operation-basis pinned revision
  == W03 access transition expected revision

delta.selected_route source keys/revisions
  == exact current selected LIVE route
  == complete W03 final-close proof

delta source set
  == the affected LIVE set required by the access transition

every source
  == exact final CLOSED/CLOSED_UNABSORBED source proven by W03 close evidence
```

ACTIVE, partial/indeterminate close, missing selected route, stale/mismatched final source or incomplete source set still block before any campaign write.

## T04B composition into one W02 transaction

T04B continues to derive PLAYER/access and Collaboration after-images from their native owners.

It then performs a collision-safe union:

```text
W03 absorption/final-routing path_operations
+ PLAYER/access path_operations
+ Collaboration obligation/route-cleanup path_operations
= one joined path_operations mapping
```

A path collision is allowed only if both owner-derived after-images are exactly identical and the ownership contract admits the overlap; otherwise fail before W02. In the intended contract these domains are disjoint.

That one joined mapping is supplied **once** to the existing `CampaignPublicationService.publish_owner_delta(...)`. W02 freezes it into one `FrozenCampaignPublicationAttempt`, then performs one tree, one commit and one non-force ref transition. The existing routed PLAYER operation may remain the W02 serialization anchor; it does not become owner of the W03 paths.

No change to RepositoryPort, `RuntimeHost`, `CampaignPublicationService`, W02 transaction semantics or `access_control.py` is required by this ruling.

## Successful publication -> accepted W03 evidence

W03 adds a group-aware owner-issued result:

```python
@dataclass(frozen=True, slots=True, weakref_slot=True)
class ComposedCampaignAbsorptionPublication:
    status: LiveAbsorptionStatus
    accepted_campaign_revision: str | None
    delta: FrozenCampaignAbsorptionDelta
    _issuer: object = field(default=None, repr=False, compare=False)
```

There is no `absorbed: bool` acknowledgement.

The classifier is:

```python
def classify_composed_campaign_absorption(
    delta: FrozenCampaignAbsorptionDelta,
    publication: PublicationOutcome,
) -> ComposedCampaignAbsorptionPublication:
    ...
```

It accepts only an owner-issued frozen delta. `ACCEPTED` is issued only from the exact typed W02 outcome of the joined publication and is bound to that delta and the accepted campaign revision. REJECTED/CONFLICT/remaining INDETERMINATE never yield accepted absorption evidence.

`validate_accepted_absorption_evidence(...)` is extended owner-locally to accept this group evidence for a source only when that exact source key/revision is a member and `final_route` proves the whole group route-away. Existing single-source `LiveAbsorptionPublication` remains valid; it is not reinterpreted.

This is classification of the **same W02 campaign commit**, not a second campaign CAS.

## Recovery, conflict and indeterminate publication

W02 remains the sole publication/reconciliation owner.

- If W02 returns ACCEPTED directly, W03 classifies the same joined publication as accepted.
- If the ref acknowledgement is indeterminate but W02's existing exact closure/ancestry reconciliation returns ACCEPTED, W03 classifies that reconciled result; no second write occurs.
- If W02 returns CONFLICT/REJECTED or remains INDETERMINATE, W03 emits no accepted composed absorption evidence and T04B cannot report success.
- Recovery re-pins one exact campaign revision and rederives the same W03 delta from the exact final LIVE sources and the exact predecessor evidence. Exact matching final owner after-images plus final route may recover the accepted result without dispatching another ref update.
- If the predecessor is still current, retry may re-use/rederive the same deterministic delta and make the one W02 attempt.
- If campaign HEAD moved, Step-5.6 rules apply: only owner-validated disjoint re-freeze/rebase is allowed; overlapping/semantic drift fails closed. There is no generic merge.

No LIVE mechanics, source close or source CAS is replayed on retry.

## CLOSED_UNABSORBED versus absorbed/final

`CLOSED_UNABSORBED` remains durable LIVE truth after phase-A close:

- it is a final source revision;
- it has zero ordinary writers;
- it remains recovery input;
- it does **not** prove campaign absorption;
- a route containing the affected CLOSED_UNABSORBED source is not the successful T04B after-state.

Accepted composed absorption exists only after W02 accepts/reconciles the one joined campaign commit and W03 issues matching composed evidence. The campaign route then no longer selects every absorbed source and the complete W03/native after-image is current in the same commit.

The old LIVE source is not reopened or rewritten merely to store an `ABSORBED` bit. `ABSORBED` remains a W03 typed lifecycle/result view supported by accepted campaign evidence.

## Required TDD / recovery witnesses

### T04B-P1 producer — `DEV/TESTS/test_rd09_access_live.py`

Required RED/GREEN evidence:

1. single-source and multi-source CLOSED/CLOSED_UNABSORBED preparation produces deterministic identical delta/digest on retry;
2. `STATE/RUNTIME/LIVE_ROUTING.yaml` is present and removes exactly the complete absorbed set while preserving unaffected route members;
3. every required packed native/provenance/privacy/chronology/unresolved-work contribution is materialized losslessly or preparation fails closed;
4. ACTIVE, stale source, wrong selected route, incomplete/mismatched pack, duplicate/conflicting owner after-image and incomplete source set produce no delta;
5. no MANIFEST LIVE surrogate, PLAYER/access/Collaboration operation or LIVE source path appears;
6. ACCEPTED W02 outcome issues owner-authenticated group evidence; CONFLICT/REJECTED/INDETERMINATE does not;
7. group evidence validates each exact source member and exact final route; forged/directly constructed evidence fails;
8. CLOSED_UNABSORBED by itself never validates as accepted absorption.

### T04B integration — `DEV/TESTS/test_rd12_collaboration.py`

Retain the existing ACTIVE/partial/indeterminate/stale/missing-route zero-write tests and add:

1. positive LIVE-sensitive T04B produces one `create_tree` / one `update_ref` whose operation set contains W03 final-routing/native after-images plus PLAYER/access plus Collaboration effects;
2. no second campaign publication/CAS follows W02 acceptance;
3. recovery from merely CLOSED_UNABSORBED route is rejected as incomplete;
4. exact final route + W03 accepted composed evidence + exact access/Collaboration after-image recovers idempotently without another ref update;
5. indeterminate ref acknowledgement that W02 reconciles as accepted returns the same closure without LIVE replay;
6. conflict/retry uses the same exact final-source evidence and never recloses/replays LIVE mechanics;
7. path collision or tampered/non-owner-issued W03 delta fails before W02 dispatch;
8. the no-LIVE T04B path remains unchanged.

## Allowed write surfaces

### T04B-P1 prerequisite

Production:
- `GAME/TOOLS/live_state.py` only.

Tests / control:
- `DEV/TESTS/test_rd09_access_live.py`;
- Wave-04 plan/status/current-progress records;
- normal version bookkeeping required by the Version Impact Gate.

Read-only dependencies may include `native_storage.py`, W02 publication types, accepted temporal/operational handoff owners and W03/access close evidence.

Not authorized by this ruling: production edits to `collaboration.py`, `access_control.py`, `runtime_host.py`, `publication.py`, `durability.py`, RepositoryPort, existing persisted schemas/templates, shared Wave-05 surfaces, CORE, catalog or identifier-policy owners.

If producer completeness cannot be achieved on those existing admitted owner surfaces, stop and raise a new System-Impact event rather than broadening the write set.

### T04B after prerequisite PASS

T04B returns to its existing lane:
- `GAME/TOOLS/collaboration.py`;
- `DEV/TESTS/test_rd12_collaboration.py`;
- mechanically required collaboration version/control bookkeeping.

It consumes the accepted W03 delta; it does not implement W03 semantics.

## Version Impact

This ruling/control-only publication: **VERSION_IMPACT: NONE**.

Expected prerequisite implementation impact, subject to fresh worker verification:

```text
GAME/TOOLS/live_state.py framework_module_version:
  1.0.20 -> 1.0.21
```

No LIVE-routing schema bump is expected: persisted route shape remains v4. No live-native-state-pack v2 or live-absorption-attempt v1 shape change is required. No campaign-contract generation, storage-format generation, engine release, catalog generation or identifier-policy generation bump is implied.

The later T04B consumer repair is a material Collaboration runtime change and must increment the then-current Collaboration module revision exactly once. The current candidate baseline is 1.0.18, so 1.0.19 is the expected transition **only if no intervening accepted Collaboration edit changes that baseline**.

Any need for a new persisted absorption record/schema or migration is outside this ruling and reopens the System-Impact gate.

## Resume / control state

Accepted control sequence:

```text
IRR-T04B-02 Senior ruling: ACCEPTED
-> W04.T04B-P1 W03 producer implementation
-> focused + integration verification
-> independent review PASS / remote read-back
-> T04B resumes immediately
-> T04B repair verification + independent re-review
-> W04_AUTHORITY_COLLABORATION_RECONCILED only after T04B PASS
-> T05C may then use the existing dependency gate
```

T07D remains independent and may continue in parallel.

SYSTEM_IMPACT disposition: **RESOLVED TO BOUNDED PREREQUISITE; NO PRODUCT-SEMANTIC CHANGE**.

PO decision: **NOT REQUIRED**.
