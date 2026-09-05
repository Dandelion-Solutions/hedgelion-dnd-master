# R2.7 WP-20 — Engine Update / Schema Evolution / Migration — Canonical Specification

Status: **CANONICALIZATION CANDIDATE — STEP 8 COMPLETE / MANDATORY SENIOR REVIEW PENDING**

Date: 2026-09-05

This specification is the final implementation-facing WP-20 architecture owner produced by Steps 2–8. It composes existing HDM owners rather than replacing their native semantics. It becomes the operative WP-20 result subject to the mandatory post-Step-8 Senior review gate.

Design provenance:

- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-architecture-task-brief.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-task-brief-critic.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-step-1-senior-review.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-step-2-research-architecture-draft.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-step-3-decision-brief.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-step-4-collaborative-review.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-step-5-candidate-specification.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-step-6-whole-project-adversarial-review.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-step-7-resolution-propagation.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-step-8-canonicalization.md`.

Product / upstream law:

- `DEV/docs/superpowers/specs/2026-09-05-hdm-v1-clean-slate-compatibility-owner-decision.md`;
- `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md`;
- `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-machine-realization-status-amendment.md`.

---

## 1. Scope and compatibility horizon

WP-20 owns the composition contract for **released HDM v1.0+ campaign/runtime/schema evolution**:

1. compatibility evidence and finite classification;
2. explicit migration support/path semantics;
3. creator/storage-owner authorization separation;
4. LIVE/currentness/accepted-work prerequisites;
5. authoritative migration publication and failure semantics;
6. reverse/downgrade policy;
7. native-versus-derived/cache transformation rules;
8. migration provenance and preservation invariants.

WP-20 does **not**:

- restore v0.8 or other pre-release compatibility;
- promise that every future release migrates every prior release;
- replace native owners for persistence, LIVE, recovery, rulesets, schemas or authority;
- define implementation code, migration language, machine schema or release-builder realization;
- execute a real migration;
- start implementation planning or WP-21.

Pre-release/v0.8 state may remain as historical provenance only. It creates no compatibility obligation.

---

## 2. Upstream versioning law remains unchanged

The accepted taxonomy is preserved without reopening:

```text
A — engine release
    MAJOR.MINOR[-prerelease]

B — engine-bound component
    ENGINE_MAJOR.ENGINE_MINOR.REVISION

C — independent contract/state namespace
    owner-local revision / schema_version / generation
```

Normative consequences:

- numbers identify/order only inside their own namespace according to that owner;
- equality or order is not compatibility proof;
- values from different namespaces are never numerically compared for compatibility;
- engine release order does not imply a migration path;
- `campaign_contract_generation`, `storage_format_generation`, local `schema_version`, ruleset compatibility generation and catalog generation remain distinct axes;
- released assets are immutable identities;
- mutable tags/current `main`, timestamps and raw Git SHA ordering are never migration identity/compatibility authority.

---

## 3. Exact target package

Compatibility and migration are evaluated against one **exact immutable target runtime package**, validated through existing package/provenance/digest contracts.

Exact target identity is based on the package's own immutable metadata/provenance and final artifact digest, not a later resolution of a mutable tag.

For a released target:

```text
same engine_version
same package_id
source-commit ancestry
```

are each insufficient by themselves to prove compatibility with different bytes.

Exact digest equality proves exact artifact identity. Different released bytes require affirmative compatibility support from the exact target contract.

---

## 4. Compatibility Evidence Envelope

### WP20-L01 — Bounded owner-composed evidence

For one selected campaign and one exact target package, construct a bounded **Compatibility Evidence Envelope (CEE)** from current owning sources as applicable:

```text
campaign repository/ref + pinned current campaign HEAD H
campaign_id
current authoritative creator identity
MANIFEST.engine.current:
  engine_version
  campaign_contract_generation
  exact package/provenance/digest identity
MANIFEST.ruleset.current:
  exact ordered ruleset-set identity
  compatibility family/generation
  catalog-generation/identity evidence required by its owner
