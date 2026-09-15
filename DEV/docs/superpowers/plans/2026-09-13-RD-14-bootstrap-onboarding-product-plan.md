# RD-14 — Bootstrap / Onboarding / Product Consumers — Executable Implementation Plan

> For implementation workers: execute task-by-task under the current HDM execution process and Superpowers TDD workflow. No production implementation begins before independent Senior plan GO.

Goal: realize the WP-19 campaign-selection/New-Game/bootstrap/progressive-onboarding and product consumer contracts with gameplay-first provisional behavior, exact generator/package identity, one-tree initial publication, ordinary-Master retrospective routing, save-success-before-clear/menu return and creator-only fail-closed behavior — without inventing lifecycle, Story/T0 startup requirements or semantic authority.

RD unit: `RD-14`
Direct readiness: `R030,R086,R098,R100`.
Composite slices: `R029.ONBOARDING,R087.SAVE_SESSION_MENU`.
Canonical owners: WP-19; gameplay retrospective/campaign-exit owner decision; Actor continuity; RD-06 save/publication truth; RD-09 principal/currentness; RD-11 ordinary retrospective; RD-12 join/rejoin; RD-13 conditional history/T0/Commentator; runtime-package/bootstrap/install owners.
Dependencies/joins: RD-03 supplies provisional Actor/READY_PC shape; RD-06 supplies save/publication truth; RD-09 supplies current principal/PLAYER/creator-sensitive identity evidence; RD-11 owns ordinary active-player retrospective context; RD-12 supplies multiplayer frontier/catch-up; RD-13 supplies native history/T0 only when qualifying material already exists and Commentator for read-only consumers.
Out of scope: release execution/fresh-project release proof; migration execution; campaign lifecycle redesign; complete-sheet prerequisite; unconditional Story/T0 creation; creator automatic recovery; Actor/history/knowledge/currentness authority.

## Implementation Impact Envelope

SPEC / APPROVED DESIGN: WP-19 Laws 1–39; product retrospective/exit decisions; current runtime-package/install/bootstrap owners; exact readiness records.
BASELINE REF: fresh branch HEAD at execution.

EXPECTED OWNERS TO CHANGE:
- bootstrap/product orchestration only;
- exact shipped bootstrap/install projections;
- existing `GAME/TOOLS/init_campaign.py` only as needed to materialize the accepted current scaffold and identity fields coherently with other repaired RD plans.

EXPECTED CONSUMERS TO CHANGE:
- RD-03 provisional Actor/onboarding;
- RD-04 allocator/scaffold state;
- RD-06 initial/save publication plans;
- RD-09 principal/creator/currentness;
- RD-11 ordinary retrospective request binding;
- RD-12 rejoin/catch-up;
- RD-13 optional/qualifying Story/T0 and Commentator entry.

ALLOWED INTERFACES / CONTRACTS TO CHANGE:
- Create `GAME/TOOLS/bootstrap.py`;
- modify existing `GAME/TOOLS/init_campaign.py` only for accepted scaffold/identity propagation required by current v1 owner contracts;
- create `DEV/SCHEMAS/bootstrap-request.schema.json`;
- create `DEV/SCHEMAS/bootstrap-result.schema.json`;
- create `DEV/SCHEMAS/campaign-selection-result.schema.json`;
- replace `GAME/INSTALL/00_DND_BOOTSTRAP.md`;
- modify `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` and `GAME/INSTALL/README.md`;
- create/modify `DEV/TESTS/test_rd14_bootstrap.py`, project-map/audit projections;
- `GAME/CORE/START.md` remains absent; do not recreate for compatibility theater.

