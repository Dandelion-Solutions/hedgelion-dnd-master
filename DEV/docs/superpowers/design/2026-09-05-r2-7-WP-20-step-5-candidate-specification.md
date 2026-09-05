# R2.7 WP-20 Step 5 — Candidate Specification

Status: **STEP 5 COMPLETE — CANDIDATE FOR ADVERSARIAL REVIEW**

Date: 2026-09-05

Domain: **Engine update / schema evolution / migration**

This candidate formalizes the Step-2 research and Step-3/4 accepted direction. It is not final authority until Steps 6–8 complete.

---

## 1. Scope

WP-20 defines safe compatibility/update/migration semantics for campaigns created by **released HDM v1.0+** runtimes.

It does not provide compatibility with v0.8/pre-release state, does not authorize implementation planning or migration execution, and does not own future release-support promises.

The accepted versioning taxonomy remains unchanged and is an upstream invariant.

---

## 2. Normative terminology

### 2.1 Exact target package

A validated immutable released runtime artifact identified by its existing semantic/package/provenance/digest contracts. Mutable tags, current `main`, timestamps and filename resemblance are not exact target identity.

### 2.2 Compatibility Evidence Envelope (CEE)

A bounded typed set of current authoritative evidence used for one source-campaign/exact-target evaluation. It is assembled from current owners and is not a new persistent owner.

### 2.3 Migration edge

One immutable directed support declaration shipped by an exact target package, with explicit source predicate, target predicate, affected authoritative scope, prerequisites, transform identity/order and post-transform validation obligations.

### 2.4 Migration path

One exact ordered composition of migration edges selected only when all source/intermediate/target predicates and dependencies compose deterministically.

---

## 3. Compatibility evidence

For a selected campaign and exact target package, evaluate all applicable axes rather than one scalar. The CEE SHALL include, as relevant:

```text
repository/campaign ref and pinned current campaign HEAD H
campaign_id
current authoritative creator identity
MANIFEST.engine.current:
  engine_version
  campaign_contract_generation
  exact package/provenance/digest identity
MANIFEST.ruleset.current:
  exact ordered ruleset-set identity
  compatibility family/generation
  catalog-generation/identity evidence required by the ruleset owner
relevant authoritative record-family schema_version predicates
storage_format_generation as a separate storage prerequisite
accepted-work/resumable-runtime closure compatibility evidence
LIVE ownership/absorption/currentness evidence
exact immutable target package identity
exact target package compatibility declarations/migration-edge set
```

The evaluator SHALL read only evidence required for the concrete classification. It must not preload the entire campaign merely to compare versions.

`campaign_update.compatibility` or equivalent release metadata may route to maintenance evaluation but is not compatibility proof.

---

## 4. Finite compatibility outcome

The evaluator returns exactly one of:

```text
DIRECT_COMPATIBLE
MAINTENANCE_REFRESH
MIGRATION_REQUIRED
UNSUPPORTED_INCOMPATIBLE
INDETERMINATE
```

### 4.1 DIRECT_COMPATIBLE

The exact target affirmatively supports the complete relevant source envelope and requires no authoritative persistent transformation.

Equality of version/generation values, package ancestry or successful schema parsing is insufficient unless the target support contract says the relevant source is directly supported.

### 4.2 MAINTENANCE_REFRESH

Only owner-permitted nonsemantic/rebuildable/local maintenance is required. This result does not silently authorize creator-owned semantic adoption or native-state transformation.

### 4.3 MIGRATION_REQUIRED

The exact target supports the source only through one deterministically selectable explicit directed migration path and all authority/currentness/prerequisites can be satisfied.

### 4.4 UNSUPPORTED_INCOMPATIBLE

Use when any required source state is explicitly unsupported, required immutable support/edge material is absent, a required predicate fails, an unsupported newer contract/generation is encountered, or a preserved accepted-work closure cannot be interpreted safely.

### 4.5 INDETERMINATE

Use when evidence is unavailable/ambiguous, currentness cannot be proven, or several valid paths remain without an exact target-declared canonical order. This state fails closed and may be re-evaluated when evidence changes; it is not permission for best-effort migration.

---

## 5. Independent compatibility axes

The following remain separate domains:

- engine release identity/version;
- exact runtime-package provenance/digest;
- campaign contract generation;
- exact ruleset-set identity and ruleset compatibility family/generation;
- catalog identity/generation where required by the owning ruleset/catalog contract;
- artifact-local persistent/protocol `schema_version`;
- storage format generation;
- accepted-work/resumability compatibility;
- LIVE/currentness state.

No equality or ordering across axes has semantic meaning. Ordering inside an axis does not manufacture compatibility or a migration edge.

---

## 6. Migration graph and path selection

### 6.1 Package-scoped ownership

Migration support SHALL be finite immutable support data associated with the exact target runtime package.

It SHALL NOT be:

- a mutable remote/global compatibility registry;
- a campaign-owned migration database;
- a service whose current state changes the interpretation of an old immutable target package;
- a generic graph authority over campaign state.

### 6.2 Edge contract

Each migration edge SHALL logically identify at least:

