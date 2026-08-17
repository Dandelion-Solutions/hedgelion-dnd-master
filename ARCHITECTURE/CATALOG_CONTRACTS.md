# HDM Catalog — Universal Record Contracts

Status: **AGREED**

Target: `feature/mechanical-runtime-hot-state`

Machine-readable schemas:

- `SCHEMAS/catalog-definition.schema.json`
- `SCHEMAS/world-record.schema.json`
- `SCHEMAS/identifier-policies.schema.json`

Machine-readable identifier policy: `CATALOG/identifier-policies.json`

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

Registry IDs describe the engine's accepted vocabulary and are closed to
ad-hoc LLM invention during play. Reusable definition instances are extensible
at ruleset and campaign scope when they validate against that vocabulary.
Adding a new executable primitive requires engine work; adding a sword, bottle,
or mortar definition does not.

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
- A new definition is justified when an object needs a reusable mechanical or
  semantic identity that cannot be expressed as instance state, existing
  definitions, facets, and tags. A different name or one-off description alone
  does not require one.
- Mechanical variations compose registered Activities, Effects, Resources,
  Rule Elements, and other catalog definitions.
- An idea that cannot be represented by registered capabilities produces a
  catalog-gap report instead of arbitrary executable data.

HDM does not define a plugin or free-form mechanics-extension contract at this
stage.

### 5.1 Definition changes are directed transformations

`definition_id` may change only when the same world object remains but its
reusable identity has changed. The permission is declared by a concrete
Activity step using the registered `op.transform_entity` primitive; it is not a
global compatibility matrix on asset kinds and is not inferred from facets.

Each step names or binds:

- the target world-record ID;
- the required current `definition_id` (`from_definition_id`);
- the resulting existing definition (`to_definition_id`).

The runtime rejects a stale source, missing target definition, wrong world kind,
or transition not present in the selected Activity. Reversibility requires a
second directed step: potion to empty bottle and empty bottle to potion are two
permissions, not one implicit bidirectional relation. The same mechanism covers
deploy/stow forms such as travelling mortar to siege mortar without implying
that arbitrary assets can transform into either.

Campaign-authored assets remain possible. When a new form is needed, the Master
may create a validated campaign definition and a campaign Activity that connects
explicit endpoints using registered capabilities. The Master never mutates
`definition_id` directly.

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

## 8.1 Authority of catalog artifacts

JSON schemas and machine-readable catalog files are authoritative for IDs,
shape, and validation. Markdown documents are authoritative for semantics,
ownership boundaries, and rationale. A contradiction is a repository defect;
runtime must not guess which representation to follow.

Executable mechanics may use only registered typed fields and capabilities.
`tags`, `details`, prose, and unknown optional fields may guide narration or
catalog authoring but never become an unvalidated mechanical input. If a value
starts affecting resolution, it is promoted to one agreed typed field and the
relevant schema/loader is updated.

## 9. Identifier boundary

The base envelopes validate IDs as machine strings. The loader additionally
selects the exact prefix, scope, strategy, and minimum numeric width from
`CATALOG/identifier-policies.json` according to record kind.

Definitions use stable semantic namespaced IDs and no numeric allocator.
Protocol values are embedded and receive no independent identity by default.
Timeline slots and encounter rounds are ordering/state values, not entity IDs.

Persistent world-record IDs and independently numbered runtime records use
campaign-scoped counters owned by runtime. Allocation and record creation form
one atomic operation. One `campaign-allocator` object stores only
`last_allocated` by policy; `next` is derived. The complete allocator is cached
in HOT/SQLite and included in the durable closure whenever canonical allocation
changes it.

Minimum widths are presentation padding, chosen from plausible record volumes
in a 200-hour campaign. They are not limits: after `turn-999999` comes
`turn-1000000` without migration.

### 9.1 Width groups

| Width | Kinds |
|---:|---|
| 3 | actor group, organization, contract, chapter |
| 4 | actor, location, connection, zone, mission, scene, encounter, hazard, lore fact, maintenance audit, catalog-gap report, session |
| 5 | asset, relationship |
| 6 | effect, knowledge, turn/interaction, publication batch, checkpoint |
| 7 | message, resolution, semantic event |
| 8 | mechanical event |

Intent plans, commands, continuations, and resolution traces derive identity
from their owning interaction or resolution. Dirty-record identity is its
target record; the allocator is a singleton.

### 9.2 Local identity and promotion

Incidental actors, groups, assets, locations, zones, hazards, and effects may
use session-scoped `local-*` IDs listed in the policy file. They remain HOT and
need not enter durable canon. Promotion atomically allocates a campaign ID,
rekeys the record and all local direct references, records lineage, and adds the
allocator change to the publication closure. The LLM never performs this
rewrite.

Concurrent writers allocate against their pinned frontier. A failed Git HEAD
comparison leaves all new IDs unpublished; runtime reloads the allocator and
atomically rekeys only conflicting unpublished records before preparing a new
batch. Published IDs are never changed or reused.
