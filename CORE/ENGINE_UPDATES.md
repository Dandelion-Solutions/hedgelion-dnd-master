# Engine Release Updates

framework_module_version: 0.6.0
load_when: storage-owner startup/resume, explicit engine-update request, safe maintenance opportunity

## Distribution model

Canonical public engine repository: `Dandelion-Solutions/hedgelion-dnd-master`.

Public `main` is development state. Gameplay engine files come from a local D&D Master release ZIP. Campaign storage contains no engine copy.

GitHub release/tag metadata may discover a newer published release, but discovering a tag does not install files. The user supplies the matching ZIP.

## Authority

Only authenticated storage owner may change storage baseline metadata or perform normal campaign engine maintenance. Guest Masters do not govern owner updates.

Campaign/player decisions required by a migration remain campaign/player authority; storage ownership does not grant fictional agency.

## Version metadata

Storage v2: `DND_STORAGE.yaml -> engine.baseline_version`.

Campaign manifest keeps base/integrated engine provenance + update policy. Published releases use exact tag SHA; authorized owner development packages may use `dev-v<version>` with nullable SHA.

## Update opportunities

Maintenance is event-driven, never per-turn polling. Consider it only at startup/resume, explicit request, owner maintenance boundary, or safe live-epoch rollover boundary.

Guest Masters perform no release check.

## Public release discovery

If a newer valid tag exists but matching ZIP is absent:
1. tell owner a new release exists;
2. request GitHub Release Source code ZIP;
3. do not clone/pull/copy engine source;
4. do not change storage/campaign metadata yet.

Never use untagged public `main` as a normal player release.

## Local package validation

Before adopting target T:
1. read local `ENGINE_VERSION.yaml`;
2. validate version/recommended-tag coherence;
3. for a published release resolve tag to exact source commit SHA;
4. respect compatibility/migration metadata;
5. ensure one coherent package, never mixed archives.

Development package use is owner-only explicit testing; identify as `dev-v<engine_version>`, allow nullable SHA, and never pin current public main merely to manufacture provenance.

## Ask / auto

Default `update_policy: ask`. When a newer locally available valid target can be adopted, offer Update / Not now / Always update automatically.

Auto runs only at safe boundaries with local target available and all authorization/compatibility/concurrency gates passing. Human-required migration choices defer rather than guess.

## Safety gates

Before maintenance as applicable:
- no unresolved player action;
- persist required dirty gameplay state first;
- no blocking active live epoch;
- validate repository role/owner identity;
- pin relevant storage/campaign frontiers;
- use `PERSISTENCE.md` transport discipline;
- never force-push;
- maintenance_required/unknown compatibility blocks blind auto.

## Phase A — storage baseline metadata

Baseline update is its own `STORAGE_METADATA_SINGLE` transaction on the storage default branch:
1. pin/validate storage metadata state as needed;
2. update only `DND_STORAGE.yaml -> engine.baseline_version`;
3. publish one independent one-file metadata commit through the permitted storage metadata profile.

No engine files are copied. No campaign ref is mutated inside this transaction.

A baseline update and campaign migration are separate durable transactions; success of one does not imply success of the other.

## Phase B — campaign engine adoption

Campaign adoption changes campaign DATA/metadata, not engine files.

Before migration:
- persist normal dirty gameplay state to a clean durable frontier;
- ensure no blocking live epoch;
- resolve current/legacy layout;
- validate target package/migrations;
- establish the campaign `known_head_sha` and required base tree/frontier;
- load only migration/schema files needed from local target package.

Prepare the complete migration delta in memory: schema/data migrations through resolved campaign paths + manifest integrated-engine provenance update, preserving unrelated canon.

Publish that delta as ONE `CAMPAIGN_TREE_TXN` under `PERSISTENCE.md`. Do not use Contents API campaign writes before/inside/after the same migration transaction. Do not create remote staging files.

If the pre-commit optimistic ref check finds campaign HEAD moved, abort before creating the stale commit, refresh only affected records, and rebuild. If the final non-force ref update loses the narrow race, invalidate/rebuild; never force.

Do not relocate legacy layout unless an explicit migration defines that conversion.

## Engine mismatch at startup

If campaign integrated engine != local package, do not silently run wrong engine. Prefer exact matching package; owner may choose authorized migration; guest must supply matching package.

## Partial success

Storage baseline and campaign migration are separate boundaries.

If baseline moves to T but campaign migration is deferred/fails, keep baseline at T and campaign on old release. Do not roll back merely to make versions equal.

## After successful campaign update

The created migration commit/tree are already the new known campaign frontier. Do not immediately refetch the branch or unchanged campaign records merely to confirm the runtime's own successful publication.

Then:
- switch runtime to exact local target package;
- invalidate entire old engine instruction cache;
- rebuild COMPLETE target CORE context once: all `CORE/*.md` + `RULES/INDEX.md` + `RULES/README.md`;
- reapply target package's header-driven activation policy from `PLAY_POLICY.md` (`load_policy: ALWAYS_DURING_GAMEPLAY` vs `load_when:`);
- reread only campaign records genuinely changed/required by migration if they are not already represented by the prepared final working set.

Do not adjudicate with mixed old/new engine context.

Never claim update success before the relevant GitHub publication succeeds. Technical maintenance must not fabricate fictional elapsed time/events.