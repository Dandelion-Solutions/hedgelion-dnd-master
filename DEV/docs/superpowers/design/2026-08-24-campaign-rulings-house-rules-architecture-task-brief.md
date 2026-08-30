# Campaign House Rules / Rulings Architecture — Step 1 Architecture Task Brief

Status: **STEP 1 AMENDED / EXPANDED-CRITIC REQUIRED / STEP 2 HELD UNTIL CRITIC PASS**

Date: 2026-08-25

This file **supersedes its previous Step-1 content in full**. The earlier Task Brief introduced an over-broad generic rulings/lifecycle framing and MUST NOT be used as architecture evidence or as a source of requirements.

The 2026-08-25 owner review accepted the core framing and added six binding amendments before Step 2: information eligibility, current-rule-context legality, live-vs-adoption authority, multiplayer effective frontier, instruction/data fencing, and campaign-policy scope fencing. Those amendments are integrated below and are not optional Step-2 hypotheses.

Current program sequence remains:

```text
R2.7 WP-06 PAUSED
    -> House Rules Steps 1..8
    -> House Rules canonicalization
    -> S6D, one full eight-step cycle per numbered task/domain
    -> S6D integrated closure
    -> R2.7 WP-06 resume
```

No GAME/schema/runtime implementation is authorized by Step 1 itself.

---

# 1. Classification

**Architectural / cross-cutting.**

The work defines a product-semantic and authority boundary between:

- campaign-specific normative game-rule/adjudication policy;
- genuine Dungeon-Master/LLM semantic adjudication;
- engine-established legality and state-derived facts;
- decision-specific information eligibility;
- deterministic execution and RNG;
- canonical truth/knowledge/relationship/mechanical state owners;
- bounded campaign-policy retrieval;
- policy adoption/publication/currentness;
- optional typed realization of formalizable campaign policy.

A wrong design can either reduce the Master to a brittle classifier in front of an oversized deterministic DSL, or create a second prose/LLM authority capable of bypassing canonical state ownership. It can also accidentally permit DM-only information to leak into role-specific adjudication, make transient rulings block play on campaign-wide adoption, or turn Markdown into a privileged instruction channel. All are unacceptable.

---

# 2. One-sentence mission

> Design the HDM campaign-specific normative game-rule/adjudication policy layer so that the LLM/Master owns fiction-dependent semantic adjudication over only decision-eligible information, accepted semantic decisions cross into execution as bounded frozen inputs, formalizable campaign policy may have a verifiable typed realization, contextual policy may remain LLM-native indefinitely, and neither policy prose nor LLM judgment can override current engine-established facts, bypass the acceptance boundary of the affected owner, escape campaign authorization/currentness, or become a privileged instruction channel.

---

# 3. Binding product purpose — what this layer is for

This purpose is owner-approved product semantics and is not a hypothesis for Step 2 to discard.

HDM intentionally preserves a real Dungeon Master rather than attempting to encode all gameplay meaning in Python/catalog mechanics.

Campaign-specific rule policy exists to answer questions of the form:

> **How should the Master interpret and resolve situations of this class in this campaign?**

It may affect:

- interpretation of natural-language intent;
- fictional applicability;
- causal and social judgment;
- meaningful uncertainty;
- whether a roll is required;
- choice among mechanically admissible tests/capabilities;
- bounded adjudicated parameters such as a fair DC or semantic classification;
- campaign-specific modifications to baseline mechanics;
- canonical fictional consequences, provided those consequences cross their normal owning acceptance boundary.

It does **not** answer:

- what RNG value occurred;
- whether current authoritative state says a spell is prepared;
- whether a resource exists when its authoritative current value is zero;
- what bytes to write into HP/Resource/Effect/ownership/current world state;
- whether an unsupported executable primitive should be invented;
- whether an owner validation/authorization rule may be bypassed;
- what secrets an NPC or player may use merely because the runtime/DM has loaded them;
- safety/session-governance/player-preference/deployment/storage/repository/UI policy already owned elsewhere.

The architecture must preserve this distinction even when a campaign rule materially changes mechanics.

---

# 4. Binding requirement: runtime must know the purpose, not rediscover it

The House Rules design is incomplete if its purpose and safety boundary exist only in dated DEV design artifacts.

By the end of this eight-step cycle, the canonical architecture MUST designate the shipped runtime owner(s) that make the following facts unambiguous during gameplay:

1. what campaign-specific normative game-rule/adjudication policy is for;
2. what kinds of decisions the Master/LLM is allowed to make from it;
3. what information is eligible for each adjudication consumer/role;
4. what current engine facts/legality the Master may not override;
5. what acceptance boundary a resulting change must cross;
6. what distinguishes immediate live adjudication authority from campaign-wide policy-adoption authority;
7. when an adopted/published policy revision becomes current for other participants/sessions;
8. what to do when a policy has no safe executable realization;
9. what to do when normative policy and its typed realization are inconsistent;
10. what information must remain with truth/knowledge/other canonical owners rather than being stored as a house rule;
11. why authorized policy Markdown is bounded policy data and not a new system-instruction tier;
12. what adjacent normative concerns are outside House Rules because another owner already exists.

The later implementation realization MUST include machine/runtime tests or equivalent enforceable checks for every part of this boundary that is mechanically enforceable.

This requirement does **not** pre-decide that a new `GAME/CORE/RULINGS.md` is needed. Existing always-active owners may own/delegate the invariant if that is clearer and avoids duplicate authority.

---

