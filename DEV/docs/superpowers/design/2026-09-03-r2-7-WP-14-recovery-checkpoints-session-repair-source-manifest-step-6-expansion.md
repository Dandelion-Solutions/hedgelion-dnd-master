# R2.7 WP-14 — Recovery / Checkpoints / Session / Repair — Step-6 Source-Manifest Expansion

Status: **ADVERSARIAL OPEN-WORLD SOURCE EXPANSION — INSPECTED BEFORE STEP-6 FINDINGS**

Date: 2026-09-03

Base manifest chain:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-recovery-checkpoints-session-repair-source-manifest.md`
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-source-manifest-step-2-expansion.md`

Step-6 whole-project attack exposed additional already-accepted owner seams that become material specifically when an explicit historical maintenance reconstruction is considered for promotion into new current state.

This addendum extends the manifest; it does not reopen any listed owner.

---

## 1. `runtime.id_allocator` owner seam

Source:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md`

Classification:

- **CANONICAL / OWNING** for campaign-scoped identity allocation/current allocator bookkeeping.

Material laws:

- `runtime.id_allocator` / `campaign-allocator` is the sole semantic owner of persistent campaign-scoped sequential allocation state;
- allocation + record creation is one atomic HOT operation;
- canonical allocation mutation joins the same durable publication closure;
- stale publication conflict reloads current allocator and rekeys only conflicting **unpublished** records/direct local refs;
- **published IDs are never changed or reused**.

WP-14 consequence:

Historical repair may not restore an old allocator high-water/collision state in a way that permits reuse of any previously published ID. A historical reconstruction may observe historical allocator evidence for diagnostics, but any promoted current state/new repair records must preserve the current allocator owner's non-reuse contract.

---

## 2. Knowledge and human-disclosure owner seam

Sources:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md`.

Classification:

- **CANONICAL / OWNING** for current fictional knowledge and durable human-player exposure / outbound disclosure semantics.

Material laws:

- current fictional subject epistemic relation is owned by `world.knowledge`;
- human player exposure is owned separately by `runtime.disclosure`;
- host/chat history is not campaign authority;
- editing/retrying/branching host history does not undo accepted gameplay or rewind `runtime.disclosure`;
- private tool/Connector/maintenance diagnostics must not intentionally become ineligible player-visible gameplay disclosure.

WP-14 consequence:

A historical world-state repair cannot silently erase already-established human disclosure or rederive fictional knowledge from the older world snapshot. If the repair footprint intentionally changes a knowledge/disclosure owner, that owner’s own correction/transition/access semantics apply. Previously real player exposure cannot be made “unexposed” merely because current world state is repaired to an older shape.

---

## 3. Retention / GC owner seam

Source:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`.

Classification:

- **CANONICAL / OWNING** for semantic retirement/current-namespace cleanup/ref cleanup and retention protection.

Material laws:

- uncertain retirement eligibility => retain;
- cleanup does not settle/rewind native owners or clear human disclosure;
- current `MANIFEST.last_checkpoint_id` protects its selected checkpoint target until coherent pointer clear/replace;
- checkpoint readers pin exact campaign revision H rather than requiring a durable GC lease;
- selected checkpoint may retire only with coherent pointer clear/replace and no other protected consumer;
- exact/live/recovery dependencies protected by owning contracts cannot be deleted merely by age;
- bounded authorized repair/security/support may inspect historical Git transport evidence, but that does not promote old bytes into ordinary semantically retained state;
- active or CLOSED_UNABSORBED selected live source cannot be cleaned;
- missing selected live source is healthy only after authority ended.

WP-14 consequence:

Historical maintenance has no guaranteed retention window. It may use only still-retained owner-valid evidence. Current recovery may not depend on old checkpoint retention. A pinned maintenance reader may finish against exact H even if later current cleanup removes the selected descriptor from a newer tree.

---

## 4. Step-5.11 exact evidence seam promoted from conditional

Source:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md`.

Classification:

- **CANONICAL / OWNING** for exact-text/semantic-history retention and compaction.

Material laws:

- host conversation is not immutable campaign transcript authority;
- no verbatim claim without exact retained evidence;
- exact payload remains protected while an admitted live consumer requires exact form;
- semantic consumers must become content-sufficient before exact payload loss;
- hidden chain-of-thought, developer/system/project instructions, private tool traces and private role reasoning are not admitted gameplay transcript history.

WP-14 consequence:

Current or historical recovery may consume exact communication evidence only when an owning live dependency still protects it. Generic chat/model memory or a support export cannot replace compacted/missing exact evidence.

---

## 5. Manifest disposition

```text
NEW_UPSTREAM_DECISION:              NO
EXISTING_OWNER_SEAMS_PROMOTED:      YES
STEP_5_1_ID_ALLOCATOR:              REQUIRED
STEP_4_STEP_5_12_DISCLOSURE:        REQUIRED FOR HISTORICAL PROMOTION/DIAGNOSTICS
STEP_5_11_EXACT_EVIDENCE:           REQUIRED WHEN LIVE DEPENDENCY EXISTS
STEP_5_13_RETENTION_GC:             REQUIRED FOR HISTORICAL MAINTENANCE
UPSTREAM_REOPEN_REQUIRED:           NO
HUMAN_DECISION_REQUIRED:            NO
```

These sources are now part of the WP-14 adversarial dependency subgraph and must be reflected in Step 7/final canonicalization wherever the corresponding seam is material.