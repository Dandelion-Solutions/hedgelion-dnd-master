# R2.7 WP-17 — Async Collaboration / Agency-Safe Progression — Architecture Task Brief

Status: **STEP-1 TASK BRIEF + SENIOR REPAIR SR17-01 — MANDATORY SENIOR REVIEW REQUIRED**

Date: 2026-09-03

Target branch: `v1/engine-rearchitecture`

Starting verified public state: `cc2c02da53c5d8b0e4cc5e759d3991716766d8c8`

Companion open-world Source Manifest:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-source-manifest.md`

Mandatory whole-project Task-Brief critic:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-task-brief-critic.md`

Senior recovery:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-step-1-senior-recovery-SR17-01.md`

This is the repaired Step-1 framing after the mandatory whole-project critic plus narrow Senior repair SR17-01. It authorizes no Step 2 work until Senior review explicitly grants GO.

---

## 1. Purpose

WP-17 performs the R2.7 implementation-facing architecture audit for **asynchronous collaboration / agency-safe progression**.

The domain is not a generic messaging, queueing or scheduling subsystem. Its job is to map the already accepted R2.5 collaboration semantics onto the current R2.7 owner/currentness/execution/information/recovery graph and determine the minimum machine owner(s), if any, required when unresolved human contribution must survive participant/chat gaps.

The Step-1 question is:

> What exact natural owner graph, admission threshold, generation/currentness rules, human-input identity and agency barriers must WP-17 inspect so that asynchronous multiplayer can wait only where material human agency is actually unresolved, progress every independent safe consequence, recover correctly across joins/rejoins/source movement, and never turn transport order, presence, message history, session state or a generic queue into gameplay authority?

Step 1 establishes the evidence graph and mandatory audit questions. It does **not** choose exact schemas/APIs, implement a collaboration record, choose a protocol kind for human collaboration input, start WP-18 or begin implementation planning.

---

## 2. Minimum owning scope

WP-17 must cover, at minimum:

1. admission boundary between `INDEPENDENT_IMMEDIATE`, `AGENCY_DEPENDENT_COLLECTIVE` and `RULE_OWNED_ORDERED` coordination;
2. exact natural owner, if one is needed, for durable/recoverable collaboration collection state;
3. collaboration obligation/window/generation identity and currentness without a campaign-global collaboration frontier;
4. required versus optional contributor enrollment and removal/supersession;
5. purpose/scope/generation binding for every accepted human collaboration input;
6. accepted human collaboration input identity and relation to current `runtime.interaction`, `runtime.message` and other admitted input owners/evidence;
7. stale, late, duplicate, retry and successor-generation response behavior;
8. maximal-safe-frontier progression and visible-consequence fencing;
9. agency-safe behavior while a required participant is absent, delayed, inactive or rejoining;
10. current principal -> PLAYER -> controlled-PC -> operation authorization where an input purports to exercise voluntary PC agency;
11. current campaign/LIVE/native owner and chronology basis required before deciding that a contribution opportunity still exists;
12. join/rejoin admission and recipient catch-up through current authoritative routes;
13. truth/knowledge/disclosure/message-evidence separation for waiting/catch-up/collaboration output;
14. durability/publication/recovery behavior for any independently durable collaboration owner that Step 2 proves necessary;
15. current CORE/catalog/identity/storage/schema/session/test consumers and negative evidence that constrain machine realization;
16. explicit collision check against existing mechanical `value.contribution` ownership before selecting any human collaboration input representation;
17. explicit boundary to WP-18 Story/continuity/Dramaturg planning and later implementation/test/performance work.

---

## 3. Natural-owner admission before representation

WP-17 must not assume that every delayed/multi-player response creates `runtime.collaboration_obligation`.

### 3.1 Coordination-family admission matrix

Step 2 must classify each relevant wait/contribution case before selecting storage:

```text
INDEPENDENT_IMMEDIATE
    no remaining material human contribution can change the dependent result
    -> no collaboration obligation merely because another player is absent

RULE_OWNED_ORDERED
    Procedure / Continuation / Choice / Reaction / equivalent native owner
    already owns responder/order/resume semantics
    -> use that owner; do not duplicate it in collaboration

AGENCY_DEPENDENT_COLLECTIVE
    a positive bounded human dependency remains materially capable of changing
    the dependent result, and no native ordered owner already owns collection
    -> evaluate whether durable/recoverable collaboration lifecycle is required
