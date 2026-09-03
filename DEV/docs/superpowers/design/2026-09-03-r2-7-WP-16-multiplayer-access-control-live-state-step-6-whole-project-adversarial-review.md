# R2.7 WP-16 — Multiplayer / Access Control / Live State — Step 6 Whole-Project Adversarial Review

Status: **STEP 6 COMPLETE — BLOCKING/SIGNIFICANT FINDINGS REQUIRE STEP-7 REPAIR**

Date: 2026-09-03

Candidate under review:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-step-5-candidate-spec.md`

This review is an independent Step-6 reconstruction. It does not treat the Step-2 Source Manifest as a sufficient review set and does not reopen accepted architecture merely because current runtime/schema prose is stale.

---

## 1. Independent dependency reconstruction

The critic rebuilt the relevant dependency graph from `DEV/PROJECT_MAP.md` and current owners/consumers.

### 1.1 Supported host / principal / repository transport

Route checked:

```text
R2.6 host assurance
-> fixed repository-transport owner clarification
-> GAME/INSTALL/PROJECT_INSTRUCTIONS.txt
-> current supported Connector authenticated-profile capability
-> GAME/CORE/RUNTIME.md
-> GAME/CORE/PERSISTENCE.md
-> WP-13 publication realization
```

Current capability evidence again establishes a trustworthy current authenticated GitHub principal surface with a stable external user identifier exposed separately from mutable login/nickname metadata. No login substitution or alternate-transport fallback is required.

### 1.2 Campaign access / membership / control

Route checked:

```text
DEV/ARCHITECTURE/ACCESS_CONTROL.md
-> DEV/ARCHITECTURE/BRANCH_MODEL.md
-> GAME/SCHEMA/player.schema.yaml
-> GAME/CORE/MULTIPLAYER.md
-> DEV/TESTS/ACCESS_CONTROL_CASES.md
-> DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md
```

The graph confirms four separate authorities that must never collapse:

```text
trusted external principal
-> current PLAYER binding/membership
-> current controlled-PC relation
-> operation-specific authorization
```

Repository capability and successful Git transport remain infrastructure evidence only.

### 1.3 LIVE ownership / exact-source currentness / publication

Route checked:

```text
Step-5.8 canonical LIVE ownership
-> WP-11 physical routing/identity/indexing
-> WP-12 HOT/SQLite realization
-> WP-13 durability/publication realization
-> WP-14 recovery/session realization
-> GAME/CORE/LIVE_SCENE.md
-> GAME/SCHEMA/live_scene.schema.yaml
-> GAME/SCHEMA/scene.schema.yaml
-> DEV/TESTS/LIVE_SCENE_CASES.md
```

The accepted model is owner-typed currentness selected by campaign routing, exact-source CAS, terminal close and forward absorption. Current scene-centric LIVE prose/schema/tests remain implementation debt where they imply scene-wide authority, generic provisional IDs or one-user-action/one-write atomicity.

### 1.4 Native owner classes / identity

Route checked:

```text
DEV/ARCHITECTURE/CATALOG_CONTRACTS.md
-> DEV/ARCHITECTURE/ENTITY_STRUCTURES.md
-> DEV/CATALOG/identifier-policies.json
-> WP-11 native-family / route law
-> Step-3 execution owner model
-> Step-5.8 claim + live-born identity laws
```

This route exposed the strongest candidate gap: current identifier policy remains campaign/sequential for many kinds that can originate inside independently writable LIVE sources, while WP-11 explicitly delegates source-native live identity realization to WP-16.

### 1.5 Chronology / execution / information / agency

Route checked:

```text
Step-3 deterministic execution
-> Step-5.8 LIVE close/CAS/accepted-edge continuity
-> R2.5 collaboration/agency
-> GAME/CORE/CHRONOLOGY.md
-> GAME/CORE/INFORMATION.md
-> current R2.7 temporal/recovery constraints
```

The candidate correctly preserves accepted execution/RNG/idempotency, rejects Git/ref/freeze order as fictional chronology, keeps objective truth/knowledge/disclosure distinct and leaves durable async collaboration to WP-17.

---

## 2. Adversarial findings

### F16-01 — BLOCKING — LIVE claim domain is not closed enough for machine realization

**Failure mechanism**

The candidate requires typed immutable claims but leaves the baseline grammar as:

```text
exact native owner
OR owner-defined writable partition
```

without closing which categories are legal now, which categories are forbidden, and how a live-born owner can begin inside an immutable claim set.

That is insufficient for the Task-Brief requirement to prove native claim/containment coverage for every supported live-mutated owner/partition. It also permits an implementation to make a dangerous but superficially type-correct choice such as routing `world.player`, mode/join-policy, controller/authorization state or the campaign LIVE route selector through the same LIVE authority whose permission/currentness depends on those campaign-domain values.

A second defect is creation. Step-5.8 explicitly allows an owner whose lifecycle validly begins inside epoch E. An exact-owner-only interpretation cannot predeclare an identity that does not yet exist; a generic partition interpretation can become an unbounded scene/global namespace unless creation admission is typed and closed.

**Required repair**

The final WP-16 contract must close the baseline claim grammar to three explicit forms:

```text
EXACT_OWNER(family, native_identity)
    pre-existing native owner selected into E

