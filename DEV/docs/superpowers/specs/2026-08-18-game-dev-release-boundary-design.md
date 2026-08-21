# GAME / DEV Runtime Distribution Boundary Design

Status: approved design direction; implementation pending written-spec review.

## Goal

Physically separate HDM game/runtime distribution content from engine-development content so that:

1. the repository has an obvious `GAME/` versus `DEV/` ownership boundary;
2. the game installation archive contains only files the installed HDM product may need;
3. the release archive is built from the contents of `GAME/` without a hand-maintained inclusion/exclusion list;
4. game/runtime files remain package-root-relative and never depend on the development repository's `GAME/` prefix;
5. files copied into campaign-storage repositories are validated in their destination layout, so source-repository paths cannot leak into generated storage/campaign content;
6. GitHub-generated Source code archives are no longer the HDM installation artifact;
7. a repository-owned build entry point defines the release package, while GitHub Actions only invokes that entry point and publishes its output.

This is a repository-layout and release-boundary change. It must preserve existing gameplay, storage, bootstrap, campaign initialization, persistence, and access semantics except where path names or release-asset discovery necessarily change.

## Architectural boundary

The repository becomes two explicit application areas plus repository metadata:

```text
/
├── GAME/                         # exact source tree of the installed game package
│   ├── ENGINE_VERSION.yaml
│   ├── INSTALL/
│   ├── CORE/
│   ├── RULES/
│   ├── SCHEMA/
│   ├── CAMPAIGN/
│   ├── TEMPLATE/
│   ├── MIGRATIONS/
│   ├── TOOLS/
│   │   └── init_campaign.py
│   ├── LICENSE
│   ├── NOTICE
│   ├── THIRD_PARTY_NOTICES.md
│   └── LICENSES/
│
├── DEV/                          # engine design, testing, maintenance and release tooling
│   ├── ARCHITECTURE/
│   ├── TESTS/
│   ├── RELEASE/
│   ├── CATALOG/
│   ├── SCHEMAS/
│   ├── TOOLS/
│   │   ├── build_release.py
│   │   ├── audit_engine.py
│   │   ├── run_maintenance_audit
│   │   └── requirements-maintenance.txt
│   └── docs/
│       └── superpowers/
│
├── .github/
│   └── workflows/
├── AGENTS.md
├── README.md
├── LICENSE
├── NOTICE
├── THIRD_PARTY_NOTICES.md
├── LICENSES/
└── .gitignore
```

`.github/` remains at repository root because GitHub requires workflow files there. Repository-level metadata such as `AGENTS.md`, the GitHub-facing `README.md`, `.gitignore`, and repository legal files also remain at root.

Feature branches continue to contain both `GAME/` and `DEV/`; this design does not introduce permanent Git branches for runtime versus development.

## Current classification

### Move into `GAME/`

The following existing trees are installed-product content and move under `GAME/`:

- `ENGINE_VERSION.yaml`;
- `INSTALL/`;
- `CORE/`;
- `RULES/`;
- singular `SCHEMA/` containing campaign/storage/runtime data contracts;
- `CAMPAIGN/`, which is the local source template for new campaign branches;
- runtime-useful `TEMPLATE/` content, including `STORAGE_README.md`;
- `MIGRATIONS/`, because installed engine updates may require campaign migration assets;
- runtime executable `TOOLS/init_campaign.py`.

Legal material needed by the standalone distributed package is also present under `GAME/`.

### Move into `DEV/`

The following existing trees are development-only at the current implementation stage:

- `ARCHITECTURE/`;
- `TESTS/`;
- `RELEASE/`;
- current `CATALOG/`;
- current plural `SCHEMAS/` containing mechanical-runtime development schemas;
- `TOOLS/audit_engine.py`;
- `TOOLS/run_maintenance_audit`;
- `TOOLS/requirements-maintenance.txt`;
- `docs/superpowers/`.

`CATALOG/` and plural `SCHEMAS/` are explicitly development-only for now because the mechanical runtime is not implemented. Future runtime reference/catalog data will be designed in the format most appropriate for that runtime and may later introduce corresponding `GAME/` data. The current development artifacts must not be included in the game package merely in anticipation of that future work.