PROTECTED INVARIANTS:
- explicit campaign-selection barrier before campaign-specific gameplay/recovery reads;
- exact selected runtime package identity before generation;
- complete generator output -> one tree from scratch -> one initialization commit parented to pinned storage default HEAD -> one non-force campaign ref create/update;
- generator failure is not replaced by LLM/schema/per-file reconstruction;
- `initializing` may contain real agency/fiction with provisional Actor when local dependencies are committed;
- no hard pre-live/true-live phase;
- READY_PC/PLAY_READY are progressive owner frontiers, not full-sheet/world preload;
- T0/Story is conditional on qualifying accepted history and never a startup prerequisite;
- save must be confirmed before selected gameplay context is cleared;
- exit does not imply pause/completion/archive/membership leave/control transfer/global stop;
- creator authority comes from accepted creator provenance, not repository permission/PLAYER ID/login convenience cache;
- bootstrap coordinates owners and owns no world/knowledge/history/currentness semantics.

Version Impact: bootstrap/result/install/generator contract changes are classified at each task. Runtime release/fresh-project proof remains trigger-gated/out of scope.

## Task 1 — RED: selection barrier and exact New Game identity

**Files**
- Create: `DEV/TESTS/test_rd14_bootstrap.py`
- Create in Task 2: `GAME/TOOLS/bootstrap.py` and request/result schemas.
- Inspect: `GAME/TOOLS/init_campaign.py`, shipped install docs, storage/runtime package projections.

**Future interfaces**
```text
select_campaign(request, bounded_campaign_cards) -> CampaignSelectionResult
resolve_new_campaign_identity(request, storage_basis, runtime_packages) -> FrozenCreationEnvelope
create_new_campaign(frozen_envelope) -> BootstrapResult
resume_existing_campaign(selection, current_manifest_basis) -> BootstrapResult
```

**RED groups**
- `CampaignSelectionBarrierTests`: generic continue/sole visible campaign cannot infer selection;
- `CreationIdentityTests`: exact package/source/package hash/ruleset-set identity and pinned storage default HEAD required;
- `ProgressiveOnboardingTests`: no hard full-sheet/Story/T0 startup gate;
- `ProductExitCreatorTests`: save/clear/menu and creator fail-closed interfaces absent.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.CampaignSelectionBarrierTests -v
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.CreationIdentityTests -v
```
Expected RED. Do not publish RED-only completion checkpoint.

## Task 2 — GREEN: campaign-selection/request/result and frozen creation envelope

**Files**
- Create: `GAME/TOOLS/bootstrap.py`
- Create: `DEV/SCHEMAS/bootstrap-request.schema.json`
- Create: `DEV/SCHEMAS/bootstrap-result.schema.json`
- Create: `DEV/SCHEMAS/campaign-selection-result.schema.json`
- Modify: `DEV/TESTS/test_rd14_bootstrap.py`
- Modify: `DEV/PROJECT_MAP.md`
- Modify: `DEV/TOOLS/audit_engine.py`

**Contracts**
```text
CampaignSelectionResult = NONE_SELECTED | EXISTING(campaign_id, route_basis) | NEW_GAME(request)

FrozenCreationEnvelope {
  storage_repository_identity
  pinned_storage_default_head
  authenticated_creator_login
  authorized_mode
  branch_name
  campaign_id
  created_at
  engine_version
  package_id
  source_commit_sha | null
  package_sha256
  ruleset_set_sha256
}

BootstrapResult {
  disposition: READY_FOR_SETUP | RESUMED | RETRY | BLOCKED
  campaign_id?
  branch?
  lifecycle?
  owner_evidence_refs[]
  reason_code?
}
```

**Cases**
- preselection reads bounded cards/manifest fallback only, no gameplay working set;
- unambiguous explicit user campaign/New Game intent satisfies barrier once;
- existing campaign runtime identity comes from current MANIFEST, never storage baseline;
- New Game freezes exact package identity and neutral branch before remote mutation;
- package version/tag without hashes is insufficient;
- branch name carries no lore/player-count/authority semantics.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.CampaignSelectionBarrierTests -v
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.CreationIdentityTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```
Expected GREEN.

REFACTOR: bootstrap remains composition/orchestration; identity validation helpers do not become package/currentness owners.

Coherent checkpoint: bootstrap selection/identity skeleton + schemas/tests/audit/project-map, independently green.

## Task 3 — exact generator/scaffold and identity propagation (`R030` creation side)

