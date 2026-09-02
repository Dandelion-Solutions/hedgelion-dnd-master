# R2.7 WP-12 — Senior Recovery — Live CAS / Local HOT Establishment Boundary

Status: **SENIOR RECOVERY COMPLETE — MANDATORY SENIOR RE-AUDIT PENDING**

Date: 2026-09-02

## 1. Scope

This record resolves one BLOCKING canonical-consistency defect found by the mandatory Senior audit after WP-12 Step 8.

It is a narrow post-Step-8 recovery. It does not reopen WP-12 research, Alternative A, native-owner topology, Step-3 execution architecture, Step-5.8 live authority, Steps 1–7, WP-13, or implementation planning.

The affected current owner is:

- `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md`

Historical Step-6 and Step-7 records are retained unchanged. They did not identify this exact cross-law inconsistency and must not be rewritten as though they had.

## 2. Senior finding

### SR01 — LAW WP12-8 can be read as making live establishment SQLite-commit-bound

Severity: **BLOCKING**

The final WP-12 canonical specification states in LAW WP12-8 that one local SQLite transaction implements one accepted Step-3 ExecutionSegment/native local atomic edge and may atomically advance implicated owner/runtime/evidence state.

That sentence is valid for native/local atomic edges whose owning authority/durability contract permits establishment in local HOT, but it was insufficiently qualified for live-claimed mutable consequences.

The current accepted authorities already require a different establishment edge for live-owned state:

- WP-12 Step-3 Decision Brief requirement 10 explicitly requires live shared establishment to be exact-source-CAS-bound rather than local-SQLite-commit-bound.
- Step-3 `ExecutionSegment` remains the embedded deterministic atomic execution edge, but later Step-5 durability/shared-state law controls how an authoritative consequence becomes established in its native partition.
- Step-5.8 LAW 5.8-18/19 makes live correctness exact-source-CAS serialized/fenced.
- Step-5.8 LAW 5.8-29 makes live atomicity one complete native durability edge rather than one user action.
- Step-5.8 shared mutation protocol freezes one native atomic transition and crosses the shared write-before-reveal boundary only after confirmed compatible exact-source CAS publication.
- Existing WP12-9 prohibits a SQLite transaction from spanning live CAS.
- Existing WP12-22 keeps pre-CAS live results prospective/non-current.
- Existing WP12-23 makes the post-CAS SQLite transaction adoption of already accepted live authority and explicitly rejects SQLite+live distributed transaction semantics.

Without a qualification in WP12-8 itself, those laws are individually compatible but the canonical text admits an incorrect implementation reading in which the local SQLite transaction is treated as the authoritative gameplay establishment boundary for a live-claimed ExecutionSegment.

Root cause: **Step-8 synthesis/canonicalization precision defect**, not a defect in Alternative A, Step-3 execution ownership, or Step-5.8 authority.

## 3. Resolution

LAW WP12-8 is repaired to distinguish two cases.

### 3.1 Native/local HOT-establishable edge

When the owning native authority/durability contract permits establishment in local HOT, one local SQLite transaction is the local atomic commit/establishment boundary for the accepted Step-3 ExecutionSegment or other already-defined native local atomic edge.

That transaction may atomically advance the implicated current local owners/runtime/evidence/dirty state as allowed by their native contracts.

### 3.2 Live-claimed mutable consequence

When an implicated mutable consequence is owned by the selected live partition, the deterministic ExecutionSegment remains the native execution edge, but **authoritative shared establishment is the exact-source live CAS durability edge**.

Therefore:

```text
pre-CAS deterministic result
    = prospective / non-current

exact-source live CAS ACCEPTED
    = authoritative shared establishment

post-CAS SQLite transaction
    = local adoption of already accepted live authority
```

The local SQLite transaction is not a substitute fence, is not a distributed half of the CAS, and does not make the prospective result current before CAS.

A post-CAS adoption failure cannot roll back the already accepted live gameplay transition. Recovery/currentness reloads the accepted live source without mechanics/RNG replay.

## 4. Scoped cross-law review

Required review surface:

```text
WP12-7/8/9
<-> WP12-22/23/24
<-> Step-3 ExecutionSegment
<-> Step-5.8 native durability edge / exact-source CAS
```

### WP12-7 -> WP12-8

WP12-7 is explicitly conditional: local owner state may establish in HOT only **where the existing native owner/durability contract permits local establishment before publication**. The repaired WP12-8 now carries the same qualifier instead of appearing to universalize local establishment to every ExecutionSegment.

Result: **CONSISTENT**.

### WP12-8 -> WP12-9

The repaired WP12-8 does not span SQLite over live CAS. Local HOT-establishable edges use one SQLite transaction locally; live-owned edges publish via external exact-source CAS and only then run a separate local adoption transaction.