# 5. Core authority model to preserve

## 5.1 Architecture invariants constrain campaign policy

Campaign policy is below HDM constitutional invariants.

No House Rule or adopted Ruling may authorize behavior that violates higher architecture law such as:

- RNG integrity;
- player agency;
- truth/knowledge/disclosure ownership and role-context eligibility;
- Actor/Asset/Effect/Resource ownership;
- deterministic acceptance and idempotency;
- repository currentness/CAS and multiplayer authorization;
- persistence/durability law;
- schema validity;
- bounded execution;
- supported deployment constraints.

A purported rule that conflicts with those invariants is not a legal House Rule realization.

## 5.2 Campaign policy is normative, not execution authority

Campaign-specific policy says **what game rule/adjudication norm the campaign has adopted** and how the Master should interpret applicable situations.

It may legitimately differ from baseline rules.

Markdown/prose may therefore have normative mechanical effect. The prohibition is not “prose may not influence mechanics.” The prohibition is direct execution/mutation from prose without the owning deterministic acceptance path.

## 5.3 LLM/Master owns fiction-dependent semantic adjudication

Within campaign policy and baseline adjudication constraints, the Master/LLM may determine genuinely semantic questions such as:

- intended outcome and approach;
- fictional positioning;
- causal feasibility not already settled by current engine-owned state/rules context;
- whether uncertainty is meaningful;
- `AUTOMATIC`, `IMPOSSIBLE`, or uncertain when that classification depends on fiction rather than an engine-established prohibition/permission;
- fictional leverage, sufficiency, scale, quality or contextual category;
- which admissible test/capability best matches intent;
- stakes and a fair adjudicated DC before randomness;
- whether natural-language intent maps to an available capability among bounded candidates.

The LLM is therefore not merely a Boolean predicate classifier in front of Python.

## 5.4 Deterministic owners retain current engine-established legality and facts

Binding law:

> **LLM owns semantic adjudication of fiction-dependent questions. Deterministic owners retain authority over engine-established legality and state-derived facts. An LLM adjudication may supply missing semantic inputs, but may not override an established engine-owned fact.**

For this law, **engine-established fact/legality means the result of authoritative current state plus the current validated campaign rules context admitted for the decision. It does not mean “whatever an old executable definition currently says.”**

Therefore:

- an authoritative prepared-spell/resource/ownership/state fact remains non-overridable by LLM judgment;
- an adopted current campaign rule may legitimately supersede baseline mechanics in its permitted scope;
- a stale typed realization does not acquire constitutional authority merely because it is executable;
- if current normative campaign policy requires mechanics that are not yet safely realized, the LLM does not rewrite the executable definition ad hoc: runtime reaches the designed policy-realization mismatch/gap behavior at the affected mechanical boundary.

Examples:

- Master may judge that a jump is fictionally impossible; Master may not declare an unprepared spell prepared.
- Master may judge that leverage justifies a lower DC; Master may not spend a Resource whose authoritative current value is zero.
- Master may map intent to an existing Activity; Master may not invent an executable primitive absent from the admitted capability set.
- If current campaign policy says potion self-use is a Bonus Action while a stale realization still says Action, the stale realization is not the definition of current legality; the inconsistency must be detected and resolved through the finite mismatch/gap contract rather than by silently executing Action or letting prose mutate cost directly.

## 5.5 Every consequence uses its owning acceptance boundary

Campaign policy may influence semantic adjudication, mechanical applicability, parameters, mechanics and canonical fictional consequences, but it never bypasses the acceptance boundary of the state owner it affects.

Conceptually:

```text
current campaign policy + decision-eligible fiction/state
        -> LLM semantic adjudication
        -> bounded accepted decision/input
        -> owning acceptance boundary
            -> mechanical owner / RNG / deterministic execution
            -> truth/world owner
            -> knowledge owner
            -> Actor/relationship/other owner
            -> narration only when no durable owner transition exists
```

A semantic result is not exempt merely because it is non-mechanical.

## 5.6 Information-eligibility boundary

Physical availability to the runtime/DM is not semantic eligibility for every adjudication consumer.

Binding law:

> **Every adjudication uses only the epistemic/world view legally eligible for that decision and role. Loaded objective truth, DM-only knowledge, another character’s knowledge, hidden prep or undisclosed information does not become an admissible input merely because it is present in context.**

This is especially important for NPC/social adjudication. For example, “is this argument convincing to this NPC?” must be evaluated from the NPC’s eligible knowledge/beliefs, goals, relationships, incentives and current circumstances — not from objective secrets unknown to that NPC.

This law does not require the Master itself to be ignorant of secrets. It requires each adjudication consumer to use only the view authorized by existing truth/knowledge/disclosure/role-context owners.

Step 2 must determine how existing Context Runtime/role-context machinery supplies or fences this eligible view without creating a parallel knowledge model inside House Rules.

## 5.7 Instruction/data fencing

Authorized House Rule/Ruling text is campaign policy **data inside a bounded policy contract**, not a new constitutional/system-instruction layer.

Therefore:

- policy prose cannot waive CORE/architecture invariants by saying “ignore CORE”, “always succeed”, “skip validation”, or equivalent;
- imperative prose in lore, NPC books, player quotations, chat text, imported documents or arbitrary Markdown does not become House Rule merely because it looks like an instruction;
- only content admitted through the campaign-policy ownership/adoption path may act as campaign normative policy, and even admitted policy remains constrained by §§5.1–5.6 and owning acceptance boundaries;
- policy interpretation must distinguish normative game-rule content from quoted/example/data text within the same document format where relevant.

