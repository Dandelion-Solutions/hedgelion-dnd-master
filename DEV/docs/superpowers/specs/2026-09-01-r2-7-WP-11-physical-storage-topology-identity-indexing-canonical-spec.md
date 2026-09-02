# R2.7 WP-11 — Physical Storage Topology, Identity and Indexing

Status: **CANONICAL — WP-11 CLOSED / SENIOR REVIEW PASS**

## Scope

This specification selects physical campaign-record topology, stable-ID routing
and bounded index rules. It does not change semantic ownership or implement
schemas, templates, runtime behavior, HOT/SQLite, publication, recovery,
bootstrap, migration or tests.

## Route law

For a native record family, semantic identity is its owner-defined simple,
derived, composite or singleton identity. The route input is:

```text
UTF-8("HDM-WP11-ROUTE-V1")
+ 0x00 + UTF-8(family_key)
+ 0x00 + uint32be(component_count)
+ each identity component in owner-defined order as:
  uint32be(byte_length(UTF-8(component))) + UTF-8(component)
```

With `H = lowercase-hex(SHA-256(route_input))`, `E =
unpadded-base32hex(route_input)`, and `E_chunks = split(E, 100 ASCII
characters)`, the route is:

```text
<family-root>/RECORDS/H[0:2]/H[2:4]/<E_chunks[0]>/.../<E_chunks[last]>.yaml
```

The first four hash hex characters select one of 65,536 leaf buckets. The
chunked encoding is injective and supplies the final filename path; the hash is
only a shard selector. Each loaded body must validate its complete native
identity and family against the requested route. A mismatch is an integrity
failure. Paths, shards, index entries and their order are never identity,
chronology, eligibility, currentness or publication authority.

Simple and derived identities use their complete canonical ID as the one
component. Knowledge uses `(knower_id, fact_id)` and Disclosure uses
`(player_id, fact_id)`, in that order.

## Fixed and exceptional routes

| Concern | Route and limit |
|---|---|
| Campaign layout/configuration | `MANIFEST.yaml`, `CONFIG.yaml` fixed singletons. |
| Campaign card | `CAMPAIGN_CARD.yaml`; compact projection only. |
| Current summary | `STATE/CURRENT.yaml`; active-scene entries contain `scene_id` only and derive the route. |
| Campaign allocator | `STATE/ID_ALLOCATOR.yaml`; operational singleton only. |
| LIVE | `live/<campaign-technical-id>/<scene_id>/<epoch_id>/LIVE/LIVE_STATE.yaml`; selected epoch overlay, no campaign index. |
| Story state | `STORY/<layer>/PROJECTION_STATE.yaml`; Story-owned noncanonical progress. |
| Story record | `STORY/<layer>/<floor(sequence/1000)>/<story_id>.yaml`; accepted layer-local sequence route. |

`MANIFEST.storage` selects static `state_root`, `index_root`, `world_root`,
`event_log_root`, `checkpoints_root`, `sessions_root` and `story_root`. It does
not carry mutable Story progress. LIVE is selected by campaign routing plus
epoch claim, never by branch presence.

## Native families

All rows use the route law unless listed above.

