# Step 5.7 — Checkpoint / Recovery Protocol — Resolution Gate

Status: **RESOLVED — READY FOR CANONICALIZATION**

Date: 2026-08-20

Candidate:

`2026-08-20-step-5-7-checkpoint-recovery-protocol-candidate-spec.md`

Adversarial review:

`2026-08-20-step-5-7-checkpoint-recovery-protocol-adversarial-review.md`

Resolved architecture direction:

> **CURRENT-AUTHORITY-FIRST / CHECKPOINT-OPTIONAL NATIVE-ROUTED BOUNDED RECOVERY**

## 1. Gate result

The adversarial review found no unresolved Step-5.7 architecture blocker and no new material owner-level decision.

All significant findings are resolved by tightening semantics or assigning exact later ownership without leaving a correctness gap.

The only potential product-level issue exposed—guaranteed player-visible historical rewind—is not currently promised by canonical gameplay architecture. Step 5.7 therefore does not silently introduce it as a checkpoint property. If such a feature is later requested, it requires its own cross-cutting retention/knowledge/history semantics.

## 2. Resolved findings

### R1 — `READY` is not a lock/lease

Accepted.

Canonical wording SHALL define recovery `READY` as:

> a validated coherent recovery basis at the recovery gate for the requested resume/read capability.

It SHALL NOT mean:

- the sources can never move after the gate;
- a global lock exists;
- next mutation may skip normal CAS/currentness/fencing;
- repository write credential implies gameplay write authority.

Subsequent campaign writes remain subject to Step-5.6 CAS. Live writes remain subject to Step-5.8 current ownership/fencing.

### R2 — root-routing/lifecycle basis participates in validation

Accepted.

Recovery MUST validate the native routing/lifecycle basis used to enumerate current roots. Legitimate movement invalidates the attempt and causes bounded retry; persisted mismatch at one pinned current source is an integrity defect for the affected scope.

No universal routing generation is introduced.

### R3 — Procedure lifecycle machine debt

Accepted as implementation debt.

Current Procedure schema lacks sufficient explicit lifecycle evidence for the canonical root-enrollment invariant. Machine realization must add/derive deterministic lifecycle evidence and atomically couple activation/termination with routing membership.

Checkpoint SHALL NOT absorb Procedure lifecycle authority as a workaround.

### R4 — checkpoint acceleration is not required

Accepted.

Ordinary recovery MAY perform zero checkpoint reads when native typed routing already provides bounded recovery closure.

Checkpoint optimization requires measured/real value and current validation.

### R5 — checkpoint pointer integrity is facility-scoped

Accepted.

A dangling/malformed optional checkpoint pointer may make checkpoint metadata/maintenance functionality suspect without automatically invalidating independently healthy gameplay current-state scopes.

### R6 — metadata-only checkpoint requires independent value

Accepted.

A clean-state checkpoint write is allowed only when it creates independently justified new recovery/maintenance evidence/value.

Time/age/freshness/session-count/heartbeat alone are not sufficient reasons.

### R7 — checkpoint hints are non-exhaustive by default

Accepted.

Checkpoint source/root/routing observations do not prove completeness or absence. Current native routing/lifecycle owns membership.

No generic checkpoint RecoveryCut is introduced.

### R8 — compatibility remains owner-native

Accepted.

Recovery orchestrates owner-specific compatibility predicates; it does not introduce one universal cross-domain compatibility ordering/frontier.

### R9 — duplicate discovery paths do not duplicate semantic obligations

Accepted.

The same native owner/temporal obligation discovered through multiple roots is hydrated/rebuilt once by stable identity. Routing duplication never creates duplicate occurrence/execution authority.

### R10 — authorization is a separate prerequisite

Accepted.

Repository capability is technical transport. Recovery/read/write/disclosure authorization is governed by application/access owners and must be validated for the requested operation.

### R11 — current-authority-first preserves accepted historical execution evidence

Accepted.

Current authority selection does not overwrite legitimately pinned accepted causal inputs/context retained by Step-3 execution owners. Recovery resolves those exact historical/accepted dependencies where required.

### R12 — RecoveryResult remains non-authoritative

Accepted.

`READY | RETRY | BLOCKED` and selected-source diagnostics are operational results only. No persisted RecoveryCut/authority record is required.

### R13 — checkpoint does not prove SAVE/handoff success

Accepted.

Checkpoint existence never upgrades incomplete native durability closure into successful save or controlled handoff.

### R14 — no checkpoint fallback for defective current authority

Accepted.

Current authority defect causes scoped blocked/integrity handling. Checkpoint/history may provide repair evidence but cannot silently replace current gameplay authority.

### R15 — Step-5.8 carry-forward

Accepted.

Step 5.8 must close:

- concurrent live writer adoption/stabilization during cold recovery;
- live ref/epoch currentness/fencing;
- partial campaign/live transfer crash windows;
- source selection in closed-but-unabsorbed / abandoned / rollover states.

5.7 supplies only generic exact pin/current-source validation requirements.

