# R2.7 WP-19 — Step 6 Whole-Project Adversarial Review

Status: **STEP 6 COMPLETE — MATERIAL FINDINGS IDENTIFIED FOR STEP 7**

Date: 2026-09-05

Candidate reviewed:
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-candidate-specification.md`.

Independent review basis:
- `DEV/PROJECT_MAP.md` concern routes;
- current WP-19 Source Manifest + Step-2 refinement;
- actual upstream owners for storage/runtime identity, publication, readiness, Actor/knowledge/context, durability, chronology, access/live, Story;
- `GAME/` bootstrap/setup/runtime/persistence/session/live consumers;
- campaign/event/storage schemas;
- release builder/materializer machine contracts;
- executable and scenario test consumers;
- Product Owner ledger/accepted decisions, including PO-003 latency amendment.

This critic does not reopen previously closed Step-1 findings merely because some realization debt overlaps them.

## 1. Whole-project reconstruction result

The candidate's composition boundary is sound: no current owner is duplicated, and no evidence requires a new bootstrap/session/history/psychology owner. The attack therefore focused on whether the rest of the repository would implement or verify the candidate incorrectly.

Critical dependency routes checked:

```text
storage v3 baseline
 -> exact RUNTIME_PACKAGE / ruleset_set_sha256
 -> init_campaign
 -> MANIFEST engine/ruleset identity
 -> first from-scratch publication
 -> initializing/provisional/READY_PC/PLAY_READY
 -> active/access/live/persistence

ordinary Master retrospective / read-only Commentator
 -> R2.3 bounded historical context
 -> Story orientation
 -> exact/native/SemanticEvent evidence
 -> disclosure/no-spoiler

material Actor decision
 -> R2.2 + world.knowledge + admitted decision context
 -> bounded T0 basis
 -> SemanticEvent history
 -> ordinary durability/index discovery
 -> later eligible retrospective

save-and-exit
 -> existing save/live durability
 -> session-local selected-gameplay clear
 -> same-chat campaign menu
 -> no durable membership/lifecycle/control side effect
```

## 2. Findings summary

```text
STEP6_BLOCKING:    0
STEP6_SIGNIFICANT: 7
STEP6_MINOR:       1
```

All seven SIGNIFICANT findings are mechanically resolvable without a new Product Owner decision or upstream architecture reopen. Their Step-7 dispositions are recorded separately.

## 3. Findings

### F19-S6-01 — SIGNIFICANT — exact ruleset-set identity is not propagated by current runtime creation prose

**Mechanism**

`release_builder.py`/RUNTIME_PACKAGE and `init_campaign.py` require exact `ruleset_set_sha256`, but current `00_DND_BOOTSTRAP.md`, `BOOTSTRAP_RUNTIME.md` and `CAMPAIGN_SETUP.md` generator-argument prose omits it. A literal runtime implementation following those surfaces can fail generator invocation or lose the exact ruleset creation identity required by MANIFEST.

**Candidate assessment**

`WP19-L04/L06` correctly defines the architecture chain. This is machine/runtime realization drift, not an owner insufficiency.

**Required disposition**

Final canonical spec must retain exact identity law and downstream realization must align all generator-call consumers and direct tests. Do not edit `GAME/` in this architecture assignment.

### F19-S6-02 — SIGNIFICANT — `DEV/ARCHITECTURE/BRANCH_MODEL.md` is a stale current projection

**Mechanism**

It still presents Storage v2 `baseline_version`, version-only storage baseline, and tag-derived campaign provenance/update wording. Current owners use Storage v3 portable exact baseline identity and RUNTIME_PACKAGE provenance.

Because `PROJECT_MAP.md` still routes access/repository work through `BRANCH_MODEL.md`, leaving it unchanged would make a current navigation path materially misleading.

**Required disposition**

Repair this current derivative architecture projection in Step 7 while preserving valid branch/root/creator/access/concurrency laws. No upstream reopen.

### F19-S6-03 — SIGNIFICANT — hard `pre-live/true-live` vocabulary survives in runtime/schema/test consumers

**Mechanism**

`CAMPAIGN_SETUP.md`, `NEW_CAMPAIGN_FAST_PATH.md`, campaign-manifest schema wording and several readiness/onboarding scenarios still use `pre-live`, `first true live scene` or equivalent wording. The accepted progressive READY_PC owner allows real locally-sufficient provisional play while lifecycle remains `initializing`; therefore those labels can incorrectly create a forbidden hard gameplay phase boundary.

**Candidate assessment**

`WP19-L12-L17` is correct and must be the implementation-facing law.

**Required disposition**

Classify affected runtime/schema/test wording as downstream realization debt. Do not create a new lifecycle state or rewrite historical test provenance during architecture canonicalization.

### F19-S6-04 — SIGNIFICANT — ordinary active-player retrospective has no direct runtime/acceptance realization

**Mechanism**

PO-001 product semantics and the candidate specify ordinary Master retrospective behavior, but current runtime/test surfaces prove only components such as bounded retrieval/knowledge leakage. There is no end-to-end contract proving an authorized active player asks a historical question and remains in ordinary gameplay under current disclosure rules.

**Required disposition**

Retain `WP19-L20-L23` canonically and route exact runtime instruction placement plus direct acceptance coverage downstream.

### F19-S6-05 — SIGNIFICANT — save-and-exit-to-selection has no direct runtime/session composition

**Mechanism**

Current save tests distinguish save from pause and true save-and-stop, and membership tests distinguish leave/removal, but no current runtime/acceptance path proves:

```text
save success
 -> selected-gameplay session state cleared
 -> same-chat campaign menu
 -> lifecycle/membership/control/live semantics preserved
