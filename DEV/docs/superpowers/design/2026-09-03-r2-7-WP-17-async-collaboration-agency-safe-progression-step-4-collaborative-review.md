# R2.7 WP-17 — Async Collaboration / Agency-Safe Progression — Step-4 Collaborative Review

Status: **STEP 4 REVIEW COMPLETE — SELECTED DIRECTION CONFIRMED / NO HUMAN DECISION REQUIRED**

Date: 2026-09-03

Reviewed Decision Brief:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-step-3-decision-brief.md`.

Evidence basis remains the repaired Step-1 package plus Step-2 evidence/manifest expansion. This review tests whether Alternative C hides a product choice, duplicates an owner, loses information after compaction, creates a global wait boundary, or conflicts with current access/currentness/recovery law.

---

## 1. Review disposition

Selected direction remains:

> **SCOPED CAMPAIGN-OWNED COLLABORATION OBLIGATION / INTERACTION-CLAUSE HUMAN INPUT IDENTITY / CONTENT-SUFFICIENT SEMANTIC REFERENCES / NATIVE-OWNER-FIRST PROGRESSION**

No reviewed issue requires a human-owned product-semantic decision or reopening accepted upstream architecture.

The candidate may proceed provided it makes the review constraints below normative and machine-facing.

---

## 2. Review issue R17-04-01 — does campaign ownership create a hidden campaign-global collaboration frontier?

**Concern:** `runtime.collaboration_obligation` lives in the campaign domain, so a naive implementation could equate campaign HEAD with collaboration generation/currentness or serialize all waits through one campaign-wide frontier.

**Resolution:** preserve three separate concepts:

```text
campaign ref/revision
    physical publication/current source fence for campaign record access

(obligation_id, generation)
    semantic collaboration generation identity

underlying native opportunity basis
    current campaign/LIVE/procedure/chronology evidence that makes the generation applicable
