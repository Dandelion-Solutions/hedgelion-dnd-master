# Implementation Planning — LIVE Campaign Identity / Physical Routing Addendum

Status: **MANDATORY OVERLAY — AUTHOR FINDING 25 REPAIR / INDEPENDENTLY UNCONFIRMED**

Scope: planning only. This addendum does not authorize production implementation.

This overlay has higher precedence than Finding-24 source-native LIVE identity wording wherever that wording treats `campaign_technical_id` as semantic campaign identity. It also amends RD-09 LIVE routing/currentness, RD-14 creation identity propagation, RD-06 ordinary campaign publication validation and RD-07 selected-LIVE recovery only at the exact identity/routing seams below.

## Finding 25 — SIGNIFICANT

Finding 24 selected a stable LIVE source key containing `campaign_technical_id`. Fresh owner review shows that this conflates two different roles:

- WP-19 freezes canonical `campaign_id` before New Game remote mutation and materializes that value through the generated campaign scaffold;
- WP-20 requires campaign identity to be preserved across compatible migration/adoption;
- WP-11 uses `<campaign-technical-id>` only as a placeholder inside the physical LIVE ref route `live/<campaign-technical-id>/<scene_id>/<epoch_id>/...` and does not define a second semantic identity owner;
- WP-16 / Step-5.8 require stable LIVE source identity but do not define `campaign_technical_id` as a semantic field;
- current `campaign_manifest.schema.yaml` admits `campaign_id` as a string and does not guarantee that raw bytes are safe as one Git ref component.

Therefore a worker could incorrectly persist a second campaign identity, derive source-native record IDs from a transport token, or place raw `campaign_id` bytes in a ref component. Any of those choices could make identity diverge across creation, routing, recovery and migration.

This is an implementation-planning defect, not an architecture reopen. Existing owners already establish one campaign identity and separately require a bounded physical LIVE route.

---

## 1. One semantic campaign identity

For the v1 baseline, the canonical semantic campaign identity used by LIVE identity is exactly the campaign's frozen `campaign_id` from WP-19 / `MANIFEST.yaml`.

There is no second semantic `campaign_technical_id` field.

The Finding-24 source key is corrected to:

```text
LiveSourceKey {
    campaign_id
    scene_id
    epoch_id
}
```

`campaign_id` is the value frozen in the New Game creation envelope and materialized into the campaign scaffold. It remains the same campaign identity for ordinary publication/recovery and across any later compatible migration path; migration execution itself remains outside the current implementation package.

Branch names, Git refs, current source revisions, local paths, creator login, display names and the physical route token defined below are not semantic campaign identity.

### 1.1 Finding-24 printable source-native ID correction

Every occurrence of `campaign_technical_id` inside Finding 24's `framed_base32hex_v1` semantic ID frame is replaced by canonical `campaign_id`.

The corrected semantic frame is:

```text
FRAME =
    UTF8("HDM-LIVE-ID-V1")
    || 0x00
    || U32BE(len(UTF8(campaign_id))) || UTF8(campaign_id)
    || U32BE(len(UTF8(scene_id))) || UTF8(scene_id)
    || U32BE(len(UTF8(epoch_id))) || UTF8(epoch_id)
    || U32BE(len(UTF8(native_family))) || UTF8(native_family)
    || U64BE(source_local_creation_ordinal)
```

The printable native ID remains:

```text
family_prefix + ":live1:" + lowercase(unpadded_base32hex(FRAME))
```

This keeps the semantic encoding injective without depending on a hashed/physical route token.

---

## 2. Derived physical LIVE campaign route token

WP-11's `<campaign-technical-id>` placeholder is realized as a **derived physical route token**, not a stored semantic identity.

Add the RD-09 helper:

```text
encode_live_campaign_route_token(campaign_id: str) -> str
```

Exact v1 algorithm:

```text
C = UTF8(campaign_id)
ROUTE_FRAME =
    UTF8("HDM-LIVE-CAMPAIGN-ROUTE-V1")
    || 0x00
    || U32BE(len(C))
    || C

digest = SHA256(ROUTE_FRAME)
campaign_route_token = "c1-" + lowercase(hex(digest))
```

Properties:

- output is exactly `c1-` plus 64 lowercase hexadecimal characters;
- output is path/ref-component safe and fixed length regardless of `campaign_id` length/content;
- token is deterministic for one canonical campaign identity;
- the token conveys no chronology, priority, authorization, creator identity or currentness;
- token is not sufficient semantic evidence for campaign identity;
- changing the encoding version in a future released contract requires the normal version/compatibility process; v1 clean-slate needs no legacy alias.

The physical WP-11 route becomes conceptually:

