# R2.7 WP-12 — HOT, SQLite and Transaction Realization — Canonical Specification

Status: **CANONICAL WP-12 RESULT — STEPS 1-8 COMPLETE / MANDATORY SENIOR AUDIT PENDING**

## 1. Scope and accepted direction

WP-12 defines the local HOT/SQLite machine-realization contract for already
accepted native semantic owners, deterministic execution, currentness,
durability/publication handoff, recovery and live-CAS composition.

Accepted direction:

> **TYPED NATIVE-OWNER HOT STORE + NARROW REBUILDABLE DERIVED HELPERS**

SQLite is the baseline local transactional substrate. It is not durable campaign
canon, not a semantic owner, not a role/access authority, not a chronology source
and not cold-recovery authority by mere physical survival.

This specification does not select exact SQL DDL, serialization format, SQLite
pragmas, local database path/lifecycle, programming API, performance target,
publication cadence, recovery wire format, bootstrap/migration procedure or
runtime implementation. Those remain downstream implementation/WP concerns
unless later evidence requires architecture reopening.

## 2. Logical isolation, owner authority and identity

### LAW WP12-1 — SQLite format creates no semantic authority

A value physically stored in SQLite retains the semantic owner, lifecycle,
identity, eligibility/currentness and mutation rules defined by its native
contract.

Table names, triggers, SQL row identity, surrogate keys, insertion/query order,
local timestamps and database-file freshness may not redefine semantic truth,
fictional chronology, native identity, currentness, write authority or gameplay
eligibility.

### LAW WP12-2 — Every operation is scoped to the selected campaign/authority context

Every owner lookup, hydration, query, mutation, transaction, helper access and
publication preparation is explicitly scoped to one selected campaign and its
current authority/routing context.

One database per campaign is an implementation option, not architecture law. A
shared physical database is admissible only with hard namespace isolation that
prevents cross-campaign owner lookup, currentness, authorization, information or
mutation inference.

### LAW WP12-3 — Current owner payload is typed and validated

A current local owner representation identifies an admitted native family and the
complete native semantic identity and validates the payload against the applicable
current structural owner/machine contract before adoption as accepted current
local state.

The owner envelope is not an arbitrary JSON property bag. Unknown family,
invalid shape, incompatible identity or incompatible interpretation context is a
typed validation/compatibility failure.

### LAW WP12-4 — Semantic owner uniqueness excludes source revision/basis

Within one selected campaign/authority context, current-owner uniqueness is:

```text
native family
+ complete native semantic identity
```

Source kind/ref/path/revision/tree/blob and current writable partition are
currentness/routing metadata for that same owner identity. They do not create a
second semantic key and cannot authorize parallel campaign/live writable copies
of one native owner.

Source-specific historical payloads may be retained only as explicitly
non-current evidence/cache and cannot satisfy a current-owner read or mutation.

### LAW WP12-5 — Native identity is never SQL-generated

Simple, derived, composite and singleton identities remain exactly those defined
by the current identifier policy and native owner contract. SQL rowid,
AUTOINCREMENT and physical row order are implementation-only and cannot escape as
native/gameplay identity, routing authority or chronology.

## 3. Access and information eligibility

### LAW WP12-6 — Local possession is not permission

Physical presence of owner payloads in HOT grants no role-context eligibility,
player/creator write authority, disclosure eligibility, membership, policy
adoption authority or secret/private-state access.

Semantic reads supplied to an HDM logical role continue through the current
Step-4/R2.3 role-context and information-eligibility contracts. Mutations and
publication continue through `ACCESS_CONTROL.md`, current campaign/live routing
and acting-principal checks.

Derived SQLite/query APIs cannot launder physically available private state into
an ineligible role or bypass native write authorization.

## 4. Local establishment and deterministic transactions

### LAW WP12-7 — Permitted local owner state may establish in HOT before durability

Where the existing native owner/durability contract permits local establishment
before publication, an accepted local atomic edge may commit current owner state
into SQLite as established `VOLATILE_DIRTY`/SOFT even when the durable Git-native
representation is older.

Loss before an applicable durability edge returns recovery to actual surviving
native durable sources. Surviving local bytes do not expand the durability
promise.

### LAW WP12-8 — ExecutionSegment is the normal local atomic commit boundary

One local SQLite transaction implements one accepted Step-3 ExecutionSegment or
another already-defined native local atomic edge.

As applicable, that transaction may atomically advance distinct native
owners/evidence including:

