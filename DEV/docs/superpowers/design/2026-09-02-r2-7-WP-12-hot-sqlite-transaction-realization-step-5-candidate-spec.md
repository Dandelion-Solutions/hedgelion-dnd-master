# R2.7 WP-12 — HOT, SQLite and Transaction Realization — Step 5 Candidate Specification

Status: **CANDIDATE — READY FOR WHOLE-PROJECT ADVERSARIAL REVIEW**

## 1. Scope

WP-12 selects the local HOT/SQLite machine-realization contract for already
accepted native owners and transaction/currentness laws. It does not change
semantic ownership, durable campaign topology, publication authority, recovery
source-selection law, live claim law, bootstrap/migration or implementation code.

The selected direction is:

> **TYPED NATIVE-OWNER HOT STORE + NARROW REBUILDABLE DERIVED HELPERS**

SQLite is the baseline local transactional substrate. It is not durable campaign
canon and not a semantic owner merely by storage format.

## 2. Core model

Conceptually, the active local runtime maintains:

```text
NATIVE OWNER WORKING STATE
    validated owner payload
    + owner-defined native identity
    + selected native source/currentness basis
    + local generation / dirty-publication metadata

DERIVED SUPPORT
    routing/query/reverse-lookup/currentness helpers
    source/ref cache
    deterministic derived mechanics caches

EPHEMERAL OPERATIONS
    prospective execution overlay
    frozen publication attempt
    recovery-attempt composition
    Context Runtime request/bundle/trace
```

These are physical/operational categories. They do not replace the semantic owner
classes already defined by Actor/Asset/Effect/runtime/etc. contracts.

## 3. Native owner envelope

### LAW WP12-1 — SQLite format does not create semantic authority

A value physically stored in SQLite retains the semantic owner, lifecycle,
identity and mutation rules defined by its native owner contract.

No SQLite table name, rowid, primary-key surrogate, query order, trigger or local
freshness timestamp may redefine semantic identity, currentness, chronology,
eligibility, ownership or gameplay truth.

### LAW WP12-2 — Current owner payload is validated and typed

A local row representing native owner state must identify the admitted native
family and owner-defined identity and must validate the owner payload through the
applicable current machine/owner contract before that payload may become accepted
current local state.

The owner envelope is not an arbitrary JSON property bag. Unknown/unadmitted
family payload or invalid owner shape is a typed validation/integrity failure.

### LAW WP12-3 — Owner identity is native, never SQL-generated

Simple, derived, composite and singleton identities remain those defined by the
current identifier policy and owner contract.

SQL `rowid`, AUTOINCREMENT values, insertion order and physical key layout are
implementation-only and may not escape as gameplay/native identity. Composite
owners such as knowledge/disclosure retain their ordered native components.

### LAW WP12-4 — One local current representation per native owner identity

For the active local runtime/campaign authority context, one native semantic
owner identity has one accepted current owner-state representation. Campaign/live
source selection is currentness/write-routing metadata for that owner, not a
license to keep competing writable campaign and live copies.

A stale source copy may be retained only as explicitly non-current evidence/cache
where a concrete operation requires it; it cannot be mutated as current truth.

## 4. Local establishment and transactions

### LAW WP12-5 — Singleplayer/local owner state may become established in HOT first

Where the native owner contract permits local establishment before durability,
one accepted ExecutionSegment may commit current owner state into SQLite and make
that state established `VOLATILE_DIRTY`/SOFT under Step 5.5 even when the last
Git-published native record is older.

Loss before applicable durability publication returns recovery to actual durable
native sources. Recovery never invents the lost newer state.

### LAW WP12-6 — ExecutionSegment is the local atomic commit boundary

One local SQLite transaction implements one accepted Step-3 ExecutionSegment or
another already-defined native local atomic edge.

As applicable it may atomically advance:

- native world owner state;
- Procedure state;
- Command/Resolution execution state;
- fixed RNG and accepted execution continuity;
- Continuation create/consume state;
- MechanicalEvent/receipt/trace evidence required by the segment;
- mandatory child/firing identity;
- idempotency state;
- owner generation and dirty/publication bookkeeping;
- helper cache/index updates or invalidations that must not observe a half-commit.

Physical co-commit does not merge those semantic owners.

### LAW WP12-7 — No transaction spans external dialogue or repository I/O

A SQLite transaction may not remain open across:

- player choice or reaction dialogue;
- another host/model exchange;
- GitHub/repository read or write;
- campaign publication ref transition;
- live source CAS;
- external research/network work.

Execution suspends/closes the local segment first and uses the already accepted
Continuation/owner protocols where external input is required.

## 5. Runtime execution-owner realization

### LAW WP12-8 — Runtime lifecycle owners remain separate

Interaction, IntentPlan, RuntimeCommand, Procedure, Resolution and Continuation
retain separate native owner rows/lifecycles according to the current catalog and
schemas.

WP-12 introduces no generic `pending_work`, `job`, `obligation`, `transaction`,
`workflow` or `execution_snapshot` semantic owner.

### LAW WP12-9 — ExecutionSegment remains embedded

