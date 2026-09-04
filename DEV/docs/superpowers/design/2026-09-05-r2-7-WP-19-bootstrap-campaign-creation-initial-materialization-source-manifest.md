# R2.7 WP-19 — Bootstrap / Campaign Creation / Initial Materialization — Source Manifest

Status: **STEP 1 SOURCE MANIFEST — REVIEW-READY FRAMING EVIDENCE**

Date: 2026-09-05

Verified execution basis: `5fc24905be5c9e1b47929ee9e7b49ea8b9f2a053`

Domain:

> **Bootstrap / campaign creation / initial materialization**

This manifest is the task-specific discovery/evidence route required by `DEV/DESIGN_PROCESS.md` and `DEV/ARCHITECTURE/DESIGN_PROCESS.md`. It is intentionally broader than the initial WP-19 scope inventory. The inventory, roadmap, project map and canonical index are routing aids; correctness-sensitive framing below is based on actual current owners, runtime consumers, schemas, templates, tools and tests inspected on the verified public basis.

This artifact does not authorize Step 2, WP-20, implementation planning, gameplay bootstrap or substantive runtime/schema/template implementation.

Companion Step-1 artifacts:

- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief-critic.md`.

---

## 1. Discovery route

The independent dependency route used for WP-19 is:

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
    -> release/package/test consumers
    -> WP-20 future compatibility boundary
```

This route was reconstructed from current `DEV/PROJECT_MAP.md` and then expanded through actual references/consumers. It was not copied from the WP-19 scope inventory.

---

## 2. Source-role manifest

### 2.1 Process, current state and R2.7 scope

| Source | Role | Required WP-19 scope / current disposition |
|---|---|---|
| `AGENTS.md` | CANONICAL repository process | Runtime overlay, taxonomy, source/evidence discipline, publication/checkpoint rules. Inspected. |
| `DEV/DESIGN_PROCESS.md` | CANONICAL development process | Step-1 brief, Source Manifest, evidence completeness, human/agent decision rights. Inspected. |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | CANONICAL HDM process adapter | Mandatory whole-project Step-1 critic and mandatory Senior stop. Inspected. |
| `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` | CANONICAL implementation process | Boundary evidence only: implementation is downstream and unauthorized here. Inspected to establish the non-goal. |
| `DEV/CURRENT_PROGRESS.md` | CANONICAL global progress authority | WP-19 Step 1 is the sole authorized unit; Step 2 blocked pending Senior GO. Inspected. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md` | TASK-LOCAL cursor | WP-19 Step-1 activation/stop boundary. Inspected. |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | DERIVATIVE sequencing/scope owner | R2.7 sequencing and implementation-planning boundary only. Inspected. |
| `DEV/PROJECT_MAP.md` | DERIVATIVE routing index | Used to reconstruct campaign-creation, storage, access, persistence, ruleset and verification routes. Inspected. |
| `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | DERIVATIVE architecture locator | Used only for accepted-owner discovery and invariant routing; never treated as semantic authority. Inspected. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md` | R2.7 owning program brief | Whole-project bidirectional audit context and WP decomposition. Inspected. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md` | DESIGN PROVENANCE / initial inventory | WP-19 minimum inventory only; not an answer key. Inspected and expanded. |
| `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md` | CANONICAL OWNER DECISION | No existing real campaigns require compatibility with the unreleased scaffold; R2.7 structural canonicalization is authorized; WP-20 owns future released-campaign evolution. Inspected. |

### 2.2 Runtime bootstrap and campaign-creation owners

| Source | Role | Required WP-19 scope / current disposition |
|---|---|---|
| `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` | RUNTIME ENTRY CONSUMER | Entry/routing into bootstrap; capability boundary. Inspected. |
| `GAME/INSTALL/00_DND_BOOTSTRAP.md` | RUNTIME INSTALL/BOOTSTRAP OWNER | Package validation, storage discovery, explicit campaign choice, New Game flow, branch/materializer/publication route. Inspected. |
| `GAME/CORE/BOOTSTRAP_RUNTIME.md` | RUNTIME BOOTSTRAP OWNER | Exact runtime selection, storage v3, explicit campaign-choice barrier, current runtime binding. Inspected. |
| `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` | RUNTIME NEW-CAMPAIGN ORDERING OWNER | Scaffold-first ordering, exact generator, from-scratch campaign tree, first publication, low-latency transition into setup. Inspected. |
| `GAME/CORE/CAMPAIGN_SETUP.md` | RUNTIME SETUP OWNER | Branch initialization, exact package/materializer inputs, low-friction setup, provisional/READY/PLAY_READY flow and first-scene handoff. Inspected. |
| `GAME/TOOLS/init_campaign.py` | IMPLEMENTATION / MACHINE MATERIALIZER | Exact authoritative scaffold materializer and required input contract. Inspected. |

