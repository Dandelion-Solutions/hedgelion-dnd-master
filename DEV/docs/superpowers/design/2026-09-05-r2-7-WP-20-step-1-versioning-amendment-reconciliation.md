# R2.7 WP-20 Step 1 — Versioning Amendment Reconciliation

Status: **SUPPLEMENTAL STEP-1 REVIEW INPUT — MANDATORY SENIOR REVIEW PENDING**

Date: 2026-09-05

This artifact records a post-Brief, human-approved architecture amendment discovered while WP-20 was already stopped at its mandatory Step-1 Senior gate.

It does not start WP-20 Step 2. It preserves the historical Step-1 Source Manifest / Architecture Task Brief / whole-project critic as completed provenance and adds the newly accepted versioning architecture to the Senior review basis.

## 1. Trigger

After the original WP-20 Step-1 package was completed, a repository-wide read-only inventory found widespread ambiguity/drift across HDM-owned version namespaces:

- engine release identity;
- CORE/runtime module versions;
- independent DEV revision counters;
- persistent family schema versions;
- aggregate `ENGINE_VERSION.schema_version`;
- storage format versioning;
- catalog `2.0.0` generation spelling;
- ruleset `package_version`, version-bearing `compatibility_id`, protocol schema versions and `_V1` digest-domain literals;
- runtime package and launcher counters;
- stale cross-document version references.

Research evidence is preserved in:

- `DEV/docs/superpowers/research/2026-09-05-versioning-namespace-inventory-and-analysis.md`.

The human architect then approved the proposed normalization architecture.

## 2. Newly accepted canonical input

Canonical implementation-facing amendment:

- `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md`.

Compact release/versioning policy projection:

- `DEV/RELEASE/VERSIONING.md`.

Neighboring canonical owners already reconciled at documentation-law level:

- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`;
- `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md`.

Machine realization is intentionally deferred.

## 3. Accepted version taxonomy

Exactly three HDM-owned numbering categories are canonical:

```text
A — ENGINE RELEASE
    MAJOR.MINOR[-prerelease]

B — ENGINE-BOUND COMPONENT/MODULE
    ENGINE_MAJOR.ENGINE_MINOR.REVISION

C — INDEPENDENT INTEGER COUNTER
    *_revision / *_schema_version / *_generation / domain-local ordinal
