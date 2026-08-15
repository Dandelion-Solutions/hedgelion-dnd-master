# Release Checklist

## Runtime
- [ ] New Project chat can materialize/extract the release Source code ZIP.
- [ ] Extracted files are used lazily; full engine is not preloaded into model context.
- [ ] `RUNTIME.md` + `AI_REASONING.md` are mandatory during gameplay.
- [ ] Existing campaign refuses silent engine-version substitution.

## Installation package
- [ ] `INSTALL/PROJECT_INSTRUCTIONS.txt` fits Project Instructions limits.
- [ ] Project Instructions locate/extract `hedgelion-dnd-master-*.zip` and then open `INSTALL/00_DND_BOOTSTRAP.md`.
- [ ] Release Source code ZIP alone contains launcher/runtime/schema/templates/tools needed by a chat.
- [ ] `INSTALL/README.md` tells the human to add Project Instructions + Source code ZIP.
- [ ] No normal install step requires engine clone/pull or engine copy into campaign storage.
- [ ] No documented install/scaffold path uses explicit base64.

## Storage v2
- [ ] Storage discovery uses exact root `DND_STORAGE.yaml`.
- [ ] <=5 accessible repositories may be exact-probed; >5 asks for repository name.
- [ ] Own-storage and friend-storage onboarding both work.
- [ ] Fresh own storage starts from a completely empty GitHub repository; user enables no README/.gitignore/license/template initializer.
- [ ] Bootstrap creates the standard human-facing storage README first and publishes `DND_STORAGE.yaml` last; marker means initialization completed.
- [ ] Fresh storage default branch contains no engine tree, campaign skeleton, hidden scaffold or placeholder files.
- [ ] Interrupted README-only initialization is recoverable without duplicating/replacing the standard README.
- [ ] A non-empty unrelated repository is not silently repurposed as storage.
- [ ] Friend repository without marker is not modified by guest.
- [ ] Legacy v1 storage is discoverable but copied engine files are never runtime source.

## Campaign initialization
- [ ] `TOOLS/init_campaign.py` works with Python standard library only.
- [ ] Generator copies complete local `CAMPAIGN/` skeleton and fills technical identity/engine provenance.
- [ ] New campaign branch is created from storage default branch.
- [ ] First campaign commit replaces inherited storage-root tree with generated campaign tree.
- [ ] Scaffold publishes as one tree/commit/ref update, not per-file commits.
- [ ] Campaign branch contains no copied CORE/RULES/SCHEMA/INSTALL engine tree.

## Updates
- [ ] Public tags are update metadata only; target Source code ZIP must be locally available.
- [ ] Storage `baseline_version` update copies zero engine files.
- [ ] Existing campaign migration changes only defined campaign data + manifest provenance.
- [ ] Guest cannot govern storage/campaign engine maintenance.
- [ ] Post-update runtime reloads exact local target package.

## Regression
- [ ] `TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md` reviewed.
- [ ] `TESTS/ENGINE_UPDATE_CASES.md` reviewed.
- [ ] Fresh-Project end-to-end test completed from GitHub-generated Source code ZIP.
- [ ] New own storage tested from a completely empty repository.
- [ ] Friend/collaborator flow tested.
- [ ] Existing campaign resume tested in a second new Project chat.

## Release
- [ ] `ENGINE_VERSION.yaml` release_status changed from `development` to `ready-for-tag`.
- [ ] version/recommended_tag coherent.
- [ ] create immutable tag.
- [ ] create GitHub Release; verify GitHub-generated Source code (zip).
- [ ] test the exact generated release ZIP in a fresh Project before announcing release.
