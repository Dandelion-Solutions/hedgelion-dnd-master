# R2.3 — Context Runtime Owner Decision

Status: **OWNER-APPROVED ARCHITECTURE DECISION**

Date: 2026-08-24

Decision basis:

- `2026-08-24-r2-3-context-runtime-lazy-discovery-task-brief.md`
- `../design/2026-08-24-r2-3-context-runtime-evidence-ledger.md`
- `2026-08-24-r2-3-context-runtime-decision-brief.md`

## Decision

The owner approves **Alternative B — Bounded Multi-Channel Discovery + Packet-First Allocation**.

R2.3 SHALL realize the existing Step-4 Context Assembler as a deterministic bounded runtime that:

1. discovers potential relevance through a small registered set of typed channels;
2. uses scene/location/current scope as the cheapest primary seed without making it the universal relevance oracle;
3. verifies routed currentness and role/subject/player/purpose eligibility before semantic material is relied upon by the receiving logical role;
4. loads complete semantic records only after discovery indicates they are required or useful;
5. satisfies a task-owned complete minimum evidence packet before optional/supporting context receives budget;
6. permits representation downgrade only to source/consumer-declared legal floors;
7. returns a typed assembly outcome and an access-restricted diagnostic trace;
8. never gains semantic authority merely because it discovered, ranked, cached or projected data.

## Storage-layout clarification approved with this decision

The owner additionally approves the following physical-storage constraint because it directly affects bounded discovery and routing:

> A durable file-per-record collection with plausible high/unbounded cardinality SHALL support deterministic bounded sharding. Sharding is a physical routing property derived from stable identity and SHALL NOT change semantic identity, ownership or authority.

High-cardinality families expected to need this treatment include append-heavy LOG/history families, durable Assets/items, durable NPC Actors and other record families whose plausible campaign cardinality materially exceeds a bounded GitHub directory working set. Exact directory names, shard widths and per-family physical mapping remain R2.7 machine-realization work.

Collections that are naturally and demonstrably small (for example PLAYERS, PCS and LOCATIONS under the current product profile) SHALL remain flat unless measured/real requirements justify sharding.

## Monolithic index decision

The owner explicitly rejects pre-emptive index partitioning for the current architecture.

Current per-type `*_INDEX.yaml` files remain **monolithic single-file routing projections**.

Rationale:

- current expected campaign scale does not prove that index file size or lookup cost is a material problem;
- index partitioning introduces extra routing, synchronization and recovery complexity now;
- the debt is cheap and reversible because indexes are derived/rebuildable routing structures rather than semantic authority.

Revisit trigger:

> Reopen index partitioning only when real large-campaign evidence, measured file-size/latency/tool-limit behavior, or a concrete host/API constraint demonstrates that a monolithic index is no longer operationally acceptable.

No current R2.3 law may imply that INDEX lookup requires an unbounded directory enumeration. A single index file may be loaded as one bounded routing artifact under the current profile.

## YAML / SQLite responsibility boundary retained

This decision does not create a new persistence owner.

- Git-published campaign YAML/JSON/Markdown native records remain the durable reconstruction/interchange representation according to their existing authority contracts.
- SQLite/HOT remains local execution/transaction/query state and may contain established-but-not-yet-durable SOFT state, hydrated working copies, operational execution records, reverse indexes and caches.
- SQLite SHALL NOT become the only durable copy of campaign canon or a competing semantic owner.
- Durable publication materializes a coherent dirty native-file delta from the accepted current HOT state under existing Step-5 durability/publication laws.

## Deferred physical details

R2.3 does not choose:

- exact shard directory spelling;
- exact shard arithmetic/width per record family;
- index partitioning (explicitly deferred by owner decision above);
- SQLite table layout for Context Runtime;
- concrete tokenizer implementation;
- physical ChatGPT prompt placement;
- exact host/tool call topology.

These remain downstream machine-realization or host-profile concerns.
