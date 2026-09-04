# Runtime Mutable GitHub Artifact Size — Product Owner Decision

Status: **OWNER-APPROVED PRODUCT / RUNTIME OPERABILITY CONSTRAINT**

Date: 2026-09-04

Target branch: `v1/engine-rearchitecture`

Decision origin: explicit Product Owner direction received during R2.7 WP-18 final Senior recovery.

## 1. Purpose

The runtime uses connected GitHub transport as durable campaign storage. Mutable game/campaign records therefore need a bounded per-file representation that can be retrieved as one semantic unit and safely rewritten without depending on chunk reconstruction or oversized whole-file replacement.

This is a project operability requirement. It is not a claim about a GitHub repository/file-size limit or a vendor hard limit.

## 2. Product Owner decision — runtime hard invariant

The accepted runtime limit is:

```text
RUNTIME_MUTABLE_GITHUB_TEXT_FILE_MAX_BYTES = 10240
```

That is **10 KiB / 10,240 bytes**.

For every semantically textual game/campaign artifact that the runtime may create, replace or update through connected GitHub transport, the final serialized UTF-8 payload MUST be no larger than 10,240 bytes.

The limit applies to runtime-authored mutable campaign/storage artifacts, including mutable records under campaign, live, state, index, world, log, checkpoint, retained-planning and equivalent runtime-owned persistence surfaces.

Measure the exact UTF-8 byte length of the final serialized file payload after serialization and before transport.

A runtime write MUST NOT publish a payload that exceeds the limit.

If a pending payload would exceed the limit, the owning runtime/domain design MUST resolve the condition before publication by an architecture-valid operation such as:

- semantically partitioning independent entities/records/families into separate files;
- compacting state that is explicitly compactable without losing required semantics;
- rolling over a bounded hot-state container such as a live epoch;
- moving independently owned material to its proper existing owner record.

The runtime MUST NOT satisfy the limit by silently truncating canonical information, dropping required provenance/history/knowledge, or splitting one semantic entity across files when the entity owner/schema does not define safe partition and reconstruction semantics.

If one indivisible semantic entity cannot be represented within the limit under its accepted owner/schema, that is an unsatisfied runtime design/representation requirement. The owner/schema must be redesigned before that representation is admitted to runtime writes; the size invariant is not bypassed.

## 3. Explicit exemption — read-only runtime material

Large engine/runtime instructions, schemas, rules, catalogs and other packaged/reference artifacts that are read-only during gameplay MAY exceed 10 KiB.

They are not subject to the mutable-file cap because runtime correctness does not require whole-file replacement of those artifacts. Bounded/range reads or other text-safe retrieval may be used when a large read-only source cannot be returned as one response.

A large derived aggregate is also acceptable when it is read-only at runtime and its mutable/source representation is maintained safely elsewhere.

The exemption does not apply merely because a file changes rarely. If the runtime may rewrite it as part of normal or maintenance operation through the connected GitHub transport, it is mutable for purposes of this invariant.

## 4. Why the project cap is 10 KiB

Current connected-transport observations on 2026-09-04 show that whole-file retrieval behavior is content/token-density dependent rather than a simple monotonic byte cutoff.

Representative current-repository probes on the same transport included:

```text
10,849 bytes  -> returned whole
14,500 bytes  -> returned whole
15,926 bytes  -> returned whole
18,028 bytes  -> returned whole
16,839 bytes  -> response truncated
20,143 bytes  -> response truncated
```

Therefore the project MUST NOT treat the largest successful probe as a guaranteed boundary.

10 KiB is intentionally below the observed ambiguous region and leaves a substantial safety margin for JSON/YAML punctuation, identifiers, escaping, Unicode text and other payload-shape differences.

No exact external hard limit is assumed by this decision. The number is a conservative project operational guarantee for the currently used connected GitHub workflow.

### Revisit triggers

Re-evaluate this value when any of the following becomes true:

- the connected GitHub transport publishes a stable documented whole-text read/write envelope that makes a different bound demonstrably safe;
- transport behavior changes materially;
- patch/range-safe mutation removes the whole-file replacement dependency;
- empirical validation shows that 10 KiB is no longer safely retrievable/writable as one runtime artifact;
- HDM adopts a different persistence transport for mutable runtime state.

Until an explicit superseding decision is published, 10 KiB remains the hard runtime cap.

## 5. Compatibility with accepted runtime architecture

This decision tightens existing architecture rather than replacing its ownership model.

`GAME/CORE/STORAGE.md` already prefers separate files for independently changing scene/PC/NPC/location/item/faction/thread/session/log records. The new constraint makes bounded file size an explicit runtime invariant in addition to semantic partitioning.

`GAME/CORE/LIVE_SCENE.md` already requires epoch rollover when `LIVE/LIVE_STATE.yaml` grows beyond a practical hot-state budget. The accepted size requirement means rollover/compaction must occur early enough that no published live-state payload exceeds 10 KiB.

`GAME/CORE/PERSISTENCE.md` already owns GitHub write transport and complete text payload publication. Its later realization must enforce the size preflight before publication and route an oversized pending artifact back to its owning semantic partition/compaction/rollover rule rather than attempting an oversized write.

This owner decision does not create a second persistence authority and does not by itself reopen the accepted storage or live-epoch architecture class.

## 6. Product Owner direction — DEV artifact recommendation

Development artifacts do **not** have a hard 10 KiB file-size requirement.

For DEV JSON and similar mutable structured artifacts, use this recommendation:

1. Prefer smaller, semantically cohesive files when independent entities, registry families, domains or other independently owned units can be separated cleanly.
2. Keep one semantic entity/owner unit together. Do not fragment one entity across several files solely to satisfy a tooling-size preference.
3. When a large aggregate is useful to consumers, prefer semantically separated authoritative source files plus a mechanically generated/read-only aggregate when that architecture is justified.
4. If a large file cannot be divided without weakening semantic cohesion, ownership clarity, atomicity or maintainability, keeping one large file is acceptable.
5. File-size convenience is subordinate to semantic integrity; this DEV rule is guidance, not a validation failure by itself.

`DEV/CATALOG/catalog-admission-ledger.json` is an immediate candidate for a later bounded evaluation of source partitioning because the current whole-file workflow has already exposed a maintenance limitation. This decision does **not** itself change that ledger's format, authority, consumers or tests; any split must preserve current semantics and update its consumers coherently.

## 7. Required downstream propagation

This decision is durable owner input. It does not authorize WP-19, implementation planning or an unrelated architecture stage while the current R2.7 WP-18 final recovery/Senior gate remains open.

Before mutable campaign persistence is implemented/released against this architecture, the requirement must be propagated coherently through the applicable current owners/consumers, including at least:

- `GAME/CORE/STORAGE.md`;
- `GAME/CORE/PERSISTENCE.md`;
- `GAME/CORE/LIVE_SCENE.md`;
- mutable campaign/live schemas and templates that can determine file layout;
- persistence/live validation and regression coverage;
- any generated or runtime writer that can produce mutable GitHub-backed game/campaign files.

The implementation-facing realization should make the invariant machine-checkable at write preflight rather than relying only on prose.

For DEV process maintenance, the recommendation in section 6 should be propagated into the appropriate development/process guidance without converting it into a hard DEV size gate.

## 8. Current-stage boundary

Recording this Product Owner decision does not alter the active R2.7 sequencing:

```text
WP-18 final Senior recovery / re-audit
    -> closure gate
    -> only then the next explicitly authorized unit
```

The decision is an accepted cross-cutting constraint to be consumed by the relevant owning work; it is not permission to start implementation or WP-19 early.
