# R2.7 WP-16 — Multiplayer / Access Control / Live State — Step 7 Resolution Gate

Status: **STEP 7 COMPLETE — ALL BLOCKING/SIGNIFICANT FINDINGS RESOLVED**

Date: 2026-09-03

Step-6 critic:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-step-6-whole-project-adversarial-review.md`

Candidate:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-step-5-candidate-spec.md`

Final implementation-facing owner to be produced by Step 8:

- `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md`

---

## 1. Resolution summary

```text
STEP_6_BLOCKING:          2
STEP_6_SIGNIFICANT:       4
UNRESOLVED_BLOCKING:      0
UNRESOLVED_SIGNIFICANT:   0
HUMAN_DECISION_REQUIRED:  NO
UPSTREAM_REOPEN_REQUIRED: NO
```

All repairs are mechanically implied by accepted Step-5.8, R2.5/R2.6, Access Control and WP-11..WP-14 contracts. No finding introduces a new product semantic choice or changes an accepted upstream authority.

---

## 2. F16-01 — LIVE claim domain closure

**Severity:** BLOCKING

**Do we agree?** YES.

### Resolution

The final WP-16 claim grammar is closed to:

```text
LiveClaim :=
    EXACT_OWNER(native_family, native_identity)
  | EPOCH_LOCAL_CREATION(native_family)
  | OWNER_DEFINED_PARTITION(partition_type, partition_key)
```

with the following laws.

### 2.1 `EXACT_OWNER`

`EXACT_OWNER` names exactly one pre-existing native semantic owner. It does not claim referenced dependencies, child objects, related scene members, same-location records or all records of the same family.

Mutation is admitted only if the complete owner-native mutation footprint for that accepted edge remains inside the selected claim/source boundary or the owning cross-source synchronization rule has been satisfied.

### 2.2 `EPOCH_LOCAL_CREATION`

`EPOCH_LOCAL_CREATION(family)` permits only creation of a new native owner of that admitted family whose lifecycle validly begins in the selected epoch.

It is not a wildcard claim over existing records of the family.

The created identity must use the source-native LIVE identity policy resolved in F16-02 before the first accepted edge exposes a stable reference.

The permitted family set is a closed machine contract. A family absent from the current set cannot be durably created in LIVE merely because generic YAML/JSON can encode it.

### 2.3 `OWNER_DEFINED_PARTITION`

An owner-defined partition is admissible only when a current owning specification defines all of:

- partition identity/type;
- deterministic bounded membership/containment;
- non-overlap rule against other selected LIVE claims;
- exact mutation authority;
- currentness/recovery semantics;
- transition/transfer semantics.

No generic sub-owner partition is active in the WP-16 baseline solely for convenience. Until such an owner contract exists, use exact-owner claims plus admitted epoch-local creation domains.

### 2.4 Campaign/access/routing authorities are not LIVE-claimable

The following remain campaign/native authority and are forbidden from LIVE claim ownership:

- `world.player` membership/binding/status and player policy grants;
- controlled-PC assignment/transfer authority;
- campaign mode and join-policy authority;
- campaign creator provenance and creator-only authorization basis;
- campaign LIVE route/claim selection, predecessor absorption and successor selection;
- campaign/storage/engine write-routing authority;
- `CAMPAIGN_CARD`, session, index, checkpoint and cache projections/helpers.

The same source whose write authorization depends on a value may not become the owner of that campaign authorization value merely to simplify revocation.

### Consequence

The final spec will replace the candidate's open generic partition wording with this closed grammar and explicit forbidden-authority class.

**Human decision required:** NO.

---

## 3. F16-02 — source-native LIVE identity policy

**Severity:** BLOCKING

**Do we agree?** YES.

### Resolution

WP-16 introduces the implementation-facing logical identity strategy:

```text
strategy: source_native_live

identity basis:
    stable live epoch/source identity
  + native family/kind identity domain
  + accepted source-local creation coordinate
    or owner-defined collision-free equivalent
```

The exact printable/wire encoding is implementation detail, but the semantic strategy and per-kind admission are canonical.

Requirements:

1. identity is fixed before or at the accepting native LIVE edge;
2. independent LIVE sources cannot collide without campaign allocator coordination;
3. accepted identity survives retry, recovery, close and campaign absorption unchanged;
4. absorption never rekeys solely because physical storage moves to campaign paths;
5. campaign `runtime.id_allocator` is not used to allocate an identity whose first accepted durable owner is LIVE;
6. ID ordering never establishes chronology, causal priority or CAS winner semantics;
7. a derived child identity already defined from a stable parent continues to derive from that stable parent and does not gain a second allocator identity;
8. composite-key owners retain their canonical semantic composite identity when all components are already stable; they do not receive a second source-native surrogate merely because their payload is transported in LIVE;
9. every native kind that may be durably born in LIVE must have an explicit machine identifier-policy disposition permitting `source_native_live` or an owner-defined equivalent;
10. a kind whose machine identity policy has no LIVE-born disposition cannot create an externally referenceable durable owner inside LIVE.

