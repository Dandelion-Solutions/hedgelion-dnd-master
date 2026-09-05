# R2.7 WP-20 Step 2 — Research & Architecture Draft

Status: **STEP 2 COMPLETE — RESEARCH / ARCHITECTURE DRAFT**

Date: 2026-09-05

Domain: **Engine update / schema evolution / migration**

Step-1 authority:

- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-architecture-task-brief.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-task-brief-critic.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-step-1-senior-review.md` — mandatory Senior PASS / GO for Steps 2–8.

This artifact executes the accepted Step-1 brief. It is design provenance, not final implementation-facing authority.

---

## 1. Scope and fixed boundaries

The compatibility horizon begins with **released HDM v1.0+ campaigns**.

The following are out of scope by Product Owner decision:

- v0.8/pre-release campaign compatibility;
- pre-release scaffold import/migration;
- dual-read/dual-write or shims retained only for pre-release state;
- rollback to v0.8;
- preservation of obsolete pre-release layouts solely because they once existed.

The accepted versioning taxonomy is an upstream invariant and was not reopened:

```text
engine release              -> MAJOR.MINOR[-prerelease]
engine-bound component      -> ENGINE_MAJOR.ENGINE_MINOR.REVISION
independent contract/state  -> owner-local revision/schema_version/generation
```

Ordering/equality inside any one namespace is not compatibility proof. Different namespaces are not numerically comparable.

No implementation planning, migration execution, code realization, real campaign migration or WP-21 work is part of Step 2.

---

## 2. Refined Source Manifest and evidence disposition

### 2.1 Process / current state

| Source | Role | Step-2 disposition |
|---|---|---|
| `AGENTS.md` | repository governance | Connector-only remote authority; no branch creation; current owners beat summaries; Step-8 synchronization required |
| `DEV/DESIGN_PROCESS.md` | canonical process | source/evidence completeness, alternatives, challenge and eight-step loop apply |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | HDM adapter | whole-project critic, finding propagation and Step-8 Senior stop apply |
| `DEV/PROJECT_MAP.md` | derivative routing | used to reconstruct update/persistence/LIVE/ruleset/schema dependency subgraph |
| `DEV/CURRENT_PROGRESS.md` | current-progress authority | WP-20 Step 2 authorized; no blocker at entry |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | sequencing only | WP-20 precedes WP-21 and later final reconciliation |

### 2.2 Product / version law

| Source | Role | Step-2 disposition |
|---|---|---|
| `DEV/PRODUCT_OWNER_INPUT.md` PO-004 | Product Owner input | v1.0 clean-slate boundary is mandatory |
| `DEV/docs/superpowers/specs/2026-09-05-hdm-v1-clean-slate-compatibility-owner-decision.md` | accepted product semantics | compatibility obligation starts at released v1.0; `NEEDS_PO: NONE` |
| `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md` | canonical version/compatibility law | retained unchanged; explicit compatibility/migration evidence is required |
| `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-machine-realization-status-amendment.md` | current realization status | current numbering/generation machine baseline is complete; migration architecture is not yet realized |
| `DEV/RELEASE/VERSIONING.md` | release/version policy | released assets are immutable; version numbers never manufacture compatibility |
| `GAME/ENGINE_VERSION.yaml` | shipped runtime contract | current development value is `1.0-alpha`; `campaign_update.compatibility` is only a coarse route/hint, not proof |

### 2.3 Identity / bootstrap / package set

| Source | Role | Step-2 disposition |
|---|---|---|
| WP-19 final canonical spec | current campaign-creation composition owner | new campaign freezes exact runtime/ruleset identity; storage baseline is New Game only; existing campaign uses its own current identity |
| `GAME/SCHEMA/campaign_manifest.schema.yaml` | machine contract | `created_with` is immutable provenance; `current` is creator-controlled adoption state; campaign contract generation is an aggregate axis |
| `GAME/SCHEMA/dnd_storage.schema.yaml` | machine contract | storage format and storage baseline are a separate storage-default authority |
| `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` | ruleset identity owner | exact ordered ruleset-set digest is identity; compatibility family/generation is semantic compatibility evidence; revision/order is not compatibility proof |
| runtime-package provenance amendment | package provenance owner | exact built artifact provenance comes from package-carried immutable evidence, never mutable current tag position |

### 2.4 Persistent state / schemas

The current physical schema directory was inspected structurally. `GAME/SCHEMA/README.md` identifies the principal persistent contracts and establishes the current rule:

- artifact-local `schema_version` belongs only to that contract;
- additive optional change may remain on the same local version;
- breaking required-form/semantic change requires a local bump;
- released persisted data requiring transformation needs an explicit migration edge;
- `campaign_contract_generation` and `storage_format_generation` are separate aggregate axes and do not replace local schema versions.

WP-10 and WP-11 were reconciled at the logical-family level. Native authority includes world/entity state, runtime accepted-work families, semantic/mechanical evidence, chronology/history/disclosure/message families and operational currentness. Physical schema presence is not itself semantic ownership, and not every logical family is required to have a one-file/one-schema physical representation.

**Step-2 rule:** compatibility classification inspects the local schema/version predicates actually relevant to the authoritative records being opened/transformed. It does not invent a global schema version and does not require the campaign MANIFEST to duplicate every family-local version.

### 2.5 Publication / recovery / concurrency

| Owner | Preserved law |
|---|---|
| WP-13 + `GAME/CORE/PERSISTENCE.md` | one coherent campaign tree commit, pinned parent/read basis, non-force ref CAS; prepared objects are not success |
| WP-13 ambiguous publication law | bounded ref read-back determines accepted/rejected/indeterminate outcome; no blind retry |
| WP-14 | recovery starts from current authority; unsupported/newer/ambiguous state fails closed rather than guessed repair |
| WP-15 | chronology/process identities, causal evidence and stable order semantics survive transformation |
| WP-16 | LIVE may temporarily own selected mutable state; branch-only migration is invalid while LIVE authority or unabsorbed closed LIVE state remains |
| Step-5.2 resumable runtime closure | accepted work freezes causal/ruleset/RNG/provenance inputs; a target runtime must be able to interpret that closure without ambient rebind/reroll |

### 2.6 Access-control reconciliation

`DEV/ARCHITECTURE/ACCESS_CONTROL.md` contains one broad historical sentence saying campaign engine maintenance is storage-owner maintenance, but the same current owner explicitly defines:

- storage default branch maintenance as storage-owner-only;
- explicit engine/ruleset adoption/migration as creator-only;
- persistence of campaign engine/ruleset identity changes as creator-only;
- repository permission as insufficient authority.

`GAME/CORE/ENGINE_UPDATES.md` independently says semantic campaign adoption is creator-controlled and storage baseline is a separate storage-owner transaction.

**Disposition:** existing-campaign semantic migration/adoption is creator-only. Storage-format/default-baseline maintenance is storage-owner-only. The broad sentence is stale/overbroad wording and can be mechanically repaired; no Product Owner decision is required.

### 2.7 Derived state and caches

WP-11/WP-12 distinguish authoritative native state from indexes and local HOT/SQLite projections.

**Disposition:**

- authoritative native records may require explicit migration;
- branch-persistent derived/index material required by the target may be deterministically rebuilt from migrated authority inside the target campaign transaction;
- local HOT/SQLite cache is invalidated/rebuilt after authoritative publication and never participates as migration authority;
- Story/other projections remain subject to their existing owner-specific rebuild/catch-up law.

### 2.8 Current migration/update surfaces

`GAME/MIGRATIONS/README.md` already has the correct high-level direction that explicit source/target campaign/schema predicates are required and storage migration is separate. It is incomplete on graph/path ambiguity, publication outcomes, LIVE absorption, accepted-work closure and reverse-edge semantics.

`DEV/TESTS/ENGINE_UPDATE_CASES.md` preserves useful safety cases, but its `Legacy CAMPAIGN/` compatibility example is pre-clean-slate provenance and cannot imply a v0.8 compatibility obligation.

`GAME/CORE/ENGINE_UPDATES.md` still contains a pre-release-era same-semantic-version rule that treats proven source ancestry as sufficient compatibility for a silent released-package refresh. That conflicts with the accepted released-asset immutability and explicit-compatibility law for the v1.0+ horizon. Source ancestry remains provenance evidence but cannot itself establish released compatibility.

---

## 3. Compatibility model

### 3.1 Compatibility Evidence Envelope (CEE)

Compatibility is evaluated from a **bounded typed evidence envelope**, not one version scalar.

For a selected campaign and exact candidate runtime, the envelope contains as applicable:

```text
campaign branch/ref + pinned current HEAD
campaign_id + authoritative creator identity
MANIFEST.engine.current:
  engine identity/version
  campaign_contract_generation
  exact package provenance/digest identity
