# S6D-11 — Tests and Machine-Contract Closure — Whole-Project Brief Critic

Status: **PASS — 0 BLOCKING / 0 SIGNIFICANT / 0 MINOR**

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

