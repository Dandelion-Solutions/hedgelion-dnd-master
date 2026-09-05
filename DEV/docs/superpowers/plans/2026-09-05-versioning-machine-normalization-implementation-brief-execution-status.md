# Versioning machine normalization — execution status

PLAN: `DEV/docs/superpowers/plans/2026-09-05-versioning-machine-normalization-implementation-brief.md`
SPEC: `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md`
BASE_SHA: `e7bb57853b2b1aa300831f88db6c201411c4795e`

STATUS: IMPLEMENTATION_COMPLETE_AWAITING_MANDATORY_SENIOR_REVIEW
CURRENT_TASK: NONE — implementation execution is closed; the repository remains at the existing WP-20 Step-1 Senior-review gate
LAST_COMPLETED_TASK: Task 13 — final reverse audit, coordinator review, status reconciliation and verification
LAST_VERIFIED_SHA: `8a5cec0c232c30d095dcf4c5f211522487daa343`
LAST_VERIFIED_CI_RUN: `33973592843`

## Completed execution

- Fresh remote HEAD matched assignment baseline `e7bb57853b2b1aa300831f88db6c201411c4795e`.
- Required runtime/process/spec/research/design/owner read set completed.
- Baseline hosted `Validate engine source` run `33964618977` succeeded on BASE_SHA.
- RED version-law checkpoint published at `6433a3c576f635330856cd3e825e9f2156513dc3`; hosted run `33965479761` failed as expected on pre-normalization machine debt.
- Exhaustive census remained classified with zero unclassified hits while active legacy debt was driven to zero.
- CORE history reconstruction completed for every current version-bearing CORE module; the six modules with post-`1.0-alpha` material changes were corrected to their reconstructed engine-bound versions:
  - `ADJUDICATION.md`: `0.2.2 -> 1.0.2`;
  - `CHARACTER.md`: `0.6.0 -> 1.0.1`;
  - `CHARACTER_READINESS.md`: `0.1.1 -> 1.0.3`;
  - `DIEGETIC_ONBOARDING.md`: `0.2.0 -> 1.0.2`;
  - `DURABILITY_GUARD.md`: `0.5.0 -> 1.0.1`;
  - `ENGINE_UPDATES.md`: `0.8.1 -> 1.0.3`.
- `BOOTSTRAP_RUNTIME.md` normalized its field name to `framework_module_version` while retaining module value `0.8.8`; no false semantic renumbering was introduced.
- DEV/GAME engine manifests now project `campaign_contract_generation: 2` and no aggregate engine-level `schema_version`.
- Campaign MANIFEST/schema moved `3 -> 4` and materialize `campaign_contract.created_with/current: 2` plus ruleset-set digest generation.
- Storage schema moved `3 -> 4`; current marker field is `storage_format_generation: 3`.
- Launcher field normalized to `launcher_revision`.
- Coordinated catalog machine artifacts use integer `catalog_generation: 2`; affected local catalog artifact schemas bumped once where their serialized shape changed.
- Built-in ruleset manifest uses schema `2`, `package_revision: 1`, stable compatibility family + generation `1`, integer catalog generation `2`.
- Resolved lock uses schema `2`; engine-contract inventory, compatibility result and conformance attestation use schema `2` after their shape changes.
- Runtime package uses schema `3` and carries `ruleset_set_digest_generation: 1`.
- Escaping accepted execution identities carry `ruleset_set_digest_generation: 1` and `catalog_context_fingerprint_generation: 1`; affected local schemas were bumped once where required.
- HDM-owned digest/canonicalization domains use explicit named generation `1` constants and `/1` domain separators.
- Current producer-derived exact ruleset identities are:
  - package snapshot SHA-256 `57c77802744619fa4d35a21bab38d133589f21de72f80044dc4d7bb58cb06d34`;
  - resolved ruleset-set SHA-256 `0700d3ccf367ade9ff56f620c4330bd5b4544fb9e22031f9d1eac3718a88ef2d`.
- All affected current identity projections/fixtures were regenerated from producer logic; no old-hash compatibility aliases were retained.
- DEV bookkeeping matches the approved target: `storage_format_revision: 5`, `persistence_revision: 9`, `campaign_identity_revision: 3`, `consistency_audit_revision: 6`; all other DEV revision counters retained their prior values.
- Current-facing versioning/release/catalog/ruleset/storage/migration documentation was reconciled to realized namespace names and generations; historical research/design/plans remain unchanged as provenance.
- Root README was checked and required no targeted versioning correction under its separate editorial contract.
- Global `DEV/CURRENT_PROGRESS.md` now records version normalization as complete/verified while preserving `WP20_STEP2_AUTHORIZED: NO` and the mandatory Senior-review gate.

## Local serialized schema / protocol bump inventory

Each affected local serialized contract was incremented at most once for this normalization:

- campaign manifest: `3 -> 4` — adds required campaign-contract generation and ruleset digest-generation provenance;
- DND storage marker: `3 -> 4` — `storage_format_version` renamed to `storage_format_generation`;
- checkpoint: `2 -> 3` — persisted ruleset digest gains explicit generation context;
- runtime package metadata: `2 -> 3` — escaping ruleset-set digest gains explicit generation context;
- ruleset package manifest: `1 -> 2` — package revision / compatibility family+generation / integer catalog generation replace legacy fields;
- resolved ruleset lock: `1 -> 2` — normalized package/compatibility/catalog axes plus digest generation;
- ruleset engine-contract inventory: `1 -> 2` — digest-generation context added;
- ruleset compatibility result: `1 -> 2` — normalized identity/generation shape;
- ruleset conformance attestation: `1 -> 2` — digest-generation context added;
- `DEV/CATALOG/core-catalog.json`: `1 -> 2` — coordinated catalog field renamed/type-normalized;
- `DEV/CATALOG/identifier-policies.json`: `1 -> 2` — coordinated catalog field renamed/type-normalized;
- activity-primitive-contracts manifest: `1 -> 2` — catalog generation type normalized;
- catalog-admission-ledger manifest: `1 -> 2` — catalog/ruleset identity shape normalized;
- ruleset-package-closure evidence: `1 -> 2` — normalized ruleset identity plus digest generation;
- house-rules mechanical-boundary evidence: `1 -> 2` — normalized ruleset identity plus digest generation;
- built-in gameplay-spine seed: `1 -> 2` — normalized package/compatibility/catalog identity axes.

Runtime resolution/continuation and related execution JSON Schemas were strengthened with explicit digest/fingerprint generation fields, but those serialized objects do not own a local `schema_version` field; this task did not invent a new schema counter solely for symmetry.

## Reverse-audit and verification evidence

Hosted `Validate engine source` run `33973592843` on `8a5cec0c232c30d095dcf4c5f211522487daa343`:

- maintenance audit: PASS (`OK: engine consistency audit passed`);
- full DEV unit suite: PASS, `419` tests;
- canonical release integration/reproducible runtime ZIP build + extracted package/generator smoke: PASS within the full suite;
- `VERSION_LEGACY_HITS=[]`;
- census unclassified hits: `0`;
- census classifications: current machine/runtime `887`, current normative documentation `495`, current test/fixture `434`, historical provenance `956`, intentional negative fixture `22`, intentional negative guard `3`, external version namespace `4`, non-version semantic identifier `9`.

The three intentional current negative guards are rejection checks only:

- `DEV/TOOLS/audit_engine.py` rejects `storage_format_version`;
- `GAME/TOOLS/ruleset_package.py` rejects `package_version`;
- `GAME/TOOLS/ruleset_package.py` rejects `compatibility_id`.

External workflow action versions and SRD `5.2.1` license/baseline identifiers remain external/non-HDM namespaces. Historical design/research/plan occurrences remain historical provenance and were not rewritten.

## Review gate

Coordinator review against the approved implementation brief/spec and the complete BASE_SHA -> verified-head diff found:

- no change outside the approved versioning Impact Envelope requiring a System-Impact decision;
- no DEV bookkeeping revision drift beyond the four approved counters;
- no pre-release compatibility shim, alias, migration edge or obsolete-hash preservation;
- no WP-20 Step-2 architecture or migration implementation;
- large formatting deltas in `mechanical-surfaces` artifacts were checked through their current schemas, registry/selector closure tests and full green machine suite rather than treated as semantic authority changes.

The Superpowers reviewer-subagent mechanism is not available in this ChatGPT harness, so no independent subagent review is claimed. The repository's separately mandated Senior review remains the authoritative human/project review gate before further WP-20 work.

## Changed-file accounting at verified implementation head

Against BASE_SHA, the implementation/reconciliation diff contains `85` changed files:

- `DEV`: `65`;
- `GAME`: `20`;
- root infrastructure/docs: `0`.

The branch is strictly ahead of BASE_SHA with no divergence.

## System-Impact Gate

SYSTEM_IMPACT: NONE

All implementation changes were mechanically implied by the already-approved versioning amendment and Impact Envelope. No new persistent owner, authority boundary, migration policy, compatibility promise, product semantic or material trade-off requiring human architecture judgment was introduced. No WP-20 Step 2 work was started.

## Compatibility / scope closure

PRE_RELEASE_COMPATIBILITY_SHIM_OR_MIGRATION_DEBT_ADDED: NO
WP20_STEP2_STARTED: NO
REAL_CAMPAIGN_MIGRATION_EXECUTED: NO

## Remaining project gate

Implementation execution has no known blocker or remaining implementation task. This status-record publication itself must receive the normal branch CI/read-back before completion is reported externally.

After that verification, the only remaining gate is the already-existing project gate:

```text
NEXT_AUTHORIZED_UNIT: NONE — MANDATORY SENIOR REVIEW
WP20_STEP2_AUTHORIZED: NO
```

A Senior GO is therefore required before starting WP-20 Step 2. This implementation does not authorize WP-21 or any later work package.

KNOWN_BLOCKERS: NONE
UNPUBLISHED_WORK: NONE
