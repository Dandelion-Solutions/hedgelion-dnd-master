# HDM Catalog — Universal Record Contracts

Status: **R2.7 WP-03 CANONICAL CLASS/ENVELOPE CONTRACT**

Active unreleased catalog generation: `2.0.0`.

Machine-readable contracts:

- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/catalog-admission-ledger.json` — admission disposition and realization-trace ledger; it is not an exact-ID, semantic, or runtime package owner.
- `DEV/CATALOG/entity-structures.json`
- `DEV/CATALOG/identifier-policies.json`
- `DEV/CATALOG/mechanical-surfaces.json`

Machine-readable schemas:

- `DEV/SCHEMAS/core-catalog.schema.json`
- `DEV/SCHEMAS/catalog-admission-ledger.schema.json`
- `DEV/SCHEMAS/catalog-definition.schema.json`
- `DEV/SCHEMAS/world-record.schema.json`
- `DEV/SCHEMAS/entity-structures.schema.json`
- `DEV/SCHEMAS/identifier-policies.schema.json`

Exact current class classification is in `CATALOG_INVENTORY.md`.

---

## 1. Minimum-sufficient class rule

HDM does not create a record merely because a concept has a name or because an implementation can serialize it.

Class admission is responsibility/lifecycle driven:

1. executable semantics -> closed engine capability/protocol registry;
2. reusable validated rules/content -> `definition.*`;
3. particular campaign thing/fact with independent world identity/lifecycle -> `world.*`;
4. independently addressable non-world operational/evidence owner needed across retry/suspension/recovery/collaboration/disclosure/audit -> `runtime.*`;
5. otherwise -> embedded typed `value.*`;
6. Story/Dramaturg retained noncanonical projections remain dedicated projection families outside canonical/current world/runtime record authority unless a later approved design explicitly changes that boundary.

Facets and tags classify/search only. They do not create identity or executable behavior.

A future promotion from embedded value/projection to independent record requires an explicit owner/lifecycle proof.

---

## 2. Definition envelope

Reusable definitions use the universal envelope:

```json
{
  "id": "campaign.moonlace_brooch",
  "kind": "definition.asset",
  "name": {
    "en": "Moonlace Brooch",
    "ru": "Брошь лунного кружева"
  },
  "facets": ["asset.wearable", "asset.artifact"],
  "tags": ["jewelry", "moon"],
  "data": {}
}
```

Required semantic fields:

- `id` — stable semantic namespaced definition identity inside one resolved catalog;
- `kind` — registered `definition.*` kind selecting the kind-specific `data` contract;
- `name` — English name plus optional campaign/player-language presentation name;
- `data` — validated kind-specific reusable content.

Optional `facets` and `tags` support classification/discovery only.

Definitions may reference other definitions and embedded registered Rule Elements/Trigger Bindings according to their kind-specific schema. Campaign/LLM content cannot introduce a new executable primitive merely by writing an unknown ID into data.

---

## 3. World-record envelope

Particular campaign things/facts use the world envelope:

```json
{
  "id": "asset-00042",
  "kind": "world.asset",
  "definition_id": "campaign.moonlace_brooch",
  "state": {}
}
```

Required semantic fields:

- stable record `id` according to the selected kind identity policy;
- registered `world.*` `kind`;
- kind-specific current `state`.

`definition_id` is legal only where `DEV/CATALOG/entity-structures.json` declares the world-kind binding as optional or required and the referenced definition kind is admitted.

No naming convention such as `world.foo -> definition.foo` creates binding automatically.

World state never stores a complete reusable definition copy merely for convenience.

---

## 4. Runtime-record boundary

`runtime.*` records are admitted only where non-world operational/evidence state has independent addressability/lifecycle.

Current admitted examples include:

- Interaction/IntentPlan/Command/Procedure/Resolution/Continuation execution owners;
- accepted message evidence;
- human disclosure relation;
- collaboration obligation generation;
- mechanical/semantic events and trace;
- checkpoint descriptor;
- allocation/audit/gap-report records.

A runtime record does not become gameplay/world truth merely because it is durable.

Conversely, a durable operational requirement must not be hidden in chat memory, an index or a generic checkpoint blob when its owning contract requires independent recovery/reference semantics.

---

## 5. Reference rules

1. Owners store semantically named forward references, not embedded copies of other mutable records.
2. Small immutable/typed protocol values may be embedded.
3. Persisted backlinks are avoided unless a concrete owner proves them semantically necessary.
4. Reverse lookup/index structures are derived/rebuildable by default and never become a competing semantic owner.
5. A durable publication cannot leave a durable reference to an unpublished dependency whose natural owner must survive.
6. Stable externally referenced IDs are not silently reused or repurposed.
7. Cycles are validated by kind-specific semantics, not forbidden globally.
8. Definition binding is machine-validated from the exact resolved catalog context.

---

## 6. Current state versus evidence/projection

HDM distinguishes current semantic ownership from historical evidence and projections.

Examples:

```text
world.actor HP                  -> current Actor owner
MechanicalEvent                 -> committed occurrence evidence
world.knowledge                 -> current subject proposition stance
runtime.message                 -> accepted communication evidence
runtime.disclosure              -> human exposure relation
Story                           -> noncanonical source-bound projection
ContextTrace                    -> diagnostic projection
index/reverse lookup            -> derived routing helper
checkpoint                      -> optional descriptor/evidence
```

A historical/derived representation cannot answer a current semantic question unless its owner contract explicitly gives it that responsibility.

---

## 7. Identifier contract

`DEV/CATALOG/identifier-policies.json` owns the machine identity strategy for each admitted world/runtime record kind.

The policy set may use more than one strategy because semantic identity requirements differ:

- namespaced semantic definition IDs;
- sequential campaign/session allocation where one allocator genuinely owns the namespace;
- parent-derived IDs for subordinate values/records;
- semantic composite keys for relation owners such as `world.knowledge` and `runtime.disclosure`;
- singleton IDs where one campaign owner is intentional.

Exact source-native identity policy for independently writable/live-created records is finalized by WP-11/WP-16. Catalog 2.0 SHALL not infer fictional order, authority or currentness from numeric/lexical ID order.

Minimum numeric widths, where a sequential policy survives, are presentation padding rather than capacity limits.

### 7.1 Composite relation identity

Current accepted relation-owner semantics include:

```text
world.knowledge
    key = (knower_id, fact_id)

