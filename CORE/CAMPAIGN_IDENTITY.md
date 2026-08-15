# Evolving Campaign Identity and README Projection

framework_module_version: 0.1.0
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: authoritative for automatic campaign naming, campaign-name provenance, CAMPAIGN_CARD name projection, and the dynamic overview block in campaign README

## Purpose

A campaign title should behave like the title of a book, not like a caption for the current paragraph.

At campaign creation there may be too little information to name the game well. `MANIFEST.campaign_name: null` is therefore a healthy state. As durable characters, setting, conflicts, themes and history accumulate, the Master may let a useful title and short README annotation crystallize from the campaign as a whole.

This feature is presentation metadata. It must never delay play, force a naming questionnaire, or become a substitute for normal canon records.

## Authoritative name and provenance

`MANIFEST.campaign_name` is the authoritative campaign title.

`MANIFEST.campaign_name_origin` is optional provenance:
- `auto` — the Master synthesized the current title and may later improve it under this module;
- `player` — the player explicitly named/renamed the campaign; automatic renaming is disabled until the player clearly delegates naming again;
- `null`/absent — no provenance is known.

Backward compatibility is conservative:
- null/absent origin + null name is eligible for automatic naming;
- null/absent origin + non-null name is treated as sticky/manual for automatic-renaming purposes. Do not silently rewrite an older campaign name whose provenance is unknown.

When the player explicitly supplies or corrects the campaign title, store that title and `campaign_name_origin: player`. If the player later says to name/rename it automatically, automatic synthesis may resume and set origin to `auto`.

## CAMPAIGN_CARD consistency

`CAMPAIGN_CARD.campaign_name` is an exact projection of `MANIFEST.campaign_name` or null.

The card MUST NOT invent a campaign name independently. If a transaction changes the authoritative name, update MANIFEST and CAMPAIGN_CARD in the SAME campaign transaction.

A card title that differs from MANIFEST is a projection defect. Repair the card from MANIFEST; never repair MANIFEST from the card.

## When an automatic title may crystallize

Do not name a campaign just because one vivid scene exists.

A useful automatic title normally reflects durable identity across more than one dimension, such as:
- protagonist or party identity;
- central premise or enduring contrast;
- recurring setting/region/culture;
- major long-running conflict, faction or objective;
- accumulated theme/tone that has actually emerged in play;
- a completed arc that has become defining for the campaign.

The title should remain reasonable if the current scene is removed from consideration.

Early states are allowed to remain unnamed. A name like `Грым и розовая пони у указателя` is too page-local if the campaign is only beginning and that encounter is not known to define the whole game.

`PLAY_READY` is the earliest normal opportunity for automatic naming, not a requirement to name. If the available evidence is still thin, keep null.

## Automatic title cadence

Automatic title synthesis is opportunistic and low-frequency.

Evaluate whether the title has become materially clearer only at an ALREADY-EXISTING durable boundary where campaign identity has changed enough to justify the thought, for example:
- PLAY_READY / first real launch;
- explicit save after substantial development;
- session pause/end;
- major arc or campaign-level transition;
- campaign completion;
- another transaction already touching broad campaign identity.

Do not create a standalone GitHub transaction merely to invent or polish a title.

An existing automatic title is sticky. Rename it only when accumulated durable history makes another title materially more representative of the campaign as a whole. Do not churn titles for synonyms, every quest, every location, or every session.

## README as a living book jacket

Campaign `README.md` has two conceptual parts:
1. a small **dynamic campaign overview** — title + short annotation that may evolve with the game;
2. a **static player guide** copied from the engine template and protected from ordinary gameplay persistence.

For current-layout campaigns the template marks them with:
- `<!-- DND_MASTER:CAMPAIGN_OVERVIEW_BEGIN -->`
- `<!-- DND_MASTER:CAMPAIGN_OVERVIEW_END -->`
- `<!-- DND_MASTER:PLAYER_GUIDE_BEGIN -->`
- `<!-- DND_MASTER:PLAYER_GUIDE_END -->`

Routine gameplay may rewrite ONLY the bytes between the overview begin/end markers.

The player-guide block, its markers, and all content outside the overview block MUST remain byte-for-byte inherited from the known base tree during ordinary saves. Engine migration/maintenance may update the guide only when that maintenance operation explicitly owns the template migration.

If a legacy README has no overview markers, ordinary gameplay MUST NOT heuristically chop/rebuild it. Leave it untouched. Marker installation belongs to an explicit compatible migration/maintenance path, not a normal save.

## Overview content

The overview is a human-facing projection, not canon authority.

When the campaign name is null, the H1 may remain a generic `# D&D Campaign`. Once an authoritative name exists, the overview H1 should normally show it.

The annotation should be concise (normally 1–3 short paragraphs) and describe the campaign as a whole so far: protagonist/party, durable premise, central developed tension, and broad tone when useful.

Use only established player-visible durable facts. Do not leak unrevealed secrets, hidden NPC motives, future plans, GM notes or speculative outcomes into README.

Do not make the annotation a transcript of the latest scene. It should read like a current book-jacket synopsis and may evolve as the story develops.

## README update cadence

The synopsis may evolve somewhat more often than the title, but it still should not rewrite on every save.

Update the overview only when an existing campaign transaction is already happening AND the accumulated story makes the current overview materially stale or empty. Do not create a standalone commit just to rephrase the synopsis.

If the title changes automatically/manually, update the README overview in that same transaction when markers exist.

If only the annotation changes, MANIFEST/CAMPAIGN_CARD do not need to change unless another projected field changed.

## Projection is not canon

README and CAMPAIGN_CARD must never become the only place where a durable campaign fact exists.

A synopsis sentence about a companion, faction, location, objective or event is supplementary. The normal authoritative entity/state/index/log records must already represent the fact when persistence rules require it.

README may summarize; it may not rescue an incomplete save.