### Delete deprecated template stub

Delete `TEMPLATE/CAMPAIGN_MANIFEST.yaml` rather than moving it. It is a deprecated compatibility stub; the authoritative new-campaign manifest template is `CAMPAIGN/MANIFEST.yaml`, copied by `TOOLS/init_campaign.py` with the rest of the campaign scaffold.

## Three path namespaces

The implementation must distinguish three different path namespaces. Mixing them is a defect.

### 1. Development repository paths

Development instructions, tests, architecture documents and maintenance tooling refer to the source repository layout:

```text
GAME/CORE/RUNTIME.md
GAME/TOOLS/init_campaign.py
DEV/TESTS/...
DEV/CATALOG/...
DEV/SCHEMAS/...
DEV/TOOLS/build_release.py
```

Development documentation must be updated to these repository-root paths where it is describing or inspecting source-tree files.

### 2. Installed package paths

Everything inside `GAME/` is written as though `GAME/` itself is the package root. Game/runtime files must not depend on or refer to the development-repository prefix `GAME/` when addressing another packaged file.

For example, a game instruction uses:

```text
CORE/RUNTIME.md
TEMPLATE/STORAGE_README.md
TOOLS/init_campaign.py
CAMPAIGN/MANIFEST.yaml
```

not:

```text
GAME/CORE/RUNTIME.md
GAME/TEMPLATE/STORAGE_README.md
```

This is required because the release builder archives the **contents** of `GAME/`, not the `GAME/` directory itself.

Therefore:

```text
repo/GAME/ENGINE_VERSION.yaml -> archive/ENGINE_VERSION.yaml
repo/GAME/CORE/RUNTIME.md      -> archive/CORE/RUNTIME.md
```

The existing bootstrap already operates in this package-root model and should retain the same effective package paths after relocation.

### 3. Published destination paths

Some package files are source templates whose content is copied into a different GitHub repository/tree. Their relative links and path references must be interpreted against the destination tree, not against either the development repository or the installed package.

Examples:

```text
GAME/TEMPLATE/STORAGE_README.md
    -> storage default branch /README.md

GAME/CAMPAIGN/README.md
    -> campaign branch /README.md

GAME/CAMPAIGN/MANIFEST.yaml
    -> campaign branch /MANIFEST.yaml
```

A copied template must never emit a path such as `GAME/TEMPLATE/...` or `GAME/CAMPAIGN/...` into storage/campaign canon merely because that was its source location.

## Source-layout leakage rule

No runtime/package behavior may require the string `GAME/` as a prefix to locate installed engine files.

For files that are copied/published into storage or campaign repositories, validation must additionally ensure that relative Markdown links and other explicit file references are valid for the destination layout. A source-repository prefix such as `GAME/` or `DEV/` in a destination-relative link is invalid unless it is intentionally ordinary prose rather than a file location.

The migration must audit existing path references instead of blindly prefixing every old path with `GAME/`:

- development-facing references normally become `GAME/...` or `DEV/...`;
- game-facing references normally retain their current package-root path such as `CORE/...` or `TOOLS/...`;
- copied-template references are evaluated in the generated storage/campaign layout.

## Runtime bootstrap behavior

The physical move does not create a new gameplay lifecycle. Existing behavior remains authoritative:

- Project Instructions locate the installed HDM release archive;
- bootstrap locates package-root `ENGINE_VERSION.yaml`;
- bootstrap uses package-local `CORE/`, `RULES/`, `SCHEMA/`, `CAMPAIGN/`, `TEMPLATE/`, `MIGRATIONS/` and runtime `TOOLS/` as required by its existing procedures;
- storage initialization copies the exact local storage README template to storage-root `README.md`;
- new-campaign initialization runs the exact package-local `TOOLS/init_campaign.py`, which copies the contents of package-local `CAMPAIGN/` into the root of a new campaign branch;
- after runtime is resolved, ordinary gameplay continues to use the existing runtime-scope and CORE activation rules rather than treating installation/template directories as ordinary gameplay instruction sources.

