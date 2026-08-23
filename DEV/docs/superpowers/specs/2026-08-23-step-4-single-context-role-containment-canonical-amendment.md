# Step 4 Canonical Amendment — Single-Context Logical Role Containment

Status: **CANONICAL ARCHITECTURE AMENDMENT — OWNER APPROVED**

Date: 2026-08-23

Amends:

- `2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`

Evidence inputs:

- `../research/2026-08-23-role-context-validation-protocol-1-sequential-containment.md`
- `../research/2026-08-23-role-context-validation-protocol-2-collapsed-multi-role.md`
- `../research/2026-08-23-role-context-validation-protocol-3-reasoning-budget.md`

This amendment records an owner-approved architectural correction after the Step-4 canonical specification was originally closed. It supersedes conflicting physical-isolation wording in the base Step-4 specification while preserving its semantic ownership, knowledge, disclosure, Story and deterministic-authority model.

---

# 1. Superseding invariant

HDM SHALL support a baseline gameplay execution model in which **one LLM operates inside one physical conversational context and, within one user request / assistant turn, sequentially performs multiple logical HDM roles with different knowledge and authority boundaries**.

Physical availability of information to the model does **not** make that information logically eligible for the currently active role.

Before every logical role phase, the LLM SHALL rebind to that role's information, authority and output contract. Material that is physically present elsewhere in the shared context remains unusable by the active role unless it is independently eligible for that role, lawfully observed or disclosed to that role's subject, or transferred through an explicitly permitted handoff.

The baseline ordinary gameplay topology therefore permits, as required by the current turn:

```text
Player input
    -> Interpreter
    -> Dramaturg
    -> Actor[subject_1]
    -> Actor[subject_2]
    -> ...
    -> deterministic/core interaction where required
    -> Narrator
    -> player-facing response
```

inside one physical chat context and one user-request/assistant-turn execution.

Logical role boundaries remain strict even when physical context is shared.

---

# 2. Logical eligibility is distinct from physical visibility

HDM SHALL distinguish at least:

```text
physical context
    material technically available to the model in the current conversation/turn

logical role context
    material the active logical role is permitted to use

typed handoff
    an explicitly allowed result transferred across logical role boundaries

observable in-fiction transfer
    speech, action, evidence or disclosure that lawfully changes what a later role/subject may use

canonical authority
    state accepted by the deterministic owning subsystem as durable/current truth
```

The following implication is forbidden:

```text
material is physically present
    => active role may use it
```

Examples:

```text
Dramaturg knows hidden fact X
    != Actor automatically knows X

Actor[NPC_A] has private belief Y
    != Actor[NPC_B] automatically inherits Y

private Actor reasoning is physically present
    != Narrator may expose it to the player
```

A later role may use material from an earlier role only when the material crosses a legitimate semantic boundary: independent eligibility, observable in-fiction evidence, player/subject disclosure, or an explicit permitted handoff.

---

# 3. Role rebinding is a runtime correctness requirement

Before each logical role phase, the LLM SHALL conceptually rebind to:

- the active logical role;
- active subject/player identity where applicable;
- role-local knowledge and belief state;
- permitted observations and disclosure state;
- allowed authoritative inputs;
- allowed prior-role results;
- the role's authority limits;
- the role's output contract.

Role rebinding is not a cosmetic change of persona. It is part of HDM correctness semantics.

The engine and shipped reasoning instructions SHALL make the boundary explicit enough that the same physical model can execute several incompatible logical roles without treating shared physical context as shared fictional knowledge or shared authority.

---

# 4. Shipped instruction layer is part of role-containment machinery

The system prompt, Project Instructions and shipped HDM Markdown reasoning/runtime instructions are not merely generic behavioral guidance. Together they form part of the runtime **role-containment machinery**.

They SHALL encode and reinforce at least:

1. **role rebinding** before every logical phase;
2. explicit separation of **objective truth, fictional cognition, observable evidence and human disclosure**;
3. prohibition of **transitive knowledge inheritance** merely because another role or subject had access to information;
4. **Actor-specific epistemics**, including subject-local knowledge, beliefs, suspicions, goals, relationships and private plans;
5. **Dramaturg latent state** as private/provisional preparation rather than automatically established world truth;
6. **Narrator disclosure boundaries**, so player-facing prose uses only player-eligible/observable/settled material;
7. the **creativity -> commit boundary**, under which generated invention, narration, intention or preparation does not become persistent canonical state without the appropriate authoritative acceptance path;
8. preservation of player agency and the distinction between information made available to a PC/player and voluntary interpretation, belief or emotion;
9. separation between logical role handoffs and calls into deterministic authority/tooling.

These instructions are therefore part of the shipped runtime correctness surface and SHALL be versioned, reviewed and tested accordingly.

They do not themselves become canonical-state authority. Deterministic owners remain responsible for validation, accepted mechanics, durable mutations and persistence.

---

# 5. Context Assembler semantics under shared physical execution

The deterministic Context Assembler continues to own role/source eligibility and bounded source selection.

A `RoleContextBundle` is a **logical execution projection** for one role phase. It is not required to be the complete physical model context of a separate invocation.

Several independently assembled logical role bundles MAY participate in one shared physical turn envelope.

The Context Assembler SHALL still determine, per logical phase:

- which authoritative/derived sources are eligible;
- which subject/player identity governs eligibility;
- which prior-role outputs are permitted;
- which evidence is excluded from role use;
- source/revision provenance needed for validation and diagnostics.

Physical co-presence of another role's bundle does not change these decisions.

