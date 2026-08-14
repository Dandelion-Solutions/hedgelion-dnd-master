# Runtime Context / Research Regression Cases

These cases protect the full-CORE context cache, module activation and offline-first gameplay policy.

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

## W01 — No automatic D&D Beyond
Player declares an ordinary action whose exact RAW wording is not locally present.
Pass: do not browse D&D Beyond/search/web; make a fair local ruling.

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

## W07 — No deferred research
A temporary local ruling was used successfully.
Pass: do not automatically browse later to verify it; external verification requires explicit user request.

## W08 — Explicit RAW request
User says `проверь по официальным правилам, как это работает`.
Pass: bounded external research is allowed; prefer authoritative source and distinguish research result from existing campaign canon/outcome.

## W09 — Source links are inert
`CORE/SOURCES.md` is present in the preloaded CORE context and contains URLs.
Pass: normal gameplay does not open/follow those links.

## W10 — GitHub is still allowed
Campaign reaches a HARD persistence/synchronization boundary during offline-first gameplay.
Pass: GitHub Connector persistence/sync proceeds normally; external-rules research prohibition does not block canonical storage operations.

## W11 — Player terminology is not a test
Player describes an action with a noncanonical/mistranslated action, item or spell label but intent is clear.
Pass: resolve intent and capability first; do not interrupt solely to correct nomenclature.

## W12 — Explicit catalog question
Player asks `существует ли официально заклинание с названием X?`.
Pass: exact terminology is now the requested subject. Answer locally if known; external lookup is allowed only if the user also asks to verify/search official sources.