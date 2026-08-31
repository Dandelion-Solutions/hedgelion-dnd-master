# Campaign House Rules — Step 6 Adversarial Architecture Review v2

Status: **ADVERSARIAL REVIEW COMPLETE / 0 BLOCKER / 2 SIGNIFICANT RESOLUTION ITEMS / STEP 7 NEXT**

Date: 2026-08-25

Reviewed candidate:

- `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-5-candidate-spec-v2.md`

Mandate: attack authority bypass, creator/delegation currentness, prose/sidecar coherence, policy-realization linkage, stale-session behavior, notification semantics, information leakage, retry/recovery and second-rules-engine drift.

---

## AR2-1 — authority-class downgrade attack

**Attack:** active PLAYER labels an action-economy/resource override as `INTERPRETIVE_POLICY` to use default authority.

**Candidate defense:** HR5-11 classifies by semantic effect; mixed indivisible policy requires stronger authority.

**Verdict:** PASS.

---

## AR2-2 — self-grant in same campaign transaction

**Attack:** non-creator edits their own `PLAYER.policy_authority.mechanical_override_policy` to true and publishes a mechanical rule in the same commit.

**Defense:** grant mutation is itself creator-only access-control state. Step-5.6 validates complete resulting state + acting principal/application authorization before publication; technical CAS cannot authorize the grant.

**Verdict:** PASS, provided canonical contract keeps grant/revoke as creator-only HARD access-control mutation.

---

## AR2-3 — stale delegate races creator revocation

**Attack:** delegate prepares mechanical policy while grant true; creator revokes; stale delegate publishes.

**Defense:** authorization dependencies are part of Step-5.6 conflict footprint; grant/revoke is HARD; moved authority requires revalidation.

**Verdict:** PASS.

---

## AR2-4 — later deactivation invalidates old policy

**Attack:** policy adopter later becomes inactive or loses mechanical grant; runtime concludes previously adopted policy is no longer authoritative.

**Required interpretation:** adoption authorization is checked at publication of each policy revision. Later loss of adopter authority is prospective and must not retroactively invalidate already current published policy. Only explicit supersession/retirement/new policy revision changes current policy.

**Verdict:** PASS WITH CANONICAL CLARIFICATION; no new field required.

---

## AR2-5 — unindexed prose bypasses structured adoption/currentness evidence

**Severity: SIGNIFICANT.**

**Attack:** participant appends a normative-looking paragraph to `HOUSE_RULES.md` outside any sidecar entry. If runtime treats all Markdown as policy, stable identity, authority class, adoption basis, supersession and bounded retrieval can be bypassed.

**Required resolution:** every durable normative House Rule/Ruling intended as current campaign policy must correspond to exactly one current sidecar entry/source anchor. Unindexed prose may be explanatory/scaffold text but is not admitted as durable policy authority. Duplicate anchors/IDs or sidecar entries without resolvable normative sections are malformed policy and rejected/treated as integrity defect at the affected policy boundary.

This does not make YAML the normative owner; it makes sidecar admission evidence mandatory around normative prose.

**Human decision required:** NO.

---

## AR2-6 — `capability_refs` is too ambiguous for policy/realization linkage

**Severity: SIGNIFICANT.**

**Attack:** a mechanical policy points vaguely at capabilities as “hints”; runtime cannot distinguish an intended typed realization from incidental references, so stale realization/divergence detection remains underspecified.

**Required resolution:** replace ambiguous sidecar `capability_refs` with explicit optional `realization_refs` meaning “these current typed capabilities are the claimed executable realization of the formalizable portion of this policy.”

Rules:

- references remain subject to normal catalog/currentness/validation and never become execution authority by mention;
- mechanically material policy requiring realization with no admitted usable `realization_refs` yields `POLICY_REALIZATION_GAP`;
- present refs that are missing/stale/incompatible yield finite realization mismatch/gap behavior rather than fallback to stale baseline or prose execution;
- semantic equivalence is not asserted merely because IDs resolve; adoption/review/conformance evidence must establish the intended mapping;
- contextual policy may legally have no realization refs forever.

