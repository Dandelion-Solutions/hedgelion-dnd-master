# SP02 compiler contract source — independent Senior allocation

Status: **GO — BOUNDED ACCEPTED-OWNER REALIZATION; NO SP01 REOPEN**
Date: 2026-10-06
Review base: `6277b8504b17a101afe4a30f7877f6b1f5f1ff87`
Accepted SP01: `30c5a66f234b75bec926462c6301454133506884`

Independent Senior source review confirmed the implementation gap: current
engine inventory schema 2 carries family/contract ID/hash summaries, not the
compiler-relevant primitive/consumer/read/value/pair/fact/profile bodies.
SP01's assertion-only structural projection correctly does not admit execution.
Execution annex §§3–5/7 already requires exact source contracts for cold
admission, frozen retention, compilation and rejection; this is missing
projection/allocation, not an unresolved product decision.

Source route inspected: `ruleset_package.py` inventory validation,
`catalog_runtime.py` basis/source admission, existing canonical assemblers and
`validate_ruleset_package_closure.py` inventory/hash producer; Activity and
machine-closure/catalog admission owners; stable SP02/common extension and
accepted complete-plan review. No production code/test PASS is inferred here.

## Authorized bounded implementation

Retain the existing `engine_contract_inventory_source: object` callable boundary
and inventory schema 2/BoundCatalogContext serialization where possible. A
closed source carrier supplies the inventory and authenticated immutable
compiler projection. The binder reuses exact natural-owner/package/source
checks; it does not accept a caller self-hash, duplicated inventory or
`validated=True` as authority. Old admitted bytes and contexts remain retained.

The existing DEV canonical source assembly is the sole derivation owner. Add
minimum deterministic generation/equality verification there. Coordinator
allocates one derived installed path, `GAME/TOOLS/activity_compiler_contracts.json`,
schema 1, distinct from SP01's structural assertion artifact. It carries no
independent authoring/activation or semantic-identity authority. A cohesive DEV
producer helper is allowed; no parallel family registry.

Important hash law: existing family identity is
`sha256(ENTRY_DOMAIN + canonical_json(assembled_family_payloads))`, preserving
manifest order. Removing DEV annotations and hashing the sanitized projection
does not reproduce that source identity. Preserve original-source identity
separately, and verify exact path-neutral projection bytes against the same
source assembly at the trusted build/installed source boundary.

`catalog_runtime.py`/`ruleset_package.py` may realize the minimum source/freeze
interface; `validate_ruleset_package_closure.py` may produce/verify the derived
view. `release_builder.py` and focused package/release consumers may change only
if necessary for installed-source authentication/stale-output rejection. Change
serialized carrier schemas and their consumers only when an actual shape change
requires it; do not opportunistically widen the catalog basis.

Conformance sources exercise real exact-source admission under their temporary
package/context. No runtime test/trusted bypass, schema-to-admission inference,
production ACTIVE_ADMITTED change or installed full support claim. Existing
synthetic inventory binder fixtures are not compiler authentication positives.

## Required proof and namespace gates

Deterministic complete family/member projection equality; missing/extra/stale/
tampered/foreign source negatives; dormant/unknown primitive/pair/accessor/fact/
profile/occurrence rejection; old frozen warm handle survives path mutation,
new cold load rejects unavailable source. Complete typed cache keys and zero
warm census/compile/network reads; real binder -> catalog -> compiler -> command
join; operation without DEV and path-neutral installed projection. Run exact
SP02 command and actual affected package/release/SP01 regressions.

New Activity runtime starts current-line revision 1; projection schema 1;
material existing module changes use fresh namespace values. Preserving inventory
shape/hash semantics does not itself bump inventory or digest generation.
Actual participating fields/normalization changes require their own synchronized
owning gate. No blanket VERSION_IMPACT NONE or count-based compatibility.

Excluded: native dispatcher/acceptance, grants/acquisition, SP01 reopening,
new/dormant production admission, full339 support, migration policy, latency or
release readiness. SP28/SP29 still own final production registry/support joins.
Reopen only for genuinely absent semantic contracts, new authority/runtime DEV
access, compatibility change, broader permissions or weakened source proof.
NEEDS_PO: NONE. SP02 completion remains unestablished until actual implementation,
independent review, required proof and publication/read-back.
