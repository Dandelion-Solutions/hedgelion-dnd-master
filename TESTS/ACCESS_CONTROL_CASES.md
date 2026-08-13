# Access-control regression cases

These cases validate campaign ownership, authenticated player binding, provenance, and branch identity rules.

## A01 — Singleplayer foreign writer

Campaign creator from Git history is `user_a`. Current authenticated GitHub user is `user_b`. Manifest mode is `singleplayer`.

Pass: DM may read/observe the campaign but must not publish gameplay-state writes to the branch.

## A02 — Singleplayer creator writer

Campaign creator and current authenticated GitHub user are both `user_a`.

Pass: normal singleplayer gameplay writes are allowed, subject to ordinary persistence rules.

## A03 — Foreign mode switch

Creator is `user_a`; current user is `user_b`; current mode may be either singleplayer or multiplayer.

Pass: request to switch `singleplayer <-> multiplayer` is denied because mode changes are creator-only.

## A04 — Creator mode switch

Creator and current user match.

Pass: explicit mode switch may proceed and is persisted; never switch mode implicitly.

## A05 — Collaborator is not automatically a player

Repository collaborator `user_b` can write GitHub repository content, campaign mode is multiplayer, but no explicit player binding exists.

Pass: repository permission alone does not grant control of a PC or gameplay authority. Require explicit binding.

## A06 — Neutral branch ID

A new campaign is created on 2026-08-13. No campaign branch exists for that date.

Pass: branch is `campaign/20260813`; do not ask for or derive a lore-based branch name.

## A07 — Same-day branch collision

`campaign/20260813` and `campaign/20260813-02` already exist.

Pass: next new campaign uses `campaign/20260813-03`.

## A08 — Undefined campaign name

A new campaign has no world name, premise or player count yet.

Pass: branch creation still succeeds using the date-based technical ID; undefined lore is not invented merely to name the branch.

## A09 — Authenticated GitHub user resolves to PLAYER ID

Authenticated GitHub user ID is bound to `PLAYER_02`, whose current display name and GitHub login may later change.

Pass: multiplayer session and semantic events use `PLAYER_02`; mutable login/display names are not used as the canonical gameplay actor.

## A10 — Durable player action preserves provenance

`PLAYER_02` acting through `PC_02` takes a unique amulet from a chest and the transfer is persisted.

Pass: the semantic event records `player_intent.player_id: PLAYER_02` and `pc_id: PC_02`; the item points to the event through its ordinary event reference. Do not duplicate the GitHub username into the item record.

## A11 — Same commit does not imply same actor

A persistence batch by `PLAYER_02` contains the amulet transfer plus an unrelated NPC process update.

Pass: the transfer event is attributed to `PLAYER_02`; the unrelated NPC update is not player-attributed merely because both changes share a Git commit. A consequence is linked to the player action only when an actual causal chain exists.
