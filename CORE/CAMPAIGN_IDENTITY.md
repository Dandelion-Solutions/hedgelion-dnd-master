# Evolving Campaign Identity and README Projection

framework_module_version: 0.2.0
load_when: campaign title creation/change, README overview refresh, campaign-card name repair, or a persistence boundary where broad campaign identity materially changed
precedence: authoritative for automatic campaign naming, name provenance, CAMPAIGN_CARD name projection, and the mutable campaign README overview

## Authority

`MANIFEST.campaign_name` is authoritative. `CAMPAIGN_CARD.campaign_name` is an exact projection, including null.

Optional `MANIFEST.campaign_name_origin`:
- `auto`: Master-generated; may evolve under this module;
- `player`: explicitly player-named; automatic renaming is disabled until the player delegates naming again;
- null/absent: unknown provenance. A legacy non-null name is treated as sticky/manual; a null name is eligible for automatic naming.

Never repair MANIFEST from a stale card. Repair card from MANIFEST in the next allowed coherent transaction.

## First useful title

A new campaign may remain unnamed. Do not ask the player merely to fill a title field.

An automatic title may first crystallize inside an already-required setup/persistence transaction once BOTH are durably clear:
1. protagonist/party identity or concept;
2. the broad surrounding world/premise beyond one local scene.

A useful early form is a short literary **hero/party + world/premise** phrase, for example:

`Эмо-вампир в мире розовых пони и радужных единорогов`

Do not title the campaign after the current room, signpost, NPC conversation or quest step. The title should still make sense if the current scene is removed.

## Later evolution

An `auto` title is sticky but may change when accumulated durable history materially changes the campaign-level identity: a defining conflict/theme emerges, the party changes fundamentally, a major arc reframes the story, or completion suggests a better retrospective title.

Do not churn titles for synonyms, ordinary quests, locations or sessions. Never create a standalone GitHub commit only to polish a title.

## README as a living book jacket

Current campaign README uses exactly these protected regions:
- `<!-- DND_MASTER:CAMPAIGN_OVERVIEW_BEGIN -->` ... `<!-- DND_MASTER:CAMPAIGN_OVERVIEW_END -->` — mutable overview;
- `<!-- DND_MASTER:PLAYER_GUIDE_BEGIN -->` ... `<!-- DND_MASTER:PLAYER_GUIDE_END -->` — static player guide.

Routine gameplay may rewrite only bytes inside the overview region. Everything outside it must be inherited byte-for-byte from the base tree. If a legacy README has no markers, leave it untouched during ordinary play; marker installation is maintenance/migration.

The overview normally contains the authoritative title (or generic `# D&D Campaign` while null) and one short sentence/small paragraph describing the campaign as a whole so far. Use only established player-visible durable facts. Do not leak secrets/future plans and do not turn the overview into a transcript of the latest scene.

README and card are projections, never sole canon authority. A fact mentioned there must still live in its normal authoritative records when persistence requires it.