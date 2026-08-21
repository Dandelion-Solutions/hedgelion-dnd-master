# Step 1 Retrospective Assurance — Slice 0B Coverage and Research

Status: **ASSURANCE SYNTHESIS — ADVERSARIAL REVIEW PENDING**

Target branch: `feature/mechanical-runtime-hot-state`

Task Charter: `2026-08-19-step-1-assurance-slice-0b-catalog-evolution-task-charter.md`

## 1. Method

The solution-blind charter was compared against:

- `ARCHITECTURE/CATALOG_MODEL.md`;
- `ARCHITECTURE/CATALOG_INVENTORY.md`;
- `ARCHITECTURE/CATALOG_CONTRACTS.md`;
- `CATALOG/identifier-policies.json`;
- `SCHEMAS/catalog-definition.schema.json`;
- `ENGINE_DEVELOPMENT.yaml` and runtime `ENGINE_VERSION.yaml`;
- campaign manifest/checkpoint engine identity and persistence/update contracts;
- the Step-1/Step-2 accepted rule that durable references cannot depend on unpublished local objects.

Targeted external sanity checks used primary packaging specifications. npm's package-lock contract demonstrates the value of a single resolved dependency snapshot for reproducibility; Python packaging metadata separates distribution name/version/dependencies as package-level metadata; Semantic Versioning requires released version meaning to change when the public contract changes. HDM does not copy these package formats, but the underlying separation between stable logical references and the resolved package set is directly applicable.

## 2. Coverage summary

| Requirement family | Coverage | Finding |
|---|---|---|
| stable semantic definition IDs | FULL | definition IDs are semantic namespaced IDs, not allocated instance IDs |
| machine capability IDs closed by engine version/catalog | FULL | core capability registry is closed and versioned |
| engine/ruleset/campaign/session strata | PARTIAL | strata exist; duplicate-ID/collision semantics are not explicit |
| deterministic resolution order | PARTIAL | order is listed but its meaning can be mistaken for shadow/override precedence |
| no silent repurposing | FULL in prose | existing IDs should not be repurposed; needs collision/snapshot enforcement |
| ruleset package identity/version | MISSING logical contract | `rules_baseline` is descriptive text, not a resolved package identity |
| campaign definition snapshot identity | IMPLICIT/FULL | campaign Git frontier can identify durable campaign files if paths/closure are defined |
| engine-shipped definition snapshot identity | PARTIAL | runtime package identity exists, but same-version descendant refresh can replace bytes silently |
| session definition promotion | PARTIAL | world local-ID promotion is specified; definition promotion semantics are not |
| local dependency closure | PARTIAL / later | publication closure principle exists; exact dependency graph belongs later |
| catalog-gap | FULL | unsupported executable semantics have explicit gap path |
| bounded LLM catalog discovery | DEFERRED_OK with minimum | Step 3 owns binder/discovery; Step 1 already distinguishes searchable definitions from capabilities/runtime records |
| migration of incompatible catalog changes | PARTIAL / later | explicit migration is required, but the catalog snapshot that compatibility applies to is underspecified |
| multiple future ruleset packages | MISSING/DEFERRED_RISK | architecture says `selected ruleset definitions` but has no package-set descriptor/collision contract |

## 3. Finding 0B-F1 — catalog strata order is semantically ambiguous

**Severity: SIGNIFICANT contract ambiguity; correction is mechanically implied.**

Current prose says:

```text
engine capability registry
  -> selected ruleset definitions
  -> campaign definitions
  -> session-local definitions
```

and calls this `Resolution order`, while separately stating that definitions do not use a universal inheritance/override mechanism.

Those statements are compatible only if the arrow means **assembly/availability order**, not `last layer wins` shadowing.

If duplicate IDs are silently resolved by scope priority, a durable plain `definition_id` can change meaning when a campaign/session definition appears or disappears. That violates stable semantic identity and makes the same world record mean different things without mutation.

### Recommended invariant

```text
A resolved catalog contains at most one definition for each definition_id.
Duplicate IDs across loaded definition sources are validation errors.
Layer order controls loading/discovery/dependency direction, not shadowing.
```

