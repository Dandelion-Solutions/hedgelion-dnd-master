# R2.1 Adversarial Review — Continuity, Memory and History Alignment

Status: **ADVERSARIAL REVIEW — CANDIDATE SURVIVES WITH REQUIRED CLARIFICATIONS**

Date: 2026-08-24

Candidate under review:

- `DEV/docs/superpowers/design/2026-08-24-r2-1-continuity-history-candidate-spec.md`

Owner decision:

- `DEV/docs/superpowers/design/2026-08-24-r2-1-continuity-projection-owner-decision.md`

Evidence ledger:

- `DEV/docs/superpowers/design/2026-08-24-r2-1-continuity-evidence-ledger.md`

---

# 1. Review question

Does the reuse-first continuity architecture provide strong long-campaign semantic continuity while preventing Story/summary/history projections from becoming hidden authority, leaking role information, surviving incompatible history incorrectly, or inflating the exact-recall promise?

Review verdict:

> **YES, after two required wording/contract clarifications that do not reopen the owner-selected architecture.**

No new product decision is required.

---

# 2. Attack matrix

## A01 — Stale Story contradicts current world state

Scenario:

- Story says an NPC is alive at an earlier point;
- current Actor/world owner records the NPC dead.

Attack:

- gameplay role receives Story orientation and acts as if the NPC is still alive.

Candidate defense:

- native current owners answer current questions;
- Story cannot override current state.

Finding:

- **PASS WITH CLARIFICATION AR-1**. The phrase “decision-critical claims” is too narrow. Any **material role decision** depending on a claim whose current/source-specific semantics matter must escalate to the proper source class, even if no immediate canonical commit occurs.

Required closure wording:

> Story may supply orientation, but it may not be the sole basis for a material Actor/Dramaturg/Interpreter/Narrator decision when the decision depends on current/source-specific semantic correctness.

---

## A02 — Story source ref exists but the Story statement is no longer current

Scenario:

- a Story record accurately summarizes an old relationship/ownership/status;
- its source refs remain valid historical evidence;
- later canonical events changed the current relation.

Attack:

- source-linked Story is mistaken for current-state evidence merely because its provenance is valid.

Finding:

- **PASS WITH CLARIFICATION AR-2**. Source traceability proves derivation, not currentness.

Required closure wording:

> Source-bound does not mean current. Any derived unit used for a current-state claim must be checked against the native current owner or another owner-defined currentness relation.

No generic projection freshness frontier is introduced.

---

## A03 — Story contains material secret ineligible to receiving Actor

Scenario:

- one Story record is physically available in the repository;
- it contains a fact Actor[NPC_B] must not know.

Attack:

- generic continuity retrieval includes the record because entity/topic relevance is high.

Defense:

- derived continuity does not widen eligibility;
- gameplay role eligibility is separate from Story/spectator availability;
- R2.3 owns concrete candidate filtering.

Verdict: **PASS**.

Closure requirement:

- R2.3 must fail closed on material eligibility ambiguity; physical/storage presence is insufficient.

---

## A04 — Player A Story continuity leaks to Player B

Scenario:

- Story/history contains material disclosed to one player but not another.

Defense:

- one repository does not imply one identical recipient projection;
- runtime.disclosure and role/player eligibility remain scoped.

Verdict: **PASS**.

---

## A05 — Actor current cognition is reconstructed from old Story prose

Scenario:

- Story says NPC once suspected the duke;
- current `world.knowledge` no longer contains that stance after later evidence.

Attack:

- Actor treats historical suspicion as current belief.

Defense:

- `world.knowledge` remains current epistemic authority;
- Story is history/orientation only.

Verdict: **PASS**, strengthened by AR-1/AR-2.

---

## A06 — Repeated summary self-amplifies an unsupported inference

Scenario:

- Story N1 contains a weak/incorrect editorial inference;
- later Story N2 summarizes N1;
- recurrence makes the model treat it as established fact.

Defense:

- derived text cannot self-amplify factual authority;
- factual support must remain traceable to admitted underlying evidence;
- recurrence is not source authority.

Verdict: **PASS**.

Implementation/evaluation obligation:

- R2.3 source-aware dedup/trace must distinguish derivative recurrence from independent evidence.

