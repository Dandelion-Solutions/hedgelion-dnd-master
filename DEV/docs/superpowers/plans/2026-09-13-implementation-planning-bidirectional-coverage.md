# HDM Implementation Planning — Bidirectional Coverage / Currentness Closure

Status: **AUTHOR REPAIR RECONCILIATION — PLAN-LEVEL COVERAGE PASS / INDEPENDENT RE-REVIEW REQUIRED**
Date: 2026-09-13
Canonical readiness authority: WP-27 final implementation-planning readiness.
Lossless proof authority: `2026-09-13-implementation-planning-lossless-proof-ledger.md` plus its WP-12/13, WP-14/15 and WP-16/17 appendices.
Currentness basis before this publication: `c616d408d8889c566a2ddd244ee7b49d7f8c9d01`.
Independent reviewed baseline: `38f4eb527fbbbd3a03e92aed4bf1e7315346cd21`.
Production implementation authorized: **NO**.

This repair separates identity/accounting coverage from executable proof routing. A readiness identity may be fully mapped while its future runtime proof has not been executed. Nothing in this document claims implementation PASS.

## 1. Canonical accounting

Exactly 133 active readiness identities are represented by exactly one canonical planning form:

```text
DIRECT: 116
PURE_PROOF: 9
COMPOSITE_PARENTS: 8
TOTAL_ACTIVE: 133
```

External disjoint sets remain excluded from current implementation execution:
- 12 trigger-gated readiness leaves remain dormant under their recorded triggers;
- 79 explicit no-work terminals remain terminals;
- R004 remains absent.

No slice/test/theme row is counted as an additional readiness identity.

## 2. Forward identity map — direct readiness -> current routed RD

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

Accounting result: 116 direct identities, no duplicate direct assignment, no direct identity missing from the accepted decomposition.

Important mixed-leaf rule: direct assignment does not imply one-RD completion. Examples include R077, whose identity is assigned to RD-08 but whose WP-15 §13.9–17 completion is an explicit cross-owner join; R080, whose current machine/scenario duties 1–21 are planned while measured duty 22 remains `EMPIRICAL_DEFERRED`; and R071/R074/R083, whose enumerated proof themes are governed item-by-item by the lossless ledger.

## 3. Forward proof map — pure-proof readiness

The nine pure-proof identities remain readiness identities but do not create production subsystems:

```text
R023 -> Stage3PackageProofTests over applicable owner-family targets
R031 -> ActorReadinessProofTests over RD-03 + RD-14
R032 -> DomainCommitmentProofTests over RD-03 + RD-14; real-target performance branch EMPIRICAL_DEFERRED
R041 -> ExecutionRetryProofTests over RD-05/RD-07/RD-08 and applicable durability/LIVE joins
R058 -> RoleContainmentProofTests over RD-10/RD-11; empirical protocol branch dormant until trigger
R061 -> ContextBoundednessProofTests over RD-11; supported-target empirical evaluation dormant until trigger
R068 -> Wp12HotProofTests, all 17 WP-12 §14 themes itemized in WP-12/WP-13 appendix
R088 -> OwnerFirstReconciliationProofTests
R089 -> ProofChannelDisciplineTests + exact-head HOSTED_CI evidence
```

Planning result: 9/9 identities have explicit proof routes and channel discipline. Runtime result: **NOT RUN / NOT AUTHORIZED**.

Schema existence, a maintenance-audit PASS, full unittest discovery or hosted CI cannot substitute for a behavior/integration/empirical channel required by the owning row.

## 4. Forward map — composite parents and required package witnesses

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

Every composite parent additionally requires `CompositeVersionImpactProofTests` over the combined sibling deltas, negative authority-transfer assertions and no half-migrated consumer/projection. Slice PASS labels alone cannot close a parent.

Planning result: 8/8 parents have complete slice maps + package witnesses + parent Version Impact route. Runtime result: **NOT RUN / NOT AUTHORIZED**.

