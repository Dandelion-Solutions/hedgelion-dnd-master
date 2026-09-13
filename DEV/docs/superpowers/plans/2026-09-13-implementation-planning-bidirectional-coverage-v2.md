# HDM Implementation Planning — Bidirectional Coverage / Currentness Closure v2

Status: **AUTHOR SIRR REPAIR RECONCILIATION — INDEPENDENT SENIOR RE-REVIEW REQUIRED**
Date: 2026-09-13
Canonical readiness authority: WP-27 final implementation-planning readiness.
Planning currentness baseline before repair publication: `d01bd4bac55115408f6347f88214475855fbac0e`.
Independent re-reviewed state: `3626a7be398fb648d6e8f0d52fda63193f1b12a4`.
Production implementation authorized: **NO**.

This closure recomputes package identity/routing after SIRR-001..SIRR-005 repair. It does not claim runtime proof PASS.

## 1. Canonical accounting

```text
DIRECT: 116
PURE_PROOF: 9
COMPOSITE_PARENTS: 8
TOTAL_ACTIVE: 133
TRIGGER_GATED: 12
NO_WORK_TERMINALS: 79
R004: ABSENT
RD_UNITS: 14
```

No repair finding creates a readiness identity or activates a trigger-gated/no-work item.

## 2. Direct readiness -> current routed RD

```text
RD01: R001,R003,R033,R043,R047,R048,R050
RD02: R007,R008,R009,R017,R049,R052
RD03: R025,R026,R027,R028,R104,R108,R109,R110,R111,R113,R114,R115,R116,R126,R128,R129,R130,R132,R136
RD04: R015,R063,R064,R065,R066,R067
RD05: R034,R035,R036,R042,R046,R112
RD06: R037,R045,R069,R070,R071
RD07: R011,R012,R038,R072,R073,R074
RD08: R010,R039,R075,R076,R077
RD09: R013,R014,R019,R020,R040,R078,R079,R080
RD10: R054,R055,R056,R057,R118,R133,R137
RD11: R059,R060,R097,R105,R106,R107,R117,R119,R120,R124,R125,R127,R134,R135,R138,R139,R140,R144,R145
RD12: R021,R044,R081,R082,R083,R121,R123,R141,R142,R143,R146
RD13: R022,R051,R084,R085,R099,R102,R131
RD14: R030,R086,R098,R100
```

Result: 116/116 direct identities remain assigned exactly once. SIRR repair changes executable detail for RD-02/RD-06/RD-09/RD-13/RD-14 but no identity assignment.

## 3. Pure-proof routing

```text
R023 -> Stage3PackageProofTests
R031 -> ActorReadinessProofTests (RD-03 + RD-14)
R032 -> DomainCommitmentProofTests (RD-03 + RD-14); real-target measurement EMPIRICAL_DEFERRED
R041 -> ExecutionRetryProofTests (RD-05/RD-07/RD-08)
R058 -> RoleContainmentProofTests (RD-10/RD-11); empirical protocol branch dormant
R061 -> ContextBoundednessProofTests (RD-11); supported-target empirical branch dormant
R068 -> Wp12HotProofTests, exact WP-12 §14 duties 1..17 in v2 appendix
R088 -> OwnerFirstReconciliationProofTests
R089 -> ProofChannelDisciplineTests + exact-head HOSTED_CI evidence
```

SIRR-001 specifically repairs R068 semantic witness binding. Row-count-only proof is no longer a current route.

## 4. Composite parents

```text
R006:
  INFO->RD02
  ACTOR->RD03
  THREAD_VISIBILITY->RD08
  package witness -> CompositeR006ProofTests

R016:
  INFO->RD02
  ACTOR->RD03
  EXECUTION->RD05
  TEMPORAL->RD08
  LIVE->RD09
  COLLAB->RD12
  STORY->RD13
  package witness -> CompositeR016ProofTests

R018:
  INFO->RD02
  ACTOR->RD03
  ROUTE/ROOT->RD04
  EXECUTION->RD05
  TEMPORAL->RD08
  LIVE->RD09
  COLLAB->RD12
  STORY->RD13
  package witness -> CompositeR018ProofTests

R029:
  ACTOR->RD03
  DURABILITY->RD06
  ONBOARDING->RD14
  package witness -> CompositeR029ProofTests

R053:
  INFO->RD02
  LIVE->RD09
  package witness -> CompositeR053ProofTests

R062:
  KNOWLEDGE->RD02
  DISCLOSURE->RD02
  RETAINED_MESSAGE->RD02
  ACTOR_CONTINUITY_RELATIONS->RD03
  EFFECT_APPLICATION->RD03
  RUNTIME_LIFECYCLE_EVIDENCE->RD05
  TEMPORAL_BINDING->RD08
  SEMANTIC_EVENT_HISTORY->RD13
  package witness -> CompositeR062ProofTests

R087:
  RETROSPECTIVE->RD11
  SEMANTIC_EVENT_T0->RD13
  SAVE_SESSION_MENU->RD14
  package witness -> CompositeR087ProofTests

R122:
  CHRONOLOGY->RD08
  CURRENTNESS_SCENE->RD09
  CONTEXT->RD11
  COLLABORATION_BRIDGE->RD12
  package witness -> CompositeR122ProofTests
```

