# Step 5.4 — Host Lifecycle & Session Handoff — Decision Brief

Status: **OWNER APPROVED — CANDIDATE/CANONICALIZATION AUTHORIZED**

Date: 2026-08-20

Owner decision recorded: 2026-08-20

Inputs:

- `2026-08-20-step-5-4-host-lifecycle-session-handoff-task-brief.md`
- `2026-08-20-step-5-4-host-lifecycle-session-handoff-research-draft.md`
- `2026-08-20-step-5-4-host-lifecycle-session-handoff-analytical-challenge.md`
- Step-5.2 canonical v2
- Step-5.3 canonical A-NARROW specification
- Step-3 execution contract
- current runtime lifecycle/persistence/session/live contracts

---

# 1. Owner decision

Approved architecture direction:

> **BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF**

The owner also explicitly added host conversation/message/context capacity exhaustion to Step-5.4 scope under the following constraint:

> HDM currently has no trustworthy remaining-capacity signal that may be treated as architecture authority. Future capacity estimation may exist only as an advisory heuristic unless a host supplies a reliable contract.

This decision authorizes candidate-spec formalization, adversarial review and canonical closure of Step 5.4. It does not authorize implementation or Step-5.5 design.

---

# 2. Approved architecture

HDM does not add a durable handoff snapshot, generic transfer ticket, campaign-global host lease, or authoritative session record.

Instead:

```text
ATTACHED HOST
    -> explicit handoff or reliable imminent destructive-context signal
    -> SCOPED HANDOFF BARRIER
       freeze further acknowledged mutation in affected ownership scope
       materialize promised unresolved semantics into existing native owners
       establish a durable Step-5.2/5.3 Resumable Runtime Closure
    -> RECOVERY_SAFE_HANDOFF acknowledged
    -> old host relinquishes pre-handoff hot state

UNEXPECTED LOSS / INCOMPLETE HANDOFF / UNWARNED HOST HARD STOP
    -> no retroactive finalization
    -> recover newest actually durable compatible native source set
```

A fresh host resumes through normal native hydration. It does not consume a handoff snapshot.

---

# 3. Core semantics

## 3.1 Host lifecycle is separate from gameplay lifecycle

Chat/context destruction does not itself:

- pause/end the campaign;
- advance fictional time;
- close a Procedure;
- cancel accepted execution;
- create NPC/world actions.

## 3.2 Controlled handoff is stronger than crash recovery

A controlled recovery-safe handoff may be acknowledged only when every gameplay-significant state promised across that handoff is actually durably recoverable.

Step 5.5 will define the exact durability class/dirty closure. Step 5.4 defines the lifecycle guarantee.

## 3.3 Barrier requires scoped quiescence

Once the handoff closure is frozen, the old host may not acknowledge additional gameplay mutation in that same scope until either:

- the handoff succeeds and the host relinquishes; or
- the handoff fails/is abandoned and normal attached operation resumes.

This is not a campaign-global lock. Independent scopes may remain independent.

## 3.4 Clean handoff does not require a heartbeat write

If the complete promised resume state is already durably recoverable, the handoff may succeed without creating a commit merely to record that a handoff occurred.

## 3.5 Failure does not become success by intent

If publication fails while the old host survives, handoff remains incomplete.

If the host is destroyed anyway, recovery uses unexpected/degraded-loss semantics and returns to the newest actual durable compatible closure.

If a write may have succeeded but acknowledgement was lost, the fresh host determines the actual durable state through later 5.6/5.7 recovery rules; it does not trust remembered intent.

---

# 4. Semantic resume ownership

No generic `resume_point` record is introduced.

Use existing owners:

| Situation | Resume owner/evidence |
|---|---|
| current world/scene state | native world or current live owner |
| accepted player input before command | `Interaction` / `IntentPlan` when handoff promises that point |
| accepted root execution | `RuntimeCommand` |
| active/suspended Activity | `Resolution` / `Continuation` |
| Procedure between commands | `runtime.procedure` |
| Choice/Reaction | same Continuation generation/offer |
| armed temporal work | native temporal source + typed routing |
| accepted temporal firing | Step-5.3 source/execution closure |
| exact wording only needed for presentation | not a recovery prerequisite |
| exact wording genuinely preserves still-unmaterialized accepted meaning | specific Interaction/message evidence until typed meaning is materialized |

Partial model reasoning / chain-of-thought is never a resume owner.

---

# 5. Session metadata

Persistent `session` records remain coordination/recovery projection and optional observability metadata.

They do not grant:

- write authority;
- current world/execution authority;
- live-epoch authority;
- definitive recovery frontier;
- stale-host fencing by status alone.

A stale/reopened host must revalidate current native authority/revisions before mutation. No campaign-global one-host lease is introduced.

---

# 6. Maintenance distinction

Two cases become explicit:

```text
NON-DESTRUCTIVE MAINTENANCE
    same host/context survives
    -> ephemeral orientation/continuation frame may help presentation

DESTRUCTIVE MAINTENANCE
    host/context will be lost
    -> ordinary controlled handoff barrier applies
```

