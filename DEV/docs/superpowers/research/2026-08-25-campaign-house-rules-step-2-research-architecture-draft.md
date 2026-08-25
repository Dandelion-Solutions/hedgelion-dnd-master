# Campaign House Rules — Step 2 Research & Architecture Draft

Status: **STEP 2 COMPLETE / SOURCE MANIFEST COMPLETE / SYNTHESIS COMPLETE / STEP 3 NEXT**

Date: 2026-08-25

Task Brief:

- `DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md`

Owner authorization:

- senior architecture audit verdict: **GO FOR STEP 2–8**;
- Step 1 is closed and is not reopened by this research.

---

## 1. Executive finding

House Rules should be a **campaign-persistent, LLM-interpreted semantic gameplay-policy layer with a lightweight durable identity/lifecycle envelope**, not a second rules engine and not an unstructured catch-all Markdown blob.

The durable policy layer owns the meaning of campaign-specific adjudication policy. It may guide semantic applicability, interpretation, selection of an existing capability and binding of legal typed inputs. It does not own RNG, canonical mechanical state, deterministic acceptance, event commit, truth/knowledge/disclosure, multiplayer authorization, repository currentness or execution semantics.

Recommended flow:

```text
eligible current fiction/state + player intent
    + current published campaign policy candidates
    + adopted baseline rules sources
        -> LLM / Master semantic adjudication
        -> bounded typed adjudication result
        -> existing Activity / Rule Element / deterministic capability
        -> deterministic validation / RNG / mutation / Event
```

When no existing deterministic capability can faithfully realize a mechanically material adopted rule, the result is a finite **CATALOG GAP / POLICY-REALIZATION GAP** at the mechanical boundary. The LLM is not permitted to compensate by mutating state directly.

Recommendation confidence: **HIGH**.

---

# 2. Source Manifest

`SOURCE_MANIFEST_STATUS: COMPLETE`

The manifest is complete for the House-Rules design scope. It distinguishes canonical owners, superseding amendments, current Round-2 owners, gameplay-policy owners, deterministic handoff owners and routing/status evidence.

## 2.1 Required constitutional/context owners

| Source | Status in synthesis | House-Rules relevance |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md` | REQUIRED CANONICAL OWNER | truth/knowledge/disclosure separation; deterministic Context Assembler; role/player/purpose-specific source eligibility |
| `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md` | **REQUIRED CANONICAL AMENDMENT / SUPERSEDES CONFLICTING PHYSICAL-ISOLATION ASSUMPTIONS** | one physical context is permitted; logical role/consumer eligibility remains strict; physical presence never grants eligibility |
| `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md` | **REQUIRED CURRENT CONTEXT-RUNTIME OWNER** | bounded typed discovery/closure/allocation; registered `ContextNeedProfile`; routed currentness; eligibility-before-semantic-use; derived indexes are routing only |
| `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md` | REQUIRED CURRENT EXECUTION/INSTRUCTION OWNER | one physical TurnEnvelope; explicit role rebinding; minimal typed handoffs; data cannot self-promote to engine instruction |
| `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md` | REQUIRED CURRENT MULTIPLAYER CONSUMER OWNER | participant TurnEnvelopes over one canon; join/rejoin must acquire current routing and eligible context before mutable play |

### Context Runtime pre-flight resolution

The exact current owning artifact required by the owner audit is:

- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`.

Its current laws directly cover all three requested cases:

1. **role/consumer information eligibility** — registered consumer/task profile plus eligibility before role-local semantic use (`R2.3-2`, `R2.3-12`);
2. **bounded House-Rules retrieval** — bounded multi-channel discovery, typed closure, no generic graph walk, routing-only indexes (`R2.3-3..9`, `R2.3-18`);
3. **policy-currentness consumption by another session/participant** — routed currentness before material current reliance (`R2.3-11`) combined with R2.5 join/rejoin current-frontier rules and Step-5 publication/currentness owners below.

Repository note: the Round-2 roadmap describes an expected convenience path `DEV/ARCHITECTURE/CONTEXT_RUNTIME.md`, but that path is absent at the researched HEAD. This does **not** leave the semantic owner unresolved: the dated R2.3 canonical specification exists and is the primary owner. The missing convenience path is documentation/index maintenance debt outside this House-Rules authority boundary.

## 2.2 Required publication/recovery/currentness owners

