# HDM Versioning Namespace Inventory and Analysis

Status: **RESEARCH EVIDENCE / DECISION SUPPORT — NOT ARCHITECTURE AUTHORITY**

Date: 2026-09-05

Repository snapshot inspected: `v1/engine-rearchitecture` at `edbd8ded9db04e404a1e959e945965e474b9dc0f`.

This document preserves the repository inventory, analysis, intermediate conclusions, defects and decision trade-offs discovered while evaluating HDM version-numbering policy. It does not change the accepted versioning policy and does not authorize any migration or renumbering.

## 1. Decision under investigation

The Product Owner is evaluating two broad directions for HDM-owned version namespaces:

1. preserve the current separation in which engine/CORE components use one versioning model while `schema_version`, `*_revision`, format revisions and similar compatibility counters retain independent numbering; or
2. move toward a uniform three-component representation in which the first two components identify the HDM engine major/minor release line and the third component is the object's own independent revision/change counter.

External version namespaces are explicitly outside this decision. This includes SRD/D&D rules-baseline numbering, JSON Schema draft identity, external dependencies and other version identifiers owned outside HDM.

## 2. Source set inspected

Primary current owners and machine surfaces inspected during the inventory included:

- `DEV/RELEASE/VERSIONING.md`
- `DEV/ENGINE_DEVELOPMENT.yaml`
- `GAME/ENGINE_VERSION.yaml`
- `GAME/CORE/CORE_INDEX.md`
- current `GAME/CORE/*.md` module headers
- `GAME/SCHEMA/README.md`
- current `GAME/SCHEMA/*.schema.yaml`
- current `GAME/CAMPAIGN/**` templates and scaffold records
- `GAME/CORE/STORAGE.md`
- `GAME/SCHEMA/dnd_storage.schema.yaml`
- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`
- `DEV/ARCHITECTURE/CATALOG_MODEL.md`
- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/entity-structures.json`
- `DEV/CATALOG/identifier-policies.json`
- `DEV/CATALOG/mechanical-surfaces.json`
- `DEV/CATALOG/activity-primitive-contracts/manifest.json`
- `DEV/CATALOG/catalog-admission-ledger/manifest.json`
- `DEV/CATALOG/domain-rules-coverage.json`
- `DEV/CATALOG/house-rules-mechanical-boundary.json`
- `DEV/CATALOG/portable-value-contracts.json`
- `DEV/CATALOG/portable-value-routes.json`
- `DEV/CATALOG/product-promise-evidence.json`
- `DEV/CATALOG/ruleset-package-closure.json`
- `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/ruleset-package-manifest.json`
- `GAME/TOOLS/ruleset_package.py`
- `DEV/TOOLS/release_builder.py`
- `DEV/TOOLS/audit_engine.py`
- `DEV/RELEASE/CHECKLIST.md`
- `GAME/MIGRATIONS/README.md`
- `DEV/docs/superpowers/specs/2026-08-18-engine-version-split-amendment.md`

Repository-wide search was used only for discovery/routing. Correctness-sensitive conclusions were checked against current owning files at the inspected branch snapshot.

## 3. Current canonical versioning policy

`DEV/RELEASE/VERSIONING.md` currently defines distinct version namespaces.

### 3.1 Engine release

Engine releases use two numeric components with an optional prerelease suffix:

```text
MAJOR.MINOR[-prerelease]
```

Examples in the policy include `v0.8`, `v0.9-RC`, `v1.5`.

Current repository manifests report:

```yaml
engine_version: 1.0-alpha
recommended_tag: v1.0-alpha
```

### 3.2 CORE/runtime modules

CORE/runtime modules use:

```text
MAJOR.MINOR.REVISION
```

The accepted semantics are:

- `MAJOR.MINOR` = engine major/minor version in which the module was last materially changed;
- `REVISION` = monotonically increasing counter owned by that module;
- a new module starts at revision `1` under the current engine major/minor;
- an engine-version change alone does not rewrite an unchanged module;
- when the module later changes, its prefix moves to the then-current engine major/minor and its own revision increments.

