# Campaign House Rules — Step 8 Canonicalization v2

Status: **CANONICALIZATION COMPLETE / HOUSE RULES STEPS 1–8 CLOSED / STOP BEFORE S6D**

Date: 2026-08-25

Primary canonical owner:

- `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`

This Step-8 record supersedes the earlier attempted House-Rules closure for gate/status purposes.

---

## 1. Valid repaired derivation chain

```text
Step 1  preserved Task Brief
Step 2  Senior-audit evidence/machine-contract repair
Step 3  amended Decision Brief
Step 3  explicit human owner decision
Step 4  collaborative review v2
Step 5  candidate specification v2
Step 6  adversarial review v2
Step 7  resolution gate v2
Step 8  this canonicalization
```

The earlier Senior Auditor `GO FOR STEP 2–8` is not treated as retrospective approval of decisions. The actual owner decision is recorded explicitly in `2026-08-25-campaign-house-rules-step-3-owner-decision.md`.

---

## 2. Canonical responsibility shape

**A + narrow C.**

Existing owners retain behavior/authority; narrow structured policy identity/currentness/adoption/realization evidence supports them.

No dedicated generic House-Rules runtime owner, universal policy graph, semantic DSL or prose-only/no-linkage architecture is introduced.

---

## 3. Canonical adoption authority

```text
INTERPRETIVE_POLICY
    multiplayer: every current active PLAYER by default
    no stored interpretive grant

MECHANICAL_OVERRIDE_POLICY
    campaign creator by default
    non-creator: current active PLAYER
                 + creator-issued PLAYER.policy_authority.mechanical_override_policy == true
```

Creator remains the existing first campaign-specific initialization-commit author; House Rules does not move creator identity into MANIFEST.

Authority class follows semantic effect rather than the writer's label. Mixed indivisible policy requires stronger mechanical-override authority.

---

## 4. Canonical policy representation

```text
RULES/HOUSE_RULES.md
    normative human/LLM-readable policy

RULES/HOUSE_RULES.yaml
    narrow structured identity/currentness/adoption/routing/realization companion
```

Every durable normative current policy entry is admitted exactly once through a sidecar entry/source anchor. Unindexed normative prose is not durable policy authority.

Exact revision is stable policy ID + exact current campaign revision selecting both files. No policy epoch/frontier is introduced.

`realization_refs` explicitly link formalizable policy portions to intended typed capabilities while leaving catalog/currentness/validation authoritative.

---

## 5. Canonical adjudication/execution boundary

LLM/Master owns fiction-dependent semantic adjudication within eligible information and reviewed typed handoff boundaries.

Deterministic owners retain engine-established facts, legality, RNG, state mutation, accounting and commit authority.

Accepted richer adjudication inputs are typed/provenanced/frozen in existing RuntimeCommand/Resolution/Continuation contracts. Registered invocation context facts remain boolean.

Missing or divergent deterministic realization stops with finite policy-realization gap/mismatch behavior; stale executable mechanics and prose mutation are both forbidden fallbacks.

---

## 6. Canonical multiplayer currentness/notification

No push or background polling subsystem exists.

On ordinary required campaign refresh:

```text
HEAD changed
-> bounded changed-path compare
-> House-Rules paths changed
-> exact current policy acquisition/revalidation
-> new affected work uses refreshed basis
-> concise OOC policy-change notice appended to current Master output
```

No exactly-once notification cursor/ledger is introduced. Accepted historical Resolution generations remain frozen across later policy changes.

---

## 7. Materialized pre-release contracts

Architecture-required clean-slate materialization now includes:

- richer adjudicated Activity parameter binding schemas/tests from Step-2 repair;
- `GAME/SCHEMA/player.schema.yaml` narrow mechanical-override grant;
- `GAME/SCHEMA/house_rules_policy.schema.yaml`;
- `GAME/CAMPAIGN/RULES/HOUSE_RULES.yaml`;
- `GAME/CAMPAIGN/RULES/HOUSE_RULES.md` runtime-facing contract;
- `GAME/CORE/ADJUDICATION.md` live-ruling/adoption/frozen-input semantics;
- `DEV/ARCHITECTURE/ACCESS_CONTROL.md` policy-adoption authority;
- focused House-Rules authority/adjudication tests.

MANIFEST creator representation was explicitly reviewed and intentionally left unchanged.

---

## 8. Verification disposition

Focused House-Rules structural assertions are GREEN after Step-7 resolutions.

`.github/workflows/validate.yml` now correctly triggers for `feature/**` and version branches `v*/*`, including `v1/engine-rearchitecture`. The current full maintenance audit still has pre-existing unrelated release/readiness failures, so this record does not claim repository-wide CI green.

Step-6 final state after Step-7 resolution:

```text
BLOCKER: 0
SIGNIFICANT OPEN: 0
HUMAN DECISION OPEN: 0
```

---

## 9. Program transition

```text
HOUSE_RULES: COMPLETE / CANONICAL
S6D: NEXT / NOT STARTED
S6D_ACTIVE_STAGE: NONE
R2.7 WP-06: PAUSED
```

**STOP HERE.** This canonicalization does not start S6D. S6D begins only on explicit subsequent owner continuation and starts its first domain at Step 1 — Architecture Task Brief.
