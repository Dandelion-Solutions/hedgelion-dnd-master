# Round 1 Step 6 Closure and Round 2 Rebaseline — Owner Decision

Status: **OWNER-APPROVED ARCHITECTURE PROGRAM DECISION**

Date: 2026-08-23

Applies to:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- the former Round-1 Step-6 working/research artifacts;
- the second HDM architecture round.

This decision changes architecture-program sequencing. It does not by itself implement runtime code, schemas, catalogs, prompts or tooling.

---

# 1. Round 1 Step 6 is closed as a separate stage

The former Step 6 is **CLOSED AS A SEPARATE ROADMAP STAGE / NOT EXECUTED AS ORIGINALLY DECOMPOSED**.

Its remaining useful questions are reallocated into Architecture Round 2.

This closure does **not** assert that the old Step-6 exit criteria were completed. The stage is being retired because its original decomposition no longer matches the accepted problem structure after subsequent research, experiments and owner decisions.

Round 1 therefore closes with:

```text
Steps 1-3   COMPLETE / ASSURED
Step 4      COMPLETE / ARCHITECTURE CLOSED
             + later single-context role-containment canonical amendment
Step 5      COMPLETE / ARCHITECTURE CLOSED
Step 6      CLOSED AS SEPARATE STAGE / SCOPE REALLOCATED TO ROUND 2
```

---

# 2. Why the original Step-6 decomposition is retired

The old Step-6 frame was materially organized around mandatory physical role isolation, genuine context reset/isolation and derivation of a minimum separate physical invocation topology.

Completed role-containment validation and the owner-approved Step-4 amendment supersede that premise for the baseline HDM gameplay profile.

The accepted baseline is now:

> HDM uses one LLM in one physical conversational context and, within one user request / assistant turn, sequentially performs multiple logical roles with different knowledge and authority boundaries. Physical availability of information does not automatically make that information eligible for the active logical role.

Consequently the following former Step-6 concerns are **retired as baseline architecture requirements**:

- mandatory separate chats/agents/processes/model calls for incompatible logical roles;
- genuine physical context reset as the ordinary role-containment mechanism;
- minimum physical invocation count derived from role secrecy;
- physical absence of ineligible information as the definition of correct role containment.

Physical separation may remain an optional future deployment mechanism or compatibility fallback, but it does not define the baseline logical architecture.

---

# 3. Useful former Step-6 work is preserved as Round-2 input

Closing Step 6 does not discard its evidence or useful unresolved questions.

Round 2 may reuse, revise, split or reject material concerning:

- single-context role activation and sequencing;
- typed nondeterministic results and lifecycle boundaries;
- Context Assembler physical realization, long-chat boundedness, retrieval and context budgets;
- latency and failure/degradation behavior;
- prompt/instruction packaging and versioning;
- prompt-injection and role-confusion defenses;
- ChatGPT-host limitations that materially affect correctness or UX;
- Narrator/player-visible emission constraints where they remain relevant after the single-context decision;
- host interaction/retry identity where existing Step-3/5 semantics require concrete support;
- Chronicler/Commentator execution policy where not already closed;
- catalog/schema/seed/runtime-document realization gaps;
- final holistic architecture review and implementation-obligation consolidation.

Former Step-6 research and working notes remain non-normative evidence/history. They do not keep their old sequencing authority.

---

# 4. Round-2 baseline product surface

The current Round-2 baseline is deliberately narrow:

```text
primary host               ChatGPT
plan                        ChatGPT Plus
player experience           ordinary public chat
physical LLM topology       one LLM / one physical chat context
ordinary turn               one user request / one assistant turn
private HDM hosting         OUT OF CURRENT SCOPE
direct model API calls      OUT OF CURRENT SCOPE
mandatory paid inference    OUT OF CURRENT SCOPE
possible future Claude move compatibility consideration only
```

A future migration to another consumer AI host may be considered later if material value justifies it. Round 2 SHALL NOT build a provider-abstraction subsystem merely because migration is imaginable.

Provider-specific limitations may influence a concrete design only when they materially constrain the current ChatGPT-Plus baseline.

---

# 5. Round 1 remains a strong base, not a mandatory re-review queue

Accepted Round-1 architecture is inherited by Round 2.

A closed Round-1 topic SHALL NOT become a Round-2 task merely because an external idea or later research mentions the same subject.

A closed topic re-enters active design only when new work:

1. requires a material extension of the accepted contract;
2. exposes a real contradiction or invalid assumption;
3. introduces a new consumer whose requirements are not satisfied by the existing contract; or
4. makes the old decision insufficient for the new architecture.

Independent confirmation of an already accepted principle is evidence, not a new roadmap stage.

Examples of inherited architecture that are not reopened by default include:

- deterministic mechanics/execution authority;
- LLM proposal versus deterministic commit boundary;
- objective truth versus fictional knowledge versus human disclosure;
- canonical Story non-authority;
- Step-5 durability, recovery, currentness and concurrency ownership;
- Git/transport order not defining fictional chronology;
- accepted mechanics/RNG not replaying because narration/transport is retried.

---

# 6. Round-2 evidence base

Round 2 uses the following as inputs:

- accepted Steps 1-5 architecture and owner decisions;
- `2026-08-23-step-4-single-context-role-containment-canonical-amendment.md`;
- completed role-context validation Protocols 1-3;
- `DEV/docs/superpowers/research/HDM_External_Architecture_Idea_Dossier_2026-08-21.md`;
- current relevant host/platform feasibility evidence, interpreted under the new single-context baseline;
- useful unresolved questions from former Step-6 working/spike artifacts;
- current GAME/DEV runtime, schema, catalog and documentation state as each Round-2 stage requires.

External/research candidates remain non-normative until deliberately accepted through the HDM design process.

---

# 7. New sequencing authority

`DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` is rebaselined as the active Architecture Round-2 roadmap.

The old six-step decomposition is historical program structure after this decision.

Round 2 SHALL derive its stages from the actual remaining problem/dependency graph rather than preserving the old numbering or forcing old Step-6 questions into one terminal stage.

Broad implementation remains deferred until the relevant Round-2 architecture closes and the normal design -> specification -> implementation-plan gate is reached.
