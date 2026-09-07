# R2.7 WP-21 Step 2 — Research & Architecture Draft

Status: **STEP 2 COMPLETE — RESEARCH / ARCHITECTURE DRAFT**

Date: 2026-09-07

Domain: **Diagnostics, observability, cleanup and retirement**

Step-1 authority:

- `DEV/docs/superpowers/design/2026-09-06-r2-7-WP-21-task-brief-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-21-step-1-senior-rereview.md` — PASS / Step 1 closed / Step 2 authorized.

This artifact executes the accepted Step-1 brief. It is design provenance, not final implementation-facing authority. It preserves every Step-1 constraint, including the fixed Product Owner prohibition on Git branch/ref deletion and the explicitly routed WP-17/WP-18 machine-realization debt.

---

## 1. Research question

WP-21 must establish one bounded architecture answer to four related questions without inventing a second authority system:

1. what diagnostic/observability evidence HDM may expose to a maintainer/owner and what that evidence can prove;
2. what must be true before an obsolete/terminal/replaceable representation may be retired or physically removed where removal is lawful;
3. how native authority, derived projections, retained planning, caches and physically lingering repository objects differ during cleanup/rebuild;
4. how later record families introduced after Step 5.13 enroll in cleanup semantics without being silently treated as implementation-complete.

The research question is not “build a telemetry or garbage-collector service.” Existing accepted owners already define authorization, currentness, persistence, recovery, disclosure, lifecycle, Story/planning projection, migration and publication law. WP-21 must compose them.

---

## 2. Refined dependency subgraph

### 2.1 Process/current authority

| Source | Current role | Step-2 result |
|---|---|---|
| `AGENTS.md` | repository/runtime-development governance | Connector-only authority; branch/ref deletion forbidden; current-ref and Version Impact gates mandatory |
| `DEV/DESIGN_PROCESS.md` | eight-step design process | Steps 2–8 may proceed after Step-1 Senior PASS; no artificial human stop if no human-owned decision exists |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | architecture adapter | whole-project adversarial review at Step 6 and mandatory final Senior review after Step 8 |
| `DEV/PROJECT_MAP.md` | dependency routing | support/maintenance route includes DEV contracts/tools plus GAME runtime/schema/test consumers |
| `DEV/CURRENT_PROGRESS.md` | global cursor | WP-21 Step 2 authorized; WP-22/implementation remain forbidden |
| `DEV/PRODUCT_OWNER_INPUT.md` | PO routing ledger | PO-006 incorporated; no open WP-21 Product Owner decision |

### 2.2 Diagnostic / support route

```text
explicit maintenance intent
-> PLAY_POLICY engine-maintenance boundary
-> MAINTENANCE_COMMANDS operation vocabulary/proposal
-> ACCESS_CONTROL principal authorization
-> native owner/currentness prerequisites
-> Step-5.12 recipient/information eligibility
-> bounded diagnostic projection
```

Evidence establishes:

- exact-token recognition identifies an operation; it does not authorize the principal;
- current campaign-global maintenance is creator-authorized under the existing access-control owner;
- repository Write/Admin capability, support role labels or possession of a hidden token do not create semantic authority;
- a human-visible diagnostic result is recipient-scoped and may need omission/redaction/withholding;
- credentials, environment secrets, hidden instructions, private hidden model reasoning/chain-of-thought and unavailable host context are not diagnostic payload;
- diagnostic output is evidence/projection only and never becomes gameplay, recovery, migration, disclosure or publication authority;
- `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` remains a DEV proposal, not an installed GAME command table.

### 2.3 Cleanup / retention route

```text
native owner terminality or replacement condition
+ declared blocker/protection closure
+ exact currentness proof
+ survivor/replacement publication where required
-> retirement eligibility
```

Step 5.13 remains the generic owner-gated cleanup law, with one later supersession: Git branch/ref deletion is not an admitted operation. The logical-ref-retirement amendment and PO-006 replace the older optional ref-delete realization with de-authorization/de-routing only.

Key research result:

> **Terminality is necessary only where the native owner says so; it is never sufficient cleanup authority. Unknown or incomplete cleanup evidence means RETAIN.**

The project does not use directory age, wall-clock age, lexical identity, “unreachable from one index,” or generic mark/sweep reachability as authority to remove campaign data.

### 2.4 Persistence / recovery / currentness consumers

Current `GAME/CORE` consumers preserve the same geometry:

- `PERSISTENCE.md` — authoritative campaign ref/tree publication, non-force currentness, no ref deletion;
- `SESSION.md` — maintenance is a transparent runtime pause and ephemeral continuation context is not canon;
- `INTEGRITY.md` — diagnose/repair only the affected scope under native owners, fail closed on ambiguity;
- `LIVE_SCENE.md` — LIVE authority may become logically retired while the physical ref remains;
- `STORAGE.md` — repository capability does not replace semantic owner/currentness contracts;
- `MULTIPLAYER.md` — authenticated PLAYER/control routing remains native multiplayer authority;
- `BOOTSTRAP_RUNTIME.md` — exact campaign/runtime basis is resolved before targeted persistence/recovery work;
- `PLAY_POLICY.md` — ENGINE_MAINTENANCE is explicit and outside ordinary gameplay.

