# R2.7 WP-16 — Multiplayer / Access Control / Live State — Architecture Task Brief

Status: **STEP-1 TASK BRIEF — WHOLE-PROJECT CRITIC APPLIED / MANDATORY SENIOR REVIEW REQUIRED**

Date: 2026-09-03

Target branch: `v1/engine-rearchitecture`

Starting verified public state: `b2afeae3033b96f8d688d437972a020eb0f1746f`

Companion open-world Source Manifest:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-source-manifest.md`

Mandatory whole-project Task-Brief critic:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-task-brief-critic.md`

This Task Brief is the repaired Step-1 framing after the mandatory whole-project critic. It authorizes no Step 2 work until Senior review explicitly grants GO.

---

## 1. Purpose

WP-16 performs the R2.7 implementation-facing architecture audit for **multiplayer / access control / live state**.

The domain is not a green-field redesign. Its job is to reconcile the current shipped access/LIVE/multiplayer machine surfaces with already accepted architecture, most importantly R2.5 collaboration/multiplayer and Step 5.8 live-epoch ownership, while preserving WP-11..WP-15 currentness, durability, recovery and chronology contracts.

The Step-1 question is:

> What exact owner graph, currentness/fencing boundaries, participant/control/authorization chain, LIVE lifecycle transitions and cross-scope constraints must WP-16 inspect so that later architecture can close the physical multiplayer/live realization without accidentally creating a global LIVE owner, permission shortcut, campaign fallback, distributed transaction, replay path or player-agency violation?

Step 1 establishes the evidence graph and audit obligations. It does **not** select new product semantics or implement any machine change.

---

## 2. Minimum owning scope

WP-16 must cover, at minimum:

1. authenticated participant identity;
2. durable PLAYER identity/binding and membership lifecycle;
3. controlled-PC authority;
4. creator/member/policy/operation-specific permissions and authorization;
5. LIVE as temporary current truth/writable authority only for the selected immutable typed shared actionable mutation scope;
6. campaign-native currentness versus live-epoch currentness and recovery;
7. exact-source live CAS and ambiguous/rejected publication behavior;
8. live-born stable identity where accepted records/evidence originate inside LIVE;
9. several simultaneously active disjoint LIVE scopes;
10. cross-scope/multi-live transitions and their freeze/absorption/successor lifecycle;
11. `CLOSED_UNABSORBED` current truth with zero ordinary writers;
12. campaign forward absorption, route movement and post-authority ref retirement;
13. participant absence, PLAYER deactivation/reactivation and controlled-PC continuity;
14. player-agency/world-continuity protection during absence/deactivation;
15. bounded recovery/currentness behavior when campaign or selected LIVE sources move, disappear or conflict;
16. current GAME/CORE, schemas, scaffold/bootstrap and regression consumers that realize or assume these semantics.

---

## 3. Binding authority distinctions

The audit must preserve the following distinctions explicitly. They are not optional terminology preferences.

### 3.1 Participant / PLAYER / PC / authorization chain

Conceptually:

```text
AUTHENTICATED EXTERNAL IDENTITY
    proves who the current GitHub principal is
        |
        v
CURRENT PLAYER BINDING / MEMBERSHIP
    maps stable external user identity to one stable campaign PLAYER identity
        |
        v
CURRENT CONTROLLED-PC RELATION
    says which PC(s) that PLAYER may voluntarily control
        |
        v
OPERATION-SPECIFIC AUTHORIZATION
    creator/member/policy/scope/currentness/native-owner checks
        |
        v
CURRENT WRITE-ADMISSION ROUTE
    campaign native owner or selected LIVE owner/partition
```

None of these stages is interchangeable with another.

Required negative rules:

- authenticated GitHub identity is not itself a PLAYER record;
- PLAYER existence is not current active membership;
- active PLAYER membership does not automatically grant control of any existing PC;
- a controlled-PC relationship does not authorize creator-only, policy-only, storage-main, engine-main or another campaign's operations;
- repository Write/Admin/collaborator capability is necessary infrastructure where applicable but never sufficient HDM gameplay authorization;
- cached login/display name/session/card/index metadata is not authority;
- mutable GitHub login is not stable gameplay identity;
- successful Git transport/CAS is not proof that application authorization was valid.

