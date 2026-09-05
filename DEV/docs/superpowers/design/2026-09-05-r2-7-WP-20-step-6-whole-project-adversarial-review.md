# R2.7 WP-20 Step 6 — Whole-Project Adversarial Architecture Review

Status: **STEP 6 COMPLETE — FINDINGS REQUIRE STEP-7 PROPAGATION**

Date: 2026-09-05

Candidate reviewed:

- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-step-5-candidate-specification.md`.

Review stance:

> Assume the candidate can still duplicate authority, hide ambiguity, reinterpret accepted state, or reintroduce obsolete compatibility assumptions. Find concrete failure mechanisms across the whole project.

---

## 1. Independently reconstructed dependency routes

The critic used `DEV/PROJECT_MAP.md` to reconstruct direct and indirect owners rather than relying on the candidate source list alone.

### 1.1 Version / release / package route

```text
clean-slate PO-004
-> accepted versioning namespace/compatibility law
-> VERSIONING release policy
-> GAME/ENGINE_VERSION
-> runtime package provenance
-> ENGINE_UPDATES
-> ruleset package identity/compatibility
```

Checked for mutable-tag identity, same-version assumptions, independent generations and released-asset immutability.

### 1.2 Campaign/storage identity route

```text
WP-19 exact creation identity
-> campaign MANIFEST
-> DND_STORAGE
-> ACCESS_CONTROL
-> ENGINE_UPDATES
-> persistence/publication
```

Checked for creator/storage-owner confusion and baseline leakage into existing campaigns.

### 1.3 Persistent-state/schema route

```text
WP-10 logical family allocation
-> WP-11 physical/native/index distinction
-> GAME/SCHEMA/README + current schema family
-> GAME/MIGRATIONS
-> WP-12 HOT/cache projection
```

Checked for global-schema assumptions, migration-by-parse, projection authority and rebuild timing.

### 1.4 Durability/recovery/currentness route

```text
WP-13 publication
-> PERSISTENCE
-> WP-14 recovery
-> Step-5.2 resumable runtime closure
-> WP-15 chronology/history
```

Checked for local-success/publication-success collapse, ref rewind, accepted-work reinterpretation and chronology loss.

### 1.5 Multiplayer/LIVE route

```text
ACCESS_CONTROL
-> WP-16 LIVE/PLAYER/currentness
-> persistence/CAS
-> recovery
```

Checked for active-only LIVE gating, pending absorption and unauthorized participant migration.

### 1.6 Regression / historical route

```text
current ENGINE_UPDATE_CASES
-> historical 2026-08-18 update/provenance amendments
-> current clean-slate/versioning law
```

Checked for obsolete v0.8-era compatibility semantics leaking into current v1.0+ architecture.

---

## 2. Findings

### F20-01 — SIGNIFICANT — Multiple valid composed paths can create accidental path authority

**Mechanism**

An explicit graph is not deterministic if source/target predicates admit two valid compositions and the runtime chooses by shortest path, edge order or another convenience heuristic. Different paths can transform different intermediate representations and produce different audit/provenance surfaces.

**Affected candidate area:** migration graph/path selection.

**Resolution required:** target package must either leave exactly one valid path or explicitly declare the canonical path/order for that source/target applicability. Otherwise classification is `INDETERMINATE`. No invented tie-breaker.

**Disposition:** AGREE / candidate already contains the core fix; Step 7 must elevate it into final normative law and test obligations.

---

### F20-02 — SIGNIFICANT — Folding `storage_format_generation` into campaign CAS would violate authority boundaries

**Mechanism**

A target can require a newer storage layout. If the migration planner treats the storage axis as just another field in one campaign transaction, a campaign creator could implicitly mutate storage-default authority or a storage owner could implicitly migrate creator-owned campaign state.

**Owners constraining this:** `DND_STORAGE`, WP-19, `ACCESS_CONTROL`, `ENGINE_UPDATES`.

**Resolution required:** storage migration remains a separate storage-owner edge/transaction. It may be a prerequisite. Per-campaign transforms remain creator-owned. Partial success is explicit and does not cross-authorize.

**Disposition:** AGREE / candidate contains this split; Step 7 must propagate it into current runtime/access/migration docs.

---

### F20-03 — SIGNIFICANT — Current `ENGINE_UPDATES.md` still treats same-version Git ancestry as released compatibility proof

**Mechanism**

Current runtime prose says that within one semantic version/package ID, a proven descendant source commit is a compatible cosmetic/maintenance refresh. For released v1.0+ assets this conflicts with two now-current laws:

1. released artifacts are immutable identities;
2. source/version ordering is provenance, not compatibility proof.

If left current, a runtime could silently use different released bytes because their source is a descendant, bypassing explicit compatibility/migration evidence.

Historical 2026-08-18 update amendments contain the same pre-release-era inference.

**Resolution required:** for released v1.0+, exact digest means exact artifact; different released bytes require affirmative target compatibility support. Source ancestry may aid provenance classification but cannot authorize compatibility or silent semantic use. Historical documents remain provenance and are explicitly superseded on this point.

**Disposition:** AGREE / SIGNIFICANT CURRENT-OWNER REPAIR REQUIRED.

---

### F20-04 — SIGNIFICANT — “No active LIVE epoch” is insufficient when a CLOSED epoch still awaits absorption

**Mechanism**

A LIVE epoch may be closed but still contain state not yet absorbed into branch authority. Migrating the branch in that interval can transform a stale branch basis and later absorb old-format state into the migrated branch.

**Owner constraining this:** WP-16 LIVE close/absorb/currentness.

**Resolution required:** migration requires both no active selected LIVE mutable authority and no CLOSED LIVE state awaiting required absorption/reconciliation.

**Disposition:** AGREE / candidate contains this stronger condition; propagate to runtime/tests.

---

### F20-05 — SIGNIFICANT — Schema readability does not prove target compatibility with accepted resumable work

**Mechanism**

A target may parse all persistent records yet be unable to resume an accepted Resolution/Continuation whose frozen ruleset/package/RNG/causal inputs are no longer interpretable. Treating parse/validation as full compatibility could reroll, ambient-rebind or strand accepted mechanics.

**Owners constraining this:** Step-5.2 resumable closure, WP-14 recovery, WP-15 chronology, deterministic mechanics owners.

**Resolution required:** accepted-work interpretation is an explicit compatibility predicate. If unproven, migration/adoption is blocked until existing owners lawfully close/continue that work under a compatible runtime or another explicit supported transition handles it.

**Disposition:** AGREE / candidate contains prerequisite; propagate to final spec/tests.

---

### F20-06 — SIGNIFICANT — Migration audit evidence can accidentally become a second publication authority or create circular identity

**Mechanism**

A migration record that claims the final result by self-embedded containing commit SHA is circular. A separate “migration succeeded” log/marker can also diverge from the actual campaign ref after CAS rejection/ambiguity and become false authority.

**Owners constraining this:** WP-13 publication, WP-14 recovery, WP-10 history allocation.

**Resolution required:** migration evidence records source HEAD/envelope, exact target, ordered edge IDs/artifact identities, auth basis and validation result. Final campaign ref/commit remains publication authority. No contained record is required to embed its own final containing commit identity. Publication success is established only by ref/CAS/read-back.

**Disposition:** AGREE / candidate contains this distinction; propagate explicitly.

---

### F20-07 — MINOR — Derived/index rebuild timing must distinguish branch-persistent projections from local HOT caches

**Mechanism**

Saying “rebuild derived state after migration” is ambiguous. A branch-persistent index required by target validation may need to be rebuilt in the prepared tree before publication, while local HOT/SQLite cache must wait for confirmed authoritative success. Mixing them could validate against stale cache or publish missing required projections.

**Resolution required:** branch-persistent rebuildable projections required by target join prepared transaction; local HOT/runtime cache invalidates/rebuilds only after confirmed publication; asynchronous projections use native owners.

**Disposition:** AGREE / candidate already separates classes; add explicit test mapping.

---

### F20-08 — MINOR — Existing regression case U17 can be misread as a pre-release legacy-layout compatibility promise

**Mechanism**

`ENGINE_UPDATE_CASES.md` currently says “Legacy CAMPAIGN/ campaign migrates engine” and preserves layout unless an explicit layout migration exists. After PO-004, that wording can accidentally preserve obsolete v0.8/pre-release structure as current compatibility scope.

**Resolution required:** retain the valid invariant — a released v1.0+ layout is changed only by an explicit applicable migration edge — but remove any implication that pre-release legacy layout is supported.

**Disposition:** AGREE / test-document repair required.

---

## 3. Negative findings / challenges that did not become issues

### N20-01 — No need for a mutable central registry

No current owner or deployment requirement requires compatibility state external to the exact target package. A central registry would add authority/currentness/network failure modes without solving a current requirement.

### N20-02 — No need to reopen the versioning taxonomy

The candidate exposes no insufficiency in the three-category version/generation law. The missing capability is explicit compatibility/migration relation, which that law intentionally delegates to WP-20.

### N20-03 — No need for a migration-specific global lock

Existing LIVE/currentness/ref-CAS prerequisites supply the required mutation boundary. A global migration lock would duplicate current owners.

### N20-04 — No Product Owner decision is exposed

The critic found no unresolved support-duration promise, pre-release compatibility question, authority trade-off or risk acceptance that current product decisions fail to settle. Future release-by-release support breadth remains a future release decision, not a current promise.

---

## 4. Severity summary

```text
BLOCKING: 0
SIGNIFICANT: 6
MINOR: 2
```

All findings are mechanically resolvable without changing the selected architecture.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
STEP_7_REQUIRED: YES
CANDIDATE_CANONICALIZATION_ALLOWED_BEFORE_STEP_7: NO
```