MANIFEST.ruleset.current:
  exact ordered ruleset-set digest identity
  compatibility family/generation evidence
  catalog generation evidence when applicable
relevant authoritative persistent-family schema_version predicates
storage_format_generation as a separate prerequisite axis
accepted-work / resumable-runtime compatibility evidence
LIVE ownership/absorption/currentness evidence
exact immutable target runtime/package identity
explicit migration-edge set shipped for that target
```

The envelope is evidence. It is not a new durable campaign owner or global registry.

### 3.2 Finite classification

Evaluation returns exactly one of:

```text
DIRECT_COMPATIBLE
MAINTENANCE_REFRESH
MIGRATION_REQUIRED
UNSUPPORTED_INCOMPATIBLE
INDETERMINATE
```

Meanings:

- `DIRECT_COMPATIBLE` — target can operate without authoritative persistent transformation; exact eligibility has been proven.
- `MAINTENANCE_REFRESH` — only nonsemantic/rebuildable/local/projection maintenance is required; no campaign semantic adoption transform is inferred from this label.
- `MIGRATION_REQUIRED` — an explicit valid directed path exists and authoritative campaign transformation is required before target adoption.
- `UNSUPPORTED_INCOMPATIBLE` — target explicitly does not support the source, a required edge/artifact is absent, a newer unsupported contract is encountered, or a preserved closure cannot be interpreted safely.
- `INDETERMINATE` — evidence is insufficient/ambiguous or currentness cannot be proven. This is fail-closed and retry/re-evaluate, not best-effort migration.

`campaign_update.compatibility` remains only a coarse discovery/routing signal into this evaluator.

---

## 4. Explicit migration graph

### 4.1 Ownership and scope

The migration graph is **immutable package-scoped support data shipped with an exact released target runtime**, not a network service, mutable global registry or campaign-owned authority.

A migration edge declares at minimum:

```text
edge_id
source compatibility predicate
exact target predicate
affected authoritative family/contract predicates
required prerequisites/dependencies
ordered transform identity
post-transform validation obligations
immutable edge artifact/provenance identity
```

The exact machine shape remains later realization work.

### 4.2 Directionality

Edges are directed. Numeric adjacency, lexical ordering, engine-version ordering, revision/generation ordering, Git ancestry and timestamps never create an edge.

A reverse/downgrade path exists only as a separately declared reverse edge with its own source/target predicates and preservation proof.

### 4.3 Deterministic path selection

For a source envelope and exact target package:

1. retain only edges whose source predicate is fully proven;
2. retain only compositions whose dependencies and intermediate target/source predicates compose exactly;
3. reject cycles for the selected active path;
4. reject any path that requires absent immutable edge code/data or unsupported intermediate contract;
5. if no path remains -> `UNSUPPORTED_INCOMPATIBLE`;
6. if one valid path remains -> select it;
7. if several valid paths remain, use only a canonical path/order explicitly declared by the exact target package;
8. if multiple paths remain without such declaration -> `INDETERMINATE`.

There is no lexicographic, shortest-path, highest-version or newest-commit tie-breaker.

---

## 5. Authority and transaction composition

### 5.1 Storage versus campaign

`storage_format_generation` belongs to storage-default authority. Storage-format migration is therefore a separate storage-owner maintenance operation.

A campaign migration:

- does not mutate the storage default marker;
- does not gain authority from storage ownership;
- does not imply sibling-campaign migration.

A storage migration:

- does not adopt a runtime/ruleset for a campaign;
- does not rewrite creator-owned campaign current identity merely because the storage owner can write the repository.

If a storage evolution also requires per-campaign native transformations, those transformations are explicit campaign migration edges executed under campaign creator authority, not hidden side effects of storage maintenance.

### 5.2 Campaign creator authority

Any operation that changes creator-controlled `MANIFEST.*.current` adoption identity or transforms authoritative campaign semantic/native state is creator-only.

A non-creator may use an exact runtime only where the target proves direct compatibility and no creator-owned manifest/native mutation is required.

### 5.3 LIVE prerequisite

Campaign migration requires a branch-authoritative durable frontier:

```text
no active LIVE-selected mutable authority
AND
no CLOSED LIVE state awaiting required absorption/reconciliation
AND
campaign HEAD/currentness basis proven
```

No migration-specific global lock/epoch is introduced. Existing LIVE close/absorb and CAS/currentness owners are reused.

### 5.4 Accepted work prerequisite

Before target adoption, the exact target must prove it can interpret every preserved accepted-work closure that remains resumable/current under existing owners, including frozen causal inputs, ruleset/package identity, RNG evidence, continuations and receipts where applicable.

If it cannot, migration/adoption is blocked. The runtime must finish/resolve the accepted work under a valid compatible runtime or follow another explicit owner-defined closure path; it may not rebind to target ambient rules, reroll or reconstruct hidden reasoning.

---

## 6. Migration execution and publication semantics

Architecture-level execution sequence:

```text
resolve creator authority
-> pin campaign ref + exact HEAD H
-> build CEE from H and exact target package
-> classify compatibility
-> require LIVE/accepted-work/storage prerequisites
-> select explicit deterministic edge path, if needed
-> transform only declared authoritative native scope in a prepared tree
-> deterministically rebuild required branch-persistent derived/index state
-> validate target contracts/invariants
-> include migration provenance evidence
-> publish through existing CAMPAIGN_TREE_TXN as one commit parented to H
-> non-force ref CAS
-> bounded read-back on ambiguous transport
-> only then bind/report target adoption success
-> invalidate/rebuild local HOT/runtime caches after authoritative success
```

A ref move during preparation invalidates the basis: abort/re-evaluate from the new current authority. Do not merge a prepared migration into a moved head and do not force.

### 6.1 Outcomes

- Local transform/validation success is only **PREPARED**.
- CAS accepted and confirmed -> migration/adoption **DURABLE SUCCESS**.
- CAS rejected/ref moved -> old ref remains authority; migration did not happen.
- Transport result unknown -> bounded ref read-back classifies accepted/rejected/indeterminate; never blind retry.
- An unreachable created commit/object has no campaign authority.

### 6.2 Rollback / downgrade

Before authoritative publication, rollback means discard/abort prepared work.

After a rejected publication, the old ref is still authority; no rollback transaction is needed.

After a confirmed accepted migration, checkpoint/ref rewind is not normal rollback authority. A downgrade requires a separately declared reverse migration edge and is published as a new forward campaign transaction under current creator/currentness/compatibility rules.

---

## 7. Preservation invariants

A valid migration preserves, unless an explicit accepted owner law for the target changes representation while preserving semantics:

- campaign identity and creator authority;
- stable entity/record identities and owner relationships;
- accepted command/resolution/continuation/receipt identities and frozen causal/RNG inputs;
- objective truth, knowledge, disclosure and private/public separation;
- chronology, history and causal evidence;
- lifecycle/readiness/current routing semantics;
- House Rules/policy authority and provenance;
- multiplayer PLAYER identity/authority and currentness;
- recovery-safe durable frontier and resumability;
- `created_with` historical provenance;
- exact ruleset/package provenance required to interpret retained state.

A migration is not permission to rewrite unrelated canon, renumber stable IDs, compact history opportunistically or reinterpret old evidence under current ambient rules.

---

## 8. Provenance

Use existing logical maintenance/audit/history allocation where realization provides it; do not create a second publication authority.

Migration evidence must be sufficient to recover at least:

```text
pinned source campaign HEAD / source envelope identity
exact target runtime/package identity
selected ordered edge IDs + immutable edge artifact identities
creator/authorization basis
validation result
```

The resulting campaign ref/commit remains authoritative publication identity. A migration evidence record is evidence only and must not attempt to self-embed the final commit hash that contains itself.

---

## 9. Alternatives

### Alternative A — package-scoped explicit graph + existing owners (**recommended**)

Benefits:
- deterministic and replay/audit friendly;
- no duplicate currentness/publication authority;
- supports multi-axis compatibility without collapsing namespaces;
- unsupported states fail closed;
- release support can remain finite and immutable.

Cost:
- every supported transformation needs explicit edge/support metadata;
- target release packaging and tests must later realize/validate the graph.

### Alternative B — mutable central migration/compatibility registry

Benefits:
- convenient global discovery.

Rejected because:
- creates a new mutable authority and availability/currentness problem;
- conflicts with exact offline/package-scoped runtime model;
- complicates replay and old-release support;
- current requirements do not need a service.

### Alternative C — infer compatibility/path from version/generation order or source ancestry

Benefits:
- smallest metadata surface.

Rejected because:
- contradicts accepted versioning law;
- cannot represent skipped/unsupported transitions, semantic incompatibility or independent axes;
- makes migration support accidental.

### Alternative D — direct-only, no composed edges

Benefits:
- simplest runtime path selection.

Not selected as a hard law because finite explicit composition is safe when intermediate predicates and edge dependencies compose exactly. The target package may still ship a direct edge when that is operationally preferable.

---

## 10. Analytical challenge

Strongest opposing case against Alternative A: an explicit graph can become release-maintenance overhead, and deterministic composition can look like infrastructure for hypothetical migration complexity.

Why it still wins: the graph is not a runtime service or generic scheduler. It is finite immutable support data only for actually supported released transitions. Without explicit edges, the accepted independent version axes provide no lawful way to infer transformation support.

Simplest viable comparison: a table of direct source->target transforms is a graph with out-degree constrained by packaging. The selected architecture allows that simple realization and does not require a graph database/registry.

Recommendation confidence: **HIGH**.

Evidence that would change the recommendation:

- an accepted owner constraining released support to direct one-step migration only and forbidding composition;
- a new hosting requirement making exact target packages unavailable/offline-incomplete and requiring an external compatibility service;
- proof that campaign currentness/publication must span several independently authoritative stores atomically rather than composing existing per-owner transactions.

None is present in current scope.

---

## 11. Answers to Q20-01…Q20-17

| Question | Step-2 answer |
|---|---|
| Q20-01 | CEE: exact bounded tuple of campaign/runtime/ruleset/schema/storage/accepted-work/LIVE evidence |
| Q20-02 | five finite outcomes: direct compatible, maintenance refresh, migration required, unsupported incompatible, indeterminate |
| Q20-03 | relations are explicit predicates across independent axes; no scalar collapse |
| Q20-04 | immutable explicit directed package-scoped edge graph with deterministic composition/path declaration |
| Q20-05 | direction is edge-local only; reverse is separate edge |
| Q20-06 | preserve IDs, owners, accepted work, truth/knowledge/disclosure, chronology, lifecycle, policy, multiplayer, recovery/provenance |
| Q20-07 | creator owns campaign adoption/migration; storage owner owns storage-default evolution |
| Q20-08 | authoritative migration publication is existing single campaign-tree CAS transaction |
| Q20-09 | prepared success != published success; reject leaves old authority unchanged |
| Q20-10 | ambiguous publish uses bounded read-back; no blind retry |
| Q20-11 | moved HEAD/LIVE/unabsorbed state blocks preparation/publication until current basis is re-established |
| Q20-12 | missing required old support/edge artifact means unsupported; never use mutable latest/main substitution |
| Q20-13 | unsupported newer contract/generation fails closed |
| Q20-14 | abort before publish; reverse only explicit separately supported edge after publish |
| Q20-15 | native authority transforms; branch-derived indexes rebuild; local HOT rebuilds after publish |
| Q20-16 | current migration/runtime docs and test catalog need targeted reconciliation; graph machine realization remains later work |
| Q20-17 | this WP owns architecture/spec + documentary owner synchronization only; code/schema/tool/executable-test realization remains post-R2.7 implementation work |

`HUMAN_DECISION_REQUIRED: NO`

`NEEDS_PO: NONE`
