# Campaign House Rules — Step 4 Collaborative Architecture Review

Status: **STEP 4 COMPLETE / DECISION READY FOR CANDIDATE SPEC / STEP 5 NEXT**

Date: 2026-08-25

Reviewed decision:

- `2026-08-25-campaign-house-rules-step-3-decision-brief.md`

Review basis:

- owner-approved Step-1 semantic framing;
- Step-2 complete Source Manifest and synthesis;
- explicit owner GO for Steps 2–8;
- current Round-1/Round-2 canonical owners.

---

## 1. Review objective

Test whether the accepted Alternative C remains coherent when integrated with:

- Step-4 truth/knowledge/disclosure and single-context role containment;
- R2.3 Context Runtime;
- R2.4 one-context TurnEnvelope and instruction/data hierarchy;
- Step-5.6/5.7/5.8 publication/currentness/recovery;
- R2.5 multiplayer join/rejoin and shared-canon semantics;
- Activity/Rule Element deterministic execution;
- current gameplay policy and hot-path constraints.

The review does not reopen Step 1 and does not choose implementation schemas.

---

# 2. Review findings

## CR-1 — PASS — Policy authority is separated from execution authority

Alternative C preserves the central deterministic architecture:

```text
semantic applicability / campaign interpretation
    -> typed proposal/binding
    -> deterministic validation/execution
```

No policy record gains RNG, mutation or event-commit authority.

## CR-2 — PASS — Current campaign policy can make baseline realization stale without making prose executable

The Decision Brief correctly avoids both invalid extremes:

- “Python definition always wins even when current authorized campaign policy changed the rule”; and
- “policy prose can directly override deterministic execution”.

The finite mismatch state is a required design property. Step 5 must name the failure contract clearly enough that implementations cannot silently choose one side.

## CR-3 — PASS WITH SPECIFICATION SHARPENING — Stable policy identity and revision basis

A durable entry needs stable semantic identity, while each accepted Resolution must also be able to identify the exact current policy basis it consumed.

Step 5 shall distinguish:

- stable `policy_id` semantics from
- current revision/publication/source-basis identity.

A policy may be amended/superseded without retroactively changing old accepted causal inputs.

## CR-4 — PASS — Live ruling does not require policy adoption

The design preserves local-first play. A lawful one-off Master adjudication may resolve the immediate situation without first publishing campaign policy.

Only durable shared precedent requires policy-adoption authority.

## CR-5 — PASS WITH SPECIFICATION SHARPENING — Conflict behavior

Same-precedence materially conflicting current policy entries must not be resolved by hidden model preference.

Step 5 shall require one of:

- explicit supersession/retirement makes only one entry current;
- an already-defined higher-level policy deterministically resolves precedence; or
- the affected policy interpretation is marked conflict/unsatisfied and escalated to authorized policy resolution.

A local scene ruling may not silently become a campaign-wide conflict resolution.

## CR-6 — PASS — Information eligibility reuses existing owners

Step-4/R2.3 already supplies the right authority model. No House-Rules knowledge store is needed.

Step 5 must make source admissibility deny-by-default at the **consumer decision** boundary and must not treat a physically present policy example as permission to use otherwise ineligible secret/world information.

## CR-7 — PASS — Instruction/data fencing reuses R2.4

The design does not create a new prompt tier. Admitted policy is scoped campaign gameplay-policy data below constitutional engine instructions.

Step 5 must explicitly reject:

- imperative prose outside the admitted policy source becoming policy by appearance;
- quoted examples becoming commands;
- policy text requesting a role switch or bypass of deterministic gates.

## CR-8 — PASS — Bounded discovery reuses R2.3

A registered House-Rules consumer profile can use existing bounded multi-channel discovery and packet closure. Derived policy indexes remain routing-only.

No separate semantic search authority or universal rule graph is justified.

## CR-9 — PASS WITH SPECIFICATION SHARPENING — Stale derived index

A stale derived index may omit or misroute a current policy candidate. Therefore:

- index/cache identity cannot be policy authority;
- material use must resolve current authoritative policy source before semantic reliance;
- an implementation claiming an exhaustive policy candidate set must derive exhaustiveness from an explicit authoritative scope contract, not from index silence.

## CR-10 — PASS — Multiplayer propagation is current publication + context assembly

No policy-copy protocol between chats is needed.

R2.5 already requires current routing and eligible context before mutable join/rejoin input. For House Rules, Step 5 should generalize this to “before the first **affected new Resolution** in a session after relevant policy currentness changes.”

## CR-11 — PASS — Accepted historical decisions remain stable

Step-5.7 recovery law is compatible with policy updates:

- unaccepted future work uses current authority;
- accepted causal inputs remain fixed for retry/resume;
- later publication does not retroactively rewrite already accepted outcomes.

## CR-12 — PASS — No global policy frontier

No evidence requires a universal policy epoch. Policy publication/source revision participates only as the applicable current campaign-policy component of the consuming operation's domain-composed basis.

## CR-13 — PASS — Promotion ladder does not force formalization

The design preserves semantic rules that should remain semantic. It also gives repeated formalizable mechanics a route into structured campaign mechanics without making House Rules a permanent backup catalog.

## CR-14 — PASS WITH SPECIFICATION SHARPENING — Trace minimum

For mechanically material adjudication, observability must retain enough accepted evidence to establish:

- which policy entry/revision or local-ruling basis was used;
- which consumer/role/purpose admitted it;
- the bounded semantic result handed to deterministic execution;
- whether execution succeeded, conflicted or encountered a realization gap.

This need not persist chain-of-thought or entire prompt/context.

## CR-15 — PASS — Scope fence

House Rules remains limited to campaign game-rule/adjudication policy. It is not the owner for lore/truth/history, player preferences, safety/session governance, deployment/storage/repository behavior, UI policy, prompts or already-structured mechanics.

---

# 3. Decision-ready deltas from review

No new product-semantic decision is required.

Step 5 must sharpen five implementation-independent contracts already implied by the accepted decision:

1. stable policy identity versus exact revision/publication basis;
2. finite same-precedence conflict result;
3. authoritative-source currentness despite stale derived index;
4. pre-acceptance stale-context detection for new affected Resolutions across sessions;
5. minimal accepted trace/provenance without hidden-reasoning persistence.

These are correctness details, not alternative architecture choices.

---

# 4. Review gate

| Question | Result |
|---|---|
| Violates Step-1 purpose? | NO |
| Creates second mechanical authority? | NO |
| Creates parallel truth/knowledge owner? | NO |
| Creates new global synchronization/frontier? | NO |
| Requires schema-first design? | NO |
| Breaks local-first adjudication? | NO |
| Breaks multiplayer currentness/recovery? | NO |
| Leaves material issue requiring owner choice? | NO |

`STEP_4_RESULT: PASS`

Next: **Step 5 — Candidate Specification**.
