# HDM Versioning Machine Normalization — Implementation Brief

> **For agentic workers:** REQUIRED SUB-SKILL: follow the current Superpowers implementation workflow required by `DEV/DEVELOPMENT_EXECUTION_PROCESS.md`. Use TDD for behavioral/contract changes, maintain coherent checkpoints, and use verification-before-completion before any PASS/completion claim.

Status: **HUMAN-AUTHORIZED IMPLEMENTATION BRIEF — EXECUTION MUST STILL FOLLOW CURRENT IMPLEMENTATION GATES**

Date: 2026-09-05

**Goal:** Realize the approved HDM versioning taxonomy across all current machine contracts, runtime files, development tooling, schemas, catalogs, ruleset package identities, digest contracts, tests and current documentation, eliminating ambiguous/invalid pre-release version spellings without carrying pre-release compatibility debt.

**Architecture:** Implement the three-category versioning law from the approved canonical specification. Preserve semantically independent namespaces rather than forcing one universal version. Normalize field names, values and machine validation atomically by contract family, regenerate all derived identities affected by canonicalization changes, and fail closed on mixed/unsupported generations.

**Tech stack:** Markdown/YAML/JSON/JSON Schema/Python standard-library runtime code, DEV Python tooling/tests, Git/GitHub release metadata, GitHub Actions validation.

**Primary spec:** `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md`

**Research inventory:** `DEV/docs/superpowers/research/2026-09-05-versioning-namespace-inventory-and-analysis.md`

**Planning source snapshot:** `185a3e92452400be7bce4c28112daf633dffaad2`

---

## 1. Global constraints

1. Read and follow current `AGENTS.md`, the applicable runtime overlay, and `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` before production changes.
2. The approved architecture is authoritative. Do not invent a fourth generic version namespace for convenience.
3. Current engine release identity remains `1.0-alpha`; `recommended_tag` remains `v1.0-alpha` unless an independent release decision changes it.
4. The last actual published pre-v1 engine tag is `v0.8`. Repository tag history contains `v0.1-beta`, `v0.2-beta`, `v0.3`, `v0.4`, `v0.5-alpha`, `v0.5-beta`, `v0.6`, `v0.7`, `v0.8` and no `v0.9` engine release.
5. Current runtime metadata moved directly to `1.0-alpha` at commit `1a4b1b12d4a9c46ea39dce98f3f88556c7b37bf5` (`Set runtime engine version to v1.0-alpha`). Treat `0.9.*` Category-B module versions as suspect/invalid until history proves what their correct `0.8` or `1.0` prefix must be. There is no legitimate released engine `0.9` line to preserve.
6. Category-B `1.1.*` values are invalid on the current `1.0-alpha` engine line unless a future independent release decision establishes engine `1.1`. This task does not.
7. Current pre-release machine shapes have **no backward-compatibility preservation requirement**. Do not add shims, dual readers/writers, compatibility aliases or migration scripts solely to keep the current obsolete spellings working.
8. Released-v1+ compatibility law remains exactly as specified by the primary spec; do not weaken fail-closed behavior.
9. External version namespaces are untouched: SRD/D&D baseline versions, JSON Schema draft URLs/versions, Git object IDs, external dependency versions and third-party versions remain owned externally.
10. Domain-local runtime/currentness revisions (`state_revision`, LIVE/currentness/frontier ordinals, etc.) are not release versions and MUST NOT be mass-renumbered.
11. Persistent family `schema_version` values are independent. Do not interpret local schema `1` as obsolete merely because `campaign_contract_generation` is `2`.
12. Any serialized artifact whose own shape changes incompatibly in this normalization MUST increment its own local schema version exactly once in the same coherent change. Multiple field changes in one normalization do not cause multiple bumps.
13. Do not change gameplay authority, persistence/CAS semantics, access authority, recovery law, RNG semantics, chronology or LLM boundaries merely to make version normalization convenient.
14. Do not start WP-20 Step 2 architecture. This task realizes the already approved versioning amendment only.
15. Do not create actual campaign migration edges for obsolete pre-release representations. Recreate/update current templates, fixtures and generated identities instead.
16. Current/human-facing documentation must use the new law. Historical provenance may retain old values only when it is explicitly describing the historical state; do not rewrite history into a false value.
17. Root `README.md`, if it contains a directly stale current version/field statement, receives only the smallest targeted correction authorized by this task; do not restructure or rewrite it.
18. All changed machine contracts require corresponding tests/audit enforcement so the old zoo cannot reappear silently.

