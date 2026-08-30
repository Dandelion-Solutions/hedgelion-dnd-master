# Step 5.13 — Garbage Collection / Orphan Cleanup — Resolution Gate

Status: **RESOLUTION GATE PASSED — READY FOR CANONICAL CONSOLIDATION**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Inputs:

- `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-task-brief.md`
- `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-research-draft.md`
- `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-analytical-challenge.md`
- `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-candidate-spec.md`
- `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-adversarial-review.md`

Candidate direction under resolution:

> **OWNER-GATED RETIREMENT / CLOSED BLOCKER CONTRACTS / COMPLETENESS-TYPED PROTECTION ROUTING / CURRENT-BASIS SAFE-RETIREMENT PROOF / REPLACEMENT-BEFORE-REMOVAL / OPTIONAL POST-AUTHORITY REF CLEANUP / HOST-MANAGED GIT OBJECT RECLAMATION**

---

# 1. Gate question

May Step 5.13 be canonicalized without a new owner decision and without weakening any canonical Step-3/4/5 correctness, retention, recovery, chronology, Story, disclosure or live-authority promise?

**YES.**

Adversarial review found 12 blockers/refinements. All are mechanically resolvable as stricter consequences of existing owner/runtime/version/concurrency laws.

No finding requires a new product promise, risk acceptance, authority transfer, history-rewrite policy or user-visible cleanup guarantee.

---

# 2. Resolution of adversarial findings

## R1 — cleanup-contract evolution / engine adoption

**Finding:** a newer engine can add a new consumer/blocker class while old targets still use an older cleanup contract.

**Resolution:** cleanup-contract interpretation is part of compatible runtime/catalog interpretation and migration.

Canonical consolidation SHALL require:

- one cleanup attempt pins the accepted cleanup-contract generation compatible with target and current campaign runtime;
- adoption that changes blocker vocabulary/reference survival/eligibility migrates affected cleanup/protection semantics before automatic cleanup under the new generation is enabled;
- legacy/incompatible targets remain retain-only until migrated;
- open execution pinned to prior accepted interpretation cannot be stranded by ambient newer cleanup semantics.

No generic runtime-wide GC generation is implied; generation is target/contract compatibility evidence.

**Status: RESOLVED.**

## R2 — Interaction/message linkage discharge

**Finding:** deleting a compact message while `runtime.interaction.raw_message_ref` still implies dereferenceability may break accepted-input/idempotency semantics.

**Resolution:** before envelope removal, every surviving Interaction/execution/history reference must be classified and sufficient accepted meaning/idempotency evidence must already live in its natural owner/survivor.

Legacy raw-message refs default to resolvable.

Opaque provenance is legal only after the consuming owner no longer needs target content/current dereferenceability.

**Status: RESOLVED.**

## R3 — protection-routing generation retirement

**Finding:** correctness-complete reverse routing could become immortal or circularly authorize its own deletion.

**Resolution:** routing generation lifecycle is governed by its own derivative owner/current-selector contract.

Old generation retires only after:

```text
compatible successor durable/current
+ current selector/basis moved
+ no active assessment may continue using old basis without revalidation
```

It never proves its own retirement through its own absence result.

**Status: RESOLVED.**

## R4 — ref-delete acknowledgement ambiguity

**Finding:** ref deletion can have accepted/rejected/indeterminate transport outcome.

**Resolution:** optional RepositoryPort ref cleanup uses targeted current-ref verification after ambiguity.

```text
ref absent
    -> cleanup achieved

ref present at exact expected old source
    -> revalidate eligibility; retry may be allowed

ref present at unexpected/different source
    -> do not delete; maintenance/integrity conflict
```

Authority was already ended before this operation, so ambiguity does not create gameplay ambiguity.

Epoch/ref authority identities are not reused.

**Status: RESOLVED.**

## R5 — semantic removal vs secure erasure

**Finding:** current-tree removal can be misunderstood as storage erasure despite append-only Git history.

**Resolution:** canonical terminology explicitly distinguishes semantic retention, current-tree availability and historical Git byte reachability.

Ordinary 5.13 provides no secure-erasure claim.

Any future secure-expungement/history-rewrite facility requires separate explicit owner/security/storage architecture.

**Status: RESOLVED.**

## R6 — Story migration/reprojection continuity

