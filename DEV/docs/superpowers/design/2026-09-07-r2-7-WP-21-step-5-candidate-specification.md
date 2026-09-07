# R2.7 WP-21 Step 5 — Candidate Specification

Status: **STEP 5 COMPLETE — CANDIDATE FOR WHOLE-PROJECT ADVERSARIAL REVIEW**

Date: 2026-09-07

Domain: **Diagnostics, observability, cleanup and retirement**

Selected architecture: **bounded owner-composed diagnostics + owner-gated retirement/rebuild + explicit late-family cleanup enrollment + logical-only Git ref retirement**.

This candidate composes existing owners. It does not replace native lifecycle/currentness, access, disclosure, persistence, recovery, LIVE, Story/planning, migration or repository policy.

---

## 1. Scope and authority

### WP21-L01 — Composition owner only

WP-21 owns the composition contract for diagnostics/observability and retirement/rebuild across existing HDM owners. It does not become the semantic owner of campaign truth, native lifecycle, recovery, access control, human disclosure, Story/planning currentness, migration or Git repository object lifetime.

### WP21-L02 — Maintenance remains outside ordinary gameplay

Maintenance/diagnostic work is entered only through the existing explicit maintenance/development boundary. A maintenance request does not by itself create gameplay chronology, a gameplay Interaction or fictional time advancement.

---

## 2. Diagnostic Evidence Projection

### WP21-L03 — Concrete-question boundedness

Diagnostics are built for one concrete maintenance/support question from the minimum relevant current owner evidence. No package/campaign-wide telemetry scan is implied merely because diagnostics are requested.

### WP21-L04 — Owner-qualified currentness

Every material diagnostic claim identifies the applicable currentness basis of its native owner/domain. Evidence from independently writable domains is not collapsed into a universal snapshot, revision or frontier.

### WP21-L05 — Routing is not authorization

A maintenance token, phrase, command identity or tool route identifies the requested operation only. It does not authorize a principal, grant gameplay authority, widen disclosure or bypass another native owner.

### WP21-L06 — Campaign-global maintenance uses existing creator authorization

Where an operation is campaign-global maintenance under current access-control law, resolve current authenticated principal and campaign creator and require the existing creator/owner authorization. Repository permission, storage ownership, framework-maintainer status, PLAYER binding, support role labels or knowledge of an undocumented command do not independently grant that authority.

### WP21-L07 — Authorization does not widen disclosure

Even an authorized maintenance principal receives only material eligible for that intended recipient under the current disclosure/information owner. Creator authorization is not a blanket permission to expose player-local/private/hidden campaign information.

When eligible output cannot safely be separated from ineligible data, omit/redact/withhold it and report the diagnostic limitation rather than leaking the underlying material.

### WP21-L08 — Forbidden diagnostic payload

Diagnostic/export output never requires or intentionally exposes credentials, environment-variable secrets, hidden instructions, chain-of-thought/private hidden model reasoning, unavailable/compacted host context or other host/tool secrets.

### WP21-L09 — Diagnostic epistemic status

A diagnostic result distinguishes, when material:

```text
OBSERVED_AUTHORITY
DERIVED_CONCLUSION
UNAVAILABLE
WITHHELD_OR_REDACTED
STALE_OR_INDETERMINATE
NON_AUTHORITATIVE_RESIDUE
```

Exact serialization is deferred.

### WP21-L10 — Diagnostic output is not authority

A generated report/file/response/dry run is a diagnostic projection. It is not gameplay truth, recovery authority, disclosure authority, migration authority, currentness owner, publication authority or a replacement for the records it summarizes.

---

## 3. Retirement Evidence Set

### WP21-L11 — Native owner controls retirement eligibility

A candidate representation may be retired, compacted, replaced, rebuilt or physically removed only according to the native owner's lifecycle/replacement semantics plus all applicable currentness and protection/blocker requirements.

### WP21-L12 — Terminality is not removal authority

A terminal, resolved, obsolete, inactive, stale, old, unindexed or apparently unreachable state is not by itself authorization for physical removal.