| Source | Status in synthesis | Inherited law |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md` | REQUIRED CANONICAL OWNER | authoritative campaign publication and exact-base CAS; prepared/unpublished material is not current campaign authority |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md` | **REQUIRED CANONICAL OWNER** | current-authority-first recovery; accepted historical/causal inputs remain frozen; no remembered chat/checkpoint appearance outranks current authority |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md` | REQUIRED CANONICAL OWNER | routed multiplayer/live currentness and exact-source CAS; no new global epoch/frontier may be inferred |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md` | INTEGRATED ASSURANCE OWNER | domain-composed current basis and cross-owner recovery/concurrency closure |

House Rules inherits these mechanisms. Research found **no evidence requiring a House-Rules-specific global synchronization or scalar policy frontier**.

## 2.3 Gameplay-policy owners

- `GAME/CORE/PLAY_POLICY.md`
- `GAME/CORE/ADJUDICATION.md`
- `GAME/CORE/MECHANICS_INTEGRITY.md`
- `GAME/RULES/README.md`
- `GAME/CAMPAIGN/RULES/HOUSE_RULES.md`

Established facts:

- campaign house rules and established campaign rulings are consulted before baseline/local rules fallback;
- ordinary adjudication is local-first and must not trigger automatic web lookup;
- a quick ruling may remain temporary;
- a consequential reusable precedent may be deliberately preserved;
- mechanics may be hidden in presentation but cannot be skipped;
- current `HOUSE_RULES.md` is explicitly campaign-local and currently contains no additional rules.

## 2.4 Deterministic handoff owners

- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`
- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`
- current Step-3 execution architecture referenced by the canonical architecture index and R2.7 execution audit.

They establish that mechanically material consequences pass through typed validation/execution and deterministic owner transitions rather than arbitrary prose/script authority.

## 2.5 Authority/routing/status sources

- `AGENTS.md`
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/PROJECT_MAP.md`
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-7-audit-status.md`
- `DEV/docs/superpowers/specs/2026-08-24-house-rules-then-s6d-eight-step-sequencing-owner-decision.md`

These route/status the work; they do not replace owning semantic specifications.

---

# 3. Evidence synthesis

## 3.1 House Rules is policy authority, not execution authority

The gameplay owners already require campaign House Rules/rulings to affect adjudication. The deterministic owners separately require accepted mechanics/RNG/state transitions to pass through typed deterministic execution. These requirements are compatible only if House Rules owns **semantic policy** and produces bounded inputs to existing deterministic capabilities.

Therefore:

```text
House Rule applicability/interpretation
    != mechanical state authority
    != RNG authority
    != execution acceptance
```

A campaign rule may legitimately make the current baseline realization stale, for example by changing when an existing capability is available or which legal parameter is selected. In that case “engine legality” means legality under the **current validated campaign rules context plus current owner state**, not blind privilege for an obsolete baseline definition. But prose still cannot bypass deterministic acceptance. A mismatch is explicit and finite.

## 3.2 House Rule and Ruling are lifecycle meanings, not necessarily separate storage systems

Evidence supports a useful semantic distinction:

- **House Rule** — deliberately adopted forward-looking campaign gameplay/adjudication policy;
- **Ruling** — a reusable precedent retained from a concrete adjudication.

Once authoritatively adopted and published, both participate in the campaign policy layer. A one-off live ruling is neither automatically durable nor automatically campaign-wide.

No evidence requires separate repositories, databases or universal record classes for the two kinds.

## 3.3 Live adjudication authority and policy-adoption authority must remain separate

A Master may need to make a lawful bounded local ruling immediately so play can continue. That authority cannot be blocked on campaign-wide policy publication.

Conversely, the ability to resolve the current scene does not automatically grant authority to publish a persistent shared norm. Durable adoption must pass the existing applicable campaign authorization and publication path.

Therefore the architecture must represent this distinction even if the first implementation uses the same human-facing file for durable policy.

## 3.4 Decision-specific information eligibility is deny-by-default

House Rules does not gain a parallel knowledge model. Its semantic decision receives only information allowed by existing Step-4/R2.3 role, subject, player and purpose contracts.

Minimum rule:

```text
candidate source physically present
    does NOT imply
source admissible to this adjudication consumer
```

The policy text itself is campaign game-policy data. If an example, counterexample or applicability note embeds material whose use would violate an existing secrecy/knowledge owner, that material must not be used merely because it appears in an admitted policy artifact. House Rules must reference or consume canonical eligible facts rather than becoming their owner.

## 3.5 Instruction/data fencing is already architecturally supported

