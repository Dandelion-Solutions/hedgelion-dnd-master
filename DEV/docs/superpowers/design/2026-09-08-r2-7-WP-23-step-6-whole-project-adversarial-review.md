# R2.7 WP-23 — Step 6 Whole-Project Adversarial Review

Status: **STEP 6 COMPLETE — MATERIAL FINDINGS IDENTIFIED / STEP 7 RESOLUTION REQUIRED**

Date: 2026-09-08

Reviewed candidate:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-step-5-candidate-specification.md`.

The critic rebuilt the direct and indirect WP-23 dependency subgraph from the current exact `DEV/PROJECT_MAP.md` rather than trusting the Step-1/Step-2 manifests as closed inventories. It inspected current semantic owners, Product Owner policy, release/build/install/update consumers, maintenance/verification surfaces, current public research/design/history artifacts and current routing/index consequences.

Search results from another ref/default branch were used only as locators; findings below are based on exact current-branch confirmation.

---

## 1. Whole-project dependency reconstruction

The critic rechecked at least these responsibility families:

```text
process/current progress
-> Product Owner public-provenance owner
-> repository ownership geometry
-> DEV/GAME release identity
-> release builder + launcher
-> release workflow + source CI
-> install/bootstrap/runtime-root consumers
-> WP-20 update/migration consumer
-> root/runtime legal payload
-> GAME source/rules routing
-> DEV architecture owners and historical derivations
-> DEV research evidence
-> DEV tests / historical audits
-> maintenance audit
-> PROJECT_MAP live routing
-> release/version/install verification
```

The review therefore tests the candidate as a whole-project release consumer, not as a local `DEV/RELEASE`/builder specification.

---

## 2. Findings

### SR23-06-01 — SIGNIFICANT — Step-2/5 public-provenance inventory omitted a current historical test/audit surface

**Exact current evidence:** `DEV/TESTS/PRE_RELEASE_AUDIT_0.1.0.md` remains in the current public tree and contains a dedicated `Research integration` section that records which external development sources/prior art informed GM-craft/LLM architecture.

**Why material:** the Product Owner decision explicitly applies repository-wide to current public `DEV/` + `GAME/`; historical/test placement is no exemption. Leaving this file unchanged would make a Step-8 repository-wide reconciliation claim false.

**Required Step-7 resolution:** sanitize the historical audit so its HDM regression/audit history and technical release history may remain, while source-specific research-integration narrative is removed. Propagate the inventory correction into the Step-2 evidence artifact and Step-5 candidate.

---

### SR23-06-02 — SIGNIFICANT — retirement of platform research would leave current project routing underspecified

**Exact current evidence:** `DEV/PROJECT_MAP.md` routes host/platform feasibility / LLM orchestration to durable feasibility/validation research under `research/`. Step 2 proposes retirement of multiple source-history platform/economic research documents whose accepted conclusions are now represented by current R2.6/roadmap owners.

**Why material:** current live routing must not lead future workers toward a retired source-history family as though it remained the default evidence owner. The map is non-normative but is the mandatory discovery route for deep work.

**Required Step-7 resolution:** update the concern route so current host/platform architecture starts from accepted R2.6/roadmap owners and only retained source-neutral/internal feasibility evidence is consulted for applicability/revalidation. Do not make the map a semantic owner.

---

### SR23-06-03 — SIGNIFICANT — mixed transport/topology evidence needs item-specific preservation disposition before sanitation

**Exact current evidence:**

- `DEV/docs/superpowers/research/2026-08-20-step-6-repository-port-transport-feasibility-spike.md` mixes private-workspace/development-source provenance and external platform/API research with durable HDM transport/currentness experiment conclusions;
- `DEV/docs/superpowers/research/2026-08-22-infrastructure-topology-options.md` is largely HDM-native topology reasoning but live-routes platform-specific evidence to a source-history comparative-research file.

The later canonical `2026-09-06-hdm-publication-currentness-supported-ref-repair-amendment.md` now owns the current supported publication/currentness conclusion previously supported by the transport spike.

**Why material:** candidate law correctly says “preserve conclusions before removal” but does not record the concrete owner/rehome result. Blind retirement of both mixed artifacts could lose topology alternatives/revisit triggers; retaining both unchanged violates the PO boundary.

**Required Step-7 resolution:** retire the transport spike from current public tree because its current publication/currentness law is already owned canonically; preserve current technical law through the canonical amendment. Retain the topology-options artifact but remove the live dependency on source-history comparative research and keep its independently stated HDM constraints/options/revisit triggers.

---

### SR23-06-04 — SIGNIFICANT — public-provenance verification is not yet realized and current maintenance audit enforces the opposite policy

**Exact current evidence:** `DEV/TOOLS/audit_engine.py` requires source-specific development-reference markers in shipped `GAME/CORE/SOURCES.md` as part of the GM-guidance audit.

**Why material:** after sanitation, leaving the check unchanged either breaks CI or forces prohibited provenance back into the shipped runtime. Candidate L30 is directionally correct but insufficient until the current machine consumer is reconciled.

**Required Step-7 resolution:**

1. preserve existing behavior/GM-craft checks on HDM-native runtime semantics;
2. remove exact source-history requirements;
3. add bounded current-tree regression guards for the known public-provenance surfaces/retired source-history artifacts;
4. explicitly protect legal/approved attribution and HDM technical provenance from false-positive sanitation;
5. do not claim the bounded guard is a universal semantic classifier.

---

### SR23-06-05 — SIGNIFICANT — candidate realization inventory must include all exact-head confirmed architecture/history surfaces

**Exact current evidence:** source-history sections are confirmed in current:

- `GAME/CORE/SOURCES.md`;
- `DEV/ARCHITECTURE/ASSET_MODEL.md`;
- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`;
- `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md`;
- `DEV/ARCHITECTURE/CRITICAL_ARCHITECTURE_AUDIT.md`;
- `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md`;
- `DEV/TESTS/PRE_RELEASE_AUDIT_0.1.0.md`.

