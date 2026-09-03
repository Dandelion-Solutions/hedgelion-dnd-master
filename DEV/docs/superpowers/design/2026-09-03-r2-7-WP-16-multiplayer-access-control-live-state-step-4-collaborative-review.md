# R2.7 WP-16 — Multiplayer / Access Control / Live State — Step-4 Collaborative Review

Status: **STEP 4 COLLABORATIVE REVIEW — PASS / NO HUMAN DECISION REQUIRED**

Date: 2026-09-03

Reviewed Decision Brief:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-step-3-decision-brief.md`

Evidence basis remains the repaired Step-1 package plus Step-2 open-world manifest/evidence extraction.

---

## 1. Review objective

Challenge the selected Step-3 direction for ambiguity, owner leakage, machine-decision gaps, recovery/concurrency failure and accidental expansion into WP-17 or implementation planning.

Selected direction:

> **STABLE-PRINCIPAL AUTHORIZATION CHAIN / OWNER-TYPED IMMUTABLE LIVE CLAIMS / DOMAIN-SEPARATED CURRENTNESS / EXACT-SOURCE CAS / FORWARD NO-WINDOW AUTHORITY TRANSFER**

---

## 2. Identity / authorization review

### Question

Does the design prove a supported-host path from authenticated principal to application authorization without equating login with stable identity?

### Result

PASS.

The current supported Connector capability provides stable external user ID separately from mutable login. The Decision Brief uses that stable ID only as the external binding key and then requires current PLAYER membership, controlled-PC relation and operation-specific authorization.

Clarification retained for the candidate:

- a resolved external principal is not itself a campaign gameplay principal;
- a PLAYER is not itself permission for every operation;
- a controlled PC is not permission to mutate every owner reachable from that PC;
- repository capability and successful CAS remain infrastructure/concurrency evidence only.

No cached identity/auth bundle becomes a lease.

---

## 3. LIVE ownership review

### Question

Can `LIVE_STATE` still become a de facto semantic mega-owner because the physical fast path stores many native owners together?

### Result

PASS with explicit candidate requirement.

The candidate must state that LIVE physical packing may contain several native owner payloads only as a source partition. For every mutable fact, native semantic owner identity and claim membership remain recoverable/machine-decidable. A claim is not inferred from physical presence, scene participation, reference reachability, touched paths or participant membership.

No generic `scene owns all mutable state while live` law survives.

---

## 4. Currentness review

### Question

Can campaign HEAD, LIVE source HEAD and local HOT adopted state be collapsed into a single “latest” notion?

### Result

PASS.

The candidate must preserve explicit domain typing:

- campaign publication currentness;
- selected LIVE source currentness;
- process-local HOT currentness/adoption.

Cross-domain relations such as `based_on`, `selected_by`, `absorbed_from` or `adopted_from` are owner-specific. Numeric revision, SHA lexical order, timestamp or local adoption order cannot compare those domains generically.

---

## 5. Revocation/deactivation review

### Question

Does the proposed close/freeze -> campaign transition actually eliminate the stale writer window?

### Result

PASS with one precision requirement.

The campaign transition must establish every same-domain fact whose separation could temporarily reauthorize the removed principal for the transferred scope, including as applicable:

- final absorption/survivor state;
- PLAYER deactivation/current membership change;
- live route release/replacement;
- completeness-critical derivative authorization/claim-routing/index updates.

A stale process that prepared from older campaign membership/currentness must fail current authorization/precondition checks before successful publication. Exact source CAS alone does not provide this guarantee.

Already accepted LIVE work that wins before close remains real. The design cannot revoke it retroactively.

---

## 6. CLOSED_UNABSORBED review

### Question

Should a closed selected LIVE source allow read fallback to campaign to reduce stalls?

### Result

NO; current Step-5.8 law is correct.

`CLOSED_UNABSORBED` remains current truth for the claims, with no ordinary writers. Campaign fallback would discard accepted live state and create current-truth ambiguity. OOC/nondependent work may continue; mutation waits for valid forward absorption/recovery.

---

## 7. Multi-LIVE review

### Question

Can cross-scope transfer avoid distributed transactions without exposing partial fiction?

### Result

PASS.

Each native source can close/freeze independently. Accepted root execution may remain unresolved/recoverable across prerequisite freezes. Only the owner-defined campaign transfer establishes the intended cross-scope fictional result. A crash mid-freeze resumes forward; no source is reopened and no global rollback is attempted.

The candidate must avoid using technical freeze completion order as fictional chronology.

---

## 8. Accepted execution / RNG review

### Question

Does conflict/revocation/source movement permit re-resolution or reroll?

### Result

NO.

Accepted RuntimeCommand/Resolution/Continuation/fixed RNG/idempotency evidence remain authoritative for the already accepted execution. A stale prospective transition may be discarded before acceptance; accepted work resumes under the pinned execution contract. A changed current state may invalidate an unaccepted prospective consequence without changing already accepted RNG semantics except where the original experiment itself is no longer the same admitted experiment under Step-3 rules.

---

## 9. Information boundary review

### Question

Can LIVE per-PC observable/known fields remain for fast sharing?

### Result

YES only as owner-constrained evidence/projection.

They may support bounded current cross-session operation, but durable fictional knowledge still normalizes to `world.knowledge` when required and human exposure to `runtime.disclosure` when required. Physical LIVE readability, participant membership, observable-event presence or one `known_by_pc_ids` list cannot collapse those responsibilities.

---

## 10. Card / manifest / session / cache review

### Question

Can these surfaces be used to reduce authorization lookups?

### Result

Only as hints/observations with owner-defined freshness. They may route or avoid redundant reads where currentness is already proven, but they cannot independently grant authority.

- CAMPAIGN_CARD: menu/display/access hint projection.
- MANIFEST: declared campaign configuration fields only.
- session: coordination/navigation observations.
- PLAYER_INDEX / other indexes: discovery only.
- cached HEAD/live/HOT state: performance state only.

A protected mutation still requires a current enough authorization/currentness basis under the owning protocol.

---

## 11. Agency / WP-17 boundary review

### Question

Does WP-16 accidentally define behavior for absent players or collaboration ordering?

### Result

NO.

WP-16 may decide whether a principal is currently authorized and which native source owns mutation. It does not decide whether an unresolved procedure may proceed without a participant, collect future contributions, time out, delegate voluntary action or synthesize a choice. Those remain native procedure/rules and WP-17 collaboration concerns.

---

## 12. Performance review

The selected direction remains compatible with bounded ordinary play:

```text
current trusted principal evidence
+ bounded PLAYER binding/control lookup
+ bounded operation-specific authorization
+ bounded WriteAuthorityLookup(target)
+ one exact-source LIVE ref/currentness probe when live-sensitive
+ local/native transition
+ one exact-source publication edge per native durability edge
```

No campaign-wide owner scan, all-live scan, global claims graph, distributed transaction, heartbeat/lease loop or per-turn broad history read is required.

Exact call counts are implementation/measurement questions for later planning/WP-24.

---

## 13. Review conclusion

No competing architecture remains viable under accepted owner law. All review clarifications are mechanically derivable and must be incorporated into the Step-5 candidate.

```text
STEP_4_RESULT: PASS
BLOCKING: 0
SIGNIFICANT_UNRESOLVED: 0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
STEP_5_READY: YES
```
