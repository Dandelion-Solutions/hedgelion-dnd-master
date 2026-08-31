# R2.5 Evidence Ledger — Collaboration & Multiplayer Interaction Semantics

Status: **RESEARCH EVIDENCE / PRE-DECISION SYNTHESIS**

Date: 2026-08-24

Task brief:

- `DEV/docs/superpowers/design/2026-08-24-r2-5-collaboration-multiplayer-task-brief.md`

This ledger preserves the current ownership subgraph, active/inherited research candidates, qualifiers and synthesis before any R2.5 owner decision.

---

## 1. Source Manifest completion

Inspected to current decision depth:

| Source family | Authority role | Status |
|---|---|---|
| current Round-2 roadmap | sequencing | verified R2.5 sole `IN PROGRESS` |
| R2.1/R2.3/R2.4 canonical specs | upstream owners | inspected for catch-up/context/TurnEnvelope handoffs |
| Step-5.4 host lifecycle/session handoff | canonical owner | inspected for session coordination vs authority and bounded resume |
| Step-5.8 multiplayer/live-epoch canonical | canonical owner | inspected for shared-scene mutable authority, CAS, live claims/lifecycle |
| Step-5.9 chronology canonical | canonical owner | inspected for independent fronts/material bridge reconciliation |
| Step-5.12 emission/disclosure | canonical owner | previously inspected in current architecture cycle; recipient exposure remains inherited |
| Step-5.14 integrated recovery/concurrency final | canonical integration owner | inspected for no-second-authority/currentness/recovery composition |
| `GAME/CORE/MULTIPLAYER.md` | shipped runtime owner | inspected for authenticated binding, join/rejoin, sync, split scene policy |
| `GAME/CORE/LIVE_SCENE.md` | shipped runtime owner | inspected for live hot path, observable events and shared-scene currentness |
| `GAME/CORE/CHRONOLOGY.md` | shipped runtime owner | inspected for partial-order and cross-scene bridge behavior |
| `player.schema.yaml` | current machine consumer | inspected |
| `session.schema.yaml` | current coordination consumer | inspected |
| `scene.schema.yaml` | current scene consumer | inspected |
| `live_scene.schema.yaml` | current live consumer | inspected |
| Round-2 evidence disposition ledger | research accounting | active/inherited candidate status verified |
| external idea dossier D21/D22/D23/S43/S44/S45/S54 | research input | task-level semantics/risks/revisit triggers inspected |

Additional exact schema syntax may be inspected in R2.7; R2.5 does not need to choose machine fields to resolve the current semantic boundary.

---

## 2. Established canonical/current facts

### C01 — Shared mutable world authority is already solved

Step 5.8 owns a scene-centered live epoch for a bounded mutable partition, exact-source CAS, terminal freeze and forward campaign absorption.

`LIVE_STATE` is current truth for claimed live scope while routed; physical live packing does not change native semantic ownership.

**Disposition:** INHERITED / DO NOT REDESIGN.

### C02 — Shared-scene synchronization is already bounded and currentness-aware

`LIVE_SCENE.md` uses cheap ref probes and one-file refresh/write on the shared hot path. Observable events carry compact perception semantics; no transcript is stored in live state.

**Disposition:** INHERITED.

### C03 — Different scenes already have independent chronology fronts

Step 5.9 and `CHRONOLOGY.md` explicitly reject a universal campaign clock/total order. Independent scenes remain unordered until a material causal/temporal bridge appears.

**Disposition:** INHERITED; D22 only has collaboration/context delta.

### C04 — Git order is not fictional turn order

Step 5.8/5.9 already require simultaneous/contested fiction to be adjudicated under rules/world chronology rather than commit order.

**Disposition:** INHERITED.

### C05 — Authenticated participant binding and PC control already exist

`MULTIPLAYER.md` + `player.schema.yaml` bind authenticated stable GitHub user identity to one active campaign `PLAYER_`; `controlled_pc_ids` determine PC control. Repository access, login text, invitation and self-identification do not grant PC agency.

Controller change requires explicit persistent event.

**Disposition:** INHERITED S41/S57.

### C06 — Membership lifecycle is already durable without deleting identity

Active/inactive player binding, creator/self deactivation and reactivation preserve stable `player_id`, PC/provenance and preferences. Rejoining does not silently reclaim a reassigned PC.

**Disposition:** INHERITED membership owner; R2.5 adds current-frontier/catch-up admission semantics only.

### C07 — Session metadata is coordination, not authority

Step 5.4 explicitly allows session metadata for coordination/navigation/audit/frontier hints while forbidding it from owning gameplay truth, live authority, definitive recovery or write authorization.

Current `session.schema.yaml` contains player/PC/scene/base-head hints and is not full chat history; it is not updated every turn.

**Disposition:** hard boundary for D21 implementation shape.

### C08 — Host/presence lifecycle does not advance fiction or grant authority

No heartbeat/polling/online-presence dependency exists. Host disappearance does not end scene, advance time, resolve player intent or authorize somebody else to act.

**Disposition:** INHERITED S46/S47.