Campaign customization of shipped content uses a new campaign definition ID and explicit references/transformation, not same-ID replacement.

This follows from existing no-universal-override and no-ID-repurposing decisions; it does not require a new human product choice.

## 4. Finding 0B-F2 — no explicit resolved catalog snapshot/package-set identity

**Severity: SIGNIFICANT architectural gap; likely human gate after adversarial review.**

A plain durable `definition_id` is meaningful only relative to the compatible definition set from which it was resolved.

Current durable runtime identity is strong for the engine ZIP:

```text
version
package_id
source_commit_sha
package_sha256
```

and campaign Git commit/tree can pin campaign-authored definitions. However:

- `MANIFEST.rules.baseline` is only a free string;
- Step-1 architecture speaks of `selected ruleset definitions` and future custom rulesets;
- there is no typed package identity/version/digest set for ruleset definition packages;
- `catalog_version = 1.2.0` identifies the machine catalog contract, not the concrete resolved reusable-definition set;
- session-local definitions are outside the durable campaign frontier until promotion.

Therefore the architecture currently cannot state, in a storage-independent typed way, which ruleset definition snapshot a durable `definition_id` belonged to once ruleset definitions become separately versioned/replaceable content.

### Recommended minimum logical contract

Introduce a **ResolvedCatalogSnapshot descriptor** as configuration/recovery metadata, not as a per-definition or world-record field and not as a second content catalog.

Conceptually:

```text
ResolvedCatalogSnapshot
    engine_capability_contract
        engine package/version identity
        machine catalog contract version

    ruleset_packages[]
        package_id
        package_version
        content_identity/digest
        compatibility identity as required

    campaign_definition_frontier
        campaign Git/tree/frontier identity

    session_overlay_identity
        ephemeral only; absent from durable snapshot until promoted
```

A durable world/checkpoint frontier must be interpretable against one compatible resolved catalog snapshot. Exact file/schema placement and Step-6 packaging remain later work.

This is deliberately package-level rather than per-record versioning.

## 5. Finding 0B-F3 — same-version runtime refresh can silently change catalog semantics unless catalog compatibility is part of the semantic contract

**Severity: SIGNIFICANT cross-contract risk; tied to F2.**

`ENGINE_UPDATES.md` allows a proven descendant runtime package with the same semantic engine version/package ID to be used silently as a compatible maintenance refresh.

That policy is safe only if same-version descendants cannot incompatibly change:

- existing executable capability semantics;
- existing shipped reusable definition meaning;
- definition kind for an existing ID;
- validation semantics in a way that invalidates accepted durable content without migration.

A raw package/source descendant relation proves ancestry, not semantic compatibility by itself.

### Required invariant

Within a same semantic compatibility line, catalog changes may be additive or otherwise explicitly backward-compatible, but may not repurpose/remove/incompatibly mutate an existing durable semantic definition/capability ID. An incompatible catalog change requires semantic adoption/migration rather than silent maintenance refresh.

The exact mechanism can be a catalog/package compatibility revision, manifest contract, or release-time compatibility audit. F2's resolved snapshot provides the place to express it without per-record versions.

## 6. Finding 0B-F4 — session definition promotion is not specified as distinctly as world-record promotion

**Severity: MODERATE.**

World local IDs intentionally rekey on promotion because campaign world identity uses allocator-owned persistent IDs.

Reusable definitions are different: their identity is already a semantic namespaced ID. Origin is loader/path context rather than a field inside the definition.

Recommended rule:

- a session-local **definition** that is promoted to campaign scope normally preserves its semantic `definition_id`;
- promotion changes owning layer/storage and publishes dependency closure, not semantic identity;
- promotion fails on any resolved-catalog ID collision;
- any local world records that reference the definition can then be promoted/rekeyed through the existing world-record mechanism;
- if the session definition used a namespace not permitted for campaign durability, promotion requires an explicit directed definition migration/new ID rather than silent rewrite.

No universal alias table is introduced.

## 7. Finding 0B-F5 — namespace ownership is described but not enforceable

**Severity: MODERATE, related to F1/F2.**

