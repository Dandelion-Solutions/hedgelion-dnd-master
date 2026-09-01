# R2.7 WP-11 Step 5 — Physical Storage Topology Candidate

Status: **CANDIDATE — PENDING STEP-6 ADVERSARIAL REVIEW**

## 1. Route law

For each native record family, semantic identity remains the owner-defined
simple, derived, composite or singleton identity. The physical route is a
validated projection:

```text
route_input = UTF-8("HDM-WP11-ROUTE-V1")
            + 0x00 + UTF-8(family_key)
            + 0x00 + uint32be(component_count)
            + for each identity component in owner-defined order:
                uint32be(byte_length(UTF-8(component))) + UTF-8(component)

H = lowercase-hex(SHA-256(route_input))
E = unpadded-base32hex(route_input)
E_chunks = split(E, 100 ASCII characters)
sharded route = <family-root>/RECORDS/H[0:2]/H[2:4]/
                <E_chunks[0]>/.../<E_chunks[last]>.yaml
```

Simple and derived identities have one component: their full canonical ID.
`world.knowledge` uses `knower_id`, then `fact_id`; `runtime.disclosure` uses
`player_id`, then `fact_id`. The record body must contain the complete native
identity and must match the requested family/identity after loading. A mismatch,
including a calculated route whose final encoded input does not match the body,
is an integrity failure. `E` is injective for the complete route input; `H` is
only a fixed shard selector and is never a uniqueness authority.

The two two-hex shard components provide 65,536 deterministic leaf buckets.
The hash, bucket and filename are routing only. No implementation may use their
lexical order as identity, chronology, currentness, publication order or
eligibility evidence.

## 2. Fixed and conditional routes

| Concern | Physical route | Qualification |
|---|---|---|
| Campaign layout and configuration | `MANIFEST.yaml`, `CONFIG.yaml` | Fixed campaign singletons. |
| Campaign card | `CAMPAIGN_CARD.yaml` | Compact projection, not authority. |
| Current summary | `STATE/CURRENT.yaml` | Routing/current summary, not Scene/history authority. Active-scene entries retain `scene_id` only; a path is derived from the Scene route and rebuilt on mismatch. |
| Campaign allocator | `STATE/ID_ALLOCATOR.yaml` | Operational singleton; no chronology/index authority. |
| Live epoch | `live/<campaign-technical-id>/<scene_id>/<epoch_id>/LIVE/LIVE_STATE.yaml` | Existing branch-local single-file operational partition; no campaign-family index. |
| Story layer state | `STORY/<layer>/PROJECTION_STATE.yaml` | Story-owned noncanonical progress only. |
| Story record | `STORY/<layer>/<floor(sequence/1000)>/<story_id>.yaml` | Existing accepted Story sequence grouping; layer-local non-reused ID and ordering only. |

`MANIFEST.storage` selects static roots as `state_root: STATE`, `index_root:
INDEX`, `world_root: WORLD`, `log_root: LOG`, `checkpoints_root: CHECKPOINTS`,
`sessions_root: SESSIONS` and `story_root: STORY`. It never carries mutable
Story progress. The live route is selected by current campaign routing and an
epoch claim; branch existence is not authority.

## 3. Native family matrix

Every row below uses the route law in Section 1 unless it is fixed or conditional
above. `RECORDS` is a physical grouping only and does not add an owner.

