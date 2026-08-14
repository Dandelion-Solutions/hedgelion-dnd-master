# Multiplayer Membership Regression Cases

These cases verify safe leave/removal/reactivation without deleting player identity or creating duplicate characters.

## M01 — Guest leaves voluntarily
A bound non-owner player requests to leave the multiplayer campaign.
Pass: only that player's PLAYER record changes to `status: inactive` with `deactivated_by: self`; normal gameplay authority stops after the durable write succeeds. Do not delete PLAYER/PC/index/provenance records.

## M02 — Guest cannot remove another guest
Bound PLAYER_B attempts to deactivate PLAYER_C.
Pass: deny. A non-owner may deactivate only their own binding.

## M03 — Creator removes a guest
Campaign creator deactivates PLAYER_B.
Pass: persist PLAYER_B as `inactive` with `deactivated_by: creator`; do not delete the stable PLAYER identity or its existing controlled PC links.

## M04 — Creator cannot remove self
Campaign creator also has a PLAYER binding and tries to deactivate that own binding through player-removal flow.
Pass: deny this operation. Creator participation/mode changes use owner-controlled campaign management rather than self-removal.

## M05 — Voluntary leaver rejoins invite-only
PLAYER_B previously left with `deactivated_by: self`; campaign is now `invite_only`; same authenticated GitHub user returns.
Pass: reactivate the same PLAYER_B binding and clear deactivated_by. Reuse existing controlled PC(s); do not create a new PLAYER or PC and do not require a new invitation.

## M06 — Voluntary leaver rejoins open game
Same as M05 but `join_policy: open_contributors`.
Pass: reactivate the same PLAYER/PC identity rather than treating the user as a new open-world participant.

## M07 — Creator-removed player cannot self-bypass
PLAYER_B has `deactivated_by: creator` and campaign uses `open_contributors`; same eligible collaborator attempts to self-enroll again.
Pass: do not create a duplicate PLAYER and do not reactivate automatically. Creator authorization is required.

## M08 — Creator re-invites removed player
Creator authorizes return of creator-deactivated PLAYER_B.
Pass: set the existing PLAYER_B binding to active and clear deactivated_by. Preserve existing PC, preferences and provenance; no replacement character is created.

## M09 — Explicit PC transfer while inactive
PLAYER_B is inactive and PC_B was explicitly reassigned through a canonical controller-change event before B rejoins.
Pass: B's PLAYER binding may reactivate when authorized, but rejoining does not silently reclaim PC_B or create a new PC. Current canonical controller state wins.

## M10 — Live-scene removal freezes old epoch
PLAYER_B participates in active live epoch E1 when creator removes B.
Pass: freeze E1 via `active -> closed`, compact it, persist B's deactivation, then open/adopt any required successor epoch without B as an authorized participant. Do not leave E1 writable after revocation.

## M11 — Removal does not move the PC fictionally
PLAYER_B is removed while PC_B is canonically standing in a tavern with other PCs.
Pass: membership maintenance does not teleport, kill, erase or make voluntary choices for PC_B. The PC remains a world entity in its established fictional state until normal play changes it.

## M12 — Stale non-live chat cannot publish after removal
PLAYER_B's separate chat has stale cached state while creator deactivates B on campaign branch.
Pass: there is no background push/polling requirement, but the next required campaign synchronization/persistence attempt revalidates the changed PLAYER binding and refuses gameplay publication under inactive PLAYER_B.

## M13 — Legacy inactive binding is conservative
An old PLAYER record has `status: inactive` but no deactivated_by field.
Pass: do not allow self-reactivation by assumption. Treat it as requiring creator authorization; after explicit reactivation reuse the same PLAYER/PC identity.
