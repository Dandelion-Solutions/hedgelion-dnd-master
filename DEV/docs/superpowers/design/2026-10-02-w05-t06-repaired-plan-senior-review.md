# W05.T06 Repaired Implementation Plan — Senior Review

Status: **NEEDS REPAIR — PRODUCTION GO NOT GRANTED**
Date: 2026-10-02
Reviewed public HEAD: `d825127cb868d0eaa87bda4f5f3852a5aa2575a4`
Plan repair checkpoint: `a61b40ff14fb53d24b715734c43449fea94fbeb9`

## Disposition

```text
SENIOR_PLAN_REVIEW: NEEDS_REPAIR
SIGNIFICANT_OPEN: 4
PRODUCT_OWNER_DECISION_REQUIRED: NO
T06_A1_ARCHITECTURE: ACCEPTED / NOT REOPENED
T06_P0_P1_P2_P3_PRODUCTION: HELD
T06_S1_S2: PRESERVED
STORY_MASTER_ADAPTER: DORMANT
T07_T08_W06: NOT STARTED
W05_PRODUCT_PATHS_READY: HELD
NEXT_AUTHORIZED_UNIT: bounded stable-plan repair of SP06-01..SP06-04
```

The dependency decomposition and most envelopes are sound. Four unresolved
producer/coherence/eligibility planning gaps prevent production GO. These are
inside the accepted T06-A1 design, not a new Product Owner decision or another
architecture eight-step loop. Finish the bounded planning repair and return for
Senior plan review.

## Evidence and scope

Fresh Connector ref read confirms the reviewed HEAD. The exact
1858b838e9a0390ec7cdccad5b6b5d519aebae7d..reviewed-HEAD comparison contains two
commits and four DEV Markdown paths only: W05 stable plan, plan index,
execution cursor and CURRENT_PROGRESS. No GAME implementation changed.

The stable plan's P0/P1/P2/P3/product steps, carrier descriptions, envelopes and
all eighteen law mappings were reviewed against the accepted T06-A1 spec and
Senior Review Stop 2. Current native HOT/RuntimeHost/catalog/mechanics
implementation and PO-001 / PO-012 owners were inspected for the findings below.

Worker-recorded evidence at a61b40ff: focused 30 passed; clean exact-source DEV
1524 passed and maintenance audit PASS. These remain worker-recorded local
evidence; this Connector reviewer did not rerun local tests. The in-place seven
contamination failures remain non-acceptance diagnostics, not a product defect
or permission to remove workspace artifacts.

Independent hosted observation: Validate engine source run 37034983388 at
d825127cb868d0eaa87bda4f5f3852a5aa2575a4 is completed / success.
CI validates the source tree; it does not settle the semantic plan findings.

## SP06-01 — SIGNIFICANT — Commentator formula imported into Master acceptance

Location: stable W05 plan, P3 Steps and checks, step 2.

The positive cases specify PUBLIC + exact PLAYER disclosure + at most one
selected controlled PC's epistemic.known. This is PO-012's baseline Commentator
formula. PO-012 explicitly refines PO-009 only for Commentator reader perspective;
PO-001 ordinary Master instead composes the existing native information and
role-context owners. The P3 envelope says PO-012 is separate, but its executable
test step prescribes the formula for Master.

Impact: implementation could treat believed/suspected/rejected information as
ineligible for even correctly qualified Master answers, or substitute the
Commentator control projection for native Master eligibility.

Required repair:
- replace P3's formula with source/aspect-specific native current
  PLAYER/control/knowledge/disclosure/access eligibility under PO-001,
  Step-4 and R2.3;
- preserve epistemic stance in the visible qualified projection; a belief or
  suspicion must not become established objective fact;
- add separate tests for an eligible qualified belief/suspicion and denial of
  the hidden objective fact, grounded in the actual native owner contract;
- retain selected-PC control and no eligibility widening/automatic union, but
  do not invent a universal Master formula or transfer Commentator metadata;
- leave PO-012 positive/negative cases on their separately named Commentator
  regression path.

This does not newly authorize disclosure. Exact native aspect eligibility
continues to decide whether any field or qualified statement may be served.

## SP06-02 — SIGNIFICANT — HOT acceptance evidence has no planned producer join

Location: P0 internal carrier, steps 1–4 and allowed-interface Envelope.

P0 correctly rejects arbitrary OwnerDocument and requires accepted native
establishment evidence. The actual NativeHotStore row contains payload,
source_basis string and generation; stage_owner_document/atomic_owner_mutation
validate identity but do not themselves supply the Host-issued acceptance proof
demanded by the new read contract. RuntimeHost currently has no HOT binding.
The plan names the read result but not the producer/admission path establishing
that proof or its source compatibility/revalidation.

Impact: a worker may either bless raw rows despite the invariant or make every
HOT read unavailable. Neither discharges accepted-unpublished current reads.

