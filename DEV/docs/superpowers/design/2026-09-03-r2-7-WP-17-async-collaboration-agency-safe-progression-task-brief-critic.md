# R2.7 WP-17 — Async Collaboration / Agency-Safe Progression — Whole-Project Task-Brief Critic

Status: **MANDATORY STEP-1 WHOLE-PROJECT TASK-BRIEF CRITIC — ALL BLOCKING/SIGNIFICANT FINDINGS REPAIRED**

Date: 2026-09-03

Starting verified public state: `cc2c02da53c5d8b0e4cc5e759d3991716766d8c8`

Reviewed Task Brief:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-task-brief.md`

Reviewed Source Manifest:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-source-manifest.md`

The critic independently reconstructed the dependency/consumer graph from current project routing and owning sources rather than checking only whether the Task Brief repeated the initial WP-17 scope list.

---

## 1. Critic method

The review attacked the Step-1 framing through these independent routes:

1. owner admission — whether delayed human input creates a new owner at all;
2. authorization/agency — whether an input can lawfully exercise a specific PC's voluntary agency;
3. currentness/generation — whether obligation/generation identity can remain current as native state/routes move;
4. execution/idempotency — whether contribution collection can accidentally become gameplay execution/replay authority;
5. chronology — whether response/transport order can leak into fictional ordering;
6. information/output — whether catch-up/waiting output can leak truth/knowledge/secrets or duplicate delivery authority;
7. persistence/recovery — whether a durable collaboration owner could become a queue/frontier/session/checkpoint authority;
8. machine inventory — whether conditional catalog/root/ID surfaces are being mistaken for a closed realization;
9. consumer reverse audit — whether current CORE/schema/tests introduce hidden assumptions;
10. neighboring-domain containment — whether WP-18 Story/Dramaturg work is being pulled into WP-17.

Severity meanings follow current HDM design process:

- `BLOCKING` — Step 1 cannot safely authorize evidence/design work until repaired;
- `SIGNIFICANT` — material omission/ambiguity likely to cause wrong owner/consumer coverage or invalid later synthesis;
- `MINOR` — clarity/maintenance issue that does not invalidate Step-1 scope.

---

## 2. Finding register

### B01 — Natural-owner admission hole

**Severity:** `BLOCKING`

**Attack:** A brief that starts from “design collaboration obligation/window/generation” can silently assume a new durable owner even when the case is `INDEPENDENT_IMMEDIATE` or already owned by Procedure/Continuation/Choice/Reaction.

**Risk:** duplicate wait/currentness owner, generic collaboration queue, second Procedure/Continuation semantics, unnecessary persistent state.

**Owning evidence:** R2.5 coordination families and collaboration-owner limit; Step-3 native ordered owners; Catalog Contracts runtime-record admission threshold; conditional catalog/WP-11 surfaces.

**Repair applied:** Task Brief now requires a three-family admission matrix before representation and admits a collaboration owner only for an independently durable/recoverable collection lifecycle not already owned by a native ordered owner.

**Disposition:** `CLOSED`.

---

### B02 — Secure contribution agency-admission hole

**Severity:** `BLOCKING`

**Attack:** A PLAYER ID, session association, LIVE participant list or existing obligation reference could be treated as sufficient authority to supply a voluntary PC contribution.

**Risk:** stale/foreign participant speaks or acts for another PC; absence becomes implicit agency transfer.

**Owning evidence:** WP-16 stable principal -> PLAYER -> control -> operation authorization chain; R2.5 absence/external-coordination laws.

**Repair applied:** Task Brief now requires current trusted-principal, active binding, current controlled-PC relation, purpose-specific authorization and current collaboration/native admission before an agency-bearing contribution is accepted. OOC/non-agency input remains typed separately.

**Disposition:** `CLOSED`.

---

### B03 — Collaboration-generation/currentness supersession hole

**Severity:** `BLOCKING`

**Attack:** One `generation`/window value could become a hidden campaign-global frontier, or an old obligation could remain writable after the underlying scene/LIVE/procedure/agency opportunity moved.

**Risk:** stale reply mutates successor state, currentness chosen from session/message age, global collaboration clock introduced by accident.

**Owning evidence:** R2.5 generation law; WP-16 domain-separated currentness; WP-14 current-authority-first recovery; WP-15 no universal frontier.

**Repair applied:** Task Brief separates collaboration generation currentness from campaign/LIVE/native, Procedure/Continuation, PLAYER/control/authorization, Interaction/message evidence and local cache currentness. It requires explicit bounded supersession/obsolete handling and forbids global-frontier semantics.