---

## A07 — Host Retry/Edit creates an alternative visible conversation

Scenario:

- accepted campaign action already exists;
- user edits/retries an older host message;
- host UI now displays a divergent path.

Attack:

- continuity re-summarizes host-visible path as accepted history.

Defense:

- only admitted HDM evidence feeds durable continuity;
- host ancestry/age is not history alignment.

Verdict: **PASS**.

---

## A08 — Abandoned Narrator draft contaminates continuity

Scenario:

- secret-bearing or incorrect draft was generated but never emission-committed/admitted.

Defense:

- unaccepted drafts are not durable continuity input.

Verdict: **PASS**.

---

## A09 — Exact quote requested after lawful compaction

Scenario:

- semantic history survives;
- exact wording has been lawfully compacted.

Attack:

- Story paraphrase is emitted as a quote.

Defense:

- exact recall terminates only at exact evidence;
- otherwise engine must state non-retention and provide semantic account.

Verdict: **PASS**.

---

## A10 — Verified Transcript exact copy survives while raw message is compacted

Scenario:

- exact Story/Transcript copy is verified under Step 5.11;
- raw source payload is removed.

Defense:

- verified exact Transcript remains an admitted exact source under its existing contract;
- Story nonauthority does not prevent content-exact communication evidence.

Verdict: **PASS**.

---

## A11 — Story is absent or badly lagging after total host-context loss

Attack:

- recovery depends on broad memory that is unavailable.

Defense:

- current/history owners remain sufficient for correctness;
- transient recap can be synthesized;
- Story may lag/fail without blocking gameplay/recovery.

Verdict: **PASS**.

Product consequence:

- quality/latency may degrade; correctness contract remains intact.

---

## A12 — Story projection contract changes

Scenario:

- semantics of candidate admission/coverage change;
- old coverage is reused blindly.

Defense:

- semantic projection-contract generation requires migration/reprojection/reset when incompatible.

Verdict: **PASS**.

---

## A13 — Model/prompt version changes without semantic projection change

Attack:

- all Story coverage is invalidated unnecessarily.

Defense:

- model/prompt version alone is not semantic coverage generation.

Verdict: **PASS**.

---

## A14 — One source is corrected/superseded

Scenario:

- derived Story references an old source whose semantics are corrected/superseded.

Defense:

- source-specific correction/supersession semantics determine compatibility;
- derived projection may be repaired/retired/excluded;
- stronger sources win.

Verdict: **PASS**.

No universal ancestry or trust lattice is required.

---

## A15 — Current question answered from historical event only

Scenario:

- an event says an item was in a chest;
- current state later moved it elsewhere.

Attack:

- history is treated as current state.

Defense:

- source authority is claim-typed;
- historical occurrence evidence is not current owner.

Verdict: **PASS**, strengthened by AR-2.

---

## A16 — Entity synopsis pressure causes duplicate durable state

Scenario:

- R2.3 retrieval is inconvenient;
- implementation adds `npc_memory_summary` writable alongside NPC/world.knowledge.

Defense:

- per-entity continuity begins as a view;
- durable synopsis is conditional and requires explicit architecture admission.

Verdict: **PASS**.

Reopen trigger remains measurable insufficiency, not implementation convenience.

---

## A17 — Whole-history preload hides under “continuity”

Scenario:

- implementation loads all Story/LOG because it is technically eligible.

Defense:

- archive and working context remain distinct;
- R2.3 must bound candidate acquisition/budget.

Verdict: **PASS AS STAGE BOUNDARY**.

R2.1 does not define algorithmic limits but explicitly forbids interpreting deep history availability as preload permission.

---

## A18 — Background summarizer becomes recovery dependency

Scenario:

- Story refresh worker fails for hours/days;
- system cannot resume because it expected fresh summary.

Defense:

- no background/per-turn correctness dependency;
- stronger sources remain recovery basis.

Verdict: **PASS**.

---

## A19 — Malformed source-bound Story passes structural validation but lies semantically

Attack:

- deterministic validator cannot detect all prose errors.

Defense:

- structural validation does not canonicalize semantic quality;
- Story remains repairable noncanonical projection;
- material role decisions escalate to stronger sources.

