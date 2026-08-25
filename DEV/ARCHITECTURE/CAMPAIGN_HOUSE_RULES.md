# Campaign House Rules and Rulings

Status: **CANONICAL ARCHITECTURE — HOUSE RULES DESIGN CLOSED / IMPLEMENTATION NOT STARTED**

Date: 2026-08-25

Canonicalization basis:

- `DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md`
- `DEV/docs/superpowers/research/2026-08-25-campaign-house-rules-step-2-research-architecture-draft.md`
- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-decision-brief.md`
- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-4-collaborative-review.md`
- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-5-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-6-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-7-resolution-gate.md`

Primary inherited owners:

- Step-4 truth/knowledge/role-context canonical specification;
- `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md`;
- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md`;
- Step-5.6 campaign publication canonical specification;
- Step-5.7 checkpoint/recovery canonical specification;
- Step-5.8 multiplayer live/currentness canonical specification;
- `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md`;
- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`;
- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`.

If this document conflicts with a later explicit canonical amendment in one of those owners' scopes, the owning later amendment wins for that scope.

---

# 1. Central invariant

House Rules / established Rulings are a **campaign-persistent, LLM-interpreted normative gameplay-policy layer** for context-dependent Master decisions that cannot or should not be fully represented as deterministic mechanics.

They answer:

> **How, in this campaign, should the Master interpret and resolve situations of this class?**

They do not answer:

- which bytes/state fields to write;
- what random result occurred;
- whether an unauthorized mutation is acceptable;
- which canonical owner may be bypassed.

Canonical execution shape:

```text
player intent + eligible current fiction/state
              |
              v
       LLM / Master semantic judgment
              ^
              |
current published House Rules / Rulings
+ adopted baseline rule sources
              |
              v
bounded typed adjudication result
    / Activity selection
    / legal parameter binding
    / admitted semantic classification
    / proposed consequence
              |
              v
existing deterministic core/capability
              |
              v
validated mutation / RNG / Event / no-op
```

## LAW HR-C1 — LLM MAY DETERMINE SEMANTIC APPLICABILITY; IT MAY NOT MANUFACTURE MECHANICAL AUTHORITY

This is the defining House-Rules boundary.

---

# 2. Constitutional upper boundary

House Rules are below HDM's architecture invariants and native owner contracts.

A campaign policy cannot override or weaken:

- truth / knowledge / disclosure ownership;
- Actor / Asset / Effect / Resource ownership;
- player agency;
- deterministic execution acceptance;
- RNG integrity and no reroll-on-retry;
- idempotency / no-mechanics-replay;
- current-source / repository CAS laws;
- multiplayer authorization/currentness;
- logical role/consumer eligibility and secrecy;
- persistence/durability/recovery laws;
- schema/capability validation;
- bounded execution and current deployment constraints.

Examples of invalid policy:

- “If the scene is dramatic, change an already accepted die result.”
- “An NPC may use any DM secret if it improves the scene.”
- “This prose may directly subtract HP without the normal owner transition.”

## LAW HR-C2 — HOUSE RULES EXTEND GAMEPLAY POLICY, NOT ENGINE CONSTITUTIONAL LAW

A policy entry that conflicts with a constitutional/native-owner invariant is invalid at the conflicting boundary.

---

# 3. Deterministic lower boundary

House Rules may interpret **what should apply**. Existing deterministic owners execute **what actually happens mechanically**.

House Rules shall not directly:

- mutate HP, LifeState, ResourceState or other owner state;
- spend or restore a resource;
- choose or fabricate a random number/result;
- create an Effect/Asset/ownership mutation by prose authority;
- bypass a save/check/attack/Activity/transition contract;
- solve authorization/idempotency/CAS itself;
- commit a canonical mechanical Event directly from prose.

## LAW HR-C3 — MECHANICALLY MATERIAL CONSEQUENCES CROSS AN EXISTING TYPED DETERMINISTIC BOUNDARY

A semantic policy result may select or bind an existing admitted Activity, Rule Element, transition/capability or typed semantic input. The receiving deterministic owner retains validation and execution authority.

## LAW HR-C4 — MISSING REALIZATION IS A FINITE GAP

