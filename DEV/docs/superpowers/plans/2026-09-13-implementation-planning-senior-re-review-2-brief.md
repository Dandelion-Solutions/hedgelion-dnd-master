# HDM Implementation Planning — Independent Senior Re-review #2 Brief

Status: **READY FOR GENUINELY INDEPENDENT SENIOR RE-REVIEW #2**
Date: 2026-09-13
Author SIRR repair checkpoint: `87941ed63028efea71eb38e03375573e31a70be2`.
Independent re-reviewed state that produced SIRR-001..005: `3626a7be398fb648d6e8f0d52fda63193f1b12a4`.
Production implementation authorized: **NO**.

## Role

Act as a genuinely independent HDM Senior Implementation Plan Re-Reviewer. Do not repair the package while reviewing. Author disposition/closure statements are claims to challenge, not authority for PASS.

The previous independent re-review returned `FAIL / REPAIR REQUIRED` with 0 BLOCKING, 4 SIGNIFICANT and 1 MINOR findings. This review must first determine whether those exact five findings are actually closed, then revalidate package-wide execution readiness sufficiently to issue a new independent verdict.

## Staged evidence / context-budget protocol

Do not bulk-read the HDM corpus and do not recursively inspect the repository.

Start in this order:
1. fresh remote HEAD of `v1/engine-rearchitecture`;
2. `DEV/CURRENT_PROGRESS.md`;
3. current `AGENTS.md` and applicable runtime overlay;
4. this brief;
5. `2026-09-13-implementation-planning-independent-senior-re-review-result.md` — exact SIRR-001..005 findings;
6. `2026-09-13-implementation-planning-senior-re-review-repair-closure.md`;
7. `2026-09-13-implementation-planning-package-index.md`;
8. `2026-09-13-implementation-planning-senior-re-review-repair-disposition.md`;
9. `2026-09-13-implementation-planning-sirr-repair-amendments.md`;
10. repaired proof, execution-wave and coverage artifacts routed by the package index.

Use `DEV/PROJECT_MAP.md` only as a router. Open canonical owner/spec evidence only for the exact finding/duty under test or when drift/disagreement/ambiguity/authority-transfer risk requires escalation.

Review current routed RD-01..RD-14 sequentially from the package index. For affected RDs, the route is the base plan **plus** the mandatory SIRR amendments. Do not silently review only the old base file.

## Currentness first

Compare author repair checkpoint:
`87941ed63028efea71eb38e03375573e31a70be2`
with fresh review HEAD before substantive review.

Expected closure-only delta should be limited to current-progress/master/index/review-control artifacts. Independently verify that expectation.

- Control-only delta -> record `NO_SEMANTIC_OWNER_DRIFT` and continue.
- Canonical owner/runtime/schema drift -> revalidate only the affected dependency subgraph.
- Material package-wide drift -> issue a currentness finding instead of reviewing stale routes exhaustively.

Also verify the repair checkpoint itself changed only the six planning artifacts claimed by the author and that exact-head GitHub Actions validation succeeded; do not accept those claims without Connector evidence.

## SIRR-001 — exact WP-12/WP-13 proof semantics

Severity previously: SIGNIFICANT.
Affected: R068, R071, SIP-009, package proof closure.

Read exact canonical WP-12 §14 duties 1..17 and WP-13 §15 duties 1..38. Then read:
- `2026-09-13-implementation-planning-lossless-proof-ledger-v2.md`;
- `2026-09-13-implementation-planning-lossless-proof-ledger-wp12-wp13-v2.md`.

Verify **semantic one-to-one binding**, not row counts:
- all 17 WP-12 duties are present once, with correct supporting target, named executable witness and admissible primary channel;
- all 38 WP-13 duties are present once under the same standard;
- positive and negative/failure semantics are executable where the owner requires them;
- storage baseline remains separate from HOT/campaign SAVE authority;
- LIVE exact-source CAS remains separate from campaign publication;
- no generic journal/global frontier/alternate transport authority is introduced;
- row 38 has explicit shipped-consumer/test disposition rather than a generic stale-search assertion.

