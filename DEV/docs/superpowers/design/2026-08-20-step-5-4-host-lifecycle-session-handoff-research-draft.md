# Step 5.4 — Host Lifecycle & Session Handoff — Research Draft

Status: **RESEARCH / DRAFT — NOT CANONICAL**

Date: 2026-08-20

Basis:

- `2026-08-20-step-5-4-host-lifecycle-session-handoff-task-brief.md`
- current Step-5.2 canonical v2
- current Step-5.3 canonical specification
- Step-3 execution contract
- current runtime SESSION / RUNTIME / BOOTSTRAP / STORAGE / DURABILITY / PERSISTENCE / INTEGRITY contracts
- current session/current/checkpoint schemas
- current multiplayer/live contracts for boundary evidence only

---

# 1. Executive research result

The current architecture does **not** need a new durable handoff snapshot, universal session-transfer record, or campaign-global host lease to make ordinary singleplayer/new-chat recovery correct.

The native owners established by Steps 3, 5.2 and 5.3 already contain the gameplay-significant state needed to resume:

```text
world/domain owners
runtime.command / resolution / procedure / continuation
accepted Interaction / IntentPlan when the handoff promise includes that point
temporal source owners + Step-3 accepted execution
current owning live scope where applicable
compatible runtime/catalog interpretation context
```

The missing Step-5.4 architecture is a **host-lifecycle barrier contract**, not another state owner.

Preliminary recommended model:

> **BARRIER-NATIVE** — When the runtime has reliable evidence that its current host/context is about to be destructively lost and a recovery-safe handoff is intended, it stops extending the handed-off mutation scope, requires the gameplay-significant state promised across that handoff to reach a valid durable Resumable Runtime Closure, and acknowledges the handoff only after that closure is known durable. A fresh host then performs ordinary bounded hydration from native durable sources; it does not consume a handoff snapshot.

Unexpected crash is fundamentally different:

> If the host disappears without a successful handoff barrier, recovery resumes from the newest actually valid durable native source set. Any newer volatile HOT/SOFT state that was destroyed is lost and is never reconstructed by plausibility, old prose, model memory, or intended-but-unconfirmed publication.

A third result is that current persistent `session` metadata is best classified as **coordination/recovery projection and optional observability**, not gameplay or write authority. `session.status`, `base_head_sha`, and `last_published_head_sha` may help coordination but cannot grant mutation rights, prove current gameplay state, or fence a stale host by themselves.

A fourth result is that the existing current-chat `maintenance continuation frame` is valid only for **non-destructive maintenance where the same context survives**. If maintenance can destroy the current context, every gameplay-significant resume fact promised after that destruction must already live in native durable owners or be materialized into them before successful handoff acknowledgement.

A fifth result is that a periodic safety ceiling for unpublished SOFT state is a necessary complementary risk-control concept, but its threshold and general policy are Step 5.5. The existing runtime hard-coded `one hour` value is therefore provisional/stale relative to the current owner direction and must not constrain Step 5.4.

---

# 2. Evidence classification

## FACT F1 — Chat/process state is explicitly temporary

Current storage contracts treat chat context and extracted runtime cache as temporary working state. ChatGPT Memory is not campaign storage. Bootstrap resolves campaign/runtime state from durable repository evidence and an exact runtime package rather than requiring old chat state.

## FACT F2 — Step 5.2 already defines cold recovery without prior chat memory

Resumable Runtime Closure requires a fresh runtime with no prior chat/model/process memory to recover the last actually promised durable gameplay point from compatible domain-native sources and bounded typed routing.

Volatile state ahead of that durable point may be lost. Recovery must not invent it.

## FACT F3 — Step 5.2 already admits unresolved accepted input as a conditional recovery owner

A materially unresolved accepted `Interaction` / `IntentPlan` is independently recovery-relevant when the applicable durability/handoff policy promises that semantic point across cold restart.

Exact wording may be irreducible temporarily only when it is the only evidence preserving accepted meaning. The full transcript does not thereby become authority.

## FACT F4 — Step 3 already has semantic resume owners

Step 3 provides distinct owners for:

```text
Interaction
IntentPlan
RuntimeCommand
Procedure
Resolution
Continuation
pending child / firing identity
fixed accepted execution evidence
```

Therefore a generic handoff payload would normally duplicate state already owned elsewhere.

