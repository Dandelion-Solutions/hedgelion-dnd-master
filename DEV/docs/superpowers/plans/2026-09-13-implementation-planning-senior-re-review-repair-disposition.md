# HDM Implementation Planning — Senior Re-Review Repair Disposition

Status: **AUTHOR REPAIR DISPOSITION — SIRR-001..SIRR-005**
Date: 2026-09-13
Baseline remote HEAD: `d01bd4bac55115408f6347f88214475855fbac0e`
Production implementation authorized: **NO**.

This artifact dispositions only the five findings from the genuinely independent Senior re-review. It does not reopen the critic-approved bounded decomposition or accepted semantic architecture.

## 1. Source Manifest

| Source | Authority / role | Repair use |
|---|---|---|
| `AGENTS.md` | repository process authority | Connector-only transport, Superpowers, coherent publication, no duplicate approval gate |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | runtime transport overlay | non-force Git-data checkpoint protocol |
| `DEV/DESIGN_PROCESS.md` | design process owner | evidence/synthesis completeness and Source Manifest |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | architecture process owner | accepted-owner discipline, no gratuitous reopening |
| `DEV/PROJECT_MAP.md` | routing map | bounded owner discovery only |
| `DEV/CURRENT_PROGRESS.md` | current global gate | author repair SIRR-001..005 is the only authorized work |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | active roadmap | Implementation Planning remains active after R2.7 closure |
| `2026-09-13-implementation-planning-candidate-bounded-decomposition-v2.md` | critic-approved decomposition | RD-01..RD-14 topology remains accepted |
| `2026-09-13-implementation-planning-independent-senior-re-review-result.md` | independent review authority | exact SIRR-001..SIRR-005 findings and severity |
| WP-11 canonical spec | storage topology owner | `MANIFEST.storage.story_root` requirement |
| WP-12 canonical spec | HOT/transaction owner | exact 17 §14 proof duties |
| WP-13 canonical spec | durability/SAVE/publication owner | exact 38 §15 proof duties and shipped-consumer cutover |
| WP-16 canonical spec | LIVE/access owner | close/fence vs CLOSED_UNABSORBED/absorption semantics |
| WP-18 canonical spec | Story/Dramaturg owner | retained Dramaturg publication/admission/rebase semantics |
| WP-19 canonical spec | bootstrap owner | exact generator identity propagation including `ruleset_set_sha256` |
| `DEV/RELEASE/VERSIONING.md` | version-impact owner | planning-only repair has no runtime/schema generation impact |
| current RD-02/RD-06/RD-09/RD-13/RD-14 plans | executable planning routes | bounded amendments only |
| current `GAME/CORE/SAVE_CONTRACT.md`, `PERSISTENCE.md`, `DURABILITY_GUARD.md`, `STORAGE.md`, `ENGINE_UPDATES.md`, `MULTIPLAYER.md`, `LIVE_SCENE.md` | shipped consumers | exact WP-13 disposition |
| current `GAME/CORE/BOOTSTRAP_RUNTIME.md`, `CAMPAIGN_SETUP.md`, `GAME/INSTALL/00_DND_BOOTSTRAP.md`, `GAME/TOOLS/init_campaign.py`, `GAME/CAMPAIGN/MANIFEST.yaml` | shipped bootstrap/scaffold consumers | exact WP-19/WP-11 drift check |

Currentness comparison from independent reviewed state `3626a7be398fb648d6e8f0d52fda63193f1b12a4` through repair baseline `d01bd4bac55115408f6347f88214475855fbac0e` shows only the independent re-review/control publication. No canonical spec, GAME runtime owner, schema/catalog owner or accepted decomposition changed. Therefore this repair is bounded plan correction, not architecture reopening.

## 2. Finding dispositions

### SIRR-001 — SIGNIFICANT — R068/R071 proof semantics

**Accepted.** The existing WP-12/WP-13 proof appendix preserved row counts but did not bind each row to the exact canonical semantic duty. Row-count equality is insufficient.

