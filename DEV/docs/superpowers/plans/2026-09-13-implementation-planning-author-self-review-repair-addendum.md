# HDM Implementation Planning — Author Self-Review Repair Addendum

Status: **CURRENT MANDATORY AUTHOR SELF-REVIEW ADDENDUM — EXECUTION NOT AUTHORIZED**
Date: 2026-09-13
Baseline: `026afe07020bc00da79c0099716f5cfe823d7141`
Production implementation authorized: **NO**.

This addendum repairs ASR-001..ASR-003 from `2026-09-13-implementation-planning-author-self-review-findings.md` after the SIRR-001..SIRR-005 author repair.

Current executable planning route is:

```text
base RD plan
+ 2026-09-13-implementation-planning-sirr-repair-amendments.md where applicable
+ this addendum where applicable
```

On conflict, this addendum controls only the exact repaired detail. It creates no new semantic owner, readiness identity or RD unit.

Affected RD units:

```text
RD-04  WP-11 fixed-root selector/schema realization
RD-06  proof/consumer disposition only; no new durability semantics
RD-13  Story-root integration + Dramaturg shared-basis correction
RD-14  generated-root/bootstrap consumer synchronization
```

RD-02/RD-09 SIRR-005 two-phase LIVE repair remains unchanged.

---

## A. ASR-001 — complete WP-11 fixed-root selector cutover

### A1. Authority and owner split

WP-11 owns physical route/root selection. RD-04 is the package realization owner for `R064`.

RD-13 owns Story projection semantics and Story-owned files under the selected Story root. It does **not** own the MANIFEST topology contract merely because Story consumes one selector.

RD-14 owns bootstrap/generator/product consumers of the final template shape. It does **not** create root semantics.

The fixed MANIFEST selector set after implementation is exactly:

```text
storage.state_root       = "STATE"
storage.index_root       = "INDEX"
storage.world_root       = "WORLD"
storage.event_log_root   = "LOG"
storage.checkpoints_root = "CHECKPOINTS"
storage.sessions_root    = "SESSIONS"
storage.story_root       = "STORY"
```

Selectors are topology only. They never contain Story progress/currentness, session currentness, chronology, authority, coverage or publication state.

### A2. RD-04 mandatory R064 task — fixed root-selector contract

Base route: `2026-09-13-RD-04-owner-native-routing-index-hot-plan.md`.

Add after native-route realization and before R064 can close:

#### Task R064-FIXED-ROOTS — RED/GREEN campaign fixed-selector contract

**Files**
- Modify: `GAME/CAMPAIGN/MANIFEST.yaml`
- Modify: `GAME/SCHEMA/campaign_manifest.schema.yaml`
- Modify: `GAME/CORE/STORAGE.md`
- Modify: `DEV/TESTS/test_rd04_native_routing_index_hot.py`
- Modify: `DEV/TOOLS/audit_engine.py`
- Inspect/consume: `GAME/CAMPAIGN/SESSIONS/**`
- Join with RD-13 Story root/scaffold creation before coherent GREEN checkpoint.

**RED class**
```text
FixedCampaignRootSelectorTests
```

RED assertions against the planning baseline:
1. MANIFEST template contains all seven WP-11 fixed selectors exactly once.
2. `campaign_manifest.schema.yaml` admits/requires the same seven selector fields with no extra root authority.
3. schema/template selector names and static values agree.
4. `SESSIONS/` is present in the campaign template and selected by `sessions_root`.
5. the RD-13 Story scaffold/root is present and selected by `story_root` at the coherent cutover checkpoint.
6. neither selector stores progress/currentness/coverage/chronology.
7. `STORAGE.md` describes all seven MANIFEST roots rather than only the old five.
8. known fixed-root access follows MANIFEST selection and never directory scan/path appearance as authority.

