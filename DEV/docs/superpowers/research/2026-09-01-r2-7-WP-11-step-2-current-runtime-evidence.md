# R2.7 WP-11 Step 2 — Current Runtime Route Evidence

Status: **EVIDENCE SLICE COMPLETE — NO TOPOLOGY DECISION**

## Source scope

This slice inspected every `GAME/` source in WP-11 Source Manifest section 5.3:
the storage, persistence, identity, integrity, session, multiplayer, live,
chronology, bootstrap, campaign and information/narrative contracts; campaign
generator; all listed campaign schemas, roots/templates and ten index templates.
The current template establishes some fixed roots and generic index payloads, but
it does not establish a full high-cardinality topology.

## Current machine facts

| Family or route | Evidence and qualifier | Step-2 disposition |
|---|---|---|
| Storage repository | Root `DND_STORAGE.yaml` identifies a new campaign-storage repository only. It does not select an existing campaign runtime. | Fixed discovery marker; not a campaign-branch record family. |
| Campaign root | `MANIFEST.yaml` is the root-layout discriminator and selects `STATE`, `INDEX`, `WORLD`, `LOG` and `CHECKPOINTS`. The generator template has null campaign identity before initialization. | Fixed singleton route; branch, template and storage-default remain separate lifecycles. |
| Config and card | `CONFIG.yaml` is campaign-scoped preference/boundary data with no independent ID. `CAMPAIGN_CARD.yaml` is a compact projection and must change with source state, but is neither canon nor access/engine authority. | Fixed singleton routes; no index or shard family follows. |
| Current state | `STATE/CURRENT.yaml` supplies a compact current-routing summary, including active scene IDs and paths. It is neither Scene detail nor total chronology. | Fixed singleton route; path is routing evidence only. |
| Scene | `scene_id` identifies a durable canonical Scene record with chronology frontier, live-epoch linkage and absorption state. `STATE/SCENES/` and `SCENE_INDEX.yaml` are placeholders; no filename, ID grammar or shard arithmetic exists. | Separate native family requiring route/index decision. |
| Live scene | A live epoch is a temporary branch-local operational overlay at `live/<campaign-technical-id>/<scene_id>/<epoch_id>` with `LIVE/LIVE_STATE.yaml`; `epoch_id` derives from Scene plus opening campaign SHA. | Separate conditional operational partition; it does not replace canonical Scene or require a campaign index. |
| PC, NPC, Faction, Item, Location, Lore, Player and Thread | Each has a current template root, `id` or `player_id` schema identity, and an empty generic monolithic index. No route formula, sharding rule or ID grammar is currently supplied. Location, player, lore, item and relationship-like fields retain their owner-specific qualifiers. | Each is a native family requiring its own physical disposition; an index route cannot disclose secrets, grant authority or make omission semantic absence. |
| Event / LOG | Event schema has string identity and optional local `world_order`; `LOG/_TEMPLATE.yaml` is compact semantic history. `EVENT_INDEX.yaml` exists, but the template provides no event-record root, filename mapping or index-entry binding. | Native history/evidence route is a material physical mapping gap, not evidence that LOG itself is a transaction journal or total clock. |
| Checkpoint | `CHECKPOINTS/_TEMPLATE.yaml` and checkpoint schema define sparse immutable recovery descriptors with an ID and optional exact commit/event references. | Native evidence family requiring a bounded route; no index or current-state authority. |
| Session | `SESSIONS/_TEMPLATE.yaml` and session schema define coordination metadata with `session_id` and source-head fields. `SESSIONS` is not selected by current MANIFEST roots. | Native coordination family; manifest-routing omission is a current machine gap requiring a WP-11 disposition, not a license to make session write authority. |
| Monolithic indexes | Ten `*_INDEX.yaml` files hold `schema_version`, `entity_type` and generic entries (`id`, name/aliases/status, `path`, optional parent/tags/last event). | Fixed index filenames and payload ceiling are evidence; they do not establish size bound, eligibility policy, rebuild source, authoritative absence or shard arithmetic. |
| No native template family | The runtime sources do not establish standalone campaign families for knowledge, disclosure, Story, Context Runtime controls or generic pending work. | Explicit no-native-family result, preserving existing owners and conditional/dormant qualifications. |

## Machine-to-architecture findings

1. Existing roots and indexes are scaffolding with no presumption that they
   already realize bounded lookup. Their missing route/rebuild/eligibility rules
   are WP-11 mapping work, not an accepted topology.
2. `SCENE` and `LIVE` are distinct: the former is durable canonical campaign
   state; the latter is epoch-scoped operational state compacted forward into the
   Scene. A shared path, index or identity rule would contradict both contracts.
3. `SESSIONS/` without a current MANIFEST selector and the `EVENT_INDEX` without
   a native event-record route are current reverse-conformance gaps. Neither
   exposes a semantic-owner conflict.

## Decision-gate check

The current runtime sources leave physical family routes, shard arithmetic and
index rebuild/eligibility policy unselected. They expose no external
compatibility requirement and no human-owned product or semantic-authority
decision.