## 5. Enumerated mixed-proof suites

The following direct leaves have item-level owner suites and therefore cannot close from a thematic RD summary:

```text
R071 -> WP-13 §15 items 1..38 -> Wp13DurabilityProofTests
R074 -> WP-14 §15 items 13..25 -> Wp14RecoveryProofTests
R077 -> WP-15 §13 items 9..17 -> Wp15TemporalProofTests
R080 -> WP-16 §15 items 1..21 current + item 22 EMPIRICAL_DEFERRED -> Wp16LiveAccessProofTests
R083 -> WP-17 §28 themes 1..26 -> Wp17CollaborationProofTests
R099 -> T0HistoricalBasisProofTests; real-target critical-path observation remains trigger-gated
R102 -> CommentatorSelfContainedProofTests
```

R068's 17 WP-12 themes and R071's 38 WP-13 themes, R074's 13 WP-14 themes, R077's 9 WP-15 themes, R080's 22 WP-16 duties and R083's 26 WP-17 themes are preserved losslessly in the three appendices. Missing one item-level witness is RED at implementation time; aggregation may not erase it.

## 6. Reverse map — current plan/task -> admitted work

Current executable routing is defined by `2026-09-13-implementation-planning-package-index.md`. It exposes one worker route for each RD-01..RD-14; superseded non-v2 RD-08/RD-10/RD-11 files are provenance only.

Reverse-scope law:
- every implementation-bearing task must close a named direct readiness obligation, composite slice, owner-valid integration join, itemized proof obligation, mandatory projection/version/checkpoint/migration consequence, or focused verification/currentness requirement;
- proof-only tasks live in the package proof target and cannot create gameplay/runtime authority;
- audit/project-map/docs edits are projections of admitted owner work, not new readiness;
- execution-wave number is scheduling preference only and creates no semantic prerequisite;
- `SHARED_FILE_CHECKPOINT` coordinates overlapping physical writes without creating semantic ownership/dependency;
- trigger-gated 12 remain dormant and the 79 no-work terminals remain untouched.

Author reverse review result: no orphan executable semantic task and no new readiness identity introduced. Exact fresh worker file choice remains constrained by each RD Impact Envelope/currentness fence; semantic drift returns to planning rather than being improvised.

## 7. Dependency/scheduling reconciliation

`2026-09-13-implementation-planning-execution-waves.md` now separates:

```text
HARD_PRECEDES
JOIN_BEFORE_INTEGRATION
INTEGRATION_COMPLETION_GATE
SHARED_FILE_CHECKPOINT
SCHEDULING_PREFERENCE
PROOF_AFTER_TARGET
CONSTRAINS_WITHOUT_ORDERING
```

This removes the old false implication that whole wave numbers are total barriers. In particular:
- RD-02/RD-03 shared `pc/npc/item` writes are ordered only as a shared-file checkpoint;
- RD-04/RD-02 `location.schema.yaml` writes are similarly coordinated without ownership transfer;
- RD-09 access/LIVE core may begin independently of unrelated RD-06/RD-07 completion;
- RD-10, RD-11, RD-12 and RD-13 owner-local cores are parallel roots where no exact edge/file collision says otherwise;
- RD-11/RD-12 core work is not cyclic: R124 is the later integration-completion join;
- composite/proof closure waits only at the named package joins.

E1..E15 remain named integration/proof closure points; their semantics are now edge-typed rather than inferred from wave number.

## 8. SIP-011 executable command reconciliation

All 14 **current routed** RD plans were read after repair. Every executable maintenance-audit invocation uses:

```bash
python3 DEV/TOOLS/run_maintenance_audit.py
```

Historical architecture/provenance documents may still use `DEV/TOOLS/run_maintenance_audit` as the canonical entry-point name; they are not current worker execution commands and are not rewritten merely for SIP-011.