```

A persistent collaboration owner is admissible only if the Catalog Contracts independent-lifecycle/addressability threshold is proved for the remaining collection responsibility.

### 3.2 Candidate collaboration owner boundary

If Step 2 proves an independent durable owner necessary, its maximum responsibility is equivalent to:

```text
stable obligation identity / generation
bounded purpose + collaboration scope
current source/currentness basis needed by that lifecycle
minimal required contributor set
optional contributor set
accepted human-input references to accepted input identities
maximal-safe-frontier association where needed
OPEN / CLOSED / RESOLVED / OBSOLETE-equivalent lifecycle
supersession / obsolete reason where needed
```

It must not own or duplicate:

- world truth or state consequences;
- Procedure/Continuation/Choice/Reaction state;
- fictional chronology;
- PLAYER membership/control/authorization;
- presence/liveness;
- `world.knowledge`;
- `runtime.disclosure`;
- `runtime.message` payload/delivery;
- Story or Dramaturg planning;
- a generic pending-work/job queue or scheduler.

R2.5 LAW R2.5-18 remains binding: collaboration state references accepted Interaction/input identities rather than copying transcript prose or becoming a second message store.

The current conditional catalog family, WP-11 conditional root and identifier policy are machine inventory to reconcile, not proof that a collaboration record must exist for every case.

---

## 4. Authority and currentness distinctions

### 4.1 Human collaboration input agency admission

A human collaboration input that would exercise voluntary PC agency must pass the current WP-16 chain before it can be accepted for that purpose:

```text
trusted current external principal
-> stable GitHub user ID
-> exactly one current active PLAYER binding
-> current controlled-PC relation
-> operation/purpose-specific authorization
-> current collaboration/native admission
```

Repository permission, mutable GitHub login, session association, cached PLAYER ID, LIVE participant list or possession of an old collaboration reference is insufficient.

OOC coordination and non-agency informational input must remain typed separately so a message does not silently acquire PC-action authority.

### 4.2 Distinct currentness dimensions

The audit must keep separate:

```text
COLLABORATION GENERATION CURRENTNESS
    whether this exact obligation/generation is still the admitted collection owner

CAMPAIGN / LIVE / NATIVE OWNER CURRENTNESS
    whether the underlying decision opportunity and mutable gameplay basis remain current

PROCEDURE / CONTINUATION CURRENTNESS
    whether a native ordered owner now owns responder/resume semantics

PLAYER / CONTROL / AUTHORIZATION CURRENTNESS
    whether this principal may supply this human collaboration input now

INTERACTION / MESSAGE EVIDENCE IDENTITY
    what accepted input/output evidence exists

LOCAL SESSION / CACHE / CURSOR FRESHNESS
    operational hints only
```

No collaboration generation, message sequence, arrival timestamp, session cursor or campaign HEAD becomes a campaign-global clock/frontier by convenience.

### 4.3 Generation supersession

A human collaboration input addressed to an obsolete/superseded generation cannot silently mutate its successor. Step 2 must define bounded current-generation acquisition plus deterministic disposition such as current accept, duplicate/idempotent acknowledgement, explicit reinterpret/reconfirmation as new current input, obsolete/stale rejection or typed ambiguity requiring refresh.

Generation supersession cannot rewrite already accepted fiction or cancel an already established native execution edge merely because a later response arrived.

---

## 5. Human collaboration input versus execution, evidence and chronology

### 5.1 Existing mechanical `value.contribution` is not collaboration input

Current architecture already owns the catalog protocol kind `value.contribution` for Rule Element mechanics. `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md` defines a Rule Element as returning a typed `value.contribution` to a deterministic Calculation Selector resolver, and `DEV/CATALOG/core-catalog.json` registers that existing kind.

The mandatory semantic separation is:

```text
existing value.contribution
    = Rule-Element mechanical calculation contribution
    != human async collaboration input
    != collaboration-obligation contribution lifecycle
