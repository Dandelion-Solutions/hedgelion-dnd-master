# SP03 complete-membership realization — independent Senior follow-up

Status: **BOUNDED GO; IMPLEMENTATION ACCEPTANCE NOT GRANTED**
Date: 2026-10-07
Reviewed source: `4222a6c88234afeee893697241830b4e75521477`
Independent review: `ses_ee92526acffe5gZybN1lYAbj77`

This records the technical application of the existing
`2026-10-06-sp03-read-slice-and-policy-allocation.md` allocation, not a replacement
membership authority, production activation or full SP03 acceptance.

## Finding and disposition

P0 and HOT requested-key observations cover only their accumulated supplied
identities. Index nomination cannot prove native absence or detect an unrequested
new member. Existing production repository ports do not expose complete native
family enumeration, and the current LIVE reader does not support arbitrary
same-family collections. These are source capability limits, not permission to
assert an empty result.

**GO / SYSTEM_IMPACT: no architecture change required for the bounded route;
NEEDS_PO: NONE.** The accepted allocation permits authentic source-backed
membership preparation/conformance without waiting for SP04. Production
coverage/admission/fencing remains a separate native integration obligation.

Inspected anchors: `current_owner.py:192–331,422–430`;
`hot_store.py:300–367,448–508,683–701`;
`native_storage.py:184–200`; `policy_basis.py:97–118`;
`runtime_host.py:1669–1685,2383–2409`; `live_state.py:1085–1135`.
WP-11 canonical specification: `2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md:76,112–129`.

## Bounded implementation route

Implement the minimum read adapter in `GAME/TOOLS/mechanical_sources.py`.
Mechanical requests are closed Effect/Asset queries derived from compiled
consumers and validated subject bindings. No caller owner list, predicate,
path/backend/SQL selection or completeness flag issues evidence.

For the first qualifying conformance source, materialize actual native campaign
documents and routing records in a small task-owned repository, pin its real
immutable Git commit/tree objects, and enumerate/read the fixed native subtrees
`WORLD/EFFECTS/RECORDS` and `WORLD/ITEMS/RECORDS`. Validate complete traversal,
source identity, family/full identity, native route and payload. Parent-tree
evidence is required to prove an absent subtree empty. Truncation, malformed
entries, unavailable reads or capacity exhaustion hold rather than shortening
the universe. Neither expected fixture IDs nor discovery indexes define it.

Selected LIVE and actually admitted HOT sources retain their existing precedence
over pinned campaign records. Add their identities only with authentic supported
coverage. Unsupported LIVE multiplicity/creation coverage holds. Raw staged HOT
rows and restart residue do not gain admission; present positive Effect/Asset
HOT establishment is not fabricated before its producer exists.

Minimal read-side extensions may touch `current_owner.py` for operation/session
source association, `hot_store.py` for an internally acquired coherent admitted
mechanical roster, and `native_storage.py` for fixed-family tree/route validation,
only if needed. Preserve P0 `require()`/admission/precedence. A wholesale mandatory
RepositoryPort extension or deployment rewiring is unnecessary for this slice.
The minimum authentic-observation join may touch `mechanical_context.py` and
`activity_contracts.py`; shared physical writers remain serialized.

## Closure and issuance conditions

Effects use native target/lifecycle/source/support and the exact accepted subject
binding/profile generation. Mentioning an Actor elsewhere does not establish
target-local membership. Retain terminal/wrong-subject candidates as material
exclusion evidence. Suppression/inapplicability is not termination.

Assets derive direct ownership, reverse container descendants and required
ancestors from native placement. Validate missing parents/cycles/exclusive
placement, held/worn/access state and applicable attunement/form/conversion
references. Possession is not accessibility. Price/handling/passive mechanics
come from admitted definitions, not duplicated equipment Effects.

Relevant owners: `HEALTH_EFFECTS_RECOVERY.md:62–68`;
`world-effect-state.schema.json:7–35,63–80`; lifecycle annex:30–38;
`ASSET_MODEL.md:201–203,266–304,319–341,369–399`;
`world-asset-state.schema.json:7–30`; `RULE_ELEMENT_MODEL.md:20–36`.

Issue recursively immutable process-local observations only after complete
closure: campaign/operation/session, compiled consumer/query/subjects, acquired
universe/source bases, full identities/P0 reads, matching members/dependencies
and material exclusions. Use genuine object/issuer lineage, not a copied seal.
Copied/replaced/rebound/mutated observations cannot inherit issuance.

Revalidation repeats universe acquisition and checks additions/removals,
excluded-to-included changes, container subtree movement, relevant native
changes and selected LIVE/HOT admission changes, not merely previous members.
Confirm coverage around dependent P0 reads; races hold. Keep coverage separate
from relevant value-cache equality. No global SHA substitutes for the relevant
mechanical footprint and no SQLite transaction spans repository I/O.

## Production boundary and required proof

Small complete source enumeration is permitted in this explicit conformance
environment. Ordinary casts must not enumerate/parse every campaign Effect/Asset
body (`RULE_ELEMENT_MODEL.md:422–457`). General production needs a bounded
rebuildable read model under existing storage/currentness owners, with coverage
and invalidation coupled to native acceptance. Its atomic producer/fence joins
SP04; it is not another inventory/Effect truth owner.

Escalate a proposed new persistent completeness/epoch/tombstone authority,
changed LIVE claims/packing/currentness, new admission/mutation authority,
ordinary-path broad scan, wider mandatory ports or unsupported subject semantics
under execution-process section 6.1. Such a technical boundary is not
automatically a human product decision.

Required proof uses the actual installed compiler/preparation route: genuine
empty/nonempty membership; matching records absent from every discovery index;
addition/removal and excluded-to-included invalidation; nested/moved/blocked or
broken containers; wrong roles/subjects/generations; LIVE precedence/unavailable
holds and raw HOT/restart rejection; forged/copied/rebound observations;
unrelated-owner/cache and P0/compiler regressions. No caller HP/AC/resource/
Condition substitution, RNG, spend or establishment is introduced.

## Version and continuation

VERSION_IMPACT: NONE for this development-only source-review record. It changes
no current version-bearing machine/runtime/schema/catalog owner or projection.
Implementation assesses actual namespaces separately: new module revision1;
material existing modules increment from refreshed values; projection/schema/
digest changes follow their owners. No automatic engine/campaign/storage/catalog
bump and no blanket implementation NONE.

Next action: source-backed RED witness with a matching Effect and nested Asset
omitted from all discovery indexes, acquisition without supplied member IDs, and
actual source addition/removal invalidating the old observation. Complete
membership alone does not issue `W05_SPELL_CONTEXT_CAST_CONSUMERS_READY`; policy
DAG/calculation/preflight, independent review and integration proof remain.