Step 2 must determine the minimum runtime contract needed to make this fencing robust without inventing a second prompt/security architecture.

---

# 6. Frozen adjudication input requirement

House Rules must preserve the existing execution principle that accepted causal inputs do not float after acceptance.

Conceptual flow:

```text
current campaign policy + decision-eligible fiction/state
        -> LLM semantic adjudication
        -> bounded typed adjudication inputs
        -> deterministic validation / acceptance
        -> frozen causal input set
        -> RNG + deterministic execution / owner transition
```

Once accepted for a concrete Resolution/transition generation, a material adjudication input such as an adjudicated DC, semantic classification, applicability result, chosen admissible test or similar value MUST NOT silently change because of:

- retry;
- suspension/resume;
- Narrator failure;
- context compaction/reconstruction;
- a later model pass;
- seeing the RNG result;
- a changed desired narrative outcome;
- a later campaign-policy publication that was not current for the accepted Resolution input set.

The current Step-2/Step-3 architecture already has this discipline for accepted invocation facts. House Rules must preserve and, where required, generalize the discipline without weakening it.

---

# 7. Bounded typed adjudication channel — explicit extension, not accidental overloading

Current Step-2 machine policy initially admits registered boolean `INVOCATION_ADJUDICATED` context facts and keeps state-sensitive selectors conservative/`ENGINE_STATE`-only.

House Rules may require richer adjudication values such as:

- bounded numeric DC/threshold input;
- enum/classification input;
- bounded candidate selection;
- semantic target/context classification;
- another reviewed scalar/value required by a real rule case.

This is a real extension of the nondeterministic input interface and MUST be designed explicitly.

Do not silently reinterpret the current boolean context-fact mechanism as a generic arbitrary-value channel.

The design must determine the minimum bounded typed adjudication interface needed for supported cases, its provenance/admission rules, its information-eligibility constraints, its consumers, its freezing/retry identity, and how engine-owned facts remain impossible to smuggle through it.

No arbitrary JSON path, expression language, eval, query DSL or free-form state mutation payload is permitted.

---

# 8. Supported rule shapes — modes, not mandatory entity classes

The architecture must support at least these semantic shapes without assuming they require distinct stored record types.

## 8.1 Policy + formal execution

Example scenario, not a default HDM rule:

```text
Campaign policy:
    a character may drink an accessible potion on self as Bonus Action;
    giving/applying it to another creature remains Action.

LLM/Master:
    interprets natural-language intent and whether the situation matches the policy.

Typed realization:
    admitted Activity/activation/cost/target rules express the deterministic part.

Deterministic owner:
    validates current campaign rule context, action economy, accessibility/resources,
    execution and state change.
```

A fully formalizable mechanical consequence may have a concise human/LLM-readable normative declaration/reference rather than a duplicated copy of every machine detail.

## 8.2 Policy + LLM adjudication + formal execution

Example scenario:

```text
Campaign policy:
    very strong established fictional leverage may make a social check automatic
    or materially change the adjudicated DC.

LLM/Master:
    evaluates only decision-eligible NPC knowledge/beliefs, evidence, motives,
    relationships and current fiction;
    decides AUTOMATIC or a bounded DC before RNG.

Deterministic owner:
    accepts/validates the input, performs real RNG/arithmetic, commits consequence.
```

Do not replace this with a pseudo-formula such as a universal `convincing_argument > 0.73` threshold.

## 8.3 Policy + primarily semantic/canonical result

A policy may resolve a fiction-sensitive situation without a mechanical roll.

If the result is only transient presentation, narration may be sufficient.

If it establishes/changes canonical world truth, knowledge, relationship, ownership or another durable semantic fact, the result still crosses that owner’s acceptance boundary.

“Non-mechanical” never means “free direct write into canon.”

---

# 9. Normative policy versus typed realization

The architecture must explicitly separate these roles:

```text
NORMATIVE CAMPAIGN POLICY
    what the campaign has adopted / how Master should rule

TYPED REALIZATION
    how the formalizable part is safely executed by existing capabilities
```

They are related but not independent competing sources of truth.

## 9.1 No mandatory full duplication

Do not require every formalized rule to exist twice in full detail in Markdown and machine definitions.

Human/LLM-readable policy may be concise and may reference its typed realization.

## 9.2 Currentness/version linkage is required where a realization claims to implement policy

If typed realization claims to implement a normative policy, the system needs a mechanically checkable way to know **which current normative decision/revision it implements**.

The exact representation is not chosen in Step 1. Step 2 must determine the minimum identity/current-revision/supersession linkage required for:

- policy change;
- realization invalidation;
- correction/supersession;
- trace/debug;
- avoiding execution of stale mechanics.

This does not pre-authorize a generic ruling registry or stable-ID schema for every one-off adjudication.

## 9.3 Divergence must be operationally finite

If current normative policy and claimed typed realization disagree, runtime MUST NOT silently choose either side merely because one is prose or the other is executable.

The design must define a finite typed integrity outcome/state for policy-realization mismatch.

A stale baseline/executable definition is not “engine-established legality” merely by being executable. Current legality is evaluated from authoritative state plus current validated campaign rules context. If the current policy cannot be faithfully realized through admitted primitives, the affected mechanical boundary must stop with the designed mismatch/gap outcome rather than execute stale semantics or let the LLM rewrite mechanics directly.

A mismatch may be recoverable only when the policy can still be faithfully represented through already-admitted bounded primitives for the current case.

