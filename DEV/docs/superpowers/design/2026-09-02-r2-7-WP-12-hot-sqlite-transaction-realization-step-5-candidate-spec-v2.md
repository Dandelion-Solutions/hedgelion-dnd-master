# R2.7 WP-12 — HOT, SQLite and Transaction Realization — Step 5 Candidate Specification v2

Status: **REPAIRED CANDIDATE — STEP-6 F01–F08 INCORPORATED**

Supersedes for current candidate wording:

- `2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-step-5-candidate-spec.md`

The v1 candidate remains design provenance. This v2 preserves its selected
direction and repairs only the authority/currentness/access/interpretability
ambiguities found by the Step-6 whole-project critic.

## 1. Scope and selected realization

WP-12 selects the local HOT/SQLite realization contract for already accepted
native owners and transaction/currentness laws:

> **TYPED NATIVE-OWNER HOT STORE + NARROW REBUILDABLE DERIVED HELPERS**

SQLite is a local transactional substrate. It is not durable campaign canon, not
a semantic owner, not a role-eligibility source and not a recovery authority by
mere survival.

Exact DDL, payload encoding, database file/path lifecycle, library/API and
performance tuning remain implementation details provided the laws below are
mechanically enforced.

## 2. Logical isolation, authority and identity

### LAW WP12-1 — SQLite format creates no semantic authority

A value physically stored in SQLite retains the semantic owner, lifecycle,
identity, information-eligibility and mutation rules of its native contract.

No table name, trigger, rowid, surrogate key, insertion/query order, local
freshness timestamp or database-file age may redefine semantic truth, chronology,
currentness, write authority or gameplay eligibility.

### LAW WP12-2 — Every operation is scoped to one selected campaign/authority context

Every owner lookup, hydration, query, mutation, transaction, derived-helper access
and publication preparation is explicitly scoped to the selected campaign and its
current authority/routing context.

A physical implementation may use one local database per campaign or a safely
namespaced shared database. Physical co-hosting is admissible only when hard
namespace isolation prevents one campaign/session context from satisfying another
campaign's currentness, owner lookup, authorization or information query.

Cross-campaign SQL visibility is never an implicit discovery or currentness path.

### LAW WP12-3 — Current owner payload is typed and validated

A current owner representation identifies the admitted native family and complete
native identity and validates the payload against the applicable current
structural owner/machine contract before acceptance.

The envelope is not an arbitrary JSON property bag. Unknown family, invalid shape
or incompatible identity is a typed validation/integrity failure.

### LAW WP12-4 — Semantic owner key excludes source revision/basis

Within the selected campaign/authority context, current-owner uniqueness is based
on:

```text
native family
+ complete native semantic identity
```

Source kind/ref/path/revision/tree/blob and writable partition are currentness/
routing metadata for that same owner identity. They do **not** participate in a
second semantic-owner key and cannot create parallel writable campaign/live rows
for one native owner.

Historical/source-specific payloads may exist only in explicitly non-current
cache/evidence storage and can never satisfy a current-owner read/mutation.

### LAW WP12-5 — Native identity is never SQL-generated

Simple, derived, composite and singleton identity stays exactly as defined by
`identifier-policies.json` and the native owner contract. SQL row identity/order
is implementation-only and cannot escape into gameplay, routing or chronology.

## 3. Access and information eligibility

### LAW WP12-6 — Local possession is not permission

Physical presence of a native owner payload in HOT does not grant:

- role-context eligibility;
- player/creator write authority;
- recipient disclosure eligibility;
- campaign membership;
- policy-adoption authority;
- secret/private information access.

All semantic reads supplied to an HDM logical role continue through R2.3/Step-4
information/role-context eligibility. All writes continue through current
`ACCESS_CONTROL.md`, campaign/live routing and acting-principal checks.

Derived SQL/query APIs cannot launder physically available private state into an
ineligible role or bypass a native write-authority check.

## 4. Local establishment and atomic execution

### LAW WP12-7 — Permitted local singleplayer owner state may establish in HOT first

Where the existing native owner/durability contract permits local establishment
before publication, an accepted local atomic edge may commit current owner state
into SQLite as established `VOLATILE_DIRTY`/SOFT even when durable Git state is
older.