Current `CATALOG_INVENTORY.md` was exact-head checked and does not retain the stale default-branch prior-art section shown by search, so it is not a current finding.

**Why material:** Step-8 repository-wide reconciliation must be based on exact-current artifacts, not a mixture of stale search hits and incomplete known-file lists.

**Required Step-7 resolution:** sanitize the confirmed current set item-by-item, explicitly preserve HDM semantics/negative requirements, and record exact dispositions. Do not mechanically modify stale/default-branch-only hits.

---

### SR23-06-06 — MINOR — Version Impact disposition must be derived after actual sanitation/check realization

**Issue:** the candidate correctly warns against automatic bumping, but final classification cannot be asserted until the actual current-tree delta is known.

**Required Step-7/8 resolution:** after sanitation/check/routing changes, run the Version Impact Gate against actual changed artifacts. A shipped documentation/routing file change alone does not require a version bump if no gameplay/runtime semantic contract, version-bearing CORE behavior, schema/generation, compatibility law or engine release identity changes.

---

### SR23-06-07 — MINOR — historical external implementation preference must be explicitly neutralized

**Exact current evidence:** `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` names an external dice implementation candidate and contains a prior-art adoption table.

**Why material:** the file is noncanonical, but current-tree retention could mislead later implementation planning after the new public-provenance policy.

**Required Step-7 resolution:** rewrite the proposal to retain only the HDM-owned DiceEngine requirements/constraints and defer concrete component selection to future authorized implementation planning.

---

## 3. Adversarial false-closure tests

| False closure | Verdict |
|---|---|
| `GAME/CORE/SOURCES.md` sanitized, therefore repository-wide provenance is reconciled | REJECTED — DEV architecture/research/test surfaces also exist |
| delete every file under `research/` | REJECTED — path is not semantic classification; internal/source-neutral evidence remains valid |
| remove every external name/URL | REJECTED — would destroy operational/legal/current dependency facts |
| keep historical files unchanged because Git history exists | REJECTED — policy applies to current tree; Git history merely removes need for history rewrite |
| delete mixed topology/transport research wholesale | REJECTED — preserve/rehome unique HDM conclusions/triggers first |
| source CI success proves Release asset acceptance | REJECTED |
| reproducible ZIP proves GitHub Release publication | REJECTED |
| future released-v1.0+ migration realization absent, therefore prerelease defect | REJECTED |
| WP-20 thematic overlap requires reopen | REJECTED |
| maintenance audit is semantic provenance authority | REJECTED — it is bounded verification consumer |

---

## 4. Severity summary

```text
STEP6_BLOCKING_FOUND: 0
STEP6_SIGNIFICANT_FOUND: 5
STEP6_MINOR_FOUND: 2

NEW_HUMAN_DECISION_REQUIRED: NO
WP20_REOPEN_REQUIRED: NO
NEW_WORKSTREAM_REQUIRED: NO
```

All SIGNIFICANT findings are mechanically resolvable under the already accepted Product Owner policy and current architecture ownership.

---

## 5. Mandatory propagation targets

Because Step 6 changed the concrete current-tree coverage required for the final law, Step 7 must propagate material corrections at least to:

- Step-2 evidence reconciliation — add historical test/audit surface and exact item dispositions;
- Step-5 candidate specification — add exact current-tree realization inventory/routing requirements;
- affected current owners/routing/check surfaces changed by sanitation;
- final canonical WP-23 specification and Step-8 checkpoint.

The Step-6 artifact itself is the finding evidence; downstream artifacts must be self-identifying where their previous coverage wording would otherwise be misleading.

---

## 6. Step-6 gate

```text
CANDIDATE_WHOLE_PROJECT_REVIEW: HOLD FOR STEP-7 REPAIRS
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 5
UNRESOLVED_MINOR: 2
HUMAN_DECISION_REQUIRED: NO
NEXT_PROCESS_UNIT: STEP 7 FINDING RESOLUTION + PROPAGATION + CURRENT-TREE RECONCILIATION
```
