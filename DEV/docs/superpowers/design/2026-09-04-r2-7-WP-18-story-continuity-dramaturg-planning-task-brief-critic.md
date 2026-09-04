# R2.7 WP-18 — Story / Continuity / Dramaturg Planning — Whole-Project Task-Brief Critic

Status: **STEP-1 SENIOR RECOVERY CRITIC — ALL CONFIRMED BLOCKING/SIGNIFICANT FINDINGS REPAIRED / MANDATORY SENIOR STEP-1 RE-REVIEW REQUIRED**

Date: 2026-09-04

Senior-recovery basis: `e35d96a08c73a818b62b0e799bc9d9fc3fc3e54e`

Reviewed Architecture Task Brief:

- `DEV/docs/superpowers/design/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-task-brief.md`

Reviewed Source Manifest:

- `DEV/docs/superpowers/design/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-source-manifest.md`

This is the mandatory whole-project **Task-Brief critic** required by `DEV/DESIGN_PROCESS.md`. It independently reconstructs the relevant owner/consumer graph and attacks the recovered Step-1 framing. It does not authorize Step 2 or implementation.

---

## 1. Provenance and count discipline

The original Step-1 package at `e35d96a08c73a818b62b0e799bc9d9fc3fc3e54e` recorded the following historical critic result:

```text
HISTORICAL_RECONSTRUCTED_BLOCKING:     6
HISTORICAL_RECONSTRUCTED_SIGNIFICANT:  8
HISTORICAL_UNRESOLVED_BLOCKING:        0
HISTORICAL_UNRESOLVED_SIGNIFICANT:     0
```

Those historical findings remain provenance. The Senior Step-1 review then found four additional defects in the supposedly review-ready package:

```text
SENIOR_BLOCKING:      2
SENIOR_SIGNIFICANT:   2
```

The Senior findings are tracked separately as `SR18-01..SR18-04`; they are not silently folded into or renamed as the earlier B18/S18 finding identities.

After repairing them, this critic ran a fresh whole-project pass. **New confirmed** findings from that recovery pass are counted separately.

---

## 2. Historical Step-1 finding identity summary

The old critic's itemized findings remain historical and substantively preserved:

### Historical BLOCKING — all previously closed

1. **B18-01** — Story and prospective planning could collapse into one narrative-state problem.
2. **B18-02** — missing legacy Story files could be mistaken for missing Story architecture.
3. **B18-03** — planning ownership could be presumed from catalog vocabulary / `PreparationDraft`.
4. **B18-04** — shared Dramaturg horizon underframed across authorization/currentness/privacy.
5. **B18-05** — missing bidirectional architecture <-> machine completeness proof.
6. **B18-06** — obvious instruction/context/disclosure/cleanup owners omitted from the earlier Manifest reconstruction.

### Historical SIGNIFICANT — all previously closed

1. **S18-01** — Story orientation could become current decision authority without proper-source escalation.
2. **S18-02** — retired chapter authority could return as narrative organization.
3. **S18-03** — Story exact-history / transcript-compaction boundary underframed.
4. **S18-04** — Chronicler service could become scheduler/queue state.
5. **S18-05** — `canon invalidates preparation` lacked implementation-facing testability framing.
6. **S18-06** — Story/planning failure and cold recovery underframed.
7. **S18-07** — technical order could become fictional chronology.
8. **S18-08** — downstream scaffold/migration/test work could be activated during Step 1.

The Senior recovery does not reopen these historical findings merely because it extends the dependency graph.

---

## 3. Senior Step-1 findings and repairs

### SR18-01 — wrong Step-1 artifact class

**Severity:** `SIGNIFICANT`

**Confirmed defect:** Current `DEV/DESIGN_PROCESS.md` defines Step 1 as **Architecture Task Brief** with a mandatory whole-project **Task-Brief critic**. The published WP-18 package incorrectly used `Decision Brief` / `decision-brief-critic` taxonomy, even though Step 3 is the decision-brief stage.

**Risk:** Process identity becomes ambiguous; a Decision Brief may be mistaken for an architecture decision artifact, and later routing can treat the wrong artifact class as authoritative.

**Repair:**