### 2.3 Storage, branch, creator and publication authority

| Source | Role | Required WP-19 scope / current disposition |
|---|---|---|
| `GAME/CORE/STORAGE.md` | RUNTIME STORAGE OWNER | Storage v3 portable baseline, root-layout campaign ownership, creator/write authority routing. Inspected. |
| `GAME/SCHEMA/dnd_storage.schema.yaml` | MACHINE CONTRACT | Storage v3 exact baseline fields and owner-only metadata invariants. Inspected. |
| `DEV/ARCHITECTURE/BRANCH_MODEL.md` | ACCEPTED ARCHITECTURE OWNER WITH CURRENT STALE PROJECTIONS | Branch ancestry/root-layout/creator laws are relevant; storage-v2/`baseline_version` and old engine-provenance wording conflict with current v3 owners and must be reconciled during WP-19. Inspected; staleness is evidence, not authority to preserve it. |
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | ACCEPTED ACCESS OWNER | Campaign creator from first campaign-specific initialization commit; singleplayer creator-only; multiplayer active PLAYER authority. Inspected. Its isolated storage-v2 wording is a stale projection to reconcile, not a new compatibility requirement. |
| `GAME/CORE/PERSISTENCE.md` | RUNTIME PUBLICATION TRANSPORT OWNER | Initial blank scaffold is the exceptional from-scratch campaign tree; later campaign publications use pinned-base campaign transactions. Inspected. |
| `GAME/CORE/RUNTIME.md` | RUNTIME INVARIANT OWNER | Repository/ref write routing and campaign lifecycle constraints. Inspected. |

### 2.4 Exact runtime/ruleset identity and package machine closure

| Source | Role | Required WP-19 scope / current disposition |
|---|---|---|
| `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` | CANONICAL S6D OWNER | `ruleset_set_sha256` is exact resolved-set identity; runtime package advertises it; campaign MANIFEST owns sibling `ruleset.created_with/current`. Inspected. |
| `DEV/ARCHITECTURE/RULESET_PACKAGE_MACHINE_CLOSURE.md` | CANONICAL MACHINE-CLOSURE OWNER | Exact resolved lock/set and conformance evidence are runtime-package provenance. Inspected. |
| `GAME/CORE/ENGINE_UPDATES.md` | RUNTIME UPDATE/IDENTITY OWNER | Creation-side distinction between storage baseline and campaign current runtime/ruleset; incompatible future migration remains WP-20. Inspected only to WP-19 boundary. |
| `DEV/TOOLS/release_builder.py` | IMPLEMENTATION / PACKAGE PRODUCER | `RUNTIME_PACKAGE.yaml` schema includes exact `ruleset_set_sha256`, resolved lock and conformance evidence. Inspected. |
| `DEV/TESTS/test_release_integration.py` | EXECUTABLE INTEGRATION EVIDENCE | Release-built runtime invokes `init_campaign.py` with package `ruleset_set_sha256`; validates generated root-layout manifest. Inspected. |

### 2.5 Campaign template, schemas and projections

