# HDM Catalog — Admission and Gap Closure

Status: **ACCEPTED S6D-02 ARCHITECTURE OWNER**

Date: 2026-08-25

## 1. Decision

HDM maintains one exact machine-readable admission ledger for the current catalog generation. The ledger classifies every registered ID without turning admission into a false claim of complete implementation.

Semantic owner: `DEV/ARCHITECTURE/CATALOG_ADMISSION.md`.

Machine-readable traceability/disposition record: `DEV/CATALOG/catalog-admission-ledger.json`.

## 2. Admission model

### LAW S6D02-01 — EXACT SET ACCOUNTING

The set of `(registry_family, id)` pairs in the admission ledger SHALL equal the set in `DEV/CATALOG/core-catalog.json`. Duplicate, missing and extra ledger entries are invalid.

### LAW S6D02-02 — TWO INDEPENDENT AXES

Each ID has:

- one admission disposition: `ACTIVE_ADMITTED`, `EMBEDDED_NONOWNER`, `DORMANT_NONSELECTABLE` or `STALE_REMOVE`;
- one realization state: `COMPLETE`, exact downstream S6D owner, or `INHERITED_ACTIVE` with exact R2.x/WP owner.

Registration is not proof of complete realization. A downstream owner is not admission evidence by itself.

### LAW S6D02-03 — THREE SCOPE STRATA

- `S6D_PRIMARY`: full admission decision now.
- `ENGINE_ENUM_CONSISTENCY`: inherits current engine/domain owner; S6D-02 proves equality and absence of stale active references.
- `INHERITED_ROUND2`: inherits accepted R2.x/Step-5 owner; S6D-02 proves consistency and records future WP routing without creating an S6D realization obligation.

An inherited item moves into S6D-primary scope only if concrete contradiction or an unsatisfied S6D consumer proves the accepted owner insufficient.

### LAW S6D02-04 — EVIDENCE ORDER

Active admission requires one of:

1. canonical owner plus active machine/runtime consumer;
2. accepted supported-profile requirement plus exact downstream realization owner;
3. reachable accepted-work, package, recovery or retention dependency.

Otherwise the result is owner-approved dormancy with a meaningful trigger or stale removal.

Rules-baseline labels, generic domain familiarity, prose mention, historical inventory appearance and hypothetical future usefulness are insufficient alone.

### LAW S6D02-05 — CLASS MODEL IS INHERITED

Capability, reusable definition, world record, runtime record, embedded value and noncanonical projection remain distinct by the existing lifecycle/authority rule. S6D-02 does not reopen the model by analogy.

### LAW S6D02-06 — NO PLACEHOLDER STATE

There is no “registered placeholder” disposition. An active ID with missing detail names the exact downstream owner and missing contract. A dormant ID is nonselectable. A stale ID is removed coherently.

## 3. Current generation result

Catalog generation `2.0.0` contains 571 admitted IDs:

- 192 `S6D_PRIMARY`;
- 276 `ENGINE_ENUM_CONSISTENCY`;
- 103 `INHERITED_ROUND2`.

No current machine registry ID is removed by S6D-02.

The complete result is machine-owned in the ledger. Prose summaries do not duplicate its 571-ID enumeration.

## 4. S6D-primary routing

- reusable definition families: S6D-07, S6D-08 or S6D-09 according to domain;
- primary protocol values: S6D-05;
- Calculation Selectors and `rule.*` operations: S6D-03;
- MechanicalContext accessors: S6D-04;
- Activity `op.*` primitives: S6D-06;
- already sufficient class/identity destinations: `COMPLETE`.

Integrated S6D `COMPLETE-or-remove` applies only to S6D-primary IDs and residual Step-6 obligations.

## 5. Package admission

### LAW S6D02-07 — MINIMUM BUILT-IN PACKAGE PROFILE

Exactly one built-in package profile is currently required:

```text
package_id = hdm.rules.dnd2024-srd52-core
compatibility_id = hdm.rules.dnd2024-srd52.v1
catalog_generation = 2.0.0
semantic_content_root = GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/
selectable_now = false
```

Namespace claims are the semantic top-level prefixes corresponding to the 37 admitted reusable definition families.

