# Step 5.2 — Resumable Runtime Closure — Architecture Task Brief

Status: **TASK BRIEF — RESEARCH AUTHORIZED BY FIXED CHARTER**

Date: 2026-08-20

Classification: **Architectural**

Pre-research framing authority:

- `DEV/docs/superpowers/design/2026-08-20-step-5-2-resumable-runtime-closure-pre-research-charter.md`

Current prerequisite:

- Step 5.1 / Frontier Model is canonical and closed under B-NARROW.

---

## 1. Problem statement

HDM currently has accepted current-state owners, in-flight deterministic execution owners, owner-local temporal obligations, live operational ownership, campaign durability, sparse checkpoints, and several rebuildable caches. However, these contracts were developed across several architecture steps and do not yet form one explicit cold-recovery classification.

The problem is to determine the minimum set of state and evidence that must remain reconstructible at an established durable recovery basis so that a fresh runtime with no prior process/chat/model memory can resume the same gameplay-significant state and unfinished deterministic work without introducing a new duplicate authority.

The design must distinguish a recoverability defect from state that is legitimately volatile because no applicable durability boundary had yet been reached.

---

## 2. Goals

1. Classify all gameplay-significant runtime state as authoritative, irreducible recovery evidence/pointer, rebuildable derived state, truly ephemeral state, volatile-ahead-of-durable state, or defect/unowned state.
2. Identify every active semantic owner that must be recoverable from the last durable recovery basis.
3. Identify the smallest irreducible recovery references/evidence needed for bounded cold recovery.
4. Prove which major caches/indexes can be rebuilt and therefore must not become persistence authorities.
5. Determine whether Step-3 portable execution contracts already contain enough in-flight semantics or whether material gaps exist.
6. Determine what fixed RNG/choice/reaction evidence must survive to prevent semantic re-roll/re-adjudication.
7. Determine the minimum temporal-owner evidence required so Temporal Agenda can remain disposable.
8. Determine cold-recovery constraints for campaign/live/allocator/session routing without designing later protocols.
9. Determine how an unresolved semantic resume point is represented when no mechanical Continuation currently owns it.
10. Establish bounded-discovery requirements so recovery does not depend on repository-wide guesswork.
11. Produce decision-ready alternatives and a recommendation only if repository evidence leaves a real material trade-off.

---

## 3. Non-goals

Step 5.2 does not decide:

- the exact timer/pending-work lifecycle;
- when context loss forces publication;
- SOFT/HARD/SAVE trigger semantics;
- Git publication retry/crash behavior;
- checkpoint serialization/hydration schema;
- live CAS/lease/absorption protocol;
- chronology representation/reconciliation;
- Story/transcript durability policy;
- disclosure-delivery acknowledgement;
- GC algorithms;
- physical LLM role topology.

It also does not persist raw chat history, hidden model state, prompts, chain-of-thought, or arbitrary RAM snapshots as campaign authority.

---

## 4. Inherited architecture invariants

The research must preserve:

- Step 5.1 domain typing and no implicit cross-domain ordering;
- native current-state ownership;
- campaign publication evidence versus HOT current truth separation;
- live operational scope ownership without premature campaign absorption;
- Step-3 Command/Resolution/Procedure/Continuation ownership;
- Procedure-only procedure-local ResourceState ownership;
- owner-local temporal obligation ownership;
- Temporal Agenda as derived index;
- deterministic fixed RNG/choice continuity;
- checkpoint as recovery descriptor/evidence rather than state authority;
- Story as durable noncanonical projection;
- no generic pending-consequence/job authority;
- no dependence on prior model/chat/process memory for the promised durable recovery point.

---

## 5. Quality attributes that may distinguish designs

Priority order for this slice:

1. **Correctness** — recovery must not invent, lose, replay, or double-own gameplay-significant state.
2. **Determinism** — accepted fixed execution inputs/outcomes must not be recomputed inconsistently after restart.
3. **Bounded recovery** — exact recovery must have bounded roots/discovery rather than campaign-wide semantic search.
4. **Ownership clarity** — recovery representation must not create a parallel current-state authority.
5. **Minimality / YAGNI** — serialize only irreducible information.
6. **Testability / diagnosability** — missing/incompatible required evidence must produce a detectable integrity/recovery failure.
7. **Compatibility with later Step-5 slices** — classifications must constrain but not preempt later protocols.
8. **Operational simplicity** — avoid a new lifecycle-bearing recovery subsystem unless evidence proves it necessary.

