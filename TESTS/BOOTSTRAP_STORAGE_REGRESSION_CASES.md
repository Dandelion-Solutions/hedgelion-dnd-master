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

## B12 — Marker-only storage init
Owned README repo has no marker.
Pass: publish one v2 marker metadata commit; no engine/campaign directories.

## B13 — Friend missing marker
Guest names accessible repo without marker.
Pass: guest does not modify it; owner must initialize.

## B14 — Campaign discovery bounded
Storage has many files.
Pass: enumerate campaign/* and read manifests only.

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
Pass: one UTF-8 tree + one initialization commit + non-force ref update; no per-file commits/base64.

## B20 — Campaign excludes storage root
Campaign branch created from storage default branch.
Pass: first campaign tree excludes DND_STORAGE.yaml and storage README.

## B21 — Development ZIP needs no public-main SHA
Authorized engine owner uses local release_status development package.
Pass: identity dev-v<version>, SHA may be null; do not query/pin public main merely for provenance.

## B22 — Published package keeps exact provenance
Normal release package is used.
Pass: resolve its published tag to exact commit SHA before new campaign/migration.

## B23 — Setup progress is staged
New campaign scaffold exists.
Pass: tell player setup has character -> minimal world -> first scene stages, with no duration estimate; surface/persist coherent results between stages rather than one long silent block.

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
Pass: show explicit `Продолжить игру` with that campaign AND `Начать новую игру`; do not auto-select the campaign.

## B28 — Multiple campaigns plus new game
Fresh chat; storage contains active and paused campaigns.
Pass: list them concisely with status and also offer `Начать новую игру`; wait for explicit choice.

## B29 — Initializing campaign
Fresh chat; one campaign has status initializing.
Pass: offer it as `продолжить незавершённую настройку` and also offer new game; do not treat it as normal active resume.

## B30 — Archived campaigns stay out of default menu
Storage contains archived and active campaigns.
Pass: default continue list shows active/non-archived only; archived appears only on explicit request.

## B31 — Selection barrier prevents wasted startup
Fresh chat; one old campaign exists but user has not chosen it.
Pass: before choice read branches + manifests only. No campaign HEAD pin for gameplay, CONFIG/STATE/SCENE/PC reads, exact campaign-engine resolution, recap, migration check, or resume preload.

## B32 — Generic play request is not campaign identity
User says `начнём`, `давай сыграем`, or equivalent in a fresh chat.
Pass: treat as desire to play, not as permission to resume the sole/most recent campaign.

## B33 — Explicit current-chat intent avoids redundant menu
User starts fresh chat with `продолжим <unambiguous campaign>` or `начать новую игру`.
Pass: treat that as explicit selection and continue directly without asking the same choice again.