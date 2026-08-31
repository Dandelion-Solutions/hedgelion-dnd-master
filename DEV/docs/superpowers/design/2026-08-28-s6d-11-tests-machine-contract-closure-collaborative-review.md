# S6D-11 — Tests and Machine-Contract Closure — Step 4 Collaborative Architecture Review

Status: **STEP 4 COMPLETE — CANDIDATE CONTRACT AGREED FROM EXISTING OWNERS**

Date: 2026-08-28

## 1. Reviewed architecture

The review converts the Step-2 evidence and Step-3 no-decision result into exact component boundaries.

## 2. Components

### Package manifest

One strict self-including path declaration with package/version/compatibility/engine/catalog/namespace/dependency metadata. It contains no snapshot or member digest authority.

### Package builder/loader

A pure bounded component validates explicit roots/manifests, hashes exact bytes, resolves exact dependencies, rejects cycles/ambiguity/collisions, validates package content, produces the exact lock and reconstructive loaded definition set, and returns closed typed failures.

### Compatibility comparator

Consumes two already-valid resolved sets plus owner-supplied semantic/machine inventories. Existing adopted entries must be present with identical kind and canonical semantic hash. Candidate additions must be independently valid and noncolliding. Insufficient proof blocks. The comparator does not own product semantics or update authority.

### Closure ledger

Accounts transitional identity, S6D-01…10 equality/proof families, projections, typed failures and tests. It is DEV conformance evidence, not runtime catalog authority.

### Release integration

The runtime release composer invokes the ruleset contract and embeds its exact generated lock/set identity in runtime provenance. It continues to own ZIP composition/provenance only. Runtime never reads DEV sources.

## 3. Identity and projection decisions

- `character-capabilities.json` becomes capability-only semantic content.
- READY_PC, domain coverage and House-Rules boundary bind to `ruleset_set_sha256` because their proofs span the selected set.
- a package-local diagnostic may reference package `content_sha256`, but no current gameplay proof needs a second durable package digest.
- accepted Resolution/Continuation retain both `ruleset_set_sha256` and `catalog_context_fingerprint`.
- campaign `ruleset.created_with/current` is sibling to engine identity; creator/persistence laws remain unchanged.
- checkpoint ruleset evidence is projection only.

## 4. Compatibility algorithm

Canonical semantic entry hashes use UTF-8 canonical JSON (`sort_keys`, compact separators, no NaN) and a versioned domain separator. For every adopted entry:

```text
candidate contains key
AND candidate.kind == adopted.kind
AND candidate.semantic_sha256 == adopted.semantic_sha256
```

Package dependency/namespace claims and active engine-owned contract entries obey the same preservation rule. Candidate-only entries are additions. Deletion, collision, changed existing entry or absent proof blocks.

The result is bound to both set digests and an evidence-inventory digest. It is produced after independent loading and before context use.

## 5. Typed failure mapping

The top-level code remains `failure.catalog_context_incompatible`. Closed reasons include the eleven S6D-02 minimum reasons. Compatibility comparison additionally produces reason rows under `BLOCKED_INCOMPATIBLE` or `BLOCKED_INSUFFICIENT_EVIDENCE`; these are not new top-level execution codes.

## 6. Acceptance walkthroughs

### Clean build/load

Explicit package root -> strict manifest -> exact bytes/hash -> one-entry resolved lock -> set digest -> strict content/reference validation -> reconstructed context -> active bounded package proof.

### Same-version additive refresh

Adopted and candidate load independently -> exact entries compared -> all adopted entries identical -> candidate-only IDs valid/noncolliding -> `COMPATIBLE_ADDITIVE` -> silent use allowed under existing update owner -> creator alone may later persist coherent pointers.

### Changed existing definition

Candidate loads independently but one existing definition hash differs -> comparator returns `BLOCKED_INCOMPATIBLE` before context use -> no silent fallback -> creator review/adoption/migration route only.

### Transitional evidence

Old READY_PC/domain/policy aggregate key is presented -> strict current schemas/validators reject it -> canonical set identity proof succeeds -> no second authority remains.

## 7. Negative space

No network registry, package discovery scan, semantic DSL, LLM compatibility judgment, per-world-record digest, global context snapshot, dormant activation, synthetic Mechanical-Null mutation, migration for nonexistent campaigns, or S6D-12 final audit is introduced.

## 8. Step-4 result

The architecture is exact enough for a candidate specification and authorized structural/machine conformance materialization. No human decision is required.

