# S6D-01 — Ruleset / Package / Catalog Snapshot Identity — Research & Architecture Draft

Status: **STEP 2 COMPLETE / RESEARCH SYNTHESIS / NOT CANONICAL**

Date: 2026-08-25

Task brief:

- `DEV/docs/superpowers/specs/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-task-brief.md`

This artifact completes Step 2 only. It does not canonicalize the recommendation, begin S6D-02, or implement package/schema/runtime changes.

## 1. Executive result

The current repository has five useful but non-equivalent identity surfaces:

1. `GAME/ENGINE_VERSION.yaml` — semantic installed-engine projection;
2. generated `RUNTIME_PACKAGE.yaml` — exact built-artifact provenance, but not its own ZIP digest and not a ruleset snapshot lock;
3. `MANIFEST.engine.created_with/current` — campaign creation/adoption provenance and exact accepted runtime ZIP digest;
4. coordinated DEV catalog generation (`2.0.0`) — machine-contract generation, not selected reusable-definition content;
5. `runtime.resolution` / `runtime.continuation.catalog_context_fingerprint` — accepted execution fingerprint, but not a reconstructive package locator.

None can be renamed into the missing contract. The minimum coherent architecture is:

```text
ruleset package semantic manifest(s)
    + exact content identities
    + exact dependency closure/order-independent set identity
    + engine/catalog compatibility requirements
    + namespace claims
        -> ResolvedRulesetSnapshotSet

engine capability identity
    + ResolvedRulesetSnapshotSet identity
    + campaign-definition owner-local frontier
    + optional session-overlay owner-local frontier
        -> derived ResolvedCatalogContext fingerprint
```

The resolved ruleset set identity is exact, content-addressed and reconstructive. The full `ResolvedCatalogContext` fingerprint is derived comparison evidence, not a stored global snapshot owner. Natural owners retain only the projections they need: runtime package advertises its embedded ruleset lock; campaign adoption records the selected ruleset-set identity; accepted execution records the exact ruleset-set identity plus its context fingerprint; recovery resolves those projections through existing owner-native routes.

No product-semantic or material-risk decision remains. The recommendation follows from already accepted no-shadowing, pinned-execution, package-isolation, creator-adoption, recovery-nonauthority and clean-slate laws.

## 2. Source Manifest completion

### Process, status and scope authorities

| Source | Role | Inspection/disposition |
|---|---|---|
| `AGENTS.md` | CANONICAL PROCESS / REPOSITORY | Read current on authoritative ref; Connector-only publication, GAME/DEV boundary and evidence gates apply |
| `DEV/DESIGN_PROCESS.md` | CANONICAL PROCESS | Read current; Source Manifest, item-level synthesis and Steps 2–8 gates apply |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | CANONICAL HDM ADAPTER | Read current; whole-project dependency route and owner/consumer distinction apply |
| `DEV/PROJECT_MAP.md` | DERIVATIVE LOCATOR | Used to route catalog, release, campaign, execution, recovery, House Rules and tests; never used as semantic authority |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | STATUS AUTHORITY | S6D-01 sole active domain; Step 1 complete; R2.7 WP-06 paused |
| S6D owner decision, workstream brief and sequencing decision | OWNER / DECOMPOSITION AUTHORITIES | Read item-level; obligations 1 and 10 are S6D-01, no legacy-campaign compatibility, each domain gets full loop |
| `DEV/docs/superpowers/research/2026-08-24-r2-7-audit-status.md` | DURABLE PAUSE AUTHORITY | Read current; catalog generation 2.0.0 and engine 1.0-alpha are distinct; no frozen pre-release compatibility |

### Catalog identity owners and assurance

| Source | Role | Inspection/disposition |
|---|---|---|
| `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md` | CANONICAL OWNER | Read fully; one context, no shadowing, package namespace ownership, exact content/compatibility identity and reconstructive frontier required |
| `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md` | CANONICAL OWNER | Read fully; definitions are stable namespaced semantic IDs; no per-world-record version repetition; no unpublished durable dependency |
| `DEV/ARCHITECTURE/CATALOG_INVENTORY.md` | CANONICAL INVENTORY | Read fully; runtime/value classes do not create a package snapshot owner; catalog generation remains coordinated pre-release machine vocabulary |
| Step-1 meta-model/evolution resolutions | CANONICAL ASSURANCE | Read fully; package-level identity and locked dependency set are deferred concrete work, not optional semantics |
| Steps-1/2 retrospective assurance final | CANONICAL INTEGRATION ASSURANCE | Read fully; Resolution/Continuation pin context, checkpoints do not own mutable truth, exact Step-6 identity remains residual |
| `DEV/CATALOG/*.json` and core catalog schemas | CURRENT MACHINE CONTRACT | Read all four coordinated catalogs and relevant schemas; only `catalog_version: 2.0.0` exists, with no ruleset package lock |
| R2.7 WP-03 mini-report and catalog tests | RESEARCH + EXECUTABLE EVIDENCE | Item-level review; engine and catalog axes separated, catalog family equality enforced, package reconstruction untested |