Bootstrap and Project Instructions should be changed only where release-asset naming/discovery or clarified package categories require it. Do not add a second parallel set of lifecycle rules simply because source files moved under `GAME/` in the development repository.

## Runtime tool split

The old mixed `TOOLS/` tree is replaced by consumer-owned tool trees.

### `GAME/TOOLS/`

Contains only executables/assets that the installed product may invoke. Initially this includes:

```text
GAME/TOOLS/init_campaign.py
```

Its existing source-root calculation remains conceptually valid because the parent of `TOOLS/` is the package root both in `repo/GAME/` and after extraction from the release archive.

### `DEV/TOOLS/`

Contains development, audit, test-support and release-build tools. Initially:

```text
DEV/TOOLS/audit_engine.py
DEV/TOOLS/run_maintenance_audit
DEV/TOOLS/requirements-maintenance.txt
DEV/TOOLS/build_release.py
```

Development launchers and audits must explicitly resolve repository root and `GAME/` root after this move; they must not assume that the parent of `DEV/TOOLS/` is the game package root.

## Canonical release builder

Add a repository-owned build entry point:

```text
DEV/TOOLS/build_release.py
```

It is the sole canonical definition of how an HDM game release asset is built. GitHub Actions must not duplicate package-selection logic.

The builder uses Python standard library unless a concrete future requirement justifies another dependency.

### Builder input

The builder operates on an exact repository checkout and receives the intended release tag/version context. It reads `GAME/ENGINE_VERSION.yaml` as the canonical package metadata source.

For a tagged release it must reject incoherent release metadata, including a tag that does not match the package's declared recommended tag/version policy.

### Builder validation

Before creating the archive, the builder must fail on at least these conditions:

1. required package-root files/directories are missing;
2. development-only trees appear inside `GAME/`, including `DEV`, `ARCHITECTURE`, `TESTS`, development `CATALOG`, development plural `SCHEMAS`, or maintenance audit tooling;
3. game/runtime path references incorrectly require the development `GAME/` prefix;
4. generated storage/campaign template outputs contain invalid relative Markdown links for their destination layout;
5. the campaign scaffold cannot be generated with exact `GAME/TOOLS/init_campaign.py` into a temporary destination;
6. generated campaign root has an unexpected extra `CAMPAIGN/` wrapper or lacks required root files;
7. distributed legal files do not match the corresponding canonical repository-root legal material;
8. deprecated `TEMPLATE/CAMPAIGN_MANIFEST.yaml` exists in the package.

The destination-template check must materialize or model the destination tree before validating links. It must not judge a copied template's links relative to `GAME/TEMPLATE/` or `GAME/CAMPAIGN/`.

### Builder output

The current required output is one installable ZIP asset with an unambiguous runtime-specific name, for example:

```text
hedgelion-dnd-master-runtime-v0.7.zip
```

The ZIP root is the contents of `GAME/`:

```text
ENGINE_VERSION.yaml
INSTALL/
CORE/
RULES/
SCHEMA/
CAMPAIGN/
TEMPLATE/
MIGRATIONS/
TOOLS/
LICENSE
NOTICE
THIRD_PARTY_NOTICES.md
LICENSES/
```

It must not contain a top-level `GAME/` wrapper.

The builder should produce files in deterministic ordering and avoid embedding irrelevant local build-environment state. Reproducible byte identity is desirable; the implementation plan should choose a simple deterministic ZIP strategy rather than relying on filesystem traversal order/timestamps.

Additional future release products, transforms or metadata may be added to this entry point later without teaching GitHub Actions the package composition.

## GitHub Actions release workflow

Add a tag-triggered workflow under `.github/workflows/`.

The workflow's responsibilities are deliberately thin:

1. check out the exact tagged repository tree;
2. set up the supported Python runtime;
3. invoke `DEV/TOOLS/build_release.py` with the tag context and output directory;
4. stop if the builder/validation fails;
5. ensure a GitHub Release exists for the exact tag;
6. upload the builder-produced runtime ZIP as a Release Asset.

The workflow must have only the GitHub permission needed to publish release assets, normally `contents: write`.

