# Step 5.10 — Story Projection Durability — Task Brief

Status: **ARCHITECTURAL RESEARCH — STEP 5.10 IN PROGRESS / SOLUTION-BLIND**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Governing process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Inherited semantic authority:

- Step 4 canonical truth/knowledge/role/Story architecture;
- Step 5.1 domain-typed frontier law;
- Steps 5.5–5.8 durability/publication/recovery/live authority;
- Step 5.9 chronology model;
- Steps 5.3/5.9 Temporal Agenda↔Chronology integration amendment where projection retention interacts with active dependencies.

---

## 1. Classification

**Architectural.**

Step 5.10 must close the persistence/restart/concurrency protocol for a durable but non-canonical four-layer Story read model. It touches publication, idempotency, allocation, recovery, source retention, concurrency and LLM/deterministic boundaries.

No GAME/schema/runtime implementation is authorized by this slice.

---

## 2. Purpose

Design the minimum architecture such that:

```text
canonical gameplay/history
    -> may advance independently

Story projection
    -> may lag
    -> may fail
    -> may restart
    -> may catch up
    -> may be corrected/regenerated
    -> never becomes gameplay authority
```

Exit target inherited from the roadmap:

> Story may lag or be regenerated/corrected without becoming gameplay authority, and a restarted Chronicler can catch up without duplicate or invented events.

---

## 3. Fixed semantic constraints

The design must preserve:

1. `STORY/{TRANSCRIPT,EVENTS,MECHANICS,NARRATIVE}` is durable but non-canonical.
2. Story lives on the campaign branch; no default long-lived spectator/public branch.
3. Story failure cannot roll back or block accepted canonical gameplay publication.
4. Story records cannot create truth, knowledge, disclosure, chronology or current-state authority.
5. Story availability/reveal semantics are dependency-based; no scalar global reveal/chronology frontier.
6. Story IDs remain layer-local human-facing identities (`T...`, `E...`, `M...`, `N...`).
7. One Story record per file is the default.
8. Story record/index/availability edits must publish coherently enough to avoid dangling or spoiler-invalid published state.
9. Physical LLM role-call topology remains Step 6.
10. A logical Chronicler role does not imply one model call, one process, one agent or one background worker.
11. Story projection must not require campaign-wide scans during ordinary operation.
12. Story source provenance does not transfer authority from canon into Story.

---

## 4. Deployment/platform constraint for this slice

The baseline HDM deployment assumption for Step 5.10 is intentionally conservative:

> **Correctness must hold with one ordinary sequential ChatGPT conversation/execution stream, without ChatGPT Work, without Pro/Enterprise-only capability assumptions, and without a permanently running independent/background Story worker.**

Current platform research (2026-08-21) is an input, not permanent architecture truth:

- ordinary ChatGPT turns cannot be treated as six independently persistent background LLM workers;
- ChatGPT Work exists for longer multi-step work on eligible paid plans, but the project owner explicitly excludes burning Work capacity for ordinary HDM gameplay;
- Scheduled Tasks are future/scheduled runs, have plan/tool/access limitations, and are not a suitable assumed per-turn Story worker;
- OpenAI API/Agents SDK and future orchestration backends may support separate invocations/workers, but physical topology belongs to Step 6 and cannot be required by Step 5.10 correctness.

Reverification of platform details remains required in Step 6.

This constraint must **not** cause Step 5.10 to invent a durable generic scheduler/job queue merely to emulate unavailable background execution.

---

## 5. Required research questions

### 5.1 Projection authority and state

- What durable Story-local state is necessary to know what source work has already been considered?
- How is that state distinguished from canonical history authority?
- Is a durable work queue necessary, or can backlog be derived from source coverage gaps?
- How is intentional omission represented so restart does not reconsider the same non-story-worthy source forever?

### 5.2 Layer-local coverage/frontiers

- What does “caught up” mean for each Story layer?
- Can a scalar cursor exist only inside a source domain that explicitly provides ordered enumeration?
- How are multiple source domains represented without violating Step 5.1 no-cross-domain-order law?
- Must layers advance independently?

### 5.3 Projection work identity / idempotency

- How does restart distinguish already-published projection from not-yet-published projection?
- What survives an ambiguous publication acknowledgement?
- How are one-to-many and many-to-one mappings between source evidence and Story records represented?
- How are intentionally skipped inputs represented?

### 5.4 Chronicler boundary

- Which work is deterministic planning/validation/publication versus generative editorial transformation?
- Can/should some Story layers be produced without an LLM call?
- What exact typed input/output does a Chronicler projection attempt use without granting it transport/ID/coverage authority?
- How can the protocol remain valid whether Step 6 later runs Chronicler inline, in a separate invocation, in Work, or in an external orchestrator?

### 5.5 Publication atomicity