---

## 2. Approved numbering categories

### Category A — engine release

```text
engine_version: MAJOR.MINOR[-prerelease]
```

Current value:

```text
1.0-alpha
```

Do not add a patch component to engine release identity.

### Category B — engine-bound shipped component/module

```text
framework_module_version: ENGINE_MAJOR.ENGINE_MINOR.REVISION
```

- first two components = engine major/minor line of the module's last material contract change;
- third component = monotonically increasing module-local revision;
- engine bump alone does not rewrite an untouched module;
- next material edit moves prefix to current engine line and increments local revision exactly once;
- normalization of a mistaken header alone does not consume another logical revision.

### Category C — independent integer counter

```text
N
```

Subtypes remain semantically distinct:

```text
*_revision        local bookkeeping/currentness revision; not a compatibility boundary
schema_version    one serialized contract version
*_schema_version  qualified serialized contract version
*_generation      semantic/compatibility generation
```

Never infer compatibility from equality of integers belonging to different namespaces.

---

## 3. Implementation Impact Envelope

```text
SPEC / APPROVED DESIGN:
  DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md

BASELINE SHA FOR THIS BRIEF:
  185a3e92452400be7bce4c28112daf633dffaad2

EXPECTED OWNERS TO CHANGE:
  DEV/RELEASE/VERSIONING.md only if realization wording/validation routing needs precise current-machine wording
  DEV/ENGINE_DEVELOPMENT.yaml
  GAME/ENGINE_VERSION.yaml
  GAME/CORE version-bearing module headers
  GAME/SCHEMA affected schemas
  GAME/CAMPAIGN affected templates
  GAME/TEMPLATE and GAME/INSTALL consumers where applicable
  GAME/TOOLS affected runtime generators/loaders
  GAME/RULES package manifests/content whose exact hashes participate
  DEV/CATALOG current machine artifacts
  DEV/SCHEMAS affected machine schemas
  DEV/TOOLS release/catalog/ruleset/audit tooling
  DEV/TESTS affected tests/scenarios/fixtures
  current architecture/release/runtime documentation that projects old field names/values

EXPECTED CONSUMERS TO CHANGE:
  release builder and package validator
  maintenance audit
  campaign initializer/bootstrap/update flows
  storage marker consumers
  catalog validators/admission/closure tools
  ruleset loader/comparator/lock builder
  conformance inventory/attestation generation
  accepted-work/checkpoint schema consumers that persist exact digest identities
  tests and generated fixtures

ALLOWED INTERFACES / CONTRACTS TO CHANGE:
  version/generation/revision field names and scalar types exactly as approved
  artifact-local schema versions required by those shape changes
  ruleset package/lock/compatibility field representation
  catalog generation representation
  digest-domain representation and resulting derived hashes/fingerprints
  explicit digest/fingerprint generation projections required by the approved spec
  campaign/storage aggregate generation projections required by the approved spec

PROTECTED ARCHITECTURE INVARIANTS:
  engine/package/ruleset/catalog/schema/digest axes remain non-equivalent
  exact SHA/content identities remain distinct from semantic generation/revision metadata
  campaign created_with provenance remains immutable
  current adoption changes only through existing authorized publication laws
  storage baseline remains NEW-campaign-only
  released asset immutability remains intact
  no fuzzy compatibility, no arithmetic migration inference
  no migration or compatibility obligation for current pre-release obsolete shapes
  currentness/RNG/persistence/access/history authority unchanged

ARCHITECTURE-SENSITIVE SURFACES:
  campaign contract generation placement
  any persistent exact hash that escapes its enclosing schema without digest-generation context
  ruleset semantic compatibility representation
  catalog coordinated-closure equality
  any new migration selector/authority
  any attempt to preserve obsolete aliases as a compatibility layer

EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION:
  full maintenance audit
  full DEV unit tests
  release builder/integration tests
  ruleset package closure validation
  catalog closure/admission validation
  campaign initialization/schema validation
  storage/bootstrap/update tests
  package build/extracted-root validation
  hosted CI on final published SHA

KNOWN OUT-OF-SCOPE OWNERS / SURFACES:
  external SRD/D&D version numbering
  JSON Schema draft identity
  third-party dependency versions
  gameplay mechanics semantics unrelated to version normalization
  new WP-20 migration graph architecture beyond the approved versioning law
  real campaign migration execution
```

