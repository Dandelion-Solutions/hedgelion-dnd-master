# R2.7 WP-19 — Bootstrap / Campaign Creation / Initial Materialization — Source Manifest

Status: **STEP 1 SENIOR RECOVERY COMPLETE — SR19-01 CLOSED — MANDATORY SENIOR RE-REVIEW**

Date: 2026-09-05

Original Step-1 execution basis: `5fc24905be5c9e1b47929ee9e7b49ea8b9f2a053`

Senior-recovery basis: `df5fe6441c2b85e9cbffcb6f83caa885501da794`

Domain:

> **Bootstrap / campaign creation / initial materialization**

This manifest is the task-specific discovery/evidence route required by `DEV/DESIGN_PROCESS.md` and `DEV/ARCHITECTURE/DESIGN_PROCESS.md`. It is intentionally broader than the initial WP-19 scope inventory. The inventory, roadmap, project map and canonical index are routing aids; correctness-sensitive framing below is based on actual current owners, runtime consumers, schemas, templates, tools, executable tests and scenario/regression catalogs inspected on the verified public bases.

Senior recovery SR19-01 expands the verification reverse-conformance leg. It does not reopen the original WP-19 findings, authorize Step 2, WP-20, implementation planning, gameplay bootstrap or substantive runtime/schema/template/test implementation.

Companion Step-1 artifacts:

- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief-critic.md`.

---

## 1. Discovery route

The independently reconstructed WP-19 route is:

```text
current progress / R2.7 program authority
    -> project-map campaign-creation route
    -> Project Instructions / install bootstrap
    -> runtime bootstrap / explicit campaign-choice gate
    -> storage baseline + exact runtime/ruleset package identity
    -> branch / creator / access-control ownership
    -> new-campaign fast path + campaign setup
    -> exact init_campaign materializer
    -> campaign template + manifest/card/config/current-state schemas
    -> first campaign-specific publication / persistence transport
    -> campaign identity/card projections
    -> PLAYER / PC / provisional onboarding / READY_PC / PLAY_READY
    -> session / resumability / first true live scene
    -> multiplayer initial mode / join policy / PLAYER authority
    -> House-Rules default materialization
    -> release/package producer and executable contract tests
    -> DEV/TESTS scenario/regression catalogs
    -> current-owner reverse-conformance disposition per material expectation
    -> WP-20 future compatibility boundary
