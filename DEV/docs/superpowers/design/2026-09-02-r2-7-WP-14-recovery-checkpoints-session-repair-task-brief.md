# R2.7 WP-14 — Recovery / Checkpoints / Session / Repair — Architecture Task Brief

Status: **STEP 1 COMPLETE — CRITIC REPAIRS APPLIED / MANDATORY SENIOR REVIEW REQUIRED**

Date: 2026-09-02

Target branch: `v1/engine-rearchitecture`

Task-specific Source Manifest:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-recovery-checkpoints-session-repair-source-manifest.md`

Mandatory whole-project Task-Brief critic:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-recovery-checkpoints-session-repair-task-brief-critic.md`

---

## 1. Mission

WP-14 realizes the already-accepted HDM recovery/checkpoint/session/repair architecture against the current R2.7 physical storage/HOT/publication machine.

The inherited canonical direction is:

> **CURRENT-AUTHORITY-FIRST / CHECKPOINT-OPTIONAL / NATIVE-ROUTED BOUNDED RECOVERY WITH EVIDENCE-GATED REPAIR**

WP-14 is not a greenfield choice among snapshot/recovery strategies. Steps 5.2/5.4/5.7 and the closed WP-11/WP-12/WP-13 packages already constrain the solution space. This work must reconcile current runtime/schema/template/test surfaces to those contracts without creating a new recovery owner, universal frontier, session lease or checkpoint authority.

Step 1 only establishes the evidence scope and decision framing. It does not perform Step-2 extraction, select final machine fields/APIs, edit implementation or begin planning.

---

## 2. Current authority and upstream closure

WP-14 consumes, without reopening by overlap alone:

- Step-3 accepted execution/Continuation/idempotency/RNG continuity;
- Step-5.2 Resumable Runtime Closure;
- Step-5.3 temporal/pending-obligation continuity;
- Step-5.4 host lifecycle/session handoff;
- Step-5.5 durability promises;
- Step-5.6 campaign publication/crash consistency;
- Step-5.7 checkpoint/recovery protocol;
- Step-5.8 live ownership/currentness;
- Step-5.9 chronology separation;
- Step-5.14 integrated recovery/concurrency review;
- WP-10 durable record-family allocation;
- WP-11 physical topology/routing/indexing;
- WP-12 HOT/SQLite transaction/currentness realization;
- WP-13 durability/SAVE/publication realization.

Closed upstream architecture may be reopened only if Step 2 establishes one of:

```text
REAL CONTRADICTION
NEW UNSATISFIED CONSUMER
MATERIAL INSUFFICIENCY
```

Implementation debt, stale prose/schema/tests, convenience or preference for a simpler snapshot model are not sufficient.

### Required forward obligations

WP-14 must explicitly discharge or preserve at least:

- **WP-11/F03:** current-route-first recovery and deterministic index rebuild;
- **WP-12 -> WP-14:** cold recovery from current native authorities/exact pins; surviving SQLite only after source-equivalence proof; recovery composition ephemeral; checkpoint optional evidence;
- **WP-13 -> WP-14:** current-authority-first sources; checkpoint remains optional/non-SAVE authority; session/cached HEAD is not authority.

---

## 3. Problem statement

Current architecture says a completely cold runtime resumes from a compatible composition of actual current native durable authorities. Current machine surfaces still contain older checkpoint/session/frontier assumptions.

Concrete current debt already established in Step 1 includes:

- `GAME/CORE/BOOTSTRAP_RUNTIME.md` post-selection startup wording that says read “latest checkpoint/hot STATE” and places checkpoint/STATE early in canon priority;
- `GAME/SCHEMA/checkpoint.schema.yaml` and `GAME/CAMPAIGN/CHECKPOINTS/_TEMPLATE.yaml` fields already dispositioned by Step 5.7 as noncanonical or narrow evidence:
  - generic `valid_through_event_id`;
  - self-referential `expected_commit_sha`;
  - copied `world_time`;
  - active PC/thread/scene observations;
  - engine provenance that is not current runtime authority;
- `GAME/SCHEMA/session.schema.yaml` and session template `base_head_sha` / `last_published_head_sha` / status fields that must remain coordination/currentness hints, never semantic currentness/recovery authority;
- bootstrap regression B25 that presently couples first scene with checkpoint creation;
- local/HOT/session/runtime prose that must be reconciled with WP-12/WP-13 source-currentness laws.

These are machine-realization debts. They do not by themselves reopen Step-5.7.

---

## 4. In-scope architecture questions