```

Without an exact session-local clear/preserve contract, implementation may either remain accidentally bound to the old campaign or over-clear durable multiplayer authority.

**Candidate assessment**

`WP19-L24-L28` supplies the required semantic contract.

**Required disposition**

Preserve those laws in final spec and route runtime/session/menu + direct acceptance realization downstream.

### F19-S6-06 — SIGNIFICANT — PO-003 semantic owner exists but current machine schema/discovery does not prove the contract

**Mechanism**

`event.schema.yaml` is append-only causal history but does not normalize the logical basis-item obligations from `WP19-L32-L33`. Current history/index surfaces also do not directly prove bounded lookup of a material Actor decision basis without broad history scanning.

Two opposite implementation errors remain possible:
- add an unnecessary new psychology/history authority;
- stuff opaque free-form rationale or mutable current-record refs into generic event fields.

**Candidate assessment**

Existing SemanticEvent owner/family remains sufficient; no reopen. Physical layout/index projection is legitimately deferred.

**Required disposition**

Final spec must keep the logical basis-item/admission/retrieval contract precise while deferring only representation. Later realization must add the minimum schema/validator/index support needed under existing owners.

### F19-S6-07 — SIGNIFICANT — PO-003 latency law lacks direct realization verification

**Mechanism**

Current performance/context/persistence tests support locality and batching but do not prove that decision-basis capture adds:

```text
0 dedicated sequential LLM calls
0 redundant serial reads when data already bound
0 separate publications
0 irrelevant-turn work
```

A functionally correct implementation could therefore violate the Product Owner's interactivity constraint while all existing component tests pass.

**Required disposition**

Retain `WP19-L38-L39` as a normative architecture law and add direct performance acceptance/evaluation downstream. Any future need for extra serial critical-path work must trigger architecture/performance re-evaluation rather than silent implementation.

### F19-S6-08 — MINOR — stale scenario expectations remain discoverable

**Mechanism**

Examples include Storage-v2/tag-provenance/staged-setup/manifest-only-discovery expectations (`B12/B22/B23/T13`) and stale phase vocabulary in other scenario files.

**Disposition direction**

Keep their Step-1/SR19-01 applicability classifications explicit. Test files are verification consumers, not architecture owners. Later realization should repair/delete/update stale expectations as appropriate; no architecture block.

## 4. Product Owner / reopen attack

No finding establishes:
- a contradictory Product Owner requirement;
- a new unresolved product quality trade-off;
- semantic insufficiency of R2.2, Step-4 SemanticEvent, WP-10, WP-13, WP-15, WP-16 or WP-18;
- need for a new history/current-state owner;
- need to accept extra serial gameplay work.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
```

## 5. Step-7 entry state

```text
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 7
```

Proceed to mandatory finding resolution and propagation sweep.