# Step 5.6 — Campaign Publication & Crash Consistency — Adversarial Review

Status: **ADVERSARIAL REVIEW — CANDIDATE NOT YET CANONICAL**

Date: 2026-08-20

Reviewed candidate:

- `2026-08-20-step-5-6-campaign-publication-crash-consistency-candidate-spec.md`

Primary-source evidence rechecked:

- GitHub REST Git references: non-force ref update requires a fast-forward update and returns explicit success/conflict/validation outcomes.
- GitHub REST Git trees: a created tree becomes branch-visible only after commit + branch ref update; `base_tree` preserves the current tree outside the supplied delta.
- GitHub compare-commits API provides bounded exact commit comparison/lineage evidence.
- OpenAI current Data Analysis documentation: ChatGPT's built-in Python environment cannot make external web/API requests.
- OpenAI current custom-app/MCP documentation: external write-capable integration is a separate host/app capability and is not equivalent to local Data Analysis Python networking.

Verdict:

> **PASS WITH REQUIRED REFINEMENTS; NO OWNER-LEVEL BLOCKER**

---

# 1. Finding AR-1 — ancestor proof must not itself authorize `saved`

Severity: **SIGNIFICANT**

Candidate LAW 5.6-17 correctly separates historical lineage from current compatibility, but wording elsewhere can still be read as if `C ancestor of D` proves the save itself is sufficiently complete.

Counterexample:

```text
H -> C   # intended save state
C -> D   # later valid transition supersedes one of C's values
```

Or, under unusual external history construction, C may become reachable through a merge while D's resulting tree does not preserve every exact C value.

Required refinement:

For ambiguity resolution, branch lineage answers only whether `C` is part of the current authoritative history. Player-facing/correctness success is determined by the **current required durable closure at D**.

Canonical rule:

```text
C == D
    -> exact intended commit currently selected
    -> evaluate required closure (normally immediate)

C ancestor of D
    -> C is durable lineage evidence
    -> inspect only D-vs-C paths/dependencies relevant to required closure
    -> if current D provides a compatible/superseding durable closure:
           publication promise may be confirmed
       else:
           conflict/revalidation required
```

Do not restore C merely to make acknowledgement simpler.

Disposition: **required canonical refinement**.

---

# 2. Finding AR-2 — ambiguity verification must not require unbounded history scan

Severity: **SIGNIFICANT**

An ancestry/reachability requirement could accidentally turn into an unbounded history traversal, violating bounded recovery/performance policy.

Required refinement:

`RepositoryPort` must provide bounded/server-side exact commit comparison/ancestry evidence where possible. The runtime must not clone/pull or walk arbitrary history in ordinary ambiguity recovery.

If backend cannot establish lineage within supported bounded evidence, outcome remains ambiguous/recovery-required rather than performing a campaign-wide history scan.

Disposition: **required canonical refinement**.

---

# 3. Finding AR-3 — successful non-force response proves ref selection only at that response point

Severity: **MODERATE**

Another writer may advance the branch immediately after our confirmed successful response but before local adoption.

This does not invalidate the save at C, but locally setting `known_head=C` can immediately be stale.

Required refinement:

Normal confirmed success may adopt C without redundant reread. `known_head=C` means **last known authoritative head produced/observed by this runtime**, not a lease asserting no later writer exists.

Before a later operation whose concurrency policy requires current campaign synchronization, normal ref probing rules apply.

No extra post-success read is added merely to close this theoretical race.

Disposition: **clarification**.

---

# 4. Finding AR-4 — same-ref atomicity requires complete result validation before tree creation

Severity: **SIGNIFICANT**

The candidate freezes path bytes and checks local invariants, but must explicitly forbid discovering mandatory companion paths only after remote tree preparation.

Examples:

- durable reference to new entity without index entry;
- CURRENT route to record not in resulting closure;
- checkpoint pointer without independently required checkpoint descriptor;
- newly enrolled recovery root without required routing evidence.

Required refinement:

Before first remote object mutation, local deterministic completeness must prove the planned **resulting tree state**, not merely each changed file independently.

If any required companion is discovered later, discard/rebuild the attempt. Prepared tree/object SHA is not patched into a second campaign publication.

Disposition: **required canonical refinement**.

---

# 5. Finding AR-5 — write-set normalization must preserve intentional deletions

Severity: **MODERATE**

A byte-equality/no-op normalization algorithm can reason about additions/updates but mishandle deletes.