Step 2–8, if later authorized, must answer at implementation-facing precision:

1. How does ordinary cold recovery begin after campaign selection without using checkpoint/session/local cache as authority?
2. Which minimum campaign-domain state anchors discovery of current owning routes?
3. How are every required mutable native source and live-owned scope exact-pinned for one recovery attempt?
4. How are current independently recoverable roots enumerated boundedly through native routing/lifecycle?
5. How are correctness-required transitive dependencies hydrated without campaign/WORLD/history scans?
6. How are open RuntimeCommand/Procedure/Resolution/Continuation, fixed RNG, mandatory children/firings and accepted Choice/Reaction recovered under stable identity without replay/reroll?
7. How are independently due temporal-source owners recovered and Agenda/derived scheduling rebuilt without duplicate occurrence materialization?
8. How is accepted runtime/catalog/rules/invocation interpretation context resolved for open work?
9. Which local SQLite bytes/helpers may be reused after cold start, and what source-equivalence proof is required first?
10. What exact role remains for `runtime.session`, session HEAD/status fields and session notes?
11. What exact checkpoint fields survive, change semantics or are retired under Step-5.7?
12. What remains the meaning of `MANIFEST.last_checkpoint_id`?
13. When may ordinary recovery read zero checkpoints?
14. How are optional checkpoint defects scoped so they do not falsely invalidate independent current gameplay RRC?
15. How do current source movement and routing movement produce `RETRY` rather than false corruption or stale resume?
16. What conditions produce `BLOCKED`/integrity-suspect recovery for a dependent scope?
17. How does repair use bounded checkpoint/history/session/transcript evidence without turning historical evidence into silent fallback authority?
18. How are derived family/index/query/Agenda/context structures rebuilt deterministically under WP-11/WP-12?
19. How are access/currentness/acting-principal requirements enforced for any repair that mutates durable state?
20. Which current runtime/schema/template/test surfaces are conforming, stale, superseded or downstream-owned?

Exact field/API/schema choices are Step-3+ synthesis/candidate work, not Step 1.

---

## 5. Canonical invariants that WP-14 must preserve

### 5.1 Current authority first

Ordinary recovery begins from the selected campaign's current authoritative campaign ref as a **campaign-domain discovery anchor**, not as a universal state snapshot.

Current owning routes then select each required native current source. No checkpoint ID, checkpoint age, event ID, session HEAD, commit timestamp or local DB freshness may choose current authority.

### 5.2 Campaign HEAD is not complete state

If current routing points a scope to a live source, recovery must exact-pin/read that source. ACTIVE and CLOSED_UNABSORBED live state remains current truth for its claimed scope until lawful forward authority movement.

Campaign base is not fallback current truth merely because it is available.

### 5.3 Exact source pinning

Each mutable native source participating in one recovery attempt is resolved to one exact revision for that attempt. No branch-relative mixed-revision hydration is valid.

Recovery composition is ephemeral operation evidence, not a durable universal RecoveryCut/frontier owner.

### 5.4 Native owner preservation

Recovery/checkpoint/session/repair metadata cannot copy or replace native current authority.

At minimum:

```text
world state                    -> native world owners
Procedure resources            -> runtime.procedure
execution cursor/state          -> runtime.command/resolution
suspension/Choice/Reaction      -> runtime.continuation
accepted fixed RNG              -> accepted execution continuity owner/evidence
temporal obligation             -> native temporal owner
live mutable truth              -> selected live source
campaign allocation             -> runtime.id_allocator
```

### 5.5 Bounded root discovery

Normal cold recovery must not require:

- campaign-wide file scans;
- full WORLD traversal;
- broad directory enumeration;
- all historical runtime records;
- full Git-history walks;
- Story/transcript semantic reconstruction.

Known-ID reads follow WP-11 exact routes. Independent roots are discovered through typed current routing/lifecycle. Derived indexes can nominate/rebuild but cannot prove semantic absence.

### 5.6 Accepted execution is resumed, not replayed

Open accepted work keeps stable identities, fixed accepted RNG, accepted invocation/catalog context, receipts/causal evidence and single-consume Continuation semantics.

Recovery never rerolls or rematerializes accepted mandatory execution merely because process/chat/SQLite state was lost.

### 5.7 Temporal continuity is owner-native

Armed independently-due temporal owners remain discoverable through their native temporal routing. Once an occurrence crossed into accepted execution, recovery resumes that accepted firing identity rather than selecting the same occurrence again from a rebuilt Agenda.

