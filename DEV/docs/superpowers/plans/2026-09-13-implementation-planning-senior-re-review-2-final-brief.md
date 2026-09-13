# HDM Implementation Planning — Independent Senior Re-Review #2 Final Brief

Status: **READY FOR GENUINELY INDEPENDENT SENIOR RE-REVIEW #2 AFTER AUTHOR ADVERSARIAL REPAIR**
Date: 2026-09-13
Author repair checkpoint to challenge: `9bbad183dd8c82f281bf334940d25f8ba8131863`
Independent state that produced SIRR-001..005: `3626a7be398fb648d6e8f0d52fda63193f1b12a4`
Production implementation authorized: **NO**.

## Role

Act as a genuinely independent HDM Senior Implementation Plan Re-Reviewer. Do not repair the author package while reviewing. Every author PASS/closure statement is a claim to challenge.

The previous independent re-review returned `FAIL / REPAIR REQUIRED` with 0 BLOCKING, 4 SIGNIFICANT and 1 MINOR findings. The author then performed two additional adversarial self-review cycles and found five more SIGNIFICANT author defects (ASR-001..ASR-005). This review must independently determine whether the final current package is now worker-ready.

## Staged evidence / context-budget protocol

Do not bulk-read or recursively inspect the repository.

Start in this order:
1. fresh remote HEAD of `v1/engine-rearchitecture`;
2. `DEV/CURRENT_PROGRESS.md`;
3. current `AGENTS.md` and applicable ChatGPT Work runtime overlay;
4. this brief;
5. `2026-09-13-implementation-planning-independent-senior-re-review-result.md`;
6. `2026-09-13-implementation-planning-author-third-pass-self-review-closure.md`;
7. current `2026-09-13-implementation-planning-package-index.md`;
8. author finding records:
   - `2026-09-13-implementation-planning-author-self-review-findings.md`;
   - `2026-09-13-implementation-planning-author-second-pass-findings.md`;
9. current repair overlays in the exact precedence order from the package index;
10. current proof/currentness/scheduling artifacts routed by the package index.

Use `DEV/PROJECT_MAP.md` only as router. Open canonical owner/spec evidence only for an exact finding/duty, currentness drift, ambiguity, disagreement, authority-transfer risk or untraceable task.

## Currentness first

Compare repair checkpoint:
`9bbad183dd8c82f281bf334940d25f8ba8131863`
with fresh review HEAD.

The expected delta is closure/handoff control artifacts only. Independently inspect the changed-file list.

Also verify:
- `3626a7be... -> 9bbad183...` changed only independent-review/control/author planning artifacts and no semantic owner/runtime/schema authority;
- exact-head GitHub Actions validation on `9bbad183...`, run `34786332166`, completed successfully with both full maintenance audit and DEV unit tests green.

If canonical owner/runtime/schema drift exists, revalidate only the affected dependency subgraph. Material package-wide drift is a finding.

## Current worker-route composition

For every affected RD, apply the current package index exactly. Current overlay precedence is:

```text
base RD plan
-> SIRR repair overlay where applicable
-> first author self-review overlay where applicable
-> second-pass author overlay where applicable
```

Later overlays supersede only conflicting repaired detail. Do not review an affected base plan in isolation.

Review RD-01..RD-14 sequentially. Current `-v2` routes remain mandatory for RD-08/RD-10/RD-11.

## Finding challenge matrix

### SIRR-001 / ASR-003 — exact lossless proof semantics

Read canonical WP-12 §14 duties 1..17 and WP-13 §15 duties 1..38, then current v2 proof routes.

Verify semantic one-to-one binding. Specifically challenge:
- WP12-05 includes HOT/native establishment + accepted execution/ExecutionSegment + LIVE exact-source CAS;
- WP12-11 includes frozen publication/generation + trustworthy principal/authorization;
- WP13-19/20 prove the fixed **gameplay runtime** publication transport and negative no-fallback law, not merely development-agent process policy;
- row 38 dispositions agree with current root/persistence/bootstrap consumer analysis.

Numeric 17/38 equality is not proof.

### SIRR-002 / ASR-002 — retained Dramaturg publication and basis

Verify:
- exactly `DRAMATURG/SHARED.yaml` and `DRAMATURG/PLAYERS/<player_id>.yaml` retained families;
- candidate is non-authoritative until ordinary RD-06 campaign publication `ACCEPTED`;
- generation promotion only after acceptance;
- rejection/indeterminate behavior, exact-base reconciliation/rebase and fresh current-generation admission;
- player-local `shared_basis.kind = ABSENT | BOUND`;
- ABSENT does not fabricate shared generation;
- BOUND requires exact accepted shared generation;
- basis dependency changes rebuild a new generation;
- no single-player durable Dramaturg, registry, scheduler or second publication authority.

### SIRR-003 / ASR-001 / ASR-005 — shipped consumers, selectors and bootstrap

Read exact WP-11 fixed routes, WP-19 generator/bootstrap law and current versioning/clean-slate owner.

Verify current plan explicitly realizes:

```text
MANIFEST.storage:
  state_root
  index_root
  world_root
  event_log_root
  checkpoints_root
  sessions_root
  story_root
```

