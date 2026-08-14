# Bootstrap / Storage Initialization Regression Cases

These cases prevent setup from drifting into slow or speculative repository manipulation.

## B01 — GitHub Connector first
A new setup requires GitHub reads/writes.
Pass: use the connected GitHub Connector immediately. Do not first try `gh`, shell git, local clone, direct HTTP/web scraping, container networking, or another transport.

## B02 — Diagnose Connector failure before fallback
A Connector operation fails.
Pass: distinguish runtime/binding, authenticated identity, App repository access, GitHub permission/status, rate/service error, and true missing capability before considering another transport.

## B03 — No speculative transport experiments
The normal Connector path is available but the Master imagines a potentially clever shortcut.
Pass: do not experiment with cross-repository SHA reuse, archive tricks, shell tools or undocumented APIs during user setup.

## B04 — Repository has a parent before D&D initialization
The current Connector requires a parent SHA for `create_commit`.
Pass: ask the user to create the fresh personal repository with GitHub's “Add a README” option. Do not create a D&D technical anchor commit when a normal initial GitHub commit can provide the parent.

## B05 — Copy is opaque transport
A complete published engine release must be installed into storage.
Pass: treat file bodies as opaque payload bytes. Do not semantically read, summarize, audit or use copied engine content as gameplay/model working context merely to copy it.

## B06 — Preserve the complete release tree
The release contains nested directories, empty `.gitkeep` files and ordinary files.
Pass: transfer the complete recursive tree preserving paths, file modes, bytes and empty files. Do not selectively copy only files that look important.

## B07 — One whole-tree checksum
The release-only target tree has been constructed.
Pass: verify exactly once that target release root tree SHA equals source release root tree SHA. Do not run per-file checksum rituals.

## B08 — Marker is last
The release-only target tree has not yet passed root-tree verification.
Pass: `DND_STORAGE.yaml` is not published or added to any visible target ref. Create/add the marker only after the exact release tree is verified.

## B09 — One D&D initialization commit
A verified release-only tree and valid storage marker are ready; target `main` still equals the pinned parent.
Pass: create one final tree, one D&D initialization commit, and one non-force ref update. No per-file commits and no marker-only commit.

## B10 — Failed preparation is non-authoritative
A blob/tree transfer or whole-tree checksum fails before final publication.
Pass: do not move target `main`. Unattached Git objects are non-authoritative; diagnose/rebuild without exposing a half-installed storage baseline.

## B11 — No redundant marker rewrite
The final marker blob already has the intended content inside the prepared final tree.
Pass: do not call `create_file`/`update_file` for the marker separately and do not create a no-op commit.

## B12 — Player-facing setup hides Git plumbing
Normal setup succeeds.
Pass: tell the player simply that setup is complete and move to the next game-relevant choice. Do not volunteer marker filenames, SHAs, refs, tree checksums, force-push details or commit topology.

## B13 — Friendly join wording
No storage is available and the user must choose a path.
Pass: ask whether to create their own campaign or join a friend's campaign. Do not describe the normal social path as joining a “foreign/somebody else's” repository in player-facing wording.

## B14 — Future Connector bulk-copy capability
A later GitHub Connector exposes a documented one-call bulk copy/import operation.
Pass: prefer it automatically, while preserving exact published-tag source selection, whole-tree equality verification before marker addition, and one final initialization commit/ref update.

## B15 — INSTALL README is for the human installer
A person opens `INSTALL/README.md` to install their own copy of D&D Master.
Pass: the document describes only actions the person must take: create/configure the ChatGPT Project, add the two install files from one release, connect GitHub, create or join a campaign repository, grant App access when needed, start play, and update the Project. It does not explain internal tree-copy algorithms, storage metadata, refs/SHAs, checksum procedure, engine-update phases, regression machinery, or other bootstrap implementation details.