### C09 — One canon already yields participant-scoped knowledge/disclosure

Step 4/Step 5.12/R2.3 separate objective truth, fictional subject knowledge and human exposure. Context Runtime builds recipient/subject-specific bundles rather than one shared secret-bearing context blob.

**Disposition:** D24 broad principle inherited; R2.5 integrates it with collaboration/catch-up.

### C10 — Per-chat execution remains independent

R2.4 `TurnEnvelope` is one user request / one assistant turn in one physical chat. Multiplayer consists of multiple such participant sessions coordinating through shared durable/native owners, not one merged LLM context.

**Disposition:** upstream boundary.

### C11 — Strict ordered response already has native owners

Where rules require ordered participation (Reaction, Choice, Procedure, Continuation, initiative-like resolution), those typed execution owners define who may respond/when. A collaboration layer must not create a second `active_player` truth for the same obligation.

**Disposition:** key YAGNI constraint on D23.

### C12 — Observational finality is already accepted

Once another participant could observe or act on a shared-established consequence, host Retry/Edit is not a silent shared-history rewrite. Step 5.12/shared publication already own this principle.

**Disposition:** D20 inherited.

---

## 3. Active Diamond / Strong candidates

### D21 — Async multiplayer as persistent collaboration protocol

Research problem:

- transcript alone cannot reliably answer which participant contribution is outstanding, what has been accepted, where return/rejoin begins, or whether unrelated play can proceed;
- async play must not block on the slowest participant by default or silently act for them.

Synthesis:

> A narrow durable coordination semantic is justified **only where an unresolved collaborative collection/response obligation must survive across participant turns/host gaps and no existing Procedure/Continuation owner already owns it**.

This does not justify a global collaboration database or transcript owner.

Current candidate responsibility:

```text
one bounded collaboration scope/window
mode
collection generation/identity
eligible/required participant contribution set
accepted contribution refs
open/closed/resolved coordination state
scope/currentness refs needed for safe resolution
```

World consequence, PC intent semantics, chronology and mechanics remain with native owners.

**Disposition:** ACTIVE — supports narrow per-scope collaboration owner.

### D22 — Split-party independent frontiers — delta

Independent scene/live/chronology frontiers are already accepted.

Active delta:

- collaboration state is scene/scope-local;
- participant catch-up/context follows their current scene/PC/recipient eligibility;
- when a material message/entity/process/participant crosses scenes, native chronology/currentness bridge resolves before receiving scope acts;
- no global party context is created merely because all participants belong to one campaign.

**Disposition:** ACTIVE DELTA / mostly inherited.

### D23 — Mode-specific orchestration

Research correctly rejects one global `active_player`.

Current synthesis identifies three semantically different families:

1. **INDEPENDENT / IMMEDIATE** — one participant input may resolve immediately in its scope when no other human contribution is semantically required;
2. **COLLECTIVE WINDOW** — a bounded free-form collaboration window may collect several participant contributions before one shared resolution;
3. **RULE-OWNED ORDERED** — Procedure/Continuation/Reaction/Choice/etc. owns admissible responder/order; collaboration metadata may display/project that obligation but cannot override it.

**Disposition:** ACTIVE — adopt mode-specific policy, no universal turn owner.

### S43 — OOC/social vs diegetic vs actionable input

A human message may contain more than one semantic segment.

Candidate classes:

```text
OOC_COORDINATION
DIEGETIC_COMMUNICATION
ACTIONABLE_INTENT
CONTROL_SIGNAL
```

Interpreter/R2.4 may classify/partition, but promotion is explicit: OOC plan/`ready` text does not become PC speech/action; diegetic speech does not become unrelated mechanical intent; control signal does not alter world state.

**Disposition:** ACTIVE / adopt typed semantic separation.

### S44 — Recipient-specific catch-up

Full transcript replay is rejected.

Catch-up should be an R2.3/R2.1 projection over authoritative/current/history/disclosure sources, containing only what the returning participant/PC is eligible to receive and what is useful now:

- current actionable scene/party state;
- material eligible changes since a useful known basis where available;
- unresolved own obligations/expected input;
- selective exact evidence when exact wording is protected/material.

A session/base frontier may accelerate selection but is not truth. If no reliable consumed frontier exists, correctness prefers a bounded current orientation + strongest eligible recent evidence rather than pretending an exact read receipt.

**Disposition:** ACTIVE — projection, not new history authority.

### S45 — Explicit join/rejoin frontier acquisition

Current membership semantics are strong, but acting safely after join/rejoin requires integration sequence:

```text
authenticate/bind
-> resolve controlled PC
-> acquire current campaign/live route and exact current source basis
-> mode-specific admission
-> assemble recipient/PC context + catch-up
-> expose unresolved own obligations
-> only then accept mutable gameplay input
```

This does not require changing player identity or live authority.

**Disposition:** ACTIVE DELTA / integrate existing owners.

### S54 — Bounded input collection window

Useful only for free-form situations where several independent short contributions should inform one shared resolution.

Key constraints:

- collection is explicit/registered, not every social scene by default;
- accepted contribution refs survive async gap if the window survives;
- window close is explicit/semantic, not inferred from hidden online-presence silence;
- no contribution means no voluntary PC action;
- a mechanical Procedure/Continuation never delegates its responder/order authority to this window;
- collection must be bounded to one scope/generation and cannot become a party chat log.

**Disposition:** ACTIVE — viable narrow feature; exact close policy is the main remaining product trade-off.

---

## 4. Inherited candidate verification

| Item | Verification | R2.5 handling |
|---|---|---|
| **D20** | shared-established output/history is not silently rewound by host Retry/Edit | preserve; no new work |
| **D24** | shared canon + recipient/subject-scoped disclosure/context already exists | integrate catch-up/TurnEnvelope only |
| **S41** | authenticated principal -> `PLAYER_` -> controlled PC binding exists | preserve |
| **S42** | creator/admin rights distinct from PC agency | preserve; collaboration admin cannot act as another PC |
| **S46** | inactivity/absence does not authorize takeover | preserve; collection close cannot synthesize absent PC intent |
| **S47** | presence/reconnect not authority | preserve; no heartbeat/debounce correctness dependency |
| **S50** | conflicting live mutations serialize by exact-source CAS/scope | preserve; collaboration collection not a lock replacement |
| **S51** | cheap live ref/currentness probes and targeted campaign refresh exist | preserve; no background push required |
| **S52** | hot transfer state bounded, durable history elsewhere | preserve; catch-up is bounded projection |
| **S57** | invitation/repository access != persistent player authority | preserve |

No inherited item currently requires reopening its owner.

---

## 5. Negative / adversarial constraints

The following candidate shapes are currently nonconforming:

- one campaign-global `active_player` or round-robin queue for all play;
- treating party chat/OOC text as diegetic canon;
- acting for an absent PC because a collection window closes;
- waiting for all players across unrelated split-party scenes;
- using wall-clock debounce/online presence as correctness authority;
- storing a second shared transcript as collaboration truth;
- using Git commit order to choose fictional simultaneous winner;
- loading all participant/private context into one common model bundle;
- using collaboration state as live/write/chronology/knowledge authority;
- replacing Procedure/Continuation responder semantics with generic multiplayer readiness;
- requiring a participant to read full transcript before rejoining.

---

## 6. Material architecture tensions

### T01 — No durable collaboration owner vs narrow scoped owner

**No new owner** minimizes persistence, but async collective input that spans chats/turns then depends on host transcript/session memory or must be discarded whenever a host disappears.

A **narrow scoped coordination owner** can survive the gap without owning gameplay consequences.

Current evidence favors the narrow owner, activated only for a real unresolved collection/coordination obligation.

### T02 — Automatic debounce vs explicit collection closure

Wall-clock debounce is convenient for synchronous chat but conflicts with the no-presence/no-heartbeat baseline and is ambiguous in async play.

Current evidence favors explicit semantic close/readiness rules; exact product default remains an owner-level choice if multiple variants remain credible.

### T03 — Participant catch-up frontier as authority vs hint

A precise persistent read/consumed frontier would require stronger delivery/read acknowledgement than HDM currently promises.

Current evidence favors frontier **hints** for efficiency plus recipient-scoped reconstruction from durable owners; do not claim exact human consumption.

### T04 — Collaboration scope vs mechanical procedure

Free-form collection needs a bounded collaboration owner. Strict ordered mechanics already have Procedure/Continuation owners.

Current evidence favors a hierarchy:

```text
native rules/execution owner wins responder/order semantics
collaboration window only owns free-form contribution collection where no native owner already does
```

---

## 7. Preliminary synthesis

Recommended semantic direction before owner decision:

> **Scoped Mode-Owned Collaboration Window + Recipient Catch-up Projection**

Properties:

- default play remains immediate/independent per participant scope;
- a free-form collective window is created only when several human contributions must be gathered before one shared resolution;
- the window durably owns only collection coordination, referencing accepted Interaction/input identities rather than copying prose/world state;
- strict mechanical sequencing delegates entirely to Procedure/Continuation/etc.;
- no absent PC action is synthesized;
- split scenes remain independent;
- catch-up is a recipient-scoped R2.3/R2.1 projection, not a transcript or truth owner;
- join/rejoin acquires current campaign/live frontier and mode admission before mutable input;
- OOC/diegetic/action/control semantics remain typed/separate.

The remaining owner-level choice is whether the current product should admit this narrow free-form collective input-window mode at all, versus keeping all free-form inputs immediate and reserving waiting only for rules-owned procedures.

---

## 8. Completeness status

- Active D21/D22/D23/S43/S44/S45/S54 individually accounted.
- Inherited D20/D24/S41/S42/S46/S47/S50/S51/S52/S57 verified as constraints rather than reopened stages.
- Current live/concurrency/chronology/session owners inspected.
- No hidden dependency on presence, background workers, global clock or transcript coordinator remains in the recommended direction.
- A material owner decision remains and should be presented before candidate specification.
