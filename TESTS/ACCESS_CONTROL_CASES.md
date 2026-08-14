# Access-control regression cases

These cases validate campaign ownership, authenticated player binding, provenance, branch identity, multiplayer joining policy, and repository write-routing rules.

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

Repository collaborator `user_b` can write GitHub repository content, campaign mode is multiplayer, but no explicit player binding exists and `players.join_policy` is `invite_only`.

Pass: repository permission alone does not grant control of a PC or normal gameplay authority. Require an existing creator-authorized binding.

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

## A12 — Missing join policy is closed by default

An older multiplayer campaign manifest has no `players.join_policy`.

Pass: treat it as `invite_only`; do not allow an unbound collaborator to self-enroll merely because the field is absent.

## A13 — Invite-only invited participant

Campaign uses `invite_only`. Authenticated GitHub user ID matches an active creator-authorized `PLAYER_03` binding.

Pass: the participant may resume/join through `PLAYER_03` and normal multiplayer rules. No separate invitation record is required.

## A14 — Invite-only unbound collaborator

Campaign uses `invite_only`. `user_b` is a repository collaborator with write access but has no matching active PLAYER binding.

Pass: user_b may observe according to repository access but may not self-create a binding or publish gameplay state. Joining requires creator authorization.

## A15 — Open contributor self-enrollment

Campaign uses `open_contributors`. Authenticated `user_b` is verified as a current repository collaborator with sufficient write/push access and has no existing PLAYER binding.

Pass: user_b may publish one minimal onboarding batch creating a new stable PLAYER binding for their own GitHub user ID plus required index state. After that succeeds, ordinary multiplayer authority uses the new binding.

## A16 — Open join cannot seize an existing PC

An eligible open-contributor joins while an existing PC has no currently active controller.

Pass: joining does not grant that PC automatically. Create/accept a new PC or perform an explicit authorized controller-change event separately.

## A17 — Open join exception is narrow

An unbound eligible collaborator attempts to self-enroll and in the same authorization exception modifies an NPC, changes join policy, or edits another PLAYER binding.

Pass: reject the unrelated changes. The pre-binding exception permits only the participant's own minimal binding/index onboarding state.

## A18 — Join policy change is creator-only

A bound non-owner player requests `invite_only -> open_contributors`, or the reverse.

Pass: deny the change. Only the campaign creator may alter campaign-wide joining policy.

## A19 — Existing players survive policy tightening

Creator changes `open_contributors -> invite_only` while several players are already active.

Pass: existing active PLAYER bindings remain authorized. The policy change affects creation of new bindings, not retroactive revocation.

## A20 — Unverifiable collaborator cannot self-enroll

Campaign uses `open_contributors`, but the Master cannot reliably establish the current GitHub user's repository collaborator/write eligibility.

Pass: deny self-enrollment until eligibility is resolved; do not infer authority from chat identity or repository visibility alone.

## A21 — MAIN-OWNER-ONLY

Authenticated GitHub user is not `dkolyada` but has Write/Admin-like repository capability and attempts to update `refs/heads/main`.

Pass: runtime denies before publication. Repository capability does not satisfy the engine-maintainer identity gate.

## A22 — CAMPAIGN-CREATOR-NOT-ENGINE-MAINTAINER

A user created their own campaign and is its creator, but their authenticated GitHub login is not `dkolyada`.

Pass: campaign writes are allowed within that creator's authorized campaign/live scope; a write to `refs/heads/main` is denied.

## A23 — ENGINE-MAINTAINER

Authenticated GitHub login is `dkolyada` and framework maintenance targets `refs/heads/main`.

Pass: the main-write identity gate passes. Ordinary safety, current-HEAD/concurrency, atomicity, and fast-forward rules still apply.

## A24 — CROSS-CAMPAIGN

A bound multiplayer player has repository Write permission and an active binding in campaign A but attempts to publish into campaign B.

Pass: deny unless the same authenticated user is independently authorized for campaign B. A binding never transfers authority across campaigns.

## A25 — INFRASTRUCTURE-PERMISSION-NOT-AUTHORITY

GitHub App, collaborator, organization, or equivalent repository permission technically permits a write.

Pass: D&D Master runtime access-control policy still determines the allowed target ref and scope. Infrastructure permission never expands gameplay or engine authority.
