# Campaign House Rules — Step 1 Task-Brief Critic

Status: **CRITIC PASS COMPLETE / ALL BLOCKING FINDINGS RESOLVED IN REWRITTEN TASK BRIEF**

Date: 2026-08-25

Reviewed artifact:

- `DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md`

Critic mandate:

> Attack the Task Brief specifically for the failure mode that triggered this rework: future architects, maintainers or runtime LLM behavior must not need to rediscover from conversation history what House Rules is for, what authority it has, what it may never own, or how it crosses into deterministic/canonical execution.

This is a **Step-1 framing critique**, not Step 6 of the eight-step House Rules design cycle. It validates the assignment before Step 2 research; it does not pre-approve a candidate architecture.

---

# 1. Critic standard

The brief fails if a competent investigator could follow it faithfully and still produce a persuasive architecture in which any of the following remain ambiguous:

- House Rules becomes a generic rulings registry/subsystem rather than campaign normative policy;
- LLM semantic judgment and engine legality are conflated;
- accepted DC/applicability/classification can drift after RNG or retry;
- richer adjudication values are smuggled through the current boolean context-fact channel;
- policy prose can directly mutate state or invent executable primitives;
- typed realization silently wins over normative policy, or vice versa;
- world truth/knowledge/lore is stored as “rules” because Markdown is convenient;
- one-off ruling persistence is confused with persistence of its accepted consequence;
- a future runtime model has no explicit shipped contract telling it what House Rules means;
- the eventual design documents the boundary but leaves no enforceable runtime/machine realization obligation.

---

# 2. Findings and resolutions

## CRIT-01 — BLOCKING — Purpose could remain DEV-only

**Attack:** A design can be semantically correct in DEV documentation while runtime `CORE` remains vague. A future model/runtime could again infer House Rules as arbitrary campaign notes or direct mechanical authority.

**Required correction:** Make runtime-facing purpose/limits an explicit closure requirement. The design must identify the shipped owner(s) and later enforceable tests/machine guards.

**Resolution in Task Brief:** Sections 3–4 and 15–17 make the runtime purpose/guard a binding output rather than an implementation afterthought.

**Disposition:** RESOLVED.

---

## CRIT-02 — BLOCKING — “LLM adjudication authority” could override engine legality

**Attack:** Saying the LLM chooses feasibility/capability/DC is too broad if it permits overriding prepared spell state, Resource state, ownership or other established facts.

**Required correction:** Separate fiction-dependent semantic adjudication from engine-established legality/state-derived facts.

**Resolution:** Section 5.4 adds the binding law that LLM may supply missing semantic inputs but may not override established engine-owned facts.

**Disposition:** RESOLVED.

---

## CRIT-03 — BLOCKING — Accepted adjudication inputs could float

**Attack:** A correct DC before one model pass can become a different DC after retry, Narrator failure, suspension or seeing the die. That destroys causal reproducibility and fairness.

**Required correction:** Treat accepted adjudication values as frozen causal inputs for the concrete execution generation.

**Resolution:** Section 6 makes freezing across retry/suspension/resume/model passes/RNG observation mandatory and connects it to existing Step-3 invocation-fact discipline.

**Disposition:** RESOLVED.

---

## CRIT-04 — BLOCKING — Current boolean context-fact channel could be silently generalized

**Attack:** The current Step-2 contract deliberately limits `INVOCATION_ADJUDICATED` facts to registered booleans. Reusing that namespace for arbitrary DCs/enums/objects would erase the prior safety boundary without explicit design.

**Required correction:** State that richer House-Rules adjudication is an explicit nondeterministic-interface extension requiring its own bounded typed contract/admission semantics.

**Resolution:** Section 7 explicitly forbids accidental overloading and requires reviewed typed value/provenance/consumer/freeze semantics.

**Disposition:** RESOLVED.

---

## CRIT-05 — BLOCKING — Normative policy versus executable realization had no operational conflict behavior

**Attack:** “Mismatch is an integrity defect” is descriptive, not operational. Runtime still needs a finite action when Markdown says Bonus Action and typed Activity says Action.

**Required correction:** Require a bounded typed mismatch state/outcome; never silently choose prose or executable definition.

**Resolution:** Section 9.3 requires finite typed integrity behavior and stopping at the affected mechanical boundary when no faithful admitted realization exists.

**Disposition:** RESOLVED.

---

## CRIT-06 — BLOCKING — Policy could become an implicit executable language

**Attack:** If prose can declare a mechanical effect for which the engine lacks a safe primitive, a naive runtime may “implement” it directly by editing state.

**Required correction:** Unsupported primitive must be an explicit capability/realization gap.

**Resolution:** Section 9.4 makes lack of an admitted primitive a hard gap, never permission for prose/LLM `eval()`.

**Disposition:** RESOLVED.

---

## CRIT-07 — SIGNIFICANT — Adoption authority/provenance was underspecified

