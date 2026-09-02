# R2.7 WP-14 — Recovery / Checkpoints / Session / Repair — Step 8 Canonicalization

Status: **STEP 8 COMPLETE + POST-STEP-8 SR14-04 RECOVERY — MANDATORY FINAL SENIOR RE-AUDIT REQUIRED**

Date: 2026-09-03

Final canonical artifact:

- `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md`

Derivation chain:

- repaired Step-1 Task Brief / Source Manifest / critic;
- `SR14-01..SR14-03` Step-1 Senior recovery;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-2-evidence-extraction.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-source-manifest-step-2-expansion.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-3-decision-brief.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-4-collaborative-review.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-5-candidate-spec.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-source-manifest-step-6-expansion.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-6-whole-project-adversarial-review.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-7-resolution-gate.md`;
- final canonical specification above;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-post-step-8-senior-recovery-checkpoint-field-disposition.md` (`SR14-04`) — post-Step-8 canonical-completeness repair required by mandatory final Senior audit.

Historical Step-6 F01-F08 remain unchanged. `SR14-04` was discovered only after Step 8 and repairs checkpoint-field coverage/accounting without changing the selected architecture.

---

## 1. Step-8 result

WP-14 selects one implementation-facing realization direction:

> **PINNED CURRENT-SOURCE RRC RECOVERY + OPTIONAL CHECKPOINT ASSISTANCE + SEPARATE EVIDENCE-GATED HISTORICAL MAINTENANCE**

The result realizes already accepted Step-3/Step-5, R2.6 and WP-10..WP-13 architecture. It does not introduce a new gameplay authority, checkpoint owner, session lease, global RecoveryCut/frontier, repair journal, distributed transaction, generic rollback slot or alternate runtime repository transport.

---

## 2. Canonicalized machine boundaries

The final specification fixes these implementation-facing laws:

- ordinary recovery targets actual current native authorities selected by current typed routes;
- campaign revision H is a bounded discovery/current-routing anchor, not universal current state;
- live-owned current truth never falls back to campaign representation while live authority remains selected/current;
- one recovery attempt exact-pins each participating mutable source and keeps that source composition ephemeral;
- independent root discovery and transitive hydration remain bounded and owner-native;
- accepted RuntimeCommand/Procedure/Resolution/Continuation/RNG/Choice/Reaction/child/firing identity resumes rather than replays/rerolls/reallocates;
- still-significant accepted work retains compatible accepted interpretation/dependency evidence;
- ambient chat/Project/model context has no recovery authority;
- surviving SQLite is reusable only after source-equivalence/derivability proof;
- Agenda/index/cache/context state rebuilds from validated native state;
- checkpoint remains optional immutable evidence/maintenance descriptor and ordinary recovery may read zero checkpoints;
- every current checkpoint schema/template field now has an explicit auditable owner/disposition after SR14-04;
- generic checkpoint `valid_through_event_id` and self-referential containing-commit `expected_commit_sha` semantics are retired;
- checkpoint identity/association and schema/format fields remain narrowly non-semantic;
- `state.current_state_path` is only a non-authoritative layout hint and never selects current state, currentness, root completeness or recovery frontier;
- active PC/thread/scene fields remain optional non-exhaustive hints only;
- checkpoint `engine.*` and `ruleset.ruleset_set_sha256` remain optional provenance/diagnostic observations, never current runtime/ruleset authority or replacement for accepted open-execution interpretation dependencies;
- no new checkpoint root/source completeness manifest, RecoveryCut or replacement frontier field is introduced;
- `MANIFEST.last_checkpoint_id` remains a nullable narrow campaign-domain pointer only;
- “last checkpoint” never falls back to directory/ID/time/Git/session/SQLite guessing when the pointer is null/dangling;
- `runtime.session` remains coordination/navigation/audit/observability evidence only;
- recovery result remains ephemeral `READY | RETRY | BLOCKED`; `READY` is not a lease;
- legitimate source/routing movement is bounded `RETRY`, not corruption by default;
- fixed shipped repository path remains deterministic Python/core -> GitHub Connector -> authoritative non-force ref transition;
- missing fixed-path capability is typed supported-profile failure, not transport fallback authorization;
- repair is explicit, bounded and evidence-gated; historical evidence never silently replaces current authority;
- historical maintenance is a distinct operation from ordinary current recovery;
- historical reconstruction requires every required owner-valid historical source/revision/interpretation dependency to remain resolvable;
- historical live-owned truth also requires historical live owner/source evidence and never falls back to campaign state;
- reconstructed historical local state is maintenance-isolated, non-current and non-playable;
- `HDM_RESET_LAST_CHECKPOINT` is conditional historical maintenance, not a generic checkpoint rollback primitive;
- current promotion of historical repair starts a new attempt from a **fresh current owner basis**, reconciles historical evidence against that current basis, freezes its footprint and uses normal owner-native forward publication;
- multi-domain repair has no global rollback/distributed transaction; partial accepted native edges remain real and actual current authority is recomposed afterward;
- current `runtime.id_allocator` cannot be regressed by historical repair and every previously published ID remains permanently non-reusable;
- historical world/runtime repair does not silently rewind `runtime.disclosure` or `world.knowledge`;
- maintenance-isolated historical state cannot drive gameplay Context Assembly, Narrator/player-visible gameplay emission, new interactions/execution, chronology, RNG, current ID allocation, disclosure or live authority;
- `HDM_EXPORT_CHECKPOINT_LOG` is exact-basis read-only diagnostic export;
- pinned historical maintenance/export readers use their exact H without creating a durable GC lease;
- old Git byte reachability does not automatically restore semantically retired evidence;
- durable `runtime.maintenance_audit` is narrow support evidence and is created through current campaign authority/current allocator/current authorization/current WP-13 publication rules;
- local reconstruction, gameplay repair publication and audit publication remain separate atomicity domains;
- support diagnostics/exports cannot self-promote into recovery authority and remain access/disclosure constrained;
- checkpoint/Git/session/audit/storage order does not create fictional chronology;
- record/path/ID identity does not grant authority.