Current campaign/sequential policies in `DEV/CATALOG/identifier-policies.json` are therefore machine-contract debt to be replaced/synchronized under later realization; they are not accepted fallback behavior.

**Human decision required:** NO.

---

## 4. F16-03 — frozen LIVE publication attempt

**Severity:** SIGNIFICANT

**Do we agree?** YES.

### Resolution

The final architecture requires one immutable ephemeral LIVE mutation attempt value, conceptually:

```text
FrozenLivePublicationAttempt {
    repository_identity
    campaign_ref_and_pinned_campaign_authorization_basis
    stable_external_principal_id
    player_id
    membership_status_basis
    controlled_pc / operation_authorization_basis
    selected_live_epoch
    immutable_claim_basis
    target_live_ref
    expected_exact_live_source_revision
    affected_native_owner_ids / generations
    bounded semantic dependency/currentness footprint
    accepted execution / RNG / idempotency references as applicable
    normalized native LIVE delta
}
```

It is operation state only: no journal, lease, permission token or semantic owner is added.

Before the first authority-changing remote mutation:

1. trusted current principal must still resolve;
2. mutable campaign-domain authorization/routing dependencies required by the operation must still satisfy their owning currentness rule;
3. the selected LIVE route/claim must still admit every affected owner;
4. the expected exact LIVE source revision must remain the CAS basis.

If campaign authority moved over relevant membership/control/policy/routing state, invalidate/rebuild or deny before LIVE mutation. A later successful LIVE CAS never cures stale application authorization.

---

## 5. F16-04 — additive authorization/reactivation/controller transfer

**Severity:** SIGNIFICANT

**Do we agree?** YES.

### Resolution

The final contract distinguishes authority changes by effect on the selected LIVE source.

### 5.1 Additive membership with no fixed-claim/authorization semantic change

An additive PLAYER activation/reactivation or newly valid participant need not close an unrelated ACTIVE LIVE source when all are true:

- the immutable LIVE claims remain identical;
- existing writers' operation-specific authority is unchanged;
- no existing controlled-PC relation is transferred;
- no LIVE-local authorization-relevant partition semantics change;
- the new participant is not treated as mutable-authorized in that source until current campaign membership/control/routing and applicable obligations are reacquired.

This is a campaign membership transition, not proof that the participant already belongs to the current LIVE writer set.

### 5.2 Controller transfer / authority substitution

If controller transfer, removal/replacement or another authority change alters who may exercise voluntary PC authority against an ACTIVE LIVE claim:

```text
close/freeze affected LIVE source(s) by exact-source CAS
-> establish exact final source revision(s)
-> one campaign authority transition for all same-domain route/absorption/
   controller/membership facts whose separation would create a stale-authority window
-> resolve successor from that new current campaign state if still required
```

The predecessor never reopens. The prior controller's stale session fails current authorization even when it retains old bytes/ref metadata.

### 5.3 Rejoin/catch-up

A newly activated/reactivated participant must reacquire:

```text
current campaign ref/routing
-> current PLAYER binding/membership
-> current controlled-PC assignment
-> selected current LIVE source if any
-> current native/collaboration obligations
-> role/recipient context
```

before mutable player input. WP-17 still owns durable async contribution realization.

---

## 6. F16-05 — exact LIVE source fence under fixed transport

**Severity:** SIGNIFICANT

**Do we agree?** YES.

### Resolution

For the supported Git-backed realization, exact LIVE currentness is fenced by the exact selected source/ref revision accepted by the authority-changing non-force transition.

Under the current fixed Connector Git-data/ref transport profile this means the attempt must protect the expected live-ref HEAD/source commit revision semantically; a content/blob SHA alone cannot prove that the authoritative ref still selects the same source revision.

Disposition of current values:

| Value | Role |
|---|---|
| selected live ref identity | source/routing identity; not sufficient without current exact revision |
| expected live-ref HEAD / exact native source revision | **authoritative CAS/currentness fence** |
| `LIVE_STATE.yaml` blob/content SHA | exact payload identity / efficient refresh / additional validation; not independent ref currentness |
| LIVE integer `revision` | source-local diagnostic/idempotency support; not authority |
| campaign `base_campaign_sha` | pinned durable base/provenance for epoch semantics; not current LIVE fence |
| campaign HEAD | campaign-domain currentness/routing basis; not substitute for live source revision |
| local HOT source basis | local adoption/cache currentness only; never remote authority |