If implementation requires a semantic change outside this envelope, trigger the System-Impact Gate instead of improvising.

---

## 4. Required bootstrap/read set for the execution agent

Read current versions on the fresh remote HEAD, not remembered copies:

1. `AGENTS.md`
2. applicable runtime overlay under `DEV/AGENT_RUNTIMES/`
3. `DEV/DEVELOPMENT_EXECUTION_PROCESS.md`
4. `DEV/CURRENT_PROGRESS.md`
5. `DEV/PROJECT_MAP.md` for dependency routing
6. `DEV/RELEASE/VERSIONING.md`
7. `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md`
8. `DEV/docs/superpowers/research/2026-09-05-versioning-namespace-inventory-and-analysis.md`
9. `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-step-1-versioning-amendment-reconciliation.md`
10. `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`
11. `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md`
12. `DEV/ENGINE_DEVELOPMENT.yaml`
13. `GAME/ENGINE_VERSION.yaml`
14. `GAME/SCHEMA/README.md`
15. current relevant `GAME/CORE`, `GAME/SCHEMA`, `GAME/CAMPAIGN`, `GAME/RULES`, `GAME/TOOLS` owners discovered by the task census

Do not bulk-read all historical design documents unless a specific historical value cannot be reconstructed from Git history/current owners.

---

## 5. Pre-change exhaustive census — mandatory

Before changing production files, build a complete census of current HDM-owned version-bearing surfaces on the fresh HEAD.

Search the entire tracked repository for at least:

```text
engine_version
framework_module_version
runtime_bootstrap_version
launcher_version
launcher_revision
schema_version
*_schema_version
*_revision
*_generation
storage_format_version
storage_format_generation
catalog_version
catalog_generation
package_version
package_revision
compatibility_id
compatibility_family
compatibility_generation
ruleset_set_sha256
catalog_context_fingerprint
_V1
.v1
0.9.
1.1.
2.0.0
1.6.0
1.2.0
```

Also search generic SemVer-looking literals and `vN`/`_VN` identifiers so hidden namespaces are not missed.

Classify every hit into exactly one disposition:

```text
CURRENT_MACHINE_OR_RUNTIME         -> normalize
CURRENT_NORMATIVE_DOCUMENTATION    -> normalize
CURRENT_TEST_OR_FIXTURE             -> normalize unless intentionally negative
HISTORICAL_PROVENANCE              -> retain exact history, annotate supersession only if needed
INTENTIONAL_NEGATIVE_FIXTURE        -> retain only with explicit test purpose
EXTERNAL_VERSION_NAMESPACE          -> untouched
NON_VERSION_SEMANTIC_IDENTIFIER     -> untouched with justification
```

The final report must include a zero-unclassified-hits statement for the search families above.

---

# Task 1 — Establish RED version-law tests before broad mutation

**Purpose:** Make the target state executable before mass editing.

**Primary files:**

- `DEV/TESTS/` new or existing focused version-policy tests
- `DEV/TOOLS/audit_engine.py`
- related validation fixtures

Add failing tests that require at minimum:

1. `DEV/ENGINE_DEVELOPMENT.yaml` and `GAME/ENGINE_VERSION.yaml` use `campaign_contract_generation`, not ambiguous aggregate `schema_version`.
2. shared release manifest projections agree.
3. all versioned CORE modules use `framework_module_version`.
4. no current CORE module declares engine line `0.9` or a future line above current `1.0`.
5. known corrected module versions resolve to the values in section 7 below.
6. catalog coordinated generation is integer `2` everywhere current and coordinated.
7. machine catalog fields use `catalog_generation`, not `catalog_version`, when they represent the coordinated generation.
8. ruleset package uses `package_revision`, `compatibility_family`, `compatibility_generation`; current legacy `package_version` and version-bearing `compatibility_id` are rejected.
9. current ruleset/catalog generation values are integers, not string `"2.0.0"`.
10. unsupported/mixed catalog generations fail validation.
11. custom digest-domain generation is explicit in validation and magic domain separators no longer rely on unexplained `_V1` spelling.
12. old machine field names (`runtime_bootstrap_version`, `storage_format_version`, `launcher_version`, old ruleset fields) fail current-contract validation after their owning slice is migrated.
13. external versions and explicitly historical/negative fixtures are not incorrectly rejected.

Verify RED failures are for missing target normalization, not unrelated breakage.

---

# Task 2 — Normalize release metadata and central campaign contract generation

## Target values

Keep:

```yaml
engine_version: 1.0-alpha
recommended_tag: v1.0-alpha
```

Replace the ambiguous aggregate field in both release manifests:

```yaml
schema_version: 2
```

with:

```yaml
campaign_contract_generation: 2
```

Affected minimum surfaces:

- `DEV/ENGINE_DEVELOPMENT.yaml`
- `GAME/ENGINE_VERSION.yaml`
- `DEV/TOOLS/release_builder.py` (`GAME_FIELDS`, `SHARED_FIELDS`, shape/equality checks)
- `DEV/TOOLS/audit_engine.py`
- release tests/integration tests
- current documentation that describes the shared field

Do **not** reinterpret artifact-local `schema_version` fields elsewhere as this aggregate generation.

If a launcher current field exists as:

```text
launcher_version: 19
```

normalize it to:

```text
launcher_revision: 19
```

and update all current consumers/tests. The value remains `19`; field renaming alone does not increment it.

---

# Task 3 — Reconstruct and normalize every CORE module version

## 3.1 Canonical header

Every versioned shipped CORE/runtime instruction module uses exactly:

```text
framework_module_version: X.Y.R
```

`BOOTSTRAP_RUNTIME.md` must no longer use `runtime_bootstrap_version`; rename the field to `framework_module_version` while preserving/reconstructing the correct module version under the history rule below.

Non-module documentation such as `README.md`/`SOURCES.md` remains unversioned only if current CORE policy/audit explicitly classifies it as non-module documentation.

## 3.2 Historical release rule

Repository tag history is authoritative evidence that there is no `v0.9` release line.

For each current CORE file:

1. inspect its version-header history and material semantic edits;
2. identify the last valid module-local revision before/currently within the relevant engine line;
3. if its last material contract change occurred on a real historical engine line `<=0.8` and the module has not materially changed since, retain that historical prefix/revision;
4. if it materially changed after the engine moved to `1.0-alpha`, target prefix is `1.0` and the module-local revision increments once per material logical change;
5. do not count pure formatting/path moves/header correction as a new logical revision;
6. do not count commits mechanically: inspect whether the module contract actually changed;
7. `0.9.*` cannot survive as a current Category-B value. Reconstruct whether its correct target is `0.8.R` or `1.0.R`; given current repository history, post-`1.0-alpha` changes use `1.0.R`;
8. `1.1.*` cannot survive while engine is `1.0-alpha`.

## 3.3 Known exact corrections already established by history

These are not guesses; execution should verify but should converge to these values unless fresh remote history materially differs:

### `GAME/CORE/DIEGETIC_ONBOARDING.md`

History:

```text
0.2.0
-> 1.0.1 at 0711cdbaf3e91ed190404e60a11c70df22eb5175
-> material edit at 19ae14b9db96728d9c7b94fb9e5f8eeb197a9c76 incorrectly wrote 1.1.0
```

Target:

```text
framework_module_version: 1.0.2
```

### `GAME/CORE/CHARACTER_READINESS.md`

History:

```text
0.1.1
-> 1.0.2 at c212effa94ba579dc463d9956070d412b640707a
-> material edit at 818d18b6d7eb46a03a9c2853b2c47fcf27fb38e9 incorrectly wrote 1.1.0
```

Target:

```text
framework_module_version: 1.0.3
```

### `GAME/CORE/ENGINE_UPDATES.md`

At the 0.8 GAME/DEV split it carried `0.8.1`. It later reached erroneous `0.9.2`; after that, S6D-11 materially extended its changed-ruleset-set compatibility contract without consuming another module revision.

Expected target after full history verification:

```text
framework_module_version: 1.0.3
```

Do not settle on `1.0.2` unless history proves the S6D-11 change was non-material, which current evidence does not support.

## 3.4 Remaining CORE modules

Do not mass-map `0.x.y -> 1.0.y`.

Audit every current module. Any stale header on a module materially changed in the `1.0` development line must be corrected using its real local revision history. Any genuinely untouched historical module may remain `0.1` through `0.8` according to its true last material change.

Update tests/audit so future material module edits cannot leave the header stale or declare a nonexistent/future engine line.

---

# Task 4 — Realize `campaign_contract_generation` in campaign persistence

Approved aggregate current generation:

```text
campaign_contract_generation = 2
```

Campaign MANIFEST must carry:

```yaml
campaign_contract:
  created_with: 2
  current: 2
```

