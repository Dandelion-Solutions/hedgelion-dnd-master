# R2.7 WP-23 — Step 3 Decision Brief

Status: **STEP 3 COMPLETE — OWNER-CONSTRAINED DECISION / NO NEW HUMAN CHOICE**

Date: 2026-09-08

Evidence owner:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-step-2-evidence-reconciliation.md`.

This brief chooses no new licensing policy, compatibility policy, release product policy or authority model. The Product Owner already fixed the public-provenance boundary, and accepted package/version/update/legal owners constrain the remaining composition.

---

## 1. Decision question

What final WP-23 architecture can make release/package/version/legal readiness coherent without:

- treating Lane A/B/C as independent passes;
- collapsing semantic version, exact package provenance and archive digest;
- claiming future release execution or fresh-environment acceptance as current proof;
- reopening accepted WP-20 law without an actual insufficiency;
- creating a new global release/currentness/compatibility authority;
- retaining prohibited source-specific development/research provenance in current public `DEV/` or `GAME/`?

---

## 2. Alternatives

### Alternative A — independent lane closure

Package, version/update and legal/provenance each receive a separate local PASS.

**Rejected.** A locally correct all-`GAME` builder can still package prohibited public material; correct version metadata can still describe an unpublished artifact; legal-file parity can coexist with unrelated prohibited development provenance.

### Alternative B — new global release-readiness registry/manifest

Create one new persistent registry that owns release identity, compatibility, legal state and release readiness.

**Rejected.** It would duplicate existing owners (`ENGINE_VERSION`, generated package provenance, archive digest, WP-20 compatibility owners, legal payload, workflow/currentness evidence) and create a false scalar/global authority.

### Alternative C — owner-composed release chain with staged proof classes

Keep native owners separate and define WP-23 as their required release-facing composition:

```text
source-owner conformance
-> release identity conformance
-> package construction conformance
-> exact artifact provenance + digest
-> install/runtime-root conformance
-> update/migration eligibility under existing owners
-> legal/approved attribution conformance
-> public provenance hygiene
-> publication evidence when a real release occurs
-> fresh-environment acceptance when a real release occurs
```

**Selected.** This is the only alternative consistent with current owners and Step-2 evidence.

---

## 3. Selected architecture decisions

### D23-01 — Release readiness is a composition, not a new owner

WP-23 defines required composition and proof boundaries. It does not create a global release registry, universal compatibility epoch or second currentness authority.

### D23-02 — Identity axes remain separate

Semantic release identity, exact built-package provenance and final archive digest retain independent meanings. Tag/release metadata is publication evidence, not replacement identity.

### D23-03 — Proof class follows actual stage

The architecture distinguishes:

```text
CURRENT_ARCHITECTURE_REQUIREMENT
CURRENT_MACHINE_BUILD_REALIZATION
IMPLEMENTATION_ONLY_OBLIGATION
DEFERRED_UNTIL_REALIZATION
RELEASE_TIME_OBLIGATION
POST_IMPLEMENTATION_ACCEPTANCE
```

Source CI/build success may establish only the checks it actually runs. It cannot establish a future release upload or fresh-project acceptance.

### D23-04 — GAME passthrough remains open-world

Do not replace all-`GAME` passthrough with a hand-maintained package allowlist merely to solve provenance hygiene. Instead, public-tree hygiene becomes a prerequisite of distributable-package readiness.

### D23-05 — Public provenance boundary is repository-wide

Current public `DEV/` and `GAME/` must not retain source-specific development/research provenance. Sanitation is purpose-based and preserves:

- independently stated HDM semantics;
- required legal/license attribution;
- explicitly approved attribution;
- HDM technical artifact provenance;
- internal HDM evidence and source-neutral/rewrite-safe research.

Historical current-tree placement is no exemption; Git history is not rewritten.

### D23-06 — Operational dependencies are not automatically provenance violations

Current product/platform names, official runtime rules-source routing, licensors and technical identifiers may remain where they are current semantic/operational/legal facts rather than development-source history.

### D23-07 — WP-20 remains closed

WP-23 consumes accepted released-v1.0+ compatibility/migration architecture. Future edge/transform realization remains conditional on released evolution. No current contradiction or unsatisfied release consumer requires reopening WP-20.

### D23-08 — Production release acceptance remains future evidence

A final WP-23 architecture PASS cannot itself certify the product as production-release-ready. Actual tag/release execution, produced asset identity/checksum and fresh-environment acceptance are release-time evidence.

---

## 4. Architecture-stage consistency realization

The current PO provenance decision requires finite current-tree consistency repairs during WP-23:

1. remove/sanitize confirmed source-specific development narrative from current runtime/architecture material while preserving HDM-native semantics;
2. retire current-tree source-history research documents where accepted current owners already preserve the durable HDM decision and no unique semantic/defer obligation would be lost;
3. source-neutralize mixed topology/transport evidence rather than deleting unique HDM conclusions;
4. replace stale machine checks that require prohibited provenance with behavior/policy conformance checks;
5. preserve legal payload and technical artifact provenance;
6. reconcile routing after any retirement/sanitation.

These are realization/consistency actions under an already accepted owner decision, not a new licensing policy or broad runtime implementation.

---

## 5. Consequences and rejection tests

The selected architecture must reject each false inference:

- reproducible ZIP -> production release ready;
- green source CI -> published release accepted;
- recommended tag -> exact package bytes;
- same semantic version -> compatibility of different released bytes;
- Git ancestry -> migration support;
- `research/` path -> automatic permission to retain source-specific provenance;
- external name/URL presence -> automatic provenance violation;
- legal-file presence -> complete public-provenance hygiene;
- future migration machinery absent -> current prerelease defect.

---

## 6. Gate

```text
SELECTED_ALTERNATIVE: C — OWNER-COMPOSED RELEASE CHAIN WITH STAGED PROOF CLASSES
HUMAN_DECISION_REQUIRED: NO
PO_PROVENANCE_DECISION_APPLIED: YES
WP20_REOPEN_REQUIRED: NO
NEW_WORKSTREAM_REQUIRED: NO
STEP3_COMPLETE: YES
NEXT_PROCESS_UNIT: STEP 4 COLLABORATIVE / CROSS-SYSTEM REVIEW
```
