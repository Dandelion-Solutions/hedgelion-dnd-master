# S6D-11 — Tests and Machine-Contract Closure — Step 2 Research and Architecture Draft

Status: **STEP 2 COMPLETE — EVIDENCE / ARCHITECTURE DRAFT**

Date: 2026-08-28

## 1. Question and method

This investigation tests whether the accepted S6D-01…10 architecture can be realized as one exact package manifest/snapshot/lock/load chain, one bounded built-in package, one reconstructable `ResolvedCatalogContext`, and one executable conformance closure without retaining transitional identity or inventing compatibility by declaration.

The current authoritative branch was read at `b75be4de44cd0b6a0ad48b3ffae2e38243053bb1`. Source selection followed `DEV/PROJECT_MAP.md`, the S6D-11 Task Brief and the process pair. Current owners, machine contracts, validators, tests, runtime projections and package members were inspected rather than inferred from prior summaries.

## 2. Source-role summary

### Canonical / owning

- `RULESET_PACKAGE_IDENTITY.md` — digest, resolved-set, projection and refresh laws;
- `CATALOG_RESOLUTION.md`, `CATALOG_ADMISSION.md`, `CATALOG_CONTRACTS.md` — definition uniqueness, package plan and failure boundary;
- S6D-03…10 canonical owners — active selector/accessor/value/primitive/seed/domain/adjudication surfaces;
- Step-3 Resolution/Continuation and Step-5 retry/recovery/currentness owners;
- `ENGINE_UPDATES.md`, `ACCESS_CONTROL.md`, `BRANCH_MODEL.md` — use, persistence and adoption authority;
- campaign manifest/checkpoint and runtime release-package contracts — physical projections.

### Machine / implementation evidence

- the four current package JSON members plus `NOTICE.md`;
- current S6D catalogs, schemas, validators and focused tests;
- `release_builder.py`, `run_release_build.py`, release tests and CI entry points;
- campaign template and `init_campaign.py`.

### Derivative / historical

- roadmap/project map are routing/status only;
- prior candidate/review artifacts explain derivation but never override current owners.

## 3. Current physical findings

### 3.1 The built-in package has no canonical manifest or resolved lock

`character-capabilities.json` currently mixes product capability metadata with a transitional package identity:

```text
content_file
content_sha256
content_files[].sha256
content_set_sha256
```

It omits the accepted `compatibility_id`, engine requirement, namespaces, exact dependencies and self-including manifest path set. The aggregate is not the S6D-01 package snapshot digest because it excludes manifest bytes and uses a different preimage. There is no current exact dependency-closed resolved lock or `ruleset_set_sha256` instance.

### 3.2 Transitional identity consumers are active machine evidence

The item-level census found these active families:

| Carrier/consumer | Current use | Required disposition |
|---|---|---|
| `character-capabilities.json.content_file` | selects character seed | REMOVE; semantic manifest declares files, capability file keeps only capability data |
| `.content_sha256` | asserts one member identity | REMOVE; package snapshot builder owns member verification |
| `.content_files[].sha256` | asserts three-member set | REMOVE; canonical manifest owns paths, builder computes hashes |
| `.content_set_sha256` | aggregate candidate identity | REMOVE; not canonical package/set identity |
| `validate_character_mvp_seed.py` | validates one member; binds READY_PC evidence to aggregate | MIGRATE to canonical package loader and `ruleset_set_sha256` |
| S6D-07 fixtures/tests | emit/assert `package_content_set_sha256` | MIGRATE to canonical resolved-set identity |
| S6D-08 package content-set helper/test | validates old list/hash aggregate | MIGRATE to canonical manifest/snapshot loader proof |
| S6D-09 coverage `package_binding.content_set_sha256` and generator | binds coverage to aggregate | MIGRATE to `ruleset_set_sha256` plus exact member path |
| S6D-09 validator package-member check | trusts old per-member table | MIGRATE to canonical loader result |
| S6D-10 boundary candidate/schema/validator/tests | hardcodes aggregate candidate | MIGRATE to canonical resolved-set identity and verified selection state |
| release/runtime package provenance | currently has no resolved ruleset lock | MIGRATE to generated exact lock/set projection |
| campaign MANIFEST/template/init/checkpoint | engine-only projection; missing sibling ruleset identity | MIGRATE to S6D-01 sibling projection; checkpoint remains nonauthoritative |
| Resolution/Continuation schemas | fingerprint only; missing exact set identity | MIGRATE to required `ruleset_set_sha256` pin |

Historical design files and explicit negative fixtures may mention the retired names as history/nonacceptance evidence. No current selector, readiness, coverage, policy, package-load or runtime projection may treat the aggregate as authority.

### 3.3 Release composer and ruleset loader are different boundaries

The release builder recursively composes `GAME/`, validates runtime-package provenance and creates the final ZIP. It does not currently resolve semantic ruleset packages. Replacing it with a ruleset solver would collapse concerns. The correct integration is:

```text
ruleset package contract module
    -> validate manifests + exact bytes
    -> resolve lock + ruleset_set_sha256
    -> return bounded generated evidence

release builder
    -> calls that contract during build
    -> embeds exact resolved lock/set identity in generated RUNTIME_PACKAGE metadata
    -> continues to own runtime composition/ZIP provenance
```