```

Unrelated campaign commits may force publication refresh/rebase but do not advance collaboration generation or fiction.

**Disposition:** CLOSED; candidate must state explicitly.

---

## 3. R17-04-02 — can `(interaction_id, clause_id)` be called exact if current schema lacks normalized collaboration content?

**Concern:** identity is exact, but current `IntentClause` schema does not yet make collaboration semantic class/content machine-closed.

**Resolution:** distinguish identity from content contract:

- exact identity is existing `(interaction_id, clause_id)`;
- the candidate requires a collaboration-relevant IntentClause specialization with closed R2.5 semantic class + bounded normalized semantic content;
- this remains inside the existing accepted input owner;
- later schema realization must materialize the contract;
- obligation stores only the reference;
- message exact-text evidence is separately retained only when required.

No new input record/value kind is needed.

**Disposition:** CLOSED; candidate must treat current schema shape as explicit downstream machine debt.

---

## 4. R17-04-03 — can one IntentClause satisfy multiple collaboration purposes silently?

**Concern:** one accepted input may be semantically relevant to more than one obligation, risking accidental cross-purpose reuse.

**Resolution:** identity and use are separate:

```text
accepted input identity = (interaction_id, clause_id)
use association = obligation_id + generation + purpose + scope + requirement
```

A single input identity may be referenced more than once only where each association independently passes deterministic semantic compatibility/currentness/admission. No wording similarity, shared message or common participant grants reuse.

Old-generation reuse follows explicit reinterpretation/reconfirmation law.

**Disposition:** CLOSED.

---

## 5. R17-04-04 — can required contributor replacement become agency transfer?

**Concern:** if PLAYER/control changes while waiting, automatically replacing a required participant could turn membership maintenance into a fictional/voluntary decision transfer.

**Resolution:** current requirement identity is generation-defining where voluntary agency is involved. Controller/membership change triggers bounded opportunity re-evaluation:

- old generation does not silently rewrite its required set;
- old input remains historical accepted input evidence only;
- if the opportunity remains valid under a new controller, use a successor generation with current authority;
- no fictional action is synthesized by the transfer itself.

**Disposition:** CLOSED.

---

## 6. R17-04-05 — when does OPEN become CLOSED?

**Concern:** if closure is implicit from message arrival order or first sufficient-looking set, late concurrency can change which inputs are considered.

**Resolution:** collection closure is an explicit owner transition under the current generation contract. It occurs only after:

1. the current required set is satisfied or otherwise lawfully discharged;
2. current underlying decision opportunity remains valid;
3. any native ordered owner takeover has been excluded/reconciled;
4. chronology/order ambiguity material to the result is resolved or the scope remains blocked;
5. the exact accepted input set for this generation is frozen.

Arrival order itself never closes a generation.

**Disposition:** CLOSED.

---

## 7. R17-04-06 — does `CLOSED` duplicate Step-3 execution state?

**Concern:** `CLOSED` might become a pseudo-Procedure state that owns the dependent consequence.

**Resolution:** `CLOSED` means collection membership is frozen only. The dependent interpretation/execution returns to the existing natural owner. `RESOLVED` stores only a discharge/evidence reference as needed; it does not mirror Procedure/Resolution/command state.

If dependent execution suspends on a native Choice/Reaction/Continuation, that native owner governs the suspension; collaboration does not reopen or mirror it.

**Disposition:** CLOSED.

---

## 8. R17-04-07 — durable input reference vs message compaction

**Concern:** a collaboration record could survive while its referenced message compacts and the semantic meaning disappears.

**Resolution:** Step-5.11 content-sufficiency law becomes a candidate invariant:

- referenced collaboration-relevant IntentClause normalized semantics remain durable for as long as a live consumer requires them;
- exact message text is protected only if exact wording remains semantically required;
- a bare message/interaction ID cannot be considered sufficient if the dependent meaning would otherwise disappear.

**Disposition:** CLOSED.

---

## 9. R17-04-08 — cross-domain durability atomicity

**Concern:** accepting input into a campaign-owned obligation while the decision basis is LIVE-owned could imply campaign+LIVE transactionality.

**Resolution:** no distributed transaction. Before campaign obligation mutation, validate the bounded current LIVE/native opportunity basis. Campaign publication then establishes only collaboration collection state. Before later closure/use, revalidate current LIVE/native basis again. If it moved materially, obsolete/reconcile the generation. Already accepted native gameplay edges remain real.

**Disposition:** CLOSED.

---

## 10. R17-04-09 — ordinary-turn publication cost

**Concern:** making obligation state durable could turn every multiplayer message into a campaign commit.

**Resolution:** only admitted durable collective obligations have collaboration-specific shared persistence. Ordinary independent or native-ordered input creates no obligation write. Within an admitted obligation, a state change must become durable before another participant/recovery/dependent edge relies on it; batching is allowed only while that reliance has not crossed the owner-required durability boundary.

No heartbeat or per-message generic save is introduced.

**Disposition:** CLOSED.

---

## 11. R17-04-10 — catch-up can accidentally become collaboration truth authority

**Concern:** a generated recap might decide that an obligation is current/satisfied or expose another player's secret context.

**Resolution:** catch-up is derived after current routing/authorization and may only project:

- current recipient-eligible world/knowledge/disclosure evidence;
- current own unresolved collaboration/native requirements;
- bounded eligible history needed for orientation.

It cannot mutate/satisfy obligations, establish truth, infer reading, copy planning or expose another participant's private context.

**Disposition:** CLOSED.

---

## 12. R17-04-11 — absence/not-immunity balance

**Concern:** agency protection could either convert silence into consent or freeze automatic world/rule consequences indefinitely.

**Resolution:** keep both R2.5 laws:

- no voluntary opportunity may be consumed from silence/absence;
- once current owners prove no applicable voluntary decision/reaction remains, automatic consequence may proceed despite absence.

The proof is owner/currentness-based, never timeout/presence-based.

**Disposition:** CLOSED.

---

## 13. R17-04-12 — discovery of open obligations without global index

**Concern:** cold recovery/rejoin might seem to require scanning `STATE/RUNTIME/COLLABORATION`.

**Resolution:** final candidate must require bounded positive routing from current player/native lifecycle references or another admitted recovery-root relation. No index omission may prove absence. If later implementation cannot meet bounded discovery without an index, that is a measured/consumer-specific helper question; any helper remains rebuildable/non-authoritative and does not change semantic ownership.

**Disposition:** CLOSED for architecture; exact helper is deferred to later realization/performance evidence.

---

## 14. R17-04-13 — terminology collision regression

**Concern:** later candidate prose could reintroduce ambiguous “typed Contribution” terminology.

**Resolution:** machine-facing human input terms are:

- `human collaboration input`;
- `accepted human input identity`;
- `collaboration-relevant IntentClause`;
- `accepted_input_ref`.

Unqualified `value.contribution` remains exclusively Rule Element mechanics.

**Disposition:** CLOSED.

---

## 15. R17-04-14 — WP-18 contamination

**Concern:** catch-up/coherence might be solved by shared Dramaturg planning.

**Resolution:** WP-18 remains downstream. No planning horizon participates in collaboration authority/currentness/catch-up eligibility merely because it can help narration. Planning-only material is explicitly excluded from player catch-up.

**Disposition:** CLOSED.

---

## 16. Candidate requirements from review

Step 5 must make explicit:

1. three-family admission before any obligation representation;
2. campaign-owned obligation, no baseline global index/frontier;
3. generation-local immutable identity-defining fields;
4. explicit `OPEN/CLOSED/RESOLVED/OBSOLETE` collection-only lifecycle;
5. accepted human input identity `(interaction_id, clause_id)`;
6. closed R2.5 semantic class + bounded normalized semantics in the existing IntentClause/input owner;
7. optional exact-text ref only through Step 5.11 when exact form matters;
8. no `value.contribution` reuse;
9. reference-only obligation association;
10. explicit closure transition, not arrival-order closure;
11. current principal/PLAYER/control/native opportunity revalidation;
12. generation successor on material requirement/control/purpose/scope change;
13. duplicate/stale/late/reuse law;
14. no replay/reroll accepted execution;
15. maximal safe frontier + same visible frontier;
16. no absence/timeout/presence agency inference;
17. bounded recipient-safe catch-up;
18. native-domain durability/recovery composition without distributed transaction;
19. bounded discovery/non-authoritative helpers only;
20. WP-18/downstream implementation boundaries.

---

## 17. Review gate

```text
SELECTED_DIRECTION_CONFIRMED: YES
REVIEW_ISSUES: 14
UNRESOLVED_REVIEW_BLOCKERS: 0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
STEP_5_READY: YES
WP18_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
```