Agenda and other scheduler-like projections rebuild; no generic pending/job queue becomes authority.

### 5.8 Checkpoint is optional immutable evidence

Checkpoint may support diagnostics, maintenance, migration/repair evidence or measured recovery acceleration. It is not:

- current gameplay authority;
- root-membership authority;
- save proof;
- handoff proof;
- session lease;
- universal recovery frontier;
- mandatory startup anchor.

Ordinary current recovery may read zero checkpoints.

### 5.9 Checkpoint hints require current-owner validation

Checkpoint observations are non-exhaustive unless a future narrowly typed contract explicitly says otherwise. Absence from checkpoint does not prove current absence. A stale checkpoint never rolls current authority back.

### 5.10 Session metadata is coordination evidence only

`runtime.session`, including cached observed HEAD values/status/notes, may support navigation, audit, coordination, observability and hints.

It cannot by itself prove:

- host alive/dead;
- current gameplay state;
- current live ownership;
- write authority;
- recovery-safe handoff;
- successful save;
- definitive recovery frontier.

### 5.11 Surviving SQLite is not cold-recovery authority

A surviving WP-12 database may be reused only after proving its relevant bytes are equal to or deterministically derivable from currently selected compatible native sources/evidence.

Local generation/mtime/apparent freshness cannot recover unpublished canon that was never durably established under its native contract.

### 5.12 No invented lost state

Destroyed unpublished HOT/SOFT state, unaccepted player choices, hidden model reasoning, intended writes, unrecorded RNG/mechanics or guessed continuation cannot be synthesized during recovery/repair.

Recovery returns to actual surviving current durable authority.

### 5.13 Interpretation closure

Open accepted execution resumes under compatible accepted runtime/catalog/rules/invocation/dependency context. A fresh host cannot silently reinterpret open work under arbitrary newer ambient mechanics.

### 5.14 Chronology remains separate

Checkpoint `world_time`, event IDs, Git/ref order, session timestamps or storage ordering cannot decide fictional chronology unless an owning chronology contract grants that exact evidence meaning.

### 5.15 Repair is evidence-gated and scope-bounded

Repair is not a new semantic owner or generic rollback feature.

Baseline disposition:

```text
current source/routing basis moved legitimately
    -> RETRY / reselect / rehydrate

current pinned basis is internally inconsistent
    -> affected scope integrity-suspect / BLOCKED
    -> bounded evidence/repair analysis

optional checkpoint facility defective but current RRC proves
    -> checkpoint facility suspect/blocked as needed
    -> independent gameplay state remains valid
```

Checkpoint/history may aid explicit repair but never silently replace current authority. Any mutating repair must preserve native owner, access, publication and durability rules.

---

## 6. Current checkpoint field disposition to carry into Step 2

The Task Brief does not choose final replacement schema, but Step 2 must begin from these already accepted Step-5.7 dispositions:

| Current field/concept | Existing canonical disposition |
|---|---|
| `valid_through_event_id` | Retire as generic recovery completeness/frontier semantics. Domain-specific event coverage may exist only under its own owner. |
| `expected_commit_sha` | Retire as containing-commit identity; self-referential under content-addressed Git. Repository revision context may carry provenance externally. |
| checkpoint copied `world_time` | Diagnostics/presentation only if retained; never chronology/currentness authority. |
| active PC/thread/scene lists | Optional non-exhaustive observations only if measured/proven useful; never root completeness. |
| checkpoint engine/runtime data | Optional provenance/diagnostics; current campaign runtime comes from current campaign authority, while open work resolves accepted interpretation pins. |
| `MANIFEST.last_checkpoint_id` | Narrow campaign-domain pointer to most recently selected/published checkpoint descriptor only. |
| new root/source completeness fields | Forbidden by default; require concrete measured bounded-recovery/diagnostic value and preserved authority laws. |

Step 2 must verify current schema/template/test references before any synthesis proposes keep/remove/replace details.

---

## 7. Current session field disposition to carry into Step 2

Current session schema/template includes:

```text
session_id
status
player_id
pc_id
scene_id
base_head_sha
last_published_head_sha
started_at
ended_at
notes
```

Step 1 fixes no final retention set. Step 2 must classify each field against actual consumers.

However, accepted architecture already forbids interpreting any of these as duplicate current gameplay authority or a correctness lease. In particular:

- `base_head_sha` / `last_published_head_sha` may remain cached observation/audit/currentness hints;
- `status` cannot prove host liveness/death or fence gameplay writes by itself;
- `notes` cannot become recovery payload/state authority;
- `player_id`/`pc_id` references do not independently grant authorization;
- session lifecycle cannot terminate Procedure/Resolution/fictional scene lifecycle by implication.

