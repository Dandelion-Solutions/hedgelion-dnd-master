# HDM Catalog — Universal Record Contracts

Status: **AGREED — STEP-5.0 CONTAMINATION RETIREMENTS APPLIED**

Target: `feature/mechanical-runtime-hot-state`

Machine-readable schemas:

- `SCHEMAS/catalog-definition.schema.json`
- `SCHEMAS/world-record.schema.json`
- `SCHEMAS/entity-structures.schema.json`
- `SCHEMAS/identifier-policies.schema.json`

Machine-readable contracts:

- `CATALOG/entity-structures.json`
- `CATALOG/identifier-policies.json`

## 1. Design rule

HDM uses the minimum sufficient record shape. A field belongs in a record only
when it describes that record and cannot be derived reliably from its kind,
definition, storage context, event history, or checkpoint.

The common envelopes do not reserve speculative extension points. A concrete
need must justify a new field or mechanism.

### 1.1 Canonical class-admission rule

A new domain noun does not automatically justify a new catalog class or record.
Classify a concept by responsibility and independent identity/lifecycle:

1. If it introduces executable semantics that deterministic runtime must
   implement, it belongs to a closed engine capability/protocol registry.
   Campaign/LLM content cannot invent it.
2. If it is reusable validated rules/content composed from registered semantics,
   it is a `definition.*` record.
3. If it is one particular campaign thing/fact with independent identity,
   lifecycle, provenance, references, or mutable state, it is a `world.*`
   record.
4. If it is an independently addressable operational owner needed across
   execution, retry, suspension, recovery, or audit but is not world canon, it
   is a `runtime.*` record.
5. Otherwise, if it exists only inside another owner/request/calculation and has
   no independent lifecycle/reference requirement, it is an embedded typed
   protocol/value object.
6. Facets and tags classify/search. They never create identity or executable
   semantics by themselves.

If a previously embedded value later requires independent addressing, retry,
reference, or lifecycle, promoting it to a record is an explicit architecture
change. Serialization inside a runtime record does not itself grant independent
identity.

The same rule applies to operational bookkeeping. A dirty-set entry or prepared
publication snapshot is not a `runtime.*` record merely because the runtime may
serialize it locally. Step 5.5/5.6 must prove independent identity/lifecycle
before such a class is admitted.

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

References to Activities, Effects, Resources, or other definitions belong in
kind-specific `data`. Embedded Rule Elements and Trigger Bindings remain with
the definition that grants them. A loader validates references and embedded
mechanics against the reviewed registries and their dedicated schemas.

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

`definition_id` is optional in the universal envelope only because different
world kinds have different reusable-definition relationships. Its semantic
legality is **not** universal.

`CATALOG/entity-structures.json` owns the closed `definition_binding` contract
for every `world.*` kind:

```text
mode = forbidden
    definition_id must be absent

mode = optional
    definition_id may be absent; if present its definition kind must be allowed

mode = required
    definition_id must be present and its definition kind must be allowed
```

The loader/compiler validates both referenced ID existence and referenced
`definition.*` kind against this mapping. Runtime code must not infer a relation
from similar names.

Examples:

```text
world.actor  -> definition.actor_archetype
world.asset  -> definition.asset
world.effect -> definition.effect | definition.condition
```

The `world.effect` case proves that definition/world compatibility is a declared
relation, not a `world.foo -> definition.foo` naming convention. Conversely, a
reusable definition does not require a same-named world kind: a Condition
application is a `world.effect`, and an Activity can execute without producing a
persistent Activity instance.

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
7. `definition_id` compatibility is validated from the machine
   `definition_binding` table; existence alone is insufficient.

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
  and embedded Rule Elements/Trigger Bindings.
- An idea that cannot be represented by registered capabilities produces a
  catalog-gap report instead of arbitrary executable data.

HDM does not define a plugin or free-form mechanics-extension contract at this
stage.

A reusable source definition does not prescribe the runtime owner of every
application of that content. For example, a reusable hazard may describe a trap,
poison, disease, or curse, while a concrete ongoing target-local disease/curse
may be represented by the ordinary Effect/Condition lifecycle if that is its
actual independent state owner. Do not create a `world.hazard` merely because a
`definition.hazard` participated in provenance.

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
a target definition kind incompatible with that world kind's
`definition_binding`, or a transition not present in the selected Activity.
Reversibility requires a second directed step: potion to empty bottle and empty
bottle to potion are two permissions, not one implicit bidirectional relation.
The same mechanism covers deploy/stow forms such as travelling mortar to siege
mortar without implying that arbitrary assets can transform into either.

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
| dirty state | HOT working-set bookkeeping owned by the runtime representation selected in Step 5.5; no independent `runtime.dirty_record` is admitted in catalog 1.6.0 |
| publication preparation/status | frozen transport/publication state selected in Step 5.6; no independent `runtime.publication_batch` is pre-admitted |
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
Serializing a protocol value inside a trace, Continuation, or checkpoint does
not change that rule: the owning runtime record owns persistence, versioning,
and lifecycle. If independent addressing becomes necessary, introducing a
runtime record is an explicit contract change.

Timeline slots and encounter rounds are ordering/state values, not entity IDs.
A sparse numeric timeline value MAY order events inside an explicit local/domain
chronology without becoming a campaign-global chronology authority.

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
| 3 | actor group, organization, contract |
| 4 | actor, location, connection, zone, mission, scene, encounter, hazard, lore fact, maintenance audit, catalog-gap report, session |
| 5 | asset, relationship |
| 6 | effect, knowledge, turn/interaction, checkpoint |
| 7 | message, resolution, semantic event |
| 8 | mechanical event |

Intent plans, commands, continuations, and resolution traces derive identity
from their owning interaction or resolution. The allocator is a singleton.
Dirty bookkeeping and publication snapshots have no record-ID policy in catalog
1.6.0.

Story layer-local IDs follow the canonical Step-4 Story contract and are outside
this world/runtime allocator table. Literary Chapter boundaries are Story index
metadata and therefore have no world-record ID policy.

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