A 17/38 numeric match with wrong semantics is FAIL.

## SIRR-002 — retained Dramaturg publication/admission/rebase

Severity previously: SIGNIFICANT.
Affected: R085, R131, SIP-006/SIP-008, E11.

Read only the applicable retained-Dramaturg WP-18 sections, then the RD-13 base plan + mandatory amendments + execution-wave addendum.

Verify worker-ready executable behavior for:
- ephemeral candidate before publication;
- exact current published base/generation freeze;
- ordinary RD-06 campaign publication as the remote mutation boundary, with no RD-13 transport/publisher authority;
- generation promotion only after ACCEPTED publication;
- rejected/indeterminate behavior and preservation/staleness classification of prior retained generation;
- semantic conflict rebase/rebuild/drop against current retained/native basis, never blind text merge;
- shared horizon current multiplayer/principal/player/role/currentness/native-dependency checks;
- player-local exact player/recipient/control + exact BOUND shared generation;
- inactive mode semantics and full revalidation on re-enable;
- named RED/GREEN focused tests and coherent checkpoint.

Confirm E11 expresses RD-06 publication as a joined consumer dependency rather than serializing unrelated owner-local work or transferring authority.

## SIRR-003 — shipped-consumer cutover

Severity previously: SIGNIFICANT.
Affected: R071, R086, SIP-002/SIP-008.

### WP-13 / RD-06

Read WP-13 shipped-consumer requirements, current RD-06 base plan + repair amendments and only these current shipped consumers unless a concrete contradiction requires more:
- `GAME/CORE/SAVE_CONTRACT.md`;
- `GAME/CORE/PERSISTENCE.md`;
- `GAME/CORE/DURABILITY_GUARD.md`;
- `GAME/CORE/STORAGE.md`;
- `GAME/CORE/ENGINE_UPDATES.md`;
- `GAME/CORE/MULTIPLAYER.md`;
- `GAME/CORE/LIVE_SCENE.md`.

Verify each receives an explicit action/disposition and that:
- SAVE_CONTRACT replacement is native-domain composition, not universal campaign-only SAVE;
- PERSISTENCE has executable frozen-attempt/outcome/reconciliation/G-specific currentness work;
- current-conforming consumers are protected by currentness evidence rather than gratuitous edits;
- LIVE-owned files stay RD-09/WP-16-owned;
- stale tests are discovered/dispositioned by semantic assertion, not assumed absent or rewritten blindly.

### WP-19 / RD-14

Read WP-19 exact generator identity requirement and current:
- `GAME/CORE/BOOTSTRAP_RUNTIME.md`;
- `GAME/CORE/CAMPAIGN_SETUP.md`;
- `GAME/INSTALL/00_DND_BOOTSTRAP.md`;
- `GAME/TOOLS/init_campaign.py`;
- RD-14 base plan + repair amendments.

Verify stale CORE consumers have explicit `ruleset_set_sha256` modification/test routes while already-conforming launcher/generator surfaces are protected by tests rather than no-op churn.

## SIRR-004 — static Story storage selector

Severity previously: SIGNIFICANT.
Affected: R051, R016/R018 STORY slices, R102 consumer path, SIP-006/SIP-008.

Read applicable WP-11/WP-18 Story topology clauses, current `GAME/CAMPAIGN/MANIFEST.yaml`, RD-13 base plan + amendments and RD-14 scaffold consumer route.

Verify:
- exact `storage.story_root: "STORY"` template action is named;
- Story storage tests prove routing through selector;
- mutable Story progress does not move into MANIFEST/CURRENT/RRC;
- no Dramaturg root selector is invented;
- generated campaign preservation is tested by RD-14;
- clean-slate v1.0 does not manufacture legacy v0.8 preservation/migration work.

