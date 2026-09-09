# R2.7 WP-21 — Diagnostics / Observability / Cleanup / Retirement — Canonical Specification

Status: **CANONICAL WP-21 RESULT — FINAL SENIOR PASS / CLOSED**

Date: 2026-09-07

This is the final implementation-facing WP-21 architecture owner after Steps 2–8 and mandatory independent final Senior review. It composes existing HDM owners; it does not replace native lifecycle/currentness, access control, disclosure, persistence, recovery, LIVE, Story/planning, migration or repository policy. WP-21 is closed; earlier design/review artifacts remain provenance.

Design provenance:

- `DEV/docs/superpowers/design/2026-09-06-r2-7-WP-21-task-brief-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-21-step-1-senior-rereview.md` — PASS / Step 1 closed;
- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-21-step-2-research-architecture-draft.md`;
- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-21-step-3-decision-brief.md`;
- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-21-step-4-collaborative-review.md`;
- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-21-step-5-candidate-specification.md`;
- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-21-step-6-whole-project-adversarial-review.md`;
- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-21-step-7-resolution-propagation.md`;
- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-21-step-8-canonicalization.md`.

Upstream fixed law includes PO-006: HDM/LLM automation never deletes Git branches/refs.

---

## 1. Scope

WP-21 owns only the cross-owner composition needed to answer:

1. how a concrete diagnostic/maintenance question obtains bounded trustworthy evidence;
2. how operation routing, principal authorization and recipient disclosure compose;
3. how retirement/removal eligibility is proven without inventing a universal GC authority;
4. how native, compactable-evidence, derived, planning, cache and repository-residue classes differ;
5. how later record families enroll in cleanup/rebuild semantics while machine realization may remain deferred.

WP-21 does **not** create:

- a global telemetry/observability database;
- a universal liveness/GC graph or frontier;
- a background cleanup queue/service;
- a generic support/admin principal or ACL;
- a second persistence/currentness/recovery authority;
- a persistent Diagnostic Evidence Projection or Retirement Evidence Set requirement;
- a maintenance command dispatcher;
- Git branch/ref deletion capability;
- implementation code, schemas, migration execution or implementation planning.

---

## 2. Diagnostic evidence composition

### WP21-L01 — Diagnostics are bounded to a concrete question

A diagnostic/support operation obtains only evidence relevant to the concrete question from the applicable current owners. Diagnostic work does not imply a package-wide/campaign-wide telemetry scan.

### WP21-L02 — Maintenance entry is outside ordinary gameplay

Maintenance follows the existing explicit maintenance/development boundary. Requesting maintenance does not by itself create a gameplay Interaction, action, chronology event, resource/RNG effect or fictional-time advancement.

### WP21-L03 — Operation routing is not authorization

An exact token, command name, natural-language maintenance request or tool route identifies the operation only. It does not authorize the principal, grant gameplay authority, widen disclosure or bypass native currentness/recovery/persistence requirements.

### WP21-L04 — Campaign-global maintenance uses existing authorization

For operations classified by current access-control law as explicit campaign-global maintenance:

```text
current authenticated principal
-> resolve current campaign creator/owner authority
-> require the existing authorization predicate
```

Repository Write/Admin capability, collaborator/organization status, storage ownership, framework-maintainer status, PLAYER binding, a “support” label or possession of an undocumented operation token does not independently satisfy campaign-global maintenance authority.

If required identity/authority cannot be established reliably, fail closed.

### WP21-L05 — Authorization and information eligibility are independent

Passing operation authorization never grants universal diagnostic visibility. Human-visible diagnostic material is filtered by the current intended-recipient information/disclosure owner.

This remains true for the campaign creator: creator authorization is not a blanket right to receive every player-local/private/hidden datum when the current disclosure owner says otherwise.

If eligible and ineligible material cannot safely be separated, omit/redact/withhold the ineligible part and state the limitation.

### WP21-L06 — Forbidden diagnostic payload

Diagnostic/export surfaces never require or intentionally expose:

- credentials or environment-variable secrets;
- hidden system/developer/tool instructions;
- chain-of-thought or private hidden model reasoning;
- unavailable/compacted host context represented as though it still existed;
- other host/tool secrets not admitted by the recipient contract.

### WP21-L07 — Owner-qualified currentness

Each material diagnostic claim identifies/uses the currentness basis of the owner/domain that makes the claim meaningful. Evidence from independently writable campaign, LIVE, session/local or other domains is not collapsed into a universal diagnostic revision, timestamp or frontier.

If a coherent cross-owner conclusion cannot be proven, report it as indeterminate rather than inventing a shared snapshot.

### WP21-L08 — Diagnostic epistemic classes

A diagnostic projection distinguishes materially different evidence states:

```text
OBSERVED_AUTHORITY
DERIVED_CONCLUSION
UNAVAILABLE
WITHHELD_OR_REDACTED
STALE_OR_INDETERMINATE
NON_AUTHORITATIVE_RESIDUE
```

These are semantic categories; exact output schema is deferred.

### WP21-L09 — Diagnostic projection is never authority

A report, export, response, attachment, dry run or support summary does not become gameplay truth, recovery state, disclosure state, migration authority, publication/currentness authority or a substitute for the source records it describes.

---

## 3. Retirement evidence composition

### WP21-L10 — Native owner controls eligibility

A representation may be retired, compacted, replaced, rebuilt/recomputed or physically removed only according to its native owner's lifecycle/replacement rules plus applicable authorization, currentness and protection/blocker requirements.

### WP21-L11 — Terminality/age/reachability is insufficient

None of the following independently authorizes physical loss:

- terminal/resolved/obsolete/inactive/stale status;
- wall-clock or Git age;
- lexical/technical ordering;
- absence from one index/route list;
- generic repository reachability/unreachability.

Semantic liveness and retention come from native owners and declared consumers.

### WP21-L12 — Fail-safe retention

If any required owner, lifecycle, currentness, blocker/protection, survivor/replacement or machine-capability evidence is missing or ambiguous:

```text
uncertain cleanup eligibility -> RETAIN
```

### WP21-L13 — Cleanup uses owner-qualified pinned/current evidence

A destructive cleanup attempt establishes the exact currentness evidence required by each owner/domain it depends on. If a required basis changes before the authoritative action/publication, the prepared cleanup basis is stale and must be re-evaluated. Do not merge stale cleanup, guess a newer basis or force publication.

### WP21-L14 — Protection/blocker closure precedes destructive loss

Every applicable protected consumer must be discharged according to its native contract before destructive loss, including where relevant:

- accepted-work/idempotency/causal evidence;
- checkpoint/recovery state;
- chronology/history/exactness requirements;
- disclosure/message retention;
- Story cross-generation references;
- LIVE/currentness state;
- multiplayer routing/agency;
- migration/compatibility prerequisites.

### WP21-L15 — Survivor/replacement first

Where continuity requires surviving evidence or a successor/rebuilt projection, that survivor is validated and made current in the native owner's required transaction/order before the old representation is destructively removed.

### WP21-L16 — Finite disposition vocabulary

Architecture-level cleanup resolves to one owner-supported disposition:

```text
RETAIN
LOGICAL_RETIRE
COMPACT_OR_REPLACE
PHYSICAL_REMOVE_IF_NATIVE_OWNER_ALLOWS
REBUILD_OR_RECOMPUTE
```

This vocabulary is not a requirement for one global persisted enum/registry.

### WP21-L17 — Dry run never reserves cleanup authority

A dry-run/diagnostic result is bounded evidence from the basis it inspected. Any later destructive action re-establishes current authorization, currentness, blockers/protections and survivor conditions. A previous “eligible” report is never a reusable cleanup authorization token.

---

## 4. Representation classes

### WP21-L18 — Authoritative native state

Native campaign/world/runtime/configuration/control state is not garbage because it is old or inactive. Removal/replacement requires native-owner terminal/replacement law plus full protection/currentness proof.

### WP21-L19 — Compactable authoritative evidence/detail

Completed execution detail, traces/receipts, chronology/message/checkpoint detail and analogous evidence may compact only when every current causal/idempotency/recovery/history/exactness/disclosure obligation has the required surviving representation.

### WP21-L20 — Branch-persistent derived projections

Story/index/other rebuildable branch-persistent projections may be rebuilt only from surviving native authority under their existing owners. Old generations may retire after current coverage and cross-generation consumers are discharged. A projection never repairs or reconstructs missing native authority.

### WP21-L21 — Noncanonical planning state

Dramaturg/planning state remains noncanonical. Inactive/stale/incompatible generations may be retained, replaced, selectively rebased, recomputed or cleaned only under their native planning owner. Physical residue is not semantic activity. Lawful loss/incompatibility of a native source invalidates/requires recomputation of dependent planning; planning cannot reconstruct canon.

### WP21-L22 — Local cache / ephemeral draft state

Private drafts, local HOT/cache and other local scratch projections may be discarded/rebuilt under their local owners when no authoritative obligation depends on them. Their disposal does not create a campaign-wide GC transaction.

### WP21-L23 — Non-authoritative repository residue

Prepared/rejected commits and physically retained non-selected refs/objects have no campaign/runtime authority merely because repository bytes remain.

---

## 5. Absolute Git branch/ref retirement law

### WP21-L24 — Branch/ref deletion is forbidden

HDM/LLM automation never deletes Git branches/refs.

### WP21-L25 — Ref retirement is logical only

A LIVE/campaign/other ref is retired only through its native semantic de-selection/de-authorization/de-routing. The physical ref may remain indefinitely.

### WP21-L26 — Physical existence does not restore authority

Presence of a retired/non-selected ref does not restore LIVE ownership, campaign authority, session authority or storage authority.

### WP21-L27 — No deletion/probe/fallback path

HDM does not design, capability-probe, invoke, retry or substitute branch/ref deletion through Connector APIs, native Git/CLI, private HTTP, manual/out-of-band deletion, delete/recreate, rewind or force techniques.

`PHYSICAL_REMOVE_IF_NATIVE_OWNER_ALLOWS` has a hard type-level exclusion for Git branches/refs; no native owner may opt a ref back into physical deletion.

---

## 6. Late-family enrollment

### WP21-L28 — Explicit cleanup enrollment completeness

A post-Step-5.13 family/representation that may become terminal/stale/replaced must establish enough contract information before automatic cleanup relies on it:

```text
family / representation identity
native owner
terminal / stale / replaced predicate
currentness basis
retirement disposition
protection / blocker consumers
survivor / rebuild / recompute obligation
machine-realization status
```

### WP21-L29 — Enrollment is not a global registry

The enrollment requirement is semantic completeness, not a storage architecture. Its facts may live in the native owner/spec/schema/test/tool contract appropriate to the family. WP-21 requires no universal GC registry/database.

### WP21-L30 — Missing enrollment retains

When the concrete cleanup contract is not sufficiently defined/machine-realized for a proposed automatic destructive action, that family remains `RETAIN`. A future implementation/revisit condition does not manufacture current implementation work.

---

## 7. Current late-family dispositions

### WP21-L31 — WP-17 collaboration obligations

WP-17 owns `runtime.collaboration_obligation` lifecycle and PLAYER routing companions.

`OPEN/CLOSED` obligations remain active under WP-17. Terminal `RESOLVED/OBSOLETE` removes affected current PLAYER route companions in the same campaign-native closure as required by WP-17.

Route-companion removal is **not** obligation-record deletion. Until a later explicitly authorized machine realization establishes cleanup enrollment/protection/survivor semantics for the terminal record, automatic physical obligation-record cleanup remains `RETAIN`.

Current exact obligation schema/fields and PLAYER collaboration-route realization remain deferred machine debt.

### WP21-L32 — WP-18 retained Dramaturg/planning horizons

Private ephemeral Dramaturg drafts are disposable local noncanonical state.

Retained shared/player horizons use WP-18's native current generation plus mode/membership/control/source/shared-basis validity. Multiplayer-disabled or otherwise inactive bytes may remain physically without semantic activity. Age alone never makes a still-current retained horizon removable.

If a current retained basis is invalidated/incompatible, planning is invalidated/recomputed/replaced under WP-18 before obsolete representations are treated as replaceable. Planning never reconstructs lost canon.

Exact retained shared/player horizon schemas/value contracts remain deferred machine debt.

---

## 8. Cross-owner boundaries

### WP21-L33 — Recovery/integrity is not cleanup authority

Diagnostics may inspect bounded recovery/integrity evidence, but “repair/cleanup” cannot bypass checkpoint/recovery/currentness owners, fabricate missing canon or rewrite accepted history outside those owners.

### WP21-L34 — Cleanup is not migration

Cleanup cannot opportunistically transform authoritative schema/semantics, adopt engine/ruleset identity or reinterpret accepted work. Released campaign/schema evolution remains under WP-20 and native migration owners.

### WP21-L35 — No generic support principal

Current architecture has no elevated non-owner “support” semantic principal. Support may guide an already-authorized principal. Adding a future non-owner principal with owner-level maintenance/diagnostic access requires explicit Product Owner/security architecture authority.

---

## 9. Machine-realization status and debt

WP-21 architecture coverage must not be reported as current machine completion.

Explicitly deferred behind future approved implementation planning/execution:

1. installed maintenance command registration/dispatcher and exact result enums;
2. executable command authorization/disclosure/redaction coverage for that future surface;
3. exact diagnostic/export report serialization, if later needed;
4. family-specific cleanup/blocker/protection automation not already realized;
5. WP-17 exact collaboration-obligation schema/fields and PLAYER route-field realization;
6. WP-18 exact retained shared/player horizon schemas/value contracts;
7. automated cleanup dry-run/execution tooling if selected later;
8. operational/performance measurement of physically retained refs; WP-24 may assess cost but cannot re-enable deletion.

No item above is implementation-authorized by WP-21 Steps 2–8.

---

## 10. Acceptance obligations for future realization

A later implementation must prove, as applicable:

- exact operation routing does not grant authorization;
- infrastructure permission does not grant campaign-global maintenance authority;
- unresolved identity/currentness fails closed;
- authorized diagnostic output respects recipient eligibility/redaction;
- hidden CoT/instructions/credentials are not exported;
- diagnostic currentness remains owner-qualified with no universal frontier;
- diagnostic/dry-run output is non-authoritative and stale evidence is re-evaluated;
- uncertain cleanup retains;
- all applicable protections/survivors precede destructive removal;
- derived/planning/cache state never reconstructs native canon;
- WP-17 terminal route removal does not imply obligation deletion;
- WP-18 current retained horizons are not age-cleaned and invalidation causes native-owner recompute/replacement;
- branch/ref deletion and deletion probing/fallback remain impossible.

Exact test layout belongs to later implementation planning.

---

## 11. Final disposition

```text
SELECTED_ARCHITECTURE:
    OWNER-COMPOSED BOUNDED DIAGNOSTICS
    + OWNER-GATED RETIREMENT/REBUILD
    + EXPLICIT LATE-FAMILY CLEANUP ENROLLMENT
    + LOGICAL-ONLY GIT REF RETIREMENT

NEW_GENERIC_OBSERVABILITY_SUBSYSTEM: NO
NEW_GENERIC_GC_SUBSYSTEM: NO
NEW_SUPPORT_ADMIN_AUTHORITY: NO
BRANCH_REF_DELETION: FORBIDDEN
UNCERTAIN_CLEANUP: RETAIN
ROUTED_MACHINE_DEBT: PRESERVED / DEFERRED
HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
NEEDS_PO: NONE

WP21_STEP8_COMPLETE: YES
WP21_FINAL_SENIOR_REVIEW: PASS
WP21_FINAL_CLOSURE: PASS
WP21_CLOSED: YES
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
```
