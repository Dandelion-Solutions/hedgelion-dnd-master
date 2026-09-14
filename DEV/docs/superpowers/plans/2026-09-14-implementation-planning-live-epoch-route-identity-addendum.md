# Implementation Planning — LIVE Epoch / Scene Route Identity Addendum

Status: **MANDATORY OVERLAY — AUTHOR FINDING 27 REPAIR / INDEPENDENTLY UNCONFIRMED**

Scope: planning only. This addendum does not authorize production implementation.

This overlay has higher precedence than RD-09 Tasks 3–6, Finding 24 and Finding 25 wherever those artifacts assume that `scene_id` / `epoch_id` may simply be interpolated into the WP-11 LIVE Git-ref route or leave epoch-ID creation/encoding unspecified.

## Finding 27 — SIGNIFICANT

Fresh post-F26 audit found two coupled worker-readiness gaps in the LIVE route:

1. WP-11 specifies the physical shape `live/<campaign-technical-id>/<scene_id>/<epoch_id>/...`, but `scene_id` is a semantic owner identity, not a transport-component contract. Current and planned scene identity policies can include forms that must not be assumed safe for direct Git-ref interpolation; in particular the F24–F26 `SOURCE_NATIVE_LIVE` printable form intentionally uses a semantic family prefix plus `:live1:` framing and therefore proves that a valid semantic `world.scene` ID cannot be treated generically as a ref component.
2. Step-5.8/WP-16 require a stable unique epoch identity and exact selected source, but RD-09 never selects an exact v1 epoch-ID derivation/printable encoding. Legacy shipped prose only recommended a truncated base-campaign-SHA example; it is not the current canonical machine owner, is not sufficient worker instruction, and does not encode the immutable claim basis that distinguishes competing candidate epochs prepared from the same campaign basis/scene with different admitted claims.

Without a repair, workers could choose incompatible epoch namespaces, truncate hashes differently, interpolate arbitrary semantic IDs into refs, or allow orphan/prepared source naming collisions to leak into authority selection.

This is delegated machine realization under already accepted WP-11 / Step-5.8 / WP-16 semantics. It does not reopen LIVE authority architecture.

---

## 1. Semantic identities remain semantic

The F25 semantic LIVE source key remains:

```text
LiveSourceKey {
    campaign_id
    scene_id
    epoch_id
}
```

where:

- `campaign_id` is the canonical immutable campaign identity;
- `scene_id` is the canonical native `world.scene` identity selected for the scene-centered LIVE route;
- `epoch_id` is the v1 epoch identity defined below.

A Git ref/path component, route token, branch name, exact current LIVE revision, local path or current campaign HEAD is not a substitute for any of these semantic identity fields.

F24 source-native IDs continue to frame semantic `(campaign_id, scene_id, epoch_id)`, never derived physical route tokens.

---

## 2. Canonical claim encoding for epoch-opening basis

Epoch identity must distinguish immutable opening bases without inventing chronology or a global allocator.

RD-09 SHALL expose one pure canonicalization helper conceptually:

```text
canonicalize_live_claim_set(claims: Iterable[LiveClaim]) -> tuple[bytes, ...] | BLOCKED
```

The claim set is semantically unordered. Canonicalization therefore produces one exact byte frame per validated claim and sorts those complete frames lexicographically as unsigned bytes. Duplicate complete claim frames are invalid rather than silently duplicated.

Use the following exact framing primitives:

```text
UTF8(s)      = UTF-8 bytes of s
U32BE(n)     = unsigned 32-bit big-endian integer
FRAME_STR(s) = U32BE(len(UTF8(s))) || UTF8(s)
FRAME_LIST(xs) = U32BE(len(xs)) || concat(U32BE(len(x)) || x for x in xs)
```

Claim frames:

### EXACT_OWNER

The native owner adapter supplies its complete semantic identity components in the exact owner-defined order already required for deterministic native routing.

```text
0x01
|| FRAME_STR(native_family)
|| FRAME_LIST([UTF8(component_0), ..., UTF8(component_n)])
```

Changing identity-component order changes the claim frame because native composite identity order is semantic.

### EPOCH_LOCAL_CREATION

```text
0x02
|| FRAME_STR(native_family)
```

### OWNER_DEFINED_PARTITION