**Attack:** An in-play Master ruling and a table-approved campaign policy are not necessarily equivalent. Multiplayer/player authority may constrain who can make a precedent normative.

**Required correction:** Design adoption bases and authorization without necessarily creating separate record classes.

**Resolution:** Section 10.1 requires explicit campaign/table decision, delegated Master authority and temporary one-off adjudication to be reconciled with existing access/multiplayer authority.

**Disposition:** RESOLVED FOR STEP 1; Step 2 evidence required.

---

## CRIT-08 — BLOCKING — Verifiable policy/realization linkage impossible without currentness semantics

**Attack:** A “linked realization” cannot be checked after policy change unless the architecture can identify which normative revision it implements.

**Required correction:** Make policy identity/current revision/supersession/invalidation a requirement where typed realization claims correspondence, without preselecting a universal ID schema.

**Resolution:** Section 9.2 makes mechanically checkable currentness mandatory while leaving representation open.

**Disposition:** RESOLVED.

---

## CRIT-09 — SIGNIFICANT — “Do not persist one-off ruling” could be misread as “do not persist outcome”

**Attack:** Ephemeral DC/rationale and durable broken-door/Resource/knowledge consequences have different owners/lifetimes.

**Required correction:** Explicitly separate policy durability from accepted consequence durability.

**Resolution:** Section 10.2 makes the dimensions independent.

**Disposition:** RESOLVED.

---

## CRIT-10 — BLOCKING — House Rules could become a prose shadow world

**Attack:** “The duke is a werewolf” or “Alice knows X” can be stored in House Rules because prose is convenient, bypassing truth/knowledge ownership.

**Required correction:** Add anti-shadow-world law and require policy to reference canonical facts rather than own them.

**Resolution:** Section 11 establishes explicit examples and requires runtime-facing enforcement/documentation.

**Disposition:** RESOLVED.

---

## CRIT-11 — BLOCKING — “Primarily semantic” outcome could bypass canonical owner acceptance

**Attack:** A no-roll semantic judgment can still establish world truth, knowledge or relationship state. Calling it “non-mechanical” must not grant direct canon authority.

**Required correction:** Generalize acceptance-boundary law beyond mechanics.

**Resolution:** Sections 5.5 and 8.3 require every durable result to cross the appropriate owner.

**Disposition:** RESOLVED.

---

## CRIT-12 — SIGNIFICANT — Formalizable and LLM-native rules could become a mandatory promotion lifecycle

**Attack:** A design might treat prose as temporary debt and force every repeated semantic norm into structured mechanics.

**Required correction:** Formalization remains optional and driven by semantic fidelity/correctness benefit.

**Resolution:** Section 12 explicitly rejects a mandatory conveyor.

**Disposition:** RESOLVED.

---

## CRIT-13 — SIGNIFICANT — New subsystem bias could reappear through requirements language

**Attack:** Stable IDs, registries, indexes, `RULINGS.md`, lifecycle objects and schemas can become self-fulfilling requirements.

**Required correction:** Requirements should name responsibilities/currentness/failure behavior, not preselect physical artifacts.

**Resolution:** Sections 9, 10, 16, 18–20 retain these as falsifiable alternatives/questions and apply YAGNI/reuse-first.

**Disposition:** RESOLVED.

---

## CRIT-14 — SIGNIFICANT — Retrieval consistency could add ordinary-turn bureaucracy

**Attack:** Persisted policy that requires a full scan/repository search/second LLM call each turn defeats the local-first gameplay invariant.

**Required correction:** Retrieval is part of correctness but must remain bounded/targeted and should reuse Context Runtime where possible.

**Resolution:** Section 14 and Source Manifest §18.6 make bounded discovery a quality/invariant question rather than an excuse for a generic global index.

**Disposition:** RESOLVED.

---

## CRIT-15 — BLOCKING — Runtime-purpose requirement was not testable

**Attack:** “Document the purpose clearly” can regress silently. The same ambiguity could return after future edits.

**Required correction:** Step-8 architecture must carry exact runtime realization/test obligations for mechanically enforceable boundaries and explicit owner/delegation for semantic ones.

**Resolution:** Sections 4, 15, 17 and research question 20 require runtime owner designation plus machine/runtime tests or equivalent enforceable checks.

**Disposition:** RESOLVED.

---

# 3. Counterexample challenge

The rewritten brief was checked against the framing question:

> If this Task Brief is followed by a competent investigator who has never seen the current conversation, can they still accidentally design House Rules as a second rules engine, a lore store, a mutable prose state owner, or a vague Markdown note layer whose semantics runtime must rediscover?

After the corrections above: **not without violating an explicit requirement in the Task Brief.**

The physical solution remains open. The purpose/authority boundary does not.

---

# 4. Critic verdict

**PASS WITH ALL BLOCKING FINDINGS RESOLVED.**

Step 2 may proceed.

Step 2 must still test the physical ownership/representation alternatives and may reject proposed files/types/indexes. It may not reopen the binding product purpose and authority laws without an explicit new owner decision.