If current campaign policy requires a mechanically material behavior that no admitted deterministic capability can faithfully realize, HDM reports a bounded `POLICY_REALIZATION_GAP / CATALOG_GAP` (conceptual naming). It shall not silently fall back to a stale contradictory baseline realization and shall not let the LLM mutate state directly.

---

# 4. What belongs in House Rules

Typical valid classes are:

1. **Non-/poorly formalizable criteria** — e.g. whether an argument conflicts with an NPC's fundamental interest.
2. **Campaign interpretation policy** — e.g. how this campaign interprets the meaning of an oath or ambiguous rule.
3. **Stable rulings/precedent** — a consequential reusable adjudication deliberately adopted for future use.
4. **Hybrid policy** — semantic fiction classification belongs to the Master/LLM while a stable deterministic capability owns amount/cost/RNG/state change.

Fundamentally semantic policy may remain prose indefinitely.

---

# 5. What does not belong in House Rules

House Rules is **not a backup mechanics catalog** and is not a generic campaign-policy warehouse.

It does not own:

- ordinary world facts or lore;
- specific NPC/PC secrets or current knowledge;
- campaign history/transcript/Story;
- player preferences or safety/session/table governance;
- deployment, repository, storage, recovery or UI configuration;
- prompt/system instruction text;
- schemas;
- deterministic mechanics already faithfully represented as Activity/Feature/Effect/Rule Element/Resource/etc.

It may reference an existing fact/capability by identity where relevant, but reference does not transfer ownership.

## LAW HR-C5 — RESTATEMENT DOES NOT CREATE OWNERSHIP

Putting a world fact, secret or mechanical state description inside policy prose does not make House Rules authoritative for that information.

---

# 6. Durable policy semantics

Durable campaign policy needs a lightweight semantic envelope. Exact file/schema syntax is implementation work.

A durable policy entry must carry enough meaning for:

```text
stable policy identity
kind                    House Rule | Ruling
lifecycle               active | superseded | retired
campaign scope
bounded gameplay domain / applicability routing
normative policy statement
applicability / non-applicability guidance when material
adoption/provenance authority
exact current revision/publication/source basis
supersession relation when applicable
optional examples / counterexamples
optional refs to existing deterministic capabilities
```

## LAW HR-C6 — SEMANTIC ENVELOPE IS NOT AN EXECUTABLE DSL

These responsibilities exist for identity, currentness, retrieval, conflict, provenance and recovery. They do not define a universal predicate language or natural-language compiler.

## LAW HR-C7 — STABLE POLICY IDENTITY AND EXACT REVISION BASIS ARE DISTINCT

Stable identity supports references/supersession/history. A concrete accepted adjudication also identifies the exact policy revision/publication/source basis it consumed.

---

# 7. House Rule, Ruling and one-off adjudication

### House Rule

A deliberately adopted forward-looking campaign game-rule/adjudication policy.

### Ruling

A reusable precedent retained from a concrete adjudication.

### One-off adjudication

A lawful situational Master decision that may resolve current play but is not durable campaign policy unless explicitly adopted.

## LAW HR-C8 — LIVE ADJUDICATION AUTHORITY != POLICY-ADOPTION AUTHORITY

HDM shall not block lawful local adjudication on campaign-wide adoption/publication. Conversely, the ability to resolve one scene does not automatically grant authority to create shared persistent policy.

## LAW HR-C9 — DURABLE PRECEDENT REQUIRES EXPLICIT AUTHORIZED ADOPTION

Repetition, remembered chat, persuasive wording, local file presence or technical write ability alone cannot make a ruling campaign-wide policy.

House Rules consumes existing campaign authorization/publication mechanisms; it introduces no new ACL model.

---

# 8. Precedence and conflict

Default semantic adjudication precedence:

```text
HDM constitutional/native-owner invariants
    > applicable current explicit campaign House Rule
    > applicable current established campaign Ruling
    > adopted baseline / structured rules sources
    > lawful local Master adjudication
```

This ordering governs semantic interpretation. It never grants prose direct execution authority.

## LAW HR-C10 — CURRENT CAMPAIGN RULES CONTEXT MATTERS

An executable baseline definition is not automatically the valid current gameplay rule merely because it exists. Current authorized campaign policy participates in legality/applicability. If realization is stale or missing, use the finite gap path rather than privileging either stale code or free-form prose.