Result: **CONSISTENT — NO SQLITE+LIVE DISTRIBUTED TRANSACTION**.

### WP12-8 -> WP12-22

For live-claimed mutable consequences, pre-CAS deterministic state remains prospective/non-current and cannot replace the accepted current owner row.

Result: **CONSISTENT — NO PRE-CAS CURRENT VISIBILITY**.

### WP12-8 -> WP12-23

After successful exact-source CAS, SQLite only adopts the accepted live state. Adoption failure reloads the accepted live authority and does not undo/replay accepted mechanics.

Result: **CONSISTENT — POST-CAS ADOPTION IS NOT AUTHORITATIVE GAMEPLAY COMMIT**.

### WP12-8 -> WP12-24

Current local live-backed rows remain subordinate to selected claim routing and exact live source revision. The repaired boundary does not create campaign/local fallback current truth.

Result: **CONSISTENT**.

### WP12-8 -> Step-3 ExecutionSegment

Step-3 still owns the deterministic embedded execution edge and its atomic implicated state/runtime/evidence semantics. WP-12 does not redefine that owner. The repair only states that the physical establishment substrate follows the native authority/durability contract: local SQLite where local establishment is permitted, exact-source CAS where live ownership requires it.

Result: **NO STEP-3 REOPENING; EXECUTION EDGE PRESERVED**.

### WP12-8 -> Step-5.8

Step-5.8 remains the controlling live ownership/durability contract. Exact-source CAS is the fence and authoritative native durability edge for live-owned mutable state; rejected prospective IDs/consequences remain noncanonical; confirmed accepted live state survives local adoption failure.

Result: **CONSISTENT — STEP-5.8 AUTHORITY PRESERVED**.

Scoped review verdict:

```text
UNRESOLVED BLOCKING:     0
UNRESOLVED SIGNIFICANT:  0
NEW HUMAN DECISION:      NO
ARCHITECTURE REOPENED:   NO
```

## 5. Verification-obligation repair

The WP-12 implementation-verification obligation formerly stating, without qualification, that one ExecutionSegment commits all implicated local owner/runtime/evidence/dirty state atomically is repaired to mirror the same authority split:

- for native/local HOT-establishable edges, one local SQLite transaction commits the implicated local owner/runtime/evidence/dirty state atomically or none;
- for live-claimed mutable consequences, pre-CAS state remains prospective/non-current, exact-source live CAS is the authoritative establishment edge, and the post-CAS SQLite transaction only atomically adopts the already accepted live state locally.

Existing obligations that prohibit SQLite transactions across external I/O, prohibit pre-CAS current/shared state, and require recovery from accepted live authority after post-CAS adoption failure remain in force.

## 6. Forward-consistency route

The existing WP-26 storage-document consistency item is broadened, without changing WP-12 semantics:

- `DEV/ARCHITECTURE/BRANCH_MODEL.md` contains stale storage-v2 marker/baseline wording;
- `DEV/ARCHITECTURE/ACCESS_CONTROL.md` contains the stale label `Storage v2 baseline maintenance...`.

Both are **MINOR documentation consistency** against the current storage machine/owner contract. Neither file is edited in this recovery. WP-26 owns their later reconciliation while preserving the settled rule that storage baseline/provenance does not override existing-campaign runtime authority.

## 7. Propagation

- Step-6 whole-project adversarial review: **RETAIN UNCHANGED AS HISTORICAL FINDING EVIDENCE**.
- Step-7 resolution/propagation record: **RETAIN UNCHANGED AS HISTORICAL RESOLUTION EVIDENCE**.
- Step-3 Decision Brief: **RETAIN UNCHANGED**; its requirement 10 already states the correct live-CAS boundary.
- final WP-12 canonical specification: **REPAIR WP12-8 + matching verification obligation + WP-26 route/status wording**.
- Step-8 canonicalization: **SYNC CURRENT POST-AUDIT STATE AND RECORD SR01 RECOVERY**.
- `DEV/CURRENT_PROGRESS.md`: **SYNC TO SENIOR RECOVERY COMPLETE / RE-AUDIT PENDING**.
- task-local R2.7 cursor: **SYNC TO SAME GATE AND BROADEN WP-26 ROUTE**.
- runtime/schema/catalog/test implementation: **NO CHANGE**.

## 8. Gate

WP-12 Steps 1–8 plus this Senior recovery are complete.

Required next unit:

> **Mandatory Senior re-audit of the repaired WP-12 package.**

Until explicit Senior GO after that re-audit:

- WP-13 remains blocked;
- implementation planning remains blocked;
- no runtime/schema/catalog/test/topology implementation begins.

Human decision required: **NO**.
