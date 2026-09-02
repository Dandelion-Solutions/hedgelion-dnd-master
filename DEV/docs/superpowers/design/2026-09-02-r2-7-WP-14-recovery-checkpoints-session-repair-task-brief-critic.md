# R2.7 WP-14 — Recovery / Checkpoints / Session / Repair — Task-Brief Critic

Status: **STEP-1 WHOLE-PROJECT TASK-BRIEF CRITIC — ALL BLOCKING/SIGNIFICANT FRAMING FINDINGS RESOLVED**

Date: 2026-09-02

Target branch: `v1/engine-rearchitecture`

Owning Step-1 artifacts:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-recovery-checkpoints-session-repair-task-brief.md`
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-recovery-checkpoints-session-repair-source-manifest.md`

This critic applies the mandatory whole-project Task-Brief gate from `DEV/ARCHITECTURE/DESIGN_PROCESS.md`. It critiques the pre-publication framing reconstructed from current repository evidence; the final published Task Brief and Source Manifest incorporate every resolution below. It does not reopen accepted Step-5 or WP-11/WP-12/WP-13 architecture.

---

## 1. Critic scope

The framing was attacked against:

- Step-3 accepted execution / Continuation / fixed-RNG / idempotency continuity;
- Steps 5.2–5.9 and Step-5.14 recovery/currentness/concurrency integration laws;
- WP-10 durable family allocation;
- WP-11 direct routing/index contract and F03;
- WP-12 HOT/SQLite survivor/currentness contract;
- WP-13 durability/SAVE/publication and its WP-14 forward obligation;
- current `GAME/CORE` startup/session/runtime/storage/integrity/persistence/live consumers;
- current checkpoint/session/current-state schemas and templates;
- bootstrap/storage regression coverage and generator surfaces;
- downstream WP-16/WP-19/WP-20/WP-22/WP-24 consumers.

Reopen threshold used throughout:

> closed upstream architecture may be reopened only for a demonstrated contradiction, a new unsatisfied consumer or material insufficiency.

No such condition was found.

---

## 2. Findings and resolutions

### C01 — BLOCKING — Checkpoint-first startup wording can silently reintroduce historical recovery authority

**Attack.** Current `GAME/CORE/BOOTSTRAP_RUNTIME.md` still says gameplay startup reads the “latest checkpoint/hot STATE”, and bootstrap regression B25 treats first scene + checkpoint as a default launch expectation. If WP-14 framing merely says “repair checkpoints”, implementation could preserve checkpoint-first selection and violate Step-5.7 current-authority-first recovery.

**Resolution applied.** Task Brief now makes current authority/routing selection the first recovery machine boundary and explicitly requires reconciliation of `BOOTSTRAP_RUNTIME.md` plus bootstrap regressions. Checkpoint is optional evidence/hint only; ordinary recovery may read zero checkpoints. `MANIFEST.last_checkpoint_id` cannot select gameplay authority.

**Disposition:** CLOSED.

### C02 — BLOCKING — Recovery framing can lose accepted execution/temporal continuity and accidentally replay/reroll

**Attack.** A world-state/checkpoint-centric scope can recover current entities while omitting open RuntimeCommand/Procedure/Resolution/Continuation state, fixed accepted RNG, mandatory child/firing identities, accepted Choice/Reaction or independently due temporal-owner routing. That can cause reroll, rematerialization or duplicate semantic consequences.

**Resolution applied.** Task Brief now includes Step-3, Step-5.2 and Step-5.3 continuity as mandatory owner evidence. WP-14 must prove bounded recovery of every still-significant accepted execution/temporal dependency under stable identity and must never use checkpoint/history/session prose to synthesize missing accepted work.

**Disposition:** CLOSED.

### C03 — BLOCKING — Campaign fallback could overwrite current live authority

**Attack.** Recovery beginning from campaign HEAD could incorrectly treat campaign data as fallback truth when current routing selects an ACTIVE or CLOSED_UNABSORBED live epoch. That contradicts Step-5.2/5.7/5.8 and the repaired WP-12 local/live boundary.

**Resolution applied.** Task Brief now requires campaign HEAD only as campaign-domain discovery anchor; current owning routes must resolve and exact-pin every required native source. Missing/incompatible selected live authority blocks/suspects only the affected scope; campaign base is never silent fallback current truth.

**Disposition:** CLOSED.

### C04 — SIGNIFICANT — Session HEAD/status fields can be mistaken for recovery/currentness authority

**Attack.** `session.schema.yaml` and `CAMPAIGN/SESSIONS/_TEMPLATE.yaml` carry `base_head_sha`, `last_published_head_sha` and status. Current runtime prose also uses session/working-set HEAD vocabulary.

**Resolution applied.** Session records are framed strictly as coordination/navigation/audit/observability/currentness hints. They cannot prove host liveness/death, write authority, current native state, recovery frontier, successful handoff or successful save. Currentness must be re-established from authoritative native sources.

**Disposition:** CLOSED.

### C05 — SIGNIFICANT — Current checkpoint schema/template fields carry superseded generic-frontier semantics

**Attack.** `checkpoint.schema.yaml` and `CAMPAIGN/CHECKPOINTS/_TEMPLATE.yaml` still expose `valid_through_event_id`, `expected_commit_sha`, copied `world_time`, active PC/thread/scene lists and engine data without the final Step-5.7 field disposition being machine-realized.