`created_with` is immutable. `current` is the mutable adoption/migration projection under the existing authorized campaign publication law.

Minimum affected surfaces:

- `GAME/SCHEMA/campaign_manifest.schema.yaml`
- `GAME/CAMPAIGN/MANIFEST.yaml`
- `GAME/TOOLS/init_campaign.py`
- bootstrap/setup/update runtime consumers
- campaign/schema tests and fixtures
- release/bootstrap acceptance tests

Because the MANIFEST serialized shape gains a new required compatibility-bearing object, increment the MANIFEST family schema exactly once:

```text
campaign_manifest schema_version: 3 -> 4
campaign template MANIFEST.schema_version: 3 -> 4
```

This pre-release shape change requires **no 3->4 migration script**. Regenerate/recreate current templates/fixtures.

Do not bump unrelated persistent family schemas merely because MANIFEST changed.

Any current documentation that treats engine-global `schema_version` as the campaign migration selector must be rewritten to use `campaign_contract_generation` plus the multi-axis compatibility envelope.

---

# Task 5 — Normalize storage generation

Canonical target:

```text
storage_format_generation: 3
```

Replace current:

```text
storage_format_version: 3
```

across storage marker/schema/runtime/bootstrap/tools/tests/current docs.

Because `dnd_storage` serialized shape changes incompatibly by field rename, bump its local schema exactly once:

```text
dnd_storage.schema_version: 3 -> 4
```

Update template/current marker examples accordingly.

`DEV/ENGINE_DEVELOPMENT.yaml` development bookkeeping field `storage_format_revision` remains an independent integer and is **not** renamed to generation or tied to engine version.

No pre-release storage migration script is required. Current obsolete marker shape is recreated.

---

# Task 6 — Normalize catalog generation and coordinated catalog schemas

## 6.1 Generation target

Every current coordinated catalog projection that currently means `2.0.0` must become integer generation:

```text
catalog_generation: 2
```

Fields named `catalog_version` that actually mean this coordinated generation must be renamed to `catalog_generation`.

No current coordinated machine artifact may retain string `"2.0.0"` as the active generation representation.

## 6.2 Coordinated closure

All current coordinated catalog artifacts and ruleset requirements must agree on generation `2`.

Mixed current closure, e.g. owner/core generation `3` with required registry/ruleset generation `2`, must fail build/audit/admission.

Local structural schema versions remain independent from generation.

## 6.3 Local schema bumps

For every serialized catalog artifact whose own shape changes because:

- `catalog_version` is renamed to `catalog_generation`, or
- generation type changes from string to integer, or
- another required field changes under this normalization,

increment that artifact's own `schema_version` exactly once.

Known likely current `schema_version: 1 -> 2` candidates include at least the catalog artifacts/manifests identified in the research inventory, such as:

- `DEV/CATALOG/core-catalog.json` where its shape carries the coordinated field;
- `DEV/CATALOG/identifier-policies.json` where applicable;
- `DEV/CATALOG/activity-primitive-contracts/manifest.json`;
- `DEV/CATALOG/catalog-admission-ledger/manifest.json`;
- any other current catalog artifact with local `schema_version: 1` whose serialized shape changes in the census.

Do **not** bump a local schema merely because another coordinated artifact changed; bump only when that artifact's own serialized contract changed.

Update corresponding JSON Schemas/validators/tests from expected local schema `1` to `2` where applicable.

## 6.4 Documentation cleanup

Current normative/current-facing references to catalog `2.0.0`, `catalog_version`, or stale `1.2.0` must be normalized to integer generation `2` and canonical naming.

Historical statements such as "superseded `1.6.0` scaffold" may retain `1.6.0` **only when explicitly historical**. Do not make a historical event falsely look as if it originally used integer generation `1`.

---

# Task 7 — Normalize ruleset package revision and compatibility generation

Current built-in package target representation:

```yaml
manifest_schema_version: 2
package_id: hdm.rules.dnd2024-srd52-core
package_revision: 1
compatibility_family: hdm.rules.dnd2024-srd52
compatibility_generation: 1
engine_requirement:
  engine_version: 1.0-alpha
catalog_generation: 2
```

Replace legacy current representation:

```yaml
manifest_schema_version: 1
package_version: 0.1.0-mvp
compatibility_id: hdm.rules.dnd2024-srd52.v1
catalog_generation: "2.0.0"
```

The package manifest shape is breaking, therefore:

```text
manifest_schema_version: 1 -> 2
```

Update at minimum:

- built-in ruleset package manifest;
- `GAME/TOOLS/ruleset_package.py` validation/loading/lock building/comparison;
- DEV package-closure validator/build tooling;
- release builder;
- ruleset manifest/lock/result JSON Schemas;
- package closure ledgers/current fixtures;
- all tests and current docs.

`package_revision` is update order only and never proves semantic compatibility.

`compatibility_family + compatibility_generation` replaces version-bearing `compatibility_id` as the typed current machine representation.

Same compatibility generation only makes the existing monotonic semantic comparison eligible. It does not bypass exact content/set identity.

---

# Task 8 — Normalize ruleset lock/protocol schemas

The resolved ruleset lock and any serialized protocol artifact whose shape changes due to Task 7 or Task 9 must bump its own schema exactly once.

Expected:

```text
lock_schema_version: 1 -> 2
```

because package-line fields and catalog-generation representation change.

For each of the following current schemas, inspect the actual serialized shape:

```text
inventory_schema_version
comparison_schema_version
attestation_schema_version
```

If the normalized contract adds/renames fields, changes catalog-generation type, adds required digest-generation context, or changes semantic meaning of the serialized payload, bump `1 -> 2` exactly once.

If a particular artifact's serialized contract truly does not change, leave its schema version unchanged; document the proof in the execution review rather than bumping for visual symmetry.

No old pre-release schema reader/adapter is required.

---

# Task 9 — Make custom digest/fingerprint generations explicit and regenerate identities

Current implementation contains magic domain separators such as:

```text
HDM_RULESET_PACKAGE_SNAPSHOT_V1\n
HDM_RESOLVED_RULESET_SET_V1\n
HDM_RULESET_SEMANTIC_ENTRY_V1\n
HDM_RULESET_COMPATIBILITY_EVIDENCE_V1\n
HDM_RULESET_ENGINE_CONTRACT_INVENTORY_V1\n
HDM_RULESET_CONFORMANCE_ATTESTATION_V1\n
```

Normalize the contract so generation is explicit and mechanically validated.

Use generation `1` for each current digest domain unless an existing owner proves a different current generation.

Canonical domain-separator representation for this normalization:

```text
HDM_RULESET_PACKAGE_SNAPSHOT/1\n
HDM_RESOLVED_RULESET_SET/1\n
HDM_RULESET_SEMANTIC_ENTRY/1\n
HDM_RULESET_COMPATIBILITY_EVIDENCE/1\n
HDM_RULESET_ENGINE_CONTRACT_INVENTORY/1\n
HDM_RULESET_CONFORMANCE_ATTESTATION/1\n
```

Define explicit named generation constants in code/validation rather than deriving generation by parsing the byte literal.

## 9.1 Escaping exact identities

Where an exact digest/fingerprint escapes its enclosing versioned protocol and is persisted/referenced independently across releases, add explicit generation context.

At minimum audit all current carriers of:

```text
ruleset_set_sha256
catalog_context_fingerprint
```

Use sibling typed fields where these hashes escape an enclosing schema:

```text
ruleset_set_digest_generation: 1
catalog_context_fingerprint_generation: 1
```

Apply them consistently to every authoritative/persisted projection that needs to interpret the exact identity later, including as applicable:

- generated runtime package provenance;
- campaign ruleset `created_with/current` projections;
- accepted Resolution/Continuation state;
- checkpoint diagnostic projection;
- any other persisted owner discovered by the census.

Do not add generation fields to ephemeral values where enclosing schema/version already unambiguously fixes the digest semantics and the value cannot escape that context.

Any serialized persistent/protocol artifact gaining a required generation field must bump its local schema exactly once.

Likely consequences to verify include:

- campaign MANIFEST already bumps `3 -> 4` in Task 4, so digest-generation fields can be included in the same schema-4 normalization without a second bump;
- checkpoint schema currently at `2` should bump to `3` if it gains required ruleset-set/fingerprint generation context;
- Resolution/Continuation and other DEV schema contracts must bump their local schema/version constants if their serialized shape changes;
- RUNTIME_PACKAGE top-level schema must bump if its validated contract gains digest-generation fields or otherwise changes nested required protocol semantics.

## 9.2 Runtime package expected schema bump

Current `RUNTIME_PACKAGE` contract is schema `2` and its validator directly constrains the nested ruleset lock/conformance shape. This normalization changes that contract materially.

Expected target:

```text
RUNTIME_PACKAGE.schema_version: 2 -> 3
```

