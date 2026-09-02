# R2.7 WP-14 — Recovery / Checkpoints / Session / Repair — Step 6 Whole-Project Adversarial Review

Status: **STEP 6 COMPLETE — 3 BLOCKING + 5 SIGNIFICANT FINDINGS / ALL MECHANICALLY RESOLVABLE**

Date: 2026-09-03

Candidate under review:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-5-candidate-spec.md`

Source graph:

- repaired Step-1 Source Manifest + SR14-01..03;
- Step-2 evidence/manifest expansion;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-source-manifest-step-6-expansion.md`.

---

## 1. Review method

The candidate was attacked across:

- Step-3 accepted execution/idempotency/RNG/Continuation;
- Step-4 truth/knowledge/human-disclosure ownership;
- Steps 5.1–5.9 and 5.11–5.14 currentness/recovery/history/GC/disclosure seams;
- R2.6 ambient-host and fixed Connector constraints;
- WP-10 record-family allocation;
- WP-11 physical identity/routes/indexes;
- WP-12 HOT/SQLite/local-vs-live establishment;
- WP-13 durability/SAVE/publication/currentness;
- current CORE recovery/session/storage/persistence/live/integrity consumers;
- checkpoint/session/MANIFEST schemas/templates/scaffold;
- maintenance command proposal and maintenance-audit allocation;
- current regression surfaces;
- downstream WP-16/WP-19/WP-20/WP-22/WP-24/WP-26 boundaries.

The reopen threshold remained contradiction/new unsatisfied consumer/material upstream insufficiency. None fired.

---

# 2. Findings

## F01 — BLOCKING — Historical current promotion lacks an explicit fresh current-basis reconciliation/freeze before authoritative write

### Attack

LAW WP14-32 says a historical repair intended to become current uses normal forward publication/currentness rules. However, the candidate does not explicitly require the reconstructed historical proposal to be reconciled against a **fresh current promotion basis** at the time promotion begins.

A long maintenance reconstruction could start from old checkpoint K while current campaign/live owners legitimately advance. Blindly serializing the reconstructed old composition as a forward commit could overwrite newer current owner changes even without force-push.

This would preserve Git monotonicity while violating semantic currentness.

### Required repair

Before any durable promotion:

1. create a fresh promotion attempt distinct from the historical reconstruction attempt;
2. resolve/pin current owning routes and every affected current native authority source;
3. verify current application authorization/principal;
4. define the explicit repair/rollback footprint and transform historical material into an owner-native replacement proposal **against that current basis**;
5. freeze the exact promotion payload/basis before remote writes;
6. publish each affected owner through its normal exact-currentness/CAS/non-force edge;
7. current movement/rejection => bounded re-evaluation/retry or typed conflict, never blind overwrite.

Historical local state is evidence/proposal input, not the current write basis.

**Severity:** BLOCKING.

---

## F02 — BLOCKING — Multi-domain historical promotion can falsely imply all-or-nothing repair

### Attack

A historical repair may touch campaign-owned state and one or more independently durable/live/native domains. Candidate LAW WP14-32 names owner-native publication, but does not explicitly state the consequence when one domain accepts and another rejects/returns indeterminate.

Accepted WP-13 architecture forbids a cross-domain distributed transaction and treats partial native-domain success as real. If WP-14 reported a global rollback failure and tried to undo an already accepted edge, or reported success while the current composition is incompatible, it would violate WP-13 and potentially replay/overwrite authority.

### Required repair

Historical current promotion is a composition of native durability/currentness edges:

- no cross-domain distributed transaction/global rollback;
- every confirmed accepted native transition remains real;
- rejected/indeterminate edges follow their own currentness/ambiguity proof;
- after any partial outcome, recover/compose **actual current authorities**;
- if current RRC is not compatible for an affected operation scope, keep that scope `BLOCKED`/maintenance-incomplete while forward repair continues or operator intervention is required;
- never replay mechanics/RNG/accepted execution to “make the rollback atomic”.

Maintenance outcome must truthfully represent partial/indeterminate promotion where applicable.

**Severity:** BLOCKING.

---

## F03 — BLOCKING — Historical promotion can regress `runtime.id_allocator` and reuse published IDs