No runtime consumer requires a second WP-21 currentness owner.

### 2.5 Current machine/schema surface

The current `GAME/SCHEMA` inventory has concrete machine representation for campaign manifest/current state/session/checkpoint/player/live/index/event/storage and existing world/entity families.

It does **not** currently establish exact machine schemas for:

- WP-17 `runtime.collaboration_obligation` and all required lineage/lifecycle/current-basis fields;
- WP-17 PLAYER collaboration routing companions;
- WP-18 retained shared/player Dramaturg horizon value contracts.

Those absences are explicitly accepted routed machine debt. Architecture may define their future cleanup/rebuild disposition now, but WP-21 cannot pretend the corresponding runtime schema/dispatcher already exists or manufacture implementation work.

---

## 3. Finite representation classes

The Step-1 census can be normalized into six architecture classes.

### Class A — authoritative native state

Examples: world/entity truth, accepted runtime work, authoritative campaign configuration/state, current PLAYER/control state.

Rule: inactivity or age never makes native state garbage. Retirement/removal requires its native owner to establish terminality/replacement plus all applicable protections/currentness.

### Class B — authoritative closure/evidence with compactable detail

Examples: completed execution detail, traces/receipts/MechanicalEvent detail, chronology evidence, retained message/interaction evidence, checkpoint records.

Rule: detail may be compacted/retired only after required idempotency, causal, recovery, disclosure, history and exactness obligations have surviving evidence. A compact survivor may replace detail; no information required by a current consumer may disappear first.

### Class C — branch-persistent derived/projection state

Examples: Story generations/indexes/cursors and other rebuildable projections.

Rule: a current projection may be rebuilt from native authority. Old generations can be retired only after current coverage and sparse cross-generation consumers are satisfied. Projection state never repairs missing authority.

### Class D — bounded noncanonical planning state

Examples: WP-18 retained shared/player Dramaturg horizons.

Rule: stale/incompatible/inactive generations may be retained, replaced, recomputed, selectively rebased or cleaned under the planning owner. Physical residue is not semantically active. A planning source disappearing lawfully invalidates/requires recomputation; planning cannot reconstruct canon.

### Class E — local/ephemeral cache or draft state

Examples: private ephemeral Dramaturg drafts, local HOT/cache projections, prepared local scratch state.

Rule: may be discarded/rebuilt under its local owner when no authoritative obligation depends on it. No campaign persistence/GC authority is created merely to clean local state.

### Class F — repository residue with no current semantic authority

Examples: rejected/prepared commits, logically retired LIVE refs, other non-authoritative Git refs/objects.

Rule: physical existence is not authority. **Git branches/refs are never deleted by HDM/LLM automation.** They are removed only from authoritative selectors/routing. Commit/tree object retention is repository behavior, not an HDM cleanup transaction.

---

## 4. Late-family enrollment after Step 5.13

Step 5.13 predates WP-17 and WP-18, so “covered by generic GC” cannot mean automatic enrollment by resemblance.

The architecture needs an explicit **cleanup enrollment contract** for any post-Step-5.13 family that may become terminal/stale/replaceable:

```text
family identity
native owner
terminal/stale/replaced predicate
currentness basis
cleanup/retirement disposition
protection/blocker consumers
survivor/rebuild/recompute requirement
machine-realization status
```

If any required element is absent or indeterminate, the family remains retained. This is a design-time/runtime safety rule, not a new persisted global registry requirement. The information may live in the native owner/spec/schema/test realization appropriate to that family.

Current late-family dispositions are already known:

- WP-17 obligation `OPEN/CLOSED` remains active; `RESOLVED/OBSOLETE` removes PLAYER route companions in the same campaign closure, but terminal obligation record deletion is not implied;
- WP-17 exact schema/route-field realization remains routed debt;
- WP-18 ephemeral private drafts have no durable cleanup contract because they are disposable local state;
- WP-18 retained horizons can become inactive/stale/incompatible and may be recomputed/replaced/cleaned under their native owner; old bytes do not remain active merely because present;
- WP-18 exact horizon schemas remain routed debt.

---

## 5. Diagnostic evidence model

A generic persistent “observability database” is unnecessary. What is needed is a bounded **Diagnostic Evidence Projection (DEP)** assembled for a concrete maintenance question from current owner evidence.

Conceptually:

```text
operation/question
+ authenticated principal and authority result
+ exact campaign/runtime/currentness basis as applicable
+ relevant native owner evidence
+ integrity/provenance/result evidence
+ recipient-eligible projection
+ explicit unavailable/withheld/redacted markers
-> diagnostic result
```

