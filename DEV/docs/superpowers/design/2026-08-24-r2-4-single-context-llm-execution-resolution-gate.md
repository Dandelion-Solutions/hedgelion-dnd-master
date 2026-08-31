# R2.4 Resolution Gate — Single-Context LLM Execution & Instruction Architecture

Status: **RESOLUTION GATE — READY FOR STAGE CLOSURE IF FRESH VERIFICATION PASSES**

Date: 2026-08-24

Inputs:

- R2.4 task brief;
- R2.4 evidence ledger;
- Chronicler service owner clarification and evidence addendum;
- Decision Brief v2;
- owner decision;
- candidate specification;
- adversarial review;
- canonical specification.

## 1. Gate question

Can R2.4 close with an explicit one-request/one-assistant-turn execution architecture that preserves logical role containment, deterministic authority, Story non-authority, Narrator disclosure fencing and first-safe-opportunity Chronicler service without requiring separate agents/calls, a Story scheduler, persistent hidden reasoning or provider-specific machinery?

**Gate answer: YES, subject to fresh remote verification of this gate and the canonical spec.**

---

## 2. Exit criteria coverage

| R2.4 exit criterion | Resolution |
|---|---|
| 1. one-request/one-assistant-turn choreography explicit | `TurnEnvelope` canonical flow defines conditional Interpreter/Dramaturg/Actor(s), deterministic gateway, envelope-level Story service checkpoint, fresh Narrator rebind, validation and `EMISSION_COMMIT` |
| 2. baseline/conditional/separate-mode roles explicit | Interpreter/Dramaturg/Actor conditional; Chronicler deferred-service/first-safe-opportunity; Narrator ordinary final visible phase; Commentator separate mode |
| 3. rebinding/no raw inheritance explicit | Laws R2.4-14..19 plus Step-4 amendment |
| 4. typed nondeterministic result lifecycle/retry semantics | minimal result families + unaccepted regeneration + accepted-frontier rule + Story/Narrator owner boundaries |
| 5. deterministic mechanics/tool/commit interleaving safe | Laws R2.4-20..22; no mechanics/RNG replay after acceptance |
| 6. Narrator/EMISSION_COMMIT integration explicit | Laws R2.4-15, R2.4-28..29 + Step 5.12 |
| 7. instruction hierarchy/conflict explicit | Laws R2.4-23..27 define present-vs-active CORE, precedence/narrowing, phase steering and data/instruction boundary |
| 8. `UNSATISFIABLE` bounded/non-looping | Law R2.4-30 with finite registered alternatives |
| 9. injection/operational-output boundaries explicit | Laws R2.4-26..29 |
| 10. Chronicler/Commentator placement resolved | Chronicler mandatory deferred-service at first safe opportunity; no scheduler; Commentator separate mode |
| 11. D16/S21/S28 item-level disposition | recorded below and in canonical spec |
| 12. Protocols 1–3 reconciled under amendment | shared-context role containment retained; mandatory physical isolation rejected; large model transport envelope lesson retained |
| 13. adversarial blockers resolved | AR-1..AR-8 incorporated into canonical laws |
| 14. R2.6/R2.7 obligations explicit | dedicated downstream sections present |

No exit criterion remains intentionally open inside R2.4.

---

## 3. Adversarial amendment closure

| Finding | Canonical resolution |
|---|---|
| AR-1 same-envelope Chronicler->gameplay feedback | Law R2.4-12 prohibits same-envelope Story feedback |
| AR-2 service check tied to mechanics | Story service checkpoint explicitly envelope-level even on non-mechanical quiet turns |
| AR-3 durable Story outruns source | Law R2.4-11 requires Step-5.10-compatible admitted source basis |
| AR-4 Story contention consumes response margin | Law R2.4-13 requires Story yield/defer before protected Narrator/output margin is threatened |
| AR-5 Chronicler->Narrator new containment channel | explicit R2.6 assurance obligation |
| AR-6 backlog check becomes unbounded scan | compact typed coverage/source-basis check required before bounded load |
| AR-7 `DEFER` becomes scheduler state | turn-local operational result; obligation remains recomputable from coverage/basis |
| AR-8 Narrator resumes without rebind | Law R2.4-15 requires fresh Narrator rebind after Chronicler |

No adversarial finding requires a new semantic owner or owner-level trade-off.

---

## 4. Chronicler final policy

The current product profile now has a stronger Story activation promise than the earlier weakest Step-5.10 baseline:

```text
no fixed turn-count or wall-clock Story freshness SLA
no background-worker guarantee
no durable Story job queue
no Story commit every turn
BUT
compatible backlog is checked every ordinary TurnEnvelope
and receives bounded service at the first safe opportunity
```

Current gameplay correctness and protected Narrator/output capacity remain higher priority. Repeated optional enrichment cannot starve serviceable Story backlog.

Newly generated Story cannot feed back into gameplay roles in the same TurnEnvelope.

---

## 5. Diamond / Strong disposition — R2.4

| Idea | Final disposition | HDM integration |
|---|---|---|
| **D16 invisible auxiliary work** | **ADOPTED WITH REWRITE** | invisible logical phases/results inside the one-turn baseline; Chronicler is a deferred-service consumer; mandatory subagents/extra calls/background workers rejected |
| **S21 late steering** | **ADOPTED** | phase-local steering is a distinct non-authoritative instruction layer; physical prompt position is optimization, not authority |
| **S28 operational protocol sanitation** | **ADOPTED / STRUCTURALIZED** | only validated Narrator payload intentionally crosses visible emission; internal role/tool/Story protocol remains fenced; string stripping is defense in depth |

No active R2.4 Diamond/Strong item remains unaccounted.

---

## 6. Explicit rejected/conditional machinery

Rejected for the current baseline:

- Model-Directed Collapsed Orchestration as sole control architecture;
- deterministic checkpoint FSM per role;
- mandatory physical role isolation;
- one model call per logical role;
- Story scheduler/job queue/background worker dependency;
- generic prompt DSL/provider abstraction;
- large universal model-generated transport envelope;
- persistent chain-of-thought.

Physical separation / stricter FSM remains only a future defense/profile option if R2.6 evidence proves the current supported host cannot preserve required behavior.

---

## 7. Downstream handoff

### R2.5

Collaboration/multiplayer must compose participant identity, recipient scope, shared/independent scenes and input coordination with the same TurnEnvelope/rebinding/Context Runtime laws.

### R2.6

Must empirically validate production-like single-context phase frames, especially Chronicler->Narrator containment, long-chat/context pressure, safe-opportunity anti-starvation, visible host surfaces, injection/role confusion and finite degradation.

### R2.7

Must map logical contracts to Project Instructions/CORE/schema/catalog/runtime/tests/tools and exact machine realization.

---

## 8. Closure recommendation

If a fresh remote read confirms:

- canonical spec contains all AR-1..AR-8 amendments;
- this gate covers all 14 task exit criteria;
- Decision Brief v2 owner decision is recorded;
- roadmap still has only R2.4 `IN PROGRESS` before transition;

then R2.4 may be marked:

> **COMPLETE / ARCHITECTURE CLOSED**

and R2.5 may become the single `IN PROGRESS` stage.
