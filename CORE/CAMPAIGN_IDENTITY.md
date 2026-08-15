# Evolving Campaign Identity and README Projection

framework_module_version: 0.1.1
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: authoritative for automatic campaign naming, campaign-name provenance, CAMPAIGN_CARD name projection, and the dynamic overview block in campaign README

## Purpose

A campaign title should behave like the title of a book, not like a caption for the current paragraph.

At campaign creation there may be too little information to name the game well. `MANIFEST.campaign_name: null` is therefore a healthy state. As the protagonist/party and broad surrounding world become clear, a concise literary title may crystallize naturally; later, accumulated history may justify changing an automatically generated title.

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

## First useful automatic title

The initial title does NOT need a completed plot, major villain or long history. It needs enough broad identity to say what kind of book/game this is.

A particularly useful early pattern is a concise literary **hero/party + world/premise** formulation after BOTH sides are durably known, for example:

`Эмо-вампир в мире розовых пони и радужных единорогов`

This is a good campaign-level title because it describes the durable protagonist/world contrast rather than the current signpost, room, NPC conversation or quest step.

The first automatic title may therefore crystallize at an already-required `PROVISIONAL_IDENTITY`, character-stage or PLAY_READY transaction when:
- protagonist/party identity or concept is stable enough to represent the game; AND
- the broad surrounding world/premise is stable enough to represent more than one local scene.

If only one side is known, keep the title null. Do not invent a world merely to fill the title.

Prefer short titles/phrases. The title does not need to be a three-paragraph synopsis, and it should not mechanically concatenate database fields. Write it as a natural book/game title in the campaign language.

## Later title evolution

An automatically generated title is allowed to evolve because the meaning of a long campaign may become clearer with history.

Reconsider an `auto` title only when accumulated durable canon changes the campaign-level identity materially, such as:
- a previously provisional premise becomes something substantially different;
- a recurring central conflict/theme eclipses the broad opening premise;
- the protagonist/party composition changes fundamentally;
- a major arc reveals what the campaign is really about;
- completion gives the whole story a better retrospective title.

The title should remain reasonable if the current scene is removed from consideration.

An existing automatic title is sticky. Do not churn it for synonyms, every quest, every location or every session.

## Automatic title cadence

Automatic title synthesis is opportunistic and low-frequency.

Evaluate title creation/revision only at an ALREADY-EXISTING durable boundary that is already writing campaign state, for example:
- PROVISIONAL_IDENTITY when hero + broad world are both now established;
- character/PLAY_READY launch;
- explicit save after substantial development;
- session pause/end;
- major arc/campaign-level transition;
- campaign completion.

Do not create a standalone GitHub transaction merely to invent or polish a title.

## README as a living book jacket

Campaign `README.md` has two conceptual parts:
1. a small **dynamic campaign overview** — title + compact annotation that may evolve with the game;
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

The annotation should be compact: normally one short sentence or a small paragraph. It may simply restate/expand the broad campaign premise when that is already expressive enough. Do not force several paragraphs of prose just because README supports Markdown.

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
