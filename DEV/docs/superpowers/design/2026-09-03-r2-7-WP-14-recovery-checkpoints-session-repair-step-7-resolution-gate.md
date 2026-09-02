# R2.7 WP-14 — Recovery / Checkpoints / Session / Repair — Step 7 Resolution Gate

Status: **STEP 7 COMPLETE — ALL BLOCKING/SIGNIFICANT FINDINGS RESOLVED**

Date: 2026-09-03

Reviewed Step-6 critic:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-6-whole-project-adversarial-review.md`

This resolution gate records binding amendments to the Step-5 candidate. Where this file is more precise than the Step-5 candidate, this resolution controls Step-8 canonicalization. It does not alter closed upstream semantics.

---

# 1. F01 resolution — fresh current-basis reconciliation before historical promotion

Finding: **BLOCKING**

Disposition: **CLOSED**

Binding amendment:

> Historical reconstruction never supplies the current write basis. Any historical repair intended to become current starts a distinct promotion attempt that resolves and exact-pins the fresh current owning basis for every affected native authority, reconciles the requested historical replacement against that basis, freezes the promotion payload/currentness/authorization footprint, and writes only through each owner's normal currentness/CAS/non-force edge.

Required sequence:

1. finish historical evidence reconstruction in maintenance isolation;
2. start a new promotion attempt;
3. resolve current owning routes and exact current source revisions for every affected scope;
4. resolve current application authorization/principal/delegation required by the affected owners;
5. define the explicit repair footprint and produce owner-native replacement state against the fresh current basis;
6. freeze the exact promotion payload, reads/dependencies, currentness basis and authorization basis before remote mutation;
7. publish through the affected owner-native WP-13/Step-5.6/Step-5.8 edge as applicable;
8. movement/rejection/ambiguity triggers bounded owner-specific re-evaluation, retry or typed conflict/blocked outcome.

Historical local state is evidence/proposal input only. A forward Git commit based on stale semantics is not sufficient merely because Git history remains monotonic.

---

# 2. F02 resolution — partial multi-domain promotion remains real

Finding: **BLOCKING**

Disposition: **CLOSED**

Binding amendment:

> Historical current promotion is a composition of native durability/currentness edges. HDM provides no cross-domain distributed transaction, no global rollback and no fiction that independently accepted edges can be undone locally.

Consequences:

- every confirmed accepted native transition remains real;
- every rejected or indeterminate edge follows its own currentness/ambiguity protocol;
- after any partial outcome, recovery recomposes the actual current authorities from native current routes;
- if the resulting affected composition cannot prove compatible RRC, dependent operation scopes remain `BLOCKED` / maintenance-incomplete until lawful forward repair/reconciliation completes;
- unrelated independent scopes remain governed by their own dependency closure;
- no already accepted gameplay/execution/RNG/ID consequence is replayed, rerolled or semantically re-executed to imitate all-or-nothing rollback;
- maintenance result/audit must distinguish complete, partial, blocked and indeterminate promotion outcomes truthfully.

This directly preserves WP-13 partial-native-domain establishment semantics.

---

# 3. F03 resolution — allocator monotonicity and permanent published-ID non-reuse

Finding: **BLOCKING**

Disposition: **CLOSED**

Binding amendment:

> Historical reconstruction may inspect old `runtime.id_allocator` state as evidence, but current promotion never restores the allocator below current published allocation/collision history and never makes a previously published campaign-scoped identity reusable.

Consequences:

- current `runtime.id_allocator` remains the sole campaign-scoped sequential allocation owner;
- previously published IDs remain never-reused even when repaired current world/runtime records are removed or replaced;
- new repair/replacement/audit records allocate through the current allocator owner and current publication/conflict rules;
- reconciliation may retain or advance current allocator state; it may not regress published-allocation history;
- accepted historical execution identities are retained as their existing identities, not reallocated;
- no checkpoint/session/historical store becomes an allocator authority.

---

# 4. F04 resolution — historical repair does not silently rewind disclosure/knowledge

Finding: **SIGNIFICANT**

Disposition: **CLOSED**

Binding amendment:

> Historical world/runtime repair does not implicitly copy older `runtime.disclosure` or `world.knowledge` state into the current replacement composition.

Consequences:

- prior real human exposure is not erased by checkpoint/world rollback or host/history rewind;
- current fictional knowledge remains with its Step-4 owner and may change only through that owner's explicit correction/transition semantics;
- if a maintenance operation explicitly targets disclosure/knowledge, it must name that owner scope and satisfy its authorization/evidence/correction contract;
- historical gameplay repair therefore treats these domains as independently reconciled current owners unless explicitly included by an admitted owner-native repair contract;
- support/maintenance diagnostics must respect recipient/access boundaries and cannot use repair inspection as a side channel for player-ineligible material.

---

# 5. F05 resolution — maintenance-isolated historical state cannot drive gameplay or emission

Finding: **SIGNIFICANT**

Disposition: **CLOSED**

Binding amendment:

Until lawful current promotion succeeds, a historical reconstructed store is **maintenance-isolated, non-current and non-playable**.

It may feed only explicitly authorized maintenance diagnostics/validation and SHALL NOT drive:

- ordinary gameplay Context Assembly;
- Narrator/player-visible gameplay emission;
- ordinary Interaction/turn/Action/RuntimeCommand/Resolution/Procedure creation;
- current fictional chronology progression;
- ordinary RNG consumption;
- current campaign-scoped ID allocation;
- current `runtime.disclosure` establishment;
- ordinary SAVE/HARD success claims;
- new live authority opening/claiming.

Diagnostic output itself remains access/disclosure constrained. The historical store becomes gameplay-eligible only after accepted owner-native forward promotion and subsequent ordinary current recovery/adoption proves the new current RRC.

---

# 6. F06 resolution — no guessed “latest checkpoint” fallback

Finding: **SIGNIFICANT**

Disposition: **CLOSED**

Binding amendment:

For operations whose contract says “last checkpoint”, `MANIFEST.last_checkpoint_id` is the only selection pointer.

```text
last_checkpoint_id = null
    -> typed NO_SELECTED_CHECKPOINT / MAINTENANCE_UNAVAILABLE