R2.4 states that player text, campaign records, Story, Actor dialogue, tool output and retrieved text are data/evidence under their source contracts, and instruction-like prose inside data cannot self-promote to engine instruction.

House Rules therefore does not need a new prompt-security hierarchy. It needs an admission contract:

- an authorized policy entry is normative **campaign game-policy data**;
- its authority comes from admitted policy identity/publication, not imperative syntax;
- it remains below host/project/engine constitutional invariants;
- quoted text/examples/source excerpts inside it do not automatically become policy commands.

## 3.6 Bounded discovery should reuse R2.3

R2.3 already provides the exact shape needed: registered consumer/task profile, finite discovery channels, typed bounded closure, routed currentness, eligibility, representation floors and routing-only indexes.

House Rules should therefore register a policy-candidate need rather than introduce a second retrieval system.

Conceptually:

```text
adjudication need/domain
    -> derived routing candidates
    -> current publication/lifecycle resolution
    -> role/consumer eligibility
    -> bounded policy packet
    -> LLM semantic applicability
```

The authoritative policy source is not scanned wholesale on every ordinary turn. A derived index/cache may accelerate discovery but is never policy authority.

## 3.7 Multiplayer propagation is publication + current context assembly

No policy prose is “copied into another player chat” as an authority mechanism.

A newly affected Resolution in any participant session must consume a context assembled from the **current authoritative published campaign policy basis**. If the relevant policy source becomes stale between assembly and acceptance, the attempt cannot silently commit under the stale basis; it must fail/reassemble according to existing currentness/retry laws.

A joining/rejoining/new session must acquire current routing/policy basis and eligible context before its first affected mutable Resolution.

Already accepted/frozen Resolution inputs remain historically stable after a later policy publication. Recovery resumes from those accepted causal inputs rather than retroactively applying the new policy to old accepted work.

## 3.8 No global House-Rules frontier

Step-5.7/5.8 and the integrated architecture explicitly reject implicit universal scalar frontiers across independently owned domains. A House-Rules-specific global epoch would duplicate accepted authority and create false cross-domain ordering.

Policy currentness should be represented through the existing exact current campaign publication/source basis required by the relevant consumer, plus any native owner bases already required by the Resolution. It is a component of a domain-composed basis, not a universal world version.

## 3.9 Lightweight semantic identity is required

Pure unstructured prose with no durable identity/revision relation is insufficient because the architecture must support:

- durable precedent identity;
- explicit active/superseded/retired lifecycle;
- conflict detection;
- bounded retrieval;
- provenance/adoption authority;
- frozen accepted input references;
- stale policy detection and historical audit.

This does not imply JSON or an executable DSL. The minimum contract can remain human/LLM-readable Markdown with machine-readable identity/lifecycle metadata or an equivalent semantic envelope decided during implementation.

## 3.10 Promotion remains optional

The evidence supports the owner’s promotion ladder:

```text
one-off adjudication
    -> durable campaign ruling / House Rule
    -> structured campaign mechanic
    -> generalized engine/core capability
```

Promotion happens only when the semantic rule is sufficiently stable/formalizable and the benefit justifies structured realization. Fundamentally contextual policy may remain prose permanently.

---

# 4. Alternatives

## Alternative A — One unstructured House-Rules Markdown corpus

**Strengths**
- minimal authoring burden;
- maximally LLM-readable.

**Rejected as complete architecture because**
- no stable identity/currentness for frozen inputs;
- weak bounded retrieval and supersession/conflict handling;
- difficult to distinguish admitted policy from examples/quoted text;
- encourages whole-corpus scans.

Human-readable Markdown remains a valid presentation/storage surface, but not without a lightweight semantic envelope.

## Alternative B — Executable House-Rules DSL / natural-language compiler

**Rejected.**

It would turn semantic DM judgment into another rule engine, duplicate Activity/Rule Element responsibilities, create a second mechanical authority and force poorly formalizable criteria into brittle predicates. It directly contradicts the product purpose.

## Alternative C — Lightweight semantic policy envelope + existing deterministic/runtime mechanisms

**Recommended.**

Characteristics:

- durable stable policy identity;
- semantic `house_rule` / `ruling` kind;
- active/superseded/retired lifecycle;
- applicability/domain/scope material for bounded discovery;
- normative LLM-readable policy text;
- adoption/provenance/current publication basis;
- explicit supersession/conflict relation when needed;
- optional examples/counterexamples and deterministic capability references as hints, never authority;
- R2.3 bounded eligible context projection;
- R2.4 instruction/data fencing and typed role gateway;
- Step-5.6/5.7/5.8 publication/recovery/currentness;
- existing Activity/Rule Element/deterministic execution.

