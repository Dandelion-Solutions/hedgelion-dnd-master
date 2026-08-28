# S6D-11 — Tests and Machine-Contract Closure — Whole-Project Brief Critic

Status: **SENIOR-AUDIT REPAIR PASS — 0 BLOCKING / 0 SIGNIFICANT / 0 MINOR**

Date: 2026-08-28

Reviewed artifact:

- `DEV/docs/superpowers/specs/2026-08-28-s6d-11-tests-machine-contract-closure-task-brief.md`

Authoritative review baseline:

- repository `Dandelion-Solutions/hedgelion-dnd-master`;
- branch `v1/engine-rearchitecture`;
- pre-publication head `66c4c3716b8338d081ab21dbbe1d44973a0df5ae`.

## 1. Whole-project review mandate executed

The critic used the current `DEV/PROJECT_MAP.md` to reconstruct the direct and indirect dependency graph rather than reviewing S6D-11 in isolation. It checked:

- `AGENTS.md`, both design-process owners, current roadmap and S6D umbrella decision/brief/plan;
- S6D-01 package identity and S6D-02 catalog admission/resolution owners;
- current bounded package content and S6D-03…10 owner/machine/test routes;
- Step-2/3 execution ownership and Step-5 retry/recovery/currentness routes;
- bootstrap, installer, `ENGINE_UPDATES`, access control and campaign projection boundaries;
- ruleset-package builder/loader versus runtime release-builder and shipped-package boundaries;
- package activation, unsupported/dormant/quarantined/conformance-only classifications;
- S6D-12 and R2.7 sequencing boundaries.

## 2. Initial findings

Initial verdict: **FAIL — 0 BLOCKING / 2 SIGNIFICANT / 1 MINOR**.

### S1 — changed ruleset-set handling collapsed distinct accepted paths

The initial brief treated every changed `ruleset_set_sha256` as campaign-creator adoption. Current `RULESET_PACKAGE_IDENTITY.md`, `ENGINE_UPDATES.md` and `ACCESS_CONTROL.md` instead distinguish:

- unchanged-set silent maintenance;
- a compatible/additive changed set inside a proven forward same-engine-version/runtime-package descendant, which may be used immediately and silently, including by a non-creator, while only the creator may later persist coherent `engine.current` plus sibling `ruleset.current` pointers;
- semantic-version, incompatible, backward, diverged or ambiguous replacement, which uses the creator adoption/migration flow.

Repair applied: §5.7 now separates and tests every classification and non-creator boundary and forbids using digest inequality alone as an adoption prompt.

### S2 — manifest/digest wording allowed self-reference or duplicate digest authority

The initial brief could be read as requiring an authoritative member-digest table inside the hashed manifest. The accepted S6D-01 owner requires the manifest to declare exact `content_files[]`, including the manifest itself, while builder-derived evidence computes exact member hashes and `content_sha256`; the resolved lock records resulting package snapshot identities/dependency edges.

Repair applied: §§3A and 5.2 now state the non-self-referential boundary explicitly. The manifest cannot store its own snapshot digest or an overriding authoritative self/member digest table. §5.6 adds a negative mutation for embedded/self-referential or overriding digest claims.

### M1 — stale roadmap subsection

Roadmap §7 still said only “S6D-10 Step 1 is closed,” although the header, dependency graph and continuation cursor correctly record S6D-10 Steps 1–8 complete.

Repair applied: brief §10 explicitly requires publication-time synchronization of that stale subsection.

## 3. Final re-review

Final verdict: **PASS — 0 BLOCKING / 0 SIGNIFICANT / 0 MINOR**.

The re-review confirmed:

- update/adoption paths now match current identity/update/access owners;
- manifest hashing is explicitly non-self-referential and builder/lock authority is exact;
- roadmap synchronization is an explicit Step-1 publication requirement;
- no new package/catalog owner, activation authority, product-scope expansion, DEV-to-runtime authority leak, S6D-12 scope theft or false verification claim was introduced;
- item-level bidirectional equality, typed failure closure, executable evidence honesty, Mechanical-Null behavior and dormant/quarantine/nonselectable boundaries remain explicit;
- the brief remains Step 1 only and stops before Step 2.