Prerelease suffixes belong to engine release/tag identity, not to module versions.

### 3.3 Independent counters

The same canonical file explicitly states that schema versions, launcher revisions, format revisions and similar compatibility counters remain independent integers unless their own specification says otherwise.

Therefore the repository's current architecture is already the "separate namespaces" model. A move to engine-prefixed schema/revision values would be a deliberate architecture/versioning-policy change, not a cleanup of an undocumented convention.

## 4. Namespace inventory

The current HDM repository contains at least the following distinct HDM-owned version/revision namespaces.

| Namespace | Current representation | Example | Meaning |
| --- | --- | --- | --- |
| Engine release | `MAJOR.MINOR[-prerelease]` | `1.0-alpha` | semantic HDM engine release identity |
| CORE/runtime module version | `MAJOR.MINOR.REVISION` | `0.8.4` | engine line of last material module change + module-local revision |
| Development component revision | integer | `persistence_revision: 8` | development bookkeeping counter for a specific concern |
| Persistent record schema | integer | `1`, `2`, `3` | compatibility generation of a particular persisted record family |
| Storage/package/protocol schema | integer | `1`, `2`, `3` | version of a particular serialized or protocol contract |
| Catalog generation | three-component generation | `2.0.0` | coordinated machine-contract catalog generation |
| Ruleset package version | package-local version string | `0.1.0-mvp` | version of an HDM ruleset package |
| Ruleset compatibility/protocol IDs | identifier-local `v1` / schema integers | `.v1`, `*_schema_version: 1` | compatibility identity for specific ruleset protocols |
| Dynamic state revision/frontier | integer ordinal | context-dependent | mutation/currentness or synchronization revision, not release identity |

The visually similar numbers do not currently have a single semantic meaning.

## 5. Central engine/release metadata

`DEV/ENGINE_DEVELOPMENT.yaml` is the full development/release bookkeeping owner. `GAME/ENGINE_VERSION.yaml` is the installed runtime projection.

Shared current identity includes:

```yaml
engine_version: 1.0-alpha
schema_version: 2
recommended_tag: v1.0-alpha
```

The development manifest additionally carries independent revision counters. At the inspected snapshot:

| Counter | Value |
| --- | ---: |
| `ai_reasoning_revision` | 3 |
| `gm_craft_revision` | 7 |
| `install_layout_revision` | 14 |
| `branch_id_revision` | 1 |
| `access_control_revision` | 5 |
| `storage_format_revision` | 4 |
| `presentation_revision` | 12 |
| `persistence_revision` | 8 |
| `campaign_card_revision` | 4 |
| `mechanics_integrity_revision` | 1 |
| `character_readiness_revision` | 4 |
| `save_contract_revision` | 3 |
| `campaign_identity_revision` | 2 |
| `runtime_scope_revision` | 3 |
| `consistency_audit_revision` | 5 |

The runtime projection deliberately excludes development-only `*_revision` counters.

### Intermediate conclusion

The development counters are not currently alternative spellings of the engine version. They are explicitly independent bookkeeping dimensions. Converting them to `1.0.N` would change their representation while adding no new information unless the prefix is intended to carry compatibility semantics.

## 6. Complete CORE module-version inventory

The current `GAME/CORE` inventory contains 43 version-bearing current CORE artifacts plus current CORE documentation files such as `README.md` and `SOURCES.md` that do not carry a module-version header.

Grouped by current version header:

| Version | Count | Files |
| --- | ---: | --- |
| `0.1.0` | 1 | `MECHANICS_INTEGRITY.md` |
| `0.1.1` | 9 | `NPC.md`, `DIALOGUE.md`, `EXPLORATION.md`, `ENCOUNTERS.md`, `CHRONOLOGY.md`, `REWARDS.md`, `ADVANCEMENT.md`, `INTEGRITY.md`, `ANTIPATTERNS.md` |
| `0.1.2` | 5 | `RANDOMNESS.md`, `INFORMATION.md`, `COMBAT.md`, `PROCESSES.md`, `LIVE_SCENE.md` |
| `0.1.3` | 1 | `AI_REASONING.md` |
| `0.1.4` | 1 | `CAMPAIGN_CARD.md` |
| `0.1.7` | 1 | `MULTIPLAYER.md` |
| `0.2.0` | 5 | `CAMPAIGN_IDENTITY.md`, `MAGIC.md`, `WORLDGEN.md`, `PREP.md`, `SAVE_CONTRACT.md` |
| `0.2.1` | 1 | `PERSISTENCE.md` |
| `0.2.2` | 1 | `ADJUDICATION.md` |
| `0.3.0` | 1 | `CORE_INDEX.md` |
| `0.4.0` | 1 | `SESSION.md` |
| `0.5.0` | 1 | `DURABILITY_GUARD.md` |
| `0.6.0` | 1 | `CHARACTER.md` |
| `0.7.0` | 1 | `STORAGE.md` |
| `0.7.2` | 2 | `CAMPAIGN_OPERATIONS.md`, `LORE.md` |
| `0.7.3` | 4 | `NEW_CAMPAIGN_FAST_PATH.md`, `GM_CRAFT.md`, `SAFETY.md`, `NARRATIVE.md` |
| `0.8.0` | 1 | `RUNTIME.md` |
| `0.8.1` | 1 | `CAMPAIGN_SETUP.md` |
| `0.8.4` | 1 | `PLAY_POLICY.md` |
| `0.8.8` | 1 | `BOOTSTRAP_RUNTIME.md` |
| `0.9.2` | 1 | `ENGINE_UPDATES.md` |
| `1.1.0` | 2 | `CHARACTER_READINESS.md`, `DIEGETIC_ONBOARDING.md` |

Most files use the header name:

```yaml
framework_module_version: ...
```

`BOOTSTRAP_RUNTIME.md` instead uses:

```yaml
runtime_bootstrap_version: 0.8.8
```

### Intermediate conclusions

1. The CORE version namespace is historically broad: current files span many engine-line prefixes.
2. That breadth is not automatically a defect under the accepted policy because unchanged modules intentionally keep the engine line of their last material change.
3. `CHARACTER_READINESS.md` and `DIEGETIC_ONBOARDING.md` are anomalous at `1.1.0` while the current engine is only `1.0-alpha`. They appear to name a future engine release line and therefore require explicit reconciliation.
4. `BOOTSTRAP_RUNTIME.md` uses a different version-field name from the dominant CORE convention. Whether that distinction is intentional or accidental should be decided and then validated mechanically.
5. `README.md` and `SOURCES.md` are current CORE artifacts without module version headers. This may be correct if they are classified as non-module documentation, but that classification is not presently enforced by versioning tooling.

## 7. Persistent campaign schema inventory

`GAME/SCHEMA/README.md` explicitly states that `schema_version` belongs to persistent campaign data and is independent of Framework/engine version.

Current schema values are not globally uniform. They vary by record family:

| `schema_version` | Count | Record/schema families |
| --- | ---: | --- |
| `1` | 15 | `campaign_card`, `campaign_config`, `event`, `faction`, `house_rules_policy`, `index`, `item`, `live_scene`, `location`, `lore`, `npc`, `pc`, `player`, `session`, `thread` |
| `2` | 3 | `checkpoint`, `current_state`, `scene` |
| `3` | 2 | `campaign_manifest`, `dnd_storage` |

The campaign templates/scaffold carry matching independent record-family values rather than one engine-derived prefix. Examples include:

- campaign manifest: `schema_version: 3`;
- checkpoint template: `schema_version: 2`;
- current state: `schema_version: 2`;
- session template: `schema_version: 1`;
- log template: `schema_version: 1`;
- house-rules sidecar: `schema_version: 1`;
- index templates: `schema_version: 1`.

### Intermediate conclusion

These are real persisted compatibility contracts. Reformatting `schema_version: 1` into an engine-prefixed string such as `1.0.1` is not a documentation-only change: validators, generators, migrations, stored campaign data and compatibility checks would need coordinated migration.