## 9.4 Unsupported realization gap is explicit

A campaign policy may not invent an engine primitive that does not exist safely.

If the intended formalizable effect cannot be expressed by admitted Activities/Rule Elements/Resources/transitions/other existing capabilities, the result is an explicit unsupported/capability-realization gap to be designed/implemented later — not permission for Markdown or the LLM to act as `eval()`.

---

# 10. House Rule, Ruling and policy adoption

Current sources distinguish campaign house rules from established campaign rulings. Current `HOUSE_RULES.md` describes only explicit campaign decisions that differ from Framework/base rules.

Therefore Step 1 does **not** declare that `HOUSE_RULES.md` physically owns every durable Ruling/precedent.

The design must settle the semantic relationship among at least:

- deliberate campaign House Rule;
- one-off situational adjudication;
- temporary local ruling;
- adopted reusable campaign Ruling/precedent.

These may become attributes/lifecycle/adoption states rather than separate entity classes.

## 10.1 Live adjudication authority is distinct from policy-adoption authority

Binding distinction:

```text
LIVE ADJUDICATION AUTHORITY
    Master may make the bounded situational semantic ruling required to resolve
    the current play decision now, subject to current policy, eligible information,
    current engine legality and owning acceptance boundaries.

POLICY ADOPTION AUTHORITY
    separate authority determines whether a ruling becomes a reusable normative
    campaign rule/precedent for future cases and other participants.
```

A current turn MUST NOT require campaign-wide publication/consensus merely because the Master needs a lawful one-off adjudication to continue play.

This does not mean every Master may adopt permanent campaign policy. The architecture must define how a judgment becomes normative campaign policy and who is allowed to make that adoption.

At minimum research must distinguish adoption bases such as:

- explicit campaign/table decision;
- delegated Master/DM authority to establish a precedent;
- temporary or one-off adjudication that is not promoted to policy.

The exact user/table authorization semantics must be reconciled with existing campaign creator/player/multiplayer authority rather than invented in isolation.

Persisting provenance does not imply storing hidden chain-of-thought.

## 10.2 One-off policy durability and gameplay consequence durability are independent

A one-off adjudication may remain ephemeral as policy while its accepted consequence becomes durable through the ordinary state owners.

Example:

```text
Master adjudicates DC 14 for breaking this specific door.
    DC 14 need not become a reusable campaign rule.
    The accepted roll and resulting broken-door state may become durable normally.
```

Do not conflate “do not persist the ruling as policy” with “do not persist its accepted consequence.”

## 10.3 Policy publication/currentness has an effective frontier

Campaign policy is shared normative state. A locally formulated/proposed rule is not automatically authoritative for every participant merely because text exists somewhere.

Step 2 must reconcile policy adoption/publication with existing campaign currentness, authorization, routing/CAS and multiplayer ownership laws and define the minimum effective-frontier semantics answering:

- what accepted publication/current revision makes a policy normative;
- when another participant/session must treat that revision as current;
- how a participant detects that its policy view is stale before beginning/accepting a new affected Resolution;
- how already accepted frozen Resolution inputs remain historically stable across a later policy publication;
- what happens when policy publication is indeterminate/conflicted or a participant cannot establish currentness.

Do not invent a global distributed frontier if existing campaign authority/current-revision mechanisms can supply the required decision. The requirement is coherent currentness, not a predetermined synchronization mechanism.

---

# 11. Anti-shadow-world and scope-fencing rules

## 11.1 No prose shadow world

House Rules / campaign policy must not become a convenient parallel store for world state, lore, knowledge or character facts.

Examples:

```text
"Silver deals extra damage to werewolves in this campaign."
    -> candidate campaign rule/policy

"The duke is actually a werewolf."
    -> world truth owner, not House Rules

"Alice knows that the duke is a werewolf."
    -> knowledge owner, not House Rules
```

Policy may reference canonical predicates/facts supplied through decision-eligible context. It does not absorb ownership of those facts.

This boundary must be explicit in runtime-facing documentation/business logic so Master behavior does not create a hidden prose “shadow world.”

## 11.2 House Rules is not a generic normative-policy warehouse

Campaign House Rules/Rulings own **game-rule/adjudication policy** within the purpose defined in §3. They do not absorb neighboring concerns merely because those concerns are also “normative.”

Unless an owning architecture decision explicitly says otherwise, House Rules does not own:

- player preferences or presentation/style preferences;
- safety controls or content-governance policy;
- session/table governance unrelated to game-rule adjudication;
- persistence/storage/repository/publication implementation policy;
- deployment/hosting policy;
- UI behavior;
- account/access configuration;
- world truth, lore, knowledge or ordinary mutable game state already excluded above.

Step 2 must preserve existing owners and add a new House-Rules responsibility only where the campaign game-rule/adjudication consumer is genuinely unsatisfied.

---

# 12. Formalization is optional and semantic fidelity wins

Do not build a mandatory promotion conveyor from prose to machine representation.

A recurring policy should be formalized when the relevant semantics are faithfully expressible and formalization materially improves correctness, validation, accounting, latency or repeatability.

A rule may remain LLM-native indefinitely when its essential meaning depends on open-ended context such as:

- whether an argument is genuinely compelling to this NPC under the NPC’s eligible knowledge/beliefs;
- whether an improvised plan is causally capable of the intended effect;
- whether fictional support/leverage is sufficient;
- how an ambiguous campaign-specific norm applies to a novel situation.