Wall-clock age, Git age/order, lexical order, one index, one route set or generic repository reachability never substitutes for native-owner evidence.

### WP21-L13 — Fail-safe retention

If owner, lifecycle, currentness, protection/blocker coverage, survivor/replacement evidence or machine capability required for a proposed cleanup is missing/ambiguous:

```text
uncertain cleanup eligibility -> RETAIN
```

### WP21-L14 — Owner-qualified pinned basis

Destructive cleanup preparation pins the exact applicable currentness evidence for every independently writable owner it depends on. Movement of a required basis before publication/execution invalidates the preparation and requires re-evaluation; no stale cleanup is merged or forced.

### WP21-L15 — Protection/blocker closure

Before destructive loss, all known protection/blocker consumers applicable to the candidate must be discharged according to their owning contracts, including as relevant recovery, accepted-work/idempotency, chronology/causal history, disclosure/exactness, Story cross-generation references, LIVE state, multiplayer routing and migration prerequisites.

### WP21-L16 — Survivor before destructive loss

Where the native owner requires continuity, a compact survivor, successor, replacement projection or other required durable evidence must be validated and made current in the same valid owner transaction/order before the old representation can be physically removed.

### WP21-L17 — Finite cleanup dispositions

A candidate resolves to one owner-supported disposition:

```text
RETAIN
LOGICAL_RETIRE
COMPACT_OR_REPLACE
PHYSICAL_REMOVE_IF_NATIVE_OWNER_ALLOWS
REBUILD_OR_RECOMPUTE
```

These are architecture dispositions, not a required universal persisted enum.

---

## 4. Representation-class laws

### WP21-L18 — Authoritative native state

Native campaign/world/runtime authority is never garbage merely because it is inactive or old. It may be removed/replaced only when its native owner establishes the lawful terminal/replacement state and all protection/currentness conditions.

### WP21-L19 — Compactable authoritative evidence

Execution traces/receipts, chronology/message/checkpoint detail and similar evidence may be compacted only after every required causal, idempotency, recovery, exactness, history and disclosure obligation has a lawful survivor where required.

### WP21-L20 — Branch-persistent derived projections

Story/index/other rebuildable branch-persistent projections may be rebuilt from surviving native authority under their existing owners. Old projection generations may retire only after current coverage and cross-generation consumer obligations discharge. A projection cannot repair or recreate missing native authority.

### WP21-L21 — Noncanonical planning state

Retained planning/Dramaturg state remains noncanonical. Inactive/stale/incompatible generations may be retained, replaced, selectively rebased, recomputed or cleaned under the planning owner. Physical residue is not semantic activity. Lawful loss of a native planning source invalidates dependent planning; canon is never reconstructed from planning.

### WP21-L22 — Local cache and ephemeral draft state

Private ephemeral drafts and local HOT/cache/scratch projections may be discarded/rebuilt under their local owners when no authoritative obligation depends on them. Their disposal does not require or create a campaign-wide GC authority.

### WP21-L23 — Repository residue

Prepared/rejected commits, logically retired refs and other repository residue have no campaign authority merely because bytes/objects remain physically present.

---

## 5. Absolute Git branch/ref rule

### WP21-L24 — Ref retirement is logical only

HDM/LLM automation never deletes Git branches/refs. Retirement consists only of removing/deactivating them from authoritative selectors, routing or eligibility according to their native owner.

### WP21-L25 — Physical ref existence is non-authoritative

A retired/non-selected ref may remain indefinitely. Its physical existence does not restore LIVE/campaign/session/storage authority.

### WP21-L26 — No deletion capability path

Do not design, probe, invoke, retry or substitute branch/ref deletion through Connector capabilities, native Git/CLI, private HTTP, manual operator fallback or delete/recreate/rewind techniques.

`PHYSICAL_REMOVE_IF_NATIVE_OWNER_ALLOWS` never applies to Git branches/refs.

---

## 6. Late-family cleanup enrollment

### WP21-L27 — Explicit enrollment contract

