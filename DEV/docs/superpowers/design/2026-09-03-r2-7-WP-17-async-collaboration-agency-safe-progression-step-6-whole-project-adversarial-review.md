# R2.7 WP-17 — Async Collaboration / Agency-Safe Progression — Step-6 Whole-Project Adversarial Review

Status: **STEP 6 ADVERSARIAL REVIEW COMPLETE — 2 BLOCKING + 4 SIGNIFICANT FINDINGS / RESOLUTION REQUIRED**

Date: 2026-09-03

Candidate under review:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-step-5-candidate-spec.md`.

Independent source reconstruction:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-step-6-source-manifest-expansion.md`.

This review did not treat the Step-2 Source Manifest as the whole-project review set. It independently reconstructed the relevant direct/indirect graph from `DEV/PROJECT_MAP.md`, then attacked the Step-5 candidate against current owners, machine contracts and consumers.

---

## 1. Finding register

### F17-01 — BLOCKING — no exact bounded recovery/rejoin route to current open obligations

**Attack:** Candidate law WP17-56 says current participant/native routing “must expose sufficient bounded positive references” but does not choose the exact correctness route. WP-11 provides direct known-ID routing and no baseline collaboration index. WP-14 forbids ordinary recovery scans of all runtime records/directories/history. Current PLAYER schema has no collaboration routing companion and current PLAYER_INDEX is not a collaboration authority/index.

**Failure mode:** after chat/session loss or rejoin, the engine may know the current PLAYER but cannot discover that PLAYER's required open obligation without either:

- scanning `STATE/RUNTIME/COLLABORATION`;
- trusting stale chat/session/cache memory;
- introducing an unreviewed global collaboration index/registry; or
- silently losing the obligation.

Any of those violates accepted recovery/currentness/agency law.

**Required resolution:** allocate one exact bounded positive routing companion from the already-resolved current required PLAYER to obligation IDs, while preserving the obligation as semantic owner. The companion must be completeness-protected with obligation required-set/lifecycle publication, nominate only, require dereference/revalidation, and never become consent/currentness/closure authority. No generic collaboration index or background scan.

**Affected artifacts:** Step-3 decision, Step-4 review issue 12, Step-5 laws WP17-23/42/54-56, final canonical spec, downstream PLAYER/schema/test realization obligations.

**Disposition:** `OPEN FOR STEP 7`.

---

### F17-02 — BLOCKING — dependent `ACTIONABLE_INTENT` release into Step-3 execution is under-specified

**Attack:** Candidate WP17-15 says a collaboration-dependent actionable clause “may remain” pending and no dependent root command executes merely because input arrived, but it does not make the pre-command boundary mandatory or close how several accepted Interactions are released without inventing a synthetic combined RuntimeCommand.

Step-3 machine law is strict: every RuntimeCommand already belongs to one `interaction_id + intent_plan_id + clause_id`. Once accepted, Command/Procedure/Continuation owns execution/idempotency/resume. A collaboration owner cannot simultaneously own the same pending executable responsibility.

**Failure modes:**

1. allocate `runtime.command` before collective collection closes, creating overlapping wait authority between collaboration and Step 3;
2. choose one participant's command anchor from arrival/commit order;
3. synthesize a new multi-Interaction/system command that Step 3 never admitted;
4. replay already accepted independent prefixes when collection later releases.

**Required resolution:**

- every collaboration-held dependent `ACTIONABLE_INTENT` remains its original accepted IntentClause in pre-command `intent.pending` state with `command_id` absent for the blocked dependent unit;
- independently executable semantic units must be split into separate clauses before command acceptance;
- collaboration never creates a new command identity;
- when collection closes, deterministic handoff maps each released actionable clause back to its **own** normal Step-3 command path, or to an already-existing native owner, or to clarification/non-executable disposition;
- if one dependent native consequence requires a single command anchor, the semantically authorized anchor clause must be generation-defining/explicit, never selected by transport order; if no admitted anchor/native mapping exists, do not synthesize one—request/accept a current input or remain blocked under the owning contract.

**Affected artifacts:** Step-3 selected direction, Step-4 issues 5/6, Step-5 laws WP17-15/18/19/32/48-54, final canonical spec, IntentClause/RuntimeCommand downstream machine/test obligations.

**Disposition:** `OPEN FOR STEP 7`.

---

### F17-03 — SIGNIFICANT — accepted collaboration-relevant IntentClause semantics are not explicitly immutable/unitary

**Attack:** Candidate correctly requires normalized semantics but does not state that the accepted semantic class/content of `(interaction_id, clause_id)` becomes immutable while referenced. Nor does it state that one collaboration-relevant clause represents exactly one semantic unit/class.

**Failure modes:**

- same stable input identity later receives different normalized meaning;
- one clause simultaneously acts as OOC coordination plus actionable intent while one obligation association assumes only one meaning;
- message compaction leaves a rewritten normalized summary that changes the accepted input while preserving identity.

**Required resolution:** once accepted/referenced, collaboration-relevant `collaboration_semantic_class + normalized_semantics + material exact-text dependency refs` are immutable accepted interpretation payload for that clause. Distinct material R2.5 semantic units from one message receive distinct IntentClauses. Correction/reinterpretation uses a new accepted input identity/current interpretation path; never rewrite old meaning in place.

**Affected artifacts:** Step-3 human-input representation, Step-4 issues 2/3, Step-5 laws WP17-11-14/28-31, final canonical spec, downstream IntentClause schema/tests.

**Disposition:** `OPEN FOR STEP 7`.

---

### F17-04 — SIGNIFICANT — obligation-ID lineage vs successor-generation boundary is incomplete