runtime.disclosure
    key = (player_id, fact_id)
```

A physical implementation may encode a deterministic ID/path from that composite key, but it may not create several independent current rows for the same semantic relation merely because surrogate allocation permits it.

### 7.2 No chronology from IDs

Timeline slots, scene-local sequences, event IDs, Git revisions and allocation counters are never campaign-global fictional chronology merely by being ordered values.

---

## 8. Catalog resolution

All execution/validation occurs against one logical `ResolvedCatalogContext` as defined by `CATALOG_RESOLUTION.md`.

Within one resolved context:

```text
one definition_id -> at most one definition
```

Loaded sources do not shadow same-ID definitions by layer order.

Discovery/ranking returns candidates; deterministic validation against the same accepted context establishes whether an ID/kind/capability is actually legal.

Model memory, fuzzy search rank, storage filename order and remote mutable tags are not catalog authority.

---

## 9. Definition customization/evolution

Definitions do not use a universal inheritance/override object.

- one-off mutable object change -> world state;
- reusable campaign-specific content -> new validated campaign definition;
- rules-bearing behavior -> registered capabilities composed in validated definitions;
- unsupported executable idea -> typed catalog gap rather than arbitrary executable prose.

A definition ID is never silently repurposed to incompatible meaning.

A world record changes `definition_id` only through an explicitly admitted transition/mechanic such as a validated transform operation; similar facets/names do not authorize transformation.

---

## 10. Catalog generation and pre-release R2.7 rule

Catalog generation identifies the coherent engine machine-contract set; it is not a per-record version field.

R2.7 uses `2.0.0` as one **unreleased** clean-slate machine generation because this architecture audit intentionally removes/changes prior catalog IDs and semantics and no real campaign depends on `1.6.0`.

Until R2.7 final closure, later owning domains may make coordinated changes to the `2.0.0` artifacts without providing a `1.6.0 -> 2.0.0` campaign migration.

After release, incompatible semantic catalog changes require the future version/evolution contract defined by WP-20; same-version published refreshes may not silently change catalog meaning.

World records do not repeat catalog version fields solely to reconstruct the resolved definition set.

---

## 11. Machine/prose authority

Machine-readable catalog/schema files are authoritative for exact IDs and validation shape.

Canonical Markdown owning contracts are authoritative for semantic responsibility, authority limits and rationale.

A contradiction between them is a repository defect. Runtime must not guess which one to prefer or synthesize a reconciliation.

Nonmechanical fields such as tags/descriptive details may guide retrieval/narration but cannot become mechanics without explicit promotion into a registered typed contract.

---

## 12. R2.7 downstream handoff

WP-03 fixes the universal classification and closed vocabulary. Later R2.7 domains must finish:

- exact Actor/Asset state structures;
- execution-record schemas;
- truth/knowledge/disclosure/message schemas;
- Context Runtime and TurnEnvelope schemas;
- durable record roots/sharding/indexes;
- source-native/multiplayer identity policies;
- HOT/SQLite tables;
- recovery/checkpoint physical contracts;
- Story/planning projection schemas.

Those later details may refine coordinated catalog 2.0 artifacts, but they may not violate the class-admission/authority rules above without reopening the applicable accepted architecture.

## 12. Admission trace authority

`CATALOG_ADMISSION.md` owns the admission/realization audit model. The ledger MUST be bidirectionally equal to `core-catalog.json`; it cannot admit an absent ID, override a domain owner, or act as a runtime catalog/package. Dormant entries require an activation trigger. `STALE_REMOVE` entries cannot survive in the active core catalog after canonical cleanup.