**Disposition:** `CLOSED`.

---

### B04 — Contribution-to-execution/idempotency seam missing

**Severity:** `BLOCKING`

**Attack:** Collected contribution or late response could itself establish gameplay consequence, or a duplicate/late input could cause a second RuntimeCommand/segment/RNG realization.

**Risk:** mechanics replay/reroll, duplicate fiction, collaboration owner becomes gameplay owner.

**Owning evidence:** R2.5 collection-only law; Step-3 Interaction/RuntimeCommand/ExecutionSegment/Continuation/RNG identity; WP-13/WP-14 no replay across transport/recovery ambiguity.

**Repair applied:** Task Brief requires contributions to associate with accepted Interaction/typed input evidence; collection never executes consequence; duplicate transport retry reuses input identity; later intentional same prose is new input; stale/late responses re-enter only through current admission and cannot replay accepted mechanics/RNG/idempotency.

**Disposition:** `CLOSED`.

---

### B05 — Recipient-safe catch-up/disclosure boundary missing

**Severity:** `BLOCKING`

**Attack:** “Catch up the returning player” can be implemented by copying full chat/history, all message evidence, another player's context or planning/secret material.

**Risk:** information leak; message evidence becomes truth/knowledge; read receipt/currentness inferred from cursors.

**Owning evidence:** R2.5 catch-up laws; R2.3 Context Runtime; Step 4 truth/knowledge/role eligibility; Step-5.11 message evidence; Step-5.12 disclosure/EMISSION_COMMIT.

**Repair applied:** Task Brief now requires current routed recipient/role eligibility, bounded catch-up, separate truth/knowledge/message/disclosure owners, own-obligation exposure only, and existing emission validation. Full transcript/planning/secret copying and cursor-as-read-proof are explicitly forbidden.

**Disposition:** `CLOSED`.

---

### S01 — Required versus optional contributor minimality underspecified

**Severity:** `SIGNIFICANT`

**Attack:** Campaign/party membership or scene presence could enroll everybody as required.

**Repair applied:** positive bounded material dependency + minimal required set are mandatory; optional eligible contributors cannot block; removal/supersession conditions must be audited.

**Disposition:** `CLOSED`.

---

### S02 — Purpose/scope/generation binding and contribution reuse underspecified

**Severity:** `SIGNIFICANT`

**Attack:** One reply could silently satisfy another question/window/generation because wording appears compatible.

**Repair applied:** Task Brief requires exact typed purpose/scope/generation binding and explicit current reinterpret/reconfirmation before any cross-generation reuse.

**Disposition:** `CLOSED`.

---

### S03 — Maximal-safe-frontier progression insufficiently operationalized

**Severity:** `SIGNIFICANT`

**Attack:** Any future dependency could globally freeze a scene/campaign, or a response could narrate beyond the semantic safe frontier.

**Repair applied:** positive dependency, safe-prefix progression, first dependent stop, scope-local waiting and same visible-consequence frontier are explicit workflows/requirements.

**Disposition:** `CLOSED`.

---

### S04 — Absence could collapse into pass/consent/control transfer

**Severity:** `SIGNIFICANT`

**Attack:** silence/timeout/offline state could be interpreted as `PASS`, agreement, speech or permission for another actor/LLM to choose.

**Repair applied:** absence/silence/delay/offline/disconnect explicitly supplies none of those; explicit typed non-action is distinct and only valid when native semantics permit it.

**Disposition:** `CLOSED`.

---

### S05 — “Absence is not consent” could be overcorrected into immunity

**Severity:** `SIGNIFICANT`

**Attack:** an absent PC could become immune to automatic world/rule consequences even when no voluntary opportunity remains open.

**Repair applied:** Task Brief preserves R2.5 absence-not-immunity and requires current owner/rule proof that no voluntary choice/reaction is being fabricated.

**Disposition:** `CLOSED`.

---

### S06 — Transport/message/ref/commit order chronology leak

**Severity:** `SIGNIFICANT`

**Attack:** contribution append order, Git CAS winner or host message arrival could decide a fictionally simultaneous/contested result.

**Repair applied:** all technical/message ordering forms are explicitly excluded from fictional-order authority; WP-15/native rule owner is required where order becomes material.

**Disposition:** `CLOSED`.

---

### S07 — Timeout/presence/heartbeat closure authority not explicitly prohibited

**Severity:** `SIGNIFICANT`

**Attack:** asynchronous waiting invites implementation of TTL, online-presence or “last seen” auto-close semantics.