```text
live/<encode_live_campaign_route_token(campaign_id)>/<scene_id>/<epoch_id>/LIVE/LIVE_STATE.yaml
```

Do not persist `campaign_route_token` as a second mutable campaign owner merely to avoid recomputation.

---

## 3. Collision / mismatch guard

A SHA-256 route token is a bounded physical locator, not an injective semantic identity. Correctness therefore cannot silently equate token equality with campaign equality.

The repaired v1 `live_scene_state` contract SHALL carry canonical `campaign_id` in the LIVE envelope. `scene_id` and `epoch_id` remain explicit as already required by the selected LIVE source contract.

Every creation, selection and recovery path validates all of:

```text
expected_campaign_id == LIVE_STATE.campaign_id
expected_scene_id    == LIVE_STATE.scene_id
expected_epoch_id    == LIVE_STATE.epoch_id
encode_live_campaign_route_token(LIVE_STATE.campaign_id)
    == physical campaign route token
```

If the physical token resolves to a LIVE source whose body contains a different `campaign_id`, return a typed integrity failure such as:

```text
LIVE_CAMPAIGN_ROUTE_IDENTITY_MISMATCH
```

and stop. Do not overwrite the source, search for a near match, select by branch-name similarity, append a random suffix, rehash with a different implicit algorithm or treat the collision/mismatch as authorization to create a second semantic ID.

The exact failure-code registry placement follows the current native failure owner at execution; the behavior and tests are mandatory even if the literal spelling is normalized to an already-admitted equivalent code.

---

## 4. Campaign identity immutability join

### RD-14 creation side

RD-14 `FrozenCreationEnvelope.campaign_id` is the only campaign identity input to the generator.

`GAME/TOOLS/init_campaign.py` must continue to project that exact value into all admitted scaffold projections that already carry campaign identity, including at least:

- `MANIFEST.yaml.campaign_id`;
- `CAMPAIGN_CARD.yaml.campaign_id`;
- `STATE/CURRENT.yaml.campaign_id` where that projection remains admitted.

Do not generate or persist a separate semantic `campaign_technical_id`.

Extend RD-14 `CreationIdentityTests` / `GeneratorScaffoldTests` to prove exact equality of these projections to the frozen envelope and to prove that the derived physical LIVE token is not written as campaign identity.

### RD-06 ordinary publication side

After initial campaign publication, ordinary campaign publication may update current state but must not rewrite canonical `MANIFEST.campaign_id`.

Extend RD-06 publication validation so a candidate ordinary campaign delta that changes `MANIFEST.campaign_id` is rejected before remote mutation. This is a protected-identity field check, not a new campaign semantic owner.

Add focused `CampaignIdentityImmutabilityTests` to `DEV/TESTS/test_rd06_durability_publication.py` proving:

- unchanged campaign identity is accepted alongside unrelated valid deltas;
- changed `campaign_id` is rejected before Connector plan construction;
- card/current projection drift cannot override MANIFEST campaign identity;
- branch/ref rename or current HEAD movement does not change campaign identity.

### RD-07 recovery side

Selected-LIVE recovery re-resolves canonical campaign identity from the selected current campaign owner, derives the physical route token, loads the exact selected LIVE source, then verifies the body tuple `(campaign_id, scene_id, epoch_id)` before accepting any LIVE owner/currentness evidence.

Add `SelectedLiveCampaignIdentityRecoveryTests` (or exact equivalent group in the RD-07 recovery test module) proving mismatch blocks recovery and no token-only/current-ref fallback is allowed.

---

## 5. Exact RD-09 amendments

RD-09 Task 3 LIVE schema replacement SHALL require `campaign_id` in the v1 LIVE envelope and remove any interpretation where `campaign_branch` or `live_branch` is campaign identity.

RD-09 Task 4 route/currentness selection SHALL use:

```text
campaign_id
-> encode_live_campaign_route_token(campaign_id)
-> exact WP-11 LIVE ref route
-> exact source revision selection/currentness
-> LIVE envelope identity tuple validation
```

RD-09 Task 5 / Finding 24 source-native ID generation SHALL frame semantic `campaign_id`, never `campaign_route_token`.

RD-09 Task 6 frozen publication attempts SHALL carry enough immutable basis to prove the semantic source tuple and exact physical selected ref/revision separately. The ref/revision is the CAS fence; the semantic tuple is identity. One cannot substitute for the other.

Required RD-09 test group:

```text
LiveCampaignRouteIdentityTests
```

It must prove at least:

1. same `campaign_id` deterministically yields the same `c1-<sha256>` token;
2. arbitrary UTF-8 campaign IDs cannot inject `/`, `..`, control characters or ref syntax into the physical token;
3. different route token/body campaign identity is integrity failure;
4. physical ref/revision movement does not alter source-native semantic IDs;
5. source-native ID encoding uses canonical `campaign_id`, not route token;
6. campaign branch name is not accepted as campaign identity;
7. no second persisted semantic `campaign_technical_id` appears in MANIFEST/LIVE identity contracts.

---

## 6. File impact

Mandatory execution-time surfaces, subject to fresh currentness:

```text
RD-09
  MODIFY GAME/TOOLS/live_state.py
  REPLACE/MODIFY GAME/SCHEMA/live_scene.schema.yaml
  MODIFY DEV/SCHEMAS/live-publication-attempt.schema.json
  MODIFY DEV/TESTS/test_rd09_access_live.py

RD-14
  INSPECT/MODIFY GAME/TOOLS/init_campaign.py only if needed to preserve exact projection equality
  MODIFY DEV/TESTS/test_rd14_bootstrap.py
  MODIFY GAME/SCHEMA/campaign_manifest.schema.yaml only to record the accepted initialization-frozen identity invariant if current schema projection still lacks it

RD-06
  MODIFY GAME/TOOLS/publication.py
  MODIFY DEV/TESTS/test_rd06_durability_publication.py

RD-07
  MODIFY GAME/TOOLS/recovery.py
  MODIFY DEV/TESTS/test_rd07_recovery.py
```

If execution currentness shows an exact file rename, route the same owner-local behavior to the current file; do not silently drop the requirement.

No new global identity service, campaign registry, semantic campaign alias table or LIVE coordinator is introduced.

---

## 7. TDD / checkpoint choreography

No future-task RED class may be committed before the task that owns its GREEN.

Recommended coherent order:

```text
RD-14 campaign identity projection proof
+ RD-06 immutable ordinary-publication guard
    -> CAMPAIGN_IDENTITY_READY

RD-09 route-token helper + LIVE envelope identity tuple + corrected F24 ID frame
    -> LIVE_CAMPAIGN_ROUTE_IDENTITY_READY

CAMPAIGN_IDENTITY_READY
+ LIVE_CAMPAIGN_ROUTE_IDENTITY_READY
    JOIN_BEFORE_INTEGRATION
RD-07 selected-LIVE recovery identity proof
```

Every publishable checkpoint obeys the package checkpoint-coherence overlay: focused tests, maintenance audit and full `DEV/TESTS` discovery are GREEN with no pre-created intentional future RED.

---

## 8. Negative stale proof

Implementation/proof fails if any current v1 path permits:

- semantic source-native identity to depend on physical `campaign_route_token` rather than canonical `campaign_id`;
- raw unconstrained `campaign_id` bytes to be inserted directly as the WP-11 Git ref component;
- a second persisted semantic `campaign_technical_id` to drift from MANIFEST campaign identity;
- ordinary campaign publication to rewrite `MANIFEST.campaign_id`;
- LIVE source selection/recovery to trust route-token equality without validating the body campaign identity;
- branch/ref name, exact revision, creator login or card projection to substitute for campaign identity;
- hash/token mismatch to be repaired by random suffix, search or silent alternate routing;
- source-native IDs to change because the physical LIVE ref/revision changes.

---

## 9. Proof routing

Add post-graph proof row `PG25`:

```text
PG25 LIVE campaign semantic identity / physical-route separation
  -> RD-14 exact campaign_id creation propagation
  -> RD-06 post-init campaign_id immutability guard
  -> RD-09 deterministic bounded route token + body tuple validation + corrected source-native ID frame
  -> RD-07 selected-LIVE recovery identity validation
```

Exact witnesses:

```text
RD-14 CreationIdentityTests / GeneratorScaffoldTests campaign-ID cases
RD-06 CampaignIdentityImmutabilityTests
RD-09 LiveCampaignRouteIdentityTests
RD-09 SourceNativeLiveIdEncodingTests corrected campaign-ID cases
RD-07 SelectedLiveCampaignIdentityRecoveryTests
```

Primary channels: `FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO + STATIC_AUDIT`.

---

## 10. Version / migration disposition

This is unreleased v1 clean-slate machine realization. The v1 LIVE schema replacement may include canonical `campaign_id` and the corrected source-key/attempt basis without a compatibility alias for legacy provisional `campaign_technical_id` semantics.

Normal execution-time Version Impact Gate still applies to the local LIVE schema/API generation. Migration execution remains outside the current package; WP-20's preserved campaign-identity law is consumed only as a constraint.

---

## 11. Disposition

```text
AUTHOR_FINDING_25: REPAIRED_IN_PLANNING
SEVERITY: SIGNIFICANT
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```