Run RED/GREEN:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot.FixedCampaignRootSelectorTests -v
```

**GREEN machine shape**
- `GAME/CAMPAIGN/MANIFEST.yaml`: add `sessions_root: "SESSIONS"` and `story_root: "STORY"`.
- `GAME/SCHEMA/campaign_manifest.schema.yaml`: add both fields under `storage` and update the invariant listing the current root set.
- The manifest local persistent schema changes incompatibly because two required selectors are added. Bump local `campaign_manifest` schema from `4 -> 5` in both schema owner and template instance.
- Do **not** bump `campaign_contract_generation`: under the current v1 clean-slate/pre-release policy old pre-release shapes are not compatibility targets and no migration of old pre-release campaign data is admitted solely to preserve them.
- Do **not** add a v4->v5 migration transform for pre-release compatibility. New v1 machine output is generated directly at schema 5; unsupported older pre-release shapes are not silently read as schema 5.
- Do **not** bump `storage_format_generation`: this changes the campaign MANIFEST local schema/root contract, not the default-branch storage marker format.
- `GAME/CORE/STORAGE.md` is a material shipped module edit; its `framework_module_version` moves from `1.0.1 -> 1.0.2` under the current module-version law.

The clean-slate exception is not permission to skip the local schema bump. It removes obsolete pre-release compatibility/migration debt while preserving truthful current schema identity.

**Coherent checkpoint rule**

Do not publish a green completion checkpoint where `story_root` is required but the current template has no Story root realization. The smallest coherent checkpoint contains:

```text
RD-04 MANIFEST + manifest schema + STORAGE projection
+ RD-13 Story root/scaffold minimum
+ focused route/schema tests
```

This is a named cross-RD integration checkpoint, not semantic owner transfer.

REFACTOR boundary: root-selector validation may be a pure topology helper; it must not become a general storage/currentness authority.

VERIFY:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot.FixedCampaignRootSelectorTests -v
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.StoryProjectionTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```

R064 cannot close until this task is green.

### A3. RD-13 Story task override

Base route: `2026-09-13-RD-13-story-t0-commentator-history-plan.md`.
Existing SIRR overlay section B1 instructed RD-13 to modify MANIFEST directly. That ownership/file action is superseded here.

RD-13 Task 4 still creates the Story-owned root and projection files under:

```text
GAME/CAMPAIGN/STORY/TRANSCRIPT/
GAME/CAMPAIGN/STORY/EVENTS/
GAME/CAMPAIGN/STORY/MECHANICS/
GAME/CAMPAIGN/STORY/NARRATIVE/
```

plus the accepted Story-local projection-state representation.

RD-13 consumes `MANIFEST.storage.story_root` from the RD-04/WP-11 topology contract. It tests that:
- the selected root resolves to `STORY` in the generated v1 scaffold;
- Story-local routes stay below that root;
- MANIFEST stores no Story coverage/progress/currentness;
- Story remains noncanonical and rebuildable under its owner.

RD-13 participates in the coherent `R064-FIXED-ROOTS` checkpoint with its minimum Story scaffold files; it does not independently bump or own the manifest schema.

### A4. RD-14 bootstrap/generator consumer cutover

Base route: `2026-09-13-RD-14-bootstrap-onboarding-product-plan.md` plus existing SIRR overlay.

Extend repaired Task 3 consumer actions.

**Files**
- Modify: `GAME/CORE/BOOTSTRAP_RUNTIME.md`
- Modify: `GAME/CORE/CAMPAIGN_SETUP.md`
- Modify: `GAME/INSTALL/00_DND_BOOTSTRAP.md`
- Inspect/protect: `GAME/TOOLS/init_campaign.py`
- Modify: `DEV/TESTS/test_rd14_bootstrap.py`

The existing SIRR ruleset-set digest synchronization remains required.

Additional GREEN requirements:
1. every expected generated-root list names `SESSIONS/` and `STORY/` in addition to the existing roots;
2. `CAMPAIGN_SETUP.md` no longer claims stale "manifest schema v3" and instead names the post-cutover current local manifest schema `5` or refers unambiguously to the current package manifest schema while tests assert value 5 for this implementation checkpoint;
3. the initial manifest description includes all seven storage selectors;
4. generated scaffold validation requires the current selector/schema contract and actual required roots;
5. generic `init_campaign.py` template copy remains unchanged unless fresh execution evidence shows it hard-codes the old root set; current baseline evidence says it already copies the complete template tree and therefore is `PROTECT_CURRENT_CONFORMING` for root propagation;
6. ruleset-set digest propagation remains exactly as already repaired.