## FACT F5 — Step 5.3 already preserves accepted temporal/pending execution

A temporal occurrence that crosses into accepted mandatory execution is recoverable through native owner state plus Step-3 execution identity. A host restart does not need a scheduler snapshot to rediscover or replay it.

## FACT F6 — Current session metadata is explicitly not full chat history

`GAME/SCHEMA/session.schema.yaml` defines coordination/recovery metadata containing session identity/status, player/PC/scene references and known branch frontier references. It is updated at persistence boundaries rather than every turn.

Nothing in the schema makes it current world/execution authority.

## FACT F7 — Current SESSION prose already distinguishes exact wording from semantic resume

If exact previous wording remains in the same chat it may be reused. If it does not, runtime should use durable semantic evidence and must not fabricate quotations.

## FACT F8 — Current maintenance continuation frame is RAM/current-chat state

`SESSION.md` explicitly says the maintenance continuation frame is current-chat working state, not automatically campaign canon, checkpoint, or commit.

Therefore that frame is insufficient by itself for maintenance that actually destroys the chat/context that contains it.

## FACT F9 — Current runtime already distinguishes lost volatile state from durable canon

`RUNTIME.md`, `SESSION.md`, `STORAGE.md`, and Step 5.2 all prohibit invention of dirty HOT/SOFT state that disappeared before publication.

## FACT F10 — Current multiplayer/live correctness does not rely on session status

Multiplayer revalidates authenticated PLAYER binding and current branch/live scope at relevant synchronization/write boundaries. Live scenes use live-epoch state and optimistic CAS. Stale sessions cannot retain authority merely because their local/session metadata still says active.

## FACT F11 — Live scope is already independently authoritative when active

During an active live epoch, mutable scene truth belongs to that live scope, not stale campaign base. A generic host handoff record cannot override this ownership.

## FACT F12 — Publication acknowledgement and durable truth are distinct

The current persistence protocol can create a commit and then fail to advance/ref-confirm it because of races/failures. Step 5.6 still owns the complete physical crash-consistency model.

Therefore Step 5.4 must define handoff acknowledgement in terms of **known durable closure**, not merely “a write was attempted.”

## FACT F13 — Current one-hour policy predates the current Step-5.5 decision

Several runtime modules hard-code a one-hour dirty-state ceiling. The current owner direction explicitly states that the number is not approved/canonical. This is existing policy debt, not evidence that Step 5.4 should adopt one hour.

---

# 3. Constraints

## C1 — Host lifecycle is not campaign lifecycle

Chat/context destruction, process restart, model-context compaction or runtime-package maintenance does not by itself mean:

```text
campaign paused
session fiction ended
world time advanced
Procedure terminated
player intent cancelled
```

Those are separate semantic decisions owned elsewhere.

## C2 — Controlled handoff and unexpected crash have different guarantees

A controlled handoff may impose a pre-destruction barrier. An unexpected crash cannot retroactively do so.

## C3 — Handoff cannot create a second current-state authority

A handoff artifact, if any, may only be coordination/recovery evidence. It cannot copy world/execution/temporal/live current truth as a second owner.

## C4 — Handoff safety cannot depend on always receiving a host warning

Host/platform lifecycle-warning capability is optional. Correct crash recovery must remain valid when no warning arrives.

## C5 — No background daemon is assumed

If the host supplies no callback or execution opportunity while inactive, HDM cannot promise an exactly timed publication.

## C6 — No raw model/process-memory durability

Hidden model state, chain-of-thought, full context windows and opaque prompt caches are not campaign authority.

## C7 — Stale host state cannot grant write authority

Any later mutation must be revalidated against current native ownership/authorization/revision constraints. `session.status=active` is insufficient.

## C8 — 5.4 specifies logical closure, not Git mechanics

Step 5.4 may require “this closure must be durable before successful handoff acknowledgement.” Step 5.6 decides how repository writes make that guarantee true and how ambiguous transport outcomes are resolved.

## C9 — 5.4 does not select general durability cadence

Step 5.4 may introduce a lifecycle-triggered forced durability reason. Step 5.5 owns SOFT/HARD/SAVE semantics and independent dirty-age policy.

---

# 4. Lifecycle taxonomy

The research finds five useful **logical conditions**, not a required persistent state machine.