ExecutionSegment remains an embedded committed edge under the owning
Command/Resolution contract. SQLite implementation may physically optimize its
storage, but WP-12 does not introduce `runtime.execution_segment` or an
independently writable segment table/class as semantic architecture.

Receipts/events/traces similarly retain their existing evidence/owner roles and
do not become alternate current-state authority.

## 6. Hydration, routing and currentness

### LAW WP12-10 — Known-ID hydration uses the WP-11 direct route

For a known native identity:

```text
native family + owner identity
-> WP-11 deterministic route
-> read exact selected native source/path
-> validate family + complete native identity + applicable owner schema
-> adopt as clean local owner state at that exact source basis
```

Known-ID hydration does not require directory enumeration or family-index lookup.

### LAW WP12-11 — Discovery/index helpers never prove authority or absence

A family index or local derived query index may locate a candidate. Material use
must then resolve/adopt the applicable current native owner.

Index/cache omission is not semantic absence unless a separate owner contract
explicitly provides complete authoritative enumeration for that scope. SQL query
order cannot select mechanics/fiction unless an owner supplies an explicit order
key/contract.

### LAW WP12-12 — Exact source basis travels with local currentness

Local owner/admitted support state retains enough exact native source basis to
validate currentness, including source/ref/scope and exact revision/blob/tree
identity as applicable to that owner/source contract.

Source movement invalidates only affected owner/helper state and dependencies.
No campaign-global source revision/frontier is introduced.

## 7. Derived support and Context Runtime

### LAW WP12-13 — Derived helpers are explicitly rebuildable

Local reverse indexes, family/query caches, loaded-record caches, MechanicalContext
cache, effect/condition aggregation, dependency/query caches and similar derived
structures are rebuildable from current native owners/evidence.

They may improve bounded lookup and atomic local visibility, but they cannot own
current gameplay values, lifecycle, eligibility, chronology or publication
authority.

### LAW WP12-14 — Context Runtime controls remain ephemeral/derived

ContextNeedProfile, RoleContextRequest, RoleContextBundle, ContextTrace, ephemeral
source basis and allocation state receive no durable/native owner or generic HOT
truth table under WP-12.

A concrete bounded derived query helper may support their runtime discovery, but
its contents remain non-authoritative and eligibility/currentness is revalidated
through R2.3/WP-09 laws.

## 8. Dirty state and publication handoff

### LAW WP12-15 — Dirty bookkeeping is owner-generation-specific and scope-relative

Local runtime tracks enough operational metadata to identify:

- the current local owner generation/fingerprint represented by accepted bytes;
- whether that generation is sufficiently durable in its required native source;
- the applicable durability/publication policy partition or scope;
- the source/currentness basis against which publication is being prepared;
- the still-relevant unpublished exposure basis needed by the owning policy.

WP-12 does not introduce one campaign-global dirty generation, one global
`durable_frontier_time`, a global HARD queue or a universal durability timer.
Exact boundary selection/publication policy remains WP-13.

### LAW WP12-16 — Publication attempt is frozen ephemeral operation state

Before remote campaign publication, deterministic persistence code freezes the
exact owner generations, dependencies, source/ref basis and resulting native path
delta required by Step 5.6.

That frozen attempt is an immutable in-memory operation object/snapshot. WP-12
does not introduce a generic persistent publication journal or transaction-log
owner.

Repository object creation and ref update occur after the local freeze and
outside SQLite transactions.

### LAW WP12-17 — Publication success clears only the frozen generation

If publication covers owner generation G:

```text
mark G durable under the confirmed compatible native source
if current local owner generation == G:
    clear its dirty membership
else:
    retain current newer generation as dirty
```

A later G+1 must never be cleared merely because G was published successfully.
Confirmed remote authority movement may require targeted local currentness
adoption/revalidation before dependent continuation.

## 9. Live/shared state

### LAW WP12-18 — Local SQLite commit does not establish shared live canon

For a live-claimed native owner whose accepted contract requires write-before-
reveal/source publication, a prospective local result is not shared established
state merely because SQLite committed/staged it locally.

The runtime freezes the deterministic prospective transition, performs the
required exact-source live CAS outside SQLite, and only after confirmed compatible
acceptance adopts the resulting exact live source/current owner state into local
HOT.

There is no SQLite + live-source distributed transaction.

### LAW WP12-19 — Live currentness follows selected claims and exact source revision

Local live-backed owner rows/helpers are valid only under the current selected
live route/claim and exact source basis. A stale/rejected/closed source invalidates
the affected prospective/current helper state according to Step 5.8.

Campaign base state does not silently become fallback current truth for an owner
still selected to live authority.

## 10. Recovery and checkpoint relation

### LAW WP12-20 — Local HOT database is not cold-recovery authority by existence

A surviving local SQLite file/cache does not outrank Step-5.7 current native
source selection merely because it is newer-looking or available locally.

Cold recovery starts from current native authorities and exact source pins.
Whether an implementation may safely reuse any local bytes as validated cache is
a performance/implementation optimization subordinate to source validation; it
cannot resurrect unpublished lost SOFT or create a `RecoveryCut` owner.