### Attack

The candidate preserves accepted execution IDs but does not explicitly constrain historical restoration of the campaign allocator itself.

Step-5.1 states:

```text
published IDs -> never changed or reused
```

If historical reconstruction restores an earlier `runtime.id_allocator.last_allocated`, later creation could reuse IDs from post-checkpoint history even if the corresponding current records were intentionally removed by repair. That would repurpose durable identity and contaminate history/provenance.

### Required repair

- historical allocator state may be inspected for diagnostics only;
- current promotion SHALL NOT regress the current allocator's published-allocation/collision bookkeeping;
- every previously published campaign-scoped ID remains permanently non-reusable even when the repaired current world no longer contains that record;
- new repair/audit/replacement records allocate under the **current allocator owner** and normal publication/conflict rules;
- owner-valid reconciliation may advance/retain allocator state, never restore it below published allocation history.

No second allocation authority is introduced.

**Severity:** BLOCKING.

---

## F04 — SIGNIFICANT — Historical repair can silently rewind durable human disclosure or fictional knowledge

### Attack

The candidate treats historical world/runtime state broadly but does not explicitly prevent a repair from copying older `world.knowledge` / `runtime.disclosure` state into the replacement composition.

Step 4 separates current fictional knowledge from human-player exposure; Step-5.12/5.13 make `runtime.disclosure` durable exposure semantics and state that host/history rewind does not make exposure disappear. A player cannot become “unexposed” merely because world state is repaired backward.

### Required repair

- historical world repair does not implicitly rewind `runtime.disclosure` or current `world.knowledge`;
- if a repair intentionally affects one of those owner domains, use that owner’s explicit correction/transition/access semantics;
- prior real human exposure cannot be erased by checkpoint/world rollback;
- maintenance diagnostics must not intentionally expose Narrator-ineligible campaign material through a player-visible surface.

**Severity:** SIGNIFICANT.

---

## F05 — SIGNIFICANT — Maintenance-isolated historical state needs a stronger no-gameplay/no-emission fence

### Attack

LAW WP14-31 prohibits ordinary gameplay mutation from a maintenance-isolated reconstructed store, but does not explicitly prohibit:

- Narrator/Context assembly from it;
- player-visible gameplay emission;
- turn/Interaction/Resolution allocation;
- fictional chronology advancement;
- RNG/id allocation performed as if it were current gameplay.

A read-only narrative response from stale historical local state could still disclose false/current-ineligible information and create later durable disclosure/message consequences.

### Required repair

Until lawful current promotion succeeds, a maintenance-isolated historical store may feed only explicitly authorized maintenance diagnostics/validation.

It SHALL NOT drive ordinary gameplay context, player-visible Narrator emission, turn/Interaction/Action/Resolution creation, current chronology progression, ordinary RNG consumption or current ID allocation.

Diagnostic output still obeys support access/disclosure constraints.

**Severity:** SIGNIFICANT.

---

## F06 — SIGNIFICANT — “Latest checkpoint” commands need an explicit no-enumeration/no-guess fallback when pointer is null/dangling

### Attack

The candidate resolves `MANIFEST.last_checkpoint_id`, but does not explicitly forbid a convenience implementation from handling null/dangling pointer by scanning `CHECKPOINTS`, taking highest `rev-*`, newest timestamp, Git order or nearest available descriptor.

That would recreate checkpoint selection authority the pointer contract intentionally owns and could select prepared/stale/unselected evidence.

### Required repair

For `HDM_EXPORT_CHECKPOINT_LOG` and `HDM_RESET_LAST_CHECKPOINT`:

- `last_checkpoint_id = null` => typed no-selected-checkpoint/unavailable result;
- dangling/malformed selected target => checkpoint-facility suspect/unavailable according to operation;
- do not infer “latest” by directory enumeration, checkpoint ID magnitude, timestamp or Git object order;
- a future command that accepts an explicit checkpoint ID is a separately explicit historical-maintenance address, not fallback “latest” selection.

**Severity:** SIGNIFICANT.

---

## F07 — SIGNIFICANT — Durable `runtime.maintenance_audit` writes need explicit current-authority publication and allocator rules