A development reference validator may implement the pure contract for conformance. Runtime must never read `DEV/`; the manifest and generated lock/provenance it consumes live in shipped `GAME/` material.

### 3.4 Current projections are incomplete

S6D-01 requires sibling campaign `ruleset.created_with/current`, exact accepted Resolution/Continuation set identity, and runtime-package advertised lock. Current campaign schema/template/init and execution schemas do not yet realize those requirements. This is current S6D-11 scope, not a new migration obligation: no compatible released campaigns exist.

## 4. Compatibility evidence analysis

### 4.1 Insufficient signals

None of the following proves semantic compatibility:

- source ancestry;
- matching package ID/version;
- matching `compatibility_id`;
- matching `catalog_generation`;
- successful independent candidate load;
- candidate-authored compatibility assertion.

They prove provenance, declared line or internal validity, not preservation of the adopted semantic surface.

### 4.2 Exact conservative proof available from current owners

The current bounded package and machine contracts allow a fail-closed monotonic-superset comparison.

For each adopted package and every existing semantic key, construct a canonical entry:

```text
entry_key = package_id + semantic kind + stable ID/path role
entry_hash = SHA-256(canonical JSON semantic value)
```

The comparison requires:

1. same engine version/package line and accepted compatibility/catalog predicates;
2. every adopted package dependency and namespace claim preserved without conflict;
3. every adopted reusable definition/Activity/value/capability entry present in candidate with the same kind and canonical semantic hash;
4. every active primitive/selector/accessor/fact/schema/portable-value/coverage/policy-boundary contract entry present with the same canonical semantic hash;
5. every adopted dependency key required by durable state, accepted work or frozen embedded values present and unchanged;
6. candidate-only entries use new noncolliding IDs/namespaces and are independently valid.

This proof is deliberately conservative. A semantically equivalent rewrite with different canonical structure is blocked unless a future explicit owner supplies machine-verifiable equivalence/migration. That is correct for silent refresh: false negatives route to creator adoption/review; false positives could corrupt accepted mechanics.

### 4.3 Comparison result

The machine result is closed:

```text
COMPATIBLE_ADDITIVE
BLOCKED_INCOMPATIBLE
BLOCKED_INSUFFICIENT_EVIDENCE
```

It binds adopted and candidate `ruleset_set_sha256` values, comparison-contract version, exact evidence inventory digest, and ordered reason rows. It is computed only after both sets independently load and before candidate context use. It grants no persistence/adoption authority.

## 5. Candidate architecture

### 5.1 Package files

`ruleset-package-manifest.json` becomes the only package declaration. It includes itself in `content_files[]` but no digest. `character-capabilities.json` remains semantic product capability metadata and loses all package snapshot fields.

The package snapshot builder computes exact member hashes and `content_sha256`. For the current one-package root set, the dependency-closed lock has one entry and the lock digest is `ruleset_set_sha256`.

### 5.2 Schemas and evidence

- strict ruleset-package-manifest schema;
- strict resolved-ruleset-lock schema including closed load failure reasons;
- strict ruleset-set compatibility-result schema;
- integrated S6D-11 closure ledger containing transitional dispositions, required equality sets, projection obligations and proof IDs;
- pure standard-library reference builder/loader/comparator with no network, glob, ambient recursion, symlink, arbitrary code or LLM surface.

### 5.3 Existing-owner amendments

- READY_PC and package capability evidence bind to canonical set identity;
- S6D-09 coverage and S6D-10 boundary bind to canonical set identity;
- Resolution and Continuation require set identity alongside the derived context fingerprint;
- campaign MANIFEST/template/init add sibling ruleset projections;
- checkpoint may repeat current set identity only as a nonauthoritative recovery projection;
- release builder embeds the generated lock and set digest in runtime provenance without becoming ruleset semantic owner.

## 6. Alternatives

### A. Keep old aggregate as alias

Rejected. It permits two identities over overlapping bytes, keeps consumer ambiguity and cannot represent manifest/dependency closure.

### B. Canonical migration with narrowly derived diagnostics — recommended

Remove the aggregate from all authoritative consumers. Permit only builder-derived per-member hashes in diagnostic output that cannot select/reconstruct/override. Bind each consumer to package snapshot or resolved-set identity according to its dependency scope.

### C. Accept declared compatibility inside one line

Rejected. It contradicts S6D-01 and cannot protect durable/accepted mechanics.

### D. Require byte-identical whole package for every silent refresh

Safe but unnecessarily rejects additive definitions. The monotonic entry-superset comparator is equally fail-closed for existing semantics and supports the accepted additive path.

## 7. Decision-rights result

No material human decision remains. Existing owners determine the only coherent technical result:

- one canonical identity chain;
- old aggregate removed/demoted/migrated item by item;
- monotonic machine-verifiable compatibility proof;
- insufficient evidence blocks silent use;
- existing non-creator/creator authority split remains unchanged.

Step 3 should record `NO HUMAN DECISION REQUIRED` and proceed.

## 8. Step-2 completeness gate

- current owners, machine contracts and consumers inspected;
- transitional carriers/consumers accounted at item level;
- qualifiers and non-goals preserved;
- package/release/runtime boundaries reconciled;
- compatibility proof inputs and failure mode established;
- no conclusion depends only on roadmap, memory or thematic sampling;
- remaining work is technical formalization, tests and cross-system review.