**Finding:** source deletion can make arbitrary future reprojection impossible.

**Resolution:** cleanup preserves enough source/enumeration semantics for **currently supported compatible coverage/migration promises**, not unlimited hypothetical future replay.

A future projection contract cannot assume deleted payload can be reconstructed. If it needs old content, an earlier retention promise/migration must protect it.

This is consistent with Step 5.10 generation semantics and Step 5.11 non-invention of lost exact text.

**Status: RESOLVED.**

## R7 — long-lived compact idempotency anchors

**Finding:** without a host-bounded retry horizon, compact accepted-invocation/result evidence may accumulate indefinitely.

**Resolution:** retain only minimum owner-required duplicate-suppression/result evidence; no arbitrary TTL.

Long-lived small anchors are permitted.

Step 6 must measure actual host retry identity/horizon feasibility and storage cost before proposing earlier expiry.

No product decision is required absent measured/material cost.

**Status: RESOLVED / MACHINE-PERFORMANCE DEBT.**

## R8 — verified-exact certification survivor proliferation

**Finding:** standalone digest anchors could become universal tombstones.

**Resolution:** prefer natural-owner/co-located verification evidence in retained Transcript state. Create no standalone anchor when no verified-exact promise survives.

Standalone narrow anchor is allowed only when a concrete retained exact-verification contract requires it and no natural owner can carry the minimum evidence.

**Status: RESOLVED.**

## R9 — cleanup versus bounded reader

**Finding:** cleanup can remove a current path while a support operation is reading it.

**Resolution:** bounded readers pin exact source revision/commit when they depend on a cleanup-eligible record. In-flight read does not create a durable GC lease/root.

Append-only source revision provides the read basis even if current tree later changes.

**Status: RESOLVED.**

## R10 — unclassified refs and epoch-name reuse

**Finding:** current Connector may leave old refs indefinitely; deterministic name reuse could cause ambiguity.

**Resolution:**

- live epoch/source authority generation identity is nonreused;
- branch existence never permits implicit adoption;
- unclassified noncurrent refs may remain as harmless clutter if bounded disposition cannot be proven;
- stronger orphan registry is YAGNI until measured accumulation demonstrates need.

**Status: RESOLVED / CAPABILITY-PERFORMANCE DEBT.**

## R11 — Story bulk generation cleanup with sparse survivors

**Finding:** whole-generation deletion can strand current cross-generation Story references/provenance.

**Resolution:** generation/epoch bulk retirement applies only to the subset proven closed under current surviving references and migration requirements.

Sparse survivors are retained/migrated individually.

Generation label never overrides Story reference closure.

**Status: RESOLVED.**

## R12 — potential future diagnostic usefulness

**Finding:** any deleted evidence might someday help forensic repair.

**Resolution:** potential usefulness alone is not universal retention authority.

Only explicitly admitted audit/repair/provenance contracts block cleanup.

Future support reports evidence as unavailable when lawfully removed; it never fabricates missing history.

**Status: RESOLVED.**

---

# 3. Final architecture direction after resolution

Canonical consolidation SHALL use:

> **OWNER-GATED RETIREMENT / CLOSED BLOCKER CONTRACTS / COMPLETENESS-TYPED PROTECTION ROUTING / PINNED CURRENT-BASIS SAFE-RETIREMENT PROOF / SURVIVOR-BEFORE-REMOVAL / OPTIONAL POST-AUTHORITY REF CLEANUP / SEMANTIC RETENTION SEPARATE FROM GIT-HISTORY REACHABILITY / HOST-MANAGED GIT OBJECT RECLAMATION**

The extra wording is intentional:

- `PINNED CURRENT-BASIS` emphasizes negative proof currentness;
- `SURVIVOR-BEFORE-REMOVAL` generalizes compact replacement/promotion/migration;
- explicit Git-history separation preserves Step-5.11 product semantics and prevents false secure-delete expectations.

---

# 4. Canonical common proof obligations

For target representation A, automatic current-namespace retirement requires all:

