# Story Persistence Growth, Sharding and Consumer-Decoupling — Product Owner Decision

Status: **OWNER-APPROVED PRODUCT / RUNTIME OPERABILITY CONSTRAINT — CURRENT AS AMENDED BY 2026-09-09 SIZING-BANDS OWNER — IMPLEMENTATION NOT ACTIVATED**

Date: 2026-09-08

## 1. Purpose and authority

This decision supplements:

- `2026-09-04-runtime-mutable-github-artifact-size-owner-decision.md` (**historical threshold owner; superseded for threshold semantics by the current sizing-bands owner below**);
- `2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md` (**current mutable-artifact sizing owner**);
- `2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md`;
- `2026-09-07-story-producer-persistence-retrospective-consumer-contract.md`;
- `2026-09-08-story-baseline-projection-source-contracts.md`.

It preserves the accepted Story/Chronicler/retrospective-consumer semantics and adds an operability requirement for long-lived GitHub-backed Story persistence. It does not create a new Story layer, history owner, consumer API, global cursor, scheduler, queue, or current architecture stage.

The former absolute 10 KiB publication cutoff is **SUPERSEDED**. Current threshold semantics come from `2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md`:

```text
PREFERRED TARGET: approximately 10–12 KiB serialized UTF-8
REVIEW: normally 13–16 KiB
REVIEW / PARTITION / ROLLOVER: above approximately 16 KiB
```

These are decision bands, not universal validity enums or one exact hard stop. Exact serialized UTF-8 measurement, bounded growth, no truncation, owner-valid partitionability and publication/currentness guarantees remain controlling.

## 2. Consumer-aware file-size policy

Persisted artifacts have different read paths and may use different practical packing densities.

### 2.1 Direct LLM-facing artifacts

A text artifact that a supported LLM host is expected to read directly as a normal semantic unit must remain deliberately small and independently retrievable.

For such artifacts:

- about 250 lines is the preferred design ceiling;
- 251–300 lines is a review zone where partitioning or a smaller semantic unit should be preferred when safe;
- more than 300 lines is not an acceptable normal steady-state shape without an explicit reason why bounded alternate retrieval is safe and why semantic partitioning would be worse.

Line count is an LLM/tooling ergonomics signal, not a substitute for the current mutable-artifact sizing bands, exact byte measurement, token pressure, or actual host/tool evidence. A very large single serialized line is not made acceptable by a low line count.

### 2.2 Machine-facing structured artifacts

A structured artifact consumed primarily through deterministic runtime code may be packed more densely when that materially reduces file fan-out, reconstruction work, atomicity complexity, or Git operations.

Machine-facing status does **not** authorize indefinite single-file growth. The current sizing bands still apply to GitHub-backed runtime mutable text: target roughly 10–12 KiB or smaller where owner-valid, review normal growth in the 13–16 KiB zone, and normally activate owner-valid partition/rollover above roughly 16 KiB. Measured Git/transport/update cost may justify partitioning earlier.

## 3. No unbounded campaign-growing singleton

No mutable Story persistence family whose serialized size can grow proportionally with campaign duration, Story-record count, source-domain/origin count, chapter count, retained lookup membership, or another unbounded campaign cardinality may rely on one ever-growing file as its only supported physical representation.

For every plausibly unbounded collection, physical realization must define or preserve a deterministic path to one or more of:

- semantic partitioning into independently owned units;
- deterministic sharding/page partitioning;
- owner-valid rollover;
- owner-valid compaction where semantics permit it;
- a compact stable root plus bounded subordinate partitions.

The partition path must exist before the current representation becomes an architectural dead end. Activation may remain measurement-driven while the monolithic form remains safely within current operational bands.

This rule forbids accidental append-only singleton growth. It does not require premature fragmentation of every small machine-facing collection.

## 4. Safe partitioning laws

Partitioning is physical routing, not semantic authority.

A shard, page, bucket, directory, filename, byte offset or partition boundary MUST NOT become:

- Story identity;
- native source identity;
- fictional chronology;
- temporal or causal evidence;
- reader eligibility/disclosure authority;
- projection-coverage meaning;
- currentness authority.

Safe partition keys may use existing owner-defined semantics such as independent semantic units, Story-ID ranges, source-domain-local enrollment ranges, or NARRATIVE editorial grouping where that owner already defines the order. A physical partition must not invent a global fictional timeline merely to make storage convenient.

Known-ID direct routing and bounded discovery requirements remain controlling. Partitioning must preserve validation of the loaded semantic identity and must not require whole-corpus directory enumeration.

## 5. Publication, currentness and migration

Sharding, rollover or repartitioning must preserve the accepted publication/currentness boundary. A transition must not expose mixed old/new authority, duplicate semantic identity, dangling Story references, falsely satisfied projection coverage, or partially migrated consumer-visible state.

