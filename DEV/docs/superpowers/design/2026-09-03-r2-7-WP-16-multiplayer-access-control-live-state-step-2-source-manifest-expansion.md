# R2.7 WP-16 — Multiplayer / Access Control / Live State — Step-2 Source Manifest Expansion

Status: **STEP 2 — OPEN-WORLD SOURCE MANIFEST EXPANDED / INSPECTED**

Date: 2026-09-03

Companion Step-1 manifest:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-source-manifest.md`

Companion Step-2 evidence extraction:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-step-2-evidence-extraction.md`

This artifact extends, rather than closes, the Step-1 Source Manifest. Discovery remains open-world through Steps 3–8: any actual owner, consumer, schema, test, recovery/publication route or superseding decision reached while challenging the candidate must be added before a coverage claim relies on it.

---

## 1. Step-2 discovery result

The Step-1 graph was traversed through current `DEV/PROJECT_MAP.md`, direct owner references, machine schemas, runtime consumers and regression suites. Senior findings `SR16-01` and `SR16-02` were fully consumed.

No Step-2 evidence requires a new authority owner, a generic multiplayer coordinator, a scene/global LIVE mega-owner, a distributed transaction or a login-based substitute for stable external identity.

Current supported-host capability evidence is sufficient to continue: the connected GitHub Connector exposed the current authenticated principal with a stable numeric GitHub user identifier while exposing mutable login separately. No exact user identifier is architecture data and none is retained here.

---

## 2. Supported-host / authenticated-principal route — SR16-01

| Source/evidence | Role | Step-2 disposition |
|---|---|---|
| current connected GitHub Connector identity capability | CURRENT HOST CAPABILITY EVIDENCE | Supported session exposed current authenticated principal plus stable numeric GitHub user ID; mutable login was separately available. Capability gate PASS. |
| `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md` | CANONICAL / OWNING | Supported profile uses connected GitHub Connector; missing required capability is typed capability failure, not alternate-transport authorization. |
| `DEV/docs/superpowers/design/2026-08-24-r2-6-fixed-repository-transport-owner-clarification.md` | OWNER CLARIFICATION | Fixed supported path remains deterministic core -> Connector -> non-force authoritative ref transition. |
| `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` | SHIPPED RUNTIME CONTRACT | Connector is supported campaign-storage transport; no shell Git/CLI/direct private HTTP fallback. |
| `GAME/INSTALL/00_DND_BOOTSTRAP.md` | SHIPPED RUNTIME CONSUMER | Bootstrap may discover identity/repository metadata, but login text must not be promoted into stable PLAYER identity. |
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | CANONICAL ACCESS OWNER | Multiplayer gameplay binding is current authenticated stable GitHub user ID -> exactly one current active `PLAYER_`; repository permission/login alone do not grant gameplay authority. |
| `GAME/SCHEMA/player.schema.yaml` | MACHINE CONTRACT | `github_binding.user_id` is stable external authorization binding; `github_binding.login` is mutable label; `player_id` is canonical campaign actor identity. |
| `DEV/TESTS/ACCESS_CONTROL_CASES.md` | TEST EVIDENCE | A09/A20/A25 and related cases reinforce stable-ID binding and fail-closed infrastructure-vs-application authorization. |

Mandatory chain established for later candidate law:

```text
SUPPORTED CHATGPT HOST
    -> connected GitHub Connector
    -> trusted current authenticated principal evidence
    -> stable external GitHub user ID
    -> current world.player / PLAYER binding by github_binding.user_id
    -> current membership status
    -> current controlled_pc_ids relation where PC control is required
    -> operation-specific authorization
    -> current native WriteAuthorityLookup / route
    -> exact current campaign or selected LIVE source basis
    -> authorized non-force publication / exact-source CAS
```

Negative law carried forward:

```text
mutable login != stable user_id
repository permission != gameplay authority
successful CAS != application authorization
cached/session/menu identity != current authorization
```

The existing creator-provenance rule that uses initial campaign Git author login remains a separate accepted campaign-owner rule. Step 2 found no evidence that permits treating that login as `github_binding.user_id`; nor did it prove a new unauthorized-grant path requiring upstream reopening. Where creator provenance cannot be established reliably, existing access law remains fail-closed.

---

## 3. Native access / membership / PC-control owners

| Source | Role | Material extraction |
|---|---|---|
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | CANONICAL / OWNING | target-ref guard, campaign creator/PLAYER authority, join/rejoin/deactivation, controlled-PC relation, House-Rule grants, fail-closed verification. |
| `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md` | CANONICAL UPSTREAM | absence is not consent/agency; native procedure/collaboration owner decides waiting/order; join/rejoin must bind PLAYER then controlled PC then current route. |
| `GAME/SCHEMA/player.schema.yaml` | MACHINE CONTRACT | active/inactive status, `deactivated_by`, stable GitHub binding, controlled PCs, preferences/grants. |
| `DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md` | TEST EVIDENCE | membership identity retention, rejoin semantics, stale-chat publication denial; M10 contains stale deactivation ordering requiring later repair. |
| `GAME/CORE/MULTIPLAYER.md` | SHIPPED CONSUMER | current stable-user-ID binding and membership flow; stale live deactivation sequence requires owner-conforming correction. |

