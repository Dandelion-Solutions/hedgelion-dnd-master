# Step 5.4 — Host Lifecycle & Session Handoff — Candidate Specification

Status: **CANDIDATE ARCHITECTURE — OWNER DIRECTION APPROVED, ADVERSARIAL REVIEW REQUIRED**

Date: 2026-08-20

Owner-approved direction:

> **BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF**

Derivation:

- `2026-08-20-step-5-4-host-lifecycle-session-handoff-task-brief.md`
- `2026-08-20-step-5-4-host-lifecycle-session-handoff-research-draft.md`
- `2026-08-20-step-5-4-host-lifecycle-session-handoff-analytical-challenge.md`
- `2026-08-20-step-5-4-host-lifecycle-session-handoff-decision-brief.md`
- Step-3 canonical execution contract
- Step-5.1 B-NARROW frontier laws
- Step-5.2 canonical Resumable Runtime Closure v2
- Step-5.3 canonical A-NARROW temporal/pending continuity

This specification defines logical host-lifecycle and handoff semantics only. It does not implement runtime schemas, select a Git publication algorithm, choose SOFT/HARD/SAVE classes or cadence, define checkpoint wire format, define live-epoch fencing, choose transcript retention, or define host-delivery acknowledgement.

---

# 1. Canonical candidate definition

**BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF** means:

> Host/chat/process lifecycle is not a gameplay-state owner. When HDM has a controlled destructive-handoff reason, it establishes a scoped mutation-quiescence barrier, materializes every promised unresolved semantic dependency into its existing native owner, and acknowledges recovery-safe handoff only after the applicable Step-5.2/5.3 Resumable Runtime Closure is actually durable. A fresh host resumes by bounded hydration of native durable sources, not from a handoff snapshot or old model memory.

If the host disappears before a successful handoff closure is established, the event is handled as unexpected loss:

> recover the newest compatible **actually durable** native source set; do not invent or reconstruct destroyed unpublished HOT/SOFT state.

The design introduces no mandatory handoff entity, universal recovery-cut record, campaign-global host lease, authoritative session generation, heartbeat commit, transcript snapshot, or serialized LLM/process state.

---

# 2. Terminology

## 2.1 Host

A **host** is the current ephemeral execution/chat/process context capable of receiving input, running HDM logic and carrying a hot working set.

Host identity is not gameplay authority merely because it exists.

## 2.2 Handoff scope

A **handoff scope** is the smallest native writable/recovery ownership scope whose current mutations and unresolved obligations must become recovery-safe before that host may relinquish it.

A handoff scope is not necessarily the entire campaign.

Examples may include:

- the current singleplayer campaign mutation closure;
- a player/session-local independent scope;
- a live-owned shared scene scope whose exact fencing is later owned by Step 5.8.

## 2.3 Recovery-safe handoff

A **recovery-safe handoff** is a controlled lifecycle result, not a record type.

It is achieved only when:

1. the applicable handoff scope is frozen against newly acknowledged dependent gameplay mutation;
2. every gameplay-significant semantic state promised across the handoff has a proper native owner;
3. every required native owner and recovery-routing derivative belongs to a valid durable Resumable Runtime Closure;
4. required compatible interpretation/runtime/catalog context is recoverable;
5. the durability result is known successful under the later publication contract;
6. the old host relinquishes use of its pre-handoff hot assumptions for that scope.

## 2.4 Host lifecycle signal

A **host lifecycle signal** is host/platform evidence about usability of the current execution context. It does not become gameplay authority.

---

# 3. Logical host conditions

These are behavioral conditions, not a required persistent state machine:

```text
ATTACHED
    current host/context is usable under ordinary authority

HANDOFF_PENDING
    controlled handoff barrier is active for one or more scopes

RELINQUISHED
    this host has completed a handoff for the affected scope and may not
    continue from its pre-handoff hot state without fresh validation/hydration

LOST
    host/context disappeared without successful local handoff completion

HYDRATING
    fresh/restarted host is reconstructing current state from durable evidence
```

Campaign lifecycle (`initializing`, `active`, `paused`, etc.), Procedure lifecycle, live-epoch lifecycle and player membership remain distinct.