**Version/revision consequences of these shipped text changes**
- `GAME/CORE/BOOTSTRAP_RUNTIME.md`: material edit; current `0.8.8 -> 1.0.9` (move prefix to current engine line and increment its existing revision exactly once).
- `GAME/CORE/CAMPAIGN_SETUP.md`: material edit; `1.0.3 -> 1.0.4`.
- `GAME/INSTALL/00_DND_BOOTSTRAP.md`: material launcher edit; `launcher_revision 19 -> 20`.

Do not increment these twice when root-list and ruleset-digest wording are repaired in the same logical file edit/checkpoint.

**Focused tests**
```text
GeneratorConsumerProjectionTests.test_expected_root_set_matches_wp11
GeneratorConsumerProjectionTests.test_current_manifest_schema_is_5
GeneratorConsumerProjectionTests.test_generated_manifest_has_all_fixed_selectors
GeneratorConsumerProjectionTests.test_sessions_and_story_roots_survive_generation
GeneratorConsumerProjectionTests.test_ruleset_set_digest_reaches_manifest
```

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.GeneratorConsumerProjectionTests -v
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.GeneratorScaffoldTests -v
```

### A5. Scheduling / integration edge

Add the named checkpoint:

```text
ROOT_SELECTOR_CUTOVER
  RD-04 WP-11 selector/schema owner
  + RD-13 Story root/scaffold owner
  JOIN_BEFORE_INTEGRATION
  -> one coherent schema/template/root checkpoint
  -> RD-14 bootstrap/generator consumers fresh-read that checkpoint
```

Physical-file coordination is a `SHARED_FILE_CHECKPOINT`; semantic ownership remains WP-11 for selectors and WP-18/Story for Story contents.

R064 and the R018 route/root integration cannot close before `ROOT_SELECTOR_CUTOVER` is green. R016/R018 Story slices additionally require RD-13 Story behavior. RD-14 generated-scaffold completion consumes the green selector/root checkpoint.

No whole-wave barrier is created.

---

## B. ASR-002 — correct Dramaturg player-local shared-basis semantics

Base route: RD-13 + SIRR repair section B2 + execution-wave SIRR addendum E11.

The following wording supersedes every statement that a player-local horizon always requires a `BOUND` shared generation.

### B1. Player-local basis contract

A player-local retained horizon carries exactly one declared shared basis:

```text
shared_basis.kind = ABSENT | BOUND
```

If `BOUND`:
```text
shared_basis.shared_generation = <exact accepted current shared generation>
```

If `ABSENT`:
```text
shared_basis.shared_generation = null/absent according to final schema spelling
```

`ABSENT` is a meaningful owner-approved statement that this player-local horizon does not depend on a retained shared horizon for its current candidate basis. It is not missing data and must not be auto-upgraded to BOUND for structural symmetry.

### B2. Candidate, publication and admission

`build_dramaturg_candidate(...)` freezes the declared shared basis together with exact native continuity/history/collaboration/control inputs.

`plan_dramaturg_publication(...)` publishes the candidate through ordinary RD-06 campaign publication. Publication remains non-authoritative until `ACCEPTED`.

After accepted publication:
- a BOUND player-local horizon is `CURRENT_COMPATIBLE` only when its referenced shared generation is the exact currently admitted accepted shared generation plus all player-local native bases remain current;
- an ABSENT player-local horizon is judged from its own frozen native bases and does not require a shared generation merely to be admitted;
- if current native dependency analysis changes the proper basis from ABSENT->BOUND or BOUND->ABSENT, the old retained generation is stale and a rebuilt candidate/new accepted generation is required;
- rejected/indeterminate publication never promotes either form;
- neither form may invent canon, agency, control or collaboration obligations.

### B3. Required tests

Replace the over-strong prior case with:

```text
DramaturgPublicationTests.test_player_local_absent_basis_is_legal_without_shared_generation
DramaturgPublicationTests.test_player_local_bound_basis_requires_exact_accepted_shared_generation
DramaturgPublicationTests.test_absent_to_bound_dependency_change_rebuilds_new_generation
DramaturgPublicationTests.test_bound_to_absent_dependency_change_rebuilds_new_generation
DramaturgAdmissionTests.test_stale_bound_shared_generation_rejected
DramaturgAdmissionTests.test_absent_basis_does_not_synthesize_shared_dependency
```

All existing privacy/currentness/publication/disabled-mode tests remain required.

### B4. E11 correction

Current E11 becomes:

```text
player-local retained horizon requires a valid declared shared basis:
  ABSENT -> no shared_generation dependency
  BOUND  -> exact accepted current shared_generation required
