# Canonical Storage and Persistence

framework_module_version: 0.5.7
load_when: session startup, state retrieval, persistence boundary, resync, canon conflict

The engine package and campaign storage are separate.

- Engine/runtime/schema/rules are read from the locally extracted D&D Master release archive.
- Persistent campaign canon lives only in the selected GitHub campaign-storage repository.
- Chat context is temporary working memory.
- ChatGPT Memory is never campaign storage.

## Storage repository metadata

A campaign-storage repository is discovered by exact root `DND_STORAGE.yaml` on its default branch.

Storage v2 marker records repository role and the owner-approved baseline engine VERSION for new campaigns:

```yaml
storage_format_version: 2
repository_role: campaign_storage
engine:
  baseline_version: "<version>"
```

Marker existence is sufficient for discovery; do not infer storage from repository name.

Storage default branch does NOT contain or need a copy of CORE/RULES/SCHEMA/INSTALL.

`baseline_version`:
- is a default/maintenance pointer;
- does not itself install an engine;
- does not automatically change existing campaigns.

Campaign branches contain campaign data only. They do not depend on `DND_STORAGE.yaml` for gameplay canon.

Legacy v1 storage may still contain copied engine files. Treat those paths as inert legacy storage data, never as runtime source.

## Campaign data layout

Current campaign branches store their data directly at branch root. Root `MANIFEST.yaml` is the current-layout discriminator and its `storage.*` fields route STATE/INDEX/WORLD/LOG/CHECKPOINTS.

Legacy campaigns may store the logical campaign tree under `CAMPAIGN/` and have `CAMPAIGN/MANIFEST.yaml`.

Bootstrap resolves one layout before gameplay. Once resolved, use manifest storage roots for all records. New current-layout writes MUST NOT create a `CAMPAIGN/` wrapper. Opening a legacy branch is not permission to relocate it.

The local engine `CAMPAIGN/` directory is a template source only and is not a remote campaign path.

## Campaign write authorization

Before game-state writes determine campaign creator from Git history: `author.login` of the first campaign-specific initialization commit.

- singleplayer: creator-only writes;
- multiplayer: active player bindings according to multiplayer rules;
- mode/join-policy changes: creator-only;
- storage metadata maintenance: authenticated storage repository owner only.

Repository permission is necessary but not sufficient.

## Authenticated player binding

For multiplayer, resolve authenticated GitHub identity and map stable GitHub user ID to exactly one active `PLAYER_` record. Canonical semantic actor identity is campaign `player_id`, not mutable GitHub login.

## Canonical read order

Project Instructions -> local release launcher/runtime bootstrap -> campaign MANIFEST -> local current CORE -> latest checkpoint/hot STATE -> exact WORLD records -> bounded LOG -> current chat -> older chats as recovery evidence only.

When a scene has an active live epoch, `LIVE_SCENE.md` inserts that operational frontier between durable campaign state and narration/adjudication.

## Stable IDs and lazy retrieval

Resolve through INDEX files, fetch exact records, and load only dependencies required for the current decision. Never recursively load the whole entity graph.

Stable-ID reservation remains a HARD persistence boundary: publish record + required index before relying on the ID as durable canon.

## Lightweight repository reads

Treat GitHub campaign storage as a versioned current-state store, not a repository to clone/pull.

Each working set has a campaign `base_head_sha`.

Routine sync:
1. fetch active campaign branch ref;
2. if unchanged, stop;
3. if changed, compare base..HEAD server-side;
4. intersect changed paths with loaded/dirty/decision/access dependencies;
5. fetch only relevant exact files pinned to one HEAD;
6. advance base HEAD.

Do not download whole campaign archives or broad history merely to learn current state.

The fact that the engine is fully extracted locally does not change this campaign-data lazy-read policy.

## Environment-level partitioning

Prefer separate files for independently changing scene/PC/NPC/location/item/faction/thread/session/log records. The resolved `STATE/CURRENT.yaml` is compact routing state, not transcript.

## Operational live canon

Active live-scene rules remain as defined by `LIVE_SCENE.md`: one temporary operational frontier, later compacted into durable campaign state, never blindly duplicated turn-by-turn.

Any legacy `CAMPAIGN/LIVE/...` notation in older runtime text is resolved through the selected campaign root; current layout uses `LIVE/...`.

## Consistency tiers

- HARD: canonical commitment whose loss would materially break resumed state; publish at the logical action boundary.
- SOFT: durable state that may remain briefly dirty until the next persistence boundary.
- EPHEMERAL: current-chat context only unless later promoted.

## Working set and persistence

Keep only relevant canonical records plus internal dirty paths/facts.

Publish normal campaign batches at natural boundaries: scene/combat/travel completion, pause/end, substantial durable bundle, accepted setup phase, explicit save, risky transition.

One durable batch should normally be one Git commit.

## Concurrent campaign HEAD change

Before publishing:
- if HEAD unchanged, publish normally;
- if changed, compare paths;
- disjoint changes may be rebased/rebuilt on latest HEAD;
- structurally independent shared-index entries may merge;
- same-entity conflicts require targeted semantic reconciliation;
- incompatible changes cause re-adjudication from latest canon.

Never force-update live campaign or live-scene refs.

## Event log and checkpoints

LOG is compact semantic history, not transaction journal/transcript. Create checkpoints at session boundaries, major transitions and before risky migrations/maintenance.

Checkpoint paths are layout-relative; new campaigns use root-layout paths such as `STATE/CURRENT.yaml`, while legacy campaigns retain their existing resolved prefix.

## Canon conflicts

Inspect the smallest relevant records/log/commit range and repair only with evidence. Never invent a reconciliation story.