Required refinement:

The normalized path delta has explicit operation semantics:

```text
UPSERT(path, exact content/blob)
DELETE(path)
```

Delete is a real mutation only when the base tree contains the path and owner policy authorizes deletion. Deleting an already-absent path is normalized away.

Deletion of a canonical owner must still satisfy lifecycle/reference/recovery rules; transport does not decide semantic deletion eligibility.

Disposition: **clarification**.

---

# 6. Finding AR-6 — commit creation after preflight must minimize the final race window

Severity: **LOW / PERFORMANCE-CORRECTNESS HYGIENE**

The preflight probe is not correctness authority, but unnecessary work between probe, commit creation and final ref update increases expected orphan conflicts.

Required refinement:

After final preflight/ref validation, perform only deterministic object finalization necessary to create the already-frozen single-parent commit and then attempt ref transition immediately. Do not run LLM calls, broad reads, semantic derivation or unrelated network work in this narrow phase.

Python ownership makes this feasible.

Disposition: **recommended canonical operational constraint**.

---

# 7. Finding AR-7 — a generic retry loop needs a bounded contention policy

Severity: **SIGNIFICANT**

Candidate says revalidate/rebuild/retry but does not explicitly forbid unlimited retries under active multiplayer contention.

An unbounded loop could monopolize latency and repeatedly create orphan objects.

Required refinement:

Python core SHALL use bounded automatic retries. Repeated movement/contention returns a typed synchronization/conflict outcome to the owning workflow rather than looping indefinitely.

Exact retry count/backoff is implementation/configuration policy, not Step-5.6 architecture.

For correctness-critical edge, the dependent edge remains unresolved. For local/private risk-control save, Step 5.5 friendly continuation semantics still apply.

Disposition: **required canonical refinement**.

---

# 8. Finding AR-8 — acting principal must be revalidated if authorization dependencies changed

Severity: **SIGNIFICANT**

Authorization was frozen at transaction start, but in multiplayer another commit may deactivate a PLAYER binding or change access/mode policy before final publication.

A purely disjoint world-path analysis would miss this.

Required refinement:

Authorization/ownership dependencies are mandatory members of the transaction dependency footprint. If campaign HEAD movement touches relevant PLAYER binding, mode, join policy or creator-only policy data, revalidate authorization before rebuild/publication.

The final Git credential succeeding is not sufficient application authorization.

Disposition: **required canonical refinement**.

---

# 9. Finding AR-9 — shared technical credential threatens commit-author-based legacy rules

Severity: **SIGNIFICANT IMPLEMENTATION/DEPLOYMENT DEBT**

The candidate records acting-principal requirements, but current runtime also derives campaign creator from Git history `author.login`.

A bridge that always commits as one bot/service identity could make new campaign creator discovery wrong even if application authorization was checked correctly.

Required refinement:

Canonical 5.6 should state:

- the repository bridge must preserve trustworthy audit/acting-principal evidence required by current access policy; and
- if the selected transport cannot preserve meaningful authenticated per-user Git authorship, machine realization must replace any rule that incorrectly treats technical commit author as the sole durable application principal, using an explicitly designed trusted alternative.

This is not permission to write arbitrary `author` metadata and trust it.

Exact identity representation may be finalized with access/deployment implementation after architecture.

Disposition: **recorded machine-realization blocker; no new product decision**.

---

# 10. Finding AR-10 — Python bridge availability is a real baseline deployment blocker

Severity: **HIGH DEPLOYMENT FEASIBILITY, NOT STEP-5.6 SEMANTIC BLOCKER**

Current official OpenAI documentation explicitly says built-in ChatGPT Data Analysis Python cannot perform external web/API requests. Therefore the already-approved owner constraint cannot be implemented by a local sandbox script alone in ordinary ChatGPT.

Required canonical disposition:

```text
Python core repository ownership remains mandatory.
A deployment profile claiming persistence must provide authenticated RepositoryPort.
Plain built-in Data Analysis Python alone does not satisfy it.
The bridge topology must be feasibility-tested before machine implementation/release.
```

This should be carried to Step 6 host/deployment feasibility and implementation planning.

Do not solve it by reverting to LLM Git tool calls.

Disposition: **explicit deferred blocker**.

---

# 11. Finding AR-11 — current runtime prose contains stale one-hour and LLM-transport assumptions

Severity: **EXPECTED MACHINE-REALIZATION DEBT**

