# Implementation Planning — WP-16 Executable Closure Addendum

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **AUTHOR GRAPH FINDING 7 — SIGNIFICANT**

## Finding

The WP-16 lossless proof ledger currently marks duties 12, 13 and 15 as `CURRENT_PLANNED`, but base RD-09 does not yet define the mechanisms those witnesses claim:

12. safe additive PLAYER activation/reactivation without unrelated LIVE rollover;
13. closed per-kind LIVE-born identity/admission;
15. multi-LIVE freeze/forward transition without distributed rollback.

This is a proof-without-mechanism defect. The canonical WP-16 / Step-5.8 laws already settle the semantics, so no architecture reopen or human product decision is required. This addendum makes the accepted laws worker-executable.

---

# 1. Safe additive activation/reactivation decision

Add one explicit RD-09 decision function, conceptually:

```text
classify_additive_authorization_change(
    campaign_change,
    selected_live_sources,
    current_claims,
    current_control_basis,
) -> NO_LIVE_ROLLOVER | LIVE_TRANSITION_REQUIRED
```

`NO_LIVE_ROLLOVER` is legal **only if all** are proven against current owner state:

1. no selected LIVE epoch's immutable claim set changes;
2. the authorization semantics of every already-authorized writer for every claimed owner remain unchanged;
3. no controlled-PC relation is transferred into or out of an affected selected LIVE source;
4. no existing LIVE source is being revoked/invalidated by the change;
5. the new/reactivated PLAYER gains no mutable LIVE authority merely from activation — current campaign membership, control, routing, collaboration and other applicable obligations must be reacquired;
6. the campaign-domain PLAYER/policy change can publish coherently without changing selected LIVE routing/currentness.

If any predicate is false or unprovable, result is `LIVE_TRANSITION_REQUIRED`: close/freeze affected source(s) by exact-source CAS, publish the campaign authority transition, then derive/adopt any successor from the new current basis. Predecessor epochs never reopen.

Required tests under RD-09 `LiveLifecycleTests` or a dedicated `LiveAdditiveAuthorizationTests` group:

- new active PLAYER with no control/claim impact leaves unrelated ACTIVE LIVE unchanged;
- self-reactivation with no control/claim impact leaves unrelated ACTIVE LIVE unchanged;
- controller transfer into/out of claimed PC forces transition;
- revocation of an existing writer forces close first;
- change requiring claim expansion cannot mutate Q(E) in place;
- new participant cannot write LIVE until current obligations are reacquired;
- missing evidence chooses transition/fail-closed, never optimistic no-rollover.

---

# 2. Exhaustive per-kind LIVE-born identity / creation admission

## 2.1 Identity policy machine shape

The current `identifier-policies.schema.json` has no representation for WP-16 `source_native_live`. Extend the unreleased v1 identifier-policy machine contract from schema version 2 to schema version 3 while keeping `catalog_generation = 2`.

Every admitted native world/runtime record policy must carry an explicit `live_birth` disposition:

```text
LiveBirthDisposition :=
    SOURCE_NATIVE_LIVE
  | OWNER_EQUIVALENT
  | FORBIDDEN
```

Conceptually:

```json
"live_birth": {
  "disposition": "source_native_live | owner_equivalent | forbidden"
}
```

For `SOURCE_NATIVE_LIVE`, the accepted identity basis is:

```text
stable live epoch/source identity
+ native family identity domain
+ accepted source-local creation coordinate
```

The exact printable encoding is an implementation detail, but the coordinate is established in the same accepted exact-source CAS transition as creation. Rejected prospective coordinates are noncanonical. Accepted identity never rekeys on retry, close, recovery or campaign absorption.

`OWNER_EQUIVALENT` means the kind's existing semantic derived/composite identity is already collision-free when its parent/components are stable; no second surrogate LIVE ID is created.

`FORBIDDEN` means `EPOCH_LOCAL_CREATION(family)` is invalid for that family. This does not by itself redefine whether an already-existing exact owner can ever be read/claimed; separate WP-16 claim exclusions/currentness laws still apply.

The campaign allocator accepts only campaign-scoped sequential creation and rejects every accepted LIVE-born creation path.

## 2.2 Closed v1 family table

After applying the already-mandatory `world.thread` and `world.player` catalog repairs and the MechanicalEvent identity repair, the v1 table is exhaustive as follows.

### World families