```

Category-C subtypes share an integer representation but remain semantically distinct.

External SRD/D&D, JSON Schema draft, Git and third-party version namespaces remain external and are not normalized by HDM policy.

## 4. Accepted compatibility/migration consequences

The amendment establishes these WP-20 inputs:

1. version equality/order is meaningful only inside one typed namespace;
2. engine version never substitutes for the full campaign compatibility envelope;
3. same compatibility generation means eligibility for a proof, not proof itself;
4. unsupported newer schema/generation fails closed;
5. migration is a directed explicit graph edge, never arithmetic over integers;
6. reverse/downgrade migration is not a baseline promise and requires an explicit reverse edge;
7. released assets are immutable rather than rewritten into newer schemas;
8. one semantic owner exists per version/generation and projections must equal it;
9. mixed coordinated catalog generations are invalid;
10. custom digest/canonicalization generation is explicit/typed and old/new generations are not one raw comparison space;
11. current pre-release hashes/fixtures MAY be recomputed during later normalization with no compatibility shim;
12. local transform success is not authoritative migration success before the existing confirmed publication edge.

## 5. Entity-specific accepted decisions

### 5.1 CORE/runtime modules

Keep `ENGINE_MAJOR.ENGINE_MINOR.REVISION` semantics. Engine bump alone does not mass-renumber unchanged modules. All versioned shipped modules converge on `framework_module_version` naming. Future engine-line claims are invalid.

### 5.2 Persistent record schemas

Keep independent integer family `schema_version`. Different record families may remain on different schema versions.

Breaking persisted family changes require a local schema bump plus explicit migration.

### 5.3 Campaign aggregate persistent contract

The ambiguous shared aggregate `ENGINE_VERSION.schema_version` concept is superseded by:

```text
campaign_contract_generation
```

Runtime/development manifests project the target generation. Released campaigns retain immutable creation generation plus mutable current adopted generation.

A breaking local family schema change requiring campaign migration MUST bump campaign contract generation. Aggregate generation may also bump for persistent semantic migration even without file-shape change.

### 5.4 Storage

Storage compatibility uses independent integer `storage_format_generation` in the target representation. Storage migration is independent from campaign migration.

### 5.5 Catalog

Catalog compatibility uses integer `catalog_generation`.

The current clean-slate pre-release `2.0.0` spelling maps conceptually to generation `2` and will be normalized later.

All coordinated projections must match the canonical generation. Local catalog artifact schema versions remain independent.

### 5.6 Ruleset packages

Target representation separates:

```text
package_revision
compatibility_family
compatibility_generation
manifest_schema_version
catalog_generation
exact typed content/resolved-set identity
```

Package revision is order only. Compatibility generation is the semantic line. Exact content identity remains separate.

Current pre-release `package_version`, version-bearing `compatibility_id`, `2.0.0` catalog spelling and `_V1` digest-domain spelling are realization debt, not future authority.

### 5.7 Package/protocol schemas

Runtime package, ruleset manifest, lock, inventory, compatibility-result and attestation schemas retain independent integer schema versions. Released artifacts are immutable; support/reject/regenerate replaces in-place schema rewriting.

### 5.8 Digest/fingerprint generations

Digest/canonicalization generation becomes explicit/typed in architecture. If an exact digest escapes its enclosing schema context across releases, the persisted identity must retain enough generation/type context to interpret it.

Current pre-release digest identities may all be recalculated during later normalization.

### 5.9 DEV revisions / launcher / dynamic currentness

DEV `*_revision`, launcher revision and owner-local runtime/currentness ordinals remain independent integers and do not become engine-prefixed pseudo-SemVer values.

## 6. Effect on original WP-20 Step-1 Brief questions

The accepted amendment resolves/refines the following framing questions without performing Step-2 research:

- **Q20-01 / Q20-03:** compatibility identity is explicitly multi-axis and version namespaces are typed;
- **Q20-04:** migration selection is an explicit directed graph, not numeric inference;
- **Q20-05:** no default reverse/downgrade support; reverse requires an explicit edge;
- **Q20-12 / Q20-13:** unsupported future schema/generation fails closed; immutable old assets are not silently rewritten;
- **Q20-14:** rollback remains publication/recovery semantics, not generic reverse migration;
- **Q20-16:** several current machine version spellings are now explicitly classified as pre-release realization debt.

The amendment does **not** resolve unrelated Step-2 owner/evidence questions such as creator-vs-storage-owner migration authority, full migration graph realization, exact affected persistent owner sets, LIVE quiescence/absorption details or publication implementation shape.

## 7. Supplemental adversarial check

The amendment was checked against the original Step-1 critic challenges.

| Challenge | Reconciliation |
|---|---|
| accidental pre-release compatibility resurrection | Further reduced: clean-slate renumbering/hash recomputation explicitly carries no shim obligation. |
| one universal version scalar | Rejected more strongly: three categories + typed Category-C subtypes. |
| mutable tag/latest migration selection | Unchanged; still forbidden. |
| partial/in-place authoritative migration | Unchanged; version normalization does not bypass publication/CAS. |
| stable identity/history loss | Exact identities become more typed; semantic native identity invariants unchanged. |
| unsafe LIVE migration | Unchanged; still Step-2 owner analysis. |
| unsupported rollback promise | Reduced: reverse migration is explicitly not baseline rollback. |
| silent forward/backward tolerance | Rejected; unsupported newer contracts fail closed and reverse edges are explicit only. |
| stale machine/version artifacts treated as authority | Reduced: named pre-release spellings are explicitly realization debt. |
| duplicate compatibility/version owners | Reduced by one-owner/projection law. |
| architecture deferred as implementation detail | Version taxonomy/compatibility laws are now canonical. |
| implementation detail promoted into architecture | Exact code/DDL/scripts remain deferred; only semantically material target fields/contracts are fixed. |

Supplemental result:

```text
SUPPLEMENTAL_BLOCKING: 0
SUPPLEMENTAL_SIGNIFICANT_UNRESOLVED: 0
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_REOPEN_REQUIRED: NO
```

The versioning amendment is consistent with the original Step-1 framing and strengthens it; it does not authorize Step 2.

## 8. Senior review requirement

The mandatory Senior review must now evaluate the complete Step-1 basis as:

```text
original Source Manifest
+ original Architecture Task Brief
+ original whole-project Task-Brief critic
+ versioning namespace research inventory
+ human-approved canonical versioning amendment
+ this supplemental reconciliation
```

Required gate remains:

```text
WP20_STEP1: COMPLETE — MANDATORY SENIOR REVIEW
WP20_STEP2_AUTHORIZED: NO
WP20_STEP2_STARTED: NO
WP21_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
VERSION_NORMALIZATION_IMPLEMENTATION_STARTED: NO
```

No prompt for machine normalization/renumbering is produced by this artifact.
