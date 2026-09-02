# R2.7 WP-14 — Recovery / Checkpoints / Session / Repair — Step 4 Collaborative Review

Status: **STEP 4 COMPLETE — SYNTHESIS REFINED / NO HUMAN DECISION REQUIRED**

Date: 2026-09-03

Reviewed direction:

> **PINNED CURRENT-SOURCE RRC RECOVERY + OPTIONAL CHECKPOINT ASSISTANCE + SEPARATE EVIDENCE-GATED HISTORICAL MAINTENANCE**

---

## 1. Review objective

Step 4 attacks the Step-3 synthesis for ambiguity before candidate specification, focusing on boundaries most likely to accidentally create a second authority or unsafe maintenance behavior.

No upstream architecture is reopened. Every refinement below is derived from accepted Step-5/R2.6/WP-10..WP-13 authority.

---

## 2. R01 — Historical local reconstruction must not silently become playable current HOT

### Risk

Step 3 allows `HDM_RESET_LAST_CHECKPOINT` to build and atomically swap a historical local store. If the runtime then treats that store as ordinary current HOT, the command would silently roll local gameplay behind current durable authority and could generate divergent new accepted actions before any lawful current-state publication.

### Refinement

Historical reconstruction has an explicit **maintenance-isolated/non-current** state until one of two outcomes occurs:

1. it remains diagnostic/local maintenance material and is later discarded/replaced by ordinary current recovery; or
2. a separately application-authorized historical repair/rollback is promoted to new current durable state through owner-native forward non-force publication/currentness rules, after which local HOT adopts the newly accepted current authority.

A historical reconstructed store SHALL NOT yield ordinary gameplay `READY` merely because it passed historical integrity/RRC validation.

This follows Step-5.7 laws 53–54 and avoids a hidden local branch of canon.

---

## 3. R02 — Checkpoint descriptor is not automatically a complete historical composition manifest

### Risk

Step-5.7 explicitly says generic checkpoint hints are non-exhaustive. `HDM_RESET_LAST_CHECKPOINT` cannot infer that every historical source needed for exact reconstruction is listed merely because a checkpoint exists.

### Refinement

Historical maintenance may proceed only when owner-valid evidence can prove the complete required historical dependency composition for the requested maintenance scope.

The evidence may include the checkpoint descriptor plus immutable owner-valid historical routing/source/revision/interpretation evidence, but:

- omitted checkpoint fields do not prove absence;
- no source is guessed from “nearest” commit/time/name;
- no campaign fallback substitutes for historical live-owned truth;
- no new universal checkpoint source manifest is mandated by WP-14.

If completeness cannot be proven, return typed maintenance unavailability. This is expected/valid because guaranteed rewind was never promised.

---

## 4. R03 — Historical live state must obey historical owner evidence, not campaign fallback

### Risk

A historical checkpoint may correspond to a time when some scopes were live-owned. Reconstructing only campaign state would create a false historical world.

### Refinement

Historical maintenance must resolve the historical native owner/source for every claimed scope from retained owner-valid evidence. If a required historical live revision is unavailable or ownership cannot be proven, reconstruction is unavailable for the dependent maintenance scope.

Current Step-5.8 live currentness remains untouched; WP-16 still owns final live physical realization.

---

## 5. R04 — `HDM_EXPORT_CHECKPOINT_LOG` must be epistemically precise under pointer movement

### Risk

The phrase “latest checkpoint” can become false if `MANIFEST.last_checkpoint_id` changes during export.

### Refinement

The export is based on an exact pinned campaign revision H and must identify that basis. It may either:

- produce an explicitly **as-of-H** diagnostic export; or
- boundedly repin/retry if the UI/command contract specifically requires “current latest” at completion.

It SHALL NOT silently relabel an as-of-H descriptor as current after the campaign source moved.

Pointer movement is normal currentness movement, not corruption.

---

## 6. R05 — Maintenance audit is not atomic with local reconstruction or durable repair publication

### Risk

`runtime.maintenance_audit` is a durable campaign record family, while local reconstruction is a local operation and any durable repaired gameplay state is an owner-native publication. Treating all three as one transaction would imply a distributed transaction across local SQLite and repository currentness.

### Refinement

No such distributed transaction exists.

- historical local reconstruction has its own local atomic replacement boundary;
- durable current-state promotion, if authorized, follows its owning forward publication/CAS rules;
- maintenance-audit durability is a support/audit publication consequence and cannot define whether gameplay authority moved.