`PERSISTENCE.md`, `STORAGE.md`, `SAVE_CONTRACT.md` already contain many good transport invariants but are written as runtime prose for an LLM-driven execution environment and still reference old one-hour durability semantics elsewhere.

Step 5.6 architecture should not partially rewrite GAME yet because later 5.7/5.8 still affect recovery/live integration.

Required disposition:

Record integrated implementation obligations:

- Python core becomes execution authority for repository operations;
- runtime Markdown becomes routing/contract documentation rather than imperative Git choreography for the LLM;
- stale one-hour assumptions are replaced by Step-5.5 scope policy;
- test suite moves from string-only expectations toward executable Python transaction/failure tests.

Disposition: **defer to integrated implementation after architecture**.

---

# 12. Finding AR-12 — current tests are insufficient for crash consistency

Severity: **SIGNIFICANT IMPLEMENTATION DEBT**

Existing PT/S save cases cover one tree/commit, no force, sparse checkpoint and no Base64, but not:

- lost ACK where C is current;
- lost ACK where current D descends from C;
- D changes required owners after C;
- C unreachable after rejected/failed update;
- process crash after remote success before dirty clearing;
- generation-specific dirty clearing;
- newer local generation surviving older publication;
- acting principal invalidated by concurrent access change;
- bounded automatic retry under contention;
- Python-only transport ownership;
- host RepositoryPort unavailable.

Canonical spec should enumerate these as mandatory future regression families.

Disposition: **required implementation test obligations**.

---

# 13. Finding AR-13 — multiple native domains need no publication order here

Severity: **SCOPE CHECK**

It is tempting for 5.6 to decide whether campaign or live domain publishes first in a multi-domain save/compaction.

That would steal Step-5.8 authority-transfer design.

Step 5.6 should only require:

- every domain publication uses its own authoritative protocol;
- partial success remains real;
- composed compatibility is revalidated;
- dependent edge remains incomplete until required closure holds;
- no rollback/distributed transaction.

Exact ordering/fencing/absorption remains 5.8.

Disposition: **scope preserved**.

---

# 14. Finding AR-14 — Git commit order remains non-fictional

Severity: **SCOPE CHECK**

A campaign commit created later in wall/Git order cannot automatically establish later fictional chronology.

Step 5.6 commit/ref ordering is storage causality only. Step 5.9 owns fictional chronology and reconciliation.

Conflict resolution must invoke domain/chronology semantics where simultaneous/contested actions require them rather than treating first Git publication as automatically fictionally earlier.

Disposition: **scope preserved**.

---

# 15. Failure matrix re-review

| Scenario | Result |
|---|---|
| clean save | NO_WRITE_NEEDED; no Git mutation |
| one dirty file | one base-tree transaction/commit |
| many dirty owners | one complete campaign commit |
| crash after tree | old ref authority; tree garbage only |
| crash after commit, before ref | old/current ref authority; C non-authoritative |
| ref race after preflight | non-force update rejects stale sibling C |
| confirmed ref rejection | no save ack; revalidate actual head |
| successful ref response | publication confirmed; no routine reread |
| lost response, current head C | verify exact selection; closure check |
| lost response, current head D with C ancestor | lineage evidence + targeted current-closure compatibility check |
| lost response, C not reachable | no current closure proof from C; rebuild/revalidate |
| success then local crash | remote source wins; no gameplay replay |
| remote disjoint change | transport-only rebuild allowed after footprint proof |
| remote dependency overlap | owner semantic revalidation required |
| later local generation after freeze | older generation may clear; newer remains dirty |
| repeated contention | bounded retry then typed conflict/sync outcome |
| campaign domain succeeds, other domain fails | campaign success remains real; composed promise incomplete |
| bridge unavailable | persistence capability unavailable; no LLM fallback |

No scenario requires force push, per-record campaign commits or persistent generic publication journal.

---

# 16. Review verdict

**PASS WITH REQUIRED REFINEMENTS.**

No owner-level decision is required before canonicalization because findings either:

- follow mechanically from already-approved Python ownership and Step-5.5 semantics;
- tighten failure-proof correctness;
- preserve previously accepted access/multiplayer authority boundaries; or
- identify explicit host/deployment prerequisites without selecting a new product tier/topology.

Canonical specification must incorporate AR-1 through AR-10 and record AR-11/AR-12 as implementation debt/verification obligations.