A host condition by itself does not advance fictional time, pause/end a campaign, terminate a Procedure, cancel accepted execution or create world/NPC action.

---

# 4. Candidate laws

## LAW 5.4-1 — HOST LIFECYCLE IS NOT GAMEPLAY AUTHORITY

Chat/process/model-context lifecycle SHALL NOT become an alternate owner of world state, execution state, temporal obligations, fictional time, player knowledge, disclosure or live ownership.

Host destruction alone has no gameplay-semantic effect except loss of volatile state that was not durably promised.

## LAW 5.4-2 — CONTROLLED HANDOFF AND UNEXPECTED LOSS ARE DISTINCT GUARANTEES

A controlled recovery-safe handoff MAY require work before destruction and SHALL NOT be acknowledged until its durability preconditions hold.

Unexpected loss has no retroactive finalization phase. Recovery after unexpected loss is bounded by the newest actually durable compatible native source set.

## LAW 5.4-3 — NATIVE RESUME OWNERS

Handoff SHALL preserve unresolved semantic state through existing native owners whenever those owners already exist.

No generic `resume_point`, handoff snapshot or transfer payload SHALL duplicate their authority.

## LAW 5.4-4 — SCOPED QUIESCENCE

Once a handoff closure is frozen for scope `S`, the old host SHALL NOT acknowledge a new gameplay mutation that belongs to or invalidates `S` until either:

1. the handoff succeeds and the host relinquishes `S`; or
2. the handoff is abandoned/failed while the host survives and `S` is returned to valid ATTACHED operation.

Independent scopes and OOC activity that cannot affect the frozen closure need not be globally blocked.

## LAW 5.4-5 — HANDOFF SUCCESS REQUIRES ACTUAL DURABILITY

Attempted, prepared, intended or locally assumed publication is insufficient.

`RECOVERY_SAFE_HANDOFF` may be acknowledged only when the promised native closure is known durably recoverable.

Ambiguous physical publication outcomes are resolved later from authoritative evidence under Steps 5.6/5.7.

## LAW 5.4-6 — NO HEARTBEAT HANDOFF WRITE

If the entire promised resume state is already durably recoverable and no correctness-relevant derivative must change, handoff correctness SHALL NOT require a commit, checkpoint, ticket, timestamp mutation or no-op record merely to state that handoff occurred.

## LAW 5.4-7 — NO INVENTED LOST VOLATILE STATE

After unexpected loss, incomplete handoff or unwarned host hard stop, destroyed unpublished gameplay state SHALL NOT be reconstructed from plausibility, stale narration, remembered chat, model inference, intended writes or approximate progress.

## LAW 5.4-8 — RELINQUISHMENT IS NOT A CAMPAIGN-GLOBAL LEASE

A host that completed handoff SHALL locally treat its pre-handoff hot state as relinquished.

If that host/chat later becomes usable again, it MAY continue only after current-source/authority/revision validation appropriate to the affected scope. The campaign does not need a mandatory global “newest host wins” token.

## LAW 5.4-9 — SESSION METADATA REMAINS NON-AUTHORITATIVE

Persistent `session` metadata MAY support coordination, navigation, audit or observability.

It SHALL NOT by itself grant write authority, own current world/execution state, define the recovery frontier, override live ownership, prove handoff success or fence a stale host.

## LAW 5.4-10 — DESTRUCTIVE MAINTENANCE USES HANDOFF SEMANTICS

Maintenance that preserves the same usable host/context MAY use ephemeral presentation/orientation state.

Maintenance known to destroy or invalidate the current host/context SHALL satisfy the same recovery-safe handoff contract for every promised gameplay-semantic dependency before successful destructive transition acknowledgement.

## LAW 5.4-11 — ACCEPTED SEMANTIC BOUNDARIES, NOT PARTIAL MODEL REASONING

Handoff correctness begins from existing accepted semantic/execution boundaries.

Partial hidden model reasoning, chain-of-thought, unaccepted candidate interpretation and opaque process state SHALL NOT become durable resume state.

If an accepted Interaction exists but its material meaning is not yet represented in typed state, the specific accepted message/provenance evidence needed to finish interpretation honestly is irreducible until materialization or an authorized abandonment/failure outcome.

