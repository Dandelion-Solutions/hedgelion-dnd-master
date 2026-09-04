# R2.7 WP-19 — Bootstrap / Campaign Creation / Initial Materialization — Architecture Task Brief

Status: **STEP 1 COMPLETE — MANDATORY SENIOR REVIEW CANDIDATE**

Date: 2026-09-05

Verified Step-1 execution basis: `5fc24905be5c9e1b47929ee9e7b49ea8b9f2a053`

This is the Architecture Task Brief required by the current HDM design process for WP-19. It frames Step-2 evidence/research only. It does not authorize or begin Step 2, WP-20, implementation planning, gameplay bootstrap, campaign creation, or substantive runtime/schema/template implementation.

Companion Step-1 artifacts:

- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief-critic.md`.

---

## 1. Problem statement

WP-19 must audit and reconcile the complete architecture-to-machine path by which an explicit **New Game** choice becomes a correctly owned, resumable campaign and then reaches the first normal mechanics-capable play frontier.

The domain is broader than copying an empty directory and narrower than ordinary gameplay. It spans several already-owned boundaries that must compose without ambiguity:

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

WP-19 must prove that every transition above has one accepted authority, correct input provenance, an honest machine/runtime destination, bounded failure semantics and a resumable publication boundary where required.

It must also perform the reverse audit: every current bootstrap instruction, materializer input, campaign-template field/root, schema constraint, setup projection and relevant test must have an accepted semantic owner or be explicitly classified as stale, derived, implementation-only, historical, safely deferred or out of scope.

The audit must not collapse technical scaffold creation, provisional onboarding, READY_PC and PLAY_READY into one generic concept of “campaign ready”. Those states have different semantic and durability meanings under existing owners.

---

## 2. Goals

WP-19 Step 2, if Senior-authorized, must establish all of the following.

1. **Creation preconditions and selection authority**
   - prove the storage discovery/selection and explicit campaign-choice gate;
   - prove which principal may create/publish the campaign and how creator identity becomes stable evidence;
   - prevent ambient package, previous chat, sole-campaign presence or repository permission from silently choosing semantic authority.

2. **Exact runtime/ruleset creation identity**
   - establish one reconstructive chain from selected storage baseline through the validated runtime package to campaign `engine.created_with/current` and `ruleset.created_with/current`;
   - reconcile every current bootstrap/materializer/test consumer of that identity;
   - fail closed rather than inventing missing provenance.

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
   - preserve the accepted player-facing contract: no installation-wizard behavior after successful scaffold publication, no compulsory Session Zero questionnaire, ask only material unresolved choices, no ceremonial confirmation when nothing blocks launch;
   - preserve provisional/diegetic onboarding where allowed without manufacturing mechanical authority.

8. **Bidirectional architecture/machine closure**
   - map accepted laws to install/CORE/tool/template/schema/test surfaces;
   - map those machine surfaces back to one accepted owner or explicit disposition;
   - leave a concrete downstream realization/test map without starting implementation planning.

---

## 3. Non-goals and explicit boundaries

WP-19 must **not**:

- execute a real campaign, create gameplay content or run campaign bootstrap as a player flow during the architecture audit;
- begin Step 2 before the mandatory Senior Step-1 GO;
- begin WP-20 or design future incompatible schema/engine/ruleset migration policy;
- preserve current unreleased scaffold fields/layouts merely for backward compatibility — the owner has explicitly stated no real campaigns depend on them;
- reopen accepted READY_PC, access-control, multiplayer, House-Rules, persistence, Story/Dramaturg or ruleset architecture merely because bootstrap consumes those owners;
- build broad world/NPC/faction/lore inventories before the first scene;
- turn `CAMPAIGN_CARD`, README, session/checkpoint/index or template placeholders into canonical gameplay authority;
- introduce a second package/ruleset resolver, second creator identity, second lifecycle owner or second publication authority;
- design implementation tasks or begin substantive runtime/schema/template code changes;
- treat future/dormant obligations as current work without their trigger.

Future released-campaign compatibility/evolution is explicitly downstream in WP-20. Current WP-19 may define the clean creation-side identity that WP-20 will later consume, but it does not decide the migration policy.

---

## 4. Established accepted constraints

### 4.1 Campaign choice is explicit

A new chat does not infer campaign continuation from recency, uniqueness or generic play intent. Campaign-specific state/runtime resolution starts only after an unambiguous existing-campaign or New Game choice.

This is already an accepted agency and latency rule in current bootstrap owners; WP-19 audits its composition, not whether to keep it.

### 4.2 New Game resolves one exact local runtime from storage baseline

For a new campaign, `DND_STORAGE.engine.baseline` identifies the storage-owner-approved portable runtime default. It does not install bytes and does not override existing campaigns.

The selected local runtime package provides:

```text
ENGINE_VERSION.yaml              semantic engine contract
RUNTIME_PACKAGE.yaml             exact built-package provenance
runtime ZIP SHA-256              exact artifact/cache identity
RUNTIME_PACKAGE.ruleset_set_sha256
                                 exact embedded resolved ruleset-set identity
