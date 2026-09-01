# R2.7 WP-11 Step 3 — Physical Topology Decision Brief

Status: **DECISION BRIEF — HUMAN DECISION REQUIRED: NO**

## Decision

Select a uniform, deterministic content-addressed route for every native
campaign record family that can grow independently. Retain fixed singleton
files, keep Story's established sequence-bucket route, and preserve the
separate branch-local LIVE layout. Monolithic indexes remain compact discovery
projections, not the route needed for exact lookup by stable ID.

For a record identity byte sequence `I`, the general native record route is:

```text
H = lowercase-hex(SHA-256(UTF-8(I)))
<family-root>/RECORDS/H[0:2]/H[2:4]/H.yaml
```

The record body must carry and validate the native semantic ID. A digest/path
mismatch or two distinct IDs at the same computed route is an integrity failure;
the path does not become an alternate identity. Composite identities use the
owner's canonical ordered component encoding before this routing calculation.

## Why this decision is needed now

Current roots and `*_INDEX.yaml` templates expose only placeholders and generic
entries. They cannot prove bounded lookup, prevent large-directory enumeration,
or supply routes for the WP-10 lifecycle/evidence families. WP-11 must make that
physical allocation before WP-12 can choose working-state realization.

## Alternatives assessed

| Alternative | Benefit | Rejected weakness |
|---|---|---|
| Flat family directories with the ID as filename | Human-visible direct paths and minimal scaffolding. | Does not bound a high-cardinality directory, depends on ID filename safety, and leaves GitHub listing limits on the ordinary route. |
| Sequence-range buckets for all native records | Intuitive locality for sequential IDs. | Does not safely route composite/derived/external IDs, invites order to be treated as chronology, and requires allocator/range coupling that current owners do not grant. |
| Uniform hash route with bounded discovery indexes | Applies to sequential, derived and composite identities without changing their semantic form; direct lookup requires only the known family and ID; two-level shards bound directory fan-out. | Paths are not human-readable and require deterministic hash/record-ID validation. This cost is acceptable because indexes supply approved discovery metadata. |

Story is the justified exception: its accepted owner already selects a
layer-local, thousand-sequence grouping for one-record-per-file projection
records. LIVE is the other exception because its one-file epoch overlay and
exact-source CAS are an accepted operational partition, not campaign-family
storage.

## Index contract

- By-ID lookup calculates the native route directly and does not enumerate a
  directory or require an index.
- A monolithic family index supports approved name/alias/status discovery and
  maps the discovered stable ID to its routing path. Existing current template
  indexes retain their fixed names; newly materialized discovery families follow
  the same family-local naming convention.
- An index entry remains compact, non-secret-bearing and owner-approved. It
  cannot contain protected knowledge, disclosure, private continuity, Story
  availability material or live write authority.
- The index is rebuilt from the authoritative family after bounded validation;
  an omitted entry is not negative semantic proof. Rebuild/index update belongs
  in the same publication closure as the native record it describes.
- Index partitioning is not selected now. It is a WP-24 revisit only when
  measured index size, search latency or host/tool limits make the monolithic
  file unsuitable.

## Boundary consequences

This maps physical roots, shard arithmetic and lookup/index interaction only.
It does not alter semantic ownership, schemas, ID allocation, HOT/SQLite,
publication, recovery, live claims, bootstrap, migration, Story record format
or index implementation. Those remain downstream obligations under their named
owners.

## Recommendation confidence and falsifiability

**Recommendation confidence: HIGH.** Change this recommendation only if a
current primary owner establishes a non-hash mandatory route, a supported host
cannot deterministically compute SHA-256 for UTF-8 identity bytes, or WP-24
measures a limit requiring a different index/shard shape. None is present in the
Step-2 evidence.
