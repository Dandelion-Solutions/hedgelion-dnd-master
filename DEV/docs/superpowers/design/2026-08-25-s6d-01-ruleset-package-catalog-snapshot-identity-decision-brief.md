# S6D-01 — Ruleset / Package / Catalog Snapshot Identity — Decision Brief

Status: **STEP 3 COMPLETE / NO HUMAN DECISION REQUIRED**

Date: 2026-08-25

## 1. Decision-ready delta

Current HDM identity surfaces are individually valid but collectively insufficient:

- engine version identifies the installed semantic engine contract;
- catalog generation identifies coordinated machine vocabulary;
- runtime package/source metadata proves artifact provenance;
- campaign package digest identifies exact ZIP bytes;
- catalog-context fingerprint identifies an accepted composed context but cannot reconstruct its ruleset packages.

The missing authority is exact package-level reusable-definition identity and dependency closure.

## 2. Recommendation

Adopt **ruleset semantic manifests + exact content-addressed dependency locks + an order-independent resolved ruleset-set digest**, projected only into natural consumers.

```text
ruleset package manifests/content
    -> exact dependency-closed ruleset set
    -> ruleset_set_sha256

engine identity
    + ruleset_set_sha256
    + campaign/session owner-local frontier refs
        -> derived catalog_context_fingerprint
```

Required projections:

- generated runtime package metadata advertises the exact embedded ruleset set;
- campaign creation/current adoption records `ruleset_set_sha256`;
- accepted Resolution/Continuation records the exact set digest plus context fingerprint;
- checkpoint remains optional routing/diagnostic evidence;
- campaign/session definition frontiers remain with their owners.

## 3. Material consequences

1. Engine version, catalog generation, source SHA, ZIP digest, package version, compatibility line, ruleset content digest and context fingerprint remain distinct.
2. A same-engine-version descendant build is a nonsemantic refresh only when its resolved ruleset-set digest is unchanged.
3. A proven forward same-engine-version runtime refresh remains silent when its ruleset set changes compatibly/additively. A non-creator may use it but cannot persist campaign engine/ruleset identity; the creator later refreshes both sibling projections coherently. Incompatible or ambiguous replacement requires explicit creator-authorized adoption/migration.
4. Accepted work retains its exact set identity and is never reinterpreted from ambient newer rules.
5. Exact required snapshots are retained while promised consumers depend on them.
6. No global snapshot record, package manager, online resolver, per-record package versions or implicit package fork is introduced.

## 4. Alternatives disposition

- Engine version + ZIP digest only: rejected because artifact bytes are not reusable-definition identity.
- Universal stored `ResolvedCatalogSnapshot`: rejected as duplicate cross-domain authority.
- Compatibility line without content digest: rejected because it cannot reconstruct or detect incompatible same-line mutation.
- Recommended content-addressed package-set model: only option satisfying existing no-shadowing, recovery, adoption and authority laws.

## 5. Exact human decision

**None.** This is an agent-owned technical consequence of accepted architecture. No unresolved product semantics, authority transfer, hard-to-reverse compatibility choice or material risk acceptance remains.

Proceed to Step 4 review and candidate specification without stopping.