### 3.2 Currentness dimensions

The audit must keep separate:

```text
CAMPAIGN CURRENTNESS
    exact selected campaign ref/HEAD and current campaign routing metadata

LIVE EPOCH CURRENTNESS
    current selected LIVE source + exact source revision/HEAD + ACTIVE/CLOSED lifecycle

LOCAL HOT CURRENTNESS
    current local adopted owner bytes proven against selected native source basis
```

A campaign HEAD may advance while a selected LIVE source remains current truth for its claimed owners. A LIVE source may move while campaign HEAD does not. SQLite/local generation and session/cache freshness are not a substitute for either.

### 3.3 Source/authority geometry

For every native mutable owner/partition X, later WP-16 synthesis must preserve an equivalent bounded decision:

```text
WriteAuthorityLookup(X)
    -> CAMPAIGN
     | LIVE(epoch/ref)
     | INTEGRITY_CONFLICT
```

A selected LIVE scope is not:

- the entire scene graph by physical proximity;
- the campaign base;
- another LIVE epoch;
- every referenced entity/dependency;
- a repository branch whose existence alone makes it authoritative.

The immutable typed claim set and native-owner containment/admission rules determine current write authority.

### 3.4 Semantic establishment versus transport order

The audit must distinguish:

- prospective local calculation;
- accepted Step-3 execution state;
- live native semantic establishment at exact-source CAS where LIVE owns the mutation;
- campaign native semantic establishment at its owner-native publication edge;
- ref/commit/CAS transport ordering;
- fictional causal/chronology ordering.

Git winner, commit order, CAS order, ref revision, LIVE integer `revision`, campaign commit order or source movement cannot silently decide fictional order or actor intent. Conversely, an already accepted native semantic edge cannot be rolled back/replayed merely because a later cross-domain edge rejects.

---

## 4. Closed upstream architecture to consume as constraints

WP-16 must consume current owning sources and determine applicability before treating older runtime/schema prose as authority.

### 4.1 R2.5 collaboration / multiplayer

Consume:

- participant-to-PLAYER/control separation;
- multiple independent participant TurnEnvelopes; no global active player;
- native ordering owner wins over transport order;
- absence is not consent and does not authorize taking over voluntary PC action;
- another participant's report of an absent player's intended action is only a hint;
- presence/heartbeat/reconnect is not authority;
- catch-up/rejoin must reacquire current campaign/live routing and own obligations before mutable input;
- collaboration owns contribution collection only, not gameplay consequence;
- split-party current state, chronology, collaboration and planning remain separate owners.

WP-17 owns durable asynchronous collaboration realization. WP-16 may consume only the owner/agency/currentness constraints necessary to its own live/access domain.

### 4.2 Step 5.8 live-epoch ownership

Treat as the primary semantic/live ownership constraint unless a proved contradiction/material insufficiency requires reopening.

Mandatory applicability checks include:

- current campaign route selects LIVE authority; branch existence does not;
- exactly one current truth authority and at most one ordinary writable authority for each claimed owner/partition;
- immutable typed non-overlapping claims;
- no implicit claim graph closure;
- machine-decidable bounded containment and write-authority lookup;
- ACTIVE exact-source CAS;
- application authorization distinct from CAS;
- ACTIVE -> CLOSED monotonic lifecycle;
- `CLOSED_UNABSORBED` = current truth + zero ordinary writers;
- route-away requires confirmed CLOSED exact final revision;
- close does not cancel accepted execution;
- live atomicity is per native durability edge, not necessarily per user action;
- prepared/unselected LIVE source is non-authoritative;
- successor selection only after predecessor absorption/transfer rules permit it;
- absorption is forward campaign publication, not branch merge/replay;
- selected LIVE recovery never falls back to campaign base;
- revocation/claim-transfer rules close affected LIVE authority before withdrawal and prevent stale-writer windows;
- multi-live transfer is coordinated freeze + campaign transition + optional successors, not a distributed transaction;
- partial freeze progress is technical state, not partial fictional establishment;
- source-native live identity remains stable where accepted identity escaped;
- no force push, generic LIVE mega-owner or Git-order chronology.

### 4.3 Access / branch ownership