**Files**
- Modify: `GAME/TOOLS/init_campaign.py` if repaired v1 scaffold contracts from RD-04/RD-12/RD-13 require additional generated files; preserve standard-library-only constraint.
- Modify current campaign template/scaffold files only through their owning RD plans and then consume their final shape here.
- Modify: `GAME/TOOLS/bootstrap.py`
- Modify: `DEV/TESTS/test_rd14_bootstrap.py`

**Interfaces**
```text
invoke_init_campaign(frozen_envelope, selected_package_root, fresh_output_root) -> GeneratedScaffold
validate_generated_scaffold(generated, frozen_envelope, expected_package_manifest) -> ScaffoldValidation
```

Call the existing selected package generator exactly once with accepted required identity inputs:
```text
--campaign-id
--branch
--engine-version
--package-id
--source-commit-sha (truthful nullable provenance)
--package-sha256
--ruleset-set-sha256
--created-at
--creator-github-login
--mode
```
plus output/source-root mechanics already owned by the generator.

The generated scaffold must include the final current template products admitted by preceding plans (for example current allocator singleton and v1 roots) through the package's `CAMPAIGN/` template, not by post-generator LLM invention.

**RED/GREEN cases**
- exact ruleset identity chain reaches `MANIFEST.ruleset.created_with/current`;
- engine/package identity reaches MANIFEST/card/current projections as owned;
- generated `campaign_id` reaches MANIFEST/card/CURRENT and any accepted current owner requiring it;
- generator output is complete package scaffold, not partial file list assembled by bootstrap;
- unavailable/failed/incomplete generator yields BLOCKED and no campaign publication;
- no per-file GitHub writes/schema reconstruction fallback;
- current `init_campaign.py` remains standard-library-only.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.GeneratorScaffoldTests -v
```
Expected GREEN.

Coherent checkpoint: generator/scaffold identity propagation + tests. All scaffold additions from sibling RD owners must already exist or be included as explicit joined file changes in this checkpoint; bootstrap may not invent them ad hoc.

## Task 4 — one from-scratch initial publication and creator provenance

**Files**
- Modify: `GAME/TOOLS/bootstrap.py`
- Modify: `DEV/TESTS/test_rd14_bootstrap.py`
- Consume RD-06 deterministic publication operation/result interface; do not implement Git/HTTP client here.

**Interface**
```text
plan_initial_campaign_publication(generated_scaffold, frozen_envelope) -> InitialPublicationPlan
adopt_initial_publication(result, frozen_envelope) -> BootstrapResult
```

`InitialPublicationPlan` is exactly:
```text
complete generated scaffold
-> one Git tree FROM SCRATCH
-> one initialization commit parented to pinned storage default HEAD H
-> one non-force campaign ref creation/update
```
No storage marker/default-branch README/owner file enters generated campaign tree merely through ancestry.

Creator authority evidence is the first campaign-specific initialization commit's `author.login` per WP19-L08. Card/MANIFEST creator fields remain projections/hints.

**Cases**
- prepared Git objects/ref-update failure have no campaign authority;
- no success/player setup reported before accepted ref publication;
- parent is frozen H, not later mutable default HEAD;
- exactly one from-scratch initial tree/commit/ref transition; later publication uses ordinary base-tree delta route;
- non-force conflict/ambiguity uses RD-06 result/reconciliation; no force/blind retry.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.InitialPublicationTests -v
```
Expected GREEN.

Coherent checkpoint: initial publication planner/consumer + tests. Publication transport/currentness remains RD-06.

## Task 5 — gameplay-first progressive onboarding (`R029.ONBOARDING`,`R030`)

**Files**
- Modify: `GAME/TOOLS/bootstrap.py`
- Modify: `DEV/TESTS/test_rd14_bootstrap.py`
- Consume RD-03 provisional Actor/READY_PC, RD-04 allocator, RD-09 principal/control, current owner routing.

**Interfaces**
```text
progress_onboarding(current_setup, accepted_player_input, owner_context) -> OnboardingProgress
compute_play_readiness(current_setup, owner_evidence) -> PLAYABLE_PROVISIONAL | READY_PC_ONLY | PLAY_READY | BLOCKED_FOR_INTERACTION
```

