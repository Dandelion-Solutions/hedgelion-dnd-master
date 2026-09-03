# R2.7 WP-16 — Multiplayer / Access Control / Live State — Mandatory Whole-Project Task-Brief Critic

Status: **STEP-1 CRITIC COMPLETE — 4 BLOCKING + 12 SIGNIFICANT / ALL MECHANICALLY RESOLVED IN PUBLISHED STEP-1 FRAMING**

Date: 2026-09-03

Task Brief under review:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-task-brief.md`

Source Manifest under review:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-source-manifest.md`

Starting verified public state:

- `b2afeae3033b96f8d688d437972a020eb0f1746f`

The critic was performed against current owning sources and current machine/test consumers, not only against roadmap wording. The Task Brief and Source Manifest published with this critic already incorporate every required repair below.

---

## 1. Critic method

The Step-1 framing was attacked across:

- R2.5 participant/collaboration/agency ownership;
- Step-5.8 LIVE authority/currentness/claims/CAS/close/absorption/revocation/multi-live laws;
- access-control and branch ownership;
- Step-3 accepted execution/idempotency/RNG;
- Step-4 and Step-5.12 information ownership;
- Step-5.13 cleanup/ref-retirement boundaries;
- WP-11 physical route/identity;
- WP-12 local-versus-live establishment;
- WP-13 publication/currentness/authorization composition;
- WP-14 recovery/current-source selection;
- WP-15 occurrence identity and technical-order/chronology separation;
- current `MULTIPLAYER`, `LIVE_SCENE`, `RUNTIME`, bootstrap/session/persistence/integrity consumers;
- PLAYER/LIVE/SCENE/SESSION/MANIFEST/CURRENT schemas and campaign scaffold;
- access, membership, LIVE and persistence regression cases;
- WP-17 neighboring async-collaboration ownership.

Severity rule:

- `BLOCKING`: the Step-1 framing could allow a later design to assign wrong authority/currentness or omit a correctness-critical owner seam.
- `SIGNIFICANT`: the Step-1 framing would materially under-specify a required reconciliation/consumer/failure boundary but would not by itself invert the central owner graph.

Reopen threshold remained contradiction/new unsatisfied consumer/material insufficiency. No threshold fired.

---

# 2. Findings

## C01 — BLOCKING — Participant identity, PLAYER binding, PC control and operation authorization were at risk of collapsing into one “player authority” concept

### Attack

A broad “multiplayer access” brief can easily treat authenticated GitHub user, durable PLAYER, active membership, controlled PC and permission to mutate current native state as one boolean. Current machine surfaces repeat user/player/PC/login associations in PLAYER, session, MANIFEST/card/index and runtime prose, so a later implementation could accidentally trust a cached association or repository permission as authority.

That would violate R2.5, `ACCESS_CONTROL.md`, PLAYER schema and Step-5.8 application-authorization separation.

### Required repair

The Task Brief must force an explicit staged authority chain:

```text
authenticated external identity
-> current PLAYER binding/membership
-> current controlled-PC relation
-> operation-specific creator/member/policy authorization
-> current native write-authority route/currentness
```

It must state that no stage implies the next merely by existence and that login/card/session/index/repository permission/CAS success are not substitutes.

### Resolution

**CLOSED.** Task Brief §3.1, §5.1 and failure cases now make the chain and negative rules mandatory; Source Manifest routes every repeated association surface for later classification.

---

## C02 — BLOCKING — Scene-centric LIVE packing could be mistaken for semantic ownership/claim scope

### Attack

Current `GAME/CORE/LIVE_SCENE.md`, `live_scene.schema.yaml` and tests organize one shared scene into one LIVE state with participants, PCs, overlays, touched entities and created entities. Without stronger framing, a later WP-16 design could conclude that everything physically in/shared with the scene is “owned by LIVE”, effectively replacing Step-5.8 immutable typed claims and native owner containment with a scene mega-owner.

### Required repair

The Step-1 package must require explicit reconciliation of:

