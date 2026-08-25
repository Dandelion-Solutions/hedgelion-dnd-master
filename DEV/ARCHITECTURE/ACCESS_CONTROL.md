# Access Control and Campaign Ownership

Repository engine ownership and campaign ownership are separate concepts.

## Repository write authority

Canonical public engine repository: `Dandelion-Solutions/hedgelion-dnd-master`

Framework maintainer GitHub login: `dkolyada`

D&D Master distinguishes repository role before interpreting a default branch:

- In canonical public engine repository, `main` is engine-maintainer-only. Only authenticated GitHub identity `dkolyada` may publish framework/runtime/schema/install/release/repository-policy changes there.
- In campaign storage, default branch is storage-owner-only and may be changed by D&D Master only for storage initialization or baseline metadata maintenance. Storage v2 baseline maintenance does not copy engine files.
- Repository Admin/Write permission, organization membership, collaborator status, campaign ownership, PLAYER binding, or ChatGPT/GitHub authorization do not by themselves grant authority to either kind of default branch.
- A guest Master MUST NOT initialize/fix another owner's storage marker, perform routine owner release maintenance, change storage baseline, or migrate the owner's campaign engine merely because repository writes are technically possible.
- A campaign creator may publish gameplay state only to their own `campaign/*` scope according to campaign rules. Creating a campaign does not grant engine-maintainer or storage-main authority.
- A multiplayer participant may publish only within campaign/live scope authorized by active `PLAYER_` binding.
- GitHub repository permission is necessary infrastructure permission but is insufficient gameplay/engine authorization.
- Campaign engine maintenance is storage-owner maintenance and may apply defined data/schema migrations, but it must preserve campaign agency/canon. A migration requiring creator/player decision is deferred.
- This is D&D Master application/runtime policy, not a claim of server-side GitHub branch protection.

Before any publication, resolve exact repository and target ref, then apply `CORE/RUNTIME.md` write routing. If required identity/repository role cannot be established reliably, deny the write. Never test authority with a probe commit.

## Campaign ownership

Campaign ownership is derived from Git history and is not duplicated in campaign data.

Campaign creator is `author.login` of the first campaign-specific initialization commit after branch creation from storage default branch.

Before an owner-only campaign operation, resolve creator login + current authenticated GitHub user and require equality.

Creator identity is immutable for the campaign. Once authoritatively resolved for an applicable session/authority operation, it may be retained as session-local derived authorization evidence; ordinary gameplay does not reread Git history per turn merely to rediscover the same creator.

Owner-only campaign operations include switching singleplayer/multiplayer, changing join policy, deactivating/reactivating another player's binding, campaign-wide engine update-policy changes, explicit engine or ruleset adoption/migration, persistence of campaign engine/ruleset identity changes, explicit access/global maintenance, and granting/revoking another PLAYER's mechanical-override policy-adoption authority. A non-creator's immediate use of a proven compatible forward same-version runtime under `GAME/CORE/ENGINE_UPDATES.md` is not adoption authority and does not authorize a MANIFEST write.

In singleplayer the creator check applies to every gameplay-state write. Other collaborators may read/observe but not publish gameplay changes.

In multiplayer normal gameplay authority requires explicit active player binding. Resolve authenticated GitHub stable user ID to exactly one active PLAYER record.

The pre-binding/self-service exceptions remain narrow:
- `open_contributors` permits a verified collaborator with sufficient access to create the minimal PLAYER binding/index for their own user ID;
- a voluntarily self-deactivated player may reactivate the same binding for the same authenticated user.

Neither exception authorizes control of another PC/binding, unrelated world changes or creator-only operations. `invite_only` permits no new self-enrollment.

Deactivation never deletes canonical PLAYER/provenance. Reactivation reuses the same stable PLAYER identity and existing PC binding unless explicitly reassigned.

GitHub login is mutable authorization/audit metadata; campaign semantic actor identity is stable PLAYER ID.

## Campaign House-Rules policy adoption authority

Policy adoption is semantic campaign authority and is distinct from technical repository permission, normal gameplay mutation authority, or the Master's right to make a one-off situational adjudication.

Two adoption authority classes are admitted:

```text
INTERPRETIVE_POLICY
MECHANICAL_OVERRIDE_POLICY
```

### INTERPRETIVE_POLICY

In multiplayer, every currently active PLAYER has `INTERPRETIVE_POLICY` adoption authority by default after authenticated identity resolves to that active PLAYER. No stored interpretive-policy grant is required.

An inactive or unbound PLAYER has no such authority. Repository collaborator/Write/Admin capability alone does not create it.

In singleplayer, the inherited creator-only gameplay publication rule remains the effective publication boundary.

### MECHANICAL_OVERRIDE_POLICY

The campaign creator has `MECHANICAL_OVERRIDE_POLICY` adoption authority by creator identity.

A non-creator may adopt `MECHANICAL_OVERRIDE_POLICY` only when all of these hold:

```text
current authenticated principal
    -> exactly one current active PLAYER
    -> PLAYER.policy_authority.mechanical_override_policy == true
```

Missing/null `mechanical_override_policy` is false for a non-creator.

Only the campaign creator may grant or revoke this PLAYER field. A participant cannot self-grant it, cannot gain it from repository permission, and cannot infer it from having previously made an interpretive ruling.

Grant/revoke is prospective access-control state. Existing accepted Resolution generations and already-established historical consequences are not reinterpreted when the grant later changes.

Neither policy authority class bypasses information eligibility, deterministic realization, RNG integrity, native owner validation, currentness, CAS, or any other constitutional runtime boundary.

The structured House-Rules policy sidecar records adoption basis/provenance/current policy identity; it is not a new ACL subsystem. Existing identity resolution and publication/CAS enforce the selected semantic authority.

If creator/current identity/player binding/open-join/policy-adoption eligibility cannot be determined reliably, deny the corresponding write until resolved.