Repair:
- supersede the WP-12/WP-13 appendix with `2026-09-13-implementation-planning-lossless-proof-ledger-wp12-wp13-v2.md`;
- enumerate all 17 WP-12 §14 duties and all 38 WP-13 §15 duties verbatim-in-substance, one row per duty;
- bind every row to a supporting RD target, one named executable witness and an admissible proof channel;
- explicitly preserve storage baseline independence from HOT/publication authority;
- route package proof through `Wp12HotProofTests` / `Wp13DurabilityProofTests` without allowing STATIC_AUDIT or HOSTED_CI to substitute for behavior/integration proof.

No readiness identity changes. R068 remains pure proof; R071 remains RD-06 implementation+proof.

### SIRR-002 — SIGNIFICANT — retained Dramaturg publication/admission

**Accepted.** RD-13 Task 7 specified retained horizon shapes/projection but did not make candidate-to-published promotion, exact published-base reconciliation and re-admission executable.

Repair is an RD-13 plan amendment, not a new owner:
- candidate remains ephemeral until ordinary RD-06 campaign publication is ACCEPTED;
- exact current published base/generation is frozen before mutation;
- publication uses the existing campaign publisher and non-force currentness semantics; RD-13 adds no transport or generic publisher;
- rejected/indeterminate publication never promotes candidate generation;
- conflict performs semantic rebase/rebuild/drop against current published horizon + native dependencies, never blind text merge;
- admission checks current multiplayer mode, current principal/player/authorization, role/recipient/control scope, exact BOUND shared generation for player-local horizon and native basis compatibility;
- disabled multiplayer yields `INACTIVE_MODE`; re-enable requires full revalidation before old bytes can be adopted;
- generation advances only after accepted publication.

`R085`/`R131` remain RD-13-owned. E11 gains an explicit RD-06 publication join but no semantic ownership transfer.

### SIRR-003 — SIGNIFICANT — omitted shipped-consumer cutover

**Accepted.** Two distinct currentness failures exist.

WP-13 / RD-06:
- `GAME/CORE/SAVE_CONTRACT.md` still states a universal campaign-only `SAVE_ALL_DIRTY -> one CAMPAIGN_TREE_TXN` contract. RD-06 must replace that with scope-relative native-domain SAVE composition; a campaign-domain sub-result may itself be one campaign tree publication, while LIVE/native domains retain their own owner establishment/currentness.
- `GAME/CORE/PERSISTENCE.md` keeps its valid base-tree/non-force/one-tree rules but must add the complete frozen-attempt/result-epistemic/reconciliation/G-specific clearing contract.
- `GAME/CORE/DURABILITY_GUARD.md`: current owner-consistent scope-relative policy; inspect/currentness test, no mandatory direct edit unless execution discovers contradiction.
- `GAME/CORE/STORAGE.md`: current storage/campaign separation is owner-consistent; inspect/currentness test, no mandatory direct edit.
- `GAME/CORE/ENGINE_UPDATES.md`: current maintenance/adoption routing remains owner-consistent; integration witness only unless currentness discovers contradiction.
- `GAME/CORE/MULTIPLAYER.md` and `GAME/CORE/LIVE_SCENE.md`: LIVE publication semantics remain RD-09/WP-16-owned. RD-06 must not overwrite them merely to satisfy WP-13; integration proves campaign SAVE composition does not replace LIVE exact-source CAS.
- stale tests asserting campaign-only SAVE, blanket dirty clear or global-hour/frontier semantics must be explicitly discovered and rewritten/retired by the owning implementation checkpoint.

WP-19 / RD-14:
- `GAME/CORE/BOOTSTRAP_RUNTIME.md` currently omits `ruleset_set_sha256` from generator-call prose;
- `GAME/CORE/CAMPAIGN_SETUP.md` currently omits it too;
- `GAME/INSTALL/00_DND_BOOTSTRAP.md` and `GAME/TOOLS/init_campaign.py` already carry the exact argument and ruleset identity propagation and therefore are current-conforming evidence, not gratuitous rewrite targets;
- RD-14 Task 3 must explicitly modify the two stale CORE consumers and test all three shipped prose/runtime consumers together.