## 4. Gate result

The S6D-11 Architecture Task Brief satisfies the mandatory whole-project Step-1 critic gate. It is ready for authoritative publication and human review. S6D-11 Step 2 remains not started.

## 5. Senior Auditor HOLD and narrow Step-1 repair

Senior Auditor subsequently held Step 1 at **0 BLOCKING / 2 SIGNIFICANT** without reopening product scope or Step 2.

### SA-S1 — transitional package identity

Verified current transitional carriers include the per-file and aggregate identity fields in `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-capabilities.json`, READY_PC/readiness evidence that consumes the aggregate identity, and `DEV/CATALOG/house-rules-mechanical-boundary.json` `identity_bound_package_candidate.content_set_sha256`. Other S6D-07/09 capability/product attestations, validators, schemas, tests, fixtures and projections may also consume the old aggregate and require census rather than assumption.

Repair: the brief now creates `TRANSITIONAL_PACKAGE_IDENTITY_KEYS` and requires field/attestation-level accounting of every carrier and consumer with one final disposition:

```text
REMOVE
DERIVED_NONAUTHORITATIVE
MIGRATE_TO_CANONICAL_PACKAGE_IDENTITY
MIGRATE_TO_CANONICAL_RULESET_SET_IDENTITY
```

Demotion is constrained so the old aggregate cannot survive under an alias or retain selection/reconstruction/override authority. Activation remains blocked on any undispositioned item. The only authoritative chain allowed after S6D-11 is manifest plus exact semantic bytes -> computed package snapshot -> exact lock -> `ruleset_set_sha256`.

### SA-S2 — machine-verifiable changed-set compatibility

The earlier brief preserved the correct same-version authority paths but did not fully specify how `compatible/additive` becomes proven rather than declared.

Repair: §5.3A now requires an exact fail-closed comparison contract between the fully validated currently adopted set and candidate forward set. It must identify exact set/manifest/content/catalog/schema/mechanical/consumer/durable-dependency inputs, semantic owner per assertion, deterministic validator owner, a closed machine-readable result/reason evidence bound to both set identities, the pre-use detection point, retained retry/recovery/audit evidence and per-family negative mutations. Ancestry, matching `compatibility_id`, matching `catalog_generation`, candidate declaration and standalone candidate-load PASS are explicitly insufficient. Missing semantic equivalence evidence blocks changed-set silent use.

The existing non-creator law is preserved: immediate same-version changed-set use remains available only after this comparator proves compatible/additive; coherent pointer persistence and incompatible/ambiguous adoption authority remain unchanged.

## 6. Renewed whole-project critic

Renewed verdict: **PASS — 0 BLOCKING / 0 SIGNIFICANT / 0 MINOR**.

The renewed critic confirmed:

- mandatory transitional seeds cover character capabilities, READY_PC/readiness, S6D-07/09 package/product evidence, S6D-10 candidate identity and all discovered schemas/validators/tests/fixtures/projections;
- every transitional carrier and consumer receives item-level authority/use/replacement/disposition and positive/negative proof;
- one canonical package-snapshot chain is an explicit activation exit condition;
- the compatibility comparator is exact, owner-grounded and fail-closed before candidate silent use;
- declarations/labels/ancestry/load success cannot substitute for semantic comparison;
- unprovable changed-set compatibility remains blocked;
- manifest self-hash prohibition, Mechanical-Null, dormant/quarantine/conformance-only nonactivation, DEV/runtime separation, bounded MVP scope and S6D-12/R2.7 sequencing remain unchanged.

Final gate result: the repaired S6D-11 Step-1 brief satisfies the Senior-Auditor repair and mandatory renewed whole-project critic. S6D-11 Step 2 remains not started pending Senior Auditor acceptance.