EPOCH_LOCAL_CREATION(kind / native-family creation domain)
    typed permission for a native owner lifecycle to begin in E under the
    source-native identity contract; not authority over all existing records

OWNER_DEFINED_PARTITION(partition_type, partition_key)
    admissible only when a current owning specification already defines bounded
    membership, containment, non-overlap, mutation authority and recovery
```

No generic owner-defined sub-owner partition is active merely because an implementation can name one. In the WP-16 baseline, absent an already-owned partition contract, use exact-owner claims plus explicitly admitted epoch-local creation domains.

The final spec must also make campaign/access/routing authority unclaimable by LIVE, including at minimum:

- `world.player` membership/binding/policy-grant authority;
- campaign mode/join policy and equivalent campaign configuration authority;
- campaign creator provenance/owner-only authority;
- campaign route/claim selection and LIVE absorption/successor routing;
- indexes, cards, sessions, caches and other projections/helpers.

This prevents circular authorization and stale-revocation windows.

**Human decision required:** NO. This is the minimum owner-preserving realization of accepted Step-5.8 and Access Control.

---

### F16-02 — BLOCKING — source-native LIVE identity is still a property, not a closed machine policy

**Failure mechanism**

WP-11 explicitly hands WP-16 source-native epoch-qualified identity materialization. Step-5.8 requires any accepted LIVE-born identity that can escape the epoch to remain stable through absorption without campaign-allocator rekeying.

The candidate states this invariant, but current `DEV/CATALOG/identifier-policies.json` still assigns campaign/sequential identity to many relevant world/runtime kinds. Without a final WP-16 strategy discriminator, implementation planning could preserve the current campaign allocator/provisional-ID pattern while claiming compliance with the prose law.

**Required repair**

The final contract must define an implementation-facing source-native identity strategy for any durable native record first accepted inside LIVE:

```text
source_native_live identity basis
    = stable epoch/source identity
    + native kind/family identity domain
    + accepted source-local creation coordinate or equivalent collision-free
      source-local stable component
