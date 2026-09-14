# HDM Implementation Planning — Manifest Player Registry Retirement Amendment

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / INDEPENDENTLY UNCONFIRMED**
Date: 2026-09-14
Finding: **AUTHOR FINDING 48 — SIGNIFICANT**
Production implementation: **NO**.

This later-precedence amendment removes a stale duplicate multiplayer-membership surface from the retained campaign manifest contract. It does not change accepted PLAYER authority, collaboration semantics, campaign-contract generation, storage generation, catalog generation or engine release identity.

## 1. Finding

The retained `GAME/SCHEMA/campaign_manifest.schema.yaml` currently admits:

```yaml
players:
  join_policy: invite_only | open_contributors
  player_ids: [string, ...]
```

and the shipped blank `GAME/CAMPAIGN/MANIFEST.yaml` initializes `players.player_ids: []`.

However, the current accepted multiplayer architecture makes exact current native PLAYER state the membership/authorization owner:

```text
authenticated principal
  -> exact active PLAYER binding
  -> current authorization / role / participation state
```

`GAME/CORE/MULTIPLAYER.md` explicitly requires authorization through current PLAYER bindings rather than repository collaboration or a global membership list. RD-09 and its principal-routing amendment bind access transitions to exact current PLAYER state; RD-12 binds collaboration obligations to current PLAYER authority; RD-14 consumes those owner contracts for onboarding and owns no separate membership/currentness authority.

The campaign generator `GAME/TOOLS/init_campaign.py` only copies the blank manifest and does not populate or maintain `players.player_ids`. `GAME/CORE/CAMPAIGN_SETUP.md` initializes `players.join_policy` but does not define a producer, same-closure mutation rule, recovery rule or consumer for `players.player_ids`.

Therefore `players.player_ids` is neither:

- current membership/authorization authority;
- a completeness-protected derivative companion;
- a bounded menu projection with an admitted producer/currentness law;
- nor required by a current consumer.

Leaving it in a canonical persistent manifest creates a writable-looking duplicate registry whose bytes can diverge indefinitely from the real PLAYER owner. A future worker or consumer could legally-lookingly rely on stale membership state despite the accepted single-owner law.

## 2. Required v1 disposition

Retire the duplicate field instead of creating another synchronized registry.

Final v1 campaign-manifest contract:

```yaml
players:
  join_policy: invite_only | open_contributors
```

`players.join_policy` remains campaign policy. `players.player_ids` does not survive as authority, cache, compatibility alias, recovery hint or menu projection.

The current owner/projection split remains:

```text
world.player / exact active PLAYER binding
  = current membership, authorization and participant authority

CAMPAIGN_CARD.multiplayer.participant_github_logins
  = bounded non-authoritative human-facing projection maintained by the accepted membership closure

MANIFEST.players.join_policy
  = enrollment policy

MANIFEST.players.player_ids
  = RETIRED
```

Do not replace the retired field with another manifest-level ID list.

## 3. Implementation joins

The later implementation worker must integrate this repair into the existing owner checkpoints rather than create a new membership service.

### RD-09 / RD-12

PLAYER access/membership transitions continue to mutate exact current PLAYER state and all already-required principal/collaboration companions. They MUST NOT write `MANIFEST.players.player_ids`.

### RD-14 / campaign generation

At the coherent campaign-manifest/scaffold checkpoint:

- remove `players.player_ids` from `GAME/SCHEMA/campaign_manifest.schema.yaml`;
- remove the blank `player_ids: []` member from `GAME/CAMPAIGN/MANIFEST.yaml` and any generated/template equivalent;
- ensure `GAME/TOOLS/init_campaign.py` emits no such member;
- preserve `players.join_policy`;
- preserve the existing same-membership-closure update of the non-authoritative campaign-card participant-login projection where applicable.

No bootstrap path may seed membership by writing the retired manifest list.

## 4. Local schema-version cutover

`campaign_manifest.schema.yaml` is a retained serialized contract currently at local `schema_version: 4`.

Removing an admitted field from the strict persistent contract is an incompatible local-shape change under the canonical versioning policy. The final v1 target is therefore:

```text
campaign_manifest.schema_version: 4 -> 5
```

The final RD-14 campaign-manifest/scaffold integration checkpoint is the single bump writer. The schema change and all shipped/generated/template manifest bytes must cut over coherently.

This later-precedence amendment extends F43's deterministic retained-schema matrix from **10 to 11** rows. `RetainedSchemaVersionCutoverTests` must also prove final `campaign_manifest` v5 bytes and absence of the retired member.

Because current HDM v1 is clean-slate/pre-release, this local cutover introduces:

```text
migration edge: NO
dual-read support: NO
legacy player_ids alias: NO
campaign_contract_generation bump solely for this pre-release cutover: NO
catalog/storage/engine version bump: NO
```

Those namespaces remain independently governed.

## 5. Required proof

The final package needs exact proof that:

1. strict campaign-manifest schema target is v5;
2. `players.join_policy` remains valid;
3. `players.player_ids` is absent from the final strict schema and blank/generated manifest;
4. campaign generation does not synthesize or preserve the retired field;
5. authorization/membership decisions read exact current PLAYER authority, not a manifest list;
6. active -> inactive -> rejoin flows update PLAYER state and required accepted projections/companions without a manifest membership write;
7. recovery/currentness logic does not consult the retired field;
8. `CAMPAIGN_CARD.multiplayer.participant_github_logins`, where present, remains explicitly non-authoritative and is maintained only under its already-accepted membership projection law;
9. the F43 package version witness now covers eleven retained schema cutovers and rejects a final mixed state with campaign-manifest v4 or surviving `player_ids`.

Owner-local RD-09/RD-12/RD-14 tests remain the primary semantic witnesses. The package version-cutover witness proves retained-contract identity/currentness and cannot substitute for those owner tests.

## 6. Graph consequence

This repair removes a false node rather than adding a new synchronization edge:

```text
MANIFEST.players.player_ids --X--> current membership authority
MANIFEST.players.player_ids --X--> recovery/currentness source
MANIFEST.players.player_ids --X--> required menu projection

exact current PLAYER authority
  -> existing principal / collaboration / campaign-card projection joins

RD14 final campaign-manifest/scaffold GREEN
  + campaign_manifest v5
  -> RETAINED_SCHEMA_VERSION_CUTOVER_PROOF_READY
```

No new cross-RD semantic cycle is introduced.

## 7. Finding disposition

```text
AUTHOR_FINDING_48: SIGNIFICANT
ROOT_CAUSE: retained canonical manifest exposed an unowned duplicate player registry with no producer/currentness/recovery/consumer law after PLAYER became the sole current membership authority
REPAIR: retire MANIFEST.players.player_ids; preserve join_policy; extend retained-schema cutover matrix with campaign_manifest 4->5
NEW_MEMBERSHIP_AUTHORITY: NO
NEW_DERIVATIVE_COMPANION: NO
MIGRATION_OR_COMPATIBILITY_DEBT: NO
ARCHITECTURE_REOPEN: NO
HUMAN_PRODUCT_DECISION_REQUIRED: NO
REPAIR_STATE: PLANNED IN THIS MANDATORY AMENDMENT
INDEPENDENT_CONFIRMATION: PENDING
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