- world owner state;
- Procedure state;
- Command/Resolution execution state;
- fixed RNG and accepted execution continuity;
- Continuation create/consume state;
- MechanicalEvent/receipt/trace evidence required by the edge;
- mandatory child/firing identity;
- idempotency state;
- local owner generation/dirty bookkeeping;
- helper updates/invalidations that must not observe a half-commit.

Physical co-commit does not merge semantic owners.

### LAW WP12-9 — Local transactions never span external boundaries

No SQLite transaction remains open across player choice/reaction, another
host/model exchange, repository/network I/O, campaign publication, live CAS or
external research.

Execution first closes/commits/suspends through the existing
Command/Resolution/Continuation contracts.

## 5. Runtime execution-owner and interpretability closure

### LAW WP12-10 — Runtime lifecycle owners remain distinct

Interaction, IntentPlan, RuntimeCommand, Procedure, Resolution and Continuation
retain their separate native owner identities/lifecycles.

WP-12 introduces no generic semantic `pending_work`, `job`, `workflow`,
`obligation`, `transaction`, `execution_snapshot` or equivalent owner.

### LAW WP12-11 — ExecutionSegment remains embedded

ExecutionSegment remains an embedded committed edge under the owning
Command/Resolution contract. Physical SQL optimization cannot create an
independently authoritative `runtime.execution_segment` semantic record/class.

Events, receipts and traces retain their existing evidence/owner roles and never
substitute for current native state.

### LAW WP12-12 — Open accepted work preserves its compatible interpretation context

Hydration/adoption of open Command/Procedure/Resolution/Continuation state
preserves or resolves the compatible accepted catalog/rules/invocation/dependency
context required by the native owner contract, including fixed accepted facts,
RNG and provenance where applicable.

Local structural migration may evolve representation but cannot silently rebind
accepted open work to arbitrary newer ambient mechanics. Missing compatible
interpretation context is a typed Step-5.2 recovery/compatibility failure.

## 6. Hydration, routing and source movement

### LAW WP12-13 — Known-ID hydration follows WP-11 direct routing

For a known native identity:

```text
native family + complete native identity
-> derive exact WP-11 route
-> pin/read exact selected native source
-> validate family + complete identity + owner structure
-> adopt clean local current owner state under that exact source basis
```

Known-ID hydration does not require family-index or directory enumeration.

### LAW WP12-14 — Discovery/index helpers are non-authoritative

Family/native indexes and local derived query helpers may nominate a candidate.
Material use then resolves/validates the applicable current native owner.

Helper omission does not prove semantic absence unless a separate owner contract
explicitly owns complete authoritative enumeration for that scope. SQL ordering
cannot choose mechanics/fiction without an owner-defined ordering law.

### LAW WP12-15 — Exact source basis accompanies local currentness

Local current owner/support state retains enough selected source basis to validate
currentness: source/ref/scope and exact revision/blob/tree identity as applicable.

Independent source revisions remain domain-scoped and do not become one campaign-
global frontier.

### LAW WP12-16 — Source movement distinguishes cache invalidation from established semantics

When a native source moves:

1. source-derived clean copies/currentness assumptions and affected helpers are
   invalidated/reloaded as required;
2. already-established local owner generation, accepted identity and fixed RNG
   are not discarded merely because transport HEAD/source revision moved;
3. proven-disjoint external movement preserves the accepted local semantic result
   and rebuilds only source/publication basis as allowed by Step 5.6;
4. relevant/overlapping dependency movement triggers owner-specific
   revalidation/re-resolution rather than blind merge or mechanics replay.

## 7. Derived support and Context Runtime

### LAW WP12-17 — Derived helpers are explicitly rebuildable

Reverse indexes, family/query caches, loaded-record caches, MechanicalContext,
condition/effect aggregation caches, dependency/query projections and similar
support are rebuildable from current native owners/evidence.

They cannot own current gameplay value, lifecycle, eligibility, chronology,
publication authority or semantic absence.

### LAW WP12-18 — Context Runtime control values remain ephemeral/derived

ContextNeedProfile, RoleContextRequest, RoleContextBundle, ContextTrace and
operation source-basis values receive no durable/native owner or generic HOT
truth record under WP-12.

Narrow derived query helpers may support bounded discovery, but R2.3 eligibility
and currentness are revalidated before role-context use.

## 8. Dirty state and campaign-publication handoff

### LAW WP12-19 — Dirty bookkeeping is owner-generation-specific and scope-relative

Local operational metadata may identify the current owner generation/fingerprint,
dirty membership, last compatible durable source basis, owning durability policy
partition and still-relevant unpublished exposure basis required by Step 5.5.