Current-route command audit: **CLEAN**.

## 9. Currentness proof

Independent Senior reviewed baseline:
`38f4eb527fbbbd3a03e92aed4bf1e7315346cd21`.

Pre-publication repair cursor:
`c616d408d8889c566a2ddd244ee7b49d7f8c9d01`.

Connector compare result:
```text
status: ahead
ahead_by: 30
behind_by: 0
```

The complete changed-file list for that interval was inspected. Every changed file is either:
- `DEV/CURRENT_PROGRESS.md`; or
- an implementation-planning/review/control artifact under `DEV/docs/superpowers/plans/**`.

No canonical spec, `GAME/**` runtime artifact, `DEV/SCHEMAS/**`, catalog, architecture owner or decomposition authority changed in the interval. Therefore the repair did not create an owner-currentness/redecomposition trigger. Owner-specific currentness rereads performed while repairing RD-05/RD-07/RD-08/RD-09/RD-12 and proof suites found no semantic owner supersession requiring architecture reopen.

This publication itself changes only this planning reconciliation artifact; final repair closure must fresh-check the new HEAD again before handing off.

## 10. Negative-law reconciliation

The repaired package still preserves the accepted invariants, including:
- no second gameplay, information, history, currentness, chronology or Procedure authority;
- eligibility precedes semantic use;
- ranking cannot override authority, eligibility or requiredness;
- TurnEnvelope/control metadata is not authority;
- physical presence is not eligibility/agency/authorization;
- late steering is non-authoritative;
- only validated Narrator payload crosses protected emission;
- sanitization is defense-in-depth only;
- no global active player;
- positive material dependency precedes scope-local waiting;
- join/rejoin establishes current frontier before mutation;
- catch-up is recipient projection;
- Story/Dramaturg remain noncanonical;
- T0 is sparse native historical basis, not parallel history;
- Context Runtime remains ephemeral projection;
- Agenda/index/current summaries remain derivative/non-authoritative;
- technical/CAS/Git/ID/list order never creates fictional chronology;
- maintenance diagnostics/audit do not install a second gameplay/command authority.

## 11. Author reconciliation verdict

```text
PLANNING_IDENTITY_COVERAGE:
    DIRECT 116 / 116 PASS
    PURE_PROOF IDENTITIES 9 / 9 ROUTED
    COMPOSITE_PARENTS 8 / 8 ROUTED
    ACTIVE_CANONICAL_READINESS 133 / 133 ACCOUNTED

LOSSLESS_EXECUTION_PROOF_ROUTING:
    PURE-PROOF ROUTES PRESENT
    ENUMERATED OWNER-SUITE ROWS PRESERVED ITEM-BY-ITEM
    COMPOSITE PACKAGE WITNESSES PRESENT
    COMPOSITE VERSION-IMPACT WITNESS PRESENT
    FUTURE EMPIRICAL / RELEASE TRIGGERS PRESERVED DORMANT
    PLAN-LEVEL RESULT: PASS

REVERSE_TASK_SCOPE: PASS — AUTHOR RECONCILIATION
SCHEDULING_EDGE_SEMANTICS: PASS — AUTHOR RECONCILIATION
CURRENT_ROUTE_AUDIT_COMMANDS: PASS
CURRENTNESS_TO_PREPUBLICATION_CURSOR: PASS

RUNTIME_IMPLEMENTATION_PROOF: NOT RUN / NOT AUTHORIZED
HOSTED_CI_FOR_FINAL_REPAIR_HEAD: PENDING FINAL CLOSURE PUBLICATION
INDEPENDENT_SENIOR_RE-REVIEW: REQUIRED / NOT YET PERFORMED
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```

This is an author-side planning reconciliation only. It does not convert planned witnesses into runtime PASS and does not authorize production implementation. Independent Senior re-review must recompute currentness, lossless proof routing, executable worker readiness and closure before any implementation GO.