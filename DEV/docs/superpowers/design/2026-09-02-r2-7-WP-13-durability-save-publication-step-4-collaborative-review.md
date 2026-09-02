# R2.7 WP-13 — Durability / SAVE / Publication — Step 4 Collaborative Review

Status: **STEP 4 COMPLETE — REFINEMENTS INCORPORATED FOR CANDIDATE DEVELOPMENT**

Date: 2026-09-02

Reviewed:

- repaired Step-1 package + SR13-01;
- Step-2 evidence/completeness record + Source Manifest expansion;
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-step-3-decision-brief.md`.

This review is advisory/pre-candidate. It does not rewrite accepted upstream architecture and does not start implementation.

---

## 1. Review dimensions

The Step-3 recommendation was reviewed against:

- authority ownership;
- native-domain composition;
- explicit SAVE semantics;
- scope/quiescence semantics;
- campaign publication atomicity;
- R2.6 fixed transport;
- currentness/conflict/ambiguity;
- generation-specific adoption;
- checkpoint/live/storage separation;
- access/acting-principal dependencies;
- boundedness/no-scan requirements;
- engine/rules maintenance consumer;
- failure and crash disposition;
- downstream WP boundaries.

The recommended Option A remains the only conforming candidate family.

---

## 2. Review findings and candidate refinements

### CR01 — Separate ref-transition epistemic outcome from operation result

Severity: **SIGNIFICANT FOR CANDIDATE PRECISION**

Step 3 grouped `NO_WRITE_NEEDED`, `CAPABILITY_FAILURE`, `REVALIDATION_REQUIRED` and accepted/rejected/indeterminate into one conceptual result vocabulary.

That is useful operationally but could obscure Step-5.6's narrower law:

```text
authority-changing final ref operation
    -> CONFIRMED_ACCEPTED | CONFIRMED_REJECTED | INDETERMINATE