**Repair applied:** no timeout/message-age/heartbeat/presence/reconnect correctness authority; no background worker is required by Step-1 framing.

**Disposition:** `CLOSED`.

---

### S08 — PLAYER/LIVE/session/cache/index/cursor projection contamination

**Severity:** `SIGNIFICANT`

**Attack:** convenient repeated fields can become alternate obligation/currentness authority.

**Repair applied:** Task Brief names each as neighbor/projection/hint only and requires current owning routes for material use.

**Disposition:** `CLOSED`.

---

### S09 — Durability/recovery/source-movement composition underframed

**Severity:** `SIGNIFICANT`

**Attack:** an admitted collaboration record could become a distributed transaction with LIVE/campaign/message sources or rollback accepted gameplay after partial failure.

**Repair applied:** WP-11/WP-13/WP-14 native-domain composition is mandatory; partial native success remains real; no rollback/distributed transaction; recovery is current-authority-first and bounded.

**Disposition:** `CLOSED`.

---

### S10 — Conditional machine surfaces could be mistaken for already-closed realization

**Severity:** `SIGNIFICANT`

**Attack:** `runtime.collaboration_obligation` in catalog/ID policy plus WP-11 root could be treated as proof of exact schema/lifecycle even though no dedicated current `GAME/SCHEMA` collaboration schema exists.

**Repair applied:** Source Manifest and Task Brief classify catalog/root/ID surfaces as conditional inventory to reconcile and schema absence as negative realization evidence. Neither activates implementation nor hides a later proved lifecycle.

**Disposition:** `CLOSED`.

---

### S11 — WP-18 Story/continuity/Dramaturg boundary porous

**Severity:** `SIGNIFICANT`

**Attack:** catch-up/planning coherence could pull WP-18 into Step 1 or let planning become collaboration evidence/authority.

**Repair applied:** WP-18 is explicit downstream boundary; only no-planning-as-authority/no-planning-secret-in-catch-up constraints are inherited. No WP-18 design is activated.

**Disposition:** `CLOSED`.

---

## 3. Whole-project consumer reconstruction result

The independent traversal reached all material owner classes required to frame Step 2 safely:

```text
collaboration product semantics
native ordered execution owners
principal / PLAYER / control / authorization
campaign + LIVE + HOT currentness
chronology / temporal owners
truth / knowledge / role context
message evidence / disclosure / delivery
durability / publication / recovery / session
conditional catalog / identity / physical route
runtime CORE consumers
schema neighbors + schema absence
executable regression consumers
WP-18 and later downstream boundaries
```

No material current owner was found that requires changing the Step-1 domain into a broader product decision.

No evidence establishes a contradiction requiring R2.5, Step 3, Step 4, Step 5.11/5.12, WP-13, WP-14, WP-15 or WP-16 reopening.

No evidence makes a generic collaboration queue, registry, scheduler, heartbeat service, global active-player owner or global collaboration frontier necessary.

---

## 4. Repaired framing invariants

After repair, later WP-17 evidence/design is constrained to prove:

1. coordination family before representation;
2. natural owner before schema/queue;
3. collaboration collection only, never gameplay consequence;
4. current authorized principal/control for agency-bearing contribution;
5. minimal required set, optional non-blocking set;
6. purpose/scope/generation-bound contribution identity;
7. stale/late/duplicate handling without successor mutation or replay;
8. maximal safe prefix before waiting;
9. absence neither consent nor agency transfer nor automatic immunity;
10. no technical/message order as fictional chronology;
11. no timeout/presence correctness authority;
12. bounded recipient-safe catch-up through current routed owners;
13. truth/knowledge/message/disclosure separation;
14. current-authority-first recovery and native-domain durability composition;
15. conditional machine surfaces remain evidence until semantic admission is proved;
16. WP-18 remains downstream.

---

## 5. Critic gate

```text
STEP_1_CRITIC_BLOCKING:      5
STEP_1_CRITIC_SIGNIFICANT:   11
STEP_1_CRITIC_MINOR:         0
UNRESOLVED_BLOCKING:         0
UNRESOLVED_SIGNIFICANT:      0
HUMAN_DECISION_REQUIRED:     NO
UPSTREAM_REOPEN_REQUIRED:    NO
TASK_BRIEF_REPAIRED:         YES
SOURCE_MANIFEST_REPAIRED:    YES
STEP_2_AUTHORIZED:           NO
NEXT_GATE:                   MANDATORY SENIOR REVIEW
```

The critic authorizes no Step 2 work. Its result is only that the repaired Step-1 package is decision-safe for mandatory Senior review.