The definition schema describes IDs as `stable semantic namespaced ID` but validates only a broad machine-string grammar. There is no machine contract assigning namespace ownership to engine/ruleset/campaign/session packages.

The architecture does not need a global internet namespace registry. It does need the loaded package set to declare the namespace(s) it owns, and loader validation must reject definitions outside those namespaces or collisions with another owner.

This can be part of future package metadata rather than another field on every definition.

## 8. Finding 0B-F6 — LLM discovery has a safe minimum deferral

**Coverage: DEFERRED_OK to Step 3/4.**

Step 1 already provides enough separation to require a bounded catalog search interface over reusable definitions/capabilities while excluding runtime records. Step 3 owns exact candidate/binder shape and Step 4 later constrains knowledge-sensitive visibility.

Minimum carried invariant:

```text
search/ranking proposes candidates;
deterministic binding validates exact IDs/kinds/capabilities against the loaded resolved catalog snapshot;
model memory or search rank is never mechanical authority.
```

A search miss is not automatically a catalog gap. `unsupported/catalog-gap` may be emitted only after bounded capability/definition discovery and deterministic validation establish that no loaded expressible path exists.

## 9. Targeted failure cases

### Campaign defines same ID as shipped spell

Under shadowing, meaning depends on loaded layer. Unsafe. Under globally unique resolved IDs, load fails and campaign creates a new ID. Recommended PASS.

### Ruleset v2 removes definition referenced by durable world record

A package-set compatibility/migration check must fail before adopting the new resolved snapshot or migrate the reference. The LLM must not recreate a replacement from memory. Current architecture lacks the explicit snapshot descriptor. FINDING F2.

### Same engine version, descendant package changes a definition

Git ancestry alone is insufficient if semantic definition meaning changed. Same-version refresh must be restricted to compatible catalog evolution. FINDING F3.

### Local custom artifact becomes durable

Definition identity can remain stable while world/local IDs rekey. Promotion closure must publish the definition before/same transaction as durable dependent records. Current architecture has most pieces but lacks the explicit definition-promotion rule. FINDING F4.

### Future custom ruleset coexists with D&D

Without package namespace ownership and package identity, collision handling is underspecified. F2/F5.

## 10. Alternatives for the snapshot problem

### A — per-record qualified/versioned references

Store `(package_id, package_version, definition_id)` or definition version on every world reference.

Pros: every reference self-describes source.

Cons: duplicates package/version facts across potentially huge world state, complicates migration and mixed-version consistency, and undermines the accepted coherent-snapshot model.

**Not recommended.**

### B — layered same-ID shadowing

Keep plain IDs and use engine/ruleset/campaign/session priority.

Pros: easy customization.

Cons: semantic identity becomes context-sensitive; durable state can change meaning without changing; debugging and migration become difficult.

**Rejected.**

### C — globally unique resolved definition IDs + package-level resolved snapshot

Keep plain stable IDs; reject duplicates in the loaded catalog; identify package/frontier set once at campaign/checkpoint/runtime context level.

Pros: preserves current record shapes, coherent snapshot semantics, cheap references, deterministic lookup, future multi-ruleset support, and explicit migration boundary.

Cons: requires a package/snapshot metadata contract and campaign customization uses new IDs rather than shadowing.

**Recommended.**

## 11. Research applicability

npm package-lock is useful only as evidence for pinning an exact resolved dependency set; HDM should not copy npm's node-module tree or file format. Python packaging metadata is useful evidence that package name/version/dependency identity belongs at distribution scope, not every object. SemVer is useful only as a compatibility principle; HDM is still pre-1.0 and already has its own runtime update policy.

## 12. Current recommendation

- Apply F1, F4 and the minimum F6 wording as mechanically implied clarifications.
- Treat F2/F3/F5 as one package/snapshot architecture decision and send them through adversarial review before asking the human architect.

Provisional recommendation: **C — globally unique resolved definition IDs + package-level ResolvedCatalogSnapshot**.

Recommendation confidence: **HIGH** that a snapshot/package identity boundary is required; **MEDIUM-HIGH** on the exact minimum fields before Step 6 packaging design.
