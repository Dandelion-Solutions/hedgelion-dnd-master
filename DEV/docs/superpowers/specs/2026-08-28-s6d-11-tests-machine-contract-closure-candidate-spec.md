# S6D-11 — Tests and Machine-Contract Closure — Step 5 Candidate Specification

Status: **STEP 5 CANDIDATE — READY FOR WHOLE-PROJECT CRITIC**

Date: 2026-08-28

## 1. Scope

This candidate realizes the already accepted S6D-01 through S6D-10 architecture as one fail-closed package/catalog machine contract. It adds no product surface, primitive authority, runtime gameplay implementation, migration policy or S6D-12 audit result.

## 2. One authoritative identity chain

strict self-including RulesetPackageManifest
+ exact declared semantic bytes
-> builder-derived member hashes
-> RulesetPackageSnapshot.content_sha256
-> exact dependency-closed ResolvedRulesetLock
-> ruleset_set_sha256

The manifest contains paths and semantic metadata, never its own digest or member digests. character-capabilities.json is capability-only content. Transitional aggregate keys are removed or migrated according to DEV/CATALOG/ruleset-package-closure.json; generated digests in that ledger are verification evidence only.

The lock is canonical JSON under HDM_RESOLVED_RULESET_SET_V1, sorted by package ID. Each package row contains package/version/compatibility/catalog identity, exact content digest, owned namespaces, exact dependencies and derived member hashes. Runtime package provenance embeds the exact lock and set digest.

## 3. Builder/loader contract

Inputs are explicit package directories, explicit root package IDs, engine version and catalog generation. The loader:

1. rejects duplicate JSON keys, unknown/invalid manifest members, paths that are external, escaping, non-normalized or symlinked;
2. requires the manifest to list itself and hashes its exact bytes without a self-declared digest;
3. resolves every exact dependency once, rejects missing/ambiguous dependencies and cycles;
4. rejects package-ID, namespace and definition collisions and requires reusable definition IDs to lie in a source-owned namespace;
5. rejects engine/catalog incompatibility and any unreconstructable or mismatched resolved set;
6. invokes the admitted package/content validators for schema, reference, catalog-admission and active-consumer closure before a context becomes usable.

The closed load-reason vocabulary is the eleven S6D-01/S6D-02 distinctions carried under failure.catalog_context_incompatible.

## 4. Compatible/additive changed-set proof

The semantic owner is DEV/ARCHITECTURE/RULESET_PACKAGE_MACHINE_CLOSURE.md. The shipped deterministic owner is GAME/TOOLS/ruleset_package.py; DEV/TOOLS/validate_ruleset_package_closure.py orchestrates build-time owner evidence and registered validators. Comparison happens after independent adopted/candidate load and before candidate context use.

Exact inputs:

- adopted and candidate resolved locks;
- canonical semantic-entry inventories derived from their exact package bytes;
- the active engine-owned primitive/selector/accessor/fact/value/schema contract inventory required by either set;
- internally derived completeness from the fixed five-family build registry compiled to path-neutral contract IDs/hashes, all registered package/content validators compiled to stable validator IDs and the campaign-owned durable-state/accepted-work dependency frontier.

Each entry is keyed by stable owner-qualified ID and carries exact kind plus SHA-256 of versioned canonical semantic JSON. For every adopted package and entry, the candidate must preserve:

- package ID, compatibility line and catalog generation;
- owned namespace claims;
- every adopted exact dependency edge;
- every existing definition/capability/active-contract entry with identical kind and semantic hash.

Candidate-only entries/dependencies are allowed only after independent validation and collision/reference closure. Removal, kind change, semantic repurposing, dependency replacement, namespace change/collision, incompatible schema/contract change, invalidated embedded accepted content or missing evidence blocks.

Result:

- COMPATIBLE_ADDITIVE: only result eligible for the existing silent forward same-version refresh;
- BLOCKED_INCOMPATIBLE: at least one incompatible difference;
- BLOCKED_INSUFFICIENT_EVIDENCE: proof inventory or registered validation is incomplete.

The result binds adopted/candidate set digests and an evidence-inventory digest. Source ancestry, matching labels and standalone candidate load never substitute for this result.

## 5. Projections

- campaign MANIFEST owns sibling immutable ruleset.created_with and creator-persisted ruleset.current;
- accepted Resolution and Continuation require the exact ruleset_set_sha256;
- checkpoint ruleset identity is a nonauthoritative projection;
- READY_PC, domain coverage and House-Rules boundary use ruleset_set_sha256;
- runtime ordinary reads use shipped GAME/ content and generated path-neutral provenance only, never DEV/; DEV filenames/test topology are compiled away before packaging.

## 6. Update authority

Existing authority is unchanged. A non-creator may use a proven forward same-engine-version descendant only when a changed embedded set returns COMPATIBLE_ADDITIVE; that user cannot persist campaign identity. The creator may later persist coherent engine/ruleset current pointers at a normal boundary. Any other changed-set result blocks silent use and routes to creator adoption/migration.

## 7. Machine artifacts

- package manifest and four strict schemas;
- reference builder/loader/comparator;
- closure census/activation ledger;
- migrated S6D-07/08/09/10 validators, fixtures and schemas;
- campaign/runtime/execution projections;
- release-builder exact-lock generation and extracted-byte verification;
- positive and negative conformance tests.

## 8. Acceptance

The current built-in package is selectable only when its manifest/bytes produce the recorded derived identities, the mandatory integrated gate executes all registered S6D-07…10 validators and completes S6D-01…10 bidirectional evidence, the repository-wide transitional census has no second authority, flattened runtime validation succeeds using GAME bytes alone, runtime/campaign projections validate and negative mutations fail closed. S6D-12 remains the next separate adversarial architecture stage.
