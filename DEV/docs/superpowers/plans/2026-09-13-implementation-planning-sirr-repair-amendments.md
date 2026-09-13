# HDM Implementation Planning — Mandatory SIRR Repair Amendments

Status: **CURRENT MANDATORY OVERLAY FOR AFFECTED RD PLANS**
Date: 2026-09-13
Baseline: `d01bd4bac55115408f6347f88214475855fbac0e`
Production implementation authorized: **NO**.

This file is a mandatory execution overlay on the current package-index routes for RD-02, RD-06, RD-09, RD-13 and RD-14. Unchanged portions of their base plans remain authoritative. If this overlay conflicts with wording in an affected base plan, this overlay controls. It does not authorize semantic redesign.

## A. RD-06 — SAVE / durability / campaign publication

Base route: `2026-09-13-RD-06-save-durability-publication-plan.md`.
Findings closed: SIRR-001, SIRR-003; SIP-002/SIP-008/SIP-009 affected portions.

### A1. Impact Envelope replacement/addition

Add explicit shipped-consumer actions:

```text
EXISTING_MODIFY GAME/CORE/SAVE_CONTRACT.md
EXISTING_MODIFY GAME/CORE/PERSISTENCE.md
INSPECT_AND_DISPOSITION GAME/CORE/DURABILITY_GUARD.md
INSPECT_AND_DISPOSITION GAME/CORE/STORAGE.md
INSPECT_AND_DISPOSITION GAME/CORE/ENGINE_UPDATES.md
OWNER_JOIN_ONLY GAME/CORE/MULTIPLAYER.md
OWNER_JOIN_ONLY GAME/CORE/LIVE_SCENE.md
DISCOVER_AND_DISPOSITION stale SAVE/durability/publication tests
```

The first two are mandatory current deltas based on the planning baseline. The next three are current-conforming consumers and are not edited merely to create churn; if fresh execution currentness reveals contradiction, stop and route the exact contradiction through the owning checkpoint. MULTIPLAYER/LIVE_SCENE remain RD-09/WP-16-owned and are integration surfaces, not RD-06 rewrite authority.

### A2. Replace base Task 5 with explicit shipped-consumer cutover

#### Task 5 — RED/GREEN shipped SAVE/publication consumer cutover + R029 durability join

**Files**
- Modify: `GAME/CORE/SAVE_CONTRACT.md`.
- Modify: `GAME/CORE/PERSISTENCE.md`.
- Inspect/disposition: `GAME/CORE/DURABILITY_GUARD.md`, `GAME/CORE/STORAGE.md`, `GAME/CORE/ENGINE_UPDATES.md`.
- Integration-inspect only: `GAME/CORE/MULTIPLAYER.md`, `GAME/CORE/LIVE_SCENE.md`.
- Modify only where current contradiction exists: `GAME/SCHEMA/session.schema.yaml`, `GAME/TEMPLATE/STORAGE_README.md`.
- Modify projections: `DEV/PROJECT_MAP.md`, `DEV/TOOLS/audit_engine.py` when actual shipped file/module inventory changes.
- Modify focused RD-06 tests; discover stale existing tests by assertion/contract semantics before editing them.

**RED groups**

`SaveContractCutoverTests` must fail while `SAVE_CONTRACT.md` still equates `SAVE_ALL_DIRTY` with one universal `CAMPAIGN_TREE_TXN` and campaign-only post-publication clearing.

`PersistencePublicationContractTests` must fail while `PERSISTENCE.md` lacks the complete frozen-attempt/result-epistemics/currentness contract required by WP-13.

`ShippedPersistenceDispositionTests` must fail if any named shipped consumer is silently omitted from disposition or if an RD-06 edit tries to replace LIVE exact-source CAS with campaign publication.

**GREEN — SAVE_CONTRACT**

Replace the universal campaign-only composition with:

```text
SAVE(scope)
  -> freeze one definite scope/root/native-generation closure
  -> partition required durability work by native owner/domain
  -> execute each domain through its own establishment/publication contract
  -> collect typed domain results
  -> prove current compatible closure for the frozen SAVE promise
  -> acknowledge overall SAVE only on compatible required-domain success
```

Required laws:
- one campaign-domain delta may use one `CAMPAIGN_TREE_TXN`; that is a domain sub-result, not a universal SAVE transaction;
- LIVE exact-source CAS remains LIVE establishment/currentness and is not folded into campaign Git transaction semantics;
- independent native domains have no invented total order, distributed rollback or global transaction frontier;
- partial domain success is real evidence but cannot produce false overall `saved` acknowledgement;
- no-write success requires current compatible closure evidence, not merely an empty dirty set;
- clearing is exact-generation/owner-specific: accepted G never clears later G+1;
- automatic/risk-control durability remains distinguishable from explicit SAVE.

