# Campaign House Rules — Step 5 Candidate Specification

Status: **CANDIDATE SPECIFICATION / STEP 5 COMPLETE / STEP 6 ADVERSARIAL REVIEW NEXT**

Date: 2026-08-25

Decision basis:

- `2026-08-25-campaign-house-rules-step-3-decision-brief.md`
- `2026-08-25-campaign-house-rules-step-4-collaborative-review.md`
- `../design/2026-08-25-campaign-house-rules-step-2-research-architecture-draft.md`

---

# 1. Purpose

Define the campaign-persistent semantic gameplay-policy boundary used by the Master/LLM for context-dependent rulings that cannot or should not be fully encoded as deterministic mechanics.

Canonical intent of the candidate:

> House Rules / established Rulings may determine semantic applicability, campaign interpretation and legal typed inputs to existing deterministic capabilities. They do not own RNG, canonical mechanical state, accepted execution, truth/knowledge/disclosure, authorization or publication currentness.

---

# 2. Non-goals

This candidate does **not** introduce:

- a natural-language rules compiler;
- executable House-Rules DSL;
- a second Activity/effect/state mutation language;
- a generic campaign policy mega-store;
- a new truth/lore/secret/knowledge owner;
- a new global policy epoch/frontier;
- automatic campaign-wide persistence of every Master ruling;
- ordinary-turn whole-repository or whole-policy-corpus scanning;
- a mandatory second LLM pass;
- a schema-first JSON/YAML contract;
- hidden-reasoning/chain-of-thought persistence.

---

# 3. Authority model

## HR-1 — CONSTITUTIONAL LAW WINS

House Rules are below HDM architecture invariants and native owner contracts. They cannot authorize violation of truth/knowledge/disclosure ownership, player agency, deterministic acceptance, RNG integrity, idempotency, no-mechanics-replay, authorization, repository/current-source CAS, persistence/durability, schema validity or bounded execution.

## HR-2 — POLICY AUTHORITY IS SEMANTIC

An active admitted campaign policy entry may govern:

- how a class of situation is interpreted;
- whether an eligible factual situation falls within a campaign norm;
- which existing legal mechanic/capability is semantically appropriate;
- legal typed parameters/targets/classification inputs when the receiving deterministic contract permits them;
- purely narrative adjudication that requires no engine-owned mutation.

It cannot directly perform the mutation/result it recommends.

## HR-3 — CURRENT RULES CONTEXT DEFINES MECHANICAL APPLICABILITY

A baseline structured definition is not constitutional merely because it is executable. If a current authorized campaign policy validly changes gameplay policy, mechanical applicability must be evaluated under that current campaign rules context.

If no admitted deterministic realization can faithfully implement the current rule, the engine reports a finite realization gap instead of silently using stale baseline behavior or allowing prose mutation.

---

# 4. Semantic policy entry contract

A durable campaign policy entry has the following **semantic responsibilities**. Exact storage/schema spelling is deferred.

```text
stable policy identity
kind                    House Rule | Ruling
lifecycle               active | superseded | retired
campaign scope
bounded gameplay domain / applicability routing material
normative policy statement
applicability guidance when needed
non-applicability guidance when needed
adoption/provenance authority
current revision/publication/source basis
supersedes/superseded-by relation when applicable
optional examples/counterexamples
optional references to existing deterministic capabilities
```

## HR-4 — STABLE IDENTITY AND REVISION BASIS ARE DISTINCT

`policy_id`-equivalent identity remains stable across lifecycle/history references. The exact revision/publication/source basis used by a concrete accepted adjudication is separately identifiable.

Updating/superseding a policy does not rewrite the content basis of an already accepted Resolution.

## HR-5 — KIND IS SEMANTIC ORIGIN, NOT EXECUTION CLASS

- **House Rule**: deliberately adopted forward-looking campaign game-rule/adjudication policy.
- **Ruling**: reusable precedent retained from a concrete adjudication.

Both may remain prose, both may have hybrid deterministic handoffs, and neither kind implies executable mechanics.