## LAW 5.4-12 — HOST CAPACITY DETECTION IS OPTIONAL CAPABILITY

HDM correctness SHALL remain valid when the host exposes no reliable remaining-message, remaining-token, remaining-context-capacity, remaining-time or imminent-hard-stop metric.

A missing warning is a normal supported case, not an integrity defect.

## LAW 5.4-13 — CAPACITY HEURISTICS ARE ADVISORY ONLY

Message count, approximate token count, chat age, remembered product limits or inferred context consumption SHALL NOT be treated as authoritative remaining-capacity evidence.

A future prediction heuristic MAY produce an advisory risk signal, warning or handoff recommendation, but SHALL NOT:

- redefine durability;
- prove imminent destruction;
- prove sufficient time remains for handoff;
- change recovery authority;
- weaken unexpected-loss fallback;
- become required for correctness.

False positive => at worst unnecessary early warning/handoff suggestion.

False negative => ordinary unexpected-loss recovery.

## LAW 5.4-14 — RELIABLE HOST DESTRUCTION SIGNAL MAY FORCE HANDOFF

A host capability that provides reliable evidence that the current context is about to become unusable MAY be mapped to `HANDOFF_PENDING` and the scoped barrier immediately when recovery-safe continuity is intended.

No universal numerical threshold is defined by Step 5.4.

## LAW 5.4-15 — ADVISORY NEAR-CAPACITY SIGNAL DOES NOT EQUAL HANDOFF SUCCESS

When the host supplies only an advisory near-capacity warning, HDM SHOULD, when an interaction opportunity exists, warn the player and offer/recommend proactive transfer to a fresh chat/runtime.

The advisory signal itself does not prove a destructive boundary or sufficient completion time. If the player/runtime converts that recommendation into an explicit handoff intent, ordinary controlled handoff semantics apply.

## LAW 5.4-16 — HOST ELAPSED TIME DOES NOT ADVANCE FICTION

Context age, inactivity, host TTL and cold restart SHALL NOT by themselves advance fictional chronology, trigger temporal work or create world consequences. Existing Step-5.3 chronology/due rules remain authoritative.

---

# 5. Host-signal classification

Step 5.4 recognizes three capability classes:

| Signal class | Meaning | Required/allowed response |
|---|---|---|
| `RELIABLE_DESTRUCTIVE` | host contract provides actionable evidence this context will become unusable | may/should enter scoped controlled handoff when continuity is intended |
| `ADVISORY_CAPACITY` | host warns that capacity/lifetime risk is elevated but remaining capacity is not guaranteed | warn/recommend proactive handoff; no correctness assumption |
| `NO_USABLE_SIGNAL` | no actionable warning/telemetry exists, or cutoff occurs first | unexpected-loss fallback |

A host adapter may expose stronger semantics in the future, but those semantics must be explicit in the adapter contract. Step 5.4 does not infer them from observed product behavior.

---

# 6. Controlled handoff protocol — logical contract

The logical protocol is:

```text
H0  ATTACHED

H1  handoff reason established
    explicit user/runtime transfer intent
    OR reliable destructive-host signal requiring continuity preservation

H2  identify affected native ownership/recovery scope(s)

H3  enter scoped HANDOFF_PENDING barrier
    freeze acknowledgement of new dependent gameplay mutation

H4  materialize any promised accepted semantic state still represented only
    by insufficient volatile evidence into its proper native owner/evidence

H5  establish the complete applicable durable Resumable Runtime Closure
    including Step-5.3 pending/temporal continuity and required routing

H6  determine that the durability boundary actually succeeded

H7  acknowledge RECOVERY_SAFE_HANDOFF

H8  old host marks affected hot assumptions RELINQUISHED locally
```

This is a semantic protocol. Steps 5.5–5.8 own the physical class/transport/recovery/live details.

## 6.1 Clean handoff

If H4/H5 discover no missing durable delta, H6 may validate the already sufficient durable closure and H7 may proceed without a new write.

## 6.2 Barrier abandonment

If required durability fails while the host remains usable:

```text
HANDOFF_PENDING
    -> retry/repair
    OR
    -> abandon handoff
       validate/restore ATTACHED operation
```