WP-12 introduces no campaign-global dirty generation, global
`durable_frontier_time`, universal HARD queue, global save clock or generic
scheduler.

### LAW WP12-20 — Frozen publication attempt includes the exact authority basis

Before campaign publication, deterministic persistence freezes the exact:

- target repository/ref and selected source/currentness basis;
- acting principal and authorization evidence/basis required by the native write
  contract;
- owner generations and dirty closure;
- dependencies/read footprint;
- resulting native path delta;
- publication reason/edge context required by Steps 5.5/5.6.

This frozen attempt is an immutable **ephemeral** operation object, not a
persistent publication journal or transaction-log owner.

Any authorization dependency mutable outside the frozen repository state is
revalidated at the owning access/publication protocol's required pre-mutation
boundary. Cached creator/PLAYER evidence remains derived evidence.

Repository object creation/ref transition occurs outside SQLite transactions.

### LAW WP12-21 — Publication success clears only exact frozen generations

Confirmed compatible publication of owner generation G marks G durable. Dirty
membership clears only when current local owner generation is still G. A newer
G+1 remains dirty.

Remote movement around publication uses targeted currentness/reconciliation and
never blanket dirty clearing.

## 9. Live/shared currentness and CAS

### LAW WP12-22 — Pre-CAS live result remains ephemeral prospective state

For a live-claimed mutable owner, the deterministic prospective transition before
the required live CAS remains in the existing Resolution/prospective operation
model and **must not replace the accepted current owner row**.

Until live CAS succeeds, current semantic reads continue to observe the
pre-transition accepted live-backed owner state. A failed/stale/closed CAS
discards/rebases the prospective transition under Step 5.8 and never exposes it
as shared established canon.

### LAW WP12-23 — Confirmed live CAS is followed by local adoption

After compatible exact-source live CAS succeeds, one local SQLite adoption
transaction updates the affected current owner rows/source basis and dependent
helpers to the confirmed accepted live state.

There is no SQLite+live distributed transaction. If local adoption fails after
successful remote CAS, recovery/currentness reloads the accepted live authority;
it does not roll back or replay already accepted mechanics.

### LAW WP12-24 — Live currentness follows selected claims and exact source revision

Local live-backed current owner rows/helpers remain valid only while current
routing/claim selection and exact source basis are compatible. Campaign base is
not fallback current truth while live owns that mutable claim.

## 10. Cold recovery and checkpoint relation

### LAW WP12-25 — Surviving local database is cache only after source-equivalence proof

Cold recovery begins from Step-5.2/5.7 current native authorities and exact pins.
A surviving SQLite file never establishes newer recoverable canon by existence,
mtime, local generation or apparent freshness.

Local bytes may be reused only as a non-authoritative optimization after proving
they are equal to or deterministically derivable from the currently selected
compatible native source/evidence. Unpublished local owner generations do not
become recovered established state merely because their bytes survived.

### LAW WP12-26 — Recovery-attempt composition remains ephemeral

Selected source composition, operational roots, dependency closure and validation
state for one recovery attempt are in-memory operation state. WP-12 introduces no
persistent RecoveryCut, recovery-frontier or generic recovery-attempt owner.

### LAW WP12-27 — Checkpoint remains optional evidence

Checkpoint may be loaded/cached as immutable native evidence. It is not current
state authority, root-membership authority, save proof or local currentness
frontier. Current noncanonical checkpoint fields remain WP-14 machine-realization
debt and are not imported into WP-12 HOT law.

## 11. Storage metadata/template boundary

### LAW WP12-28 — Storage metadata is configuration/provenance, not campaign HOT authority

`DND_STORAGE.yaml` may be loaded/cached for exact storage discovery, format
validation, storage-owner operations and new-campaign baseline runtime provenance.
Its baseline cannot override an existing campaign's `MANIFEST.engine.current`.

Storage-default metadata publication is a separate storage-owner operation and
never joins a campaign owner-state transaction.

### LAW WP12-29 — Storage template prose has no machine authority

`GAME/TEMPLATE/STORAGE_README.md` requires no SQLite/native record. It remains a
supporting human-facing template and must stay consistent with actual storage,
branch and runtime owners without becoming a semantic source.

## 12. Implementation-facing physical constraints

Implementation may choose exact tables, columns, payload encoding, pragmas,
local database lifecycle and typed data-access APIs only if the laws above remain
mechanically enforceable.

The baseline logical surfaces are:

1. **current native owner state**, unique by selected campaign/authority context
   + native family + complete native identity, with source basis as metadata;
2. **operational currentness and owner-generation/dirty support** sufficient for
   deterministic validation/publication invariants;
