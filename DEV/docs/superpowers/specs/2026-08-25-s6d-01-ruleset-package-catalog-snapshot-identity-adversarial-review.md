# S6D-01 — Ruleset / Package / Catalog Snapshot Identity — Adversarial Review

Status: **STEP 6 COMPLETE / FINDINGS ISSUED**

Date: 2026-08-25

Reviewed candidate:

- `DEV/docs/superpowers/specs/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-candidate-spec.md`

## 1. Attack surface

The review attacked requirement fit, duplicate owners, identity-axis collapse, digest ambiguity, dependency/namespace closure, campaign authority, accepted execution, recovery/checkpoint, cleanup retention, House Rules, same-version refresh, YAGNI, failure routing and downstream S6D ownership.

## 2. Findings

### AR-01 — Ruleset projection was incorrectly nested under engine identity

Severity: **BLOCKING**

Original candidate: campaign `engine.created_with/current` would gain `ruleset_set_sha256`.

Attack: independently selected ruleset semantics would become structurally subordinate to the engine projection. That would make future ruleset-only adoption awkward, obscure separate authority axes and tempt consumers to infer ruleset identity from engine identity.

Required resolution: use sibling campaign `ruleset.created_with/current` projections. Engine and ruleset may update coherently but neither owns the other.

### AR-02 — Digest serialization was not reproducible enough

Severity: **SIGNIFICANT**

Original candidate: “domain-separated canonical sequence” did not fix serialization, whitespace, case or domain separator.

Attack: two correct implementations could compute different identities for identical content, defeating reconstruction.

Required resolution: specify canonical UTF-8 JSON, exact domain separator, normalized paths, lower-case hex and excluded metadata.

### AR-03 — `content_roots` could hide traversal/enumeration ambiguity

Severity: **SIGNIFICANT**

Attack: root expansion rules, ignored files, symlinks and future files could change snapshot membership implicitly. A package manifest must identify its semantic file set deterministically.

Required resolution: baseline contract uses explicit normalized `content_files[]`. A future deterministic generated inventory may replace it only through an explicit schema version.

### AR-04 — Failure names risked premature catalog admission

Severity: **SIGNIFICANT**

Attack: S6D-01 must define finite failure distinctions, but exact `failure.*` registry membership belongs to later catalog/machine closure. Treating names as already registered would trespass into S6D-02.

Required resolution: classify the names as semantic distinctions; S6D-02/S6D-11 may admit exact IDs or map them through an existing typed envelope without loss.

### AR-05 — Exact ruleset lock could become a universal context snapshot

Severity: **CHALLENGE / NOT A DEFECT AFTER REVIEW**

Attack: ruleset set might absorb campaign/session definitions and operational frontiers.

Disposition: candidate laws explicitly keep campaign/session frontiers owner-local and make `catalog_context_fingerprint` derived. No change required.

### AR-06 — Exact pinning might overconstrain compatible maintenance

Severity: **CHALLENGE / ACCEPTED CONSERVATIVE BOUNDARY**

Attack: the candidate incorrectly converted a compatible/additive ruleset-set change inside a proven forward same-version runtime into creator-gated adoption, contradicting the established silent-refresh contract.

Disposition: corrected. The runtime may be used immediately without a player prompt; a non-creator cannot persist campaign engine/ruleset identity; the creator refreshes both sibling projections coherently at the next valid persistence boundary. Accepted work keeps exact meaning. Incompatible or ambiguous replacements still require explicit creator-authorized adoption/migration.

### AR-07 — Package-set retention could imply global refcount/GC

Severity: **CHALLENGE / NOT A DEFECT AFTER REVIEW**

Disposition: candidate routes protection through Step-5.13 typed owner dependencies and explicitly rejects universal refcount/frontier. No change required.

### AR-08 — House Rules might force profile packages

Severity: **CHALLENGE / NOT A CURRENT REQUIREMENT**

Disposition: canonical House Rules already supports typed realization refs without same-ID replacement. Candidate correctly refuses to invent a profile/fork. Revisit only if a proven reusable replacement mechanic requires it.

## 3. Whole-project scenario attacks

| Scenario | Required outcome | Candidate result |
|---|---|---|
| same engine/source descendant, identical ruleset set | silent maintenance allowed | PASS |
| same engine/source descendant, compatible/additive changed ruleset set | silent use; creator-only identity persistence | PASS |
| same ZIP content claim but rules file tampered | content/lock validation fails | PASS after AR-02/03 correction |
| packages discovered in different order | same set digest | PASS after serialization correction |
| dependency cycle or namespace collision | finite load failure | PASS |
| campaign adopts new set while Continuation is open | new work uses current; old execution retains exact set | PASS |
| old exact set unavailable on recovery | finite prerequisite failure, no ambient reinterpretation | PASS |
| stale checkpoint names old/new context | native campaign/execution owners win | PASS |
| House Rules realization ref missing in current set | finite policy realization gap | PASS |
| campaign/session definition changes | owner-local refs change context fingerprint; ruleset lock unchanged | PASS |
| cleanup wants to retire old rules snapshot | protected accepted consumer blocks retirement | PASS |
| source SHA/tag moves while package bytes fixed | provenance changes do not redefine content identity | PASS |

## 4. Review conclusion

No new owner decision is required. Resolve AR-01 through AR-04, recheck the candidate, then proceed to Step 7.