**GREEN — PERSISTENCE**

Preserve valid base-tree, one-tree, single-parent, non-force and no per-file Contents laws, and add executable documentation/projection for:
- frozen repository/ref/principal/authorization evidence;
- exact owner generations/read/dependency/path-index closure;
- `ACCEPTED | REJECTED | INDETERMINATE` transition epistemics;
- rejection classification before retry;
- bounded authority observation/lineage/current-closure reconciliation after indeterminate result;
- disjoint target movement preserving established semantic IDs/RNG/outcomes while rebuilding only transport basis;
- overlapping movement invoking owner-specific revalidation, never generic text merge;
- bounded retry;
- exact G clearing and preservation of G+1;
- crash after remote acceptance recovering from native authority without a persistent publication journal or gameplay replay;
- Git/ref ordering remaining non-authoritative for fictional chronology.

**Named no-direct-edit dispositions at planning baseline**
- `DURABILITY_GUARD.md`: current scope-relative NORMAL/ELEVATED/DANGER policy, zero-I/O/zero-heartbeat posture and failure-not-HARD rule are compatible; no mandatory edit.
- `STORAGE.md`: storage-baseline/campaign separation is compatible; no mandatory edit.
- `ENGINE_UPDATES.md`: maintenance/adoption already consumes canonical campaign publication with its own authority; no mandatory edit.
- `MULTIPLAYER.md` / `LIVE_SCENE.md`: LIVE owner alignment occurs under RD-09; RD-06 integration only proves campaign SAVE does not absorb LIVE currentness authority.

**Stale test disposition**
Execution currentness must search existing tests for semantic assertions equivalent to:
- all SAVE is one campaign tree transaction;
- every dirty source clears on one campaign publication success;
- universal hourly/global frontier/HARD save queue;
- successful object preparation equals publication success;
- ambiguous update may be blindly retried.

Every actual stale assertion is rewritten/retired in the same owner checkpoint with its replacement witness. Absence is recorded as a negative finding; do not invent tests solely to retire them.

**R029.DURABILITY** remains a slice: provisional Actor/onboarding state may enter this same scope-relative machinery; RD-14 retains onboarding/lifecycle semantics.

Focused commands:
```bash
python3 -m unittest DEV.TESTS.test_rd06_durability_publication.SaveContractCutoverTests -v
python3 -m unittest DEV.TESTS.test_rd06_durability_publication.PersistencePublicationContractTests -v
python3 -m unittest DEV.TESTS.test_rd06_durability_publication.ShippedPersistenceDispositionTests -v
```

### A3. Replace R071 thematic closure with exact ledger route

Base Task 6 remains the integrated verification task, but `R071` closes only through all 38 rows of `2026-09-13-implementation-planning-lossless-proof-ledger-wp12-wp13-v2.md`. The RD-06 thematic scenario list is supporting coverage only.

`Wp13DurabilityProofTests` is the package witness. Every row must execute through its assigned primary proof channel. Missing row = RED. `NOT_APPLICABLE` requires a current owner citation. Future-trigger rows are not manufactured.

## B. RD-13 — Story selector + retained Dramaturg publication/admission

Base route: `2026-09-13-RD-13-story-t0-commentator-history-plan.md`.
Findings closed: SIRR-002, SIRR-004; SIP-006/SIP-008 affected portions.

### B1. Add Story root selector to Story storage checkpoint

In the task that materializes native Story storage/currentness, add:

**Files**
- Modify: `GAME/CAMPAIGN/MANIFEST.yaml`.
- Modify: RD-13 focused tests.
- Consume in RD-14 generator/scaffold integration tests.

**Required current template delta**
```yaml
storage:
  story_root: "STORY"
```

The selector is a static storage route. It does not make MANIFEST a Story-progress owner.

Add `StoryStorageSelectorTests`:
- manifest template contains exactly one admitted `storage.story_root` selector;
- Story record/projection paths resolve beneath that selector according to WP-11/WP-18 topology;
- mutable Story sequence/progress remains in Story-owned records, not MANIFEST/CURRENT/RRC;
- no extra Dramaturg root selector is invented;
- generated campaign preservation is proven by RD-14, not by a second generator path.

Pre-v1.0 clean-slate rule: do not add a legacy v0.8 migration/compatibility alias solely for this selector.

### B2. Replace/extend Dramaturg Task 7 with retained-generation publication lifecycle