**Resolution applied.** Manifest now makes schema/template reconciliation mandatory Step-2 evidence. Task Brief preserves exact Step-5.7 dispositions: generic event coverage is noncanonical, containing commit SHA is self-referential/noncanonical, copied world time is not chronology authority, active lists are non-exhaustive observations, engine data is provenance only, and no replacement completeness fields may be invented without proven value.

**Disposition:** CLOSED.

### C06 — SIGNIFICANT — Surviving SQLite could be promoted into cold-recovery authority

**Attack.** A local database surviving host/process loss may contain newer unpublished bytes than durable Git/native sources.

**Resolution applied.** Task Brief consumes WP-12 directly: cold recovery begins from current native durable authority; SQLite reuse is only an optimization after source-equivalence/deterministic-derivability proof. Local mtime/generation/apparent freshness never promotes unpublished bytes into recovered canon.

**Disposition:** CLOSED.

### C07 — SIGNIFICANT — WP-11 F03 can be lost if recovery is framed around directory/index scans

**Attack.** Recovery/repair convenience could use broad directory enumeration or treat index absence as semantic absence.

**Resolution applied.** Task Brief consumes WP-11 F03 explicitly: known-ID reads derive exact routes; bounded typed routing discovers admitted roots; derived indexes rebuild deterministically from native families and remain non-authoritative. Ordinary recovery cannot depend on broad campaign/WORLD/history scans.

**Disposition:** CLOSED.

### C08 — SIGNIFICANT — “Repair” can become silent historical fallback or invented reconciliation

**Attack.** Checkpoint/history/session/transcript evidence is useful for diagnostics, but a generic repair command could silently choose an older checkpoint or fabricate missing state when current authority is contradictory.

**Resolution applied.** Task Brief defines evidence-gated repair: current-source movement => RETRY/reselect; missing/incompatible required current source => BLOCKED/suspect affected scope; checkpoint/history may provide bounded evidence only after current authority is suspect and never becomes silent fallback authority. No invented lost HOT, player choice, RNG, mechanics or execution.

**Disposition:** CLOSED.

### C09 — SIGNIFICANT — Runtime/catalog interpretability can be omitted from recovery readiness

**Attack.** Hydrating owner bytes under an arbitrary current runtime could reinterpret open accepted execution.

**Resolution applied.** Task Brief requires recovery of compatible accepted runtime/catalog/rules/invocation/dependency context for open execution. Missing compatible interpretation context is a typed recovery/compatibility prerequisite failure, not permission to rebind semantics.

**Disposition:** CLOSED.

### C10 — SIGNIFICANT — Checkpoint/world/Git ordering can leak into chronology

**Attack.** Copied checkpoint `world_time`, event IDs, Git commit order or session timestamps could accidentally decide due/order/fictional chronology during recovery.

**Resolution applied.** Task Brief binds Step-5.9: chronology uses owner-approved typed evidence only. Recovery transport/checkpoint/session order cannot create fictional precedence or resolve an otherwise indeterminate temporal relation.

**Disposition:** CLOSED.

### C11 — SIGNIFICANT — Checkpoint facility defects and SAVE/handoff success can be conflated with gameplay recovery validity

**Attack.** Missing/malformed checkpoint could poison otherwise valid current RRC, or checkpoint creation could be treated as proof that explicit SAVE/controlled handoff succeeded.

**Resolution applied.** Task Brief makes checkpoint defects facility-scoped when current native RRC still proves; operations depending on the defective checkpoint remain blocked. Checkpoint never proves SAVE, handoff, current state or root completeness. WP-13/native durability proof remains authoritative for durability promises.

**Disposition:** CLOSED.

---

## 3. Whole-project impact result

The repaired framing preserves all upstream ownership boundaries:

```text
native owners                 -> gameplay/current/execution truth
campaign authoritative ref    -> campaign-domain current durable publication
current owning routes         -> native source selection
live exact source             -> live-owned current truth when selected
checkpoint                    -> optional immutable recovery/maintenance evidence
session                       -> coordination/navigation/audit hints
SQLite                        -> local HOT/cache after currentness proof
recovery attempt composition  -> ephemeral operation state
repair evidence               -> evidence only, never substitute owner
```

No generic RecoveryCut, snapshot owner, session lease, checkpoint frontier, repair owner, global root registry or broad-scan recovery authority is introduced.

---

## 4. Reopen / decision analysis

```text
UPSTREAM_CONTRADICTION:          NO
NEW_UNSATISFIED_CONSUMER:        NO
MATERIAL_UPSTREAM_INSUFFICIENCY: NO
HUMAN_DECISION_REQUIRED:         NO
```

All findings are framing/machine-reconciliation obligations mechanically implied by accepted architecture.

---

## 5. Critic count and gate

```text
STEP_1_CRITIC_BLOCKING:        3
STEP_1_CRITIC_SIGNIFICANT:     8
UNRESOLVED_BLOCKING:           0
UNRESOLVED_SIGNIFICANT:        0
HUMAN_DECISION_REQUIRED:       NO
STEP_1_PACKAGE_MAY_PUBLISH:    YES
```

The final Task Brief and Source Manifest must contain the resolutions above. After publication and cursor synchronization, WP-14 stops at mandatory Senior review; Step 2, WP-15 and implementation planning remain blocked.