The workflow must not independently decide which repository directories belong in the game package. There is exactly one package-composition authority: `DEV/TOOLS/build_release.py`.

The upload path should be idempotent enough for a rerun of the same tagged workflow to replace/re-upload the same named runtime asset rather than create ambiguously named duplicates.

## GitHub-generated source archives

GitHub's automatic `Source code (zip)` and `Source code (tar.gz)` remain present as repository source snapshots but are no longer installation artifacts.

User-facing installation documentation and Project Instructions must direct users to the custom runtime asset and must no longer say to install from GitHub's generated Source code archive.

The runtime archive name must be sufficiently distinct that installation instructions can identify it unambiguously.

## Legal files

Repository-root legal files remain because they govern/describe the source repository. Equivalent legal material is also included under `GAME/` so the standalone runtime distribution carries its required notices.

To avoid silent drift, release validation must compare the distributed copies against the canonical root copies. This applies to:

- `LICENSE`;
- `NOTICE`;
- `THIRD_PARTY_NOTICES.md`;
- the required contents of `LICENSES/`.

The implementation may copy these files into `GAME/` as tracked files, but any mismatch must make the release build fail.

## Development-path migration

Moving files changes development-facing references across architecture docs, tests, audit scripts, release checklist, root README and `AGENTS.md`.

The implementation must audit repository-internal path references systematically. It must not perform a global textual replacement such as `CORE/ -> GAME/CORE/`, because that would corrupt package-root instructions inside `GAME/` and destination-relative template content.

Expected examples after migration:

```text
AGENTS.md maintenance command:
DEV/TOOLS/run_maintenance_audit

Development architecture reference:
GAME/CORE/PERSISTENCE.md

Development mechanical schema reference:
DEV/SCHEMAS/rule-element.schema.json

Runtime bootstrap reference inside GAME:
CORE/PERSISTENCE.md

Runtime new-game tool reference inside GAME:
TOOLS/init_campaign.py
```

## Maintenance audit migration

The canonical engine-maintenance audit remains development-only and moves to:

```text
DEV/TOOLS/run_maintenance_audit
```

Its isolated cache may remain repository-local (for example `.hdm-maintenance/`) but the launcher must derive repository root correctly from its new location.

`DEV/TOOLS/audit_engine.py` and its tests must be updated to validate the new source layout. In particular, development audits should understand both:

- source-tree locations such as `GAME/CORE/...`;
- release/package-root expectations such as `CORE/...` after packaging.

Maintenance dependencies stay development-only and must never enter the runtime ZIP.

## Testing and regression coverage

Implementation must add or update automated/regression coverage for the following categories.

### Repository boundary

- required source trees live under the correct `GAME/` or `DEV/` branch of the directory tree;
- no known development-only tree/tool is present under `GAME/`;
- `CATALOG/` and plural `SCHEMAS/` are under `DEV/` for the current mechanical-runtime phase;
- deprecated `TEMPLATE/CAMPAIGN_MANIFEST.yaml` is absent.

### Package construction

- builder packages exactly the contents of `GAME/` at archive root;
- archive has `ENGINE_VERSION.yaml` at root and no top-level `GAME/` directory;
- runtime ZIP contains required installation/bootstrap/runtime/schema/template/runtime-tool/legal files;
- runtime ZIP excludes `DEV/`, `AGENTS.md`, development tests, architecture proposals, superpowers specs/plans, audit launcher/dependencies, and development catalogs/schemas.

### Runtime smoke tests

From an extracted produced ZIP:

- bootstrap can find `ENGINE_VERSION.yaml` and its required package trees;
- all `CORE/*.md` plus required RULES routing files can be found with existing package-root paths;
- `TOOLS/init_campaign.py` runs from the extracted package and creates the expected campaign-root scaffold.

### Destination-template tests

- exact `TEMPLATE/STORAGE_README.md` can be treated as storage-root `README.md` without broken relative links;
- generated `CAMPAIGN/README.md` and other copied Markdown are validated at their campaign destination paths;
- no destination-relative Markdown link contains an accidental development source prefix such as `GAME/` or `DEV/`;
- campaign generation still places `MANIFEST.yaml`, `README.md`, `STATE/`, `WORLD/`, and other scaffold content at campaign branch root.