```

Requirements:

- generated before/at the accepting native LIVE edge;
- collision-free across independent LIVE sources without campaign allocator access;
- stable through retry, recovery, close and absorption;
- never rekeyed merely because persistence moves to campaign storage;
- lexical/numeric order has no chronology/priority meaning;
- derived child identities continue to derive from their stable accepted parent where the native owner already defines that rule;
- composite identities continue to use their semantic components and do not receive a second allocator identity;
- current machine identifier-policy realization must gain an explicit source-native LIVE disposition for every kind that may be durably born in LIVE; kinds without that disposition cannot create externally referenceable durable owners inside LIVE.

Exact string encoding remains implementation detail, but the strategy and per-kind admission are not.

**Human decision required:** NO. This directly discharges WP-11/F04 and Step-5.8.

---

### F16-03 — SIGNIFICANT — LIVE mutation lacks an explicit frozen authorization/currentness attempt envelope

**Failure mechanism**

The candidate correctly says exact-source CAS is not application authorization, but it does not make the application authorization/currentness footprint concrete enough for the final mutation race.

A session can resolve an action while PLAYER membership/control/policy/routing is current, then race a campaign-domain revocation or controller transfer before the LIVE mutation. An exact-source LIVE CAS can still succeed if the LIVE ref itself did not move. Treating that success as sufficient would recreate the stale-authorization window the task is required to eliminate.

**Required repair**

Define an immutable ephemeral `FrozenLivePublicationAttempt` or equivalent operation value containing at least:

```text
trusted stable external principal identity
resolved PLAYER identity + current membership basis
current controlled-PC / operation-specific authorization basis
selected campaign route / immutable LIVE claim basis
exact target LIVE source/ref + expected authoritative source revision
native owner identities/generations and bounded semantic dependency footprint
accepted execution/RNG/idempotency references needed by the mutation
```

Before the first authority-changing LIVE remote mutation, any mutable campaign-domain authorization/routing dependency required by the operation must still satisfy its owning currentness rule. If not, invalidate/rebuild or deny; successful LIVE CAS cannot retroactively legalize stale authorization.

This value is ephemeral operation state, not a permission lease, durable journal or new semantic owner.

---

### F16-04 — SIGNIFICANT — additive authorization, reactivation and controller transfer are not fully closed around ACTIVE LIVE

**Failure mechanism**

The candidate closes removal/deactivation well, but the Task Brief requires join, leave, removal, controller change and stale-session interaction. Step-5.8 additionally allows additive authorization to avoid rollover only when fixed claims/authorization-relevant semantics do not change.

Without an explicit rule, an implementation can either over-roll every additive join or, worse, switch PC control while an old controller still holds an ACTIVE source whose authorization basis was selected under the previous relation.

**Required repair**

Final law must distinguish:

- additive PLAYER activation/reactivation may remain a campaign-domain membership transition without touching unrelated LIVE sources when immutable claims and the source's authorization-relevant participant/control semantics do not change;
- a newly authorized participant must still reacquire current campaign/LIVE route, current PLAYER/control state and applicable native/collaboration obligations before mutable input;
- controller transfer or any authority change that alters who may exercise voluntary PC authority against an ACTIVE LIVE scope requires affected source close/freeze first, followed by the campaign authority transition and any successor from the new current basis;
- when route/absorption/control/membership facts form one no-window authority boundary, publish them in one campaign closure;
- the old controller's stale session must fail current authorization even if it retains old LIVE bytes/ref metadata.

No presence/heartbeat semantics are introduced.

---

### F16-05 — SIGNIFICANT — exact LIVE fence is semantically correct but physically under-specified against the fixed transport

**Failure mechanism**

Current shipped LIVE prose uses a cached `LIVE_STATE.yaml` blob/file SHA as an optimistic guard, while R2.6/WP-13 fix supported gameplay publication to Connector Git-data/ref operations ending in authoritative non-force ref transition. A content blob can prove payload identity but does not by itself prove that the selected live ref still names the expected current source revision.

The candidate's phrase “exact current selected source revision” is semantically right but leaves room for an implementation to use only the file/blob SHA as final currentness authority.

**Required repair**

For the supported Git-backed LIVE realization:

- the authoritative currentness fence is the exact selected live source/ref revision accepted by the authority-changing non-force transition; in the current Git realization this is the expected live-ref HEAD commit/source revision;
- `LIVE_STATE.yaml` blob/content SHA may validate exact payload identity and support efficient refresh, but cannot independently establish ref currentness;
- source-local integer `revision` remains diagnostics/idempotency support only;
- any Connector primitive used by implementation must be semantically equivalent to exact expected-source CAS; if the fixed supported Connector cannot provide that property, it is a capability failure rather than permission to fall back to another transport.

---

### F16-06 — SIGNIFICANT — projection fields are demoted, but post-selection revalidation is not explicit enough

**Failure mechanism**

SR16-02 required not only demotion of `CAMPAIGN_CARD`, session/index/MANIFEST/cache hints but explicit post-selection revalidation against actual Git provenance, PLAYER/access owners and current native write route/currentness.

Candidate laws correctly say these surfaces are not authority, but a future bootstrap/resume implementation could still use a fresh-looking card/session/cache value to skip the authoritative reads after campaign selection.

**Required repair**

Final law must require that after campaign selection/resume and before mutable gameplay:

```text
card/menu/session/index/cache hint
-> select candidate campaign only
-> pin current campaign ref
-> rederive/validate applicable creator provenance
-> load current mode/join policy from its owner
-> resolve current stable-ID PLAYER binding/membership
-> resolve current controlled-PC relation
-> resolve current campaign/LIVE write route and exact source currentness
-> only then admit mutable operation
```

MANIFEST may remain authoritative for its explicitly owned configuration fields, but a copied card/session/cache projection of those fields cannot replace the owner.

---

## 3. Non-findings / retained candidate strengths

The independent attack found no defect requiring change in these candidate decisions:

1. **Stable principal != login.** Current supported Connector capability is sufficient to continue; no identity fallback is needed.
2. **Campaign currentness != LIVE currentness != local HOT currentness.** No global source frontier is justified.
3. **`CLOSED_UNABSORBED` remains current truth with zero ordinary writers.** Campaign base cannot substitute.
4. **No distributed transaction/global rollback across LIVE refs.** Partial freeze is technical currentness only.
5. **Accepted execution/RNG/idempotency survives close/conflict/recovery.** Transport conflict cannot replay/reroll accepted mechanics.
6. **Technical CAS/ref/freeze order is not fictional chronology.** Native chronology/rules own contested ordering.
7. **Absence is not voluntary PC agency transfer.** Membership maintenance does not teleport/rewrite the PC.
8. **LIVE physical packing does not create world.knowledge/runtime.disclosure authority.** Information owners remain separate.
9. **WP-17 remains downstream.** No durable async-collaboration queue/timeout policy belongs in WP-16.
10. **No upstream architecture reopen is justified.** All findings are mechanically derivable realization closures under accepted owners.

---

## 4. Current stale consumer disposition

The critic reconfirms current implementation debt rather than treating it as architecture authority:

- `GAME/CORE/LIVE_SCENE.md` remains scene-centric and contains one-logical-action/one-live-write wording;
- `GAME/SCHEMA/live_scene.schema.yaml` lacks typed immutable claim grammar and source-native identity realization;
- `GAME/SCHEMA/scene.schema.yaml` treats scene LIVE pointer as broader mutable-scene authority than the final typed-claim model permits;
- `DEV/CATALOG/identifier-policies.json` still uses campaign/sequential strategies that cannot by themselves satisfy LIVE-born source-native identity;
- `DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md` M10 preserves the stale `close -> compact -> deactivate` sequence;
- `DEV/TESTS/LIVE_SCENE_CASES.md` L04 preserves user-action-level write atomicity and several cases remain scene/entity-centric.

These are downstream WP-19/WP-20/WP-22/WP-26 implementation/migration/test/doc obligations after architecture closure. They do not authorize rewriting runtime/schema/test files inside WP-16 Step 6.

---

## 5. Finding counts and gate

```text
STEP_6_BLOCKING:          2
STEP_6_SIGNIFICANT:       4
STEP_6_MINOR:             0
UNRESOLVED_BLOCKING:      2
UNRESOLVED_SIGNIFICANT:   4
HUMAN_DECISION_REQUIRED:  NO
UPSTREAM_REOPEN_REQUIRED: NO
```

Step 7 must repair F16-01..F16-06, propagate every changed/materially qualified law into the final owner, and explicitly mark the Step-5 candidate as historical where its wording differs.