### LAW WP12-21 — Recovery attempt remains ephemeral

The selected campaign/live/operational source composition, hydration roots,
dependency closure and validation state for one recovery attempt remain an
in-memory operation value. No persistent generic recovery-attempt table/frontier
is introduced.

### LAW WP12-22 — Checkpoint remains optional evidence

Checkpoint may be loaded/cached as its existing native immutable evidence record.
It does not become current-state authority, root membership authority, save proof
or a local currentness frontier. Current noncanonical checkpoint fields remain
WP-14 realization debt and are not re-adopted by WP-12.

## 11. Storage metadata/template boundary

### LAW WP12-23 — Storage metadata is configuration/provenance, not campaign HOT owner

`DND_STORAGE.yaml` may be loaded/cached for storage discovery, format validation,
storage-owner operations and baseline runtime provenance. Its `engine.baseline`
applies to new-campaign default selection only and cannot override an existing
campaign's `MANIFEST.engine.current`.

Storage metadata publication remains a separate storage-default-branch operation,
not a campaign/local owner transaction.

### LAW WP12-24 — Storage template prose has no machine authority

`GAME/TEMPLATE/STORAGE_README.md` requires no SQLite/native record. It remains a
supporting human-facing template whose statements must remain consistent with
actual owning storage/branch/runtime contracts.

## 12. Physical-shape constraints left to implementation

The implementation plan may select exact DDL, payload encoding, SQLite pragmas,
file location/lifecycle, typed access APIs and narrowly normalized helper columns
only if all laws above remain mechanically enforceable.

Baseline expectation:

- a small owner-state/envelope surface keyed by explicit native family + owner
  identity and current source basis;
- separate operational source/currentness and dirty-generation support where
  that improves invariants without becoming owner state;
- derived/query helper tables only for concrete bounded consumers;
- no universal schema-generated entity model or reflection layer beyond current
  need.

A future dedicated family table/projection is admissible only for a concrete
validated need and remains subordinate to the native owner/schema. No such need
is selected by current WP-12 evidence.

## 13. Cross-system impact

Depends on:

- Step-3 execution owners/ExecutionSegment;
- Step-5.2/5.5/5.6/5.7/5.8 recovery/durability/publication/live laws;
- R2.3/WP-09 Context Runtime;
- WP-10 logical record families;
- WP-11 routes/identity/index rules;
- current Actor/Asset/Effect/catalog/runtime machine contracts.

Constrains:

- WP-13 durability/SAVE/publication machine realization;
- WP-14 recovery/checkpoint realization;
- WP-16 multiplayer/live realization;
- WP-19/WP-20 bootstrap/migration realization;
- WP-22 deterministic conformance tests;
- WP-24 measured performance/scale evaluation;
- later implementation-plan data-access/transaction interfaces.

Owns:

- only the local HOT/SQLite physical working-state/transaction boundary and its
  authority-preserving realization laws.

Does not own:

- gameplay semantics;
- durable native paths/topology;
- publication timing/ref protocol;
- recovery source selection;
- live claim/close/absorption semantics;
- bootstrap/migration;
- final implementation API/DDL.

## 14. Verification obligations for later implementation

The approved implementation/verification plan must prove at least:

1. owner payload cannot be accepted without family/native identity/schema
   validation;
2. SQL row identity/order cannot leak as native identity/chronology/mechanics;
3. one ExecutionSegment atomically commits all implicated local owner/runtime/
   evidence/dirty changes or none;
4. no SQLite transaction spans external dialogue or repository/network I/O;
5. known-ID hydration derives one WP-11 route without index/directory scan and
   revalidates loaded identity;
6. derived index/cache absence cannot prove semantic absence and rebuild succeeds;
7. source movement invalidates only affected local state and stale live state is
   not used as current;
8. publication generation G cannot clear local G+1;
9. no generic pending-work/publication-journal/recovery-cut authority exists;
10. live prospective state is not exposed/adopted as shared canon before required
    confirmed CAS;
11. cold recovery does not trust an orphan/stale local database over current
    native authorities;
12. storage baseline cannot override existing campaign runtime selection;
13. current legacy global timer/frontier and checkpoint debt are not encoded into
    the WP-12 local model as accepted law.

The current maintenance audit does not yet prove these obligations; WP-22 and the
later implementation plan must assign executable checks.

## 15. Deferred/downstream work

- WP-13: exact durability-edge/publication bookkeeping realization and repair of
  stale global timer/frontier runtime/test surfaces.
- WP-14: checkpoint/recovery schema and current-authority-first machine repair.
- WP-16: final live claim/currentness/CAS machine representation and current
  `LIVE_STATE` debt reconciliation.
- WP-19/WP-20: local database initialization/lifecycle integration only as needed
  by bootstrap/migration; durable campaign format remains native files.
- WP-22: conformance/integration/failure-injection tests.
- WP-24: measured query/storage/performance assessment and any proven narrow
  normalization/index optimization.

No downstream item is activated as a new architecture decision by this candidate.
