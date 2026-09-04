# R2.7 WP-19 — Bootstrap / Campaign Creation / Initial Materialization — Whole-Project Task-Brief Critic

Status: **STEP 1 WHOLE-PROJECT CRITIC COMPLETE — MANDATORY SENIOR REVIEW CANDIDATE**

Date: 2026-09-05

Verified critic basis: `5fc24905be5c9e1b47929ee9e7b49ea8b9f2a053`

This is the mandatory Step-1 whole-project Task-Brief critic required by `DEV/DESIGN_PROCESS.md` and `DEV/ARCHITECTURE/DESIGN_PROCESS.md`.

The critic was reconstructed independently from current `DEV/PROJECT_MAP.md` and actual owners/consumers. It did not use the WP-19 scope inventory or the completed Task Brief as an answer key.

Companion artifacts:

- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief.md`.

---

## 1. Independent reconstruction method

Starting from the project-map campaign-creation route, the critic independently followed these direct and indirect dependency paths:

```text
Project Instructions / install bootstrap
    -> explicit campaign-choice barrier
    -> storage discovery / storage v3 baseline
    -> exact runtime package selection
    -> ruleset package identity / release metadata
    -> branch ancestry / creator / access authority
    -> New Campaign fast path / Campaign Setup
    -> init_campaign materializer
    -> GAME/CAMPAIGN template tree
    -> MANIFEST / CONFIG / CARD / CURRENT schemas
    -> initial from-scratch publication
    -> normal persistence/currentness boundary
    -> campaign identity/card projections
    -> PLAYER / PC / provisional onboarding
    -> READY_PC / PLAY_READY / lifecycle active
    -> session/resume / first true live scene
    -> multiplayer mode/join policy/PLAYER authorization
    -> House-Rules default materialization
    -> release-builder + integration-test consumer
    -> future migration/evolution boundary in WP-20
```

For each route the critic checked whether an existing owner already answers the question, whether a current machine/runtime consumer contradicts that owner, whether a stale source is being mistaken for current law, and whether a real unresolved human-owned decision remains.

---

## 2. Findings summary

```text
BLOCKING:    2
SIGNIFICANT: 5
MINOR:       1

UNRESOLVED_BLOCKING:    0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
```

All mechanically resolvable BLOCKING/SIGNIFICANT defects were repaired in the Source Manifest and Task Brief before this checkpoint. No finding authorizes Step 2 or implementation.

---

## 3. Finding dispositions

### F19-S1-01 — BLOCKING — exact ruleset-set identity was missing from bootstrap framing

**Defect**

A bootstrap framing based only on current prose argument lists could describe a materializer invocation that cannot satisfy the actual machine contract: `GAME/TOOLS/init_campaign.py` requires `--ruleset-set-sha256`, but current `00_DND_BOOTSTRAP.md`, `BOOTSTRAP_RUNTIME.md` and `CAMPAIGN_SETUP.md` omit it from their listed generator arguments.

Without discovering this dependency, Step 2 could incorrectly treat ruleset creation identity as a later/optional detail or invent a source for it.

**Actual owner/evidence**

- `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` — campaign ruleset created/current projection and exact set identity;
- `DEV/ARCHITECTURE/RULESET_PACKAGE_MACHINE_CLOSURE.md` — runtime package contains exact resolved set/lock evidence;
- `DEV/TOOLS/release_builder.py` — generated `RUNTIME_PACKAGE.yaml` includes required `ruleset_set_sha256`;
- `GAME/TOOLS/init_campaign.py` — required CLI input and manifest materialization;
- `DEV/TESTS/test_release_integration.py` — executable producer/consumer proof passes `package_meta["ruleset_set_sha256"]`.

**Resolution**

CLOSED. The Source Manifest and Task Brief now require Step 2 to reconcile one exact chain:

```text
selected validated runtime package
    -> RUNTIME_PACKAGE.ruleset_set_sha256
    -> init_campaign --ruleset-set-sha256
    -> MANIFEST.ruleset.created_with/current
