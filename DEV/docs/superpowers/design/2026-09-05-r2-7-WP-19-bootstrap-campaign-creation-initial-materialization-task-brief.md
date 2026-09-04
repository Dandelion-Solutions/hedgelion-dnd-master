# R2.7 WP-19 — Bootstrap / Campaign Creation / Initial Materialization — Architecture Task Brief

Status: **STEP 1 SENIOR RECOVERY COMPLETE — MANDATORY SENIOR RE-REVIEW CANDIDATE**

Date: 2026-09-05

Original Step-1 execution basis: `5fc24905be5c9e1b47929ee9e7b49ea8b9f2a053`

Senior-recovery basis: `df5fe6441c2b85e9cbffcb6f83caa885501da794`

This is the Architecture Task Brief required by the current HDM design process for WP-19. Senior recovery SR19-01 materially qualifies the evidence framing: verification/scenario catalogs and executable tests are first-class reverse-conformance consumers that must themselves be reconciled against current owners rather than presumed current because they exist or pass CI.

This brief does not authorize or begin Step 2, WP-20, implementation planning, gameplay bootstrap, campaign creation, or substantive runtime/schema/template/test implementation.

Companion Step-1 artifacts:

- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief-critic.md`.

---

## 1. Problem statement

WP-19 must audit and reconcile the complete architecture-to-machine path by which an explicit **New Game** choice becomes a correctly owned, resumable campaign and then reaches the first normal mechanics-capable play frontier.

The domain is broader than copying an empty directory and narrower than ordinary gameplay:

```text
storage selection / storage baseline
    -> explicit New Game choice
    -> exact runtime + exact ruleset-set resolution
    -> neutral campaign branch / creator provenance
    -> exact scaffold materialization
    -> first campaign-specific publication
    -> lifecycle = initializing
    -> low-friction player setup
    -> optional PROVISIONAL_IDENTITY durability
    -> READY_PC mechanical readiness
    -> minimal starting world / current routing
    -> PLAY_READY durable launch frontier
    -> lifecycle = active
    -> first true mechanics-capable live scene / normal runtime