```

Therefore WP-17 SHALL NOT automatically reuse `value.contribution` as the representation of a human collaboration response merely because R2.5 uses the English word “contribution”.

Collaboration owns collection only. Accepted human collaboration input references SHALL anchor to accepted Interaction/input identities under R2.5 LAW R2.5-18 rather than copied transcript prose. Step 2, if later authorized, must determine the exact representation of human collaboration input from the current Interaction/message/input owner graph and evidence, including Step-3 execution/input identity and Step-5.11 accepted-message evidence.

Step 1 does not invent a replacement protocol kind, value kind, record kind, field name or schema for that input. Exact representation remains an evidence/design question for later authorized Steps.

A collaboration record, if admitted, cannot by itself execute an Activity, mutate world state, close a Procedure, establish chronology or declare a player-visible fact true.

Dependent consequence returns through the current Step-3/native execution owner after the required human-input condition is satisfied.

### 5.2 Duplicate, retry and late input

Step 2 must preserve Step-3 identity rules:

- transport retry of the same accepted Interaction is the same input identity, not a second human collaboration input/action;
- identical prose in a later intentional Interaction is new input and must pass current admission;
- duplicate association cannot execute the same gameplay consequence twice;
- stale/late input cannot replay a settled RuntimeCommand/ExecutionSegment;
- accepted RNG, firing/event identity and Continuation state are not rerolled/reallocated because collaboration delivery was delayed;
- source movement or publication ambiguity is handled through currentness/idempotency, not mechanics replay.

### 5.3 Transport order is not fictional chronology

The audit must never use any of these as an implicit fictional winner/order:

- host message arrival;
- collaboration input append/order;
- Git commit/ref/CAS order;
- message/Interaction/record ID order;
- session/catch-up order;
- wall-clock receipt time.

Where relative fictional order becomes material, use the WP-15 chronology/native rules owner. Where simultaneous/contested human agency is still unresolved, stop at the maximal safe frontier rather than letting transport choose the outcome.

---

## 6. Required/optional contributors and maximal safe frontier

### 6.1 Positive bounded dependency first

A required contributor is enrolled only after a concrete bounded material dependency proves that their still-open contribution can change the dependent result under current owners.

Failure to prove universal independence is not enough. Party/campaign membership, scene co-presence, repository access, online status or possible interest alone cannot create a required set.

### 6.2 Minimal required set

Step 2 must determine:

- which contributor(s) are required;
- which are merely eligible/optional;
- the exact purpose for which each is enrolled;
- the current PLAYER/PC relation relevant to that purpose;
- when a contributor ceases to be required because the opportunity resolves, becomes obsolete, is lawfully superseded or moves to a native ordered owner.

Optional contributors never block closure solely through silence.

Explicit `PASS`, `READY`, `NO_FURTHER_INPUT` or equivalent may satisfy a required contribution only where the owning semantics admit that typed non-action. Absence itself never supplies one.

### 6.3 Maximal safe frontier

The audit must preserve this progression shape:

```text
accepted current input
-> identify concrete material dependency
-> resolve every consequence independent of missing contribution
-> establish and expose only the safe prefix
-> stop before first dependent consequence
-> collect/revalidate missing contribution if still required
```

Waiting is bounded to the dependent collaboration/native scope. Independent scenes/processes and unrelated consequences remain free to progress under their owners.

Player-visible established consequence must not cross beyond the same safe frontier that constrains semantic mutation.

---

## 7. Absence, deactivation and agency

WP-17 must preserve all of:

- absence, silence, offline status, delay or disconnect is not consent;
- absence is not voluntary PC speech/action/belief/emotion/pass/approval;
- absence never transfers voluntary PC control to another participant or LLM;
- another participant's report of the absent player's intention is a discovery hint, not authority;
- temporary absence is not PLAYER deactivation;
- deactivation/controller transfer remains WP-16-owned and does not itself invent fictional action;
- absence is also not immunity: automatic consequences may proceed when current rules/causal owners require them and no applicable voluntary decision/reaction remains open;
- timeout, message age, heartbeat, online/presence state or reconnect status cannot close a correctness-critical contribution obligation in the baseline architecture.

If the current basis cannot establish whether a material voluntary opportunity still exists, refresh the smallest owning scope and stop at the last proven safe frontier rather than guessing.

---

## 8. Join/rejoin and recipient catch-up

Before accepting mutable collaboration/gameplay input after join/rejoin, the audit must preserve an equivalent route:

```text
resolve trusted current principal
-> current PLAYER binding/membership
-> current controlled PC
-> current campaign/LIVE/native write routing
-> current Procedure/Continuation/collaboration admission
-> R2.3 recipient/role-eligible context assembly
-> bounded recipient-safe catch-up
-> expose unresolved obligations belonging to this contributor
-> accept mutable input
```

Catch-up is a recipient projection assembled from current owners and eligible evidence. It is not:

- a second truth owner;
- a full transcript/history dump;
- all-player/all-role context merge;
- proof of what the human read;
- permission to expose another player's private/secret context;
- a Story/Dramaturg planning feed.

Session/collaboration cursors may be routing hints only. They cannot prove human consumption or collaboration currentness.

---

## 9. Information / message / disclosure boundaries

Step 2 must disposition collaboration-related output against existing owners:

```text
objective truth             -> natural world owner / Step 4
fictional PC knowledge      -> world.knowledge
human recipient exposure    -> runtime.disclosure / Step 5.12
accepted communication      -> runtime.message / Step 5.11
role-context projection     -> R2.3 / Step 4
collaboration collection    -> admitted collaboration owner, if proved
```

A message being present, retained or associated with an obligation does not make its proposition true, make every PC know it, prove delivery/reading, or make it eligible for catch-up.

Collaboration/waiting output must pass recipient/source/material-reveal admission before the existing `EMISSION_COMMIT` boundary. Repeated presentation after Retry/interruption must not repeat gameplay mechanics or a fictional action.

---

## 10. Durability, recovery and publication framing

If Step 2 proves an independently durable collaboration owner, it must use existing WP-11/WP-13/WP-14 routing/publication/recovery disciplines rather than introduce a separate transaction system.

Mandatory questions include:

1. what exact native identity/current source selects one current obligation generation;
2. whether any helper/index is needed and why it remains non-authoritative;
3. how the owner participates in required durable source closure;
4. how stale campaign/LIVE/native movement invalidates or obsoletes a generation without global scans;
5. how recovery discovers an open independent collaboration root boundedly, if that lifecycle qualifies as a recovery root;
6. how accepted input identities survive retry/recovery without duplicate use;
7. how partial publication/currentness outcomes remain truthful without rollback of accepted native gameplay edges;
8. how selected LIVE currentness composes where a collaboration dependency touches a live-owned scope without making LIVE the collaboration owner;
9. how session/checkpoint/SQLite/cache survival remains non-authoritative;
10. how no background scheduler/heartbeat is required for correctness.

No distributed transaction across collaboration/campaign/LIVE/message sources is introduced. Native successes remain real; dependent progression waits/revalidates as required.

---

## 11. Current machine/consumer reconciliation questions

Step 2 must reverse-audit at least:

- conditional `runtime.collaboration_obligation` catalog admission;
- existing `value.contribution` catalog registration in `DEV/CATALOG/core-catalog.json`;
- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md` as the semantic owner showing that existing `value.contribution` is the embedded Rule-Element mechanical calculation contribution returned to deterministic selector resolution;
- the exact human collaboration input representation through current `runtime.interaction`, `runtime.message` and other admitted input owners/evidence, without automatically reusing `value.contribution`;
- current campaign-scoped identifier policy for the conditional collaboration-obligation family;
- WP-11 conditional `STATE/RUNTIME/COLLABORATION` root with no baseline index;
- absence of a dedicated current collaboration schema in `GAME/SCHEMA/`;
- `GAME/CORE/MULTIPLAYER.md` waiting/join/rejoin/absence/currentness behavior;
- `GAME/CORE/SESSION.md` recap/session assumptions;
- `GAME/CORE/RUNTIME.md`, `GAME/CORE/LIVE_SCENE.md`, `GAME/CORE/CHRONOLOGY.md` and `GAME/CORE/INFORMATION.md` where they consume affected boundaries;
- current PLAYER/session/LIVE schemas only as neighboring owners/projections, never collaboration authority;
- access-control, membership, live-scene, chronology, Context Runtime and Step-3 regression consumers;
- lack of dedicated async-collaboration executable coverage as a downstream verification obligation rather than license to implement tests in WP-17 Step 1.