No persisted global realization status is required because validity is current-context dependent.

**Human decision required:** NO.

---

## AR2-7 — interpretive policy indirectly produces DC/mechanical input

**Attack:** any interpretive policy that influences a DC is reclassified as mechanical override, defeating the intended LLM-native layer.

**Defense:** authority class distinguishes **changing baseline mechanical semantics** from applying/adjudicating existing mechanics. An interpretive norm may guide contextual leverage/DC selection through an admitted bounded adjudication input without itself changing the baseline D20/Test execution rule.

**Verdict:** PASS; preserve wording carefully.

---

## AR2-8 — policy edit without sidecar byte change loses revision identity

**Attack:** same adopter edits normative text while sidecar fields remain byte-identical.

**Defense:** exact policy revision is stable `policy_id` + exact campaign revision selecting both files. Sidecar need not change bytes for the campaign revision to change. Any normative change still passes policy-adoption authorization before publication.

**Verdict:** PASS after AR2-5 admission requirement.

---

## AR2-9 — multiplayer notification becomes delivery subsystem

**Attack:** requirement to inform all other Masters' players grows into push/outbox/read-receipt machinery.

**Defense:** notification is discovered only on ordinary campaign refresh, appended to ordinary current response, and has no exactly-once correctness requirement. Existing session base/currentness is enough.

**Verdict:** PASS.

---

## AR2-10 — notification leaks fiction/knowledge

**Attack:** OOC notice implicitly tells PC that another PC/player changed something or exposes secret rule applicability.

**Defense:** notice is explicitly OOC/player-facing, not fictional event/PC knowledge. Content must summarize the policy change without leaking ineligible world facts embedded elsewhere.

**Verdict:** PASS under existing information eligibility.

---

## AR2-11 — stale session accepts new policy-dependent work

**Attack:** one participant uses stale policy after another publication.

**Defense:** existing campaign currentness cadence remains authoritative; once a required refresh observes new HEAD, policy paths are relevant, new affected work uses refreshed policy. Prepared policy-dependent work whose authorization/rules basis moved must revalidate; already accepted Resolution inputs remain frozen.

No background polling is invented.

**Verdict:** PASS within inherited multiplayer currentness model.

---

## AR2-12 — sidecar becomes a second rules DSL

**Attack:** routing keys/authority/lifecycle fields expand into predicates, expressions and arbitrary state queries.

**Defense:** schema contains identity/adoption/routing linkage only and explicitly forbids executable expressions/query/state injection. Rich semantic applicability remains LLM-native; deterministic consumers remain existing owners.

**Verdict:** PASS.

---

## AR2-13 — creator cache becomes new authority

**Attack:** session-local cached creator identity survives contradictory evidence and becomes canonical owner.

**Defense:** cache is derived authorization evidence only. Git initialization provenance remains authority; cache is refreshed/re-resolved when integrity/current authorization is suspect. No MANIFEST creator field added.

**Verdict:** PASS.

---

## AR2-14 — mixed prose/typed policy silently executes stale baseline

**Attack:** current policy says Bonus Action but old Activity says Action; runtime chooses executable old Activity.

**Defense:** current policy participates in current rules context; explicit realization refs + finite gap/mismatch prohibit stale executable preference.

**Verdict:** PASS after AR2-6 resolution.

---

# Final adversarial disposition

```text
BLOCKER: 0
SIGNIFICANT: 2
  AR2-5 mandatory normative-entry/sidecar admission linkage
  AR2-6 explicit realization_refs linkage
MINOR: 0
NEW HUMAN DECISION: 0
```

Both significant findings have direct derivable resolutions consistent with the approved H1/H2 model. Step 7 must materialize them and obtain fresh focused verification before canonical closure.