Disposition:

- `PLAYER_` remains campaign-stable gameplay principal identity.
- `github_binding.user_id` binds the external authenticated principal to that PLAYER.
- `controlled_pc_ids` is current control relation; joining or absence never assigns a PC by implication.
- deactivation preserves PLAYER/PC/provenance and removes gameplay authorization once the authoritative campaign transition establishes it.
- voluntary PC agency is never inferred from absence, transport timeout, disconnect or membership maintenance.

---

## 4. LIVE ownership / currentness / CAS route

| Source | Role | Material extraction |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md` | CANONICAL / OWNING | routed fixed-claim epoch, typed immutable claims, exact-source CAS, ACTIVE/CLOSED semantics, source-native IDs, freeze/absorption/revocation, multi-LIVE slow path. |
| `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md` | R2.7 UPSTREAM | paths/indexes/branch existence are routing only; source-native identity; PLAYER_INDEX non-authoritative. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md` | R2.7 UPSTREAM | campaign/live/local-HOT currentness distinct; pre-CAS LIVE result prospective; exact-source CAS establishes live mutation; local adoption cannot roll back/replay remote success. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md` | R2.7 UPSTREAM | acting-principal evidence belongs in frozen publication attempt; no auth lease; partial native success is real; no distributed rollback. |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md` | R2.7 UPSTREAM | route-first current native recovery; selected ACTIVE/CLOSED_UNABSORBED live source never falls back to campaign base; session/checkpoint non-authority. |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md` | R2.7 UPSTREAM | accepted execution/RNG/Continuation survives source movement/retry; CAS/ref/freeze/storage order does not become fictional chronology. |
| `GAME/CORE/LIVE_SCENE.md` | SHIPPED CONSUMER / DEBT | useful one-file fast-path evidence but scene-centric owner wording, per-action write assumption and blob/revision fencing wording require owner-conforming disposition. |
| `GAME/SCHEMA/live_scene.schema.yaml` | MACHINE CONTRACT / DEBT | lacks explicit typed immutable claims; participant/PC/touched sets cannot substitute for claims/auth; local revision not exact-source authority. |
| `GAME/SCHEMA/scene.schema.yaml` | MACHINE CONTRACT | live route/epoch pointer and absorption evidence; route metadata does not merge native owners. |
| `DEV/TESTS/LIVE_SCENE_CASES.md` | TEST EVIDENCE / DEBT | most recovery/currentness cases align; L04 is stale against native durability-edge atomicity. |
| `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md` | TEST EVIDENCE | PT19/PT20 preserve distinct LIVE source transition; terminology remains physical transport evidence only. |

Currentness separation carried forward:

```text
campaign currentness
    authoritative campaign ref/revision for campaign-owned scope

LIVE currentness
    current selected epoch/source exact revision for its immutable claims

local HOT currentness
    coherent process-local adopted view/delta over native owners
```

No marker dominates another merely because it is newer numerically or physically later.

---

## 5. LIVE claims / identity / class-boundary expansion

Actual catalog/class traversal reached:

- `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md`;
- `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`.

Disposition:

1. physical LIVE packing never promotes a scene/global live record into semantic mega-owner;
2. an immutable claim is a typed native-owner or owner-defined writable-partition reference only where containment/membership is machine-decidable;
3. claim sets for one epoch are immutable and selected LIVE routes may not overlap;
4. participant lists, `player_character_ids`, touched paths/entities and physical overlays are evidence/projections, not claims by themselves;
5. live-born externally referenced durable identities use the current source-native/epoch-qualified identity contract; a generic `provisional_id` may survive only where the native owner contract explicitly permits non-escaped provisional identity;
6. ID/path/revision/allocation order never establishes authority or fictional chronology.

---

## 6. Information / disclosure boundary reached from LIVE fields

Actual owner traversal reached:

- `GAME/CORE/INFORMATION.md`;
- Step-4 truth/knowledge owner chain already consumed by WP-07/WP-15;
- current live schema/runtime observable/knowledge fields.

Disposition:

- objective live state stays with its native world owner;
- fictional subject knowledge remains `world.knowledge` authority;
- human PLAYER exposure remains `runtime.disclosure` under its owner contract;
- a live observable event may be causal/evidence input but does not become a second global knowledge/disclosure owner;
- `known_by_pc_ids`, participant visibility, file readability or same-scene presence do not by themselves establish both fictional knowledge and human disclosure.

Any final LIVE machine shape must route/normalize those projections through the existing information owners instead of making LIVE a parallel knowledge store.

---

## 7. CAMPAIGN_CARD / MANIFEST / session / cache route — SR16-02

| Surface | Proven role | Forbidden role |
|---|---|---|
| `GAME/CORE/CAMPAIGN_CARD.md` + `GAME/SCHEMA/campaign_card.schema.yaml` + template | menu/display projection and access hint | gameplay authorization, creator/PLAYER identity authority, currentness |
| `creator_github_login` | cached/display creator hint | stable external identity or authorization proof |
| `multiplayer.participant_github_logins` | menu participant hint | PLAYER membership/control authority |
| card `join_policy` / derived lock/join icon | menu hint | current policy authority after selection |
| `GAME/SCHEMA/campaign_manifest.schema.yaml` | campaign configuration/mode/join-policy routing owner where declared | creator identity, PLAYER binding, controlled-PC authority |
| `GAME/CORE/SESSION.md` + `GAME/SCHEMA/session.schema.yaml` | coordination/navigation/currentness observation | write authority, liveness lease, current source selector |
| `CURRENT`, indexes and cached HEAD/live state | bounded routing/working projection according to owner | authorization or semantic owner merely by being loaded/current locally |

After explicit campaign selection/resume, authorization-sensitive operations re-resolve current native sources rather than trusting card/session/index/cache snapshots.

---

## 8. Recovery / cleanup / ref retirement

Actual traversal reached:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`;
- `GAME/CORE/INTEGRITY.md`;
- `DEV/TESTS/INTEGRITY_CASES.md`.

