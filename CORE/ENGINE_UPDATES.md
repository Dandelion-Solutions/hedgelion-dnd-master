# Engine Release Updates

framework_module_version: 0.1.2
load_when: gameplay startup/resume, explicit engine-update request, safe engine maintenance opportunity, tagged release integration

## Release authority

A campaign updates only from published engine release tags. `main` HEAD is development state and MUST NOT be treated as an available campaign update merely because it contains newer commits.

From the campaign runtime side, release discovery against engine tags and `main` is read-only. A campaign Master may read tags, release metadata, ancestry and comparisons needed to select a release, but it never publishes changes to the engine repository or `refs/heads/main`.

Valid engine release tags follow `RELEASE/VERSIONING.md` (`vMAJOR.MINOR` with an optional prerelease suffix). Ignore legacy/non-engine tags for automatic discovery.

At an update opportunity, list release tags once. A candidate release is usable only when:
- the tag resolves to an engine release commit on the normal release line;
- `ENGINE_VERSION.yaml` read at that exact tag is coherent with the tag (including `recommended_tag` when present);
- the target release is a forward descendant of the campaign's currently integrated release source; ambiguous/non-linear ancestry is maintenance, not automatic update.

Do not infer a release from untagged commits. Do not merge current `main` when applying an update; integrate the exact selected tag commit.

## Campaign update metadata

`CAMPAIGN/MANIFEST.yaml -> engine` tracks:
- `base_tag` / `base_sha`: immutable origin release from which the campaign was created;
- `integrated_tag`: most recent published engine release actually integrated into this campaign;
- `integrated_main_sha`: exact engine source commit targeted by `integrated_tag` (kept for precise provenance/backward compatibility with existing manifests);
- `update_policy`: `ask` or `auto`.

New campaigns initialize `integrated_tag == base_tag`, `integrated_main_sha == base_sha`, and `update_policy: ask`.

For an older campaign missing `integrated_tag` or `update_policy`:
- default policy is `ask`;
- derive `integrated_tag` only when the existing engine SHA can be matched unambiguously to a valid release tag, or when `integrated_main_sha == base_sha` and `base_tag` is valid;
- if the installed release cannot be determined safely, do not auto-update. Require one bounded maintenance adoption instead of guessing.

## Who may update

Engine version and update policy are campaign-global maintenance state. Only the campaign creator may change `update_policy` or integrate an engine release.

In multiplayer, non-owner Masters continue using the campaign's currently integrated engine and do not prompt their players to choose a campaign-wide engine policy.

## Update opportunities

Engine release discovery is event-driven, never time-polled.

Perform a release-tag check only at a safe opportunity such as:
- new gameplay chat/session startup or resume after a meaningful pause;
- an explicit user request to check/update the engine;
- creator-owned campaign maintenance;
- a live-epoch rollover boundary, after durable compaction and before opening a successor epoch, but only when the campaign is otherwise safe for a global engine update.

Do not query release tags every turn, every message, every Git sync, or on a wall-clock timer. Ordinary campaign HEAD synchronization is unrelated to engine release discovery.

A long uninterrupted play segment may remain on its current release until the next update opportunity. This is preferable to adding release checks to the hot path.

## Ask policy

`update_policy: ask` is the default.

When a newer valid release tag is discovered and the creator is present, ask one concise maintenance question with these choices:
- `Update` — attempt the safe update at this opportunity;
- `Not now` — continue on the current release;
- `Always update automatically` — persist `update_policy: auto` and use automatic updates at future safe opportunities.

`Not now` is not a permanent rejection. Remember the deferred target only in the current gameplay/session working context so the same tag is not offered repeatedly during ordinary play. Offer it again at a later startup/resume or explicit maintenance/update opportunity. A newly published newer tag may be offered when next discovered.

Do not create a permanent ignored-version list unless the user explicitly requests such a feature in the future.

## Auto policy

`update_policy: auto` means: automatically integrate a newer tagged release when and only when the update can be proven safe at a maintenance boundary.

