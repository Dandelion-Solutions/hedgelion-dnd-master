# HDM Catalog — Universal Record Contracts

Status: **WORKING PROTOTYPE / READY FOR REVIEW**

Target: `feature/mechanical-runtime-hot-state`

Machine-readable schemas:

- `SCHEMAS/catalog-definition.schema.json`
- `SCHEMAS/world-record.schema.json`

## 1. Scope

This document defines the common envelope shared by reusable catalog
definitions and the common envelope shared by durable or promotable world
records. It does not define actor HP, item ownership, mission stages, or other
kind-specific content. Those structures belong inside `data` or `state` and
are designed next.

The envelope is intentionally small. A field belongs here only when every
consumer needs the same meaning for it.

## 2. Reusable definition envelope

```json
{
  "id": "campaign.moonlace_brooch",
  "kind": "definition.asset",
  "schema_version": 1,
  "origin": "campaign",
  "name": "Moonlace Brooch",
  "facets": ["asset.wearable", "asset.decoration", "asset.artifact"],
  "tags": ["jewelry", "moon"],
  "requires": ["op.create_effect"],
  "extends": "ruleset.brooch",
  "data": {},
  "provenance": {},
  "extensions": {}
}
```

Required fields:

| Field | Contract |
|---|---|
| `id` | Stable ASCII ID, unique in the resolved definition catalog. |
| `kind` | Registered `definition.*` kind selecting the schema for `data`. |
| `schema_version` | Integer version of that kind's data contract. |
| `origin` | `engine`, `ruleset`, `campaign`, or `session`. |
| `name` | Human-facing label; never used as identity. |
| `data` | Kind-specific, schema-validated reusable content. |

Optional fields:

| Field | Contract |
|---|---|
| `facets` | Registered classifiers. They do not grant behavior. |
| `tags` | Search terms with no executable meaning. |
| `requires` | Engine capability IDs that must exist before the definition can load. |
| `extends` | One exact base definition. Multiple inheritance is not supported. |
| `provenance` | Source, authorship, license, or import notes. Non-executable. |
| `extensions` | Namespaced metadata not interpreted by core unless a schema explicitly claims it. |

`requires` contains engine capabilities such as an `op.*` primitive. References
to granted Activities, Effects, Resources, or Rule Elements are kind-specific
relationships and belong in `data`; they are not blurred into `requires`.

## 3. World-record envelope

```json
{
  "id": "asset-00042",
  "kind": "world.asset",
  "schema_version": 1,
  "revision": 7,
  "canonicality": "canonicality.canonical",
  "definition_id": "campaign.moonlace_brooch",
  "facets": ["asset.quest_item"],
  "state": {},
  "overrides": {},
  "provenance": {},
  "extensions": {}
}
```

Required fields:

| Field | Contract |
|---|---|
| `id` | Runtime-allocated identity for this particular record. |
| `kind` | Registered `world.*` kind selecting the schema for `state`. |
| `schema_version` | Integer version of that kind's state contract. |
| `revision` | Monotonic record revision used for conflict detection. Starts at zero. |
| `canonicality` | Registered canonicality class. |
| `state` | Kind-specific current world state. |

Optional fields:

| Field | Contract |
|---|---|
| `definition_id` | Reusable definition from which an instantiable record was created. |
| `facets` | Valid instance-specific facets in addition to inherited facets. |
| `overrides` | Validated instance-specific changes to definition data. |
| `provenance` | Creation/import/promotion context. Non-executable. |
| `extensions` | Namespaced metadata under the same rule as definitions. |

Not every world record has a reusable definition. A lore fact, relationship,
chapter, or timeline marker may be authored directly, so `definition_id` is
optional. A kind-specific schema may require it for a narrower record class.

Durability/publication status is deliberately absent. It describes the
runtime's relationship with storage, not the fictional object. Dirty state,
publication batches, and checkpoint frontiers remain runtime records.

## 4. Reference rules

1. Records store forward references in semantically named kind-specific fields,
   for example `owner_actor_id`; there is no universal `references` bag.
2. A reference stores an ID, not an embedded copy of the target record.
   Small immutable value objects may still be embedded.
3. Persisted backlinks are avoided. SQLite may index reverse relationships as
   a disposable projection.
4. A canonical record may not depend on an ephemeral or session-local record.
   The publication planner must promote the dependency closure or reject the
   publication.
5. Durable referenced records are retired/tombstoned rather than silently
   deleted, and their IDs are not reused.
6. A base definition is single-valued (`extends`). Reusable behavior is
   composed through registered Activities, Effects, Resources, and Rule
   Elements instead of multiple inheritance.
7. Cycles are not generally forbidden, because relationships and location
   connections may naturally be reciprocal. Each kind-specific schema or
   validator must decide whether a cycle is meaningful.

These rules preserve referential integrity without turning the durable model
into a manually maintained web of backlinks.

## 5. Versioning and resolution

- `schema_version` versions structure and migration logic for one record kind.
- `catalog_version` versions the resolved catalog seed as a whole and remains
  in the catalog manifest, not repeated in every record.
- Git/checkpoints preserve the exact durable frontier used by a campaign.
- Changing a definition's mechanics is an explicit catalog change. Existing
  instances are not silently rewritten; migration policy decides whether they
  retain, re-resolve, or override the changed values.
- Resolution order remains `engine -> ruleset -> campaign -> session`.
- An override must name its base and validate against a compatible schema.

This separates structural migration from content release numbering and avoids
copying transport/version metadata into every object.

## 6. Extension namespace

Keys in `extensions` use a dotted namespace with at least one separator, for
example `dandelion.hdm.debug` or `campaign.red_moon.foreshadowing`. Core ignores
unknown extension values. An extension cannot alter authoritative mechanics
unless the applicable schema and engine version explicitly define that key.

## 7. Identifier boundary

The base schemas validate identifiers as non-empty machine strings; they do not
hard-code a universal prefix, numeric width, or allocator. Those decisions are
made per independently identified kind. This keeps `asset-00042`, a semantic
definition ID, and a timeline slot from being forced into one counter policy.

The runtime remains the sole allocator for world-record IDs. Allocation and
record creation are one atomic operation. Formatting width is a minimum display
width, never an overflow limit.

## 8. Deliberately excluded from the envelope

- wall-clock creation/update timestamps;
- a generic status or lifecycle shared by unrelated kinds;
- ownership, location, HP, visibility, or knowledge fields;
- persisted backlinks;
- transport state and Git commit information;
- derived/cache-only values.

These are either kind-specific state, runtime metadata, or disposable indexes.
Keeping them out prevents the universal object from becoming a second
monolithic game model.