## 8. Storage demonstrates the semantic separation clearly

One subsystem currently exposes four distinct version/revision axes:

| Surface | Current value | Meaning |
| --- | --- | --- |
| `GAME/CORE/STORAGE.md` | `framework_module_version: 0.7.0` | version of the runtime instruction module |
| storage marker | `storage_format_version: 3` | persisted storage layout/format generation |
| `dnd_storage.schema.yaml` | `schema_version: 3` | schema contract generation |
| `DEV/ENGINE_DEVELOPMENT.yaml` | `storage_format_revision: 4` | development bookkeeping revision |

These values are not four encodings of one concept. They answer different questions.

### Intermediate conclusion

A universal visual format can make the system look cleaner while obscuring semantic independence. Any unification should first prove that the prefix changes compatibility behavior rather than merely decorating a local counter.

## 9. Runtime package and launcher namespaces

The launcher/runtime package layer has additional independent counters.

Current launcher metadata uses an independent integer revision (`launcher_version`, observed at revision `19` during the inventory).

The generated runtime package contract uses:

```yaml
schema_version: 2
```

`DEV/TOOLS/release_builder.py` explicitly validates that runtime package metadata has `schema_version == 2`.

Therefore converting these values to an engine-prefixed representation would require changes to package validation and potentially package-discovery/compatibility behavior.

## 10. Catalog generation is deliberately independent

Current canonical catalog authority defines:

```text
Catalog generation: 2.0.0
```

`DEV/ARCHITECTURE/CATALOG_INVENTORY.md` explicitly describes `2.0.0` as the unreleased clean-slate R2.7 machine-contract generation and identifies the older `1.6.0` scaffold as superseded.

Current coordinated machine artifacts use this generation, including:

- `DEV/CATALOG/core-catalog.json` -> `catalog_version: 2.0.0`, `schema_version: 1`;
- `DEV/CATALOG/entity-structures.json` -> `catalog_version: 2.0.0`;
- `DEV/CATALOG/identifier-policies.json` -> `catalog_version: 2.0.0`, `schema_version: 1`;
- `DEV/CATALOG/mechanical-surfaces.json` -> `catalog_version: 2.0.0`;
- activity primitive contract manifest -> `catalog_generation: 2.0.0`, `schema_version: 1`;
- catalog admission manifest -> `catalog_generation: 2.0.0`, `schema_version: 1`.

### Important distinction

`2.0.0` here is not the HDM engine release. Current engine identity is `1.0-alpha`. The catalog generation is a separate coordinated machine-contract namespace and is intentionally allowed to advance independently.

## 11. Stale catalog reference found

`DEV/ARCHITECTURE/CATALOG_MODEL.md` still states that `CATALOG/core-catalog.json` is version `1.2.0`, while the current machine artifact and canonical catalog inventory use `2.0.0`.

This is a concrete stale cross-document version reference and should be repaired independently of the larger versioning-policy decision.

## 12. Ruleset package and protocol namespaces

The shipped HDM ruleset package has several independent identifiers in one manifest:

```text
manifest_schema_version: 1
package_version:          0.1.0-mvp
compatibility_id:         hdm.rules.dnd2024-srd52.v1
engine_requirement:       1.0-alpha
catalog_generation:       2.0.0
```

The surrounding runtime protocol adds additional independent schema-generation fields, including:

```text
lock_schema_version:        1
inventory_schema_version:   1
comparison_schema_version:  1
attestation_schema_version: 1
```

It also uses compatibility/contract identifiers ending in `.v1` and hash-domain constants ending in `_V1`.

### Intermediate conclusion

These protocol versions are not safe candidates for a blind numeric-format rewrite. Some `V1` markers participate in deterministic identity/hashing domains. Renaming or changing their generation can alter derived identities even when business semantics are unchanged.

## 13. External namespaces explicitly excluded

The following should remain outside an HDM renumbering exercise unless their external owner/version changes:

- D&D/SRD baseline identities such as SRD `5.2.1`;
- JSON Schema draft URI/version such as Draft 2020-12;
- external library/dependency versions;
- externally owned module/component versions.

These numbers may be carried, validated or referenced by HDM, but HDM does not own their numbering.

## 14. Ambiguous global `ENGINE_VERSION.schema_version`

Both `DEV/ENGINE_DEVELOPMENT.yaml` and `GAME/ENGINE_VERSION.yaml` currently report:

```yaml
schema_version: 2
```

At the same time current persistent surfaces include:

- campaign manifest schema v3;
- storage schema v3;
- storage format v3.

An earlier approved engine-version-split amendment described shared `ENGINE_VERSION.schema_version` as runtime schema-compatibility metadata and required campaign-scaffold schema coherence unless a later schema explicitly established a different relationship.

Current maintenance validation now independently requires campaign manifest/storage v3 while still accepting shared engine metadata `schema_version: 2`.

### Intermediate conclusion

The meaning of the global `schema_version: 2` is now ambiguous and requires explicit reconciliation. Plausible outcomes include:

1. it is a stale global counter that should be advanced;
2. it intentionally denotes a different aggregate compatibility contract and therefore needs clearer naming/ownership;
3. the global field no longer provides useful information and should eventually be retired;
4. later architecture has intentionally decoupled it from individual persistent record schemas, in which case that decoupling should be made explicit in the current owner.

This research does **not** recommend mechanically changing it to `3` without resolving its intended semantics and consumers.

## 15. Why current automated checks do not catch CORE drift

`DEV/TOOLS/audit_engine.py` currently checks many relevant consistency conditions, including:

- GAME/DEV layout and shared engine metadata;
- campaign manifest/storage v3 requirements;
- JSON Schema validity;
- catalog cross-validation;
- equality of the coordinated main catalog versions;
- numerous runtime architecture invariants.

However, it does not validate `framework_module_version` / `runtime_bootstrap_version` against the rules in `DEV/RELEASE/VERSIONING.md`.

Consequences:

- old or inconsistent module prefixes can remain indefinitely;
- a future-line value such as `1.1.0` can pass the general maintenance audit while engine version is `1.0-alpha`;
- inconsistent header names are not detected;
- policy and actual CORE headers can silently drift.

### Intermediate conclusion

Regardless of the Product Owner's final numbering choice, the accepted policy should gain machine-verifiable invariants. Versioning consistency should not rely on manual inspection.

## 16. Option analysis

### Option A — preserve separate namespaces

Under this model:

- engine remains `MAJOR.MINOR[-prerelease]`;
- CORE/runtime modules retain `MAJOR.MINOR.REVISION`;
- persistent schema versions remain independent integers;
- format/package/protocol schema versions remain independent integers;
- DEV `*_revision` counters remain independent integers;
- catalog generation remains its own coordinated version;
- package-local versions remain package-local.

#### Advantages

- preserves current semantic separation;
- no artificial schema migrations on engine-only releases;
- a persisted format changes only when that persisted format actually changes;
- simple integer equality remains sufficient for many validators;
- history of each compatibility surface is explicit and local;
- existing migrations and package contracts require less churn.

#### Disadvantages

- many visually different numbers coexist;
- a reader must know which namespace a field belongs to;
- inconsistent naming such as generic `schema_version` can be ambiguous without better taxonomy;
- tooling must understand multiple kinds of version fields.

### Option B — engine-prefixed versions for all HDM-owned objects

Conceptually:

```text
ENGINE_MAJOR.ENGINE_MINOR.LOCAL_REVISION
```

for schemas, revisions and components.

#### Potential advantage

The value itself immediately reveals the engine line in which the object's latest revision was established.

#### Structural problem

Consider a persistent NPC schema whose local schema generation remains unchanged while engine moves from `1.0` to `1.1`.

If it is rewritten from `1.0.1` to `1.1.1`, its number changes even though its data contract did not. This suggests a schema migration/change that did not occur.