**Required behavior**
- new scaffold starts `initializing`;
- real agency/fiction may occur while initializing when the attempted interaction's local dependencies are committed;
- stable protagonist identity anchor crosses existing PROVISIONAL_IDENTITY durability boundary as the same native Actor identity;
- missing mechanics block only interactions requiring those unresolved mechanics and are progressively resolved;
- READY_PC closes only current material ordinary-mechanics dependencies;
- lifecycle `active` only after READY_PC + minimum PLAY_READY durable routing/scene frontier;
- last genuine blocker closure may launch playable fiction in same visible response without extra ceremonial continue;
- explicit save/stop during unfinished onboarding preserves `initializing`; it does not manufacture readiness/pause.

**Critically: no unconditional Story/T0/history prerequisite exists here.** RD-13 T0 is captured only if/when a qualifying accepted material decision/cognitive transition occurs. Story may be absent/lagging while gameplay remains valid. Commentator is not part of gameplay bootstrap.

**Tests**
- provisional player can perform nonmechanical/locally complete fiction before READY_PC;
- unresolved mechanic blocks that mechanic only;
- no complete character sheet/world preload/session-zero questionnaire required;
- no Story/T0 file required for first valid provisional fiction;
- if a qualifying material Actor decision occurs during onboarding, ordinary RD-03/RD-13 event/T0 path captures it in-band with zero extra serial call/publication solely for T0;
- stable provisional Actor identity survives later READY_PC/durability join.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.ProgressiveOnboardingTests -v
```
Expected GREEN.

Coherent checkpoint: progressive onboarding composition + tests; no Story/T0 owner change.

## Task 6 — multiplayer join/rejoin product path

**Files**
- Modify: `GAME/TOOLS/bootstrap.py`
- Modify: `DEV/TESTS/test_rd14_bootstrap.py`
- Consume RD-09 current principal/PLAYER/control and RD-12 PLAYER collaboration routes/frontier/catch-up.

For a creator-authorized multiplayer invitation, accept the invitee's GitHub login, resolve trustworthy current account ID + login through the supported Connector, then use the existing PLAYER access-transition producer and principal-routing closure. The resulting active binding is the invitation; no email identity, user-supplied numeric ID or separate invitation registry is required. Existing-account matching uses the stable ID and never substitutes for creator authority. Before mutable multiplayer input:
```text
trusted current principal
-> current active PLAYER/control
-> exact current campaign/native routes
-> exact nonterminal collaboration obligations from PLAYER companion where applicable
-> recipient-safe catch-up/frontier
-> accept new mutation/input
```

**Cases**
- invitation by login resolves and displays the intended account, writes its verified stable ID + login through the authorized PLAYER transition, and reuses an existing matching binding under current reactivation rules; absent participant does not create global wait without positive dependency;
- unresolved/ambiguous login lookup, email-only evidence, a reused login offered to inherit an existing binding owned by a different account ID, and attempted binding without current creator authority cannot grant access; a login-label refresh cannot transfer an existing binding; rejoin cannot mutate from stale session/card/chat cache;
- private catch-up material remains recipient isolated;
- collaboration catch-up projection never becomes history/knowledge authority.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.MultiplayerJoinRejoinTests -v
```
Expected GREEN.

Coherent checkpoint: product join/rejoin adapter + tests.

## Task 7 — ordinary active-player retrospective consumer (`R097` integration)

**Files**
- Modify: `GAME/TOOLS/bootstrap.py` only for product/interaction routing if no existing interaction router owns the dispatch; otherwise modify that exact current router discovered by execution currentness and keep `bootstrap.py` as no-op consumer evidence.
- Modify: `DEV/TESTS/test_rd14_bootstrap.py`
- Consume RD-11 registered retrospective ContextNeedProfile/request interface and RD-09 principal/PLAYER/disclosure eligibility.