**Attack:** Candidate defines generation-defining fields but not when a changed dependency remains the same stable obligation lineage versus when a completely new collaboration obligation ID is required.

**Failure mode:** stable `obligation_id` may be silently repurposed for an unrelated decision opportunity, violating stable identity/reference semantics; or every small generation change may allocate unrelated IDs and break bounded lineage/currentness reasoning.

**Required resolution:** one `obligation_id` represents one stable bounded collaboration dependency lineage anchored to one admitted dependency/purpose family. Material evolution of that same lineage uses successor generation. A semantically unrelated/new decision opportunity gets a new obligation ID. Old obligation/generation identity is never repurposed.

**Affected artifacts:** Step-3 generation model, Step-5 laws WP17-7-9/17-21/26/31, final canonical spec, downstream schema/identity tests.

**Disposition:** `OPEN FOR STEP 7`.

---

### F17-05 — SIGNIFICANT — catch-up may leak other participants' collaboration input semantics

**Attack:** Candidate excludes private context/planning dumps, but an obligation itself references accepted inputs from multiple players. Treating “current own obligation” as catch-up-eligible could expose another participant's OOC/private semantic input merely because it participates in the same obligation.

**Failure mode:** collaboration collection state becomes an implicit disclosure grant and bypasses Step-4/R2.3/Step-5.11/5.12 recipient eligibility.

**Required resolution:** define a recipient-safe obligation projection. A returning participant may receive the obligation purpose/status/current own requirement and only other input content independently eligible through current message/knowledge/disclosure/context rules. Presence of an input ref in collaboration state grants no disclosure. Private/OOC input of another participant remains hidden unless an existing owner independently permits exposure.

**Affected artifacts:** Step-4 catch-up issue, Step-5 laws WP17-42-47, final canonical spec, downstream Context Runtime/catch-up tests.

**Disposition:** `OPEN FOR STEP 7`.

---

### F17-06 — SIGNIFICANT — `RESOLVED` is coupled too loosely to downstream gameplay completion and partial publication

**Attack:** Candidate WP17-20 describes `RESOLVED` as discharged by accepted native consequence/evidence, but collaboration owns collection only. If native execution consumes the closed collection and later suspends/fails/continues, collaboration must not remain an alternate execution owner. Conversely, if native handoff/accepted execution succeeds but collaboration terminal publication fails, recovery must not replay the action or reopen collection.

**Failure modes:**

- collaboration lifecycle remains coupled to full gameplay completion;
- partial cross-domain success creates a stale `CLOSED` record that appears executable again;
- recovery re-releases already consumed inputs because `RESOLVED` metadata did not publish;
- collaboration mirrors Procedure/Continuation execution state.

**Required resolution:** redefine collaboration resolution as **accepted handoff/consumption of the closed collection by the admitted native owner(s)**, not completion of all downstream gameplay. Handoff uses immutable evidence equivalent to:

```text
(obligation_id, generation, closed_input_set_fingerprint)
```

plus the native execution/input owner refs that consumed it. Native command/input fingerprints/dependency evidence retain this source basis. If native handoff succeeded but collaboration terminalization did not publish, recovery recognizes already-consumed handoff evidence and forward-repairs `RESOLVED`; it never replays/rerolls/reopens. Later Choice/Reaction/Continuation remains purely native.

**Affected artifacts:** Step-4 issue 6/8, Step-5 laws WP17-17-20/32/48-54, final canonical spec, downstream execution/recovery tests.

**Disposition:** `OPEN FOR STEP 7`.

---

## 2. Whole-project challenge areas with no finding

The independent review found no defect requiring change for:

- SR17-01 mechanical `value.contribution` separation;
- three-family coordination classification itself;
- campaign ownership of admitted collaboration record;
- optional contributors non-blocking;
- absence not consent / not immunity balance;
- no timeout/presence/heartbeat correctness;
- maximal-safe-frontier and visible-frontier principle;
- technical/message/ref/CAS order not chronology;
- no distributed transaction/global queue/scheduler/frontier;
- WP-16 principal/PLAYER/control constraints;
- WP-18 downstream boundary.

---

## 3. Severity summary

```text
STEP_6_BLOCKING:      2
STEP_6_SIGNIFICANT:   4
STEP_6_MINOR:         0
```

All six findings are mechanically resolvable inside WP-17 without changing product semantics or reopening an accepted upstream owner.

---

## 4. Step-7 propagation requirements

Step 7 must resolve and propagate each item individually:

| Finding | Required final propagation |
|---|---|
| F17-01 | exact required-PLAYER -> current obligation routing companion + completeness/nonauthority law; recovery/catch-up/performance/downstream schema/test impact |
| F17-02 | mandatory pre-command collaboration-held clause + deterministic native release/handoff; no synthetic command/arrival anchor |
| F17-03 | immutable unitary accepted collaboration-relevant clause semantics |
| F17-04 | stable obligation lineage vs new obligation ID boundary |
| F17-05 | recipient-safe obligation projection / no input-ref disclosure grant |
| F17-06 | collection handoff/consumption semantics + partial-publication no-replay repair |

The selected Step-3 Alternative C may remain if all six repairs fit without changing its core owner allocation.

---

## 5. Step-6 gate

```text
STEP_6_BLOCKING:          2
STEP_6_SIGNIFICANT:       4
STEP_6_MINOR:             0
HUMAN_DECISION_REQUIRED:  NO
UPSTREAM_REOPEN_REQUIRED: NO
STEP_7_REQUIRED:          YES
WP18_STARTED:             NO
IMPLEMENTATION_PLANNING:  NO
```