An equivalent future Connector operation is admissible only if it preserves exact expected-source CAS semantics on the selected authority. Missing required fixed-Connector capability is a supported-profile capability failure, not an alternate-transport trigger.

---

## 7. F16-06 — post-selection owner revalidation

**Severity:** SIGNIFICANT

**Do we agree?** YES.

### Resolution

After campaign selection/resume, card/menu/session/index/cache data may nominate a candidate only.

Before mutable gameplay the supported route is:

```text
candidate campaign selection
-> pin current selected campaign ref
-> rederive/validate applicable creator provenance where the operation needs it
-> load current mode/join policy from its owning campaign configuration
-> resolve current stable-user-ID PLAYER binding/membership
-> resolve current controlled-PC relation
-> resolve operation-specific authorization
-> resolve current campaign/LIVE write authority and exact native source currentness
-> admit mutation
```

`MANIFEST` remains authoritative only for fields it actually owns. A repeated card/session/index/cache projection never replaces current owner validation.

This explicitly consumes SR16-02's post-selection requirement.

---

## 8. Finding-propagation sweep

The mandatory Step-7 propagation sweep is satisfied as follows.

| Artifact / owner | Disposition |
|---|---|
| Step-1 Task Brief | **RETAIN CURRENT** — already required claim-class coverage, live-born identity, join/removal/controller interaction and projection revalidation. Findings make those requirements concrete; no rejected Step-1 law is preserved. |
| Step-1 Source Manifest + Senior repair | **RETAIN CURRENT/HISTORICAL EVIDENCE** — open-world discovery obligations remain valid. No current semantic authority is assigned there. |
| Step-2 evidence extraction / manifest expansion | **RETAIN HISTORICAL** — evidence remains valid; Step-6 adds stricter realization closure. No rewrite as if Step 2 originally made later repairs. |
| Step-3 Decision Brief | **RETAIN HISTORICAL / DECISION STILL VALID** — Alternative B and human-decision disposition are unchanged. Findings refine machine completeness inside the selected direction. |
| Step-4 collaborative review | **RETAIN HISTORICAL / DIRECTION STILL VALID** — no accepted product trade-off changed. |
| Step-5 candidate | **MUST BE MARKED SUPERSEDED FOR FINAL LAW WHERE DIFFERENT** — especially generic claim grammar, identity materialization, LIVE attempt envelope, additive/controller lifecycle, exact fence and post-selection revalidation. Step 8 will add an explicit supersession banner. |
| Step-6 critic | **RETAIN FINDING RECORD** — counts remain 2 BLOCKING + 4 SIGNIFICANT. |
| Step-7 resolution | **CURRENT RESOLUTION PROVENANCE** until Step-8 final owner is published. |
| Final WP-16 canonical spec | **ONE CURRENT IMPLEMENTATION-FACING OWNER** — must contain every resolved law above. |
| `DEV/CURRENT_PROGRESS.md` | **UPDATE AT STEP 8** to WP-16 Steps 1-8 complete / mandatory final Senior audit; next authorized unit is only that audit. |
| R2.7 task-local cursor | **UPDATE AT STEP 8** with final SHA/artifacts/counts and no unpublished work. |
| `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | **UPDATE AT STEP 8** because WP-16 creates a material accepted physical-realization locator for live access/currentness/identity. Index remains derivative. |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | **NO UPDATE** — sequence/scope/dependencies do not change. WP-17 remains next domain only after Senior authorization. |
| `GAME/CORE/LIVE_SCENE.md`, `GAME/CORE/MULTIPLAYER.md`, schemas/catalog identity policies/tests | **RETAIN AS CURRENT IMPLEMENTATION DEBT / DOWNSTREAM REALIZATION** — do not silently rewrite during architecture Step 7. WP-19/WP-20/WP-22/WP-26 receive the existing obligations. |
| Deferred/backlog | **NO NEW OWNER** — WP-17 async collaboration, WP-22 executable tests, WP-24 measurement and WP-26 stale-doc/schema/test consistency remain in their existing downstream domains. |

No current normative statement is left solely in the historical candidate after Step 8.

---

## 9. Step-7 gate

```text
F16_01: CLOSED
F16_02: CLOSED
F16_03: CLOSED
F16_04: CLOSED
F16_05: CLOSED
F16_06: CLOSED

STEP_6_BLOCKING:          2
STEP_6_SIGNIFICANT:       4
UNRESOLVED_BLOCKING:      0
UNRESOLVED_SIGNIFICANT:   0
HUMAN_DECISION_REQUIRED:  NO
UPSTREAM_REOPEN_REQUIRED: NO
STEP_8_AUTHORIZED:        YES
```

Step 8 must canonicalize these resolutions, run final consistency review, synchronize derivative/current-progress state, publish one coherent final checkpoint and stop at mandatory Senior final audit.