No new numeric RPO/latency/storage target is invented in this slice.

---

## 6. Repository evidence that must be inspected

Structural discovery follows `DEV/PROJECT_MAP.md` and then current owning artifacts.

Mandatory evidence families:

1. Step 5.0 final and Step 5.1 canonical/result chain.
2. Step 3 canonical execution architecture and machine schemas/tests for:
   - RuntimeCommand;
   - Resolution;
   - Procedure;
   - Continuation;
   - ExecutionSegment;
   - pending child invocation;
   - receipts/idempotency;
   - Choice/Reaction;
   - invocation/fixed input evidence.
3. Step 2 temporal/recovery ownership and schemas for Effects, Resources, LifeState and TemporalBindings.
4. GAME runtime persistence/recovery hot path:
   - `RUNTIME.md`;
   - `STORAGE.md`;
   - `SESSION.md`;
   - `DURABILITY_GUARD.md`;
   - `SAVE_CONTRACT.md`;
   - `PERSISTENCE.md`;
   - `INTEGRITY.md`;
   - `RANDOMNESS.md`.
5. `MULTIPLAYER.md`, `LIVE_SCENE.md`, `CHRONOLOGY.md` only for constraints crossing into recovery.
6. Active GAME schemas/templates for manifest/current/session/checkpoint/scene/live/event/index and any relevant operational records.
7. `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` as support/recovery consumer.
8. Current catalog/identifier policies for runtime owner identities and allocator semantics.
9. Existing regression tests/case catalogs.
10. Historical derivation only when necessary to identify stale assumptions/provenance.

Repository search must follow structural inspection; zero search results are not evidence of absence by themselves.

---

## 7. Research questions

The research must answer at least:

1. What exactly is promised to survive total runtime/chat/process loss at the last durable basis?
2. Which Step-2/3 owners may be active at such a basis?
3. How are those owners found without scanning/guessing?
4. Which operational values are irreducible versus deterministically reconstructible?
5. Which currently process-local values are genuine defects if a boundary is durable?
6. Which fixed random/choice/adjudication facts must survive so restart cannot change accepted outcomes?
7. Can Temporal Agenda always be rebuilt from owner-local roots and chronology evidence?
8. Which ID allocator/reservation state matters to already-recoverable identities?
9. Can campaign + active live scopes be resumed from native roots without a new merged authority?
10. What does “resume point” mean when there is no active Resolution/Continuation?
11. Does `runtime.session` own durable gameplay semantics, or only coordination/recovery metadata?
12. Does checkpoint need to know the closure, or can 5.7 derive it from other roots?
13. Which missing/stale-reference cases are `RECOVERY_REQUIRED`, `CANON_SUSPECT`, recoverable refresh, or unrecoverable defect?
14. Is a first-class `Resumable Runtime Closure` record actually required?
15. What constraints must 5.3–5.9 inherit from the answer?

---

## 8. Mandatory analytical outputs

The research/draft must contain:

- evidence map;
- classification ledger;
- bounded recovery-root graph;
- in-flight execution closure analysis;
- fixed RNG/choice/reaction analysis;
- temporal-owner/Agenda analysis;
- allocator/identity analysis;
- live-scope recovery constraints;
- semantic resume-point analysis;
- explicit rebuildable/ephemeral list with justification;
- integrity/defect taxonomy for missing closure evidence;
- failure-scenario walkthroughs from the pre-research charter;
- simplest viable architecture;
- strongest counterargument;
- assumption/evidence ledger;
- exact later-slice deferrals;
- recommendation and confidence;
- explicit statement whether a human architecture decision is required.

---

## 9. Exit criteria for research phase

The research phase is complete when, for every gameplay-significant state or obligation that may exist at a durable recovery basis, the draft can mechanically state:

```text
native semantic owner
-> durable/recoverable state or irreducible reference
-> bounded discovery root
-> rebuildable derived state
-> deterministic resume dependency
-> integrity outcome if required evidence is missing/incompatible
```

and when the draft has demonstrated that no proposed new recovery abstraction duplicates current writable authority or exists only for conceptual symmetry.

If a fundamental ownership/product/RPO trade-off remains after challenge, produce a Decision Brief and stop at the human gate. If no such trade-off remains, proceed mechanically through candidate specification, adversarial review and resolution under the canonical design process.