Required repair:
- identify the actual accepted native establishment/adoption producer(s) used
  by these consumers and exact input evidence;
- name the infrastructure-only admission/join interface and carrier, with its
  validation, campaign/owner/source binding and lifecycle;
- include required existing producer modifications in the P0 file set and
  Envelope rather than leaving them implicitly inspect-only;
- distinguish accepted unpublished local state, clean source-derived cache,
  selected-LIVE adoption and pre-CAS prospective state;
- prove successful current Context read immediately after a real accepted
  native local change without SAVE, rejection of the equivalent raw forged
  row, and correct revalidation after relevant external movement/cold recovery.

A new semantic acceptance authority is forbidden. The adapter must consume
existing native acceptance, not mint it from a Host token or source_basis text.
If a required producer cannot be identified under accepted owners, report the
specific gap through System-Impact rather than inventing one.

## SP06-03 — SIGNIFICANT — dynamically expanded read closure lacks coherence protocol

Location: P0 read_owner_snapshot(owner_keys), CurrentOwnerView.read_owner and P1/P3 joins.

The snapshot copies only requested keys then closes SQLite. READY_PC/Context
closure and retrospective eligibility can expose additional required owners
after reading the first owner. The plan does not define who supplies the initial
key set, how new keys join, or how the previously detached rows and absence
observations are validated against the expanded observation.

Impact: separately correct snapshots can yield a mixed Actor/Asset/Effect/
PLAYER/knowledge packet that never coexisted. One opaque operation token alone
does not prevent it.

Required repair:
- specify the bounded operation-scoped closure/observation protocol;
- when keys expand, either reacquire the bounded union from one closed snapshot
  and invalidate/recompute affected derivations, or provide an equivalent
  proof that all retained observations remain compatible;
- include row absence, helper/index inputs and current source/routing basis
  where material; define a finite retry/revalidation/failure termination;
- keep all remote I/O outside SQLite transactions;
- add a test where a newly discovered dependency and an earlier owner change
  between snapshots; prohibit mixed assessment and require bounded failure or
  compatible revalidated success.

No campaign-global semantic generation, frontier or new chronology is selected.
Physical token/factoring may be chosen under the existing operation-coherence law.

## SP06-04 — SIGNIFICANT — P1 input carrier and catalog binding have no executable issuer path

Location: P1 BoundMechanicalDependencySet and readiness service interfaces/steps.

assess_local_sufficiency requires a RuntimeHost-issued dependency set, but no
task names its issuing method, accepted input, derivation owner or consumer
handoff. assess_ready_pc has no catalog argument; the plan says one admitted
BoundCatalogContext is used, but does not name how that context is bound to the
Host/readiness operation or refreshed/revalidated. Existing bind_catalog_context
is an admitted producer, not an implicit RuntimeHost catalog service.

Impact: first consumer has no supported call path, or product code constructs
the supposedly owner-issued dependency list / silently selects ambient rules.

Required repair:
- specify the producer/signature and finite native derivation for the exact
  proposed mechanic dependency set, and its consumer call sequence;
- use already admitted catalog/native mechanic evidence; do not execute,
  reroll or mutate mechanics merely to ask whether they are sufficient;
- specify infrastructure/operation binding of BoundCatalogContext, its exact
  catalog/ruleset identity and revalidation policy;
- ensure Actor/current-owner basis, catalog context and dependency carrier
  belong to the same compatible operation, or explicitly rebind/revalidate;
- add wrong-host, stale revision/catalog, forged dependency list and positive
  real producer-to-assessment tests;
- include necessary producer/consumer files and steps in the existing P1
  Envelope.

Do not replace the DEV conformance fixture with caller-authored runtime facts or
introduce a second rules engine. Names/factoring are implementation-plan details;
the accepted owners still control every derivation/admission rule.

## Preserved plan strengths

P0 -> P1 and P0 -> P2 -> P3 -> product joins are explicit. P2 names local event
establishment, durable publication and LIVE pack/absorption index companions.
Direct-known-ID bypass and no index-absence proof are retained. P3 retains an
unforgeable same-operation route and field-level eligibility, with no Story
baseline dependency, private payload leak, new role/model phase or save edge.
The four findings refine executable proof, not this accepted dependency graph.

## Repair exit and Version Impact

Repair the existing stable W05 plan and index with the exact missing
producer/carrier/closure interfaces, steps, Envelope extensions and tests.
Update execution/global cursors coherently. Account SP06-01..SP06-04 item by
item, self-review against all eighteen laws, verify and publish/read back.
Then return for Senior plan review. No production RED/GREEN work is authorized.

VERSION_IMPACT: NONE for this review/status/routing checkpoint. No runtime module,
schema, catalog, serialized protocol, digest or generation changed. Actual
future implementation remains subject to namespace-specific classification.

UNPUBLISHED_REPOSITORY_WORK: NONE after this checkpoint publication/read-back.