Update release builder generation/validation/tests accordingly.

## 9.3 Recompute, do not preserve

Because all current affected identities are pre-release:

- recompute package content hashes;
- recompute semantic-entry hashes;
- recompute resolved-set hashes;
- recompute conformance inventory/evidence/attestation hashes;
- recompute catalog-context fingerprints where generated fixtures carry them;
- regenerate locks, closure ledgers and fixtures;
- update all exact expected digest values in tests/current evidence.

Do **not** add old-hash aliases or translation tables merely to preserve the obsolete pre-release hash domain.

Tests must prove that the new hashes are deterministic and that old/new domain generations are not treated as raw comparable identity spaces.

---

# Task 10 — Normalize current documentation and examples project-wide

After machine contracts are stable, sweep all current documentation.

Current normative/current-facing text must use:

```text
campaign_contract_generation
storage_format_generation
catalog_generation: integer
package_revision
compatibility_family
compatibility_generation
framework_module_version
launcher_revision
explicit digest/fingerprint generation terminology
```

Update current examples and diagrams accordingly.

Do not preserve misleading current examples such as a supposed engine `v0.9-RC` merely as a generic example when repository history has no `0.9` line; use real/currently meaningful examples instead (`v0.8`, `v1.0-alpha`, or another non-misleading generic form).

Historical design/audit records:

- retain exact old values if they are evidence of what existed then;
- do not mechanically rewrite historical `1.6.0`, `2.0.0`, old hash strings, old field names, etc. into values that did not exist historically;
- where a historical document is still easy to mistake for current authority, add the smallest supersession note or rely on existing authority/status taxonomy rather than rewriting its historical body.

For root `README.md`, only make minimal targeted corrections to directly stale current statements; preserve editorial structure/voice.

---

# Task 11 — Strengthen maintenance audit so the zoo cannot return

Extend deterministic audit/validation to enforce at least:

1. one current engine release field shape (`MAJOR.MINOR[-prerelease]`);
2. shared DEV/GAME `campaign_contract_generation` equality;
3. no ambiguous aggregate `schema_version` in engine version manifests;
4. every versioned CORE module uses the canonical header name and valid three-integer format;
5. no Category-B module prefix refers to nonexistent `0.9` or a future engine line;
6. coordinated current catalog generation equality and integer type;
7. no active machine `catalog_version` aliases for coordinated generation;
8. no active ruleset `package_version`/version-bearing `compatibility_id` fields;
9. ruleset manifest/lock/protocol local schema versions match their normalized shapes;
10. RUNTIME_PACKAGE normalized schema/version-generation contract;
11. storage marker canonical field and schema;
12. campaign MANIFEST aggregate generation and schema;
13. explicit digest generation for escaping exact identities;
14. no old `_V1` digest-domain spelling in active implementation;
15. no forbidden GAME -> DEV runtime dependency introduced by the refactor;
16. intentional historical/negative/external occurrences are explicitly scoped so audit remains low-noise.

Prefer structured parsing and owner-aware validation over broad string bans when a textual occurrence can be legitimately historical/external.

---

# Task 12 — Full reverse audit after implementation

Repeat the repository-wide census from section 5 on the final candidate state.

For every surviving old spelling/value, assign a disposition and prove why it remains.

Required final zero-current-debt assertions include:

```text
CURRENT machine runtime_bootstrap_version occurrences: 0
CURRENT machine launcher_version-as-revision occurrences: 0
CURRENT machine storage_format_version occurrences: 0
CURRENT coordinated catalog_version fields: 0
CURRENT coordinated catalog generation string "2.0.0": 0
CURRENT ruleset package_version fields: 0
CURRENT version-bearing ruleset compatibility_id fields: 0
CURRENT unexplained digest-domain _V1 literals: 0
CURRENT Category-B CORE 0.9.* versions: 0
CURRENT Category-B CORE 1.1.* versions while engine=1.0-alpha: 0
UNCLASSIFIED version/revision/generation hits from the census: 0
```

Historical/external/negative-fixture occurrences do not violate the assertion when explicitly classified and non-authoritative.

---

# Task 13 — Verification, publication and execution status

Run fresh verification required by the current process, including at minimum:

```text
focused version-policy tests
ruleset package/closure tests
catalog tests/validators
campaign/schema/init tests
storage/bootstrap/update tests
release builder/integration tests
full DEV unit tests
full maintenance audit
runtime release build/package validation when permitted by current task/runtime policy
hosted CI on published final SHA
remote branch read-back
```