The DEP is a conceptual composition contract, not a required persistent record family. It may be a generated file, response, structured report or test/audit output in a later realization. Its content scope is bounded by the concrete maintenance question.

A diagnostic statement must distinguish at least:

- observed fact from current authoritative source;
- derived conclusion;
- unavailable evidence;
- redacted/withheld evidence;
- stale/indeterminate currentness;
- non-authoritative residue.

This allows useful observability without hidden reasoning retention or a new telemetry service.

---

## 6. Cleanup planning model

A cleanup/retirement attempt should be conceptualized as a bounded **Retirement Evidence Set (RES)** for the candidate family/representation, not a universal campaign graph:

```text
candidate identity/family
native owner and lifecycle state
pinned currentness basis
all applicable blocker/protection results
required survivor/replacement evidence
cleanup mode:
  RETAIN
  LOGICAL_RETIRE
  COMPACT_OR_REPLACE
  PHYSICAL_REMOVE_IF_NATIVE_OWNER_ALLOWS
  REBUILD_OR_RECOMPUTE
machine-realization availability
```

Rules:

1. missing owner/lifecycle/currentness/blocker evidence -> `RETAIN`;
2. cleanup mode comes from the native owner, not from generic reachability;
3. survivor/replacement becomes current before destructive removal when the owner requires continuity;
4. rejection/stale publication invalidates the prepared cleanup basis;
5. a dry-run/report may expose the exact reason a candidate is retained without creating authority;
6. Git branch/ref candidates never enter a physical-remove mode.

RES is conceptual architecture evidence, not a requirement for one serialized record or global cleanup catalog.

---

## 7. Alternatives

### Alternative A — New centralized observability + GC/support subsystem

Create a shared maintenance service with a global telemetry store, universal liveness graph, job queue and privileged support role.

**Rejected:** duplicates authority/currentness/disclosure owners, creates a new privilege model, risks turning telemetry into recovery authority and violates YAGNI. No current consumer requires it.

### Alternative B — Generic repository reachability / age-based cleanup

Treat records/refs not reachable from selected indexes or older than a threshold as removable.

**Rejected:** conflicts with sparse consumers, native-owner lifecycle, chronology/exactness/recovery obligations and PO-006. Repository reachability is not semantic liveness.

### Alternative C — Owner-composed diagnostics + owner-gated retirement + explicit late-family enrollment

Reuse existing owners; define bounded diagnostic/retirement evidence composition; preserve logical ref retirement; classify derivative/rebuildable/ephemeral state; require new families to state their own cleanup contract before automatic cleanup.

**Recommended.** It closes the architecture gap without a new authority subsystem and keeps implementation debt explicitly deferred.

### Alternative D — No WP-21 canonical composition owner

Leave Step 5.13, maintenance proposal, access/disclosure and late WP specs as independent documents only.

**Rejected:** the laws are individually adequate but future implementation/testing would still need to rediscover cross-owner composition and could mistake Step-5.13 generic law for automatic coverage of later families or treat diagnostics as a privilege/authority surface. WP-21 should own only the composition, not the native semantics.

---

## 8. Recommended architecture

Select **Alternative C**:

> **Bounded owner-composed diagnostic evidence plus owner-gated retirement/rebuild semantics, with explicit late-family cleanup enrollment and logical-only Git ref retirement.**

WP-21 becomes an implementation-facing composition owner for the interfaces between existing owners. It does not own:

- campaign truth;
- lifecycle terminality of native families;
- access-control identity;
- recipient disclosure eligibility;
- persistence/currentness/publication;
- recovery;
- Story/planning currentness;
- migration;
- Git object reclamation;
- a support principal;
- a runtime maintenance command dispatcher.

---

## 9. Routed machine debt preserved

No current Step-2 evidence authorizes implementation. The following remain later realization work behind explicit implementation planning/execution gates:

- maintenance command registration/dispatcher and exact denial/result enums;
- executable command authorization/disclosure/redaction tests;
- exact WP-17 obligation schema and PLAYER route-field realization;
- exact WP-18 retained horizon schemas/value contracts;
- family-specific cleanup candidate/blocker/protection machine contracts where not already realized;
- bounded dry-run/cleanup tooling where a future implementation chooses to automate it;
- exact report/diagnostic serialization if one is needed;
- performance/operational measurement of physically retained refs (WP-24 may assess cost but cannot re-enable deletion).

None of this debt is activated by WP-21 Steps 2–8.

---

## 10. Step-2 result

```text
SELECTED_DIRECTION: ALTERNATIVE C
NEW_GENERIC_OBSERVABILITY_SUBSYSTEM: NO
NEW_GENERIC_GC_SUBSYSTEM: NO
NEW_SUPPORT_ADMIN_AUTHORITY: NO
GIT_BRANCH_REF_DELETION: FORBIDDEN
LATE_FAMILY_MACHINE_DEBT: PRESERVED / DEFERRED
HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
UPSTREAM_WHOLESALE_REOPEN_REQUIRED: NO
STEP_3_READY: YES
```