Operation reporting must preserve partial/indeterminate outcomes honestly. Audit publication failure cannot retroactively make an already accepted gameplay repair disappear, and gameplay repair failure cannot be hidden by a successful audit write.

Exact audit retry/idempotency fields remain implementation planning/TDD detail, but stable maintenance operation identity is required if durable audit publication may be retried.

---

## 7. R06 — Reset command token is not sufficient durable gameplay authorization

### Risk

Current maintenance proposal says exact command invocation authorizes a scoped destructive local operation. That could be misread as authorizing arbitrary durable campaign/live rollback.

### Refinement

The exact maintenance token may authorize the defined **local maintenance operation** under the support contract. It does not bypass application-level authorization for durable gameplay mutation.

Any promoted current repair must independently satisfy current application authorization, owner-specific write authority, currentness/CAS and durability/publication rules. Technical Connector capability also remains insufficient.

---

## 8. R07 — Ordinary recovery and historical maintenance have distinct result semantics

### Risk

Reusing `READY | RETRY | BLOCKED` for historical maintenance could make a historical reconstruction result look like current recovery readiness.

### Refinement

`READY | RETRY | BLOCKED` remains the ordinary current-recovery result family.

Historical maintenance uses a distinct maintenance outcome vocabulary/operation state at implementation-defined precision, with at least the semantic distinctions:

- reconstructed/validated historical material exists locally but is non-current;
- historical dependency unavailable/incompatible;
- current promotion accepted/rejected/indeterminate when separately attempted;
- local replacement failed/old store retained;
- audit publication success/failure/indeterminate where relevant.

WP-14 does not require one persisted generic maintenance-state machine or queue.

---

## 9. R08 — Surviving SQLite may accelerate current recovery, not historical-source proof

### Risk

A surviving database may happen to contain historical bytes matching a checkpoint and could be treated as historical source authority.

### Refinement

SQLite bytes can be reused for either current or historical reconstruction only after equality/deterministic-derivability proof against the applicable authoritative current or retained historical native sources/evidence. SQLite cannot supply missing historical authority merely because matching-looking rows survive locally.

---

## 10. R09 — `last_checkpoint_id` update is metadata publication, not checkpoint freshness authority

### Risk

A pointer update can become a heartbeat or pseudo-frontier if implementation treats “most recently selected descriptor” as “freshest valid recovery state”.

### Refinement

When K is created and selected together, descriptor + pointer update are one campaign publication transaction. No pointer-only freshness write is justified. Pointer selection records which descriptor the checkpoint facility selected; it does not rank native state freshness or establish currentness.

A prepared/unreachable K is not selected merely because its object exists.

---

## 11. R10 — Support exports and ambient context cannot backfill missing recovery evidence

### Risk

A prior maintenance export, chat transcript, Project memory or model context may contain apparently exact source IDs/values after durable sources are missing.

### Refinement

Such material is diagnostics only unless a separate owning contract explicitly admits the exact artifact as irreducible durable evidence. Generic support export/chat/model memory cannot self-promote into recovery or historical-maintenance authority.

---

## 12. Candidate requirements after review

Step-5 candidate must therefore state explicitly:

1. ordinary recovery uses only current native authorities/exact pins;
2. historical maintenance is distinct and cannot return ordinary gameplay READY by local reconstruction alone;
3. historical reconstruction requires provable complete required historical composition for its scope;
4. historical live-owned truth cannot fall back to campaign state;
5. promoted rollback/repair is a forward publication, never force/ref rewind;
6. maintenance audit is separate from gameplay authority and from local atomic replacement;
7. local maintenance command authorization is not durable gameplay mutation authority;
8. checkpoint export is exact-basis/as-of aware;
9. `last_checkpoint_id` remains metadata pointer only;
10. SQLite/support export/ambient context remain non-authoritative;
11. accepted execution/RNG/Continuation remains stable under both current recovery and historical reconstruction;
12. fixed gameplay Connector path remains the only supported remote path.

---

## 13. Review gate

```text
MATERIAL_SYNTHESIS_CHANGE:        NO
MECHANICAL_PRECISION_REFINEMENT:  YES
UPSTREAM_REOPEN_REQUIRED:         NO
HUMAN_DECISION_REQUIRED:          NO
STEP_5_CANDIDATE_ALLOWED:         YES
```

No human-owned trade-off remains.