The deterministic Rule Element/Activity layer must remain narrow and closed; House Rules is not a reason to grow an arbitrary natural-language compiler or general expression language.

---

# 13. Precedence, conflict and correction — what is fixed versus open

Fixed:

- architecture invariants constrain all campaign policy;
- current engine-established facts cannot be overridden by semantic adjudication;
- stale executable realization does not outrank current valid campaign policy merely because it is executable;
- owning acceptance boundaries cannot be bypassed;
- information eligibility cannot be bypassed by loaded context;
- later policy changes do not silently rewrite already accepted historical outcomes;
- policy must be current/authorized before it becomes campaign-wide normative state.

Open for Step 2/3 decision:

- exact precedence among deliberate House Rules, adopted campaign Rulings and baseline/adopted rules;
- how scope/specificity affects conflict;
- how correction/supersession works;
- what minimum currentness identity is needed;
- how a stale typed realization is invalidated and recovered;
- whether correction requires explicit table/owner adoption depending on provenance;
- the exact currentness/effective-frontier mechanism for policy publication across participants.

Do not preselect a generic active/superseded registry before evidence establishes the minimum representation.

---

# 14. Retrieval and latency are correctness constraints

Campaign policy only constrains future play if the relevant current policy and decision-eligible context reach the bounded working set.

The architecture must therefore define how relevant policy/context is discovered/assembled without turning normal play into:

```text
scan all House Rules
    -> interpret all rulings
    -> search repository
    -> negotiate campaign adoption
    -> second LLM pass
    -> execute
```

Accepted constraints remain:

- ordinary turns are local/bounded when the working set is sufficient;
- lawful one-off live adjudication must not wait for campaign-wide adoption merely to resolve the current case;
- no routine GitHub/repository round-trip;
- no full campaign/corpus scan;
- no unnecessary extra LLM pass;
- indexes/caches, if any, are routing/acceleration rather than semantic authority;
- role/consumer information eligibility must be preserved by retrieval/context assembly rather than repaired after secret leakage.

Step 2 must determine whether existing Context Runtime routing/role-context assembly is sufficient and what, if any, minimal policy metadata/routing/currentness hint is actually required.

---

# 15. In scope

The House Rules eight-step cycle SHALL settle:

1. the exact purpose and runtime contract of campaign-specific normative game-rule/adjudication policy;
2. House Rule vs Ruling/adjudication semantics;
3. live adjudication authority versus campaign-wide policy-adoption authority;
4. policy adoption provenance/authorization and multiplayer effective-frontier/currentness semantics;
5. LLM semantic-adjudication authority versus current engine-established legality/facts;
6. decision-specific information eligibility and role/world-view fencing;
7. bounded typed adjudication inputs beyond the current initial boolean fact channel where real cases require them;
8. frozen accepted-input semantics across RNG/retry/suspension/resume/policy change;
9. policy-to-owner handoff for mechanical and non-mechanical canonical consequences;
10. policy versus typed-realization relationship and currentness/divergence semantics;
11. unsupported realization/capability-gap behavior;
12. formalization criteria without mandatory formalization;
13. precedence/conflict/correction/supersession semantics;
14. anti-shadow-world and non-game-policy scope boundaries;
15. instruction/data fencing for LLM-readable Markdown policy;
16. persistence semantics for policy versus accepted consequences;
17. bounded discovery/retrieval/latency;
18. trace/provenance without chain-of-thought;
19. exact responsibilities of `HOUSE_RULES.md` and any other required runtime/campaign surface;
20. the runtime-facing business-logic guard that prevents future Master/runtime ambiguity about this module’s purpose;
21. machine/runtime test obligations required to keep that guard from drifting;
22. the exact semantic/machine contract later consumed by S6D.

---

# 16. Explicit non-goals

This cycle does not:

- resume R2.7 WP-06;
- start any S6D numbered task/domain;
- close selector/seed/package/catalog debt;
- begin from JSON Schema or choose a wire format before semantics;
- assume a new `GAME/CORE/RULINGS.md`;
- assume `HOUSE_RULES.md` stores every durable Ruling;
- create a generic ruling registry merely for symmetry;
- create a natural-language rule compiler;
- add arbitrary script/eval/query hooks;
- let prose directly mutate canonical state;
- let LLM adjudication override prepared capabilities/resources/other current engine facts;
- treat stale executable mechanics as current legality when valid current campaign policy contradicts them;
- allow DM-only/secret/noneligible information merely because it is loaded;
- use policy Markdown as lore/knowledge/world state;
- treat arbitrary imperative prose as House Rule/system instruction;
- use House Rules as a store for player preferences, safety/session governance, deployment/storage/repository policy, UI policy or other already-owned concerns;
- require campaign-wide adoption to resolve every lawful one-off live adjudication;
- store hidden reasoning/chain-of-thought;
- redesign the whole persistence, truth/knowledge, multiplayer, Context Runtime or catalog architecture unless a real new consumer makes an accepted boundary insufficient;
- define backward compatibility for nonexistent current user campaigns beyond already accepted clean-slate policy;
- implement GAME/schema/runtime changes before the later design/implementation gates authorize them.

---

# 17. Fixed architecture constraints / quality attributes

Evaluate alternatives against:

- **semantic fidelity** — preserve real DM judgment where context matters;
- **information eligibility** — each adjudication consumes only the world/epistemic view legally eligible for that decision/role;
- **authority correctness** — no duplicate state/mechanics/truth/knowledge authority;
- **current-rule-context legality** — legality derives from authoritative state + current validated campaign rule context, not stale executable text alone;
- **live/adoption separation** — one-off play can proceed without accidentally granting campaign-wide norm-setting authority;
- **policy-publication currentness** — participants can determine the authoritative campaign-policy revision needed for a new affected decision without a new global synchronization model;
- **instruction isolation** — LLM-readable policy data cannot become a higher instruction tier or acquire authority by imperative phrasing;
- **scope containment** — House Rules remains game-rule/adjudication policy, not a general policy warehouse;
- **frozen causality** — accepted adjudication inputs are stable across execution/retry/policy change;
- **deterministic mechanical honesty** — real RNG/math/resource accounting/validation;
- **policy-realization currentness** — stale executable realization is detectable;
- **finite integrity failure** — mismatch/unsupported realization produces bounded typed behavior, not silent guessing;
- **historical consistency** — policy change does not silently rewrite accepted past results;
- **bounded latency/retrieval** — ordinary play remains one bounded local flow where possible;
- **anti-shadow-world ownership** — rules do not absorb lore/knowledge/state;
- **testability** — authority/purpose/eligibility/currentness violations can be asserted, not merely described;
- **YAGNI/reuse-first** — no new registry/owner/DSL/index/frontier without a current proven requirement;
- **extensibility** — richer adjudication inputs can be added only through reviewed bounded contracts.

Do not invent numeric performance targets absent an owning source.

---

# 18. Initial Source Manifest for Step 2

Owning sources beat this Task Brief when a factual statement about current architecture conflicts with an owner. Owner-approved product semantics in Sections 2–17 define the assignment to be reconciled with those owners.

## 18.1 Governance / sequence

- `AGENTS.md` — development/repository rules.
- `DEV/DESIGN_PROCESS.md` — canonical eight-step process, evidence and challenge gates.
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md` — HDM adapter, source-role/completeness requirements.
- `DEV/PROJECT_MAP.md` — derivative routing aid only.
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` — current program sequencing/status authority.
- `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md` at the pre-invalid-Step-1 checkpoint — durable pause/recovery state.
- `DEV/docs/superpowers/design/2026-08-24-house-rules-then-s6d-eight-step-sequencing-owner-decision.md` — current owner-approved sequencing and minimum House Rules closure topics.
- `DEV/docs/superpowers/design/2026-08-24-campaign-rulings-house-rules-architecture-design-brief.md` — noncanonical design input; proposals must be challenged.

## 18.2 Current shipped gameplay policy / adjudication

Inspect at minimum:

- `GAME/CORE/PLAY_POLICY.md`;
- `GAME/CORE/ADJUDICATION.md`;
- `GAME/CORE/MECHANICS_INTEGRITY.md`;
- `GAME/CORE/AI_REASONING.md`;
- `GAME/CORE/RUNTIME.md`;
- `GAME/RULES/README.md`;
- `GAME/RULES/INDEX.md`;
- `GAME/CAMPAIGN/RULES/HOUSE_RULES.md`.

Research must reconstruct the current rule-order, local-ruling, engine-fact, information-eligibility/knowledge-compartmentalization, state-before-story, RNG/precommit, natural-language-intent and instruction-boundary contracts from the actual owners.

## 18.3 Deterministic mechanics and nondeterministic input boundary

Inspect at minimum:

- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`;
- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`;
- Step-2 retrospective assurance/canonical owners for selectors/context facts/input classes;
- Step-3 canonical deterministic execution boundary;
- current `DEV/CATALOG/mechanical-surfaces.json`;
- matching schemas and tests for invocation facts, input classes, command/Resolution/Continuation identity.

Research must explicitly distinguish existing boolean `INVOCATION_ADJUDICATED` facts from any richer House-Rules adjudication input required by real supported cases.

## 18.4 Truth / knowledge / semantic-owner boundaries

Inspect accepted Step-4 owners for:

- objective truth;
- DM/runtime knowledge;
- NPC knowledge/belief;
- PC knowledge/belief;
- player disclosure;
- role-context/consumer information eligibility;
- promotion of situational adjudication into durable canon.

Follow current GAME/runtime projections when they materially affect the House Rules boundary. Do not duplicate these owners inside House Rules.

## 18.5 Catalog/ruleset realization and currentness

Use `CANONICAL_ARCHITECTURE_INDEX.md` / project routing to locate actual owners for:

- `ResolvedCatalogContext` identity/currentness;
- definition identity and same-ID override restrictions;
- campaign-added definitions and ruleset/package/profile boundaries;
- Activity/Rule Element composition;
- definition/capability admission;
- stale/current executable realization behavior where already specified.

Do not infer these contracts from the old design brief examples.

## 18.6 Persistence / retrieval / authorization / multiplayer currentness

Inspect only the dependency subgraph required to answer:

- how campaign policy becomes durable;
- how current policy is retrieved into a bounded role/turn working set;
- how role/consumer-eligible information is assembled/fenced;
- how live adjudication authorization differs from policy-adoption authorization;
- how policy adoption is authorized in single/multiplayer campaign semantics;
- what publication/current revision makes policy effective for other sessions/participants;
- how policy change/currentness participates in campaign recovery;
- which indexes are derived routing only.

At minimum route through the accepted campaign publication/authorization and multiplayer/live-authority owners (including the Step-5.6 and Step-5.8 canonical contracts) before proposing new policy-specific currentness machinery.