## HR-6 — STATUS CONTROLS CURRENT POLICY ELIGIBILITY

Only active current policy participates as current normative policy. Superseded/retired entries remain addressable for history/recovery/audit where needed but do not silently re-enter new adjudication.

---

# 5. Ephemeral adjudication and adoption

## HR-7 — LIVE ADJUDICATION DOES NOT REQUIRE CAMPAIGN POLICY ADOPTION

A lawful bounded one-off Master ruling may resolve current play under existing live adjudication authority without waiting for campaign-wide policy publication.

The accepted consequence of that adjudication follows ordinary deterministic/persistence law even if the ruling itself remains ephemeral.

## HR-8 — PERSISTENT PRECEDENT REQUIRES EXPLICIT ADOPTION

A one-off ruling becomes a durable established Ruling/House Rule only through an authorized campaign-policy adoption path.

Model repetition, persuasive wording, local file creation or one participant's technical write ability does not by itself grant campaign-wide normative authority.

## HR-9 — ADOPTION AUTHORITY IS NOT REDEFINED HERE

House Rules consumes existing campaign/user authorization and publication mechanisms. Exact UI/workflow is implementation work. This specification creates no parallel ACL model.

---

# 6. Precedence and conflict

For semantic adjudication, the default precedence is:

```text
HDM constitutional/native-owner invariants
    > applicable current explicit House Rule
    > applicable current established Ruling
    > adopted baseline/structured rules source
    > lawful local Master adjudication
```

This ordering never gives prose direct execution authority.

## HR-10 — SAME-LEVEL MATERIAL CONFLICT IS EXPLICIT

If two active same-precedence policy entries materially conflict for the current decision and no already-authoritative rule resolves that conflict, the runtime/model must not choose a durable interpretation by hidden preference.

The affected semantic policy result is `POLICY_CONFLICT` (conceptual name) and requires authorized conflict resolution before a new mechanically material consequence that depends on choosing one side is accepted.

A local temporary ruling may proceed only when it can lawfully resolve the immediate situation without purporting to change or silently supersede shared campaign policy.

## HR-11 — SUPERSESSION IS FORWARD, NOT RETROACTIVE

Supersession/retirement controls new policy use. Previously accepted/frozen adjudication inputs retain their exact historical policy basis.

---

# 7. Decision-specific information eligibility

## HR-12 — ELIGIBILITY IS DENY-BY-DEFAULT

Policy adjudication receives only evidence admitted for the concrete receiving role/subject/player/purpose/consumer under Step-4 and R2.3.

A source being physically loaded in one ChatGPT context, mentioned in an index, or referenced from a policy entry does not make its semantic contents eligible.

## HR-13 — POLICY DOES NOT OWN WORLD FACTS

House Rules may express abstract applicability criteria or reference existing canonical facts. It does not become authority for NPC secrets, campaign truth, player knowledge, disclosure or history by restating them.

If a policy example/counterexample contains material whose use would violate the receiving consumer's eligibility, that material must not be supplied/used as decision evidence merely because it appears inside the policy artifact.

## HR-14 — NO ELIGIBILITY ESCALATION BY POLICY TEXT

A policy statement cannot instruct the model to use otherwise ineligible information. Eligibility is resolved by existing deterministic/context owners before semantic use.

---

# 8. Instruction/data fencing and scope

## HR-15 — ADMITTED POLICY IS GAMEPLAY-POLICY DATA

House Rule/Ruling text is normative campaign gameplay-policy data under its admitted policy identity. It is not a new system/developer/CORE instruction tier.

## HR-16 — AUTHORITY COMES FROM ADMISSION, NOT IMPERATIVE SYNTAX

Instruction-like text in player input, lore, Story, dialogue, examples, quotes or arbitrary campaign records does not become House Rule merely because it sounds imperative.

Quoted/source/example material inside a policy entry does not self-promote beyond its declared semantic role.

## HR-17 — LOWER POLICY CANNOT OVERRIDE CONSTITUTIONAL INSTRUCTIONS