Disposition:

- live ref deletion is post-authority cleanup only;
- deleting a branch never makes it non-authoritative;
- source-native routing/absorption/terminality must already have moved/ended authority;
- stale/missing selected LIVE source is bounded integrity suspicion, never campaign fallback;
- cleanup cannot cancel accepted execution/Continuation/fixed RNG or erase required provenance/idempotency evidence.

---

## 9. Revocation/deactivation realization issue

Current shipped `MULTIPLAYER.md` / test M10 describe roughly:

```text
close E
-> compact
-> separately persist PLAYER deactivation
```

That sequence is insufficient as a normative authorization guarantee because a completed absorption that restores campaign write authority before deactivation becomes current can create a stale authorization/write window.

Owner-conforming Step-2 disposition:

```text
1. exact-source close/freeze affected LIVE source(s)
2. confirm exact final CLOSED source(s)
3. one authoritative campaign transition, when the affected route/membership changes share that campaign boundary, establishes together:
   - final absorption/survivor state
   - PLAYER deactivation / authorization removal
   - route/claim-index/current membership updates
4. only then may any successor route/epoch be opened for remaining authorized participants
```

A write accepted before close remains accepted. A stale ordinary write losing to close is rejected. No retroactive rollback/replay is authorized.

This is a mechanical reconciliation of Step-5.8 currentness and existing membership semantics; no human decision is required.

---

## 10. Multi-LIVE / cross-scope composition

Preserved owner law:

```text
freeze/close each required current native LIVE source
-> prove exact final source(s)
-> one owner-approved campaign-domain transfer/reconciliation where required
-> optional successor source(s)
```

A partial freeze is recoverable technical state, not partial fictional transfer. No distributed transaction, global rollback, global live coordinator, arbitrary commit-order winner or fictional chronology inference is introduced.

---

## 11. Step-2 regression/deferred accounting

Current tests inspected:

- `DEV/TESTS/ACCESS_CONTROL_CASES.md`;
- `DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md`;
- `DEV/TESTS/LIVE_SCENE_CASES.md`;
- `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md`;
- `DEV/TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md`;
- `DEV/TESTS/INTEGRITY_CASES.md`;
- `DEV/TESTS/TODO_MULTIPLAYER_LIVE_BRANCH.md`.

Current implementation/test debt is evidence, not current law. In particular:

- repair login-oriented cases where they are accidentally read as stable PLAYER identity rather than a separate owner-specific login check;
- repair M10 revocation ordering;
- repair L04 per-user-action one-write assumption to native durability-edge semantics;
- add typed claim/currentness/application-authorization/CLOSED_UNABSORBED/source-native-ID adversarial coverage;
- retain the manual two-independent-session smoke test as downstream verification when the execution surface exists.

These are WP-22/WP-26 implementation/documentation obligations, not authorization to edit tests/runtime now.

---

## 12. Step-2 completeness gate

```text
SOURCE_MANIFEST_OPEN_WORLD: YES
ACTUAL_OWNERS_INSPECTED: YES
SR16_01_FULLY_CONSUMED: YES
SR16_02_FULLY_CONSUMED: YES
SUPPORTED_CONNECTOR_STABLE_PRINCIPAL_CAPABILITY: VERIFIED
MUTABLE_LOGIN_USED_AS_STABLE_PLAYER_IDENTITY: NO
OWNER/CONSUMER/SCHEMA/TEST ROUTES INSPECTED: YES
CURRENT_ACCEPTED_DECISIONS_RECONCILED: YES
GENUINE_CONTRADICTION_REQUIRING_STOP: NO
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
STEP_3_READY: YES
```

The manifest remains open for new dependencies discovered by Steps 3–8, especially the mandatory independent Step-6 whole-project reconstruction.