**Interface behavior**
```text
route_active_player_retrospective(request, current_gameplay_binding) -> RD11RetrospectiveRequest
```
An authorized active player asks history inside ordinary Master interaction. No Commentator transition and no fictional-time advance solely from asking. The request binds registered historical purpose, current player/PC, recipient/disclosure scope and bounded history retrieval. Story may orient; material/source-specific claim uses native eligible evidence via RD-11.

If execution discovers an existing canonical interaction router, this task's exact file action is transferred to that router with evidence; the semantic interface and tests are not optional. This is a file-location currentness resolution, not worker permission to redesign routing.

**Tests**
- active participant retrospective routes to RD-11, not Commentator;
- read-only/nonparticipant visible campaign routes to RD-13 Commentator instead;
- no whole-history scan after coarse selector failure;
- exact motive remains qualified when T0 evidence insufficient;
- physical access never widens disclosure.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.OrdinaryRetrospectiveRoutingTests -v
```
Expected GREEN.

Coherent checkpoint: exact product/interaction routing adapter + tests.

## Task 8 — save-success -> session-local clear -> same-chat menu (`R087.SAVE_SESSION_MENU`,`R098`)

**Files**
- Modify: `GAME/TOOLS/bootstrap.py`
- Modify: `DEV/TESTS/test_rd14_bootstrap.py`
- Consume RD-06 SAVE result and current session/local HOT/live handles.

**Interfaces**
```text
save_and_exit_to_selection(current_binding, save_scope) -> SaveExitResult
clear_selected_gameplay_context(current_binding, confirmed_save_result) -> ClearedSessionContext
build_campaign_selection_menu(cleared_context, bounded_cards) -> CampaignMenu
```

**Exact order**
```text
SAVE_ALL_DIRTY/native durability
-> confirmed required campaign/live save success
-> clear this chat's selected gameplay context
-> bounded normal campaign-selection gate/menu
```

**Clear** as applicable: selected campaign/branch/root gameplay binding; pinned native gameplay working set; flushed HOT dirty ownership for this chat; active gameplay role-context/player/PC binding; this chat's live participation handle.

**Preserve**: authenticated principal/session identity; selected storage repository sufficient for menu; inert package caches; durable campaign lifecycle/PLAYER membership/PC-control/world state; benign caches only if they cannot bypass selection/currentness revalidation.

**Cases**
- FAILED/REJECTED/INDETERMINATE save does not claim combined success and does not discard strongest recovery-safe selected context;
- confirmed success clears only session-local selected gameplay state;
- exit alone does not set paused/completed/archived, deactivate PLAYER, transfer PC, leave membership or stop shared live epoch;
- same-chat menu has no implicit priority/reselection of exited campaign.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.SaveExitMenuTests -v
```
Expected GREEN.

Coherent checkpoint: save-exit consumer + clear/preserve/menu tests. No lifecycle enum addition.

## Task 9 — creator provenance and fail-closed creator-only consumer (`R086`,`R100`)

**Files**
- Modify: `GAME/TOOLS/bootstrap.py`
- Modify: `DEV/TESTS/test_rd14_bootstrap.py`
- Consume RD-09 trusted principal/current identity evidence and initialization-commit provenance reader.

**Interfaces**
```text
load_campaign_creator_provenance(initialization_commit) -> CreatorProvenance
classify_creator_authority(current_principal, creator_provenance) -> CREATOR_CONFIRMED | NOT_CREATOR | CREATOR_UNRESOLVED
```

Creator-only mutation path requires confirmed accepted creator provenance. Repository permission, current PLAYER identity, card/manifest creator cache, mutable convenience label alone or self-assertion cannot substitute.

