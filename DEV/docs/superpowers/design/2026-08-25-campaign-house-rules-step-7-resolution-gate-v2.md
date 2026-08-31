# Campaign House Rules — Step 7 Resolution Gate v2

Status: **PASS / ALL STEP-6 SIGNIFICANT FINDINGS RESOLVED / STEP 8 CANONICALIZATION AUTHORIZED**

Date: 2026-08-25

Inputs:

- Step-5 candidate v2;
- Step-6 adversarial review v2;
- current materialized schemas/runtime-facing contracts/tests.

---

## 1. AR2-5 — normative prose admission linkage

**Resolved.**

`GAME/SCHEMA/house_rules_policy.schema.yaml` now requires the semantic invariant:

> every durable normative House Rule/Ruling intended as current campaign policy has exactly one current sidecar entry with a resolvable source anchor; unindexed normative prose is not admitted as durable campaign policy authority.

Duplicate IDs/anchors, unresolved anchors and orphan sidecar entries are malformed policy/integrity defects at the affected boundary.

`GAME/CAMPAIGN/RULES/HOUSE_RULES.md` exposes the same runtime business rule.

This preserves normative Markdown ownership while preventing prose from bypassing identity/adoption/currentness evidence.

---

## 2. AR2-6 — typed realization linkage

**Resolved.**

Ambiguous `capability_refs` was replaced before canonicalization with explicit:

```text
realization_refs: array[string]
```

Meaning:

- explicit declared relation between policy and typed capabilities intended to realize its formalizable portion;
- references remain subject to current catalog/currentness/validation;
- references do not gain execution authority by mention;
- required mechanically material realization absent -> finite `POLICY_REALIZATION_GAP`;
- missing/stale/incompatible refs -> finite mismatch/gap behavior;
- contextual LLM-native policy may have no realization refs indefinitely.

No persisted generic realization-status registry is introduced.

---

## 3. Delegation lifecycle hardening

`PLAYER.policy_authority.mechanical_override_policy` now explicitly records:

- missing/null false for non-creator;
- active PLAYER required;
- creator-only grant/revoke;
- self-grant forbidden;
- grant/revoke is a HARD access-control persistence boundary;
- stale prepared policy write revalidates authorization after relevant movement;
- later revocation is prospective.

Already-published policy is not retroactively invalidated merely because its adopter later becomes inactive or loses delegation.

---

## 4. Creator ownership review

No MANIFEST field was added.

Current creator authority remains inherited Git initialization provenance. Runtime fast-path law already prohibits per-turn history reads; resolved immutable creator identity may be retained as session-local derived authorization evidence.

This explicitly resolves the earlier proposed-but-rejected MANIFEST rewrite.

---

## 5. Notification/currentness review

No notification cursor, queue, worker or global policy frontier was introduced.

Current behavior is:

```text
ordinary required campaign refresh
-> HEAD movement
-> bounded changed-path compare
-> House-Rules paths changed
-> exact pinned current policy acquisition/revalidation
-> new affected work uses new basis
-> concise OOC notice appended to current Master output
```

Repeated notification after context loss is allowed; exactly-once delivery is not a correctness requirement.

---

## 6. Focused verification

TDD sequence for reopened authority/sidecar contract:

1. executable contract test was added before the grant/sidecar existed;
2. RED condition was observed against the current pre-repair shapes (`policy_authority` absent; sidecar absent);
3. minimal grant/sidecar/runtime contract was materialized;
4. Step-6 adversarial requirements were first added to the test, then schema/runtime contracts were tightened;
5. focused structural assertions against the exact current fetched schema shapes are GREEN for:
   - narrow mechanical grant only;
   - no stored interpretive grant;
   - HARD creator-only grant lifecycle;
   - explicit `realization_refs`;
   - no `capability_refs` fallback;
   - no global policy epoch;
   - mandatory sidecar admission for normative policy.

Repository-wide `validate.yml` is now correctly triggered on `v1/*`, but the workflow currently fails earlier in the pre-existing full maintenance audit on unrelated release/readiness inconsistencies. This Resolution Gate therefore does **not** claim full repository CI green.

---

## 7. Gate result

```text
STEP-6 BLOCKER: 0
STEP-6 SIGNIFICANT OPEN: 0
MATERIAL HUMAN DECISION OPEN: 0
HOUSE-RULES MACHINE CONTRACT: MATERIALIZED FOR SETTLED CURRENT SCOPE
STEP 8: AUTHORIZED
S6D: STILL BLOCKED UNTIL STEP 8 COMPLETES
R2.7 WP-06: PAUSED
```