The barrier is not a durable lock and does not imply infinite waiting.

## 6.3 External destruction despite failure

If an external host/product destroys the context after handoff failure or before H7, the engine cannot convert that event into success. Recovery uses actual durable state.

---

# 7. Semantic resume ownership matrix

| Situation at handoff/restart | Owner/evidence |
|---|---|
| current world/domain truth | native world owner or current live owner |
| accepted Interaction before fully typed meaning | `runtime.interaction` + required accepted message/provenance evidence |
| material typed player intent | `runtime.intent_plan` |
| accepted root execution | `runtime.command` |
| active/suspended Activity | `runtime.resolution` / `runtime.continuation` |
| active Procedure between Commands | `runtime.procedure` |
| Choice/Reaction | same Continuation generation/offer/responder/options |
| mandatory child work | Step-3 pending child/firing identity and root closure |
| armed independently-due temporal source | native temporal owner + Step-5.2 typed temporal routing |
| accepted temporal firing | Step-5.3 owner occurrence/firing closure + Step-3 execution identity |
| fixed accepted RNG | owning Resolution/Continuation/execution evidence keyed to stable experiment identity |
| runtime/catalog interpretation | compatible accepted context required by Step 5.2 |
| exact wording only for narrative smoothness | not a recovery requirement |
| exact wording is only evidence of accepted material meaning | retain only required specific Interaction/message evidence until typed materialization |
| partial model reasoning | never a resume owner |

A generic continuation summary may be useful for presentation but cannot substitute for missing authoritative/irreducible typed state.

---

# 8. Unexpected-loss and hard-stop recovery contract

After process crash, context eviction, product conversation hard stop, forced close or any other loss that occurs without successful recovery-safe handoff:

```text
1. discard assumptions about unpublished lost hot state
2. resolve selected campaign/runtime identity normally
3. select/pin compatible native durable source revisions
4. resolve current owning scope(s), including live authority when applicable
5. boundedly enumerate operational/temporal recovery roots
6. validate required owners + interpretation context
7. hydrate native state and rebuild derived state
8. classify outcome
9. only then accept new dependent mutation
```

Candidate recovery outcomes are conceptual only; Step 5.7 owns final vocabulary:

```text
NORMAL_RESUME
RECOVERY_REQUIRED / SCOPE_BLOCKED
CANON_SUSPECT
```

### Recovery-point objective

The promised unexpected-loss recovery point is:

> the newest compatible actually durable Resumable Runtime Closure that can be selected and validated from native sources.

This may be a composition of domain-native sources rather than one scalar commit/event frontier.

---

# 9. Stale-host contract

A stale or reopened host SHALL NOT publish from old hot/transaction assumptions merely because the chat remains accessible.

Before dependent mutation/write it must satisfy current applicable:

- campaign/live ownership routing;
- authorization/player binding;
- branch/live revision validation;
- pinned-source compatibility;
- accepted execution idempotency/resume identity;
- interpretation/runtime compatibility.

If state is unchanged, an old chat may rehydrate/validate the same durable state and continue. Step 5.4 does not prohibit reuse solely because another host once existed.

If state advanced, current native truth constrains the old host after refresh.

No universal “latest session wins” rule is introduced.

---

# 10. Maintenance contract

## 10.1 Non-destructive maintenance

If host/model context remains usable throughout maintenance:

- current-chat orientation/continuation hints may remain ephemeral;
- maintenance does not by itself force a handoff publication;
- gameplay truth still comes from native owners;
- runtime/package compatibility changes must still obey their own migration/adoption contracts.

## 10.2 Destructive maintenance

If maintenance will destroy/invalidate the host context and current gameplay point is promised after the operation:

- enter ordinary scoped handoff barrier;
- persist/recover native semantic dependencies first;
- do not rely only on ephemeral maintenance continuation frame;
- acknowledge successful destructive maintenance handoff only after recovery-safe closure.

---

# 11. Host capacity exhaustion contract

The observed product case is explicitly supported:

```text
chat is writable
    -> host may or may not provide warning
    -> product reaches conversation/message/context limit
    -> current chat can become physically unwritable
```

