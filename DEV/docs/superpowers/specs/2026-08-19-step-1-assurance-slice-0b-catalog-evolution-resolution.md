# Step 1 Retrospective Assurance — Slice 0B Resolution

Status: **ASSURED / AMENDED / STEP 1 REMAINS CLOSED**

Target branch: `feature/mechanical-runtime-hot-state`

## 1. Verdict

The accepted engine/ruleset/campaign/session layering remains viable, but its
evolution semantics required explicit correction. The architecture now treats
catalog loading as construction of one deterministic `ResolvedCatalogContext`,
not as ambient last-layer-wins overriding.

Step 1 remains closed; no accepted class/ownership boundary needed reversal.

## 2. Accepted amendments

Canonical contract:

- `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md`

It establishes:

1. one logical `ResolvedCatalogContext` for a loader/binder/Resolution;
2. one `definition_id` maps to at most one definition inside that context;
3. duplicate IDs across loaded sources fail validation;
4. catalog layer order is assembly/dependency/discovery order, not shadowing;
5. campaign/session content cannot implicitly replace shipped content by reusing
   its ID;
6. true changes to existing ruleset definitions belong to explicit ruleset
   profile/package migration/fork semantics, deferred to Step 6;
7. session definition promotion normally preserves semantic definition ID while
   world local IDs continue to rekey;
8. namespace ownership belongs at package/context level;
9. durable restore must identify a compatible engine/ruleset/campaign frontier,
   rather than depending on ambient files or LLM memory;
10. same-version source ancestry is provenance evidence, not sufficient proof of
    catalog semantic compatibility;
11. search/ranking proposes candidates but deterministic validation against the
    same resolved context remains authority.

## 3. House-rule/customization disposition

No generic same-ID campaign override is introduced.

Initial safe model:

```text
new campaign content
    -> new campaign-owned definition IDs

house rules expressible through existing policy/Feature/Rule Element/Activity
    -> use those typed mechanisms

true replacement of existing reusable ruleset definitions
    -> explicit future ruleset package/profile migration/fork mechanism
       if Step 6 proves it necessary
```

This retains option value without weakening stable definition identity today.

## 4. Ruleset package identity

The assurance found that `rules_baseline` text and machine `catalog_version` are
not, by themselves, sufficient to identify a future independently versioned
ruleset definition snapshot.

The minimum semantic requirement is now fixed: a future selected ruleset package
must have package-level identity/version/content compatibility sufficient to
reconstruct a compatible ResolvedCatalogContext. Exact manifest fields and
storage are Step-6 work. Per-definition/world-record package version fields are
rejected.

## 5. Runtime update interaction

`ENGINE_UPDATES.md` same-version descendant refresh remains a provenance/update
policy, but it may not be interpreted as permission for incompatible catalog
semantic changes. Step-6 release/migration validation must distinguish compatible
additive/maintenance evolution from an incompatible definition/capability change
that needs explicit adoption/migration.

## 6. External research applicability

Package managers commonly distinguish package-level name/version/dependency
metadata and lock a resolved dependency set for reproducibility. This supports
HDM's package-level context boundary but does not justify copying npm/Python
package formats. SemVer similarly supports the principle that released semantic
contracts cannot change incompatibly without version/compatibility consequences;
HDM retains its own pre-1.0 update policy.

## 7. Safe deferrals

Step 3:

- exact typed discovery candidate/binder protocol.

Step 4:

- knowledge/visibility filtering of catalog/context discovery.

Step 5:

- checkpoint/publication transport of the durable catalog-context identity.

Step 6:

- ruleset package manifest and namespace schema;
- ruleset package derivation/fork mechanics if required;
- compatibility/migration tooling;
- full SRD seed packaging.

These deferrals are now bounded by a minimum earlier contract and are no longer
unowned assumptions.

## 8. Final disposition

Recommendation: **KEEP Step 1 closed with the catalog-resolution amendment.**

Human decision required: **NO** under current product semantics. A future human
gate is required only if transparent same-ID campaign overriding of shipped
content becomes an explicit product requirement.

Confidence: **HIGH** for unique IDs + ResolvedCatalogContext; **MEDIUM-HIGH** for
deferring concrete ruleset-package/fork implementation to Step 6.