Check:
- `GAME/CAMPAIGN/MANIFEST.yaml` + `GAME/SCHEMA/campaign_manifest.schema.yaml` are explicit RD-04/WP-11 actions;
- local manifest schema `4 -> 5` is planned once;
- no unjustified campaign-contract/storage-generation bump or pre-release compatibility migration is manufactured;
- `STORAGE.md`, `BOOTSTRAP_RUNTIME.md`, `CAMPAIGN_SETUP.md`, `INSTALL/00_DND_BOOTSTRAP.md` have exact dispositions;
- `init_campaign.py` is protected as generic current-conforming template copier unless fresh body evidence disproves it;
- ruleset-set digest propagation remains exact;
- physical `SESSIONS/` blank-template root is distinguished from static `story_root`;
- blank New Game, provisional gameplay, READY_PC and PLAY_READY do **not** require physical Story/T0 files.

A static `story_root: STORY` selector may be valid before any Story projection is materialized.

### SIRR-004 / ASR-004 — Story static selector and exact physical routes

Verify topology ownership stays WP-11/RD-04 while Story semantics stay RD-13.

Exact current planned routes must be:

```text
<story_root>/<layer>/PROJECTION_STATE.yaml
<story_root>/<layer>/<floor(sequence/1000)>/<story_id>.yaml
```

for `TRANSCRIPT | EVENTS | MECHANICS | NARRATIVE`.

No worker-selected alternate projection-state path, partitioning, global index/allocator/frontier or chronology-from-sequence is allowed.

Story materializes on demand and remains noncanonical/gameplay-nonblocking.

### SIRR-005 — LIVE close vs later absorption

Verify two phases:

```text
A: ACTIVE -> CLOSED exact-source fence
B: normalize/handoff/publish/absorb
```

If B fails/indeterminate after A succeeds, exact final CLOSED source remains `CLOSED_UNABSORBED` selected truth with zero ordinary writers. No reopen and no campaign-base fallback.

## Sequential RD package executability

For each RD retain a compact result covering:
- exact files/actions;
- named RED cases;
- GREEN acceptance;
- REFACTOR boundary;
- focused VERIFY command;
- coherent green checkpoint;
- Version/System Impact classification;
- currentness fence;
- remaining material worker design choice, if any.

Specially re-evaluate RD-04/RD-06/RD-13/RD-14 after the new author repairs. RD-02/RD-09 must include SIRR-005 overlay. Unchanged RD routes may use the previous independent evidence unless currentness/delta gives a reason to broaden.

## SIP-001..SIP-011

Recompute the original SIP matrix. Do not inherit the author's third-pass labels.

At minimum independently challenge:
- SIP-002 surviving shipped consumers/root/schema surfaces;
- SIP-003 LIVE->information normalization and close/absorb interaction;
- SIP-006 native history/Story/T0/Commentator/Dramaturg;
- SIP-007 bootstrap/product, especially no Story startup requirement;
- SIP-008 current composed route executability;
- SIP-009 item-level proof semantics;
- SIP-010 dependency/scheduling after removal of the false root-selector->Story materialization barrier;
- SIP-011 executable maintenance command spelling.

## Canonical accounting / reverse coverage

Independently reconfirm:

```text
116 direct
9 pure proof
8 composite parents
= 133 active identities
12 trigger-gated outside current execution
79 no-work terminals
R004 absent
14 RD units
```

Then reverse-check current plans/overlays/proof routes. In particular verify:

```text
R064 -> RD-04 seven selectors/schema/STORAGE projection
R018.ROUTE_ROOT -> RD-04 static topology
R016.STORY/R018.STORY -> RD-13 exact Story route/lifecycle
R085/R131 -> RD-13 Dramaturg retained lifecycle/basis
R030/R086 -> RD-14 bootstrap consumers without Story startup dependency
R068/R071 -> exact proof routes
```

Report orphan work, double ownership, architecture invention or missing consumer.

## Protected invariants

Adversarially check at least:
- no second gameplay/knowledge/history/currentness/chronology authority;
- no global active player;
- no generic save frontier/journal/rollback transaction;
- LIVE CAS remains separate from campaign publication;
- physical presence/path/index cannot create semantic authority;
- Story is noncanonical and not a gameplay prerequisite;
- T0 is sparse conditional historical basis, not parallel history/startup requirement;
- Context Runtime remains ephemeral;
- Dramaturg remains bounded noncanonical retained multiplayer projection only;
- technical sequence/Git/ref/ID order never creates fictional chronology;
- no legacy v0.8 preservation constraint is reintroduced.

## Verdict and publication

Report exact `BLOCKING`, `SIGNIFICANT`, `MINOR` findings. Do not repair them.

Final verdict must be exactly one:
- `PASS / GO` — no unresolved BLOCKING or SIGNIFICANT defect and package execution-ready;
- `FAIL / REPAIR REQUIRED` — otherwise.

A PASS advances only the implementation execution gate; it does not itself execute implementation/migration/release/gameplay bootstrap.

Publish a new result under `DEV/docs/superpowers/plans/`, preferably:
`2026-09-13-implementation-planning-independent-senior-re-review-2-result.md`.

Update `DEV/CURRENT_PROGRESS.md` only according to that independent verdict.