Requests inside policy data to change role, bypass eligibility, override deterministic validation, reveal hidden data, fabricate RNG or mutate state are invalid regardless of wording.

## HR-18 — GAME-POLICY SCOPE FENCE

House Rules does not own:

- ordinary world/lore facts;
- NPC/PC knowledge or secrets;
- campaign history/transcript/Story;
- player preference, safety or session/table governance;
- deployment/storage/repository/recovery configuration;
- UI/prompt engineering;
- deterministic definitions already faithfully owned by Activities/Features/Effects/Resources/Rule Elements.

---

# 9. Discovery, retrieval and context assembly

House Rules registers one or more bounded R2.3 consumer/task profiles appropriate to adjudication domains. Exact profile IDs are implementation work.

Conceptual pipeline:

```text
adjudication request
    -> bounded candidate discovery from current scope / explicit refs / active dependencies / policy index
    -> resolve authoritative current policy source/lifecycle
    -> role/consumer eligibility
    -> bounded required policy packet
    -> legal representation allocation
    -> LLM semantic applicability/interpretation
```

## HR-19 — R2.3 OWNS BOUNDED DISCOVERY

House Rules does not introduce an independent retrieval engine, world graph or universal natural-language policy search authority.

## HR-20 — INDEX/CACHE IS ROUTING ONLY

A derived policy index/cache may contain stable identity, domain/applicability hints, lifecycle/currentness hints and path/routing data needed for bounded discovery. It does not define policy meaning/currentness and cannot override the authoritative policy source.

Index omission does not prove policy absence unless an explicit current authoritative scope contract guarantees exhaustiveness.

## HR-21 — CURRENT SOURCE MUST BE RESOLVED BEFORE MATERIAL RELIANCE

A policy candidate discovered through stale metadata must be resolved against the applicable current authoritative campaign publication/source before it is used for a mechanically material new adjudication.

## HR-22 — ORDINARY-TURN RETRIEVAL IS BOUNDED/LOCAL

Normal play must not require whole-repository scans, whole-policy-corpus scans, automatic external web lookup, unnecessary repository round trips or an additional LLM pass merely to consult House Rules.

---

# 10. Publication, multiplayer and currentness

## HR-23 — PUBLICATION REUSES STEP 5.6 / STEP 5.8

Durable policy becomes authoritative/current through existing campaign publication/current-source mechanisms and their authorization/CAS rules. File existence or prepared content alone is insufficient.

## HR-24 — NO HOUSE-RULES GLOBAL FRONTIER

No new universal policy epoch, campaign-wide scalar currentness number or global synchronization ledger is introduced.

The applicable campaign-policy source/revision participates as one component of the consuming operation's existing domain-composed current basis.

## HR-25 — NEW AFFECTED RESOLUTION MUST USE CURRENT POLICY

Before acceptance of a new Resolution whose semantics depend on campaign policy, the relevant policy context must still be current under the applicable publication/source basis.

If currentness changes after context assembly and before acceptance, the stale attempt does not silently commit. It follows the existing finite retry/reassembly/current-authority path.

## HR-26 — NEW/JOINING/REJOINING SESSION USES CURRENT POLICY BEFORE AFFECTED MUTATION

A participant/session does not receive authority by copying policy prose from another chat. It acquires current routed campaign policy through normal R2.3/R2.5 context assembly before its first affected new mutable Resolution.

## HR-27 — MULTIPLAYER POLICY PROPAGATION IS NOT CHAT SYNCHRONIZATION

The architectural propagation mechanism is authoritative campaign publication/currentness plus bounded eligible context assembly. There is no requirement to mirror Markdown text among visible player chats.

---

# 11. Retry, recovery and frozen adjudication inputs

## HR-28 — ACCEPTED SEMANTIC INPUTS FREEZE WITH THE RESOLUTION GENERATION

When a semantic adjudication result becomes an accepted causal input to a concrete Resolution generation, the minimum material basis is frozen sufficiently to reproduce/continue that accepted decision across retry/resume without reinterpretation from newly published policy.

