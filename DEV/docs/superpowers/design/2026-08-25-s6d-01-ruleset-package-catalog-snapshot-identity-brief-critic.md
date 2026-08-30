# S6D-01 — Architecture Task Brief Critic

Status: **CRITIC COMPLETE / BLOCKING AND SIGNIFICANT FINDINGS RESOLVED**

Date: 2026-08-25

Reviewed artifact:

- `DEV/docs/superpowers/design/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-task-brief.md`

Review boundary: Step 1 framing only. No S6D-01 Step 2 research or S6D-02 work was performed.

## 1. Critic mandate

Independently attack the brief under `DEV/DESIGN_PROCESS.md` Step 1 and the HDM architecture adapter. The review was required to cover stale assumptions, embedded solutions, incorrect abstraction boundaries, whole-project consumers, simpler/deletion outcomes, YAGNI, negative cases, Source Manifest auditability and exact stop conditions.

The whole-project dependency pass explicitly considered catalog identity/namespace ownership, engine and runtime-package provenance, release composition, campaign manifest/adoption, Step-3 Resolution/Continuation, Step-5 recovery/checkpoint, cleanup compatibility, House Rules typed realization, later S6D domains, paused R2.7 WP-06 and the future WP-20 boundary.

## 2. Coverage check: twelve domains vs eleven residual obligations

**Result: PASS.** The natural twelve-domain list covers all eleven residual obligations without loss.

- S6D-01 absorbs both exact identity/compatibility and deterministic ruleset/package seed reconstruction.
- S6D-02 and S6D-09 split admitted vocabulary/catalog gaps from proof over the supported mechanics surface.
- S6D-03 through S6D-08 cover selector, accessor/input/dependency, protocol-value, primitive, progression/choice and concrete state/temporal obligations; proven scheduled/invocation extensions are routed across S6D-04/05/08 by their natural owner.
- S6D-11 supplies executable contract closure and S6D-12 supplies the final integrated catalog/schema/seed audit.
- S6D-10 is the later-required integration with the now-canonical House Rules boundary, not a fabricated twelfth historical residual.

The prose list is the requested single execution list. A cross-matrix is unnecessary. The original eleven obligations remain the integrated completion ledger.

## 3. Findings and resolutions

### B-01 — Source Manifest used non-resolvable aggregate labels

Severity: **BLOCKING — RESOLVED**

Affected brief sections: 10 and 12.

Finding: several rows referred only to families such as “Step-3 canonical owners”, “Step-5 canonical specs”, “campaign manifest/schema” or “canonical House Rules owner”. A researcher could choose a stale or incomplete artifact while still claiming the row was inspected. That violated the auditable-source-selection requirement and weakened the mandatory whole-project dependency review.

Resolution: the Source Manifest now names exact current paths for:

- R2.7 status and WP-03/WP-06 evidence;
- Step-1 assurance and retrospective artifacts;
- engine-version, runtime-package-provenance and migration amendments;
- Step-3 canonical execution plus Resolution schemas;
- Step-5.2, Step-5.7 and Step-5.13 canonical owners;
- campaign manifest/schema/init/update surfaces and focused identity tests;
- canonical House Rules prose/sidecar/schema surfaces;
- R2.7 audit decomposition and the future WP-20 boundary.

Patterns remain only for genuinely homogeneous implicated test/schema families and are paired with named high-risk files.

### S-01 — Roadmap would remain contradictory after Step-1 publication

Severity: **SIGNIFICANT — RESOLVED IN PUBLICATION SET**

Affected brief sections: 10 and 12; authoritative status owner.

Finding: before this work the roadmap said `S6D: NEXT / NOT STARTED` and `S6D_ACTIVE_STAGE: NONE`. Publishing a Step-1-complete brief and critic without changing that status would leave two incompatible continuation points.

Resolution: the same publication set updates `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` to record S6D started, S6D-01 Step 1 complete, R2.7 still paused at WP-06, and the exact stop before S6D-01 Step 2. No later S6D domain becomes active.

### M-01 — WP-20 source boundary was too generic

Severity: **MINOR — RESOLVED**

Affected brief sections: 7 and 10.

Finding: the brief named future WP-20 but not the artifacts that currently establish its boundary.

Resolution: the Source Manifest now names the R2.7 audit task briefs and roadmap. It also states that no separate WP-20 architecture owner exists yet, so Step 2 must not invent post-release migration requirements.

## 4. Confirmed non-findings

No additional blocking/significant framing defect remains:

- the problem is bounded separately from S6D-02 and broad runtime implementation;
- package, snapshot, lock and manifest terminology is explicitly hypothetical;
- the brief permits derivation, deletion, splitting or rejection of proposed abstractions;
- engine version, catalog generation, artifact digest, source provenance and semantic compatibility are not collapsed;
- checkpoint/global-snapshot and hot-path remote-resolution traps are explicitly prohibited;
- quality attributes and failure classes distinguish real alternatives;
- whole-project consumers include execution, recovery, release, campaign, House Rules, cleanup, later S6D and R2.7;
- clean-slate pre-release scope and future WP-20 ownership remain separate;
- stop conditions prohibit Step 2 and S6D-02.

## 5. Work explicitly deferred to Step 2

The critic did not require Step 1 to perform research synthesis or decide:

- one ruleset package versus a package set;
- manifest/schema fields, hashes, compatibility relations or validation algorithms;
- House Rules realization/profile shape;
- campaign/session-definition incorporation details;
- exact owner-local storage/projection of context identity;
- implementation, tests, release or campaign changes.

Those are research/design outputs to be investigated only after an explicit continuation into S6D-01 Step 2.

## 6. Critic conclusion

After the recorded corrections, the task brief is fit to govern a bounded S6D-01 Step 2 investigation. The current work must stop after publication and remote verification of the brief, critic and status update.