- native owner/partition classes eligible for claim;
- immutable typed claim membership;
- machine-decidable containment;
- bounded overlap/write-authority lookup;
- campaign route selecting exact LIVE source;
- touched/participant/PC/index/source-existence fields as non-authoritative unless an owner explicitly grants a role.

Physical one-file packing must not merge semantic owners.

### Resolution

**CLOSED.** Task Brief §3.3 and §5.2 plus Manifest §§3, 6, 7 make typed claims/containment and physical-packing nonauthority binding Step-2 obligations.

---

## C03 — BLOCKING — PLAYER deactivation/revocation during ACTIVE LIVE lacked an explicit no-authorization-window/currentness closure requirement

### Attack

Current `MULTIPLAYER.md` and membership case M10 use a sequence resembling “freeze LIVE -> compact -> deactivate -> successor”. Step-5.8 additionally requires current authorization/current-route coherence and specifies that, when absorption and removing authorization are one campaign boundary, they share one campaign transaction strongly enough to avoid a stale authorization/write window.

A vague Step-1 brief could preserve current prose mechanically and permit an intermediate campaign state in which a participant is inactive while the selected old LIVE source remains ordinary writable, or a route is moved while authority removal is not current.

### Required repair

Step 1 must require a full revocation/deactivation state machine review:

- exact-source close/fence first where affected LIVE authority requires it;
- stale writer/close race behavior;
- accepted pre-close semantics remain real;
- CLOSED_UNABSORBED current truth and zero writers;
- forward campaign absorption/route movement;
- coherent authorization removal when it is the same semantic campaign boundary;
- successor only from new authorized basis;
- no reopen/rollback/replay.

### Resolution

**CLOSED.** Task Brief §5.4 explicitly binds all eight requirements; Source Manifest highlights current `MULTIPLAYER.md`/M10 as evidence to reconcile rather than final sequencing authority.

---

## C04 — BLOCKING — Multi-LIVE / cross-scope transitions could drift into either a distributed transaction or false global rollback semantics

### Attack

Cross-scene transfer/global effects may involve campaign plus several LIVE sources. Current tests describe freeze/compact/reopen slow paths, while WP-13/Step-5.8 reject distributed transactions and global rollback. A weak brief could still imply “all affected branches change atomically” or, conversely, let partial technical freeze order leak into fictional/semantic acceptance.

### Required repair

The brief must separate:

- per-source currentness/freeze edges;
- technical partial-freeze progress;
- semantic cross-scope acceptance;
- campaign route movement;
- chronology relation establishment;
- successor opening;
- ref cleanup.

It must state that confirmed accepted native edges remain real, partial rejection/indeterminate outcomes require current-source recomposition/block/retry/repair, and neither replay nor global rollback is allowed.

### Resolution

**CLOSED.** Task Brief §5.6 and failure matrix now make this separation explicit and ban distributed transaction/global LIVE owner/global rollback semantics.

---

## C05 — SIGNIFICANT — Exact LIVE currentness/fence values were under-specified relative to current schema fields

### Attack

Current surfaces expose campaign HEAD/base SHA, live branch/ref, live `revision`, blob/file SHA, opening/final absorbed LIVE SHAs, session HEAD observations and local HOT source bases. If Step 1 says only “use CAS”, a later design can accidentally select the wrong fence or combine incomparable currentness dimensions.

### Required repair

Require field-by-field disposition of every currentness/fencing candidate and explicitly keep campaign-native, LIVE-source and local-HOT currentness separate. Exact Step-5.8 source ref/revision remains the authoritative LIVE mutation fence unless later evidence proves a real contradiction.

### Resolution

**CLOSED.** Task Brief §§3.2 and 5.3 require this exact classification; Manifest §7 enumerates the machine surfaces.

---

## C06 — SIGNIFICANT — Current provisional/rekey identity wording can violate stable accepted LIVE-born identity

### Attack

`live_scene.schema.yaml` and current LIVE prose permit `provisional_id` identities that rekey on compaction. Step-5.8/WP-11 permit provisional identity only if no durable external stable reference escapes before promotion; accepted live-born owner/evidence identity otherwise must be collision-free, source-native, stable through absorption and not use campaign allocator fallback.

