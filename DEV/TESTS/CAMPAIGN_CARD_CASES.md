# Campaign Card / Fast Menu Regression Cases

## C01 — New campaign has card
Generator creates a new campaign.
Pass: branch root contains CAMPAIGN_CARD.yaml with campaign_id, mode, initializing status, semantic engine version and cached creator login.

## C02 — Singleplayer has no participant list
Singleplayer card exists.
Pass: protagonist object is present; multiplayer is null; no participant_github_logins list is stored.

## C03 — Multiplayer card
Multiplayer card exists.
Pass: protagonist is null; multiplayer contains join_policy + active participant_github_logins.

## C04 — Card-first menu
Fresh chat discovers several current-layout campaigns with valid cards.
Pass: one small card read per branch is sufficient for menu rendering; do not read MANIFEST/STATE/WORLD/PC/PLAYER merely for the menu.

## C05 — Legacy fallback
Campaign has no card.
Pass: fall back to root/legacy MANIFEST for minimal menu entry; do not open deeper campaign state just to synthesize card fields.

## C06 — No implicit resume
Exactly one valid campaign card exists and user says `давай сыграем`.
Pass: still show that campaign plus `Начать новую игру`; do not auto-select.

## C07 — Active own singleplayer
Card says active singleplayer and creator login == authenticated login.
Pass: render 🟢 with protagonist + role/race + location + active status.

## C08 — Locked foreign singleplayer
Readable singleplayer card has creator login != authenticated login.
Pass: render 🔒 and indicate singleplayer/read-only; selecting it still performs authoritative creator check before any write.

## C09 — Joinable multiplayer
Multiplayer card is active, current login not in participants, join_policy=open_contributors.
Pass: render 👀 with `можно присоединиться`; actual collaborator/write eligibility is verified only after selection.

## C10 — Invite-only multiplayer
Multiplayer card is active, current login not in participants, join_policy=invite_only.
Pass: render 👀 with `присоединение по приглашению`; do not imply self-enrollment.

## C11 — Existing multiplayer participant
Current login is in active participant list.
Pass: active campaign may render 🟢 subject to normal authoritative PLAYER revalidation after selection.

## C12 — Paused/initializing
Authorized candidate is paused or initializing.
Pass: render 🟡 and label paused/unfinished setup.

## C13 — Completed campaign
Card status completed, note `погиб`.
Pass: render 🟥 and human text `завершена: погиб`; do not silently resume it.

## C14 — Archived hidden by default
Card status archived.
Pass: omit from normal menu unless user explicitly requests archived games.

## C15 — Card mismatch cannot grant authority
Card claims current login is creator/participant but authoritative Git provenance or PLAYER binding disagrees after selection.
Pass: deny unauthorized write; source records win; card is merely stale/suspect display cache.

## C16 — Card joins existing transaction
PC/location/status/engine/membership change creates a normal durable campaign transaction.
Pass: updated CAMPAIGN_CARD is included in the same tree/commit; no separate card-only commit.

## C17 — Soft location update does not force save
Current focal location changes during SOFT dirty play without persistence boundary.
Pass: mark card projection dirty in memory; do not create a GitHub call solely for menu freshness.

## C18 — Legacy backfill is opportunistic
Selected old campaign has no card; authoritative PC/location/access records are naturally loaded.
Pass: build card and include it in the next normal coherent save/maintenance transaction; do not run a pre-selection deep scan.

## C19 — Engine card is display only
Card says engine_version 0.5 but MANIFEST exact integrated tag/SHA differs or requires another package.
Pass: after selection MANIFEST provenance wins; card cannot select or authorize engine migration.

## C20 — Completion is explicit
PC dies but campaign authority has not concluded the campaign.
Pass: do not automatically set card/manifest status completed. Completion is a separate campaign lifecycle decision.

## C21 — Menu is always N+1 numbered
Three visible campaigns exist.
Pass: render explicit options `1`, `2`, `3` for those campaigns and exactly one final `4. ➕ Начать новую игру`; a reply `2` selects only the second item from that shown menu.

## C22 — One campaign keeps the same numbered UI
Exactly one visible campaign exists.
Pass: render `1. <campaign>` and `2. ➕ Начать новую игру`; do not switch to an unnumbered special case.

## C23 — Natural language remains valid
Numbered menu is visible.
Pass: `новая игра`, an unambiguous campaign name/protagonist reference, or another unambiguous natural-language choice works without requiring the number.

## C24 — Bare continue is not guessed with several games
Several plausible continuable campaigns are visible and user says only `продолжить`.
Pass: ask for number/name; do not choose by recency/order. With exactly one continuable campaign the same phrase may select that one.

## C25 — Menu number is never canon
User selected campaign by number 3.
Pass: use the number only to resolve the current UI choice; never persist `3` as campaign identity, branch metadata, card state, log fact or PLAYER state.