- replacement artifact is `...-task-brief.md` with explicit Architecture Task Brief identity;
- replacement critic is `...-task-brief-critic.md`;
- Source Manifest, global progress and task-local cursor route only to these corrected Step-1 artifacts;
- old `...-decision-brief.md` and `...-decision-brief-critic.md` are removed from the final tree rather than retained as competing Step-1 artifacts.

**Disposition:** `CLOSED`.

---

### SR18-02 — native Actor-owned planning/intent owner omitted

**Severity:** `BLOCKING`

**Confirmed defect:** The earlier owner/dependency graph discussed Dramaturg planning and Story/continuity without pinning the current R2.2 source-Actor owner for canonical in-world goals/objectives/intentions/commitments/reconsideration.

**Risk:** WP-18 could accidentally store an NPC's “real plan” in retained Dramaturg preparation or infer current intent from Story, creating duplicate/shadow Actor authority.

**Owning evidence reconstructed:**

- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-canonical-spec.md`;
- `DEV/ARCHITECTURE/ACTOR_MODEL.md`;
- `DEV/SCHEMAS/world-actor-state.schema.json`;
- `DEV/SCHEMAS/world-record.schema.json`;
- `DEV/CATALOG/entity-structures.json`;
- `DEV/TESTS/test_r2_7_wp04_actor_asset_conformance.py`.

Current machine evidence explicitly materializes sparse source-Actor `long_term_goal`, `current_objective`, `next_intention`, `material_commitments` and `reconsideration_cues` and tests the single-owner boundary.

**Repair:** Architecture Task Brief and Source Manifest now impose:

```text
Actor/NPC canonical current intentional state
    = source Actor owner

Dramaturg preparation
    = prospective noncanonical conditional guidance

Story/continuity
    = retrospective noncanonical projection/orientation