Verdict: **PASS**, dependent on AR-1.

---

## A20 — Human review accidentally becomes required to trust summaries

Defense:

- human/editor review is optional quality tooling, not gameplay correctness gate.

Verdict: **PASS**.

---

## A21 — Story availability is confused with gameplay-role eligibility

Attack:

- a record is safe for a spectator mode but unsafe for Actor/Narrator/player scope.

Defense:

- candidate explicitly separates the concepts.

Verdict: **PASS**.

R2.3 must define receiving-role eligibility independently.

---

## A22 — Broad orientation steers Dramaturg toward obsolete plot state

Scenario:

- Story is old but still source-valid as historical narrative;
- Dramaturg uses it as current pressure state.

Finding:

- **PASS only with AR-1/AR-2**. Dramaturg creative freedom does not permit treating historical derived orientation as current premise where current state/process owners exist.

---

## A23 — Summary omission becomes false negative authority

Scenario:

- an important fact is absent from a broad summary because Story lagged/omitted it;
- model concludes the fact does not exist.

Defense required:

> Absence from a derived projection is not evidence of absence from canon/history unless the projection contract explicitly proves exhaustive coverage for that semantic question.

Assessment: **SIGNIFICANT CLARIFICATION AR-3**.

This follows existing Story coverage semantics but must be explicit in the final R2.1 contract because gameplay-role consumption increases the risk.

No new owner decision required.

---

## A24 — Projection coverage is complete but semantic claim class differs

Scenario:

- Story layer coverage proves every candidate in a source domain was considered;
- gameplay asks a question the Story projection contract never promised to represent exhaustively.

Defense:

- coverage is layer/source/semantic-contract typed;
- it cannot be generalized into global semantic completeness.

Verdict: **PASS**, with AR-3.

---

# 3. Required clarification set

## AR-1 — MATERIAL ROLE DECISION ESCALATION

Replace the narrow interpretation of “decision-critical claim” with:

> A derived continuity projection may orient a role, but whenever a **material role decision** depends on a claim whose current/source-specific correctness matters, the role must use the appropriate owning/admitted source class rather than relying solely on derived prose.

This applies even when the role output is still noncanonical, because wrong orientation can materially affect Actor/Dramaturg/Narrator behavior.

## AR-2 — SOURCE-BOUND DOES NOT MEAN CURRENT

Add:

> Source traceability proves derivation, not currentness. A derived historical statement cannot answer a current-state question unless currentness is established through the applicable native owner/currentness relation.

No generic projection freshness frontier is introduced.

## AR-3 — PROJECTION ABSENCE IS NOT SEMANTIC ABSENCE

Add:

> Omission/absence from Story or another derived projection is not evidence that the underlying fact/event/entity does not exist unless that exact projection contract explicitly proves exhaustive coverage for the semantic question being asked.

Story coverage is typed to its own candidate/terminal-disposition contract and cannot be generalized into a global closed-world claim.

---

# 4. Exit-criteria review

| R2.1 exit requirement | Result |
|---|---|
| admitted continuity classes / rejected alternatives | PASS |
| owner / authority / lifecycle | PASS |
| source / provenance / coverage | PASS with AR-2/AR-3 |
| stability / consolidation | PASS |
| history / branch alignment | PASS |
| stale / conflict / repair / rebuild / retirement | PASS |
| semantic vs exact recall | PASS |
| Story / Chronicler relationship | PASS |
| bounded generative validation | PASS |
| R2.2 / R2.3 downstream contracts | PASS with AR-1/AR-3 |
| no duplicate authority | PASS |
| recovery without hidden model/context memory | PASS |
| no background-worker correctness dependency | PASS |

---

# 5. Review conclusion

The owner-selected reuse-first architecture survives adversarial review.

The review does **not** justify:

- a new generic memory subsystem;
- a durable entity synopsis now;
- a host-history ancestry model;
- a new freshness frontier;
- universal Story completeness;
- background continuity machinery.

Required next action:

1. incorporate AR-1, AR-2 and AR-3 into the canonical R2.1 specification;
2. perform a closure/coverage check against the Task Brief and active Dossier items;
3. if no contradiction remains, close R2.1 and transition exactly one active stage to R2.2.