- What must be atomic within one Story layer transaction: record files, layer indexes, ID allocator state, availability, coverage claims, crossrefs?
- Are cross-layer atomic transactions required or harmful?
- What happens when EVENTS succeeds and NARRATIVE fails?

### 5.6 Same-branch concurrency

- How do Story-only commits coexist with canonical gameplay commits on one branch?
- Can Story-only ref movement be classified as proven-disjoint movement for canonical publication rebuild?
- Must Story always yield to gameplay under contention?
- How are Story-vs-Story allocator conflicts resolved without rerunning accepted gameplay or unnecessarily rerunning LLM generation?

### 5.7 Layer-local ID allocation

- Where does each Story layer's next sequence live?
- Can final IDs be allocated only at publication time so generative drafts use temporary local keys?
- How are IDs remapped after Story-writer conflicts without changing content semantics?
- Can deleted/regenerated Story reuse old IDs? What stability is promised?

### 5.8 Cross-reference closure and availability

- May a new Story record reference only already-durable Story records or records in the same atomic Story transaction?
- Are reverse refs authoritative or derived?
- How are availability requirements validated atomically with content/index publication?
- How does correction/regeneration prevent spoiler metadata drift?

### 5.9 Lag / catch-up policy

- With no required background worker, what events may trigger opportunistic catch-up?
- Can exact trigger/frequency remain Step-6 policy while Step 5.10 defines only correctness of any chosen activation?
- What bounded work-selection protocol prevents a long backlog from monopolizing a gameplay turn?

### 5.10 Correction / regeneration

- When may a Story record be edited in place?
- When does split/merge/coverage change require new Story IDs or retirement/redirect handling?
- How does correction interact with coverage claims and indexes?
- How does a projector version/policy change avoid silently rebuilding all history?

### 5.11 Source retention / compaction dependency

- What Story fidelity cannot be regenerated after exact transcript/source deletion?
- Must unprojected source evidence be protected from compaction?
- What does `source_refs` promise after source content is compacted: identity provenance, dereferenceability, or both?
- Which questions must be handed to Step 5.11/5.13 rather than solved here?

### 5.12 Save/recovery semantics

- Does explicit SAVE require Story catch-up? Presumptively no unless evidence proves otherwise.
- Does cold gameplay recovery require Story hydration? Presumptively no.
- How does Chronicler restart recover its own lag/catch-up basis without checkpoint authority?

---

## 6. Alternatives that must receive genuine consideration

The research must compare at least these distinct families rather than assuming one projection architecture:

A. synchronous Story inside canonical gameplay publication;
B. foreground post-canon Story projection on every turn;
C. queue-free lazy/opportunistic catch-up from durable typed coverage;
D. durable projection work ledger/job queue;
E. deterministic source-keyed Story identities / source-to-record mapping;
F. rebuild/regenerate Story on demand with minimal progress state.

Hybridization is allowed only after each alternative is challenged independently.

---

## 7. Required analytical challenge

Challenge any candidate against at least:

- plain ChatGPT sequential execution with no background worker;
- ten turns of Story lag followed by restart;
- generation succeeds but publication loses CAS;
- publication succeeds but acknowledgement is ambiguous;
- canonical gameplay commit lands while Story draft is being prepared;
- two future Story workers race same layer allocation;
- EVENTS projection succeeds while NARRATIVE generation fails;
- source event intentionally produces no Story record;
- one Story event summarizes several semantic events;
- one semantic event is split into several presentation records;
- Story correction after Commentator/index refs exist;
- source transcript is compacted after Story publication;
- source transcript is about to compact while Story has not projected it;
- availability metadata itself would leak a hidden identity;
- independent multiplayer scenes generate Story in different chronology domains;
- explicit SAVE with Story far behind;
- full Story deletion followed by optional rebuild;
- no LLM Chronicler invocation is available for several gameplay turns;
- future asynchronous worker is introduced without changing semantic protocol.

---

## 8. Decision rights

Escalate only material owner choices after technical alternatives are narrowed.

Likely owner-level questions, if they survive analysis, include:

- how much historical/presentation fidelity Story is expected to preserve after source compaction;
- whether Story freshness is a user-visible product guarantee or best-effort eventual projection;
- whether stable Story URLs/IDs must survive structural regeneration/split/merge.

Do not escalate mechanical questions such as allocator CAS, coverage-index shape or retry rules if one design dominates technically under already accepted requirements.

---

## 9. Explicit non-goals

Step 5.10 does not decide:

- physical six-role model-call topology;
- model/provider selection;
- Work/API/agent deployment architecture;
- token/latency budget policy;
- exact transcript retention/deletion policy (5.11);
- exact host-emission/disclosure acknowledgement (5.12);
- physical GC/deletion algorithm (5.13);
- broad Story runtime/schema implementation.

Step 5.11 MUST NOT begin before Step 5.10 architecture closes.