```

Planning may reference/predict Actor behavior but cannot own/override the Actor's current intentional state. Story may inform/orient but cannot establish it. Current Actor/native owner movement may invalidate preparation.

**Reopen check:** No contradiction, newly unsatisfied R2.2 consumer or material insufficiency was demonstrated. R2.2 remains closed.

**Disposition:** `CLOSED`.

---

### SR18-03 — incomplete current runtime consumer reconstruction

**Severity:** `BLOCKING`

**Confirmed defect:** The prior Source Manifest claimed a current CORE consumer set while listing only a short subset and omitting material direct consumers including Senior examples `NARRATIVE`, `INFORMATION`, `LORE`, `NPC`, `MULTIPLAYER`.

**Risk:** Step 2 could produce a locally consistent Story/Prep mapping that conflicts with actual runtime information, Actor, presentation, shared-state, recovery or chronology behavior while still claiming whole-project coverage.

**Recovery reconstruction method:** Starting from `DEV/PROJECT_MAP.md` concern and dependency hot paths, the critic followed current owners into actual runtime consumers and grouped the material direct subgraph as:

**Role/reasoning/preparation/presentation**

- `GAME/CORE/RUNTIME.md`
- `GAME/CORE/AI_REASONING.md`
- `GAME/CORE/PLAY_POLICY.md`
- `GAME/CORE/PREP.md`
- `GAME/CORE/GM_CRAFT.md`
- `GAME/CORE/NARRATIVE.md`
- `GAME/CORE/INFORMATION.md`
- `GAME/CORE/LORE.md`
- `GAME/CORE/NPC.md`
- `GAME/CORE/DIALOGUE.md`

**World continuity / causal development**

- `GAME/CORE/PROCESSES.md`
- `GAME/CORE/WORLDGEN.md`
- `GAME/CORE/CAMPAIGN_OPERATIONS.md`
- `GAME/CORE/SESSION.md`

**Durability/currentness/recovery/shared-state**

- `GAME/CORE/DURABILITY_GUARD.md`
- `GAME/CORE/STORAGE.md`
- `GAME/CORE/PERSISTENCE.md`
- `GAME/CORE/SAVE_CONTRACT.md`
- `GAME/CORE/INTEGRITY.md`
- `GAME/CORE/MULTIPLAYER.md`
- `GAME/CORE/LIVE_SCENE.md`
- `GAME/CORE/CHRONOLOGY.md`
- `GAME/CORE/SOURCES.md`

The Source Manifest separately adds the relevant current schemas/catalog/tests and R2.7 owners.

**Repair:** Task Brief/Manifest now route Step 2 through this reconstructed direct consumer graph and explicitly prohibit interpreting it as a repository-global closed-world proof. The prior positive `CURRENT_CORE_CONSUMER_SET` completeness wording is removed.

**Disposition:** `CLOSED`.

---

### SR18-04 — R2.6 applicability omitted

**Severity:** `SIGNIFICANT`

**Confirmed defect:** The earlier Step-1 package did not explicitly include the current R2.6 host-assurance owner where WP-18 must map instruction/runtime/test/evaluation obligations.

**Risk:** Architecture could either omit required behavioral-containment acceptance obligations or incorrectly activate production-like MVP evaluation before implementation.

**Owning evidence:** `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md`, including:

- observable behavioral containment as supported-host correctness;
- ambient Project/chat context has no campaign authority;
- R2.7 instruction mapping requirement;
- production-like acceptance coverage for Dramaturg/Actor/Chronicler -> Narrator containment, planning containment, no same-envelope Story feedback, local/shared planning retrieval/conflict/rebase/no-plot-restoration;
- LAW R2.6-10: production-like integrated evaluation runs on the implemented MVP rather than a parallel pre-implementation MVP.

**Repair:** Task Brief/Manifest now classify R2.6 obligations into architecture mapping now versus post-implementation production-like acceptance later. No implementation/harness is activated.

**Disposition:** `CLOSED`.

---

## 4. Fresh whole-project recovery critic method

After the four repairs, the critic did not merely reread the edited prose. It re-attacked the package through these routes:

1. process taxonomy — Step-1 artifact class and routing;
2. Story authority/lifecycle — Step 4 + Step 5.10/5.11/5.12/5.13;
3. continuity — R2.1 source escalation;
4. Actor ownership — R2.2 + current Actor machine schema/catalog/test realization;
5. Context Runtime — R2.3 bounded discovery/currentness/eligibility;
6. role execution — R2.4 typed handoffs and no same-envelope feedback;
7. retained multiplayer planning — R2.5;
8. host assurance — R2.6 architecture versus post-implementation acceptance boundary;
9. current R2.7 realization — WP-08..WP-17 applicable owners;
10. runtime direct consumers — role/reasoning, information/lore/NPC, processes/worldgen/session, durability/recovery and multiplayer/live/chronology clusters;
11. machine reverse audit — Actor schema/catalog/test; Story/planning vocabulary; manifest/schema negative realization evidence;
12. downstream containment — WP-19/WP-20/WP-22/WP-24/WP-25 and implementation planning.

The critic asked, for every claimed responsibility:

- who currently owns it;
- which consumer can invalidate the proposed boundary;
- whether a machine field is only representation or a real semantic owner;
- whether a completeness statement is actually supported;
- whether a dormant/downstream obligation is being falsely activated.

---

## 5. Recovery-pass candidate issue rejected by further evidence

During reconstruction, one candidate SIGNIFICANT concern was raised:

> The current Actor machine mapping might materialize only `current_goal`/`next_intended_action` on legacy NPC surfaces and therefore leave material commitments/reconsideration unrepresented, tempting WP-18 planning to become the substitute.

This was **not** retained as a finding. Fresh current R2.7 machine evidence showed:

- `DEV/SCHEMAS/world-actor-state.schema.json` contains the full accepted sparse evolving set: `long_term_goal`, `current_objective`, `next_intention`, `material_commitments`, `reconsideration_cues`;
- `DEV/CATALOG/entity-structures.json` routes `world.actor` to typed `continuity`;
- `DEV/TESTS/test_r2_7_wp04_actor_asset_conformance.py` explicitly asserts that exact field set and the single Actor continuity owner.

Therefore the suspected gap was disproved before critic disposition and is **not** counted as a new SIGNIFICANT finding.

---

## 6. Recovery adversarial pass

| Attack state | Required safe framing/result |
|---|---|
| Dramaturg plan says NPC will betray an ally; Actor intention changed | Actor current owner wins; prep invalidates/rebases. |
| Story says NPC still pursues an old objective | Story cannot establish current cognition; resolve Actor owner. |
| NPC runtime file contains planning-looking text | Reverse-audit to current R2.2 owner versus noncanonical prep; physical field does not decide authority. |
| `PreparationDraft` is serialized | Serialization alone does not admit durable owner. |
| Story deleted, Actor/world healthy | Gameplay/recovery remains valid. |
| Story contradicts current lore/knowledge/Actor state | Current routed owner wins. |
| Chronicler backlog persists | No scheduler/job/heartbeat authority. |
| Newly produced Story remains physically in chat before Narrator | R2.4/R2.6 containment and fresh rebind prohibit same-envelope feedback. |
| Ambient chat contains stale Actor goal or plan | R2.6 ambient context is nonauthority; current routed owner wins. |
| Shared planning contains local private information | R2.3/R2.5/WP-16/WP-17 eligibility protects recipient boundary. |
| PLAYER/control changes during shared-plan update | Revalidate authorization/current source before acceptance. |
| LIVE changes while plan is edited | Planning cannot become LIVE authority; revalidate/rebase. |
| Planning generation/file/Git order appears newer | No fictional/current native authority follows from technical order. |
| `story_root`/schema absent | Machine realization debt/downstream scaffold concern, not architecture reopen. |
| Integrated host-leakage test has not run yet | Correct at architecture stage; preserve explicit R2.6 post-implementation acceptance obligation, do not fabricate a parallel MVP. |

No additional confirmed BLOCKING/SIGNIFICANT defect survived this pass.

---

## 7. Recovered Step-1 invariants

The repaired package now forces later work to preserve:

1. Architecture Task Brief / Task-Brief critic taxonomy;
2. Story retrospective projection != Dramaturg prospective preparation != source-Actor current intentional state;
3. R2.2 source Actor owns goals/objectives/intentions/commitments/reconsideration when durable/current;
4. `world.knowledge` remains separate proposition-stance authority;
5. no Actor-intent inference from Story or hidden canonical intent stored in planning;
6. current Actor/player/mechanic/native transitions may invalidate preparation;
7. Step-4/5.10 Story semantics remain controlling despite stale/missing legacy paths;
8. no chapter resurrection;
9. Story and planning remain nonauthority for gameplay recovery;
10. single-player durable planning remains unadmitted absent proven need;
11. R2.5 local/shared multiplayer planning remains noncanonical, privacy-scoped and fenced/rebased;
12. actual direct runtime consumers include narrative/information/lore/NPC/dialogue/process/worldgen/session/multiplayer/live/chronology and persistence boundaries, not merely Story/Prep files;
13. no unsupported positive closed-world completeness statement;
14. R2.6 behavioral-containment requirements are mapped as architecture obligations now and implemented-MVP acceptance later;
15. no parallel pre-implementation MVP/evaluation harness;
16. architecture->machine and machine->architecture proof remain mandatory;
17. physical persistence, cache, index, Story or planning generation cannot create semantic authority;
18. Step 2, WP-19 and implementation planning remain blocked pending Senior GO.

---

## 8. Critic gate

```text
HISTORICAL_ITEMIZED_BLOCKING:             6
HISTORICAL_ITEMIZED_SIGNIFICANT:          8
HISTORICAL_UNRESOLVED_BLOCKING:           0
HISTORICAL_UNRESOLVED_SIGNIFICANT:        0

SENIOR_RECOVERY_BLOCKING:                 2
SENIOR_RECOVERY_SIGNIFICANT:              2
SR18_01:                                  CLOSED
SR18_02:                                  CLOSED
SR18_03:                                  CLOSED
SR18_04:                                  CLOSED

RECOVERY_CRITIC_NEW_BLOCKING:             0
RECOVERY_CRITIC_NEW_SIGNIFICANT:          0
RECOVERY_CRITIC_NEW_MINOR:                0

UNRESOLVED_BLOCKING:                      0
UNRESOLVED_SIGNIFICANT:                   0
HUMAN_DECISION_REQUIRED:                  NO
UPSTREAM_REOPEN_REQUIRED:                 NO
ARCHITECTURE_SELECTED:                    NO
IMPLEMENTATION_CHANGED:                   NO
WP_19_AUTHORIZED:                         NO
STEP_2_AUTHORIZED:                        NO
NEXT_GATE:                                MANDATORY SENIOR STEP-1 RE-REVIEW
```

The critic authorizes no Step-2 work. Its only disposition is that the recovered Step-1 package has no confirmed unresolved BLOCKING/SIGNIFICANT critic finding and may be returned to the mandatory Senior gate.