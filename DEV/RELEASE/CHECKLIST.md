# Release Checklist

## Source tree
- [ ] Repository root contains only repository infrastructure/metadata plus `GAME/` and `DEV/`; old root product/development trees are absent.
- [ ] `GAME/` is the exact runtime distribution source tree.
- [ ] `DEV/` contains architecture/tests/release policy/catalog development/developer tooling.
- [ ] Repository-root `docs/` is absent; Superpowers artifacts live only under `DEV/docs/superpowers/`.
- [ ] Exactly one tracked `ENGINE_VERSION.yaml` exists: `GAME/ENGINE_VERSION.yaml`.

## Version metadata
- [ ] `DEV/ENGINE_DEVELOPMENT.yaml` contains the full bookkeeping record.
- [ ] `GAME/ENGINE_VERSION.yaml` contains only the approved runtime projection.
- [ ] Shared fields are identical.
- [ ] version/recommended_tag are coherent.
- [ ] For release preparation, change shared `release_status` from `development` to `ready-for-tag` in both files.
- [ ] Tag publication is rejected unless status is `ready-for-tag` and tag equals `recommended_tag`.

## Runtime package
- [ ] `DEV/TOOLS/run_release_build --tag <tag>` builds the local pre-tag candidate into ignored repository-root `builds/`; `--output <dir>` is an optional override for CI or other explicit destinations.
- [ ] Builder archives every valid file under `GAME/`, not a maintained include list, and does not add the `GAME/` wrapper.
- [ ] ZIP root contains `ENGINE_VERSION.yaml`, `CORE/`, `RULES/`, `SCHEMA/`, `CAMPAIGN/`, `INSTALL/`, runtime `TOOLS/` and required support/legal files.
- [ ] ZIP contains no `DEV/`, development tests, architecture, release policy or maintenance tooling.
- [ ] Builder rejects output inside GAME, symlinks, build junk and case-insensitive path collisions.
- [ ] Repeated builds from the same tree/parameters are byte-identical; rebuilding the same tag replaces the same local filename rather than accumulating numbered variants.
- [ ] SHA-256 sidecar is produced next to the ZIP.
- [ ] Package-local and destination-relative template links validate in their correct namespaces.
- [ ] `INSTALL/README.md` embedded Project Instructions match `INSTALL/PROJECT_INSTRUCTIONS.txt`.

## Runtime behavior
- [ ] Fresh Project accepts only `hedgelion-dnd-master-runtime-v<version>.zip` package shape; GitHub source snapshots are rejected as install packages.
- [ ] After exact package resolution, complete local `CORE/*.md` + `RULES/INDEX.md` + `RULES/README.md` are preloaded once; campaign/world data remains lazy.
- [ ] Runtime scope is positive and package-local; GAME instructions do not name DEV-only paths/tools.
- [ ] `GAME/TOOLS/init_campaign.py` remains standard-library-only and works from extracted runtime package.
- [ ] Campaign generator produces root-layout campaign tree with no copied engine tree.
- [ ] Existing campaign refuses silent engine-version substitution.

## Maintenance regression
- [ ] `python -m unittest discover -s DEV/TESTS -v` passes.
- [ ] `DEV/TOOLS/run_maintenance_audit` passes.
- [ ] Audit validates GAME/DEV geometry, version projection, catalogs/schemas, runtime policy, Project Instructions parity, legal copies and an actual built runtime ZIP.
- [ ] Deprecated `GAME/TEMPLATE/CAMPAIGN_MANIFEST.yaml` is absent.
- [ ] `GAME/MIGRATIONS/README.md` describes campaign data/schema migration only; no engine-tree merge semantics remain.

## Tag and GitHub Release
- [ ] Pre-tag candidate from the final `ready-for-tag` tree is tested in a fresh Project.
- [ ] Create immutable tag exactly equal to `recommended_tag` from the approved release lineage.
- [ ] Tag-triggered `.github/workflows/release-runtime.yml` checks out the exact tag and calls only `DEV/TOOLS/run_release_build` for package composition/validation, using an explicit runner-temporary `--output` rather than repository-local `builds/`.
- [ ] Workflow get-or-creates the GitHub Release for the tag.
- [ ] Existing same-name runtime asset may be reused only when bytes/hash are identical; different bytes are a hard error and are never clobbered.
- [ ] GitHub-generated `Source code (zip)` / `Source code (tar.gz)` remain source snapshots and **are not runtime installation artifacts**.
- [ ] Test the exact uploaded runtime asset in a fresh Project before announcing the release.