This profile is not an empty executable rules seed. It becomes selectable only after S6D-07–09 content exists and S6D-11 proves manifest, dependency lock, digest, builder and loader contracts.

Additional packages require a current consumer; S6D-02 does not split the built-in seed speculatively.

### LAW S6D02-08 — NAMESPACE APPLICABILITY

Package namespace claims apply to reusable definition IDs. Engine capabilities/protocol IDs remain closed engine-owned vocabulary. World/runtime instance identities are not package namespace claims.

Campaign/session definitions remain owner-local frontiers and cannot shadow loaded same-ID definitions.

## 6. Failure admission

### LAW S6D02-09 — EXISTING FAILURE OWNERS REMAIN

`failure.catalog_context_incompatible` remains the execution failure code for package/catalog reconstruction failure, with a typed reason to be materialized by S6D-11.

`runtime.catalog_gap_report` remains the independently addressable unsupported-capability report after bounded discovery.

S6D-02 does not create one top-level execution failure ID for every diagnostic reason.

## 7. Retired references

### LAW S6D02-10 — RETIRED IDS MAY APPEAR ONLY AS NEGATIVE EVIDENCE

Retired IDs may remain in explicit retirement history and negative tests. They may not remain in current field/class tables or runtime guidance as selectable/current vocabulary.

The current retired audit covers:

- `world.relationship`;
- `world.timeline_marker`;
- `runtime.dirty_record`;
- `runtime.publication_batch`;
- `runtime.execution_segment`;
- `runtime.resolution_chain`.

`value.execution_segment` is not the retired runtime record.

## 8. Bounded owner repairs

- remove the obsolete `world.relationship` row from `ENTITY_STRUCTURES.md`;
- route Procedure-local combat timing/order/action-budget state to `runtime.procedure`;
- route significant items to `world.asset` and reusable properties to `definition.asset`;
- route per-subject item knowledge through the existing knowledge boundary;
- update the PC schema note from ITEM IDs to `world.asset` IDs.

No runtime algorithm or persistence migration is added.

## 9. Verification contract

Focused verification SHALL prove:

1. ledger/catalog set equality;
2. unique entry per pair;
3. all family profiles resolve;
4. census totals equal 571 and family counts match;
5. no placeholder disposition exists;
6. S6D-primary downstream routes are explicit;
7. inherited Round-2 entries are `INHERITED_ACTIVE` with exact owners;
8. package profile is nonselectable and has exact namespace claims;
9. retired IDs are absent from active machine sets;
10. stale active prose/consumer wording is repaired.

## 10. Downstream boundaries

- S6D-03–09 own the realization obligations recorded in the ledger.
- S6D-11 owns physical package manifest/lock/schema/builder/loader realization and final machine closure.
- S6D-12 attacks integrated admission/realization completeness.
- R2.7 WP-07+ retains its paused realization work.
- R2.7 WP-20 retains future released incompatible migration.

## 11. Human decision

Human decision required: **NO**.

The candidate applies accepted owners and the approved S6D scope. It introduces no new semantic state owner or material product trade-off.


## Step-6 corrections incorporated before review

### Ledger authority boundary

The ledger owns only admission disposition, scope stratum, realization routing, and evidence traceability. `DEV/CATALOG/core-catalog.json` remains the exact-ID authority, and canonical domain owners remain semantic authority. A ledger entry:

- MUST correspond bidirectionally to exactly one current `core-catalog.json` family/ID pair;
- MUST NOT admit an ID absent from the core catalog or override a semantic owner;
- MUST NOT be loaded as a runtime ruleset catalog or package source;
- MUST carry a trigger when dormant, an exact accepted owner when `INHERITED_ACTIVE`, and a legal downstream S6D owner when realization is deferred;
- MUST NOT remain `STALE_REMOVE` after canonical cleanup.

### Package-profile boundary

`ruleset_package_admission` is a **non-runtime admission plan/profile**, not a `RulesetPackageSnapshot`, manifest, lock member, or proof of reconstructive content closure. S6D-02 closes only the single built-in package topology and reserves definition-ID namespace ownership. Its 37 claims are explicit future semantic ID prefixes (for example `ability.*`, `skill.*`, and `spell.*`), not the `definition.*` kind identifiers. S6D-07 through S6D-09 own the exact definition IDs and semantic files; S6D-11 owns physical manifest/lock/builder/loader realization. Until those gates pass, the profile remains nonselectable and no active package snapshot is claimed.