```

Every transition must have one accepted authority, correct input provenance, an honest machine/runtime destination, bounded failure semantics and a resumable publication boundary where required.

WP-19 must also perform the reverse audit: every current bootstrap instruction, materializer input, campaign-template field/root, schema constraint, setup projection, executable test and materially relevant scenario expectation must have an accepted semantic owner or be explicitly classified as current, current-with-qualifier, stale/superseded, historical, derived, implementation-only, safely deferred or out of scope.

The audit must not collapse technical scaffold creation, provisional onboarding, READY_PC and PLAY_READY into one generic concept of “campaign ready”. It must also not let a stale regression scenario override a later/current owner.

---

## 2. Goals

WP-19 Step 2, **only if Senior-authorized**, must establish all of the following.

1. **Creation preconditions and selection authority**
   - prove storage discovery/selection and explicit campaign-choice gate;
   - prove which principal may create/publish a campaign and how creator identity becomes stable evidence;
   - prevent ambient package, previous chat, sole-campaign presence or repository permission from silently choosing semantic authority.

2. **Exact runtime/ruleset creation identity**
   - establish one reconstructive chain from storage baseline through validated runtime package to campaign `engine.created_with/current` and `ruleset.created_with/current`;
   - reconcile every current bootstrap/materializer/package/test consumer of that identity;
   - fail closed rather than inventing missing provenance or re-resolving an old package from a mutable tag position.

3. **Branch and initial publication contract**
   - reconcile storage-default ancestry, neutral campaign branch identity, from-scratch generated campaign tree and first campaign-specific commit;
   - ensure inherited storage infrastructure does not become campaign canon;
   - preserve non-force publication and exact creator provenance.

4. **Initial campaign data model/materialization**
   - account for every material current campaign-template root/record needed at creation;
   - distinguish native authority from projections/placeholders/index support;
   - identify stale/retired scaffold structures that must be removed or replaced under the existing pre-release structural-canonicalization authority.

5. **Lifecycle and first-play readiness**
   - prove the state transitions from blank scaffold through provisional onboarding, READY_PC, PLAY_READY and `active`;
   - ensure resumability/durability is truthful at every admitted intermediate state;
   - ensure first normal mechanics-dependent live play cannot outrun required mechanical and persistence readiness.

6. **Player/PC and multiplayer authority**
   - reconcile initial PLAYER/PC creation/binding with singleplayer creator authority and multiplayer active-PLAYER rules;
   - preserve creator-explicit mode changes, `invite_only` default and card projection semantics;
   - do not reopen closed access/multiplayer architecture absent demonstrated insufficiency.

7. **Low-friction product semantics**
   - preserve scaffold-first **invisible** infrastructure and human game-facing handoff;
   - preserve no compulsory Session Zero questionnaire and smallest-material-question behavior;
   - preserve provisional/diegetic onboarding without manufacturing mechanical authority;
   - prevent stale “show technical setup stages” regression text from becoming implementation guidance.

8. **Bidirectional architecture/machine/verification closure**
   - map accepted laws to install/CORE/tool/template/schema/test surfaces;
   - map those surfaces back to one accepted owner or explicit disposition;
   - independently classify scenario-catalog expectations rather than treating `DEV/TESTS/*_CASES.md` as normative;
   - distinguish executable green evidence from semantic currentness of nonexecuted scenario text;
   - leave a concrete downstream realization/test map without starting implementation planning.

---

## 3. Non-goals and explicit boundaries

WP-19 must **not**:

- execute a real campaign, create gameplay content or run campaign bootstrap as a player flow during this audit;
- begin Step 2 before explicit Senior GO;
- begin WP-20 or design future incompatible schema/engine/ruleset migration policy;
- preserve current unreleased scaffold fields/layouts merely for backward compatibility;
- reopen accepted READY_PC, access-control, multiplayer, House-Rules, persistence, Story/Dramaturg or ruleset architecture merely because bootstrap consumes them;
- treat `DEV/TESTS/*_CASES.md`, historical audits or a passing CI run as architecture authority;
- rewrite stale tests/scenarios during Step 1 merely for repository cleanliness;
- build broad world/NPC/faction/lore inventories before the first scene;
- turn `CAMPAIGN_CARD`, README, session/checkpoint/index, test fixture or scenario catalog into canonical gameplay authority;
- introduce a second package/ruleset resolver, creator identity, lifecycle owner or publication authority;
- design implementation tasks or begin substantive runtime/schema/template/test changes;
- activate future/dormant obligations before their trigger.

Future released-campaign compatibility/evolution is explicitly downstream in WP-20. Current WP-19 may define the clean creation-side identity WP-20 later consumes, but it does not decide migration policy.

---

## 4. Established accepted constraints

### 4.1 Campaign choice is explicit

A new chat does not infer campaign continuation from recency, uniqueness or generic play intent. Campaign-specific state/runtime resolution starts only after an unambiguous existing-campaign or New Game choice.

### 4.2 New Game resolves one exact local runtime from storage baseline

For a new campaign, current storage schema v3 `DND_STORAGE.engine.baseline` identifies the storage-owner-approved portable runtime default. It does not install bytes and does not override existing campaigns.

The selected runtime package provides distinct identities:

```text
ENGINE_VERSION.yaml                    semantic engine contract
RUNTIME_PACKAGE.yaml                   built-package provenance
runtime ZIP SHA-256                    exact artifact/cache identity
RUNTIME_PACKAGE.ruleset_set_sha256     exact resolved ruleset-set identity
```

`current_runtime_root` is ephemeral cache only.

### 4.3 New campaign branch and first commit have special semantics

The branch name is neutral `campaign/YYYYMMDD[-NN]` and starts from storage default HEAD for ancestry. The first campaign-specific commit publishes the generated campaign tree from scratch; storage marker/README are excluded.

Campaign creator authority derives from Git provenance of that first campaign-specific commit. Card creator login is a nonauthoritative hint.

### 4.4 Scaffold is produced by one exact materializer

`GAME/TOOLS/init_campaign.py` is authoritative for selected-runtime scaffold generation and requires:

```text
campaign_id
branch
engine_version
package_id
source_commit_sha?       # nullable when provenance truthfully lacks it
package_sha256
ruleset_set_sha256
created_at
creator_github_login
mode
```

It copies selected runtime `CAMPAIGN/` contents into the campaign root and fills technical identity/projection fields only.

### 4.5 Current bootstrap prose has a mechanically settled ruleset-input defect

`00_DND_BOOTSTRAP.md`, `BOOTSTRAP_RUNTIME.md` and `CAMPAIGN_SETUP.md` omit required `--ruleset-set-sha256` from their listed materializer arguments.

Current machine evidence is unambiguous:

- `init_campaign.py` requires and writes it;
- ruleset architecture requires the campaign projection;
- `RUNTIME_PACKAGE.yaml` carries it;
- `test_release_builder.py` validates package production;
- `test_release_integration.py` passes it into the generator.

Later authorized WP-19 work must reconcile these consumers; this is not a Product Owner decision.

### 4.6 Current storage/branch documentation and some scenario catalogs contain stale v2 projections

`DEV/ARCHITECTURE/BRANCH_MODEL.md` and `BOOTSTRAP_STORAGE_REGRESSION_CASES.md:B12` contain storage-v2 / `baseline_version` assumptions while current runtime/schema/executable tests use storage v3 exact baseline identity.

The branch/root/creator laws that remain valid must be preserved separately from stale storage identity text. No backward compatibility is required for the current unreleased scaffold.

### 4.7 Package provenance is package-owned, not reconstructed from mutable tag state

A selected package's exact source provenance comes from its own `RUNTIME_PACKAGE.source_commit_sha` when truthfully present. The current position of a tag may assist bounded comparison where the relevant owner permits it, but must not be used to manufacture the provenance of an already-built package.

Therefore `BOOTSTRAP_STORAGE_REGRESSION_CASES.md:B22` is stale where it requires resolving the published tag to obtain the new-campaign package source SHA.

### 4.8 Campaign projections are not authority

MANIFEST/native owners/Git provenance remain authoritative. Card/README are projections and change only with their owner transitions.

Current card status presentation distinguishes:

```text
initializing -> 🟡
paused       -> ⏸️
active       -> 🟢 (when otherwise eligible)
```

Therefore `CAMPAIGN_CARD_CASES.md:C12` is stale where it assigns 🟡 to both paused and initializing.

### 4.9 Lifecycle states are semantically distinct

```text
scaffold publication
    -> campaign identity exists
    -> initializing

optional PROVISIONAL_IDENTITY
    -> stable setup truth may be durable/resumable
    -> PC may remain provisional
    -> initializing

READY_PC
    -> reconstructable initial mechanical commitment frontier

PLAY_READY
    -> minimum starting/current routing + durable launch state
    -> with READY_PC permits active
    -> first normal mechanics-capable live scene
```

Save does not manufacture readiness. Stopped unfinished setup remains initializing, not paused.

### 4.10 First-play latency is intentionally bounded and technical setup is normally invisible

Accepted runtime behavior is scaffold-first, then human game-facing setup, minimal material questions, minimal starting horizon and immediate launch when the last true blocker is resolved.

`NEW_CAMPAIGN_FAST_PATH.md` has precedence over older setup wording that would expose internal stages. `BOOTSTRAP_STORAGE_REGRESSION_CASES.md:B23` is therefore stale; it must not direct future implementation to announce the character/world/scene setup pipeline.

### 4.11 Menu discovery is card-first

Current campaign discovery probes `CAMPAIGN_CARD.yaml` first and uses MANIFEST only as fallback. `REGRESSION_CASES.md:T13` is stale where it says discovery reads manifests only.

### 4.12 Multiplayer creation consumes closed access architecture

Mode is creator-controlled. `invite_only` is the safe baseline unless explicitly changed. Normal multiplayer gameplay requires active authenticated PLAYER binding. Open-contributor self-enrollment remains the narrow accepted exception.

### 4.13 House-Rules template presence does not reactivate House-Rules design

Scaffold House-Rules files inherit existing policy ownership; copy/materialization is not policy adoption.

### 4.14 Verification evidence is subordinate to current owners

Executable tests and scenario catalogs are implementation/verification consumers. They are essential reverse-conformance evidence but do not create semantic authority by existence, age or pass status.

Current evidence already demonstrates mixed generations:

- executable tests enforce storage/manifest v3 and current package identity;
- some Markdown regression cases still demand storage v2, tag-derived provenance, visible setup stages, old paused icon behavior, or manifest-only campaign discovery.

This mixed state is itself a material WP-19 audit fact.

---

## 5. Quality attributes

Step-2 analysis must evaluate against:

- authority correctness;
- deterministic/reconstructive engine + ruleset identity;
- honest resumability across scaffold/provisional/READY/PLAY_READY states;
- player agency;
- low setup latency and bounded I/O;
- failure containment;
- atomic/current publication;
- projection safety;
- multiplayer authorization safety;
- verification traceability across current owners, executable tests and scenario expectations;
- maintainability: no competing v2/v3 or stale/current verification contracts survive final closure.

Do not invent numerical performance targets not already owned.

---

## 6. Step-2 evidence questions after Senior GO

### A. Storage discovery / explicit selection
1. Do Project Instructions, install bootstrap and CORE bootstrap agree on exact discovery/selection barriers?
2. Does storage v3 have one authoritative baseline shape across runtime docs/schema/tool/tests?
3. Can foreign/friend/development-package paths accidentally grant owner/creator authority?

### B. Exact runtime and ruleset identity
4. Is every creation input derivable from the selected validated package without ambient cache guesses or mutable-tag provenance reconstruction?
5. Is `ruleset_set_sha256` routed exactly once from `RUNTIME_PACKAGE.yaml` to materializer and MANIFEST?
6. Are package failure/mismatch cases finite and fail-closed?
7. Does any human-facing label substitute for exact identity?

### C. Branch/materializer/publication
8. Do branch creation and first root replacement preserve ancestry without storage-byte leakage?
9. Is creator identity unambiguous on first successful publication?
10. Does generator emit exactly intended current root and technical identity fields?
11. Are partial/retry/failure states safe?
12. Do docs/tool/executable tests/scenario cases agree on generator inputs/publication contract, and if not, which expectation is stale?

### D. Manifest/config/card/identity projections
13. Do templates/schemas match accepted owner allocation?
14. Is naming optional/projection-safe?
15. Can card/menu data become authorization or canon accidentally?
16. Are mode/status/location/engine/membership projections current and same-transaction?
17. Do menu scenario expectations match current card-first route and fixed status icons?

### E. PLAYER / PC / provisional onboarding / READY_PC
18. At what durability boundary is stable PLAYER/PC identity first required?
19. Which provisional fields may be absent?
20. Is every READY_PC dependency reconstructable from exact selected ruleset/current owners?
21. Do legacy flattened PC surfaces regain authority anywhere?
22. Can setup inference harden a discretionary choice too late?
23. Do readiness/onboarding scenario and executable tests agree with the accepted owner boundary?

### F. PLAY_READY / first scene / session / resumability
24. What owner set must exist at PLAY_READY?
25. Is minimum starting scene/current routing sufficient without broad world materialization?
26. Does session/recovery distinguish unfinished initializing from active/paused?
27. Is checkpoint creation optional/required only by its actual owner?
28. Does launch preserve projection/currentness/persistence atomically?

### G. Multiplayer and House Rules
29. Does initial multiplayer preserve creator-only mode/join-policy and PLAYER identity?
30. Does card participant projection remain nonauthority?
31. Are default House-Rules surfaces materialized without policy activation by presence?

### H. Architecture <-> machine <-> verification realization
32. For every accepted law, where is the current instruction/schema/template/tool/executable-test destination?
33. For every current template/schema/materializer/setup instruction, what owner/disposition justifies it?
34. For every materially relevant `DEV/TESTS/*_CASES.md` expectation, is it CURRENT, CURRENT WITH QUALIFIER, STALE/SUPERSEDED, HISTORICAL, or downstream/out of scope?
35. Which stale tests/scenarios could misdirect future implementation if copied literally?
36. Which stale/duplicate current surfaces must be canonicalized before WP-19 can close?
37. Which obligations are architecture requirements now but production implementation/test work later?

### I. Product Owner boundary
38. After owner reconciliation, does any residual question genuinely alter product semantics, authority, compatibility, hard-to-reverse lifecycle, material quality trade-off or explicit risk acceptance?
39. If yes, narrow it to decision-ready alternatives first.
40. If no, keep it agent-owned.

### J. WP-20 boundary
41. Which creation identity/version facts are stable inputs to future migration/evolution?
42. Which update/migration test expectations belong strictly to WP-20 and must not leak into WP-19?

---

## 7. Source Manifest / dependency subgraph requirements

Step 2 must use the companion Source Manifest as an evidence ledger, not a closed list. The active subgraph now explicitly includes verification consumers:

```text
INSTALL/PROJECT_INSTRUCTIONS
00_DND_BOOTSTRAP
BOOTSTRAP_RUNTIME
NEW_CAMPAIGN_FAST_PATH
CAMPAIGN_SETUP
    -> STORAGE / dnd_storage schema
    -> BRANCH_MODEL / ACCESS_CONTROL
    -> RULESET_PACKAGE_IDENTITY / machine closure / ENGINE_UPDATES boundary
    -> release package producer
    -> init_campaign materializer
    -> GAME/CAMPAIGN tree + MANIFEST/CONFIG/CARD/CURRENT
    -> campaign/storage/card/current/session/player/pc schemas
    -> PERSISTENCE / RUNTIME / DURABILITY_GUARD
    -> CAMPAIGN_IDENTITY / CAMPAIGN_CARD
    -> CHARACTER_READINESS / canonical READY_PC owner / DIEGETIC_ONBOARDING
    -> SESSION / MULTIPLAYER / CAMPAIGN_HOUSE_RULES
    -> executable producer/identity/integration/readiness/ruleset tests
    -> bootstrap/install/card/identity/readiness/onboarding/durability/save/access/persistence/latency scenario catalogs
    -> item-level currentness/supersession disposition
    -> WP-20 update/evolution test boundary
```

Derivative indexes, historical audits and test names never substitute for actual owners.

---

## 8. Failure scenarios later architecture must survive

At minimum:

1. one existing campaign exists but user only says “let's play”;
2. storage baseline package exists but another cached runtime entered bootstrap;
3. selected package ruleset differs from ambient/older package;
4. generator is invoked without required ruleset digest;
5. generator fails after branch creation but before first campaign-specific commit;
6. initial ref publication races/fails;
7. storage README/marker leaks into campaign tree;
8. scaffold succeeds and chat ends before protagonist selection;
9. stable protagonist is durable before READY_PC and chat ends;
10. READY_PC exists but PLAY_READY/current-scene publication is incomplete;
11. save during initializing setup;
12. card says active but readiness/lifecycle owners disagree;
13. singleplayer collaborator tries to publish setup changes;
14. multiplayer selected without valid applicable PLAYER authorization;
15. stale Storage-v2 B12 expectation is followed instead of current v3 owner;
16. stale B22 tag-resolution expectation overwrites package-owned provenance;
17. stale B23 setup-stage narration is implemented despite fast-path precedence;
18. stale Campaign Card C12 maps paused to 🟡 instead of ⏸️;
19. stale T13 manifest-only menu discovery bypasses current card-first fast path;
20. a passing executable suite is treated as proof that all Markdown scenarios are current;
21. a legacy/flattened PC surface is treated as authority despite qualifier;
22. future migration concerns preserve obsolete current scaffold structures despite pre-release canonicalization authority.

---

## 9. Senior recovery verification qualifier

SR19-01 established a material framing defect in the original Step-1 reverse-conformance claim: the original Source Manifest/critic named the materializer, schemas, package producer and `test_release_integration.py`, but did not inspect the directly affected verification/scenario subgraph deeply enough to support the claimed test coverage.

Recovery independently inspected, among others:

- bootstrap/storage/install/menu/identity scenario families;
- readiness/diegetic/durability/save scenario families;
- access/multiplayer/persistence/runtime-latency scenario families;
- package provenance/build/integration executable tests;
- storage/manifest identity executable tests;
- S6D READY_PC and ruleset-package closure executable tests;
- engine update/mismatch neighbors for WP-20 routing;
- historical pre-release audit evidence.

The recovered evidence found no contradiction requiring upstream architecture reopen. Instead it found stale/qualified verification expectations with already-settled current owners.

This materially changes the **evidence requirements** of Step 2, but not the accepted WP-19 product semantics or architecture direction.

---

## 10. Product Owner decision status after recovery

Current owners already settle:

- explicit campaign choice and low-friction invisible setup;
- creator/access authority;
- exact engine/ruleset creation identities;
- package-owned provenance;
- card-first menu/status projection;
- provisional onboarding vs READY_PC vs PLAY_READY;
- current pre-release compatibility policy;
- future migration ownership in WP-20;
- multiplayer and House-Rules boundaries.

The stale verification expectations are technical supersession/consistency defects.

```text
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
```

---

## 11. Recovered Step-1 exit criteria

```text
[x] Task-specific Source Manifest constructed beyond initial scope inventory.
[x] Actual bootstrap/storage/access/ruleset/readiness/persistence owners inspected.
[x] Current templates/schemas/materializer/package producers included.
[x] Directly implicated executable verification families inspected.
[x] Directly implicated scenario/regression families independently discovered and inspected.
[x] Material scenario expectations receive item-level current/stale/qualified/downstream disposition.
[x] Architecture Task Brief now makes verification reverse-conformance explicit.
[x] Product Owner boundary rechecked after evidence expansion.
[x] Whole-project critic recovered for SR19-01.
[x] Original two BLOCKING findings remain confirmed/closed.
[x] No mechanically resolvable BLOCKING/SIGNIFICANT framing omission remains knowingly delegated to Senior.
[x] Step 2 remains unauthorized and unstarted.
[x] WP-20 remains unstarted.
[x] Implementation planning remains unauthorized and unstarted.
```

The next process action after recovery publication is **mandatory Senior re-review**. Only explicit Senior GO may authorize WP-19 Step 2.