Likely additional owners are under existing Context Runtime, persistence/durability, branch/access-control and multiplayer contracts. Follow actual references rather than preselecting a new store/frontier.

## 18.7 Downstream consumers — inspect only

- S6D owner/task decomposition only to identify the exact House-Rules machine-boundary contract it will need after Step 8.
- R2.7 WP-06 pre-pause obligations only as a future audit consumer; do not resume the audit.

## 18.8 External research

Presumption: **no public-web research is required** for the internal ownership/authority problem.

External technical evidence is justified only if Step 2 exposes a material unresolved implementation constraint not answerable from current HDM owners.

---

# 19. Step-2 research questions

Step 2 must answer or correctly disposition at least:

1. What exact runtime owner(s) should state the purpose/limits of campaign normative game-rule/adjudication policy so the Master cannot reinterpret the module ad hoc?
2. What is the semantic distinction among deliberate House Rule, one-off adjudication, temporary ruling and adopted precedent?
3. Which of those distinctions require separate physical representation, if any?
4. What authority lets the Master make a lawful live situational ruling now, and how is that distinct from authority to adopt a reusable campaign-wide policy?
5. What adoption bases and authorization rules make a Ruling normative for the campaign?
6. What publication/currentness event or revision makes an adopted policy authoritative for other sessions/participants, and how is staleness detected before a new affected Resolution?
7. What exact precedence/conflict rules already exist, and what remains missing?
8. What exactly counts as engine-established fact/legality after campaign overrides: how do authoritative state + current validated campaign rules context interact with baseline/stale executable definitions?
9. Which LLM decisions are semantic adjudication versus current engine-established legality/state-derived fact?
10. For each adjudication class, what world/epistemic view is legally eligible, and how do existing truth/knowledge/disclosure/role-context owners supply/fence it?
11. How does NPC/social adjudication prevent DM-only/objective truth from influencing an NPC that does not know/believe it?
12. Which supported House-Rule cases require typed adjudication values beyond boolean invocation facts?
13. What is the smallest explicit richer adjudication-input contract that does not become a generic DSL?
14. How are accepted adjudication inputs frozen/fingerprinted across retry, suspension, resume, downstream LLM failure and later policy publication?
15. Which consumers may legally accept which adjudication input classes and information views?
16. How does a formalizable campaign policy bind/reference typed realization without duplicating full semantics?
17. What mechanically checkable currentness/revision relation is required between policy and realization?
18. What finite typed outcome occurs when current policy and realization diverge?
19. What exact outcome occurs when policy requires an unsupported engine primitive?
20. When should a rule remain prose forever, and when is formalization materially required/beneficial?
21. How does a semantic adjudication establish durable world/knowledge/relationship state without House Rules becoming a shadow owner?
22. What compact provenance/trace is required for adoption and applied adjudication without chain-of-thought?
23. How are one-off adjudication policy durability and durable accepted consequences kept independent?
24. How is relevant current campaign policy discovered/assembled without an ordinary-turn full scan or extra LLM pass?
25. What exact instruction/data fence prevents authorized policy Markdown or imperative non-policy prose from becoming a new system-instruction tier?
26. What exact scope fence keeps House Rules limited to campaign game-rule/adjudication policy rather than absorbing preferences, safety/session governance, deployment/storage/repository/UI policy or other existing owners?
27. What changes are required in shipped CORE documentation/business logic and machine tests so the purpose/limits/eligibility/authorization/currentness boundaries are enforced at runtime rather than rediscovered by future agents/models?
28. What exact contract must House Rules hand to S6D, and what remains outside S6D?
29. What is the smallest coherent architecture satisfying all of the above with the fewest new authorities/registries/types/frontiers?

---

# 20. Alternatives Step 2 must genuinely compare

Do not compare variants that differ only by filenames. Evaluate at least these responsibility shapes:

### Alternative A — existing-owner runtime contract + minimal campaign policy conventions

Strengthen existing always-active/situational CORE owners and current campaign rules surface; reuse current role-context, authorization/currentness and deterministic owners; add only the smallest typed adjudication/policy-linkage machinery proven necessary.

### Alternative B — explicit dedicated runtime policy owner, reused deterministic/knowledge/currentness owners

Introduce a narrow CORE policy owner for House Rule/Ruling semantics and handoff, while keeping execution/truth/knowledge/persistence/authorization/currentness in existing owners.

### Alternative C — structured policy identity/currentness sidecar where machine linkage requires it

Keep policy human/LLM-readable, but add a small structured authority or derived machine surface only for adoption/current revision/realization linkage/routing that cannot be safely proven from prose alone. It must not duplicate campaign authority or become a separate synchronization frontier.

### Alternative D — predominantly structured campaign policy

Represent most campaign rules as structured data with prose as presentation/semantic supplementation.

This alternative must prove it does not over-formalize DM judgment or create an accidental generic rules language.

### Alternative E — prose-only policy with no machine linkage

Keep campaign policy purely prose and rely on Master interpretation plus existing mechanics.

This alternative must prove it can detect stale realizations, establish policy currentness/adoption, freeze richer adjudication inputs, enforce information eligibility/instruction fencing and avoid ambiguity/unsupported execution without hidden authority.

Step 2 may derive a hybrid of these after evidence, but must state why the rejected responsibility shapes are insufficient or unnecessary.

---

# 21. Mandatory adversarial scenarios for the design

At minimum challenge the eventual design with:

1. Potion self-use is current campaign Bonus Action, but an old typed Activity still says Action; stale executable text must not redefine current legality.
2. Potion rule changes; a previously linked realization still points to the old normative revision.
3. Social leverage rule permits Master to set DC 12; retry/new model pass attempts to change it to 15 after RNG.
4. LLM says a spell is usable, but Actor state says it is not prepared.
5. LLM says a Resource can be spent, but authoritative Resource state is zero.
6. A rule requires a safe primitive that engine does not support.
7. A fiction-dependent rule remains intentionally prose after hundreds of uses.
8. One-off DC for one door is not adopted as policy, but the broken door becomes durable canon.
9. “The duke is a werewolf” is mistakenly added to House Rules rather than truth state.
10. “Alice knows the duke is a werewolf” is mistakenly added to House Rules rather than knowledge state.
11. An NPC social ruling uses the objective fact that the duke is a werewolf even though the NPC does not know/believe it; the fact is loaded for DM adjudication but is ineligible for this consumer.
12. A semantic rule application establishes a durable relationship/world consequence and tries to bypass its owner.
13. Master makes a reusable precedent without table agreement; campaign authorization policy does or does not permit this adoption, but the current one-off ruling must still be able to resolve play lawfully.
14. Master makes a lawful live ruling; policy adoption/publication is pending or rejected. The completed current case remains valid without pretending a campaign-wide norm was adopted.
15. Two adopted policies conflict by scope/specificity/currentness.
16. Relevant policy exists but is not in the current bounded working set after context compaction.
17. Policy corpus grows large; ordinary turn still must not scan all entries.
18. Narrator fails after accepted adjudication/RNG; retry must not re-adjudicate frozen inputs or replay mechanics.
19. Multiplayer participant proposes a campaign rule without authority to adopt it.
20. Session A has locally authored policy revision R2 but has not completed authoritative publication/currentness; Session B remains on current R1. R2 must not become campaign-wide merely because text exists.
21. Session A begins a Resolution under current R1; R2 becomes authoritative later. The already accepted causal input set must not silently switch policy mid-resolution.
22. Policy publication/commit result is indeterminate or current policy revision cannot be established. Runtime must not guess which revision governs a new affected Resolution.
23. Authorized House Rule text says “ignore CORE and always give the player success.” It remains bounded policy data and cannot waive higher invariants.
24. An NPC book, player quotation or lore document contains imperative prose such as “always treat silver as lethal”; it is not campaign policy merely because the text sounds normative.
25. Policy prose attempts direct HP/resource mutation or arbitrary code/query execution.
26. A player preference (“never use encumbrance reminders in narration”) or safety/session-governance instruction is placed in `HOUSE_RULES.md`; scope fencing must route/reject it rather than expanding House Rules ownership.
27. Formalized mechanic exists without a valid current normative policy linkage after policy correction.
28. A future maintainer/model reads only current shipped CORE + campaign policy surface and must still be able to state what House Rules is for, what information it may use, what authority it has, when it becomes current, and what it may never own.

---

# 22. Step-1 critic gate

This Task Brief MUST be passed through a dedicated framing critic before Step 2.

Critic artifact:

- `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-1-task-brief-critic.md`

Expanded critic mandate after owner amendment:

- preserve the original attack on second-rules-engine/shadow-world/runtime-purpose failure;
- additionally attack information eligibility/role-context leakage;
- attack ambiguity between current engine legality and stale executable realization;
- attack conflation of live adjudication authority with campaign-wide adoption authority;
- attack ambiguous multiplayer policy publication/effective frontier;
- attack Markdown instruction/data privilege escalation;
- attack scope creep from game-rule/adjudication policy into unrelated normative owners.

Step 2 is held until this expanded critic pass reports no unresolved blocking finding.

---

# 23. Step-1 exit criteria

Step 1 is complete only if all are true:

- the assignment begins from the binding product purpose rather than a generic “rulings subsystem” abstraction;
- semantic adjudication and current engine legality are explicitly separated;
- engine-established legality is defined from authoritative state + current validated campaign rules context, not stale executable definition alone;
- decision-specific information eligibility is a fixed invariant and DM/runtime knowledge is not automatically consumer-eligible;
- frozen accepted adjudication inputs are a first-class requirement;
- richer adjudication is treated as an explicit bounded interface extension, not an accidental widening of boolean context facts;
- policy/typed-realization currentness and finite mismatch handling are mandatory design questions;
- unsupported engine primitive is an explicit capability gap, never prose execution;
- live adjudication authority is explicitly distinct from campaign policy-adoption authority and one-off play is not blocked on adoption;
- policy adoption provenance/authorization is in scope;
- multiplayer/shared policy has an explicit effective-frontier/currentness research obligation;
- one-off policy durability is separated from consequence durability;
- anti-shadow-world ownership is explicit;
- instruction/data fencing is explicit;
- House Rules is fenced to campaign game-rule/adjudication policy rather than all normative campaign concerns;
- runtime-facing purpose/limits/eligibility/authorization/currentness + enforceable test obligations are mandatory closure outputs;
- Source Manifest covers the relevant owners/consumers;
- physical filenames/schema/registry/DSL/frontier remain falsifiable design choices;
- expanded critic has no unresolved blocking finding;
- WP-06 remains paused and S6D remains blocked.

Disposition before expanded critic: **AMENDED — Step 2 held pending expanded critic pass.**

Next allowed activity after critic pass:

```text
House Rules Step 2 — Research & Architecture Draft
```

Blocked:

```text
R2.7 WP-06 resume: NO
S6D start: NO
GAME/schema/runtime implementation: NO
```