### Attack

Candidate LAW WP14-35/36 classifies audit correctly but could still be implemented by serializing audit from the maintenance-isolated historical store or allocating `audit-*` from historical allocator state.

Because `runtime.maintenance_audit` is a durable campaign record family, publishing it is itself a current campaign-domain mutation subject to WP-13 and Step-5.1 allocator rules.

### Required repair

- durable audit creation uses current campaign authority and current allocator owner, never historical local allocator/state as write authority;
- audit record creation + allocator mutation follow their owning local/publication closure;
- remote publication uses frozen current-basis WP-13/non-force semantics;
- conflict/retry must preserve one semantic maintenance operation identity and must not duplicate the audit meaning;
- audit publication success/failure/indeterminate is reported separately from gameplay-repair establishment and local reconstruction outcome.

No generic audit queue/journal is introduced.

**Severity:** SIGNIFICANT.

---

## F08 — SIGNIFICANT — Historical retention/current cleanup interaction needs exact pinned-reader semantics

### Attack

Candidate correctly says rewind is not guaranteed, but does not explicitly compose historical maintenance with Step-5.13 cleanup concurrency.

A selected checkpoint may be removed from a later current campaign tree after coherent pointer clear/replace, while a maintenance reader already pinned older H. Conversely, old Git bytes may remain physically reachable after semantic compaction but no longer be admitted as ordinary retained gameplay memory.

### Required repair

- maintenance/export reader that resolved pointer/descriptor at exact campaign revision H reads required descriptor/evidence against that exact pinned basis; later current cleanup does not retroactively invalidate the already pinned historical read;
- no durable reader lease is required;
- if required dependencies were already semantically retired/not protected before the attempt, mere old Git byte reachability does not automatically restore ordinary semantic evidence authority;
- bounded authorized repair/support may inspect transport history only under its maintenance evidence contract;
- current recovery never depends on old checkpoint retention.

**Severity:** SIGNIFICANT.

---

# 3. Explicit non-findings

The adversarial review found **no** need to:

- reopen current-authority-first recovery;
- make checkpoint mandatory;
- create a RecoveryCut/global recovery frontier;
- create a session lease;
- promote SQLite/local freshness;
- trust ambient chat/model memory;
- permit campaign fallback over current live authority;
- replay/reroll accepted execution;
- reopen fixed runtime Connector transport selection;
- introduce alternate Git transport fallback;
- promise guaranteed historical rewind;
- force-push/ref-rewind history;
- start WP-15/WP-16 implementation;
- build a generic repair/audit queue.

---

# 4. Downstream impact review

Required final-canonical/downstream routes after resolution:

- WP-16 must preserve current live owner/source semantics used by WP-14 and supply final physical live fencing/CAS machine;
- WP-19/WP-20 must integrate repaired checkpoint/session/MANIFEST/bootstrap shape without making checkpoint mandatory;
- WP-22 must cover current recovery, stale/missing/malformed checkpoint, live no-fallback, accepted-execution no-replay, SQLite survivor proof, historical reset unavailability/isolation/promotion, allocator non-regression, partial multi-domain repair, disclosure preservation and fixed-Connector failures;
- WP-24 may measure bounded recovery/maintenance reads before optimization;
- WP-26 keeps separately routed documentation consistency debt only.

---

# 5. Finding counts and gate

```text
F01 BLOCKING     fresh current-basis reconciliation/freeze for historical promotion
F02 BLOCKING     multi-domain partial historical promotion semantics
F03 BLOCKING     historical allocator regression / published ID reuse
F04 SIGNIFICANT  knowledge/disclosure rewind protection
F05 SIGNIFICANT  maintenance-isolated no-gameplay/no-emission fence
F06 SIGNIFICANT  no guessed latest-checkpoint fallback
F07 SIGNIFICANT  maintenance-audit current publication/allocator rules
F08 SIGNIFICANT  retention/GC pinned-reader and semantic-history boundary
```

Counts:

```text
STEP_6_BLOCKING:       3
STEP_6_SIGNIFICANT:    5
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
```

All eight findings are mechanically resolvable from already accepted architecture. Step 7 is authorized to incorporate the binding repairs without human escalation.