If activating a partition changes a compatibility-bearing physical layout, Story projection-state representation, persisted schema, or storage-generation meaning, the implementation must use the applicable Version Impact Gate and migration/adoption law. Physical optimization is not permission for an unversioned semantic reinterpretation.

Current sizing policy is prospective and owner-valid rather than an absolute 10 KiB rejection rule. A producer/writer measures the projected final serialized UTF-8 size before publication: roughly 10–12 KiB is the preferred working band, 13–16 KiB normally triggers explicit review, and above roughly 16 KiB normally triggers partition/rollover selection before indefinite further growth. Earlier partitioning may be selected from measured whole-file replacement cost, Git diff/commit amplification, transfer latency, host/tool behavior, conflict pressure, or other valid operational evidence under the applicable performance/scale owner.

## 6. Story-specific realization requirements

`STORY/<layer>/PROJECTION_STATE.yaml` may remain a compact fixed control/root artifact while that representation satisfies all applicable bounds. Its accepted route does not imply that every growth-bearing lookup, coverage, editorial, chapter, or future auxiliary collection must remain embedded in one unbounded file forever.

Future Story physical realization must explicitly inspect every field or subordinate collection whose cardinality grows with campaign history. If the growth-bearing material cannot remain within the current sizing bands and operational budgets, realization must select a deterministic bounded representation without changing Story semantic identity or retrospective meaning.

Individual Story units are also subject to the current mutable-artifact sizing policy. Semantic records should be split only where the layer contract permits independent units. A unit entering the review or review/partition band is not automatically invalid: the owner must preserve exact archival requirements, reference closure, identity and atomicity, and choose the safest valid representation. Exact material must never be truncated or paraphrased merely to reduce storage size. If an accepted exact archival scope can exceed one indivisible file, its owner/schema must define safe bounded partition/reconstruction semantics before such a representation is admitted.

This decision does not select a concrete `PROJECTION_STATE` shard layout, index partition count, chapter-file layout, or exact rollover threshold. Those choices remain implementation/performance evidence work under their existing owners.

## 7. Retrospective-consumer decoupling

The public retrospective consumer boundary is semantic and storage-topology-neutral.

A retrospective consumer must not require knowledge of:

- physical Story filenames or directories;
- shard/page IDs;
- partition counts or rollover boundaries;
- `PROJECTION_STATE` internal packing;
- Git tree layout as semantic evidence.

Context Runtime and the Story/native evidence provider boundary remain responsible for physical routing, bounded acquisition, currentness and representation validation. Consumer-visible `StoryRef`, evidence kinds, native references, read bases, eligibility and failure semantics remain independent of whether a provider reads one file or several bounded shards internally.

Therefore a later physical Story repartition, by itself, MUST NOT require a semantic redesign of a conforming retrospective consumer. A consumer contract change is justified only when the semantic evidence/read contract changes, not because storage was sharded.

## 8. Relationship to WP-11 and WP-24

WP-11's accepted monolithic family-index baseline and its measured WP-24 partition trigger remain in force except for the superseded absolute 10 KiB threshold semantics. This decision does not prematurely select index partitioning.

WP-24 and later physical-realization work must, however, treat bounded partitionability as a design requirement for every plausibly unbounded GitHub-backed Story collection. Measurement and the current sizing bands decide **when and how** a larger machine-facing structure should partition; they do not permit a representation with no safe partition path at all.

Story backlog remains derived and bounded per operation. This requirement does not introduce background Chronicler workers, queues, leases, heartbeats, or whole-campaign preload.

## 9. Required downstream consumption

When Story/Chronicler persistence is planned or implemented, the Source Manifest must include this decision together with the Story integration contract, baseline projection source contracts, WP-11 physical topology, `2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md`, publication/currentness owners, and applicable WP-24 performance/scale results.

Implementation acceptance must verify at least:

1. growth-bearing mutable Story files apply the current target/review/review-and-partition sizing bands using exact serialized UTF-8 measurement rather than a universal 10 KiB rejection cutoff;
2. direct LLM-facing Story material remains bounded and independently retrievable;
3. every campaign-growing machine-facing collection has a deterministic bounded partition path;
4. partitioning preserves identity, publication/currentness, reference closure and coverage semantics;
5. retrospective consumers do not bind to physical Story shard topology;
6. required Story material is never truncated or semantically falsified merely to satisfy a target size.

## 10. Version and current-stage impact

```text
VERSION_IMPACT: NONE
```

This documentation reconciliation changes no implemented machine value, persistent schema, storage generation, Story schema version, projection semantic generation, runtime module version, engine version or package protocol. It constrains future physical realization. Any later implementation that changes a version-bearing layout or schema must perform its own Version Impact Gate.

Recording this decision does not activate Story implementation, start implementation planning, authorize WP-27, release execution or gameplay bootstrap. Concrete writer partition topology remains downstream realization work.