| Condition | Meaning | Durability implication |
|---|---|---|
| `ATTACHED` | current host/context is usable and may continue under normal authority | ordinary 5.5 durability rules |
| `CONTROLLED_DESTRUCTION_PENDING` | reliable current evidence says this host/context is intentionally about to become unusable and recovery-safe handoff is intended | freeze relevant mutation window; require handoff durability closure |
| `RELINQUISHED` | controlled handoff was acknowledged and old host must no longer continue from its pre-handoff hot state | any later use must rehydrate/resync as a new/current host |
| `LOST` | host/context disappeared without successful handoff acknowledgement | recover only actual durable source set |
| `HYDRATING` | fresh/restarted host is rebuilding from durable native evidence | no mutation until required source/authority/interpretation validation succeeds |

These conditions need not be stored as one campaign record. They describe runtime behavior.

`paused`, `active`, `ended`, campaign lifecycle and live-epoch lifecycle remain separate concepts.

---

# 5. Host-event classification

| Event | Logical class | Key rule |
|---|---|---|
| new chat after normal prior durable state | fresh hydration | bootstrap from durable native sources |
| explicit “move/continue in another chat/runtime” | controlled destructive handoff | require recovery-safe handoff closure before success acknowledgement |
| host gives reliable context-expiry warning | controlled destructive handoff opportunity | trigger barrier if there is gameplay-significant state to preserve |
| runtime-package switch, same context retained | non-destructive maintenance | ephemeral continuation context may help presentation; native state still governs |
| runtime-package switch destroys context | controlled destructive handoff | ephemeral maintenance frame alone is insufficient |
| maintenance restart | controlled destructive if old context will be lost | same barrier semantics |
| user explicitly pauses campaign | gameplay/campaign lifecycle boundary plus host/session behavior | separate semantic pause decision; may also cause durability boundary |
| user simply closes chat | host loss/termination, not automatically campaign pause | recovery guarantee depends on last durable closure unless a controlled barrier completed |
| process/context crash | uncontrolled loss | no finalization promise; recover durable closure only |
| stale old chat returns | stale/resumed host | must revalidate current authority/revision; cannot use stale hot state blindly |
| network/write failure during handoff | failed/incomplete controlled handoff | do not acknowledge recovery-safe success without durable proof |

---

# 6. Semantic resume-point ownership

No universal `resume_point` object is currently justified.

Use the narrowest existing native owner that actually carries the unresolved semantic state.

| Resume situation | Native evidence/owner | Handoff requirement |
|---|---|---|
| no unresolved accepted input/execution | world/current routing + active roots | durable current gameplay state sufficient |
| accepted player message interpreted but no executable command yet | `Interaction` / `IntentPlan` | if handoff promises this point, preserve accepted message identity/meaning sufficiently |
| RuntimeCommand accepted | `runtime.command` | command/root closure must be recoverable |
| Activity executing/suspended | `runtime.resolution` + `runtime.continuation` | preserve fixed accepted inputs/cursor/RNG/offer state |
| Procedure active between commands | `runtime.procedure` | independent Procedure root remains recoverable |
| pending Choice/Reaction | `runtime.continuation` | same generation/offer/responder/options survive |
| temporal occurrence still merely armed | native temporal owner + temporal routing | recover candidate and reevaluate |
| temporal occurrence already accepted | source claim/final state + Step-3 execution | resume same firing/execution |
| current world/scene state only | normal world/live owners | no handoff copy required |
| exact prior wording only useful for prose continuity | transcript/current chat if available | not a recovery prerequisite |
| exact wording is the only evidence preserving accepted material meaning | specific Interaction/message evidence | must remain recoverable until meaning is materialized into typed state |

### Research inference

The current `SESSION.md` maintenance continuation frame should be split conceptually:

```text
presentation/orientation hints
    may remain ephemeral when host survives

accepted gameplay meaning / unresolved execution
    must live in typed native owners if promised across destructive handoff
```

A durable prose “continuation summary” should not become a substitute for missing typed state.

---

# 7. Controlled handoff model

## 7.1 Barrier purpose

A successful controlled handoff must prevent this state:

```text
old host acknowledges “safe to continue elsewhere”
while gameplay-significant state that the handoff promised to preserve
still exists only in the soon-to-die context
```

Therefore the recommended logical sequence is:

```text
reliable destructive-lifecycle signal / explicit handoff intent
    -> enter handoff barrier for affected mutation scope
    -> stop acknowledging new gameplay mutations in that scope
    -> materialize any accepted semantic state that is still RAM-only
       into its proper native owner as required
    -> require applicable resumable closure to become durably recoverable
    -> verify success at the logical durability boundary
    -> acknowledge RECOVERY_SAFE_HANDOFF
    -> old host relinquishes use of pre-handoff hot state
```

## 7.2 Scope of freeze

The barrier should freeze only the ownership/mutation scopes being handed off, not an unrelated entire campaign/world by default.

Examples:

- singleplayer current campaign/runtime scope: effectively the current active mutation closure;
- independent multiplayer scene: only the affected player/session/current owning scope unless shared/live rules require broader coordination;
- active live scene: 5.8 owns exact transfer/fencing, but 5.4 requires no acknowledged handoff to strand current live-owned recovery obligations.

## 7.3 What “complete” means

Step 5.4 does not define the general dirty classifier. It requires:

> Every gameplay-significant state that the controlled handoff promises to preserve must belong to a valid durable Resumable Runtime Closure before handoff success is acknowledged.

Step 5.5 determines which current SOFT/HARD/SAVE/operational dirty state must join that forced handoff boundary.

## 7.4 No-op case

If all promised gameplay-significant state is already durably recoverable and no recovery-critical derivative needs updating, a controlled handoff does not need a heartbeat commit merely to record that a handoff happened.

The handoff can succeed by validating/relying on the existing durable closure.

This is important evidence against a mandatory handoff-ticket record.

---

# 8. Handoff failure semantics

## 8.1 Publication fails while old host remains alive

The runtime SHALL NOT report recovery-safe handoff success.

Preferred behavior:

```text
handoff remains incomplete
old host/context remains the only holder of any unpublished state
retry/repair the required durability boundary when possible
```

If the platform/operator destroys the host anyway, the event becomes an uncontrolled/degraded loss with recovery only from the last actual durable point.

## 8.2 Host dies during an ambiguous publication attempt

The new host SHALL NOT trust the old host’s intended result or missing acknowledgement.

It must resolve the actually durable native source set from repository/live evidence according to 5.6/5.7.

Logical outcomes:

```text
publication actually durable
    -> resume that newer closure

publication did not become authoritative
    -> resume prior durable closure

source evidence inconsistent/ambiguous beyond allowed protocol
    -> RECOVERY_REQUIRED / CANON_SUSPECT equivalent
```

## 8.3 User/operator insists on termination after failed handoff

The architecture cannot prevent an external host from being killed.

It can only preserve semantic honesty:

- do not call it a successful safe handoff;
- do not promise state that was not durably closed;
- after loss recover the prior actual durable point.

No special rollback commit is implied.

---

# 9. Unexpected-loss recovery objective

Proposed RPO statement:

> After an unexpected host/context loss, HDM guarantees recovery to the most recent compatible **actually durable Resumable Runtime Closure** whose native source set can be selected and validated. It does not guarantee recovery of newer state that existed only in lost volatile context.

This is not necessarily one campaign commit SHA because Step 5.2 permits a compatible composition of campaign/live/operational native sources.

The guarantee is therefore **semantic and domain-typed**, not a scalar global “latest event/commit” promise.

A dirty-age ceiling in Step 5.5 may bound ordinary exposure in environments where runtime receives execution opportunities, but it cannot change the truth of an abrupt crash that occurs before the next publication opportunity.

---

# 10. Fresh-host bootstrap contract

A fresh host should conceptually perform:

```text
1. resolve selected campaign and exact compatible runtime package
2. select/pin current native durable source revisions
3. resolve current owning scope(s), including live routing when applicable
4. enumerate bounded operational and temporal recovery roots
5. validate required native owners + interpretation context
6. hydrate active world/execution/Procedure/Continuation state
7. rebuild derived caches/Agenda/MechanicalContext/context bundles
8. classify recovery:
       NORMAL_RESUME
       RECOVERY_REQUIRED / SCOPE_BLOCKED
       CANON_SUSPECT / equivalent
9. only then accept new mutation against the resumed scope
```

The exact checkpoint/source-selection wire protocol is deferred to 5.7.