---

## 3. Step-6 findings and Step-7 closure

The mandatory Step-6 whole-project critic found:

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

Step 7 resolved every item mechanically from already accepted authority.

Final historical Step-6/Step-7 state remains:

```text
STEP_6_BLOCKING:         3
STEP_6_SIGNIFICANT:      5
UNRESOLVED_BLOCKING:     0
UNRESOLVED_SIGNIFICANT:  0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPENED:       NO
```

Post-Step-8 Senior audit finding:

```text
SR14-04 SIGNIFICANT      incomplete checkpoint field-by-field disposition
SR14-04:                 CLOSED
```

---

## 4. Source Manifest / completeness closure

The repaired Step-1 Source Manifest remained open-world throughout Step 2 and was expanded again before Step-6 findings when historical promotion exposed additional material owner seams.

Step-2 additions/promotions included:

- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`;
- `DEV/CATALOG/identifier-policies.json`;
- `DEV/TOOLS/run_maintenance_audit.py` as explicit negative-scope/developer-tool evidence;
- `GAME/CORE/CHRONOLOGY.md`;
- `GAME/CORE/ENGINE_UPDATES.md`;
- `GAME/TOOLS/init_campaign.py`;
- `DEV/TESTS/EXPLICIT_SAVE_CASES.md`;
- explicit historical-maintenance laws from Step 5.7.

Step-6 expansion promoted already accepted owner seams material to historical current promotion:

- Step-5.1 `runtime.id_allocator` published-ID non-reuse;
- Step-4 / Step-5.12 `world.knowledge` and `runtime.disclosure` ownership;
- Step-5.11 exact-evidence retention;
- Step-5.13 retention/GC/pinned-reader semantics.

The mandatory final Senior audit then identified that Step-2's broad checkpoint-field categories did not constitute complete leaf-by-leaf accounting. `SR14-04` repaired that completeness claim by mapping every current `GAME/SCHEMA/checkpoint.schema.yaml` member and corresponding template representation to one binding role/disposition, including the schema-admitted/template-absent `ruleset.ruleset_set_sha256` field.

No new semantic owner was created. No unconsumed Source Manifest/evidence gap remains after SR14-04.

`SR14-01..SR14-04` are now all consumed/closed:

- ambient host context never became authority and shipped runtime transport stayed fixed Connector-only;
- `MAINTENANCE_COMMANDS.md` was reconciled as a proposal/consumer, not authority;
- `MANIFEST.last_checkpoint_id` stayed a nullable narrow descriptor pointer across schema/template/scaffold semantics;
- every current checkpoint field now has an explicit auditable disposition without introducing new checkpoint completeness structures.

---

## 5. Cross-system consistency review

### Step 3 / Step 5.2 / 5.3

Accepted execution identity, fixed RNG, Continuation and temporal-owner recovery are preserved. Recovery rebuilds native RRC/derived Agenda without replay. CONSISTENT.

### Step 4 / Step 5.12

Fictional knowledge and human disclosure remain separate native owners. Historical repair cannot erase actual exposure or use maintenance diagnostics as a player-visible side channel. CONSISTENT.

### Step 5.1

No global frontier is introduced. Historical repair cannot regress the current campaign allocator or reuse published IDs. CONSISTENT.

### Step 5.7

Checkpoint remains optional immutable evidence, current authority wins ordinary recovery, historical maintenance is separate, rewind is not guaranteed and current replacement uses forward publication. SR14-04 now mirrors Step-5.7 section-17 field dispositions at leaf-level precision; no field is elevated into authority. CONSISTENT.

### Step 5.8

Selected current/historical live-owned scopes require the owning live source/revision evidence. Campaign fallback over current or required historical live authority remains forbidden. CONSISTENT.

### Step 5.11 / Step 5.13

Historical availability depends on retained owner-valid evidence. Exact pinned historical reads do not create durable GC leases, and residual transport bytes do not become ordinary retained semantic state automatically. CONSISTENT.

### R2.6

Only deterministic Python/core + GitHub Connector + non-force authoritative ref transition is supported for shipped runtime remote work. Missing capability fails typed; no alternate transport probing/fallback. CONSISTENT.

### WP-11

Exact direct routes and deterministic derivative index rebuild remain routing/lookup mechanics, not authority. `runtime.maintenance_audit` uses the allocated current route/identity family without becoming recovery owner. CONSISTENT.

### WP-12

SQLite remains local HOT/cache realization and may survive restart only after exact source-equivalence proof. Historical maintenance local stores are explicitly non-current until lawful promotion. CONSISTENT.

### WP-13

Historical promotion uses fresh current frozen owner-native publication attempts, truthful currentness/ambiguity semantics and no distributed transaction/global rollback. Partial accepted edges remain real. CONSISTENT.

No accepted upstream decision required reopening.

---

## 6. Current machine impact

No runtime/schema/template/catalog/test/tool implementation was changed in WP-14 Steps 2–8 or SR14-04 recovery.

The final canonical result explicitly routes later implementation repair for current debt including:

- checkpoint-first recovery wording in current bootstrap/storage/session surfaces;
- checkpoint schema/template reduction/alignment according to the exhaustive SR14-04 field dispositions;
- noncanonical checkpoint frontier/self-commit fields;
- template absence of schema-admitted optional `ruleset.ruleset_set_sha256` as alignment debt, without implying it must be retained;
- session fields whose wording can imply recovery/currentness authority;
- stale `MAINTENANCE_COMMANDS.md` reset/export behavior;
- narrow nullable `MANIFEST.last_checkpoint_id` schema/template/scaffold semantics;
- surviving SQLite verification/adoption behavior;
- fixed Connector recovery/maintenance failure/currentness coverage;
- current recovery/live no-fallback behavior;
- accepted-execution no-replay/reroll behavior;
- historical reset retention-unavailability and non-playable maintenance isolation;
- fresh-current-basis forward promotion and partial multi-domain repair;
- allocator non-regression/published-ID non-reuse;
- disclosure/knowledge preservation;
- maintenance-audit current publication/current allocator/idempotency;
- pinned historical reader/GC semantics;
- stale checkpoint-at-PLAY_READY/ordinary-save regressions.

Executable changes remain later implementation/WP-22 work after the required architecture/planning gates.

---

## 7. Downstream obligations

- **WP-15:** not started and not authorized; consumes WP-14 only after mandatory Senior final re-audit and explicit authorization.
- **WP-16:** final live physical realization must preserve selected owner/source recovery, exact-source CAS and no campaign fallback.
- **WP-19/WP-20:** bootstrap/migration must reconcile checkpoint/session/MANIFEST/recovery machine shape without making checkpoint mandatory or authority.
- **WP-22:** executable conformance/failure-injection coverage for current recovery, checkpoint optionality, checkpoint-field authority boundaries, live no-fallback, accepted execution no-replay, SQLite survivor proof, historical maintenance, allocator/disclosure preservation, partial repair and fixed Connector failures.
- **WP-24:** measure bounded recovery/maintenance reads before optimization.
- **WP-26:** previously routed documentation-consistency debt remains separate.
- **implementation planning:** exact APIs/schema fields/retry bounds/error vocabulary only after architecture authorization.

These routes do not authorize those domains now.

---

## 8. Final self-review

```text
[x] repaired Step-1 package + SR14-01..03 preserved
[x] Source Manifest kept open-world through Step 2
[x] Step-2 evidence/completeness gate passed before synthesis, with post-Step-8 SR14-04 correcting the checkpoint-field completeness defect
[x] Step-2 manifest expansion recorded
[x] Step-3 alternatives/tradeoffs/recommendation documented
[x] Step-4 collaborative refinements incorporated
[x] Step-5 candidate written before adversarial critic
[x] Step-6 dependency subgraph expanded where historical promotion exposed real owner seams
[x] Step-6 whole-project critic itemized 3 BLOCKING + 5 SIGNIFICANT findings
[x] Step-7 all historical Step-6 BLOCKING/SIGNIFICANT findings mechanically resolved
[x] historical Step-6 F01-F08 remain unchanged by post-Step-8 recovery
[x] SR14-04 recorded separately as the final-Senior-audit checkpoint-field completeness defect
[x] every current checkpoint.schema.yaml field and current template representation has an explicit auditable disposition after SR14-04
[x] state.current_state_path explicitly remains only a non-authoritative layout hint
[x] checkpoint engine/ruleset projections explicitly remain provenance only and cannot replace current or accepted open-execution interpretation authority
[x] no new checkpoint source/root manifest, RecoveryCut/frontier or mandatory checkpoint field introduced by SR14-04
[x] final canonical source contains every Step-7 repair plus SR14-04 field-completeness clarification
[x] checkpoint/session/SQLite/ambient context/exports/audit remain non-authoritative
[x] no campaign fallback over current or required historical live authority
[x] no replay/reroll/reallocation of accepted execution
[x] fixed gameplay Connector path preserved with no runtime transport fallback
[x] HDM_RESET_LAST_CHECKPOINT explicitly reconciled as conditional historical maintenance
[x] checkpoint export explicitly exact-basis/read-only
[x] MANIFEST.last_checkpoint_id retained only as nullable narrow descriptor pointer
[x] no human-owned product/authority/risk decision remains
[x] no upstream architecture reopened without contradiction/new consumer/material insufficiency
[x] no runtime/schema/template/catalog/test/tool implementation changed
[x] no WP-15 work started
[x] no implementation planning started
[x] final next gate is mandatory Senior final re-audit
```

---

## 9. Step-8 + SR14-04 gate

```text
WP-14_STEPS_2_8:          COMPLETE
SR14-04:                  CLOSED
STEP_6_BLOCKING:          3
STEP_6_SIGNIFICANT:       5
UNRESOLVED_BLOCKING:      0
UNRESOLVED_SIGNIFICANT:   0
HUMAN_DECISION_REQUIRED:  NO
NEXT_GATE:                MANDATORY SENIOR FINAL RE-AUDIT
```

Do not start WP-15 or implementation planning before mandatory Senior final re-audit and explicit subsequent authorization.
