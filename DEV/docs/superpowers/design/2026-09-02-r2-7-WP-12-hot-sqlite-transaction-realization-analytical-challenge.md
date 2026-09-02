# R2.7 WP-12 — Analytical Challenge Before Decision Brief

Status: **COMPLETE — RECOMMENDATION CHALLENGED**

## Preferred direction under challenge

A typed native-owner HOT store physically backed by SQLite, with validated owner
payloads plus narrow rebuildable routing/query helpers. Native semantic owners
remain explicit; SQLite supplies local transactionality and operational metadata.

## Strongest opposing case

The strongest alternative is dedicated normalized SQL tables for each native
world/runtime family. It offers stronger column-level constraints, direct query
plans and easier SQL introspection than a typed owner-envelope whose payload may
remain structurally close to the owner schema.

That alternative would be preferable if HDM's primary requirement were broad
relational analytics over a stable small set of record shapes. The current
architecture instead has a large typed owner vocabulary, embedded protocol values,
pre-release schema evolution and a strong requirement that durable/native schemas
and owner contracts remain the semantic source. Duplicating every owner shape in
SQL would introduce another migration surface and make schema drift itself an
authority risk.

## Simplest viable comparison

A still simpler realization is pure in-memory native objects with SQLite used only
for optional indexes/caches. That can preserve semantic ownership, but it does not
supply one deterministic transactional substrate for the accepted Step-3 segment
edge across multiple native world/runtime owners. Re-implementing equivalent
atomicity in an ad-hoc in-memory transaction layer would duplicate the mechanism
SQLite already supplies and would weaken crash/debug/test observability without a
compensating accepted requirement.

The recommendation therefore uses SQLite for local owner-state transactions, but
does not make SQLite durable campaign canon.

## Assumption attack

### A1 — Owner payload validation remains deterministic

If a local owner envelope could accept arbitrary unvalidated JSON, the design
would become a generic memory database and could bypass owner schemas.

Required mitigation: every owner payload entering/adopting current local state is
validated against the applicable admitted family/owner machine contract before it
may become accepted current state.

### A2 — Local transactions are not held open across external I/O

If correctness required a single transaction covering SQLite plus Git/live CAS,
the design would fail because the accepted architecture explicitly rejects a
distributed transaction and external-dialogue-spanning segment.

Evidence shows this assumption is false: publication/live authority changes are
separate native boundaries. Local state is frozen, remote authority changes, and
the confirmed result is then adopted/revalidated locally.

### A3 — Broad SQL joins are not required for ordinary correctness

If ordinary mechanics required unrestricted relational joins across the whole
campaign, a generic owner-envelope could be too opaque. Existing R2.3/WP-11 laws
instead require bounded typed discovery/direct routing and explicitly reject
campaign-wide scans. Narrow derived indexes can support admitted queries without
promoting the SQL schema into owner authority.

### A4 — Owner identity can be preserved independently of SQL row identity

If downstream code relied on SQL rowid/AUTOINCREMENT as semantic identity or
chronology, native identity laws would be violated. The realization must therefore
store/use owner-defined simple/derived/composite/singleton identity explicitly;
SQL physical row identity is implementation-only.

## Failure scenarios

1. **G publishes while G+1 exists locally.** Publication success must mark only
   frozen generation G durable and leave G+1 dirty.
2. **Live CAS loses a race.** Prospective local state is discarded/revalidated;
   it is not shared canon and accepted RNG/identity is not blindly replayed.
3. **Index cache is missing.** Known-ID direct route still hydrates the owner;
   missing helper data cannot prove semantic absence.
4. **Process dies with unpublished singleplayer SOFT.** Cold recovery returns to
   actual durable native sources; orphan/stale local HOT state is not invented as
   durable truth.
5. **Checkpoint is newer-looking than current routing.** Current native authority
   wins; checkpoint cannot become a recovery frontier.
6. **Storage baseline differs from an existing campaign runtime.** Existing
   campaign `MANIFEST.engine.current` wins; storage baseline remains new-campaign
   provenance/default only.
7. **One segment touches Actor + Asset + Procedure + Resolution + Event.** One
   local SQLite transaction can commit the accepted native owner changes and
   execution/evidence bookkeeping atomically without creating a new mega-owner.
8. **External choice interrupts execution.** Segment commits/suspends and the
   SQLite transaction closes before dialogue; Continuation owns the suspension.
9. **SQL query order differs.** No mechanical/fictional result may depend on that
   order unless an owning rule supplies an explicit order key.
10. **Machine schema evolves during pre-release.** Owner payload/table adaptation
    must remain subordinate to the accepted native schema; local SQL shape is not
    allowed to freeze superseded semantics.

## Local-versus-global optimization check

The recommendation centralizes only the physical local commit kernel and common
operational metadata. It does **not** centralize semantic ownership, lifecycle,
recovery roots, publication policy, live claims, chronology or query semantics.
This avoids simplifying local code by exporting a generic SQL authority to the
rest of the system.

## Reversibility / option value

A typed owner envelope minimizes irreversible duplication because owner payloads
remain close to existing machine contracts. Narrow derived helper tables can be
added/removed as measured query needs emerge. Dedicated family normalization can
still be introduced later for a proven hotspot without changing owner identity or
durable representation.

The reverse migration—from many independent SQL-semantic schemas back to native
owner contracts—would be more expensive. This favors the envelope direction under
current pre-release uncertainty.

## Recommendation falsifiability

Recommendation confidence: **HIGH**

Evidence that would change the recommendation:

- a current accepted requirement for high-volume relational joins over owner
  fields that cannot be served by bounded derived helpers;
- a current owner contract requiring independent SQL-column lifecycle/constraints
  beyond the native schema;
- measured implementation evidence that validated envelope payloads cannot meet
  the required local transaction/query envelope without unacceptable complexity;
- a new accepted architecture decision making SQLite itself a durable/shared
  native authority.

None of those conditions is present in the inspected current source set.
