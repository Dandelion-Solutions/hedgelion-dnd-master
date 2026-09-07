# HDM Public Research-Provenance and Attribution Owner Decision

Status: **OWNER-APPROVED / CANONICAL PRODUCT POLICY**

Date: 2026-09-08

## 1. Decision

Public HDM material under `DEV/` and `GAME/` SHALL NOT retain source-specific development/research provenance whose purpose is to record which named external sites, authors, projects, products, papers, research sources, or comparable third-party materials were consulted during development, nor to narrate which HDM ideas were derived from such sources.

The only permitted attribution exceptions are:

1. attribution, notices, license text, copyright statements, or source identification required by an applicable license or other legal obligation; and
2. attribution that the Product Owner has separately and explicitly approved for public HDM material.

Absent one of those two bases, external development/research provenance belongs outside the public HDM repository. Public HDM semantics must be stated independently in HDM terminology and must not depend on named research provenance for their authority.

## 2. Scope

This decision applies to current public HDM content in both:

- `DEV/` — architecture, research/design/specification provenance, tests, tooling and other development material;
- `GAME/` — the exact runtime source tree and therefore all content eligible to enter a runtime package.

It also applies to future public artifacts derived from those trees.

This decision does not require rewriting Git history. It governs current and future public material and release artifacts.

## 3. Required attribution remains preserved

This decision does not remove or weaken legally required or explicitly approved attribution.

Canonical legal/notice owners remain responsible for required public notices and license payloads. Where external material is lawfully incorporated under an attribution-bearing license, the required attribution remains present through the appropriate legal owner rather than through a development-research narrative.

## 4. Technical provenance is a different concern

The following engineering provenance is not development/research provenance and remains required wherever current architecture owns it:

- source commit SHA and release/tag identity;
- `RUNTIME_PACKAGE.yaml` artifact provenance;
- package/archive cryptographic digests;
- semantic engine/version identity;
- schema/ruleset/protocol generation and compatibility identity;
- migration/update lineage and deterministic machine evidence;
- repository/currentness evidence required for safe publication, recovery or verification.

This decision therefore does not weaken release integrity, update safety, migration classification, reproducibility or auditability of HDM-owned artifacts.

## 5. Private research boundary

Lawful exploratory research and source-specific provenance may be retained in the private HDM Lab where useful. Promotion into public HDM requires independent rewriting in HDM terminology and removal of source-specific development/research provenance unless attribution is legally required or separately Product-Owner-approved.

Private material does not become public architecture authority merely because it informed research.

## 6. WP-23 disposition

This decision resolves `WP23-S1-F01`.

WP-23 SHALL treat repository-wide public provenance hygiene as part of its existing Lane C rather than creating a separate workstream. Steps 2–8 must independently identify affected current `DEV/` and `GAME/` surfaces, preserve required/approved attribution, preserve technical artifact provenance, and bring current public architecture/machine checks/routing into one consistent policy.

The Step-1 evidence that originally exposed the runtime-facing issue remains valid historical design provenance; this owner decision broadens the final public policy from the shipped `GAME/` boundary to the full public `DEV/` + `GAME/` repository boundary.

No WP-20 reopen is implied.

## 7. Decision state

```text
WP23-S1-F01: CLOSED BY PRODUCT OWNER DECISION
PUBLIC_DEV_RESEARCH_PROVENANCE: NOT ALLOWED BY DEFAULT
PUBLIC_GAME_RESEARCH_PROVENANCE: NOT ALLOWED BY DEFAULT
LEGAL_REQUIRED_ATTRIBUTION: PRESERVE
EXPLICIT_PO_APPROVED_ATTRIBUTION: PRESERVE
INDEPENDENT_HDM_SEMANTICS: REQUIRED
TECHNICAL_ARTIFACT_PROVENANCE: PRESERVE WHERE OWNED
GIT_HISTORY_REWRITE_REQUIRED: NO
NEW_WORKSTREAM_REQUIRED: NO
WP20_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED_FOR_THIS_BOUNDARY: NO
```

## 8. Version impact

This owner-decision publication is development documentation/architecture policy only.

```text
VERSION_IMPACT: VERIFIED
VERSION_BUMP_REQUIRED: NO
VERSION_IMPACT_DISPOSITION: NONE
```

Later WP-23 realization changes to `GAME/`, release-visible content, machine checks or other version-bearing surfaces must run the normal Version Impact Gate on their own actual delta.