| Source | Role | Required WP-19 scope / current disposition |
|---|---|---|
| `GAME/CAMPAIGN/` current tree | MACHINE TEMPLATE FAMILY | Actual generated root topology, including `MANIFEST.yaml`, `CAMPAIGN_CARD.yaml`, `CONFIG.yaml`, `STATE/`, `WORLD/`, `INDEX/`, `LOG/`, `CHECKPOINTS/`, `RULES/`, `SESSIONS/`. Inspected structurally rather than inferred from prose. |
| `GAME/CAMPAIGN/MANIFEST.yaml` | TEMPLATE / MACHINE INPUT | Schema-v3 seed; technical identity nulls before materialization; ruleset sibling fields; lifecycle seed. Inspected. |
| `GAME/SCHEMA/campaign_manifest.schema.yaml` | MACHINE CONTRACT | Root-layout identity, engine/ruleset provenance, lifecycle and branch invariants. Inspected. |
| `GAME/CAMPAIGN/CAMPAIGN_CARD.yaml` | TEMPLATE PROJECTION | Initial menu projection shape. Inspected. |
| `GAME/SCHEMA/campaign_card.schema.yaml` | MACHINE CONTRACT | Card is projection only; `active` requires READY_PC + PLAY_READY; same-transaction refresh. Inspected. |
| `GAME/CORE/CAMPAIGN_CARD.md` | RUNTIME PROJECTION OWNER | Card menu/projection/authority boundary and status semantics. Inspected. |
| `GAME/CORE/CAMPAIGN_IDENTITY.md` | RUNTIME CAMPAIGN-NAME OWNER | MANIFEST owns campaign name; card/README are projections; title may remain null. Inspected. |
| `GAME/CAMPAIGN/CONFIG.yaml` | TEMPLATE / CAMPAIGN CONFIG | Optional premise/world/tone/boundaries/play-style seed. Inspected. |
| `GAME/CAMPAIGN/STATE/CURRENT.yaml` | TEMPLATE / ROUTING STATE | Empty compact current-state seed. Inspected. |
| `GAME/SCHEMA/current_state.schema.yaml` | MACHINE CONTRACT | Compact current routing, no generic pending bucket. Inspected. |

### 2.6 Character/readiness/first-play and resumability owners

| Source | Role | Required WP-19 scope / current disposition |
|---|---|---|
| `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md` | CANONICAL READY_PC OWNER | Exact reconstructable legal initial mechanics and ruleset-bound readiness evidence. Inspected. |
| `GAME/CORE/CHARACTER_READINESS.md` | RUNTIME READINESS OWNER | READY_PC semantics and prohibition on LLM draft directly becoming mechanical authority. Inspected. |
| `GAME/CORE/DIEGETIC_ONBOARDING.md` | RUNTIME PRE-READY ONBOARDING OWNER | Provisional pre-READY play is allowed with noncanonical/unresolved boundaries; does not imply mechanics-capable live readiness. Inspected. |
| `GAME/CORE/DURABILITY_GUARD.md` | RUNTIME DURABILITY/LIFECYCLE OWNER | `PROVISIONAL_IDENTITY`, READY_PC and PLAY_READY durability boundaries; active lifecycle only after READY_PC + PLAY_READY. Inspected. |
| `GAME/CORE/SESSION.md` | RUNTIME SESSION/RESUME OWNER | Initializing setup remains initializing when stopped; session/recovery routing. Inspected. |
| `GAME/SCHEMA/session.schema.yaml` | MACHINE CONTRACT | Session coordination/recovery record shape. Inspected. |
| `GAME/SCHEMA/player.schema.yaml` | MACHINE CONTRACT | Stable PLAYER binding, authorization identity, preferences. Inspected. |
| `GAME/SCHEMA/pc.schema.yaml` | MACHINE CONTRACT / PARTLY LEGACY PROJECTION | Provisional/active PC status and READY_PC requirement. Qualifier preserved: several flattened mechanics/knowledge/relationship surfaces are explicitly non-authoritative pending accepted owner migration and must not be promoted by WP-19. Inspected. |

### 2.7 Multiplayer and House-Rules neighbors

| Source | Role | Required WP-19 scope / current disposition |
|---|---|---|
| `GAME/CORE/MULTIPLAYER.md` | RUNTIME MULTIPLAYER OWNER | Creator-explicit mode, `invite_only` default, active PLAYER authority, initial membership constraints. Inspected. |
| `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` | CANONICAL HOUSE-RULES OWNER | Empty/default campaign House-Rules materialization is inherited current architecture; policy semantics are closed and must not be reopened merely because template files are copied. Inspected. |
| `GAME/CAMPAIGN/RULES/HOUSE_RULES.md` + `HOUSE_RULES.yaml` | TEMPLATE / MACHINE PROJECTION | Existing baseline policy surfaces copied into scaffold. Inspected structurally. |

