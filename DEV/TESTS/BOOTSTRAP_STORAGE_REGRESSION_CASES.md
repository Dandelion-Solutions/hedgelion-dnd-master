# Bootstrap / Storage v2 Regression Cases

## B01 — Archive first
Fresh Project chat has no extracted engine.
Pass: materialize/extract local D&D ZIP before bootstrap; no GitHub engine install.

## B02 — Temp filesystem is chat-local
Previous chat extracted engine.
Pass: current chat checks local availability independently and re-extracts if needed.

## B03 — No GitHub engine installation
Missing local engine.
Pass: request/materialize ZIP; no clone/pull/blob-copy.

## B04 — No base64 fallback
Any archive/scaffold limitation occurs.
Pass: use ordinary ZIP/filesystem/UTF-8 operations or stop; never explicit base64 reconstruction.

## B05 — Lazy context
Full package is local.
Pass: do not preload whole package into model context; campaign/world data remains lazy while exact CORE cache follows runtime policy.

## B06 — Connector first for campaign GitHub
Storage action needed.
Pass: use connected GitHub Connector first.

## B07 — Discovery <=5
At most five accessible repos.
Pass: exact-probe root DND_STORAGE.yaml.

## B08 — Discovery >5
More than five repos.
Pass: ask for repository name; do not mass-probe.

## B09 — Marker existence is discovery signal
Unknown/legacy marker exists.
Pass: recognize candidate; validate after selection.

## B10 — No marker own/friend choice
No candidate.
Pass: ask “Создать своё хранилище игр или подключиться к игре друга?”

## B11 — Own ownership gate
Supplied own repo owner != authenticated login.
Pass: route to friend flow; no own initialization.

## B12 — Empty own storage initialization
Owned NEW EMPTY repository has no marker.
Pass: create exact TEMPLATE/STORAGE_README.md first, then create v2 DND_STORAGE.yaml LAST; no engine/campaign directories, .gitignore, license or hidden scaffolding. Marker publication defines successful installation.

## B12a — Interrupted storage init retry
Repository has no marker but contains only the exact standard storage README from a prior interrupted initialization.
Pass: recognize partial initialization and create only the missing marker; do not duplicate/replace README.

## B12b — Do not repurpose populated repo silently
Owned repository has no marker and contains unrelated/user files.
Pass: do not initialize it silently; ask for a new empty repository or explicit maintenance decision.

## B13 — Friend missing marker
Guest names accessible repo without marker.
Pass: guest does not modify it; owner must initialize.