```text
edge_id
source compatibility predicate
exact target/intermediate predicate
affected authoritative record/family/contract predicates
prerequisites/dependencies
ordered transform identity
post-transform validation obligations
immutable edge artifact/provenance identity
```

Exact machine serialization and transform language are deferred to implementation design/planning after R2.7.

### 6.3 Directionality

Every edge is directed. A migration from A to B does not imply B to A.

Engine version ordering, generation ordering, local schema-version ordering, Git ancestry, timestamps or lexical order SHALL NOT create a direction or path.

### 6.4 Deterministic selection

For one source CEE and exact target:

1. filter edges by fully proven source predicate;
2. compose only where the prior target/intermediate predicate exactly satisfies the next source predicate and all dependencies remain valid;
3. reject a selected path containing a cycle;
4. reject paths requiring absent immutable transform/support artifacts;
5. no valid path -> `UNSUPPORTED_INCOMPATIBLE` unless direct compatibility is independently proven;
6. exactly one valid path -> select it;
7. several valid paths -> select only an exact target-declared canonical path/order;
8. several valid paths without exact canonical declaration -> `INDETERMINATE`.

The runtime SHALL NOT choose by shortest path, highest target number, latest commit, lexical edge ID or any other invented tie-breaker.

---

## 7. Authority composition

### 7.1 Storage owner

Storage-default authority owns:

- `storage_format_generation` evolution and storage-layout/default-marker migration;
- `DND_STORAGE.engine.baseline` maintenance for New Game.

Storage migration is a separate storage-owner transaction. It does not migrate existing campaign semantic/native state or adopt a runtime/ruleset for a campaign.

### 7.2 Campaign creator

Existing-campaign operations are creator-only when they:

- change `MANIFEST.engine.current` or `MANIFEST.ruleset.current` adoption identity;
- transform authoritative campaign semantic/native state;
- publish a campaign migration result.

Storage ownership, repository permission, collaborator status or active PLAYER status does not grant this authority.

A non-creator may use an exact target only where direct compatibility is affirmatively proven and no creator-owned campaign identity/native mutation is required.

### 7.3 Separate success domains

If storage evolution and campaign migration are both required, they remain separate authority transactions. The applicable storage target state may be a prerequisite to campaign migration, but success/failure of one never implies success/failure or rollback of the other.

---

## 8. Currentness / LIVE / accepted-work prerequisites

### 8.1 Pinned source basis

Before preparing a campaign migration, pin exact current campaign HEAD `H` and all owner-qualified mutable currentness evidence required by the transformation.

If the campaign ref or another required independently writable owner changes before publication, the prepared basis is stale. Abort and re-evaluate; do not merge the prepared migration onto a moved head.

### 8.2 LIVE

Migration is blocked until both are true:

```text
no active LIVE-selected mutable authority for affected state
AND
no CLOSED LIVE state awaiting required absorption/reconciliation
```

Use existing LIVE close/absorb/currentness contracts. No migration-specific global lock or epoch is introduced.

### 8.3 Accepted resumable work

The exact target SHALL prove safe interpretation of every current preserved accepted-work closure that may resume after migration, including applicable:

- stable command/resolution/continuation identities;
- frozen causal inputs;
- exact ruleset/package identity evidence;
- fixed RNG evidence/receipts;
- owner-specific currentness/provenance required for continuation.

If safe interpretation is not proven, target adoption/migration is blocked. Migration SHALL NOT rebind accepted work to target ambient rules, reroll outcomes, reconstruct hidden LLM reasoning or silently discard accepted closure.

---

## 9. Transformation scope

### 9.1 Authoritative native records

Only authoritative native paths/families declared by the selected edge path may be transformed. Unrelated canon/history/state is preserved byte-for-byte or semantically unchanged according to its owner.

### 9.2 Stable identities and history

Migration SHALL preserve stable campaign/entity/event/command/resolution/continuation/PLAYER identities and historical provenance unless an explicit accepted owner law defines a semantics-preserving representation change.

Migration is not an opportunity to renumber IDs, rewrite unrelated canon, compact history, infer symmetric relations or promote projections into authority.

### 9.3 Branch-persistent derived/index projections

A required branch-persistent derived/index projection whose source authority is transformed may be deterministically rebuilt from the prepared migrated authoritative state when its owner permits rebuild. The rebuilt projection joins the same prepared campaign tree transaction.

It must not be used as source authority to decide the transformation.

### 9.4 Local HOT/runtime caches

Local HOT/SQLite/runtime instruction caches are not campaign authority and do not participate in authoritative migration publication. After durable campaign success, invalidate/rebuild affected local caches from the confirmed target authority.

### 9.5 Other projections

Story and other owner-specific noncanonical/asynchronous projections follow their existing catch-up/rebuild contracts. Migration does not promote them to authority merely to simplify transformation.

---

## 10. Preparation and validation

Architecture-level sequence:

```text
resolve authorized principal/creator
-> pin current campaign HEAD H + required currentness evidence
-> resolve exact immutable target package
-> build bounded CEE
-> classify
-> satisfy storage/LIVE/accepted-work prerequisites
-> select exact directed edge path when required
-> prepare declared authoritative transformations from H
-> rebuild required branch-persistent derived/index projections
-> validate all target predicates/invariants
-> prepare migration evidence
```