### Release workflow

- tag/version mismatch fails before asset publication;
- builder failure prevents release asset publication;
- successful tag build produces the expected runtime asset name;
- workflow publishes the builder output rather than GitHub's source archive.

## Documentation updates

Update at least:

- root `README.md` to explain `GAME/` versus `DEV/` and point installation to the custom runtime release asset;
- `GAME/INSTALL/README.md` and `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` to replace Source code ZIP installation language with the custom runtime asset;
- `DEV/RELEASE/CHECKLIST.md` and `DEV/RELEASE/VERSIONING.md` where paths/release semantics changed;
- `AGENTS.md` for new development tool paths and the explicit source/runtime boundary;
- relevant development architecture/test documents that name moved paths.

Do not add `GAME/` prefixes to runtime-local path instructions merely to reflect the development repository layout.

## Error handling and failure policy

Release construction is fail-closed. If package classification, metadata coherence, template destination validity, legal-copy identity, scaffold generation, or archive validation is uncertain or incorrect, the builder exits non-zero and no runtime release asset is published.

The GitHub workflow must surface the builder's actual failure output. It must not repair, synthesize or silently omit files to make packaging succeed.

Normal gameplay behavior must not gain dependency on GitHub Actions, development audit tools or the source repository layout.

## Migration strategy

This is a large path migration and should be implemented as one coherent feature-branch operation with staged verification, not as a series of partially usable releases.

Recommended implementation sequence:

1. add regression expectations for new boundaries and build output;
2. create `GAME/` and move runtime/install/template/schema/campaign content;
3. split runtime versus development tools;
4. create `DEV/` and move architecture/tests/release/catalog/mechanical schemas/superpowers material;
5. delete deprecated `TEMPLATE/CAMPAIGN_MANIFEST.yaml`;
6. update development-facing repository paths without altering package-root semantics inside `GAME/`;
7. update maintenance audit/root detection;
8. implement and test canonical `DEV/TOOLS/build_release.py`;
9. update install/release documentation from Source code ZIP to custom runtime asset;
10. add tag-triggered GitHub Actions publishing wrapper;
11. build a real ZIP locally/from CI, extract it, and run package/runtime/template/scaffold smoke checks;
12. run the complete maintenance audit against the final source tree.

No release tag should be cut from an intermediate state of this migration.

## Non-goals

This change does not:

- implement the mechanical runtime;
- make current `DEV/CATALOG/` or `DEV/SCHEMAS/` part of gameplay;
- redesign campaign/storage schemas;
- redesign gameplay CORE logic;
- change persistence transaction semantics;
- change campaign branch layout;
- copy engine files into campaign-storage repositories;
- introduce permanent Git branches for game versus development;
- remove GitHub's automatically generated source archives from the Release UI;
- require gameplay to know the source repository has `GAME/` and `DEV/` directories.

## Success criteria

The migration is complete when all of the following are true:

1. the source repository has clear `GAME/` and `DEV/` directory-tree boundaries;
2. `GAME/` alone is a complete source tree for the installed HDM package;
3. current mechanical `CATALOG/` and plural `SCHEMAS/` are development-only under `DEV/`;
4. deprecated `TEMPLATE/CAMPAIGN_MANIFEST.yaml` is removed;
5. package-local runtime instructions use package-root paths without `GAME/` prefixes;
6. development docs/tools use explicit source-tree paths where appropriate;
7. copied storage/campaign templates validate against their destination layouts and do not leak source-tree prefixes;
8. `DEV/TOOLS/build_release.py` is the sole package-composition authority;
9. a tag-triggered GitHub Action invokes the builder and publishes its ZIP as a custom Release Asset;
10. installation documentation points to the custom runtime asset, not Source code ZIP;
11. extracted runtime ZIP contains no development-only trees/tools and can bootstrap/generate a campaign using existing package-root conventions;
12. maintenance/regression verification passes on the final source tree and built runtime package.