```

Everything else in the repaired retained-Dramaturg publication/admission join remains unchanged.

---

## C. ASR-003 — lossless proof route precision

The current file `2026-09-13-implementation-planning-lossless-proof-ledger-wp12-wp13-v2.md` is repaired in the same checkpoint. The exact corrected rows are:

```text
WP12-05 supporting targets:
  RD-04 HOT/native-edge establishment
  + RD-05 accepted execution/ExecutionSegment edge
  + RD-09 LIVE exact-source CAS/currentness

WP12-11 supporting targets:
  RD-06 frozen campaign publication
  + RD-04 generation support
  + RD-09 trustworthy principal/authorization evidence

WP13-19 supporting target:
  RD-06 gameplay campaign publication
  + fixed R2.6/WP-13 gameplay GitHub transport contract

WP13-20 supporting target:
  RD-06 gameplay campaign publication negative path
  + fixed R2.6/WP-13 no-alternate-gameplay-transport law
```

Development-agent Connector policy may support implementation discipline, but it is not the semantic proof owner for WP13-19/20.

The WP-13 row-38 consumer table is also corrected:
- `STORAGE.md` is `MODIFY` for R064 root-topology projection under RD-04; RD-06 only verifies storage-baseline/SAVE independence;
- `BOOTSTRAP_RUNTIME.md` and `CAMPAIGN_SETUP.md` are `MODIFY` for both ruleset-set identity and complete root/schema projection under RD-14;
- `INSTALL/00_DND_BOOTSTRAP.md` is `MODIFY`, not PROTECT, because its generated-root list lacks SESSIONS/STORY;
- `init_campaign.py` remains PROTECT_CURRENT_CONFORMING for generic template copying and existing ruleset-set propagation unless fresh execution currentness disproves that classification.

These corrections alter proof routing precision only; readiness identity counts/channels remain unchanged.

---

## D. Package/currentness/negative-law reconciliation

This addendum preserves:
- 116 direct + 9 pure-proof + 8 composite = 133 active identities;
- 12 trigger-gated and 79 no-work terminals untouched;
- R004 absent;
- RD count 14;
- no new gameplay/history/knowledge/currentness/Story/planning authority;
- no global save frontier/journal/rollback transaction;
- no pre-release compatibility shim/migration project;
- no forced BOUND Dramaturg dependency when WP-18 says ABSENT;
- no MANIFEST Story progress/currentness;
- no directory/path appearance as semantic authority;
- no whole-wave serialization from the new root-selector integration checkpoint.

Planning publication Version Impact: **NONE**. The future implementation consequences are explicitly pre-classified where mechanically determined above; actual worker checkpoint still verifies those classifications against fresh current bytes.

## E. Author repair acceptance checklist

This repair is author-complete only when a second author pass verifies all of the following against the published repair SHA:

```text
[ ] WP-11 seven-selector set is represented losslessly in the executable route
[ ] manifest schema/template cutover is one local schema 4->5 transition
[ ] pre-release clean-slate law is not misrepresented as permission to keep schema_version 4
[ ] no migration/campaign-contract/storage-generation work is manufactured for obsolete pre-release shapes
[ ] Story contents remain RD-13-owned while selector topology remains WP-11/RD-04-owned
[ ] RD-14 names every stale bootstrap/root/schema consumer and exact module/revision consequence
[ ] player-local Dramaturg permits both ABSENT and BOUND with correct conditional generation law
[ ] WP12-05/WP12-11 owner routes are complete
[ ] WP13-19/WP13-20 gameplay transport owner is not conflated with development-agent transport policy
[ ] row-38 consumer dispositions agree with the repaired root/consumer analysis
[ ] no new readiness identity/RD/whole-wave barrier introduced
[ ] hosted validation succeeds on exact repair SHA
```

Until that second pass is recorded, independent re-review #2 is not ready to start.