Loss before required durability publication returns recovery to actual native
durable sources. Surviving bytes do not expand the durability promise.

### LAW WP12-8 — ExecutionSegment is the normal deterministic local commit boundary

One local SQLite transaction implements one accepted Step-3 ExecutionSegment or
another already-defined native local atomic edge.

As applicable it may atomically advance distinct native owners/evidence:

- world owner state;
- Procedure state;
- Command/Resolution execution state;
- fixed RNG/accepted execution continuity;
- Continuation create/consume state;
- MechanicalEvent/receipt/trace evidence;
- mandatory child/firing identity;
- idempotency state;
- local owner generation/dirty bookkeeping;
- helper updates/invalidations required not to observe a half-commit.

Physical co-commit does not merge semantic owners.

### LAW WP12-9 — Local transactions never span external boundaries

No SQLite transaction remains open across player choice/reaction, another
host/model exchange, repository/network reads/writes, campaign publication, live
CAS or external research.

Execution closes/commits/suspends through the existing Command/Resolution/
Continuation contracts before such a boundary.

## 5. Runtime execution-owner and interpretability closure

### LAW WP12-10 — Runtime lifecycle owners remain distinct

Interaction, IntentPlan, RuntimeCommand, Procedure, Resolution and Continuation
retain separate native owner rows/lifecycles. WP-12 admits no generic
`pending_work`, `job`, `workflow`, `obligation`, `transaction` or
`execution_snapshot` owner.

### LAW WP12-11 — ExecutionSegment remains embedded

ExecutionSegment remains an embedded committed edge of the owning
Command/Resolution contract. Physical SQL optimization cannot create an
independently authoritative `runtime.execution_segment` record/class.

Events/receipts/traces retain their existing evidence/owner roles and never
substitute for current native state.

### LAW WP12-12 — Open accepted work preserves interpretation context

Hydration/adoption of an open Command/Procedure/Resolution/Continuation preserves
or resolves the compatible accepted catalog/rules/invocation/dependency context
required by its native contract, including fixed accepted facts/RNG/provenance
where applicable.

Structural local representation may migrate, but open accepted work is never
silently rebound/reinterpreted under arbitrary newer ambient mechanics merely
because current local schemas/catalogs changed.

Missing compatible interpretation context is a typed recovery/compatibility
failure under Step 5.2, not permission to reinterpret.

## 6. Hydration, routing and source movement

### LAW WP12-13 — Known-ID hydration uses WP-11 deterministic routing

```text
native family + complete native identity
-> derive exact WP-11 route
-> pin/read exact selected native source
-> validate family + complete identity + owner structure
-> adopt clean local current owner state under that exact source basis
```

Known-ID hydration does not require family index/directory enumeration.

### LAW WP12-14 — Discovery/index helpers are non-authoritative

Family/native indexes and local query helpers can nominate a candidate only. The
candidate must resolve through current native routing/body validation before
material use.

Helper omission does not prove semantic absence unless a separate owner contract
explicitly owns complete authoritative enumeration. SQL order never chooses
mechanics/fiction without an owner-defined order key.

### LAW WP12-15 — Exact source basis accompanies local currentness

Local current owner/support state retains enough exact selected source basis for
currentness validation: source/ref/scope and revision/blob/tree identity as
applicable. Independent source revisions remain domain-scoped and do not become a
campaign-global frontier.

### LAW WP12-16 — Source movement distinguishes cache invalidation from established semantics

When a native source moves:

1. source-derived clean copies/currentness assumptions and affected helpers are
   invalidated/reloaded as required;
2. already-established local owner generation/accepted RNG/IDs are **not**
   discarded merely because transport HEAD moved;
3. if the external change footprint is proven disjoint from the local accepted
   owner/dependency footprint, preserve the local semantic result and rebuild only
   publication/source basis as Step 5.6 permits;
4. if relevant/overlapping dependencies changed, perform owner-specific
   revalidation/re-resolution; never blind merge or semantic replay solely for
   transport movement.

## 7. Derived support and Context Runtime

### LAW WP12-17 — Derived helpers are rebuildable

Reverse indexes, family/query caches, loaded-record caches, MechanicalContext/
condition/effect aggregation caches, dependency/query projections and similar
support are rebuildable from current native owners/evidence.