---

## 8. Concrete current machine/test debt to reverse-audit

Mandatory Step-2 machine targets include at least:

- `GAME/CORE/BOOTSTRAP_RUNTIME.md` — replace checkpoint-first interpretation with current-authority-first/native-route hydration while preserving campaign-selection barrier and bounded lazy reads;
- `GAME/CORE/SESSION.md` — reconcile host/session handoff and durable session record role;
- `GAME/CORE/RUNTIME.md` — reconcile cold-start/currentness/lost-dirty behavior;
- `GAME/CORE/INTEGRITY.md` — classify repair and scoped integrity outcomes without invented fallback;
- `GAME/CORE/STORAGE.md` / `PERSISTENCE.md` — source/currentness/crash evidence consumed by recovery;
- `GAME/CORE/LIVE_SCENE.md` / `MULTIPLAYER.md` — current live authority and stale-session behavior;
- `GAME/SCHEMA/checkpoint.schema.yaml` and checkpoint template;
- `GAME/SCHEMA/session.schema.yaml` and session template;
- `GAME/SCHEMA/current_state.schema.yaml`;
- bootstrap regression B25/B42 plus persistence/save tests that constrain checkpoint optionality;
- any executable schema/contract tests discovered in Step 2.

A current implementation/test contradiction with accepted architecture is implementation debt unless it establishes one of the formal upstream reopen conditions.

---

## 9. Non-goals

WP-14 does not:

- redesign Step-3 execution;
- redefine SOFT/HARD/SAVE or publication;
- choose a new global recovery snapshot;
- create a persistent RecoveryCut/frontier;
- make checkpoint mandatory;
- make session a host lease;
- add generic pending/job/repair queues;
- redefine live claims/CAS/absorption (WP-16 owns final machine);
- redesign chronology;
- redesign Story/transcript/disclosure/GC unless a bounded recovery dependency requires inspection;
- implement bootstrap/migration (WP-19/WP-20);
- edit runtime/schema/template/tests in Step 1;
- begin WP-15;
- begin implementation planning.

---

## 10. Evidence and completeness requirements for Step 2

If Senior GO later authorizes Step 2, evidence extraction must:

1. consume the Source Manifest as open-world, not a closed list;
2. extract relevant owner laws item-by-item with qualifiers/exceptions;
3. map every current checkpoint/session/recovery field and behavior to an owner/disposition;
4. map every admitted independent recovery root and required dependency class;
5. inventory concrete current consumers/tests/tools before proposing schema removal/change;
6. distinguish currentness movement (`RETRY`) from pinned-basis corruption (`BLOCKED`/repair);
7. prove where optional checkpoint defects are facility-only;
8. preserve negative findings/non-goals/revisit triggers;
9. close the synthesis-completeness gate before Step 3.

No candidate final schema/API/protocol is authorized before that gate.

---

## 11. Expected deliverables after future authorization

This Step-1 package anticipates, without starting them:

- Step 2: item-level evidence extraction + Source Manifest expansion/completeness gate;
- Step 3: Decision Brief for the implementation-facing recovery/checkpoint/session/repair machine;
- Steps 4–5: candidate development/review;
- Step 6: whole-project adversarial critic;
- Step 7: resolution of mechanically resolvable findings;
- Step 8: final canonicalization;
- later downstream implementation/TDD only after normal architecture/planning gates.

---

## 12. Step-1 critic result

Mandatory whole-project framing critic found and mechanically resolved:

```text
BLOCKING:     3
SIGNIFICANT:  8
```

Resolved areas:

- checkpoint-first startup authority;
- accepted execution/temporal recovery continuity;
- live-current-source/campaign-fallback protection;
- session hint non-authority;
- checkpoint field disposition;
- surviving SQLite proof;
- WP-11 direct routing/index rebuild;
- evidence-gated repair;
- interpretation closure;
- chronology separation;
- checkpoint facility vs SAVE/handoff/current-state proof.

Final Step-1 state:

```text
UNRESOLVED_BLOCKING:     0
UNRESOLVED_SIGNIFICANT:  0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
```

---

## 13. Mandatory gate

WP-14 Step 1 ends here.

After coherent publication, cursor synchronization and fresh verification:

> **MANDATORY SENIOR REVIEW REQUIRED**

Do not begin Step 2, WP-15 or implementation planning without explicit Senior GO.