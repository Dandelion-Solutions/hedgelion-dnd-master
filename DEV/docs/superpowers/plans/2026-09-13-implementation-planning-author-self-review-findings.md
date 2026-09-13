# HDM Implementation Planning — Author Adversarial Self-Review Findings

Status: **AUTHOR SELF-REVIEW FINDINGS — REPAIR REQUIRED BEFORE INDEPENDENT RE-REVIEW #2**
Date: 2026-09-13
Review baseline: `026afe07020bc00da79c0099716f5cfe823d7141`
Production implementation authorized: **NO**.

## 1. Purpose and method

The previous independent Senior re-review found SIRR-001..SIRR-005. The first author repair addressed those findings, but before spending another independent-review cycle this author pass re-ran the adversarial checks against current canonical owners instead of trusting the prior author closure.

This self-review is not an independent gate and cannot produce implementation GO. It exists to find author defects before the next genuinely independent Senior review.

Evidence was staged and bounded:
- fresh branch/current-progress/process bootstrap;
- complete previous independent re-review result;
- current re-review #2 brief;
- exact WP-11, WP-12, WP-13, WP-18, WP-19 and versioning owner clauses implicated by the repaired findings;
- current routed plans/overlays and exact shipped consumers implicated by those clauses;
- reverse consumer check from each repaired owner contract into schema/template/bootstrap/proof surfaces.

No production implementation was performed.

## 2. Accounting/currentness

Canonical package accounting remains unchanged:

```text
DIRECT: 116
PURE_PROOF: 9
COMPOSITE_PARENTS: 8
ACTIVE: 133
TRIGGER_GATED: 12
NO_WORK: 79
R004: ABSENT
RD_UNITS: 14
```

The fresh baseline contains only planning/control work since the independently reviewed owner state. No canonical owner/spec/decomposition drift was found that requires architecture reopening.

## 3. Findings

### ASR-001 — SIGNIFICANT — SIRR-004 repair stops before the complete WP-11 fixed-root contract

**Problem.** The first SIRR repair made `GAME/CAMPAIGN/MANIFEST.yaml -> storage.story_root` an RD-13 action, but reverse checking WP-11 R064 shows that the durable route contract is broader and owned by the WP-11 realization route. The current machine contract still has only five selectors:

```text
state_root
index_root
world_root
event_log_root
checkpoints_root
```

WP-11 requires the fixed selector set:

```text
state_root
index_root
world_root
event_log_root
checkpoints_root
sessions_root
story_root
```

Current evidence:
- `GAME/CAMPAIGN/SESSIONS/` already exists, but `MANIFEST.storage.sessions_root` is absent;
- `GAME/CAMPAIGN/STORY/` is planned by RD-13, but `story_root` is absent;
- `GAME/SCHEMA/campaign_manifest.schema.yaml` schema version 4 admits only the five old selectors;
- the prior repair did not name that schema at all;
- `GAME/CORE/STORAGE.md` says MANIFEST routes only STATE/INDEX/WORLD/LOG/CHECKPOINTS;
- `GAME/CORE/BOOTSTRAP_RUNTIME.md`, `GAME/CORE/CAMPAIGN_SETUP.md` and `GAME/INSTALL/00_DND_BOOTSTRAP.md` expose the same incomplete generated-root view;
- `CAMPAIGN_SETUP.md` also still says "manifest schema v3" while the current machine schema is v4 even before the required selector cutover.

**Why significant.** A worker following the current package can create a template with `story_root` that its own shipped manifest schema does not admit, while leaving another mandatory fixed selector (`sessions_root`) missing. That is not worker-ready and leaves R064/R018 root integration partially realized.

**Repair direction.** Route the selector shape through RD-04/WP-11, keep Story semantics/root contents in RD-13, then make RD-14 consume the coherent generated shape. Perform one coherent pre-release manifest local-schema cutover rather than two partial incompatible edits.

### ASR-002 — SIGNIFICANT — retained Dramaturg repair illegally narrows player-local `shared_basis`

**Problem.** The SIRR repair/addendum says a player-local retained horizon "additionally requires exact BOUND shared generation". WP-18 explicitly permits:

```text
shared_basis.kind = ABSENT | BOUND
```

For `BOUND`, exact `shared_generation` is required. For `ABSENT`, a shared generation must not be invented merely to satisfy the player-local record.

**Why significant.** The repair accidentally converts an owner-admitted state into an impossible state and would force a dependency on a shared horizon where the canonical owner permits no such dependency. That changes accepted semantics rather than merely specifying implementation.

**Repair direction.** Player-local candidate/publication/admission must preserve the declared basis exactly: `BOUND` validates exact accepted shared generation; `ABSENT` carries no fabricated generation. A native dependency change that changes ABSENT<->BOUND requires rebuild/new accepted generation, not mutation of an old retained generation.

### ASR-003 — SIGNIFICANT — lossless proof routes still contain owner/target imprecision

The v2 WP-12/WP-13 proof rows are now semantically close to the canonical duties, but three route descriptions remain insufficiently precise for an executable lossless proof package:

1. WP-12 duty 5 names only RD-04 + RD-09 even though the canonical duty includes the local accepted execution/ExecutionSegment establishment edge as well as LIVE exact-source CAS. RD-05 must participate in the supporting route.
2. WP-12 duty 11 freezes principal/authorization plus exact generation, but its supporting route omits RD-09 principal/authorization evidence.
3. WP-13 duties 19/20 call the fixed gameplay Git transport a generic `process transport/process negative law`. WP-13 explicitly separates gameplay runtime transport semantics from development-agent transport policy. The proof route must name the admitted R2.6/WP-13 gameplay publication transport; process rules may be supporting discipline only.

The shipped-consumer table also marks `STORAGE.md` and `INSTALL/00_DND_BOOTSTRAP.md` as current-conforming even though ASR-001 proves root-topology consumer drift.

**Why significant.** SIRR-001 was specifically about semantic one-to-one proof binding. Leaving supporting owner routes ambiguous risks another false PASS from a test attached to the wrong authority.

**Repair direction.** Correct the supporting routes and consumer dispositions in the current v2 appendix without changing readiness identities or proof channels.

## 4. Non-findings / checked boundaries

The self-review found no new architecture or Product Owner decision requirement in these areas:
- SIRR-003 SAVE/PERSISTENCE native-domain composition and tri-state publication direction remains owner-consistent;
- SIRR-005 two-phase LIVE `ACTIVE -> CLOSED` then absorption/handoff remains correct; failure after successful close leaves `CLOSED_UNABSORBED` selected truth with zero ordinary writers;
- retained Dramaturg still uses ordinary RD-06 campaign publication rather than a new publisher;
- Story remains noncanonical and MANIFEST root selectors carry topology only, never Story progress/currentness;
- v1 clean-slate policy permits replacement of pre-release machine shapes without compatibility shims for old pre-release data;
- no new RD unit/readiness identity or whole-wave barrier is needed.

## 5. Required repair and gate

Before independent re-review #2:
1. repair ASR-001..ASR-003 in current planning routes;
2. publish the repair as a planning-only checkpoint;
3. fresh-read the exact checkpoint and compare its delta;
4. run hosted validation on the exact checkpoint;
5. perform a second author adversarial pass against the repaired package and the current re-review #2 brief;
6. only if that second pass has no unresolved BLOCKING/SIGNIFICANT/MINOR author finding, publish author self-review closure and hand off to the independent reviewer.

Until that closure:

```text
AUTHOR_SELF_REVIEW_VERDICT: FAIL / REPAIR REQUIRED
INDEPENDENT_RE_REVIEW_2_READY: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
