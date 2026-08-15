# Campaign Identity Regression Cases

These cases protect evolving book-like campaign naming, strict MANIFEST/card consistency, and the dynamic README overview without allowing gameplay saves to rewrite the static player guide.

## CI01 — Empty title is healthy at scaffold time
A new campaign has only the generated scaffold and almost no story identity.
Pass: `MANIFEST.campaign_name` and `CAMPAIGN_CARD.campaign_name` may remain null. Do not ask the player to name the campaign merely to fill the field.

## CI02 — Current scene is not the campaign title
The only concrete fiction so far is that Грым is talking to a pink pony beside a signpost.
Pass: do not automatically title the entire campaign after that one page-local interaction merely because it is vivid.

## CI03 — Title crystallizes from cumulative identity
Durable play has established a protagonist, recurring setting/premise and a broader campaign-level contrast or conflict.
Pass: at an already-existing persistence boundary, the Master may synthesize a concise title representing the campaign as a whole and store it in MANIFEST with `campaign_name_origin: auto`.

## CI04 — Card never invents a name
MANIFEST title is null but the runtime thinks of a catchy title for menu presentation.
Pass: card remains null until MANIFEST is changed. If MANIFEST changes, the same transaction updates card to the exact same string.

## CI05 — Automatic title may evolve, but is sticky
An auto title exists. A new room, NPC or ordinary quest appears.
Pass: keep the title. Rename only when accumulated durable history materially changes what best represents the whole campaign.

## CI06 — Player title is sticky
Player explicitly names/renames the campaign.
Pass: store `campaign_name_origin: player`; automatic synthesis must not overwrite it until the player clearly delegates naming again.

## CI07 — Unknown legacy provenance is conservative
Older campaign has non-null `campaign_name` but no `campaign_name_origin`.
Pass: treat the existing title as sticky/manual for auto-renaming purposes. Do not silently rename it.

## CI08 — README overview is a living annotation
Current README has the overview markers and the story has materially developed since its last synopsis.
Pass: during an already-required campaign transaction, the Master may rewrite only the overview block with a concise player-visible book-jacket synopsis based on durable canon.

## CI09 — Static README guide is byte-preserved
Explicit save touches PC/NPC/scene state and README has the current template markers.
Pass: everything outside the overview block, especially the player-guide block, inherits exactly from the base tree. No truncation, reformatting or template shortening occurs.

## CI10 — README is never canon authority
Synopsis mentions a recurring companion or conflict.
Pass: the fact must already live in normal authoritative campaign records when persistence requires it. Removing README must not erase canon.

## CI11 — No secret leakage in README
GM knows an unrevealed villain identity/future plan.
Pass: dynamic annotation uses only established player-visible durable facts and does not expose the hidden information.

## CI12 — No standalone cosmetic title commit
The Master merely thinks a different automatic title sounds better, but no other persistence boundary exists and campaign identity has not materially shifted.
Pass: no GitHub write. Reconsider at a later legitimate boundary.

## CI13 — Legacy README without markers is not heuristically rewritten
A campaign README predates the overview markers.
Pass: ordinary gameplay/save leaves it untouched. Marker installation requires an explicit compatible migration/maintenance path.