### Required repair

The brief must require an explicit live-born identity disposition: identify which current objects may legally remain provisional, which accepted records/evidence require stable epoch-qualified identity and when an ID becomes externally referenceable.

### Resolution

**CLOSED.** Task Brief §5.7 and Manifest §7.1 explicitly route this reconciliation.

---

## C07 — SIGNIFICANT — Current “one logical action = one LIVE write” tests/prose could override native durability-edge granularity

### Attack

LIVE case L04 and persistence case PT19 encode current one-file/action batching assumptions. Step-5.8 and WP-12 define semantic establishment per native durability edge, and one user action may contain multiple durable edges because of choices/reactions/accepted execution lifecycle.

### Required repair

Step 1 must require reconciliation of current batching tests with native owner/ExecutionSegment edge semantics. Physical batching is permitted only where the semantic establishment boundary is genuinely shared; user-message/action grouping cannot create atomicity.

### Resolution

**CLOSED.** Task Brief §5.8 and Manifest §§7.1/9.1 preserve test intent while making native-edge semantics controlling.

---

## C08 — SIGNIFICANT — Participant/PLAYER/PC/session/MANIFEST/index lists could be treated as complete authority maps

### Attack

Current runtime/scaffold repeats participants, player IDs, PC IDs and session associations. Such lists are useful discovery/routing evidence but can become unsafe shortcuts for active membership, control or live claim membership if their completeness/ownership is not declared.

### Required repair

The brief/manifest must require every repeated list/index/summary to be classified as owner, complete owner-defined routing, derivative index, association, projection or stale debt, and forbid inference of authority from omission/presence unless a current owner contract grants completeness.

### Resolution

**CLOSED.** Task Brief §§5.1–5.2 and Manifest §§7–8 make the classification mandatory.

---

## C09 — SIGNIFICANT — Absence/deactivation semantics needed a direct player-agency and world-continuity negative contract

### Attack

Multiplayer/LIVE work can over-focus on technical writability and accidentally treat an absent or inactive participant's PC as free for the GM/another player to command, teleport, remove or narratively resolve. R2.5 explicitly says absence is not consent; current membership tests preserve PC identity/location/state.

### Required repair

Require explicit cases proving:

- temporary absence is not deactivation;
- no timeout/presence authority;
- absence/deactivation does not invent voluntary action/speech/belief/emotion or erase/teleport/kill the PC;
- native automatic consequences may still happen when lawful and no voluntary choice is fabricated;
- reactivation/rejoin reuses stable PLAYER/control state subject to explicit intervening controller transfer.

### Resolution

**CLOSED.** Task Brief §5.5 binds these cases; Manifest §§3.1/10 route R2.5 and runtime agency owners.

---

## C10 — SIGNIFICANT — LIVE information fields could become parallel `world.knowledge` / `runtime.disclosure` authority

### Attack

Current LIVE state contains `known_by_pc_ids`, `perceived_by_pc_ids`, live facts and observable events. Physical co-location inside current LIVE authority for some world owners does not grant ownership of all information semantics.

### Required repair

The brief must explicitly classify these fields against Step-4/WP-07/Step-5.12 natural owners and require absorption/normalization without creating parallel current knowledge/disclosure/message authority.

### Resolution

**CLOSED.** Task Brief §5.10 and Manifest §§3/10 cover the information boundary.

---

## C11 — SIGNIFICANT — `CLOSED_UNABSORBED` needed first-class recovery/currentness framing, not merely “closed means no writes”

### Attack

Current tests correctly block writes after close but some scene-centric flows can encourage switching early to campaign base or treating close as successful compaction. Step-5.8/WP-14 state that selected CLOSED LIVE remains current truth until lawful absorption, with zero writers.

### Required repair

Step 1 must require explicit recovery/startup cases for ACTIVE, CLOSED_UNABSORBED, absorbed predecessor + successor, absorbed without successor, missing selected LIVE, orphan/unselected LIVE, and stale local prospective state. Campaign fallback is forbidden while current route selects LIVE.