relevant authoritative persistent/protocol family schema_version predicates
storage_format_generation as a separate storage prerequisite
accepted-work / resumable-runtime closure compatibility evidence
LIVE ownership / absorption / currentness evidence
exact immutable target package identity
exact target package direct-compatibility declarations and migration-edge support
```

The CEE is temporary evidence. It is not a new persistent campaign record, global snapshot, version registry or currentness owner.

Only evidence required for the concrete classification need be loaded. Whole-campaign scanning is not the default compatibility algorithm.

### WP20-L02 — Coarse compatibility metadata is routing only

Fields such as `campaign_update.compatibility` may route the runtime into maintenance evaluation, but they are not complete compatibility proof and do not authorize migration.

---

## 5. Finite compatibility classification

### WP20-L03 — Exact outcome set

One CEE/exact-target evaluation returns exactly one of:

```text
DIRECT_COMPATIBLE
MAINTENANCE_REFRESH
MIGRATION_REQUIRED
UNSUPPORTED_INCOMPATIBLE
INDETERMINATE
```

### WP20-L04 — DIRECT_COMPATIBLE

Use only when the exact target affirmatively supports the complete relevant source envelope and no authoritative persistent transformation is required.

Successful parsing, equal generations, equal semantic engine version or source ancestry does not independently establish this result.

### WP20-L05 — MAINTENANCE_REFRESH

Use only when the target requires owner-permitted nonsemantic/rebuildable/local maintenance and no authoritative campaign semantic/native transformation is required.

This outcome never grants creator-owned adoption authority to a non-creator.

### WP20-L06 — MIGRATION_REQUIRED

Use when the exact target supports the source only through a deterministically selectable explicit directed migration path and all owner/currentness/prerequisite gates can be satisfied.

### WP20-L07 — UNSUPPORTED_INCOMPATIBLE

Use when a required source state/predicate is explicitly unsupported, required immutable support material is absent, an unsupported newer contract/generation is encountered, or accepted resumable work cannot be interpreted safely by the target.

### WP20-L08 — INDETERMINATE

Use when evidence/currentness is insufficient or ambiguous, or more than one valid migration path remains without an exact target-declared canonical path/order.

`INDETERMINATE` fails closed. It permits re-evaluation when evidence/currentness changes; it does not permit guessed compatibility or best-effort migration.

---

## 6. Independent compatibility axes

### WP20-L09 — No scalar collapse

The evaluator must preserve independent owner semantics for:

- engine release;
- exact runtime package;
- campaign contract generation;
- exact ruleset set;
- ruleset compatibility family/generation;
- catalog compatibility/identity where applicable;
- artifact-local persistent/protocol schema version;
- storage format generation;
- accepted-work resumability;
- LIVE/currentness.

No axis becomes a universal compatibility epoch.

### WP20-L10 — Local schema evolution

Artifact-local `schema_version` belongs to its persistent/protocol contract. A compatible additive optional change may remain on the same local version where its owner allows it. A breaking required-form or semantic change requires a local version change, and released persisted state that needs transformation requires an explicit applicable migration edge.

`campaign_contract_generation` may express an aggregate campaign-wide compatibility boundary but does not replace local schema predicates or prove full compatibility by equality.

---

## 7. Explicit migration graph

### WP20-L11 — Package-scoped immutable support

Migration support is finite immutable support data associated with the exact target package.

It is not:

- a mutable global/remote migration registry;
- a campaign-owned migration database;
- a graph database/service;
- a background compatibility service;
- an authority whose later mutation changes the meaning of an older released target.

A target may support only direct edges. General-purpose graph infrastructure is not required.

### WP20-L12 — Edge semantics

Each supported directed migration edge shall logically define at least:

```text
edge_id
source compatibility predicate
exact target/intermediate predicate
affected authoritative record/family/contract predicates
required prerequisites/dependencies
ordered transform identity
post-transform validation obligations
immutable edge artifact/provenance identity
```

Exact realization format is deferred to later implementation planning.

### WP20-L13 — Direction is explicit

A supported `A -> B` edge never implies `B -> A`.

Engine-version ordering, generation/schema ordering, Git ancestry, timestamps, lexical order and numeric adjacency never manufacture an edge or direction.

### WP20-L14 — Deterministic path selection

Given one source CEE and exact target:

1. retain only edges whose source predicates are fully proven;
2. compose edges only when each intermediate target predicate exactly satisfies the next source predicate and all prerequisites/dependencies remain valid;
3. reject a selected path containing a cycle;
4. reject any path requiring missing immutable edge/transform support;
5. if no path remains and direct compatibility is not independently proven -> `UNSUPPORTED_INCOMPATIBLE`;
6. if exactly one valid path remains -> select it;
7. if several valid paths remain, select only an exact target-declared canonical path/order;
8. if several valid paths remain without that declaration -> `INDETERMINATE`.

No shortest-path/newest-version/latest-commit/lexical tie-breaker is permitted.

---

## 8. Authority composition

### WP20-L15 — Storage authority is separate

The storage owner controls storage-default evolution, including `storage_format_generation` and `DND_STORAGE.engine.baseline` under its existing contract.

Storage migration is a separate storage-owner transaction. It does not migrate existing campaign semantic/native state or adopt a runtime/ruleset for a campaign.

### WP20-L16 — Campaign migration is creator-owned

Changing creator-controlled campaign current engine/ruleset identity or transforming authoritative campaign semantic/native state is a creator-only operation.

Storage ownership, repository Write/Admin permission, collaborator status and PLAYER membership do not independently grant existing-campaign migration authority.

### WP20-L17 — Separate prerequisites and outcomes

A required storage format may be a prerequisite to campaign migration, but storage and campaign operations retain separate authority/publication/success domains.

If both are needed, partial success is explicit. Neither transaction silently rolls back or authorizes the other.

### WP20-L18 — Non-creator compatibility use

A non-creator may use an exact target only when direct compatibility is affirmatively proven and no creator-owned campaign identity/native-state mutation is required. A non-creator may not persist campaign adoption identity merely because a target runtime can read the state.

---

## 9. Currentness and concurrency prerequisites

### WP20-L19 — Pinned current source basis

Before preparing migration, pin exact current campaign HEAD `H` and all independently writable owner currentness evidence required by the selected transform.

If any required source changes before publication, the prepared basis is stale. Abort/re-evaluate from current authority. Do not merge the prepared migration onto a moved head and never force.

### WP20-L20 — LIVE boundary

Campaign migration is blocked until both are true:

```text
no active LIVE-selected mutable authority for affected state
AND
no CLOSED LIVE state awaiting required absorption/reconciliation
```

Existing LIVE close/absorb/currentness contracts are reused. WP-20 introduces no migration-specific global lock/epoch.

---

## 10. Accepted resumable work

### WP20-L21 — Frozen accepted work is a compatibility predicate

Before target adoption, the exact target must prove safe interpretation of every preserved accepted-work closure that may remain resumable/current, including applicable:

- stable command/resolution/continuation identities;
- frozen causal inputs;
- exact ruleset/package evidence;
- fixed RNG evidence and receipts;
- owner-qualified currentness/provenance required for continuation.

### WP20-L22 — No ambient reinterpretation

Migration shall not:

- rebind accepted work to target ambient rules;
- reroll accepted randomness;
- reconstruct hidden LLM reasoning;
- silently discard accepted closure;
- reinterpret prior accepted evidence merely because the target runtime changed.

If the target cannot prove safe interpretation, migration/adoption is blocked until the existing owner supplies a lawful compatible closure/continuation path.

---

## 11. Transformation scope

### WP20-L23 — Declared authoritative scope only

Only authoritative native paths/families declared by the selected edge path may be transformed.

Unrelated canon/history/state remains unchanged according to its owner. Migration is not authorization for opportunistic cleanup, compaction, ID renumbering or semantic reinterpretation.

### WP20-L24 — Preserve stable authority and identity

Unless an explicit accepted target edge changes physical representation while preserving semantics, retain:

- campaign identity and creator authority;
- stable entity/PLAYER/event/command/resolution/continuation identities;
- owner direction, including directed relation semantics;
- truth/knowledge/disclosure separation;
- chronology/history/causal evidence;
- lifecycle/readiness/current-routing semantics;
- House Rules/policy authority and provenance;
- multiplayer binding/agency/currentness;
- recovery-safe durability/resumability;
- immutable `created_with` history;
- exact package/ruleset evidence needed to interpret retained state.

### WP20-L25 — Branch-persistent derived/index state

A branch-persistent derived/index projection whose source authority changes may be deterministically rebuilt from the prepared migrated authoritative state when its owner permits rebuild and the target requires the projection.

Such rebuild may join the prepared campaign transaction. The projection never becomes migration input authority.

### WP20-L26 — Local HOT/runtime cache

HOT/SQLite/local runtime/instruction caches are non-authoritative. They do not join campaign publication and are invalidated/rebuilt only after authoritative migration publication is confirmed.

### WP20-L27 — Other projections

Story and other owner-specific noncanonical/asynchronous projections use their existing catch-up/rebuild law; migration does not promote them into authority.

---

## 12. Preparation and validation

### WP20-L28 — No authority change during preparation

Architecture-level preparation is:

```text
resolve creator authority
-> pin campaign H + required currentness evidence
-> resolve exact target package
-> build bounded CEE
-> classify
-> satisfy storage/LIVE/accepted-work prerequisites
-> select exact directed path if required
-> transform only declared native scope in a prepared tree
-> rebuild required branch-persistent projections
-> validate target contracts/invariants
-> prepare bounded migration evidence
```

Successful transformation and validation is only `PREPARED` and has no campaign authority.

---

## 13. Authoritative migration publication

### WP20-L29 — Reuse existing campaign tree transaction

A campaign migration/adoption publishes through the existing campaign publication contract:

```text
one complete prepared tree
-> one commit parented to pinned H
-> one non-force campaign-ref CAS/update
```

No migration-specific second currentness/publication authority is introduced.

### WP20-L30 — Durable success

Only confirmed accepted ref publication establishes durable migration/adoption success.

Target runtime binding and post-publication local cache rebuild occur only after that authority change is confirmed.

### WP20-L31 — Rejected publication

If the ref moved/CAS is rejected, the current ref remains authority. Prepared commit/objects have no campaign authority. Re-evaluate from current authority; do not force or blind-merge.

### WP20-L32 — Ambiguous publication

If transport result is unknown, use the existing bounded authoritative ref read-back:

- ref equals prepared commit -> accepted;
- ref proves another current successor/head -> rejected/stale;
- outcome still cannot be proven -> indeterminate/recovery state.

Never blind-retry authority-changing migration publication.

---

## 14. Rollback / reverse / downgrade

### WP20-L33 — Before accepted publication

Abort/discard prepared state. If publication was rejected, current old authority already remains in place. No rollback transaction is needed.

### WP20-L34 — After accepted publication

A prior checkpoint, old ref or old release is not generic rollback authority.

A downgrade/reverse transition is supported only by a separately declared reverse edge/path applicable to the exact current source and exact older target. It executes as a **new forward creator-authorized campaign publication** under current CEE/currentness/LIVE/accepted-work rules.

---

## 15. Unsupported older/newer states

### WP20-L35 — Missing source/support material

Never substitute mutable latest/main/current-tag state for missing exact source or migration support material. Missing required immutable evidence yields `UNSUPPORTED_INCOMPATIBLE` or `INDETERMINATE` according to whether non-support or uncertainty is proven.

### WP20-L36 — Unsupported newer state fails closed

An older runtime encountering a campaign/schema/ruleset/storage contract it does not explicitly support must fail closed. Parse success, numeric decrement or guessed reverse transformation is not compatibility.

---

## 16. Migration provenance

### WP20-L37 — Evidence, not authority

Use an existing admitted maintenance/audit/history allocation or a later realization of that allocation for bounded migration evidence. The evidence is never a second publication/currentness owner.

Logically preserve at least:

```text
pinned source campaign HEAD / source-envelope identity
exact target runtime/package identity
ordered selected migration edge IDs
immutable edge artifact identities
creator/authorization basis
validation outcome
```

The resulting campaign ref/commit remains authoritative publication identity.

### WP20-L38 — No circular containing-commit requirement

A migration evidence record contained in the publication shall not be required to embed its own final containing commit hash. Source basis and immutable edge/target identities provide pre-publication provenance; the published ref/commit identifies the resulting authoritative tree externally.

---

## 17. Current supersession map

### WP20-L39 — Historical same-version ancestry inference superseded for released v1.0+

Historical 2026-08-18 update/provenance designs remain useful provenance and retain these accepted principles where not otherwise superseded:

- storage baseline and campaign current identity are separate;
- local runtime root is ephemeral;
- package-carried exact provenance is preferable to mutable tag inference;
- a non-creator cannot persist creator-owned campaign adoption identity.

For **released v1.0+**, any historical rule that treats same semantic version/package ID plus proven Git descendant ancestry as sufficient compatibility/silent-use authority is superseded by this specification.

Git ancestry remains provenance evidence only. Different released bytes require affirmative exact-target compatibility support.

### WP20-L40 — Pre-release migration examples are non-authoritative for current scope

Any historical `0.8`, pre-release scaffold or “legacy CAMPAIGN/” example does not establish a current migration obligation. Current regression language must describe released-v1.0+ source layouts unless explicitly discussing history.

---

## 18. Realization boundary

Architecture is complete here; realization remains deferred until the full R2.7 sequence and implementation-planning gates authorize it.

Later realization must decide/implement, without changing these laws unless architecture is explicitly reopened:

- exact machine schema/serialization for compatibility declarations and migration edges;
- transform artifact/module format and safe execution boundary;
- compatibility evaluator/path resolver;
- release-builder/package validation for complete immutable migration support;
- target schema/data validators and fixtures;
- executable migration/update/recovery tests;
- implementation plan and TDD execution.

WP-20 Steps 2–8 do not authorize those changes.

---

## 19. Required regression classes for later realization

At minimum, later implementation/testing must cover:

1. equality of one/many version axes does not imply compatibility;
2. source ancestry alone does not imply released same-version compatibility;
3. explicit direct compatibility succeeds without transform;
4. migration required only by explicit path;
5. no path -> unsupported;
6. multiple undeclared valid paths -> indeterminate;
7. unsupported newer local schema/campaign/storage/ruleset contract fails closed;
8. storage migration and campaign migration retain separate authority/outcomes;
9. active LIVE blocks migration;
10. CLOSED-unabsorbed LIVE blocks migration;
11. accepted-work interpretation incompatibility blocks migration;
12. branch ref movement invalidates prepared migration;
13. rejected publication leaves old authority unchanged;
14. ambiguous publication uses bounded read-back, not blind retry;
15. reverse/downgrade requires explicit reverse edge and new forward publication;
16. branch-persistent derived projection rebuild versus local HOT post-publication rebuild;
17. unrelated canon/stable IDs/history preserved;
18. pre-release/v0.8 layout has no compatibility obligation.

---

## 20. Final architecture result

```text
SELECTED_ARCHITECTURE:
  IMMUTABLE EXACT-TARGET PACKAGE-SCOPED COMPATIBILITY EVIDENCE
  + EXPLICIT DIRECTED MIGRATION-EDGE GRAPH
  + EXISTING CREATOR / STORAGE / LIVE / RECOVERY / CAS OWNERS

MUTABLE_GLOBAL_MIGRATION_REGISTRY: NO
VERSION_ORDER_AS_COMPATIBILITY: NO
GIT_ANCESTRY_AS_RELEASED_COMPATIBILITY: NO
AUTOMATIC_REVERSE_OR_REF_REWIND: NO
PRE_RELEASE_COMPATIBILITY: NONE
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
IMPLEMENTATION_AUTHORIZED: NO
REAL_MIGRATION_EXECUTED: NO
```