```

Candidate refinement:

- keep **RefTransitionOutcome** epistemically exact for the final authority-changing operation;
- keep a broader **NativeDurabilityResult** for operation-level no-write/prepublication/capability/revalidation outcomes;
- never infer `CONFIRMED_REJECTED` from a capability failure that prevented dispatch.

Disposition: **INCORPORATE IN STEP 5**.

### CR02 — Cross-domain SAVE composition must not imply a global domain order

Severity: **SIGNIFICANT FOR CANDIDATE PRECISION**

A composite SAVE needs an execution plan, but Step 5.1/5.5 prohibit inventing one universal cross-domain total order.

Candidate refinement:

- domain ordering exists only where native dependency/authority transfer requires it;
- otherwise implementation may choose a safe deterministic operational order without assigning semantic chronology/dominance;
- partial success remains real in whatever legal order was used;
- live close/absorption ordering remains Step 5.8-owned.

Disposition: **INCORPORATE IN STEP 5**.

### CR03 — Scope-relative exposure support must track surviving relevant dirtiness, not a resettable scope clock

Severity: **SIGNIFICANT FOR CANDIDATE PRECISION**

Replacing `durable_frontier_time` with `scope_dirty_since` alone could still be wrong if the oldest generation becomes superseded while another older still-relevant generation remains, or if one sub-root publishes while another remains dirty.

Candidate refinement:

- architecture requires an evaluable **oldest still-relevant unpublished basis** for the policy scope;
- representation may be aggregate or per-owner, but must update from actual current dirty/recovery relevance;
- unrelated publication cannot reset the scope's still-relevant exposure basis;
- no exact numeric threshold is selected here.

Disposition: **INCORPORATE IN STEP 5**.

### CR04 — `NO_WRITE_NEEDED` is a closure result, not path-delta emptiness alone

Severity: **SIGNIFICANT FOR CANDIDATE PRECISION**

An empty campaign delta does not by itself prove an overall explicit SAVE when another native domain remains unresolved.

Candidate refinement:

- campaign `NO_WRITE_NEEDED` means campaign-domain portion requires no mutation and its required campaign source closure is already compatible/durable;
- overall SAVE succeeds only after every required native domain satisfies its own closure;
- no-write acknowledgement must still be based on known compatible authoritative evidence.

Disposition: **INCORPORATE IN STEP 5**.

### CR05 — Authorization/currentness dependencies must be revalidated at both rebuild and final mutation boundary as owned

Severity: **SIGNIFICANT FOR CANDIDATE PRECISION**

Step 3 freezes authorization basis but could be misread as granting a durable authorization snapshot.

Candidate refinement:

- frozen auth evidence is attempt input, not authority;
- mutable authorization/routing dependencies participate in conflict footprint;
- when owner/access policy requires fresh pre-mutation authorization, revalidate at that boundary;
- a rebuilt attempt on a new HEAD cannot reuse stale permission merely because semantics were disjoint.

Disposition: **INCORPORATE IN STEP 5**.

### CR06 — Engine/rules maintenance is a consumer, not an alternate publication owner

Severity: **MINOR / OWNERSHIP CLARITY**

Candidate refinement:

- campaign engine/rules provenance/adoption changes enter the same campaign-domain publication protocol only after their own owner authorizes the semantic delta;
- storage baseline remains a separate storage-owner transaction;
- WP-13 does not absorb migration compatibility or runtime-package selection.

Disposition: **INCORPORATE IN STEP 5**.

### CR07 — Prepared-object identities may aid ambiguity evidence but must not become durable attempt identity

Severity: **MINOR / AUTHORITY CLARITY**

Candidate refinement:

- intended commit C is exact evidence for one prepared campaign attempt and ambiguity verification;
- no persistent `attempt_id` or journal is required;
- crash before local adoption resolves from current repository/native authority, not from recovered attempt metadata.

Disposition: **INCORPORATE IN STEP 5**.

### CR08 — Bounded completeness must include DELETE-side index/routing effects

Severity: **SIGNIFICANT FOR WP-11 F02 COMPLETENESS**

Record+index closure is not only creation/update. Owner-valid deletion/retirement may require removal/update of derived discovery/routing projections in the same campaign transaction.

Candidate refinement:

- exact path delta includes owner-authorized UPSERT/DELETE plus every directly required derived index/projection companion;
- index absence never becomes semantic absence authority;
- cleanup/semantic retirement itself remains owner/WP-26/Step-5.13 territory as applicable.

Disposition: **INCORPORATE IN STEP 5**.

---

## 3. Non-findings / rejected scope expansion

The review found no basis to add:

- a persistent generic durability queue;
- a persistent publication journal;
- one global save frontier;
- a distributed transaction coordinator;
- a campaign-wide semantic lock;
- a new chronology order;
- checkpoint as SAVE proof;
- a transport alternative/fallback layer;
- a new gameplay authorization source;
- a generic repository merge engine;
- a new live authority model.

No external research is required.

---

## 4. Candidate acceptance criteria after review

Step 5 candidate must explicitly show:

1. owner-defined edge/root semantics feed shared machinery but stay owner-owned;
2. RRC closure and pending write set remain distinct;
3. composite SAVE has no global total order/distributed rollback;
4. `NO_WRITE_NEEDED` is domain-scoped and closure-proven;
5. campaign attempt freezes before remote object mutation;
6. exact Connector path is fixed and capability failure has no fallback;
7. final ref outcome uses exact accepted/rejected/indeterminate epistemics;
8. indeterminate result uses bounded current authority/lineage/current-closure verification;
9. currentness footprint includes reads, owner roots, auth/routing and recovery dependencies;
10. auth basis cannot become a stale permission lease;
11. WP-11 UPSERT/DELETE + required index/projection companions share campaign closure;
12. G-specific adoption preserves G+1;
13. oldest still-relevant unpublished exposure basis cannot be reset by unrelated publication;
14. checkpoint/live/storage/maintenance consumers remain inside their owner boundaries.

---

## 5. Step-4 disposition

```text
COLLABORATIVE_SIGNIFICANT_REFINEMENTS: 6
COLLABORATIVE_MINOR_REFINEMENTS:       2
UNRESOLVED_FOR_STEP_5:                 0
HUMAN_DECISION_REQUIRED:               NO
UPSTREAM_REOPEN_REQUIRED:              NO
STEP_5_MAY_PROCEED:                    YES
```

All findings are mechanical precision refinements within accepted architecture.