Consume `DEV/ARCHITECTURE/ACCESS_CONTROL.md` and `DEV/ARCHITECTURE/BRANCH_MODEL.md` for:

- engine/storage/campaign authority separation;
- campaign creator derivation and creator-only operations;
- stable external user-ID -> PLAYER binding;
- invite-only/open-contributor admission boundaries;
- narrow self-enrollment/self-reactivation exceptions;
- active/inactive PLAYER lifecycle;
- explicit controlled-PC transfer;
- mechanical-policy authority as a separate sub-authority;
- non-force campaign/live publication and target-ref routing.

### 4.4 WP-11..WP-15

Mandatory constraint review:

- **WP-11:** LIVE exceptional physical route, native semantic identity/routing, source-native epoch-qualified identity, indexes/paths non-authoritative;
- **WP-12:** local prospective state versus authoritative live-CAS establishment; post-CAS local adoption; no SQLite+LIVE distributed transaction; local possession != permission;
- **WP-13:** frozen authorization/currentness footprint, owner-native publication edges, no cross-domain rollback/replay, non-force publication and partial outcome truthfulness;
- **WP-14:** current-native recovery, selected LIVE no campaign fallback, exact pins, `CLOSED_UNABSORBED` recovery and session/cache non-authority;
- **WP-15:** native occurrence identity, no duplicate materialization across CAS conflict/recovery, fixed RNG/idempotency and technical-order/chronology separation.

Closed upstream work is not reopened because current shipped schemas are stale. Reopen only on a demonstrated contradiction, newly unsatisfied consumer or material insufficiency.

---

## 5. Mandatory machine/consumer reconciliation questions

Step 2, if Senior-authorized later, must answer these from evidence. Step 1 merely defines the required traversal.

### 5.1 Identity, membership and control

Determine the exact current source/derivation for each:

- authenticated external principal identity;
- campaign creator identity;
- stable PLAYER identity;
- external user binding;
- active/inactive membership and deactivation provenance;
- controlled-PC assignment;
- join/self-enrollment/reactivation eligibility;
- operation-specific creator/member/policy authority;
- target campaign/repository/ref authorization.

Inspect all cache/index/card/MANIFEST/session fields that repeat or project these facts and classify them as owner, association, projection, hint or stale debt. No repeated field may become a parallel authority by convenience.

### 5.2 LIVE routing and claim realization

Reverse-audit current scene-centric LIVE realization against the Step-5.8 typed-claim model.

Current `GAME/SCHEMA/live_scene.schema.yaml` / `GAME/CORE/LIVE_SCENE.md` contain scene participants, PC lists, overlays, touched paths/entities, provisional entities and one-file source state. Step 2 must establish:

- which native owner/partition classes may actually be claimed;
- how claim membership/containment is represented or deterministically derived;
- how overlap is rejected boundedly across selected LIVE routes;
- which fields are current native owner payload, derivative routing, evidence, projection or obsolete implementation shape;
- how campaign current routing selects the exact LIVE source without treating source existence/scene membership as authority;
- how known native identities route through the WP-11/Step-5.8 physical model.

Physical one-file packing may remain an implementation option only if it preserves native owner boundaries and per-edge semantic/currentness rules.

### 5.3 Exact-source CAS and currentness

Explicitly disposition all candidate fence/currentness values:

- campaign HEAD/base campaign SHA;
- campaign route generation/material routing fields;
- live source ref/HEAD/exact source revision;
- schema `revision` integer;
- blob SHA / file SHA;
- session `base_head_sha`/`last_published_head_sha`;
- local HOT source basis;
- scene `opening_live_head_sha` / `last_absorbed_live_head_sha`;
- touched/dependency metadata.

The result must identify which exact value fences an authoritative mutation, which values support diagnostics/idempotency/recovery, and which cannot establish currentness.

### 5.4 Deactivation/revocation while LIVE is selected

Audit the exact current sequence for voluntary leave, creator removal, permission revocation, controller transfer and other authority withdrawal that intersects an ACTIVE LIVE epoch.

The later architecture must satisfy all of:

1. no already-selected live writer continues ordinary mutation after authority withdrawal becomes current;
2. an affected ACTIVE source is terminally closed/fenced through its exact-source CAS rules where required;
3. a stale writer that loses to close rejects rather than publishes/replays;
4. already accepted native semantics before close remain real;
5. campaign absorption/current-route movement occurs through forward owner-native publication;
6. when absorption and authorization removal are one semantic campaign boundary, they publish coherently enough to avoid a current campaign state where authorization is removed while the old live route remains ordinary-writable, or vice versa;
7. `CLOSED_UNABSORBED` remains current truth with zero writers until lawful forward movement;
8. successor epoch, if any, uses the new authorized claim/participant basis and never reopens the predecessor.

Current CORE/test wording such as “freeze -> compact -> deactivate” is evidence to reconcile, not presumed canonical sequencing.

### 5.5 Absence and player agency

The domain must preserve:

- temporary human absence is not membership revocation;
- no liveness heartbeat/timeout gives authority to another participant;
- absence/deactivation does not teleport, delete, kill, rewrite beliefs/emotions/speech or invent voluntary material actions for the absent player's PC;
- the PC remains a world entity under ordinary world/native owners;
- automatic consequences may still occur only when their existing rules/causal owners require them and no unresolved voluntary choice is being fabricated;
- another player/LLM may not claim absent-player agency because a shared scene or LIVE source is writable;
- rejoin/reactivation restores the same PLAYER identity and current control state, subject to explicit intervening controller transfers and current authority.

### 5.6 Multi-LIVE and cross-scope transitions

Audit concrete cases where one semantic operation depends on or changes more than one independently writable live/campaign scope.

Required boundary:

```text
NO ordinary global transaction
NO global LIVE owner
NO rollback of accepted native edges
NO fictional ordering from freeze/CAS order
```

A cross-scope transition may require bounded freeze/currentness proof over affected sources, a campaign/native semantic acceptance edge, and forward successor setup. If one native edge accepts while another rejects/returns indeterminate, the accepted edge remains real; current sources must be recomposed and affected gameplay may block/retry/repair rather than fabricate atomic rollback.

Step 2 must distinguish:

- technical freeze progress;
- semantic transition acceptance;
- campaign route movement;
- chronology relation establishment;
- source cleanup.

### 5.7 Live-born identity

Reconcile current `provisional_id` / compaction-rekey assumptions with Step-5.8/WP-11 identity law.

An epoch-local provisional/rekeyable ID is legal only where the native owner contract proves that no stable external reference escapes before promotion. Any accepted LIVE-born owner/evidence identity that participates in durable causal/idempotency/current state references must use a collision-free source-native stable identity and survive absorption without rekeying.

### 5.8 Native durability edge granularity

Reconcile current tests/prose that imply “one logical user action = one LIVE_STATE write” with Step-3/Step-5.8/WP-12 per-native-durability-edge semantics.

Later physical batching may combine data only when all participating native semantics share one lawful atomic establishment edge. Player-message/action grouping alone cannot manufacture atomicity, nor may one LIVE file force unrelated owners into one semantic transaction.

### 5.9 Recovery and `CLOSED_UNABSORBED`

Audit startup/resume/currentness paths for:

- selected ACTIVE LIVE;
- selected CLOSED unabsorbed LIVE;
- absorbed predecessor + active successor;
- absorbed predecessor with no successor yet;
- missing selected LIVE source/state;
- orphan/unselected live source;
- campaign route/source movement during local cached play;
- locally surviving prospective/pre-CAS state;
- authorization change during recovery.

Campaign base never silently substitutes for selected LIVE current truth. Session, cache, checkpoint, card or apparent newest source may not select authority.

### 5.10 Information surfaces inside LIVE

Classify `live_facts`, `known_by_pc_ids`, `perceived_by_pc_ids`, observable events and similar fields against Step-4/WP-07/Step-5.12 owners.

LIVE may physically carry current/evidence data required by its selected native scope, but physical presence cannot create a second `world.knowledge`, `runtime.disclosure` or `runtime.message` owner. Absorption/normalization must preserve the correct natural owner and information eligibility.

---

## 6. Required current consumers / realization surfaces

The open-world Source Manifest controls the complete set. At minimum Step 2 must directly inspect the relevant portions of:

### Runtime / CORE