They cannot own current gameplay value, lifecycle, role eligibility, chronology,
publication authority or semantic absence.

### LAW WP12-18 — Context Runtime controls remain ephemeral/derived

ContextNeedProfile, RoleContextRequest, RoleContextBundle, ContextTrace and
operation source-basis values have no durable/native owner or generic HOT truth
record under WP-12.

Narrow derived query helpers may support bounded discovery, but R2.3 eligibility
and currentness must be revalidated before role-context use.

## 8. Dirty state and campaign publication handoff

### LAW WP12-19 — Dirty bookkeeping is owner-generation-specific and scope-relative

Local operational metadata may identify owner generation/fingerprint, dirty
membership, last compatible durable source basis, owning policy partition and the
still-relevant unpublished exposure basis needed by Step 5.5.

There is no campaign-global dirty generation, global `durable_frontier_time`,
universal HARD queue, global save clock or generic durability scheduler.

### LAW WP12-20 — Frozen publication attempt includes exact authority basis

Before campaign publication, deterministic persistence freezes the exact:

- target repository/ref and source/currentness basis;
- acting principal and authorization evidence/basis required by the native write
  contract;
- owner generations and dirty closure;
- dependencies/read footprint;
- resulting native path delta;
- publication reason/edge context required by Step 5.6/5.5.

This is an immutable **ephemeral** operation object, not a persistent publication
journal/owner.

Any authorization dependency that is mutable outside the frozen repository state
is revalidated at the owning access/publication protocol's required pre-mutation
boundary. Cached creator/PLAYER evidence is derived evidence only.

Repository object creation/ref update occurs outside SQLite transactions.

### LAW WP12-21 — Publication success clears only exact frozen generations

For frozen generation G, confirmed compatible publication marks G durable. Dirty
membership clears only if the current local generation is still G; newer G+1
remains dirty.

Remote source movement after/around publication triggers the targeted
currentness/reconciliation rules, not blanket dirty clearing.

## 9. Live/shared currentness and CAS

### LAW WP12-22 — Pre-CAS live result is ephemeral prospective state only

For live-claimed mutable owners, the deterministic prospective transition before
required live CAS is held in the existing Resolution/prospective operation model
and **must not replace/commit into the accepted current owner row**.

It may be computed from a pinned local current view and frozen as an in-memory
prospective transition. Until the owning live CAS succeeds, current local semantic
reads continue to see the pre-transition accepted live-backed owner state.

A failed/stale/closed CAS discards/rebases the prospective transition according to
Step 5.8 and never exposes it as shared established canon.

### LAW WP12-23 — Confirmed live CAS is followed by local adoption

After a compatible exact-source live CAS succeeds, one local SQLite adoption
transaction updates the affected current owner rows/source basis and dependent
helpers to the confirmed accepted live source state.

There is no SQLite+live distributed transaction. If local adoption fails after
remote CAS, recovery/currentness reloads the accepted live authority; it does not
roll back or replay the already accepted live transition.

### LAW WP12-24 — Live currentness follows selected claims/exact source

Live-backed current owner rows remain valid only while current routing/claim
selection and exact source basis are compatible. Campaign base is not fallback
current truth while live owns that mutable claim.

## 10. Cold recovery and checkpoint relation

### LAW WP12-25 — Surviving local database is cache only after source-equivalence proof

Cold recovery starts from Step-5.7/5.2 current native authorities and exact pins.
A surviving SQLite file never establishes newer recoverable canon by existence,
mtime, local generation or apparent freshness.

Local bytes may be reused only as a non-authoritative optimization after proving
they are equal to or deterministically derivable from the currently selected
compatible native source/evidence. Unpublished local owner generations are not
recovered as established state merely because their bytes survived.

### LAW WP12-26 — Recovery-attempt composition remains ephemeral

Selected source composition, roots, dependency closure and validation state for
one recovery attempt are in-memory operation state. No persistent RecoveryCut,
recovery-frontier or generic recovery-attempt owner is introduced.

### LAW WP12-27 — Checkpoint remains optional evidence