```

The SR19-01 recovery did **not** treat the Senior-provided file list as an answer key. It started from current `DEV/PROJECT_MAP.md`, enumerated `DEV/TESTS/`, then followed the actual bootstrap/storage/package/readiness/persistence/access/test dependency graph.

A critical evidence rule emerged and is now explicit:

```text
TEST EXISTS / CI GREEN != EXPECTATION IS CURRENT ARCHITECTURE
```

`DEV/TESTS/test_*.py` and `DEV/TESTS/*_CASES.md` are verification evidence/consumers. Current owning architecture/runtime/schema contracts remain authoritative when a test or scenario expectation is stale.

---

## 2. Source-role manifest

### 2.1 Process, current state and R2.7 scope

| Source | Role | WP-19 disposition |
|---|---|---|
| `AGENTS.md` | CANONICAL repository process | Current process/runtime overlay and publication discipline. |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | REQUIRED runtime overlay | Connector-only remote work and current-runtime constraints. |
| `DEV/DESIGN_PROCESS.md` | CANONICAL development process | Source Manifest, evidence-completeness, decision rights, Step-1 critic/repair discipline. |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | CANONICAL HDM process adapter | Whole-project critic and mandatory Senior gate. |
| `DEV/CURRENT_PROGRESS.md` | CANONICAL global progress authority | WP-19 Step 1 only; Step 2 blocked until Senior GO. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md` | TASK-LOCAL cursor | WP-19 local gate/status. |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | DERIVATIVE sequencing owner | Routing/sequence only. |
| `DEV/PROJECT_MAP.md` | DERIVATIVE routing index | Used to reconstruct owners **and verification routes**; explicitly gives tests no presumption of correctness against superseding owners. |
| `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | DERIVATIVE locator | Owner discovery only. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md` | R2.7 program brief | Bidirectional architecture<->machine audit requirement. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md` | DESIGN PROVENANCE | Initial minimum inventory only; expanded independently. |
| `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md` | CANONICAL OWNER DECISION | No real campaigns require compatibility with unreleased scaffold; direct R2.7 structural canonicalization allowed; future released-campaign evolution belongs to WP-20. |

### 2.2 Runtime bootstrap and campaign-creation owners

| Source | Role | WP-19 disposition |
|---|---|---|
| `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` | RUNTIME ENTRY CONSUMER | Current bootstrap entry/guardrails. |
| `GAME/INSTALL/00_DND_BOOTSTRAP.md` | RUNTIME INSTALL/BOOTSTRAP OWNER | Package/storage/menu/New Game/publication path. |
| `GAME/CORE/BOOTSTRAP_RUNTIME.md` | RUNTIME BOOTSTRAP OWNER | Exact package binding, storage v3, explicit choice barrier. |
| `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` | RUNTIME NEW-CAMPAIGN PRECEDENCE OWNER | Scaffold-first ordering, one generator, invisible infrastructure, low-friction handoff. |
| `GAME/CORE/CAMPAIGN_SETUP.md` | RUNTIME SETUP OWNER | Initial package/materialization, low-friction setup, provisional/READY/PLAY_READY flow. |
| `GAME/TOOLS/init_campaign.py` | MACHINE MATERIALIZER | Authoritative scaffold generator and required identity inputs. |

### 2.3 Storage, branch, creator and publication authority

| Source | Role | WP-19 disposition |
|---|---|---|
| `GAME/CORE/STORAGE.md` | RUNTIME STORAGE OWNER | Current storage/root/runtime-baseline behavior. |
| `GAME/SCHEMA/dnd_storage.schema.yaml` | MACHINE CONTRACT | Storage schema v3 and exact portable `engine.baseline`. |
| `DEV/ARCHITECTURE/BRANCH_MODEL.md` | ACCEPTED OWNER WITH STALE PROJECTIONS | Branch/root/creator laws remain relevant; storage-v2 / `baseline_version` and old provenance text are stale against current owners. |
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | ACCEPTED ACCESS OWNER WITH QUALIFIED STALE WORDING | Creator/PLAYER/ref authority is current; isolated storage-v2/old engine-maintenance phrasing is reconciled through later storage/engine owners, not preserved as a second policy. |
| `GAME/CORE/PERSISTENCE.md` | RUNTIME PUBLICATION OWNER | Initial scaffold from-scratch exception; later base-tree campaign transactions. |
| `GAME/CORE/RUNTIME.md` | RUNTIME INVARIANT OWNER | Ref/write/lifecycle routing. |

### 2.4 Exact runtime/ruleset identity and package machine closure

| Source | Role | WP-19 disposition |
|---|---|---|
| `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` | CANONICAL S6D OWNER | Exact `ruleset_set_sha256`; campaign sibling created/current projection. |
| `DEV/ARCHITECTURE/RULESET_PACKAGE_MACHINE_CLOSURE.md` | CANONICAL MACHINE-CLOSURE OWNER | Exact lock/set/conformance evidence. |
| `GAME/CORE/ENGINE_UPDATES.md` | RUNTIME IDENTITY/UPDATE OWNER | Creation-side storage-baseline/campaign-current distinction; future incompatible migration downstream. |
| `DEV/TOOLS/release_builder.py` | PACKAGE PRODUCER | Produces `RUNTIME_PACKAGE.yaml` with exact ruleset lock/set/provenance. |

### 2.5 Campaign template, schemas and projections

| Source | Role | WP-19 disposition |
|---|---|---|
| `GAME/CAMPAIGN/` | MACHINE TEMPLATE FAMILY | Current generated campaign root topology. |
| `GAME/CAMPAIGN/MANIFEST.yaml` | TEMPLATE | v3 engine/ruleset/lifecycle seed. |
| `GAME/SCHEMA/campaign_manifest.schema.yaml` | MACHINE CONTRACT | Current branch/lifecycle/engine/ruleset authority. |
| `GAME/CAMPAIGN/CAMPAIGN_CARD.yaml` | TEMPLATE PROJECTION | Initial menu projection. |
| `GAME/SCHEMA/campaign_card.schema.yaml` | MACHINE CONTRACT | Card nonauthority and active/readiness invariants. |
| `GAME/CORE/CAMPAIGN_CARD.md` | RUNTIME PROJECTION OWNER | Current menu icons/status/projection behavior. |
| `GAME/CORE/CAMPAIGN_IDENTITY.md` | RUNTIME CAMPAIGN-IDENTITY OWNER | MANIFEST name authority, README/card projections. |
| `GAME/CAMPAIGN/CONFIG.yaml` | TEMPLATE / CAMPAIGN CONFIG | Optional setup defaults/preferences surface. |
| `GAME/CAMPAIGN/STATE/CURRENT.yaml` + `GAME/SCHEMA/current_state.schema.yaml` | TEMPLATE + MACHINE CONTRACT | Compact current routing seed/shape. |

### 2.6 Character/readiness/first-play and resumability owners

| Source | Role | WP-19 disposition |
|---|---|---|
| `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md` | CANONICAL READY_PC OWNER | Reconstructable legal initial mechanics. |
| `GAME/CORE/CHARACTER_READINESS.md` | RUNTIME READINESS OWNER | READY_PC runtime semantics. |
| `GAME/CORE/DIEGETIC_ONBOARDING.md` | RUNTIME PRE-READY OWNER | Provisional locally-sufficient play and stable identity boundary. |
| `GAME/CORE/DURABILITY_GUARD.md` | RUNTIME DURABILITY/LIFECYCLE OWNER | PROVISIONAL_IDENTITY / READY_PC / PLAY_READY boundaries. |
| `GAME/CORE/SESSION.md` | RUNTIME SESSION/RESUME OWNER | Initializing setup/resume semantics. |
| `GAME/SCHEMA/session.schema.yaml` | MACHINE CONTRACT | Coordination/recovery shape. |
| `GAME/SCHEMA/player.schema.yaml` | MACHINE CONTRACT | Stable PLAYER binding and preferences. |
| `GAME/SCHEMA/pc.schema.yaml` | MACHINE CONTRACT / PARTLY LEGACY PROJECTION | Provisional/active and READY_PC requirement; explicit nonauthoritative flattened surfaces remain qualified. |

### 2.7 Multiplayer and House-Rules neighbors

| Source | Role | WP-19 disposition |
|---|---|---|
| `GAME/CORE/MULTIPLAYER.md` | RUNTIME MULTIPLAYER OWNER | Creator-explicit mode, invite-only default, PLAYER authority. |
| `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` | CANONICAL HOUSE-RULES OWNER | Existing default/policy semantics; no reopen by template presence. |
| `GAME/CAMPAIGN/RULES/HOUSE_RULES.md` + `HOUSE_RULES.yaml` | TEMPLATE PROJECTIONS | Inherited scaffold surfaces. |

### 2.8 Verification / scenario reverse-conformance subgraph — SR19-01 recovery expansion

The following families were independently located and read because they can constrain or misdirect WP-19 realization. Disposition applies to the **material expectation**, not automatically to the entire file.

#### Direct bootstrap/storage/runtime-package verification

| Source | Material expectation(s) | Disposition |
|---|---|---|
| `DEV/TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md` | B01-B11 discovery/local-package/Connector/storage-selection laws | **CURRENT**, subject to current bootstrap owners. |
| same | B12 says fresh storage creates **v2** marker with v2 framing | **STALE / SUPERSEDED** by `dnd_storage.schema.yaml` v3 + current bootstrap storage-v3 baseline. |
| same | B12a/B12b interrupted init / no silent repurpose | **CURRENT WITH QUALIFIER**: retry/no-repurpose law current, marker emitted is v3. |
| same | B14-B21 card-first discovery, root layout, generator/publication, dev package provenance | **CURRENT**; B16 legacy fallback is compatibility-only and does not create a preservation requirement for unreleased scaffold. |
| same | B22 says normal release resolves published tag to exact commit before new campaign | **STALE / SUPERSEDED**: exact source provenance comes from selected ZIP `RUNTIME_PACKAGE.source_commit_sha`; mutable-current-tag archaeology must not manufacture old-package provenance. |
| same | B23 says tell player technical setup has visible character/world/scene stages | **STALE / SUPERSEDED** by `NEW_CAMPAIGN_FAST_PATH` precedence: successful scaffold/setup plumbing is invisible; no internal setup-plan narration by default. |
| same | B24 | **CURRENT**: character before broad unused worldbuilding. |
| same | B25 | **CURRENT WITH QUALIFIER**: launch when READY_PC + minimum PLAY_READY are satisfied; checkpoint is optional unless its owner independently requires one. |
| same | B26-B45 | **CURRENT** in the WP-19-relevant portions: explicit choice, generator-only scaffold, one initialization transaction, provisional/PLAY_READY separation, technical silence, UTF-8 transport. |
| `DEV/TESTS/test_multi_runtime_bootstrap_contract.py` | multiple ZIPs, isolated `current_runtime_root`, package provenance, dev-package repository-owner gate | **CURRENT** direct executable contract. |
| `DEV/TESTS/test_multi_runtime_release_consistency.py` | campaign/storage schemas both v3; retired `baseline_version` absent from active runtime | **CURRENT** and directly contradicts stale B12 scenario wording. |
| `DEV/TESTS/test_runtime_identity_schema.py` | manifest/storage v3 portable identity + generator identity shape | **CURRENT** direct executable contract; ruleset projection coverage is not complete by this test alone. |
| `DEV/TESTS/test_runtime_package_provenance.py` | exact package provenance producer behavior | **CURRENT** supporting producer evidence. |
| `DEV/TESTS/test_release_builder.py` | runtime package contains exact `ruleset_set_sha256`, lock and conformance evidence; flat package | **CURRENT** direct producer evidence. |
| `DEV/TESTS/test_release_integration.py` | release ZIP -> generator, explicitly passes package `ruleset_set_sha256`, root-layout smoke | **CURRENT** direct end-to-end evidence. |
| `DEV/TESTS/test_release_game_passthrough.py` | valid GAME additions become runtime package members | **CURRENT SUPPORTING** package-composition evidence; not a bootstrap authority. |
| `DEV/TESTS/test_destination_template_boundary.py` | internal source paths cannot leak into user-facing storage template | **CURRENT SUPPORTING** destination-template hygiene. |
| `DEV/TESTS/test_game_dev_layout.py` | GAME/DEV separation and retired template-stub absence | **CURRENT SUPPORTING** source/package-layout evidence. |

#### Install/menu/campaign projection verification

| Source | Material expectation(s) | Disposition |
|---|---|---|
| `DEV/TESTS/INSTALL_ONBOARDING_CASES.md` I01-I08 | Project Instructions are guardrails; bootstrap every chat; no implicit resume; numbered explicit menu | **CURRENT**. |
| `DEV/TESTS/CAMPAIGN_CARD_CASES.md` C01-C11 | card creation, card-first menu, nonauthority/access hints | **CURRENT**. |
| same | C12 says both paused and initializing render 🟡 | **STALE / SUPERSEDED** by current `CAMPAIGN_CARD.md`: initializing 🟡, paused ⏸️. |
| same | C13-C25 | completed/archived/card-dirty/numbered-menu/noncanon number semantics | **CURRENT**. |
| `DEV/TESTS/CAMPAIGN_IDENTITY_CASES.md` CI01-CI13 | nullable/evolving title, MANIFEST authority, projection-only README/card | **CURRENT**. |
| `DEV/TESTS/GM_TONE_ONBOARDING_CASES.md` GT01-GT07 | post-scaffold human opening, optional genre/style, no setup jargon, targeted sensitive-theme check | **CURRENT** direct product-facing setup evidence. GT08-GT13 are broader runtime/tone/maintenance concerns and are not activated by WP-19. |
| `DEV/TESTS/REGRESSION_CASES.md` T13 | says new-game discovery reads **manifests only** | **STALE / SUPERSEDED** by current card-first discovery + manifest fallback owner. Other generic T-cases are outside the direct WP-19 creation frame unless separately routed by their native owner. |
| `DEV/TESTS/PRE_RELEASE_AUDIT_0.1.0.md` | old pre-release bootstrap/skeleton observations | **HISTORICAL ONLY**; file explicitly declares itself non-normative historical snapshot. |

#### Readiness/onboarding/durability verification

| Source | Material expectation(s) | Disposition |
|---|---|---|
| `DEV/TESTS/CHARACTER_READINESS_CASES.md` C01-C17 | concept != READY_PC; hidden mechanics still complete; locally sufficient provisional play; READY_PC dependency closure; combined PLAY_READY allowed | **CURRENT**. C14/C15 are existing broken/legacy repair cases, not a requirement to preserve unreleased scaffold compatibility. |
| `DEV/TESTS/DIEGETIC_ONBOARDING_CASES.md` DO01-DO14 | PROVISIONAL_IDENTITY, same PC ID promotion, initializing until READY/PLAY_READY, save/stop semantics | **CURRENT**. |
| `DEV/TESTS/DURABILITY_BOUNDARY_CASES.md` D01-D07, D16-D22 | scaffold != play-ready; provisional durability; READY_PC+PLAY_READY; save/stop/lifecycle boundaries | **CURRENT** direct WP-19 evidence. D08-D15 are later-play cadence cases; they remain current under persistence owners but are not activated as creation work. |
| `DEV/TESTS/EXPLICIT_SAVE_CASES.md` S17-S20 plus S05-S07/S13 where creation/resume is material | onboarding save remains initializing; active requires READY_PC+PLAY_READY; no forced checkpoint; projection refresh joins authoritative save | **CURRENT**. Other save mechanics are persistence-owned supporting evidence. |
| `DEV/TESTS/ENGINE_CONSISTENCY_CASES.md` EC07, EC08, EC10, EC14, EC15 | lifecycle, provisional identity, title owner, scaffold smoke, init_campaign-only runtime tool exception | **CURRENT**. |
| `DEV/TESTS/test_s6d_07_character_mvp_seed.py` | READY_PC is dependency closure, provisional locally sufficient play is admitted, unresolved material choices block readiness | **CURRENT SUPPORTING / S6D-OWNED** machine evidence; WP-19 consumes it but does not own the ruleset seed. |
| `DEV/TESTS/test_s6d_11_ruleset_package_closure.py` | exact ruleset-set identity/lock/conformance and mismatch blocking | **CURRENT SUPPORTING / S6D-OWNED** upstream proof; not a campaign-bootstrap owner. |

#### Publication/access/multiplayer verification

| Source | Material expectation(s) | Disposition |
|---|---|---|
| `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md` PT02, PT06-PT10, PT22-PT24, PT30-PT31 | coherent non-force publication/currentness; blank scaffold is from-scratch exception; later base-tree deltas | **CURRENT** direct/supporting evidence. |
| same | PT21 storage metadata and campaign maintenance are separate transactions | **CURRENT WITH QUALIFIER**: storage baseline metadata is storage-owner scope; campaign engine/ruleset adoption remains campaign-creator scope under current `ENGINE_UPDATES.md`/access owners. |
| `DEV/TESTS/RUNTIME_SCOPE_LATENCY_CASES.md` RL01-RL06 | runtime never reads/runs DEV verification as game instructions; RL04 permits only exact `init_campaign.py` for New Game | **CURRENT** and important negative-runtime evidence. |
| `DEV/TESTS/ACCESS_CONTROL_CASES.md` A01-A08 | creator/singleplayer/neutral branch creation authority | **CURRENT** direct evidence. |
| same | A12-A20 | invite-only/open-contributor binding policy | **CURRENT** inherited WP-16/access evidence relevant to initial multiplayer binding. |
| same | A26/A27/A29/A30 | storage-default authority separation | **CURRENT WITH QUALIFIER**: only storage initialization/baseline metadata belongs there; wording implying copied-engine or campaign-engine maintenance on storage main is not current authority. |
| same | A28 says guest skips release discovery and uses “campaign-integrated engine” | **SUPERSEDED IN PART / CURRENT WITH QUALIFIER**: guest cannot persist storage baseline or creator-only campaign adoption, but exact local package discovery/use and compatible same-version behavior follow current `ENGINE_UPDATES.md`; campaign storage contains no integrated engine copy. |
| `DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md` | leave/remove/rejoin/live deactivation behavior | **OUTSIDE WP-19 / OWNED BY CLOSED WP-16**, except as negative evidence that campaign creation does not absorb later membership lifecycle. |

#### Update/evolution neighbor verification

| Source | Material expectation(s) | Disposition |
|---|---|---|
| `DEV/TESTS/ENGINE_UPDATE_CASES.md` U01-U24 | update/migration scenarios | **OWNED DOWNSTREAM / WP-20** for future migration semantics, except creation-adjacent package provenance. U04/U08/U10 contain older wording (`Always update automatically`, `baseline_version`, tag-resolution style) and must not be imported into WP-19 as current creation authority. |
| `DEV/TESTS/test_engine_mismatch_recovery_contract.py` | existing-campaign missing-package recovery | **OUTSIDE WP-19 / ENGINE_UPDATES-WP20 NEIGHBOR**, current executable evidence for its owner. |
| `DEV/TESTS/test_engine_update_policy_contract.py` | storage baseline and campaign engine authority independent; same-version/creator policy | **CURRENT SUPPORTING BOUNDARY EVIDENCE**, substantive migration remains WP-20. |

### 2.9 Reverse-conformance conclusion

The verification graph is presently mixed:

```text
current owners + current executable tests
    coexist with
stale scenario expectations in several DEV/TESTS/*_CASES.md files
```

This means prior hosted CI success does not establish that every human-readable regression expectation is current. Step 2, if Senior-authorized, must use the dispositions above rather than treating scenario catalogs as an answer key.

No test/scenario files were rewritten during SR19-01 recovery. Their synchronization is not mechanically required to complete Step-1 framing; changing them now would cross from evidence recovery into design realization/implementation-adjacent work without Step-2 authorization. The recovered manifest instead makes the stale expectations explicit and routes them to current owners for later authorized reconciliation.

---

## 3. Material evidence ledger

### SM19-01 — explicit campaign selection precedes campaign-specific work

**Claim:** explicit existing-campaign/New Game choice precedes campaign-specific state/runtime resolution.

**Owners:** `00_DND_BOOTSTRAP.md`, `BOOTSTRAP_RUNTIME.md`, `CAMPAIGN_CARD.md`.

**Disposition:** CURRENT; not an open product decision.

### SM19-02 — new campaign runtime comes from storage baseline

**Claim:** New Game resolves current storage v3 `DND_STORAGE.engine.baseline` to one validated local runtime package/current runtime root.

**Disposition:** CURRENT. Storage baseline is new-campaign default only.

### SM19-03 — branch ancestry and first campaign-specific tree are distinct

**Claim:** neutral campaign branch starts from storage default HEAD for ancestry; first campaign-specific commit replaces inherited storage-root bytes with generated campaign root tree.

**Disposition:** CURRENT. Storage marker/README never become campaign canon.

### SM19-04 — campaign creator comes from first campaign-specific publication provenance

**Disposition:** CURRENT. Card creator login is hint only.

### SM19-05 — exact materializer input includes resolved ruleset identity

**Claim:** `init_campaign.py` requires `--ruleset-set-sha256` and materializes MANIFEST ruleset created/current identity from selected runtime package provenance.

**Disposition:** CURRENT / mechanically settled.

### SM19-06 — bootstrap prose is incomplete against materializer contract

**Claim:** current bootstrap/setup prose omits required `--ruleset-set-sha256`; machine/package/test chain proves the required input.

**Disposition:** ORIGINAL F19-S1-01 remains CLOSED as a framing finding; later authorized WP-19 work must reconcile the current consumers. No new Product Owner decision.

### SM19-07 — storage/branch prose contains stale v2 projections

**Disposition:** CURRENT CONSISTENCY OBLIGATION; exact current storage owner is v3. No compatibility preservation required for unreleased scaffold.

### SM19-08 — scaffold creation is not PLAY_READY

**Disposition:** CURRENT lifecycle invariant.

### SM19-09 — provisional onboarding is separate from mechanical readiness

**Disposition:** CURRENT lifecycle/durability invariant.

### SM19-10 — READY_PC and PLAY_READY are distinct gates

**Disposition:** CURRENT; `active` requires both.

### SM19-11 — projections never become authority

**Disposition:** CURRENT.

### SM19-12 — initial publication and later setup publication use different transaction shapes

**Disposition:** CURRENT.

### SM19-13 — initial multiplayer choices remain creator/access controlled

**Disposition:** INHERITED / CURRENT; no WP-16 reopen.

### SM19-14 — House Rules baseline is inherited, not newly activated architecture

**Disposition:** INHERITED / ALREADY SATISFIED unless a concrete contradiction is later found.

### SM19-15 — campaign naming/config defaults are low-friction and may remain partially undefined

**Disposition:** CURRENT product-facing constraint.

### SM19-16 — future released-campaign compatibility is downstream

**Disposition:** DEFERRED TO WP-20 by explicit owner/sequencing rule; current unreleased scaffold has no compatibility obligation.

### SM19-17 — verification/test evidence is a consumer graph, not an authority shortcut

**Claim:** WP-19 reverse-conformance coverage must independently reconcile both executable tests and human-readable scenario catalogs against current owners. A passing executable suite cannot silently bless stale scenario text; conversely a stale scenario must not override a current schema/runtime/canonical owner.

**Recovered evidence:**

- current executable v3 evidence: `test_multi_runtime_release_consistency.py`, `test_runtime_identity_schema.py`;
- current package/ruleset path: `test_release_builder.py`, `test_release_integration.py`, `test_s6d_11_ruleset_package_closure.py`;
- current readiness path: `test_s6d_07_character_mvp_seed.py`, readiness/onboarding/durability case families;
- explicit stale scenario items: B12, B22, B23, Campaign Card C12, generic Regression T13;
- qualified access/update neighbors routed to their current owners rather than activated into WP-19.

**Disposition:** SR19-01 CLOSED by evidence expansion and item-level routing. No test rewrite is required for Step-1 closure; later authorized design-realization must not use a stale expectation as implementation truth.

---

## 4. Negative findings / non-activation boundaries

The recovery found no present requirement to:

- run a real campaign or gameplay bootstrap;
- create campaign/storage branches as part of this architecture audit;
- rewrite regression/test catalogs during Step 1 merely because stale entries were discovered;
- make historical scenario catalogs normative;
- treat CI success as proof that every scenario expectation is current;
- design WP-20 migration/evolution policy now;
- reopen closed multiplayer/access, READY_PC, House-Rules, Story/Dramaturg or persistence architecture merely because bootstrap consumes it;
- preserve stale v2 scaffold fields for backward compatibility;
- prebuild broad world/Story/planning material before first play;
- turn card/README/session/checkpoint/test fixture into a new canonical owner;
- begin implementation planning or substantive runtime/schema/template/test implementation.

Coverage does not activate downstream work.

---

## 5. Product Owner boundary re-check after SR19-01

| Watch area | Recovery disposition |
|---|---|
| Product semantics | Stale B23/C12/T13 expectations conflict with already-current human-opening/card/menu owners; no new semantic alternative remains undecided. |
| Canonical authority / ownership | Storage v3, package provenance, creator, PLAYER/PC/readiness and projections already have current owners. Stale tests cannot create authority. |
| Meaningful compatibility policy | Current unreleased scaffold remains clean-slate under owner clarification. Future released-campaign evolution remains WP-20. |
| Hard-to-reverse lifecycle/product behavior | Readiness/onboarding/durability tests confirm existing scaffold/provisional/READY_PC/PLAY_READY separation; no new lifecycle decision. |
| Material quality trade-off | Low-friction invisible setup and card-first menu are already accepted. Recovery found stale expectations, not an unresolved strategy trade-off. |
| Explicit risk acceptance | No new material risk requiring human acceptance. |

```text
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
```

---

## 6. Completeness gate after Senior recovery

```text
[x] Current process/status/owners re-read on Senior-recovery basis.
[x] DEV/PROJECT_MAP used to reconstruct the verification route independently.
[x] DEV/TESTS directory inspected beyond the Senior minimum file list.
[x] Direct bootstrap/storage/package/menu/readiness/durability/access/publication scenario families inspected.
[x] Direct producer/integration/identity/readiness/ruleset executable tests inspected.
[x] Update/evolution test families explicitly routed to WP-20 where downstream.
[x] Historical pre-release audit classified HISTORICAL ONLY.
[x] Stale expectations are itemized rather than hidden under file-level labels.
[x] Current-with-qualifier expectations preserve their applicable semantics.
[x] Scenario/test evidence is subordinate to current owning architecture/runtime/schema contracts when superseded.
[x] Original two BLOCKING findings remain confirmed/closed; no unsupported reopen introduced.
[x] SR19-01 verification-evidence defect is CLOSED by expansion/routing.
[x] Product Owner boundary rechecked: no human-owned decision found.
[x] Step 2, WP-20 and implementation planning remain unstarted/unauthorized.
```

The Source Manifest is now sufficient for the **recovered Step-1 framing claim** and is ready for mandatory Senior re-review. It is not Step-2 research/canonicalization and does not claim that stale test/scenario files have already been synchronized.