Step 5.4 does not assume an API exposing exact remaining capacity.

## 11.1 Reliable signal path

If a future/current host exposes a documented reliable imminent-cutoff signal:

```text
signal
    -> controlled lifecycle opportunity
    -> scoped barrier
    -> recovery-safe closure
    -> handoff recommendation/transition
```

## 11.2 Advisory path

If a host exposes only an advisory warning or HDM later derives an explicitly heuristic risk estimate:

```text
advisory risk
    -> warn player that current chat may be nearing a host limit
    -> recommend/offer continuation in a fresh chat
    -> if transfer is accepted/initiated, use normal handoff barrier
```

The warning should not state an exact number of messages/tokens/time remaining unless the host contract actually supplies such a guarantee.

## 11.3 No-warning path

If the product hard-stops without an actionable signal, no pre-destruction handoff is guaranteed.

This is expected degradation, not an architectural failure:

- recover newest actually durable closure;
- lose only state that genuinely remained unpublished and was destroyed;
- rely on Step 5.5 risk-control policy to bound ordinary exposure where execution opportunities permit.

---

# 12. Failure matrix

| Case | Required result |
|---|---|
| fresh host from durable state | bounded native hydration; no old-chat requirement |
| controlled handoff, no dirty/recovery delta | validate existing closure; no heartbeat write |
| controlled handoff, dirty gameplay state | scoped barrier -> required closure -> acknowledge only after actual durability |
| active Command/Resolution | preserve/resume same root execution identity |
| waiting Choice/Reaction | preserve same Continuation generation/offer; no regenerated choice |
| accepted Interaction not yet fully materialized | retain specific accepted evidence or materialize typed meaning before safe handoff |
| hidden partial model reasoning only | discard; not recovery state |
| reliable destruction signal | enter/offer controlled handoff according to host adapter/policy |
| advisory capacity signal | warn/recommend; no claim of guaranteed remaining capacity |
| heuristic false positive | unnecessary warning/early handoff at worst; no semantic corruption |
| heuristic false negative | host may hard-stop; unexpected-loss fallback |
| hard stop without warning | recover actual durable closure only |
| publication failure, host alive | handoff incomplete; retry/repair or abandon barrier |
| host dies during ambiguous write | new host resolves actual authoritative result under 5.6/5.7 |
| durable write succeeded but old acknowledgement lost | recover newer durable closure; no rollback because acknowledgement missing |
| intended/prepared write never authoritative | recover prior closure |
| old relinquished host reopened | rehydrate/resync before mutation |
| stale campaign state after another valid host advanced | refresh/revalidate; stale write cannot bypass revision checks |
| active live scope newer than campaign base | current live owner wins; no stale campaign fallback |
| non-destructive maintenance | ephemeral orientation allowed; no lifecycle publication solely because maintenance occurred |
| destructive maintenance | controlled handoff barrier |
| no dirty state at warning/handoff | no heartbeat/no-op publication |

---

# 13. Session metadata disposition

Persistent session records remain eligible for:

- coordination/navigation;
- player/PC/scene association hints;
- start/end/audit metadata;
- known/base frontier hints;
- optional support diagnostics.

They are not admitted as:

- world/execution/temporal current-state owners;
- write ACL authority;
- current host lease;
- recovery-cut authority;
- proof that old host is dead;
- proof that handoff completed safely;
- transcript authority.

Later machine realization may simplify or reshape session fields after 5.7/5.8, provided these authority limits remain intact.

---

# 14. Interaction with Step 5.5 periodic durability

Step 5.4 defines **event-driven lifecycle reasons** for a forced recovery-safe closure.

Step 5.5 separately owns ordinary durability exposure policy when no reliable destructive signal exists.

Carry-forward:

```text
reliable impending destruction
    -> 5.4 controlled handoff trigger

advisory capacity warning / future heuristic
    -> optional warning/proactive transfer

no usable warning + risk of abrupt expiry
    -> 5.5 maximum unpublished-SOFT exposure policy
```

No numerical duration is approved here.

The existing runtime hard-coded `one hour` rule is pre-5.5 provisional policy/debt. Step 5.5 must decide whether to retain, replace or remove that value.