Conceptually record/reference:

```text
policy_id(s) where durable policy participated
exact policy revision/publication/source basis
consumer/purpose identity
accepted semantic result / typed handoff identity
other accepted causal inputs already required by execution
```

Exact persistence location follows existing Resolution/recovery ownership; House Rules does not create a duplicate execution ledger.

## HR-29 — LATER POLICY PUBLICATION IS FORWARD-LOOKING

Later policy publication affects new adjudication/current work. It cannot silently change an already accepted result generation, reroll RNG or force replay of accepted mechanics.

## HR-30 — RECOVERY STARTS FROM CURRENT AUTHORITY FOR NEW WORK

Cold/restarted work follows Step-5.7 current-authority-first recovery. Accepted historical inputs are restored/continued as historical causal evidence; new work uses current policy publication.

---

# 12. LLM applicability and typed handoff

The LLM/Master may decide semantic matters such as:

- whether concrete fiction satisfies a qualitative policy criterion;
- whether leverage is “strong”, an interest is “fundamental”, an oath violation is meaningful, a flame source is suitable, etc.;
- which existing capability is the appropriate realization;
- which legal typed parameter value follows from the current policy and eligible fiction when the receiving contract delegates that semantic input.

## HR-31 — SEMANTIC APPLICABILITY DOES NOT CREATE MECHANICAL AUTHORITY

The model cannot infer from “this rule applies” that it may directly write HP/resources/effects/assets/ownership or choose an RNG result.

## HR-32 — HANDOFF USES EXISTING ADMITTED CAPABILITIES

Mechanically material output crosses an existing typed deterministic boundary: Activity selection/binding, Rule Element invocation, admitted typed fact/classification, transition request or another already-owned deterministic consumer.

A candidate capability reference inside policy is a routing hint until normal currentness/validation establishes it.

## HR-33 — NO INVENTED EXECUTABLE PRIMITIVE

If the needed capability/type/parameter is not admitted by the current engine/catalog contract, the model cannot invent it in prose and treat it as executable.

## HR-34 — PURELY NARRATIVE ADJUDICATION MAY TERMINATE WITHOUT MECHANICAL HANDOFF

If the policy decision has no canonical mechanical mutation, it may resolve as narrative/fictional interpretation subject to ordinary truth/agency/narration owners.

---

# 13. Realization mismatch / catalog gap

Conceptual finite outcomes for a policy-dependent mechanical handoff include:

```text
REALIZABLE
POLICY_CONFLICT
POLICY_REALIZATION_GAP / CATALOG_GAP
INELIGIBLE_CONTEXT
STALE_POLICY_CONTEXT
```

Exact enums are implementation work.

## HR-35 — GAP FAILS CLOSED AT THE AFFECTED MECHANICAL BOUNDARY

A gap does not authorize stale baseline execution when that would violate current campaign policy, and does not authorize direct LLM mutation.

The engine may continue unrelated independent work and may allow an authorized human to adopt/revise policy or add a structured capability through the appropriate later workflow.

---

# 14. Promotion

## HR-36 — PROMOTION IS EXPLICIT AND OPTIONAL

A useful conceptual ladder is:

```text
ONE-OFF ADJUDICATION
    -> durable Ruling / House Rule
    -> structured campaign mechanic
    -> generalized engine/core capability
```

Triggers favoring structured promotion include repeated execution, stable semantics, clear typed inputs/outputs, need for deterministic reuse/performance or recurring catalog-gap pressure.

Fundamentally contextual semantic rules may remain House Rules forever.

## HR-37 — STRUCTURED MECHANIC BECOMES ITS OWN EXECUTION OWNER

When policy is formalized into an admitted Activity/Feature/Effect/Rule Element/etc., the structured owner owns deterministic execution. The House Rule may remain as normative provenance/interpretive policy where useful, but it does not duplicate mechanical state/execution semantics.

---

# 15. Observability and trace