Any post-Step-5.13 family/representation that may become terminal/stale/replaced must define, before automatic cleanup semantics rely on it:

```text
family identity
native owner
terminal / stale / replaced predicate
currentness basis
retirement disposition
protection / blocker consumers
survivor / rebuild / recompute obligation
machine-realization status
```

This does not require one global cleanup registry. The contract may reside in the native owner/spec/schema/test realization appropriate to the family.

### WP21-L28 — Missing enrollment fails to RETAIN

A new family that has not established enough of this contract for a proposed cleanup remains retained. Future revisit conditions do not manufacture current implementation work.

---

## 7. Current late-family dispositions

### WP21-L29 — WP-17 collaboration obligation

`runtime.collaboration_obligation` uses WP-17's native lifecycle:

```text
OPEN -> CLOSED -> RESOLVED
OPEN/CLOSED -> OBSOLETE as admitted by WP-17
```

`OPEN/CLOSED` obligations remain active/protected by their native owner. Terminal `RESOLVED/OBSOLETE` removes affected current PLAYER routing companions in the same campaign-native closure as required by WP-17.

That terminal transition does **not** independently authorize deletion of the obligation record. Any later physical compaction/removal requires explicit enrolled protection/survivor semantics. Exact obligation schema and PLAYER route-field realization remain deferred machine debt.

### WP21-L30 — WP-18 Dramaturg/planning families

Private ephemeral Dramaturg drafts are local/disposable noncanonical state.

Retained shared/player horizons may become inactive, stale or incompatible under WP-18. Old bytes may remain; currentness/membership/control/source/shared-basis validation determines reuse. They may be recomputed/replaced/cleaned only under WP-18's native rules, and source loss invalidates dependent planning rather than promoting planning to canon.

Exact retained-horizon schemas/value contracts remain deferred machine debt.

---

## 8. Cross-owner boundaries

### WP21-L31 — Recovery/integrity boundary

Diagnostics may inspect bounded recovery/integrity evidence, but cleanup cannot bypass checkpoint/recovery/integrity owners or rewrite accepted canon under the label of repair.

### WP21-L32 — Migration boundary

Cleanup is not migration. It cannot opportunistically transform authoritative campaign semantics/schema identity, adopt a runtime/ruleset or reinterpret accepted work. Those operations remain under WP-20 and native migration owners.

### WP21-L33 — No generic support principal

Current architecture admits no owner-level “support” semantic principal. Support may guide an already-authorized principal. Any future non-owner support principal with elevated diagnostic access requires explicit Product Owner/architecture authority before realization.

### WP21-L34 — Dry-run/currentness rule

A dry-run/report may explain why a candidate is retained or eligible based on its observed basis, but it does not reserve the decision. Any later destructive action re-establishes required currentness/authorization/protection evidence.

---

## 9. Machine-realization boundary

### WP21-L35 — Architecture coverage is not implementation completion

The following remain explicitly deferred until separately authorized implementation planning/execution:

- installed maintenance command registration/dispatcher and exact machine result enums;
- executable command authorization/disclosure/redaction tests;
- exact diagnostic report serialization, if needed;
- family-specific cleanup/blocker tooling not already realized;
- WP-17 obligation/PLAYER-route schemas;
- WP-18 retained-horizon schemas/value contracts;
- automated dry-run/retirement tooling;
- operational measurement of retained-ref cost.

No Step-5 law requires these artifacts to exist now.

### WP21-L36 — No mandatory global machinery

WP-21 requires no global observability store, universal liveness graph/frontier, GC database, background cleanup queue, maintenance lock, support ACL or persistent DEP/RES record.

---

## 10. Candidate status

```text
SELECTED_ALTERNATIVE: C
NEW_AUTHORITY_SUBSYSTEM: NO
BRANCH_REF_DELETION: FORBIDDEN
UNCERTAIN_CLEANUP: RETAIN
LATE_MACHINE_DEBT: PRESERVED / DEFERRED
HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
STEP_6_REQUIRED: YES
```