### Failure-distinction preservation

S6D-02 does not collapse package/load failure semantics into `runtime.catalog_gap_report`. The active top-level execution code remains `failure.catalog_context_incompatible`, but S6D-11 MUST materialize a closed typed reason discriminant preserving at least: invalid manifest, content mismatch, missing dependency, ambiguous dependency, dependency cycle, package-ID ambiguity, namespace conflict, engine incompatibility, catalog incompatibility, resolved-set mismatch, and unreconstructable context. `runtime.catalog_gap_report` is only unsupported-capability evidence. The ledger records this downstream realization obligation; focused tests prevent the two surfaces from being treated as substitutes.

### Legacy-owner drift boundary

The focused PC-schema wording repair does not certify that legacy `knowledge`, `relationships`, flattened `mechanics`, or inventory shapes are canonical owners. They remain legacy projection/input surfaces whose migration is owned by S6D-07 and the already accepted Round-2 record owners; canonical subjective knowledge is `world.knowledge`, subjective relationship state is source-Actor-owned, significant inventory identity is `world.asset`, and mechanical truth is derived from accepted definition/effect/resource owners.

`ENTITY_STRUCTURES.md` is also aligned for `world.encounter`: durable encounter identity/status may reference its active `runtime.procedure`, while initiative, round, active participant and local procedure time are not world-record fields. Lore/knowledge field-shape refinement remains inherited WP-07 work and is not claimed as S6D-02 closure.


## Step-6 item-level evidence and embedded-value correction

Every ledger entry now materializes its effective scope stratum, disposition, realization state, semantic owner, evidence class, exact evidence citation, and active consumer or reachable accepted dependency. Family profiles remain compression/routing metadata only; they are not accepted as proof when an item-level field is required. S6D-primary admission rests on a current accepted owner requirement or current supported-profile dependency, never merely on the name of a later S6D domain.

All 35 `value.*` protocol kinds are `EMBEDDED_NONOWNER`. This is compatible with active usability: they are typed values embedded in an owning phase/interface and have no independent writable lifecycle. Their S6D-primary versus inherited-Round-2 realization routing remains separate from admission disposition. The earlier pre-review totals are superseded by the executable-capability quarantine correction below; effective strata remain 192 / 276 / 103.

The strict schema now admits explicit disposition, containing owner and dormant trigger; enforces closed strata/dispositions/realization states, conditional embedded/dormant/inherited rules, legal downstream owners, and the exact compatibility-reason list. Referential equality, profile existence, census arithmetic, exact evidence presence, namespace derivation, schema validation, prose repair assertions, and the prohibition on surviving stale entries are executable-test obligations.


## Step-6 executable-capability quarantine correction

Registration is not executable support. The final ledger therefore admits only the five selectors and seven `rule.*` operations materialized and consumed by `DEV/CATALOG/mechanical-surfaces.json`, plus all ten accessors materialized there. The remaining 29 selectors and 19 operations are `DORMANT_NONSELECTABLE` until S6D-03 proves complete metadata and supported-profile reachability. All 31 Activity primitives are `DORMANT_NONSELECTABLE` until S6D-06 provides an exact contract and a supported Activity consumer. Final admission totals are 457 `ACTIVE_ADMITTED`, 35 `EMBEDDED_NONOWNER`, 79 `DORMANT_NONSELECTABLE`, and 0 stale.

Each embedded protocol value names its actual containing architecture/interface owner; generic “exact owner” placeholders are forbidden. Executable checks require profile/family equality, reject placeholder owner/evidence text, require inherited owners, and enforce every downstream realization-to-owner mapping.

## Canonical authority and downstream boundary

This document is canonical for S6D-02 admission disposition, realization routing, evidence sufficiency and the built-in package admission-plan boundary. It does not replace exact IDs in `core-catalog.json`, semantic domain owners, or runtime package snapshots. S6D-03 is next; no S6D-03 design is performed here.