Auto mode must defer rather than force an update when:
- there is an unresolved player action/adjudication;
- gameplay state is dirty and has not yet been safely persisted;
- any authoritative live epoch in the campaign is still active;
- the current campaign HEAD moved during update preparation;
- the release declares or implies maintenance/migration that cannot be safely applied automatically;
- campaign-local modifications overlap engine-owned paths changed by the release;
- release ancestry/version identity is ambiguous;
- required authorization or repository state cannot be established.

A deferred automatic update does not block ordinary safe gameplay on the currently integrated release. Retry only at a later update opportunity.

If auto mode encounters a migration/conflict that requires a human decision, stop automatic integration and ask the creator at a safe boundary. Never silently guess through a schema migration or semantic conflict.

## Release compatibility marker

A tagged release may declare `ENGINE_VERSION.yaml -> campaign_update.compatibility`:
- `compatible`: normal automatic integration is permitted when all other safety checks pass;
- `maintenance_required`: automatic integration is not permitted; use bounded maintenance/migration;
- missing/unknown: treat conservatively as maintenance-required for auto mode.

Tag existence is what publishes the release. Untagged `ENGINE_VERSION.yaml` changes on `main` do not make a release available to campaigns.

## Safe integration preparation

Before integrating a tagged release:
1. pin current campaign HEAD `C` and confirm creator authorization;
2. persist any required dirty gameplay state so the campaign has a clean durable frontier;
3. ensure no authoritative live epoch remains active anywhere in the campaign; if shared play continues, compact/close first and delay successor opening until the update decision is complete;
4. resolve target release tag to exact commit `T` and validate release metadata;
5. compare the currently integrated release source to `T` to obtain only engine changes introduced by the release;
6. inspect whether the campaign has independently modified any engine-owned path touched by the release;
7. if a touched engine-owned path has a campaign-local modification, use bounded semantic maintenance instead of blind overwrite;
8. treat populated `CAMPAIGN/**` as campaign-owned data. Do not replace real campaign state with the empty/template `CAMPAIGN/` tree from the release. Changes to existing campaign data occur only through explicit compatible metadata updates or a defined migration.

Normal engine-owned paths include CORE, RULES, SCHEMA, INSTALL/runtime infrastructure, RELEASE metadata, architecture/tests/templates and other framework files outside populated campaign data.

Do not scan campaign history broadly. Use tag-to-tag changed paths plus the smallest campaign compare needed to detect overlap on those engine paths.

## Publishing the update

A successful engine update is one coherent campaign maintenance commit. Its publication target is the selected campaign branch only.

Build the resolved tree from:
- current campaign-owned state at `C`;
- engine-owned files from exact tagged release `T`;
- any explicitly safe migration/metadata delta;
- updated manifest engine metadata (`integrated_tag`, `integrated_main_sha`, and policy when changed).

Prefer a merge-style commit whose first parent is current campaign HEAD `C` and whose additional parent is tagged release commit `T`. This preserves provenance without merging arbitrary untagged `main` state.

Use a human-readable message such as:
`engine: update <old-tag> -> <new-tag>`

Publish with optimistic fast-forward semantics only. If campaign HEAD moved after preparation, do not force-push and do not publish the stale prepared tree; refresh the affected state and retry/re-evaluate at a safe boundary.

A campaign Master never publishes engine fixes, campaign merges, or campaign state back to `main`. Engine maintenance on `main` is a separate engine-maintainer operation governed by `ARCHITECTURE/ACCESS_CONTROL.md` and the runtime write-routing guard.

Blobs/trees/unattached commits created before a failed ref update are non-authoritative and may be ignored/cleaned later.

## After successful integration

Only after the campaign branch write succeeds:
- consider the new release installed;
- set working campaign HEAD to the successful update commit;
- invalidate cached engine/CORE/rule/bootstrap content that may have changed;
- reload `BOOTSTRAP_RUNTIME.md`, `CORE_INDEX.md`, `RUNTIME.md`, `AI_REASONING.md`, and only situational modules required before the next adjudication;
- preserve safe conversational context and unchanged campaign-world working context when no migration invalidated it;
- if migration changed campaign records, reread only the affected state before continuing.

Never claim an engine update succeeded until the campaign branch actually points to the completed update commit.

Automatic update success does not need to interrupt player-facing narration. If maintenance materially delays/blocks play or requires a decision, communicate it briefly and technically; never invent fictional downtime to hide it.