---

## 3. Material evidence ledger

The following item-level claims are the minimum evidence set that Step 2 must preserve. Coverage does not activate every neighboring subsystem.

### SM19-01 — explicit campaign selection precedes campaign-specific work

**Actual claim:** a new chat may not implicitly resume the sole/most recent campaign; an explicit campaign/New Game choice is required before campaign-specific state/runtime resolution.

**Owners/evidence:** `00_DND_BOOTSTRAP.md`, `BOOTSTRAP_RUNTIME.md`, `CAMPAIGN_CARD.md`.

**Qualifiers:** an already unambiguous current-chat request counts as the choice. This is both player-agency and latency policy.

**Disposition:** ACTIVE WP-19 invariant; not an open product decision.

### SM19-02 — new campaign runtime comes from storage baseline, not ambient package choice

**Actual claim:** New Game resolves `DND_STORAGE.engine.baseline` to one validated local runtime package and binds one exact `current_runtime_root`.

**Owners/evidence:** `STORAGE.md`, `dnd_storage.schema.yaml`, `BOOTSTRAP_RUNTIME.md`, `CAMPAIGN_SETUP.md`.

**Qualifiers:** baseline applies to NEW campaigns only and does not mutate existing campaigns; development-package authorization has its own repository-owner gate.

**Disposition:** ACTIVE creation invariant.

### SM19-03 — branch ancestry and first campaign-specific commit are distinct from campaign tree contents

**Actual claim:** `campaign/YYYYMMDD[-NN]` is created from storage default-branch HEAD for ancestry; the first campaign-specific commit replaces inherited storage-root contents with a generated root-layout campaign tree.

**Owners/evidence:** `BRANCH_MODEL.md`, `NEW_CAMPAIGN_FAST_PATH.md`, `CAMPAIGN_SETUP.md`, `PERSISTENCE.md`.

**Qualifiers:** storage `README.md` / `DND_STORAGE.yaml` must not leak into campaign canon; no force-push.

**Disposition:** ACTIVE; stale BRANCH_MODEL metadata elsewhere does not invalidate this branch law.

### SM19-04 — campaign creator authority derives from publication provenance

**Actual claim:** campaign creator is the `author.login` of the first campaign-specific initialization commit.

**Owners/evidence:** `ACCESS_CONTROL.md`, `BRANCH_MODEL.md`, `CAMPAIGN_SETUP.md`, `STORAGE.md`.

**Qualifiers:** card creator login is only a display/access hint; repository permission is not gameplay authority.

**Disposition:** ACTIVE authority invariant.

### SM19-05 — exact materializer input includes resolved ruleset identity

**Actual claim:** current `GAME/TOOLS/init_campaign.py` requires `--ruleset-set-sha256`, validates it, and writes it to `MANIFEST.ruleset.created_with/current`.

**Owners/evidence:** `init_campaign.py`, `RULESET_PACKAGE_IDENTITY.md`, `RULESET_PACKAGE_MACHINE_CLOSURE.md`.

**Qualifiers:** the exact source is selected runtime `RUNTIME_PACKAGE.ruleset_set_sha256`, not model inference or a human-facing rules baseline string.

**Disposition:** ACTIVE and mechanically settled.

### SM19-06 — current bootstrap prose is incomplete against the materializer contract

**Actual claim:** current `00_DND_BOOTSTRAP.md`, `BOOTSTRAP_RUNTIME.md` and `CAMPAIGN_SETUP.md` materializer argument lists omit required `--ruleset-set-sha256`, while the generator requires it and `test_release_integration.py` passes `RUNTIME_PACKAGE.ruleset_set_sha256`.

**Authority classification:** MACHINE/RUNTIME CONSUMER CONTRADICTION, not a new architecture choice.

**Qualifiers:** Step 1 records the defect and repairs framing only. Runtime/doc synchronization itself belongs to later WP-19 Steps after Senior GO under the design process.

**Disposition:** ACTIVE Step-2 audit obligation; no Product Owner decision required.

### SM19-07 — storage/branch prose contains stale v2 identity projections

