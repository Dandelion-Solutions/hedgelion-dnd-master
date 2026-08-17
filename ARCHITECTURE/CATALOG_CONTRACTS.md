# HDM Catalog — Universal Record Contracts

Status: **AGREED**

Target: `feature/mechanical-runtime-hot-state`

Machine-readable schemas:

- `SCHEMAS/catalog-definition.schema.json`
- `SCHEMAS/world-record.schema.json`

## 1. Design rule

HDM uses the minimum sufficient record shape. A field belongs in a record only
when it describes that record and cannot be derived reliably from its kind,
definition, storage context, event history, or checkpoint.

The common envelopes do not reserve speculative extension points. A concrete
need must justify a new field or mechanism.

## 2. Reusable definition envelope

```json
{
  "id": "campaign.moonlace_brooch",
  "kind": "definition.asset",
  "name": {
    "en": "Moonlace Brooch",
    "ru": "Брошь лунного кружева"
  },
  "facets": ["asset.wearable", "asset.decoration", "asset.artifact"],
  "tags": ["jewelry", "moon"],
  "data": {}
}
```

Required fields:

| Field | Contract |
|---|---|
| `id` | Stable ASCII ID, unique in the resolved definition catalog. |
| `kind` | Registered `definition.*` kind selecting the schema for `data`. |
| `name` | English name and, optionally, the campaign/player-language name. |
| `data` | Kind-specific, schema-validated reusable content. |

Optional fields:

| Field | Contract |
|---|---|
| `facets` | Registered classifiers. They do not grant behavior. |
| `tags` | Search terms with no executable meaning. |

References to Activities, Effects, Resources, Rule Elements, or other
definitions belong in kind-specific `data`. A loader validates those references
against the reviewed registries.

## 3. World-record envelope

```json
{
  "id": "asset-00042",
  "kind": "world.asset",
  "definition_id": "campaign.moonlace_brooch",
  "state": {}
}
```

Required fields:

| Field | Contract |
|---|---|
| `id` | Runtime-allocated identity for this particular record. |
| `kind` | Registered `world.*` kind selecting the schema for `state`. |
| `state` | Kind-specific current world state. |

`definition_id` is optional in the universal envelope. A kind-specific schema
may require it when records of that kind are instantiated from reusable
definitions. Lore facts, relationships, chapters, and timeline markers may be
authored directly.

Instance-specific roles and classifications are kind-specific state. Facets
from a reusable definition are not copied into the world record and there is no
universal facet-merging algorithm.

## 4. Reference rules

1. Records store forward references in semantically named kind-specific fields,
   for example `owner_actor_id`; there is no universal `references` bag.
2. A reference stores an ID, not an embedded copy of the target record. Small
   immutable value objects may still be embedded.
3. Persisted backlinks are avoided. SQLite may index reverse relationships as
   a disposable projection.
4. Durable canon may not depend on an unpublished ephemeral entity. The
   publication planner promotes the dependency or rejects the publication.
5. Referenced durable records are retired/tombstoned rather than silently
   deleted, and persistent IDs are not reused.
6. Cycles are decided by kind-specific validation. Some relationships and
   location connections are naturally reciprocal.

## 5. Reuse and customization

Definitions do not use inheritance or a universal override object.

- Runtime changes to a particular object belong in kind-specific `state`.
- A unique object with different permanent properties receives a campaign
  definition.
- Mechanical variations compose registered Activities, Effects, Resources,
  Rule Elements, and other catalog definitions.
- An idea that cannot be represented by registered capabilities produces a
  catalog-gap report instead of arbitrary executable data.

HDM does not define a plugin or free-form mechanics-extension contract at this
stage.

## 6. Version placement

Individual definitions and world records do not repeat schema or content
versions. Compatible versions are recorded at the level that owns them:

- engine version;
- catalog version;
- campaign/checkpoint format version;
- checkpoint Git frontier.

A loaded campaign is a coherent snapshot. Incompatible updates require an
explicit campaign migration; HDM does not support mixed per-record schema
versions inside one runtime state.

`definition_id` is therefore a plain stable reference. Checkpoint/catalog
frontiers identify the corresponding definition snapshot.

## 7. Localization

Stored definition names contain:

- mandatory English (`en`);
- at most one optional campaign/player-language value.

If another player uses a different language, the LLM translates presentation
text for that response. HDM does not accumulate a translation dictionary in
every definition. Machine IDs remain language-independent.

The same compact localized-text shape may be reused for kind-specific stored
descriptions when a description is actually required.

## 8. Metadata placement

The following data is deliberately excluded from the universal records:

| Information | Owner |
|---|---|
| canonical/local/ephemeral status | runtime and checkpoint frontier |
| dirty/publication status | runtime dirty record/publication batch |
| object creation or change history | mechanical/semantic event log |
| source and license of a rules package | catalog/package metadata |
| import and migration history | migration log |
| Git commit and storage path | checkpoint/transport metadata |
| reverse references | disposable SQLite indexes |
| record revision | global state/checkpoint revision until per-record concurrency is justified |

This placement avoids duplicating facts across every object while retaining
their authoritative source.

## 9. Identifier boundary

The base schemas validate IDs as machine strings without imposing one prefix,
numeric width, or allocator policy on unrelated classes. Identifier policy is
defined per independently identified kind.

The runtime remains the allocator for persistent world-record IDs. Allocation
and record creation form one atomic operation. A configured numeric width is a
minimum presentation width rather than an overflow limit.
