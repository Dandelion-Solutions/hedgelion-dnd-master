# R2.7 WP-13 — Durability / SAVE / Publication — Step 6 Whole-Project Adversarial Review

Status: **STEP 6 COMPLETE — BLOCKING/SIGNIFICANT FINDINGS REQUIRE STEP 7 RESOLUTION**

Date: 2026-09-02

Reviewed candidate:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-step-5-candidate-spec.md`

Evidence/authority basis:

- repaired Step-1 package + `SR13-01`;
- Step-2 evidence + Source Manifest expansion;
- Step-3 Decision Brief;
- Step-4 collaborative review;
- current accepted R2.6 fixed gameplay transport authority;
- Step 3 / Step 5.1–5.14 owners;
- WP-11 / WP-12;
- current Access Control / onboarding / readiness / multiplayer / House Rules / engine-update consumers;
- current PERSISTENCE / SAVE / DURABILITY / STORAGE machine contracts and principal regressions.

This is the mandatory whole-project critic. It attacks the candidate as an integrated system, not as an isolated persistence module.

---

## 1. Attack model

The review challenged at least these routes:

1. clean explicit SAVE from a stale local campaign basis;
2. clean domain A while domain B is dirty;
3. domain A confirms, domain B confirms later, then A moves before acknowledgement;
4. domain A confirms and B rejects;
5. domain A confirms and B is indeterminate;
6. campaign create-tree succeeds but final ref result is lost;
7. final ref rejection is stale conflict versus branch-rule/authorization/infrastructure rejection;
8. branch moves disjointly after freeze;
9. branch moves over read-only but semantically relevant dependency;
10. G publishes while G+1 is created locally;
11. derived index DELETE/update races native record publication;
12. current campaign publication succeeds but local adoption crashes;
13. required Connector capability is absent before dispatch;
14. Connector ref operation is dispatched but response is unknown;
15. technical repository credential exists but trustworthy HDM acting-principal evidence is absent;
16. PLAYER binding/policy authority changes between preparation/rebuild attempts;
17. risk-control exposure threshold fires and publication fails while coherent local HOT survives;
18. named HARD edge publication fails;
19. explicit SAVE fails while no independent HARD edge exists;
20. save quiescence is established then prepublication failure occurs;
21. save quiescence is established then final ref outcome remains indeterminate;
22. live exact-source CAS participates in a composed SAVE;
23. live CAS succeeds but campaign portion later fails;
24. checkpoint is absent from a valid SAVE;
25. storage baseline update and campaign adoption have independent outcomes;
26. engine/rules campaign maintenance consumes publication under creator authority;
27. prepared commit remains unreachable after race;
28. Git commit order conflicts with fictional simultaneity;
29. current stale one-hour runtime policy is mechanically reused as a HARD barrier under a new field name;
30. broad completeness code attempts to enumerate all campaign records.

The candidate survives most attacks. Six findings remain.

---

# 2. Findings

## F01 — Overall SAVE success lacks an explicit final compatible-current-source proof at acknowledgement

Severity: **BLOCKING**

### Attack

A composed SAVE requires domains A and B.

```text
A -> CONFIRMED durable at source A1
B -> later CONFIRMED durable at source B1
external writer moves A -> A2 before overall `saved` acknowledgement
```

The candidate says every domain must prove compatible durable closure and requires revalidation before dependent continuation after **partial failure**, but it does not state strongly enough that overall success is a single current compatibility assertion at the acknowledgement boundary over the exact selected native source composition.

Independent historical success of A1 and B1 is insufficient if current owner routing/currentness now selects a materially incompatible A2.

### Authority violated if left ambiguous

- Step 5.2 domain-native compatible RRC;
- Step 5.5 laws 10, 12, 15;
- Step 5.7 current-authority-first / exact-pin composition;
- Step 5.8 live/current-source ownership.

### Required Step-7 repair

Before SAVE/HARD success acknowledgement, prove one **current compatible source composition** for the promised closure using domain-native currentness rules. Previously confirmed native publication remains real lineage/durability evidence, but success depends on current compatible authorities at the success boundary.

This proof is bounded to participating sources/dependencies and creates no global snapshot/frontier.

---

## F02 — Domain `NO_WRITE_NEEDED` can be misread as reusable stale proof

Severity: **BLOCKING**

### Attack

Local bookkeeping says campaign portion is clean at cached H. External current campaign authority advances to N and changes a save-relevant dependency/authorization/routing fact. Player now says SAVE.

Candidate WP13-11/18 require a “proven compatible/durable” closure but do not explicitly state that no-write proof must be current for **this durability operation** under the native currentness policy.

An implementation could reuse stale cached proof and acknowledge `saved` without checking current authority where the currentness contract requires it.

### Authority violated if left ambiguous

- Step 5.5 LAW 13 — known compatible durable closure;
- Step 5.7 current-authority-first and exact source pinning;
- WP-12 local known-head/cache non-authority;
- Access/currentness dependencies.

### Required Step-7 repair

`NO_WRITE_NEEDED` is valid only after this operation proves the relevant native domain's current authoritative source basis and required closure are compatible/durable according to that domain's currentness rules. “No pending local write” is not proof.

This does not require gratuitous repository reads when currentness is already lawfully established for the operation.

---

## F03 — Trustworthy acting-principal/delegation source is under-specified

Severity: **SIGNIFICANT**

### Attack

The Connector or repository bridge has technical write capability, but the runtime cannot establish a trustworthy authenticated application principal for a creator/player-authorized publication. Candidate WP13-15 says technical permission is insufficient, but does not explicitly reject forgeable commit-author metadata or require the bridge/session identity source to satisfy Step-5.6 principal semantics.

### Authority at risk

- Step 5.6 laws 2, 29, 30;
- `ACCESS_CONTROL.md` creator/player/policy authority;
- R2.6 supported-profile capability envelope.

### Required Step-7 repair

Publication requires trustworthy resolved acting-principal/delegation evidence from the admitted authentication/identity boundary. Arbitrary caller-supplied commit author/login metadata is not authorization evidence. If the supported profile cannot supply required trustworthy principal evidence, the affected publication is a typed capability/authorization failure.

WP-13 does not redefine creator/player semantics; it consumes their resolved authority.

---

## F04 — `CONFIRMED_REJECTED` lacks mandatory cause classification before retry disposition

Severity: **SIGNIFICANT**

### Attack

`update_ref(force=false)` returns a confirmed rejection. Causes can include:

- stale/non-fast-forward conflict;
- branch/rules/configuration rejection;
- authorization loss;
- invalid target/infrastructure condition.

Candidate preserves rejection versus indeterminate but can be read as sending every confirmed rejection into repin/revalidation/retry.

### Authority at risk

- Step 5.6 laws 14, 21, 28, 29, 38;
- R2.6 capability-failure/no-fallback rule;
- Access Control deny-on-uncertain authorization.

### Required Step-7 repair

A confirmed rejection must be classified before retry:

- stale/currentness conflict -> bounded repin/revalidation path;
- authorization/configuration/capability/infrastructure rejection -> typed failure/repair path, no semantic retry loop and no transport fallback;
- unclassifiable confirmed rejection -> fail closed / typed unresolved infrastructure result rather than guessing stale conflict.

---

## F05 — SAVE quiescence release/abandonment semantics are incomplete

Severity: **SIGNIFICANT**

### Attack

Explicit SAVE freezes local affected scope, then:

- local completeness fails before remote dispatch; or
- campaign publication is confirmed rejected; or
- a required domain fails while coherent HOT survives.

Candidate defines the freeze and failure semantics but not the exact rule for ending that ephemeral quiescence. An implementation could either leave scope accidentally frozen or resume from invalid pre-attempt assumptions.

### Authority at risk

- Step 5.5 LAW 11 / LAW 14;
- Step 5.4 scoped handoff barrier analogy;
- WP-12 currentness/source-movement rules.

### Required Step-7 repair

On successful promise completion, release the SAVE quiescence against the accepted current source composition. On a confirmed failed/abandoned explicit SAVE where coherent HOT remains usable and no independent HARD edge blocks continuation, revalidate/adopt current native source basis as required and then release the local freeze. On indeterminate/unresolved authority, only affected dependent scope remains gated until currentness is established or operation is safely abandoned under owner rules.

No persistent lock/lease record is introduced.

---

## F06 — Risk-control exposure flush can still be accidentally implemented as HARD

Severity: **SIGNIFICANT**

### Attack

Current `DURABILITY_GUARD.md` one-hour rule blocks additional ordinary play after threshold. Candidate rejects the global timer and models scope exposure, but does not explicitly restate Step-5.5's key failure rule:

> a risk-control exposure flush for deferrable local/private state is not itself a correctness-critical HARD barrier.

An implementation could preserve the old blocking semantics under a new scope-relative timestamp.

### Authority at risk

- Step 5.5 laws 17–24;
- Step-5.4 advisory-host-capacity boundary;
- product expectation of long zero-I/O singleplayer stretches.

### Required Step-7 repair

A scope-relative risk-control exposure condition may request opportunistic durability at a safe established-state point. If publication fails while coherent local/private HOT survives, protection is degraded and retry remains due, but ordinary local/private play may continue unless a separate named HARD edge is active. The threshold itself never upgrades the state to HARD.

No numeric threshold is selected in WP-13.

---

# 3. Attacks that passed without new findings

The critic found no defect requiring repair for these candidate properties:

- semantic establishment remains native-owner-relative;
- no global durability frontier/timer/queue/journal;
- bounded closure versus write-set distinction;
- WP-11 direct route and record+required-index publication closure;
- owner-authorized DELETE-side companion updates;
- base-tree byte preservation and semantic no-op normalization;
- one campaign tree + one single-parent commit;
- fixed R2.6 Connector transport and no alternate probing/fallback;
- non-force ref transition;
- accepted/rejected/indeterminate epistemic distinction itself;
- bounded ambiguity verification / no blind retry;
- disjoint transport-only rebuild preserving IDs/RNG/semantics;
- relevant overlap requires native-owner reconciliation;
- automatic retry boundedness;
- exact-generation G adoption / G+1 preservation;
- crash after remote success uses current native authority, not a journal;
- live exact-source CAS remains authoritative;
- checkpoint remains optional/non-authoritative;
- storage metadata stays independent;
- engine/rules maintenance remains a consumer, not publication authority;
- Git order does not become fictional chronology;
- broad scan/global snapshot remains prohibited.

---

# 4. Reopen / decision analysis

None of F01–F06 requires a new product semantic choice.

They are all direct consequences of accepted owners and can be repaired mechanically in Step 7.

```text
UPSTREAM_CONTRADICTION:       NO
NEW_UNSATISFIED_CONSUMER:     NO
MATERIAL_UPSTREAM_INSUFFICIENCY: NO
HUMAN_DECISION_REQUIRED:      NO
```

No external research is required.

---

# 5. Step-6 count

```text
STEP_6_BLOCKING:      2
STEP_6_SIGNIFICANT:   4
STEP_6_MINOR:         0
```

Step 7 must resolve F01–F06 before canonicalization.