```text
P1 CLEANUP CONTRACT COMPATIBLE
    target kind/generation understood under current accepted runtime

P2 NATIVE TERMINALITY / REPLACEMENT
    owner responsibility ended or moved lawfully

P3 BLOCKER VOCABULARY CLOSED
    every admitted blocker class known for this contract generation

P4 BLOCKER ABSENCE / DISCHARGE CURRENT
    negative evidence valid under pinned current source basis

P5 CROSS-SOURCE BLOCKER CREATION COVERED
    self-contained consumer, protection registration or source fence

P6 SURVIVOR CLOSURE COMPLETE
    idempotency, provenance, chronology, cursor, exact certification,
    reference semantics and other promised evidence preserved

P7 REFERENCE SURVIVAL VALID
    every incoming survivor ref remains resolvable/opaque/survivor-backed
    according to its owner contract

P8 RESULTING CURRENT STATE VALID
    no required dangling owner/routing/integrity dependency

P9 PUBLICATION CURRENTNESS HOLDS
    relevant movement causes revalidation/retry
```

Any failed/unknown obligation => retain.

---

# 5. Canonical reference semantics requirement

The final spec must require a machine-level semantic distinction equivalent to:

```text
REQUIRES_CURRENT_TARGET
OPAQUE_STABLE_PROVENANCE
SURVIVOR_BACKED
```

This is necessary to reconcile stable historical IDs with lawful record retirement.

It is not a generic tombstone system.

Legacy/unknown refs default conservative.

---

# 6. Canonical protection-routing requirement

Final spec must distinguish:

```text
best-effort candidate/discovery index
vs
correctness-complete typed protection routing
```

Only the second may participate in negative proof, and only after its completeness/currentness contract is validated.

The consuming owner remains authority.

---

# 7. Canonical Git boundary

The final spec must explicitly state:

```text
remove from current campaign tree
    !=
remove from campaign Git history
    !=
server object reclamation
```

Old Git history is not normal retained semantic evidence after lawful Step-5.11 compaction.

This prevents hidden tape-recorder behavior.

---

# 8. Canonical live-ref boundary

Final spec must preserve:

```text
ACTIVE -> never delete
CLOSED_UNABSORBED -> never delete
ABSORBED/NONAUTHORITATIVE -> optional delete after dependency proof
PREPARED ORPHAN -> optional delete after bounded nonauthority proof
UNCLASSIFIED NONCURRENT -> retain/report
```

Current lack of Connector ref-delete capability is a deployment capability gap only.

Ref cleanup is never required for gameplay readiness.

---

# 9. Canonical execution-history boundary

Final spec must preserve minimum idempotency/result/causal evidence independently of detailed execution payload.

No time-based expiry is introduced.

Step 6/implementation measures whether stable host invocation identities allow further bounded compaction.

---

# 10. No new owner decision

No unresolved decision belongs to the human architect at this gate.

Existing owner decisions already establish:

- semantic continuity over universal verbatim archive;
- no force/history rewrite ordinary runtime;
- native owner authority;
- bounded recovery;
- no global frontier/refcount;
- Story nonauthority;
- sparse durable disclosure;
- no background-delivery subsystem.

5.13 simply derives safe cleanup mechanics from them.

---

# 11. Canonicalization checklist

Before closing Step 5.13, canonical spec must include:

- [x] five-layer cleanup distinction;
- [x] no universal GC authority/refcount/frontier;
- [x] cleanup-contract compatibility/generation;
- [x] pinned safe-retirement proof obligations;
- [x] candidate-discovery vs protection-routing distinction;
- [x] cross-source blocker creation handling;
- [x] survivor-before-removal ordering;
- [x] reference-survival semantics;
- [x] execution/idempotency retention split;
- [x] checkpoint cleanup;
- [x] message-envelope cleanup;
- [x] Story cursor/exact-certification continuity;
- [x] chronology delegation to Step 5.9;
- [x] disclosure non-GC baseline;
- [x] live-ref cleanup classes;
- [x] optional/capability-gated ref deletion + ambiguity;
- [x] no prepared-object GC registry;
- [x] Git semantic-retention vs history-reachability distinction;
- [x] no secure-erasure promise;
- [x] no generic world entity deletion;
- [x] no background/job queue;
- [x] conservative legacy migration;
- [x] bounded performance contract;
- [x] machine-realization debt;
- [x] Step-5.14 adversarial carry-forward.

---

# 12. Gate verdict

**RESOLUTION GATE PASSED.**

Step 5.13 is ready for canonical consolidation.

No architecture blocker or owner-level decision remains at this gate.