dangling or malformed selected target
    -> checkpoint-facility suspect/unavailable for the dependent operation

valid selected target
    -> resolve exactly from the pinned campaign basis
```

Forbidden fallback selectors include:

- directory enumeration;
- highest `rev-*` / ID magnitude;
- checkpoint timestamp;
- Git commit/object ordering;
- “nearest” surviving checkpoint;
- session/cached HEAD;
- checkpoint guessed from local SQLite.

A future explicitly addressed command that accepts a checkpoint ID is a different historical-maintenance operation, not fallback semantics for “last”.

---

# 7. F07 resolution — `runtime.maintenance_audit` writes use current authority

Finding: **SIGNIFICANT**

Disposition: **CLOSED**

Binding amendment:

> Durable `runtime.maintenance_audit` creation is itself a current campaign-domain mutation. It uses current campaign authority, current `runtime.id_allocator`, current authorization/currentness and normal WP-13 publication semantics; historical maintenance state never supplies its write authority.

Consequences:

- stable maintenance operation identity is established independently from a historical store's old allocator state;
- audit record creation plus required current allocator mutation join their owner-valid local/publication closure;
- remote publication uses one frozen current-basis publication attempt and non-force ref semantics;
- publication conflict/retry preserves one semantic maintenance operation identity and does not create duplicate audit meaning;
- audit publication outcome is distinct from local reconstruction outcome and gameplay-repair establishment;
- failed/indeterminate audit publication cannot roll back an already accepted gameplay repair;
- successful audit publication cannot establish gameplay authority or make an otherwise failed repair successful.

No generic repair/audit journal or queue is introduced.

---

# 8. F08 resolution — exact pinned historical readers and retention boundary

Finding: **SIGNIFICANT**

Disposition: **CLOSED**

Binding amendment:

> A maintenance/export reader that resolves a checkpoint/descriptor/evidence target from exact campaign revision H reads the required evidence against that exact pinned basis. Later current-tree cleanup does not retroactively invalidate the already pinned historical read, and no durable reader lease is required.

Further constraints:

- if required historical dependencies were already semantically retired or never protected before the attempt, residual Git bytes do not automatically regain ordinary semantic evidence authority;
- bounded authorized repair/support may inspect retained transport history only under its explicit maintenance evidence contract;
- Step-5.13 current-tree/ref cleanup may proceed under its owner rules after current selection/protection changes; new maintenance attempts must resolve their own currently available evidence;
- current recovery correctness never depends on old checkpoint retention;
- explicit historical maintenance truthfully returns unavailable when the required retained native composition/evidence no longer exists under the admitted maintenance contract.

---

# 9. Cross-finding consistency review

| Cross-check | Result |
|---|---|
| historical reconstruction vs fresh promotion basis | CONSISTENT — evidence proposal and current write basis remain distinct |
| fresh promotion vs WP-13 frozen attempts | CONSISTENT — promotion freezes current basis/footprint before remote mutation |
| multi-domain repair vs no distributed transaction | CONSISTENT — native accepted edges remain real; final RRC is recomposed |
| allocator preservation vs historical rollback | CONSISTENT — current allocator monotonicity/history is not a world-state rewind surface |
| disclosure/knowledge preservation vs Step 4 / Step 5.12 | CONSISTENT — exposure and fictional knowledge retain independent owners |
| maintenance isolation vs Narrator/Interaction semantics | CONSISTENT — non-current evidence cannot create new gameplay consequences |
| last-checkpoint pointer vs optional checkpoint | CONSISTENT — nullable narrow pointer is locator only, not recovery authority |
| maintenance audit vs authority | CONSISTENT — audit records operation evidence but does not establish repair/currentness |
| pinned historical reader vs Step-5.13 cleanup | CONSISTENT — exact historical read basis does not create a durable GC lease |
| live-owned scope vs historical/current campaign fallback | CONSISTENT — live source/revision evidence remains mandatory when that scope is/was live-owned |
| accepted execution/RNG/Continuation vs repair | CONSISTENT — no replay/reroll/reallocation is introduced |
| fixed R2.6 Connector transport | CONSISTENT — no alternate runtime transport/fallback is introduced |

No finding requires upstream reopening or a new product/authority decision.

---

# 10. Resolution status

```text
F01 BLOCKING:     CLOSED
F02 BLOCKING:     CLOSED
F03 BLOCKING:     CLOSED
F04 SIGNIFICANT:  CLOSED
F05 SIGNIFICANT:  CLOSED
F06 SIGNIFICANT:  CLOSED
F07 SIGNIFICANT:  CLOSED
F08 SIGNIFICANT:  CLOSED

STEP_6_BLOCKING:         3
STEP_6_SIGNIFICANT:      5
UNRESOLVED_BLOCKING:     0
UNRESOLVED_SIGNIFICANT:  0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
STEP_8_MAY_PROCEED:      YES
```

Step 8 must incorporate every binding amendment above into the final canonical WP-14 specification and perform final cross-system/status verification.