Checkpoint can be loaded/cached as immutable native evidence. It is not current
state/root membership/save proof/currentness frontier. Current noncanonical
checkpoint fields remain WP-14 machine debt and are not imported into HOT law.

## 11. Storage metadata/template boundary

### LAW WP12-28 — Storage metadata is separate configuration/provenance

`DND_STORAGE.yaml` can be loaded/cached for exact storage discovery, format
validation, storage-owner operations and new-campaign baseline runtime provenance.
It is not a campaign gameplay owner and its baseline cannot override an existing
campaign's `MANIFEST.engine.current`.

Storage-default metadata publication is a separate operation outside campaign
owner transactions.

### LAW WP12-29 — Storage template prose has no machine authority

`GAME/TEMPLATE/STORAGE_README.md` needs no SQLite/native record. It remains
supporting human-facing template prose and must follow actual storage/branch/
runtime owners.

## 12. Physical-shape constraints left to implementation

Implementation may choose exact tables/columns/payload encoding/pragmas/file
location/API and narrow normalized projections only if the laws above remain
enforced.

Baseline logical surfaces are:

1. **current native owner state**, unique by selected campaign/authority context
   + native family + complete native identity; source basis is metadata;
2. **operational source/currentness and owner-generation/dirty support** where
   useful for deterministic invariants;
3. **narrow derived query/routing helpers** for concrete bounded consumers;
4. **no persistent generic prospective/publication/recovery job/journal state**.

A dedicated family-specific normalized table/projection is admissible only for a
concrete measured/validated need and remains subordinate to its native owner/schema.

## 13. Cross-system impact

Depends on: Step-3 execution; Step-5.2/5.5/5.6/5.7/5.8/5.14; R2.3/WP-09;
WP-10; WP-11; Access Control; Actor/Asset/Effect/catalog/runtime contracts.

Constrains: WP-13, WP-14, WP-16, WP-19/WP-20, WP-22, WP-24 and later
implementation data-access/transaction interfaces.

Owns only: local HOT/SQLite physical working-state/transaction realization.

Does not own: gameplay semantics, durable topology, publication timing/ref
protocol, recovery source selection, live claim/absorption semantics,
bootstrap/migration or exact implementation DDL/API.

## 14. Verification obligations for later implementation

At minimum prove:

1. owner payload/family/native identity validation before current adoption;
2. hard campaign/context namespace isolation;
3. physical HOT possession cannot bypass role/access/information eligibility;
4. SQL row identity/order cannot leak as native identity/chronology/mechanics;
5. one ExecutionSegment commits all implicated local owner/runtime/evidence/dirty
   state atomically or none;
6. no SQLite transaction spans dialogue/repository/network I/O;
7. open execution resumes under compatible accepted interpretation context, not
   arbitrary ambient mechanics;
8. known-ID direct route requires no index/directory scan and validates body ID;
9. derived cache omission cannot prove semantic absence; cache rebuild works;
10. disjoint source movement preserves accepted local semantics while relevant
    overlap forces owner-specific revalidation;
11. frozen publication includes current authorization basis and generation G
    cannot clear G+1;
12. no generic pending-work/publication-journal/recovery-cut authority exists;
13. pre-CAS live prospective state is not current/shared owner state;
14. post-CAS local-adoption failure recovers from accepted live authority without
    replaying mechanics;
15. cold recovery ignores unpublished surviving local generations unless already
    proven durable in selected native sources;
16. storage baseline cannot override existing campaign runtime;
17. legacy global timer/frontier and checkpoint debt do not enter WP-12 law.

## 15. Forward consistency/debt routing

- WP-13: durability/SAVE/publication realization and legacy timer/frontier repair.
- WP-14: checkpoint/recovery machine repair.
- WP-16: live machine realization/current `LIVE_STATE` debt.
- WP-19/WP-20: bootstrap/migration integration if required.
- WP-22: executable WP-12 conformance/failure-injection coverage.
- WP-24: measured performance and any proven narrow normalization/index need.
- WP-26: reconcile stale `DEV/ARCHITECTURE/BRANCH_MODEL.md` storage-v2 marker
  wording with the current storage owner/machine contract without changing the
  settled baseline-versus-existing-campaign authority rule.

No forward item reopens the selected WP-12 architecture.