The conditional catalog/root/identifier surfaces are evidence of an anticipated physical slot, not semantic proof that every collaboration case must instantiate a record. The existing mechanical `value.contribution` is a separate already-owned surface and is not evidence of a human-collaboration input representation. Conversely, absence of a current collaboration schema cannot be used to hide a proven independent durable lifecycle in chat/session state.

---

## 12. Representative workflows that later evidence must close

### 12.1 Independent participant

```text
PLAYER_A input
-> no positive dependency on B
-> resolve/persist/narrate under native owners
-> no collaboration wait merely because B is absent
```

### 12.2 Collective agency dependency

```text
current input A
-> prove bounded dependency on B
-> establish maximal safe prefix
-> admit/reuse current collaboration generation if required
-> collect current authorized B human input
-> revalidate underlying current basis
-> resolve dependent consequence once through native execution
```

### 12.3 Native ordered responder

```text
Procedure/Continuation/Reaction owns responder/order
-> use native owner
-> collaboration does not duplicate response queue/currentness
```

### 12.4 Late obsolete response

```text
reply targets generation G
-> current generation is G+1 / scope obsolete
-> do not mutate G+1 automatically
-> do not rewind accepted fiction
-> if meaningfully reusable, treat only through explicit current interpretation/reconfirmation path
```