```

One isolated `current_runtime_root` is ephemeral session cache only and must never become campaign/storage authority.

### 4.3 New campaign branch and first commit have special semantics

The branch name is neutral `campaign/YYYYMMDD[-NN]` and starts from current storage default-branch HEAD for ancestry. The first campaign-specific commit publishes a generated campaign tree **from scratch**; storage marker/README or other inherited storage-root data are not campaign canon.

Campaign creator authority derives from Git provenance of that first campaign-specific initialization commit. Card creator login remains a nonauthoritative hint.

### 4.4 Scaffold is produced by one exact materializer

`GAME/TOOLS/init_campaign.py` is the authoritative scaffold materializer for the selected runtime package. The current generator requires at least:

```text
campaign_id
branch
engine_version
package_id
source_commit_sha?        # nullable where package provenance truthfully has none
package_sha256
ruleset_set_sha256
created_at
creator_github_login
mode
```

It copies the selected runtime package's `CAMPAIGN/` template contents into the future campaign root and fills technical identity/projection fields only. It does not create gameplay lore and does not contact GitHub.

The materialized `MANIFEST.engine.created_with/current` start equal. `MANIFEST.ruleset.created_with/current` start from the exact package ruleset-set identity.

### 4.5 Current bootstrap prose has a mechanically settled cross-contract defect

Current `00_DND_BOOTSTRAP.md`, `BOOTSTRAP_RUNTIME.md` and `CAMPAIGN_SETUP.md` list the generator identity arguments but omit required `--ruleset-set-sha256`.

Current machine evidence is unambiguous:

- `init_campaign.py` requires the argument and writes both ruleset projections;
- canonical ruleset-package architecture requires the campaign projection;
- release-package metadata carries `ruleset_set_sha256`;
- `test_release_integration.py` invokes the generator with `package_meta["ruleset_set_sha256"]`.

Therefore Step 2 must reconcile the affected runtime/instruction surfaces to the accepted exact identity chain. This is not a Product Owner decision and does not justify inventing a new ruleset-selection policy.

### 4.6 Current storage/branch documentation contains stale v2 projections

`DEV/ARCHITECTURE/BRANCH_MODEL.md` still contains storage-v2 / `baseline_version` and older campaign engine-provenance wording while later/current owners use storage v3 exact package baseline and manifest-v3 sibling engine/ruleset identity.

The useful branch/root/creator laws remain relevant. Step 2 must determine the precise current owner/supersession repair instead of treating the whole document as either automatically authoritative or automatically obsolete.

No compatibility preservation is required for the current unreleased scaffold. R2.7 owner clarification already settles that policy; no Product Owner compatibility gate remains merely because stale v2 prose exists.

### 4.7 Campaign projections are not authority

`MANIFEST` owns campaign lifecycle/mode/current engine/ruleset/storage routes; native PC/PLAYER/STATE/WORLD records and Git provenance own their respective facts. `CAMPAIGN_CARD` and campaign README are human/menu projections.

Projection updates join the same coherent campaign transaction as their owner changes. Projection freshness alone never creates a persistence boundary.

### 4.8 Lifecycle states are semantically distinct

The accepted creation/readiness path is:

```text
SCaffold publication
    -> campaign identity exists
    -> lifecycle initializing

