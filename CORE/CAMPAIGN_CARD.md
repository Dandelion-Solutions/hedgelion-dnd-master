# Campaign Card and Fast Campaign Menu

framework_module_version: 0.1.2
load_when: campaign discovery/menu, campaign setup, campaign status/location/PC/membership/engine changes, persistence affecting card projection fields

## Purpose

`CAMPAIGN_CARD.yaml` is a tiny branch-root projection used to render a useful campaign menu without opening STATE/WORLD/PC/PLAYER records.

It is NOT a new source of canon or access authority. Its job is speed and presentation.

Current-layout path: `CAMPAIGN_CARD.yaml`.
Legacy-layout path when backfilled: `CAMPAIGN/CAMPAIGN_CARD.yaml`.

## Menu fields

The card carries only compact human-facing state:
- protagonist name and role/race summary for singleplayer;
- current focal location label;
- campaign mode;
- status + optional short status note;
- human engine version;
- campaign name when available;
- cached creator GitHub login for singleplayer menu lock hints;
- for multiplayer only: join policy and active participant GitHub login labels.

Do not store participant login lists in singleplayer cards.

## Projection, not authority

Authoritative sources remain:
- MANIFEST for mode/status/engine provenance/join policy;
- PC/PLAYER records for characters and multiplayer bindings;
- STATE/SCENE/WORLD for current location;
- Git provenance + PLAYER binding rules for actual write authority.

A stale or tampered card must never grant gameplay authority, migrate an engine, alter canon or override those records.

After the user selects a campaign, perform the normal authoritative verification. If loaded source records disagree with the card, trust the source records and refresh the card at the next allowed coherent campaign transaction.

## Fast menu read path

For each `campaign/*` branch during new-chat discovery:
1. probe root `CAMPAIGN_CARD.yaml`;
2. if absent, probe legacy `CAMPAIGN/CAMPAIGN_CARD.yaml`;
3. if a valid card exists, use it to render the menu and DO NOT read MANIFEST merely for menu presentation;
4. if no card exists, use the legacy manifest-only fallback; do not open PC/STATE/WORLD just to manufacture a pretty menu.

A legacy campaign without a card may be backfilled only after it is explicitly selected and the required authoritative records are naturally loaded. Backfill joins the next normal campaign transaction; do not create a special menu-only commit unless the user explicitly requests maintenance.

## Numbered choice contract

Whenever one or more visible campaigns are presented as a choice, render one explicit ordered menu:
- campaigns are numbered `1..N` in displayed order;
- the final option is always `N+1. ➕ Начать новую игру`;
- even when `N == 1`, show both `1.` and `2.` rather than switching to an unnumbered layout;
- do not use unnumbered bullets as the primary campaign-choice interface.

A displayed number is only an ephemeral alias for that exact menu. Never store it in MANIFEST, CAMPAIGN_CARD, branch names, logs, PLAYER records or campaign canon.

Accept either:
- the displayed number;
- an unambiguous campaign name/branch/protagonist reference;
- an unambiguous natural-language intent such as `новая игра`.

With exactly one continuable campaign, a bare `продолжить` is unambiguous and may select it. With multiple plausible campaigns, bare `продолжить` is ambiguous: ask for the number/name rather than guessing.

## Emoji/menu semantics

Use one primary emoji per row.

Priority:
1. `completed` -> 🟥.
2. singleplayer where cached creator login is known and differs from current authenticated GitHub login -> 🔒.
3. multiplayer where current login is not in cached active participant logins -> 👀.
4. `paused` or `initializing` -> 🟡.
5. active authorized/participant candidate -> 🟢.

`archived` stays out of the normal new-chat menu unless the user asks to show archived campaigns; when shown it may use 🟥.

The icons are presentation hints, not authorization decisions.

Recommended concise Russian menu:
- `1. 🟢 Джон Вольт — Человек, маг — Таверна "Пьяная кружка" — активная`
- `2. 🟥 Бобби Ли — Воин — Поле "Злая пустошь" — завершена: погиб`
- `3. 🔒 Элиас — Эльф, следопыт — Северная дорога — одиночная, только просмотр`
- `4. 👀 Рыночная площадь — активная, присоединение по приглашению`
- `5. ➕ Начать новую игру`

For multiplayer `open_contributors`, an unbound row may say `можно присоединиться`; for `invite_only`, use `присоединение по приглашению`.

Do not list all participant logins in the normal player-facing menu unless useful or requested; they exist primarily to classify the current user cheaply.

## Status semantics

Supported card/manifest lifecycle:
- `initializing` — setup not finished;
- `active` — ongoing play;
- `paused` — intentionally paused;
- `completed` — story/campaign ended; `status_note` may summarize why;
- `archived` — retained but hidden from normal menu.

A PC death does not automatically complete a campaign. Mark `completed` only when the campaign is actually concluded under normal campaign authority.

## Keeping the card fresh

Whenever a durable transition changes any projected field, mark the card dirty too and publish it inside the SAME `CAMPAIGN_TREE_TXN` as the authoritative records.

Typical projected changes:
- accepted/changed protagonist identity or role/race summary;
- durable current focal-location change;
- mode/status/campaign-name transition;
- engine migration;
- multiplayer join-policy change;
- PLAYER binding activation/deactivation/reactivation or GitHub-login refresh.

### Singleplayer save-boundary semantics

For singleplayer, the card is also used to define a small number of natural persistence boundaries under `DURABILITY_GUARD.md`.

These projected changes normally create a boundary:
- protagonist becomes established/changes materially;
- `current_location` is first established for live play or changes to a new human-facing focal location;
- lifecycle status changes (`initializing -> active`, pause, completed, archived/reactivated).

At such a boundary, do NOT publish a card-only commit. Publish the authoritative source transition + card projection + all accumulated valid SOFT campaign dirty state in ONE coherent transaction.

`current_location` is intentionally coarse. It should name the location useful in the campaign menu, not tactical movement inside the same place. A move from tavern to market square may change it; moving between tables in the same tavern normally does not.

Other card freshness changes that arise only as maintenance/projection cleanup do not automatically justify a special gameplay commit unless another rule creates a boundary.

For multiplayer, publication timing follows shared-world/membership/live synchronization policy; do not delay a material shared change merely to imitate the sparse singleplayer cadence.

For multiplayer `participant_github_logins`, include active PLAYER bindings only. Login labels are mutable conveniences; stable GitHub user IDs in PLAYER records remain the authorization binding.