Only an already admitted owner-defined partition may use this form. Its owner adapter supplies a complete deterministic ordered tuple of string key components. If the owner cannot expose such a bounded deterministic key, the partition claim is not v1-encodable and opening is BLOCKED rather than serialized from arbitrary JSON/model prose.

```text
0x03
|| FRAME_STR(partition_type)
|| FRAME_LIST([UTF8(component_0), ..., UTF8(component_n)])
```

No path glob, arbitrary JSON object ordering, current directory order, model wording or hash-table iteration participates in claim identity.

`DEV/SCHEMAS/live-claim.schema.json` must expose enough typed structure to validate these exact complete identity/key components. This is an encoding projection of the already accepted closed claim grammar, not a new claim kind.

---

## 3. Exact v1 epoch identity

Add RD-09 helper:

```text
derive_live_epoch_id(
    campaign_id: str,
    scene_id: str,
    opening_campaign_revision: str,
    immutable_claims: Iterable[LiveClaim],
) -> str | BLOCKED
```

First canonicalize the immutable claim set as §2. Then build:

```text
EPOCH_FRAME =
    UTF8("HDM-LIVE-EPOCH-ID-V1")
    || 0x00
    || FRAME_STR(campaign_id)
    || FRAME_STR(scene_id)
    || FRAME_STR(opening_campaign_revision)
    || FRAME_LIST(canonical_claim_frames)
```

The v1 semantic epoch ID is:

```text
epoch_id = "e1-" + lowercase(hex(SHA256(EPOCH_FRAME)))
```

Exact shape:

```text
^e1-[0-9a-f]{64}$
```

Rationale and invariants:

- campaign/scene/opening revision/immutable claims all participate;
- claim input container order does not participate;
- different exact-owner identity component order does participate where the owner says the identity tuple is ordered;
- acting principal/session/host/model response/timestamp/randomness do not participate;
- current LIVE revision after opening does not participate;
- the full 256-bit digest is used; no 12-hex or other truncation;
- the digest conveys no fictional time, ordering, authority, priority or generation.

The complete opening basis is already native routing/claim evidence under Step-5.8 and SHALL remain available for exact validation. `epoch_id` is therefore never accepted solely because two digests compare equal: current route/source validation compares the complete expected opening basis against the selected LIVE envelope as described below. A digest collision or body mismatch is an integrity conflict, not an alias rule.

---

## 4. Candidate/opening semantics

The epoch ID is computed before preparing the candidate LIVE source from one pinned campaign opening basis.

Conceptual v1 opening sequence:

```text
pin exact current campaign revision H
-> resolve canonical campaign_id
-> resolve canonical scene_id
-> freeze exact immutable typed claim set Q
-> validate authorization / containment / non-overlap prerequisites
-> epoch_id = derive_live_epoch_id(campaign_id, scene_id, H, Q)
-> derive bounded physical route components (§5)
-> prepare candidate LIVE source non-authoritatively
-> campaign authority transaction CAS-selects exact route / Q / opening basis
-> only accepted campaign route selection establishes LIVE authority
```

Step-5.8 LAW 5.8-38 remains controlling: prepared source existence is never authority.

If campaign route-selection CAS definitely rejects/stales:

- the prospective candidate epoch is noncanonical unless another accepted current route already selects the exact same complete opening basis/source;
- refresh the campaign basis and recompute epoch identity before a new opening attempt;
- do not preserve rejected candidate identity through a random suffix/alias.

If campaign route-selection outcome is indeterminate, reconcile the original campaign publication/currentness result before preparing a logically new opening. Do not create a second epoch merely because acknowledgement was lost.

Two candidate attempts from the same complete opening basis intentionally derive the same `epoch_id`; the campaign route-selection CAS decides authority. Two candidates that differ in immutable claim basis derive different epoch IDs even if campaign revision and scene are equal.

A successor after predecessor absorption uses the then-current campaign revision and therefore cannot silently reuse the predecessor's complete opening basis/epoch ID.

---

## 5. Bounded physical LIVE route components

F25 already defines:

```text
campaign_route_token = encode_live_campaign_route_token(campaign_id)
                      = "c1-" + 64 lowercase SHA-256 hex characters
```

Add RD-09 helper:

```text
encode_live_scene_route_token(scene_id: str) -> str
```

with exact algorithm:

```text
SCENE_ROUTE_FRAME =
    UTF8("HDM-LIVE-SCENE-ROUTE-V1")
    || 0x00
    || FRAME_STR(scene_id)

scene_route_token = "s1-" + lowercase(hex(SHA256(SCENE_ROUTE_FRAME)))
```

Exact shape:

```text
^s1-[0-9a-f]{64}$
```

The v1 `epoch_id` from §3 is already fixed-length ASCII with exact safe machine spelling and is used as the epoch route component.

The resulting physical WP-11 LIVE route is:

```text
live/<campaign_route_token>/<scene_route_token>/<epoch_id>/LIVE/LIVE_STATE.yaml
```

Example shape only:

```text
live/c1-<64hex>/s1-<64hex>/e1-<64hex>/LIVE/LIVE_STATE.yaml
```

The campaign and scene tokens are physical locators only. `epoch_id` is semantic identity but has an intentionally transport-safe v1 spelling. Branch/ref existence still never selects authority.

Do not interpolate raw `campaign_id` or raw `scene_id` into the LIVE ref. Do not derive route components from display names, campaign branch names, current LIVE revision, timestamps, model text or local paths.

---

## 6. LIVE envelope / route validation

The repaired v1 LIVE envelope must carry at least the semantic/opening evidence needed to validate:

```text
campaign_id
scene_id
epoch_id
opening_campaign_revision
immutable typed claims Q
lifecycle
exact current source/currentness metadata required by the existing owner
```

The campaign LiveRoute/current routing evidence likewise retains the owner-required semantic/opening basis from Step-5.8.

On selection/recovery, validate all of:

```text
expected campaign_id == LIVE_STATE.campaign_id
expected scene_id == LIVE_STATE.scene_id
expected epoch_id == LIVE_STATE.epoch_id
expected opening_campaign_revision == LIVE_STATE.opening_campaign_revision
canonical(expected Q) == canonical(LIVE_STATE.Q)

derive_live_epoch_id(
    LIVE_STATE.campaign_id,
    LIVE_STATE.scene_id,
    LIVE_STATE.opening_campaign_revision,
    LIVE_STATE.Q,
) == LIVE_STATE.epoch_id

encode_live_campaign_route_token(LIVE_STATE.campaign_id)
    == physical campaign route token
encode_live_scene_route_token(LIVE_STATE.scene_id)
    == physical scene route token
```

Any mismatch is a typed integrity/currentness failure and blocks adoption/mutation/recovery for the affected scope.

Do not repair mismatch by scanning refs, picking a nearest-looking branch, accepting the digest alone, rewriting the semantic scene/epoch ID, truncating/rehashing differently or manufacturing an alias.

---

## 7. F24/F25/F26 interaction

The current source-native identity basis after this overlay is:

```text
canonical campaign_id
+ canonical scene_id
+ exact v1 epoch_id from §3
+ native family
+ accepted source-local creation ordinal from F24/F26
```

F24's `framed_base32hex_v1` continues to use semantic values, not route tokens.

F25 remains authoritative for campaign semantic identity and `c1-...` physical campaign token.

F26 remains authoritative for deterministic multiple-source-native creation ordering within one frozen LIVE mutation.

This overlay only closes epoch creation and remaining physical route-component realization.

---

## 8. Exact RD-09 amendments

### Task 3 — LIVE envelope / claim schema

In addition to F24–F26 changes:

- require canonical `campaign_id`, `scene_id`, `epoch_id`, `opening_campaign_revision` and immutable typed claims in the final v1 LIVE envelope;
- make `epoch_id` satisfy `^e1-[0-9a-f]{64}$`;
- make `live-claim.schema.json` expose exact typed owner/partition identity components required by §2 canonical framing;
- remove/demote legacy fields/wording that treat branch name as semantic identity or permit truncated/example-only epoch-ID rules to control v1 behavior.

### Task 4 — route/currentness/opening helper

Extend `GAME/TOOLS/live_state.py` with conceptually:

```text
canonicalize_live_claim_set(...)
derive_live_epoch_id(...)
encode_live_campaign_route_token(...)   # F25
encode_live_scene_route_token(...)
build_live_ref(campaign_id, scene_id, epoch_id) -> str
validate_live_route_identity(expected_route, live_state, physical_ref) -> None
```

`build_live_ref` accepts semantic IDs and internally derives bounded physical tokens. Callers must not concatenate raw semantic IDs into the ref themselves.