Current runtime wording that relies only on a current-chat maintenance continuation frame is therefore insufficient for destructive maintenance and becomes later realization debt.

---

# 7. Host-capacity and context-expiry signal contract

Step 5.4 distinguishes capability from guarantee:

```text
RELIABLE IMPENDING-DESTRUCTION SIGNAL
    host contract says current context/chat will become unusable
    -> controlled handoff barrier trigger

ADVISORY NEAR-CAPACITY SIGNAL
    host warns that exhaustion may be approaching
    but remaining messages/tokens/time are not guaranteed
    -> player-facing warning/recommendation MAY be emitted
    -> proactive handoff MAY be attempted
    -> correctness does not depend on completion before cutoff

NO USABLE SIGNAL / HARD STOP
    host becomes unwritable without actionable warning
    -> unexpected-loss semantics
```

The architecture does **not** currently assume access to a reliable remaining-message, remaining-token, remaining-context-capacity or time-to-hard-stop metric.

Message count, approximate token count, chat age, remembered product limits and inferred capacity are not authoritative remaining-capacity evidence.

A future heuristic may estimate risk and issue advisory warnings, but:

- it must be explicitly non-authoritative;
- false positives may cause only unnecessary early handoff suggestions;
- false negatives must degrade safely to unexpected-loss recovery;
- it must not redefine what state is durable or recoverable;
- it must not be required for correctness.

No numerical capacity threshold or prediction algorithm is approved by Step 5.4.

---

# 8. Context-expiry and periodic safety flush boundary

The owner direction is incorporated as follows:

```text
reliable current context-expiry/destruction signal
    -> Step 5.4 handoff barrier trigger

advisory near-capacity signal
    -> optional warning/proactive handoff recommendation

generic risk that context may expire without usable warning
    -> Step 5.5 durability-risk / max unpublished-SOFT exposure policy
```

No Step-5.4 timer value is approved.

The existing runtime `one hour` dirty ceiling is **not** treated as canonical architecture. It is provisional/stale policy to be resolved by Step 5.5.

The semantic risk metric should concern age/exposure of gameplay-significant unpublished state, not merely time since any Git commit. Clean state must not create heartbeat writes.

---

# 9. Alternatives considered

## A — BARRIER-NATIVE — APPROVED

Reuse native owners; lifecycle adds a scoped barrier and acknowledgement precondition.

**Pros:** minimal state, no duplicate authority, no clean heartbeat, domain-partitionable, works with current Step-5.2/5.3 model.

**Cons:** temporarily quiesces affected mutation scope; later slices must implement physical durability/recovery mechanics.

## B — Durable handoff ticket

Persist source/target session, recovery refs, status and resume summary.

**Pros:** explicit transfer observability.

**Rejected because:** duplicates recovery/session/checkpoint concerns, risks becoming universal recovery-cut authority, creates clean handoff writes, requires retention/GC/repair, and does not solve live native ownership.

## C — Authoritative session epoch/lease

Make newest/current session generation the write-fencing authority.

**Pros:** explicit stale-chat rejection.

**Rejected because:** promotes coordination metadata into gameplay authority, conflicts with legitimate concurrent multiplayer/independent scopes, requires liveness/lease recovery, and duplicates native revision/authorization/live fencing.

---

# 10. Confidence and reversibility

Recommendation/decision confidence: **HIGH**.

BARRIER-NATIVE does not prevent later addition of a scoped native lease/token if Step 5.8 proves one is required for a specific live ownership domain.

It intentionally avoids making that future possibility a campaign-global abstraction now.

A later optional audit record can also be added without changing handoff correctness if operational observability proves useful.

Likewise, future host-capacity telemetry or a predictive heuristic may be added as a warning/trigger adapter without changing recovery correctness, because the base architecture already supports the no-warning hard-stop case.

---

# 11. Carry-forward

Candidate/canonical specification must emit requirements to:

- **5.5** — define handoff durability class/completeness and independent maximum unpublished-SOFT exposure policy; no numerical value pre-approved;
- **5.6** — make authoritative publication outcome determinable across crash/ambiguous acknowledgement;
- **5.7** — hydrate newest compatible valid native source set without handoff snapshot;
- **5.8** — define any required live/scoped ownership fencing/transfer;
- **5.11** — retain exact transcript only for genuine live semantic dependency;
- **5.12** — separately define generated/emitted/acknowledged player-facing delivery.

Host-capacity warning heuristics, if ever implemented, must remain capability-dependent/advisory unless a future host contract provides stronger reliable semantics.

No Step 5.5 design begins as part of this decision.

---

# 12. Decision record

```text
BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF   [APPROVED]

HOST CAPACITY EXHAUSTION                         [IN SCOPE]
RELIABLE REMAINING-CAPACITY METRIC               [NOT ASSUMED]
FUTURE CAPACITY HEURISTIC                         [ADVISORY ONLY / DEFERRED]
```

Proceed to candidate specification, adversarial review and canonical closure of Step 5.4. Do not implement runtime changes and do not begin Step 5.5 until Step 5.4 closes.