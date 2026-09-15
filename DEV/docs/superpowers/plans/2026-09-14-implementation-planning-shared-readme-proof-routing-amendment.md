# HDM Implementation Planning — Shared README Proof-Routing Amendment

Status: **CURRENT HIGHEST-PRECEDENCE MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **AUTHOR FINDING 47 — SIGNIFICANT**
Production implementation: **NO**.

This amendment repairs the proof-routing gap left by F41. It changes no semantic owner, no shipped behavior, no execution ordering and no F41 shared-file integration mechanism.

## 1. Finding

F41 correctly requires one final physical integration checkpoint for each shared documentation projection:

```text
GAME_SCHEMA_README_FINAL_INTEGRATION_READY
GAME_STORAGE_README_FINAL_INTEGRATION_READY
```

and correctly states that isolated RD-02/RD-03/RD-04/RD-07 GREEN results are insufficient because the final integrated bytes may still lose another owner's projection.

However, F41's proof section only says that the package must add a direct cross-owner projection witness. It does not name an executable witness, does not bind that witness to a concrete proof module and does not assign a primary proof channel. The current post-graph proof ledger and exact witness matrix likewise contain no F41/README row.

Therefore a legal package-closure implementation could execute all owner-local focused suites, satisfy the two integration checkpoint names in prose, and still never inspect the final integrated README bytes through a package-bound witness. That violates the F22 exact-witness law:

```text
mechanism + named executable witness + primary proof channel
```

must all exist before a post-graph repair can be considered planned-closed.

## 2. Exact executable witness

When implementation/proof execution is authorized, add exactly one package proof class:

```text
DEV/TESTS/test_implementation_proof_ledger.py
  SharedSchemaStorageReadmeIntegrationProofTests
```

Primary proof channel:

```text
STATIC_AUDIT
```

Owner-local RD tests remain supporting semantic/projection evidence. They do not substitute for this final integrated-byte witness.

The proof class is created only in the authorized proof task that owns the final package proof surface; it is not pre-created as a failing future test.

## 3. Exact byte targets and assertions

`SharedSchemaStorageReadmeIntegrationProofTests` must read the actual final package bytes of:

```text
GAME/SCHEMA/README.md
GAME/TEMPLATE/STORAGE_README.md
```

and prove all of the following.

### 3.1 `GAME/SCHEMA/README.md`

1. No stale embedded epistemic-authority route remains: knowledge/disclosure/message projections do not create a second writable truth/knowledge/disclosure owner.
2. Actor/Asset/Effect are projected as the admitted native families and the README does not resurrect PC/NPC/item as independent native owner families.
3. Indexes/routes are described as rebuildable/non-authoritative discovery/routing helpers and known-ID direct routing remains the correctness path where the owner defines it.
4. Checkpoint/event/frontier/session metadata is not presented as currentness, recovery-source or global-frontier authority. The RD-08 CURRENT projection remains compact routing/current-summary metadata, not a campaign-wide chronology owner.
5. All five current F41/F55 owner-local projection contributions (RD02/RD03/RD04/RD07/RD08) are simultaneously present in the final integrated bytes, including RD-08's required CURRENT/schema and applicable temporal-contract projection. Dropping the RD-08 contribution fails even if the original four remain. Proof against isolated fixtures or pre-integration snapshots is invalid.

### 3.2 `GAME/TEMPLATE/STORAGE_README.md`

6. The final bytes simultaneously preserve RD-02 information-owner separation, RD-03 Actor/Asset/Effect native cutover and RD-04 owner-native direct-routing/rebuildable-index/storage laws.
7. The file does not restore legacy PC/NPC/item native compatibility fiction or embedded writable epistemic authority.
8. A final-file regression that drops any one owner contribution fails even if every individual RD focused suite remains GREEN.

### 3.3 Shared-writer negative law

9. The proof must operate on the final integrated package bytes after both F41 physical integration checkpoints; test-name existence or owner-local candidate text cannot discharge F47.
10. No documentation projection gains semantic authority merely because the package proof validates it.

## 4. Proof checkpoint

Add the proof-only sink:

```text
GAME_SCHEMA_README_FINAL_INTEGRATION_READY
+ GAME_STORAGE_README_FINAL_INTEGRATION_READY
+ SharedSchemaStorageReadmeIntegrationProofTests GREEN
  PROOF_AFTER_TARGET
SHARED_SCHEMA_STORAGE_README_PROOF_READY
```

`SHARED_SCHEMA_STORAGE_README_PROOF_READY` is a proof sink only. It does not feed any semantic producer, does not serialize RD-02/RD-03/RD-04/RD-07/RD-08 owner work and cannot participate in an execution cycle.

Package author closure and later independent Senior handoff may not claim F41 repaired/verified without this proof sink.

## 5. Proof-router precedence

The current proof route is amended as follows:

```text
historical v2 proof ledger/appendices
+ post-graph proof ledger v3
+ F27-F31 control amendment
+ exact post-graph witness matrix
+ F34-F46 later-precedence proof amendments
+ this F47 proof-routing amendment
```

Where the older proof router is silent about F41 final integrated README bytes, this amendment controls.

No new historical readiness ID or semantic PG mechanism row is created. F47 is a proof-routing repair over the already accepted F41 mechanism.

## 6. Execution / version / migration consequence

```text
NEW_EXECUTION_EDGE: NO
NEW_SEMANTIC_OWNER: NO
NEW_RD: NO
NEW_READINESS_ID: NO
VERSION_IMPACT: NONE
MIGRATION_IMPACT: NONE
```

The two existing F41 integration checkpoint identities remain unchanged; F55 extends the schema-README input set in overlay 30. F47 makes their final integrated-byte proof explicit and mandatory.

## 7. Disposition

```text
AUTHOR_FINDING_47: SIGNIFICANT
ROOT_CAUSE: F41 required integrated-byte proof but did not name an executable package witness or primary proof channel, and the current proof router omitted that mechanism
EXACT_WITNESS: SharedSchemaStorageReadmeIntegrationProofTests
PRIMARY_CHANNEL: STATIC_AUDIT
PROOF_SINK: SHARED_SCHEMA_STORAGE_README_PROOF_READY
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```

This author-side repair does not constitute zero-open closure and does not unblock independent Senior review.

## 8. F55 — RD-08 shared schema-README contribution

The exact module/class and primary `STATIC_AUDIT` channel above are unchanged. The existing schema-README target now consumes `RD08_SCHEMA_DOC_DELTA_READY` as its fifth projection input under overlay 30; the storage-template target retains its three original inputs. Run this same actual-final-byte witness after both targets, with the RD-08 assertion included. No new semantic checkpoint, test class or whole-RD/R077 barrier is introduced.
