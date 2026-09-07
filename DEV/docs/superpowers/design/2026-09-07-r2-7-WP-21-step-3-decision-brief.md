# R2.7 WP-21 Step 3 — Decision Brief

Status: **STEP 3 COMPLETE — DECISION READY**

Date: 2026-09-07

Domain: **Diagnostics, observability, cleanup and retirement**

Inputs:

- Senior-PASSed Step-1 package;
- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-21-step-2-research-architecture-draft.md`;
- current cleanup, persistence, recovery, LIVE, access-control, disclosure, Story/planning and migration owners;
- fixed PO-006 branch/ref deletion prohibition.

---

## 1. Decision

WP-21 must decide whether diagnostics/cleanup need a new shared subsystem or whether existing owner semantics can be composed into one implementation-facing contract that tells later realization how to obtain bounded diagnostics, prove retirement eligibility, rebuild derivative state and enroll post-Step-5.13 families.

## 2. Non-negotiable requirements

1. diagnostic evidence never becomes gameplay/recovery/publication authority;
2. hidden CoT, hidden instructions, credentials and unavailable host context are not required observability state;
3. operation routing is separate from principal authorization;
4. human-visible diagnostics remain recipient/information-eligibility filtered;
5. native owner lifecycle/currentness controls cleanup;
6. terminality, age or generic reachability is never sufficient removal authority;
7. uncertain cleanup eligibility fails safe to `RETAIN`;
8. survivor/replacement evidence must exist before destructive loss when continuity requires it;
9. derived/planning/cache state cannot reconstruct missing canon/native authority;
10. Git branches/refs are retired logically only and are never deleted/probed for deletion by HDM/LLM automation;
11. later WP-17/WP-18 machine debt remains deferred rather than being fabricated as implemented;
12. no generic support/admin principal or universal GC/observability service is invented.

## 3. Alternatives

### A — Centralized observability + GC/support service

A shared telemetry store, universal liveness graph, cleanup queue and privileged support role.

**Reject.** Adds new authority/currentness/disclosure surfaces without a current consumer requirement, risks circular recovery authority and duplicates existing owners.

### B — Repository reachability/age-based cleanup

Use index/ref reachability, age or repository topology as the principal deletion criterion.

**Reject.** Repository topology is not semantic liveness; sparse consumers and native lifecycle/protection rules make this unsafe, and Git ref deletion is forbidden.

### C — Owner-composed diagnostics + owner-gated retirement + explicit late-family enrollment

Use existing access/disclosure/currentness/lifecycle owners; define bounded diagnostic and retirement evidence composition; classify native/derived/planning/cache/residue state; require new families to state cleanup semantics before automation relies on them.

**Recommend.** Closes the cross-owner implementation contract without adding a second authority system.

### D — No WP-21 composition owner

Leave all laws distributed among Step 5.13, maintenance/access/disclosure and later WP specs.

**Reject.** Native owners are sufficient individually, but future realization would have to rediscover their composition and could incorrectly infer automatic GC coverage or diagnostic privilege.

## 4. Recommendation

Select **Alternative C**.

Architecture shape:

```text
concrete maintenance question
+ current principal/owner authorization
+ owner-qualified currentness/evidence
+ recipient eligibility
-> bounded diagnostic projection

candidate representation
+ native lifecycle/currentness
+ blocker/protection closure
+ required survivor/rebuild evidence
-> RETAIN | LOGICAL_RETIRE | COMPACT_OR_REPLACE |
   PHYSICAL_REMOVE_IF_NATIVE_OWNER_ALLOWS | REBUILD_OR_RECOMPUTE
```

Git branches/refs are globally excluded from physical-remove mode.

## 5. Strongest weakness

The composition contract spans many owners and can be over-read as a universal runtime schema or global cleanup registry. The mitigation is explicit non-ownership: Diagnostic Evidence Projection and Retirement Evidence Set are conceptual envelopes, not required persisted families, queues or services. Native owners continue to define lifecycle, currentness, disclosure and concrete machine representation.

## 6. Remaining uncertainty

Only realization details remain deferred:

- exact maintenance dispatcher/result enums;
- exact diagnostic serialization;
- family-specific cleanup tooling;
- WP-17 obligation/PLAYER-route schemas;
- WP-18 retained-horizon schemas;
- executable authorization/redaction/cleanup tests when implementation is authorized.

These do not alter the architecture choice.

## 7. Human / PO decision

Current accepted owners mechanically settle the alternatives. No material product semantic, privilege expansion, retention promise or risk acceptance remains unresolved.

```text
SELECTED_ALTERNATIVE: C
RECOMMENDATION_CONFIDENCE: HIGH
HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
NEEDS_PO: NONE
STEP_4_READY: YES
```
