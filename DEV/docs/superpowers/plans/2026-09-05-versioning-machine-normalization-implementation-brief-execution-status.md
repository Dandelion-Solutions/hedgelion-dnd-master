# Versioning machine normalization — execution status

PLAN: `DEV/docs/superpowers/plans/2026-09-05-versioning-machine-normalization-implementation-brief.md`
SPEC: `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md`
BASE_SHA: `e7bb57853b2b1aa300831f88db6c201411c4795e`

STATUS: EXECUTING_FINAL_GATES
CURRENT_TASK: Task 12/13 — reverse audit, review and final verification
LAST_COMPLETED_TASK: Task 10/11 — current-facing documentation normalization and machine enforcement
LAST_VERIFIED_SHA: `d97e16c3c7cc34743428e617518a876e6e3483f2`
LAST_VERIFIED_CI_RUN: `33973319834`

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
- DEV bookkeeping matches the approved target: `storage_format_revision: 5`, `persistence_revision: 9`, `campaign_identity_revision: 3`, `consistency_audit_revision: 6`; other DEV revision counters were not opportunistically changed.
- Current-facing versioning/release/catalog/ruleset/storage/migration documentation was reconciled to realized namespace names and generations; historical research/design/plans remain unchanged as provenance.
- Root README was checked and required no targeted versioning correction under its separate editorial contract.

## Reverse-audit evidence at LAST_VERIFIED_SHA

Hosted `Validate engine source` run `33973319834` on `d97e16c3c7cc34743428e617518a876e6e3483f2`:

- maintenance audit: PASS (`OK: engine consistency audit passed`);
- full DEV unit suite: PASS, `419` tests;
- `VERSION_LEGACY_HITS=[]`;
- census unclassified hits: `0`;
- census classifications: current machine/runtime `887`, current normative documentation `496`, current test/fixture `434`, historical provenance `925`, intentional negative fixture `22`, intentional negative guard `3`, external version namespace `4`, non-version semantic identifier `9`.

The three intentional current negative guards are rejection checks only:

- `DEV/TOOLS/audit_engine.py` rejects `storage_format_version`;
- `GAME/TOOLS/ruleset_package.py` rejects `package_version`;
- `GAME/TOOLS/ruleset_package.py` rejects `compatibility_id`.

External workflow action versions and SRD `5.2.1` license/baseline identifiers remain external/non-HDM namespaces. Historical design/research/plan occurrences remain historical provenance and were not rewritten.

## System-Impact Gate

SYSTEM_IMPACT: NONE

All implementation changes were mechanically implied by the already-approved versioning amendment and Impact Envelope. No new persistent owner, authority boundary, migration policy, compatibility promise, product semantic or material trade-off requiring human architecture judgment was introduced. No WP-20 Step 2 work was started.

## Remaining final gates

- Superpowers review gate against the approved plan/spec and final diff.
- Fresh final release build/package validation evidence on the post-status final SHA.
- Fresh final hosted CI on the post-status final SHA.
- Final remote branch read-back and changed-file accounting.
- Reconcile current progress/roadmap status without activating WP-20 Step 2.

KNOWN_BLOCKERS: NONE
UNPUBLISHED_WORK: NONE