**Cases**
- confirmed creator may perform admitted creator-only product operation;
- noncreator active PLAYER remains ordinary participant only;
- creator provenance mismatch/unavailable/ambiguous fails closed for creator-only mutation;
- fail-closed creator-only authority does not make otherwise readable campaign invisible and does not invent automatic creator recovery/transfer;
- login/cache changes cannot silently transfer creator authority;
- multiplayer ordinary participant operations remain unaffected when they do not require creator privilege.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.CreatorAuthorityTests -v
```
Expected GREEN.

Coherent checkpoint: creator provenance consumer + tests. No new identity owner.

## Task 10 — shipped bootstrap/install projections and known stale consumers (`R086` consumer alignment)

**Files**
- Replace: `GAME/INSTALL/00_DND_BOOTSTRAP.md`
- Modify: `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`
- Modify: `GAME/INSTALL/README.md`
- Modify: `GAME/CAMPAIGN/README.md` if current body contradicts the repaired machine flow;
- Modify: `DEV/TOOLS/audit_engine.py`
- Modify: `DEV/TESTS/test_rd14_bootstrap.py`
- Do not create `GAME/CORE/START.md`.

Projection order must match machine flow:
```text
bounded campaign selection
-> exact existing-current or frozen New Game package identity
-> generator + initial publication for New Game
-> progressive initializing/provisional setup
-> READY_PC + PLAY_READY when dependencies close
-> ordinary gameplay/product routes
```
No root-relative stale `SESSION/...` write semantics, legacy START dependency, hard pre-live/true-live phase, full-sheet gate or Story/T0-before-gameplay rule.

**RED/GREEN cases**
- prose stage order agrees with `bootstrap.py` tests;
- generator/package identity and failure behavior stated without internal infrastructure narration in successful user flow;
- known current shipped projections cannot resurrect stale campaign-root paths or creator/login authority shortcuts.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.ShippedBootstrapProjectionTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```
Expected GREEN.

Coherent checkpoint: all active install/bootstrap projections + conformance tests/audit.

## Task 11 — failure, retry and idempotence

**Files**
- Modify: `GAME/TOOLS/bootstrap.py`
- Modify: `DEV/TESTS/test_rd14_bootstrap.py`

**Cases**
- failure before authoritative campaign ref publication leaves no campaign authority and safe retry reuses/freshens only owner-permitted identity components;
- duplicate bootstrap request cannot create second campaign lineage accidentally;
- interrupted owner call is reconciled through that owner's idempotency/currentness evidence, never blind replay;
- after campaign publication, later onboarding failure resumes same campaign/Actor identity rather than rerunning generator/initial commit;
- save-exit retry never clears before confirmed accepted save.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.FailureRetryTests -v
```
Expected GREEN.

Coherent checkpoint: failure/idempotence behavior + tests.

## Task 12 — composite joins and RD-14 verification

`R029.ONBOARDING`: same provisional RD-03 Actor identity + RD-06 durability + this progressive onboarding branch; no complete-sheet prerequisite/retrofit identity.

`R087.SAVE_SESSION_MENU`: this Task-8 product/session branch joins RD-11 retrospective and RD-13 SemanticEvent/T0 sibling branches at parent reconciliation. It does not require Story/T0 before ordinary startup or save/menu operation unless a concrete owner result itself has that dependency.

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected PASS for currently active deterministic/scenario obligations.

Negative stale proof searches inferred campaign selection, version-only package identity, per-file scaffold publication, LLM generator fallback, hard pre-live/true-live gate, complete-sheet/world preload, Story/T0 startup prerequisite, premature context clear, implicit exit lifecycle side effects, creator-login/PLAYER/repository-permission substitution, stale `SESSION/...` writes and recreated START dependency.

Version Impact Gate: classify bootstrap request/result/scaffold/generator/projection contract changes. System Impact Gate stops on any new campaign lifecycle semantics, semantic owner, creator-transfer mechanism, Story/T0 startup authority or release/migration activation.

Currentness fence: fresh-read WP-19/product owner decisions, current `init_campaign.py`, install projections, RD-03/RD-04/RD-06/RD-09/RD-11/RD-12/RD-13 and exact touched files. Owner drift stops execution.

Final coherent checkpoint: selection/New Game identity/generator/publication/progressive onboarding/product retrospective/save-exit/creator/projection tests all green, audit/full DEV tests green and remote read-back recorded. RD-14 closes only its direct leaves/listed slices; package composite/pure-proof closure remains the proof-ledger checkpoint.