The two admitted retained families remain exactly:
```text
DRAMATURG/SHARED.yaml
DRAMATURG/PLAYERS/<player_id>.yaml
```
No registry, global plot graph, scheduler, agenda authority, MANIFEST selector or single-player durable planning system is added.

**Interfaces**
```text
project_shared_dramaturg_horizon(current_multiplayer_basis) -> DramaturgCandidate
project_player_dramaturg_horizon(player_id, eligible_basis) -> DramaturgCandidate

prepare_dramaturg_publication(candidate, exact_published_base, current_basis)
    -> DramaturgPublicationAttempt

classify_dramaturg_admission(retained_horizon, current_basis)
    -> ABSENT | CURRENT_COMPATIBLE | STALE | INACTIVE_MODE | CORRUPT

reconcile_dramaturg_publication(candidate, observed_published, current_basis)
    -> REBASE | REBUILD | DROP

promote_accepted_dramaturg_generation(candidate, accepted_publication)
    -> PublishedDramaturgGeneration
```

These are RD-13 semantic planning/projection interfaces. Remote mutation is delegated to the ordinary RD-06 campaign publication operation/result; RD-13 creates no new Git/Connector/transport publisher.

**Candidate law**
- projected candidate is EPHEMERAL;
- it is not selected by another context and is not a retained generation before publication acceptance;
- a candidate generation number is provisional metadata only; retained generation advances only on accepted publication.

**Frozen publication/admission basis**
For shared horizon, freeze/revalidate:
- current campaign/ref/currentness basis;
- active multiplayer mode;
- trustworthy current principal -> active PLAYER where operation requires it;
- operation/role eligibility;
- exact current retained shared generation/base;
- exact native continuity/history/currentness dependencies used by the horizon.

For player-local horizon additionally freeze/revalidate:
- exact target `player_id` native route/current active binding;
- recipient/control/role eligibility;
- exact `BOUND shared generation` consumed by the player-local horizon;
- native/private-source compatibility without widening disclosure.

**Publication result law**
- `ACCEPTED`: only then may the candidate become the new retained generation;
- `REJECTED`: candidate remains unpublished; observe current retained authority before any retry;
- `INDETERMINATE`: no promotion/acknowledgement/blind replay; bounded authority observation first;
- previous published generation remains usable only if it still classifies `CURRENT_COMPATIBLE`; otherwise use ABSENT/STALE, never the failed candidate.

**Conflict/rebase law**
On exact-base movement:
1. read current retained horizon and only required native dependencies;
2. revalidate multiplayer/principal/player/role/recipient/control eligibility;
3. classify current retained generation/base;
4. preserve only candidate material still compatible with current native/shared basis;
5. semantically rebase/rewrite compatible derived horizon content;
6. discard incompatible provisional content;
7. publish one successor attempt through RD-06.

No blind text merge and no generic planner transaction authority.

**Mode transition/admission law**
- multiplayer disabled -> retained Dramaturg families classify `INACTIVE_MODE`; physical bytes may remain but are not selected by singleplayer;
- re-enable does not automatically reactivate old bytes: full mode/player/role/recipient/control/native-basis/exact-bound-shared-generation validation runs again;
- inactive/deactivated player-local horizon cannot be selected merely because its file exists.

**Focused tests**
`DramaturgPublicationTests`:
- unpublished candidate is not retained/current;
- accepted ordinary campaign publication promotes exactly one next generation;
- rejected/indeterminate result does not promote;
- previous compatible generation remains selected after failed successor;
- exact-base movement forces reconcile, not blind replay.

`DramaturgAdmissionTests`:
- shared horizon requires current multiplayer/current authorization/native compatibility;
- player-local horizon requires active exact player plus recipient/control scope and exact BOUND shared generation;
- mismatched shared generation -> STALE;
- disabled mode -> INACTIVE_MODE;
- re-enable requires complete fresh admission.

`DramaturgRebaseTests`:
- disjoint compatible owner movement can preserve/rebase derived material;
- incompatible continuity/history/currentness invalidates affected provisional material;
- recipient-private material never crosses player-local scope during rebase.

Focused commands:
```bash
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.DramaturgPublicationTests -v
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.DramaturgAdmissionTests -v
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.DramaturgRebaseTests -v
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.StoryStorageSelectorTests -v
```

The exact test module/class prefix may follow the base RD-13 file's current module name at execution, but these class responsibilities and cases are mandatory.

## C. RD-02 / RD-09 — close vs absorption wording correction

Finding closed: SIRR-005; SIP-003 wording disposition.

### C1. RD-02 Task 5 correction

Replace any requirement that “close/absorb is blocked” by normalization failure with:

