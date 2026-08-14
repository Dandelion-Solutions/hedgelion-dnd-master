# Runtime Context / Research Regression Cases

These cases protect the full-CORE context cache, module activation, low-latency live play and bounded preparation research.

## C01 — Exact engine first
Multiple local engine ZIPs exist and selected campaign requires version A.
Pass: bootstrap resolves exact package A before building the CORE context cache; it does not preload a different package merely because it was discovered first.

## C02 — Full CORE preload
Exact engine package is resolved.
Pass: read complete local `CORE/*.md` into current model context once before gameplay/substantial setup; also preload `RULES/INDEX.md` and `RULES/README.md`.

## C03 — Context is not ChatGPT Memory
CORE is preloaded.
Pass: treat it as current-chat immutable instruction context, not campaign canon or ChatGPT Memory.

## C04 — Loaded is not active
All CORE text is present while an ordinary non-magic social scene is running.
Pass: magic/combat/update/live-scene procedures remain dormant and add no extra checks/retrievals merely because their files are present.

## C05 — No CORE reread
A later turn activates a module that was dormant at startup.
Pass: use the already-present module; no disk/GitHub fetch of that CORE file.

## C06 — Scene change does not evict CORE
Campaign moves from dialogue to exploration to combat.
Pass: activation set changes; full CORE context cache remains available without rereading/evicting modules.

## C07 — Campaign data stays lazy
CORE is fully preloaded.
Pass: do not preload all WORLD/LOG/INDEX/entities; retrieve only decision-relevant campaign records.

## C08 — Engine switch invalidates cache
Authorized migration changes exact engine package A -> B.
Pass: invalidate old engine instructions and build full CORE cache from exact package B once before further adjudication.

## C09 — Context loss recovery
Runtime can positively determine required engine instructions are no longer available after context compaction.
Pass: rehydrate full CORE cache once; do not repeatedly reread individual modules turn-by-turn.

## W01 — No automatic D&D Beyond in a live turn
Player declares an ordinary action whose exact RAW wording is not locally present.
Pass: do not browse D&D Beyond/search/web merely to validate the action; make a fair local ruling.

## W02 — Approximate spell wording
Player raises a hand and shouts `Замри!` at a moving chest, clearly intending to stop/immobilize it.
Pass: treat wording as fictional intent; do not respond primarily that no official spell named `Замри` exists; determine whether actual character capability can produce the effect and adjudicate locally.

## W03 — No manufactured ability
Player uses an invented spell word but PC has no capability plausibly producing the requested effect.
Pass: do not create a new permanent spell; explain/resolve the capability constraint briefly without external search.

## W04 — Equivalent mapping
Player's approximate wording clearly maps to one already-known ability with equivalent cost/risk/effect.
Pass: normalize internally and continue play without forcing the player to name the official ability.

## W05 — Material ambiguity
Two available abilities plausibly match the wording but consume materially different resources or produce different risks.
Pass: ask one minimal clarification; do not ask merely for official terminology.

## W06 — Local ruling precedent
Exact RAW is locally unavailable and the Master makes a consequential reusable ruling.
Pass: continue scene without web lookup and persist the ruling if future analogous consistency requires it.

## W07 — No automatic deferred RAW verification
A temporary local ruling was used successfully.
Pass: do not automatically browse later merely to check whether the Master was right. External RAW verification requires explicit user request or a separate authorized maintenance/research reason.

## W08 — Explicit RAW request
User says `проверь по официальным правилам, как это работает`.
Pass: bounded external research is allowed; prefer authoritative source and distinguish research result from existing campaign canon/outcome.

## W09 — Source links are inert during normal play
`CORE/SOURCES.md` is present in the preloaded CORE context and contains URLs.
Pass: normal gameplay does not open/follow those links merely because they exist.

## W10 — GitHub is still allowed
Campaign reaches a HARD persistence/synchronization boundary during local-first gameplay.
Pass: GitHub Connector persistence/sync proceeds normally; live-turn external-rules policy does not block canonical storage operations.

## W11 — Player terminology is not a test
Player describes an action with a noncanonical/mistranslated action, item or spell label but intent is clear.
Pass: resolve intent and capability first; do not interrupt solely to correct nomenclature.

## W12 — Explicit catalog question
Player asks `существует ли официально заклинание с названием X?`.
Pass: exact terminology is now the requested subject. Answer locally if known; external lookup is allowed when the user asks to verify/search official sources.

## R01 — Worldbuilding research is allowed
The campaign is between setup phases or at a session-prep boundary and the next region would benefit from accurate published-setting/cultural lore.
Pass: Master may use bounded trustworthy web/source research without requiring an explicit `search the web` request first.

## R02 — Research does not interrupt unresolved action
A player has declared a live action while the Master notices an interesting lore question.
Pass: adjudicate the action locally first; defer optional enrichment research to a later prep boundary.

## R03 — Batch and distill
Several related lore facts are needed for the next scene.
Pass: research them in one bounded pass, distill adopted facts into compact prep/WORLD state, then stop browsing; do not reopen sources for every sentence.

## R04 — Source authority tiers
Official setting source, reputable wiki and forum disagree.
Pass: use official/primary source for exact published facts when source fidelity requires it; use wiki as secondary navigation/cross-reference; treat forum/community interpretation as inspiration rather than automatic fact authority.

## R05 — Community inspiration is welcome
A forum/article contains a strong atmospheric idea but no authoritative canon claim.
Pass: it may inspire original prep when compatible with campaign canon; do not falsely attribute it as official D&D fact.

## R06 — Character setup lookup is front-loaded
A new spellcaster needs exact durable spell/feature mechanics not locally stored.
Pass: a bounded official-source setup pass is allowed; store chosen mechanics so live turns do not repeatedly browse them.

## R07 — Research horizon stays bounded
One village is relevant, but the setting wiki contains thousands of pages.
Pass: research only the facts needed for the current/next horizon; do not crawl the whole setting because information is available.

## P01 — Mechanics question has meaningful anchors
New player has no mechanics presentation preference.
Pass: explain 0 as story-first/no numbers, 5 as important rolls/resources, 10 as full visible tracking/calculations; do not ask a bare `0..10` question.

## P02 — Mechanics detail changes presentation only
Player chooses mechanics detail 0 or 10.
Pass: underlying rules/math/randomness are identical; only player-facing mechanical detail changes.

## P03 — D&D lore fidelity is campaign-wide
New campaign asks how source-faithful/bookish D&D should feel.
Pass: store `CONFIG.play_style.dnd_lore_fidelity` 0..10, not in an individual PLAYER record.

## P04 — Lore fidelity has meaningful anchors
Player is asked for dnd_lore_fidelity.
Pass: explain 0 as free lore/terminology with honest D&D mechanics, 5 as recognizable D&D without source pedantry, and 10 as close adherence to adopted official lore/terminology/published interpretations.

## P05 — Lore fidelity never changes mechanics
Two otherwise identical campaigns use dnd_lore_fidelity 0 and 10.
Pass: dice math, DC fairness, resources, action economy, PC capabilities and established rules remain identical unless an explicit house rule independently changes them.

## P06 — Low fidelity may still research
Campaign has dnd_lore_fidelity 1 and Master is preparing a new region.
Pass: trustworthy external sources may still inspire rich content; they do not automatically constrain original campaign fiction.

## P07 — High fidelity checks material setting facts
Campaign has dnd_lore_fidelity 10 in an adopted published setting and a major setting fact matters to upcoming play.
Pass: bounded authoritative research is appropriate at prep boundary; once adopted/persisted, resulting campaign canon is not silently rewritten later.
