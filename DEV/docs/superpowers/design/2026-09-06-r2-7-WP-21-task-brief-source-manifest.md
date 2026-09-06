# R2.7 WP-21 Step 1 — Task Brief + Source Manifest + Whole-Project Critic

Status: **STEP 1 COMPLETE — WORKER CLOSURE CANDIDATE — MANDATORY INDEPENDENT SENIOR REVIEW PENDING**

Date: 2026-09-06

Starting evidence basis: `7e1f09878f770b95467071a51389e211ad2d5495`.

Domain: **Diagnostics, observability, cleanup and retirement**.

This artifact owns the WP-21 Step-1 framing/evidence/critic checkpoint only. It does not authorize Step 2, WP-22, implementation planning, substantive implementation, runtime migration or gameplay bootstrap.

---

## 1. Task brief

WP-21 asks whether the whole project already has a coherent, bounded maintainer/support surface for:

1. useful diagnostics without hidden-chain-of-thought dependence;
2. cleanup/retirement across obsolete representations;
3. blocker/currentness proof before irreversible current-state loss;
4. rebuild/repair of derivative Story/planning/index/cache state;
5. support/maintenance actions that do not become gameplay authority or bypass privilege/disclosure boundaries.

The default posture is reconciliation, not invention. Closed owners are not reopened merely because WP-21 overlaps their subject matter.

### Non-goals

WP-21 Step 1 does not create:

- a generic observability subsystem;
- a universal GC graph/frontier/job queue;
- a new repair authority;
- permanent hidden LLM reasoning storage;
- a branch/ref deletion subsystem;
- a Connector deletion capability probe;
- a manual/native-Git/private-HTTP deletion fallback;
- a new Story/planning authority;
- a new global support/admin privilege system;
- implementation code or runtime schema changes.

Fixed Product Owner policy: physical Git branch/ref deletion is outside HDM automation. Logical retirement/de-authorization/de-routing is sufficient and physical refs may remain indefinitely.

---

## 2. Source Manifest

### A. Process / current authority

- `AGENTS.md`
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/PROJECT_MAP.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`
- `DEV/CURRENT_PROGRESS.md`
- `DEV/PRODUCT_OWNER_INPUT.md`

### B. Diagnostic / execution / role-containment owners

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md`

Coverage purpose: deterministic/runtime evidence, bounded context eligibility, role separation, diagnostic/support degradation and no requirement to preserve private hidden reasoning as an authority surface.

### C. Retention / cleanup / currentness owners

- `DEV/docs/superpowers/specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-10-story-projection-durability-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md`
- `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-09-06-hdm-publication-currentness-supported-ref-repair-amendment.md`
- `DEV/docs/superpowers/specs/2026-09-06-hdm-branch-ref-deletion-prohibition-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-09-06-step-5-13-logical-ref-retirement-canonical-amendment.md`

Coverage purpose: publication/currentness proof, native-owner terminality, survivor-before-removal, bounded blocker contracts, conservative retention, checkpoint/Story/chronology/text/disclosure retention, logical ref retirement and separation from Git object reclamation.

### D. Story / planning / derivative rebuild owners

- `DEV/docs/superpowers/specs/2026-08-21-step-5-10-story-projection-durability-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-canonical-spec.md`

Coverage purpose: derivative Story/planning/index/cache state remains rebuildable/routing-oriented and cannot silently become truth authority merely because a repair/maintenance path uses it.

### E. Privilege / multiplayer / support-safety owners

- `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-canonical-spec.md`

Coverage purpose: maintenance/support visibility and action do not imply creator/player/gameplay authority and do not bypass disclosure/control eligibility.

### F. Post-WP-20 repair/status evidence

- `DEV/docs/superpowers/design/2026-09-06-whole-project-audit-repair-task.md`
- `DEV/docs/superpowers/design/2026-09-06-whole-project-audit-repair-closure.md`
- `DEV/docs/superpowers/design/2026-09-06-whole-project-audit-repair-senior-review.md`
- `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md`

Coverage purpose: R1-R4 are already independently Senior-PASSed; WP-21 must consume that closed state rather than reopen it.

---

## 3. Evidence coverage matrix