A stale `session.status=active` is not a blocker if native durable ownership says the old host is gone/non-authoritative; conversely `session.status=ended` cannot terminate a still-active native Procedure or mandatory execution chain.

---

# 11. Stale-host semantics

A host is stale when its cached state/authority assumptions are no longer sufficient for the action it is about to perform.

Step 5.4 does not introduce a universal host lease. Instead:

1. a host that locally completed a controlled handoff treats its old hot working set as relinquished;
2. if that host/chat is later used again, it must re-enter through normal current-source validation/hydration rather than continuing from pre-handoff dirty state;
3. any host approaching a correctness-sensitive write must satisfy current authorization, owning-scope and revision checks;
4. campaign/live HEAD or ownership movement invalidates stale transaction assumptions through existing optimistic concurrency rules;
5. current live epoch authority overrides stale campaign copies;
6. `session.status`, local timestamps or remembered host identity cannot bypass these checks.

### Why no campaign-global host lease yet

A generic one-active-host lease would conflict with legitimate multiplayer sessions and may unnecessarily serialize independent scopes.

If Step 5.8 proves that a particular live/multiplayer owner requires fencing/lease tokens, that mechanism should be scoped to that native ownership domain rather than introduced here as a campaign-global session authority.

---

# 12. Session-record disposition

Current `session` record is useful as:

- human/support coordination metadata;
- cached player/PC/scene association;
- last known/base frontier hints;
- session start/end audit/projection;
- potentially a recovery navigation aid.

It should **not** own:

- current world truth;
- command/resolution/continuation state;
- pending temporal work;
- write authorization;
- live-epoch authority;
- the definitive recovery frontier;
- exact chat transcript;
- the fact that a controlled handoff is safe.

Research recommendation:

> Keep `session` metadata non-authoritative. Do not promote it into a handoff lease/ticket owner in Step 5.4.

Its exact future fields/lifecycle may be adjusted during machine realization after 5.4/5.7/5.8, but correctness must not require its status to fence current gameplay ownership.

---

# 13. Maintenance split

Current runtime prose treats maintenance continuation uniformly, but two cases differ architecturally.

## 13.1 Non-destructive maintenance

Examples:

- tool/update operation while same host/model context remains intact;
- runtime package cache switch where the orchestration context survives.

An ephemeral continuation/orientation frame is acceptable because the context carrying it remains alive.

Gameplay state still belongs to native owners.

## 13.2 Destructive maintenance

Examples:

- operation requires a new chat/context;
- controlled restart destroys the current process/model context;
- known context compaction invalidates required working state.

An ephemeral frame is insufficient. If the system promises resume at the current semantic point, the handoff barrier must ensure that point is recoverable from native durable evidence first.

Therefore current `SESSION.md` / `RUNTIME.md` maintenance-continuation prose needs later realization/alignment to make this distinction explicit.

---

# 14. Host lifecycle signal versus dirty-age policy

The architecture should distinguish:

```text
OBSERVED DESTRUCTIVE LIFECYCLE SIGNAL
    host/runtime knows destruction is imminent now
    -> Step 5.4 handoff barrier trigger

GENERAL RISK THAT CONTEXT MAY EXPIRE
    no current reliable destruction signal
    -> Step 5.5 durability-risk/cadence input
```

Examples of observed signals:

- explicit user/requested handoff;
- operator-controlled restart;
- host-provided reliable context-expiry warning;
- maintenance operation known to invalidate context.

A platform having an approximate or documented maximum lifetime is not by itself a new semantic lifecycle state if the runtime cannot observe when destruction will occur. It may motivate a conservative Step-5.5 dirty-age ceiling.

If a host exposes a reliable remaining-TTL signal, an adapter may translate it into `CONTROLLED_DESTRUCTION_PENDING`; Step 5.4 still does not choose a universal threshold.

---

# 15. Alternatives

## Alternative A — BARRIER-NATIVE

No new durable handoff entity.

Controlled destructive lifecycle adds a scoped mutation barrier and requires a valid native durable Resumable Runtime Closure before safe handoff acknowledgement.

Fresh host uses ordinary Step-5.2/5.7 hydration.

### Strengths

- reuses existing semantic owners;
- no duplicate snapshot/recovery authority;
- no heartbeat write when already durable;
- naturally compatible with composed campaign/live sources;
- no campaign-global session lease;
- clean separation from 5.5–5.8;
- smallest new conceptual surface.