3. **narrow rebuildable routing/query helpers** for concrete bounded consumers;
4. **ephemeral prospective/publication/recovery operation values**, with no
   persistent generic job/journal authority.

A dedicated normalized table/projection for one family is admissible only for a
concrete measured/validated need and remains subordinate to the native owner/schema.
WP-12 establishes no current requirement for wholesale per-family SQL schema
duplication.

## 13. Cross-system ownership and downstream constraints

WP-12 depends on:

- Step-3 deterministic execution/ExecutionSegment owners;
- Steps 5.2/5.5/5.6/5.7/5.8 and Step-5.14 integration laws;
- Step-4/R2.3 information/role-context eligibility;
- WP-09 bounded Context Runtime realization;
- WP-10 logical durable record families;
- WP-11 physical routing/identity/index rules;
- Access Control and current Actor/Asset/Effect/catalog/runtime contracts.

WP-12 constrains:

- WP-13 durability/SAVE/publication machine realization;
- WP-14 recovery/checkpoint machine realization;
- WP-16 multiplayer/live machine realization;
- WP-19/WP-20 bootstrap/migration integration;
- WP-22 deterministic conformance/failure-injection coverage;
- WP-24 measured HOT/query/storage performance work;
- later implementation-plan data-access/transaction boundaries.

WP-12 owns only the local HOT/SQLite physical working-state/transaction
realization boundary. It does not own gameplay semantics, durable native topology,
publication timing/ref protocol, recovery source selection, live claim/absorption
semantics, bootstrap/migration policy or exact implementation DDL/API.

## 14. Mandatory later verification obligations

The implementation/verification plan must prove at least:

1. current owner adoption requires family/native identity/shape validation;
2. hard campaign/context namespace isolation exists;
3. physical HOT possession cannot bypass role/access/information eligibility;
4. SQL row identity/order cannot leak as native identity, chronology or mechanics;
5. one ExecutionSegment commits all implicated local owner/runtime/evidence/dirty
   state atomically or none;
6. no SQLite transaction spans external dialogue or repository/network I/O;
7. open accepted execution resumes under compatible accepted interpretation
   context rather than arbitrary ambient mechanics;
8. known-ID hydration derives the WP-11 route without directory/index scan and
   validates loaded full identity;
9. derived-cache/index absence cannot prove semantic absence and rebuild succeeds;
10. proven-disjoint source movement preserves accepted local semantics while
    relevant overlap forces owner-specific revalidation;
11. frozen publication includes the required acting-principal/authorization basis
    and generation G publication cannot clear newer G+1;
12. no generic pending-work/publication-journal/recovery-cut authority exists;
13. pre-CAS live prospective state cannot become current/shared owner state;
14. post-CAS local-adoption failure recovers from accepted live authority without
    replaying mechanics/RNG;
15. cold recovery ignores unpublished surviving local generations unless they are
    already proven durable/equivalent to selected native sources;
16. storage baseline cannot override existing campaign runtime selection;
17. legacy global timer/frontier and checkpoint debt are not encoded as WP-12
    accepted law.

The current maintenance audit does not yet constitute proof of these obligations.
Executable coverage is assigned to WP-22 and the later approved implementation
plan.

## 15. Forward/debt routing

- **WP-13** — exact durability-edge/SAVE/publication realization and repair of
  stale global timer/frontier runtime/test surfaces.
- **WP-14** — checkpoint/recovery machine repair.
- **WP-16** — final live claim/currentness/CAS machine realization and current
  live-surface debt reconciliation.
- **WP-19/WP-20** — bootstrap/migration integration if local HOT lifecycle needs
  it; durable campaign format remains native files.
- **WP-22** — executable WP-12 conformance/integration/failure-injection tests.
- **WP-24** — measured performance/query/storage evaluation and any proven narrow
  normalization/index optimization.
- **WP-26** — reconcile stale `DEV/ARCHITECTURE/BRANCH_MODEL.md` storage-v2 marker
  wording with the current storage machine/owner contract without changing the
  settled baseline-versus-existing-campaign authority rule.

These forward items do not reopen WP-12 architecture merely by overlap.

## 16. Final decision

Recommendation confidence: **HIGH**

Human decision required: **NO**

WP-12 architecture is complete under the current accepted product/deployment
scope. Step-6 findings F01–F08 are incorporated in this final law; F09 is the
bounded WP-26 documentation-consistency item above.

No implementation is authorized by this specification alone. After Step-8
canonicalization, the mandatory Senior audit must pass before WP-13 or any
implementation-planning transition is authorized.
