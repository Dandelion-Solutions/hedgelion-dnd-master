# Engine Release Updates

framework_module_version: 0.5.6
load_when: storage-owner startup/resume, explicit engine-update request, safe maintenance opportunity

## Distribution model

Canonical public engine repository:
`Dandelion-Solutions/hedgelion-dnd-master`

Public `main` is development state.

Gameplay engine FILES come from a local D&D Master release ZIP. Campaign storage does not contain an engine copy.

GitHub release/tag metadata may be queried to discover a newer published release, but discovering a tag does not install its files. The user supplies the corresponding release ZIP to Project Sources/current chat.

## Authority

Only authenticated storage repository owner may:
- change storage baseline metadata;
- perform normal release-discovery prompts for that storage;
- approve/perform campaign engine migrations as storage maintenance.

A guest Master:
- does not modify storage metadata;
- does not govern engine updates;
- continues only with an exact engine package matching the campaign, or observes read-only if other access rules permit.

Campaign creator/player decisions required by a migration remain creator/player authority; storage ownership does not grant fictional agency.

## Version metadata

Storage v2:

`DND_STORAGE.yaml -> engine.baseline_version`

This is the approved default version for new campaigns.

Campaign manifest retains exact provenance:
- `base_tag` / `base_sha`
- `integrated_tag` / `integrated_main_sha`
- `update_policy`

A storage baseline may be newer than a campaign. That is valid.

For published releases SHA fields record exact tag commit provenance. Explicit engine-owner development campaigns may use `dev-v<version>` with nullable SHA fields.

## Update opportunities

Engine maintenance is event-driven, never per-turn polling. For a storage-owner Master, consider updates only at safe opportunities:
- new gameplay chat/session startup or resume after meaningful pause;
- explicit engine-update request;
- owner maintenance boundary;
- live-epoch rollover after durable compaction and before successor opening, when no other active live epoch blocks global maintenance.

Guest Masters perform no release check.

## Public release discovery

Valid tags follow `RELEASE/VERSIONING.md`. A newer GitHub tag is metadata only until the corresponding local ZIP is available.

If a newer valid tag exists but its release ZIP is not available locally:
1. tell the owner a new release is available;
2. ask them to download GitHub Release **Source code (zip)** and add/attach it;
3. do not attempt to clone/pull/copy the engine from GitHub;
4. do not change storage/campaign engine metadata yet.

Never use untagged public `main` as a normal player release.

## Local package validation

Before adopting local target engine T:
1. read local `ENGINE_VERSION.yaml`;
2. validate version/recommended tag coherence;
3. for normal published releases resolve public tag to exact source commit SHA;
4. respect `campaign_update.compatibility`;
5. ensure selected target is one coherent package, not mixed files from archives.

### Development package

If local `release_status: development`:
- allow only explicit framework testing when authenticated GitHub login equals local `engine_owner_login`;
- identify package as `dev-v<engine_version>`;
- campaign SHA fields may be null;
- do not query or pin current public `main` solely to manufacture development provenance;
- never offer this package to normal users as a published release.

## Ask and auto policy

`update_policy: ask` is the default for a campaign.

When storage owner is operating that campaign and a newer locally available valid release can be adopted, offer:
- `Update`;
- `Not now`;
- `Always update automatically`.

`Not now` is session-local deferral, not a permanent ignored-version list.

`update_policy: auto` allows automatic maintenance only at safe boundaries and only when the target package is locally available and all authorization/compatibility/concurrency gates pass. If migration/conflict requires a human decision, defer and ask rather than guessing.

## Safety gates

Before baseline/migration work as applicable:
- no unresolved player action/adjudication;
- persist required dirty gameplay state first;
- no authoritative active live epoch when global migration would invalidate it;
- validate repository role/owner identity;
- pin relevant storage/campaign HEADs;
- use optimistic concurrency and never force-push;
- maintenance_required or missing/unknown compatibility blocks blind auto.

## Phase A — storage baseline metadata

If storage owner approves local engine version T for new campaigns:
1. pin storage default-branch HEAD;
2. update only `DND_STORAGE.yaml -> engine.baseline_version` to T;
3. publish one coherent non-force metadata commit.

No engine files are copied to storage. No unrelated storage files are deleted/replaced.

## Phase B — campaign engine adoption

Existing campaign adoption changes campaign DATA/metadata, not engine-owned file paths.

Before migration:
- persist required dirty gameplay state;
- ensure no blocking active live epoch;
- pin campaign HEAD;
- resolve current vs legacy campaign layout;
- validate target compatibility/migrations;
- load only migration/schema files required from the local target package.

Prepare one campaign maintenance batch:
- apply explicit required data/schema migrations through resolved campaign paths;
- preserve all unrelated campaign canon;
- update manifest integrated engine identity to T;
- keep immutable base provenance;
- never copy CORE/RULES/SCHEMA/INSTALL files into campaign branch.

Published target stores tag + exact public tag SHA. Authorized development target may store dev tag + null SHA.

Do not relocate a legacy `CAMPAIGN/` layout merely because engine version changes unless an explicit migration defines that layout conversion.

Publish with optimistic non-force semantics. If HEAD moved, refresh affected state and re-evaluate.

## Engine mismatch at startup

If campaign integrated engine != current local package:
- do not silently use the wrong engine;
- prefer loading the exact matching package;
- owner may choose an authorized upgrade if target is newer and compatible;
- guest must supply/use matching package rather than upgrading storage/campaign.

## Partial success

Storage baseline metadata update and campaign migration are separate durable boundaries.

If baseline moves to T but campaign migration is deferred/fails, keep baseline at T and campaign on old release. Do not rollback merely to equalize versions.

## After successful campaign update

Only after campaign publication succeeds:
- repin campaign HEAD;
- switch runtime to the exact local target package;
- invalidate the entire old engine instruction cache;
- rebuild the COMPLETE target-package CORE context cache once: all local `CORE/*.md` plus `RULES/INDEX.md` and `RULES/README.md`;
- treat `RUNTIME.md`, `AI_REASONING.md`, and `PLAY_POLICY.md` as always-active and all other preloaded CORE modules as activation-gated under the new package;
- reread only campaign records touched by migration, keeping unrelated campaign WORLD/STATE/INDEX/LOG data lazy.

Do not continue adjudication on a mixed old/new engine context. Do not reload only a hand-picked subset of CORE after an engine switch.

Never claim update success before GitHub publication succeeds. Technical maintenance must not fabricate fictional elapsed time/events.
