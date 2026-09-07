# R2.7 WP-23 — Step 4 Cross-System Collaborative Review

Status: **STEP 4 COMPLETE — CROSS-SYSTEM REVIEW PASS WITH CARRY-FORWARD CONDITIONS**

Date: 2026-09-08

Reviewed direction:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-step-3-decision-brief.md`;
- Step-2 evidence reconciliation;
- current package/build/install/update/legal/verification consumers.

This review tests the selected owner-composed release chain against neighboring systems. It does not certify a production release.

---

## 1. Review lenses

### 1.1 Package/build lens

Current builder and release-integration tests support the selected boundary:

```text
GAME source
-> validated flat runtime ZIP
-> generated RUNTIME_PACKAGE provenance
-> final SHA-256
-> extracted package-root validation
-> packaged init_campaign smoke
```

The open-world `GAME/` passthrough is intentional and should not be replaced with a manually curated include list to solve Lane C.

**Review result:** compatible with D23-01..D23-04.

### 1.2 Install/runtime lens

Install/bootstrap contracts require exact package root and exact runtime binding, reject repository source archives as runtime assets, and prevent cross-version file mixing.

A provenance sanitation that changes only development/source-history prose must not alter these runtime-root laws.

**Review result:** no conflict.

### 1.3 Version/update/migration lens

WP-20 and current `ENGINE_UPDATES.md` already separate semantic version, exact artifact identity, compatibility evidence and migration authority. The selected WP-23 composition consumes those laws without inventing a release-level compatibility shortcut.

**Review result:** `WP20_REOPEN_REQUIRED: NO`.

### 1.4 Legal/attribution lens

Required legal/approved attribution is a distinct preserve-class. Release builder parity checks and runtime legal payload remain valid consumers.

The public-research sanitation rule must never be implemented as a generic “remove third-party names/URLs” transform because that would destroy permitted legal/operational material.

**Review result:** selected classification is necessary.

### 1.5 Public provenance lens

Current-tree source-history content is incompatible with the Product Owner boundary even when historical or noncanonical. However, deleting mixed artifacts wholesale could discard HDM-native conclusions, safe-defer triggers or technical publication evidence.

**Review result:** sanitation must be item-level and conclusion-preserving.

### 1.6 Verification lens

Current release integration test provides deterministic source-tree evidence for reproducible package construction, flat shape, generated provenance and packaged campaign-generator smoke.

Current source CI runs maintenance audit + DEV unit tests. Neither route executes a production tag publication or a fresh ChatGPT Project install from an uploaded Release asset.

**Review result:** proof classes in Step 3 are correct and must remain explicit in the candidate/final spec.

---

## 2. Cross-system review findings

### S4-01 — provenance hygiene cannot be a global string blacklist

**Severity:** SIGNIFICANT design condition.

A blanket prohibition on external product/source names or URLs would conflict with:

- mandatory legal attribution;
- current operational rules-source routing;
- actual host/platform dependency names;
- repository/release identity;
- technical artifact provenance.

**Required candidate law:** classify by purpose/authority; machine scans may be bounded regression evidence only, not a substitute for semantic reconciliation.

### S4-02 — mixed historical artifacts require semantic preservation before sanitation

**Severity:** SIGNIFICANT design condition.

`GAME/CORE/SOURCES.md`, several architecture documents, infrastructure topology evidence and transport feasibility evidence mix source-history material with reusable HDM conclusions.

**Required candidate law:** preserve or rehome HDM-native conclusions/exclusions/revisit triggers before removing source-specific development trail.

### S4-03 — no false release PASS from source verification

**Severity:** SIGNIFICANT design condition.

A passing builder/integration test can establish only source-build invariants. A green source workflow can establish only checks actually executed at exact HEAD.

**Required candidate law:** actual tag workflow, uploaded asset identity/checksum and fresh-environment acceptance remain release-time proof.

### S4-04 — legal copies and technical provenance are protected consumers

**Severity:** SIGNIFICANT design condition.

Sanitation must not remove root/runtime legal parity, generated package provenance, source commit/ref where valid, archive digest, migration lineage, version/generation identities or publication/currentness evidence.

**Required candidate law:** explicit preserve classes.

### S4-05 — no implicit implementation candidate survives from historical prior-art prose

**Severity:** SIGNIFICANT design condition.

A noncanonical proposal currently names an external implementation candidate. After the PO provenance decision, historical preference must not silently become an implementation requirement.

**Required candidate law:** implementation component selection requires current HDM requirements/approved implementation planning, not retained prior-art preference.

### S4-06 — current operational dependencies remain nameable

**Severity:** MINOR clarification.

The public-provenance decision does not require euphemistic removal of the actual supported host, repository transport, rule-source authority or licensor where those are current product/legal facts.

**Required candidate law:** distinguish operational fact from development-source history.

### S4-07 — version impact must follow semantic effect, not shipped-file presence alone

**Severity:** MINOR clarification.

`GAME/CORE/SOURCES.md` is shipped, but source-history sanitation does not by itself change gameplay semantics, schema/generation, compatibility behavior or engine release identity if the runtime file remains a non-behavioral routing/provenance boundary.

**Required candidate law:** apply final Version Impact Gate to actual resulting change set; do not mechanically bump merely because a shipped documentation/routing file changed.

---

## 3. Negative and boundary review

The selected direction does **not** authorize:

- release/tag/deployment execution;
- broad runtime refactor;
- new migration registry or compatibility epoch;
- private Lab import;
- Git history rewrite;
- external legal research;
- root README rewrite;
- removal of required attribution;
- deletion of internal/source-neutral HDM evidence merely because it is under `research/`.

No reviewed neighbor requires any of those actions for WP-23 closure.

---

## 4. Candidate requirements carried forward

Step 5 must encode at least:

1. one owner-composed release readiness chain;
2. explicit semantic-package-digest identity separation;
3. current-build versus release-time proof separation;
4. open-world `GAME/` passthrough plus public-tree hygiene prerequisite;
5. repository-wide prohibited development/research provenance boundary;
6. preserve classes for legal/approved attribution and HDM technical provenance;
7. item-level sanitation with HDM conclusion/revisit-trigger preservation;
8. bounded machine verification that does not claim semantic-universe completeness;
9. WP-20 non-reopen and deferred released-v1.0+ realization discipline;
10. explicit fail-closed requirements for malformed/mixed package identity and unsupported/indeterminate compatibility;
11. final Version Impact classification from actual Step-7/8 realization.

---

## 5. Gate

```text
STEP4_CROSS_SYSTEM_REVIEW: PASS
BLOCKING_FOUND: 0
SIGNIFICANT_DESIGN_CONDITIONS: 5
MINOR_CLARIFICATIONS: 2
NEW_HUMAN_DECISION_REQUIRED: NO
WP20_REOPEN_REQUIRED: NO
NEXT_PROCESS_UNIT: STEP 5 CANDIDATE SPECIFICATION
```
