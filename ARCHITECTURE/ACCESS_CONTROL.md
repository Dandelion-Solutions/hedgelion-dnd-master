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

Owner-only campaign operations include switching singleplayer/multiplayer, changing join policy, deactivating/reactivating another player's binding, campaign-wide engine update-policy changes, engine migration, and explicit access/global maintenance.

In singleplayer the creator check applies to every gameplay-state write. Other collaborators may read/observe but not publish gameplay changes.

In multiplayer normal gameplay authority requires explicit active player binding. Resolve authenticated GitHub stable user ID to exactly one active PLAYER record.

The pre-binding/self-service exceptions remain narrow:
- `open_contributors` permits a verified collaborator with sufficient access to create the minimal PLAYER binding/index for their own user ID;
- a voluntarily self-deactivated player may reactivate the same binding for the same authenticated user.

Neither exception authorizes control of another PC/binding, unrelated world changes or creator-only operations. `invite_only` permits no new self-enrollment.

Deactivation never deletes canonical PLAYER/provenance. Reactivation reuses the same stable PLAYER identity and existing PC binding unless explicitly reassigned.

GitHub login is mutable authorization/audit metadata; campaign semantic actor identity is stable PLAYER ID.

If creator/current identity/player binding/open-join eligibility cannot be determined reliably, deny corresponding write until resolved.