### Task 6 — frozen opening/publication evidence

The applicable frozen opening/publication attempt evidence must retain exact semantic/opening basis and exact physical target ref separately. Exact current source revision remains the CAS fence after opening; it never enters semantic epoch identity.

---

## 9. RD-06 / RD-07 / RD-16 joins

### RD-06 campaign route-selection publication

When campaign publication selects a new LIVE route, the candidate route must bind one exact semantic/opening basis plus target physical ref. Campaign CAS acceptance, not prepared branch existence, establishes authority.

Where RD-06 owns the campaign transaction that establishes/changes current LIVE routing, add integration proof that the route cannot be selected if the candidate source's full opening basis/ref encoding fails §6 validation.

This does not make RD-06 the epoch identity owner; it consumes RD-09's deterministic construction/validator.

### RD-07 recovery

Selected-LIVE recovery:

```text
current campaign route
-> semantic campaign_id / scene_id / epoch_id / opening basis
-> derive c1/s1 physical route components
-> exact target ref
-> pin exact selected LIVE source revision
-> validate full LIVE envelope/opening basis
-> only then hydrate current native owners
```

No raw semantic-ID interpolation, directory/ref scan or legacy `E_<12hex>` inference is allowed.

### RD-16 shared identifier policy

F27 does not introduce a new native record family or campaign allocator policy. RD-16's shared identifier policy proof only needs to preserve compatibility with the final F24–F27 source-native identity basis; epoch identity itself is LIVE route identity owned by RD-09, not a new catalog record identity policy.

---

## 10. Exact tests

Add RD-09 group:

```text
LiveEpochRouteIdentityTests
```

Required cases:

1. identical complete opening basis derives identical `epoch_id`;
2. changing `campaign_id`, `scene_id`, pinned opening campaign revision or immutable claim set changes the epoch ID;
3. reordering the input claim container does not change the epoch ID;
4. changing owner-defined identity-component order inside an ordered composite identity does change the relevant claim frame/epoch ID;
5. duplicate canonical claim frames are rejected;
6. unencodable owner-defined partition key blocks opening instead of serializing arbitrary JSON/model text;
7. epoch ID uses the full SHA-256 digest and exact `e1-[0-9a-f]{64}` spelling; no 12-hex truncation baseline survives;
8. principal/session/host/timestamp/randomness/current LIVE revision do not alter epoch ID;
9. `scene_id = "scene:live1:..."` or other semantic ID spelling never appears raw in the physical LIVE ref; it maps to `s1-<64hex>`;
10. physical LIVE ref exact shape is `live/c1-<64hex>/s1-<64hex>/e1-<64hex>/LIVE/LIVE_STATE.yaml`;
11. c1/s1 token equality alone cannot override semantic body mismatch;
12. recomputed epoch ID must equal body epoch ID and full expected opening basis must equal body basis;
13. prepared source without accepted campaign route remains non-authoritative;
14. definite stale/rejected route selection requires refreshed campaign basis before a new logical opening;
15. indeterminate route selection is reconciled before another logical epoch is prepared;
16. same complete basis prepared concurrently maps to one prospective epoch identity and cannot gain two authorities;
17. different immutable claim bases from the same campaign revision/scene derive different candidate epoch IDs;
18. successor after accepted predecessor absorption uses new current campaign basis and cannot silently reuse predecessor epoch ID;
19. F24/F25/F26 source-native IDs continue to frame semantic campaign/scene/epoch values and are unaffected by c1/s1 token spelling;
20. no legacy branch-name/existence/current-revision heuristic can select epoch authority.

Extend RD-06 publication integration tests with route-selection candidate identity mismatch/blocking cases.

Extend RD-07 `SelectedLiveCampaignIdentityRecoveryTests` / `SourceNativeLiveRecoveryTests` with c1/s1/e1 exact-route and full-opening-basis validation.

---

## 11. File impact

Mandatory execution-time surfaces, subject to fresh currentness:

```text
RD-09
  MODIFY GAME/TOOLS/live_state.py
  REPLACE/MODIFY GAME/SCHEMA/live_scene.schema.yaml
  CREATE/MODIFY DEV/SCHEMAS/live-claim.schema.json
  MODIFY DEV/SCHEMAS/live-publication-attempt.schema.json where opening basis/ref is frozen
  MODIFY DEV/TESTS/test_rd09_access_live.py

RD-06
  MODIFY GAME/TOOLS/publication.py at the campaign LIVE-route selection validation seam
  MODIFY DEV/TESTS/test_rd06_durability_publication.py

RD-07
  MODIFY GAME/TOOLS/recovery.py
  MODIFY DEV/TESTS/test_rd07_recovery.py
```

Do not introduce a new global epoch allocator, campaign-wide fencing counter, random UUID service, branch-name authority, directory scanner or second LIVE route registry.

If execution currentness shows exact file renames, route the same behavior to the current owner file; do not drop the requirement.

---

## 12. Checkpoint / dependency choreography

Owner-local work may proceed independently until named joins.

```text
RD-09 LIVE_EPOCH_ROUTE_IDENTITY_READY
    = final claim encoding
    + epoch derivation
    + scene token
    + LIVE envelope/ref validator

RD-09 LIVE_EPOCH_ROUTE_IDENTITY_READY
+ RD-09 F24/F25/F26 SOURCE_NATIVE pieces
    JOIN_BEFORE_INTEGRATION
RD09_SOURCE_NATIVE_ID_READY
```

RD-06 route-selection integration consumes `LIVE_EPOCH_ROUTE_IDENTITY_READY` before it can claim new-LIVE campaign route publication GREEN.

RD-07 selected-LIVE recovery consumes the same checkpoint before it can claim exact selected-source recovery GREEN.

No whole-RD cycle is introduced. RD-09 still owns epoch/route realization; RD-06 consumes its validator at campaign publication; RD-07 consumes it at recovery; RD-16 consumes only the resulting source-native identifier-policy integration.

Every publishable checkpoint obeys the package checkpoint-coherence overlay: all committed tests, maintenance audit and full DEV discovery GREEN; no future-task intentional RED is pre-created.

---

## 13. Negative stale proof

Implementation/proof fails if any current v1 path permits:

- raw semantic `scene_id` to be interpolated directly into the LIVE Git ref;
- source-native scene IDs such as `scene:live1:...` to determine physical ref spelling directly;
- epoch ID spelling to remain implementation-choice/example-only;
- truncated `E_<first-12-hex>` to remain the v1 baseline contract;
- claim container iteration order/model prose/arbitrary JSON serialization to affect epoch identity;
- principal/session/time/randomness/current LIVE revision to affect epoch identity;
- branch/ref existence to establish authority;
- digest/token equality to override full semantic/opening-basis mismatch;
- stale/indeterminate opening attempts to create alias/random-suffix successor identities without currentness reconciliation;
- directory/ref scanning to recover a selected epoch when current route should provide bounded exact semantic/source routing;
- physical c1/s1 token spelling to enter F24 semantic source-native identity frames.

---

## 14. Proof routing

Add post-graph proof row `PG27`:

```text
PG27 exact LIVE epoch identity + bounded scene/ref realization
  -> RD-09 canonical claim-set framing
  -> deterministic e1 epoch derivation from full immutable opening basis
  -> c1/s1/e1 bounded physical LIVE ref construction
  -> full route/body/opening-basis validation
  -> RD-06 campaign route-selection validation
  -> RD-07 selected-LIVE exact recovery
  -> preservation of F24–F26 source-native semantic identity
```

Exact witnesses:

```text
RD-09 LiveEpochRouteIdentityTests
RD-09 LiveCampaignRouteIdentityTests
RD-09 SourceNativeLiveIdEncodingTests
RD-06 LIVE route-selection identity integration cases
RD-07 SelectedLiveCampaignIdentityRecoveryTests
RD-07 SourceNativeLiveRecoveryTests
```

Primary channels: `FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO + STATIC_AUDIT`.

---

## 15. Version / migration disposition

This is unreleased v1 clean-slate LIVE route/epoch machine realization. The final v1 LIVE schema/ref contract may replace legacy recommended/truncated epoch spelling without a compatibility alias for pre-v1 runtime data.

Run the normal execution-time Version Impact Gate for the final LIVE schema/API/attempt contracts. Migration execution remains outside the current package.

---

## 16. Disposition

```text
AUTHOR_FINDING_27: REPAIRED_IN_PLANNING
SEVERITY: SIGNIFICANT
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```