If it stays `1.0.1`, then its first two components no longer mean the current engine line; they only mean the engine line of its last change, which is exactly the current CORE-module policy and does not provide a universal current-version prefix.

The same tension applies to runtime package schemas, storage formats, lock/attestation protocol schemas and other compatibility objects.

#### Additional migration cost

A universal rewrite would touch or potentially affect:

- persisted campaign records;
- YAML schema validators and generators;
- runtime package builders/validators;
- migration detection;
- tests and fixtures;
- ruleset lock/attestation protocols;
- compatibility comparisons;
- documentation and release policy;
- potentially deterministic hash-domain identities where version IDs participate in canonical input.

This is materially larger than a formatting cleanup.

## 17. Current recommendation from this research

The evidence favors **preserving independent semantic namespaces**, but tightening taxonomy, naming and validation.

A practical target model is:

| Type | Recommended representation |
| --- | --- |
| HDM engine | `MAJOR.MINOR[-prerelease]` |
| CORE/runtime instruction module | `MAJOR.MINOR.REVISION` |
| Persistent record schema | independent integer generation |
| Storage format | independent integer generation |
| Runtime/package/manifest protocol schema | independent integer generation |
| DEV component revision | independent integer ordinal |
| Catalog generation | independent coordinated generation version, currently `2.0.0` |
| HDM ruleset package | package-local SemVer/version contract |
| Dynamic state revision/frontier | independent integer ordinal |
| External versions | preserve external owner numbering unchanged |

The preferred cleanup is therefore **not to make every value look the same**, but to make every version field's semantic type obvious and mechanically enforced.

## 18. Concrete cleanup candidates independent of the final decision

The following defects/gaps exist even if the current separate-namespace policy is retained:

1. reconcile the two CORE modules currently marked `1.1.0` against current engine `1.0-alpha`;
2. decide whether `runtime_bootstrap_version` is a distinct intended namespace or should use the standard CORE module-version field;
3. repair stale `DEV/ARCHITECTURE/CATALOG_MODEL.md` reference from `1.2.0` to the current catalog generation or, preferably, route to the canonical catalog owner rather than hard-coding a stale number;
4. resolve the semantic meaning of shared `ENGINE_VERSION.schema_version: 2` relative to current persistent v3 surfaces;
5. decide whether current unversioned CORE documentation files are intentionally outside module-version policy;
6. extend maintenance/version audits so accepted module/version rules are actually checked;
7. document a short taxonomy distinguishing release version, module version, schema generation, format generation, package version, catalog generation and state revision.

## 19. Questions requiring Product Owner / architecture decision

The repository evidence does not answer these product/architecture choices by itself:

1. Is the Product Owner's goal primarily visual consistency, easier human diagnosis, or a stronger compatibility invariant? The correct representation depends on which problem is being solved.
2. Should CORE module prefixes continue to identify the engine release line of the module's **last material change**, or should all current modules be normalized at a future release boundary?
3. Should catalog generation remain a fully independent machine-contract generation? Current architecture strongly treats it that way.
4. What precise semantic contract does the shared `ENGINE_VERSION.schema_version` represent today?
5. Which version families should be visible to runtime/users versus remain development-only metadata?

## 20. Bottom line

The repository does not merely contain inconsistent spellings of one version. It contains multiple intentional compatibility dimensions plus several real drift defects.

The strongest current evidence is:

- independent schema/revision counters are an explicit canonical policy, not an accident;
- persistent schemas already evolve independently by record family;
- catalog `2.0.0` is a deliberate catalog generation, not engine release identity;
- protocol/schema integers often participate directly in validators and compatibility logic;
- CORE module version headers show real historical drift and lack automated policy enforcement;
- some individual values/references are clearly stale or anomalous and should be repaired regardless of the larger policy choice.

Accordingly, any future architecture decision should separate **semantic namespace design** from **cleanup of incorrect current values**. A global renumbering before that distinction is formalized risks converting useful independent compatibility axes into cosmetic engine-prefixed numbers and creating unnecessary migration burden.