### 12.5 Rejoin catch-up

```text
principal/PLAYER/control/routing current
-> own native/collaboration obligations current
-> assemble bounded recipient-safe catch-up
-> expose only eligible current/history evidence
-> accept response against exact current purpose/generation
```

---

## 13. Explicit non-goals

WP-17 Step 1 does not:

- implement `runtime.collaboration_obligation` schema/code;
- create a new human collaboration input protocol kind/name/schema;
- repurpose existing mechanical `value.contribution` as human async collaboration input;
- create a generic collaboration queue/registry/scheduler/job system;
- create a global active-player loop or round-robin turn owner;
- use timeout/presence/heartbeat as correctness authority;
- change Step-3 execution/Continuation/Choice/Reaction ownership;
- change Step-4 truth/knowledge or Step-5.11/5.12 message/disclosure ownership;
- change WP-15 chronology;
- change WP-16 PLAYER/control/LIVE/access authority;
- implement runtime/schema/template/catalog/test changes;
- start WP-18 Story/continuity/Dramaturg design;
- choose exact SQL/Python/wire schemas;
- start implementation planning.

---

## 14. WP-18 boundary

WP-18 remains downstream.

WP-17 may preserve only constraints needed to prevent cross-domain contamination, including:

- Story/planning cannot establish collaboration currentness or contributor authority;
- Dramaturg preparation cannot consume an absent player's voluntary agency;
- catch-up cannot expose planning-only information merely because planning exists;
- collaboration resolution may later produce canonical evidence that Story/planning lawfully consumes through its own source rules.

WP-17 Step 1 must not design Story coverage, continuity projection, local/shared Dramaturg horizons or planning persistence.

---

## 15. Failure / ambiguity classes that evidence must preserve

The audit must explicitly cover at least:

- no material human dependency despite another participant being absent;
- material dependency whose native owner is already Procedure/Continuation/Choice/Reaction;
- material collective dependency requiring persistence across chat gaps;
- zero/multiple/obsolete collaboration generation candidates;
- required contributor no longer authorized/controlling the relevant PC;
- optional contributor silent;
- duplicate transport retry of same Interaction;
- identical later prose in a new Interaction;
- late reply to obsolete generation;
- underlying campaign/LIVE/native state moves while waiting;
- chronology becomes material while contributions were transport-ordered differently;
- already accepted execution exists before a late contribution arrives;
- recovery after process/chat/session loss;
- missing/malformed conditional collaboration state if current routing says it is required;
- stale session/cursor/index/card/cache suggests wrong obligation;
- catch-up candidate contains ineligible secret/planning/message material;
- host interruption/Retry around collaboration status output;
- partial durability/publication success across independent native domains;
- attempted timeout/presence-based auto-close;
- another participant attempts to speak/act voluntarily for an absent PC;
- existing Rule-Element mechanical `value.contribution` is mistaken for human async collaboration input or collaboration-obligation lifecycle state.

Ambiguity produces bounded refresh/revalidation/wait/block under the owning contract, not guessing, silent takeover, replay or global freeze.

---

## 16. Evidence and synthesis requirements for later Steps

Before a Decision Brief/candidate/canonical result, later WP-17 work must demonstrate:

1. complete owner/admission graph for all three coordination families;
2. explicit proof whether `runtime.collaboration_obligation` is required and for which exact lifecycle only;
3. field/consumer disposition for obligation identity/generation/scope/purpose/contributors/accepted-input references/currentness;
4. minimal required/optional contributor admission and removal rules;
5. current principal/PLAYER/control/authorization proof for agency-bearing human input;
6. stale/late/duplicate/retry semantics tied to Interaction/idempotency without gameplay replay;
7. maximal-safe-frontier and visible-output fencing without transport chronology;
8. bounded currentness composition across collaboration, campaign/LIVE/native owner and Procedure/Continuation domains;
9. join/rejoin/catch-up flow through current routing and recipient eligibility;
10. truth/knowledge/message/disclosure separation;
11. durability/recovery behavior without session/checkpoint/cache authority or generic background scheduler;
12. exact negative ownership proof preventing collaboration from becoming gameplay, chronology, authorization or planning authority;
13. explicit separation of existing mechanical `value.contribution` from human async collaboration input and collaboration-obligation lifecycle;
14. evidence-based selection of the exact human collaboration input representation through current Interaction/message/input owners without inventing or reusing a protocol kind by assumption;
15. downstream executable coverage routed to WP-22;
16. any measured scaling/latency/retention question routed to WP-24;
17. stale CORE/schema/catalog/test wording routed to the appropriate later realization/cleanup domain rather than modified during Step 1.

The Source Manifest remains open-world through Step 8 if Senior authorizes continuation.

---

## 17. Step-1 completion criteria

```text
TASK_BRIEF_PRESENT:                            YES
OPEN_WORLD_SOURCE_MANIFEST_PRESENT:            YES
WHOLE_PROJECT_TASK_BRIEF_CRITIC_PRESENT:       YES
SENIOR_REPAIR_SR17_01_PRESENT:                 YES
ALL_BLOCKING_FRAMING_FINDINGS_RESOLVED:        YES
ALL_SIGNIFICANT_FRAMING_FINDINGS_RESOLVED:     YES
COORDINATION_FAMILY_ADMISSION_EXPLICIT:         YES
NATURAL_OWNER_THRESHOLD_EXPLICIT:               YES
REQUIRED_OPTIONAL_CONTRIBUTORS_EXPLICIT:        YES
PURPOSE_SCOPE_GENERATION_BINDING_EXPLICIT:      YES
STALE_LATE_DUPLICATE_SEMANTICS_REQUIRED:        YES
MAXIMAL_SAFE_FRONTIER_REQUIRED:                 YES
ABSENCE_AGENCY_BOUNDARY_REQUIRED:               YES
TRANSPORT_ORDER_NOT_CHRONOLOGY:                 YES
JOIN_REJOIN_CATCHUP_ROUTE_REQUIRED:             YES
KNOWLEDGE_DISCLOSURE_MESSAGE_SEPARATED:         YES
VALUE_CONTRIBUTION_COLLISION_DISAMBIGUATED:     YES
HUMAN_INPUT_REPRESENTATION_DEFERRED_TO_STEP2:   YES
NEW_PROTOCOL_KIND_IN_STEP1:                     NO
NO_GENERIC_QUEUE_SCHEDULER_ASSUMPTION:          YES
WP18_BOUNDARY_EXPLICIT:                         YES
UPSTREAM_REOPEN_REQUIRED:                       NO
HUMAN_DECISION_REQUIRED:                        NO
IMPLEMENTATION_WORK:                            NONE
STEP_2_AUTHORIZED:                              NO
```

---

## 18. Downstream routing

- **WP-18:** Story/continuity/Dramaturg planning; not activated.
- **WP-19/WP-20:** later bootstrap/migration materialization if an approved collaboration record/schema requires it.
- **WP-22:** executable tests for owner admission, required sets, generation staleness, retries, maximal frontier, absence, join/rejoin, catch-up and information containment.
- **WP-24:** measure collaboration fanout/record growth/currentness/retrieval latency before introducing optimization/partitioning/indexing.
- **WP-26:** reconcile stale CORE/schema/catalog/test prose after accepted architecture where required.
- **WP-27:** implementation-planning readiness only after the R2.7 sequence reaches it.

These are obligations only. Step 1 activates none of them.

---

## 19. Step-1 gate

```text
WP17_STEP_1:                 COMPLETE
SENIOR_REPAIR_SR17_01:       CLOSED
STEP_1_CRITIC_BLOCKING:      5
STEP_1_CRITIC_SIGNIFICANT:   11
UNRESOLVED_BLOCKING:         0
UNRESOLVED_SIGNIFICANT:      0
HUMAN_DECISION_REQUIRED:     NO
UPSTREAM_REOPEN_REQUIRED:    NO
STEP_2_AUTHORIZED:           NO
WP18_STARTED:                NO
IMPLEMENTATION_PLANNING:     NO
NEXT_GATE:                   MANDATORY SENIOR REVIEW
```