- `GAME/CORE/MULTIPLAYER.md`
- `GAME/CORE/LIVE_SCENE.md`
- `GAME/CORE/RUNTIME.md`
- `GAME/CORE/BOOTSTRAP_RUNTIME.md`
- `GAME/CORE/SESSION.md`
- `GAME/CORE/PERSISTENCE.md`
- `GAME/CORE/STORAGE.md`
- `GAME/CORE/INTEGRITY.md`
- `GAME/CORE/INFORMATION.md` where LIVE information fields cross eligibility/knowledge/disclosure
- chronology/process modules only where currentness/technical-order or accepted occurrence identity constrains LIVE behavior.

### Machine schemas / campaign scaffold

- `GAME/SCHEMA/player.schema.yaml`
- `GAME/SCHEMA/live_scene.schema.yaml`
- `GAME/SCHEMA/scene.schema.yaml`
- `GAME/SCHEMA/session.schema.yaml`
- `GAME/SCHEMA/campaign_manifest.schema.yaml`
- `GAME/SCHEMA/current_state.schema.yaml`
- relevant event/PC/knowledge/disclosure/runtime schemas discovered through actual refs;
- `GAME/CAMPAIGN/MANIFEST.yaml`
- PLAYER/SCENE/CURRENT/index/scaffold templates and generator code that establish initial membership/routing fields.

### Regression / conformance evidence

At minimum:

- `DEV/TESTS/ACCESS_CONTROL_CASES.md`
- `DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md`
- `DEV/TESTS/LIVE_SCENE_CASES.md`
- `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md`
- `DEV/TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md`
- `DEV/TESTS/INTEGRITY_CASES.md`
- `DEV/TESTS/TODO_MULTIPLAYER_LIVE_BRANCH.md`
- any additional tests/conformance checks actually reached while tracing the owners above.

Tests are evidence/consumers. Stale expectations do not override closed architecture.

---

## 7. Explicit non-goals

WP-16 Step 1 does not:

- implement LIVE schemas/runtime/tooling;
- choose SQL tables or exact Python APIs;
- build a websocket/server/leader/lease service;
- add background polling or heartbeat authority;
- add a distributed transaction across campaign/live refs;
- create a global LIVE owner, global currentness frontier or universal lock;
- change Step-3 execution ownership;
- change Step-4 knowledge/disclosure ownership;
- redefine fictional chronology;
- create or realize durable async collaboration obligations owned by WP-17;
- decide Dramaturg physical realization;
- implement migration/bootstrap changes;
- repair stale tests/docs now;
- start implementation planning.

---

## 8. WP-17 boundary

WP-17 — async collaboration is a neighboring domain, not part of this Step-1 architecture task.

WP-16 may consume only constraints that affect immediate access/live correctness, for example:

- an absent participant's unresolved voluntary choice remains owned by collaboration/agency semantics rather than being invented by LIVE;
- a durable collaboration obligation, if later admitted, must route through its natural owner/currentness and must not turn LIVE into a generic async queue;
- current LIVE closure/absorption cannot erase already-owned pending collaboration state.

Any question whose primary purpose is durable asynchronous contribution, offline response collection, collaboration deadline/fallback policy or long-lived collaboration record realization must be routed to WP-17 unless a direct contradiction proves WP-16 cannot close without it.

---

## 9. Failure / ambiguity classes that must be represented in evidence

The audit must explicitly cover at least:

- authenticated identity unavailable/ambiguous;
- zero or multiple active PLAYER bindings for one principal;
- inactive binding;
- controlled-PC mismatch;
- creator/member/policy authorization mismatch;
- repository capability present but HDM authorization absent;
- stale prepared authorization;
- selected LIVE route conflicts or overlapping claims;
- selected source missing/incompatible;
- exact live source moved before CAS;
- CAS rejection;
- CAS result indeterminate;
- stale writer racing terminal close;
- campaign route movement while live cache is held;
- CLOSED selected source awaiting absorption;
- partial multi-live freeze/transition;
- orphan/prepared/unselected live source;
- live-born identity collision/rekey hazard;
- post-CAS local adoption failure;
- recovery with stale session/cache/player association;
- deactivated/absent participant while PC remains fictionally present;
- async collaboration concern that must be routed to WP-17 rather than silently solved in LIVE.

Ambiguity must produce bounded refresh/retry/block/integrity handling under the owning contract, not guessing or force-pushing.