| Kind | LIVE-born disposition | Notes |
|---|---|---|
| `world.actor` | `SOURCE_NATIVE_LIVE` | lifecycle may begin inside an admitted LIVE mutation horizon |
| `world.actor_group` | `SOURCE_NATIVE_LIVE` | same; create-time owner/containment validation still required |
| `world.asset` | `SOURCE_NATIVE_LIVE` | supports accepted LIVE-born object/equipment consequences |
| `world.location` | `SOURCE_NATIVE_LIVE` | only when owner/partition containment validates |
| `world.connection` | `SOURCE_NATIVE_LIVE` | only when owner/partition containment validates |
| `world.zone` | `SOURCE_NATIVE_LIVE` | bounded region owner |
| `world.organization` | `SOURCE_NATIVE_LIVE` | only when selected epoch explicitly admits creation and containment validates |
| `world.contract` | `SOURCE_NATIVE_LIVE` | same |
| `world.mission` | `SOURCE_NATIVE_LIVE` | same |
| `world.scene` | `SOURCE_NATIVE_LIVE` | same; no scene mega-owner implication |
| `world.encounter` | `SOURCE_NATIVE_LIVE` | same |
| `world.hazard` | `SOURCE_NATIVE_LIVE` | supports local hazard lifecycle start |
| `world.effect` | `SOURCE_NATIVE_LIVE` | supports atomic LIVE mechanical consequence |
| `world.lore_fact` | `SOURCE_NATIVE_LIVE` | only with native truth-owner evidence; not Story authority |
| `world.knowledge` | `OWNER_EQUIVALENT` | semantic composite `(knower_id,fact_id)` |
| `world.thread` | `SOURCE_NATIVE_LIVE` | only when final WP-15 thread scope is machine-contained by the selected mutation partition; otherwise creation claim rejects |
| `world.player` | `FORBIDDEN` | campaign-only access/control authority; WP-16 explicitly excludes from LIVE claims |

### Runtime families

| Kind | LIVE-born disposition | Notes |
|---|---|---|
| `runtime.session` | `FORBIDDEN` | coordination/session owner, not LIVE gameplay authority |
| `runtime.message` | `SOURCE_NATIVE_LIVE` | explicit R27-R013 / live-message debt |
| `runtime.interaction` | `SOURCE_NATIVE_LIVE` | independently addressable accepted invocation owner |
| `runtime.procedure` | `SOURCE_NATIVE_LIVE` | independently writable Procedure owner |
| `runtime.intent_plan` | `OWNER_EQUIVALENT` | derived from stable Interaction identity |
| `runtime.command` | `OWNER_EQUIVALENT` | derived from stable Interaction identity |
| `runtime.resolution` | `SOURCE_NATIVE_LIVE` | independently addressable Activity invocation owner |
| `runtime.continuation` | `OWNER_EQUIVALENT` | derived from stable Resolution identity |
| `runtime.mechanical_event` | `OWNER_EQUIVALENT` | exact composite `(segment_id,event_ordinal)` per Finding 10 |
| `runtime.semantic_event` | `SOURCE_NATIVE_LIVE` | native history event may first establish from accepted LIVE evidence |
| `runtime.resolution_trace` | `OWNER_EQUIVALENT` | derived from stable Resolution identity |
| `runtime.disclosure` | `OWNER_EQUIVALENT` | semantic composite `(player_id,fact_id)` |
| `runtime.collaboration_obligation` | `FORBIDDEN` | WP-17 campaign-domain collaboration lifecycle / PLAYER routing companion |
| `runtime.checkpoint` | `FORBIDDEN` | recovery descriptor/evidence, not LIVE-created gameplay owner |
| `runtime.id_allocator` | `FORBIDDEN` | campaign allocator authority |
| `runtime.maintenance_audit` | `FORBIDDEN` | maintenance evidence |
| `runtime.catalog_gap_report` | `FORBIDDEN` | maintenance/catalog-gap evidence |

The table grants **identity capability only together with explicit family creation admission**. Actual LIVE lifecycle start still requires an immutable selected `EPOCH_LOCAL_CREATION(family)` claim and all owner-specific validation, scope/containment, authorization/currentness and native durability rules. Generic serialization never grants creation.

Unknown native kinds, future kinds without explicit table entry and stale legacy kinds fail closed.

## 2.3 Claim-schema validation

RD-09 `live-claim.schema.json` / claim validation must reject:

- `EPOCH_LOCAL_CREATION` for `FORBIDDEN` or unknown family;
- family whose current identifier-policy `live_birth` entry is absent/incompatible;
- `SOURCE_NATIVE_LIVE` creation that attempts campaign allocator fallback;
- `OWNER_EQUIVALENT` creation that attempts a new surrogate ID;
- `world.player` creation/claim through LIVE;
- create-time owner/partition whose scope cannot satisfy applicable containment/currentness law.

Tests must prove accepted source-native IDs remain unchanged after retry/close/recovery/absorption and collide neither across epochs nor with campaign-sequential IDs under the final encoding rules.

---

# 3. Multi-LIVE forward-only transition

Add an explicit ephemeral operation model in RD-09. It is not a durable coordinator, transaction record, lock or new authority owner.

Conceptual interfaces:

```text
freeze_multi_live_forward_plan(
    current_campaign_basis,
    affected_live_routes,
    owning_transition_request,
) -> FrozenMultiLiveForwardPlan

advance_multi_live_freeze(
    plan,
    exact_source_outcomes,
) -> WAIT_FOR_CURRENT_SOURCES | READY_FOR_FORWARD_TRANSITION | INTEGRITY_FAILURE

publish_forward_transition(
    plan,
    exact_final_live_sources,
    current_campaign_basis,
) -> CampaignPublicationResult
```