| Route | Current evidence result | WP-21 disposition |
|---|---|---|
| diagnostic evidence without hidden CoT | Existing execution/context/role/assurance owners provide structured/deterministic evidence surfaces; hidden model reasoning is not a required authority artifact | SATISFIED — no new CoT/telemetry owner |
| retirement across obsolete families | Step 5.13 provides owner-gated retirement across runtime/message/checkpoint/Story/chronology/disclosure/live families | SATISFIED after F21-01 ref-retirement reconciliation |
| blocker/currentness proof | Step 5.13 closed blocker/protection model + Step 5.6/WP-13/R1 publication currentness provide bounded proof/fail-closed movement handling | SATISFIED |
| derived Story/planning/index/cache rebuild/repair | Step 5.10, R2.1, WP-11 and WP-18 keep derivative state rebuildable/non-authoritative under current owners | SATISFIED |
| support surfaces non-authoritative / privilege-safe | Step 5.12, Step 5.8, WP-16/WP-17 preserve disclosure/control/authority separation | SATISFIED |

No missing consumer requires a new generic WP-21 subsystem at Step 1.

---

## 4. Whole-project critic

### F21-01 — BLOCKER — Step-5.13 physical ref-delete model conflicts with fixed PO policy

Evidence:

- Step 5.13 still described optional `RepositoryPort DeleteRef`, `CAPABILITY_DEFERRED`, ambiguous delete verification/retry, future capability re-check, machine debt and regression cases for deletion.
- Current supported GitHub Connector has no branch/ref-delete command.
- Product Owner policy explicitly forbids HDM from designing, probing, invoking, retrying or substituting an out-of-band deletion path.

Root cause: the older Step-5.13 platform assumption was never reconciled after the later fixed Product Owner policy.

Repair:

- `DEV/docs/superpowers/specs/2026-09-06-step-5-13-logical-ref-retirement-canonical-amendment.md` supersedes only the physical-ref-deletion assumptions.
- Ref retirement is now logical de-authorization/de-routing only.
- Physical ref existence is explicitly non-authoritative and may persist indefinitely.
- Delete capability probing/invocation/retry/manual fallback is removed from current HDM automation debt/tests.
- `DEV/TESTS/test_branch_ref_retirement_policy.py` adds a current-contract regression guard.

Worker disposition: **REPAIRED / SENIOR CONFIRMATION REQUIRED**.

### F21-02 — SIGNIFICANT — publication/currentness R1 amendment had stale review status

Evidence:

- R1 amendment header still projected `MANDATORY SENIOR REPAIR REVIEW PENDING`.
- `DEV/docs/superpowers/design/2026-09-06-whole-project-audit-repair-senior-review.md` records `FINAL SENIOR REVIEW PASS`, including `R1_PUBLICATION_CURRENTNESS_PROOF: PASS`.

Repair:

- R1 amendment status synchronized to `CANONICAL — FINAL SENIOR REVIEW PASS` with exact review provenance.
- No R1 semantic law was changed.

Worker disposition: **REPAIRED / STATUS-ONLY**.

### Other routes

No additional blocking/significant gap was established. Overlap alone is not evidence to reopen accepted architecture.

```text
F21-01: REPAIRED — SENIOR CONFIRMATION REQUIRED
F21-02: REPAIRED — STATUS ONLY
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_WHOLESALE_REOPEN_REQUIRED: NO
```

These are worker-side dispositions, not an independent Senior PASS.

---

## 5. Version Impact Gate

Step-1 changes are development architecture/status/tests only. They do not change a GAME runtime module, persistent/protocol schema, engine release identity, campaign/storage/catalog generation, ruleset package identity or compatibility-bearing namespace.

```text
VERSION_IMPACT: VERIFIED
VERSION_BUMP_REQUIRED: NO
VERSION_IMPACT_DISPOSITION: NONE
VERSIONING_TAXONOMY_REOPENED: NO
```

---

## 6. Exit / mandatory gate

WP-21 Step 1 worker package is complete when this artifact, the logical-ref-retirement amendment, the R1 status synchronization and their regression coverage are published and exact-head verification passes.

The next gate is mandatory and independent:

```text
NEXT_ELIGIBLE_UNIT: MANDATORY SENIOR WP-21 STEP-1 REVIEW
NEXT_AUTHORIZED_UNIT: NONE
WP21_STEP2_AUTHORIZED: NO
WP22_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
```

The current worker context does not self-pass that gate.