## SIRR-005 — close vs absorption semantics

Severity previously: MINOR.
Affected: RD-02/RD-09 R053/WP-16 integration wording.

Read exact WP-16 close/CLOSED_UNABSORBED/absorption clauses and the RD-02/RD-09 base plans + repair amendments.

Verify:
- `ACTIVE -> CLOSED` fence can succeed independently;
- failed/indeterminate normalization or campaign absorption after close leaves exact final CLOSED source as `CLOSED_UNABSORBED` current truth with zero ordinary writers;
- no campaign-base fallback;
- no reopening of closed source;
- only absorption/route-away remains blocked/retryable;
- tests exercise close-success + Phase-B failure/indeterminate + later successful absorption from same final source.

Do not invent a new lifecycle state to fix wording.

## Full SIP/package regression check

After SIRR-specific review, revalidate all SIP-001..SIP-011 dispositions at the smallest sufficient evidence scope. Previously closed findings may be sampled from their current routes unless SIRR repair or currentness creates a concrete interaction risk. SIP-008/SIP-009 require full current route/proof completeness checks.

Sequentially review current RD-01..RD-14. For each record compactly:
- admitted readiness/slices;
- exact base plan + mandatory overlay if any;
- Impact Envelope exactness;
- named RED cases;
- GREEN interfaces/acceptance;
- REFACTOR boundary;
- focused VERIFY command;
- coherent passing checkpoint;
- Version/System Impact gate;
- currentness fence;
- unresolved material worker design choices.

Any unresolved human/material design choice = finding. Worker-local naming/implementation detail within accepted contracts is not automatically a defect.

## Canonical accounting / reverse coverage

Independently reconfirm:
```text
116 direct
9 pure proof
8 composite parents
= 133 active
12 trigger-gated outside current execution
79 explicit no-work
R004 absent
14 RD units
```

Then reverse-check all current executable tasks, proof routes and execution-wave addendum. Every task must trace to admitted readiness/slice, owner-valid integration join, proof obligation, version/projection consequence or required validation/currentness evidence. Report orphan work or architecture invention.

## Protected invariants

Adversarially check at least:
- no second gameplay/information/history/currentness/chronology/procedure authority;
- eligibility before semantic use;
- ranking cannot override authority/eligibility/requiredness;
- no global active player or global SAVE/currentness frontier;
- no generic publication journal or alternate transport;
- LIVE exact-source CAS remains owner-native;
- Story remains noncanonical projection; T0 remains sparse native historical basis rather than parallel history;
- retained Dramaturg is bounded derivative multiplayer horizon and never a generic planner;
- Context Runtime remains ephemeral;
- Git/ref/ID/list order never creates fictional chronology;
- positive material dependency precedes scope-local waiting;
- catch-up is recipient projection;
- GAME clean-slate v1.0 policy does not preserve legacy v0.8 by accident.

## Verdict and publication

Report itemized `BLOCKING`, `SIGNIFICANT`, `MINOR` findings with exact evidence. Do not silently repair.

Final verdict exactly one:
- `PASS / GO` — no unresolved BLOCKING or SIGNIFICANT defect and package is worker-ready;
- `FAIL / REPAIR REQUIRED` — otherwise.

A PASS advances only to the production implementation execution gate. It does not itself perform implementation, migration, release or gameplay bootstrap.

Publish a new result, preferably:
`DEV/docs/superpowers/plans/2026-09-13-implementation-planning-independent-senior-re-review-2-result.md`
containing review HEAD/baseline, currentness, SIRR matrix, SIP matrix, sequential RD status, lossless proof result, dependency/reverse-coverage result, findings, final verdict and exact next authorized unit.

Update `DEV/CURRENT_PROGRESS.md` only according to the independent verdict. The re-review is complete only when the reviewer has independently proved or disproved all five SIRR repairs and package execution readiness under current owners.