## LAW HR-C11 — SAME-LEVEL MATERIAL CONFLICT IS EXPLICIT

Two active same-precedence policies that materially conflict for the current decision cannot be resolved by hidden model preference.

Acceptable resolution is one of:

- explicit supersession/retirement;
- an already-authoritative higher rule that deterministically resolves precedence;
- an explicit `POLICY_CONFLICT`-equivalent result requiring authorized policy resolution before the affected mechanically material consequence is accepted.

A local ruling cannot silently become campaign-wide supersession.

---

# 9. Decision-specific information eligibility

House Rules creates no parallel knowledge model.

The existing Step-4 truth/knowledge/disclosure architecture, the single-context role-containment amendment and R2.3 Context Runtime determine which sources are admissible to the concrete semantic decision.

## LAW HR-C12 — INFORMATION ELIGIBILITY IS CONSUMER-SPECIFIC AND DENY-BY-DEFAULT

Physical co-residence in one ChatGPT context, index discovery, explicit mention or policy reference does not grant semantic use eligibility.

The decision receives only the world/epistemic/disclosure material admitted for its role, subject/player and purpose.

## LAW HR-C13 — POLICY TEXT CANNOT ESCALATE ELIGIBILITY

An entry cannot authorize the model to use a fact that the existing information owners deny to that consumer.

Examples/counterexamples or quoted material inside policy are still subject to their proper information eligibility. Policy should prefer abstract criteria or canonical references over embedding secret campaign truth.

---

# 10. Instruction/data fencing

R2.4 instruction architecture remains authoritative.

House Rule/Ruling content is admitted **campaign gameplay-policy data**. It is normative inside that scoped semantic domain because it was validly admitted/published, not because it contains imperative language.

## LAW HR-C14 — POLICY DATA IS NOT A NEW ENGINE-INSTRUCTION TIER

Campaign policy cannot override host/project/CORE constitutional instructions, change logical roles, enlarge tool/authority scope or bypass deterministic gates.

## LAW HR-C15 — DATA CANNOT SELF-PROMOTE TO POLICY

Instruction-like text from player input, lore, Story, Actor dialogue, arbitrary files, quotes or examples does not become House Rule because it “looks like a rule”. Admission/provenance/current publication defines policy authority.

---

# 11. Bounded discovery and retrieval

R2.3 Context Runtime owns bounded House-Rules discovery/closure/currentness/eligibility/allocation.

Conceptually:

```text
registered adjudication need/profile
    -> bounded candidate discovery
    -> authoritative current policy/source resolution
    -> lifecycle filter
    -> role/consumer eligibility
    -> bounded required policy packet
    -> legal representation allocation
    -> LLM semantic applicability
```

## LAW HR-C16 — NO INDEPENDENT HOUSE-RULES RETRIEVAL ENGINE

House Rules shall not introduce a generic policy graph, mandatory vector authority or whole-campaign search loop. It registers the minimum real consumer needs with R2.3.

## LAW HR-C17 — INDEX/CACHE IS ROUTING ONLY

A derived policy index may carry identity/domain/applicability/currentness hints needed for bounded discovery. It is not semantic authority and cannot override the current policy source.

Index omission is not proof of policy absence unless a future explicit authoritative scope contract guarantees exhaustiveness.

## LAW HR-C18 — ORDINARY PLAY REMAINS BOUNDED/LOCAL

House Rules must not require ordinary-turn full-policy scans, full-repository scans, automatic web lookup, unnecessary repository round trips or an extra LLM pass when the needed current policy projection is already available in the working set.

---

# 12. Publication, currentness and multiplayer

Durable campaign policy inherits Step-5.6/5.8 publication/current-source/CAS laws and R2.5 participant currentness.

## LAW HR-C19 — FILE EXISTENCE IS NOT CURRENT CAMPAIGN POLICY

Prepared/local/unpublished content does not become campaign authority merely by existing. Current policy is established through the applicable authorized campaign publication/current-source contract.

## LAW HR-C20 — NO HOUSE-RULES GLOBAL FRONTIER

HDM introduces no universal `policy_epoch`, scalar campaign policy clock or chat synchronization ledger.

The applicable exact campaign policy source/revision participates only as a component of the consuming operation's existing domain-composed current basis.

