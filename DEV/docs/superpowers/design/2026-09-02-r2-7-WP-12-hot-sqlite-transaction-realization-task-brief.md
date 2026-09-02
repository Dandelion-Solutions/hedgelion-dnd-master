# R2.7 WP-12 - HOT, SQLite and Transaction Realization - Architecture Task Brief

Status: **STEP-1 TASK BRIEF / WHOLE-PROJECT CRITIC REPAIRED - READY FOR MANDATORY SENIOR REVIEW**

## 1. Mandate

WP-12 maps the already accepted semantic owners and physical native-record routes
to a bounded HOT/SQLite working-state realization. It must answer, for every
material current owner or operational structure that needs local working-state
support:

```text
semantic owner
-> owner-state working copy or DERIVED ONLY structure
-> hydration/currentness basis
-> dirty/publication and transaction/CAS role
-> crash/loss/recovery behavior
-> durable native materialization target
-> rebuildability
```

The investigation must be able to conclude `NO SQLITE OWNER`, `DERIVED ONLY`,
or `EPHEMERAL ONLY`; the title does not presume that every concern needs a
SQLite table or that SQLite is the correct representation for every HOT value.

## 2. Authorization and boundaries

- `DEV/CURRENT_PROGRESS.md` authorizes only WP-12 Step 1: this Task Brief, its
  Source Manifest and the whole-project critic.
- Mandatory Senior GO is required before WP-12 Step 2. WP-13 and
  implementation planning remain blocked.
- The R2.7 whole-project Task Brief v2 and owner clarification require both
  architecture-to-machine and machine-to-architecture evidence. This WP is one
  domain slice, not a closure claim for R2.7.
- WP-11 is a closed upstream route-law input. Its F01 requires WP-12 to realize
  route-law hydration and derived-index separation; WP-12 does not alter the
  route algorithm, family allocation or index authority.
- WP-13 owns durability-edge/publication realization, WP-14 owns recovery and
  checkpoint realization, WP-16 owns live access/currentness realization, and
  WP-19/WP-20 own bootstrap/migration. WP-12 may identify interfaces and
  forward obligations but may not select their contracts.

## 3. Existing laws the investigation must preserve

- Native world/runtime/live owners retain semantic authority. SQLite is a
  format and may not become durable campaign canon or a duplicate writable
  owner.
- A Step-3 execution segment may atomically cover owner mutation, execution
  state, fixed RNG, continuations, events/receipts, idempotency and dirty
  bookkeeping, but it never spans an external choice, reaction or host dialogue.
- SOFT is established, deferrable volatile-dirty state; HARD is a named
  `MUST_BE_DURABLE_BEFORE(edge)` obligation. Required durable closure differs
  from the physical pending write set.
- Campaign publication freezes complete inputs before remote mutation, emits one
  base-tree-derived single-parent commit and uses non-force ref selection. Dirty
  clearing is frozen-generation-specific.
- Recovery follows current native authority, exact-pins mutable sources, hydrates
  bounded required closure and rebuilds derived state. Lost unpublished HOT/SOFT
  state is never invented.
- Live currentness uses selected immutable claims and exact-source CAS. It has no
  campaign-allocator hot-path dependency, global transaction, lease, heartbeat
  or global currentness frontier.
- WP-11 known-ID hydration derives a route directly, validates family and full
  identity after load, and never lets path/index order or index absence become
  authority.

## 4. Questions for Step 2

1. Which accepted native owners can be newer in local HOT state, and in which
   authority/write partitions?
2. Which local structures are owner-state working copies, execution-attempt
   state, publication bookkeeping, or derived caches/indexes/projections?
3. What exact native source/revision and WP-11 route hydrate each structure;
   when must a cached value be revalidated or discarded?
4. Which mutations share one local transaction, which use remote campaign CAS or
   live CAS, and where do external interaction boundaries prohibit spanning
   transactions?
5. How does a frozen publication attempt distinguish owner generations, dirty
   generations and already-durable closure dependencies without creating a
   persistent transaction journal or duplicate authority?
6. What survives a process crash, what is rebuilt, and what must materialize to
   which native campaign or live record before a named durability edge can pass?
7. Which current GAME/DEV surfaces are stale implementation debt rather than
   accepted architecture, and which downstream WP owns their repair?
8. What deterministic integration, recovery, conflict and failure-injection
   tests will a later approved implementation need?

## 5. Required Step-2 evidence and exit criteria

Step 2 must produce an item-level realization matrix covering at least world
owner working copies, runtime execution owners, routing/currentness support,
durability bookkeeping, publication attempts, recovery-attempt state, indexes,
caches and live working state. For every row, it must name the native owner,
currentness source, loss/rebuild disposition and downstream native target.

The research must demonstrate that a proposed table, cache, dirty marker or
transaction helper does not create any of the following:

- SQLite-only durable canon or a duplicate semantic owner;
- a generic memory database, graph, scheduler, pending-work table or global HOT
  snapshot;
- a generic persistent publication journal, generic YAML merge authority or
  distributed campaign/live transaction;
- a global durability timer/frontier, campaign-wide scan, or SQL/list ordering
  that decides mechanics or fiction;
- a SQLite transaction spanning external choice/reaction/dialogue; or
- a physical layout, index or cache that overrides WP-11 route/currentness law.

Step 2 is complete only when the matrix maps every included structure to one
accepted owner/disposition, records bounded hydration and invalidation behavior,
and identifies no unowned current state or unresolved authority transfer. It
must leave schema/catalog/runtime implementation for the architecture-approved
implementation phase.

## 6. Current-machine debt handling

The shipped one-hour `durable_frontier_time` model is current runtime/test
consumer evidence, not accepted WP-12 law. Step 5.5 explicitly classifies a
universal one-hour threshold and campaign-global frontier as noncanonical debt.
WP-12 Step 2 must preserve the actual scope-qualified exposure-policy laws and
may not silently reselect the old timer model. Editing those GAME contracts or
their tests is outside this documentation-only Step-1 package and requires the
later owner-conforming realization work.

Likewise, the current checkpoint schema contains fields Step 5.7 has marked
noncanonical. That is a WP-14/recovery realization input, not permission for
WP-12 to redesign checkpoint authority.

## 7. Source Manifest

The task-specific source set, authority roles, inspection depth and Step-2
discovery obligations are recorded in:

- `2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-source-manifest.md`

## 8. Step-1 decision and next gate

The framing exposes no human-owned product or semantic-owner decision. It does
expose current-machine debt that Step 2 must classify against settled owners;
the investigation may not convert that debt into new architecture by default.

Do not begin WP-12 Step 2, WP-13 or implementation planning without explicit
Senior GO.