optional PROVISIONAL_IDENTITY
    -> stable protagonist/Actor/setup truth may be durable/resumable
    -> PC still provisional where mechanics remain unresolved
    -> lifecycle still initializing

READY_PC
    -> reconstructable initial mechanical commitment frontier
    -> exact required current mechanics exist
    -> still does not alone imply campaign activation

PLAY_READY
    -> minimum starting location/current-scene/routing + required durable launch state
    -> with READY_PC authorizes lifecycle active
    -> first true normal mechanics-capable live scene
```

An explicit save before PLAY_READY does not manufacture readiness. Stopped unfinished setup remains `initializing`, not `paused`.

### 4.9 First-play latency is intentionally bounded

Accepted runtime behavior prefers:

- scaffold first, invisibly;
- then human-facing setup;
- minimal protagonist questions;
- accepted defaults/inference for nonmaterial preferences;
- minimal starting horizon only;
- immediate launch when the last true blocker is resolved.

No current requirement justifies a broad pre-generated world or a setup questionnaire merely because template/schema capacity exists.

### 4.10 Multiplayer creation consumes closed access architecture

Mode is creator-controlled. `invite_only` is the safe baseline unless explicitly changed. Normal multiplayer gameplay requires an active authenticated PLAYER binding under current access owners.

WP-19 may discover a bootstrap consumer mismatch, but closed WP-16/access semantics reopen only for demonstrated contradiction, a newly unsatisfied consumer or material insufficiency.

### 4.11 House-Rules template presence does not reactivate House-Rules design

Current scaffold includes `RULES/HOUSE_RULES.md` and `RULES/HOUSE_RULES.yaml`. Their semantic ownership remains the accepted House-Rules architecture. Copying an empty/default policy surface is initial materialization, not a new policy decision.

---

## 5. Quality attributes that distinguish a correct WP-19 result

Step-2 alternatives/recommendations must be evaluated against the actual accepted product/runtime qualities:

- **authority correctness** — one owner for creator, package/ruleset identity, lifecycle and canonical gameplay state;
- **deterministic/reconstructive identity** — a created campaign records enough exact engine/ruleset provenance to resolve later without ambient-memory guesses;
- **resumability** — every admitted durable intermediate state can be recovered honestly;
- **player agency** — campaign selection and material character choices are not guessed from convenience metadata;
- **low setup latency / bounded I/O** — no broad repository/package/world scans or unnecessary commits merely to begin play;
- **failure containment** — malformed package/materializer/publication stops rather than silently synthesizing a different scaffold;
- **atomicity/currentness** — initial and later setup publications have explicit coherent transaction shapes;
- **projection safety** — menu/README/session convenience data never gains canonical authority;
- **multiplayer safety** — collaborator access does not become PLAYER or creator authority;
- **testability** — package -> generator -> template/schema -> publication/readiness invariants have concrete executable verification points;
- **maintainability** — stale v2/current v3 dual descriptions do not survive as competing live contracts.

Do not invent numerical latency/throughput targets not already owned by the project.

---

## 6. Step-2 evidence questions after Senior GO

### A. Storage discovery / explicit selection

1. Do Project Instructions, install bootstrap and CORE bootstrap agree on the exact discovery/selection barrier?
2. Does storage v3 have one authoritative baseline shape across runtime docs/schema/template/support surfaces?
3. Can a foreign/friend storage or development package path accidentally grant storage-owner or campaign-creator authority?

### B. Exact runtime and ruleset package identity

4. Is every creation input derivable from the selected validated package without mutable-tag archaeology or ambient cache assumptions?
5. Is `ruleset_set_sha256` routed exactly once from `RUNTIME_PACKAGE.yaml` into the materializer and campaign MANIFEST projections?
6. Are package failure/mismatch cases finite and fail-closed?
7. Does any human-facing baseline label accidentally substitute for exact ruleset identity?

### C. Branch/materializer/publication

8. Do branch creation, first commit and campaign root replacement preserve storage ancestry without copying storage infrastructure into campaign canon?
9. Is creator identity unambiguous on first successful campaign publication?
10. Does the generator emit exactly the intended current campaign root and only technical identity fields?
11. Are partial publication/retry/failure states safe, with no half-created campaign treated as ready?
12. Do current docs/tool/test agree on all generator arguments and validation requirements?

### D. Manifest/config/card/identity projections

13. Do manifest/card/config templates and schemas match accepted owner allocation?
14. Is campaign naming optional and projection-safe from the first setup transaction onward?
15. Can card/menu data ever be mistaken for authorization or current canon after selection?
16. Are mode/status/current-location/engine/membership projections updated only with their native owners?

### E. PLAYER / PC / provisional onboarding / READY_PC

17. At what exact durability boundary is stable PLAYER/PC identity first required for singleplayer and multiplayer?
18. Which provisional fields may be absent without blocking honest onboarding?
19. Is every READY_PC-required mechanical dependency reconstructable from the exact selected ruleset/current owners?
20. Do any legacy flattened PC schema surfaces accidentally regain authority during bootstrap?
21. Can a player-facing setup inference improperly harden a discretionary mechanical choice after situational information is known?

### F. PLAY_READY / first scene / session / resumability

22. What exact owner set must exist coherently at PLAY_READY for honest resume and ordinary mechanics-dependent play?
23. Is the minimum starting scene/current routing represented without inventing broad unused world state?
24. Does initial session/recovery state distinguish an unfinished initializing campaign from an active/paused campaign?
25. Are checkpoint creation and session files optional/required only under their actual owners rather than ceremony?
26. Does the first active launch transaction preserve projection/currentness/persistence invariants atomically?

### G. Multiplayer and House Rules

27. Does new multiplayer setup preserve creator-only mode/join-policy authority and active PLAYER identity from the first applicable write?
28. Does card participant projection remain a hint/cache rather than access authority?
29. Are empty/default House-Rules surfaces created with the intended accepted baseline without triggering policy adoption or executable mechanics by presence alone?

### H. Architecture <-> machine realization

30. For every accepted bootstrap/creation/readiness law, where is the current instruction/schema/template/tool/test destination?
31. For every current campaign-template root/schema/materializer field/setup instruction, what accepted owner or explicit disposition justifies it?
32. Which stale/duplicate current surfaces must be structurally canonicalized before WP-19 can close?
33. Which behavioral obligations are architecture requirements now but production implementation/test work later?

### I. Product Owner boundary

34. After owner reconciliation, does any remaining question genuinely alter product semantics, canonical authority, meaningful compatibility, hard-to-reverse lifecycle behavior, material quality trade-off or explicit risk acceptance?
35. If yes, can all technical evidence first narrow it to decision-ready alternatives with a recommendation?
36. If no, keep it agent-owned and do not create an artificial human approval gate.

### J. WP-20 boundary

37. Which creation-side identity/version facts must be stable inputs to later migration/evolution?
38. Which questions are strictly future released-campaign compatibility and therefore must remain deferred until WP-20 authorization?

---

## 7. Source Manifest / dependency subgraph requirements

Step 2 must use the companion Source Manifest as a starting evidence ledger, not a closed list. If research exposes another actual owner/consumer capable of changing the conclusion, add it and inspect it.

At minimum the active evidence subgraph includes:

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
    -> campaign/storage/card/current schemas
    -> PERSISTENCE / RUNTIME / DURABILITY_GUARD
    -> CAMPAIGN_IDENTITY / CAMPAIGN_CARD
    -> CHARACTER_READINESS / canonical READY_PC owner / DIEGETIC_ONBOARDING
    -> SESSION + session/player/pc schemas
    -> MULTIPLAYER
    -> CAMPAIGN_HOUSE_RULES + template policy files
    -> release integration / other implicated executable tests
```

