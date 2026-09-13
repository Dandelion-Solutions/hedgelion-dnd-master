# HDM Implementation Planning — Execution Waves SIRR Repair Addendum

Status: **CURRENT MANDATORY ADDENDUM TO PB-06 EXECUTION WAVES**
Date: 2026-09-13
Baseline: `d01bd4bac55115408f6347f88214475855fbac0e`
Production implementation authorized: **NO**.

Base scheduling authority remains `2026-09-13-implementation-planning-execution-waves.md` except where this addendum explicitly replaces or strengthens an edge/join after SIRR-001..SIRR-005 repair.

Wave numbers remain scheduling preferences only. This addendum creates no new semantic owner or RD unit.

## 1. Lossless proof route override

Every reference in the base execution-wave document to:
```text
2026-09-13-implementation-planning-lossless-proof-ledger.md
2026-09-13-implementation-planning-lossless-proof-ledger-wp12-wp13.md
```
for current execution is superseded by:
```text
2026-09-13-implementation-planning-lossless-proof-ledger-v2.md
2026-09-13-implementation-planning-lossless-proof-ledger-wp12-wp13-v2.md
```

The WP-14/15 and WP-16/17 appendices remain unchanged current routes.

## 2. EW-3 / E4 — RD-06 repaired completion

`R069 HARD_PRECEDES R070` remains unchanged.

R071 integration/proof completion now additionally requires:
- RD-06 shipped SAVE/publication consumer cutover from the mandatory SIRR repair amendments;
- all exact 38 WP-13 §15 rows in the v2 appendix;
- explicit current dispositions for `SAVE_CONTRACT`, `PERSISTENCE`, `DURABILITY_GUARD`, `STORAGE`, `ENGINE_UPDATES`, `MULTIPLAYER`, `LIVE_SCENE` and discovered stale tests;
- proof that campaign SAVE composition preserves LIVE exact-source CAS and storage-baseline independence.

This is an `INTEGRATION_COMPLETION_GATE`; it does not prevent owner-local RD-09 LIVE work from progressing independently.

## 3. EW-4 / E10 — Story selector closure

Existing E10 history/T0 semantics remain unchanged.

Add `SHARED_FILE_CHECKPOINT` / integration condition:
- RD-13 Story storage checkpoint publishes the canonical campaign-template `MANIFEST.storage.story_root` selector;
- RD-14 generator/scaffold checkpoint consumes the fresh template and proves the selector survives generated campaign materialization;
- neither RD creates a second Story currentness/progress owner in MANIFEST.

R051 and the STORY slices of R016/R018 cannot close before this static selector + generated-consumer join is green.

## 4. EW-4 / E11 — retained Dramaturg replacement

Replace the base E11 completion wording with:

```text
E11 — RETAINED DRAMATURG PUBLICATION / ADMISSION JOIN

Owner-local RD-13 candidate projection may begin from current WP-18/native-history inputs.
A candidate remains EPHEMERAL and is not a retained generation.

Before R085/R131 retained-horizon completion:
  RD-06 ordinary campaign publication operation/result
  + RD-09 current principal/PLAYER/currentness evidence
  + RD-10 current role/recipient containment
  + RD-12 current collaboration/player scope
  + RD-13 exact native continuity/history dependencies
  JOIN_BEFORE_INTEGRATION
  -> exact-published-base publication attempt
  -> accepted-generation promotion only after publication ACCEPTED
  -> current admission/rebase classification

Rejected or indeterminate publication does not promote a generation.
Base movement invokes bounded semantic rebase/rebuild/drop, never blind merge.
Player-local horizon additionally requires exact BOUND shared generation.
Disabled multiplayer makes retained horizons semantically INACTIVE_MODE; re-enable requires full fresh admission.
```

Only the two WP-18 retained families remain admitted:
```text
DRAMATURG/SHARED.yaml
DRAMATURG/PLAYERS/<player_id>.yaml
```

No planner publisher, global agenda, scheduler, MANIFEST Dramaturg selector or new transport is introduced.

Edge types:
- RD-06 campaign publication -> RD-13 retained-generation promotion: `JOIN_BEFORE_INTEGRATION`, not whole-RD `HARD_PRECEDES`;
- RD-09/RD-10/RD-12 owner-local cores may proceed independently; their current evidence joins only at publication/admission completion;
- R131 remains an `INTEGRATION_COMPLETION_GATE` over the retained multiplayer Dramaturg behavior.

## 5. EW-3/EW-4 LIVE close/absorb correction

The RD-09 lifecycle join is explicitly two-phase:
- Phase A `ACTIVE -> CLOSED` exact-source close/fence;
- Phase B normalization/native handoff/campaign absorption/route-away.

If Phase A succeeds and Phase B fails/indeterminate:
```text
state = CLOSED_UNABSORBED
selected current truth = exact final CLOSED source
ordinary writers = zero
campaign base fallback = forbidden
reopen closed epoch = forbidden
```

RD-02 information-normalization failure therefore blocks Phase B completion, not an already accepted Phase A close. This correction changes no WP-16 lifecycle state model and adds no new edge type.

## 6. EW-5 RD-14 generator consumer checkpoint

RD-14 Task 3 current completion additionally requires:
- fresh edits to stale `BOOTSTRAP_RUNTIME.md` and `CAMPAIGN_SETUP.md` generator-call prose;
- current-conforming protection tests for `INSTALL/00_DND_BOOTSTRAP.md` and `TOOLS/init_campaign.py`;
- exact `ruleset_set_sha256` propagation proof into MANIFEST created/current ruleset identity;
- generated-scaffold preservation of RD-13 `storage.story_root`.

This is a `SHARED_FILE_CHECKPOINT`/consumer join, not a new semantic prerequisite for unrelated bootstrap selection work.

## 7. EW-6 proof closure

EW-6 must consume v2 proof routes. In particular:
- R068 requires all exact 17 WP-12 rows;
- R071 requires all exact 38 WP-13 rows;
- R016/R018 require repaired Story selector/current consumer proof;
- R053 proof uses corrected CLOSED_UNABSORBED semantics;
- composite Version Impact proof includes the actual future Story-selector and CORE consumer version/schema classifications.

## 8. Topology reconciliation

After SIRR repair:
- RD count remains 14;
- E1..E15 remain the named integration/proof closure set;
- no whole-wave barrier is added;
- no existing accepted hard prerequisite is removed;
- one previously implicit dependency is now explicit: RD-13 retained Dramaturg **publication completion** consumes RD-06 ordinary campaign publication;
- this is a joined consumer dependency, not authority transfer and not a reason to serialize unrelated RD-13/RD-06 owner-local work.

## 9. Planning Version Impact

This addendum is planning-only. Version Impact: **NONE**.