No new global frontier, rule compiler, truth store or state mutation channel is introduced.

---

# 5. Candidate architecture requirements derived from research

1. **Semantic policy only.** House Rules owns campaign game-rule/adjudication meaning, not canonical state or deterministic execution.
2. **Constitutional precedence.** Engine architecture invariants constrain every policy entry.
3. **Explicit durable identity.** Durable policy needs stable identity and revision/current publication reference sufficient for recovery/audit.
4. **Two semantic kinds.** House Rule and Ruling are distinguished by adoption origin/lifecycle meaning; separate physical stores are not required.
5. **Ephemeral ruling is legal.** A lawful one-off adjudication can resolve current play without campaign-policy adoption.
6. **Adoption is explicit and authorized.** Persistence as shared policy requires existing campaign authorization/publication semantics.
7. **Deny-by-default information eligibility.** Policy adjudication consumes only information admitted to the specific role/consumer/purpose.
8. **Policy data is not engine instruction.** Admission/publication gives scoped gameplay-policy authority; imperative syntax does not.
9. **Bounded retrieval uses R2.3.** No ordinary-turn full-corpus scan and no generic House-Rules graph.
10. **Currentness uses inherited mechanisms.** No House-Rules-specific global synchronization/frontier.
11. **New affected Resolution uses current policy.** Stale context before acceptance fails/reassembles.
12. **Accepted historical inputs stay frozen.** Later policy does not rewrite already accepted Resolution inputs on retry/recovery.
13. **Typed deterministic handoff only.** Semantic adjudication may select/bind existing capabilities or remain narrative; it cannot mutate engine-owned state.
14. **Missing realization is finite.** Mechanically material mismatch becomes `CATALOG GAP / POLICY-REALIZATION GAP`, not arbitrary prose execution.
15. **Conflict is explicit.** Same-precedence active conflicts cannot be silently resolved into durable campaign meaning by model preference.
16. **Promotion is optional.** Formalizable high-frequency policy may move to structured mechanics; semantic policy may remain prose indefinitely.
17. **Index/cache is derived.** It can route candidates but cannot define policy authority or prove absence unless an explicit exhaustive owner contract exists.
18. **Multiplayer propagation is authoritative publication/currentness, not chat copying.**
19. **Scope fence.** House Rules excludes truth/lore/history, player preference/safety/session governance, engine config, prompts, storage/repository/UI policy and data already owned by structured mechanics.
20. **Ordinary-turn latency stays bounded/local.** No new network/repository round trip or extra LLM pass is required solely because House Rules exists when the current working set already contains the needed current policy projection.

---

# 6. Evidence gaps and dispositions

## EG-1 — Convenience Context Runtime architecture path is absent

`DEV/ARCHITECTURE/CONTEXT_RUNTIME.md` is named in Round-2 planning material but absent at the researched HEAD.

**Disposition:** nonblocking documentation/index maintenance debt. The exact semantic owner exists at `2026-08-24-r2-3-context-runtime-canonical-spec.md`; House Rules consumes that owner directly.

## EG-2 — Exact future machine schema for campaign policy entries does not exist

**Disposition:** intentionally deferred. Step 1 forbids schema-first design. Step 5 should specify semantic fields/invariants and implementation acceptance obligations without freezing JSON/YAML syntax prematurely.

## EG-3 — Exact campaign policy-adoption UI/workflow is not fixed

**Disposition:** not an architecture blocker. The contract requires explicit authorized adoption/publication and permits current implementation to remain simple. UI/workflow belongs to later machine realization/implementation.

No unresolved evidence gap changes the recommended semantic architecture.

---

# 7. Step-2 completion gate

- Required Source Manifest entries present: **PASS**.
- Step-4 superseding amendment explicitly included: **PASS**.
- Step-5.7 explicitly included as required canonical owner: **PASS**.
- Exact Context Runtime/context-assembly owners resolved: **PASS**.
- Evidence extracted at item level for authority, eligibility, currentness, recovery, multiplayer, deterministic handoff, retrieval, conflict and promotion: **PASS**.
- No House-Rules-specific global synchronization mechanism assumed: **PASS**.
- Alternatives preserve ability to reject schema/DSL/second-engine designs: **PASS**.
- Synthesis completeness sufficient for a Decision Brief: **PASS**.

`STEP_2_RESULT: COMPLETE`

Next: **Step 3 — Decision Brief**.