Derivative indexes/roadmaps never substitute for those owners.

---

## 8. Failure scenarios the later architecture must survive

Step 2 must challenge at least these concrete cases where applicable:

1. one existing campaign exists but user only says “let's play”;
2. storage baseline package exists but a different cached runtime was used to enter bootstrap;
3. selected package ruleset set differs from an ambient/older package;
4. generator is invoked without a required ruleset set digest;
5. generator fails after branch creation but before first campaign-specific commit;
6. initial ref publication races or fails;
7. storage README/marker accidentally enters the campaign tree;
8. scaffold commit succeeds and the chat ends before protagonist selection;
9. stable protagonist becomes durable before READY_PC and the chat ends;
10. READY_PC is achieved but PLAY_READY/current-scene publication is not yet complete;
11. a save is requested during initializing setup;
12. card says active but authoritative readiness/lifecycle sources do not;
13. singleplayer repository collaborator tries to publish setup changes;
14. multiplayer is selected but no valid active PLAYER binding exists yet;
15. a legacy/stale storage-v2 branch document is followed instead of current v3 schema/runtime owner;
16. a stale/flattened PC schema field is treated as authority despite its explicit nonauthoritative qualifier;
17. future migration concerns are used to preserve obsolete current scaffold structures despite the owner-approved pre-release canonicalization boundary.