### Runtime package, release and campaign adoption owners

| Source | Role | Inspection/disposition |
|---|---|---|
| `DEV/ENGINE_DEVELOPMENT.yaml`; `GAME/ENGINE_VERSION.yaml` | DEVELOPMENT OWNER + SHIPPED PROJECTION | Read current; engine/rules baseline/schema/update fields exist, but no exact ruleset content identity |
| engine-version split amendment | CANONICAL AMENDMENT | Read fully; runtime never reads DEV metadata; shared-field parity is build-time validation |
| runtime-package provenance amendment | CANONICAL AMENDMENT | Read fully; generated artifact provenance is separate from semantic version; exact ZIP digest is external |
| release-migration safety addendum | CANONICAL AMENDMENT | Read applicable sections; runtime ZIP shape/provenance and release lineage do not prove ruleset semantic compatibility |
| `DEV/ARCHITECTURE/BRANCH_MODEL.md`; `DEV/RELEASE/VERSIONING.md` | CANONICAL TOPOLOGY / VERSIONING | Read fully; runtime source, local package and campaign storage are different surfaces |
| `DEV/TOOLS/release_builder.py`; release checklist/tests | MACHINE OWNER / EXECUTABLE EVIDENCE | Read relevant code and tests; generated `RUNTIME_PACKAGE.yaml` has seven exact fields and no ruleset lock; deterministic composition exists |
| `GAME/CORE/BOOTSTRAP_RUNTIME.md` | SHIPPED RUNTIME OWNER | Read fully; runtime binds one validated local root, never mixes cache roots, and validates artifact provenance |
| `GAME/CORE/ENGINE_UPDATES.md` | SHIPPED ADOPTION OWNER | Read fully; same-version descendant currently treated as compatible using ancestry, which is insufficient when ruleset snapshot meaning changes |
| `GAME/CAMPAIGN/MANIFEST.yaml`; schema; `GAME/TOOLS/init_campaign.py` | CAMPAIGN PROJECTION / MACHINE REALIZATION | Read fully; campaign records engine version/package/source/digest but no ruleset-set identity |
| update, mismatch, multi-runtime, provenance and release integration tests | EXECUTABLE EVIDENCE | Read; current behavior enforces package provenance and campaign adoption but cannot distinguish same-version ruleset changes |

### Accepted execution, recovery, cleanup and House Rules consumers

| Source | Role | Inspection/disposition |
|---|---|---|
| Step-3 execution canonical spec and Activity/Rule Element owners | CANONICAL EXECUTION | Read applicable sections; accepted execution freezes bindings/RNG/context and rejects ambient reinterpretation |
| Resolution/Continuation/receipt/procedure schemas | CURRENT MACHINE CONTRACT | Read; continuation carries `catalog_context_fingerprint` and dependency refs, but no exact ruleset-set locator |
| Step-5.2 canonical spec | CANONICAL RECOVERY OWNER | Read fully; accepted interpretation evidence must remain recoverable; natural owners and bounded routing remain authority |
| Step-5.7 canonical spec | CANONICAL CHECKPOINT OWNER | Read applicable laws; checkpoint optional/nonauthoritative, engine data diagnostic only, accepted work resolves its own pinned dependencies |
| Step-5.13 canonical spec | CANONICAL CLEANUP OWNER | Read applicable laws; interpretation compatibility affects retention; exact required snapshots cannot retire while promised consumers depend on them |
| `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` and shipped policy/sidecar/schema/tests | CANONICAL POLICY OWNER + MACHINE CONSUMER | Read fully; `realization_refs` are linkage, not execution authority; current catalog validation remains mandatory; no package fork is implied |
| R2.7 WP-06 mini-report | CURRENT RESEARCH CHECKPOINT | Read item-level; rules/adjudication gaps remain paused; no evidence creates another package identity owner |

### Search/completeness result

Concrete searches/extractions covered `ResolvedCatalogContext`, `catalog_context_fingerprint`, `catalog_version`, `engine_version`, `rules_baseline`, `RUNTIME_PACKAGE`, `package_id`, `package_sha256`, source SHA/ref, compatibility, namespace, dependency frontier, Continuation, checkpoint, House Rules realization and cleanup compatibility across owning source families and focused tests. No current ruleset-package semantic manifest, exact ruleset-set digest or campaign/Continuation ruleset snapshot projection exists.

## 3. Item-level evidence ledger