**Actual claim:** `BRANCH_MODEL.md` still describes storage v2 / `baseline_version` and an older campaign engine identity, while current `STORAGE.md`, `dnd_storage.schema.yaml`, bootstrap owners and manifest schema use storage v3 portable package identity plus sibling engine/ruleset campaign identity.

**Owner classification:** accepted branch topology plus stale current projections that need reconciliation against later/current owners.

**Qualifiers:** R2.7 owner clarification states no real campaigns require backward compatibility with the unreleased scaffold and authorizes direct structural canonicalization. Future released-campaign evolution remains WP-20.

**Disposition:** ACTIVE WP-19 consistency obligation; no compatibility-policy decision remains at Step 1.

### SM19-08 — scaffold creation is not PLAY_READY

**Actual claim:** successful blank-scaffold publication establishes technical campaign identity/creator while lifecycle remains `initializing`.

**Owners/evidence:** `NEW_CAMPAIGN_FAST_PATH.md`, `CAMPAIGN_SETUP.md`, manifest/card schemas.

**Disposition:** ACTIVE lifecycle invariant.

### SM19-09 — provisional onboarding is a separate state from mechanical readiness

**Actual claim:** a stable protagonist/Actor may cross `PROVISIONAL_IDENTITY` and become durably resumable while the PC remains provisional and campaign remains `initializing`.

**Owners/evidence:** `DIEGETIC_ONBOARDING.md`, `DURABILITY_GUARD.md`, `CHARACTER_READINESS.md`.

**Qualifiers:** unresolved mechanically material choices cannot be retrofitted after use; provisional onboarding is not a true post-PLAY_READY live scene.

**Disposition:** ACTIVE; already accepted product semantics.

### SM19-10 — READY_PC and PLAY_READY are distinct gates

**Actual claim:** READY_PC is the reconstructable initial mechanical commitment frontier; `active` lifecycle requires READY_PC plus a durable PLAY_READY frontier. First true mechanics-capable live scene starts only after this gate.

**Owners/evidence:** canonical READY_PC owner, `CHARACTER_READINESS.md`, `DURABILITY_GUARD.md`, `RUNTIME.md`, manifest/card schemas.

**Disposition:** ACTIVE; not an open lifecycle decision.

### SM19-11 — projections never become authority

**Actual claim:** `CAMPAIGN_CARD.yaml` and campaign README are menu/human projections. MANIFEST and native PC/PLAYER/STATE/WORLD/Git provenance remain authoritative.

**Owners/evidence:** `CAMPAIGN_CARD.md`, `CAMPAIGN_IDENTITY.md`, card schema.

**Qualifiers:** projection changes join the same coherent persistence transaction; card freshness alone is not a save boundary.

**Disposition:** ACTIVE.

### SM19-12 — first publication and later setup publication use different transaction shapes

**Actual claim:** initial blank scaffold is one from-scratch Git tree/commit/ref update; later setup/PLAY_READY changes use normal campaign transactions from pinned campaign HEAD.

**Owners/evidence:** `NEW_CAMPAIGN_FAST_PATH.md`, `CAMPAIGN_SETUP.md`, `PERSISTENCE.md`, `DURABILITY_GUARD.md`.

**Disposition:** ACTIVE resumability/currentness invariant.

### SM19-13 — initial multiplayer choices remain creator/access controlled

**Actual claim:** campaign mode is creator-explicit; multiplayer default join policy is `invite_only`; normal multiplayer writes require current active PLAYER binding.

**Owners/evidence:** `MULTIPLAYER.md`, `ACCESS_CONTROL.md`, `player.schema.yaml`, manifest/card schemas.

**Qualifiers:** closed WP-16 authority must not be reopened absent contradiction/new unsatisfied consumer/material insufficiency.

**Disposition:** INHERITED / ACTIVE CONSTRAINT; no reopen identified.

### SM19-14 — House Rules baseline is inherited, not newly activated architecture

**Actual claim:** scaffold includes current House-Rules policy surfaces, but copying them does not reopen House-Rules semantics or create a new policy authority.

**Owners/evidence:** `CAMPAIGN_HOUSE_RULES.md`, campaign template RULES files.

**Disposition:** INHERITED / ALREADY SATISFIED. Preserve exact default/materialization semantics; do not expand WP-19 into policy redesign.