### Resolution

**CLOSED.** Task Brief §5.9 and failure matrix make CLOSED_UNABSORBED a first-class state; Manifest routes WP-14 plus current tests/schema.

---

## C12 — SIGNIFICANT — WP-17 async collaboration could be absorbed into WP-16 through absence/offline scenarios

### Attack

R2.5 carries collaboration-obligation concepts and WP-16 necessarily handles absent/rejoining participants. Without an explicit boundary, the live/access audit could start designing durable offline response queues, collaboration deadlines/fallbacks or shared async workflow state.

### Required repair

Define WP-17 ownership explicitly. WP-16 may consume only agency/currentness constraints required for LIVE/access correctness and route durable async contribution/offline collaboration realization downstream unless a proved contradiction makes it unavoidable.

### Resolution

**CLOSED.** Task Brief §8 and Manifest §11 explicitly exclude/route WP-17 realization.

---

## C13 — SIGNIFICANT — Mechanical House-Rules policy authority could be mistaken for ordinary gameplay/PC/live authority

### Attack

PLAYER schema and access architecture include a separate mechanical policy-authority sub-role. A generic permission matrix could accidentally allow policy authority to control PCs or mutate arbitrary LIVE state, or allow ordinary active PLAYER authority to change policy.

### Required repair

Require operation-specific authority classification that preserves creator/member/controlled-PC/policy/storage/engine roles as separate authorities.

### Resolution

**CLOSED.** Task Brief §§3.1/5.1 and Manifest §4 include the policy-authority seam without reopening House Rules.

---

## C14 — SIGNIFICANT — Prepared/orphan/unselected LIVE source existence and cleanup semantics needed explicit nonauthority framing

### Attack

LIVE creation can produce an orphan/prepared branch/source before campaign route selection, and absorbed sources may remain physically present afterward. Source existence, age, name or retained Git bytes must not become current authority or imply that deleting a ref transfers authority.

### Required repair

Require explicit prepared/unselected/orphan/absorbed source dispositions. Selection/current routing establishes authority; cleanup is post-authority under Step-5.13 and cannot establish non-authority retroactively.

### Resolution

**CLOSED.** Task Brief §§3.3/5.9 and Manifest §§3/10 include source-existence and post-authority cleanup boundaries.

---

## C15 — SIGNIFICANT — Bootstrap/menu/card cached identity surfaces could grant premature multiplayer authority

### Attack

Bootstrap deliberately renders menus from compact cards/cached creator/participant logins before full campaign selection. Those values are useful UX hints but must never authorize joining/writing. Current runtime already says real access revalidates after selection; Step-1 scope initially risked omitting this owner consumer.

### Required repair

Include `BOOTSTRAP_RUNTIME.md`, campaign MANIFEST/card/player routing and bootstrap regression surfaces. Require selected-campaign exact basis plus current identity/PLAYER/control/authorization resolution before mutable access.

### Resolution

**CLOSED.** Task Brief §§5.1/6 and Manifest §§6/8/9 include bootstrap and explicitly mark cached login/card/session/index values non-authoritative.

---

## C16 — SIGNIFICANT — Transport/CAS/ref winner could be mistaken for semantic or fictional winner in cross-scope races

### Attack

Exact-source CAS serializes one native source, but R2.5/WP-15 explicitly separate transport order from player intent, native mechanics and fictional chronology. A CAS winner may establish the current source result for one owner without proving arbitrary fictional precedence over another independent scope.

### Required repair

The brief must distinguish prospective calculation, accepted execution, native semantic establishment, transport/ref/CAS order and fictional chronology. Cross-scope chronology/ordering is established only by its owning rules/evidence, not freeze/CAS sequence.

### Resolution

**CLOSED.** Task Brief §3.4 and §5.6, plus Manifest §§3/10, make this distinction binding.

---

# 3. Critic counts