---

## 9. Product Owner decision status at Step 1

The dedicated Step-1 Product Owner watch found no genuine residual human-owned decision.

Established owners already settle:

- explicit campaign choice and low-friction setup semantics;
- creator/access authority;
- exact engine/ruleset creation identity classes;
- provisional onboarding versus READY_PC versus PLAY_READY lifecycle;
- current pre-release compatibility policy;
- future migration ownership in WP-20;
- projection/nonauthority boundaries;
- multiplayer default authority and House-Rules baseline semantics.

The observed runtime/document contradictions are technical consistency defects against those accepted owners.

```text
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
```

If Step 2 later establishes a true contradiction/material insufficiency rather than a stale consumer, the normal design process governs escalation. Step 1 does not pre-authorize such a reopen.

---

## 10. Step-1 exit criteria

This Task Brief is review-ready only together with its Source Manifest and independent whole-project critic.

Step-1 exit requires:

```text
[x] Task-specific Source Manifest constructed beyond the initial scope inventory.
[x] Actual owning bootstrap/storage/access/ruleset/readiness/persistence sources inspected.
[x] Current templates/schemas/materializer/release-test consumers included.
[x] Architecture Task Brief defines scope, goals, non-goals, invariants, quality attributes and evidence questions.
[x] Product Owner boundary explicitly tested.
[x] Whole-project Task-Brief critic performed independently through DEV/PROJECT_MAP and actual owners.
[x] Every mechanically resolvable BLOCKING/SIGNIFICANT framing defect repaired in the Step-1 package.
[x] No residual framing blocker/significant omission is knowingly delegated to Senior.
[x] Step 2 remains unauthorized and unstarted.
[x] Implementation planning remains unauthorized and unstarted.
```

The next process action after publication is the **mandatory Senior Step-1 review**. Senior may grant or withhold GO for Step 2; this Task Brief cannot grant it itself.