| Family key | Root | Index disposition |
|---|---|---|
| `world.scene` | `STATE/SCENES` | `INDEX/SCENE_INDEX.yaml` discovery only. |
| `world.actor` | `WORLD/ACTORS` | PC/NPC indexes may classify Actors; no route subtype. |
| `world.actor_group` | `WORLD/ACTOR_GROUPS` | No baseline discovery index. |
| `world.faction` | `WORLD/FACTIONS` | `INDEX/FACTION_INDEX.yaml`. |
| `world.asset` | `WORLD/ITEMS` | `INDEX/ITEM_INDEX.yaml`. |
| `world.location` | `WORLD/LOCATIONS` | `INDEX/LOCATION_INDEX.yaml`. |
| `world.lore_fact` | `WORLD/LORE` | `INDEX/LORE_INDEX.yaml`; no protected state. |
| `world.player` | `WORLD/PLAYERS` | `INDEX/PLAYER_INDEX.yaml`; never authorization. |
| `world.thread` | `WORLD/THREADS` | `INDEX/THREAD_INDEX.yaml`. |
| `world.effect` | `WORLD/EFFECTS` | No baseline discovery index. |
| `world.connection` | `WORLD/CONNECTIONS` | No baseline discovery index. |
| `world.zone` | `WORLD/ZONES` | No baseline discovery index. |
| `world.organization` | `WORLD/ORGANIZATIONS` | No baseline discovery index. |
| `world.contract` | `WORLD/CONTRACTS` | No baseline discovery index. |
| `world.mission` | `WORLD/MISSIONS` | No baseline discovery index. |
| `world.encounter` | `WORLD/ENCOUNTERS` | No baseline discovery index. |
| `world.hazard` | `WORLD/HAZARDS` | No baseline discovery index. |
| `world.knowledge` | `WORLD/KNOWLEDGE` | No discovery index; direct composite route only after eligibility. |
| `runtime.interaction` | `STATE/RUNTIME/INTERACTIONS` | No baseline discovery index. |
| `runtime.intent_plan` | `STATE/RUNTIME/INTENT_PLANS` | No baseline discovery index. |
| `runtime.command` | `STATE/RUNTIME/COMMANDS` | No baseline discovery index. |
| `runtime.procedure` | `STATE/RUNTIME/PROCEDURES` | No baseline discovery index. |
| `runtime.resolution` | `STATE/RUNTIME/RESOLUTIONS` | No baseline discovery index. |
| `runtime.continuation` | `STATE/RUNTIME/CONTINUATIONS` | No baseline discovery index. |
| `runtime.resolution_trace` | `STATE/RUNTIME/RESOLUTION_TRACES` | No baseline discovery index. |
| `runtime.disclosure` | `STATE/RUNTIME/DISCLOSURES` | No discovery index; direct composite route only after eligibility. |
| `runtime.collaboration_obligation` | `STATE/RUNTIME/COLLABORATION` | Conditional root; no baseline index. |
| `runtime.maintenance_audit` | `STATE/RUNTIME/MAINTENANCE_AUDITS` | No baseline discovery index. |
| `runtime.catalog_gap_report` | `STATE/RUNTIME/CATALOG_GAP_REPORTS` | No baseline discovery index. |
| `runtime.semantic_event` | `LOG/SEMANTIC_EVENTS` | `INDEX/EVENT_INDEX.yaml` compact discovery only. |
| `runtime.mechanical_event` | `LOG/MECHANICAL_EVENTS` | No baseline discovery index. |
| `runtime.message` | `LOG/MESSAGES` | No baseline discovery index. |
| `runtime.checkpoint` | `CHECKPOINTS` | No index; immutable recovery evidence. |
| `runtime.session` | `SESSIONS` | No index; coordination only. |

Definitions remain in resolved catalog sources. Receipts, execution segments,
intent clauses, choices, reactions and temporal bindings remain embedded values.
Context controls, role bundles/traces and single-player Dramaturg state have no
campaign native record; multiplayer Dramaturg remains conditional WP-18 work.

The route law consumes, but does not allocate, canonical IDs. Live-created
Message and execution evidence require the source-native epoch-qualified ID
already required by the live/message owners; WP-16 realizes that identity policy
without a campaign-allocator fallback.

## Index rules

1. A known-ID read calculates one route and never enumerates a directory or
   loads an index.
2. Discovery loads only the expected family index, selects an eligible compact
   entry, loads its exact path, then validates identity and eligibility again.
3. Entries use only owner-approved non-secret compact routing fields: ID, name,
   aliases, status, path, parent ID, tags and last-event ID. They contain no
   record body, private continuity, knowledge, disclosure, Story availability,
   live claim or authorization grant.
4. Each current discoverable record has at most one entry per family index;
   aliases never redefine identity. Record and required index update share a
   publication closure; an invalid index rebuilds from its native family.
5. Indexes are non-authoritative and cannot prove semantic absence. Only a
   separately owner-proven complete protection route can support cleanup.
6. `*_INDEX.yaml` stays monolithic by family. Only WP-24 measured size,
   transfer-latency or host/tool-limit evidence may select index partitioning,
   while preserving this authority and direct-route law.

## Forward obligations and traceability

| ID | Target | Required discharge evidence |
|---|---|---|
| WP-11/F01 | WP-12 | Route-law hydration and derived-index separation. |
| WP-11/F02 | WP-13 | Atomic native-record plus required-index publication closure. |
| WP-11/F03 | WP-14 | Current-route-first recovery and deterministic index rebuild. |
| WP-11/F04 | WP-16 | Source-native, epoch-qualified live identity materialization. |
| WP-11/F05 | WP-19 | Scaffold, fixed index files and new MANIFEST root selectors. |
| WP-11/F06 | WP-20 | Pre-release path/schema/template migration preserving IDs/currentness/history. |
| WP-11/F07 | WP-22 | Route, shard, index, stale-path and no-directory-enumeration regression cases. |
| WP-11/F08 | WP-24 | Measured monolithic-index and host/tool-budget assessment. |

## Decision and risk record

**Decision:** deterministic family-local routing uses a framed identity encoding,
two-level SHA-256 bucket selection and injective encoded filenames; Story and
LIVE retain their accepted exceptional routes.

**Risk:** stale path/index metadata could be mistaken for authority.
**Mitigation:** derive known-ID routes, revalidate loaded body and eligibility,
rebuild helpers from native families, and prohibit index-absence proof.

**Risk:** live identity allocation is not yet materialized.
**Mitigation:** F04 blocks its realization on the existing source-native live-ID
requirements; WP-11 neither falls back to the campaign allocator nor selects
ID syntax.