### SIRR-004 — SIGNIFICANT — missing static Story selector

**Accepted.** WP-11 requires `MANIFEST.storage.story_root`; current `GAME/CAMPAIGN/MANIFEST.yaml` lacks it while RD-13 creates Story storage.

Repair:
- RD-13 Story storage checkpoint explicitly modifies the campaign manifest template to add `storage.story_root: "STORY"`;
- `StoryStorageSelectorTests` prove Story reads/writes resolve under that selector and mutable Story progress does not migrate into MANIFEST/CURRENT/RRC;
- RD-14 generator/scaffold tests prove copied generated campaigns preserve the selector;
- this is a pre-v1.0 clean-slate template correction. No legacy v0.8 preservation/migration requirement is invented.

### SIRR-005 — MINOR — close/absorb wording ambiguity

**Accepted as wording correction.** No WP-16 semantic change is needed.

RD-02/RD-09 integration language is corrected so that:
- Phase A close/fence is monotonic `ACTIVE -> CLOSED` and may succeed independently;
- Phase B normalization/native handoff/absorption is separate;
- if Phase B cannot complete, the exact final CLOSED source remains selected as `CLOSED_UNABSORBED` current truth with zero ordinary writers;
- campaign base is not fallback, closed source is not reopened, and route-away/absorption remains blocked/retryable until compatible completion;
- normalization failure therefore blocks absorption/handoff, not an already accepted close transition.

## 3. SIP reconciliation

| SIP | Post-repair disposition |
|---|---|
| SIP-001 | remains CLOSED |
| SIP-002 | repaired by explicit WP-13/WP-19 shipped-consumer cutover in the mandatory amendments |
| SIP-003 | semantic repair remains CLOSED; SIRR-005 wording ambiguity corrected |
| SIP-004 | remains CLOSED |
| SIP-005 | remains CLOSED |
| SIP-006 | repaired by Dramaturg publication/admission/rebase and Story selector actions |
| SIP-007 | remains CLOSED |
| SIP-008 | repaired affected Impact Envelopes/checkpoint ownership through mandatory amendments |
| SIP-009 | repaired by exact semantic WP-12/WP-13 v2 proof appendix/control ledger |
| SIP-010 | remains CLOSED |
| SIP-011 | remains CLOSED; executable maintenance command remains `python3 DEV/TOOLS/run_maintenance_audit.py` |

## 4. Architecture/decomposition disposition

No finding requires:
- a new RD unit;
- a new semantic owner;
- a new persistent authority;
- a new publication transport;
- a new lifecycle state;
- a legacy compatibility layer;
- a human-owned product/semantic decision.

The accepted RD-01..RD-14 decomposition therefore remains current. The repair changes worker instructions, proof routing, shipped-consumer cutover scope and one existing integration edge only.

## 5. Version Impact Gate

This author repair checkpoint changes planning/control documentation only. It does not change runtime bytes, persistent schemas, catalog generation, campaign contract generation, launcher revision, CORE module version or migration edges.

**Version Impact: NONE for this planning checkpoint.**

Future implementation of the repaired tasks must still run the local Version Impact Gate on the actual runtime/schema delta under `DEV/RELEASE/VERSIONING.md`.

## 6. Repair gate

Author repair is complete only after all of the following are published and read back together:
1. this disposition;
2. mandatory RD repair amendments;
3. v2 WP-12/WP-13 proof appendix + v2 control ledger;
4. execution-wave repair addendum;
5. repaired bidirectional/currentness closure;
6. exact-head repair closure and fresh independent Senior re-review brief.

Production implementation remains forbidden until that independent Senior re-review returns PASS / GO.