All eight parent witnesses still require negative authority-transfer assertions and `CompositeVersionImpactProofTests`.

Repair-specific parent conditions:
- R016/R018 STORY cannot close until `MANIFEST.storage.story_root` and generated-scaffold preservation are green;
- R029 DURABILITY consumes native-domain SAVE composition rather than campaign-only universal SAVE;
- R053 INFO/LIVE witness must preserve CLOSED_UNABSORBED after successful close + failed absorption/handoff.

## 5. Enumerated mixed-proof suites

```text
R071 -> exact WP-13 §15 duties 1..38 -> Wp13DurabilityProofTests -> v2 WP-12/WP-13 appendix
R074 -> WP-14 §15 items 13..25 -> Wp14RecoveryProofTests
R077 -> WP-15 §13 items 9..17 -> Wp15TemporalProofTests
R080 -> WP-16 §15 items 1..21 current + item 22 EMPIRICAL_DEFERRED -> Wp16LiveAccessProofTests
R083 -> WP-17 §28 themes 1..26 -> Wp17CollaborationProofTests
R099 -> T0HistoricalBasisProofTests; real-target critical-path observation dormant
R102 -> CommentatorSelfContainedProofTests
```

SIRR-001 repair result: R068 and R071 are now semantically itemized, not just numerically itemized. Every WP-12/WP-13 row has one owner duty, supporting target, named executable witness and primary channel.

## 6. Reverse map — current plan/task -> admitted work

Current worker route is the base package-index RD plan plus `2026-09-13-implementation-planning-sirr-repair-amendments.md` for affected RDs.

Reverse-scope law remains:
- implementation-bearing work must discharge a direct readiness obligation, admitted composite slice, owner-valid integration join, exact proof obligation, or required projection/version/checkpoint/migration consequence;
- proof-only tasks create no gameplay authority;
- docs/audit/project-map edits are projections of admitted owner work;
- shared-file checkpoints coordinate physical writes only;
- no worker may infer new semantic work from a wave number or repair prose.

Repair reverse review:
- RD-06 SAVE/PERSISTENCE consumer edits discharge R071/WP-13 shipped-consumer obligations and existing durability/publication readiness; no new readiness;
- RD-14 bootstrap CORE prose edits discharge existing R030/R086 bootstrap identity/currentness and WP-19 consumer alignment; no new readiness;
- RD-13 Story selector is required projection/topology closure for R051 and R016/R018 STORY slices; no new readiness;
- RD-13 Dramaturg publication/admission makes existing R085/R131 worker-ready; no planner authority introduced;
- RD-02/RD-09 wording/test correction preserves R053/WP-16 lifecycle semantics and creates no new state.

No orphan semantic task is introduced by SIRR repair.

## 7. Scheduling/edge reconciliation

Base scheduling remains `2026-09-13-implementation-planning-execution-waves.md` plus the mandatory `2026-09-13-implementation-planning-execution-waves-sirr-repair-addendum.md`.

Material deltas:
1. R071 completion consumes exact v2 WP-13 proof rows + shipped-consumer cutover.
2. RD-13 Story selector -> RD-14 generated-scaffold preservation is a bounded shared-file/consumer checkpoint.
3. E11 now explicitly joins RD-06 ordinary campaign publication before retained Dramaturg generation promotion; RD-09/RD-10/RD-12 provide current access/role/collaboration admission evidence.
4. LIVE close/fence and absorption/handoff are explicit separate phases; failure after close leaves CLOSED_UNABSORBED selected truth.
5. RD-14 generator consumer checkpoint synchronizes exact ruleset-set digest across stale CORE prose and already-conforming launcher/generator surfaces.

No whole-wave barrier is added. RD count remains 14 and E1..E15 remain the closure topology.

## 8. Shipped-consumer reconciliation

### WP-13