### R16 — Step-5.11 carry-forward

Accepted.

Exact wording/evidence still required by Step-5.2 unresolved accepted execution is retention-protected while that dependency remains live. Transcript retention cannot delete it without replacement by sufficient typed state/evidence.

## 3. Checkpoint field resolution

Canonical Step 5.7 SHALL establish semantic disposition without freezing final wire schema:

| Current field | Resolution |
|---|---|
| `schema_version` | retain equivalent format/version identity |
| `id` | retain stable descriptor identity |
| `campaign_id` | retain association |
| `created_at` | allowed diagnostic metadata; no ordering authority |
| `valid_through_event_id` | retire as generic checkpoint/recovery completeness field |
| `expected_commit_sha` | retire; containing-commit self-reference is invalid design |
| `world_time` | not chronology authority; remove from minimum checkpoint contract |
| `state.current_state_path` | not authority; retain only if actual layout indirection needs it |
| active PC/thread/scene lists | optional non-exhaustive hints only |
| `recovery_notes` | diagnostic only |
| `engine` | optional provenance/compatibility observation only |
| `schema_data_version` | retain only as format/migration metadata if required |
| `MANIFEST.last_checkpoint_id` | optional campaign-domain descriptor pointer, not recovery frontier |

No new root-manifest/routing fingerprint fields are mandated before machine implementation proves their value.

## 4. Canonical recovery flow to preserve

```text
campaign selected
    -> pin current campaign authority H
    -> read bounded current identity/runtime/owning routes at H
    -> resolve + exact-pin current native authority sources
    -> enumerate current Step-5.2 roots from native typed routing/lifecycle
    -> hydrate required native owner + transitive correctness closure
    -> optionally consult/validate checkpoint evidence
    -> rebuild derived state
    -> validate routing/lifecycle/current-source basis
    -> validate interpretation/reference/integrity/RRC
    -> READY | RETRY | BLOCKED
```

Important:

```text
READY
    != permanent source currentness
    != mutation lease
    != permission bypass
```

The next mutation still uses its normal owning concurrency/authorization contract.

## 5. Canonical recovery/integrity separation

Recovery result stays operational:

```text
READY
RETRY / typed reason
BLOCKED / typed reason
```

Persisted canon integrity remains owned by existing semantics:

```text
CANON_OK
CANON_SUSPECT
CANON_CORRUPT
```

Examples:

- source moved -> `RETRY`, no corruption implied;
- runtime package unavailable -> `BLOCKED`, canon may remain OK;
- required current source missing -> `BLOCKED` + affected scope suspect;
- confirmed contradictory current authority -> `BLOCKED` + affected scope corrupt;
- malformed optional checkpoint -> checkpoint facility suspect, gameplay may still READY.

## 6. Historical maintenance boundary

Canonical Step 5.7 SHALL NOT promise guaranteed rewind from every checkpoint.

Historical checkpoint maintenance is conditional on exact retained native source/revision/interpretation dependencies still being resolvable and compatible.

Any operation that establishes a different current state after approved historical repair/rollback uses a normal forward publication. No force-ref rewind.

## 7. Machine-realization obligations

Deferred implementation work includes at least:

1. Step-5.2 typed partitioned recovery routing representation;
2. Procedure lifecycle/root-enrollment machine evidence;
3. checkpoint schema/template reduction;
4. narrow `last_checkpoint_id` semantics;
5. current-authority-first bootstrap order;
6. deterministic Python cold-recovery executor;
7. non-authoritative RecoveryResult type/reason vocabulary;
8. final currentness/root-routing validation;
9. bounded retry handling;
10. no-checkpoint recovery regression;
11. optional malformed/stale checkpoint non-blocking regression;
12. post-publication/lost-ACK cold recovery regressions;
13. duplicate discovery-path temporal/root deduplication;
14. authorization-change recovery tests;
15. maintenance reset/export semantics;
16. removal of tests/prose that require checkpoint at ordinary PLAY_READY/save absent independent reason.

These are implementation obligations, not reasons to duplicate state in checkpoint.

## 8. Later-slice obligations

### Step 5.8

Must define current live-source/fencing/adoption semantics strongly enough that 5.7 exact-pin/currentness recovery can classify active concurrent live recovery without guessing.

### Step 5.9

Owns chronology persistence; checkpoint world-time copies cannot fill that role.

### Step 5.11

Must preserve exact evidence while it remains an irreducible accepted recovery dependency.

### Step 5.13

Owns physical checkpoint/orphan retention and cleanup. Current recovery cannot depend on retaining obsolete optional checkpoints.

### Step 6

Owns final migration/runtime-package and RepositoryPort host/deployment realization, without weakening 5.7 recovery authority semantics.

## 9. Gate verdict

**PASS — READY FOR CANONICALIZATION.**

No unresolved owner-level decision remains for Step 5.7.

Canonical direction:

> **CURRENT-AUTHORITY-FIRST / CHECKPOINT-OPTIONAL NATIVE-ROUTED BOUNDED RECOVERY**