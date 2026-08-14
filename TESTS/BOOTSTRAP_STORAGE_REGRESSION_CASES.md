# Bootstrap / Storage v2 Regression Cases

These cases protect the release-ZIP + lightweight-storage architecture.

## B01 — Archive first
New Project chat has no extracted engine.
Pass: locate D&D Master ZIP from Project Sources/current-chat attachment and extract locally before gameplay/bootstrap.

## B02 — Do not trust another chat's temp filesystem
A previous Project chat extracted the engine.
Pass: current chat independently checks local availability and re-extracts if necessary.

## B03 — No GitHub engine installation
Local engine files are missing.
Pass: do not clone/pull/download/reconstruct engine source from GitHub; ask for/materialize the release ZIP.

## B04 — No base64 fallback
Archive/scaffold handling encounters a tool limitation.
Pass: never explicitly encode/reconstruct files with base64. Use normal ZIP/filesystem/UTF-8 tree operations or stop with a capability error.

## B05 — Lazy context despite full local package
Whole release is extracted locally.
Pass: do not preload whole CORE/RULES/SCHEMA into model context; load only routed files plus mandatory runtime modules.

## B06 — Connector first for campaign GitHub
Storage discovery/read/write is needed.
Pass: use connected GitHub Connector before shell git/gh/private HTTP alternatives.

## B07 — Discovery threshold <= 5
At most five accessible repositories exist.
Pass: exact-probe root `DND_STORAGE.yaml` only in those repositories.

## B08 — Discovery threshold > 5
Six or more accessible repositories are detected.
Pass: stop broad probing and ask user for repository name.

## B09 — Marker existence is discovery signal
A repository has root `DND_STORAGE.yaml` with legacy/unknown content.
Pass: recognize it as storage candidate; defer semantic validation until metadata is needed.

## B10 — No marker: preserve own/friend choice
No storage candidate exists.
Pass: ask “Создать своё хранилище игр или подключиться к игре друга?”

## B11 — Own repo ownership gate
User selects own storage but supplied repository owner != authenticated GitHub login.
Pass: do not initialize as own storage; route to friend/join flow.

## B12 — Fresh own storage is marker-only
Owned README-initialized repository has no marker.
Pass: publish one v2 `DND_STORAGE.yaml` metadata commit. Do not copy engine or create campaign directories.

## B13 — Friend repository missing marker
Guest can access named friend's repository but root marker is absent.
Pass: do not modify it; report incorrect D&D storage initialization and require owner action.

## B14 — Friend marker exists
Guest can access named repository and marker exists.
Pass: select it and continue campaign discovery without owner-infrastructure administration.

## B15 — Campaign discovery is bounded
Selected storage has many files.
Pass: enumerate only `campaign/*`, read manifests only, and do not scan WORLD/LOG to list games.

## B16 — Observer mode
User can read campaign but lacks gameplay authorization.
Pass: campaign may be inspected/read; no gameplay-state publication.

## B17 — New campaign scaffold is local
New game is requested.
Pass: use local `TOOLS/init_campaign.py` / local `CAMPAIGN/` skeleton; do not obtain scaffold blobs from public GitHub.

## B18 — One campaign initialization commit
Generated scaffold contains many files/placeholders.
Pass: publish as one coherent UTF-8 tree + one campaign initialization commit + one non-force ref update.

## B19 — Campaign excludes storage root
Campaign branch was created from storage default branch containing marker/README.
Pass: first campaign commit replaces inherited tree with generated campaign tree; marker/README do not become campaign canon.

## B20 — v1 storage is inert engine source
Legacy v1 storage contains full copied CORE tree.
Pass: marker identifies storage, but runtime never reads those copied CORE files as engine.

## B21 — Human install is simple
A user follows `INSTALL/README.md`.
Pass: Project Instructions + Source code ZIP + GitHub Connector are sufficient; user is not instructed to copy engine files into campaign repository.

## B22 — Missing Project Source materialization
ZIP is listed as Project Source but current chat cannot access it as a local archive.
Pass: ask user to attach the same ZIP directly to current chat; do not switch to GitHub engine download.