### Costs

- host/runtime adapter must know when a destructive boundary is reliably observed;
- barrier requires temporarily stopping new mutation in affected scope;
- durability/publication failure prevents acknowledgement of a safe handoff;
- later slices must provide the physical publication/recovery protocol.

## Alternative B — Durable handoff ticket / transfer record

Create a durable record such as:

```text
handoff_id
source_session/host
optional target
selected recovery refs
resume summary/status
prepared -> complete/aborted
```

### Strongest case

- explicit observability of transfer;
- can distinguish planned restart from crash;
- could point a target host directly to a known source set;
- can record “handoff completed” even when no gameplay state was dirty.

### Costs / risks

- tends to become a scalar recovery-cut authority over domain-native sources;
- duplicates session/checkpoint/routing metadata;
- creates heartbeat writes for otherwise clean handoffs if mandatory;
- requires lifecycle, retention, GC, migration and stale-ticket repair;
- target may not be known;
- does not itself make underlying native state durable;
- live/multiplayer transfer still needs 5.8 native ownership protocol.

Research assessment: **not justified for current requirements**.

## Alternative C — Authoritative session epoch/lease

Promote persistent session state into a fencing authority: only the current session generation may mutate campaign/runtime state after takeover.

### Strongest case

- explicit stale-host rejection;
- easy “one current host” mental model;
- old chats can be fenced after takeover.

### Costs / risks

- conflicts with legitimate multiple multiplayer hosts and independent scopes;
- makes coordination metadata gameplay/write authority;
- adds per-session lease transfer/renewal/liveness semantics;
- may require background expiry or manual recovery;
- duplicates native branch/live optimistic concurrency and authorization;
- campaign-global lease would serialize independent work.

Research assessment: **reject at Step 5.4**. If a native live owner later requires scoped fencing, design it in 5.8.

---

# 16. Preliminary recommendation

Recommend **Alternative A — BARRIER-NATIVE** with HIGH confidence.

Core rules:

1. host lifecycle and gameplay/campaign lifecycle are separate;
2. reliable known destructive context loss creates a **scoped handoff barrier**;
3. while the barrier is pending, do not acknowledge further mutation in the handed-off scope that would escape the closure being published;
4. safe handoff acknowledgement requires the promised gameplay-significant resume state to be durably recoverable through native Step-5.2/5.3 owners;
5. no mandatory handoff record/commit exists when state is already safely durable;
6. unexpected crash recovers only the newest actually durable compatible native source set;
7. ambiguous write intent/acknowledgement is resolved from actual durable evidence after restart, not from host memory;
8. persistent session metadata remains non-authoritative coordination/recovery projection;
9. stale hosts must revalidate current native authority/revisions before mutation; a relinquished host must not continue from its pre-handoff hot state;
10. destructive maintenance uses the same barrier; non-destructive maintenance may use ephemeral continuation/orientation context;
11. exact wording is recovery-critical only when it genuinely carries accepted meaning not yet represented elsewhere;
12. independent max unpublished-SOFT age remains Step 5.5; no numerical value is approved by Step 5.4.

---

# 17. Crash / lifecycle matrix

| Case | Required logical result |
|---|---|
| fresh new chat, previous state durable | bounded hydrate from native sources; no old-chat requirement |
| controlled handoff, no dirty/recovery delta | validate existing durable closure; no heartbeat commit required |
| controlled handoff, dirty gameplay state | barrier -> forced durability closure -> acknowledge only after success |
| handoff with active Command/Resolution | native execution owner included/recoverable; resume same execution |
| handoff waiting on Choice/Reaction | preserve same Continuation generation/offer; do not regenerate choices |
| handoff while accepted Interaction/IntentPlan unresolved | preserve typed accepted input if handoff promises that point |
| expiry warning arrives before any accepted new input | close current safe point; no invented extra interaction |
| expiry warning arrives while internal unaccepted model interpretation exists | internal thought is not durable state; preserve only established/accepted semantic state |
| publication failure, old host alive | handoff not successful; retry/repair or remain attached |
| host dies during ambiguous publication | fresh host inspects actual native durable evidence under 5.6/5.7 |
| abrupt crash with unpublished SOFT | lost SOFT is not reconstructed; resume prior durable closure |
| crash immediately after confirmed durability | resume that closure even if old host did not produce a friendly farewell |
| non-destructive maintenance | ephemeral orientation frame may survive; no durability boundary solely from maintenance |
| destructive maintenance | same controlled handoff barrier as context replacement |
| stale `session.status=active` from dead host | ignore as authority; validate native current owners/routing |
| relinquished old host reopened | rehydrate/resync before mutation; discard stale hot assumptions |
| campaign HEAD advanced by another valid host | stale transaction invalidated/rebased/revalidated |
| live scope owns newer truth than campaign | resolve through live owner; campaign base is not fallback authority |
| exact utterance unavailable, semantic IntentPlan durable | resume meaning; summarize rather than invent quote |
| exact wording genuinely only accepted evidence | retain the specific message/Interaction evidence until semantic materialization |
| no warning and SOFT accumulates | 5.5 dirty-age policy limits exposure when runtime gets an execution opportunity |
| no dirty state at lifecycle/age check | no heartbeat write |

