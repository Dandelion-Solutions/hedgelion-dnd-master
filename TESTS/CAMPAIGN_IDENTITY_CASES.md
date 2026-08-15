# Campaign Identity Regression Cases

These cases protect evolving book-like campaign naming, strict MANIFEST/card consistency, and the dynamic README overview without allowing gameplay saves to rewrite the static player guide.

## CI01 — Empty title is healthy at scaffold time
A new campaign has only the generated scaffold and almost no story identity.
Pass: `MANIFEST.campaign_name` and `CAMPAIGN_CARD.campaign_name` may remain null. Do not ask the player to name the campaign merely to fill the field.

## CI02 — Hero + broad world is enough for a first title
Durable setup now establishes the protagonist concept `эмо-вампир` and the broad surrounding premise `мир розовых пони и радужных единорогов`; no major plot exists yet.
Pass: at an already-required persistence boundary the Master MAY synthesize a concise literary title such as `Эмо-вампир в мире розовых пони и радужных единорогов`, store it in MANIFEST with `campaign_name_origin: auto`, and project the exact same string to CAMPAIGN_CARD. It need not wait for a villain/quest/arc.

## CI03 — Current scene is not the campaign title
The current fiction also includes a pink pony beside a road sign and a cupcake conversation.
Pass: do not title the whole campaign `Грым у указателя с пони и кексом` merely because that is the current scene. Prefer the durable protagonist/world identity.

## CI04 — One side missing keeps title null
Protagonist concept is known but the broad world is still undefined, or vice versa.
Pass: keep the automatic title null; do not invent missing premise solely to fill campaign_name.

## CI05 — Card never invents a name
MANIFEST title is null but runtime thinks of a catchy menu title.
Pass: card remains null until MANIFEST changes. If MANIFEST changes, the same transaction updates card to the exact same string.

## CI06 — Automatic title may evolve, but is sticky
An auto title exists. A new room, NPC or ordinary quest appears.
Pass: keep the title. Rename only when accumulated durable history materially changes what best represents the whole campaign.

## CI07 — Player title is sticky
Player explicitly names/renames the campaign.
Pass: store `campaign_name_origin: player`; automatic synthesis must not overwrite it until the player clearly delegates naming again.

## CI08 — Unknown legacy provenance is conservative
Older campaign has non-null `campaign_name` but no `campaign_name_origin`.
Pass: treat the existing title as sticky/manual for auto-renaming purposes. Do not silently rename it.

## CI09 — README overview is compact living annotation
Current README has overview markers and protagonist/world identity is now established.
Pass: during an already-required campaign transaction, Master may replace the overview with the title plus a short one-sentence/small-paragraph annotation. Do not expand it into several paragraphs unless the actual campaign later warrants that much context.

## CI10 — Static README guide is byte-preserved
Explicit save touches PC/NPC/scene state and README has the current template markers.
Pass: everything outside the overview block, especially the player-guide block, inherits exactly from the base tree. No truncation, reformatting or template shortening occurs.

## CI11 — README is never canon authority
Synopsis mentions a recurring companion or conflict.
Pass: the fact must already live in normal authoritative campaign records when persistence requires it. Removing README must not erase canon.

## CI12 — No secret leakage in README
GM knows an unrevealed villain identity/future plan.
Pass: dynamic annotation uses only established player-visible durable facts and does not expose hidden information.

## CI13 — No standalone cosmetic title commit
Master merely thinks a different automatic title sounds better, but no other persistence boundary exists and campaign identity has not materially shifted.
Pass: no GitHub write. Reconsider at a later legitimate boundary.

## CI14 — Legacy README without markers is not heuristically rewritten
A campaign README predates the overview markers.
Pass: ordinary gameplay/save leaves it untouched. Marker installation requires an explicit compatible migration/maintenance path.