The relevant durability metric should track exposure of gameplay-significant unpublished state, not merely elapsed time since any repository commit.

Clean state does not require heartbeat writes.

---

# 15. Explicit non-goals / rejected abstractions

Step 5.4 does not introduce:

- `runtime.handoff` class;
- `HandoffTicket` / transfer ledger;
- generic `resume_point` record;
- campaign-global host/session generation;
- campaign-global host lease;
- durable `RELINQUISHED` marker required for correctness;
- mandatory handoff checkpoint;
- serialized prompt/model memory/chain-of-thought;
- generic host TTL timer;
- exact remaining-message/token estimator;
- authoritative heuristic capacity prediction;
- background save daemon;
- universal recovery frontier.

Step 5.8 may still introduce a narrower native live ownership/fencing concept if that subsystem proves it necessary.

---

# 16. Carry-forward requirements

## Step 5.5 — SOFT / HARD / SAVE

Must define:

- exact state included in controlled-handoff durability closure;
- whether/how every established gameplay-significant SOFT mutation joins that closure;
- independent maximum age/exposure policy for unpublished gameplay-significant state;
- execution-opportunity/inactivity limitation;
- no-heartbeat behavior;
- resolution of stale hard-coded `one hour` runtime policy.

## Step 5.6 — campaign publication / crash consistency

Must make authoritative publication outcome determinable after failures around prepare/commit/ref update/acknowledgement and preserve the Step-5.4 “actual durability, not intent” rule.

## Step 5.7 — checkpoint / recovery

Must select/pin the newest compatible valid native recovery source set and hydrate without requiring handoff snapshot, old chat memory or authoritative session status.

## Step 5.8 — multiplayer / live ownership

Must define native scoped stale-host fencing/transfer/lease semantics only where actually required by live/shared ownership.

## Step 5.11 — transcript retention

Must retain exact literal utterance only while an actual live semantic/evidentiary dependency requires it; narrative smoothness alone does not justify universal transcript retention.

## Step 5.12 — host delivery

Must separately define generated/emitted/acknowledged player-facing output across crash/retry. Durable mechanics do not prove the player received narration.

## Host adapter / future realization

May support reliable or advisory host-capacity signals. Any heuristic estimator remains optional/advisory unless a future host contract explicitly strengthens its semantics.

---

# 17. Runtime alignment debt

Later integrated machine/runtime realization must review at minimum:

- `GAME/CORE/SESSION.md` — distinguish non-destructive maintenance frame from destructive handoff;
- `GAME/CORE/RUNTIME.md` — align context-loss/handoff semantics;
- `GAME/CORE/BOOTSTRAP_RUNTIME.md` — hydrate from current durable native evidence without old-chat authority;
- `GAME/CORE/DURABILITY_GUARD.md`, `SESSION.md`, `STORAGE.md`, `PERSISTENCE.md` — remove/replace unapproved hard-coded one-hour policy after 5.5;
- `GAME/SCHEMA/session.schema.yaml` — retain non-authoritative semantics or reshape if later recovery/live design justifies it;
- tests for controlled handoff, abrupt hard stop, capacity-warning false positives/negatives and stale-host recovery.

No runtime changes occur in Step 5.4 architecture closure itself.

---

# 18. Candidate fitness checks

The candidate passes by construction only if adversarial review confirms:

1. no controlled handoff can be acknowledged while promised gameplay-significant resume state exists only in the doomed host;
2. no unexpected-loss path invents unpublished state;
3. no generic handoff/session record becomes duplicate authority;
4. no clean handoff requires a heartbeat write;
5. no stale host can bypass current native authority/revision rules;
6. no hidden model reasoning becomes recovery state;
7. no host capacity warning/heuristic becomes correctness authority;
8. no missing host warning breaks recovery correctness;
9. multiplayer/live partitioning is not globally serialized;
10. later 5.5–5.8/5.11–5.12 owners remain intact.

---

# 19. Candidate status

Owner has approved the BARRIER-NATIVE direction and the host-capacity-exhaustion scope refinement.

This candidate is **not canonical** until adversarial review attacks the complete specification, including the new reliable/advisory/no-signal capacity split, and all significant findings are resolved.