```text
accepted ACTIVE -> CLOSED fence may complete first;
required normalization/native-owner handoff failure blocks absorption/route-away only;
while unresolved, exact final CLOSED source is CLOSED_UNABSORBED current truth with zero ordinary writers;
campaign base is not fallback and the closed source is not reopened;
retry/reconciliation resumes from the exact final CLOSED source and current owner basis.
```

Update the integration case accordingly. The normalizer still owns information semantics; it gains no LIVE lifecycle authority.

### C2. RD-09 Task 7/8 correction

Make the lifecycle explicitly two-phase:

```text
Phase A — CLOSE/FENCE
  ACTIVE -> CLOSED exact-source transition
  capture exact final closed source L
  ordinary writers disabled

Phase B — NORMALIZE / DURABLY HAND OFF / ABSORB
  consume L
  normalize/apply required material owner evidence
  publish compatible campaign/native closure
  route away/mark absorbed only after success
```

If Phase B fails or is indeterminate after Phase A succeeded:
- state remains CLOSED_UNABSORBED;
- L remains selected current truth for admitted live-owned scope;
- zero ordinary writer exists;
- do not reopen the epoch;
- do not fall back to campaign base;
- bounded retry/reconciliation restarts Phase B against L/current owners.

Add/repair `LiveClosedUnabsorbedTests` covering successful close + failed normalization, successful close + indeterminate campaign publication and later successful absorption from the same final source.

## D. RD-14 — exact generator consumer synchronization

Base route: `2026-09-13-RD-14-bootstrap-onboarding-product-plan.md`.
Finding closed: SIRR-003 WP-19 portion; SIP-002/SIP-008 affected portions.

### D1. Impact Envelope additions

Add:
```text
EXISTING_MODIFY GAME/CORE/BOOTSTRAP_RUNTIME.md
EXISTING_MODIFY GAME/CORE/CAMPAIGN_SETUP.md
INSPECT_CURRENT_CONFORMING GAME/INSTALL/00_DND_BOOTSTRAP.md
INSPECT_CURRENT_CONFORMING GAME/TOOLS/init_campaign.py
CONSUME GAME/CAMPAIGN/MANIFEST.yaml Story selector from RD-13 checkpoint
```

### D2. Task 3 generator/scaffold addition

`BOOTSTRAP_RUNTIME.md` and `CAMPAIGN_SETUP.md` must list the exact generator identity chain including:
```text
--engine-version
--package-id
--source-commit-sha when non-null
--package-sha256
--ruleset-set-sha256
--created-at
--creator-github-login
--mode as applicable
```

Both consumers must state that the digest reaches `MANIFEST.ruleset.created_with/current.ruleset_set_sha256` under the current digest-generation contract. No fallback may reconstruct missing identity from another package/tag/current `main`.

`GAME/INSTALL/00_DND_BOOTSTRAP.md` and `GAME/TOOLS/init_campaign.py` are current-conforming at the planning baseline; tests protect them from regression rather than forcing a no-op edit.

Add `GeneratorConsumerProjectionTests`:
- all shipped generator-call consumers expose `ruleset_set_sha256` consistently;
- generator rejects missing/invalid exact digest;
- generated MANIFEST created/current ruleset digests equal the frozen envelope input;
- no consumer derives the ruleset-set digest from semantic engine version or package tag;
- generated scaffold includes the RD-13-provided `storage.story_root` selector unchanged.

Focused command:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.GeneratorConsumerProjectionTests -v
```

## E. Worker currentness and checkpoint law

Before executing any amended task, worker fresh-reads:
1. current branch HEAD;
2. `AGENTS.md` + applicable runtime overlay;
3. `DEV/CURRENT_PROGRESS.md` and current package index;
4. base RD plan + this mandatory overlay;
5. only the exact canonical owners and shipped files named by that task.

If owner semantics changed after this planning package, stop the affected task and return to planning. File-location drift that preserves semantics may be resolved through the base plan's currentness fence and recorded in handoff.

Every coherent implementation checkpoint follows RED -> GREEN -> REFACTOR -> VERIFY and runs the exact focused tests plus maintenance audit. No RED-only publication.

## F. Version Impact

This overlay is planning-only: Version Impact `NONE` for publication of this file.

During future implementation:
- material CORE edits increment their owner `framework_module_version` exactly once under `DEV/RELEASE/VERSIONING.md`;
- the MANIFEST selector/schema change is classified against its persistent schema/campaign-contract owner from actual implemented shape; do not pre-guess a bump in planning;
- no migration is activated merely because pre-v1.0 template bytes change;
- any real incompatible persisted change discovered at implementation must stop at the Version Impact/System Impact Gate rather than being hidden in the worker patch.