---

# 6. No transitive raw-role inheritance

The base Step-4 rule against transitive context inheritance remains semantically valid but is clarified as follows.

A logical role SHALL NOT treat another role's raw frame or private source set as its own eligible evidence merely because both are physically present in the same conversation or turn envelope.

Allowed:

```text
Dramaturg frame
    -> Dramaturg preparation/result
    -> explicitly allowed cue/handoff
    -> Narrator logical frame
```

Allowed:

```text
Actor[NPC_A] public utterance
    -> observable scene evidence
    -> Actor[NPC_B] may react to that utterance
```

Forbidden:

```text
Dramaturg hidden source
    -> physical co-presence
    -> Actor/Narrator uses hidden source directly
```

Forbidden:

```text
Actor[NPC_A] private cognition
    -> physical co-presence
    -> Actor[NPC_B] inherits private cognition
```

---

# 7. Role-specific consequences

## 7.1 Interpreter

Interpreter may physically coexist with broader campaign material in the shared turn envelope, but its logical interpretation phase SHALL use only Interpreter-eligible sources. Unrestricted private world truth does not become valid interpretation evidence merely because it is physically visible to the model.

## 7.2 Dramaturg

Dramaturg may use its broader eligible preparation/truth frame and may generate latent complications, motives, branches and possibilities. Such material remains provisional unless later established through an authoritative path.

## 7.3 Actor

Each `Actor[subject]` phase SHALL bind to that subject's own cognition, goals, relationships, capabilities, observations and eligible scene evidence.

Multiple Actors MAY execute sequentially within one assistant turn and one physical context while retaining distinct knowledge/belief sets.

A public utterance/action by an earlier Actor may become observable evidence for a later Actor. Private frame material does not transfer unless a legitimate in-fiction or typed handoff path exists.

## 7.4 Narrator

Narrator may execute in the same physical context that also contains broader Dramaturg or Actor-private material.

That material remains logically ineligible to Narrator unless independently player-eligible or explicitly transformed through an allowed, validated handoff.

Narrator SHALL preserve the existing disclosure boundary and SHALL NOT expose hidden Dramaturg material, private Actor cognition, unsupported objective truth, or uncommitted persistent state merely because the model can physically see it.

## 7.5 Chronicler and Commentator

This amendment does not require Chronicler or Commentator to share the ordinary gameplay physical invocation. Their later physical placement remains a deployment/roadmap decision, while their existing logical authority and information contracts remain in force.

---

# 8. Creativity does not imply authority

Single-context execution deliberately permits substantial generative initiative. The relevant correctness boundary is authority, not absence of invention.

The runtime SHALL distinguish at least these authority levels conceptually:

```text
ephemeral flavor
local scene action
Dramaturg latent invention
persistent fictional cognition
persistent canonical state
```

Generated material may remain transient when no future continuity depends on it.

Generated material that must affect future turns SHALL cross the appropriate typed/authoritative persistence boundary.

Persistent fictional cognition remains distinct from objective world truth.

Persistent canonical state requires acceptance by the owning authoritative subsystem.

The governing rule is:

```text
invented != canonical
```

---

# 9. Physical separation becomes optional deployment defense

The base Step-4 requirement that incompatible logical roles must use separate physical invocations or a genuine context reset is **superseded**.

HDM SHALL NOT make separate chats, agents, processes, model calls or physically isolated contexts a baseline semantic requirement for Interpreter, Dramaturg, Actor(s) and Narrator.

A future deployment profile MAY use physical separation as:

- defense in depth;
- compatibility fallback for a model/host that fails role-containment validation;
- latency/quality optimization where justified;
- provider-specific implementation detail.

Such separation must not change campaign semantics, persistence formats or logical authority contracts.

---

# 10. Superseded wording in the base Step-4 specification

This amendment has later canonical authority over conflicting wording in `2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`.

In particular, it supersedes the physical-topology interpretation of:

- §9.5 where "raw-context inheritance" could be read as requiring physical absence rather than prohibiting logical use;
- §9.6 `Physical context compatibility rule` in full;
- role-contract wording that says a role physically "does not receive" another role's private material when the actual invariant is logical ineligibility/use;
- §11 wording that implies each role bundle necessarily requires an independent physical receiving invocation;
- §26 wording that treats physical exclusion as the primary generative-containment mechanism;
- §28 Step-6 handoff items that make context reset/isolation or minimum physical call separation a required semantic consequence of Step 4.

The following base Step-4 architecture remains intact unless separately superseded:

- objective/current world ownership;
- `world.lore_fact` truth semantics;
- `world.knowledge` fictional epistemics;
- `runtime.disclosure` human exposure semantics;
- deterministic Context Assembler ownership of eligibility;
- logical role responsibility/authority contracts;
- typed handoff concept;
- Story non-authority;
- promotion/commit boundaries;
- deterministic validation and canonical-state ownership.

---

# 11. Round-2 handoff

This amendment is a baseline input to the second HDM architecture round.

Round 2 SHALL use the accepted Steps 1–5 architecture as a strong base together with:

- completed role-containment validation evidence;
- current platform/deployment feasibility research;
- the external architecture idea dossier;
- useful unresolved questions preserved from the previous Step-6 framing;
- any later evidence accepted through the normal architecture process.

The previous Step-6 decomposition is not binding on Round 2. A new roadmap SHALL be derived from the actual current problem structure, dependencies and evidence rather than preserving the old six-step sequence by inertia.

No broad implementation is authorized by this amendment.