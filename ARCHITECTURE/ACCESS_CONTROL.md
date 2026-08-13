# Access Control and Campaign Ownership

Campaign ownership is derived from Git history and is not duplicated in campaign data.

The campaign creator is `author.login` of the first campaign-specific initialization commit after the branch is created from an engine release.

Before an owner-only operation, resolve:
1. creator login from Git history;
2. currently authenticated GitHub user;
3. allow only if they match.

Owner-only operations include switching `singleplayer <-> multiplayer` and any future access-mode changes explicitly marked owner-only.

In `singleplayer`, the same creator check applies to every gameplay-state write. Other collaborators may read/observe but must not publish gameplay changes, even if repository permissions technically allow push.

In `multiplayer`, repository permission alone is still insufficient: gameplay authority requires explicit player binding. Resolve the authenticated GitHub account's stable user ID to exactly one active `PLAYER_` record before accepting its `player_id` or controlled PC context.

GitHub login is a mutable authorization/audit label. Campaign state and semantic events use stable `PLAYER_` IDs; a login or display-name change must not change gameplay authorship history.

If creator identity, current GitHub identity, or required multiplayer player binding cannot be determined reliably, deny the corresponding write until resolved.
