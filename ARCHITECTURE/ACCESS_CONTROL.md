# Access Control and Campaign Ownership

Campaign ownership is derived from Git history and is not duplicated in campaign data.

The campaign creator is `author.login` of the first campaign-specific initialization commit after the branch is created from an engine release.

Before an owner-only operation, resolve:
1. creator login from Git history;
2. currently authenticated GitHub user;
3. allow only if they match.

Owner-only operations include switching `singleplayer <-> multiplayer` and any future access-mode changes explicitly marked owner-only.

In `singleplayer`, the same creator check applies to every gameplay-state write. Other collaborators may read/observe but must not publish gameplay changes, even if repository permissions technically allow push.

In `multiplayer`, repository permission alone is still insufficient: gameplay authority requires explicit player binding. Participants may publish only according to shared-world rules and their bound player/PC context.

If creator identity or current GitHub identity cannot be determined reliably, deny owner-only and singleplayer write operations until resolved.