Required behavior:

1. pin current campaign routing and the exact selected source revision for every affected LIVE epoch;
2. validate authorization/claim/currentness for the owning cross-scope transition;
3. close/freeze each affected LIVE source through its own exact-source CAS; technical attempt order may be deterministic for reproducibility but has **no fictional chronology meaning**;
4. a confirmed accepted close is final and remains real even if another source later rejects or is indeterminate;
5. a stale/rejected source is refreshed/revalidated; an indeterminate source is resolved by bounded exact-source/lineage verification;
6. until every required source has one confirmed exact final CLOSED revision, do **not** publish the dependent fictional/campaign forward transition;
7. already-closed sources remain `CLOSED_UNABSORBED`; never reopen or roll them back merely because another source is still active/uncertain;
8. after all exact final source revisions are proven, publish the owning campaign forward transition/absorption with those exact bases under RD-06;
9. only after the forward campaign transition may optional successor epoch(s) be selected from the new current basis;
10. if a previously accepted native gameplay edge exists in one source while another source later rejects, preserve the accepted edge and recompose/retry the dependent transition — never compensate by reroll/replay or fictional rollback.

Recovery requires no persistent global multi-LIVE coordinator. It re-derives outstanding work from current campaign routes plus each selected LIVE source lifecycle/currentness and resumes forward.

Required `MultiLiveForwardTransitionTests`:

- A closes, B stale rejects: A stays CLOSED_UNABSORBED; no campaign transition yet;
- A closes, B publication indeterminate: resolve B; never reopen A;
- both close: one campaign forward transition consumes exact final revisions;
- campaign publication conflicts after all close: both remain closed; refresh/retry campaign publication, no LIVE reopen;
- one source contains already accepted RNG/mechanics evidence: later source failure never rerolls it;
- freeze/CAS order never appears as chronology;
- no global LIVE ref scan, distributed rollback, 2PC, lease or leader introduced.

---

# 4. Shared identifier-policy integration checkpoint

`DEV/CATALOG/identifier-policies.json` and `DEV/SCHEMAS/identifier-policies.schema.json` are shared machine surfaces touched by multiple semantic RDs. They must have **one ordered integration checkpoint**, not concurrent independent edits.

The checkpoint consumes, in this order-independent semantic set:

- RD-08 / Finding 4 `world.thread` admission and campaign default identity;
- Finding 8 `world.player` admission + LIVE-forbidden disposition;
- RD-05 / Finding 10 `runtime.mechanical_event` composite identity;
- this Finding 7 exhaustive `live_birth` table;
- R27-R013 explicit `runtime.message` source-native requirement.

Machine cutover:

```text
identifier-policies.schema_version 2 -> 3
catalog_generation stays 2
```

Update all exact catalog/schema/inventory/conformance surfaces that validate identifier-policy shape. No compatibility shim or dual old/new policy is required solely for unreleased v1 clean-slate state.

`CampaignAllocatorTests` must enumerate the final policy table and prove allocator participation exactly for campaign-default sequential paths; LIVE-born accepted IDs, composite/derived IDs, singleton/control owners and FORBIDDEN LIVE families never fall back through allocator logic.

Execution-wave planning must serialize this shared-file checkpoint before RD-09 final identity proof and before package R018 closure.

---

# 5. RD-09 executable amendments

Base Task 5 is superseded where it says to modify unspecified "exact artifacts" without an exact per-kind table. Task 5 becomes the explicit machine/table realization above plus source-native ID generation/validation.

Base Task 7 is extended with the safe-additive predicate and multi-LIVE forward transition protocol above.

No new generic ACL service, identity service, LIVE coordinator or transaction manager is introduced.

---

# 6. Proof-ledger amendments

WP-16 R080 rows 12, 13 and 15 are green-plan claims only after this overlay is in force:

- **12** -> safe-additive predicate + `LiveAdditiveAuthorizationTests`/equivalent exact cases;
- **13** -> identifier-policy schema v3 + exhaustive per-kind `live_birth` table + claim admission + `SourceNativeIdentityTests`;
- **15** -> explicit ephemeral multi-LIVE forward protocol + `MultiLiveForwardTransitionTests` + RD-06 campaign publication join.

Row 14 additionally composes with Finding 10: owner-equivalent derived/composite identities, including MechanicalEvent, never rekey and never gain a source-native surrogate merely because they are physically established in LIVE.

A proof witness cannot count as current planned closure if its corresponding mechanism/table is removed or becomes conditional again.

---

# 7. Version / migration disposition

This is unreleased v1 machine realization. `GAME/**` legacy v0.8 preservation is not a constraint. Do not add compatibility aliases, dual identifier formats or migration shims solely to preserve the current provisional policy schema. Apply normal execution-time Version Impact Gate to any additional change discovered after fresh currentness.

---

# 8. Disposition

```text
AUTHOR_GRAPH_FINDING_7: REPAIRED_IN_PLANNING
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```