Maintain an execution status file at:

`DEV/docs/superpowers/plans/2026-09-05-versioning-machine-normalization-implementation-brief-execution-status.md`

Record coherent task checkpoints, final SHA, verification evidence, any System-Impact events/rulings, remaining debt and `UNPUBLISHED_WORK`.

Do not report COMPLETE until fresh final verification and the required final integration review gates have passed.

---

## 6. Expected target-state summary

The target machine vocabulary should read conceptually like this:

```yaml
# Engine release manifests
engine_version: 1.0-alpha
campaign_contract_generation: 2
recommended_tag: v1.0-alpha

# CORE module
framework_module_version: 1.0.3  # example; per-module history determines R

# Campaign manifest
schema_version: 4
campaign_contract:
  created_with: 2
  current: 2

# Storage marker
schema_version: 4
storage_format_generation: 3

# Coordinated catalog artifact
schema_version: 2  # only where that artifact's own shape changed from local schema 1
catalog_generation: 2

# Built-in ruleset package
manifest_schema_version: 2
package_id: hdm.rules.dnd2024-srd52-core
package_revision: 1
compatibility_family: hdm.rules.dnd2024-srd52
compatibility_generation: 1
engine_requirement:
  engine_version: 1.0-alpha
catalog_generation: 2

# Escaping exact identities
ruleset_set_digest_generation: 1
ruleset_set_sha256: <recomputed sha256>
catalog_context_fingerprint_generation: 1
catalog_context_fingerprint: <recomputed fingerprint>

# Runtime package
schema_version: 3
ruleset_set_digest_generation: 1
```

Independent DEV `*_revision` counters remain integers with their current values unless the owning concern itself materially changes as part of this implementation and its established bookkeeping law requires a bump.

Dynamic state/currentness revisions remain untouched except for schema wiring mechanically required to preserve their existing semantics.

---

## 7. Migration/backward-compatibility behavior by entity

This implementation must preserve the approved policy rather than inventing migrations:

| Entity | Current pre-release normalization | Released-v1+ future rule |
| --- | --- | --- |
| Engine release | keep `1.0-alpha` | engine number alone never proves compatibility |
| CORE module version | correct metadata/history only | no campaign migration; module consumed inside exact runtime package |
| DEV `*_revision` | retain independent integer | no migration semantics |
| Persistent family schema | bump only affected local serialized contract | explicit reader support; breaking persisted change needs explicit migration edge |
| Campaign contract generation | establish current generation `2` | different released generations require explicit campaign migration/adoption or unsupported |
| Storage format generation | rename current generation `3`; storage schema becomes `4` | explicit storage migration edge; independent of campaign migration |
| Runtime/package schema | regenerate current pre-release package/schema | released old assets immutable; readers explicitly support or reject |
| Catalog generation | normalize `2.0.0 -> 2` | cross-generation use requires explicit translation/adoption/migration or unsupported |
| Ruleset package revision | normalize current package to revision `1` | revision alone has no compatibility meaning |
| Ruleset compatibility generation | normalize current family/gen `1` | different generation requires explicit creator adoption/migration or unsupported |
| Ruleset/protocol local schemas | bump affected shapes once | explicit reader support/regeneration; campaign migration only if a persisted owner is affected |
| Digest/fingerprint generation | normalize current domain to generation `1`, recompute all pre-release identities | persisted released identities retain generation context; cross-generation identity is not raw-equal |
| Dynamic currentness revisions | do not renumber | owner-specific semantics only |

No task in this implementation may infer migration paths from integer arithmetic.

---

## 8. Required completion report

Return a concise evidence-backed report containing:

- starting and final SHA;
- changed-file count grouped by `GAME`, `DEV`, root infrastructure/docs;
- final version namespace census;
- complete CORE old -> new version table with historical justification for every changed module;
- local schema-version bumps and why each bumped;
- catalog field/value normalization summary;
- ruleset package/lock/protocol old -> new field/value summary;
- digest-domain generations and newly recomputed exact hashes;
- list of historical/external/negative-fixture old spellings intentionally retained;
- zero-unclassified-hits evidence;
- focused/full tests, maintenance audit, release build/package validation, hosted CI evidence;
- any System-Impact events and rulings;
- confirmation that no pre-release compatibility shim/migration debt was added;
- confirmation that WP-20 Step 2 architecture was not started as part of this implementation.