---

## 10. Evidence and synthesis requirements for later Steps

If Step 2 is authorized, evidence extraction must preserve item-level qualifiers, negative findings, scope limits and downstream routing. The Source Manifest remains open-world through Step 8.

Before any Decision Brief/candidate/canonical result, later work must demonstrate:

1. complete owner/source manifest for the material participant/access/live graph;
2. explicit field/consumer disposition for repeated authority/currentness identifiers;
3. native claim/containment coverage for every supported live-mutated owner/partition;
4. exact lifecycle/currentness table for ACTIVE, CLOSED_UNABSORBED, absorbed and successor states;
5. authorization/currentness interaction proof for join, leave, removal, controller change and stale sessions;
6. exact-source CAS/ambiguous-publication contract consistent with Step-5.8/WP-12/WP-13;
7. multi-live/cross-scope composition without distributed transaction semantics;
8. live-born identity compatibility with WP-11/Step-5.8;
9. player-agency/absence/deactivation negative cases;
10. recovery compatibility with WP-14;
11. chronology/currentness separation with WP-15;
12. explicit WP-17 boundary and routed obligations;
13. later executable coverage routed to WP-22;
14. measured optimization/repartition questions routed to WP-24.

---

## 11. Step-1 completion criteria

WP-16 Step 1 is complete only when all are true:

```text
TASK_BRIEF_PRESENT:                         YES
OPEN_WORLD_SOURCE_MANIFEST_PRESENT:         YES
WHOLE_PROJECT_TASK_BRIEF_CRITIC_PRESENT:    YES
ALL_BLOCKING_FRAMING_FINDINGS_RESOLVED:     YES
ALL_SIGNIFICANT_FRAMING_FINDINGS_RESOLVED:  YES
AUTH_ID_PLAYER_PC_AUTH_SEPARATED:            YES
CAMPAIGN_VS_LIVE_CURRENTNESS_SEPARATED:      YES
TYPED_LIVE_CLAIM_SCOPE_REQUIRED:             YES
EXACT_SOURCE_CAS_REQUIRED:                   YES
CLOSED_UNABSORBED_FIRST_CLASS:               YES
DEACTIVATION_AGENCY_BOUNDARY_REQUIRED:       YES
MULTI_LIVE_NO_DISTRIBUTED_TXN:               YES
WP17_BOUNDARY_EXPLICIT:                      YES
UPSTREAM_REOPEN_REQUIRED:                    NO unless later evidence proves threshold
HUMAN_DECISION_REQUIRED:                     NO at Step 1
IMPLEMENTATION_WORK:                         NONE
STEP_2_AUTHORIZED:                           NO
```

After publication and cursor synchronization, work stops at mandatory Senior review.

---

## 12. Downstream routing

- **WP-17:** durable asynchronous collaboration and offline contribution realization; not activated.
- **WP-18:** Dramaturg implementation must consume access/live/agency constraints but gains no state/control authority.
- **WP-19/WP-20:** bootstrap/migration eventually realize approved PLAYER/LIVE/routing/schema changes after architecture approval.
- **WP-22:** executable conformance/failure-injection for identity/binding/control/authorization, claims, CAS, close/absorption, stale writers, multi-live, recovery and agency.
- **WP-24:** measure live-state size/fanout/latency before selecting packing/repartition/rollover optimization.
- **WP-26:** reconcile stale CORE/schema/test wording after accepted architecture, including any old scene-centric, one-action-one-write, provisional-ID or chronology-currentness wording.

These are obligations only. WP-16 Step 1 activates none of them.

---

## 13. Step-1 gate

```text
WP16_STEP_1:                 COMPLETE AFTER COHERENT PUBLICATION
STEP_1_CRITIC_BLOCKING:      4
STEP_1_CRITIC_SIGNIFICANT:   12
UNRESOLVED_BLOCKING:         0
UNRESOLVED_SIGNIFICANT:      0
HUMAN_DECISION_REQUIRED:     NO
UPSTREAM_REOPEN_REQUIRED:    NO
STEP_2_AUTHORIZED:           NO
WP17_STARTED:                NO
IMPLEMENTATION_PLANNING:     NO
NEXT_GATE:                   MANDATORY SENIOR REVIEW
```