```

The affected bootstrap prose is explicitly part of the Step-2 consistency audit. No new ruleset-selection authority or Product Owner choice is permitted by this finding.

**Human decision required:** NO.

---

### F19-S1-02 — BLOCKING — “campaign creation / first play” could collapse four different lifecycle states

**Defect**

The initial WP-19 label is broad enough that a weak Task Brief could collapse:

```text
blank scaffold created
PROVISIONAL_IDENTITY durable
READY_PC achieved
PLAY_READY / lifecycle active
```

into one generic “campaign is ready” state. That would change hard-to-reverse product behavior: when mechanical facts may become authoritative, when an interrupted setup is resumable, and when normal mechanics-dependent live play is allowed.

**Actual owner/evidence**

- `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` — technical scaffold publication remains initializing;
- `GAME/CORE/DIEGETIC_ONBOARDING.md` — admitted provisional pre-READY play;
- `GAME/CORE/CHARACTER_READINESS.md` + `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md` — READY_PC semantics;
- `GAME/CORE/DURABILITY_GUARD.md` — PROVISIONAL_IDENTITY / READY_PC / PLAY_READY durability boundaries;
- `GAME/CORE/RUNTIME.md`, manifest/card schemas — lifecycle active requires READY_PC + PLAY_READY;
- `GAME/CORE/SESSION.md` — interrupted unfinished setup remains initializing.

**Resolution**

CLOSED. The Task Brief now has an explicit transition model, separate evidence questions and failure scenarios for scaffold, provisional durability, READY_PC and PLAY_READY. It records that these semantics are already accepted and are to be audited for composition, not reopened as a new Product Owner decision.

**Human decision required:** NO.

---

### F19-S1-03 — SIGNIFICANT — branch/storage authority route and stale v2 owner projections were not safe to omit

**Defect**

A bootstrap-only file list misses the architectural owner that explains why a campaign branch starts from storage default HEAD, why inherited storage bytes are not campaign canon, and why the first campaign-specific commit establishes creator authority.

At the same time, current `DEV/ARCHITECTURE/BRANCH_MODEL.md` still contains storage-v2 / `baseline_version` and old engine-provenance wording, conflicting with current storage-v3/bootstrap/schema/ruleset owners. Treating the file as wholly current or wholly irrelevant would both be incorrect.

**Actual owner/evidence**

- `DEV/ARCHITECTURE/BRANCH_MODEL.md` — branch/root/creator topology plus stale v2 projections;
- `DEV/ARCHITECTURE/ACCESS_CONTROL.md` — creator/write authority;
- `GAME/CORE/STORAGE.md` + `GAME/SCHEMA/dnd_storage.schema.yaml` — current storage v3;
- `GAME/SCHEMA/campaign_manifest.schema.yaml` — current engine/ruleset campaign identity;
- R2.7 owner clarification — no compatibility obligation for unreleased scaffold, direct structural canonicalization authorized.

**Resolution**

CLOSED. The Source Manifest distinguishes the still-applicable branch/creator laws from stale v2 identity projections, and the Task Brief makes exact supersession/current-owner reconciliation a Step-2 obligation. Current pre-release compatibility policy is already owner-set; WP-20 remains future released-campaign evolution.

**Human decision required:** NO.

---

### F19-S1-04 — SIGNIFICANT — campaign identity/card/config projection owners were missing from a narrow bootstrap graph

**Defect**

Scaffold creation directly materializes MANIFEST, CONFIG, CAMPAIGN_CARD and CURRENT surfaces. If the Task Brief audited only branch creation and the generator, it could miss projection authority, lifecycle projection rules, campaign-name semantics and same-transaction consistency.

**Actual owner/evidence**

- `GAME/CORE/CAMPAIGN_IDENTITY.md` — MANIFEST campaign name authority; card/README projections;
- `GAME/CORE/CAMPAIGN_CARD.md` + card schema — menu projection only and lifecycle projection rules;
- manifest schema/template, CONFIG template, CURRENT template/schema;
- `GAME/CORE/CAMPAIGN_SETUP.md` — initial setup/defaults and same-batch projection behavior.

**Resolution**

CLOSED. These owners and machine projections are explicit in the Source Manifest. The Task Brief requires machine->architecture accounting and prevents card/README/config convenience surfaces from becoming new authority.

**Human decision required:** NO.

---

### F19-S1-05 — SIGNIFICANT — initial publication, later setup durability and resumability were under-scoped

**Defect**

The first scaffold publication is structurally exceptional: one from-scratch campaign tree replaces inherited storage contents. Later setup/PLAY_READY persistence is normal campaign publication from a pinned campaign HEAD. Treating both as one generic save operation would obscure retry/currentness/resume semantics and could let partial setup masquerade as an active campaign.

**Actual owner/evidence**

- `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` and `CAMPAIGN_SETUP.md` — initial scaffold publication;
- `GAME/CORE/PERSISTENCE.md` — campaign transaction transport and initial-scaffold exception;
- `GAME/CORE/DURABILITY_GUARD.md` — when provisional/readiness/activation publication is required;
- `GAME/CORE/SESSION.md`, session/current-state schemas — recovery/resume coordination.

**Resolution**

CLOSED. The Task Brief now audits initial publication and later setup/launch publication as separate transaction classes and includes interrupted-setup/retry/resume failure scenarios.

**Human decision required:** NO.

---

### F19-S1-06 — SIGNIFICANT — multiplayer initial authority was not guaranteed by a singleplayer-shaped creation frame

**Defect**

The materializer and card support both singleplayer and multiplayer. A narrow creation frame could audit only the default singleplayer path and miss creator-explicit mode, `invite_only` default, PLAYER binding and card participant projection semantics.

**Actual owner/evidence**

- `GAME/CORE/MULTIPLAYER.md`;
- `DEV/ARCHITECTURE/ACCESS_CONTROL.md`;
- `GAME/SCHEMA/player.schema.yaml`;
- manifest/card schemas and setup owner.

**Resolution**

CLOSED. The Task Brief includes multiplayer mode/join-policy/PLAYER authority from the first applicable durable write and keeps cached participant logins nonauthoritative. It explicitly preserves the closed-architecture rule: no WP-16/access reopen without contradiction/new unsatisfied consumer/material insufficiency.

**Human decision required:** NO.

---

### F19-S1-07 — SIGNIFICANT — prose-only audit would fail the R2.7 bidirectional machine-realization requirement

**Defect**

The initial scope inventory names runtime prose owners but does not by itself prove that the current materializer, campaign template, schemas, release package producer and integration test agree with those owners. WP-19 is part of a whole-project final audit whose explicit requirement is architecture->machine **and** machine->architecture.

The ruleset-set contradiction was discovered precisely because the machine consumer graph was followed beyond the initial prose inventory.

**Actual owner/evidence**

- current `GAME/CAMPAIGN/` tree and template files;
- `GAME/SCHEMA/dnd_storage.schema.yaml`, campaign manifest/card/current/session/player/pc schemas;
- `GAME/TOOLS/init_campaign.py`;
- `DEV/TOOLS/release_builder.py`;
- `DEV/TESTS/test_release_integration.py`;
- R2.7 whole-project task brief and owner clarification.

**Resolution**

CLOSED. The Source Manifest includes machine/template/test families as first-class evidence rather than downstream examples, and the Task Brief explicitly requires bidirectional ownership/disposition for every material current bootstrap surface.

**Human decision required:** NO.

---

### F19-S1-08 — MINOR — future compatibility and dormant neighboring work could bleed into WP-19

**Defect**

`ENGINE_UPDATES.md`, ruleset package adoption and broad campaign topology naturally expose future migration questions. Template presence also exposes House-Rules and other roots that are not automatically active design work.

Without an explicit boundary, WP-19 could expand into WP-20 migration design or reopen closed House-Rules/Story/planning architecture merely because related files exist in a campaign.

**Actual owner/evidence**

- R2.7 owner clarification: no compatibility requirement for current unreleased scaffold; WP-20 owns future evolution;
- `RULESET_PACKAGE_IDENTITY.md` / `ENGINE_UPDATES.md`: future incompatible migration boundary;
- `CAMPAIGN_HOUSE_RULES.md`: existing policy owner;
- design-process coverage-does-not-imply-activation rule.

**Resolution**

CLOSED. The Task Brief makes WP-20, substantive implementation and unrelated closed architecture explicit non-goals. House-Rules/default template materialization is classified inherited/already satisfied unless a concrete contradiction is found. Dormant/future obligations retain their trigger rather than becoming current work.

---

## 4. Product Owner boundary review

The critic independently challenged the repaired Step-1 frame for hidden human-owned decisions.

### Product semantics

Current owners already decide:

- explicit campaign selection;
- scaffold-first invisible infrastructure;
- low-friction setup and minimal questions;
- provisional/diegetic onboarding;
- READY_PC/PLAY_READY and first true live scene semantics;
- lifecycle `initializing/active/paused` meaning.

No unresolved product-semantic alternative remains at Step 1.

### Canonical authority / ownership

Current owners already allocate:

- storage baseline -> storage default branch / storage owner;
- current campaign runtime/ruleset -> MANIFEST;
- creator -> first campaign-specific commit provenance;
- player authority -> creator/active PLAYER rules;
- PC readiness -> READY_PC owner;
- durable current/canon -> native state owners;
- card/README/session/index/checkpoint -> projection/coordination roles only.

The stale v2 prose is a current-consistency defect, not an unresolved ownership trade-off.

### Meaningful compatibility policy

The Product Owner already clarified that no real campaigns depend on the unreleased current scaffold and no backward compatibility is required during R2.7 structural canonicalization. WP-20 owns future released-campaign compatibility/evolution.

No current compatibility decision remains for WP-19 Step 1.

### Hard-to-reverse lifecycle/product behavior

The lifecycle transition to active is already constrained by READY_PC + PLAY_READY, while provisional setup may be durable and resumable under `initializing`. No competing unresolved lifecycle policy was discovered.

### Material quality trade-off

The current design already prefers low-friction setup, bounded package/storage reads, one coherent initial publication and no broad worldbuilding before play. The critic found consistency/audit work inside those constraints, not a new material trade-off between viable product strategies.

### Explicit risk acceptance

No new material risk requiring Product Owner acceptance was discovered.

```text
HUMAN_DECISION_REQUIRED: NO
```

The mandatory Senior review still applies as an independent process gate.

---

## 5. Closed-upstream architecture review

The critic tested whether WP-19 evidence requires reopening an accepted upstream architecture block rather than repairing a current consumer.

Results:

- ruleset-set propagation defect conforms to existing S6D exact-identity architecture;
- storage-v2 prose conflicts with later/current storage/ruleset owners and the explicit pre-release canonicalization decision; no upstream product decision is needed to recognize it as stale;
- READY_PC/PLAY_READY lifecycle evidence confirms existing owners rather than contradicting them;
- multiplayer creation consumes current access law without exposing a new unsatisfied authority case;
- House-Rules/template presence creates no new policy semantics;
- first-publication/persistence distinction is already supported by current runtime owners.

```text
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
```

A later Step-2 contradiction/material insufficiency would be handled by the normal design process, but none is established by Step-1 evidence.

---

## 6. Step-1 critic gate

Final framing disposition:

```text
F19-S1-01 BLOCKING    CLOSED — exact ruleset-set propagation added to evidence/task scope
F19-S1-02 BLOCKING    CLOSED — scaffold/provisional/READY_PC/PLAY_READY lifecycle separated
F19-S1-03 SIGNIFICANT CLOSED — branch/storage/access/stale-v2 reconciliation added
F19-S1-04 SIGNIFICANT CLOSED — identity/card/config/current projections added
F19-S1-05 SIGNIFICANT CLOSED — publication/durability/session/resume route added
F19-S1-06 SIGNIFICANT CLOSED — multiplayer initial authority route added
F19-S1-07 SIGNIFICANT CLOSED — machine/template/schema/test reverse audit added
F19-S1-08 MINOR       CLOSED — WP-20/dormant-neighbor non-activation boundary made explicit

UNRESOLVED_BLOCKING:    0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
STEP_2_STARTED: NO
STEP_2_AUTHORIZED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
```

### Critic recommendation to Senior

The repaired Step-1 package is sufficiently complete for the mandatory Senior review. The critic finds no remaining framing blocker/significant omission and no current Product Owner decision gate.

**Recommendation:** Senior may grant GO for WP-19 Step 2 if the independent Senior review agrees with this framing/evidence package.

This recommendation is not authorization. The worker must stop at the mandatory Senior checkpoint after publication/status synchronization.
