# R2.7 WP-21 Step 6 — Whole-Project Adversarial Architecture Review

Status: **STEP 6 COMPLETE — FINDINGS REQUIRE STEP-7 PROPAGATION**

Date: 2026-09-07

Candidate reviewed:

- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-21-step-5-candidate-specification.md`.

Review stance:

> Assume the composition candidate can still leak privilege, invent a false universal frontier, delete needed evidence, turn projections into authority or accidentally reactivate forbidden repository operations. Find concrete failure mechanisms across current owners and late-family debt.

---

## 1. Independently reconstructed routes

### 1.1 Support / disclosure route

```text
PLAY_POLICY maintenance boundary
-> MAINTENANCE_COMMANDS proposal
-> ACCESS_CONTROL
-> Step 5.12 disclosure
-> session/integrity/recovery evidence
```

Checked for token-as-authorization, creator-as-universal-recipient and diagnostic-output authority.

### 1.2 Cleanup / publication / recovery route

```text
Step 5.13 cleanup law
-> logical-ref amendment / PO-006
-> WP-13 publication/currentness
-> WP-14 recovery/checkpoints
-> PERSISTENCE / INTEGRITY
```

Checked for stale dry-run decisions, destructive-before-survivor ordering and ref-deletion leakage.

### 1.3 Story/planning route

```text
Step 5.10 Story
-> R2.1 continuity
-> WP-18 planning/horizons
-> native source owners
```

Checked for projection resurrection of canon and premature planning cleanup.

### 1.4 Collaboration route

```text
WP-17 obligation lifecycle
-> PLAYER routing companions
-> accepted input/native handoff
-> campaign durability closure
```

Checked for equating terminal routing with record deletion and for falsely claiming machine realization.

### 1.5 Migration / versioning route

```text
WP-20 migration
-> local schemas/native-versus-derived law
-> WP-21 retirement/rebuild
```

Checked for cleanup becoming an undeclared schema/semantic migration.

---

## 2. Findings

### F21-201 — SIGNIFICANT — creator maintenance authorization can be misread as universal diagnostic disclosure

**Mechanism**

A maintainer may correctly pass creator authorization for a global operation but the diagnostic payload can contain player-local/private material that the current disclosure owner does not permit to that recipient. Treating authorization as payload eligibility would bypass Step 5.12.

**Required resolution**

Final law must state that authorization and recipient eligibility are independent gates; an authorized result is redacted/withheld when necessary. Creator status alone never upgrades disclosure eligibility.

**Disposition:** AGREE. Candidate contains the core separation; Step 7 must elevate it into the final normative contract and acceptance obligations.

### F21-202 — SIGNIFICANT — a diagnostic “current state” report can manufacture a false universal frontier

**Mechanism**

Campaign, LIVE, local runtime/session and other independently writable owners can have different currentness evidence. A report that emits one `current_revision`/“snapshot time” and treats it as globally authoritative can claim coherence that no owner established.

**Required resolution**

Diagnostic evidence must remain owner-qualified. Cross-domain output records the exact basis of each material claim or explicitly reports indeterminate composition. No universal diagnostic frontier/revision is introduced.

**Disposition:** AGREE. Propagate explicitly.

### F21-203 — SIGNIFICANT — cleanup disposition wording could accidentally re-enable Git ref deletion

**Mechanism**

A generic `PHYSICAL_REMOVE_IF_NATIVE_OWNER_ALLOWS` mode can be implemented mechanically across candidate types and later applied to a retired LIVE/campaign ref, contradicting PO-006 even if the native LIVE owner considers it semantically retired.

**Required resolution**

Git branch/ref identity is a hard type-level exclusion from physical removal. No owner may opt it back in through the generic cleanup mode; logical de-routing/de-authorization is final HDM action.

**Disposition:** AGREE. Candidate already says this; Step 7 must make the exclusion impossible to miss in the final cleanup matrix/tests debt.

### F21-204 — SIGNIFICANT — WP-17 terminal obligation can be deleted while provenance/accepted-input consumers still depend on it

**Mechanism**

WP-17 atomically removes PLAYER route refs at `RESOLVED/OBSOLETE`. An implementation could infer that the terminal obligation itself is now garbage and remove the record even though accepted input/handoff/recovery/history provenance may still require it.

**Required resolution**

Routing-companion removal and obligation-record retention are distinct. Terminality permits route removal under WP-17, not physical record deletion. Automatic record cleanup remains `RETAIN` until an explicit enrolled protection/survivor contract is machine-realized.

**Disposition:** AGREE. Routed machine debt preserved; no WP-17 reopen required.

### F21-205 — SIGNIFICANT — WP-18 planning cleanup can invalidate a still-current retained horizon without a recompute boundary

**Mechanism**

Old/inactive planning bytes are cleanable, but a naive cleanup pass could classify a retained horizon as stale from age or source movement alone while it is still the current bounded retained generation for an eligible player/shared basis.

**Required resolution**

Planning cleanup uses WP-18 current generation, mode/membership/control, source basis and shared-basis validation. If a current basis is lost or becomes incompatible, invalidate/recompute according to WP-18 before treating the old horizon as replaceable. Planning never reconstructs canon.

**Disposition:** AGREE. No new planning owner/schema now.

### F21-206 — SIGNIFICANT — dry-run/report output can become stale authority for later destructive cleanup

**Mechanism**

A support report may say “eligible to remove.” If a later action trusts that report after currentness/protection movement, the report becomes an accidental cleanup authorization cache.

**Required resolution**

Dry-run/diagnostic results are time/basis-bounded evidence only. A destructive action must re-establish current authorization, currentness, blockers/protections and survivor conditions; reports never reserve eligibility.

**Disposition:** AGREE. Propagate explicitly.

### F21-207 — MINOR — late-family enrollment could be misread as a mandatory global registry

**Mechanism**

A fixed enrollment field list may tempt implementation to build a centralized GC registry/database even though native specs/schemas/tests can carry the required contract.

**Required resolution**

State explicitly that enrollment is a completeness obligation, not a physical storage choice. No global registry is required.

**Disposition:** AGREE.

### F21-208 — MINOR — architecture coverage can be misreported as current machine implementation

**Mechanism**

The final canonical spec could say WP-17/WP-18 cleanup is covered and downstream readers may infer their exact schemas/tooling exist now.

**Required resolution**

Final spec and Step-8 checkpoint must preserve `STALE_DEBT_ALREADY_ROUTED`/deferred status for exact WP-17 obligation/route and WP-18 retained-horizon machine realization and for maintenance command dispatch/authorization tests.

**Disposition:** AGREE.

---

## 3. Negative findings

### N21-201 — No current owner requires a global observability store

Bounded owner evidence is sufficient. A global telemetry database would create new retention/currentness/disclosure obligations without a present consumer.

### N21-202 — No universal GC graph/frontier is required

Step 5.13 plus native-owner enrollment supplies safe cleanup semantics. Sparse consumers and heterogeneous owners make one universal liveness graph actively risky.

### N21-203 — No generic support/admin principal is required

Current maintenance composition can be performed by the existing authorized principal. A future elevated non-owner support role would be a new Product Owner/security decision, not something WP-21 should infer.

### N21-204 — No wholesale reopen of Step 5.13, WP-17, WP-18 or WP-20

The candidate only composes their accepted semantics. The ref-delete contradiction was already repaired during Step 1; late-family machine debt is already routed.

### N21-205 — No Product Owner decision exposed

The critic found no unresolved deletion policy, privilege expansion, retention guarantee or product behavior that accepted owners fail to settle.

---

## 4. Severity / gate

```text
BLOCKING: 0
SIGNIFICANT: 6
MINOR: 2
HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
NEEDS_PO: NONE
STEP_7_REQUIRED: YES
CANDIDATE_CANONICALIZATION_ALLOWED_BEFORE_STEP_7: NO
```

All findings are resolvable by sharpening the WP-21 composition contract. No current native owner requires semantic change.