```text
SAVE_CONTRACT.md      -> MODIFY under RD-06
PERSISTENCE.md        -> MODIFY under RD-06
DURABILITY_GUARD.md   -> CURRENT_CONFORMING / INSPECT
STORAGE.md            -> CURRENT_CONFORMING / INSPECT
ENGINE_UPDATES.md     -> CURRENT_CONFORMING / INSPECT
MULTIPLAYER.md        -> RD-09/WP-16 owner route; integration only from RD-06
LIVE_SCENE.md         -> RD-09/WP-16 owner route; integration only from RD-06
stale SAVE/hour/global-frontier tests -> DISCOVER + exact owner disposition
```

### WP-19

```text
BOOTSTRAP_RUNTIME.md  -> MODIFY exact --ruleset-set-sha256 generator prose
CAMPAIGN_SETUP.md     -> MODIFY exact --ruleset-set-sha256 generator prose
INSTALL/00_DND_BOOTSTRAP.md -> CURRENT_CONFORMING / PROTECT
TOOLS/init_campaign.py       -> CURRENT_CONFORMING / PROTECT
```

### WP-11 / Story

```text
GAME/CAMPAIGN/MANIFEST.yaml -> ADD static storage.story_root selector in RD-13 Story checkpoint
RD-14 generated scaffold -> PROVE selector preserved
```

The current package therefore no longer treats these shipped surfaces as implied cleanup.

## 9. Negative-law reconciliation

Repair preserves:
- one native semantic owner per domain;
- no second information/history/currentness/chronology/procedure authority;
- no global save frontier/clock/rollback transaction;
- no parallel publication journal;
- no alternate Git transport fallback;
- LIVE exact-source CAS distinct from campaign publication;
- storage baseline distinct from existing campaign runtime and campaign SAVE;
- candidate Dramaturg material non-authoritative before accepted publication;
- no Dramaturg registry/global agenda/scheduler/singleplayer durable planner;
- Story/Dramaturg remain derived/noncanonical where owner defines them so;
- no MANIFEST Story-progress/currentness authority;
- no fictional chronology from Git/ref/ID/list order;
- no reopening of CLOSED LIVE epoch after failed absorption;
- no campaign-base fallback while CLOSED_UNABSORBED source remains selected;
- no legacy v0.8 preservation constraint added under clean-slate v1.0 planning.

## 10. Currentness to repair-publication baseline

Fresh branch ref immediately before repair publication was:
```text
d01bd4bac55115408f6347f88214475855fbac0e
```

Compared with independent re-reviewed state:
```text
3626a7be398fb648d6e8f0d52fda63193f1b12a4
```
only the independent Senior re-review/control publication is present. No canonical owner/spec, GAME runtime artifact, DEV schema/catalog authority or decomposition authority changed.

The repair Source Manifest additionally fresh-read the exact owner specs and affected shipped consumers named in SIRR-001..005. No semantic owner supersession or human-owned decision gate was found.

This document is part of the repair publication itself. Exact post-publication HEAD/currentness is intentionally completed by the separate repair-closure checkpoint after read-back; this avoids self-referential SHA claims.

## 11. Planning Version Impact

All artifacts in the author repair publication are planning/control documentation. Version Impact for the planning checkpoint: **NONE**.

Future implementation workers must classify actual CORE/persistent-schema/runtime changes under the current version owner. In particular the Story selector must not be pre-classified here as compatible/incompatible before the actual schema delta is realized and tested.

## 12. Author reconciliation verdict before checkpoint publication

```text
DIRECT_READINESS: 116 / 116 ROUTED
PURE_PROOF: 9 / 9 ROUTED
COMPOSITE_PARENTS: 8 / 8 ROUTED
ACTIVE_CANONICAL_READINESS: 133 / 133 ACCOUNTED
TRIGGER_GATED: 12 / 12 PRESERVED
NO_WORK: 79 / 79 PRESERVED
R004: ABSENT

SIRR-001: REPAIRED IN PLANNING PACKAGE
SIRR-002: REPAIRED IN PLANNING PACKAGE
SIRR-003: REPAIRED IN PLANNING PACKAGE
SIRR-004: REPAIRED IN PLANNING PACKAGE
SIRR-005: REPAIRED IN PLANNING PACKAGE

SEMANTIC_OWNER_DRIFT_TO_PREPUBLICATION_HEAD: NONE FOUND
HUMAN_OWNED_DECISION_GATE: NONE
RUNTIME_IMPLEMENTATION_PROOF: NOT RUN / NOT AUTHORIZED
EXACT_POSTPUBLICATION_CURRENTNESS: PENDING REPAIR-CLOSURE CHECKPOINT
INDEPENDENT_SENIOR_RE_REVIEW: REQUIRED
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
