# Access Control and Campaign Ownership

Campaign ownership is derived from Git history and is not duplicated in campaign data.

The campaign creator is `author.login` of the first campaign-specific initialization commit after the branch is created from an engine release.

Before an owner-only operation, resolve:
1. creator login from Git history;
2. currently authenticated GitHub user;
3. allow only if they match.

Owner-only operations include switching `singleplayer <-> multiplayer`, changing multiplayer joining policy, deactivating/reactivating another player's binding, campaign-wide engine update-policy changes, engine-release integration/migration, and any future access/global-maintenance changes explicitly marked owner-only.

In `singleplayer`, the same creator check applies to every gameplay-state write. Other collaborators may read/observe but must not publish gameplay changes, even if repository permissions technically allow push.

In `multiplayer`, normal gameplay authority requires explicit active player binding. Resolve the authenticated GitHub account's stable user ID to exactly one active `PLAYER_` record before accepting its `player_id` or controlled PC context.

The pre-binding/self-service exceptions are narrow:
- `players.join_policy: open_contributors` permits a verified current collaborator with sufficient write/push access to create the minimal initial `PLAYER_` binding/index state for their own GitHub user ID;
- an inactive player whose binding was voluntarily deactivated with `deactivated_by: self` may reactivate that same binding for the same authenticated GitHub user ID.

Neither exception authorizes control of an existing unrelated PC, edits to another binding, unrelated world changes, or creator-only operations. `invite_only` permits no new self-enrollment; an active creator-authorized binding is the invitation.

A bound non-owner participant may deactivate only their own binding voluntarily. The creator may deactivate another participant, but must not deactivate their own creator/player binding through the membership-removal flow. Creator-deactivated and legacy/unknown inactive bindings require creator reactivation even when the campaign uses `open_contributors`.

Deactivation never physically deletes the PLAYER record or historical PC/provenance links. Reactivation reuses the same stable PLAYER identity and existing PC binding unless an explicit controller-change event changed it while inactive.

Non-owner multiplayer sessions use the engine version already integrated into the campaign. They do not change the campaign-wide engine update policy or integrate a newer release merely because a release tag exists.

GitHub login is a mutable authorization/audit label. Campaign state and semantic events use stable `PLAYER_` IDs; a login or display-name change must not change gameplay authorship history.

If creator identity, current GitHub identity, required multiplayer player binding, or open-join collaborator eligibility cannot be determined reliably, deny the corresponding write until resolved.