## B14 — Campaign discovery bounded
Storage has many files.
Pass: enumerate campaign/* and read campaign cards first; manifest is fallback only. Do not deep-load campaign state for menu presentation.

## B15 — Current root manifest
Campaign branch contains root MANIFEST.yaml.
Pass: identify current layout with campaign_root_prefix empty after selection.

## B16 — Legacy manifest fallback
Root MANIFEST absent but CAMPAIGN/MANIFEST.yaml exists.
Pass: identify legacy prefix CAMPAIGN/ and continue without automatic relocation after selection.

## B17 — Generator root layout
Local TOOLS/init_campaign.py outputs MANIFEST.yaml + STATE/... directly in output root.
Pass: publish exactly that output as branch root. MUST NOT “fix” it by wrapping output inside CAMPAIGN/.

## B18 — Human campaign README
Generator output contains README.md.
Pass: README gives player-facing play tips/orientation, not a directory inventory or “empty skeleton” explanation.

## B19 — One scaffold publication
Generated scaffold has many files.
Pass: one UTF-8 tree + one initialization commit + non-force ref publication/update; no per-file commits/base64.

## B20 — Campaign excludes storage root
Campaign branch is descended from storage default branch.
Pass: first campaign tree excludes DND_STORAGE.yaml and storage README.

## B21 — Development ZIP needs no public-main SHA
Authorized engine owner uses local release_status development package.
Pass: identity dev-v<version>, SHA may be null; do not query/pin public main merely for provenance.

## B22 — Published package keeps exact provenance
Normal release package is used.
Pass: resolve its published tag to exact commit SHA before new campaign/migration.

## B23 — Setup progress is staged
New campaign scaffold exists.
Pass: tell player setup has character -> minimal world -> first scene stages, with no duration estimate; surface coherent game-facing results rather than one long silent preparation block.

## B24 — Character before broad worldbuild
New PC is unresolved.
Pass: resolve/accept character first except genuinely required world constraints; no unrelated encyclopedia generation.

## B25 — Early play
PC accepted and minimal starting situation is ready.
Pass: create first scene/checkpoint and begin play; defer optional worldbuilding.

## B26 — Observer mode
Read access exists but gameplay authorization absent.
Pass: allow read/observe, deny game-state publication.

## B27 — One campaign is not implicit resume
Fresh chat; selected storage contains exactly one active campaign. User says `давай сыграем`.
Pass: show explicit campaign choice plus `Начать новую игру`; do not auto-select the campaign.

## B28 — Multiple campaigns plus new game
Fresh chat; storage contains active and paused campaigns.
Pass: list them concisely with status and also offer `Начать новую игру`; wait for explicit choice.

## B29 — Initializing campaign
Fresh chat; one campaign has status initializing.
Pass: offer it as unfinished setup and also offer new game; do not treat it as normal active resume.

## B30 — Archived campaigns stay out of default menu
Storage contains archived and active campaigns.
Pass: default menu shows non-archived visible entries; archived appears only on explicit request.

## B31 — Selection barrier prevents wasted startup
Fresh chat; one old campaign exists but user has not chosen it.
Pass: before choice read branches + cards/legacy manifests only. No campaign HEAD pin for gameplay, CONFIG/STATE/SCENE/PC reads, exact campaign-engine resolution, recap, migration check, or resume preload.

## B32 — Generic play request is not campaign identity
User says `начнём`, `давай сыграем`, or equivalent in a fresh chat.
Pass: treat as desire to play, not as permission to resume the sole/most recent campaign.

## B33 — Explicit current-chat intent avoids redundant menu
User starts fresh chat with `продолжим <unambiguous campaign>` or `начать новую игру`.
Pass: treat that as explicit selection and continue directly without asking the same choice again.

## B34 — Campaign menu uses N+1 numbering
Fresh chat has N >= 1 visible campaign choices.
Pass: render campaigns as explicit `1..N` entries and exactly one final `N+1. ➕ Начать новую игру`; number input resolves against that current menu only.

## B35 — One campaign is still numbered
Fresh chat has exactly one visible campaign.
Pass: render `1. <campaign>` and `2. ➕ Начать новую игру`; user may answer `1`, `2`, `продолжить`, or `новая игра`.

## B36 — Ambiguous bare continue does not guess
Fresh chat has multiple plausible continuable campaigns; user says only `продолжить`.
Pass: ask for number/name instead of selecting most recent/first campaign.

## B37 — Mandatory generator before questions
User explicitly selects New Game.
Pass: before asking character/world/style questions, run exact local TOOLS/init_campaign.py into a fresh output directory and successfully publish that generated scaffold.

## B38 — No semantic scaffold reconstruction
New campaign template contains scene/NPC/location/faction/index placeholders.
Pass: copy generator output mechanically. Do not open schemas to recreate those files, do not invent empty YAML blobs, and do not create scaffold files individually through GitHub Contents API.

## B39 — Generator failure has no per-file fallback
TOOLS/init_campaign.py is missing/fails or generated output cannot be bulk-published.
Pass: stop new-game initialization with a short actionable error. Never reconstruct scaffold file-by-file.

## B40 — Blank scaffold is one technical commit
Generator output contains many files.
Pass: first campaign-specific durable state is exactly one empty-scaffold commit/tree, with no invented lore/world content and no storage README/marker leakage.

## B41 — Exploratory drafting is local, adopted identity is the exception
Blank scaffold exists and character details are still tentative.
Pass: exploratory alternatives cause zero writes. If DIEGETIC_ONBOARDING adopts the first stable PC identity anchor, PROVISIONAL_IDENTITY is allowed/required before further fiction relies on it; otherwise batch until READY_PC/PLAY_READY or another authoritative boundary.

## B42 — Minimal world and first scene normally share launch batch
READY_PC is durable and no intervening player decision/pause exists.
Pass: create only immediate starting horizon + scene/current routing + recovery state actually required + active status in one coherent PLAY_READY launch transaction, then start true live narration. Do not create broad unused catalogs first.

## B43 — Setup technical silence
Scaffold/character/launch publication succeeds normally.
Pass: player-facing text does not mention YAML, schemas, branch/ref/HEAD, commits, staging, or “technical initialization is not finished”. Use game-facing progress only.

## B44 — No confirmation rereads after scaffold publication
Blank scaffold publication succeeds and Connector returns the created commit/tree information.
Pass: adopt it as known frontier; do not immediately refetch just-written scaffold files/HEAD solely to reconfirm own write.

## B45 — Bootstrap text transport stays UTF-8
Fresh own-storage initialization writes root `README.md` and `DND_STORAGE.yaml` before complete CORE preload.
Pass: use Connector UTF-8/text interfaces for semantically textual repository payloads; do not manually Base64-encode/decode text for transport, chunking, staging, reconstruction or verification. Connector-internal Base64 required by an underlying API is allowed and is not an LLM/runtime conversion.
