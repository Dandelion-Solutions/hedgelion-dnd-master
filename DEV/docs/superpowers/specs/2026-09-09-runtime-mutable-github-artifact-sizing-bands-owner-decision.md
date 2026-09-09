# Runtime Mutable GitHub Artifact Sizing Bands — Product Owner Superseding Decision

Status: **OWNER-APPROVED PRODUCT / RUNTIME OPERABILITY CONSTRAINT — CURRENT SIZE POLICY**

Date: 2026-09-09

## 1. Purpose and supersession

This decision replaces the previous interpretation of **10 KiB as an absolute per-file publication cap** for runtime-authored mutable GitHub-backed text artifacts.

It supersedes, only for file-size threshold semantics:

- `DEV/docs/superpowers/specs/2026-09-04-runtime-mutable-github-artifact-size-owner-decision.md`, especially its former `RUNTIME_MUTABLE_GITHUB_TEXT_FILE_MAX_BYTES = 10240` hard-cap law;
- `DEV/docs/superpowers/specs/2026-09-08-r2-7-WP-24-performance-scale-operational-budget-canonical-spec.md` LAW `WP24-13` where it treats 10 KiB as an absolute publication trigger;
- `DEV/docs/superpowers/specs/2026-09-08-story-persistence-growth-sharding-consumer-decoupling-owner-decision.md` wherever it treats 10 KiB as an absolute Story mutable-file cap.

All unaffected ownership, partitionability, currentness, atomicity, no-truncation, transport, Story identity and consumer-decoupling laws remain in force.

This is not a claim about a GitHub vendor hard limit. It is HDM operational guidance for deciding when a growth-bearing mutable text representation should remain in its current file, be reviewed, or be partitioned/rolled over.

## 2. Product sizing policy

The current operational bands are:

```text
PREFERRED TARGET BAND
    approximately 10–12 KiB serialized UTF-8

REVIEW BAND
    materially above the target through approximately 16 KiB
    with 13–16 KiB as the normal explicit review zone

REVIEW / PARTITION / ROLLOVER BAND
    above approximately 16 KiB
```

These are **decision bands, not validity enums and not a universal byte-hard-stop**.

For deterministic implementation comparisons, measure the exact serialized UTF-8 byte length. The KiB labels are human-operational bands rather than a promise that transport behavior changes at one exact byte.

### LAW SIZE-1 — 10 KiB is shorthand, not a hard cutoff

Architecture and human-facing guidance may continue to say “about 10 KiB” where a compact conservative reminder is useful.

That shorthand MUST NOT be implemented as a universal rule that rejects every payload above 10,240 bytes.

### LAW SIZE-2 — The target band is a preferred steady-state working size

For mutable containers whose contents can grow over campaign lifetime, implementations SHOULD aim to keep ordinary steady-state files around **10–12 KiB or smaller** when this is compatible with the owning semantic model.

Smaller files are valid. The target band is not a minimum and no implementation may add padding or artificial fragmentation merely to approach 10 KiB.

### LAW SIZE-3 — Review begins when a file materially leaves the target band

A growth-bearing file that moves materially above the target band requires an owner-valid size/shape review rather than an automatic failure.

The practical **13–16 KiB region is the normal review zone**. The review asks whether continued growth remains safe and cohesive or whether the owner should activate an already-valid partition, rollover, compaction or semantic split.

The implementation should not wait for a transport error to begin this review.

### LAW SIZE-4 — Above approximately 16 KiB, partition/rollover is the default expectation

A mutable growth-bearing artifact above approximately **16 KiB** is in the **review/partition/rollover zone**.

The default expectation is to activate an owner-valid bounded representation before allowing indefinite continued growth.

This is still not an automatic semantic invalidity rule. If one indivisible owner unit cannot be split without breaking identity, atomicity, provenance, exactness or another accepted semantic law, the owning design must choose the safest valid representation. It must not truncate required material or invent a semantically false split merely to hit a number.

### LAW SIZE-5 — Growth decisions are prospective

A writer/producer responsible for a campaign-growing container should use the **projected serialized size of the pending write** when deciding whether to remain in the current file or activate rollover/partitioning.

Do not knowingly grow an already review-zone file indefinitely and defer the decision until a later unrelated operation.

## 3. Preserved semantic constraints

The sizing bands do not weaken these existing laws:

- independently owned semantic units should remain independently addressable where the owner already permits it;
- no truncation or omission of required canon, history, provenance, knowledge, disclosure, exact text or Story material merely to reduce file size;
- no physical shard/page/file boundary becomes semantic identity, chronology, authority, currentness, eligibility or projection-coverage meaning;
- publication/currentness atomicity must survive partition/rollover;
- known-ID bounded routing must not degrade into whole-directory or whole-corpus scans;
- one semantic entity must not be fragmented unless its owner/schema defines safe reconstruction;
- mutable campaign-growing singleton structures require a deterministic bounded partition/rollover path before they become an operational dead end.

## 4. Runtime and Story application

### Runtime campaign/live/storage writers

The writer responsible for a mutable GitHub-backed text artifact must measure the final serialized UTF-8 payload and apply the bands before publication.

The size decision belongs with the artifact's semantic owner and physical-realization contract. `PERSISTENCE.md` remains transport authority and does not independently invent partition semantics.

### Story / Chronicler persistence

Story remains subject to the existing bounded-growth and consumer-decoupling architecture. The new bands replace only the former absolute 10 KiB threshold.

Story producers/storage realization should:

```text
prefer roughly 10–12 KiB or smaller steady-state mutable units
-> review growth in the roughly 13–16 KiB region
-> normally partition/roll over above roughly 16 KiB
```

Exact Story record indivisibility, reference closure, exact archival requirements, projection coverage and publication atomicity remain controlling.

### Read-only runtime/reference material

Packaged read-only engine instructions, schemas, rules, catalogs and other reference artifacts are not governed by these mutable-growth bands merely because they are larger. Their own retrieval/context/tooling constraints remain separate.

## 5. DEV artifacts

This decision does not create a hard size gate for DEV prose, architecture documents, catalogs or test artifacts.

For development artifacts, semantic cohesion and owner clarity remain primary. Large DEV files may be reorganized when doing so improves navigation/maintenance, but file-size bands alone do not authorize destructive historical rewriting or fragmentation of one coherent owner.

WP-26 may identify stale size-policy statements and routing debt, but should distinguish current implementation-facing owners from historical provenance rather than rewriting the entire design history.

## 6. Relationship to WP-24, WP-26 and WP-27

### WP-24

WP-24's general performance architecture remains closed. Only the former absolute 10 KiB trigger is superseded. Its broader laws on bounded operations, evidence-driven optimization, owner-preserving partitioning and real-target measurement remain current.

### WP-26

WP-26 must include this decision in its Source Manifest because current routing/supersession cleanup must prevent implementation agents from treating the retired 10 KiB hard cutoff as current law.

It must locate current/historical references to the old hard-cap formulation and classify them as:

```text
CURRENT AND MUST BE REPAIRED/ROUTED
HISTORICAL PROVENANCE AND SAFE TO RETAIN WITH SUPERSESSION
DERIVATIVE INDEX/ROUTING THAT MUST POINT TO THIS OWNER
TEST/MACHINE ASSERTION REQUIRING LATER REALIZATION OR CURRENT REPAIR
```

### WP-27 and implementation planning

Implementation planning must derive the concrete file-growth/rollover workstreams from this owner together with the owning runtime/Story/storage schemas and tests.

It must not recreate `10240` as an unconditional rejection threshold unless a narrower concrete owner independently proves and accepts such a hard limit for its own representation.

## 7. Product Owner input disposition

The Product Owner sizing clarification is fully incorporated by this owner decision.

```text
PRODUCT_OWNER_INPUT_STATUS: INCORPORATED
OPEN_PO_DECISION: NONE
OLD_10_KIB_HARD_CAP: SUPERSEDED
CURRENT_POLICY: TARGET / REVIEW / REVIEW-AND-PARTITION BANDS
```

No further Product Owner decision is required for the sizing policy itself.

## 8. Version and current-stage impact

```text
VERSION_IMPACT: NONE FOR THIS DOCUMENT-ONLY OWNER DECISION
ENGINE_VERSION_BUMP_REQUIRED: NO
PERSISTED_SCHEMA_GENERATION_CHANGE: NONE BY THIS DOCUMENT
MIGRATION: NONE BY THIS DOCUMENT
```

Future machine realization that changes a persisted layout, sharding scheme, schema, module or compatibility-bearing representation must run its own Version Impact Gate.

Publishing this decision does not itself implement runtime partitioning or Story storage. It is a binding input to WP-26 routing/supersession work and later WP-27/implementation planning.