## LAW HR-C21 — NEW AFFECTED RESOLUTION USES CURRENT POLICY

Before a new Resolution that materially depends on campaign policy is accepted, its policy basis must still be current. If relevant policy currentness changes after assembly and before acceptance, the stale attempt follows the inherited finite currentness/reassembly path instead of committing silently.

## LAW HR-C22 — MULTIPLAYER PROPAGATION IS PUBLICATION + CONTEXT ASSEMBLY

Another/new/joining/rejoining participant does not gain current policy by copying Markdown into a player chat. It acquires the current routed published policy through ordinary R2.3/R2.5 context assembly before its first affected new mutable Resolution.

---

# 13. Retry, recovery and historical stability

Step-5.7 current-authority-first recovery remains the owner.

## LAW HR-C23 — ACCEPTED POLICY-DEPENDENT INPUTS FREEZE WITH THE RESOLUTION GENERATION

Once a semantic adjudication result is accepted as a causal input to a concrete Resolution generation, retain/reference enough accepted evidence to identify:

- participating durable policy IDs, if any;
- exact policy revision/publication/source basis;
- consumer/purpose identity;
- accepted semantic result/typed handoff;
- normal existing accepted execution dependencies.

The exact storage owner is the existing Resolution/recovery architecture, not a duplicate House-Rules execution ledger.

## LAW HR-C24 — LATER POLICY PUBLICATION IS FORWARD-LOOKING

A later policy revision affects new work. It does not retroactively reinterpret an accepted decision generation, reroll RNG or replay accepted mechanics.

## LAW HR-C25 — NEW WORK RECOVERS CURRENT AUTHORITY; OLD ACCEPTED WORK RECOVERS ITS CAUSAL BASIS

This is the required distinction across cold recovery/resume.

---

# 14. LLM semantic applicability

The LLM/Master is deliberately used where meaning and context matter, such as:

- whether leverage is strong enough;
- whether an NPC interest is fundamental;
- whether conduct meaningfully violates an oath;
- whether a concrete fictional source satisfies a qualitative campaign criterion;
- which existing mechanic is the appropriate realization;
- which legal typed value follows when the deterministic consumer explicitly delegates that semantic input.

## LAW HR-C26 — NO UNIVERSAL NATURAL-LANGUAGE PREDICATE COMPILER

These judgments remain bounded semantic adjudication. HDM does not require every policy criterion to be translated into deterministic predicates.

---

# 15. Typed deterministic handoff

Permitted handoffs, where already supported by the receiving owner, include:

- select an existing Activity/capability;
- bind legal typed parameters/targets;
- provide an admitted semantic classification/applicability fact;
- select among already legal deterministic consequences;
- request an existing transition;
- terminate as purely narrative adjudication where no canonical mechanical mutation is required.

## LAW HR-C27 — POLICY CAPABILITY REFERENCES ARE HINTS UNTIL VALIDATED

A capability mentioned by policy is not proven to exist/currently apply merely by mention. Normal catalog/currentness/validation owns admission.

## LAW HR-C28 — NO INVENTED EXECUTABLE PRIMITIVE

The LLM cannot invent an unknown Activity/effect/resource/transition/parameter in prose and treat it as admitted execution.

---

# 16. Promotion ladder

Canonical conceptual ladder:

```text
ONE-OFF ADJUDICATION
    ephemeral
        |
        | explicit durable adoption when useful
        v
CAMPAIGN RULING / HOUSE RULE
    persistent semantic policy
        |
        | stable + formalizable + worth deterministic realization
        v
STRUCTURED CAMPAIGN MECHANIC
    Activity / Feature / Effect / Rule Element / Resource / definition
        |
        | genuinely general engine capability
        v
ENGINE / CORE
```

## LAW HR-C29 — PROMOTION IS OPTIONAL

Repeated semantic policy is not forced into Python/structured mechanics if contextual judgment is intrinsic to the rule.

## LAW HR-C30 — STRUCTURED PROMOTION DOES NOT DUPLICATE MECHANICAL OWNERSHIP

After promotion, the structured definition owns deterministic execution semantics. Remaining prose may retain interpretive policy/provenance only where still genuinely needed.

---

# 17. Failure classes

Conceptual finite policy-boundary results include:

```text
SEMANTIC_RESULT_ACCEPTED
POLICY_CONFLICT
POLICY_REALIZATION_GAP / CATALOG_GAP
INELIGIBLE_CONTEXT
STALE_POLICY_CONTEXT
CONTEXT_UNSATISFIABLE
UNAUTHORIZED_POLICY_ADOPTION
```

Exact enum names are implementation work.

## LAW HR-C31 — FAILURE IS FINITE AND NON-AUTHORITY-CREATING

A boundary failure may block only the affected dependent consequence and may allow unrelated independent work to continue. It cannot create new authority, trigger unbounded retry/scanning or justify direct LLM mutation.

---

# 18. Observability

For mechanically material policy-dependent adjudication, accepted trace/recovery evidence must make it possible to determine:

- which policy IDs/revision basis participated, or that the adjudication was ephemeral;
- which role/consumer/purpose admitted them;
- the accepted semantic result/typed handoff;
- the deterministic consumer/capability invoked;
- terminal conflict/gap/staleness class if execution did not proceed.

## LAW HR-C32 — TRACE IS BOUNDARY EVIDENCE, NOT PRIVATE REASONING

Do not require persistent chain-of-thought, whole prompt/context or whole policy corpus for replay/recovery/audit.

Derived trace/index data never becomes policy or gameplay authority.

---

# 19. Machine-realization acceptance obligations

Later implementation/S6D/R2.7 work must prove at least:

1. House Rule prose cannot directly mutate canonical mechanical state or RNG.
2. Current authorized campaign policy can make stale baseline applicability invalid without granting prose execution authority.
3. Lawful one-off adjudication does not require durable policy publication.
4. Unauthorized local/model-generated policy cannot silently become campaign-wide authority.
5. Same-level material policy conflict is explicit/finite.
6. Ineligible information physically present in the shared ChatGPT context remains unavailable to the concrete policy decision.
7. Policy prose cannot self-promote into higher engine instruction or role switch.
8. House-Rules candidate retrieval is bounded and does not require ordinary-turn whole-corpus/repository scanning.
9. A stale derived policy index cannot override the authoritative current policy source.
10. Relevant policy currentness change before new affected acceptance causes stale detection/reassembly.
11. Joining/rejoining/new participant context consumes current policy before affected mutation.
12. Already accepted policy-dependent Resolution inputs survive retry/resume after later policy publication without reinterpretation or RNG replay.
13. Missing deterministic realization produces a catalog/policy-realization gap rather than free-form mutation.
14. Structured promotion does not duplicate deterministic owner state/behavior.
15. Boundary trace is sufficient without hidden-reasoning persistence.
16. No House-Rules-specific global synchronization/frontier subsystem is required for correctness.

These are architecture obligations, not authorization to implement them in this design cycle.

---

# 20. R2.3 documentation note

The exact current Context Runtime owner used by this architecture is:

- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`.

A convenience architecture path previously named in planning material, `DEV/ARCHITECTURE/CONTEXT_RUNTIME.md`, is absent at the canonicalization HEAD. This is nonblocking navigation/documentation debt and does not transfer R2.3 ownership into this document.

Revisit during the corresponding R2.7 architecture↔machine/navigation reconciliation or an explicit R2.3 documentation maintenance pass.

---

# 21. Explicit forbidden interpretations

This specification must not be read as permission to:

- make every natural-language rule executable;
- persist every improvised ruling;
- read all campaign policy every turn;
- give House Rules a global policy clock;
- synchronize player chats by copying policy prose;
- use House Rules as lore/history/secrets/preferences/config storage;
- let policy text bypass role eligibility or deterministic execution;
- treat a stale executable baseline as higher authority than current valid campaign policy;
- treat current campaign policy as permission for unvalidated prose mutation;
- force fundamentally semantic rules into structured mechanics.

---

# 22. Closure

House Rules is intentionally the durable place where HDM preserves campaign-specific Dungeon Master meaning that benefits from LLM contextual interpretation **without turning the LLM into a second mechanical engine**.

The architecture is closed. Exact schemas/storage realization, concrete ContextNeedProfile IDs, deterministic capability coverage and tests remain downstream implementation/S6D/R2.7 work under their own gates.

`HOUSE_RULES_ARCHITECTURE_STATUS: CANONICAL / CLOSED`