| Logical/native family | `family_key` | Family root | Index interaction |
|---|---|---|---|
| Scene | `world.scene` | `STATE/SCENES` | `INDEX/SCENE_INDEX.yaml` for compact discovery; exact ID route bypasses index. |
| Actor | `world.actor` | `WORLD/ACTORS` | `INDEX/PC_INDEX.yaml` and `INDEX/NPC_INDEX.yaml` may classify discoverable Actor records; no route discriminator, relationship or continuity contents. |
| Actor group | `world.actor_group` | `WORLD/ACTOR_GROUPS` | No baseline discovery index. |
| Faction | `world.faction` | `WORLD/FACTIONS` | `INDEX/FACTION_INDEX.yaml`. |
| Asset/Item | `world.asset` | `WORLD/ITEMS` | `INDEX/ITEM_INDEX.yaml`; possession/placement remain owner semantics. |
| Location | `world.location` | `WORLD/LOCATIONS` | `INDEX/LOCATION_INDEX.yaml`. |
| Lore fact | `world.lore_fact` | `WORLD/LORE` | `INDEX/LORE_INDEX.yaml`; excludes protected knowledge/disclosure. |
| Player binding | `world.player` | `WORLD/PLAYERS` | `INDEX/PLAYER_INDEX.yaml`; never grants authorization. |
| Thread | `world.thread` | `WORLD/THREADS` | `INDEX/THREAD_INDEX.yaml`; no scheduler implication. |
| Effect/application | `world.effect` | `WORLD/EFFECTS` | No baseline discovery index; condition aggregation remains derived. |
| Connection | `world.connection` | `WORLD/CONNECTIONS` | No baseline discovery index. |
| Zone | `world.zone` | `WORLD/ZONES` | No baseline discovery index. |
| Organization | `world.organization` | `WORLD/ORGANIZATIONS` | No baseline discovery index. |
| Contract | `world.contract` | `WORLD/CONTRACTS` | No baseline discovery index. |
| Mission | `world.mission` | `WORLD/MISSIONS` | No baseline discovery index. |
| Encounter | `world.encounter` | `WORLD/ENCOUNTERS` | No baseline discovery index. |
| Hazard | `world.hazard` | `WORLD/HAZARDS` | No baseline discovery index. |
| Knowledge relation | `world.knowledge` | `WORLD/KNOWLEDGE` | No discovery index; protected subject/fact lookup uses the direct composite route after eligibility. |
| Interaction | `runtime.interaction` | `STATE/RUNTIME/INTERACTIONS` | No baseline discovery index. |
| IntentPlan | `runtime.intent_plan` | `STATE/RUNTIME/INTENT_PLANS` | No baseline discovery index; clauses remain embedded. |
| Command | `runtime.command` | `STATE/RUNTIME/COMMANDS` | No baseline discovery index. |
| Procedure | `runtime.procedure` | `STATE/RUNTIME/PROCEDURES` | No baseline discovery index. |
| Resolution | `runtime.resolution` | `STATE/RUNTIME/RESOLUTIONS` | No baseline discovery index. |
| Continuation | `runtime.continuation` | `STATE/RUNTIME/CONTINUATIONS` | No baseline discovery index; choice/reaction remain embedded. |
| ResolutionTrace | `runtime.resolution_trace` | `STATE/RUNTIME/RESOLUTION_TRACES` | No baseline discovery index; bounded diagnostic evidence only. |
| Disclosure | `runtime.disclosure` | `STATE/RUNTIME/DISCLOSURES` | No discovery index; direct composite route after recipient eligibility. |
| Collaboration obligation | `runtime.collaboration_obligation` | `STATE/RUNTIME/COLLABORATION` | Conditional root; no baseline index. |
| Maintenance audit | `runtime.maintenance_audit` | `STATE/RUNTIME/MAINTENANCE_AUDITS` | No baseline discovery index. |
| Catalog gap report | `runtime.catalog_gap_report` | `STATE/RUNTIME/CATALOG_GAP_REPORTS` | No baseline discovery index. |
| Semantic event | `runtime.semantic_event` | `LOG/SEMANTIC_EVENTS` | `INDEX/EVENT_INDEX.yaml` contains only compact, owner-approved discovery data. |
| Mechanical event | `runtime.mechanical_event` | `LOG/MECHANICAL_EVENTS` | No baseline discovery index; distinct from semantic event history. |
| Retained message | `runtime.message` | `LOG/MESSAGES` | No baseline discovery index; compaction survivor rules remain unchanged. |
| Checkpoint descriptor | `runtime.checkpoint` | `CHECKPOINTS` | No index; immutable recovery evidence, not current authority. |
| Session coordination | `runtime.session` | `SESSIONS` | No index; MANIFEST must route this root without creating write authority. |

Definitions remain in their resolved catalog source and do not acquire a
campaign-root route. Receipts, execution segments, intent clauses, choices,
reactions and temporal bindings remain embedded values. Context controls, role
bundles/traces and single-player Dramaturg state have no campaign native record.
Multiplayer Dramaturg remains a conditional WP-18 concern rather than a route
selected here.

The route law consumes each owner's canonical ID without selecting how it is
allocated. For a live-created Message or other live-created execution evidence,
the live owner must supply the source-native, epoch-qualified ID required by
Steps 5.8 and 5.12; this is a WP-16 identity-materialization obligation, not a
campaign allocator fallback or a WP-11 identity-syntax choice.

## 4. Index rules

1. An ordinary known-ID read calculates exactly one native route. It performs no
   directory listing and need not load a monolithic index.
2. A discovery read loads only the expected family index, selects an eligible
   compact entry, then loads its exact `path`. It must recheck native-record
   identity and caller eligibility.
3. An index entry may contain only the existing compact routing fields
   (`id`, name, aliases, status, path, parent ID, tags, last event ID) when each
   is owner-approved and non-secret-bearing. It contains no body, private
   continuity, knowledge, disclosure, Story availability, live claim or
   authorization grant.
4. One current discoverable record has at most one entry in its family index;
   aliases are aids, not identity. Index membership/update is in the native
   record's publication closure and the index is rebuilt from that family when
   invalid or stale.
5. An index is routing evidence, not writable authority or closed-world negative
   proof. Cleanup may rely on a separately owner-proven complete protection
   route, never a best-effort discovery index.
6. Current `*_INDEX.yaml` remains one monolithic file per family. WP-24 may
   supersede this only on measured size, transfer-latency or host/tool-limit
   evidence; it must preserve stable IDs, direct routes and index authority
   limits.

## 5. Cross-system contract

| Relation | WP-11 allocation | Downstream owner |
|---|---|---|
| HOT/SQLite | Hydrates owner records by the route law or keeps derived query state; format receives no authority. | WP-12 |
| Publication | Includes each changed record and required index entry in one owner-valid closure. | WP-13 |
| Recovery | Resolves current native routes first, then rebuilds indexes/caches; checkpoint/session never override route selection. | WP-14 |
| Live-created identity | Supplies epoch-qualified source-native IDs to the unchanged route law; preserves them through retry/recovery/absorption. | WP-16 |
| Bootstrap | Materializes the selected roots, fixed index files and MANIFEST root selectors. | WP-19 |
| Migration | Converts existing placeholder/scaffold paths to this layout while preserving IDs/history/currentness. | WP-20 |
| Scale | Tests current index payload/lookup behavior and measures any need to partition an index. | WP-24 |

## 6. Non-goals and validation

This candidate neither implements routes nor changes schemas, templates,
catalogs, runtime files, data migration or tests. It also selects no HOT table,
transaction protocol, index API, retention policy, Story schema or live claim.
Its physical decisions are valid only while preserving existing semantic owners,
eligibility, publication/currentness and chronology laws.