## HR-38 — TRACE PRESERVES ACCEPTED BOUNDARY EVIDENCE, NOT PRIVATE REASONING

For a mechanically material policy-dependent Resolution, diagnostic/recovery evidence must make it possible to determine at least:

- policy entry identities/revision basis used, or that the ruling was ephemeral;
- consumer/role/purpose that admitted the policy/evidence;
- accepted semantic result/typed handoff;
- deterministic consumer/capability invoked;
- terminal class where conflict/gap/staleness prevented execution.

Chain-of-thought, entire model prompt and entire policy corpus are not required persistence.

## HR-39 — DERIVED TRACE/INDEX DOES NOT BECOME AUTHORITY

Observability artifacts are evidence/routing only and never supersede the policy source or execution owner.

---

# 16. Failure behavior

| Failure | Required behavior |
|---|---|
| candidate policy source stale | resolve current source; reassemble before new affected acceptance |
| active same-level material conflict | finite `POLICY_CONFLICT`; no hidden preference |
| ineligible secret/context material | omit/fail affected semantic decision; no eligibility escalation |
| required policy packet cannot be assembled | R2.3 `UNSATISFIABLE` / registered safe alternate path |
| current policy lacks faithful deterministic realization | `POLICY_REALIZATION_GAP / CATALOG_GAP`; fail closed mechanically |
| unauthorized adoption attempt | do not publish as campaign policy; local adjudication authority remains separately evaluated |
| downstream LLM/presentation failure after mechanics accepted | do not replay accepted mechanics/RNG |
| policy changes after accepted Resolution inputs freeze | old accepted generation remains stable; new work uses current policy |
| derived index missing/corrupt | do not infer semantic absence; targeted authoritative recovery/audit path |

---

# 17. Acceptance requirements for later machine realization

Implementation cannot claim House-Rules conformance until tests/equivalent proofs demonstrate:

1. campaign policy cannot directly mutate engine-owned state or RNG;
2. a current campaign policy can invalidate stale baseline applicability without granting prose execution authority;
3. one-off live adjudication works without persistent adoption;
4. unauthorized local ruling cannot silently become shared campaign policy;
5. same-level conflict is explicit and finite;
6. secret/ineligible source physically present in the shared context is not usable by an ineligible consumer;
7. policy text cannot role-switch or override higher engine instructions;
8. bounded retrieval does not require full-policy/repository scan in ordinary play;
9. stale derived index does not outrank authoritative policy source;
10. policy change before new affected Resolution acceptance causes stale detection/reassembly;
11. new/joining/rejoining participant uses current policy before affected mutation;
12. accepted policy-dependent Resolution survives retry/resume after later policy publication without reinterpretation/reroll;
13. missing deterministic capability yields catalog/realization gap rather than prose mutation;
14. promotion to structured mechanics does not duplicate mechanical ownership;
15. trace identifies the accepted policy basis/result without persisting hidden reasoning;
16. no House-Rules global currentness/frontier subsystem is required for correctness.

---

# 18. Downstream integration obligations

## R2.3 Context Runtime

Register/realize the minimum policy discovery profile(s), candidate routing metadata, currentness resolution, eligibility and bounded packet closure required by supported adjudication consumers. No new Context Runtime authority is introduced.

## R2.4 single-context execution

Carry policy packet/result through existing TurnEnvelope/role-rebind/data-fencing principles. Do not create a privileged prompt tier.

## Step 5.6 / 5.7 / 5.8 and R2.5

Reuse publication/CAS/current-authority/recovery/multiplayer currentness. No new global synchronization model.

## S6D / later machine realization

S6D may need to close concrete deterministic capability/catalog gaps exposed by current campaign-policy examples and ensure structured rules can represent supported promoted mechanics. This candidate does **not** start S6D.

---

# 19. Candidate gate

The candidate satisfies the approved Step-1 semantic frame, Step-2 evidence and Step-3 decision without selecting an executable policy DSL or duplicating existing owners.

`STEP_5_RESULT: COMPLETE`

Next: **Step 6 — Adversarial Architecture Review**.