---

# 18. Later-slice requirements / debt

## Step 5.5 — durability semantics

Must define:

- how a controlled handoff reason escalates applicable gameplay-significant SOFT/operational state into required publication closure;
- the independent maximum age/exposure policy for unpublished gameplay-significant SOFT;
- the semantic age metric, not merely arbitrary commit age;
- behavior when no execution opportunity occurs during inactivity;
- no-heartbeat rule for clean state;
- replacement/retirement of current hard-coded `one hour` runtime wording unless that value is separately approved later.

## Step 5.6 — publication/crash consistency

Must make it possible to establish whether a handoff publication actually became authoritative when failure/crash occurs between preparation, commit creation, ref update and acknowledgement.

No “intended write” may count as durable success.

## Step 5.7 — checkpoint/recovery protocol

Must select/pin the newest compatible valid native recovery source set without requiring a handoff ticket or old session memory. It must distinguish normal resume from missing/incompatible recovery evidence.

## Step 5.8 — multiplayer/live ownership

Must provide any native scoped fencing/lease/transfer semantics actually required for live authority. Step 5.4 does not authorize a campaign-global session lease.

## Step 5.11 — transcript retention

Must not retain universal exact transcript merely for handoff smoothness. Exact message evidence is required only when a still-live semantic dependency genuinely needs literal wording/provenance.

## Step 5.12 — host delivery

Must independently resolve crashes around generated/emitted/acknowledged narration. Step 5.4 does not infer that player saw output merely because mechanics were durable.

## Runtime alignment debt

Current runtime prose requiring later alignment includes at minimum:

- `GAME/CORE/SESSION.md` maintenance continuation frame distinction for destructive maintenance;
- `GAME/CORE/RUNTIME.md` maintenance/context-loss wording;
- `GAME/CORE/DURABILITY_GUARD.md`, `SESSION.md`, `STORAGE.md`, `PERSISTENCE.md` hard-coded one-hour policy pending 5.5;
- `GAME/SCHEMA/session.schema.yaml` only if machine realization needs clearer non-authoritative session/handoff status semantics.

---

# 19. Remaining analytical challenges

Before candidate design, challenge at least:

1. Does the barrier require a dedicated durable token to prevent an old host from resuming silently when no gameplay commit was needed?
2. Is optimistic revision/ownership validation sufficient stale-host fencing for singleplayer and independent multiplayer scopes?
3. Can a controlled handoff legally acknowledge success if only a subset of current SOFT state is preserved? If yes, what exactly is the promised subset and can a user understand the loss?
4. Does freezing mutation during handoff create a user-visible deadlock if publication stalls?
5. Could a `session` record provide useful fencing without becoming campaign-global authority?
6. Is accepted Interaction/IntentPlan persistence enough for a response interrupted before RuntimeCommand acceptance, or is specific literal message retention ever required beyond existing Interaction evidence?
7. Can a host TTL signal be trusted as a lifecycle trigger without turning platform-specific timing into canonical gameplay policy?
8. Do live/multiplayer scopes expose a hidden need for a transfer token that should be deferred rather than rejected globally?
9. Does acknowledgement itself need durability, or is actual native durable state sufficient when the acknowledgement is lost?

Preliminary expectation: these challenges are likely resolvable without a new owner-level product decision, but they require explicit adversarial review before a candidate specification.