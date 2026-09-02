# R2.7 WP-12 — HOT, SQLite and Transaction Realization — Step 2 Evidence

Status: **STEP 2 COMPLETE — EVIDENCE EXTRACTED / READY FOR DECISION BRIEF**

## 1. Scope and method

This evidence record executes the approved WP-12 Step-1 Task Brief against the
current Source Manifest. It is an architecture/machine-realization analysis only.
It does not change runtime, schemas, catalogs, tests, storage topology or accepted
upstream architecture.

The evidence set was expanded only where required rows exposed direct owners or
consumers. Current semantic owners remain authoritative; current GAME/DEV machine
surfaces are realization evidence and may contain downstream debt.

The central question is not whether SQLite can store a value. The question is
which native owner the value belongs to, whether a local physical copy may hold
current established state, what exact native source/currentness basis hydrates
it, which local mutations are atomic, and how loss/publication/recovery preserve
that ownership.

## 2. Extracted controlling evidence

### 2.1 Owner state may be current in HOT without changing semantic ownership

- `DEV/ARCHITECTURE/ACTOR_MODEL.md` explicitly permits accepted SOFT Actor state
  to be newer in HOT/SQLite than the durable Git frontier while preserving Actor
  as semantic owner.
- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`
  permits SQLite to physically host current established owner state as well as
  hydrated copies, execution/transaction state and derived query/index caches.
  SQLite format itself grants no authority.
- `DEV/ARCHITECTURE/ASSET_MODEL.md` and
  `DEV/SCHEMAS/world-effect-state.schema.json` preserve Asset and Effect as
  independent native owners. Derived accessibility, reverse lookup and similar
  helpers do not become writable state merely because SQL can index them.

Disposition: current local owner state in SQLite is valid when it is the physical
working representation of the native owner. It is not a second semantic copy.

### 2.2 Runtime execution owners remain separate

`CATALOG_CONTRACTS.md`, `core-catalog.json` and the runtime state schemas preserve
separate lifecycles for Interaction, IntentPlan, Command, Procedure, Resolution
and Continuation. Step-3 execution architecture further fixes:

- RuntimeCommand as root execution-chain closure owner;
- Procedure as sole owner of procedure-local ResourceState;
- Resolution as one Activity invocation;
- Continuation as one suspended Resolution generation;
- ExecutionSegment as an embedded atomic execution edge, not a standalone
  runtime record;
- MechanicalEvent/receipt/trace as committed evidence, not current world state.

Disposition: WP-12 must not collapse these owners into a generic SQL
`pending_work`, `jobs`, transaction-log or snapshot abstraction.

### 2.3 Local atomicity is an ExecutionSegment property

The Step-3 canonical execution boundary allows one local segment commit to
atomically advance, as applicable, native world state, Procedure state,
Command/Resolution execution state, fixed RNG, Continuation state,
MechanicalEvents/receipts, idempotency state, mandatory-child identity and dirty
bookkeeping. It explicitly forbids a SQLite transaction from spanning an
external choice, reaction or host dialogue.

Disposition: the local database transaction boundary must implement one accepted
ExecutionSegment/local owner-commit edge. It is not a conversation transaction,
a Git transaction or a cross-source distributed transaction.

### 2.4 Publication is outside the local database transaction

Step 5.6 requires a publication attempt to freeze exact owner generations,
source/ref basis, dependencies and final path delta before remote mutation. The
remote authority change occurs only at the native ref-selection/CAS boundary.
Dirty clearing is generation-specific: publishing generation G cannot clear a
newer local G+1.

Disposition: WP-12 needs local generation and dirty/publication bookkeeping, but
must not persist a generic publication journal as another authority. The frozen
publication attempt is an ephemeral deterministic operation object over a stable
local snapshot. Network/repository I/O occurs outside the SQLite transaction.

### 2.5 Durability bookkeeping is partition-relative, not a global clock

Step 5.5 defines SOFT/HARD as owner/policy-relative durability state and
obligations. Required durable closure differs from the pending write set. The
current `durable_frontier_time` / one-hour global-frontier wording in shipped
runtime/tests is explicitly noncanonical debt because exposure begins from
actual unpublished state in the applicable policy partition.

Disposition: WP-12 may require enough local metadata to identify owner
generations, dirty membership and policy partition/exposure basis. It must not
select one campaign-global durability frontier, timer or queue; WP-13 owns final
durability-edge/publication realization.

### 2.6 Hydration follows WP-11 route law and exact native currentness

WP-11 fixes known-ID hydration as direct route derivation followed by family and
full-identity validation. Indexes are discovery helpers only. Step 5.2/5.7
require each mutable native source used by a hydration/recovery attempt to be
exact-revision pinned, and derived state to rebuild.

Disposition: local owner rows/caches retain the exact native source/currentness
basis needed to detect staleness. An index hit, SQL row order or cached value
cannot establish identity, semantic absence or currentness.

### 2.7 Live/shared establishment is source-CAS-bound

Step 5.8 keeps native semantic owners intact even when physically packed into a
live epoch. Current selected claims determine write authority; exact live source
revision is the mutation fence. Shared consequences that require write-before-
reveal are established only through the accepted live CAS edge.

Disposition: a local SQLite prospective mutation for live-claimed state is not
shared established canon before the required live CAS. The local runtime may
prepare/freeze the deterministic prospective result, perform the exact-source CAS
outside SQLite, then adopt the confirmed live source/current owner state locally.
There is no SQLite+Git distributed transaction.

### 2.8 Recovery-attempt composition and checkpoints do not become HOT owners

Step 5.7 makes recovery-attempt source composition ephemeral operational state.
Checkpoint is optional immutable evidence/hint, never current-state authority;
current checkpoint fields such as generic `valid_through_event_id` and
`expected_commit_sha` are already marked noncanonical for later WP-14 repair.

Disposition: WP-12 introduces no persistent `recovery_cut`, recovery-attempt table
or checkpoint-derived current frontier. A loaded checkpoint may be cached as
native evidence without becoming an owner.

### 2.9 Storage discovery/provenance is separate from campaign HOT ownership

`GAME/SCHEMA/dnd_storage.schema.yaml` directly defines exact-root storage
discovery and storage-format/runtime-baseline provenance. Its baseline applies to
new campaigns only and cannot select or mutate an existing campaign runtime.
`GAME/TEMPLATE/STORAGE_README.md` is a human-facing supporting template describing
storage main plus separate campaign branches; it has no semantic authority.

Disposition: storage metadata may be loaded/cached as configuration/provenance
for storage operations. It is not a campaign owner row, HOT gameplay truth or
runtime selector for existing campaigns. The README requires no machine/HOT
representation.

### 2.10 Current verification has no dedicated WP-12 machine gate yet

`DEV/TOOLS/run_maintenance_audit.py` delegates to `audit_engine.py`. Current audit
coverage checks repository/process/runtime invariants, but no existing gate proves
the future WP-12 local owner-envelope, generation, live-adoption or derived-cache
separation contract.

Disposition: the canonical WP-12 result must carry explicit later verification
obligations rather than treating the current maintenance audit as proof of HOT
realization.

## 3. Item-level realization matrix

| Structure / concern | Native owner / disposition | Permitted local SQLite role | Hydration / currentness basis | Local atomic / dirty role | Loss / durable target |
|---|---|---|---|---|---|
| `world.actor` | Actor owner | Current owner working representation or clean hydrated copy | WP-11 exact Actor route + full identity validation + selected native revision | Mutated inside applicable ExecutionSegment; local generation becomes dirty/SOFT when establishment is local | Unpublished SOFT may be lost; durable target is native Actor record through owning publication scope |
| `world.asset` | Asset owner | Same owner-working representation model | WP-11 Asset route + owner validation | Atomic with related owner/runtime changes when one segment requires it | Native Asset record; derived possession/access indexes rebuild |
| `world.effect` | Effect owner | Same owner-working representation model | WP-11 Effect route + lifecycle/identity validation | Effect lifecycle/temporal state joins owning segment when changed | Native Effect record; aggregation/reverse indexes rebuild |
| Other admitted `world.*` owners | Their existing native owners | Typed owner row only when loaded/currently required | Family-specific WP-11 route/current source | No family acquires SQL authority by co-location | Native family record; unloaded data remains remote/durable owner representation |
| `runtime.interaction` | Interaction | Native runtime owner row only when retained by its lifecycle/recovery contract | Direct runtime family route / accepted source | May join local commit when accepted linkage changes | Native Interaction record when durability promise requires it |
| `runtime.intent_plan` | IntentPlan | Native runtime owner row | Derived canonical ID + WP-11 route | Clause-state changes remain IntentPlan-owned | Native IntentPlan record when required; no generic plan snapshot |
| `runtime.command` | RuntimeCommand | Native root-closure owner row | Command identity / routed current owner | Atomic command disposition, child linkage and idempotency state in segment commit | Native Command record while required for retry/recovery |
| `runtime.procedure` | Procedure | Native procedure owner row | Procedure ID / routed current owner | Procedure ResourceState changes join applicable segment | Native Procedure record; no copy in Resolution/Continuation |
| `runtime.resolution` | Resolution | Native execution owner row | Resolution ID / accepted catalog/rules/source basis | Central segment owner for action-backed execution; fixed RNG/cursor/children retained | Native Resolution record while recovery/idempotency requires it |
| `runtime.continuation` | Continuation | Native suspended-generation owner row | Resolution-derived ID + exact accepted causal inputs | Create/consume/update atomically at suspension/resume segment boundary | Native Continuation record when suspension is promised durable |
| ExecutionSegment | Embedded value, no independent owner | Embedded in owning Command/Resolution state; optional transient prepared form | Owning execution record | **Local atomic transaction boundary** | Durable through owning execution/evidence representation; no standalone table requirement |
| Mechanical/Semantic Event, retained Message, Disclosure, trace/evidence owners | Their existing native runtime owners | Typed native/evidence rows when required; not world-state authority | Their own identity/route/current or immutable source | Join a segment only where the accepted owner contract requires atomic materialization | Native log/runtime target; retention/GC stays with owning downstream contracts |
| Campaign ID allocator | `runtime.id_allocator` singleton | Native operational singleton row when loaded | Fixed singleton route | Allocation mutation may join local owner commit where campaign-local allocation applies | `STATE/ID_ALLOCATOR.yaml`; live-born identities do not depend on it |
| MANIFEST / CURRENT / fixed routing records | Existing campaign owners/routing projections | Clean/current loaded working copies as needed | Exact selected campaign source revision | Dirty only when their owning semantics actually change | Existing fixed native files; CURRENT remains compact routing, not pending work |
| Source/frontier metadata | DERIVED operational support | Narrow source/ref/revision/tree/blob cache | Exact native source probe/read results | Used for validation/invalidation; never semantic mutation | Rebuild/re-read; not campaign canon |
| Family discovery/index data | DERIVED routing support | Query/index cache allowed | Native family index + exact body validation | Updated/invalidated as helper only; absence cannot settle semantic absence | Rebuild from native family; durable index publication remains WP-13 closure work |
| MechanicalContext / condition/effect aggregation / query caches | DERIVED | Rebuildable cache only | Current owner inputs | No dirty/canon role | Recompute after invalidation/restart |
| ContextNeedProfile / RoleContextBundle / ContextTrace / source basis | EPHEMERAL / derived R2.3 execution controls | No durable owner representation; transient process values only | Current Context Runtime assembly | No owner dirty/publication role | Rebuild each applicable assembly; no campaign target |
| Dirty/generation bookkeeping | OPERATIONAL metadata attached to native owner/policy scope | Local generation, dirty membership and required source/publication basis | Derived from accepted local owner transitions + last known compatible durable source | Generation G is frozen for publication; success may clear G only, never G+1 | Reconstructed from surviving HOT plus durable source; exact publication policy belongs WP-13 |
| Frozen campaign publication attempt | EPHEMERAL deterministic operation state | In-memory immutable snapshot/object; **no generic persistent journal** | Exact frozen owner generations + source/ref/dependency basis | Repository I/O occurs after local freeze, outside DB transaction | Remote authority result adopted/revalidated; retry rebuilt from current authority |
| Recovery-attempt source composition | EPHEMERAL operational state | In-memory only | Step-5.7 current-authority-first exact pins | No gameplay dirty state | Recreated on recovery; no `RecoveryCut` owner |
| Checkpoint | `runtime.checkpoint` evidence only | Loaded/cached evidence record if needed | Exact checkpoint descriptor + current-owner validation | Never local current-state frontier or save proof | Native checkpoint descriptor; WP-14 owns wire repair |
| Live-claimed native owner state | Same native owner; live route selects current writable source | Current exact live-backed working copy after adoption; prospective result may be staged transiently | Current selected live route/claim + exact live source revision | Shared establishment follows live CAS; after confirmed CAS adopt exact accepted state locally | Current truth remains live until transfer; local cache loss rehydrates exact selected live source |
| `DND_STORAGE.yaml` | Storage metadata/provenance contract, not campaign gameplay owner | Optional configuration/provenance cache | Storage default branch exact root marker + semantic validation | Separate storage-metadata operation; no campaign transaction role | Storage default-branch metadata |
| `STORAGE_README.md` | Supporting template only | **NO SQLITE REPRESENTATION REQUIRED** | N/A for runtime mechanics | None | Template/documentation only |

## 4. Negative findings / rejected realization shortcuts

The evidence rejects the following as WP-12 realization directions:

1. committing the SQLite database as campaign canon;
2. using one global HOT snapshot as recovery/current-state authority;
3. adding a generic `pending_work` / scheduler / job / publication-journal table;
4. making ExecutionSegment an independent runtime record solely for SQL
   convenience;
5. allowing SQL row order, surrogate row IDs or index presence to decide native
   identity, chronology, eligibility or semantic absence;
6. clearing all dirty state after a publication that covered only an older owner
   generation;
7. treating a local prospective live mutation as shared established state before
   the required exact-source CAS;
8. keeping one SQLite transaction open across GitHub/network I/O or external
   player dialogue;
9. deriving current campaign runtime from storage baseline metadata;
10. reviving checkpoint fields or the legacy global one-hour durability frontier
    as WP-12 law.

## 5. Synthesis completeness gate

- [x] Every Step-1 `REQUIRED STEP-2 INSPECTION` source was inspected.
- [x] Directly exposed Actor/Asset/Effect and runtime owner schemas were inspected.
- [x] WP-09/WP-10/WP-11 upstream allocations were reconciled.
- [x] Step-3 and Step-5.2/5.5/5.6/5.7/5.8 authority/atomicity/recovery laws were reconciled.
- [x] Current storage discovery/template surfaces were classified without semantic promotion.
- [x] Current GAME debt was separated from accepted architecture.
- [x] Current maintenance-audit coverage was checked and not overstated.
- [x] No conclusion depends only on roadmap/index/summary/search output.

## 6. Step-2 conclusion

The evidence supports a bounded local transactional substrate in which native
owner identity and lifecycle remain explicit, while SQLite supplies physical
working-state storage and derived query support. It does not support a generic
memory database or a second persistence authority.

No human-owned product/semantic/authority decision is exposed by Step 2. Step 3
may compare concrete realization shapes under these already-settled constraints.