| Item | Actual current claim | Qualifier / negative evidence | Disposition |
|---|---|---|---|
| E-01 | `ResolvedCatalogContext` includes engine capability, selected ruleset package set, campaign frontier and optional session frontier | It is logical context, not a new world entity | Preserve as derived composition |
| E-02 | One `definition_id` maps to at most one reusable definition per context | Layer order is not shadow precedence | Package loader rejects duplicate IDs/namespaces |
| E-03 | Namespace ownership belongs at package/context level | No global internet registry required | Manifest declares claims; validation is local/bounded |
| E-04 | `catalog_version` identifies engine machine-catalog contract | It does not identify complete selected reusable definitions | Rename nothing; keep separate generation axis |
| E-05 | `rules_baseline` is human-readable baseline metadata | Insufficient exact package identity | Retain as presentation/legal baseline only |
| E-06 | `engine_version` is semantic installed-engine identity | Same engine version may have different artifact/source bytes | Use as engine capability requirement, not content digest |
| E-07 | generated runtime package metadata proves artifact source state/ref/SHA | It cannot self-contain final ZIP digest and currently lacks ruleset lock | Extend generated metadata with resolved ruleset snapshot set |
| E-08 | campaign `engine.current.package_sha256` identifies exact accepted ZIP | Exact artifact bytes are broader than reusable definitions and same-version refresh may change them | Add separate ruleset-set projection; do not infer it from ZIP digest alone |
| E-09 | same-version descendant source ancestry currently allows silent refresh | Ancestry proves provenance, not catalog semantic compatibility | Require exact same ruleset-set identity for nonsemantic refresh; changed ruleset set is semantic adoption |
| E-10 | Continuation stores opaque catalog context fingerprint and dependency frontier refs | Fingerprint compares but does not locate an old ruleset snapshot | Add exact resolved ruleset-set identity to accepted execution owner |
| E-11 | accepted work cannot be reinterpreted under incompatible ambient mechanics | Compatible recovery may compose owner-native sources | Exact ruleset snapshot set remains retained/resolvable while required |
| E-12 | checkpoint is optional evidence and engine metadata is diagnostic | It must not become current/context authority | Recovery follows campaign/execution/package owners; checkpoint may only repeat refs as hints |
| E-13 | campaign/session definitions participate in context | They have owner-local revisions and promotion rules, not release-package identity by default | Keep their frontiers owner-local; context fingerprint incorporates exact refs |
| E-14 | House Rules typed realizations resolve through current catalog validation | Prose/sidecar is not executable and does not automatically create a fork | No S6D-01 package fork; later explicit profile only if a real same-ID replacement consumer is proven |
| E-15 | cleanup compatibility participates in runtime/catalog interpretation | Cleanup remains owner-local and no universal GC frontier exists | Ruleset snapshot retention is a typed dependency/protection obligation |
| E-16 | no existing user campaign depends on discarded pre-release schema | Future released migration remains WP-20 | Clean replacement allowed; expose compatibility hooks without legacy adapters |
| E-17 | coordinated catalog generation is currently `2.0.0` | It is not a compatibility freeze and may still change before release | Package manifest references generation; S6D-02 supplies final namespace/content |
| E-18 | S6D-02 owns admitted definitions/IDs and S6D-11 owns integrated machine tests | S6D-01 must not invent seed contents | Define manifest/lock/context contracts and explicit downstream obligations only |

## 4. Alternatives

### Alternative A — Reuse engine version + runtime ZIP digest

Shape:

```text
ResolvedCatalogContext identity = engine_version + package_sha256
```

Advantages: no new ruleset metadata; exact artifact available today.

Failures:

- conflates engine code/docs/templates with reusable definition semantics;
- prevents recognizing the same ruleset snapshot in another valid build;
- does not declare namespaces or package dependencies;
- makes same-version maintenance policy the accidental catalog compatibility policy;
- cannot support independent ruleset packages without redesign.

Disposition: **REJECT**.

### Alternative B — Store one universal `ResolvedCatalogSnapshot` record

Shape: materialize engine, ruleset, campaign, session, execution and recovery frontiers in one canonical snapshot object.

Advantages: one apparent locator and easy diagnostics.

Failures:

- duplicates native campaign/session/execution owners;
- conflicts with no-universal-frontier and checkpoint-nonauthority laws;
- creates cross-domain update/currentness coupling;
- risks hot-path/global scans and stale snapshot authority.

Disposition: **REJECT**.

### Alternative C — Ruleset package manifests + exact resolved-set identity + owner-local projections

Shape:

```text
package semantic manifest
    -> exact package content digest
    -> exact dependency lock
    -> order-independent resolved-set digest

runtime package advertises embedded resolved set
campaign adoption records selected set digest
accepted Resolution/Continuation records selected set digest
context fingerprint derives from set digest + owner-local definition frontiers
```

Advantages:

- exact, reconstructive and independent of ZIP/source accidents;
- keeps package meaning separate from engine/catalog/artifact axes;
- supports one shipped package now and a bounded exact package set later;
- preserves owner-local recovery and campaign/session frontiers;
- provides a finite same-version refresh/adoption test;
- does not require per-definition/world-record versions or online resolution.

Costs: new semantic manifest/lock schema and projections; release builder must compute deterministic digests; retention must protect referenced snapshots.

Disposition: **RECOMMEND**.

### Alternative D — Compatibility line only, without exact content identity

Advantages: easy compatible substitution and smaller metadata.

Failures: cannot reconstruct exact accepted meaning, cannot detect dishonest/incompatible same-line changes, and cannot distinguish additive definition changes from repacks.

Disposition: **REJECT**. Compatibility identity is useful only beside exact content identity.

## 5. Recommended architecture

### 5.1 Semantic package manifest

Each admitted ruleset package has one semantic manifest declaring:

- schema version;
- stable package ID;
- presentation/package version;
- compatibility ID/line;
- required engine version/capability relation;
- required catalog generation;
- owned semantic namespaces;
- exact dependency declarations;
- explicit content-root/file-set rules.

The manifest does not store its own content digest. The builder/loader computes a domain-separated digest over the normalized ordered `(relative path, byte digest)` set defined by the manifest, including the manifest bytes, avoiding self-reference.

### 5.2 Exact resolved snapshot set

The selected package set is a closed exact lock:

```text
package_id
package_version
compatibility_id
content_sha256
dependency package_id -> exact content_sha256
```

Its set identity is a domain-separated digest of canonical entries sorted by package ID. Input order has no meaning. Duplicate package IDs, cycles, missing exact dependencies, namespace overlap and engine/catalog incompatibility fail validation.

### 5.3 Identity axes remain distinct

```text
engine_version                 semantic engine/capability release axis
catalog_generation             machine vocabulary/schema generation axis
runtime package_id/source SHA  built-artifact provenance axis
runtime ZIP SHA-256            exact complete artifact bytes
ruleset package version        presentation/adoption version axis
ruleset compatibility_id       declared semantic compatibility line
ruleset content_sha256         exact package content identity
ruleset_set_sha256             exact selected dependency-closed set identity
catalog_context_fingerprint    derived engine + ruleset set + owner-local frontier identity
```

No axis silently substitutes for another.

### 5.4 Natural-owner projections

- Generated runtime package metadata carries the exact embedded resolved ruleset set and its digest.
- Campaign `engine.created_with/current` carries the resolved ruleset-set digest beside existing engine/package/source/artifact identity.
- Accepted Resolution and Continuation carry the exact ruleset-set digest beside `catalog_context_fingerprint`.
- Campaign/session definition revisions remain owner-local exact frontier/dependency refs; they are inputs to the fingerprint, not copied into a package lock.
- Checkpoint may repeat these refs for diagnostics/routing but never owns or overrides them.

### 5.5 Adoption and refresh

Same-version/source-descendant refresh is nonsemantic only when the resolved ruleset-set digest is unchanged. If it changes, even compatibly/additively, campaign semantics changed:

- creator authorization and coherent adoption are required;
- prepared/unaccepted work revalidates;
- accepted work retains its exact ruleset-set identity;
- non-creator cannot silently advance the campaign ruleset set;
- exact old snapshots remain protected while a promised accepted consumer needs them.

WP-20 later owns released-campaign migration between incompatible compatibility lines. S6D-01 only defines the finite identity/adoption boundary.

## 6. Downstream obligations

- **S6D-02:** create admitted package instance(s), namespace claims and complete content roots from the supported seed.
- **S6D-03–06:** ensure selector/accessor/value/primitive registries participate in declared catalog generation and snapshot content where execution depends on them.
- **S6D-07–09:** prove the locked package content reconstructs the supported mechanics and READY_PC seed.
- **S6D-10:** validate House Rules realization refs against the active resolved context without prose execution or implicit fork.
- **S6D-11:** TDD for manifest/lock schemas, digest determinism, dependency closure, collision/cycle rejection, campaign/Continuation projections, refresh/adoption and reconstruction.
- **S6D-12:** attack mixed axes, dishonest compatibility, missing retained snapshots, duplicate owners and global-snapshot regressions.
- **R2.7 WP-20:** define post-release compatibility-line evolution/migration policy; do not reopen exact identity semantics.

## 7. Human decision gate

No human decision is required at Step 3. Alternative C is forced by accepted authority boundaries and quality constraints. Choosing A, B or D would contradict already approved architecture rather than express a legitimate product preference.

Confidence: **HIGH** for identity separation, exact resolved-set digest, natural-owner projections and refresh/adoption boundary. **MEDIUM-HIGH** for exact field naming and digest serialization details, which are agent-owned technical specification and must survive adversarial review before canonicalization.