```text
C01 BLOCKING     identity -> PLAYER -> controlled PC -> operation authorization separation
C02 BLOCKING     typed LIVE claims/native owner containment vs scene mega-owner
C03 BLOCKING     deactivation/revocation + close/absorption no-authorization-window closure
C04 BLOCKING     multi-LIVE/cross-scope composition without distributed transaction/global rollback

C05 SIGNIFICANT  exact currentness/fence field disposition
C06 SIGNIFICANT  live-born stable identity vs provisional rekey
C07 SIGNIFICANT  native durability edge vs one-action-one-write assumption
C08 SIGNIFICANT  participant/player/PC/session/index summaries nonauthority
C09 SIGNIFICANT  absence/deactivation player agency + world continuity
C10 SIGNIFICANT  LIVE information fields vs knowledge/disclosure owners
C11 SIGNIFICANT  CLOSED_UNABSORBED recovery/current truth
C12 SIGNIFICANT  WP-17 async collaboration boundary
C13 SIGNIFICANT  policy authority distinct from gameplay/PC/live authority
C14 SIGNIFICANT  prepared/orphan/unselected/absorbed LIVE source nonauthority + cleanup
C15 SIGNIFICANT  bootstrap/menu/card cached identity nonauthority
C16 SIGNIFICANT  transport/CAS order vs semantic/fictitious order
```

Counts:

```text
STEP_1_CRITIC_BLOCKING:       4
STEP_1_CRITIC_SIGNIFICANT:    12
UNRESOLVED_BLOCKING:          0
UNRESOLVED_SIGNIFICANT:       0
HUMAN_DECISION_REQUIRED:      NO
UPSTREAM_REOPEN_REQUIRED:     NO
```

---

# 4. Mechanical repair verification

The repaired Task Brief and Source Manifest now require all material Step-1 framing dimensions:

- authenticated principal / PLAYER / controlled-PC / operation authorization separation;
- creator/member/policy/storage/engine authority separation;
- campaign currentness / LIVE currentness / local HOT currentness separation;
- immutable typed LIVE claim/containment model;
- exact-source CAS/currentness field audit;
- active/closed/absorbed/successor lifecycle;
- deactivation/revocation no-writer-window review;
- absent-player agency/world continuity;
- source-native accepted LIVE identity;
- per-native durability-edge semantics;
- prepared/orphan source nonauthority;
- recovery no campaign fallback;
- multi-live partial outcomes without distributed transaction/global rollback;
- technical order distinct from semantic/fictional order;
- LIVE information fields constrained by natural information owners;
- bootstrap/cache/index summaries treated as nonauthoritative until revalidated;
- WP-17 async collaboration realization explicitly excluded/routed downstream;
- current CORE/schema/test expectations included as consumers/evidence rather than presumed owners.

No framing repair selected an implementation, reopened accepted architecture or introduced a new human-owned product decision.

---

# 5. Explicit non-findings

The critic found no Step-1 evidence requiring:

- a new global player/session authority;
- a LIVE leader/lease/heartbeat;
- a global LIVE owner or global currentness frontier;
- a distributed campaign+LIVE transaction;
- campaign fallback over selected LIVE current truth;
- force push/ref rewind;
- replay/reroll of accepted mechanics on source conflict;
- a new universal live merge algorithm;
- chronology derived from Git/CAS order;
- deletion/takeover of absent-player PCs;
- implementation of WP-17 async collaboration;
- reopening R2.5, Step-5.8 or WP-11..WP-15;
- implementation planning.

---

# 6. Step-1 critic gate

```text
STEP_1_CRITIC_COMPLETE:        YES
BLOCKING_FOUND:                 4
SIGNIFICANT_FOUND:              12
BLOCKING_RESOLVED:              4
SIGNIFICANT_RESOLVED:           12
UNRESOLVED_BLOCKING:            0
UNRESOLVED_SIGNIFICANT:         0
HUMAN_DECISION_REQUIRED:        NO
UPSTREAM_REOPEN_REQUIRED:       NO
TASK_BRIEF_REPAIRED:            YES
SOURCE_MANIFEST_REPAIRED:       YES
STEP_2_AUTHORIZED:              NO
NEXT_GATE:                      MANDATORY SENIOR REVIEW
```