### SM19-15 — campaign naming/config defaults are low-friction and may remain partially undefined

**Actual claim:** campaign title may remain null; genre/tone/lore/mechanics presentation may use accepted defaults/inference where no material player decision is blocked.

**Owners/evidence:** `CAMPAIGN_IDENTITY.md`, `CAMPAIGN_SETUP.md`, `CONFIG.yaml`, PLAYER preferences.

**Disposition:** ACTIVE product-facing constraint already decided.

### SM19-16 — future released-campaign compatibility is downstream

**Actual claim:** WP-19 must produce a clean creation/materialization contract; future incompatible schema/ruleset/engine migration policy is WP-20.

**Owners/evidence:** R2.7 owner clarification, `RULESET_PACKAGE_IDENTITY.md`, `ENGINE_UPDATES.md`, R2.7 sequencing.

**Qualifiers:** current unreleased scaffold has no backward-compatibility obligation.

**Disposition:** DEFERRED TO WP-20 by explicit owner/sequencing rule; trigger is WP-20 activation. It is not current WP-19 design work.

---

## 4. Negative findings / non-activation boundaries

The evidence pass did **not** establish any present requirement to:

- run a real campaign or validate gameplay content during Step 1;
- create a new campaign branch in this repository;
- design WP-20 migration/evolution policy now;
- reopen closed multiplayer/access, READY_PC, House-Rules, Story/Dramaturg or persistence architecture merely because bootstrap consumes it;
- preserve stale v2 scaffold fields for backward compatibility;
- prebuild broad world, NPC, faction or Story/planning material before first play;
- turn card/README/session/checkpoint into a new canonical owner;
- introduce a second runtime/ruleset selection authority;
- begin implementation planning or substantive runtime/schema/template implementation.

These negative findings are part of the WP-19 boundary and must survive Step-2 synthesis.

---

## 5. Product Owner boundary check

Step-1 evidence was explicitly tested for residual human-owned decisions.

| Watch area | Evidence disposition |
|---|---|
| Product semantics | Explicit campaign choice, low-friction setup, provisional onboarding, READY_PC/PLAY_READY and first-live-scene semantics already have accepted owners. No unresolved semantic alternative identified. |
| Canonical authority / ownership | Storage baseline, campaign MANIFEST, ruleset identity, creator Git provenance, PLAYER/PC/native state and projection boundaries are already allocated. Stale prose is a reconciliation defect, not an open authority decision. |
| Meaningful compatibility policy | Current unreleased scaffold has no compatibility requirement by owner decision. Future released-campaign evolution is WP-20. |
| Hard-to-reverse lifecycle/product behavior | `initializing -> active` requires READY_PC + PLAY_READY; provisional onboarding and pause semantics are already explicit. No unresolved lifecycle choice identified. |
| Material quality trade-off | Low-friction setup, explicit selection, bounded I/O and coherent publication are accepted current constraints. Step 1 found implementation/document consistency work, not a new quality trade-off. |
| Explicit risk acceptance | No new material risk requiring owner acceptance was identified in framing. |

```text
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
```

This does not waive the mandatory Senior Step-1 review. It means that review is currently a framing/evidence gate, not a Product Owner choice gate.

---

## 6. Completeness gate

Step-1 Source Manifest checks:

```text
[x] Current progress and R2.7 owning program sources inspected.
[x] DEV/PROJECT_MAP used to reconstruct the task-specific dependency subgraph.
[x] Actual bootstrap/setup/storage/access/ruleset/readiness/persistence owners inspected.
[x] Current schemas/templates/materializer and executable integration consumer inspected.
[x] Material qualifiers, negative findings and WP-20 defer boundary preserved.
[x] Scope inventory treated as a minimum/routing aid rather than an answer key.
[x] Machine -> architecture and architecture -> machine directions represented.
[x] Known current contradictions are recorded without prematurely selecting new architecture.
[x] Closed upstream architecture was not reopened by thematic overlap.
[x] No correctness-sensitive framing conclusion depends only on roadmap/index/history snippets.
[x] Product Owner watch completed; no residual human-owned decision identified.
```

The evidence set is sufficient for the **Step-1 framing claim**. It is not a Step-2 research result and does not claim that WP-19 architecture has been audited/canonicalized yet.