No step above changes campaign authority.

Local transform/validation success means only `PREPARED`.

---

## 11. Authoritative publication

A campaign migration/adoption SHALL publish through the existing campaign-tree transaction contract:

```text
one complete prepared tree
-> one commit parented to pinned H
-> one non-force target campaign-ref CAS/update
```

No migration-specific second publication authority, force push or hidden branch rewrite is introduced.

### 11.1 Durable success

Only a confirmed accepted ref update establishes migration/adoption success.

After confirmation, the campaign current identity/projections in the committed tree describe the target state, and subsequent runtime binding/cache rebuild may proceed.

### 11.2 Ref rejection / race

If the ref moved or CAS is rejected, the old/current ref remains authority. Prepared migration objects are unreachable evidence only. Rebuild/re-evaluate from current authority; never force or silently merge.

### 11.3 Ambiguous transport

If publication transport result is unknown, perform bounded authoritative ref read-back under the existing persistence contract:

- ref at prepared commit -> accepted;
- ref proves another successor/current head -> rejected/stale;
- outcome still cannot be proven -> indeterminate, stop/recover by current owner law.

Do not blindly retry an authority-changing migration publication.

---

## 12. Reverse / downgrade / rollback

### 12.1 Before publication

Abort/discard prepared transformation. No rollback transaction is needed because authority never changed.

### 12.2 Rejected publication

Old/current ref remains authority. No rollback transaction is needed.

### 12.3 After confirmed migration

A prior checkpoint, old ref or previous release cannot be used as generic rollback authority.

A downgrade/reverse transition is supported only if a separately declared reverse migration edge/path exists for the exact current source and exact older target. It executes as a new creator-authorized forward campaign publication under current CEE/currentness/LIVE/accepted-work rules.

---

## 13. Unsupported older/newer state

### 13.1 Missing old runtime/support material

Do not substitute mutable latest/main/current-tag state for missing source support. If exact source evidence or immutable edge artifact required by the target cannot be obtained, classify unsupported or indeterminate as appropriate.

### 13.2 Unsupported newer contract

An older runtime encountering a campaign/schema/ruleset/storage contract generation/version it does not explicitly support SHALL fail closed. It must not parse-success its way into compatibility, decrement a number, or choose a guessed reverse edge.

---

## 14. Migration evidence

Migration shall leave bounded provenance evidence using an existing admitted maintenance/audit/history allocation or a later implementation-realized member of that allocation. The evidence must not become publication/currentness authority.

Logically preserve at least:

```text
pinned source campaign HEAD / source envelope identity
exact target runtime/package identity
ordered migration edge IDs + immutable edge artifact identities
creator/authorization basis
validation outcome
```

The resulting campaign ref/commit is authoritative publication identity. A record contained in that commit must not circularly require its own final containing commit hash.

---

## 15. Compatibility preservation invariants

Unless an explicit target migration edge changes representation while preserving owner semantics, migration SHALL preserve:

1. campaign identity and creator authority;
2. stable semantic/entity/PLAYER IDs;
3. authoritative owner direction and relationship semantics;
4. accepted execution identities, causal inputs and RNG evidence;
5. truth/knowledge/disclosure separation;
6. chronology/history/causal evidence;
7. lifecycle/readiness/current-routing semantics;
8. House Rules/policy authority/provenance;
9. multiplayer binding/agency/currentness;
10. recovery-safe durability and resumability;
11. immutable `created_with` provenance;
12. exact package/ruleset evidence needed to interpret retained state.

---

## 16. Current-document implications

If this candidate survives Step 6, Step 7 must synchronize these current surfaces:

- `GAME/CORE/ENGINE_UPDATES.md` — remove released-v1+ compatibility inference from same-version source ancestry; source ancestry remains provenance only;
- `DEV/ARCHITECTURE/ACCESS_CONTROL.md` — remove the broad storage-owner wording that conflicts with explicit creator-only existing-campaign migration/adoption;
- `GAME/MIGRATIONS/README.md` — state graph/path ambiguity, separate storage edge, publication outcome and explicit reverse-edge law;
- `DEV/TESTS/ENGINE_UPDATE_CASES.md` — reframe pre-release legacy-layout case and add architecture-level regression requirements for the new failure classes.

Historical 2026-08-18 design amendments remain provenance. Their portable storage-baseline separation and exact package-provenance rules survive. Their same-version source-ancestry compatibility inference does not govern released v1.0+ campaigns if this candidate becomes canonical.

---

## 17. Deferred realization

WP-20 architecture does not implement:

- migration-edge machine schema/catalog;
- migration transform code/interpreter;
- release-builder migration closure validation;
- runtime compatibility evaluator code;
- executable migration fixtures/tests;
- real campaign/storage migration;
- implementation plan.

Those are post-R2.7 implementation consumers after the required planning/review gates.

```text
CANDIDATE_RECOMMENDATION: ACCEPT PACKAGE-SCOPED EXPLICIT GRAPH
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
STEP_6_REQUIRED: YES
```
